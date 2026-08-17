# Git Workflow

## 1. Purpose

This document defines the Git workflow for the AI Concierge project.

The workflow is designed to maintain:

* Clean version history
* Traceable development
* Controlled feature integration
* Consistent collaboration
* Reliable code review
* Safe deployment
* Clear separation between stable and experimental work

---

# 2. Repository Strategy

The project uses Git for:

* Source-code version control
* Documentation version control
* Collaboration
* Code review
* CI/CD integration
* Release management

The repository contains:

```text
docs/
backend_docs/
ml/
backend/
frontend/
infrastructure/
tests/
```

Changes to documentation and implementation should be tracked through the same repository.

---

# 3. Main Branches

The project uses the following conceptual branches:

```text
main
│
├── feature/*
├── fix/*
├── docs/*
├── experiment/*
└── refactor/*
```

## `main`

The `main` branch represents the stable version of the project.

It should contain code that:

* Builds successfully
* Passes required tests
* Meets project quality standards
* Is suitable for demonstration or deployment

Direct development on `main` should be avoided.

---

# 4. Feature Branches

New functionality should be developed in a dedicated feature branch.

Naming convention:

```text
feature/<short-description>
```

Examples:

```text
feature/user-authentication
feature/chat-api
feature/retrieval-pipeline
feature/user-memory
```

A feature branch should contain changes belonging to one logical feature or development task.

---

# 5. Bug-Fix Branches

Bug fixes should use:

```text
fix/<short-description>
```

Examples:

```text
fix/auth-token-validation
fix/retrieval-timeout
fix/database-connection
```

The branch should focus on resolving the identified problem without introducing unrelated changes.

---

# 6. Documentation Branches

Documentation-only changes may use:

```text
docs/<short-description>
```

Examples:

```text
docs/api-spec-update
docs/backend-architecture
docs/ml-documentation
docs/project-readme
```

This is useful when a change does not require modification of application code.

---

# 7. Experiment Branches

Experimental ML/AI work should use:

```text
experiment/<short-description>
```

Examples:

```text
experiment/embedding-model
experiment/reranking-strategy
experiment/prompt-optimization
```

Experimental work should not automatically be merged into the stable implementation.

The experiment should first be evaluated against the project's defined criteria.

---

# 8. Refactoring Branches

Refactoring work should use:

```text
refactor/<short-description>
```

Examples:

```text
refactor/service-layer
refactor/rag-module
refactor/database-access
```

Refactoring should preserve existing behavior unless the change explicitly includes a functional modification.

---

# 9. Creating a Branch

Before creating a new branch, synchronize with the latest `main` branch.

Conceptually:

```bash
git checkout main
git pull
git checkout -b feature/example-feature
```

The exact command may vary depending on the configured Git workflow.

---

# 10. Commit Standards

Commits should represent small, logical changes.

A commit should ideally answer:

> What changed?

Examples:

```text
Add user authentication service
Implement chat API endpoint
Add conversation database model
Document RAG architecture
Add retrieval evaluation tests
```

Avoid vague commit messages such as:

```text
changes
updates
fixed stuff
work
final
new code
```

---

# 11. Commit Structure

A good commit should generally:

* Have a clear purpose
* Contain related changes
* Avoid unrelated modifications
* Be easy to review
* Be easy to revert

For example, instead of:

```text
Add API + redesign frontend + modify database + update documentation
```

prefer separate logical commits:

```text
Add conversation database model
Add chat API endpoint
Update API documentation
Update chat interface
```

---

# 12. Recommended Commit Format

The project may use a lightweight conventional format:

```text
<type>: <description>
```

Recommended types:

```text
feat
fix
docs
refactor
test
chore
perf
```

Examples:

```text
feat: add conversation API
fix: handle expired authentication token
docs: update database design
refactor: simplify retrieval service
test: add chat API tests
chore: update development dependencies
perf: optimize document retrieval
```

---

# 13. Commit Message Guidelines

Commit messages should:

* Be concise
* Start with an action
* Describe the actual change
* Avoid unnecessary implementation details

Prefer:

```text
feat: add conversation history endpoint
```

over:

```text
feat: made some changes to the API so that users can now get their previous conversations
```

---

# 14. Pull Requests

Changes should be merged through a Pull Request when collaboration or formal review is required.

A Pull Request should explain:

### What changed?

Describe the implementation.

### Why was it changed?

Describe the requirement or problem.

### How was it tested?

List relevant tests or validation performed.

### Documentation impact

Mention documentation that was added or updated.

---

# 15. Pull Request Example Structure

```text
## Summary

Implemented the initial conversation API.

## Changes

- Added conversation endpoint
- Added request/response schemas
- Added service-layer logic
- Added API tests

## Testing

- Unit tests
- API tests

## Documentation

- Updated API specification
```

The actual Pull Request template may be formalized later under:

```text
.github/
```

---

# 16. Code Review

Before merging, reviewers should check:

* Functional correctness
* Architecture
* Readability
* Security
* Error handling
* Tests
* Performance
* Documentation
* Compatibility

Review comments should be specific and constructive.

---

# 17. Merge Requirements

A branch should be merged only after the required checks have passed.

Typical requirements include:

```text
Code review
     +
Tests
     +
Linting
     +
Type checking
     +
Build validation
     +
Documentation update
```

Not every change requires every check, but the appropriate validation should be performed based on the scope of the change.

---

# 18. Keeping Branches Updated

Long-running branches should periodically synchronize with `main`.

