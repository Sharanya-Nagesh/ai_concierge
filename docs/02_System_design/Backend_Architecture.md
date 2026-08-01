# Backend Architecture

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 2.0

> **Status:** Draft

---

# 1. Purpose

This document describes the backend architecture of AI Concierge.

The backend serves as the central orchestration layer that manages authentication, user profiles, conversations, document processing, long-term memory, Retrieval-Augmented Generation (RAG), AI agents, and communication with Large Language Models (LLMs).

The architecture follows a **layered, modular, service-oriented design** to ensure scalability, maintainability, and ease of testing.

---

# 2. Design Goals

The backend is designed to be:

- Modular
- Stateless where possible
- Scalable
- Secure
- Testable
- AI-first
- Cloud-ready
- Easy to extend

---

# 3. Technology Stack

| Layer | Technology |
|---------|------------|
| Framework | FastAPI |
| Language | Python 3.12+ |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Authentication | JWT |
| Database | PostgreSQL |
| Vector Database | Qdrant |
| AI Framework | LangChain |
| LLM | Gemini (Configurable) |
| Dependency Management | Poetry / uv |
| Containerization | Docker |

---

# 4. High-Level Backend Architecture

```
                 Client (React)
                       │
                 REST API Requests
                       │
                       ▼
                FastAPI Application
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Authentication     API Router      Middleware
                       │
                       ▼
               Business Services
      ┌────────────────┼──────────────────┐
      ▼                ▼                  ▼
 Chat Service   Document Service   Memory Service
      ▼                ▼                  ▼
 Agent Layer    RAG Pipeline      Planner Service
      └────────────────┼──────────────────┘
                       ▼
                  LLM Gateway
                       ▼
                  Gemini API
```

---

# 5. Layered Architecture

The backend follows five logical layers.

```
Presentation Layer

↓

Application Layer

↓

Business Logic Layer

↓

AI Layer

↓

Data Layer
```

---

# 6. Presentation Layer

Responsible for:

- REST endpoints
- Request validation
- Response serialization
- HTTP status codes
- Authentication checks

Example endpoints:

```
POST /chat

POST /documents/upload

GET /history

GET /memory

POST /planner
```

Business logic is **never implemented in API routes**.

---

# 7. Application Layer

Coordinates incoming requests.

Responsibilities:

- Dependency Injection
- Request validation
- Service orchestration
- Transaction management
- Exception handling

This layer connects API routes to backend services.

---

# 8. Business Logic Layer

Contains independent services.

```
services/

chat_service.py

memory_service.py

document_service.py

planner_service.py

recommendation_service.py

user_service.py

history_service.py
```

Each service performs one well-defined responsibility.

Example:

`ChatService`

- Receives user message
- Retrieves context
- Invokes Agent Orchestrator
- Saves conversation
- Returns formatted response

---

# 9. Agent Layer

The Agent Layer decides **how to answer** a user's request.

```
             User Prompt
                    │
                    ▼
            Intent Classifier
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
 Memory Agent   RAG Agent   Planner Agent
      │             │             │
      └─────────────┼─────────────┘
                    ▼
            Prompt Builder
                    ▼
              LLM Gateway
                    ▼
              Final Response
```

Responsibilities:

- Detect intent
- Retrieve memories
- Retrieve documents
- Build prompts
- Call LLM
- Validate output

---

# 10. LLM Gateway

The backend communicates with external LLM providers through a dedicated gateway.

Advantages:

- Model independence
- Centralized API management
- Retry handling
- Cost tracking
- Logging

Supported providers:

- Gemini
- OpenAI (Future)
- Anthropic Claude (Future)
- Local models (Future)

The rest of the backend remains unaware of the specific LLM provider.

---

# 11. RAG Integration

Document workflow:

```
Upload PDF

↓

Extract Text

↓

Chunk Document

↓

Generate Embeddings

↓

Store in Qdrant
```

Query workflow:

```
User Question

↓

Embedding

↓

Similarity Search

↓

Top-k Chunks

↓

Prompt Construction

↓

LLM

↓

Response
```

---

# 12. Memory Integration

The Memory Service manages long-term personalization.

Workflow:

```
Conversation

↓

Memory Extractor

↓

Important?

↓

Store

↓

Retrieve in Future
```

Stored memories include:

- Preferred language
- Learning goals
- Interests
- Response style
- User preferences

---

# 13. Database Access

PostgreSQL stores:

- Users
- Conversations
- Messages
- Profiles
- Memories
- Metadata

Qdrant stores:

- Document embeddings
- Memory embeddings

Repositories abstract database operations.

Example:

```
UserRepository

ConversationRepository

DocumentRepository

MemoryRepository
```

Services never execute raw SQL directly.

---

# 14. File Handling

Uploaded documents are processed by the Document Service.

Pipeline:

```
Upload

↓

Virus Scan (Future)

↓

Validation

↓

Storage

↓

Text Extraction

↓

Chunking

↓

Embedding

↓

Indexing
```

Supported formats (MVP):

- PDF

Future:

- DOCX
- PPTX
- TXT

---

# 15. API Communication Flow

```
Frontend

↓

POST /chat

↓

FastAPI

↓

Chat Service

↓

Agent Orchestrator

↓

LLM

↓

Response

↓

Frontend
```

---

# 16. Error Handling

The backend uses centralized exception handling.

Common errors:

| Error | HTTP Code |
|--------|-----------|
| Validation Error | 400 |
| Unauthorized | 401 |
| Forbidden | 403 |
| Resource Not Found | 404 |
| Internal Server Error | 500 |

Errors returned to users are friendly and do not expose internal implementation details.

---

# 17. Logging

The backend logs:

- API requests
- Errors
- Authentication events
- Document uploads
- LLM latency
- Vector search latency
- Memory retrieval

Sensitive information such as passwords or API keys is never logged.

---

# 18. Security

The backend implements:

- JWT authentication
- bcrypt password hashing
- HTTPS (production)
- Input validation
- Authorization checks
- File type validation
- Prompt injection mitigation
- SQL injection prevention

---

# 19. Scalability

The architecture supports future scaling by introducing:

- Redis caching
- Celery background workers
- Kafka event streaming
- Kubernetes
- Load balancing
- Horizontal API scaling

These additions require minimal changes because services are already modular.

---

# 20. Project Structure

```
backend/

├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── agents/
│   ├── rag/
│   ├── memory/
│   ├── auth/
│   ├── utils/
│   └── main.py
│
├── tests/
├── uploads/
├── alembic/
├── Dockerfile
├── pyproject.toml
└── .env
```

---

# 21. Backend Request Lifecycle

```
User sends request

↓

Authentication

↓

Input Validation

↓

Route Handler

↓

Business Service

↓

Agent Layer

↓

RAG / Memory

↓

LLM

↓

Response Validation

↓

Database Update

↓

HTTP Response
```

---

# 22. Future Enhancements

Planned improvements include:

- Streaming LLM responses
- WebSocket support
- Background document processing
- Voice transcription
- Image understanding
- Multi-agent collaboration
- Graph RAG
- Real-time notifications

---

# 23. Summary

The AI Concierge backend is designed around modular services and an AI orchestration layer. Each responsibility—authentication, memory, document retrieval, planning, and response generation—is isolated into dedicated components. This architecture enables rapid feature development while remaining scalable and maintainable as the platform evolves into a production-grade AI system.
