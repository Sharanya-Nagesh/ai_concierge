from app.services.llm_provider import LLMProvider


class MockLLMProvider(LLMProvider):
    def generate_response(self, user_message: str) -> str:
        """
        Generate a temporary mock response.

        This provider is used during development and testing.
        """
        return f"Mock response to: {user_message}"