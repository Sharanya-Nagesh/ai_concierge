from datetime import date
from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Planner Task Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_task(client, user_id):
    payload = {
        "user_id": user_id,
        "title": "Complete project documentation",
        "description": "Finish the remaining project documentation.",
        "due_date": "2026-12-31",
        "priority": "high",
        "status": "pending",
    }

    response = client.post(
        "/planner-tasks/",
        json=payload,
    )

    assert response.status_code == 201

    return response.json()


def test_create_planner_task(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
        "title": "Complete project documentation",
        "description": "Finish the remaining project documentation.",
        "due_date": "2026-12-31",
        "priority": "high",
        "status": "pending",
    }

    response = client.post(
        "/planner-tasks/",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["due_date"] == "2026-12-31"
    assert data["priority"] == "high"
    assert data["status"] == "pending"


def test_get_planner_task(client):
    user_id = create_test_user(client)

    task = create_test_task(
        client,
        user_id,
    )

    task_id = task["id"]

    response = client.get(
        f"/planner-tasks/{task_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["user_id"] == user_id
    assert data["title"] == "Complete project documentation"


def test_get_user_tasks(client):
    user_id = create_test_user(client)

    create_test_task(client, user_id)

    second_payload = {
        "user_id": user_id,
        "title": "Review API tests",
        "description": None,
        "due_date": None,
        "priority": "medium",
        "status": "pending",
    }

    second_response = client.post(
        "/planner-tasks/",
        json=second_payload,
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/planner-tasks/user/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(item["user_id"] == user_id for item in data)


def test_get_nonexistent_planner_task(client):
    task_id = str(uuid4())

    response = client.get(
        f"/planner-tasks/{task_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Planner task not found"


def test_delete_planner_task(client):
    user_id = create_test_user(client)

    task = create_test_task(
        client,
        user_id,
    )

    task_id = task["id"]

    response = client.delete(
        f"/planner-tasks/{task_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/planner-tasks/{task_id}"
    )

    assert get_response.status_code == 404