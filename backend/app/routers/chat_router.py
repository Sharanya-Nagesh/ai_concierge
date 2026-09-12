from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    chat_data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    try:
        conversation, assistant_response = service.chat(
            user_id=current_user.id,
            conversation_id=chat_data.conversation_id,
            user_message=chat_data.message,
        )

    except ValueError as error:
        error_message = str(error)

        if error_message == "Conversation not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message,
            )

        if (
            error_message
            == "You do not have access to this conversation"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=error_message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message,
        )

    return ChatResponse(
        conversation_id=conversation.id,
        user_message=chat_data.message,
        assistant_message=assistant_response,
    )