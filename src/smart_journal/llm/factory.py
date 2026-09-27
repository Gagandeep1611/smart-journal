from smart_journal.core.config import settings
from smart_journal.llm.base import LLMProvider
from smart_journal.llm.openai import OpenAILLMProvider
from smart_journal.llm.ollama import OllamaLLMProvider


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return OpenAILLMProvider()

    if provider == "ollama":
        return OllamaLLMProvider()

    raise ValueError(f"Unsupported LLM provider: {provider}")