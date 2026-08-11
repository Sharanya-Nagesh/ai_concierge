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
    "full_name": "ABC Agarwal",
    "email": "abc@example.com",
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

# 14. Planner APIs

The Planner module enables AI Concierge to create, manage, and track personalized learning plans, project milestones, reminders, and productivity tasks.

The planner combines user goals, AI recommendations, and task management to provide an intelligent study assistant.

---

# 14.1 Create Task

### Endpoint

```http
POST /planner/tasks
```

### Authentication

✅ Required

---

### Description

Creates a new planner task.

---

### Request

```json
{
    "title": "Complete Azure AI-900 Course",
    "description": "Finish all modules and practice exams.",
    "priority": "High",
    "due_date": "2026-08-30"
}
```

---

### Success Response

**201 Created**

```json
{
    "success": true,
    "message": "Task created successfully.",
    "data": {
        "task_id": "task_001"
    }
}
```

---

# 14.2 Get All Tasks

### Endpoint

```http
GET /planner/tasks
```

### Authentication

✅ Required

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| page | Page number |
| limit | Items per page |
| status | Pending / In Progress / Completed |
| priority | Low / Medium / High |

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "task_id": "task_001",
            "title": "Complete Azure AI-900",
            "status": "In Progress",
            "priority": "High",
            "due_date": "2026-08-30"
        }
    ]
}
```

---

# 14.3 Get Task Details

### Endpoint

```http
GET /planner/tasks/{task_id}
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "task_id": "task_001",
        "title": "Complete Azure AI-900",
        "description": "Finish all modules.",
        "status": "Pending",
        "priority": "High",
        "created_at": "2026-08-01T09:00:00Z"
    }
}
```

---

# 14.4 Update Task

### Endpoint

```http
PATCH /planner/tasks/{task_id}
```

### Request

```json
{
    "title": "Complete AI-900",
    "priority": "Medium",
    "due_date": "2026-09-05"
}
```

---

### Success Response

```json
{
    "success": true,
    "message": "Task updated successfully."
}
```

---

# 14.5 Update Task Status

### Endpoint

```http
PATCH /planner/tasks/{task_id}/status
```

### Request

```json
{
    "status": "Completed"
}
```

---

### Supported Status

- Pending
- In Progress
- Completed
- Cancelled

---

### Success Response

```json
{
    "success": true,
    "message": "Task status updated."
}
```

---

# 14.6 Delete Task

### Endpoint

```http
DELETE /planner/tasks/{task_id}
```

---

### Success Response

```json
{
    "success": true,
    "message": "Task deleted successfully."
}
```

---

# 14.7 AI Generate Study Plan

### Endpoint

```http
POST /planner/generate
```

---

### Description

Generates a personalized study roadmap using AI.

---

### Request

```json
{
    "goal": "Become an NLP Engineer",
    "duration_weeks": 16,
    "hours_per_day": 3
}
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "roadmap_id": "roadmap_001",
        "weeks": 16,
        "estimated_completion": "2026-12-01"
    }
}
```

---

# 14.8 Weekly Planner

### Endpoint

```http
GET /planner/weekly
```

---

### Description

Returns tasks grouped by week.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "week": "2026-W31",
        "tasks": [
            {
                "title": "Finish RAG Module",
                "status": "Pending"
            }
        ]
    }
}
```

---

# 14.9 Daily Planner

### Endpoint

```http
GET /planner/daily
```

---

### Description

Returns today's scheduled tasks.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "date": "2026-08-01",
        "tasks": [
            {
                "title": "Watch MLOps Lecture",
                "status": "Pending"
            }
        ]
    }
}
```

---

# 14.10 Mark Task Complete

### Endpoint

```http
POST /planner/tasks/{task_id}/complete
```

---

### Description

Marks a task as completed.

---

### Success Response

```json
{
    "success": true,
    "message": "Congratulations! Task completed."
}
```

---

# 14.11 Progress Dashboard

### Endpoint

```http
GET /planner/progress
```

---

### Description

Returns learning analytics and productivity statistics.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "completed_tasks": 42,
        "pending_tasks": 8,
        "completion_rate": 84,
        "study_hours": 126,
        "current_streak": 15
    }
}
```

