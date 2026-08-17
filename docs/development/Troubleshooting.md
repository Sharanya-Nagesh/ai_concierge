# Troubleshooting

## 1. Purpose

This document provides a structured approach for identifying and resolving common development, integration and runtime issues in the AI Concierge project.

The objective is to make troubleshooting:

* Systematic
* Reproducible
* Easy to document
* Easy to communicate
* Suitable for both development and deployment environments

---

# 2. Troubleshooting Philosophy

When an issue occurs, avoid immediately changing multiple components.

Use the following approach:

```text
Problem
   ↓
Reproduce
   ↓
Identify Layer
   ↓
Collect Evidence
   ↓
Isolate Root Cause
   ↓
Apply Fix
   ↓
Test Fix
   ↓
Add Regression Test
   ↓
Document if Necessary
```

The goal is to fix the underlying cause rather than only the visible symptom.

---

# 3. System Layers

Issues should first be categorized by layer.

```text
User Interface
      ↓
Frontend
      ↓
API
      ↓
Backend Services
      ↓
Database
      ↓
RAG / Memory / Agent
      ↓
LLM / External Services
      ↓
Infrastructure
```

A failure at a lower layer can appear as a failure at a higher layer.

For example:

```text
Frontend shows error
       ↓
API request failed
       ↓
Backend could not connect to database
```

Therefore, debugging should proceed from evidence rather than assumptions.

---

# 4. First-Level Diagnosis

Before making changes, collect:

```text
Error message
Timestamp
Affected component
Request / operation
Expected behavior
Actual behavior
Recent code changes
Environment
Relevant logs
```

Ask:

1. Can the issue be reproduced?
2. Does it happen consistently?
3. Does it happen locally, in staging, or in production?
4. Did it start after a specific change?
5. Is the problem isolated to one component?

---

# 5. Check Application Status

Verify whether the required services are running.

For Docker-based environments:

```bash
docker ps
```

Check:

```text
Backend
Database
Redis, if configured
Vector store, if configured
Other supporting services
```

If a required service is not running, inspect its logs before changing configuration.

---

# 6. Check Git State

Before debugging a development issue:

```bash
git status
```

Review recent changes:

```bash
git log --oneline -n 10
```

Inspect uncommitted changes:

```bash
git diff
```

This helps determine whether the problem was introduced by a local modification.

---

# 7. Environment Variable Problems

Symptoms may include:

* Application fails during startup.
* Database connection fails.
* External AI service cannot be reached.
* Authentication fails.
* Vector store cannot be accessed.

Check:

```text
.env exists
Required variables are present
Variable names are correct
Values match the current environment
No accidental whitespace exists
Development credentials are being used
```

Never print secret values while debugging.

---

# 8. Missing Environment Variable

A common startup error is caused by a missing configuration variable.

Troubleshooting:

```text
Application Error
      ↓
Identify Missing Variable
      ↓
Check .env.example
      ↓
Check Local .env
      ↓
Add Correct Development Configuration
      ↓
Restart Application
```

If a new variable is required by the application, update:

```text
.env.example
```

and the appropriate documentation.

---

# 9. Python Environment Problems

Symptoms may include:

```text
ModuleNotFoundError
ImportError
Dependency conflict
Incorrect Python version
```

Check:

```bash
python --version
```

Verify the active environment.

Then inspect installed packages:

```bash
pip list
```

If dependencies are missing, reinstall them from the project's dependency configuration.

Avoid solving dependency issues by installing arbitrary packages without updating the project's dependency configuration.

---

# 10. Dependency Conflicts

A dependency conflict may occur when two packages require incompatible versions.

Troubleshooting:

```text
Identify conflicting packages
        ↓
Check dependency requirements
        ↓
Check project-supported versions
        ↓
Select compatible versions
        ↓
Update dependency configuration
        ↓
Reinstall environment
        ↓
Run tests
```

Dependency changes should be reviewed because they may affect unrelated components.

---

# 11. Node.js / Frontend Dependency Problems

Common symptoms:

```text
npm install failure
Module not found
Build failure
Runtime JavaScript error
```

Check:

```bash
node --version
npm --version
```

Verify that the frontend dependencies are installed.

If dependencies are inconsistent, reinstall according to the project's package-management workflow.

Do not delete lock files casually because they help maintain reproducible dependency versions.

---

