# Reranking

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / RAG Retrieval Design

---

# Table of Contents

1. Introduction
2. What Is Reranking?
3. Why Reranking Is Needed
4. Retrieval Pipeline
5. Initial Retrieval
6. Reranking Stage
7. Reranker Input
8. Reranker Output
9. Vector Search vs Reranking
10. Cross-Encoder Reranking
11. Multilingual Reranking
12. Code-Mixed Reranking
13. Reranking and RAG
14. Top-K Strategy
15. Score Thresholds
16. Metadata Filtering
17. Reranking Architecture
18. Reranker Selection Criteria
19. Candidate Model Categories
20. Latency Considerations
21. Cost Considerations
22. Failure Handling
23. Evaluation Strategy
24. Reranking Metrics
25. When Reranking Should Be Used
26. Initial Implementation Strategy
27. Future Improvements
28. Summary

---

# 1. Introduction

Reranking is an optional second stage in the information retrieval pipeline.

The first retrieval stage quickly finds a set of potentially relevant documents.

The reranker then examines those candidates more carefully and determines which ones are most relevant to the user's query.

The overall process is:

```text
User Query
    │
    ▼
Embedding
    │
    ▼
Qdrant
    │
    ▼
Candidate Documents
    │
    ▼
Reranker
    │
    ▼
Best Documents
    │
    ▼
LLM
```

---

# 2. What Is Reranking?

A vector database provides an initial ranking based on vector similarity.

However, the highest-scoring vector is not always the most useful piece of information.

A reranker performs a second, more detailed relevance assessment.

Conceptually:

```text
Query
  +
Candidate Document
  │
  ▼
Reranker
  │
  ▼
Relevance Score
```

The candidates are then reordered according to their relevance.

---

# 3. Why Reranking Is Needed

Vector search is designed to be fast.

It may retrieve:

```text
Top 20 candidate chunks
```

but only some of them may actually be useful.

For example:

```text
Query
 │
 ▼
Vector Search
 │
 ├── Chunk A → Relevant
 ├── Chunk B → Somewhat Relevant
 ├── Chunk C → Irrelevant
 ├── Chunk D → Highly Relevant
 └── ...
```

A reranker can reorder these:

```text
Highly Relevant
      ↓
Relevant
      ↓
Somewhat Relevant
      ↓
Irrelevant
```

The LLM can then receive only the strongest candidates.

---

# 4. Retrieval Pipeline

The complete retrieval architecture becomes:

```text
                    User Query
                        │
                        ▼
                 Query Embedding
                        │
                        ▼
                     Qdrant
                        │
                        ▼
              Initial Candidate Set
                        │
                        ▼
                    Reranker
                        │
                        ▼
               Top Relevant Chunks
                        │
                        ▼
                   Context Builder
                        │
                        ▼
                       LLM
                        │
                        ▼
                     Response
```

This is known as a **two-stage retrieval pipeline**.

---

# 5. Initial Retrieval

The first stage uses the embedding model.

```text
Query
  │
  ▼
Embedding
  │
  ▼
Vector
  │
  ▼
Qdrant
  │
  ▼
Top-N Candidates
```

The objective is high recall.

In other words:

> Find enough potentially relevant information so that the correct information is unlikely to be missed.

The candidate count can be larger than the number ultimately sent to the LLM.

---

# 6. Reranking Stage

The reranker receives:

```text
User Query
+
Candidate Chunks
```

and produces relevance scores.

Example:

```text
Query
  │
  ▼
Candidate Chunks
  │
  ▼
Reranker
  │
  ├── Chunk A → 0.91
  ├── Chunk B → 0.42
  ├── Chunk C → 0.87
  └── Chunk D → 0.25
```

After sorting:

```text
Chunk A → 0.91
Chunk C → 0.87
Chunk B → 0.42
Chunk D → 0.25
```

Only the strongest chunks may then be passed to the LLM.

---

# 7. Reranker Input

The reranker generally receives pairs such as:

```text
Query
+
Candidate Document
```

For example:

```text
Query:
"How can rewards be redeemed?"

Candidate:
"Customers can exchange accumulated points
for eligible rewards..."
```

The reranker determines how relevant the candidate is to the query.

---

# 8. Reranker Output

The reranker should produce a relevance score or ranking.

Conceptually:

```text
Candidate 1 → 0.94
Candidate 2 → 0.78
Candidate 3 → 0.31
Candidate 4 → 0.12
```

The system sorts candidates according to their scores.

The exact score interpretation depends on the selected reranker.

A score should not automatically be treated as a probability unless the model explicitly defines it that way.

---

# 9. Vector Search vs Reranking

These two components have different responsibilities.