---

# 14.12 AI Recommendations

### Endpoint

```http
GET /planner/recommendations
```

---

### Description

Provides AI-generated recommendations based on planner progress.

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "type": "study",
            "message": "You have been consistent this week. Consider starting the MLOps module."
        }
    ]
}
```

---

# Planner API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /planner/tasks | Create task |
| GET | /planner/tasks | List tasks |
| GET | /planner/tasks/{id} | Get task |
| PATCH | /planner/tasks/{id} | Update task |
| PATCH | /planner/tasks/{id}/status | Update task status |
| DELETE | /planner/tasks/{id} | Delete task |
| POST | /planner/generate | Generate AI roadmap |
| GET | /planner/daily | Daily planner |
| GET | /planner/weekly | Weekly planner |
| POST | /planner/tasks/{id}/complete | Complete task |
| GET | /planner/progress | Progress dashboard |
| GET | /planner/recommendations | AI recommendations |

---

# Internal Processing Flow

```text
User Goal

↓

AI Planner

↓

Roadmap Generation

↓

Weekly Schedule

↓

Daily Tasks

↓

Task Completion

↓

Progress Analysis

↓

AI Feedback

↓

Updated Roadmap
```

---

# Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|201|Task Created|
|400|Validation Error|
|401|Unauthorized|
|404|Task Not Found|
|500|Internal Server Error|

# 15. Agent APIs

The Agent module manages the orchestration of specialized AI agents responsible for handling different user requests.

Instead of relying on a single LLM prompt, AI Concierge routes requests to specialized agents such as Chat, RAG, Memory, Planner, and Recommendation agents. This modular design improves response quality, scalability, and maintainability.

---

# 15.1 Execute Agent

### Endpoint

```http
POST /agents/execute
```

### Authentication

✅ Required

---

### Description

Executes the appropriate AI agent based on the user request.

---

### Request

```json
{
    "conversation_id": "conv_001",
    "message": "Create a 12-week roadmap to learn MLOps."
}
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "agent": "planner_agent",
        "response": "Here is your personalized 12-week roadmap...",
        "execution_time_ms": 2350
    }
}
```

---

# 15.2 Agent Router

### Endpoint

```http
POST /agents/router
```

---

### Description

Determines which agent(s) should handle the request.

---

### Example

User Message

```
Summarize my uploaded NLP notes.
```

Selected Agent

```
rag_agent
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "selected_agent": "rag_agent",
        "confidence": 0.97
    }
}
```

---

# 15.3 List Available Agents

### Endpoint

```http
GET /agents
```

---

### Description

Returns all available AI agents.

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "name": "chat_agent",
            "description": "General conversation"
        },
        {
            "name": "rag_agent",
            "description": "Document-based question answering"
        },
        {
            "name": "memory_agent",
            "description": "Long-term memory retrieval"
        },
        {
            "name": "planner_agent",
            "description": "Study planning and task generation"
        },
        {
            "name": "recommendation_agent",
            "description": "Personalized suggestions"
        }
    ]
}
```

---

# 15.4 Get Agent Details

### Endpoint

```http
GET /agents/{agent_name}
```

---

### Description

Returns metadata about a specific agent.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "name": "rag_agent",
        "version": "1.0",
        "status": "active",
        "supported_tools": [
            "Vector Search",
            "Document Parser",
            "Citation Generator"
        ]
    }
}
```

---

# 15.5 Agent Execution History

### Endpoint

```http
GET /agents/history
```

---

### Description

Returns previous agent executions.

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| page | Page number |
| limit | Results per page |

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "execution_id": "exec_001",
            "agent": "planner_agent",
            "status": "completed",
            "execution_time_ms": 2310,
            "created_at": "2026-08-01T10:00:00Z"
        }
    ]
}
```

