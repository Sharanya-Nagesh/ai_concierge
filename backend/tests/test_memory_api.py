from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Memory Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_memory(client, user_id):
    payload = {
        "user_id": user_id,
        "memory_type": "preference",
        "content": "User prefers concise responses.",
        "importance": 0.8,
        "source": "conversation",
        "embedding_id": None,
    }

    response = client.post(
        "/memories/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_create_memory(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "memory_type": "preference",
        "content": "User prefers concise responses.",
        "importance": 0.8,
        "source": "conversation",
        "embedding_id": None,
    }

    response = client.post(
        "/memories/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["memory_type"] == "preference"
    assert data["content"] == payload["content"]
    assert data["importance"] == 0.8
    assert data["source"] == "conversation"
    assert data["embedding_id"] is None


def test_get_memory(client):
    user_id = create_test_user(client)

    memory = create_test_memory(
        client,
        user_id,
    )

    memory_id = memory["id"]

    response = client.get(
        f"/memories/{memory_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == memory_id
    assert data["user_id"] == user_id
    assert data["content"] == "User prefers concise responses."


def test_get_user_memories(client):
    user_id = create_test_user(client)

    create_test_memory(client, user_id)

    second_payload = {
        "user_id": user_id,
        "memory_type": "fact",
        "content": "User is learning machine learning.",
        "importance": 0.7,
        "source": "conversation",
        "embedding_id": None,
    }

    second_response = client.post(
        "/memories/",
        json=second_payload,
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/memories/user/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(item["user_id"] == user_id for item in data)


def test_get_nonexistent_memory(client):
    memory_id = str(uuid4())

    response = client.get(
        f"/memories/{memory_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Memory not found"


def test_delete_memory(client):
    user_id = create_test_user(client)

    memory = create_test_memory(
        client,
        user_id,
    )

    memory_id = memory["id"]

    response = client.delete(
        f"/memories/{memory_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/memories/{memory_id}"
    )

    assert get_response.status_code == 404