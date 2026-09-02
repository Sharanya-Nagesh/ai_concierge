from uuid import UUID

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: UUID
    sender: str
    content: str
    model_name: str | None = None
    tokens_used: int | None = None


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    sender: str
    content: str
    model_name: str | None
    tokens_used: int | None

    model_config = {
        "from_attributes": True
    }