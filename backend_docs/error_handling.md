# Error Handling

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** Backend Error Handling Design

---

# Table of Contents

1. Introduction
2. Error Handling Objectives
3. Error Handling Principles
4. Error Categories
5. Error Handling Architecture
6. HTTP Status Codes
7. API Error Response Format
8. Request Validation Errors
9. Authentication Errors
10. Authorization Errors
11. Database Errors
12. RAG Errors
13. LLM Errors
14. Agent Errors
15. External Service Errors
16. File Processing Errors
17. Background Task Errors
18. Timeout Handling
19. Rate Limit Handling
20. Retry Strategy
21. Fallback Strategy
22. Logging Errors
23. User-Facing Error Messages
24. Global Exception Handling
25. Error Monitoring
26. Development vs Production Errors
27. Testing Error Handling
28. Error Handling Checklist
29. Summary

---

# 1. Introduction

Error handling defines how the backend detects, processes, logs, and communicates failures.

Failures can occur at many levels:

```text
Frontend
   │
   ▼
API
   │
   ├── Validation Error
   ├── Authentication Error
   ├── Authorization Error
   ├── Database Error
   ├── RAG Error
   ├── LLM Error
   ├── Agent Error
   ├── External Service Error
   └── Background Task Error
```

The backend should handle these failures consistently rather than allowing raw exceptions to reach the client.

---

# 2. Error Handling Objectives

The error-handling system should:

- Detect failures reliably
- Return appropriate HTTP status codes
- Provide useful information to the client
- Avoid exposing sensitive implementation details
- Log technical details for developers
- Support debugging
- Handle temporary failures gracefully
- Retry appropriate operations
- Provide fallbacks where possible
- Maintain application stability

---

# 3. Error Handling Principles

## Principle 1 — Fail Safely

The application should never expose sensitive internal information to users.

---

## Principle 2 — Log Technical Details

Developers need enough information to investigate the problem.

```text
User
  ↓
Safe Error Message

Backend Logs
  ↓
Detailed Technical Information
```

---

## Principle 3 — Use Appropriate HTTP Status Codes

The HTTP status should communicate the general category of failure.

---

## Principle 4 — Do Not Hide All Errors

Errors should not be silently swallowed.

Every significant failure should either:

- Be handled
- Be returned
- Be logged
- Be retried
- Or trigger a defined fallback

---

## Principle 5 — Distinguish Temporary and Permanent Errors

For example:

```text
Temporary
    ↓
Retry may succeed

Permanent
    ↓
Retry will not help
```

---

# 4. Error Categories

The backend will classify errors into several categories.

```text
Client Errors
│
├── Validation
├── Authentication
├── Authorization
├── Not Found
└── Conflict

Application Errors
│
├── Business Logic
├── RAG
├── Agent
└── File Processing

Infrastructure Errors
│
├── Database
├── Vector Database
├── LLM Provider
├── Network
└── External Services
```

---

# 5. Error Handling Architecture

The general flow is:

```text
Request
   │
   ▼
API Route
   │
   ▼
Service Layer
   │
   ▼
Exception
   │
   ▼
Exception Handler
   │
   ├───────────────┐
   ▼               ▼
Logging        Safe Response
                   │
                   ▼
                 Client
```

The API should not expose raw Python exceptions.

---

# 6. HTTP Status Codes

The backend should use standard HTTP status codes.

| Status | Meaning | Example |
|---|---|---|
| 200 | Success | Successful GET |
| 201 | Created | New resource |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Insufficient permission |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource |
| 422 | Unprocessable Entity | Validation failure |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected backend failure |
| 502 | Bad Gateway | Upstream service failure |
| 503 | Service Unavailable | Temporary service unavailable |
| 504 | Gateway Timeout | Upstream timeout |

---

# 7. API Error Response Format

Error responses should follow a consistent structure.

Conceptual format:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource could not be found.",
    "request_id": "example-request-id"
  }
}
```

The exact schema should remain consistent across APIs.

---

## Error Fields

A standardized error response may contain:

```text
code
message
request_id
details
```

Sensitive internal information should not be included.

---

# 8. Request Validation Errors

Validation errors occur when the client sends invalid data.

Examples:

```text
Missing required field
Invalid email format
Invalid enum value
File too large
Unsupported file type
Invalid parameter
```

Flow:

```text
Request
   │
   ▼
Pydantic Validation
   │
   ├── Valid → Continue
   │
   └── Invalid → 422
