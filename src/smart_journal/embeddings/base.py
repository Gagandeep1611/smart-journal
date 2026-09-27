from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):

    @abstractmethod
    def generate_embedding(self, text: str) -> list[float]:
        """Generate an embedding vector for the given text."""
        raise NotImplementedError