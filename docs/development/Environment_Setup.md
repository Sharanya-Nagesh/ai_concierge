# Environment Setup

## 1. Purpose

This document describes the development environment required to set up and run the AI Concierge project locally.

The goal is to provide a reproducible environment for:

* Backend development
* Frontend development
* ML/AI development
* Database development
* Testing
* Local service integration

This document focuses on environment configuration rather than application-specific implementation.

---

# 2. Development Environment Overview

The project consists of several development components:

```text
Developer Machine
│
├── Backend
│   └── Python environment
│
├── Frontend
│   └── Node.js environment
│
├── Database
│   └── PostgreSQL
│
├── ML / AI
│   └── Python + ML libraries
│
└── Supporting Services
    ├── Vector database / vector store
    ├── Redis (if required)
    └── External AI services
```

The exact services enabled locally may evolve as implementation progresses.

---

# 3. Prerequisites

The following tools should be installed before starting development.

## 3.1 Git

Git is required for source-code version control.

Verify installation:

```bash
git --version
```

---

## 3.2 Python

Python is required for:

* Backend development
* ML development
* RAG pipelines
* Evaluation
* Data processing

Verify installation:

```bash
python --version
```

The project should use a single supported Python version across development wherever possible.

The exact version should be pinned once the backend and ML dependencies are finalized.

---

## 3.3 Node.js

Node.js is required for frontend development.

Verify:

```bash
node --version
npm --version
```

The project should use an LTS version where possible.

If the project adopts a specific Node.js version, it should be documented in the repository configuration.

---

## 3.4 PostgreSQL

PostgreSQL is the primary relational database considered for the application.

Verify:

```bash
psql --version
```

The database version should be consistent between development and deployment environments as far as practical.

---

## 3.5 Docker

Docker is recommended for running supporting services consistently.

Verify:

```bash
docker --version
docker compose version
```

Docker may be used for:

* PostgreSQL
* Redis
* Vector databases
* Backend services
* Supporting infrastructure

---

# 4. Repository Setup

Clone the repository:

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd <project-directory>
```

Verify the repository:

```bash
git status
```

The repository should follow the finalized project structure.

---

# 5. Project Structure

The high-level structure is:

```text
project-root/
│
├── docs/
├── backend_docs/
├── ml/
├── backend/
├── frontend/
├── infrastructure/
├── tests/
├── .env.example
├── .gitignore
└── README.md
```

Documentation and implementation should remain separated according to the finalized project structure.

---

# 6. Python Virtual Environment

A dedicated virtual environment should be used for Python development.

Create the environment:

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, verify:

```bash
python --version
```

The terminal should indicate that the project virtual environment is active.

---

# 7. Python Dependency Installation

Backend and ML dependencies should be explicitly defined by the project.

Typical dependency files may include:

```text
requirements.txt
requirements-dev.txt
```

or an equivalent dependency-management configuration.

Install dependencies using the project's selected dependency manager.

For a requirements-based setup:

```bash
pip install -r requirements.txt
```

Development dependencies may be installed separately:

```bash
pip install -r requirements-dev.txt
```

The final dependency-management strategy should be documented once implementation is finalized.

---

# 8. Frontend Environment

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server using the command defined by the frontend framework.

For example:

```bash
npm run dev
```

The exact command may differ depending on the framework selected for implementation.

---

# 9. Environment Variables

Environment-specific configuration should be stored outside source code.

A template should be maintained:

```text
.env.example
```

Developers create their local environment file from the template.

Example:

```text
DATABASE_URL=<local-database-url>
API_BASE_URL=<backend-url>
LLM_API_KEY=<development-key>
VECTOR_STORE_URL=<vector-store-url>
```

These are **general placeholders only**.

Actual secrets must never be committed to Git.

---

# 10. Environment Variable Categories

Environment variables may include:

### Application

```text
APP_ENV
APP_NAME
APP_HOST
APP_PORT
```

### Database

```text
DATABASE_URL
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
```

### Authentication

```text
JWT_SECRET
AUTH_TOKEN_EXPIRY
```

### AI Services

```text
LLM_API_KEY
EMBEDDING_API_KEY
```

### Vector Store

```text
VECTOR_STORE_URL
VECTOR_STORE_API_KEY
```

### Observability

```text
LOG_LEVEL
MONITORING_ENDPOINT
```

The exact variables should be finalized during implementation.

---

# 11. Local Database Setup

The application requires a local database for development.

The database may be installed directly or run through Docker.

A Docker-based approach may use:

```bash
docker compose up -d postgres
```

Verify that the database is running:

```bash
docker ps
```

The application should connect to the local database using environment-based configuration.

---

# 12. Database Initialization

After starting PostgreSQL:

```text
Application
     │
     ▼
