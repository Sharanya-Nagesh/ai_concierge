from uuid import UUID

from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.repositories.memory_repository import MemoryRepository


class MemoryService:
    def __init__(self, db: Session):
        self.repository = MemoryRepository(db)

    def create_memory(self, memory: Memory) -> Memory:
        return self.repository.create(memory)

    def get_memory(self, memory_id: UUID) -> Memory | None:
        return self.repository.get_by_id(memory_id)

    def get_user_memories(self, user_id: UUID) -> list[Memory]:
        return self.repository.get_by_user_id(user_id)

    def update_memory(self, memory: Memory) -> Memory:
        return self.repository.update(memory)

    def delete_memory(self, memory: Memory) -> None:
        self.repository.delete(memory)