# 12. Frontend Does Not Start

Troubleshooting sequence:

```text
Frontend fails to start
        ↓
Check Node.js version
        ↓
Check dependencies
        ↓
Check environment variables
        ↓
Inspect terminal error
        ↓
Check port availability
        ↓
Restart development server
```

If the problem persists, isolate whether it is:

* Dependency issue
* Configuration issue
* Build issue
* Source-code issue

---

# 13. Frontend Loads but API Requests Fail

Check the request flow:

```text
Browser
   ↓
Frontend
   ↓
API URL
   ↓
Backend
```

Inspect:

* Browser network tab
* Request URL
* HTTP method
* Request body
* Response status
* Response body
* Backend logs

Common causes include:

```text
Incorrect API URL
Backend not running
CORS configuration
Authentication failure
Incorrect request schema
Backend exception
```

---

# 14. CORS Problems

Symptoms may include browser messages indicating that a request was blocked by cross-origin policy.

Check:

```text
Frontend origin
Backend allowed origins
HTTP method
Headers
Credentials configuration
```

CORS configuration should be environment-specific where necessary.

Do not solve CORS problems by allowing every origin in production without understanding the security implications.

---

# 15. Backend Does Not Start

Troubleshooting sequence:

```text
Backend startup failure
        ↓
Check Python version
        ↓
Check virtual environment
        ↓
Check dependencies
        ↓
Check environment variables
        ↓
Check database configuration
        ↓
Inspect startup logs
```

The first meaningful error in the startup log is often more useful than the final cascading error.

---

# 16. API Returns 4xx Errors

A `4xx` response generally indicates a client/request-related problem.

Examples:

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Validation Error
```

Check:

```text
Request URL
HTTP method
Headers
Authentication
Request body
Parameter names
Schema
```

Compare the request with:

```text
docs/system_design/API_Spec.md
```

---

# 17. API Returns 5xx Errors

A `5xx` response generally indicates a server-side failure.

Troubleshooting:

```text
API 5xx
 ↓
Inspect backend logs
 ↓
Identify failing service
 ↓
Check database / external service
 ↓
Reproduce locally
 ↓
Fix root cause
 ↓
Add regression test
```

Do not expose internal stack traces to end users.

---

# 18. Database Connection Problems

Symptoms may include:

```text
Connection refused
Authentication failure
Timeout
Database does not exist
Migration failure
```

Check:

```text
Database service running
Host
Port
Database name
Username
Password
Network accessibility
```

For Docker environments, verify the database container is running.

---

# 19. Database Migration Problems

If a migration fails:

```text
Stop
 ↓
Read migration error
 ↓
Identify affected migration
 ↓
Inspect current database state
 ↓
Check migration dependencies
 ↓
Resolve safely
 ↓
Test on development/staging database
```

Do not manually modify migration history without understanding the consequences.

Production database changes require additional caution.

---

# 20. Database Query Problems

Symptoms may include:

* Slow API response
* Timeout
* Incorrect data
* Missing records
* Unexpected duplicate records

Investigate:

```text
Generated query
Database indexes
Query parameters
Transaction behavior
Database size
Connection pool
```

Performance issues should be measured rather than assumed.

---

# 21. Authentication Problems

Possible symptoms:

```text
401 Unauthorized
403 Forbidden
Token rejected
Session not recognized
User cannot access protected resource
```

Check:

```text
Authentication header
Token validity
Token expiry
Signing configuration
User identity
Authorization rules
```

Never log authentication tokens or secrets.

---

# 22. Authorization Problems

Authentication answers:

> Who is the user?

Authorization answers:

> What is the user allowed to access?

If authentication succeeds but access is denied:

```text
Check user identity
       ↓
Check role / permission
       ↓
Check resource ownership
       ↓
Check authorization policy
```

Authorization failures should not be solved by broadly increasing permissions.

---

# 23. External AI Service Problems

AI service failures may involve:

```text
Invalid credentials
Rate limits
Timeout
Network failure
Service outage
Model unavailable
Invalid request
```

Troubleshooting:

```text
Application
    ↓
AI Service Request
    ↓
Check request configuration
    ↓
Check credentials
    ↓
Check service response
    ↓
