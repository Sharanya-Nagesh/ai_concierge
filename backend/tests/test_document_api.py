from uuid import uuid4


def create_test_user(client):
    payload = {
        "email": f"user-{uuid4()}@example.com",
        "full_name": "Document Test User",
        "password_hash": "test-password-hash",
    }

    response = client.post("/users/", json=payload)

    assert response.status_code == 201

    return response.json()["id"]


def create_test_document(client, user_id):
    payload = {
        "user_id": user_id,
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
    )

    assert response.status_code == 201

    return response.json()


def test_create_document(client):
    user_id = create_test_user(client)

    payload = {
        "user_id": user_id,
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
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["user_id"] == user_id
    assert data["filename"] == payload["filename"]
    assert data["original_filename"] == payload["original_filename"]
    assert data["file_size"] == 1024
    assert data["mime_type"] == "application/pdf"
    assert data["page_count"] == 5
    assert data["upload_status"] == "completed"
    assert data["storage_path"] == payload["storage_path"]


def test_get_document(client):
    user_id = create_test_user(client)

    document = create_test_document(
        client,
        user_id,
    )

    document_id = document["id"]

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == document_id
    assert data["user_id"] == user_id
    assert data["filename"] == "test_document.pdf"


def test_get_user_documents(client):
    user_id = create_test_user(client)

    create_test_document(client, user_id)

    second_payload = {
        "user_id": user_id,
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
    )

    assert second_response.status_code == 201

    response = client.get(
        f"/documents/user/{user_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(item["user_id"] == user_id for item in data)


def test_get_nonexistent_document(client):
    document_id = str(uuid4())

    response = client.get(
        f"/documents/{document_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_delete_document(client):
    user_id = create_test_user(client)

    document = create_test_document(
        client,
        user_id,
    )

    document_id = document["id"]

    response = client.delete(
        f"/documents/{document_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/documents/{document_id}"
    )

    assert get_response.status_code == 404