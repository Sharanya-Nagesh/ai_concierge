from uuid import UUID

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user: User) -> User:
        existing_user = self.repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        return self.repository.create(user)

    def get_user(self, user_id: UUID) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def delete_user(self, user: User) -> None:
        self.repository.delete(user)