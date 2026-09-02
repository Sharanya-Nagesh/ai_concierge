from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.message import Message
from app.schemas.message_schema import MessageCreate, MessageResponse
from app.services.message_service import MessageService


router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post(
    "/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
):
    service = MessageService(db)

    message = Message(
        conversation_id=message_data.conversation_id,
        sender=message_data.sender,
        content=message_data.content,
        model_name=message_data.model_name,
        tokens_used=message_data.tokens_used,
    )

    return service.create_message(message)


@router.get(
    "/conversation/{conversation_id}",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    service = MessageService(db)

    return service.get_conversation_messages(conversation_id)


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
)
def get_message(
    message_id: UUID,
    db: Session = Depends(get_db),
):
    service = MessageService(db)

    message = service.get_message(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    return message


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_message(
    message_id: UUID,
    db: Session = Depends(get_db),
):
    service = MessageService(db)

    message = service.get_message(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    service.delete_message(message)