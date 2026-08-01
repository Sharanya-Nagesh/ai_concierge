# System Architecture

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 1.0

> **Status:** Draft

---

# 1. Purpose

This document describes the overall architecture of AI Concierge.

It explains how the major software components interact to deliver a personalized AI assistant capable of conversational AI, document understanding, long-term memory, multilingual communication, and intelligent recommendations.

This serves as the blueprint for backend, frontend, database, and AI system development.

---

# 2. High-Level Architecture

```
                        ┌─────────────────────┐
                        │       User          │
                        └──────────┬──────────┘
                                   │
                            HTTPS Requests
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │ React Frontend (UI)      │
                    └──────────┬───────────────┘
                               │ REST API
                               ▼
                    ┌──────────────────────────┐
                    │ FastAPI Backend          │
                    └──────────┬───────────────┘
                               │
               ┌───────────────┼────────────────┐
               ▼               ▼                ▼
        Authentication    Agent System     File Service
               │               │                │
               ▼               ▼                ▼
         PostgreSQL     Agent Orchestrator    Storage
                               │
         ┌─────────────────────┼──────────────────────┐
         ▼                     ▼                      ▼
    Memory Agent         Retrieval Agent       Planner Agent
         │                     │                      │
         ▼                     ▼                      ▼
    PostgreSQL            Qdrant Vector DB      PostgreSQL
                               │
                               ▼
                      Gemini / OpenAI LLM
                               │
                               ▼
                          AI Response
                               │
                               ▼
                          React Frontend
```

---

# 3. Architecture Goals

The architecture is designed with the following goals:

- Modular
- Scalable
- Maintainable
- Extensible
- Secure
- AI-first
- Production-ready

---

# 4. Major Components

The system consists of six major layers.

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

↓

Infrastructure Layer
```

---

# 5. Presentation Layer

Technology

- React
- TypeScript
- Tailwind CSS
- Shadcn/UI

Responsibilities

- Display UI
- Handle user interactions
- Render chat
- Upload documents
- Manage authentication
- Display AI responses
- Settings management

This layer contains **no business logic**.

---

# 6. Application Layer

Technology

- FastAPI

Responsibilities

- API routing
- Authentication
- Validation
- Request processing
- Response formatting
- Session management

Every frontend request enters the system through this layer.

---

# 7. Business Logic Layer

Contains all application services.

Examples

- Chat Service
- User Service
- Memory Service
- Document Service
- Planner Service
- Recommendation Service

Each service performs one responsibility.

---

# 8. AI Layer

The AI layer is the heart of AI Concierge.

It consists of multiple specialized agents coordinated by an Agent Orchestrator.

```
                    User Prompt
                         │
                         ▼
                 Intent Detection
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   Memory Agent    Retrieval Agent   Planner Agent
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                  Prompt Builder
                         │
                         ▼
                     Gemini LLM
                         │
                         ▼
                  Response Validator
                         │
                         ▼
                   Final Response
```

---

# 9. Agent Responsibilities

## Intent Agent

Determines:

- User intent
- Required services
- Query type

Example

```
Explain CNN

↓

Intent = General Question
```

---

## Memory Agent

Responsible for:

- Retrieve user preferences
- Retrieve goals
- Store new memories
- Update memories

---

## Retrieval Agent

Responsibilities

- Search uploaded documents
- Semantic retrieval
- Chunk ranking
- Citation generation

---

## Planner Agent

Creates:

- Study plans
- Weekly schedules
- Productivity plans

---

## Response Generator

Builds final prompt.

Calls LLM.

Formats response.

---

# 10. Data Layer

Two databases are used.

---

## PostgreSQL

Stores

- Users
- Chats
- Messages
- Memory
- Settings
- Metadata

---

## Qdrant

Stores

- Document embeddings
- Memory embeddings
- Semantic vectors

Used for

- RAG
- Similarity Search

---

# 11. File Storage

MVP

```
uploads/

    user_id/

        pdfs/

        images/
```

Future

Amazon S3

Azure Blob

Google Cloud Storage

---

# 12. Request Flow

Example

User asks

```
Explain Attention Mechanism.
```

Flow

```
User

↓

Frontend

↓

FastAPI

↓

Authentication

↓

Intent Detection

↓

Memory Retrieval

↓

Need RAG?

↓

YES

↓

Vector Search

↓

Retrieve Chunks

↓

Prompt Builder

↓

Gemini

↓

Response

↓

Frontend
```

---

# 13. Document Upload Flow

```
Upload PDF

↓

FastAPI

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

# 14. Conversation Flow

```
User Message

↓

Retrieve Conversation Context

↓

Retrieve Memory

↓

Retrieve Documents

↓

Merge Context

↓

Prompt Engineering

↓

LLM

↓

Validate

↓

Store Conversation

↓

Display Response
```

---

# 15. Authentication Flow

```
Login

↓

Verify Password

↓

Generate JWT

↓

Return Token

↓

Frontend Stores Token

↓

Authenticated APIs
```

---

# 16. Memory Flow

```
Conversation

↓

Memory Extractor

↓

Important?

↓

Yes

↓

Store Memory

↓

Future Conversation

↓

Retrieve Memory
```

---

# 17. RAG Flow

```
Upload PDF

↓

Text Extraction

↓

Chunking

↓

Embeddings

↓

Qdrant

↓

User Query

↓

Similarity Search

↓

Top-k Chunks

↓

Prompt

↓

LLM
```

---

# 18. API Communication

Frontend communicates with FastAPI using REST APIs.

Example endpoints

```
POST /auth/login

POST /chat

POST /documents/upload

GET /history

GET /memory

PUT /profile

DELETE /conversation/{id}
```

---

# 19. Error Handling Strategy

The architecture follows graceful degradation.

Examples

If vector database is unavailable:

- Continue normal chat
- Inform user that document search is temporarily unavailable

If memory retrieval fails:

- Continue conversation without personalization

If LLM API fails:

- Retry once
- Return user-friendly error

---

# 20. Security Architecture

Security measures include:

- JWT Authentication
- Password hashing (bcrypt)
- HTTPS
- Input validation
- User-level authorization
- SQL injection protection
- Prompt injection mitigation
- Rate limiting (future)

---

# 21. Scalability Strategy

The architecture supports future horizontal scaling.

Future improvements include:

- Redis caching
- Celery workers
- Kubernetes
- Load balancer
- Object storage
- Monitoring
- Event queues

No architectural redesign should be required to add these components.

---

# 22. Deployment Architecture

```
                Internet
                     │
                     ▼
                Nginx Reverse Proxy
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
   React Frontend          FastAPI Backend
                                    │
             ┌──────────────────────┼─────────────────────┐
             ▼                      ▼                     ▼
      PostgreSQL              Qdrant Vector DB      File Storage
                                    │
                                    ▼
                               Gemini API
```

---

# 23. Design Principles

The architecture follows these principles:

- Single Responsibility
- Separation of Concerns
- Loose Coupling
- High Cohesion
- API-first Design
- Modular Components
- Cloud-ready Deployment
- AI-first Architecture

---

# 24. Future Evolution

Version 2

- Voice assistant
- Email assistant
- Calendar integration

Version 3

- Multi-agent collaboration
- Mobile application
- Workflow automation

Version 4

- Enterprise deployment
- Team workspaces
- Knowledge graphs
- Graph RAG

---

# 25. Summary

The AI Concierge architecture is designed as a modular AI platform where each component has a clearly defined responsibility.

The separation between frontend, backend, business services, AI agents, databases, and infrastructure enables the project to evolve from an MVP into a production-grade system without major architectural changes.

This document serves as the high-level blueprint that guides the detailed design of backend services, database schema, APIs, memory management, RAG pipeline, and deployment.
