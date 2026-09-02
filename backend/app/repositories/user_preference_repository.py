from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_preference import UserPreference


class UserPreferenceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, preferences: UserPreference) -> UserPreference:
        self.db.add(preferences)
        self.db.flush()
        self.db.refresh(preferences)

        return preferences

    def get_by_user_id(
        self,
        user_id: UUID
    ) -> UserPreference | None:
        statement = select(UserPreference).where(
            UserPreference.user_id == user_id
        )

        return self.db.execute(statement).scalar_one_or_none()

    def update(
        self,
        preferences: UserPreference
    ) -> UserPreference:
        self.db.flush()
        self.db.refresh(preferences)

        return preferences

    def delete(self, preferences: UserPreference) -> None:
        self.db.delete(preferences)