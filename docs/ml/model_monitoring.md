# Model Monitoring

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / Production Monitoring

---

# Table of Contents

1. Introduction
2. Why Model Monitoring Is Required
3. What Should Be Monitored?
4. Monitoring Architecture
5. Application Metrics
6. LLM Metrics
7. Retrieval Metrics
8. Reranker Metrics
9. RAG Quality Monitoring
10. Hallucination Monitoring
11. Multilingual Monitoring
12. Code-Mixed Monitoring
13. Memory and Personalization Monitoring
14. Latency Monitoring
15. Token and Cost Monitoring
16. Error Monitoring
17. Data Drift
18. Model Drift
19. Prompt Drift
20. Knowledge Base Changes
21. User Feedback
22. Logging Strategy
23. Traceability
24. Alerts
25. Dashboards
26. Offline Monitoring
27. Online Monitoring
28. Privacy and Security
29. Failure Handling
30. Retraining and Model Updates
31. Monitoring Workflow
32. Implementation Strategy
33. Future Improvements
34. Summary

---

# 1. Introduction

Building an ML/RAG system is only the first step.

After deployment, the system must be continuously monitored.

A model that performs well during development may behave differently in production because:

```text
User queries change
+
Knowledge base changes
+
Traffic changes
+
Models change
+
Prompts change
+
Data distribution changes
```

Therefore, monitoring is required to determine whether the AI Concierge continues to work as expected.

---

# 2. Why Model Monitoring Is Required

Without monitoring, failures may remain unnoticed.

For example:

```text
Embedding model changes
        ↓
Retrieval quality decreases
        ↓
LLM receives poorer context
        ↓
Answer quality decreases
        ↓
Users receive worse responses
```

If no monitoring exists, the problem may be difficult to identify.

Monitoring helps answer:

```text
Is the system healthy?

Is retrieval working?

Is the LLM responding correctly?

Are responses becoming slower?

Are costs increasing?

Are hallucinations increasing?

Are some languages performing poorly?

Are users dissatisfied?

```

---

# 3. What Should Be Monitored?

Monitoring should cover multiple layers.

```text
                    AI Concierge
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
   Application          ML/RAG          Infrastructure
       │                 │                 │
       ▼                 ▼                 ▼
    Errors           Retrieval         CPU / Memory
    Requests         Groundedness      GPU
    Sessions         Hallucination     Network
                     Latency
                     Cost
```

Monitoring should therefore not focus only on the LLM.

---

# 4. Monitoring Architecture

A conceptual architecture is:

```text
                    User
                     │
                     ▼
                AI Concierge
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Backend        RAG          LLM
        │            │            │
        └────────────┼────────────┘
                     │
                     ▼
               Metrics / Logs
                     │
                     ▼
                Monitoring
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Dashboard     Alerts       Reports
```

The exact monitoring tools can be selected during implementation.

---

# 5. Application Metrics

The backend should monitor basic application-level metrics.

Examples:

```text
Requests per minute
Requests per hour
Active sessions
Successful requests
Failed requests
HTTP error rates
Tool failures
Timeouts
```

These metrics help determine whether the application itself is healthy.

---

# 6. LLM Metrics

LLM-specific metrics may include:

```text
Response latency
Input tokens
Output tokens
Total tokens
Requests
Errors
Timeouts
Retries
Model failures
```

For example:

```text
Average input tokens
Average output tokens
Average response time
P95 response time
```

Monitoring these values can reveal unexpected changes.

---

# 7. Retrieval Metrics

The RAG retrieval layer should also be monitored.

Potential metrics include:

```text
Number of retrieved chunks
Similarity scores
Top-K scores
Retrieval latency
Empty retrieval rate
Low-score retrieval rate
```

A sudden increase in:

```text
Queries with no useful results
```

may indicate a problem with:

```text
Embeddings
Knowledge base
Chunking
Metadata filters
Query processing
```

---

# 8. Reranker Metrics