---

# 15.6 Retry Agent Execution

### Endpoint

```http
POST /agents/history/{execution_id}/retry
```

---

### Description

Retries a previous agent execution.

---

### Success Response

```json
{
    "success": true,
    "message": "Execution restarted."
}
```

---

# 15.7 Streaming Agent Response

### Endpoint

```http
POST /agents/stream
```

---

### Description

Streams responses from the selected agent.

---

### Transport

```
Server-Sent Events (SSE)
```

Future

```
WebSockets
```

---

# 15.8 Multi-Agent Workflow

### Endpoint

```http
POST /agents/workflow
```

---

### Description

Executes multiple agents sequentially or in parallel.

---

### Request

```json
{
    "conversation_id": "conv_001",
    "message": "Create a study plan based on my uploaded ML notes."
}
```

---

### Example Workflow

```
Router Agent

↓

Memory Agent

↓

RAG Agent

↓

Planner Agent

↓

Recommendation Agent

↓

Response Generator
```

---

### Success Response

```json
{
    "success": true,
    "data": {
        "agents_used": [
            "memory_agent",
            "rag_agent",
            "planner_agent"
        ],
        "response": "Based on your uploaded notes, here is your personalized study plan..."
    }
}
```

---

# 15.9 Agent Health Check

### Endpoint

```http
GET /agents/health
```

---

### Description

Returns the health status of all registered agents.

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "agent": "chat_agent",
            "status": "healthy"
        },
        {
            "agent": "rag_agent",
            "status": "healthy"
        },
        {
            "agent": "planner_agent",
            "status": "healthy"
        }
    ]
}
```

---

# Supported Agents

| Agent | Responsibility |
|---------|----------------|
| chat_agent | General conversations |
| router_agent | Intent classification and routing |
| rag_agent | Retrieval-Augmented Generation |
| memory_agent | Long-term memory retrieval |
| planner_agent | Study plans and task generation |
| recommendation_agent | Personalized recommendations |

---

# Agent Routing Logic

```text
User Request

↓

Authentication

↓

Router Agent

↓

Intent Detection

↓

Memory Retrieval

↓

Document Retrieval

↓

Planner (if needed)

↓

Recommendation (if needed)

↓

LLM Response

↓

Store Conversation

↓

Return Response
```

---

# Agent Execution Lifecycle

```text
Receive Request

↓

Validate JWT

↓

Identify Intent

↓

Select Agent

↓

Execute Tools

↓

Collect Context

↓

Construct Prompt

↓

Call LLM

↓

Validate Output

↓

Store Response

↓

Return Result
```

---

# Agent API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /agents/execute | Execute an agent |
| POST | /agents/router | Route request to agent |
| GET | /agents | List available agents |
| GET | /agents/{agent_name} | Get agent details |
| GET | /agents/history | Execution history |
| POST | /agents/history/{id}/retry | Retry execution |
| POST | /agents/stream | Stream responses |
| POST | /agents/workflow | Execute multi-agent workflow |
| GET | /agents/health | Agent health status |

---

# Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|400|Invalid Request|
|401|Unauthorized|
|404|Agent Not Found|
|409|Workflow Conflict|
|500|Agent Execution Failed|
|503|Agent Temporarily Unavailable|

---

# Future Enhancements

Future versions of the Agent module may include:

- Dynamic agent registration
- Agent marketplace
- Tool discovery
- Parallel workflow execution
- Human-in-the-loop approvals
- Cost-aware agent selection
- Agent performance analytics
- Automatic workflow optimization

# 16. Recommendation APIs

The Recommendation module generates personalized suggestions based on user behavior, learning progress, long-term memory, uploaded documents, planner tasks, and conversation history.

Unlike standard chat responses, recommendations are proactive and personalized.

---

# 16.1 Get Personalized Recommendations

### Endpoint

```http
GET /recommendations
```

### Authentication

✅ Required

---

### Description

Returns personalized recommendations for the authenticated user.

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| category | Optional recommendation category |
| limit | Maximum number of recommendations |

---

### Example

```http
GET /recommendations?category=learning&limit=5
```

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "recommendation_id": "rec_001",
            "category": "learning",
            "title": "Study Attention Mechanism",
            "description": "Based on your recent conversations, this topic will strengthen your understanding of Transformers.",
            "priority": "High",
            "confidence": 0.94
        }
    ]
}
```

---

# 16.2 Get Learning Recommendations

### Endpoint

```http
GET /recommendations/learning
```

---

### Description

Returns AI-generated learning suggestions.

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "title": "Complete Azure AI-900",
            "reason": "You have already completed 75% of the syllabus."
        },
        {
            "title": "Start MLOps",
            "reason": "Recommended after AI-900."
        }
    ]
}
```

---

# 16.3 Get Project Recommendations

### Endpoint

```http
GET /recommendations/projects
```

---

### Description

Suggests projects based on the user's interests, skills, and learning progress.

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "title": "Build a Medical RAG Assistant",
            "difficulty": "Intermediate",
            "estimated_duration": "4 weeks"
        }
    ]
}
```

---

# 16.4 Get Resource Recommendations

### Endpoint

```http
GET /recommendations/resources
```

---

### Description

Returns recommended learning resources.

---

### Query Parameters

| Parameter | Description |
|------------|-------------|
| topic | Learning topic |

---

### Example

```http
GET /recommendations/resources?topic=RAG
```

---

### Success Response

```json
{
    "success": true,
    "data": [
        {
            "title": "Attention Is All You Need",
            "type": "Research Paper"
        },
        {
            "title": "LangChain Documentation",
            "type": "Documentation"
        }
    ]
}
```

---

# 16.5 Get Daily Recommendations

### Endpoint

```http
GET /recommendations/daily
```

---

### Description

Returns personalized recommendations for the current day.

---

### Success Response

```json
{
    "success": true,
    "data": {
        "tasks": [
            "Complete today's MLOps lesson",
            "Review yesterday's planner tasks",
            "Revise Transformer architecture"
        ]
    }
}
```

---

# 16.6 Dismiss Recommendation

### Endpoint

```http
PATCH /recommendations/{recommendation_id}/dismiss
```

---

### Description

Marks a recommendation as dismissed.

---

### Success Response

```json
{
    "success": true,
    "message": "Recommendation dismissed."
}
```

---

# 16.7 Feedback on Recommendation

### Endpoint

```http
POST /recommendations/{recommendation_id}/feedback
```

---

### Description

Collects user feedback to improve recommendation quality.

---

### Request

```json
{
    "rating": 5,
    "helpful": true,
    "comment": "This recommendation was very useful."
}
```

---

### Success Response

```json
{
    "success": true,
    "message": "Feedback received."
}
```

---

# Recommendation Categories

Supported categories include:

- Learning
- Projects
- Certifications
- Study Plans
- Books
- Courses
- Research Papers
- Productivity
- Career
- Skills

---

# Recommendation Generation Pipeline

```text
User Activity

↓

Conversation History

↓

Long-Term Memory

↓

Planner Progress

↓

Uploaded Documents

↓

Recommendation Engine

↓

Ranking Algorithm

↓

Top Recommendations

↓

User Dashboard
```

---

# Recommendation Ranking Factors

Recommendations are ranked using multiple signals:

| Factor | Description |
|---------|-------------|
| User Goals | Career and learning goals |
| Memory | Stored long-term preferences |
| Planner | Current task progress |
| Conversation History | Recently discussed topics |
| Uploaded Documents | Available study material |
| Feedback Score | Previous user ratings |
| Recency | Recent interactions |
| Priority | AI-assigned importance |

