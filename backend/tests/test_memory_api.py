from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Memory Test User",
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


def create_test_memory(client, user):
    payload = {
        "user_id": user["id"],
        "memory_type": "preference",
        "content": "User prefers concise responses.",
        "importance": 0.8,
        "source": "conversation",
        "embedding_id": None,
    }

    response = client.post(
        "/memories/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_memory(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "memory_type": "preference",
        "content": "User prefers concise responses.",
        "importance": 0.8,
        "source": "conversation",
        "embedding_id": None,
    }

    response = client.post(
        "/memories/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user["id"]
    assert data["memory_type"] == "preference"
    assert data["content"] == payload["content"]
    assert data["importance"] == 0.8
    assert data["source"] == "conversation"
    assert data["embedding_id"] is None


def test_get_memory(client):
    user = create_test_user(client)

    memory = create_test_memory(
        client,
        user,
    )

    memory_id = memory["id"]

    response = client.get(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == memory_id
    assert data["user_id"] == user["id"]
    assert data["content"] == "User prefers concise responses."


def test_get_user_memories(client):
    user = create_test_user(client)

    create_test_memory(
        client,
        user,
    )

    second_payload = {
        "user_id": user["id"],
        "memory_type": "fact",
        "content": "User is learning machine learning.",
        "importance": 0.7,
        "source": "conversation",
        "embedding_id": None,
    }

    second_response = client.post(
        "/memories/",
        json=second_payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/memories/user/{user['id']}",
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


def test_get_nonexistent_memory(client):
    user = create_test_user(client)

    memory_id = str(uuid4())

    response = client.get(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Memory not found"


def test_delete_memory(client):
    user = create_test_user(client)

    memory = create_test_memory(
        client,
        user,
    )

    memory_id = memory["id"]

    response = client.delete(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert get_response.status_code == 404


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_memory_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "memory_type": "preference",
        "content": "Unauthorized memory",
        "importance": 0.8,
        "source": "conversation",
        "embedding_id": None,
    }

    response = client.post(
        "/memories/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_memory(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    memory = create_test_memory(
        client,
        user2,
    )

    memory_id = memory["id"]

    response = client.get(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_memories(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    create_test_memory(
        client,
        user2,
    )

    response = client.get(
        f"/memories/user/{user2['id']}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_delete_another_users_memory(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    memory = create_test_memory(
        client,
        user2,
    )

    memory_id = memory["id"]

    response = client.delete(
        f"/memories/{memory_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )