from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.core.authorization import require_user_ownership


def test_user_can_access_own_resource():
    user_id = uuid4()

    require_user_ownership(
        current_user_id=user_id,
        requested_user_id=user_id,
    )


def test_user_cannot_access_another_users_resource():
    current_user_id = uuid4()
    requested_user_id = uuid4()

    with pytest.raises(HTTPException) as error:
        require_user_ownership(
            current_user_id=current_user_id,
            requested_user_id=requested_user_id,
        )

    assert error.value.status_code == 403
    assert error.value.detail == (
        "You do not have access to this user's resources"
    )