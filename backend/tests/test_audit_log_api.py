from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Audit Log Test User",
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


def create_test_audit_log(client, user):
    payload = {
        "user_id": user["id"],
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
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_audit_log(client):
    user = create_test_user(client)
    entity_id = str(uuid4())

    payload = {
        "user_id": user["id"],
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
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user["id"]
    assert data["action"] == "created"
    assert data["entity_type"] == "conversation"
    assert data["entity_id"] == entity_id
    assert data["metadata"]["source"] == "api_test"
    assert data["metadata"]["test"] is True
    assert "created_at" in data


def test_get_audit_log(client):
    user = create_test_user(client)

    audit_log = create_test_audit_log(
        client,
        user,
    )

    audit_log_id = audit_log["id"]

    response = client.get(
        f"/audit-logs/{audit_log_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == audit_log_id
    assert data["user_id"] == user["id"]
    assert data["action"] == "created"
    assert data["entity_type"] == "conversation"
    assert data["metadata"]["source"] == "api_test"


def test_get_user_audit_logs(client):
    user = create_test_user(client)

    create_test_audit_log(
        client,
        user,
    )

    second_payload = {
        "user_id": user["id"],
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
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/audit-logs/user/{user['id']}",
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


def test_get_nonexistent_audit_log(client):
    user = create_test_user(client)

    audit_log_id = str(uuid4())

    response = client.get(
        f"/audit-logs/{audit_log_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Audit log not found"


def test_create_audit_log_without_user(client):
    user = create_test_user(client)

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
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["user_id"] is None
    assert data["action"] == "system_event"
    assert data["entity_type"] == "system"
    assert data["entity_id"] is None
    assert data["metadata"]["source"] == "system"


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_audit_log_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "action": "created",
        "entity_type": "conversation",
        "entity_id": str(uuid4()),
        "metadata": {
            "source": "unauthorized_test",
        },
    }

    response = client.post(
        "/audit-logs/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_audit_log(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    audit_log = create_test_audit_log(
        client,
        user2,
    )

    audit_log_id = audit_log["id"]

    response = client.get(
        f"/audit-logs/{audit_log_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_audit_logs(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    create_test_audit_log(
        client,
        user2,
    )

    response = client.get(
        f"/audit-logs/user/{user2['id']}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )