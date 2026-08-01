# Technology Stack

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 1.0

> **Status:** Draft

---

# 1. Purpose

This document describes the technology stack chosen for AI Concierge and explains why each technology was selected.

Rather than simply listing programming languages and frameworks, this document provides the rationale behind each decision. These choices are guided by the project's goals of scalability, maintainability, modularity, developer productivity, and production readiness.

---

# 2. Technology Stack Overview

| Layer | Technology |
|---------|------------|
| Frontend | React + TypeScript |
| UI Components | Shadcn/UI |
| Styling | Tailwind CSS |
| Backend | FastAPI |
| Language | Python 3.12+ |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Relational Database | PostgreSQL |
| Vector Database | Qdrant |
| AI Framework | LangChain |
| Embedding Model | BAAI/bge-small-en-v1.5 (initial) |
| LLM | Gemini 2.x (configurable) |
| File Storage | Local Storage (MVP) |
| Containerization | Docker |
| Reverse Proxy | Nginx |
| Version Control | Git + GitHub |
| API Documentation | OpenAPI (Swagger) |
| Deployment | Docker Compose (MVP) |

---

# 3. Frontend Stack

## React

React is chosen because:

- Component-based architecture
- Large ecosystem
- Easy state management
- Excellent community support
- Widely adopted in industry

React allows the frontend to be modular and reusable.

---

## TypeScript

TypeScript improves:

- Code safety
- Autocomplete
- Refactoring
- Maintainability
- Developer productivity

Since the project is expected to grow, static typing reduces future bugs.

---

## Tailwind CSS

Tailwind CSS enables:

- Rapid UI development
- Consistent styling
- Responsive layouts
- Minimal custom CSS

---

## Shadcn/UI

Shadcn/UI provides:

- Modern components
- Accessibility
- Easy customization
- Clean design

It integrates naturally with React and Tailwind CSS.

---

# 4. Backend Stack

## FastAPI

FastAPI is selected because it provides:

- High performance
- Automatic API documentation
- Async support
- Type validation
- Easy integration with AI libraries

It is one of the most popular backend frameworks for AI applications.

---

## Python

Python is selected because:

- Excellent AI ecosystem
- Rich NLP libraries
- Easy integration with LLMs
- Large community support

Libraries such as LangChain, Transformers, and PyTorch integrate naturally with Python.

---

# 5. Database Layer

## PostgreSQL

Stores:

- Users
- Conversations
- Messages
- Memories
- Settings
- Metadata

Advantages:

- ACID compliance
- Reliability
- Mature ecosystem
- Strong indexing support
- Excellent performance

---

## Qdrant

Qdrant stores vector embeddings for semantic search.

Used for:

- Document retrieval
- Semantic search
- Memory retrieval
- RAG pipeline

Advantages:

- Fast vector search
- Metadata filtering
- Open source
- Easy Docker deployment

---

# 6. AI Stack

## LangChain

LangChain provides:

- Prompt management
- RAG pipeline utilities
- Tool calling
- Memory integration
- Agent workflows

---

## Gemini

Gemini is initially selected because:

- Strong reasoning capabilities
- Long context window
- Multimodal support
- Competitive API pricing

The architecture is model-agnostic, allowing future replacement with OpenAI, Claude, or open-source models.

---

## Embedding Model

Initial model:

BAAI/bge-small-en-v1.5

Reasons:

- Good retrieval quality
- Lightweight
- Fast inference
- Open source

Future upgrades may include multilingual embedding models to improve support for Indian languages.

---

# 7. Authentication

JWT (JSON Web Token)

Provides:

- Stateless authentication
- Scalable session management
- Easy API integration

Passwords will be hashed using bcrypt before storage.

---

# 8. File Storage

### MVP

Uploaded documents are stored on the local file system.

Advantages:

- Simple setup
- Easy debugging
- Suitable for development

### Future

Cloud object storage such as Amazon S3 or Azure Blob Storage.

---

# 9. Containerization

Docker will be used to package:

- Backend
- Frontend
- PostgreSQL
- Qdrant
- Nginx

Benefits:

- Consistent environments
- Simplified deployment
- Easy onboarding

---

# 10. Reverse Proxy

Nginx will:

- Route requests
- Serve frontend assets
- Handle HTTPS termination
- Support load balancing in future

---

# 11. Development Tools

| Tool | Purpose |
|------|---------|
| Git | Version Control |
| GitHub | Repository Hosting |
| VS Code | Development |
| Postman | API Testing |
| Docker Desktop | Local Containers |
| pgAdmin | PostgreSQL Management |
| Qdrant Dashboard | Vector Database Inspection |

---

# 12. Documentation

Documentation will include:

- Swagger/OpenAPI
- Markdown design documents
- Mermaid diagrams
- Architecture diagrams

---

# 13. Future Technologies

The architecture is designed to accommodate future additions such as:

- Redis (caching)
- Celery (background jobs)
- Kafka (event streaming)
- Kubernetes (container orchestration)
- Prometheus (metrics)
- Grafana (monitoring)
- MinIO (object storage)
- Elasticsearch (advanced search)

These are intentionally deferred until they solve a real scaling or operational need.

---

# 14. Technology Selection Principles

The technology stack follows these principles:

- Open-source first where practical
- Production-ready frameworks
- Strong community support
- Active maintenance
- Easy learning curve
- Scalability
- Modular architecture

---

# 15. Summary

The selected technology stack balances simplicity for an MVP with the flexibility to evolve into a production-grade AI platform. Each technology has been chosen to support modular development, maintainability, and future scalability while leveraging modern AI engineering practices.

---

## Stack Summary

| Category | Technology |
|----------|------------|
| Frontend | React + TypeScript + Tailwind CSS + Shadcn/UI |
| Backend | FastAPI + Python |
| Database | PostgreSQL |
| Vector Store | Qdrant |
| AI Framework | LangChain |
| LLM | Gemini (Configurable) |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Authentication | JWT + bcrypt |
| Storage | Local (MVP), Cloud (Future) |
| Deployment | Docker + Nginx |
| Version Control | Git + GitHub |
