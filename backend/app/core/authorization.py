from uuid import UUID

from fastapi import HTTPException, status


def require_user_ownership(
    current_user_id: UUID,
    requested_user_id: UUID,
) -> None:
    if current_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this user's resources",
        )