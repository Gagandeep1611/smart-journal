"""add journal embeddings

Revision ID: 1475c8563c3a
Revises: 63137ca8a92d
Create Date: 2026-09-27 16:16:45.923188

"""

from typing import Sequence, Union

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1475c8563c3a"
down_revision: Union[str, Sequence[str], None] = "63137ca8a92d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # The existing journal_embeddings table is legacy schema
    # and currently contains no data.
    op.drop_table("journal_embeddings")

    op.create_table(
        "journal_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("journal_entry_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("embedding", Vector(1536), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["journal_entry_id"],
            ["journal_entries.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("journal_entry_id"),
    )

    op.create_index(
        op.f("ix_journal_embeddings_journal_entry_id"),
        "journal_embeddings",
        ["journal_entry_id"],
        unique=True,
    )

    op.create_index(
        op.f("ix_journal_embeddings_user_id"),
        "journal_embeddings",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_journal_embeddings_user_id"),
        table_name="journal_embeddings",
    )

    op.drop_index(
        op.f("ix_journal_embeddings_journal_entry_id"),
        table_name="journal_embeddings",
    )

    op.drop_table("journal_embeddings")
