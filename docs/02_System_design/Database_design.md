# Database Design

> Project: AI Concierge – Personalized AI Assistant

> Version: 1.0

> Status: Draft

---

# Table of Contents

1. Introduction
2. Database Overview
3. Database Technology Stack
4. High-Level Database Architecture
5. Entity Relationship Diagram
6. Tables
7. Relationships
8. Indexing Strategy
9. Constraints
10. Data Lifecycle
11. Backup Strategy
12. Future Improvements

---

# 1. Introduction

The AI Concierge platform stores structured application data using PostgreSQL and semantic vector data using Qdrant.

The architecture separates transactional data from vector embeddings to improve scalability and retrieval performance.

---

# 2. Database Overview

The platform uses two databases:

## PostgreSQL

Stores:

- Users
- Conversations
- Messages
- Planner Tasks
- Long-Term Memories
- Uploaded Document Metadata
- Recommendations
- Agent Logs

---

## Qdrant

Stores:

- Document Embeddings
- Memory Embeddings
- Semantic Search Index
- Retrieval Metadata

---

# 3. Database Technology Stack

| Component | Technology |
|------------|------------|
| Relational Database | PostgreSQL |
| Vector Database | Qdrant |
| ORM | SQLAlchemy |
| Migration Tool | Alembic |
| Cache | Redis (Future) |

---

# 4. High-Level Architecture

```text
                React Frontend
                      │
                      ▼
                 FastAPI Backend
                      │
      ┌───────────────┴───────────────┐
      ▼                               ▼
 PostgreSQL                      Qdrant
(Structured Data)          (Vector Embeddings)
```

---

# 5. Core Tables

## Users

Stores account information.

Fields:

- id (UUID)
- full_name
- email
- password_hash
- role
- created_at
- updated_at

---

## Conversations

Stores chat sessions.

Fields:

- id
- user_id
- title
- created_at
- updated_at

---

## Messages

Stores every chat message.

Fields:

- id
- conversation_id
- sender (user/assistant)
- content
- token_count
- model_used
- created_at

---

## Documents

Stores uploaded document metadata.

Fields:

- id
- user_id
- filename
- storage_path
- file_size
- mime_type
- status
- uploaded_at

---

## Memories

Stores long-term user memories.

Fields:

- id
- user_id
- category
- memory_text
- importance_score
- embedding_id
- created_at

---

## Planner Tasks

Stores learning plans and productivity tasks.

Fields:

- id
- user_id
- title
- description
- status
- priority
- due_date
- completed_at

---

## Recommendations

Stores AI-generated recommendations.

Fields:

- id
- user_id
- category
- title
- description
- confidence
- dismissed
- created_at

---

## Agent Executions

Stores execution history for AI agents.

Fields:

- id
- conversation_id
- selected_agent
- execution_time_ms
- status
- created_at

---

# 6. Relationships

User

├── Conversations

├── Documents

├── Memories

├── Planner Tasks

├── Recommendations

└── Agent Logs

Conversation

└── Messages

Document

└── Multiple Vector Embeddings (Qdrant)

Memory

└── One Vector Embedding (Qdrant)

---

# 7. Entity Relationships

```text
User
 │
 ├──── Conversations
 │          │
 │          └──── Messages
 │
 ├──── Documents
 │
 ├──── Memories
 │
 ├──── Planner Tasks
 │
 ├──── Recommendations
 │
 └──── Agent Logs
```

---

# 8. Indexing Strategy

Indexes improve query performance.

Examples:

Users

- email

Conversations

- user_id

Messages

- conversation_id

Planner

- user_id
- due_date

Documents

- user_id
- filename

Memories

- user_id
- category

---

# 9. Constraints

Examples

- Email must be unique.
- One message belongs to one conversation.
- One conversation belongs to one user.
- Cascade delete enabled.
- UUID primary keys.

---

# 10. Data Lifecycle

Conversation

Create

↓

Store Messages

↓

Retrieve

↓

Archive (Future)

↓

Delete

---

Document

Upload

↓

Extract Text

↓

Chunk

↓

Embedding

↓

Store in Qdrant

↓

Delete

---

# 11. Backup Strategy

PostgreSQL

- Daily backup
- Point-in-time recovery

Qdrant

- Snapshot backups
- Weekly export

---

# 12. Future Improvements

- Multi-tenant architecture
- Read replicas
- Database sharding
- Redis caching
- Soft delete
- Audit logs
- Encryption at rest

---

# Summary

The AI Concierge platform follows a hybrid database architecture, using PostgreSQL for transactional data and Qdrant for vector embeddings. This separation ensures efficient CRUD operations, scalable semantic search, and a clean foundation for Retrieval-Augmented Generation (RAG), personalized memory, and multi-agent workflows.
