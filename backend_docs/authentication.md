# Authentication

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** Backend Authentication Design

---

# Table of Contents

1. Introduction
2. Authentication Objectives
3. Authentication Architecture
4. User Registration
5. Password Security
6. Login Flow
7. JWT Authentication
8. Access Token
9. Refresh Token
10. Token Lifecycle
11. Protected Endpoints
12. Authorization
13. User Data Isolation
14. Logout
15. Token Expiration
16. Authentication Errors
17. Security Requirements
18. Authentication API Endpoints
19. Implementation Structure
20. Testing
21. Future Enhancements
22. Summary

---

# 1. Introduction

Authentication is responsible for verifying the identity of users accessing AI Concierge.

The authentication system ensures that:

- Users can create accounts
- Users can securely log in
- Authenticated users can access protected resources
- Users can only access their own data
- Authentication tokens expire appropriately
- Passwords are never stored in plain text

The general authentication architecture is:

```text
User
  │
  ▼
Authentication API
  │
  ▼
Credential Verification
  │
  ▼
JWT Token
  │
  ▼
Authenticated Requests
```

---

# 2. Authentication Objectives

The authentication system should provide:

- Secure registration
- Secure login
- Password hashing
- JWT-based authentication
- Access-token validation
- Refresh-token support
- Protected API endpoints
- User-level authorization
- User data isolation
- Secure logout
- Token expiration
- Consistent authentication errors

---

# 3. Authentication Architecture

The authentication system consists of several components:

```text
                    Authentication
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
     Registration       Login         Token Validation
          │               │               │
          ▼               ▼               ▼
       Password        Password         JWT
       Hashing         Verification    Verification
                          │
                          ▼
                    Token Generation
```

The backend will use:

- FastAPI for authentication endpoints
- Pydantic for request/response validation
- PostgreSQL for user records
- SQLAlchemy for database access
- Secure password hashing
- JWT for authentication tokens

---

# 4. User Registration

Registration allows a new user to create an account.

## Registration Flow

```text
User
 │
 ▼
Registration Form
 │
 ▼
POST /api/v1/auth/register
 │
 ▼
Validate Input
 │
 ▼
Check Existing Account
 │
 ├───────────────┐
 │               │
Exists          New User
 │               │
 ▼               ▼
Error        Hash Password
                 │
                 ▼
          Create User Record
                 │
                 ▼
          Return Registration
                 │
                 ▼
              Success
```

---

## Registration Data

The initial registration request may contain:

```text
Email
Password
Display Name
```

Additional profile information can be collected later.

---

## Email Validation

The backend should validate that:

- Email is present
- Email has a valid format
- Email is normalized consistently
- Duplicate accounts are prevented

---

# 5. Password Security

Passwords must **never be stored in plain text**.

Instead:

```text
User Password
      │
      ▼
Password Hashing Algorithm
      │
      ▼
Password Hash
      │
      ▼
PostgreSQL
```

When a user logs in:

```text
Entered Password
      │
      ▼
Password Verification
      │
      ▼
Stored Password Hash
```

The system verifies whether the password corresponds to the stored hash.

---

## Password Requirements

The application should define minimum password requirements such as:

- Minimum length
- Reasonable complexity
- No obviously invalid values

Password requirements should balance security and usability.

---

# 6. Login Flow

The login process is:

```text
User
 │
 ▼
Email + Password
 │
 ▼
POST /api/v1/auth/login
 │
 ▼
Validate Request
 │
 ▼
Find User
 │
 ▼
Verify Password
 │
 ├──────────────┐
 │              │
Invalid        Valid
 │              │
 ▼              ▼
Error       Generate Tokens
                │
                ▼
          Return Authentication
                │
                ▼
              Client
```

---

# 7. JWT Authentication

JWT stands for **JSON Web Token**.

A JWT allows the backend to identify the authenticated user when processing subsequent requests.

General flow:

```text
Login
  │
  ▼
Credentials Verified
  │
  ▼
JWT Generated
  │
  ▼
Client Receives Token
  │
  ▼
Token Included in Requests
  │
  ▼
Backend Verifies Token
  │
  ▼
User Identified
```

---

## JWT Request

Authenticated requests will generally use the:

```text
Authorization
```

