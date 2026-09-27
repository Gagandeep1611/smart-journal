from openai import OpenAI

from smart_journal.core.config import settings
from smart_journal.llm.base import LLMProvider


class OllamaLLMProvider(LLMProvider):

    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key or "ollama",
        )
        self.model = settings.llm_model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""
