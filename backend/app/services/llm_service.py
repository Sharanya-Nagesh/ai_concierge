from app.services.llm_provider import LLMProvider
from app.services.mock_llm_provider import MockLLMProvider


class LLMService:
    def __init__(self, provider: LLMProvider | None = None):
        self.provider = provider or MockLLMProvider()

    def generate_response(self, user_message: str) -> str:
        return self.provider.generate_response(user_message)