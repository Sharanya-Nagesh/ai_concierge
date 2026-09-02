from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Conversation Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_conversation(client, user_id):
    payload = {
        "user_id": user_id,
        "title": "Test Conversation",
    }

    response = client.post(
        "/conversations/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_create_conversation(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "title": "Test Conversation",
    }

    response = client.post(
        "/conversations/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["title"] == payload["title"]


def test_get_conversation(client):
    user_id = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user_id,
    )

    conversation_id = conversation["id"]

    response = client.get(
        f"/conversations/{conversation_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == conversation_id
    assert data["user_id"] == user_id
    assert data["title"] == "Test Conversation"


def test_get_user_conversations(client):
    user_id = create_test_user(client)

    create_test_conversation(client, user_id)

    second_payload = {
        "user_id": user_id,
        "title": "Second Conversation",
    }

    second_response = client.post(
        "/conversations/",
        json=second_payload,
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/conversations/user/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(item["user_id"] == user_id for item in data)


def test_get_nonexistent_conversation(client):
    conversation_id = str(uuid4())

    response = client.get(
        f"/conversations/{conversation_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_delete_conversation(client):
    user_id = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user_id,
    )

    conversation_id = conversation["id"]

    response = client.delete(
        f"/conversations/{conversation_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/conversations/{conversation_id}"
    )

    assert get_response.status_code == 404