# AI Concierge - Entity Relationship (ER) Diagram

## Purpose

This document defines the relational database structure for the AI Concierge platform.

---

# High-Level ER Diagram

```text
User
 │
 ├── UserPreference
 │
 ├── Session
 │      │
 │      └── Conversation
 │              │
 │              └── Message
 │
 ├── Document
 │      │
 │      └── DocumentChunk
 │
 ├── Feedback
 │
 └── AuditLog
```

---

# Entity Definitions

## User

Stores account information.

| Field         | Type      | Description        |
| ------------- | --------- | ------------------ |
| id            | UUID      | Primary Key        |
| username      | VARCHAR   | Unique username    |
| email         | VARCHAR   | Unique email       |
| password_hash | VARCHAR   | Encrypted password |
| created_at    | TIMESTAMP | Account creation   |
| updated_at    | TIMESTAMP | Last modification  |

Relationship:

```text
User
├── UserPreference
├── Session
├── Document
├── Feedback
└── AuditLog
```

---

## UserPreference

Stores personalization settings.

| Field            | Type      |
| ---------------- | --------- |
| id               | UUID      |
| user_id          | UUID FK   |
| response_style   | VARCHAR   |
| interests        | JSONB     |
| budget           | VARCHAR   |
| food_preferences | VARCHAR   |
| created_at       | TIMESTAMP |

Example:

```json
{
  "response_style":"detailed",
  "interests":["AI","Research"],
  "budget":"medium"
}
```

---

## Session

Represents a login session.

| Field      | Type      |
| ---------- | --------- |
| id         | UUID      |
| user_id    | UUID FK   |
| created_at | TIMESTAMP |
| expires_at | TIMESTAMP |

Relationship:

```text
User 1 ---- N Session
```

---

## Conversation

Stores chat threads.

| Field      | Type      |
| ---------- | --------- |
| id         | UUID      |
| session_id | UUID FK   |
| title      | VARCHAR   |
| created_at | TIMESTAMP |

Relationship:

```text
Session 1 ---- N Conversation
```

---

## Message

Stores chat messages.

| Field           | Type      |
| --------------- | --------- |
| id              | UUID      |
| conversation_id | UUID FK   |
| role            | VARCHAR   |
| content         | TEXT      |
| timestamp       | TIMESTAMP |

Roles:

```text
user
assistant
system
tool
```

Relationship:

```text
Conversation 1 ---- N Message
```

---

## Document

Stores uploaded files.

| Field       | Type      |
| ----------- | --------- |
| id          | UUID      |
| user_id     | UUID FK   |
| filename    | VARCHAR   |
| file_path   | VARCHAR   |
| upload_date | TIMESTAMP |

Relationship:

```text
User 1 ---- N Document
```

---

## DocumentChunk

Stores chunk metadata.

| Field       | Type    |
| ----------- | ------- |
| id          | UUID    |
| document_id | UUID FK |
| chunk_index | INTEGER |
| chunk_text  | TEXT    |
| vector_id   | VARCHAR |

Relationship:

```text
Document 1 ---- N DocumentChunk
```

Note:

Actual embeddings reside in Qdrant.

---

## Feedback

Stores user ratings.

| Field      | Type    |
| ---------- | ------- |
| id         | UUID    |
| user_id    | UUID FK |
| message_id | UUID FK |
| rating     | INTEGER |
| comment    | TEXT    |

Values:

```text
1–5
```

---

## AuditLog

Tracks important events.

| Field     | Type      |
| --------- | --------- |
| id        | UUID      |
| user_id   | UUID FK   |
| action    | VARCHAR   |
| timestamp | TIMESTAMP |

Examples:

```text
LOGIN
UPLOAD_DOCUMENT
DELETE_DOCUMENT
UPDATE_PROFILE
```

---

# Future Entities

## Recommendation

Stores generated recommendations.

## AgentTrace

Stores execution traces from agents.

## ToolUsage

Stores tool invocation metrics.

## Analytics

Stores user activity summaries.

---

# Database Strategy

Relational Data:

* PostgreSQL

Vector Data:

* Qdrant

Cache (Future):

* Redis

---

# Design Principles

* UUID-based primary keys
* Soft-delete support
* Auditability
* Scalability
* Separation of relational and vector storage