If a reranker is used, monitor:

```text
Reranking latency
Number of candidates
Final number of chunks
Reranker score distribution
Reranker failures
Fallback frequency
```

For example:

```text
Qdrant
  ↓
20 candidates
  ↓
Reranker
  ↓
5 final chunks
```

If the reranker frequently fails, the system may need to fall back to vector ranking.

That fallback rate should be measurable.

---

# 9. RAG Quality Monitoring

Production monitoring should attempt to detect deterioration in RAG quality.

Possible indicators include:

```text
Low retrieval scores
Empty retrieval
Repeated fallback
Low answer confidence
Negative user feedback
Human review failures
```

Production quality monitoring can be supplemented by periodically running a fixed evaluation dataset.

---

# 10. Hallucination Monitoring

Hallucination should be treated as a quality risk.

Possible indicators include:

```text
Unsupported claims
Contradictions with retrieved context
User corrections
Negative feedback
Human evaluation failures
```

A practical architecture is:

```text
Generated Answer
       │
       ▼
Grounding Check
       │
       ├── Supported
       │
       └── Potentially Unsupported
                         │
                         ▼
                     Review / Log
```

Automated hallucination detection is imperfect.

Therefore, it should be treated as a monitoring signal rather than absolute truth.

---

# 11. Multilingual Monitoring

The system should monitor performance by language.

Instead of only measuring:

```text
Overall Accuracy
```

track metrics such as:

```text
Language A
Language B
Language C
...
```

Possible measurements:

```text
Retrieval quality
Answer quality
Latency
Fallback rate
User feedback
```

This can reveal problems hidden by overall averages.

For example:

```text
Overall performance → Good

Language A → Good
Language B → Good
Language C → Poor
```

The overall metric might not immediately reveal this imbalance.

---

# 12. Code-Mixed Monitoring

Code-mixed queries should be tracked separately when possible.

Useful metadata includes:

```text
Detected language pattern
Code-mixed flag
Retrieval performance
Response language
Fallback rate
User feedback
```

This helps determine whether code-mixed interactions behave differently from monolingual interactions.

---

# 13. Memory and Personalization Monitoring

The personalization system should also be monitored.

Important signals include:

```text
Memory retrieval frequency
Memory retrieval relevance
Memory lookup latency
Incorrect personalization reports
Memory update failures
```

The system should not assume:

```text
More memory
=
Better response
```

Irrelevant memories can reduce response quality.

---

# 14. Latency Monitoring

Latency should be measured across the entire pipeline.

For example:

```text
Request
  │
  ├── Query Processing
  │
  ├── Embedding
  │
  ├── Vector Search
  │
  ├── Reranking
  │
  ├── LLM
  │
  └── Response
```

Each component should ideally have its own latency measurement.

---

## Percentile Latency

Average latency alone is insufficient.

Useful measurements include:

```text
P50
P90
P95
P99
```

For example:

```text
P50 = typical request
P95 = slow requests
P99 = extreme slow requests
```

---

# 15. Token and Cost Monitoring

LLM usage can generate significant costs.

Monitor:

```text
Input tokens
Output tokens
Total tokens
Cost per request
Cost per session
Cost per day
Cost per user
```

A sudden increase in input tokens may indicate:

```text
Too much conversation history
Too much memory
Too many retrieved chunks
Prompt growth
```

---

# 16. Error Monitoring

Errors should be categorized.

Examples:

```text
Embedding error
Vector database error
Reranker error
LLM error
Tool error
Timeout
Validation error
Authentication error
```

Instead of storing only:

```text
Request failed
```

the system should record the relevant failure category.

This makes debugging easier.

---

# 17. Data Drift

Data drift occurs when incoming data changes over time.

For an AI Concierge, user queries may change.

For example:

```text
Earlier:
Mostly short English queries

Later:
More multilingual and code-mixed queries
```

This may affect system performance.

Potential signals include:

```text
Query length distribution
Language distribution
Intent distribution
Code-mixed frequency
Topic distribution
```

---

# 18. Model Drift

Model drift can occur when the deployed model becomes less suitable for the current data distribution.

The system should therefore track:

```text
Model version
Performance
Error rates
Evaluation metrics
User feedback
```

If a model is replaced:

```text
Old Model
   ↓
Baseline
   ↓
New Model
   ↓
Evaluation
   ↓
Deployment
```

A new model should not automatically be deployed merely because it is newer.

---

# 19. Prompt Drift

Prompts are part of the system configuration.

Changing a prompt can change model behavior.

Therefore, monitor:

```text
Prompt version
Prompt changes
Evaluation results
Production quality
```

Example:

```text
Prompt v1
   ↓
Evaluation
   ↓
Production

Prompt v2
   ↓
Evaluation
   ↓
Compare with v1
   ↓
Deploy only if acceptable
```

---

# 20. Knowledge Base Changes

RAG depends heavily on the knowledge base.

If documents change:

```text
Document Added
Document Updated
Document Deleted
```

retrieval behavior may change.

The system should therefore track:

```text
Knowledge base version
Document version
Embedding version
Index version
```

This helps explain retrieval changes.

---

# 21. User Feedback

User feedback is an important production signal.

Possible feedback mechanisms include:

```text
👍 Helpful
👎 Not Helpful
```

and optionally:

```text
Reason for negative feedback
```

Feedback can help identify:

```text
Incorrect answers
Poor recommendations
Poor language quality
Irrelevant retrieval
Unhelpful responses
```

User feedback should not be treated as perfect ground truth.

It is one signal among several.

---

# 22. Logging Strategy

Logs should provide enough information to debug failures.

A conceptual request record may contain:

```text
Request ID
Conversation ID
Timestamp
Model version
Prompt version
Embedding version
Retrieved document IDs
Reranker information
Latency
Token usage
Response status
```

Sensitive user content should not automatically be stored in unrestricted logs.

---

# 23. Traceability

Each request should ideally be traceable across the system.

For example:

```text
Request ID
    │
    ├── Backend Request
    │
    ├── Embedding Request
    │
    ├── Qdrant Query
    │
    ├── Reranker Request
    │
    ├── Tool Calls
    │
    └── LLM Request
```

This makes it possible to investigate:

> Why did the system produce this answer?

---

# 24. Alerts

Alerts should be triggered when important metrics cross defined thresholds.

Possible alerts:

```text
High error rate
High latency
LLM unavailable
Vector database unavailable
High fallback rate
Unusual token usage
High cost
Retrieval failure spike
```

Alerts should be meaningful.

Too many alerts can lead to:

```text
Alert fatigue
```

---

# 25. Dashboards

A production dashboard can contain several sections.

## Application

```text
Requests
Errors
Success Rate
Active Sessions
```

## RAG

```text
Retrieval Latency
Empty Retrieval Rate
Similarity Scores
Reranker Usage
```

## LLM

```text
Latency
Tokens
Errors
Cost
```

## Quality

```text
Groundedness
User Feedback
Evaluation Score
Fallback Rate
```

## Languages

```text
Queries by Language
Quality by Language
Fallback Rate by Language
```

---

# 26. Offline Monitoring

Offline monitoring uses a fixed evaluation dataset.

For example:

```text
Evaluation Dataset
        │
        ▼
Current System
        │
        ▼
Metrics
```

This is useful after:

```text
Model changes
Prompt changes
Embedding changes
Chunking changes
Reranker changes
```

Offline evaluation is controlled and reproducible.

---

# 27. Online Monitoring

Online monitoring uses actual production behavior.

Examples:

```text
Latency
Errors
Token usage
User feedback
Retrieval statistics
Fallbacks
```

Online monitoring reflects real-world usage.

However, production data may be noisy.

Therefore:

```text
Offline Evaluation
        +
Online Monitoring
```