```

The response should identify which input is invalid where appropriate.

---

# 9. Authentication Errors

Authentication failures include:

- Missing token
- Invalid token
- Expired token
- Invalid credentials
- Invalid refresh token

Typical response:

```text
401 Unauthorized
```

Example:

```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "Authentication is required.",
    "request_id": "example-request-id"
  }
}
```

Authentication errors should not reveal unnecessary information.

---

# 10. Authorization Errors

Authorization failures occur when an authenticated user does not have permission to perform an operation.

Typical response:

```text
403 Forbidden
```

Example:

```text
Authenticated User
        │
        ▼
Permission Check
        │
        ▼
Access Denied
        │
        ▼
403 Forbidden
```

---

# 11. Database Errors

Database failures can include:

```text
Connection failure
Timeout
Constraint violation
Transaction failure
Unavailable database
Unexpected query failure
```

The backend should distinguish between errors that can safely be retried and errors that require immediate failure.

---

## Database Failure Flow

```text
Database Operation
       │
       ▼
Failure
       │
 ┌─────┴──────────┐
 ▼                ▼
Temporary       Permanent
 ▼                ▼
Retry          Return Error
```

Database implementation details should remain isolated within the repository/service layers.

---

# 12. RAG Errors

RAG-related failures may occur during:

```text
Document ingestion
       │
       ├── Text extraction
       ├── Chunking
       ├── Embedding
       └── Vector indexing
```

or during retrieval:

```text
Query
  │
  ├── Embedding failure
  ├── Qdrant failure
  ├── Retrieval failure
  └── Reranking failure
```

---

## No Relevant Context

Not finding useful documents is not necessarily a system error.

The system should distinguish:

```text
No relevant information found
```

from:

```text
Qdrant unavailable
```

The first is a valid retrieval result.

The second is an infrastructure failure.

---

# 13. LLM Errors

LLM-related failures may include:

- Provider unavailable
- API authentication failure
- Request timeout
- Rate limit
- Invalid request
- Context too large
- Model unavailable
- Unexpected provider response

---

## LLM Failure Flow

```text
LLM Request
    │
    ▼
Provider
    │
 ┌──┴───────────────┐
 ▼                  ▼
Success            Failure
                     │
              Classify Error
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        Retry      Fallback   Return
```

Not every LLM error should be retried.

---

# 14. Agent Errors

Agent workflows can fail because of:

- Invalid routing
- Tool failure
- Invalid tool parameters
- Unexpected model output
- Agent loop
- Maximum iteration reached
- Missing context

The backend should enforce boundaries.

For example:

```text
Maximum Agent Iterations
Maximum Tool Calls
Maximum Execution Time
```

If these limits are reached, the workflow should stop rather than continuing indefinitely.

---

# 15. External Service Errors

External dependencies may include:

```text
LLM Provider
Qdrant
Email Service
Authentication Provider
Other APIs
```

External failures should be isolated from the rest of the application.

For example:

```text
External Service
       │
       ▼
Timeout
       │
       ▼
Service Layer
       │
       ▼
Retry / Fallback
       │
       ▼
Safe Response
```

---

# 16. File Processing Errors

Document processing may fail because of:

- Unsupported file format
- Corrupted file
- Empty document
- Text extraction failure
- File size limit
- Encoding problems
- Embedding failure
- Vector indexing failure

A document should maintain a processing state.

Example:

```text
UPLOADED
    │
    ▼
PROCESSING
    │
 ┌──┴───────┐
 ▼          ▼
INDEXED    FAILED
```

If processing fails, the user should be informed that the document could not be processed.

---

# 17. Background Task Errors

Background tasks should not silently fail.

Example:

```text
Document Upload
      │
      ▼
Background Task
      │
      ▼
Processing
      │
 ┌────┴─────┐
 ▼          ▼
Success    Failure
 │          │
 ▼          ▼
INDEXED    FAILED
```

Failures should be:

- Logged
- Associated with the relevant task/resource
- Reflected in status
- Retryable where appropriate

---

# 18. Timeout Handling

Timeouts prevent a request from waiting indefinitely.

Potential timeout points include:

```text
Database
Qdrant
LLM
External APIs
Agent execution
File processing
```

Each external operation should have an appropriate timeout.

---

## Timeout Flow

```text
Request
  │
  ▼
External Service
  │
  ▼
Timeout
  │
  ▼
Cancel / Stop Operation
  │
  ▼
Retry or Fallback
  │
  ▼
Return Response
```

Timeout values should be configurable.

---

# 19. Rate Limit Handling

External AI providers and other services may impose rate limits.

Typical response:

```text
429 Too Many Requests
```

The backend should avoid immediately retrying repeatedly.

A controlled retry strategy may use:

```text
Exponential Backoff
```

Conceptually:

```text
Attempt 1
   ↓
Wait
   ↓
Attempt 2
   ↓
Longer Wait
   ↓
Attempt 3
```

A maximum retry count must be enforced.

---

# 20. Retry Strategy

Retries should only be used for errors that are likely to be temporary.

Suitable examples may include:

```text
Temporary network failure
Service unavailable
Transient timeout
Rate limiting
```

Retries are generally inappropriate for:

```text
Invalid credentials
Invalid request
Invalid input
Permission denied
Unsupported file type
```

---

## Retry Rules

A retry system should define:

```text
Maximum Attempts
Initial Delay
Maximum Delay
Backoff Strategy
Retryable Errors
```

---

# 21. Fallback Strategy

Fallbacks allow the application to continue functioning when a component is unavailable.

Potential examples:

```text
Primary LLM
     │
     ▼
Failure
     │
     ▼
Fallback LLM
```

Another example:

```text
RAG Retrieval
     │
     ▼
No Relevant Context
     │
     ▼
General AI Response
     │
     ▼
Clearly Indicate Limitation
```

Fallback behavior must not cause the system to fabricate information.

---

# 22. Logging Errors

Every significant backend error should generate a structured log.

A useful error log may contain:

```text
timestamp
log level
service
request ID
user ID (if appropriate and safe)
error code
exception type
operation
duration
```

Sensitive information must be excluded.

Never log:

```text
Passwords
Access Tokens
Refresh Tokens
API Keys
Full Sensitive Documents
```

---

# 23. User-Facing Error Messages

User-facing messages should be:

- Clear
- Concise
- Non-technical
- Actionable where possible

Avoid exposing messages such as:

```text
SQLAlchemy IntegrityError
ConnectionRefusedError
ProviderInternalServerError
```

Instead, provide a simple explanation.

Example:

```text
"Sorry, the service is temporarily unavailable. Please try again."
```

---

## Error Message Principle

```text
Technical Error
      │
      ├── Detailed Developer Log
      │
      └── Safe User Message
```

---

# 24. Global Exception Handling

The backend should use centralized exception handlers.

Conceptually:

```text
                    Exception
                        │
                        ▼
                Global Handler
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Log Error    Map Error      Request ID
                        │
                        ▼
                  API Response
```

This avoids repeating error-handling logic in every API route.

---

# 25. Error Monitoring

Production errors should be monitored.

Important metrics include:

```text
Total Errors
Errors by Endpoint
Errors by Error Type
LLM Failures
RAG Failures
Database Failures
Average Response Time
Timeout Rate
Retry Rate
```

The monitoring system can later be integrated with an observability platform.

---

# 26. Development vs Production Errors

Error responses may differ between development and production.

## Development

Developers may need more debugging information.

For example:

```text
Detailed stack trace
Exception type
Debug logs
```

---

## Production

Users should receive safe messages.

```text
Generic user-facing message
Request ID
Appropriate HTTP status
```

Detailed stack traces should remain in server-side logs.

---

# 27. Testing Error Handling

Error handling should be tested deliberately.

## API Tests

Test:

```text
Invalid request
Missing authentication
Invalid authentication
Forbidden access
Resource not found
Duplicate resource
```

---

## Database Tests

Test:

```text
Connection failure
Constraint violation
Transaction failure
Timeout
```

---

## AI Tests

Test:

```text
LLM timeout
LLM rate limit
LLM unavailable
Invalid model response
RAG retrieval failure
Embedding failure
```

---

## Background Task Tests

Test:

```text
Successful processing
Processing failure
Retry
Permanent failure
Status update
```

---

# 28. Error Handling Checklist

Before considering backend error handling complete:

```text
[ ] Standard HTTP status codes defined
[ ] Standard error response schema defined
[ ] Validation errors handled
[ ] Authentication errors handled
[ ] Authorization errors handled
[ ] Database errors handled
[ ] RAG errors handled
[ ] LLM errors handled
[ ] Agent errors handled
[ ] File-processing errors handled
[ ] Background-task errors handled
[ ] Timeouts configured
[ ] Retry strategy defined
[ ] Fallback strategy defined
[ ] Sensitive data excluded from logs
[ ] Global exception handling implemented
[ ] Request IDs supported
[ ] Error tests created
```

---

# 29. Summary

The error-handling architecture ensures that failures are handled consistently across the backend.

The overall approach is:

```text
                   Error
                     │
                     ▼
              Classify Error
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Client     Temporary   Internal
        Error       Error      Error
          │          │           │
          ▼          ▼           ▼
       Response    Retry /     Log +
                   Fallback    Response
          │          │           │
          └──────────┼───────────┘
                     ▼
                   Client
```

The system should prioritize:

- Security
- Reliability
- Clear user communication
- Detailed developer observability
- Controlled retries
- Safe fallbacks
- Consistent API behavior

Error handling should be implemented alongside each backend feature rather than added only after the application is complete.