This reduces the chance of large merge conflicts.

Conceptually:

```text
main
 │
 ├───────────────┐
 │               │
 ▼               ▼
feature branch   updates
 │               │
 └───────┬───────┘
         ▼
      synchronize
         │
         ▼
       merge
```

The project should avoid keeping feature branches open for unnecessarily long periods.

---

# 19. Merge Conflicts

When conflicts occur:

1. Identify the conflicting files.
2. Understand both changes.
3. Resolve conflicts carefully.
4. Run tests.
5. Review the resulting diff.
6. Commit the conflict resolution.

Do not blindly accept one side of a conflict without understanding the impact.

---

# 20. Documentation Changes

Documentation should be version-controlled just like source code.

For example:

```text
docs/system_design/API_Spec.md
```

should be updated when an API contract changes.

Similarly:

```text
backend_docs/Backend_Architecture.md
```

should remain aligned with the backend implementation.

---

# 21. ML / AI Experiment Tracking

ML experiments should be kept separate from stable production changes.

For example:

```text
experiment/embedding-model-a
experiment/embedding-model-b
```

Each experiment should record:

* Objective
* Configuration
* Model/version
* Dataset/version
* Evaluation metrics
* Result
* Decision

Once an experiment is validated, the resulting implementation can be moved into the appropriate production branch.

---

# 22. Prompt Changes

Prompt modifications can affect AI behavior even when application code does not change.

Therefore prompt changes should be treated as meaningful changes.

Examples:

```text
docs: document prompt behavior
feat: add prompt versioning
test: evaluate updated response prompt
```

Prompt changes should be evaluated when they can affect system behavior.

---

# 23. Configuration and Secrets

Never commit real secrets.

The repository may contain:

```text
.env.example
```

but should not contain production credentials.

Avoid committing:

```text
.env
credentials.json
private keys
API tokens
database passwords
```

If a secret is accidentally committed, it should be revoked and replaced rather than simply deleted from the latest commit.

---

# 24. Generated Files

Generated artifacts should not automatically be committed.

Examples may include:

```text
__pycache__/
build/
dist/
temporary files
local logs
large generated datasets
```

The project's `.gitignore` should define which files are excluded.

---

# 25. Large ML Artifacts

Large model files, datasets and generated artifacts should not be committed directly to Git unless explicitly justified.

Depending on project requirements, use appropriate artifact or model storage.

The Git repository should primarily contain:

```text
Source code
Configuration templates
Documentation
Tests
Small metadata files
```

rather than large binary artifacts.

---

# 26. Releases

Stable versions may be marked using Git tags.

Example:

```text
v0.1.0
v0.2.0
v1.0.0
```

Release numbering can follow semantic versioning:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
1.2.3
```

where:

* MAJOR indicates breaking changes.
* MINOR indicates backward-compatible functionality.
* PATCH indicates backward-compatible fixes.

---

# 27. Hotfixes

Critical production issues may require a dedicated hotfix branch.

Example:

```text
hotfix/security-vulnerability
```

The fix should be:

1. Implemented
2. Tested
3. Reviewed
4. Merged into the stable branch
5. Released
6. Documented where necessary

---

# 28. CI/CD Integration

Git workflow should eventually integrate with the project's CI/CD pipeline.

A typical flow is:

```text
Developer
   │
   ▼
Feature Branch
   │
   ▼
Commit
   │
   ▼
Pull Request
   │
   ▼
CI Checks
   │
   ├── Tests
   ├── Lint
   ├── Type Check
   └── Build
   │
   ▼
Code Review
   │
   ▼
Merge
   │
   ▼
main
   │
   ▼
Deployment
```

The detailed CI/CD process is documented separately under:

```text
docs/mlops/CI_CD.md
```

---

# 29. Recommended Development Cycle

For normal feature development:

```text
1. Review requirement
        ↓
2. Review relevant documentation
        ↓
3. Create branch
        ↓
4. Implement feature
        ↓
5. Add/update tests
        ↓
6. Update documentation
        ↓
7. Run validation
        ↓
8. Commit changes
        ↓
9. Create Pull Request
        ↓
10. Review
        ↓
11. Merge
```

This ensures that implementation, testing and documentation evolve together.

---

# 30. Git Workflow for This Project

The overall workflow can be summarized as:

```text
                    main
                     │
       ┌─────────────┼─────────────┐
       │             │             │
       ▼             ▼             ▼
   feature/*      docs/*      experiment/*
       │             │             │
       ▼             ▼             ▼
    develop       review        evaluate
       │             │             │
       └─────────────┼─────────────┘
                     ▼
                  Pull Request
                     │
                     ▼
                  CI Checks
                     │
                     ▼
                   Review
                     │
                     ▼
                    main
```

The exact branching strategy may evolve as the project moves from individual development to team-based development.

---

# 31. Final Guidelines

The Git workflow for the AI Concierge project follows these principles:

1. Keep `main` stable.
2. Use branches for meaningful changes.
3. Keep commits small and logical.
4. Use descriptive commit messages.
5. Review important changes before merging.
6. Run appropriate tests before merging.
7. Keep documentation synchronized with implementation.
8. Separate ML experiments from production changes.
9. Never commit secrets.
10. Avoid committing unnecessary generated or large artifacts.
11. Use CI/CD to automate validation.
12. Record significant architectural decisions.
13. Prefer short-lived feature branches.
14. Make the Git history understandable to another developer.

The objective is not merely to maintain Git history, but to make the project's development process **traceable, reproducible and maintainable**.
