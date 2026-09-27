from sqlalchemy.orm import Session

from smart_journal.models import JournalEmbedding, JournalEntry


def search_similar_entries(
    db: Session,
    query_embedding: list[float],
    user_id: int,
    top_k: int = 5,
    similarity_threshold: float = 0.2,
):
    distance = JournalEmbedding.embedding.cosine_distance(query_embedding)

    results = (
        db.query(
            JournalEmbedding,
            JournalEntry,
            (1 - distance).label("similarity"),
        )
        .join(
            JournalEntry,
            JournalEntry.id == JournalEmbedding.journal_entry_id,
        )
        .filter(
            JournalEmbedding.user_id == user_id,
            JournalEntry.user_id == user_id,
            (1 - distance) >= similarity_threshold,
        )
        .order_by(distance)
        .limit(top_k)
        .all()
    )

    return [
        {
            "journal_entry_id": embedding.journal_entry_id,
            "title": journal.title,
            "content": journal.content,
            "similarity": float(similarity),
        }
        for embedding, journal, similarity in results
    ]