| Component | Main Objective |
|---|---|
| Embedding + Vector Search | Quickly find candidates |
| Reranker | Carefully rank candidates |

Conceptually:

```text
Vector Search
     ↓
High Recall
     ↓
Candidate Set
     ↓
Reranker
     ↓
High Precision
```

Vector search is optimized for speed.

Reranking is optimized for relevance.

---

# 10. Cross-Encoder Reranking

One common reranking approach is a cross-encoder.

Instead of independently embedding:

```text
Query
```

and:

```text
Document
```

the model processes them together.

Conceptually:

```text
Query + Document
        │
        ▼
   Cross-Encoder
        │
        ▼
Relevance Score
```

This allows the model to examine the interaction between the query and document more directly.

The tradeoff is that this is generally more computationally expensive than simple vector similarity.

---

# 11. Multilingual Reranking

Because AI Concierge supports multiple languages, the reranker should ideally support the project's target languages.

Possible cases include:

```text
Query: Language A
Document: Language A
```

and:

```text
Query: Language A
Document: Language B
```

and:

```text
Query: Code-Mixed
Document: English
```

The selected reranker should be evaluated on these scenarios.

---

# 12. Code-Mixed Reranking

Code-mixed queries should be explicitly tested.

Example:

```text
User Query
     │
     ▼
Code-Mixed Text
     │
     ▼
Vector Search
     │
     ▼
Candidate Chunks
     │
     ▼
Multilingual Reranker
     │
     ▼
Ranked Results
```

The goal is to determine whether the reranker can understand the semantic relationship between code-mixed queries and candidate documents.

---

# 13. Reranking and RAG

Reranking improves the quality of context supplied to the LLM.

Without reranking:

```text
Query
 ↓
Qdrant
 ↓
Top Chunks
 ↓
LLM
```

With reranking:

```text
Query
 ↓
Qdrant
 ↓
Candidate Chunks
 ↓
Reranker
 ↓
Best Chunks
 ↓
LLM
```

The second approach can reduce irrelevant context.

This may improve:

```text
Answer relevance
Groundedness
Context utilization
Token efficiency
```

However, the improvement must be demonstrated through evaluation.

---

# 14. Top-K Strategy

There are two important values:

```text
Initial K
```

and:

```text
Final K
```

For example:

```text
Qdrant
  ↓
Retrieve 20 candidates
  ↓
Rerank 20 candidates
  ↓
Keep top 5
  ↓
LLM
```

The actual values should be determined experimentally.

A larger initial K can improve recall but increases reranking cost.

A larger final K provides more context but increases LLM input size.

---

# 15. Score Thresholds

A minimum relevance threshold may optionally be used.

Conceptually:

```text
Reranker Score
      │
      ▼
Above Threshold?
      │
 ┌────┴─────┐
 ▼          ▼
Yes         No
 │           │
 ▼           ▼
Keep       Discard
```

This can help prevent clearly irrelevant chunks from reaching the LLM.

However, thresholds should be calibrated using an evaluation dataset.

A score from one reranker should not automatically be assumed to have the same meaning as a score from another reranker.

---

# 16. Metadata Filtering

Metadata filtering should generally happen before expensive reranking when possible.

For example:

```text
User Query
    │
    ▼
Security / Tenant Filter
    │
    ▼
Vector Search
    │
    ▼
Candidate Chunks
    │
    ▼
Reranker
```

This prevents the reranker from processing documents that the user is not authorized to access.

Security filtering must never depend solely on the LLM or reranker.

---

# 17. Reranking Architecture

The proposed architecture is:

```text
                         Query
                           │
                           ▼
                    Query Embedding
                           │
                           ▼
                        Qdrant
                           │
                           ▼
                  Candidate Documents
                           │
                           ▼
                       Reranker
                           │
                           ▼
                   Ranked Documents
                           │
                           ▼
                  Context Construction
                           │
                           ▼
                          LLM
                           │
                           ▼
                       Response
```

---

# 18. Reranker Selection Criteria

The reranker should be evaluated based on:

```text
Retrieval improvement
Multilingual support
Indian-language support
Code-mixed support
Latency
Memory requirements
Cost
Deployment complexity
Model availability
```

The most important question is:

> Does the reranker meaningfully improve retrieval quality enough to justify its additional latency and complexity?

---

# 19. Candidate Model Categories

Potential approaches include:

## Cross-Encoder Models

Advantages:

```text
Strong query-document relevance modeling
Good reranking capability
```

Disadvantages:

```text
More computationally expensive
Higher latency
```

---

## Multilingual Cross-Encoders

These are preferable when the system must rerank multiple languages.

They should be tested specifically on the target languages rather than assuming that general multilingual support guarantees good performance.

