
from abc import ABC, abstractmethod


class LLMProviderError(Exception):
    """Raised when an LLM provider fails."""
    pass


class LLMProvider(ABC):

    @abstractmethod
    def generate_response(
        self,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate an assistant response using conversation history.

        Each message contains:
        - role: user or assistant
        - content: message text
        """
        pass
