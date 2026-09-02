from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Audit Log Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_audit_log(client, user_id):
    payload = {
        "user_id": user_id,
        "action": "created",
        "entity_type": "conversation",
        "entity_id": str(uuid4()),
        "metadata": {
            "source": "api_test",
        },
    }

    response = client.post(
        "/audit-logs/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_create_audit_log(client):
    user_id = create_test_user(client)
    entity_id = str(uuid4())

    payload = {
        "user_id": user_id,
        "action": "created",
        "entity_type": "conversation",
        "entity_id": entity_id,
        "metadata": {
            "source": "api_test",
            "test": True,
        },
    }

    response = client.post(
        "/audit-logs/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["action"] == "created"
    assert data["entity_type"] == "conversation"
    assert data["entity_id"] == entity_id
    assert data["metadata"]["source"] == "api_test"
    assert data["metadata"]["test"] is True
    assert "created_at" in data


def test_get_audit_log(client):
    user_id = create_test_user(client)

    audit_log = create_test_audit_log(
        client,
        user_id,
    )

    audit_log_id = audit_log["id"]

    response = client.get(
        f"/audit-logs/{audit_log_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == audit_log_id
    assert data["user_id"] == user_id
    assert data["action"] == "created"
    assert data["entity_type"] == "conversation"
    assert data["metadata"]["source"] == "api_test"


def test_get_user_audit_logs(client):
    user_id = create_test_user(client)

    create_test_audit_log(client, user_id)

    second_payload = {
        "user_id": user_id,
        "action": "updated",
        "entity_type": "memory",
        "entity_id": str(uuid4()),
        "metadata": {
            "source": "api_test",
        },
    }

    second_response = client.post(
        "/audit-logs/",
        json=second_payload,
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/audit-logs/user/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(item["user_id"] == user_id for item in data)


def test_get_nonexistent_audit_log(client):
    audit_log_id = str(uuid4())

    response = client.get(
        f"/audit-logs/{audit_log_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Audit log not found"


def test_create_audit_log_without_user(client):
    payload = {
        "user_id": None,
        "action": "system_event",
        "entity_type": "system",
        "entity_id": None,
        "metadata": {
            "source": "system",
        },
    }

    response = client.post(
        "/audit-logs/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] is None
    assert data["action"] == "system_event"
    assert data["entity_type"] == "system"
    assert data["entity_id"] is None
    assert data["metadata"]["source"] == "system"