Check retry / timeout behavior
```

The application should handle temporary external-service failures gracefully.

---

# 24. LLM Latency Problems

High latency may originate from:

```text
Large prompt
Large context
Slow retrieval
Slow reranking
External API latency
Large model
Network latency
Repeated model calls
```

Break down the total latency:

```text
Request
  ↓
Authentication
  ↓
Retrieval
  ↓
Reranking
  ↓
Memory
  ↓
LLM
  ↓
Response
```

Measure each stage before optimizing.

---

# 25. RAG Problems

Common RAG symptoms:

```text
Relevant information not retrieved
Incorrect documents retrieved
Irrelevant context
Poor answer despite relevant documents
Slow retrieval
```

Debug the pipeline stage by stage:

```text
Question
   ↓
Query Processing
   ↓
Retrieved Documents
   ↓
Similarity / Ranking
   ↓
Reranking
   ↓
Final Context
   ↓
LLM Response
```

Do not assume that a poor final answer is always an LLM problem.

---

# 26. Retrieval Problems

If relevant documents are not retrieved, inspect:

```text
Embedding model
Embedding generation
Chunk size
Chunk overlap
Metadata
Similarity metric
Top-k
Query representation
Vector store
```

Compare retrieval results against a known evaluation set where available.

---

# 27. Reranking Problems

If initial retrieval is correct but final context is poor:

```text
Initial Retrieval
       ↓
Reranker
       ↓
Incorrect ordering
```

Check:

* Reranker configuration
* Input format
* Number of candidates
* Ranking scores
* Thresholds

Changes should be evaluated using consistent test data.

---

# 28. Memory Problems

Possible symptoms:

```text
Memory not saved
Incorrect memory retrieved
Irrelevant memory used
Memory persists unexpectedly
Memory appears for wrong user
```

Debug:

```text
Conversation
    ↓
Memory Extraction
    ↓
Memory Validation
    ↓
Memory Storage
    ↓
Memory Retrieval
    ↓
Context Injection
```

Verify user isolation at every stage.

---

# 29. Agent Problems

Possible symptoms:

```text
Wrong tool selected
Tool not selected
Repeated tool calls
Incorrect arguments
Agent loop
Unexpected response
```

Debug:

```text
User Request
     ↓
Agent Decision
     ↓
Selected Tool
     ↓
Tool Input
     ↓
Tool Output
     ↓
Next Decision
```

Agent behavior should be evaluated using representative test cases.

---

# 30. Agent Loop / Repeated Calls

If an agent repeatedly invokes the same operation:

```text
Agent
  ↓
Tool
  ↓
Agent
  ↓
Same Tool
  ↓
Agent
```

Check:

* Termination conditions
* Maximum iterations
* Tool output
* Agent state
* Error handling
* Retry configuration

A safety limit should prevent uncontrolled execution.

---

# 31. Model Loading Problems

For local ML models, common problems include:

```text
Model not found
Incompatible model format
Insufficient memory
GPU unavailable
CUDA mismatch
Tokenizer mismatch
```

Troubleshooting:

```text
Verify model identifier
       ↓
Verify downloaded artifacts
       ↓
Check framework version
       ↓
Check hardware compatibility
       ↓
Run minimal inference test
```

---

# 32. GPU Problems

If GPU acceleration fails:

```text
Check GPU visibility
       ↓
Check driver
       ↓
Check CUDA compatibility
       ↓
Check ML framework
       ↓
Run simple GPU test
```

Development should support CPU execution for components where GPU acceleration is not mandatory.

---

# 33. Out-of-Memory Problems

Symptoms:

```text
CUDA out of memory
RAM exhausted
Container killed
Process terminated
```

Potential causes:

```text
Large model
Large batch size
Large context
Large embeddings
Memory leak
Too many concurrent requests
```

Potential mitigations should be based on measured resource usage.

---

# 34. Container Problems

If a Docker container fails:

```text
Check container status
       ↓
Inspect logs
       ↓
Check environment variables
       ↓
Check exposed ports
       ↓
Check mounted volumes
       ↓
Check image version
```

Useful commands include:

```bash
docker ps
docker logs <container>
```

Avoid repeatedly rebuilding containers without understanding the underlying error.

---

# 35. Port Conflicts

If an application cannot bind to its configured port:

```text
Port already in use
        ↓
Identify process
        ↓
Stop unnecessary process
        ↓
