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

            # Make sure the conversation belongs to the user
            if conversation.user_id != user_id:
                raise ValueError(
                    "You do not have access to this conversation"
                )

        # 2. Store the user's message
        user_message_record = Message(
            conversation_id=conversation.id,
            sender="user",
            content=user_message,
        )

        self.message_service.create_message(
            user_message_record
        )

        # 3. Generate assistant response
        assistant_response = (
            self.llm_service.generate_response(
                user_message
            )
        )

        # 4. Store the assistant's message
        assistant_message_record = Message(
            conversation_id=conversation.id,
            sender="assistant",
            content=assistant_response,
        )

        self.message_service.create_message(
            assistant_message_record
        )

        # 5. Return conversation and assistant response
        return conversation, assistant_response