# API Specification

> **Project:** AI Concierge – Personalized AI Assistant

> **Document Version:** 2.0

> **Status:** Draft

---

# Table of Contents

1. Introduction
2. API Design Principles
3. Base URL
4. Authentication
5. Common Headers
6. Common Response Format
7. Error Handling
8. Authentication APIs
9. User APIs
10. Conversation APIs
11. Message APIs
12. Document APIs
13. Memory APIs
14. Planner APIs
15. Recommendation APIs
16. Agent APIs
17. Health APIs
18. Error Codes
19. Pagination
20. Rate Limiting
21. Versioning
22. Future APIs

---

# 1. Introduction

This document defines the REST API specification for the AI Concierge platform.

The APIs enable communication between the React frontend and the FastAPI backend while following RESTful principles.

Every endpoint specifies:

- Purpose
- HTTP Method
- URL
- Authentication
- Request Body
- Response Body
- Status Codes
- Error Responses

---

# 2. API Design Principles

The API follows these principles:

- RESTful architecture
- Stateless communication
- JSON request/response
- JWT Authentication
- Versioned endpoints
- Predictable URLs
- Consistent error handling
- Secure by default

---

# 3. Base URL

Development

```

http://localhost:8000/api/v1

```

Production

```

https://api.aiconcierge.com/api/v1

```

All endpoints in this document are relative to the Base URL.

---

# 4. Authentication

Protected endpoints require a JWT access token.

Example:

```

Authorization: Bearer <ACCESS_TOKEN>

```

If authentication fails:

```

401 Unauthorized

```

---

# 5. Common Headers

Request

```

Content-Type: application/json

Authorization: Bearer <TOKEN>

Accept: application/json

```

Response

```

Content-Type: application/json

```

---

# 6. Standard Response Format

## Success

```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": {}
}
```

---

## Error

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [
    {
      "field": "email",
      "message": "Email is required."
    }
  ]
}
```

---

# 7. HTTP Status Codes

| Code | Meaning |
|------|----------|
|200|OK|
|201|Created|
|204|No Content|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|429|Too Many Requests|
|500|Internal Server Error|

---

# 8. Authentication APIs

The Authentication module manages user registration, login, logout, and account security.
