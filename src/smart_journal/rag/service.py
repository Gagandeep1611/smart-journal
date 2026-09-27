import logging

from sqlalchemy.orm import Session

from smart_journal.llm.factory import get_llm_provider
from smart_journal.services.embedding_service import generate_embedding
from smart_journal.services.vector_service import search_similar_entries

logger = logging.getLogger(__name__)
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


class RAGService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_provider = get_llm_provider()

    def answer_question(
        self,
        question: str,
        user_id: int,
        top_k: int = 3,
        similarity_threshold: float = 0.2,
    ) -> dict:
        """
        Execute the complete RAG pipeline for one authenticated user.
        """

        logger.info(
            "RAG request started: user_id=%s, question=%r",
            user_id,
            question,
        )

        # ---------------------------------------------------------
        # 1. Generate embedding for the user's question
        # ---------------------------------------------------------
        try:
            query_embedding = generate_embedding(question)

            logger.info(
                "Question embedding generated: user_id=%s, dimensions=%s",
                user_id,
                len(query_embedding),
            )

        except Exception:
            logger.exception(
                "Failed to generate question embedding: user_id=%s",
                user_id,
            )
            raise

        # ---------------------------------------------------------
        # 2. User-scoped vector retrieval
        # ---------------------------------------------------------
        try:
            results = search_similar_entries(
                db=self.db,
                query_embedding=query_embedding,
                user_id=user_id,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
            )

            logger.info(
                "Vector retrieval completed: user_id=%s, results=%s, "
                "top_k=%s, threshold=%s",
                user_id,
                len(results),
                top_k,
                similarity_threshold,
            )

        except Exception:
            logger.exception(
                "Vector retrieval failed: user_id=%s",
                user_id,
            )
            raise

        # ---------------------------------------------------------
        # 3. Handle no relevant context
        # ---------------------------------------------------------
        if not results:
            logger.info(
                "No relevant journal entries found: user_id=%s",
                user_id,
            )

            return {
                "answer": (
                    "I couldn't find any relevant information in your "
                    "journal to answer that question."
                ),
                "sources": [],
            }

        # ---------------------------------------------------------
        # 4. Build context
        # ---------------------------------------------------------
        context = self._build_context(results)

        # ---------------------------------------------------------
        # 5. Construct RAG prompt
        # ---------------------------------------------------------
        prompt = self._build_prompt(
            question=question,
            context=context,
        )

        logger.info(
            "RAG prompt constructed: user_id=%s, context_entries=%s",
            user_id,
            len(results),
        )

        # ---------------------------------------------------------
        # 6. Send prompt to LLM abstraction
        # ---------------------------------------------------------
        try:
            answer = self.llm_provider.generate(prompt)

            logger.info(
                "LLM response generated: user_id=%s",
                user_id,
            )

            sources = [
                {
                    "journal_entry_id": result["journal_entry_id"],
                    "title": result["title"],
                    "created_at": result["created_at"],
                }
                for result in results
            ]

            return {
                "answer": answer,
                "sources": sources,
            }

        except Exception:
            logger.exception(
                "LLM generation failed: user_id=%s",
                user_id,
            )
            raise

    @staticmethod
    def _build_context(results: list[dict]) -> str:
        """
        Convert retrieved journal entries into LLM context.
        """

        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(f"""Journal Entry {index}
                Title: {result["title"]}
                Content: {result["content"]}
                Similarity: {result["similarity"]:.4f}
                """)

        return "\n".join(context_parts)

    @staticmethod
    def _build_prompt(
        question: str,
        context: str,
    ) -> str:
        """
        Construct the prompt that constrains the LLM to journal context.
        """

        return f"""You are a personal journal assistant.

Answer the user's question using ONLY the journal entries provided below.

If the journal entries do not contain enough information to answer the
question, clearly say that you could not find the answer in the user's
journal.

Do not invent facts.
Do not assume personal information.
Do not use information outside the provided journal entries.

Journal entries:
----------------
{context}
----------------

User question:
{question}

Answer:
"""
