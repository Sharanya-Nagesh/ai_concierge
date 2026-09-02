from uuid import uuid4


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user(client):
    email = f"test-{uuid4()}@example.com"

    payload = {
        "email": email,
        "full_name": "Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == email
    assert data["full_name"] == payload["full_name"]
    assert "password_hash" not in data
    assert data["role"] == "user"


def test_create_duplicate_user(client):
    email = f"duplicate-{uuid4()}@example.com"

    payload = {
        "email": email,
        "full_name": "Duplicate User",
        "password_hash": "test-password-hash",
    }

    first_response = client.post("/users/", json=payload)
    second_response = client.post("/users/", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_get_user(client):
    email = f"getuser-{uuid4()}@example.com"

    payload = {
        "email": email,
        "full_name": "Get User",
        "password_hash": "test-password-hash",
    }

    create_response = client.post("/users/", json=payload)

    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["email"] == email
    assert data["full_name"] == payload["full_name"]
    assert "password_hash" not in data
    assert data["role"] == "user"


def test_get_nonexistent_user(client):
    user_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"