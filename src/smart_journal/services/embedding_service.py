from smart_journal.embeddings.factory import get_embedding_provider


def generate_embedding(text: str) -> list[float]:
    provider = get_embedding_provider()
    return provider.generate_embedding(text)