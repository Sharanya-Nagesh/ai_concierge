from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user_preference import UserPreference
from app.repositories.user_preference_repository import UserPreferenceRepository


class UserPreferenceService:
    def __init__(self, db: Session):
        self.repository = UserPreferenceRepository(db)

    def create_preferences(
        self,
        preferences: UserPreference,
    ) -> UserPreference:
        existing_preferences = self.repository.get_by_user_id(
            preferences.user_id
        )

        if existing_preferences:
            raise ValueError("User preferences already exist")

        return self.repository.create(preferences)

    def get_preferences(
        self,
        user_id: UUID,
    ) -> UserPreference | None:
        return self.repository.get_by_user_id(user_id)

    def update_preferences(
        self,
        preferences: UserPreference,
    ) -> UserPreference:
        return self.repository.update(preferences)

    def delete_preferences(
        self,
        preferences: UserPreference,
    ) -> None:
        self.repository.delete(preferences)