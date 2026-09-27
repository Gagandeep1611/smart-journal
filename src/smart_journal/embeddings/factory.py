from smart_journal.core.config import settings
from smart_journal.embeddings.base import EmbeddingProvider
from smart_journal.embeddings.openai import OpenAIEmbeddingProvider


def get_embedding_provider() -> EmbeddingProvider:
    provider = settings.embedding_provider.lower()

    if provider == "openai":
        return OpenAIEmbeddingProvider()

    raise ValueError(f"Unsupported embedding provider: {provider}")