Database Connection
     │
     ▼
Migration System
     │
     ▼
Database Schema
```

Database migrations should be used rather than manually modifying production-style schemas.

The migration framework will be finalized during backend implementation.

---

# 13. Local Supporting Services

Additional services may be required depending on the implementation.

Possible services include:

```text
PostgreSQL
Redis
Vector Database
Object Storage
Local Model Server
```

Not every developer environment needs to run every service simultaneously.

Only the services required for the current development task should be enabled where practical.

---

# 14. Docker-Based Development

Docker Compose can provide a reproducible local environment.

Conceptually:

```text
Docker Compose
│
├── Backend
├── PostgreSQL
├── Redis
└── Vector Store
```

The frontend may either run directly on the host machine or through Docker depending on the final development workflow.

---

# 15. Backend Startup

After activating the Python environment and configuring environment variables:

```text
1. Activate virtual environment
2. Install dependencies
3. Configure .env
4. Start database
5. Apply migrations
6. Start backend server
```

The exact backend startup command will depend on the selected framework and implementation.

---

# 16. Frontend Startup

Typical workflow:

```text
1. Install Node.js dependencies
2. Configure frontend environment variables
3. Start backend
4. Start frontend development server
5. Open application in browser
```

The frontend should communicate with the backend through the configured API base URL.

---

# 17. Backend–Frontend Connection

The local architecture should resemble:

```text
Browser
   │
   ▼
Frontend
   │
   │ HTTP/API
   ▼
Backend
   │
   ├── PostgreSQL
   ├── RAG
   ├── Memory
   ├── Agent
   └── External AI Services
```

This allows frontend development to proceed against a locally running backend.

---

# 18. ML Environment

ML development should use the same project's supported Python environment where practical.

Typical ML dependencies may include:

```text
PyTorch
Transformers
Datasets
NumPy
Pandas
Scikit-learn
Embedding libraries
Evaluation libraries
```

The final dependency list should be maintained in the project's dependency configuration rather than installed manually without documentation.

---

# 19. GPU Environment

GPU acceleration may be useful for:

* Model inference
* Fine-tuning
* Embedding generation
* Evaluation
* ML experimentation

If GPU support is required, developers should verify:

```text
GPU availability
CUDA compatibility
Driver compatibility
Framework compatibility
```

CPU-based development should remain possible for lightweight development and testing whenever practical.

---

# 20. RAG Development Environment

RAG development may require:

```text
Document source
      ↓
Parser
      ↓
Chunker
      ↓
Embedding model
      ↓
Vector store
      ↓
Retriever
      ↓
Reranker
      ↓
LLM
```

Each component should have a locally testable configuration where feasible.

The specific RAG infrastructure will be documented in:

```text
docs/system_design/RAG_Design.md
```

---

# 21. API Development

The backend API should be locally accessible through the configured development server.

Developers should be able to:

```text
Start backend
     ↓
Access API
     ↓
Send test request
     ↓
