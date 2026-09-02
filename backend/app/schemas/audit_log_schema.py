from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class AuditLogCreate(BaseModel):
    user_id: UUID | None = None
    action: str
    entity_type: str
    entity_id: UUID | None = None
    metadata: dict[str, Any] | None = None


class AuditLogResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    action: str
    entity_type: str
    entity_id: UUID | None
    metadata: dict[str, Any] | None = Field(
        default=None,
        validation_alias="metadata_",
        serialization_alias="metadata",
    )
    created_at: datetime

    model_config = {
        "from_attributes": True
    }