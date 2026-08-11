# AI Concierge — Folder Structure

## 1. Overview

This document defines the canonical repository structure for the AI Concierge project.

The repository is organized into clearly separated areas for:

- Product documentation
- System design
- Backend documentation
- Machine learning
- MLOps / LLMOps
- Development documentation
- Backend implementation
- Frontend implementation
- Infrastructure
- Testing
- CI/CD
- Architecture diagrams

The structure is designed to support:

- Modularity
- Maintainability
- Scalability
- Testability
- Production readiness
- MLOps / LLMOps
- Clear separation of concerns
- Easy onboarding and collaboration


---

# 2. Complete Repository Structure

```text
ai-concierge/
│
├── docs/
│   │
│   ├── product/
│   │   ├── PRD.md
│   │   ├── Project_Overview.md
│   │   ├── Vision.md
│   │   ├── User_Personas.md
│   │   ├── User_Stories.md
│   │   ├── Functional_Requirements.md
│   │   ├── Non_Functional_Requirements.md
│   │   ├── Feature_Walkthrough.md
│   │   └── UI_Walkthrough.md
│   │
│   ├── system_design/
│   │   ├── Technology_Stack.md
│   │   ├── System_Architecture.md
│   │   ├── Frontend_Architecture.md
│   │   ├── Backend_Architecture.md
│   │   ├── Authentication.md
│   │   ├── Database_Design.md
│   │   ├── ER_Diagram.md
│   │   ├── API_Spec.md
│   │   ├── Memory_Architecture.md
│   │   ├── Agent_Design.md
│   │   ├── RAG_Design.md
│   │   ├── Security.md
│   │   ├── Deployment.md
│   │   ├── Testing.md
│   │   ├── Monitoring.md
│   │   ├── Evaluation.md
│   │   └── Decision_Log.md
│   │
│   ├── development/
│   │   ├── Folder_Structure.md
│   │   ├── Coding_Standards.md
│   │   ├── Git_Workflow.md
│   │   ├── Environment_Setup.md
│   │   ├── Local_Development.md
│   │   ├── Deployment_Guide.md
│   │   └── Troubleshooting.md
│   │
│   ├── mlops/
│   │   ├── MLOps_Pipeline.md
│   │   ├── LLMOps.md
│   │   ├── CI_CD.md
│   │   ├── Model_Versioning.md
│   │   ├── Prompt_Versioning.md
│   │   ├── Monitoring_AI.md
│   │   └── Evaluation_Framework.md
│   │
│   ├── diagrams/
│   │   ├── system_architecture.png
│   │   ├── er_diagram.png
│   │   ├── backend_flow.png
│   │   ├── rag_pipeline.png
│   │   ├── memory_pipeline.png
│   │   └── ui_wireframes.png
│   │
│   └── README.md
│
│
├── backend_docs/
│   ├── Backend_Architecture.md
│   ├── API_Spec.md
│   ├── Authentication.md
│   ├── Database_Design.md
│   ├── ER_Diagram.md
│   ├── Backend_Flow.md
│   ├── Service_Layer.md
│   ├── Agent_Backend_Integration.md
│   ├── RAG_Backend_Integration.md
│   ├── Memory_Backend_Integration.md
│   ├── Error_Handling.md
│   ├── Logging.md
│   ├── Configuration.md
│   ├── Background_Tasks.md
│   ├── Caching.md
│   ├── Security.md
│   ├── Testing.md
│   ├── Deployment.md
│   └── README.md
│
│
├── ml/
│   ├── ML_Architecture.md
│   ├── Dataset.md
│   ├── Data_Preprocessing.md
│   ├── Multilingual_NLP.md
│   ├── Intent_Classification.md
│   ├── Embeddings.md
│   ├── RAG.md
│   ├── Retrieval.md
│   ├── Reranking.md
│   ├── LLM.md
│   ├── Prompt_Engineering.md
│   ├── Fine_Tuning.md
│   ├── Memory_Models.md
│   ├── Recommendation_System.md
│   ├── Evaluation.md
│   ├── AI_Safety.md
│   └── README.md
│
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   └── health.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   │
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── base.py
│   │   │   └── migrations/
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── preference.py
│   │   │   ├── session.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   └── document.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── chat.py
│   │   │   └── document.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── document_service.py
│   │   │   └── llm_service.py
│   │   │
│   │   ├── agents/
│   │   │   ├── intent_agent.py
│   │   │   ├── memory_agent.py
│   │   │   ├── retrieval_agent.py
│   │   │   ├── tool_agent.py
│   │   │   └── response_agent.py
│   │   │
│   │   ├── rag/
│   │   │   ├── parser.py
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   │
│   │   ├── memory/
│   │   │   ├── short_term.py
│   │   │   ├── long_term.py
│   │   │   ├── summarizer.py
│   │   │   └── profile_manager.py
│   │   │
│   │   ├── tools/
│   │   │   ├── calculator.py
│   │   │   ├── search.py
│   │   │   └── external_apis.py
│   │   │
│   │   ├── utils/
│   │   │   ├── helpers.py
│   │   │   ├── validators.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── middleware/
│   │   │   └── ...
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   │
│   ├── alembic/
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── contexts/
│   │   ├── routes/
│   │   └── App.tsx
│   │
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
│
├── infrastructure/
│   ├── docker/
│   ├── monitoring/
│   │   ├── prometheus.yml
│   │   └── grafana/
│   │
│   ├── deployment/
│   └── scripts/
│
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── performance/
│
│
├── .github/
│   ├── workflows/
│   │   ├── backend-test.yml
│   │   ├── frontend-test.yml
│   │   ├── docker-build.yml
│   │   └── deploy.yml
│   │
│   └── ISSUE_TEMPLATE/
│
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```


---

# 3. Folder Responsibilities

## `docs/`

Contains high-level project documentation.

```text
docs/
├── product/
├── system_design/
├── development/
├── mlops/
└── diagrams/
```

### `docs/product/`

Defines:

- What the product is
- Why it exists
- Who uses it
- User requirements
- Functional requirements
- Non-functional requirements
- Feature and UI walkthroughs


### `docs/system_design/`

Defines the overall technical architecture.

Contains:

- Technology decisions
- System architecture
- Frontend architecture
- Backend architecture
- Authentication
- Database design
- ER diagram
- API specification
- Memory architecture
- Agent design
- RAG design
- Security
- Deployment
- Testing
- Monitoring
- Evaluation
- Architecture decision records


### `docs/development/`

Defines how developers work with the project.

Contains:

- Repository structure
- Coding standards
- Git workflow
- Environment setup
- Local development
- Deployment workflow
- Troubleshooting


### `docs/mlops/`

Defines how ML and LLM systems are operated.

Contains:

- MLOps pipeline
- LLMOps
- CI/CD
- Model versioning
- Prompt versioning
- AI monitoring
- Evaluation framework


### `docs/diagrams/`

Contains architecture and workflow diagrams.


---

# 4. `backend_docs/`

Contains detailed backend-specific documentation.

This folder is intentionally separate from:

```text
docs/system_design/
```

because the two have different purposes.

### `docs/system_design/`

Answers:

> How is the overall system architected?

### `backend_docs/`

Answers:

> How is the backend implemented?

Backend documentation includes:

- Backend architecture
- API implementation
- Authentication
- Database implementation
- Backend flow
- Service layer
- Agent integration
- RAG integration
- Memory integration
- Error handling
- Logging
- Configuration
- Background tasks
- Caching
- Security
- Testing
- Deployment


---

# 5. `ml/`

Contains the detailed AI/ML documentation.

This folder is separate from:

```text
docs/mlops/
```

because ML methodology and ML operations are different concerns.

### `ml/`

Focuses on:

- Datasets
- Data preprocessing
- NLP
- Intent classification
- Embeddings
- RAG
- Retrieval
- Reranking
- LLMs
- Prompt engineering
- Fine-tuning
- Memory models
- Recommendations
- AI evaluation
- AI safety


