# API Specification

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 2.0

> **Status:** Draft

---

# Table of Contents

1. Introduction
2. API Design Principles
3. Base URL
4. Authentication
5. Common Headers
6. Common Response Format
7. Error Handling
8. Authentication APIs
9. User APIs
10. Conversation APIs
11. Message APIs
12. Document APIs
13. Memory APIs
14. Planner APIs
15. Recommendation APIs
16. Agent APIs
17. Health APIs
18. Error Codes
19. Pagination
20. Rate Limiting
21. Versioning
22. Future APIs

---

# 1. Introduction

This document defines the REST API specification for the AI Concierge platform.

The APIs enable communication between the React frontend and the FastAPI backend while following RESTful principles.

Every endpoint specifies:

- Purpose
- HTTP Method
- URL
- Authentication
- Request Body
- Response Body
- Status Codes
- Error Responses

---

# 2. API Design Principles

The API follows these principles:

- RESTful architecture
- Stateless communication
- JSON request/response
- JWT Authentication
- Versioned endpoints
- Predictable URLs
- Consistent error handling
- Secure by default

---

# 3. Base URL

Development

```

http://localhost:8000/api/v1

```

Production

```

https://api.aiconcierge.com/api/v1

```

All endpoints in this document are relative to the Base URL.

---

# 4. Authentication

Protected endpoints require a JWT access token.

Example:

```

Authorization: Bearer <ACCESS_TOKEN>

```

If authentication fails:

```

401 Unauthorized

```

---

# 5. Common Headers

Request

```

Content-Type: application/json

Authorization: Bearer <TOKEN>

Accept: application/json

```

Response

```

Content-Type: application/json

```

---

# 6. Standard Response Format

## Success

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

---

## Error

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "email",
      "message": "Email is required."
    }
  ]
}
```

---

# 7. HTTP Status Codes

| Code | Meaning |
|------|----------|
|200|OK|
|201|Created|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|429|Too Many Requests|
|500|Internal Server Error|

---

# 8. Authentication APIs

The Authentication module manages user registration, login, logout, and account security.
# 9. User APIs

The User module manages profile information and personalization settings.

---

## 9.1 Get Current User Profile

### Endpoint

```http
GET /users/me
```

---

### Description

Returns the authenticated user's profile.

---

### Authentication

✅ Required

---

### Headers

```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

### Request Body

None

---

### Success Response

**200 OK**

```json
{
  "success": true,
  "data": {
    "id": "b2f79c9d-45e7-41c1-8db6-37f4b9d8f98e",
    "full_name": "Sharanya N",
    "email": "sharanya@example.com",
    "role": "user",
    "created_at": "2026-07-22T10:15:20Z"
  }
}
```

---

### Error Responses

```json
{
    "success": false,
    "message": "Unauthorized."
}
```

Status Code

```
401 Unauthorized
```

---

## 9.2 Update User Profile

### Endpoint

```http
PATCH /users/me
```

---

### Description

Updates editable user profile fields.

---

### Authentication

✅ Required

---

### Request Body

```json
{
    "full_name": "Sharanya N",
    "email": "sharanya@example.com"
}
```

---

### Validation Rules

| Field | Validation |
|---------|------------|
| full_name | 2–100 characters |
| email | Valid email |
| email | Must be unique |

---

### Success Response

```json
{
    "success": true,
    "message": "Profile updated successfully.",
    "data": {
        "full_name": "Sharanya N",
        "email": "sharanya@example.com"
    }
}
```

---

## 9.3 Delete User Account

### Endpoint

```http
DELETE /users/me
```

---

### Description

Deletes the authenticated user's account and all associated data.

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "message": "Account deleted successfully."
}
```

---

### Notes

Deleting a user also removes:

- Conversations
- Messages
- Uploaded Documents
- Memories
- Planner Tasks
- User Preferences

This is implemented using database cascade deletion.

---

## 9.4 Get User Preferences

### Endpoint

```http
GET /users/preferences
```

---

### Description

Returns personalization settings.

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "data": {
        "preferred_language": "English",
        "response_style": "Detailed",
        "theme": "Dark",
        "timezone": "Asia/Kolkata"
    }
}
```

---

## 9.5 Update User Preferences

### Endpoint

```http
PATCH /users/preferences
```

---

### Authentication

✅ Required

---

### Request Body

```json
{
    "preferred_language": "Hindi",
    "response_style": "Concise",
    "theme": "Light",
    "timezone": "Asia/Kolkata"
}
```

