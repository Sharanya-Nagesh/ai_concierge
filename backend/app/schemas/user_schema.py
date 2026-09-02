from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password_hash: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str

    model_config = {
        "from_attributes": True
    }