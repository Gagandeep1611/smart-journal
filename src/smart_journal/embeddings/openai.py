from openai import OpenAI

from smart_journal.core.config import settings
from smart_journal.embeddings.base import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):

    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.embedding_base_url,
            api_key=settings.embedding_api_key,
        )
        self.model = settings.embedding_model

    def generate_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
