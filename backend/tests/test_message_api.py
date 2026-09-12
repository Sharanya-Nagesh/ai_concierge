from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Message Test User",
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


def create_test_conversation(client, user):
    payload = {
        "user_id": user["id"],
        "title": "Test Conversation",
    }

    response = client.post(
        "/conversations/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def create_test_message(client, conversation_id, token):
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
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_message(client):
    user = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user,
    )

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
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
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
    user = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user,
    )

    message = create_test_message(
        client,
        conversation_id,
        user["token"],
    )

    message_id = message["id"]

    response = client.get(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == message_id
    assert data["conversation_id"] == conversation_id
    assert data["content"] == "This is a test message."


def test_get_conversation_messages(client):
    user = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user,
    )

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

    headers = {
        "Authorization": f"Bearer {user['token']}",
    }

    first_response = client.post(
        "/messages/",
        json=first_message,
        headers=headers,
    )

    second_response = client.post(
        "/messages/",
        json=second_message,
        headers=headers,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get(
        f"/messages/conversation/{conversation_id}",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["content"] == "First message"
    assert data[1]["content"] == "Second message"


def test_get_nonexistent_message(client):
    user = create_test_user(client)

    message_id = str(uuid4())

    response = client.get(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Message not found"


def test_delete_message(client):
    user = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user,
    )

    message = create_test_message(
        client,
        conversation_id,
        user["token"],
    )

    message_id = message["id"]

    response = client.delete(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert get_response.status_code == 404

def test_user_cannot_create_message_in_another_users_conversation(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user2,
    )

    payload = {
        "conversation_id": conversation_id,
        "sender": "user",
        "content": "Unauthorized message",
        "model_name": None,
        "tokens_used": None,
    }

    response = client.post(
        "/messages/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_message(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user2,
    )

    message = create_test_message(
        client,
        conversation_id,
        user2["token"],
    )

    message_id = message["id"]

    response = client.get(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_conversation_messages(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user2,
    )

    create_test_message(
        client,
        conversation_id,
        user2["token"],
    )

    response = client.get(
        f"/messages/conversation/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_delete_another_users_message(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation_id = create_test_conversation(
        client,
        user2,
    )

    message = create_test_message(
        client,
        conversation_id,
        user2["token"],
    )

    message_id = message["id"]

    response = client.delete(
        f"/messages/{message_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )