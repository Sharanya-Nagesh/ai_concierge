from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        self.db.flush()
        self.db.refresh(conversation)

        return conversation

    def get_by_id(
        self,
        conversation_id: UUID
    ) -> Conversation | None:
        statement = select(Conversation).where(
            Conversation.id == conversation_id
        )

        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(
        self,
        user_id: UUID
    ) -> list[Conversation]:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
        )

        return list(self.db.execute(statement).scalars().all())

    def delete(self, conversation: Conversation) -> None:
        self.db.delete(conversation)