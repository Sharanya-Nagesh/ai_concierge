from uuid import uuid4

from fastapi.testclient import TestClient
from app.services.llm_provider import LLMProviderError
from app.services.llm_service import LLMService
from app.services.chat_service import ChatService
from app.models.message import Message, MessageSender





def create_test_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "email": f"chat_{uuid4()}@example.com",
            "full_name": "Chat Test User",
            "password": "testpassword123",
        },
    )

    assert response.status_code == 201

    user = response.json()

    login_response = client.post(
        "/auth/login",
        json={
            "email": user["email"],
            "password": "testpassword123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return user, headers


def test_create_new_chat(client: TestClient):
    user, headers = create_test_user(client)

    response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["conversation_id"] is not None
    assert data["user_message"] == "Hello"
    assert data["assistant_message"] == "Mock response to: Hello"


def test_continue_existing_chat(client: TestClient):
    user, headers = create_test_user(client)

    first_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "Hello",
        },
    )

    assert first_response.status_code == 200

    conversation_id = first_response.json()["conversation_id"]

    second_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "conversation_id": conversation_id,
            "message": "How are you?",
        },
    )

    assert second_response.status_code == 200

    data = second_response.json()

    assert data["conversation_id"] == conversation_id
    assert data["user_message"] == "How are you?"
    assert (
        data["assistant_message"]
        == "Mock response to: How are you?"
    )


def test_chat_requires_authentication(client: TestClient):
    response = client.post(
        "/chat/",
        json={
            "message": "Hello",
        },
    )

    assert response.status_code == 401


def test_chat_persists_messages(client: TestClient):
    user, headers = create_test_user(client)

    chat_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "What is RAG?",
        },
    )

    assert chat_response.status_code == 200

    data = chat_response.json()
    conversation_id = data["conversation_id"]

    # Verify conversation was persisted
    conversation_response = client.get(
        f"/conversations/{conversation_id}",
        headers=headers,
    )

    assert conversation_response.status_code == 200

    conversation = conversation_response.json()

    assert conversation["id"] == conversation_id
    assert conversation["user_id"] == user["id"]

    # Verify both messages were persisted
    messages_response = client.get(
        f"/messages/conversation/{conversation_id}",
        headers=headers,
    )

    assert messages_response.status_code == 200

    messages = messages_response.json()

    assert len(messages) == 2

    assert messages[0]["sender"] == "user"
    assert messages[0]["content"] == "What is RAG?"

    assert messages[1]["sender"] == "assistant"
    assert (
        messages[1]["content"]
        == "Mock response to: What is RAG?"
    )


def test_chat_rejects_empty_message(client: TestClient):
    user, headers = create_test_user(client)

    response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "",
        },
    )

    assert response.status_code == 422


def test_chat_rejects_message_over_5000_characters(
    client: TestClient,
):
    user, headers = create_test_user(client)

    response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "a" * 5001,
        },
    )

    assert response.status_code == 422

def test_new_chat_llm_failure_rolls_back(
    client,
    monkeypatch,
):
    user, headers = create_test_user(client)

    def mock_failure(self, user_message):
        raise LLMProviderError("Simulated LLM failure")

    monkeypatch.setattr(
        LLMService,
        "generate_response",
        mock_failure,
    )

    response = client.post(
        "/chat/",
        headers=headers,
        json={"message": "Hello"},
    )

    assert response.status_code == 503

    # Verify that no conversation was persisted
    conversations_response = client.get(
        f"/conversations/user/{user['id']}",
        headers=headers,
    )

    assert conversations_response.status_code == 200
    assert conversations_response.json() == []

