# Database Design

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 1.0

> **Status:** Draft

---

# 1. Purpose

This document defines the database architecture of AI Concierge.

The system uses two complementary databases:

- PostgreSQL for structured relational data.
- Qdrant for semantic vector search.

Separating relational and vector data allows the system to efficiently manage user information while supporting Retrieval-Augmented Generation (RAG) and semantic memory retrieval.

---

# 2. Database Architecture

```
                    AI Concierge

                         │

        ┌────────────────┴────────────────┐

        ▼                                 ▼

 PostgreSQL                         Qdrant

(Relational Data)             (Vector Database)

        │                                 │

 Users                           Document Embeddings

 Conversations                   Memory Embeddings

 Messages                        Semantic Search

 Planner                         Similarity Search

 Settings

 Metadata
```

---

# 3. PostgreSQL Tables

The MVP contains the following tables.

| Table | Purpose |
|---------|---------|
| users | User accounts |
| user_preferences | Personalization settings |
| conversations | Chat sessions |
| messages | Individual chat messages |
| memories | Long-term memory |
| documents | Uploaded documents |
| planner_tasks | Study planner |
| audit_logs | System activity |

---

# 4. users Table

Stores registered users.

| Column | Type | Constraints |
|---------|------|-------------|
| id | UUID | Primary Key |
| full_name | VARCHAR(100) | Not Null |
| email | VARCHAR(255) | Unique |
| password_hash | TEXT | Not Null |
| role | VARCHAR(20) | Default: user |
| created_at | TIMESTAMP | Not Null |
| updated_at | TIMESTAMP | Not Null |

---

# 5. user_preferences Table

Stores personalization settings.

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID (FK users.id) |
| preferred_language | VARCHAR |
| response_style | VARCHAR |
| theme | VARCHAR |
| timezone | VARCHAR |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

# 6. conversations Table

Each chat session is stored here.

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| title | VARCHAR |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

One conversation contains many messages.

---

# 7. messages Table

Stores every chat message.

| Column | Type |
|---------|------|
| id | UUID |
| conversation_id | UUID |
| sender | ENUM(user, assistant) |
| content | TEXT |
| model_name | VARCHAR |
| tokens_used | INTEGER |
| created_at | TIMESTAMP |

---

# 8. memories Table

Stores personalized long-term memory.

Examples:

- Career goal
- Preferred language
- Learning style
- Interests

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| category | VARCHAR |
| memory_text | TEXT |
| importance_score | FLOAT |
| created_at | TIMESTAMP |
| updated_at | TIMESTAMP |

---

# 9. documents Table

Stores uploaded document metadata.

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| filename | VARCHAR |
| original_filename | VARCHAR |
| file_size | BIGINT |
| mime_type | VARCHAR |
| upload_status | VARCHAR |
| page_count | INTEGER |
| storage_path | TEXT |
| uploaded_at | TIMESTAMP |

---

# 10. planner_tasks Table

Stores user study plans.

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| title | VARCHAR |
| description | TEXT |
| due_date | DATE |
| status | VARCHAR |
| priority | VARCHAR |
| created_at | TIMESTAMP |

---

# 11. audit_logs Table

Tracks important system events.

Examples:

- Login
- Logout
- Upload
- Delete
- Password change

| Column | Type |
|---------|------|
| id | UUID |
| user_id | UUID |
| action | VARCHAR |
| entity | VARCHAR |
| entity_id | UUID |
| created_at | TIMESTAMP |

---

# 12. Table Relationships

```
User

│

├──────── Preferences

│

├──────── Conversations

│            │

│            └──────── Messages

│

├──────── Documents

│

├──────── Memories

│

├──────── Planner Tasks

│

└──────── Audit Logs
```

---

# 13. Entity Relationships

```
Users

1 ─────── N Conversations

1 ─────── N Documents

1 ─────── N Memories

1 ─────── N Planner Tasks

1 ─────── 1 Preferences

Conversation

1 ─────── N Messages
```

---

# 14. Indexing Strategy

Indexes improve query performance.

Recommended indexes:

```
users.email

messages.conversation_id

documents.user_id

memories.user_id

planner_tasks.user_id

conversations.user_id
```

Future indexes:

- Full-text search
- Date indexes
- Composite indexes

---

# 15. Soft Delete Strategy

For MVP:

- Hard delete

Future:

```
deleted_at TIMESTAMP
```

Allows recovery of accidentally deleted records.

---

# 16. Audit Fields

Every major table contains:

```
created_at

updated_at
```

Future:

```
created_by

updated_by

deleted_at
```

---

# 17. Constraints

Examples:

Email:

Unique

Password:

Not Null

User ID:

Foreign Key

Conversation ID:

Foreign Key

Message Sender:

ENUM

Status:

CHECK Constraint

---

# 18. Qdrant Collections

Unlike PostgreSQL, Qdrant stores vectors.

Collections:

```
documents

memories
```

---

# 19. Document Vector Schema

Each document chunk contains:

```
chunk_id

document_id

user_id

text

embedding

page_number

metadata
```

---

# 20. Memory Vector Schema

Each stored memory contains:

```
memory_id

user_id

memory_text

embedding

importance_score

metadata
```

---

# 21. Data Flow

### Chat Flow

```
User

↓

Conversation

↓

Message

↓

Memory

↓

LLM

↓

Assistant Response

↓

Message Stored
```

---

### Document Flow

```
Upload

↓

Metadata

↓

Extract Text

↓

Chunk

↓

Embedding

↓

Qdrant
```

---

# 22. Backup Strategy

PostgreSQL

- Daily backups
- WAL (future)

Qdrant

- Snapshot backups
- Collection export

---

# 23. Security

The database should enforce:

- Foreign key constraints
- Least privilege database users
- Encrypted credentials
- Parameterized SQL queries
- Regular backups
- Secure connection strings

---

# 24. Scaling Strategy

Future improvements:

- Read replicas
- Connection pooling
- Table partitioning
- Redis caching
- Horizontal vector database scaling

---

# 25. Summary

The AI Concierge database architecture combines PostgreSQL for structured relational data with Qdrant for semantic vector search. This hybrid design enables efficient user management, conversation storage, personalization, document retrieval, and Retrieval-Augmented Generation while remaining scalable and maintainable for future growth.

---

# Appendix A – PostgreSQL Tables

| Table | Description |
|---------|-------------|
| users | User accounts |
| user_preferences | User settings |
| conversations | Chat sessions |
| messages | Chat history |
| memories | Long-term memory |
| documents | Uploaded file metadata |
| planner_tasks | Study planner |
| audit_logs | Activity tracking |

---

# Appendix B – Qdrant Collections

| Collection | Purpose |
|------------|----------|
| documents | Document chunk embeddings |
| memories | Long-term memory embeddings |
