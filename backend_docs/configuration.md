# Backend Configuration

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** Backend Configuration Design

---

# Table of Contents

1. Introduction
2. Configuration Objectives
3. Configuration Architecture
4. Environment Variables
5. `.env` vs `.env.example`
6. Configuration Categories
7. Application Settings
8. Database Configuration
9. Qdrant Configuration
10. LLM Configuration
11. Authentication Configuration
12. CORS Configuration
13. File Upload Configuration
14. Logging Configuration
15. Environment Management
16. Secret Management
17. Configuration Validation
18. Configuration Loading
19. Example Configuration
20. Docker Configuration
21. Development Configuration
22. Production Configuration
23. Configuration Security
24. Testing Configuration
25. Configuration Checklist
26. Summary

---

# 1. Introduction

Configuration management defines how the backend obtains settings required to run the application.

The backend should not hard-code environment-specific values such as:

- Database URLs
- API keys
- JWT secrets
- LLM credentials
- Qdrant connection details
- CORS origins
- Logging levels

Instead, these values should be supplied through environment-specific configuration.

The general principle is:

```text
Application Code
       │
       ▼
Configuration Layer
       │
       ▼
Environment Variables
       │
       ├── Development
       ├── Testing
       └── Production
```

---

# 2. Configuration Objectives

The configuration system should:

- Keep secrets outside source code
- Support multiple environments
- Validate required configuration
- Provide sensible defaults where appropriate
- Prevent accidental exposure of credentials
- Make local development easy
- Work with Docker
- Support CI/CD
- Allow AI providers and models to be changed without modifying business logic

---

# 3. Configuration Architecture

Configuration should be centralized.

Conceptually:

```text
Environment
     │
     ▼
Environment Variables
     │
     ▼
Configuration Module
     │
     ▼
Validated Settings
     │
 ┌───┼──────────────┐
 ▼   ▼              ▼
API Database      AI Services
```

Application components should retrieve configuration through the configuration layer rather than directly reading environment variables throughout the codebase.

---

# 4. Environment Variables

Environment variables allow configuration to be changed without modifying application source code.

Examples include:

```text
DATABASE_URL
QDRANT_URL
LLM_PROVIDER
LLM_MODEL
JWT_SECRET
LOG_LEVEL
```

The actual values depend on the environment.

---

# 5. `.env` vs `.env.example`

These are **different files**.

## `.env`

Contains the actual configuration values used by a local environment.

Example:

```text
DATABASE_URL=<local-database-url>
JWT_SECRET=<local-development-secret>
LLM_API_KEY=<local-api-key>
```

The real `.env` file may contain secrets.

Therefore:

```text
.env
```

should normally be excluded from Git.

---

## `.env.example`

Contains the **names and structure** of required environment variables but does not contain real secrets.

Example:

```text
DATABASE_URL=
JWT_SECRET=
LLM_API_KEY=
QDRANT_URL=
```

This file **should be committed to Git**.

It tells another developer:

> "These are the configuration values you need to provide."

---

## Relationship

```text
.env.example
      │
      │ Copy
      ▼
    .env
      │
      ▼
Fill in actual values
      │
      ▼
Run application
```

The repository should therefore contain:

```text
.env.example       ✅ Commit
.env               ❌ Do not commit
```

---

# 6. Configuration Categories

Configuration can be grouped into:

```text
Application
Database
Vector Database
LLM
Authentication
CORS
File Upload
Logging
External Services
```

---

# 7. Application Settings

Application-level configuration may include:

```text
APP_NAME
APP_ENV
APP_VERSION
DEBUG
API_PREFIX
```

Example:

```text
APP_NAME=AI-Concierge
APP_ENV=development
APP_VERSION=1.0.0
DEBUG=true
API_PREFIX=/api/v1
```

Production values should be different where appropriate.

---

# 8. Database Configuration

PostgreSQL connection details should be configurable.

Example:

```text
DATABASE_URL=<database-connection-string>
```

The backend should use this configuration when initializing SQLAlchemy.

Conceptual flow:

```text
DATABASE_URL
      │
      ▼
Configuration
      │
      ▼
SQLAlchemy Engine
      │
      ▼
PostgreSQL
```

Database credentials must never be hard-coded.

---

# 9. Qdrant Configuration

Qdrant connection details should also be configurable.

Example:

```text
QDRANT_URL=<qdrant-url>
QDRANT_API_KEY=<qdrant-api-key>
QDRANT_COLLECTION=<collection-name>
```

For a local development environment, the configuration may point to a locally running Qdrant instance.

For production, it may point to a managed or remotely hosted instance.

---

# 10. LLM Configuration

The application should not hard-code a specific LLM provider into the business logic.

Configuration should allow the provider and model to be changed.

Example:

```text
LLM_PROVIDER=<provider>
LLM_MODEL=<model>
LLM_API_KEY=<api-key>
```

Optional configuration may include:

```text
LLM_TEMPERATURE
LLM_MAX_TOKENS
LLM_TIMEOUT
```

The application should access these values through an LLM configuration object.

Conceptually:

```text
Configuration
      │
      ▼
LLM Service
      │
      ▼
Configured Provider
      │
      ▼
Configured Model
```

---

# 11. Authentication Configuration

Authentication-related settings should be configurable.

Examples:

```text
JWT_SECRET
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS
```

The JWT secret must be sufficiently strong and must never be committed to Git.

---

# 12. CORS Configuration

Cross-Origin Resource Sharing (CORS) controls which frontend origins can communicate with the backend.

Example configuration:

```text
CORS_ORIGINS=<allowed-origins>
```

During local development, the frontend development server may be allowed.

Production should use an explicit allowlist rather than permitting arbitrary origins.

Avoid using unrestricted configuration such as:

```text
*
```

unless there is a deliberate security reason and the implications are understood.

---

# 13. File Upload Configuration

The application may allow users to upload documents for RAG.

Configuration should define limits such as:

```text
MAX_FILE_SIZE_MB
ALLOWED_FILE_TYPES
MAX_FILES_PER_REQUEST
```

Example conceptual configuration:

```text
MAX_FILE_SIZE_MB=20
ALLOWED_FILE_TYPES=pdf,txt,docx
```

The exact limits should be finalized based on application requirements.

File validation must happen on the backend.

---

# 14. Logging Configuration

Logging should be configurable.

Example:

```text
LOG_LEVEL=INFO
```

Possible levels include:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Development may use:

```text
DEBUG
```

while production will generally use:

```text
INFO
```

or another appropriate level.

Sensitive information must never be logged.

---

# 15. Environment Management

The application should support separate environments.

```text
Development
     │
     ▼
Testing
     │
     ▼
Staging
     │
     ▼
Production
```

Each environment can have different configuration values.

---

## Development

Used for local development.

Typical characteristics:

```text
DEBUG enabled
Local PostgreSQL
Local Qdrant
Development LLM credentials
Verbose logging
```

---

## Testing

Used for automated tests.

Typical characteristics:

```text
Test database
Mock or controlled external services
Predictable configuration
Isolated test data
```

---

## Staging

Used to test production-like behavior before release.

---

## Production

Used by real users.

Typical characteristics:

```text
DEBUG disabled
Secure secrets
Production database
Production vector database
Restricted CORS
Secure logging
Monitoring enabled
```

---

# 16. Secret Management

Secrets include:

```text
API Keys
Database Passwords
JWT Secrets
OAuth Credentials
Encryption Keys
```

Secrets should never be stored directly in source code.

Avoid:

```python
JWT_SECRET = "some-secret"
```

Instead:

```text
Environment
    ↓
Configuration
    ↓
Application
```

---

# 17. Configuration Validation

The backend should validate configuration during application startup.

Conceptually:

```text
Application Startup
       │
       ▼
Load Configuration
       │
       ▼
Validate Required Values
       │
 ┌─────┴─────┐
 ▼           ▼
Valid       Invalid
 │           │
 ▼           ▼
Start      Fail Fast
```

If a required production secret is missing, the application should fail clearly rather than starting with an insecure configuration.

---

# 18. Configuration Loading

A centralized configuration class can be used.

Conceptually:

```python
class Settings:
    app_name: str
    app_env: str
    database_url: str
    qdrant_url: str
    llm_provider: str
    llm_model: str
    jwt_secret: str
```

The actual implementation should use an appropriate configuration mechanism, such as Pydantic Settings.

---

## Configuration Flow

```text
.env / Environment
       │
       ▼
Settings Loader
       │
       ▼
Validation
       │
       ▼
Application Settings
       │
 ┌─────┼──────────────┐
 ▼     ▼              ▼
API  Database       AI
```

---

# 19. Example Configuration

The following is a **generic example only**.

It does not contain real credentials.

## `.env.example`

```text
# Application
APP_NAME=AI-Concierge
APP_ENV=development
APP_VERSION=1.0.0
DEBUG=true
API_PREFIX=/api/v1

# Database
DATABASE_URL=

# Qdrant
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=

# LLM
LLM_PROVIDER=
LLM_MODEL=
LLM_API_KEY=
LLM_TEMPERATURE=
LLM_MAX_TOKENS=
LLM_TIMEOUT=

# Authentication
JWT_SECRET=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=

# CORS
CORS_ORIGINS=

# File Upload
MAX_FILE_SIZE_MB=
ALLOWED_FILE_TYPES=

# Logging
LOG_LEVEL=INFO
```

These values are placeholders and should be replaced with appropriate environment-specific values.

---

# 20. Docker Configuration

Docker containers should receive configuration through environment variables.

Conceptually:

```text
Docker Compose
      │
      ▼
Environment Configuration
      │
 ┌────┼─────────┐
 ▼    ▼         ▼
Backend PostgreSQL Qdrant
```

Secrets should preferably be injected securely rather than baked into Docker images.

---

## Docker Principle

Do not place secrets directly inside:

```text
Dockerfile
docker-compose.yml
```

unless a secure mechanism is being used intentionally.

---

# 21. Development Configuration

Local development may use:

```text
.env
```

with values appropriate for the developer's machine.

Example:

```text
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
```

The developer should create `.env` from `.env.example`.

---

# 22. Production Configuration

Production configuration must:

- Disable debug mode
- Use secure secrets
- Use production database credentials
- Restrict CORS
- Use HTTPS
- Use appropriate logging
- Protect API credentials
- Validate all required configuration

Example conceptual configuration:

```text
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
```

Actual secrets should be supplied through the deployment platform's secret-management system.

---

# 23. Configuration Security

Configuration must follow these rules:

### Rule 1

Never commit `.env`.

### Rule 2

Never commit API keys.

### Rule 3

Never commit database passwords.

### Rule 4

Never commit JWT signing secrets.

### Rule 5

Do not place secrets in frontend code.

### Rule 6

Do not expose backend environment variables to the browser unless they are explicitly intended to be public.

### Rule 7

Rotate compromised secrets immediately.

---

# 24. Testing Configuration

Automated tests should use isolated configuration.

The test environment should not accidentally connect to production services.

Conceptually:

```text
Tests
  │
  ▼
Test Configuration
  │
  ├── Test Database
  ├── Test Qdrant / Mock
  └── Mock or Controlled LLM
```

This prevents tests from modifying real application data.

---

# 25. Configuration Checklist

Before running the backend, verify:

```text
[ ] Application configuration defined
[ ] Database URL configured
[ ] Qdrant configuration defined
[ ] LLM provider configured
[ ] LLM model configured
[ ] LLM API key configured
[ ] JWT secret configured
[ ] Token expiration configured
[ ] CORS configured
[ ] File-upload limits configured
[ ] Logging configured
```

---

# 26. Summary

The configuration system separates application code from environment-specific values.

The most important distinction is:

```text
.env.example
     │
     │ Template
     ▼
    .env
     │
     │ Actual local values
     ▼
Application
```

The repository should contain the template:

```text
.env.example
```

while actual secret-bearing configuration should remain outside version control:

```text
.env
```

Production secrets should preferably be managed by the deployment environment or a dedicated secret-management system.

A centralized configuration layer ensures that the backend remains secure, portable, testable, and easy to deploy across different environments.