Inspect response
```

API testing tools may include:

* Swagger/OpenAPI interface
* Postman
* curl
* Automated API tests

The final API workflow should remain consistent with:

```text
docs/system_design/API_Spec.md
```

---

# 22. Testing Environment

Before submitting code, developers should be able to run the relevant test suite locally.

Typical categories:

```text
Unit Tests
Integration Tests
API Tests
Frontend Tests
ML Evaluation
```

The exact commands will be defined as implementation progresses.

---

# 23. Code Quality Tools

The project should eventually configure automated tools for:

* Formatting
* Linting
* Type checking
* Testing
* Dependency checking

The final tools will be selected based on project requirements and documented in:

```text
docs/development/Coding_Standards.md
```

---

# 24. IDE Configuration

Developers may use any suitable IDE or editor.

The environment should support:

* Python
* JavaScript/TypeScript
* Markdown
* YAML
* JSON
* Docker
* Git

Recommended editor configuration may include:

```text
Automatic formatting
Linting
Type checking
Git integration
Python virtual-environment selection
```

Editor-specific configuration should not become a mandatory dependency unless required by the project.

---

# 25. Git Configuration

Before development:

```bash
git config --global user.name "<name>"
git config --global user.email "<email>"
```

Verify:

```bash
git config --list
```

The configured identity should correspond to the developer's Git account.

---

# 26. Environment Validation

After setup, verify the following:

```text
✓ Git installed
✓ Python installed
✓ Virtual environment active
✓ Python dependencies installed
✓ Node.js installed
✓ Frontend dependencies installed
✓ PostgreSQL available
✓ Environment variables configured
✓ Backend starts
✓ Frontend starts
✓ Database connection works
✓ Basic API request works
```

A simple validation flow is:

```text
Developer Machine
       │
       ▼
Frontend starts
       │
       ▼
Backend starts
       │
       ▼
Database connects
       │
       ▼
API request succeeds
       │
       ▼
Basic application flow works
```

---

# 27. Common Environment Problems

Common problems may include:

### Python version mismatch

```text
Cause:
Different Python version from the project's supported version.

Solution:
Use the documented Python version.
```

### Missing dependency

```text
Cause:
Dependency not installed.

Solution:
Install dependencies from the project's dependency configuration.
```

### Database connection failure

```text
Cause:
Database is not running or configuration is incorrect.

Solution:
Check database status and environment variables.
```

### Invalid API credentials

```text
Cause:
Missing or incorrect development credentials.

Solution:
Verify local environment configuration.
```

### Port already in use

```text
Cause:
Another process is using the configured port.

Solution:
Identify the process or configure another development port.
```

---

# 28. Environment Security

Local development environments must follow the same basic security principles as production environments.

Never:

* Commit secrets.
* Share private credentials through source control.
* Store production credentials in local configuration.
* Use production databases for experimental development unless explicitly authorized.
* Log sensitive information.

Development credentials should have limited permissions whenever possible.

---

# 29. Reproducibility

The development environment should be reproducible.

Important environment dependencies should be documented through:

```text
Dependency files
Environment templates
Docker configuration
Version files
README instructions
```

A new developer should be able to reconstruct the environment without relying on undocumented manual steps.

---

# 30. Setup Workflow

The complete setup process can be summarized as:

```text
Clone Repository
      ↓
Install Prerequisites
      ↓
Create Python Environment
      ↓
Install Dependencies
      ↓
Configure .env
      ↓
Start Database
      ↓
Apply Migrations
      ↓
Start Backend
      ↓
Start Frontend
      ↓
Run Tests
      ↓
Verify End-to-End Connection
```

---

# 31. Future Improvements

As the project matures, the development environment may be improved through:

* Docker Compose development profiles
* Automated environment validation
* Pre-commit hooks
* Development containers
* Dependency lock files
* Local observability stack
* Automated database initialization
* Reproducible ML environments
* GPU-enabled development profiles

These improvements should be introduced only when they provide measurable development value.

---

# 32. Final Environment Standard

The development environment should satisfy five principles:

1. **Reproducible** — another developer can recreate it.
2. **Secure** — secrets remain outside source control.
3. **Consistent** — supported versions are clearly defined.
4. **Testable** — backend, frontend and ML components can be validated locally.
5. **Maintainable** — setup instructions evolve alongside the implementation.

This document should be updated whenever a significant development-environment dependency or workflow is introduced.
