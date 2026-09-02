from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.planner_task import PlannerTask
from app.schemas.planner_task_schema import (
    PlannerTaskCreate,
    PlannerTaskResponse,
)
from app.services.planner_task_service import PlannerTaskService


router = APIRouter(
    prefix="/planner-tasks",
    tags=["Planner Tasks"],
)


@router.post(
    "/",
    response_model=PlannerTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task_data: PlannerTaskCreate,
    db: Session = Depends(get_db),
):
    service = PlannerTaskService(db)

    task = PlannerTask(
        user_id=task_data.user_id,
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        priority=task_data.priority,
        status=task_data.status,
    )

    return service.create_task(task)


@router.get(
    "/user/{user_id}",
    response_model=list[PlannerTaskResponse],
)
def get_user_tasks(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    service = PlannerTaskService(db)

    return service.get_user_tasks(user_id)


@router.get(
    "/{task_id}",
    response_model=PlannerTaskResponse,
)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    service = PlannerTaskService(db)

    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planner task not found",
        )

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db),
):
    service = PlannerTaskService(db)

    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planner task not found",
        )

    service.delete_task(task)