from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.memory import Memory
from app.schemas.memory_schema import MemoryCreate, MemoryResponse
from app.services.memory_service import MemoryService


router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)


@router.post(
    "/",
    response_model=MemoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_memory(
    memory_data: MemoryCreate,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memory = Memory(
        user_id=memory_data.user_id,
        memory_type=memory_data.memory_type,
        content=memory_data.content,
        importance=memory_data.importance,
        source=memory_data.source,
        embedding_id=memory_data.embedding_id,
    )

    return service.create_memory(memory)


@router.get(
    "/user/{user_id}",
    response_model=list[MemoryResponse],
)
def get_user_memories(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    return service.get_user_memories(user_id)


@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
)
def get_memory(
    memory_id: UUID,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memory = service.get_memory(memory_id)

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    return memory


@router.delete(
    "/{memory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_memory(
    memory_id: UUID,
    db: Session = Depends(get_db),
):
    service = MemoryService(db)

    memory = service.get_memory(memory_id)

    if memory is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Memory not found",
        )

    service.delete_memory(memory)