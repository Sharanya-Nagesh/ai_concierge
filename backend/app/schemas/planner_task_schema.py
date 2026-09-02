from datetime import date
from uuid import UUID

from pydantic import BaseModel


class PlannerTaskCreate(BaseModel):
    user_id: UUID
    title: str
    description: str | None = None
    due_date: date | None = None
    priority: str
    status: str


class PlannerTaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    due_date: date | None
    priority: str
    status: str

    model_config = {
        "from_attributes": True
    }