---

# Recommendation API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /recommendations | Personalized recommendations |
| GET | /recommendations/learning | Learning recommendations |
| GET | /recommendations/projects | Project ideas |
| GET | /recommendations/resources | Learning resources |
| GET | /recommendations/daily | Daily recommendations |
| PATCH | /recommendations/{id}/dismiss | Dismiss recommendation |
| POST | /recommendations/{id}/feedback | Submit recommendation feedback |

---

# Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|400|Invalid Request|
|401|Unauthorized|
|404|Recommendation Not Found|
|500|Internal Server Error|

---

# Future Enhancements

Future improvements may include:

- Real-time recommendations
- Collaborative filtering
- Personalized course sequencing
- Calendar-aware recommendations
- Deadline-aware recommendations
- Team recommendations
- Recommendation explainability
- Reinforcement learning from user feedback

# 17. Health & Monitoring APIs

The Health module provides endpoints for monitoring the availability and operational status of the AI Concierge platform and its dependent services.

---

## 17.1 System Health Check

### Endpoint

```http
GET /health
```

### Authentication

❌ Not Required

---

### Description

Returns the overall health status of the backend.

---

### Success Response

```json
{
    "status": "healthy",
    "timestamp": "2026-08-01T14:35:20Z",
    "version": "1.0.0"
}
```

---

## 17.2 Detailed Health Status

### Endpoint

```http
GET /health/details
```

### Authentication

✅ Required (Admin)

---

### Success Response

```json
{
    "backend": "healthy",
    "database": "healthy",
    "vector_database": "healthy",
    "llm_provider": "healthy",
    "storage": "healthy",
    "cache": "healthy"
}
```

---

## 17.3 Readiness Probe

### Endpoint

```http
GET /health/ready
```

Returns whether the application is ready to receive requests.

---

## 17.4 Liveness Probe

### Endpoint

```http
GET /health/live
```

Returns whether the application process is alive.

---

## 17.5 Metrics

### Endpoint

```http
GET /metrics
```

Returns Prometheus-compatible metrics.

---

## Health API Summary

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /health | Basic health check |
| GET | /health/details | Detailed service health |
| GET | /health/ready | Kubernetes readiness |
| GET | /health/live | Kubernetes liveness |
| GET | /metrics | Prometheus metrics |

---

# 18. API Error Handling

All APIs return errors using a standardized format.

---

## Standard Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": [
        {
            "field": "email",
            "message": "Email already exists."
        }
    ]
}
```

---

## Common Error Codes

| HTTP Status | Meaning |
|-------------|----------|
|200|Success|
|201|Resource Created|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|413|Payload Too Large|
|415|Unsupported Media Type|
|422|Validation Error|
|429|Too Many Requests|
|500|Internal Server Error|
|503|Service Unavailable|

---

## Business Error Codes

| Code | Description |
|------|-------------|
|AUTH_001|Invalid Credentials|
|AUTH_002|Expired Token|
|USER_001|User Not Found|
|DOC_001|Unsupported File|
|DOC_002|Document Processing Failed|
|CHAT_001|Conversation Not Found|
|CHAT_002|Message Too Long|
|MEM_001|Memory Not Found|
|PLAN_001|Task Not Found|
|AGENT_001|Agent Execution Failed|
|RAG_001|Vector Search Failed|

---

# 19. Pagination

Endpoints returning collections use pagination.

---

## Request

```http
GET /documents?page=1&limit=20
```

---

## Response

```json
{
    "success": true,
    "pagination": {
        "page": 1,
        "limit": 20,
        "total_pages": 8,
        "total_records": 145
    },
    "data": []
}
```

---

## Pagination Parameters

| Parameter | Default | Maximum |
|------------|----------|----------|
| page | 1 | Unlimited |
| limit | 20 | 100 |

---

# 20. Filtering & Sorting

Many endpoints support filtering.

Example

```http
GET /planner/tasks?status=completed
```

Sorting

```http
GET /documents?sort=uploaded_at&order=desc
```

---

# 21. Rate Limiting

To prevent abuse, APIs enforce rate limits.

---

## Default Limits

| Endpoint | Limit |
|-----------|-------|
| Authentication | 10 requests/minute |
| Chat | 60 requests/minute |
| Upload | 20 requests/hour |
| Planner | 100 requests/hour |
| Recommendations | 100 requests/hour |

---

### Rate Limit Response

```json
{
    "success": false,
    "message": "Rate limit exceeded."
}
```

HTTP Status

```
429 Too Many Requests
```

---

# 22. API Versioning

Current version

```
v1
```

Base URL

```
/api/v1/
```

Future

```
/api/v2/
```

Older versions remain supported during migration.

---

# 23. Security

All APIs follow security best practices.

Authentication

- JWT Access Tokens

Authorization

- User-specific data access

Transport

- HTTPS

Passwords

- bcrypt hashing

Secrets

- Environment variables

Validation

- Pydantic models

---

# 24. Streaming APIs

Future versions will support streaming AI responses.

Endpoint

```http
POST /agents/stream
```

Technology

- Server-Sent Events (SSE)

Future

- WebSockets

---

## Streaming Flow

```
User Message