---

## LLM-Based Reranking

An LLM can theoretically rank candidate documents.

However, this may be:

```text
Expensive
Slow
Less predictable
```

Therefore, a dedicated reranker should generally be evaluated first.

---

# 20. Latency Considerations

Reranking adds another model inference step.

Without reranking:

```text
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
LLM
```

With reranking:

```text
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
Reranker
 ↓
LLM
```

Therefore, the system must measure whether the retrieval-quality improvement justifies the additional latency.

---

# 21. Cost Considerations

If a hosted reranker is used, every query may incur an additional cost.

The cost depends on:

```text
Number of candidates
Query length
Candidate length
Number of requests
Model pricing
```

Reducing the number of candidates can reduce cost, but overly aggressive reduction may hurt recall.

---

# 22. Failure Handling

The reranker may fail because of:

```text
Timeout
Model unavailable
Rate limit
Invalid input
Resource exhaustion
```

The system should have a fallback.

Possible strategy:

```text
Vector Search
      │
      ▼
Reranker
      │
   Failure
      │
      ▼
Use Vector Ranking
      │
      ▼
Continue RAG
```

This means the system can still answer using vector-search results if reranking is temporarily unavailable.

However, fallback behavior should be logged.

---

# 23. Evaluation Strategy

The reranker should be evaluated against the baseline:

```text
Vector Search Only
```

and compared with:

```text
Vector Search + Reranking
```

The goal is to determine whether reranking produces a measurable improvement.

---

## Evaluation Dataset

A synthetic dataset can contain:

```text
Query
Relevant Chunk
Non-Relevant Chunks
Language
Code-Mixed Flag
```

Example categories:

```text
Simple queries
Ambiguous queries
Long queries
Multilingual queries
Code-mixed queries
Follow-up questions
```

---

# 24. Reranking Metrics

Potential retrieval metrics include:

### Recall@K

Measures whether the relevant document appears among the top K results.

---

### Precision@K

Measures how many of the top K results are relevant.

---

### MRR

Mean Reciprocal Rank measures how highly the first relevant result appears.

---

### nDCG

Normalized Discounted Cumulative Gain considers the ranking position and relevance of multiple results.

---

## Important Comparison

The evaluation should compare:

```text
Vector Search
       VS
Vector Search + Reranker
```

rather than evaluating the reranker in isolation.

---

# 25. When Reranking Should Be Used

Reranking is particularly useful when:

```text
The knowledge base is large
```

or:

```text
Many similar documents exist
```

or:

```text
Vector search retrieves noisy results
```

or:

```text
Retrieval quality is limiting answer quality
```

It may be unnecessary for a very small knowledge base.

Therefore, reranking should be introduced based on measured need.

---

# 26. Initial Implementation Strategy

The project should not make reranking mandatory from the first implementation.

A practical development approach is:

## Phase 1 — Baseline

```text
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
Top-K
 ↓
LLM
```

Measure retrieval quality.

---

## Phase 2 — Add Reranking

```text
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
Top-N
 ↓
Reranker
 ↓
Top-K
 ↓
LLM
```

Compare results.

---

## Phase 3 — Optimize

Tune:

```text
Initial K
Final K
Chunk Size
Reranker
Threshold
Latency
```

---

# 27. Future Improvements

Potential improvements include:

- Multilingual rerankers
- Hybrid retrieval
- Sparse + dense retrieval
- Query rewriting before retrieval
- Query expansion
- Language-aware reranking
- Metadata-aware ranking
- Domain-specific reranking
- Learned ranking
- Adaptive reranking
- Retrieval caching

---

# 28. Summary

Reranking is the second stage of the retrieval pipeline.

The architecture is:

```text
                 User Query
                     │
                     ▼
                Embedding
                     │
                     ▼
                  Qdrant
                     │
                     ▼
             Candidate Results
                     │
                     ▼
                 Reranker
                     │
                     ▼
              Best Results
                     │
                     ▼
                    LLM
                     │
                     ▼
                 Response
```

The responsibilities are:

```text
Embedding Model
      ↓
Represent meaning

Qdrant
      ↓
Find candidate information

Reranker
      ↓
Determine which candidates are most relevant

LLM
      ↓
Generate the final response
```

Reranking should not be added merely because it is a common RAG component.

The project should first establish a vector-search baseline and then measure whether reranking provides a meaningful improvement.

The final decision should consider:

```text
Retrieval Quality
+
Multilingual Performance
+
Code-Mixed Performance
+
Latency
+
Cost
+
Infrastructure Complexity
```

The architecture should also allow reranking to be disabled or bypassed if the additional complexity does not provide sufficient benefit.
