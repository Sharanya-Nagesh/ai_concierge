from uuid import UUID

from pydantic import BaseModel


class UserPreferenceCreate(BaseModel):
    user_id: UUID
    preferred_language: str
    response_style: str
    theme: str
    timezone: str


class UserPreferenceResponse(BaseModel):
    id: UUID
    user_id: UUID
    preferred_language: str
    response_style: str
    theme: str
    timezone: str

    model_config = {
        "from_attributes": True
    }