from smart_journal.db.database import SessionLocal
from smart_journal.rag.service import RAGService


db = SessionLocal()

try:
    rag = RAGService(db)

    response = rag.answer_question(
        question="what is my favourite football team",
        user_id=6,
        top_k=5,
        similarity_threshold=0.3,
    )

    print("\nRAG RESPONSE:")
    print(response)

finally:
    db.close()