---

### Request Fields

| Field | Description |
|---------|-------------|
| preferred_language | Preferred interaction language |
| response_style | Concise / Detailed |
| theme | Light / Dark / System |
| timezone | User timezone |

---

### Success Response

```json
{
    "success": true,
    "message": "Preferences updated successfully."
}
```

---

## 9.6 Upload Profile Picture (Future)

### Endpoint

```http
POST /users/avatar
```

---

### Authentication

✅ Required

---

### Content-Type

```
multipart/form-data
```

---

### Request

```
avatar=<image_file>
```

Supported formats

- PNG
- JPG
- JPEG
- WEBP

Maximum size

```
5 MB
```

---

### Success Response

```json
{
    "success": true,
    "message": "Profile picture uploaded successfully.",
    "data": {
        "avatar_url": "/uploads/avatar/user123.png"
    }
}
```

---

## 9.7 Delete Profile Picture (Future)

### Endpoint

```http
DELETE /users/avatar
```

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "message": "Profile picture removed."
}
```

---

# User API Summary

| Method | Endpoint | Description |
|----------|-------------------------|------------------------------|
| GET | /users/me | Get current user |
| PATCH | /users/me | Update profile |
| DELETE | /users/me | Delete account |
| GET | /users/preferences | Get preferences |
| PATCH | /users/preferences | Update preferences |
| POST | /users/avatar | Upload avatar *(Future)* |
| DELETE | /users/avatar | Delete avatar *(Future)* |

---

# User API Flow

```text
User

↓

Login

↓

GET /users/me

↓

Display Profile

↓

Edit Profile

↓

PATCH /users/me

↓

Update Database

↓

Return Updated Profile
```

---

# Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|400|Validation Error|
|401|Unauthorized|
|404|User Not Found|
|409|Email Already Exists|
|500|Internal Server Error|

---

# Notes

- Every endpoint requires a valid JWT except registration and login.
- User data is always scoped to the authenticated user.
- Email addresses are globally unique.
- Future versions may support profile images and additional user settings.

# 10. Conversation APIs

The Conversation module manages chat sessions. A conversation represents a collection of messages exchanged between the user and the AI assistant.

---

## 10.1 Create Conversation

### Endpoint

```http
POST /conversations
```

### Description

Creates a new conversation.

### Authentication

✅ Required

### Request Body

```json
{
    "title": "Learning Transformers"
}
```

### Validation

| Field | Rules |
|---------|--------|
| title | Optional, Maximum 200 characters |

If no title is provided, the backend generates one automatically.

### Success Response

**201 Created**

```json
{
    "success": true,
    "message": "Conversation created successfully.",
    "data": {
        "id": "conv_01",
        "title": "Learning Transformers",
        "created_at": "2026-08-01T14:30:00Z"
    }
}
```

---

## 10.2 List Conversations

### Endpoint

```http
GET /conversations
```

### Description

Returns all conversations belonging to the authenticated user.

### Authentication

✅ Required

### Query Parameters

| Parameter | Type | Description |
|------------|------|-------------|
| page | Integer | Page number |
| limit | Integer | Items per page |
| search | String | Search conversation title |

### Example

```http
GET /conversations?page=1&limit=20
```

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "id": "conv_01",
            "title": "Learning Transformers",
            "last_message_at": "2026-08-01T14:45:20Z"
        },
        {
            "id": "conv_02",
            "title": "Azure AI-900",
            "last_message_at": "2026-08-01T12:10:50Z"
        }
    ]
}
```

---

## 10.3 Get Conversation

### Endpoint

```http
GET /conversations/{conversation_id}
```

### Authentication

✅ Required

### Description

Returns metadata for a specific conversation.

### Success Response

```json
{
    "success": true,
    "data": {
        "id": "conv_01",
        "title": "Learning Transformers",
        "created_at": "2026-08-01T14:30:00Z",
        "updated_at": "2026-08-01T14:45:20Z"
    }
}
```

---

## 10.4 Rename Conversation

### Endpoint

```http
PATCH /conversations/{conversation_id}
```

### Request

```json
{
    "title": "Transformer Architecture"
}
```

### Success Response

```json
{
    "success": true,
    "message": "Conversation renamed successfully."
}
```

---

## 10.5 Delete Conversation

### Endpoint

```http
DELETE /conversations/{conversation_id}
```

### Description

Deletes the conversation and all associated messages.

### Success Response

