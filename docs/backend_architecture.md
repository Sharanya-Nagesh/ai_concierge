# AI Concierge - Backend Architecture

## Purpose

This document defines the architecture of the backend system, including:

* FastAPI application structure
* Dependency flow
* Authentication design
* Service layer architecture
* Repository pattern
* Agent orchestration
* RAG integration
* Memory integration
* Database access strategy

---

# Architectural Principles

The backend follows:

* Clean Architecture
* Separation of Concerns
* Dependency Injection
* Repository Pattern
* Service Layer Pattern
* Modular Design

Goals:

* Easy testing
* Easy maintenance
* Scalability
* Extensibility

---

# Backend Overview

```text
Frontend

↓

API Layer

↓

Service Layer

↓

Agent Layer

↓

RAG / Memory / Tools

↓

Repository Layer

↓

PostgreSQL + Qdrant
```

---

# Request Lifecycle

Example:

User asks:

"Summarize Chapter 2 of my uploaded PDF"

Flow:

```text
React Frontend

↓

POST /chat/message

↓

Chat Router

↓

Chat Service

↓

Agent Orchestrator

↓

Intent Agent

↓

Retrieval Agent

↓

RAG Pipeline

↓

LLM Service

↓

Response Agent

↓

Chat Service

↓

API Response
```

---

# FastAPI Application Structure

```text
app/

├── api/
├── core/
├── db/
├── repositories/
├── services/
├── agents/
├── rag/
├── memory/
├── tools/
├── models/
├── schemas/
├── middleware/
└── main.py
```

---

# API Layer

Location:

```text
app/api/
```

Purpose:

* Define endpoints
* Validate requests
* Return responses

No business logic allowed.

Example:

```python
@router.post("/chat/message")
async def send_message():
    pass
```

The router only calls services.

---

# Service Layer

Location:

```text
app/services/
```

Purpose:

* Business logic
* Workflow coordination
* Validation rules

Examples:

```text
AuthService
UserService
ChatService
DocumentService
```

---

# Repository Layer

Location:

```text
app/repositories/
```

Purpose:

* Database operations only

Example:

```text
UserRepository

create_user()

get_user()

update_user()
```

Benefits:

* Database abstraction
* Easier testing
* Easier migration

---

# Database Access Pattern

Incorrect:

```text
Router
 ↓
Database
```

Correct:

```text
Router
 ↓
Service
 ↓
Repository
 ↓
Database
```

This keeps the architecture clean.

---

# Dependency Injection

FastAPI Dependencies:

```python
Depends()
```

Example:

```text
Database Session

↓

Repository

↓

Service

↓

Router
```

Benefits:

* Testability
* Loose coupling

---

# Authentication Architecture

## Login Flow

```text
User

↓

POST /auth/login

↓

AuthService

↓

UserRepository

↓

Password Verification

↓

JWT Generation

↓

Response
```

---

## Protected Endpoint

```text
JWT

↓

Auth Middleware

↓

Current User

↓

Protected Route
```

---

# JWT Strategy

Access Token:

```text
15 minutes
```

Refresh Token:

```text
7 days
```

Stored:

```text
HTTP-only Cookie
```

Future:

```text
Redis-based token blacklist
```

---

# Chat Architecture

## Chat Service Responsibilities

* Create conversations
* Save messages
* Trigger agents
* Return responses

Example:

```text
send_message()

↓

store user message

↓

orchestrator.run()

↓

store AI response

↓

return response
```

---

# Agent Architecture

## Why Agents?

Different responsibilities should be isolated.

Instead of:

```text
One giant prompt
```

Use:

```text
Multiple specialized modules
```

---

# Agent Orchestrator

Location:

```text
agents/orchestrator.py
```

Responsibilities:

* Coordinate agents
* Route tasks
* Merge outputs

---

# Intent Agent

Responsibilities:

Classify request type.

Outputs:

```text
CHAT

RAG_QUERY

TOOL_CALL

RECOMMENDATION
```

Example:

```text
"What is Chapter 2 about?"

↓

RAG_QUERY
```

---

# Memory Agent

Responsibilities:

Retrieve:

* User profile
* Past conversations
* Conversation summaries

Output:

Relevant memory context.

---

# Retrieval Agent

Responsibilities:

* Query vector database
* Retrieve document chunks

Output:

Relevant chunks.

---

# Tool Agent

Responsibilities:

Execute:

* Calculator
* Search
* APIs

Future:

* Calendar
* Email
* Maps

---

# Response Agent

Responsibilities:

Combine:

* User prompt
* Memory
* Retrieved documents
* Tool outputs

Generate final prompt.

Call LLM.

Return response.

---

# Memory Architecture

## Short-Term Memory

Source:

Current conversation

Storage:

PostgreSQL

Window:

Last N messages

---

## Long-Term Memory

Source:

Conversation summaries

Storage:

PostgreSQL

Purpose:

Persistent personalization

---

## User Profile Memory

Stores:

```json
{
  "response_style":"detailed",
  "interests":["AI"],
  "budget":"medium"
}
```

Used in every response.

---

# RAG Architecture

## Upload Flow

```text
PDF Upload

↓

Parser

↓

Chunker

↓

Embedding Model

↓

Qdrant
```

---

## Query Flow

```text
Question

↓

Embedding

↓

Similarity Search

↓

Top K Chunks

↓

LLM Context
```

---

# Qdrant Strategy

Store:

```text
vector
metadata
document_id
chunk_id
```

Do NOT store embeddings in PostgreSQL.

---

# LLM Architecture

Location:

```text
services/llm_service.py
```

Responsibilities:

* Prompt templates
* Model invocation
* Retry handling
* Response formatting

Supported Models:

```text
Gemini

OpenAI

Llama

Mistral

Qwen
```

Through adapter pattern.

---

# Error Handling

Centralized exception handling.

Location:

```text
middleware/
```

Examples:

```text
Authentication Error

Validation Error

Database Error

LLM Error
```

---

# Logging Architecture

Structured JSON logs.

Track:

```text
Request ID

User ID

Latency

Errors

Agent Decisions
```

Destination:

```text
Console

File

Future:
Grafana
```

---

# Monitoring

Metrics:

```text
Request Count

Response Time

LLM Latency

Database Latency

Token Usage
```

Tools:

```text
Prometheus

Grafana
```

---

# Testing Strategy

## Unit Tests

Test:

* Services
* Repositories
* Agents

---

## Integration Tests

Test:

* Database
* APIs

---

## End-to-End Tests

Test:

Complete user flows.

---

# Future Scalability

Current:

```text
Monolithic Backend
```

Future:

```text
Microservices

Memory Service

RAG Service

Agent Service

Authentication Service
```

Only if scale requires it.

---

# Version 1 Scope

Must Build:

✓ Authentication

✓ Chat

✓ User Profiles

✓ Memory

✓ RAG

✓ Agent Orchestrator

✓ Docker

✓ PostgreSQL

✓ Qdrant

---

# Version 2 Scope

Future:

✓ Voice Assistant

✓ Multi-modal Inputs

✓ Recommendation Engine

✓ Multi-Agent Planning

✓ Cloud Deployment

✓ Kubernetes
