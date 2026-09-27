"""remove redundant journal embedding index

Revision ID: 104f9e256227
Revises: 1475c8563c3a
"""

from typing import Sequence, Union

from alembic import op


revision: str = "104f9e256227"
down_revision: Union[str, Sequence[str], None] = "1475c8563c3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(
        "ix_journal_embeddings_journal_entry_id",
        table_name="journal_embeddings",
    )


def downgrade() -> None:
    op.create_index(
        "ix_journal_embeddings_journal_entry_id",
        "journal_embeddings",
        ["journal_entry_id"],
        unique=True,
    )