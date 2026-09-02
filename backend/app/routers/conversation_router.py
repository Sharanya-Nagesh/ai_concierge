from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.conversation import Conversation
from app.schemas.conversation_schema import (
    ConversationCreate,
    ConversationResponse,
)
from app.services.conversation_service import ConversationService


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "/",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    conversation = Conversation(
        user_id=conversation_data.user_id,
        title=conversation_data.title,
    )

    return service.create_conversation(conversation)


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    conversation = service.get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return conversation


@router.get(
    "/user/{user_id}",
    response_model=list[ConversationResponse],
)
def get_user_conversations(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    return service.get_user_conversations(user_id)


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
):
    service = ConversationService(db)

    conversation = service.get_conversation(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    service.delete_conversation(conversation)