Restart application
```

Alternatively, use a different development port if supported.

Port changes should be reflected in the relevant local configuration.

---

# 36. Network Problems

External service failures may result from:

```text
DNS failure
Network connectivity
Firewall
Proxy
Incorrect endpoint
TLS configuration
Timeout
```

Determine whether the problem affects:

```text
Only one service
All external services
Only local development
Only staging / production
```

This helps distinguish application problems from infrastructure problems.

---

# 37. Performance Problems

When an application becomes slow:

```text
Measure
 ↓
Locate bottleneck
 ↓
Profile
 ↓
Optimize
 ↓
Measure again
```

Potential metrics:

```text
API latency
Database latency
Retrieval latency
LLM latency
Memory latency
CPU
RAM
GPU
Network
```

Do not optimize components that have not been identified as bottlenecks.

---

# 38. Unexpected AI Output

AI output problems may arise from:

```text
Prompt
Context
Retrieved documents
Memory
Model
Temperature / generation settings
Tool results
Output parsing
```

Debug in this order:

```text
Input
 ↓
Prompt
 ↓
Retrieved Context
 ↓
Memory
 ↓
Model Output
 ↓
Post-processing
```

This makes it easier to identify where the unexpected behavior was introduced.

---

# 39. Evaluation Failures

If an AI component performs worse after a change:

```text
Identify changed component
        ↓
Compare evaluation results
        ↓
Inspect representative failures
        ↓
Determine regression source
        ↓
Rollback or improve
        ↓
Re-evaluate
```

Possible causes include:

* Model change
* Prompt change
* Retrieval change
* Chunking change
* Reranker change
* Memory change
* Agent change

AI evaluation should therefore be treated as part of the development lifecycle.

---

# 40. Logging and Debugging

Logs should contain enough context to reconstruct an issue without exposing sensitive data.

Useful fields may include:

```text
Timestamp
Request ID
Component
Operation
Status
Latency
Error type
```

Avoid:

```text
Passwords
Tokens
API keys
Sensitive personal information
Private credentials
```

---

# 41. Reproducing a Bug

A bug report should ideally include:

```text
Environment:
Development / Staging / Production

Steps:
1. ...
2. ...
3. ...

Expected:
...

Actual:
...

Error:
...

Recent Change:
...

Relevant Logs:
...
```

A reproducible issue is significantly easier to fix than an issue described only as "it doesn't work."

---

# 42. Regression Testing

When a bug is fixed, add a test when practical.

```text
Bug
 ↓
Fix
 ↓
Regression Test
 ↓
Future Code Changes
 ↓
Test Prevents Recurrence
```

This is especially important for:

* Authentication
* Database operations
* API contracts
* RAG retrieval
* Memory isolation
* Agent behavior

---

# 43. When to Update Documentation

Update documentation when a troubleshooting issue reveals:

* A new required environment variable
* A new setup step
* A changed API
* A changed architecture
* A deployment requirement
* A known limitation
* A recurring operational problem

For significant architectural changes, update:

```text
docs/system_design/Decision_Log.md
```

---

# 44. Escalation

If an issue cannot be resolved locally, collect evidence before escalating.

Provide:

```text
Problem description
Environment
Reproduction steps
Expected behavior
Actual behavior
Logs
Recent changes
Tests performed
```

Do not send secrets or sensitive credentials when sharing diagnostic information.

---

# 45. Troubleshooting Checklist

```text
☐ Reproduce the issue
☐ Identify environment
☐ Identify affected component
☐ Check recent changes
☐ Check application logs
☐ Check service status
☐ Check configuration
☐ Check database
☐ Check external dependencies
☐ Isolate root cause
☐ Apply minimal fix
☐ Run regression test
☐ Review side effects
☐ Update documentation if required
```

---

# 46. Final Troubleshooting Principles

The project follows these principles:

1. **Reproduce before modifying.**
2. **Use evidence rather than assumptions.**
3. **Debug one layer at a time.**
4. **Inspect logs and intermediate outputs.**
5. **Separate configuration problems from code problems.**
6. **Measure performance before optimizing.**
7. **Treat AI failures as pipeline failures until the failing stage is identified.**
8. **Protect secrets and sensitive information during debugging.**
9. **Add regression tests for important bugs.**
10. **Update documentation when recurring problems reveal missing knowledge.**

The objective is to turn troubleshooting from ad-hoc debugging into a repeatable engineering process.
