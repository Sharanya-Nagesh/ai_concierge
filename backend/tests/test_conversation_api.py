from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Conversation Test User",
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

    return response.json()


def test_create_conversation(client):
    user = create_test_user(client)

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

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user["id"]
    assert data["title"] == payload["title"]


def test_get_conversation(client):
    user = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user,
    )

    conversation_id = conversation["id"]

    response = client.get(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == conversation_id
    assert data["user_id"] == user["id"]
    assert data["title"] == "Test Conversation"


def test_get_user_conversations(client):
    user = create_test_user(client)

    create_test_conversation(
        client,
        user,
    )

    second_payload = {
        "user_id": user["id"],
        "title": "Second Conversation",
    }

    second_response = client.post(
        "/conversations/",
        json=second_payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/conversations/user/{user['id']}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(
        item["user_id"] == user["id"]
        for item in data
    )


def test_get_nonexistent_conversation(client):
    user = create_test_user(client)

    conversation_id = str(uuid4())

    response = client.get(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"


def test_delete_conversation(client):
    user = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user,
    )

    conversation_id = conversation["id"]

    response = client.delete(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert get_response.status_code == 404


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_conversation_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "title": "Unauthorized Conversation",
    }

    response = client.post(
        "/conversations/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_conversation(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user2,
    )

    conversation_id = conversation["id"]

    response = client.get(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_conversations(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    create_test_conversation(
        client,
        user2,
    )

    response = client.get(
        f"/conversations/user/{user2['id']}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_delete_another_users_conversation(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    conversation = create_test_conversation(
        client,
        user2,
    )

    conversation_id = conversation["id"]

    response = client.delete(
        f"/conversations/{conversation_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )