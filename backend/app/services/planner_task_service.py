from uuid import UUID

from sqlalchemy.orm import Session

from app.models.planner_task import PlannerTask
from app.repositories.planner_task_repository import PlannerTaskRepository


class PlannerTaskService:
    def __init__(self, db: Session):
        self.repository = PlannerTaskRepository(db)

    def create_task(self, task: PlannerTask) -> PlannerTask:
        return self.repository.create(task)

    def get_task(self, task_id: UUID) -> PlannerTask | None:
        return self.repository.get_by_id(task_id)

    def get_user_tasks(self, user_id: UUID) -> list[PlannerTask]:
        return self.repository.get_by_user_id(user_id)

    def update_task(self, task: PlannerTask) -> PlannerTask:
        return self.repository.update(task)

    def delete_task(self, task: PlannerTask) -> None:
        self.repository.delete(task)