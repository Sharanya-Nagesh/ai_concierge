
import logging
import os

from openai import OpenAI, OpenAIError

from app.services.llm_provider import (
    LLMProvider,
    LLMProviderError,
)

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured"
            )

        if not model:
            raise RuntimeError(
                "OPENAI_MODEL is not configured"
            )

        self.client = OpenAI(
            api_key=api_key,
            timeout=30.0,
            max_retries=2,
        )

        self.model = model

    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:

        try:
            response = self.client.responses.create(
                model=self.model,
                input=messages,
            )

            answer = response.output_text

            if not answer or not answer.strip():
                raise LLMProviderError(
                    "The LLM returned an empty response"
                )

            return answer.strip()

        except OpenAIError as error:
            logger.exception(
                "OpenAI API request failed"
            )

            raise LLMProviderError(
                "Unable to generate a response currently"
            ) from error