```json
{
    "success": true,
    "message": "Conversation deleted successfully."
}
```

---

## 10.6 Search Conversations

### Endpoint

```http
GET /conversations/search
```

### Query Parameters

```
query=transformers
```

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "id": "conv_01",
            "title": "Learning Transformers"
        }
    ]
}
```

---

## 10.7 Archive Conversation (Future)

### Endpoint

```http
PATCH /conversations/{conversation_id}/archive
```

Archives an old conversation without deleting it.

---

## Conversation API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /conversations | Create conversation |
| GET | /conversations | List conversations |
| GET | /conversations/{id} | Get conversation |
| PATCH | /conversations/{id} | Rename conversation |
| DELETE | /conversations/{id} | Delete conversation |
| GET | /conversations/search | Search conversations |
| PATCH | /conversations/{id}/archive | Archive conversation *(Future)* |

# 11. Message APIs

The Message module handles communication between the user and the AI Concierge.

Every message belongs to exactly one conversation.

---

## 11.1 Send Message

### Endpoint

```http
POST /conversations/{conversation_id}/messages
```

### Authentication

✅ Required

### Description

Sends a user message to the AI assistant.

### Request

```json
{
    "message": "Explain Retrieval-Augmented Generation.",
    "language": "English"
}
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "message_id": "msg_123",
        "conversation_id": "conv_01",
        "assistant_response": "Retrieval-Augmented Generation (RAG)...",
        "citations": [
            {
                "document": "NLP Notes.pdf",
                "page": 12
            }
        ],
        "tokens_used": 845,
        "model": "Gemini"
    }
}
```

---

## 11.2 Stream Message (Future)

### Endpoint

```http
POST /conversations/{conversation_id}/messages/stream
```

### Description

Returns AI responses using streaming instead of waiting for the complete answer.

Transport

```
Server-Sent Events (SSE)
```

Future

```
WebSockets
```

---

## 11.3 Get Messages

### Endpoint

```http
GET /conversations/{conversation_id}/messages
```

### Description

Returns every message belonging to a conversation.

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "sender": "user",
            "content": "Explain RAG."
        },
        {
            "sender": "assistant",
            "content": "Retrieval-Augmented Generation..."
        }
    ]
}
```

---

## 11.4 Edit User Message (Future)

### Endpoint

```http
PATCH /messages/{message_id}
```

### Description

Allows editing the latest user message before regeneration.

---

### Request

```json
{
    "message": "Explain Graph RAG."
}
```

---

## 11.5 Regenerate AI Response

### Endpoint

```http
POST /messages/{message_id}/regenerate
```

### Description

Generates another answer using the same prompt.

### Success Response

```json
{
    "success": true,
    "message": "Response regenerated successfully.",
    "data": {
        "assistant_response": "Another explanation..."
    }
}
```

---

## 11.6 Delete Message (Future)

### Endpoint

```http
DELETE /messages/{message_id}
```

Deletes a specific message.

---

## 11.7 Give Feedback

### Endpoint

```http
POST /messages/{message_id}/feedback
```

### Request

```json
{
    "rating": "thumbs_up",
    "comment": "Very helpful."
}
```

Supported ratings

- thumbs_up
- thumbs_down

### Success Response

```json
{
    "success": true,
    "message": "Feedback submitted."
}
```

---

## Message API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /conversations/{id}/messages | Send message |
| GET | /conversations/{id}/messages | Get conversation messages |
| POST | /conversations/{id}/messages/stream | Streaming chat *(Future)* |
| PATCH | /messages/{id} | Edit message *(Future)* |
| POST | /messages/{id}/regenerate | Regenerate response |
| DELETE | /messages/{id} | Delete message *(Future)* |
| POST | /messages/{id}/feedback | User feedback |

---

## Internal Processing Flow

```
User Message

↓

Authentication

↓

Conversation Validation

↓

Intent Detection

↓

Memory Retrieval

↓

Document Retrieval (RAG)

↓

Prompt Construction

↓

LLM

↓

Response Validation

↓

Store Messages

↓

Return Response
```
# 12. Document APIs

The Document module manages user-uploaded files that serve as the knowledge base for Retrieval-Augmented Generation (RAG).

Uploaded documents are stored, processed, chunked, embedded, indexed into the vector database (Qdrant), and made available for semantic retrieval.

---

## 12.1 Upload Document

### Endpoint

```http
POST /documents
```

### Authentication

✅ Required

### Content-Type

```
multipart/form-data
```

### Description

