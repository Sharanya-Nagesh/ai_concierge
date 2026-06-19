# AI Concierge - Repository Structure

## Goal

Create a production-grade repository structure inspired by industry AI systems.

---

# Repository Layout

```text
ai-concierge/

├── docs/
│
├── backend/
│
├── frontend/
│
├── infrastructure/
│
├── tests/
│
├── .github/
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# Backend Structure

```text
backend/

├── app/
│
├── tests/
│
├── alembic/
│
├── requirements.txt
│
└── Dockerfile
```

---

# App Structure

```text
app/

├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── agents/
├── rag/
├── memory/
├── tools/
├── utils/
├── middleware/
└── main.py
```

---

# api/

Contains API routes.

```text
api/

├── auth.py
├── users.py
├── chat.py
├── documents.py
└── health.py
```

Responsibilities:

* Route definitions
* Request handling
* Response handling

---

# core/

Application configuration.

```text
core/

├── config.py
├── security.py
├── logging.py
└── constants.py
```

---

# db/

Database setup.

```text
db/

├── session.py
├── base.py
└── migrations/
```

---

# models/

SQLAlchemy models.

```text
models/

├── user.py
├── preference.py
├── session.py
├── conversation.py
├── message.py
└── document.py
```

---

# schemas/

Pydantic schemas.

```text
schemas/

├── auth.py
├── user.py
├── chat.py
└── document.py
```

---

# services/

Business logic.

```text
services/

├── auth_service.py
├── user_service.py
├── chat_service.py
├── document_service.py
└── llm_service.py
```

---

# agents/

Agent implementations.

```text
agents/

├── intent_agent.py
├── memory_agent.py
├── retrieval_agent.py
├── tool_agent.py
└── response_agent.py
```

---

# rag/

RAG pipeline.

```text
rag/

├── parser.py
├── chunker.py
├── embeddings.py
├── retriever.py
└── vector_store.py
```

---

# memory/

Memory subsystem.

```text
memory/

├── short_term.py
├── long_term.py
├── summarizer.py
└── profile_manager.py
```

---

# tools/

External tool integrations.

```text
tools/

├── calculator.py
├── search.py
└── external_apis.py
```

---

# utils/

Helper utilities.

```text
utils/

├── helpers.py
├── validators.py
└── exceptions.py
```

---

# Frontend Structure

```text
frontend/

├── src/
│
├── public/
│
├── package.json
│
└── Dockerfile
```

---

# Frontend src/

```text
src/

├── components/
├── pages/
├── services/
├── hooks/
├── contexts/
├── routes/
└── App.tsx
```

---

# Infrastructure

```text
infrastructure/

├── docker/
├── monitoring/
├── deployment/
└── scripts/
```

---

# Monitoring

```text
monitoring/

├── prometheus.yml
└── grafana/
```

---

# CI/CD

```text
.github/

├── workflows/
│
└── ISSUE_TEMPLATE/
```

Workflow examples:

```text
backend-test.yml
frontend-test.yml
docker-build.yml
deploy.yml
```

---

# Tests

```text
tests/

├── unit/
├── integration/
├── api/
└── performance/
```

---

# Development Phases

Phase 1:

* api
* core
* db
* models
* schemas

Phase 2:

* services
* frontend

Phase 3:

* rag

Phase 4:

* memory

Phase 5:

* agents

Phase 6:

* monitoring
* deployment

---

# Repository Design Principles

* Modular
* Testable
* Scalable
* Production-ready
* Clean Architecture
* Separation of Concerns
* MLOps Friendly
