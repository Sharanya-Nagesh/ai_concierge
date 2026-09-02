from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.planner_task import PlannerTask


class PlannerTaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: PlannerTask) -> PlannerTask:
        self.db.add(task)
        self.db.flush()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: UUID) -> PlannerTask | None:
        statement = select(PlannerTask).where(PlannerTask.id == task_id)
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_user_id(self, user_id: UUID) -> list[PlannerTask]:
        statement = (
            select(PlannerTask)
            .where(PlannerTask.user_id == user_id)
            .order_by(PlannerTask.created_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())

    def update(self, task: PlannerTask) -> PlannerTask:
        self.db.flush()
        self.db.refresh(task)
        return task

    def delete(self, task: PlannerTask) -> None:
        self.db.delete(task)