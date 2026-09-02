from uuid import UUID

from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, db: Session):
        self.repository = MessageRepository(db)

    def create_message(self, message: Message) -> Message:
        return self.repository.create(message)

    def get_message(self, message_id: UUID) -> Message | None:
        return self.repository.get_by_id(message_id)

    def get_conversation_messages(
        self,
        conversation_id: UUID,
    ) -> list[Message]:
        return self.repository.get_by_conversation_id(conversation_id)

    def delete_message(self, message: Message) -> None:
        self.repository.delete(message)