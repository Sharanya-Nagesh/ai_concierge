from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(
        self,
        email: str,
        full_name: str,
        password: str,
    ) -> User:
        """
        Register a new user.

        Raises:
            ValueError: If a user with the email already exists.
        """
        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise ValueError("A user with this email already exists")

        password_hash = hash_password(password)

        user = User(
            email=email,
            full_name=full_name,
            password_hash=password_hash,
        )

        return self.user_repository.create(user)

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:
        """
        Verify user credentials.

        Returns:
            User if credentials are valid.
            None otherwise.
        """
        user = self.user_repository.get_by_email(email)

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

    def create_user_token(self, user: User) -> str:
        """
        Create an access token for an authenticated user.
        """
        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "role": user.role,
            },
            expires_delta=access_token_expires,
        )

        return access_token