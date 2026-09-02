from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.memory import Memory


class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, memory: Memory) -> Memory:
        self.db.add(memory)
        self.db.flush()
        self.db.refresh(memory)
        return memory

    def get_by_id(self, memory_id: UUID) -> Memory | None:
        statement = select(Memory).where(Memory.id == memory_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID) -> list[Memory]:
        statement = (
            select(Memory)
            .where(Memory.user_id == user_id)
            .order_by(Memory.created_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())

    def update(self, memory: Memory) -> Memory:
        self.db.flush()
        self.db.refresh(memory)
        return memory

    def delete(self, memory: Memory) -> None:
        self.db.delete(memory)