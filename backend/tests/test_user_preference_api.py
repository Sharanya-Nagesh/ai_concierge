from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Preference Test User",
        "password": password,
    }

    register_response = client.post(
        "/auth/register",
        json=payload,
    )

    assert register_response.status_code == 201

    user_id = register_response.json()["id"]

    login_response = client.post(
        "/auth/login",
        json={
            "email": payload["email"],
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "id": user_id,
        "token": token,
    }


def test_create_user_preferences(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    response = client.post(
        f"/users/{user['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user["id"]
    assert data["preferred_language"] == "English"
    assert data["response_style"] == "concise"
    assert data["theme"] == "light"
    assert data["timezone"] == "UTC"


def test_get_user_preferences(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "preferred_language": "English",
        "response_style": "detailed",
        "theme": "dark",
        "timezone": "UTC",
    }

    create_response = client.post(
        f"/users/{user['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/users/{user['id']}/preferences/",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user["id"]
    assert data["preferred_language"] == "English"
    assert data["response_style"] == "detailed"
    assert data["theme"] == "dark"
    assert data["timezone"] == "UTC"


def test_create_duplicate_user_preferences(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    first_response = client.post(
        f"/users/{user['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    second_response = client.post(
        f"/users/{user['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_create_preferences_with_mismatched_user_id(client):
    user = create_test_user(client)
    different_user_id = str(uuid4())

    payload = {
        "user_id": different_user_id,
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    response = client.post(
        f"/users/{user['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "User ID in path and request body must match"
    )


def test_get_nonexistent_user_preferences(client):
    user = create_test_user(client)
    nonexistent_user_id = str(uuid4())

    response = client.get(
        f"/users/{nonexistent_user_id}/preferences/",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_preferences_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    response = client.post(
        f"/users/{user2['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_preferences(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "preferred_language": "English",
        "response_style": "detailed",
        "theme": "dark",
        "timezone": "UTC",
    }

    create_response = client.post(
        f"/users/{user2['id']}/preferences/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user2['token']}",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/users/{user2['id']}/preferences/",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )