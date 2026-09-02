from uuid import UUID

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    user_id: UUID
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    page_count: int | None = None
    upload_status: str
    storage_path: str


class DocumentResponse(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    page_count: int | None
    upload_status: str
    storage_path: str

    model_config = {
        "from_attributes": True
    }