↓

Agent

↓

LLM

↓

Stream Tokens

↓

Frontend

↓

Render Response
```

---

# 25. OpenAPI Standards

The backend automatically generates documentation.

Available endpoints

```
/docs
```

Swagger UI

```
FastAPI Swagger Interface
```

Alternative

```
/redoc
```

---

# 26. API Lifecycle

```
Client Request

↓

Authentication

↓

Validation

↓

Business Logic

↓

Database

↓

Vector Search (Optional)

↓

LLM (Optional)

↓

Response Formatting

↓

JSON Response
```

---

# 27. API Design Principles

The API follows these principles:

- RESTful architecture
- Stateless communication
- Consistent response format
- Predictable endpoints
- Versioned APIs
- Secure by default
- Comprehensive validation
- Standard HTTP status codes

---

# 28. Future APIs

The following APIs are planned for future releases.

## Notifications

```
GET /notifications
POST /notifications
PATCH /notifications/{id}
```

---

## Calendar Integration

```
GET /calendar/events
POST /calendar/events
```

---

## Email Integration

```
POST /email/send
```

---

## Voice Assistant

```
POST /voice/transcribe
POST /voice/synthesize
```

---

## Code Execution

```
POST /code/run
```

---

## External Integrations

```
Google Calendar
GitHub
Notion
Google Drive
Microsoft OneDrive
Slack
Microsoft Teams
```

---

# Appendix A – Authentication Header

```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

# Appendix B – Standard Success Response

```json
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": {}
}
```

---

# Appendix C – Standard Error Response

```json
{
    "success": false,
    "message": "Validation failed.",
    "errors": []
}
```

---

# Appendix D – API Modules

| Module | Status |
|----------|--------|
| Authentication | MVP |
| Users | MVP |
| Conversations | MVP |
| Messages | MVP |
| Documents | MVP |
| Memory | MVP |
| Planner | MVP |
| Agents | MVP |
| Recommendations | MVP |
| Health | MVP |
| Notifications | Future |
| Calendar | Future |
| Voice | Future |
| Code Execution | Future |

---

# Summary

The AI Concierge REST API provides a secure, scalable, and modular interface for user authentication, conversations, AI-powered messaging, document management, long-term memory, study planning, multi-agent orchestration, personalized recommendations, and system monitoring. Built on RESTful principles with JWT authentication, standardized responses, and versioned endpoints, it is designed to support both the MVP and future enterprise-scale enhancements while maintaining consistency, extensibility, and developer-friendly integration.