should be used together.

---

# 28. Privacy and Security

Monitoring systems must follow the application's privacy requirements.

Do not automatically log:

```text
Sensitive personal information
Authentication credentials
Secrets
API keys
Private user data
```

Logs should use:

```text
Access control
Redaction
Encryption
Retention policies
```

where applicable.

Monitoring infrastructure should be treated as part of the application's security boundary.

---

# 29. Failure Handling

When a monitored component fails, the application should degrade gracefully when possible.

Example:

```text
Reranker unavailable
       │
       ▼
Use vector ranking
       │
       ▼
Continue response
```

Another example:

```text
Knowledge retrieval unavailable
       │
       ▼
Do not invent application-specific information
       │
       ▼
Return appropriate fallback
```

Monitoring should record the fallback event.

---

# 30. Retraining and Model Updates

Monitoring can identify when a model or component needs improvement.

The workflow may be:

```text
Production Monitoring
        │
        ▼
Detect Problem
        │
        ▼
Analyze Failure Cases
        │
        ▼
Create / Update Dataset
        │
        ▼
Train / Tune / Replace Model
        │
        ▼
Offline Evaluation
        │
        ▼
Deploy
        │
        ▼
Monitor Again
```

This creates a continuous improvement cycle.

---

# 31. Monitoring Workflow

The overall production workflow is:

```text
                    Production System
                           │
                           ▼
                    Collect Signals
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     Metrics             Logs             Feedback
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                       Analysis
                           │
                           ▼
                     Detect Problem
                           │
                           ▼
                    Investigate Cause
                           │
                           ▼
                   Improve System
                           │
                           ▼
                    Evaluate Change
                           │
                           ▼
                      Deploy Again
```

---

# 32. Implementation Strategy

Monitoring should be implemented gradually.

## Phase 1 — Application Monitoring

Start with:

```text
Request count
Errors
Latency
```

---

## Phase 2 — LLM Monitoring

Add:

```text
Token usage
LLM latency
LLM errors
Model version
```

---

## Phase 3 — RAG Monitoring

Add:

```text
Retrieval latency
Retrieved chunks
Similarity scores
Empty retrieval
Reranker failures
```

---

## Phase 4 — Quality Monitoring

Add:

```text
Groundedness
User feedback
Evaluation dataset
Failure analysis
```

---

## Phase 5 — Multilingual Monitoring

Add:

```text
Language distribution
Language-specific quality
Code-mixed queries
```

---

## Phase 6 — Continuous Evaluation

Automate:

```text
Offline evaluation
Regression testing
Model comparison
Prompt comparison
```

---

# 33. Future Improvements

Potential improvements include:

- Automated quality monitoring
- Real-time dashboards
- Advanced tracing
- Drift detection
- Automated evaluation
- LLM observability
- Cost optimization
- Language-specific monitoring
- Automated anomaly detection
- Human review workflows
- Active learning
- Feedback-driven dataset creation

---

# 34. Summary

Model monitoring ensures that the AI Concierge continues to work correctly after deployment.

The monitoring architecture covers:

```text
Application
    +
LLM
    +
RAG
    +
Reranker
    +
Memory
    +
Infrastructure
    +
User Feedback
```

Important signals include:

```text
Quality
Latency
Errors
Token Usage
Cost
Retrieval Performance
Groundedness
User Feedback
Language Performance
Drift
```

The overall continuous improvement cycle is:

```text
Build
  ↓
Evaluate
  ↓
Deploy
  ↓
Monitor
  ↓
Detect Problems
  ↓
Analyze
  ↓
Improve
  ↓
Evaluate Again
  ↓
Deploy
```

The most important principle is:

> **A production ML system should not be considered finished when it is deployed. It should be continuously measured, evaluated, and improved.**

Monitoring therefore becomes the bridge between:

```text
ML Development
       ↓
Production
       ↓
Real-World Feedback
       ↓
Continuous Improvement
```
