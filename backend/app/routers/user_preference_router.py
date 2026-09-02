from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user_preference import UserPreference
from app.schemas.user_preference_schema import (
    UserPreferenceCreate,
    UserPreferenceResponse,
)
from app.services.user_preference_service import UserPreferenceService


router = APIRouter(
    prefix="/users/{user_id}/preferences",
    tags=["User Preferences"],
)


@router.post(
    "/",
    response_model=UserPreferenceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_preferences(
    user_id: UUID,
    preference_data: UserPreferenceCreate,
    db: Session = Depends(get_db),
):
    service = UserPreferenceService(db)

    if preference_data.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID in path and request body must match",
        )

    preferences = UserPreference(
        user_id=preference_data.user_id,
        preferred_language=preference_data.preferred_language,
        response_style=preference_data.response_style,
        theme=preference_data.theme,
        timezone=preference_data.timezone,
    )

    try:
        return service.create_preferences(preferences)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )


@router.get(
    "/",
    response_model=UserPreferenceResponse,
)
def get_preferences(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    service = UserPreferenceService(db)

    preferences = service.get_preferences(user_id)

    if preferences is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found",
        )

    return preferences