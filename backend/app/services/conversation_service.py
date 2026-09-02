from uuid import UUID

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, db: Session):
        self.repository = ConversationRepository(db)

    def create_conversation(
        self,
        conversation: Conversation,
    ) -> Conversation:
        return self.repository.create(conversation)

    def get_conversation(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        return self.repository.get_by_id(conversation_id)

    def get_user_conversations(
        self,
        user_id: UUID,
    ) -> list[Conversation]:
        return self.repository.get_by_user_id(user_id)

    def delete_conversation(
        self,
        conversation: Conversation,
    ) -> None:
        self.repository.delete(conversation)