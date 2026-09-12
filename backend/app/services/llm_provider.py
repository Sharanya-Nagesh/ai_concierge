from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, user_message: str) -> str:
        """
        Generate an assistant response for a user message.
        """
        pass