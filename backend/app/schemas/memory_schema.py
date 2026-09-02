from uuid import UUID

from pydantic import BaseModel


class MemoryCreate(BaseModel):
    user_id: UUID
    memory_type: str
    content: str
    importance: float
    source: str
    embedding_id: str | None = None


class MemoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    memory_type: str
    content: str
    importance: float
    source: str
    embedding_id: str | None

    model_config = {
        "from_attributes": True
    }