import os

from openai import OpenAI

from app.services.llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured"
            )

        self.client = OpenAI(api_key=api_key)

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-luna",
        )

    def generate_response(self, user_message: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=user_message,
        )

        return response.output_text