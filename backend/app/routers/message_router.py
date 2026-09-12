from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_user_ownership
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message_schema import MessageCreate, MessageResponse
from app.services.conversation_service import ConversationService
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
    current_user: User = Depends(get_current_user),
):
    conversation_service = ConversationService(db)

    conversation = conversation_service.get_conversation(
        message_data.conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    require_user_ownership(
        current_user_id=current_user.id,
        requested_user_id=conversation.user_id,
    )

    message_service = MessageService(db)

    message = Message(
        conversation_id=message_data.conversation_id,
        sender=message_data.sender,
        content=message_data.content,
        model_name=message_data.model_name,
        tokens_used=message_data.tokens_used,
    )

    return message_service.create_message(message)


@router.get(
    "/conversation/{conversation_id}",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation_service = ConversationService(db)

    conversation = conversation_service.get_conversation(
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    require_user_ownership(
        current_user_id=current_user.id,
        requested_user_id=conversation.user_id,
    )

    message_service = MessageService(db)

    return message_service.get_conversation_messages(
        conversation_id
    )


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
)
def get_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message_service = MessageService(db)

    message = message_service.get_message(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    conversation_service = ConversationService(db)

    conversation = conversation_service.get_conversation(
        message.conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    require_user_ownership(
        current_user_id=current_user.id,
        requested_user_id=conversation.user_id,
    )

    return message


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message_service = MessageService(db)

    message = message_service.get_message(message_id)

    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    conversation_service = ConversationService(db)

    conversation = conversation_service.get_conversation(
        message.conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    require_user_ownership(
        current_user_id=current_user.id,
        requested_user_id=conversation.user_id,
    )

    message_service.delete_message(message)