### `docs/mlops/`

Focuses on:

- ML lifecycle
- Model deployment
- Versioning
- CI/CD
- Monitoring
- Evaluation operations
- LLMOps


---

# 6. `backend/`

Contains the actual backend source code.

The backend follows a layered structure:

```text
API
 ↓
Services
 ↓
Models / Database
```

with specialized AI components:

```text
Agents
RAG
Memory
Tools
```

### `api/`

HTTP API endpoints.

### `core/`

Application configuration and security.

### `db/`

Database connections and migrations.

### `models/`

Database models.

### `schemas/`

Pydantic request/response schemas.

### `services/`

Application and business logic.

### `agents/`

Agent orchestration.

### `rag/`

Retrieval-Augmented Generation implementation.

### `memory/`

Short-term and long-term memory implementation.

### `tools/`

Tools that agents can invoke.

### `utils/`

Reusable helper functions.

### `middleware/`

Cross-cutting request processing.


---

# 7. `frontend/`

Contains the frontend application.

```text
frontend/src/

├── components/
├── pages/
├── services/
├── hooks/
├── contexts/
├── routes/
└── App.tsx
```

### `components/`

Reusable UI components.

### `pages/`

Application pages.

### `services/`

API communication.

### `hooks/`

Reusable frontend hooks.

### `contexts/`

Global state and shared application context.

### `routes/`

Frontend routing.


---

# 8. `infrastructure/`

Contains deployment and operational infrastructure.

```text
infrastructure/

├── docker/
├── monitoring/
├── deployment/
└── scripts/
```

### `docker/`

Docker-related configuration.

### `monitoring/`

Monitoring infrastructure.

### `deployment/`

Deployment configuration.

### `scripts/`

Infrastructure automation.


---

# 9. `tests/`

Contains repository-level tests.

```text
tests/

├── unit/
├── integration/
├── api/
└── performance/
```

### Unit

Individual functions and modules.

### Integration

Interactions between components.

### API

API contracts and endpoint behavior.

### Performance

Latency, throughput, concurrency, and resource usage.


---

# 10. `.github/`

Contains GitHub automation.

```text
.github/

├── workflows/
└── ISSUE_TEMPLATE/
```

Workflows can handle:

- Automated testing
- Docker builds
- CI
- Deployment


---

# 11. Root-Level Files

## `.env.example`

Contains example environment variables.

No real secrets should be committed.

---

## `docker-compose.yml`

Defines the local multi-service development environment.

---

## `README.md`

Provides the main project introduction and instructions.

---

## `LICENSE`

Defines project licensing.


---

# 12. Separation of Responsibilities

The repository follows this conceptual separation:

```text
                    AI CONCIERGE
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
    PRODUCT           SYSTEM             CODE
    DOCS              DESIGN
       │                 │                 │
       │                 │          ┌──────┴──────┐
       │                 │          │             │
       ▼                 ▼          ▼             ▼
 docs/product     docs/system   backend       frontend
                         │
              ┌──────────┼──────────┐
              │                     │
              ▼                     ▼
       backend_docs                 ml
              │                     │
              ▼                     ▼
      Backend Details        AI/ML Details
                         │
                         ▼
                    docs/mlops/
                         │
                         ▼
                   ML/LLM Operations
```


---

# 13. Documentation vs Implementation

A key principle of this repository is:

```text
Documentation
        ≠
Implementation
```

For example:

```text
docs/system_design/API_Spec.md
```

describes the API architecture and contract.

While:

```text
backend/app/api/
```

contains the actual API implementation.

Similarly:

```text
ml/RAG.md
```

documents the RAG methodology.

While:

```text
backend/app/rag/
```

contains the backend implementation of the RAG pipeline.

---

# 14. High-Level Data and AI Flow

The repository structure reflects the following conceptual system:

```text
User
 │
 ▼
Frontend
 │
 ▼
Backend API
 │
 ▼
Agent / Orchestration
 │
 ├───────────────┐
 │               │
 ▼               ▼
Memory          RAG
 │               │
 ▼               ▼
Database       Vector DB
 │               │
 └───────┬───────┘
         ▼
        LLM
         │
         ▼
      Response
         │
         ▼
      Frontend
```

The corresponding implementation is distributed across:

```text
frontend/
backend/app/api/
backend/app/agents/
backend/app/memory/
backend/app/rag/
backend/app/services/
ml/
```

---

# 15. Development Principles

The repository follows these principles:

1. **Separation of concerns**
2. **Single responsibility**
3. **Modularity**
4. **Loose coupling**
5. **Testability**
6. **Scalability**
7. **Security by design**
8. **Observability**
9. **Reproducibility**
10. **Documentation-driven development**

---

# 16. Naming Conventions

Documentation files use:

```text
PascalCase_With_Underscores.md
```

Examples:

```text
System_Architecture.md
Database_Design.md
Memory_Architecture.md
User_Stories.md
```

Python files use:

```text
snake_case.py
```

Examples:

```text
chat_service.py
vector_store.py
profile_manager.py
```

Frontend TypeScript/React components may use:

```text
PascalCase.tsx
```

Examples:

```text
ChatWindow.tsx
RewardCard.tsx
UserProfile.tsx
```

---

# 17. Growth Strategy

The structure is designed to grow without reorganizing the entire repository.

As the project becomes more sophisticated:

```text
backend/
    ↓
More services and modules

ml/
    ↓
More ML components and experiments

backend_docs/
    ↓
More implementation documentation

docs/mlops/
    ↓
More production ML lifecycle documentation

infrastructure/
    ↓
More deployment and monitoring components

tests/
    ↓
More comprehensive test suites
```

New files should be added according to responsibility rather than convenience.


---

# 18. Rules for Adding New Files

Before adding a new file, determine what it represents.

### Product requirement

```text
docs/product/
```

### System-level architecture

```text
docs/system_design/
```

### Backend implementation documentation

```text
backend_docs/
```

### ML / AI documentation

```text
ml/
```

### Developer workflow

```text
docs/development/
```

### MLOps / LLMOps

```text
docs/mlops/
```

### Backend source code

```text
backend/
```

### Frontend source code

```text
frontend/
```

### Infrastructure

```text
infrastructure/
```

### Tests

```text
tests/
```

### Diagrams

```text
docs/diagrams/
```


---

# 19. Canonical Structure

The following structure is the final canonical structure for the project:

```text
ai-concierge/
│
├── docs/
│   ├── product/
│   ├── system_design/
│   ├── development/
│   ├── mlops/
│   ├── diagrams/
│   └── README.md
│
├── backend_docs/
│
├── ml/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── agents/
│   │   ├── rag/
│   │   ├── memory/
│   │   ├── tools/
│   │   ├── utils/
│   │   ├── middleware/
│   │   └── main.py
│   │
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── contexts/
│   │   ├── routes/
│   │   └── App.tsx
│   │
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── infrastructure/
│   ├── docker/
│   ├── monitoring/
│   ├── deployment/
│   └── scripts/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── api/
│   └── performance/
│
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```


---

# 20. Final Rule

This document is the **single source of truth for the AI Concierge repository structure**.

All future documentation and implementation should follow this structure.

Do not introduce alternate top-level folders such as:

```text
backend_documentation/
ml_docs/
ai/
server/
application/
```

unless the architecture is explicitly revised.

The established separation is:

```text
docs/
    → General project documentation

backend_docs/
    → Backend-specific documentation

ml/
    → ML/AI-specific documentation

backend/
    → Backend source code

frontend/
    → Frontend source code

infrastructure/
    → Infrastructure and deployment

tests/
    → Repository-level testing

.github/
    → CI/CD and GitHub configuration
```

Any future structural change should be documented as an architectural decision in:

```text
docs/system_design/Decision_Log.md
```
