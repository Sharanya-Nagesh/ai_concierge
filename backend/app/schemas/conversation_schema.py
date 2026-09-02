from uuid import UUID

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    user_id: UUID
    title: str


class ConversationResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str

    model_config = {
        "from_attributes": True
    }