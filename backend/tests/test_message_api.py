from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Message Test User",
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

    return response.json()["id"]


def create_test_message(client, conversation_id):
    payload = {
        "conversation_id": conversation_id,
        "sender": "user",
        "content": "This is a test message.",
        "model_name": None,
        "tokens_used": None,
    }

    response = client.post(
        "/messages/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_create_message(client):
    user_id = create_test_user(client)
    conversation_id = create_test_conversation(client, user_id)

    payload = {
        "conversation_id": conversation_id,
        "sender": "user",
        "content": "Hello, this is a test.",
        "model_name": None,
        "tokens_used": None,
    }

    response = client.post(
        "/messages/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["conversation_id"] == conversation_id
    assert data["sender"] == "user"
    assert data["content"] == payload["content"]
    assert data["model_name"] is None
    assert data["tokens_used"] is None


def test_get_message(client):
    user_id = create_test_user(client)
    conversation_id = create_test_conversation(client, user_id)

    message = create_test_message(
        client,
        conversation_id,
    )

    message_id = message["id"]

    response = client.get(
        f"/messages/{message_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == message_id
    assert data["conversation_id"] == conversation_id
    assert data["content"] == "This is a test message."


def test_get_conversation_messages(client):
    user_id = create_test_user(client)
    conversation_id = create_test_conversation(client, user_id)

    first_message = {
        "conversation_id": conversation_id,
        "sender": "user",
        "content": "First message",
        "model_name": None,
        "tokens_used": None,
    }

    second_message = {
        "conversation_id": conversation_id,
        "sender": "assistant",
        "content": "Second message",
        "model_name": "test-model",
        "tokens_used": 10,
    }

    first_response = client.post(
        "/messages/",
        json=first_message,
    )

    second_response = client.post(
        "/messages/",
        json=second_message,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get(
        f"/messages/conversation/{conversation_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["content"] == "First message"
    assert data[1]["content"] == "Second message"


def test_get_nonexistent_message(client):
    message_id = str(uuid4())

    response = client.get(
        f"/messages/{message_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_delete_message(client):
    user_id = create_test_user(client)
    conversation_id = create_test_conversation(client, user_id)

    message = create_test_message(
        client,
        conversation_id,
    )

    message_id = message["id"]

    response = client.delete(
        f"/messages/{message_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/messages/{message_id}"
    )

    assert get_response.status_code == 404