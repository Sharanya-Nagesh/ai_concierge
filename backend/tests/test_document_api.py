from uuid import uuid4


def create_test_user(client):
    password = "test-password"

    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Document Test User",
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


def create_test_document(client, user):
    payload = {
        "user_id": user["id"],
        "filename": "test_document.pdf",
        "original_filename": "Test Document.pdf",
        "file_size": 1024,
        "mime_type": "application/pdf",
        "page_count": 5,
        "upload_status": "completed",
        "storage_path": "/documents/test_document.pdf",
    }

    response = client.post(
        "/documents/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_document(client):
    user = create_test_user(client)

    payload = {
        "user_id": user["id"],
        "filename": "test_document.pdf",
        "original_filename": "Test Document.pdf",
        "file_size": 1024,
        "mime_type": "application/pdf",
        "page_count": 5,
        "upload_status": "completed",
        "storage_path": "/documents/test_document.pdf",
    }

    response = client.post(
        "/documents/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user["id"]
    assert data["filename"] == payload["filename"]
    assert data["original_filename"] == payload["original_filename"]
    assert data["file_size"] == 1024
    assert data["mime_type"] == "application/pdf"
    assert data["page_count"] == 5
    assert data["upload_status"] == "completed"
    assert data["storage_path"] == payload["storage_path"]


def test_get_document(client):
    user = create_test_user(client)

    document = create_test_document(
        client,
        user,
    )

    document_id = document["id"]

    response = client.get(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["user_id"] == user["id"]
    assert data["filename"] == "test_document.pdf"


def test_get_user_documents(client):
    user = create_test_user(client)

    create_test_document(
        client,
        user,
    )

    second_payload = {
        "user_id": user["id"],
        "filename": "second_document.pdf",
        "original_filename": "Second Document.pdf",
        "file_size": 2048,
        "mime_type": "application/pdf",
        "page_count": 10,
        "upload_status": "completed",
        "storage_path": "/documents/second_document.pdf",
    }

    second_response = client.post(
        "/documents/",
        json=second_payload,
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/documents/user/{user['id']}",
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


def test_get_nonexistent_document(client):
    user = create_test_user(client)

    document_id = str(uuid4())

    response = client.get(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_delete_document(client):
    user = create_test_user(client)

    document = create_test_document(
        client,
        user,
    )

    document_id = document["id"]

    response = client.delete(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user['token']}",
        },
    )

    assert get_response.status_code == 404


# ---------------------------------------------------------
# Authorization / Ownership Tests
# ---------------------------------------------------------


def test_user_cannot_create_document_for_another_user(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    payload = {
        "user_id": user2["id"],
        "filename": "unauthorized.pdf",
        "original_filename": "Unauthorized.pdf",
        "file_size": 1024,
        "mime_type": "application/pdf",
        "page_count": 1,
        "upload_status": "completed",
        "storage_path": "/documents/unauthorized.pdf",
    }

    response = client.post(
        "/documents/",
        json=payload,
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_document(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    document = create_test_document(
        client,
        user2,
    )

    document_id = document["id"]

    response = client.get(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_get_another_users_documents(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    create_test_document(
        client,
        user2,
    )

    response = client.get(
        f"/documents/user/{user2['id']}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )


def test_user_cannot_delete_another_users_document(client):
    user1 = create_test_user(client)
    user2 = create_test_user(client)

    document = create_test_document(
        client,
        user2,
    )

    document_id = document["id"]

    response = client.delete(
        f"/documents/{document_id}",
        headers={
            "Authorization": f"Bearer {user1['token']}",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this user's resources"
    )
