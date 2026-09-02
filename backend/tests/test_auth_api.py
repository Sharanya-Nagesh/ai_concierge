from datetime import timedelta
from uuid import uuid4

from app.core.security import create_access_token


def test_register_user(client):
    email = f"register-{uuid4()}@example.com"

    payload = {
        "email": email,
        "full_name": "Register Test User",
        "password": "test-password-123",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == email
    assert data["full_name"] == payload["full_name"]
    assert data["role"] == "user"

    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_user(client):
    email = f"duplicate-auth-{uuid4()}@example.com"

    payload = {
        "email": email,
        "full_name": "Duplicate Auth User",
        "password": "test-password-123",
    }

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == (
        "A user with this email already exists"
    )


def test_login_success(client):
    email = f"login-{uuid4()}@example.com"
    password = "test-password-123"

    register_payload = {
        "email": email,
        "full_name": "Login Test User",
        "password": password,
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_payload = {
        "email": email,
        "password": password,
    }

    login_response = client.post(
        "/auth/login",
        json=login_payload,
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_wrong_password(client):
    email = f"wrong-password-{uuid4()}@example.com"
    password = "correct-password"

    register_payload = {
        "email": email,
        "full_name": "Wrong Password User",
        "password": password,
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_payload = {
        "email": email,
        "password": "wrong-password",
    }

    login_response = client.post(
        "/auth/login",
        json=login_payload,
    )

    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    email = f"nonexistent-{uuid4()}@example.com"

    login_payload = {
        "email": email,
        "password": "test-password-123",
    }

    response = client.post(
        "/auth/login",
        json=login_payload,
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_get_current_user_with_valid_token(client):
    email = f"current-user-{uuid4()}@example.com"
    password = "test-password-123"

    register_payload = {
        "email": email,
        "full_name": "Current User Test",
        "password": password,
    }

    register_response = client.post(
        "/auth/register",
        json=register_payload,
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email
    assert data["full_name"] == register_payload["full_name"]
    assert data["role"] == "user"
    assert "password_hash" not in data


def test_get_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"


def test_get_current_user_with_malformed_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "NotBearer some-token",
        },
    )

    assert response.status_code == 401
def test_get_current_user_with_expired_token(client):
    email = f"expired-token-{uuid4()}@example.com"
    password = "test-password-123"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": "Expired Token User",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    expired_token = create_access_token(
        data={
            "sub": register_response.json()["id"],
            "role": "user",
        },
        expires_delta=timedelta(minutes=-1),
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {expired_token}",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid or expired token"