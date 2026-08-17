# Local Development

## 1. Purpose

This document defines the standard workflow for developing, running, testing and debugging the AI Concierge project locally.

It builds on the environment configuration described in:

```text
docs/development/Environment_Setup.md
```

The objective is to provide a repeatable development workflow from starting the project through validating changes.

---

# 2. Local Development Overview

The local development environment consists of:

```text
Developer Machine
│
├── Frontend
│
├── Backend
│
├── PostgreSQL
│
├── AI / ML Components
│
├── RAG Components
│
└── Supporting Services
```

A typical application flow is:

```text
Browser
   │
   ▼
Frontend
   │
   ▼
Backend API
   │
   ├── Authentication
   ├── Application Services
   ├── Memory
   ├── RAG
   ├── Agent
   └── AI Services
   │
   ▼
Database / External Services
```

---

# 3. Development Workflow

The standard workflow is:

```text
Pull Latest Changes
        ↓
Create / Switch Branch
        ↓
Start Development Services
        ↓
Implement Change
        ↓
Run Tests
        ↓
Run Quality Checks
        ↓
Update Documentation
        ↓
Review Changes
        ↓
Commit
        ↓
Push Branch
```

This workflow should be followed for both backend and ML-related development.

---

# 4. Start of Development Session

Before beginning work:

```bash
git status
```

Check the current branch:

```bash
git branch
```

Update the local repository:

```bash
git pull
```

If working on a feature branch, ensure it is synchronized with the latest project state according to the Git workflow.

---

# 5. Activate the Development Environment

For Python development, activate the project virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Verify:

```bash
python --version
```

For frontend development:

```bash
node --version
npm --version
```

---

# 6. Configure Environment Variables

Before starting application services, verify the local environment configuration.

The project should provide:

```text
.env.example
```

Developers should create their local environment configuration from this template.

Example:

```text
DATABASE_URL=<local-database>
API_BASE_URL=<local-backend>
LLM_API_KEY=<development-key>
```

Actual credentials must never be committed.

---

# 7. Start Supporting Services

Start the services required for local development.

A Docker-based environment may use:

```bash
docker compose up -d
```

Alternatively, only required services can be started.

For example:

```bash
docker compose up -d postgres
```

Verify running containers:

```bash
docker ps
```

---

# 8. Database Development

The local application should use a development database rather than a production database.

Typical flow:

```text
Start PostgreSQL
      ↓
Verify Connection
      ↓
Run Migrations
      ↓
Start Backend
      ↓
Validate Database Access
```

Database schema changes should be handled through the project's migration system.

Avoid manually modifying database schemas without recording the corresponding change.

---

# 9. Database Migrations

When database models change:

```text
Model Change
     ↓
Migration Generation
     ↓
Migration Review
     ↓
Migration Execution
     ↓
Database Validation
```

Migration commands depend on the framework selected for implementation.

Migration files should be committed alongside the corresponding application changes.

---

# 10. Start the Backend

The backend should be started using the development command defined by the selected backend framework.

Conceptually:

```text
Activate Python Environment
        ↓
Load Environment Variables
        ↓
Verify Database
        ↓
Start Backend Server
```

The backend should expose:

* API endpoints
* Development documentation where applicable
* Health/status endpoints where implemented

---

# 11. Backend Development Loop

For backend development:

```text
Modify Code
    ↓
Run Unit Tests
    ↓
Run API Tests
    ↓
Run Linter / Formatter
    ↓
Check Logs
    ↓
Review API Behavior
```

Small changes should be validated before moving to the next component.

---

# 12. Start the Frontend

Move into the frontend directory:

```bash
cd frontend
```

Install dependencies when required:

```bash
npm install
```

Start the development server using the configured project command.

For example:

```bash
npm run dev
```

The frontend should connect to the local backend through the configured API URL.

---

# 13. Frontend Development Loop

The standard frontend workflow is:

```text
Modify Component
      ↓
Run Development Server
      ↓
Test UI Interaction
      ↓
Check Browser Console
      ↓
Verify API Request
      ↓
Run Frontend Tests
```

Reusable components should be preferred over duplicated UI logic.

---

# 14. Backend–Frontend Integration

During integrated development:

```text
Frontend
   │
   │ HTTP Request
   ▼
Backend API
   │
   ▼
Service Layer
   │
   ├── Database
   ├── Memory
   ├── RAG
   └── Agent
```

When debugging an application flow, determine first whether the issue originates from:

1. Frontend
2. API request
3. Backend
4. Database
5. AI/RAG component
6. External service

This avoids debugging unrelated components simultaneously.

---

# 15. API Development

API changes should follow:

```text
Requirement
    ↓
API Specification
    ↓
Schema
    ↓
Endpoint
    ↓
Service Logic
    ↓
Tests
    ↓
Documentation
```

The API contract should remain consistent with:

```text
docs/system_design/API_Spec.md
```

When an API contract changes, the corresponding documentation should also be updated.

---

# 16. API Testing During Development

API endpoints may be tested using:

* Automated tests
* OpenAPI/Swagger interface
* Postman
* curl
* Frontend integration

A basic development cycle is:

```text
Start Backend
     ↓
Send Request
     ↓
Inspect Response
     ↓
Check Logs
     ↓
Modify Implementation
     ↓
Repeat
```

---

# 17. ML Development

ML development should remain separate from production application logic where practical.

Typical workflow:

```text
Define Experiment
      ↓
Prepare Data
      ↓
Run Model / Pipeline
      ↓
Evaluate
      ↓
Record Results
      ↓
Compare Alternatives
      ↓
Select Approach
      ↓
Integrate Validated Component
```

Experimental code should not automatically become production code.

---

# 18. RAG Development

RAG development should follow the documented pipeline:

```text
Documents
    ↓
Parsing
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Storage
    ↓
Retrieval
    ↓
Reranking
    ↓
Context Construction
    ↓
LLM
    ↓
Response
```

Each stage should be independently testable where practical.

Changes to retrieval configuration should be evaluated rather than judged only from a few manual examples.

---

# 19. Memory Development

Memory-related functionality should be developed independently from ordinary request processing.

A typical flow is:

```text
Conversation
     ↓
Memory Extraction
     ↓
Validation / Filtering
     ↓
Memory Storage
     ↓
Future Retrieval
     ↓
Context Construction
```

Memory changes should consider:

* Relevance
* Persistence
* Retrieval
* Expiration
* Privacy
* User control

The detailed architecture is documented in:

```text
docs/system_design/Memory_Architecture.md
```

---

# 20. Agent Development

Agent functionality should be developed incrementally.

A typical flow is:

```text
User Request
     ↓
Intent / Task Understanding
     ↓
Agent Decision
     ↓
Tool / RAG / Memory Selection
     ↓
Execution
     ↓
Response Generation
```

Each tool or capability should be independently testable.

Agent behavior should not be treated as reliable merely because an individual manual test succeeds.

---

# 21. Logging During Development

Logs should be used to understand application behavior.

Useful development logs may include:

```text
Request received
Authentication result
Service execution
Database operation
Retrieval result
Agent decision
External service response
Error details
```

Sensitive information must not be logged.

Avoid logging:

```text
Passwords
API keys
Authentication tokens
Private user information
Secrets
```

---

# 22. Debugging Workflow

When a problem occurs:

```text
Reproduce Problem
      ↓
Identify Layer
      ↓
Inspect Logs
      ↓
Inspect Request / Response
      ↓
Check Configuration
      ↓
Isolate Component
      ↓
Fix
      ↓
Add Regression Test
      ↓
Re-test
```

The objective is to identify the root cause rather than only patch the visible symptom.

---

# 23. Error Handling During Development

Errors should be reproducible and understandable.

When debugging an error, capture:

* Error message
* Relevant logs
* Request context
* Component involved
* Reproduction steps
* Expected behavior
* Actual behavior

This information should be useful when creating an issue or documenting a bug.

---

# 24. Testing During Development

Tests should be run continuously rather than only before release.

Recommended progression:

```text
Small Code Change
      ↓
Unit Test
      ↓
Component Test
      ↓
Integration Test
      ↓
End-to-End Test
```

Not every change requires the entire test suite, but the appropriate tests should be run before committing.

---

# 25. Code Quality Checks

Before pushing a significant change:

```text
Formatter
   ↓
Linter
   ↓
Type Checker
   ↓
Tests
   ↓
Build
```

The exact tools will be finalized during implementation.

---

# 26. Working With Documentation

Documentation should be treated as part of development.

When implementing a component, first check the relevant documentation.

For example:

```text
Backend implementation
        ↓
Backend_Architecture.md
API implementation
        ↓
API_Spec.md
Database implementation
        ↓
Database_Design.md
RAG implementation
        ↓
RAG_Design.md
Memory implementation
        ↓
Memory_Architecture.md
```

If implementation intentionally deviates from the design, the documentation should be updated.

---

# 27. Development With Feature Branches

Follow the Git workflow defined in:

```text
docs/development/Git_Workflow.md
```

Typical flow:

```text
main
  ↓
feature/<feature-name>
  ↓
Implementation
  ↓
Testing
  ↓
Review
  ↓
Pull Request
  ↓
Merge
```

Avoid making unrelated changes within the same feature branch.

---

# 28. Local Testing of Authentication

Authentication should be tested locally before integrating protected functionality.

The development workflow should verify:

```text
Unauthenticated Request
        ↓
Rejected

Authenticated Request
        ↓
Authorized
        ↓
Endpoint Access
```

Tests should also cover invalid or expired credentials where applicable.

---

# 29. Local Testing of RAG

RAG development should include checks for:

* Document ingestion
* Chunking
* Embedding generation
* Retrieval
* Reranking
* Context construction
* Response generation

A useful debugging approach is to inspect each intermediate stage rather than only the final response.

```text
Question
  ↓
Retrieved Documents
  ↓
Ranked Documents
  ↓
Final Context
  ↓
Generated Response
```

---

# 30. Local Testing of Memory

Memory functionality should be tested for:

```text
Store
 ↓
Retrieve
 ↓
Use
 ↓
Update
 ↓
Delete / Expire
```

The expected behavior should be explicitly defined before implementing persistent memory.

---

# 31. Working With External AI Services

External AI services may introduce:

* Network failures
* Authentication errors
* Rate limits
* Latency
* Service outages
* Model changes

Local development should therefore support graceful failure.

Where practical, components should be abstracted behind services or interfaces so that they can be tested independently.

---

# 32. Offline / Mock Development

Where external services are expensive, unavailable or slow, development may use mocks or local substitutes.

Example:

```text
Production:
Application → External AI Service

Local Testing:
Application → Mock AI Service
```

Mock responses should resemble the expected interface without pretending to reproduce actual model behavior.

AI quality should still be evaluated separately using real model outputs.

---

# 33. Data Handling During Development

Development datasets should be appropriate for local use.

Avoid copying sensitive production data into development environments.

Where possible:

```text
Production Data
      ↓
Anonymization / Filtering
      ↓
Development Dataset
```

Development data should be versioned or referenced reproducibly when required for ML experiments.

---

# 34. Performance Debugging

Performance issues should be measured rather than assumed.

Potential metrics include:

```text
API latency
Database query time
Retrieval latency
LLM latency
Memory retrieval latency
Token usage
CPU usage
GPU usage
Memory usage
```

Performance optimization should focus on measured bottlenecks.

---

# 35. Local Observability

During development, observability should make it possible to understand:

```text
Request
  ↓
API
  ↓
Service
  ↓
Database / RAG / Memory / Agent
  ↓
External Service
  ↓
Response
```

As monitoring infrastructure matures, tracing and metrics can be integrated according to:

```text
docs/system_design/Monitoring.md
```

---

# 36. End-to-End Local Validation

Before considering a major feature complete, validate the complete flow.

Example:

```text
Start Services
      ↓
Open Frontend
      ↓
Authenticate
      ↓
Submit Request
      ↓
Backend Receives Request
      ↓
Service Executes
      ↓
AI / RAG / Memory Components Run
      ↓
Response Returned
      ↓
Frontend Displays Response
```

This validates integration rather than only individual components.

---

# 37. Stopping Development Services

After development, stop services that are no longer required.

For Docker-based services:

```bash
docker compose down
```

If persistent volumes are intentionally required, avoid deleting them unless necessary.

---

# 38. End-of-Day Workflow

Before finishing a development session:

```text
Save Changes
    ↓
Run Relevant Tests
    ↓
Review git diff
    ↓
Update Documentation
    ↓
Commit Changes
    ↓
Push Branch
```

Check:

```bash
git status
```

before ending the session.

---

# 39. Recommended Local Development Checklist

```text
☐ Repository synchronized
☐ Correct branch selected
☐ Python environment activated
☐ Dependencies installed
☐ Environment variables configured
☐ Database running
☐ Supporting services running
☐ Backend running
☐ Frontend running
☐ Feature implemented
☐ Tests updated
☐ Tests passing
☐ Code formatted
☐ Linting passed
☐ Documentation updated
☐ git diff reviewed
☐ Changes committed
☐ Branch pushed
```

---

# 40. Final Development Principles

Local development should follow these principles:

1. Keep development reproducible.
2. Work in isolated branches.
3. Make small, testable changes.
4. Validate changes continuously.
5. Keep frontend and backend responsibilities separate.
6. Keep ML experiments isolated from production logic.
7. Treat RAG and memory as independently testable components.
8. Never expose secrets through code or logs.
9. Keep implementation synchronized with documentation.
10. Measure performance rather than assuming bottlenecks.
11. Add regression tests when fixing bugs.
12. Prefer incremental integration over building the entire system at once.

The objective is to make local development predictable enough that the same implementation can later move through testing, CI/CD and deployment with minimal environmental surprises.