def test_existing_chat_llm_failure_preserves_history(
    client,
    monkeypatch,
):
    user, headers = create_test_user(client)

    # First create a successful conversation
    initial_response = client.post(
        "/chat/",
        headers=headers,
        json={"message": "Hello"},
    )

    assert initial_response.status_code == 200

    conversation_id = initial_response.json()["conversation_id"]

    def mock_failure(self, user_message):
        raise LLMProviderError("Simulated LLM failure")

    monkeypatch.setattr(
        LLMService,
        "generate_response",
        mock_failure,
    )

    # Attempt to continue the conversation
    failed_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "conversation_id": conversation_id,
            "message": "Explain RAG",
        },
    )

    assert failed_response.status_code == 503

    # Verify that the original two messages remain
    messages_response = client.get(
        f"/messages/conversation/{conversation_id}",
        headers=headers,
    )

    assert messages_response.status_code == 200

    messages = messages_response.json()

    assert len(messages) == 2
    assert messages[0]["content"] == "Hello"
    assert messages[1]["sender"] == "assistant"

def test_unauthorized_chat_does_not_call_llm(
    client,
    monkeypatch,
):
    user_a, headers_a = create_test_user(client)
    user_b, headers_b = create_test_user(client)

    # User B creates a conversation
    initial_response = client.post(
        "/chat/",
        headers=headers_b,
        json={"message": "My private conversation"},
    )

    assert initial_response.status_code == 200

    conversation_id = initial_response.json()["conversation_id"]

    # Track whether the LLM is invoked
    calls = {"count": 0}

    def mock_generate(self, user_message):
        calls["count"] += 1
        return "Mock response"

    monkeypatch.setattr(
        LLMService,
        "generate_response",
        mock_generate,
    )

    # User A attempts to access User B's conversation
    response = client.post(
        "/chat/",
        headers=headers_a,
        json={
            "conversation_id": conversation_id,
            "message": "Unauthorized access",
        },
    )

    assert response.status_code == 403
    assert calls["count"] == 0

def test_user_cannot_continue_another_users_conversation(
    client: TestClient,
):
    # Create User A
    user_a, headers_a = create_test_user(client)

    # Create User B
    user_b, headers_b = create_test_user(client)

    # User B creates a conversation
    response = client.post(
        "/chat/",
        headers=headers_b,
        json={
            "message": "This is User B's conversation",
        },
    )

    assert response.status_code == 200

    conversation_id = response.json()["conversation_id"]

    # User A tries to continue User B's conversation
    response = client.post(
        "/chat/",
        headers=headers_a,
        json={
            "conversation_id": conversation_id,
            "message": "I should not be able to access this.",
        },
    )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "You do not have access to this conversation"
    )

def test_chat_preserves_conversation_history(client: TestClient):
    user, headers = create_test_user(client)

    # First message
    first_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "message": "Hello",
        },
    )

    assert first_response.status_code == 200

    conversation_id = first_response.json()["conversation_id"]

    # Second message
    second_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "conversation_id": conversation_id,
            "message": "What is RAG?",
        },
    )

    assert second_response.status_code == 200

    # Third message
    third_response = client.post(
        "/chat/",
        headers=headers,
        json={
            "conversation_id": conversation_id,
            "message": "Explain it simply.",
        },
    )

    assert third_response.status_code == 200

    # Retrieve conversation history
    messages_response = client.get(
        f"/messages/conversation/{conversation_id}",
        headers=headers,
    )

    assert messages_response.status_code == 200

    messages = messages_response.json()

    assert len(messages) == 6

    assert messages[0]["sender"] == "user"
    assert messages[0]["content"] == "Hello"

    assert messages[1]["sender"] == "assistant"

    assert messages[2]["sender"] == "user"
    assert messages[2]["content"] == "What is RAG?"

    assert messages[3]["sender"] == "assistant"

    assert messages[4]["sender"] == "user"
    assert messages[4]["content"] == "Explain it simply."

    assert messages[5]["sender"] == "assistant"

def test_context_window_limits_messages(client):
    user, headers = create_test_user(client)

    service = ChatService(
        db=next(
            app.dependency_overrides[get_db]()
        )
    )