Uploads a document for indexing.

### Request

| Field | Type | Required |
|---------|------|----------|
| file | File | Yes |

---

### Supported Formats

- PDF
- DOCX *(Future)*
- TXT *(Future)*
- PPTX *(Future)*

---

### Maximum File Size

```
25 MB
```

---

### Success Response

**201 Created**

```json
{
    "success": true,
    "message": "Document uploaded successfully.",
    "data": {
        "document_id": "doc_001",
        "filename": "Transformers.pdf",
        "status": "processing"
    }
}
```

---

### Processing Pipeline

```
Upload

↓

Virus Scan (Future)

↓

Store File

↓

Extract Text

↓

Chunk Text

↓

Generate Embeddings

↓

Store in Qdrant

↓

Ready for Search
```

---

## 12.2 List Documents

### Endpoint

```http
GET /documents
```

### Authentication

✅ Required

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| page | Page number |
| limit | Items per page |
| search | Search filename |

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "document_id": "doc_001",
            "filename": "Transformers.pdf",
            "status": "indexed",
            "uploaded_at": "2026-08-01T09:20:00Z"
        },
        {
            "document_id": "doc_002",
            "filename": "Attention.pdf",
            "status": "processing",
            "uploaded_at": "2026-08-01T09:30:00Z"
        }
    ]
}
```

---

## 12.3 Get Document Details

### Endpoint

```http
GET /documents/{document_id}
```

### Description

Returns metadata for a document.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "document_id": "doc_001",
        "filename": "Transformers.pdf",
        "file_size": 3456789,
        "page_count": 245,
        "status": "indexed",
        "uploaded_at": "2026-08-01T09:20:00Z"
    }
}
```

---

## 12.4 Download Document

### Endpoint

```http
GET /documents/{document_id}/download
```

### Authentication

✅ Required

---

### Response

Returns the original uploaded file.

---

## 12.5 Delete Document

### Endpoint

```http
DELETE /documents/{document_id}
```

### Description

Deletes:

- Original document
- Chunk metadata
- Vector embeddings

---

### Success Response

```json
{
    "success": true,
    "message": "Document deleted successfully."
}
```

---

## 12.6 Preview Document

### Endpoint

```http
GET /documents/{document_id}/preview
```

### Description

Returns preview information.

Example

```json
{
    "success": true,
    "data": {
        "page_count": 245,
        "preview_pages": [
            1,
            2,
            3
        ]
    }
}
```

---

## 12.7 Re-index Document

### Endpoint

```http
POST /documents/{document_id}/reindex
```

### Description

Recreates embeddings after updating the embedding model or chunking strategy.

---

### Success Response

```json
{
    "success": true,
    "message": "Document re-indexing started."
}
```

---

## 12.8 Semantic Search

### Endpoint

```http
POST /documents/search
```

### Description

Performs semantic similarity search across uploaded documents.

---

### Request

```json
{
    "query": "Explain self-attention.",
    "top_k": 5
}
```

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "document": "Transformers.pdf",
            "page": 32,
            "score": 0.94,
            "chunk": "Self-attention computes..."
        }
    ]
}
```

---

## 12.9 RAG Query

### Endpoint

```http
POST /documents/query
```

### Description

Answers a question using uploaded documents.

---

### Request

```json
{
    "question": "Summarize Chapter 4."
}
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "answer": "Chapter 4 discusses...",
        "sources": [
            {
                "document": "Transformers.pdf",
                "page": 91
            }
        ]
    }
}
```

---

## 12.10 Processing Status

### Endpoint

```http
GET /documents/{document_id}/status
```

### Description

Returns indexing progress.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "status": "embedding",
        "progress": 72
    }
}
```

Possible Status Values

- uploaded
- extracting
- chunking
- embedding
- indexing
- indexed
- failed

---

## Document API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /documents | Upload document |
| GET | /documents | List documents |
| GET | /documents/{id} | Get document details |
| GET | /documents/{id}/download | Download document |
| GET | /documents/{id}/preview | Preview document |
| DELETE | /documents/{id} | Delete document |
| POST | /documents/{id}/reindex | Re-index document |
| POST | /documents/search | Semantic search |
| POST | /documents/query | RAG query |
| GET | /documents/{id}/status | Processing status |

---

## Internal Processing Flow

```
Upload Document

↓

Validate File

↓

Store Metadata

↓

Extract Text

↓

Chunk Text

↓

Generate Embeddings

↓

Store in Qdrant

↓

Ready for Semantic Search

↓

User Query

↓

Retrieve Relevant Chunks

↓

LLM

↓

Generate Answer
```

