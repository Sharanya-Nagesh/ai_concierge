# AI Concierge - API Specification

## Authentication

### Register

POST /auth/register

Request:

{
"username": "user",
"email": "[user@email.com](mailto:user@email.com)",
"password": "password"
}

### Login

POST /auth/login

Returns:

JWT Access Token

---

## User Profile

### Get Profile

GET /users/profile

### Update Profile

PUT /users/profile

---

## Chat

### Create Conversation

POST /chat/conversation

### Send Message

POST /chat/message

Request:

{
"conversation_id": "123",
"message": "Explain transformers"
}

### Get History

GET /chat/history/{conversation_id}

---

## Documents

### Upload Document

POST /documents/upload

### List Documents

GET /documents

### Delete Document

DELETE /documents/{id}

---

## RAG Query

POST /documents/query

Request:

{
"question": "Summarize chapter 2"
}

---

## Health Check

GET /health

Returns:

{
"status": "healthy"
}

## Future APIs

* Tool Calling
* Recommendation APIs
* Agent Analytics APIs
