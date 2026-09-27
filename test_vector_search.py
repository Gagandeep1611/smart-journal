from smart_journal.db.database import SessionLocal
from smart_journal.embeddings.factory import get_embedding_provider
from smart_journal.services.vector_service import search_similar_entries


db = SessionLocal()

try:
    provider = get_embedding_provider()

    query = "What did I work on in spring boot"

    query_embedding = provider.generate_embedding(query)

    results = search_similar_entries(
        db=db,
        query_embedding=query_embedding,
        user_id=7,
        top_k=5,
        similarity_threshold=0.0,
    )

    print("\nRetrieved entries:")

    for result in results:
        print(result)

finally:
    db.close()