from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    conversation_id: UUID | None = None
    message: str = Field(..., min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    conversation_id: UUID
    user_message: str
    assistant_message: str