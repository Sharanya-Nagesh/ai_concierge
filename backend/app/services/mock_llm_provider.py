
from app.services.llm_provider import LLMProvider


class MockLLMProvider(LLMProvider):

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        user_message = messages[-1]["content"]

        return f"Mock response to: {user_message}"
