from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from smart_journal.db.database import Base


class JournalEmbedding(Base):
    __tablename__ = "journal_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)

    journal_entry_id: Mapped[int] = mapped_column(
        ForeignKey("journal_entries.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    embedding = mapped_column(
        Vector(1536),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    journal_entry = relationship(
        "JournalEntry",
        back_populates="embedding",
    )