HTTP header.

Conceptually:

```text
Authorization: Bearer <access-token>
```

The exact token value must never be hard-coded or committed to source control.

---

# 8. Access Token

The access token is used to authenticate API requests.

Example flow:

```text
Client
   │
   │ Access Token
   ▼
FastAPI
   │
   ▼
Validate JWT
   │
   ▼
Extract User Identity
   │
   ▼
Authorize Request
```

Access tokens should have a relatively short lifetime.

This limits the impact if an access token is compromised.

---

## Access Token Claims

The token may contain claims such as:

```text
subject / user identifier
issued-at timestamp
expiration timestamp
token type
```

Only the minimum information required for authentication should be included.

Sensitive personal information should not be placed inside JWT claims unnecessarily.

---

# 9. Refresh Token

A refresh token allows a user to obtain a new access token without entering their password again.

General flow:

```text
Access Token Expires
        │
        ▼
Client Sends Refresh Token
        │
        ▼
Backend Validates Refresh Token
        │
        ▼
Generate New Access Token
        │
        ▼
Continue Session
```

This provides a balance between:

- Security
- User convenience

---

## Refresh Token Storage

Refresh-token handling should be designed carefully.

Possible approaches include:

- Secure HTTP-only cookies
- Server-side token storage
- Token rotation

The final approach should be selected during implementation based on the deployment architecture.

---

# 10. Token Lifecycle

The complete lifecycle is:

```text
             Login
               │
               ▼
       Generate Tokens
               │
               ▼
        Access Token
               │
               ▼
       Authenticated APIs
               │
               ▼
       Access Token Expires
               │
               ▼
        Refresh Token
               │
               ▼
    Generate New Access Token
               │
               ▼
       Continue Session
```

If the refresh token is invalid or expired:

```text
Refresh Failed
      │
      ▼
Require Login Again
```

---

# 11. Protected Endpoints

Not every endpoint needs authentication.

## Public Endpoints

Examples:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
GET  /api/v1/health
```

## Protected Endpoints

Examples:

```text
GET  /api/v1/users/me

GET  /api/v1/conversations
POST /api/v1/conversations

POST /api/v1/chat

GET  /api/v1/documents
POST /api/v1/documents

GET  /api/v1/memory
POST /api/v1/memory

GET  /api/v1/planner
POST /api/v1/planner
```

The exact endpoint list is defined in:

```text
docs/system_design/API_spec.md
```

---

# 12. Authorization

Authentication answers:

> **Who is this user?**

Authorization answers:

> **What is this user allowed to access?**

The backend must perform both checks.

Example:

```text
Request
   │
   ▼
Is user authenticated?
   │
   ├── No → 401 Unauthorized
   │
   ▼
Is user authorized for this resource?
   │
   ├── No → 403 Forbidden
   │
   ▼
Allow operation
```

---

# 13. User Data Isolation

User data must be isolated.

For example:

```text
User A
 ├── Conversations
 ├── Documents
 ├── Memories
 └── Planner

User B
 ├── Conversations
 ├── Documents
 ├── Memories
 └── Planner
```

A request from User A must never return User B's information.

---

## Ownership Verification

When retrieving a resource, the backend should verify ownership.

Conceptually:

```text
Request
   │
   ▼
Authenticated User ID
   │
   ▼
Requested Resource
   │
   ▼
Check Resource Owner
   │
 ┌─┴─────────────┐
 │               │
Match          Different
 │               │
 ▼               ▼
Allow         Deny
```

This check must happen on the backend.

The frontend must never be trusted to enforce data ownership.

---

# 14. Logout

Logout should invalidate the user's authenticated session as appropriate for the selected token strategy.

For example:

```text
User
 │
 ▼
Logout
 │
 ▼
Client Removes Session Credentials
 │
 ▼
Refresh Token Invalidated
 │
 ▼
User Must Authenticate Again
```

If refresh-token rotation or server-side token tracking is used, the backend should invalidate the relevant refresh session.

---

# 15. Token Expiration

Tokens must have an expiration time.

Example conceptual policy:

```text
Access Token
    ↓
Short Lifetime

Refresh Token
    ↓
