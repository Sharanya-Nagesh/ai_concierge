
import os

from app.services.llm_provider import LLMProvider
from app.services.mock_llm_provider import MockLLMProvider
from app.services.openai_provider import OpenAIProvider


class LLMService:

    def __init__(self, provider: LLMProvider | None = None):

        if provider is not None:
            self.provider = provider
            return

        provider_name = os.getenv(
            "LLM_PROVIDER",
            "mock"
        ).strip().lower()

        if provider_name == "mock":
            self.provider = MockLLMProvider()

        elif provider_name == "openai":
            self.provider = OpenAIProvider()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider_name}"
            )

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        return self.provider.generate_response(messages)
