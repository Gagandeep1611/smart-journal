from smart_journal.core.config import settings
from smart_journal.llm.base import LLMProvider
from smart_journal.llm.ollama import OllamaLLMProvider
from smart_journal.llm.openrouter import OpenRouterLLMProvider


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower()

    if provider == "ollama":
        return OllamaLLMProvider()

    if provider == "openrouter":
        return OpenRouterLLMProvider()

    raise ValueError(f"Unsupported LLM provider: {provider}")