Longer Lifetime
```

The exact durations should be configurable rather than hard-coded.

For example:

```text
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS
```

These values should be stored in application configuration.

---

# 16. Authentication Errors

The API should return consistent authentication errors.

| Situation | HTTP Status |
|---|---:|
| Invalid credentials | 401 |
| Missing authentication | 401 |
| Invalid token | 401 |
| Expired token | 401 |
| Insufficient permissions | 403 |
| Duplicate registration | 409 |
| Invalid request | 422 |

The response should not reveal unnecessary security-sensitive information.

---

## Example

Instead of exposing:

```text
"User exists but password is incorrect."
```

a login failure can use a generic message such as:

```text
"Invalid email or password."
```

This reduces unnecessary account-enumeration risk.

---

# 17. Security Requirements

Authentication must follow these principles.

## 17.1 Never Store Plain-Text Passwords

Only password hashes should be persisted.

---

## 17.2 Protect JWT Secrets

JWT signing secrets must be stored in environment configuration.

They must not appear in:

```text
Source code
Git history
README files
Public documentation
```

---

## 17.3 Use HTTPS in Production

Authentication tokens and credentials should be transmitted over encrypted connections.

---

## 17.4 Secure Cookies

If cookies are used for refresh tokens, production configuration should consider:

```text
HttpOnly
Secure
SameSite
```

---

## 17.5 Rate Limiting

Authentication endpoints should eventually support rate limiting to reduce:

- Brute-force attacks
- Credential stuffing
- Automated abuse

---

## 17.6 Avoid Sensitive Logging

Do not log:

```text
Passwords
JWT values
Refresh tokens
API keys
```

---

# 18. Authentication API Endpoints

The initial authentication API may include:

| Method | Endpoint | Purpose | Authentication |
|---|---|---|---|
| POST | `/api/v1/auth/register` | Register user | No |
| POST | `/api/v1/auth/login` | Authenticate user | No |
| POST | `/api/v1/auth/refresh` | Refresh access token | Refresh token |
| POST | `/api/v1/auth/logout` | End session | Yes |
| GET | `/api/v1/users/me` | Retrieve current user | Yes |

The exact request and response schemas are defined in the API specification.

---

# 19. Implementation Structure

Authentication-related code should be separated into appropriate modules.

Conceptual structure:

```text
backend/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── auth.py
│   │
│   ├── core/
│   │   ├── security.py
│   │   └── config.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── auth.py
│   │
│   ├── services/
│   │   └── auth_service.py
│   │
│   └── repositories/
│       └── user_repository.py
```

The exact project structure may evolve during implementation.

---

# 20. Testing

Authentication should be tested independently before integrating it with the rest of the application.

## Registration Tests

Test:

- Valid registration
- Invalid email
- Weak password
- Missing required fields
- Duplicate account

---

## Login Tests

Test:

- Correct credentials
- Incorrect password
- Unknown account
- Invalid request
- Successful token generation

---

## Token Tests

Test:

- Valid access token
- Expired access token
- Invalid token
- Malformed token
- Missing token

---

## Authorization Tests

Test:

- Authenticated user accessing own resource
- User attempting to access another user's resource
- Unauthenticated access to protected endpoint
- Insufficient permissions

---

# 21. Future Enhancements

Potential future authentication features include:

- OAuth 2.0 providers
- Google authentication
- Microsoft authentication
- GitHub authentication
- Multi-factor authentication
- Email verification
- Password reset
- Device/session management
- Login history
- Suspicious-login detection
- Account recovery

These should be added only when required by the project's scope.

---

# 22. Authentication Summary

The authentication system provides secure identity management for AI Concierge.

The overall flow is:

```text
                 REGISTER
                    │
                    ▼
              Password Hash
                    │
                    ▼
                PostgreSQL
                    │
                    ▼
                  LOGIN
                    │
                    ▼
             Verify Password
                    │
                    ▼
              Generate JWT
                    │
                    ▼
            Access Protected APIs
                    │
                    ▼
             Validate JWT
                    │
                    ▼
           Identify Current User
                    │
                    ▼
          Check Resource Ownership
                    │
                    ▼
             Allow / Deny
```

The design prioritizes secure credential handling, short-lived access tokens, controlled refresh sessions, backend-enforced authorization, and strict user-data isolation.