---

## Error Codes

| Status | Meaning |
|---------|----------|
|201|Uploaded Successfully|
|400|Invalid File|
|401|Unauthorized|
|404|Document Not Found|
|413|File Too Large|
|415|Unsupported File Type|
|500|Processing Error|

# 13. Memory APIs

The Memory module enables AI Concierge to maintain long-term personalized context for each user.

Unlike conversation history, memories persist across chat sessions and allow the assistant to provide personalized responses.

Examples of memories include:

- Career goals
- Preferred language
- Learning style
- Interests
- Frequently used technologies
- Long-term projects

---

## 13.1 Get All Memories

### Endpoint

```http
GET /memories
```

### Authentication

✅ Required

---

### Description

Returns all stored memories belonging to the authenticated user.

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| page | Page number |
| limit | Number of results |
| category | Filter by category |

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "memory_id": "mem_001",
            "category": "career",
            "memory_text": "User wants to become an NLP Engineer.",
            "importance_score": 0.98,
            "created_at": "2026-08-01T09:20:00Z"
        }
    ]
}
```

---

## 13.2 Get Memory

### Endpoint

```http
GET /memories/{memory_id}
```

### Description

Returns a specific memory.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "memory_id": "mem_001",
        "category": "career",
        "memory_text": "User wants to become an NLP Engineer.",
        "importance_score": 0.98
    }
}
```

---

## 13.3 Create Memory

### Endpoint

```http
POST /memories
```

### Authentication

✅ Required

---

### Description

Creates a new long-term memory.

---

### Request

```json
{
    "category": "career",
    "memory_text": "User is preparing for Azure AI-900."
}
```

---

### Success Response

```json
{
    "success": true,
    "message": "Memory created successfully."
}
```

---

## 13.4 Update Memory

### Endpoint

```http
PATCH /memories/{memory_id}
```

### Request

```json
{
    "memory_text": "User completed Azure AI-900 certification."
}
```

---

### Success Response

```json
{
    "success": true,
    "message": "Memory updated successfully."
}
```

---

## 13.5 Delete Memory

### Endpoint

```http
DELETE /memories/{memory_id}
```

### Description

Removes a stored memory.

---

### Success Response

```json
{
    "success": true,
    "message": "Memory deleted successfully."
}
```

---

## 13.6 Search Memories

### Endpoint

```http
POST /memories/search
```

### Description

Performs semantic similarity search over stored memories.

---

### Request

```json
{
    "query": "What certifications am I studying?"
}
```

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "memory_id": "mem_001",
            "memory_text": "User is preparing for Azure AI-900.",
            "score": 0.95
        }
    ]
}
```

---

## 13.7 Automatic Memory Extraction

### Endpoint

```http
POST /memories/extract
```

### Description

Extracts important facts from a conversation and stores them as memories.

---

### Request

```json
{
    "conversation_id": "conv_001"
}
```

---

### Success Response

```json
{
    "success": true,
    "message": "3 memories extracted.",
    "data": {
        "memories_created": 3
    }
}
```

---

## 13.8 Memory Categories

Supported categories include:

- career
- education
- preferences
- projects
- skills
- hobbies
- language
- goals
- personal_notes
- custom

---

## 13.9 Memory Importance Score

Each memory receives an importance score between **0.0** and **1.0**.

Example:

| Score | Meaning |
|--------|----------|
|0.95|Critical long-term memory|
|0.80|Important|
|0.60|Useful|
|0.30|Low priority|

Higher-scoring memories are more likely to be included in prompts.

---

## 13.10 Memory Retrieval During Chat

Whenever a user sends a message, the system performs:

```
Receive User Message

↓

Generate Embedding

↓

Search Qdrant

↓

Retrieve Top Memories

↓

Rank by Similarity

↓

Select Most Relevant

↓

Inject into Prompt

↓

LLM Generates Response
```

---

## Memory API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /memories | List memories |
| GET | /memories/{id} | Get memory |
| POST | /memories | Create memory |
| PATCH | /memories/{id} | Update memory |
| DELETE | /memories/{id} | Delete memory |
| POST | /memories/search | Semantic memory search |
| POST | /memories/extract | Automatic memory extraction |

---

## Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|201|Created|
|400|Validation Error|
|401|Unauthorized|
|404|Memory Not Found|
|500|Internal Server Error|
