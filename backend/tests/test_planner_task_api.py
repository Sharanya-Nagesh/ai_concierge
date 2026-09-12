from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Planner Task Test User",
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


def create_test_task(client, user):
    payload = {
        "user_id": user["id"],
        "title": "Complete project documentation",
        "description": "Finish the remaining project documentation.",
        "due_date": "2026-12-31",
        "priority": "high",
        "status": "pending",
    }

    response = client.post(
        "/planner-tasks/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_planner_task(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "title": "Complete project documentation",
        "description": "Finish the remaining project documentation.",
        "due_date": "2026-12-31",
        "priority": "high",
        "status": "pending",
    }

    response = client.post(
        "/planner-tasks/",
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
    assert data["description"] == payload["description"]
    assert data["due_date"] == "2026-12-31"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


def test_get_planner_task(client):
    user = create_test_user(client)

    task = create_test_task(
        client,
        user,
    )

    task_id = task["id"]

    response = client.get(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["user_id"] == user["id"]
    assert data["title"] == "Complete project documentation"


def test_get_user_tasks(client):
    user = create_test_user(client)

    create_test_task(
        client,
        user,
    )

    second_payload = {
        "user_id": user["id"],
        "title": "Review API tests",
        "description": None,
        "due_date": None,
        "priority": "medium",
        "status": "pending",
    }

    second_response = client.post(
        "/planner-tasks/",
        json=second_payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/planner-tasks/user/{user['id']}",
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


def test_get_nonexistent_planner_task(client):
    user = create_test_user(client)

    task_id = str(uuid4())

    response = client.get(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Planner task not found"


def test_delete_planner_task(client):
    user = create_test_user(client)

    task = create_test_task(
        client,
        user,
    )

    task_id = task["id"]

    response = client.delete(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert get_response.status_code == 404


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_task_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "title": "Unauthorized task",
        "description": "This task should not be allowed.",
        "due_date": "2026-12-31",
        "priority": "high",
        "status": "pending",
    }

    response = client.post(
        "/planner-tasks/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_task(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    task = create_test_task(
        client,
        user2,
    )

    task_id = task["id"]

    response = client.get(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_tasks(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    create_test_task(
        client,
        user2,
    )

    response = client.get(
        f"/planner-tasks/user/{user2['id']}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_delete_another_users_task(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    task = create_test_task(
        client,
        user2,
    )

    task_id = task["id"]

    response = client.delete(
        f"/planner-tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )