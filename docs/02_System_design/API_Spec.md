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
# 9. User APIs

The User module manages profile information and personalization settings.

---

## 9.1 Get Current User Profile

### Endpoint

```http
GET /users/me
```

---

### Description

Returns the authenticated user's profile.

---

### Authentication

✅ Required

---

### Headers

```http
Authorization: Bearer <ACCESS_TOKEN>
```

---

### Request Body

None

---

### Success Response

**200 OK**

```json
{
  "success": true,
  "data": {
    "id": "b2f79c9d-45e7-41c1-8db6-37f4b9d8f98e",
    "full_name": "Sharanya N",
    "email": "sharanya@example.com",
    "role": "user",
    "created_at": "2026-07-22T10:15:20Z"
  }
}
```

---

### Error Responses

```json
{
    "success": false,
    "message": "Unauthorized."
}
```

Status Code

```
401 Unauthorized
```

---

## 9.2 Update User Profile

### Endpoint

```http
PATCH /users/me
```

---

### Description

Updates editable user profile fields.

---

### Authentication

✅ Required

---

### Request Body

```json
{
    "full_name": "Sharanya N",
    "email": "sharanya@example.com"
}
```

---

### Validation Rules

| Field | Validation |
|---------|------------|
| full_name | 2–100 characters |
| email | Valid email |
| email | Must be unique |

---

### Success Response

```json
{
    "success": true,
    "message": "Profile updated successfully.",
    "data": {
        "full_name": "Sharanya N",
        "email": "sharanya@example.com"
    }
}
```

---

## 9.3 Delete User Account

### Endpoint

```http
DELETE /users/me
```

---

### Description

Deletes the authenticated user's account and all associated data.

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "message": "Account deleted successfully."
}
```

---

### Notes

Deleting a user also removes:

- Conversations
- Messages
- Uploaded Documents
- Memories
- Planner Tasks
- User Preferences

This is implemented using database cascade deletion.

---

## 9.4 Get User Preferences

### Endpoint

```http
GET /users/preferences
```

---

### Description

Returns personalization settings.

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "data": {
        "preferred_language": "English",
        "response_style": "Detailed",
        "theme": "Dark",
        "timezone": "Asia/Kolkata"
    }
}
```

---

## 9.5 Update User Preferences

### Endpoint

```http
PATCH /users/preferences
```

---

### Authentication

✅ Required

---

### Request Body

```json
{
    "preferred_language": "Hindi",
    "response_style": "Concise",
    "theme": "Light",
    "timezone": "Asia/Kolkata"
}
```

---

### Request Fields

| Field | Description |
|---------|-------------|
| preferred_language | Preferred interaction language |
| response_style | Concise / Detailed |
| theme | Light / Dark / System |
| timezone | User timezone |

---

### Success Response

```json
{
    "success": true,
    "message": "Preferences updated successfully."
}
```

---

## 9.6 Upload Profile Picture (Future)

### Endpoint

```http
POST /users/avatar
```

---

### Authentication

✅ Required

---

### Content-Type

```
multipart/form-data
```

---

### Request

```
avatar=<image_file>
```

Supported formats

- PNG
- JPG
- JPEG
- WEBP

Maximum size

```
5 MB
```

---

### Success Response

```json
{
    "success": true,
    "message": "Profile picture uploaded successfully.",
    "data": {
        "avatar_url": "/uploads/avatar/user123.png"
    }
}
```

---

## 9.7 Delete Profile Picture (Future)

### Endpoint

```http
DELETE /users/avatar
```

---

### Authentication

✅ Required

---

### Success Response

```json
{
    "success": true,
    "message": "Profile picture removed."
}
```

---

# User API Summary

| Method | Endpoint | Description |
|----------|-------------------------|------------------------------|
| GET | /users/me | Get current user |
| PATCH | /users/me | Update profile |
| DELETE | /users/me | Delete account |
| GET | /users/preferences | Get preferences |
| PATCH | /users/preferences | Update preferences |
| POST | /users/avatar | Upload avatar *(Future)* |
| DELETE | /users/avatar | Delete avatar *(Future)* |

---

# User API Flow

```text
User

↓

Login

↓

GET /users/me

↓

Display Profile

↓

Edit Profile

↓

PATCH /users/me

↓

Update Database

↓

Return Updated Profile
```

---

# Error Codes

| Status | Meaning |
|---------|----------|
|200|Success|
|400|Validation Error|
|401|Unauthorized|
|404|User Not Found|
|409|Email Already Exists|
|500|Internal Server Error|

---

# Notes

- Every endpoint requires a valid JWT except registration and login.
- User data is always scoped to the authenticated user.
- Email addresses are globally unique.
- Future versions may support profile images and additional user settings.
