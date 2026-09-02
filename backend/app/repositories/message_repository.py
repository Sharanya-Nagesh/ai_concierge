from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.flush()
        self.db.refresh(message)

        return message

    def get_by_id(
        self,
        message_id: UUID
    ) -> Message | None:
        statement = select(Message).where(
            Message.id == message_id
        )

        return self.db.execute(statement).scalar_one_or_none()

    def get_by_conversation_id(
        self,
        conversation_id: UUID
    ) -> list[Message]:
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )

        return list(
            self.db.execute(statement).scalars().all()
        )

    def delete(self, message: Message) -> None:
        self.db.delete(message)