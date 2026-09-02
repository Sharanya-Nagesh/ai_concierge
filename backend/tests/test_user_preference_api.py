from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Preference Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def test_create_user_preferences(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    response = client.post(
        f"/users/{user_id}/preferences/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["preferred_language"] == "English"
    assert data["response_style"] == "concise"
    assert data["theme"] == "light"
    assert data["timezone"] == "UTC"


def test_get_user_preferences(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "preferred_language": "English",
        "response_style": "detailed",
        "theme": "dark",
        "timezone": "UTC",
    }

    create_response = client.post(
        f"/users/{user_id}/preferences/",
        json=payload,
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/users/{user_id}/preferences/"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == user_id
    assert data["preferred_language"] == "English"
    assert data["response_style"] == "detailed"
    assert data["theme"] == "dark"
    assert data["timezone"] == "UTC"


def test_create_duplicate_user_preferences(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    first_response = client.post(
        f"/users/{user_id}/preferences/",
        json=payload,
    )

    second_response = client.post(
        f"/users/{user_id}/preferences/",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_create_preferences_with_mismatched_user_id(client):
    user_id = create_test_user(client)
    different_user_id = str(uuid4())

    payload = {
        "user_id": different_user_id,
        "preferred_language": "English",
        "response_style": "concise",
        "theme": "light",
        "timezone": "UTC",
    }

    response = client.post(
        f"/users/{user_id}/preferences/",
        json=payload,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "User ID in path and request body must match"
    )


def test_get_nonexistent_user_preferences(client):
    user_id = str(uuid4())

    response = client.get(
        f"/users/{user_id}/preferences/"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User preferences not found"