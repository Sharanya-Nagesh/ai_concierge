# Coding Standards

## 1. Purpose

This document defines the coding standards and development conventions for the AI Concierge project.

The goal is to maintain code that is:

* Readable
* Consistent
* Maintainable
* Testable
* Modular
* Scalable
* Easy for new developers to understand

These standards apply across the project, with language-specific conventions where required.

---

# 2. General Principles

The project follows these principles:

1. **Keep code simple and readable.**
2. **Follow a consistent naming convention.**
3. **Use modular components instead of large monolithic files.**
4. **Avoid unnecessary duplication.**
5. **Separate business logic from API and presentation layers.**
6. **Write code that is easy to test.**
7. **Handle errors explicitly.**
8. **Document non-obvious design decisions.**
9. **Avoid hard-coded configuration values.**
10. **Prefer maintainability over premature optimization.**

---

# 3. Python Standards

The backend and ML components primarily use Python.

Python code should follow standard Python conventions and PEP 8 principles.

## 3.1 Naming

### Variables and functions

Use `snake_case`.

```python
user_profile = get_user_profile()
conversation_history = load_conversation_history()
```

### Classes

Use `PascalCase`.

```python
class UserService:
    pass


class RetrievalService:
    pass
```

### Constants

Use uppercase with underscores.

```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
```

### Private members

Use a leading underscore where appropriate.

```python
def _validate_request():
    pass
```

---

# 4. File Naming

Python files should use `snake_case`.

Examples:

```text
chat_service.py
user_service.py
vector_store.py
profile_manager.py
```

Avoid:

```text
ChatService.py
chatService.py
chat-service.py
```

---

# 5. Function Design

Functions should have a single clear responsibility.

Prefer:

```python
def retrieve_documents(query):
    ...
```

over a function that performs unrelated operations:

```python
def process_everything():
    ...
```

Large functions should be divided into smaller functions when doing so improves readability or testability.

---

# 6. Type Hints

Type hints should be used for important application and service interfaces.

Example:

```python
def get_user(user_id: str) -> User:
    ...
```

For collections:

```python
def retrieve_documents(query: str) -> list[Document]:
    ...
```

Type hints should make interfaces easier to understand and maintain.

---

# 7. Docstrings

Public classes, functions and important modules should have concise docstrings.

Example:

```python
def retrieve_documents(query: str, top_k: int) -> list[Document]:
    """Retrieve the most relevant documents for a query."""
    ...
```

Docstrings should explain the purpose and important behavior rather than restating the code.

---

# 8. Imports

Imports should be organized into logical groups:

1. Standard library
2. Third-party packages
3. Internal application modules

Example:

```python
import logging
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_service import ChatService
```

Unused imports should be removed.

---

# 9. Backend Architecture Standards

The backend should maintain clear separation between layers.

```text
API
 ↓
Service
 ↓
Repository / Data Access
 ↓
Database
```

AI-specific components may be invoked through appropriate service or orchestration layers:

```text
API
 ↓
Service / Orchestrator
 ↓
Agent
 ├── Memory
 ├── RAG
 └── Tools
 ↓
LLM
```

API endpoints should not contain large amounts of business logic.

Prefer:

```python
@router.post("/chat")
def chat(request: ChatRequest):
    return chat_service.process(request)
```

rather than implementing the complete conversation pipeline inside the endpoint.

---

# 10. API Standards

API endpoints should:

* Use clear resource names.
* Validate incoming requests.
* Return consistent response structures.
* Use appropriate HTTP status codes.
* Handle errors explicitly.
* Avoid exposing internal implementation details.

Example:

```text
POST /api/v1/chat
GET  /api/v1/users/{user_id}
GET  /api/v1/conversations/{conversation_id}
```

API versioning should be used where appropriate:

```text
/api/v1/
```

---

# 11. Database Standards

Database access should be separated from business logic.

Database models should represent persistent entities, while services should contain application-level behavior.

Avoid embedding complex business logic directly inside database models.

Database queries should:

* Be explicit.
* Be reusable where appropriate.
* Avoid unnecessary repeated queries.
* Use appropriate indexes.
* Handle transaction boundaries correctly.

---

# 12. Configuration Standards

Configuration values should not be hard-coded.

Avoid:

```python
DATABASE_URL = "some-production-database-url"
```

Prefer environment-based configuration:

```python
DATABASE_URL = settings.database_url
```

Sensitive information must never be committed to source control.

Examples include:

```text
API keys
Passwords
Database credentials
Access tokens
Private keys
```

Use:

```text
.env
.env.example
```

appropriately.

---

# 13. Error Handling

Errors should be handled at the appropriate application boundary.

Avoid silently ignoring exceptions:

```python
try:
    process_request()
except Exception:
    pass
```

Prefer explicit handling:

```python
try:
    process_request()
except ServiceError as exc:
    logger.error("Request processing failed: %s", exc)
    raise
```

Application-specific exceptions should be defined where useful.

Example:

```python
class RetrievalError(Exception):
    """Raised when document retrieval fails."""
```

Do not expose internal stack traces or sensitive implementation details to API clients.

---

# 14. Logging

Use structured and meaningful logging.

Prefer:

```python
logger.info("Conversation processing started", extra={"conversation_id": conversation_id})
```

over:

```python
print("something happened")
```

Logs should help with:

* Debugging
* Monitoring
* Error investigation
* Performance analysis
* Production troubleshooting

Sensitive information must not be logged.

---

# 15. AI / ML Code Standards

ML and AI components should follow the same principles of modularity and reproducibility.

Separate:

```text
Data
 ↓
Preprocessing
 ↓
Model / Embedding
 ↓
Retrieval / Inference
 ↓
Evaluation
```

Do not mix experimentation code with production application logic without a clear boundary.

For example:

```text
ml/
    experiments/
    models/
    evaluation/
```

may be introduced later if the implementation requires it.

Model configuration should be explicit and versionable.

---

# 16. Prompt Standards

Prompts should not be scattered throughout application code.

Where practical, prompts should be:

* Centralized
* Versioned
* Clearly named
* Testable
* Separated from application logic

Avoid:

```python
response = llm("some very large prompt...")
```

inside multiple unrelated functions.

Prompt versions should be traceable when changes can affect model behavior.

---

# 17. RAG Standards

RAG components should maintain clear separation between:

```text
Document ingestion
        ↓
Parsing
        ↓
Chunking
        ↓
Embedding
        ↓
Vector storage
        ↓
Retrieval
        ↓
Reranking
        ↓
Context construction
        ↓
LLM generation
```

Each stage should be independently testable where practical.

Retrieval configuration should not be hidden inside unrelated business logic.

---

# 18. Memory Standards

Memory operations should be explicitly separated from ordinary conversation processing.

Memory-related code should clearly distinguish between:

* Short-term conversation context
* Long-term user information
* User preferences
* Summarized history
* Retrieved memory

Memory should not be written automatically without defined rules for relevance, privacy and lifecycle.

---

# 19. Frontend Standards

Frontend code should use consistent component and file naming.

React components should generally use `PascalCase`.

Example:

```text
ChatWindow.tsx
MessageCard.tsx
UserProfile.tsx
```

Reusable logic should be extracted into hooks or services rather than duplicated across components.

---

# 20. Comments

Comments should explain **why**, not simply **what**.

Avoid:

```python
# Increment i by 1
i += 1
```

Prefer:

```python
# Retry only transient failures because validation errors are not recoverable.
```

Remove comments that become incorrect or redundant after code changes.

---

# 21. Testing Standards

New functionality should include appropriate tests.

Testing should cover, where applicable:

```text
Unit tests
Integration tests
API tests
AI/ML evaluation
Performance tests
```

Tests should be:

* Deterministic where possible.
* Independent.
* Readable.
* Repeatable.

Production code should not depend on manual testing alone.

---

# 22. Test Naming

Test names should describe the expected behavior.

Example:

```python
def test_returns_user_when_valid_id_is_provided():
    ...
```

For failure cases:

```python
def test_rejects_invalid_authentication_token():
    ...
```

---

# 23. Dependency Management

Dependencies should be explicitly declared and version-controlled.

Avoid adding packages without a clear requirement.

Before introducing a new dependency, consider:

* Necessity
* Maintenance status
* Security
* License
* Compatibility
* Project complexity

---

# 24. Security Standards

Security-sensitive code should receive additional review.

Never commit:

```text
API keys
Passwords
Tokens
Secrets
Private credentials
```

Validate external input.

Use authentication and authorization consistently.

Avoid returning sensitive user information through APIs.

---

# 25. Git-Friendly Code

Changes should be organized into logical commits.

Avoid combining unrelated changes such as:

```text
database changes
UI redesign
prompt changes
documentation changes
```

in a single commit unless they are intentionally part of the same feature.

Code should be formatted before committing.

---

# 26. Code Review Standards

Before merging code, review:

* Correctness
* Readability
* Architecture
* Security
* Error handling
* Tests
* Performance
* Documentation
* Backward compatibility

Reviewers should focus on improving the system rather than only checking formatting.

---

# 27. Documentation and Code Consistency

When implementation changes affect documented architecture, the corresponding documentation should be updated.

For example:

```text
API implementation change
        ↓
backend/app/api/
        ↓
Update API_Spec.md
```

Similarly:

```text
Architecture change
        ↓
Update relevant system-design document
        ↓
Record significant decision in Decision_Log.md
```

Documentation should not intentionally describe an architecture that the implementation no longer follows.

---

# 28. Formatting and Quality Checks

Before submitting code, developers should run the project's configured:

* Formatter
* Linter
* Type checker
* Unit tests
* Integration tests where applicable

The exact tools may be finalized during implementation and documented in the development environment setup.

---

# 29. Recommended Development Workflow

The preferred workflow is:

```text
Understand requirement
        ↓
Review relevant architecture
        ↓
Implement small change
        ↓
Write/update tests
        ↓
Run formatting and validation
        ↓
Review code
        ↓
Update documentation if required
        ↓
Commit
```

This keeps implementation aligned with the documented architecture.

---

# 30. Final Principles

The most important coding standards for this project are:

1. Write readable code.
2. Keep components modular.
3. Separate responsibilities.
4. Avoid unnecessary duplication.
5. Use type hints and meaningful names.
6. Handle errors explicitly.
7. Never hard-code secrets.
8. Test important behavior.
9. Keep AI/ML components reproducible and modular.
10. Keep documentation synchronized with implementation.
11. Prefer simple solutions before introducing complexity.
12. Record significant architectural changes.

These standards provide the baseline for backend, frontend and ML development while allowing more specific language and framework conventions to be introduced as implementation progresses.
