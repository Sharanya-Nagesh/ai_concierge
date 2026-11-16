
import os
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.message_service import MessageService


class ChatService:

    def __init__(self, db: Session):
        self.db = db
        self.conversation_service = ConversationService(db)
        self.message_service = MessageService(db)
        self.llm_service = LLMService()

        self.context_max_messages = int(
            os.getenv("LLM_CONTEXT_MAX_MESSAGES", "20")
        )

        if self.context_max_messages < 1:
            raise ValueError(
                "LLM_CONTEXT_MAX_MESSAGES must be at least 1"
            )

    def _build_conversation_context(
        self,
        conversation_history: list[Message],
    ) -> list[dict[str, str]]:

        # Keep only the most recent messages
        recent_messages = conversation_history[
            -self.context_max_messages:
        ]

        messages = []

        for message in recent_messages:

            role = (
                message.sender.value
                if hasattr(message.sender, "value")
                else str(message.sender)
            )

            messages.append({
                "role": role,
                "content": message.content,
            })

        # Avoid starting context with an assistant response
        if messages and messages[0]["role"] == "assistant":
            messages.pop(0)

        return messages

    def chat(
        self,
        user_id: UUID,
        conversation_id: UUID | None,
        user_message: str,
    ):

        # 1. Get existing conversation or create a new one
        if conversation_id is None:

            conversation = Conversation(
                user_id=user_id,
                title=user_message[:50],
            )

            conversation = (
                self.conversation_service.create_conversation(
                    conversation
                )
            )

        else:

            conversation = (
                self.conversation_service.get_conversation(
                    conversation_id
                )
            )

            if conversation is None:
                raise ValueError("Conversation not found")

            if conversation.user_id != user_id:
                raise ValueError(
                    "You do not have access to this conversation"
                )

        # 2. Store the current user message
        user_message_record = Message(
            conversation_id=conversation.id,
            sender="user",
            content=user_message,
        )

        self.message_service.create_message(
            user_message_record
        )

        # 3. Retrieve conversation history
        conversation_history = (
            self.message_service.get_conversation_messages(
                conversation.id
            )
        )

        # 4. Build limited conversation context
        messages = self._build_conversation_context(
            conversation_history
        )

        # 5. Generate response
        assistant_response = (
            self.llm_service.generate_response(messages)
        )

        # 6. Store assistant response
        assistant_message_record = Message(
            conversation_id=conversation.id,
            sender="assistant",
            content=assistant_response,
        )

        self.message_service.create_message(
            assistant_message_record
        )

        return conversation, assistant_response
