# RAG Evaluation

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / RAG Evaluation

---

# Table of Contents

1. Introduction
2. Why RAG Evaluation Is Required
3. What We Need to Evaluate
4. RAG Evaluation Pipeline
5. Evaluation Dataset
6. Query Categories
7. Ground Truth
8. Retrieval Evaluation
9. Answer Evaluation
10. Groundedness
11. Faithfulness
12. Context Relevance
13. Context Recall
14. Retrieval Metrics
15. Generation Metrics
16. End-to-End Evaluation
17. Multilingual Evaluation
18. Code-Mixed Evaluation
19. Memory-Aware Evaluation
20. Out-of-Domain Evaluation
21. Failure Cases
22. Baseline Evaluation
23. Reranker Evaluation
24. LLM Evaluation
25. Human Evaluation
26. Automated Evaluation
27. Evaluation Pipeline
28. Experiment Tracking
29. Evaluation Thresholds
30. Regression Testing
31. Evaluation Reports
32. Implementation Strategy
33. Future Improvements
34. Summary

---

# 1. Introduction

Retrieval-Augmented Generation (RAG) combines:

```text
Retrieval
+
Language Model
```

The system retrieves relevant information and provides it to the LLM to generate a response.

A technically functioning RAG pipeline does not necessarily mean that the answers are good.

For example:

```text
Query
  ↓
Retriever
  ↓
Wrong Document
  ↓
LLM
  ↓
Confident Wrong Answer
```

Therefore, AI Concierge needs a systematic evaluation strategy.

---

# 2. Why RAG Evaluation Is Required

RAG quality depends on several independent components.

A poor final answer may be caused by:

```text
Poor query understanding
        ↓
Poor retrieval
        ↓
Poor reranking
        ↓
Insufficient context
        ↓
Poor prompt
        ↓
Poor LLM response
```

Therefore, evaluating only the final answer is not enough.

We should evaluate:

```text
Retrieval
+
Context Quality
+
Generation
+
Groundedness
+
End-to-End Quality
```

---

# 3. What We Need to Evaluate

The evaluation framework should answer questions such as:

```text
Did we retrieve the correct information?

Was the retrieved information relevant?

Did the LLM use the retrieved information?

Did the LLM invent unsupported information?

Was the final answer useful?

Did multilingual queries work?

Did code-mixed queries work?

Did memory improve personalization without introducing errors?

What happens when the answer is not present?

```

---

# 4. RAG Evaluation Pipeline

The evaluation pipeline is:

```text
Evaluation Query
       │
       ▼
Query Processing
       │
       ▼
Embedding
       │
       ▼
Vector Search
       │
       ▼
Reranking
       │
       ▼
Retrieved Context
       │
       ▼
LLM
       │
       ▼
Generated Answer
       │
       ▼
Evaluation
       │
       ├── Retrieval Metrics
       ├── Context Metrics
       ├── Answer Metrics
       └── End-to-End Metrics
```

---

# 5. Evaluation Dataset

A dedicated evaluation dataset should be created.

The dataset should contain representative user queries and the information required to answer them.

A conceptual record can contain:

```text
{
    "query": "...",
    "language": "...",
    "is_code_mixed": false,
    "expected_intent": "...",
    "relevant_document_ids": [...],
    "relevant_chunks": [...],
    "expected_answer_properties": [...]
}
```

The evaluation dataset should be kept separate from the data used for development where practical.

---

# 6. Query Categories

The evaluation dataset should contain multiple types of queries.

## Simple Queries

Straightforward questions with a clear answer.

---

## Paraphrased Queries

Different wording with the same meaning.

```text
Question A
Question B
```

Both should retrieve the same relevant information.

---

## Conversational Queries

Questions that depend on previous turns.

```text
User:
"I want travel-related options."

Assistant:
"..."

User:
"What about hotels?"
```

---

## Ambiguous Queries

Questions where the system should ask for clarification rather than guess.

---

## Multilingual Queries

Queries written in supported Indian languages.

---

## Code-Mixed Queries

Queries combining multiple languages.

---

## Out-of-Domain Queries

Queries unrelated to the application's intended purpose.

---

## Unanswerable Queries

Questions for which the knowledge base does not contain sufficient information.

These are especially important for evaluating hallucination behavior.

---

# 7. Ground Truth

Ground truth represents what the system should ideally retrieve or produce.

For retrieval evaluation:

```text
Query
   │
   ▼
Expected Relevant Documents
```

For answer evaluation:

```text
Query
   +
Relevant Context
   │
   ▼
Expected Answer Properties
```

Ground truth does not always need to be a single exact sentence.

For open-ended answers, it may be more appropriate to define:

```text
Required facts
+
Forbidden claims
+
Expected language
+
Expected behavior
```

---

# 8. Retrieval Evaluation

Retrieval evaluation asks:

> Did the system retrieve the information required to answer the question?

Example:

```text
Query
  ↓
Retriever
  ↓
Top 5 Chunks
```

If the correct chunk appears among those five, retrieval may be considered successful for that query.

---

# 9. Answer Evaluation

After retrieval, the LLM generates an answer.

The answer should be evaluated for:

```text
Correctness
Relevance
Completeness
Groundedness
Language quality
```

A technically correct retrieval system can still produce poor answers.

Therefore:

```text
Good Retrieval
      ≠
Automatically Good Answer
```

---

# 10. Groundedness

Groundedness measures whether the answer is supported by the retrieved information.

Example:

```text
Retrieved Context:
"Customers can redeem points for eligible rewards."

Answer:
"Customers can redeem points for eligible rewards."

→ Grounded
```

If the answer introduces unsupported information:

```text
Retrieved Context:
"Customers can redeem points for eligible rewards."

Answer:
"Customers can redeem points for flights, hotels,
and restaurants."

→ Potentially Unsupported
```

The additional claims need to be verified against the available context.

---

# 11. Faithfulness

Faithfulness asks:

> Does the generated answer accurately reflect the information provided by the retrieval context?

A response should not contradict the retrieved information.

Conceptually:

```text
Retrieved Context
       │
       ▼
    LLM Answer
       │
       ▼
Check Claims
       │
       ├── Supported
       └── Unsupported
```

Faithfulness is especially important for knowledge-based responses.

---

# 12. Context Relevance

Context relevance asks:

> Is the retrieved context actually useful for answering the query?

For example:

```text
Query:
"How can points be redeemed?"

Retrieved:
Document about reward redemption
→ Highly relevant
```

versus:

```text
Retrieved:
Document about account password policies
→ Low relevance
```

A retrieval system should not simply retrieve semantically similar text.

It should retrieve information useful for the specific question.

---

# 13. Context Recall

Context recall measures whether the retrieval stage found the information required to answer the question.

Example:

```text
Required Information:
A + B + C

Retrieved:
A + B

Missing:
C
```

The system may therefore have incomplete context.

High context recall is important because the LLM cannot reliably use information that was never retrieved.

---

# 14. Retrieval Metrics

The project can use standard retrieval metrics.

## Recall@K

Measures whether relevant information appears within the top K results.

```text
Recall@5
Recall@10
```

can be evaluated separately.

---

## Precision@K

Measures how many of the retrieved results are relevant.

```text
Precision@5
Precision@10
```

---

## Mean Reciprocal Rank (MRR)

MRR evaluates how highly the first relevant result appears.

Higher-ranked relevant results produce better scores.

---

## nDCG

Normalized Discounted Cumulative Gain evaluates ranking quality when multiple results have different degrees of relevance.

---

# 15. Generation Metrics

Generated answers can be evaluated using several dimensions.

## Correctness

Does the answer contain the correct information?

---

## Relevance

Does the answer actually address the user's question?

---

## Completeness

Does the answer include the important information required to answer the question?

---

## Groundedness

Are the claims supported by the available context?

---

## Language Quality

Is the response understandable and natural in the expected language?

---

# 16. End-to-End Evaluation

The final system should also be evaluated as a complete pipeline.

```text
User Query
     │
     ▼
Retrieval
     │
     ▼
Reranking
     │
     ▼
Context
     │
     ▼
LLM
     │
     ▼
Final Answer
```

The evaluation should determine whether the complete system provides a useful response.

A component can perform well individually but still fail when integrated with other components.

---

# 17. Multilingual Evaluation

Every supported language should have dedicated evaluation examples.

For example:

```text
English
Language A
Language B
Language C
Language D
Language E
```

Each language should be evaluated for:

```text
Query Understanding
Retrieval
Reranking
Answer Generation
Groundedness
Response Quality
```

Performance should not be averaged blindly across languages.

A model may perform strongly in one language and poorly in another.

---

# 18. Code-Mixed Evaluation

Code-mixed queries should be evaluated separately.

Test cases should include:

```text
English + Language A
English + Language B
Language A + English
Language B + English
```

where relevant to the selected languages.

Evaluation should consider:

```text
Language Detection
Query Understanding
Retrieval
Answer Language
Meaning Preservation
Response Naturalness
```

---

# 19. Memory-Aware Evaluation

AI Concierge includes a personalization layer.

Therefore, evaluation should also test whether memory is being used appropriately.

Example:

```text
Previous conversation:
User expressed a preference.

Current query:
Related recommendation request.
```

The evaluation should determine whether:

```text
Relevant memory
      ↓
Improves response
```

without causing:

```text
Irrelevant memory
      ↓
Incorrect personalization
```

Memory should not override the user's current explicit request.

---

# 20. Out-of-Domain Evaluation

The system should be tested with questions outside its intended domain.

Expected behavior may be:

```text
Recognize unsupported request
       ↓
Respond appropriately
       ↓
Redirect to supported functionality
```

The system should not fabricate an answer merely because the LLM can answer the question in general.

---

# 21. Failure Cases

The evaluation dataset should intentionally include difficult cases.

Examples:

```text
Relevant information does not exist
Multiple documents contain similar information
Query is ambiguous
Query contains spelling errors
Query is code-mixed
Query uses Romanized text
Query switches language
Retrieved context is incomplete
Retrieved documents conflict
```

These cases help expose weaknesses before deployment.

---

# 22. Baseline Evaluation

The project should establish a baseline before adding advanced retrieval components.

Initial baseline:

```text
Embedding
   ↓
Qdrant
   ↓
Top-K
   ↓
LLM
```

Record:

```text
Retrieval Metrics
+
Answer Metrics
+
Latency
```

This becomes the reference point for future improvements.

---

# 23. Reranker Evaluation

After establishing the baseline:

```text
Embedding
   ↓
Qdrant
   ↓
Reranker
   ↓
Top-K
   ↓
LLM
```

Compare:

```text
Baseline
     VS
Reranked System
```

The goal is to determine whether reranking improves:

```text
Recall
Precision
MRR
nDCG
Answer Quality
Groundedness
```

while keeping latency acceptable.

---

# 24. LLM Evaluation

Different LLMs should be evaluated using the same retrieval context where possible.

For example:

```text
Model A
Model B
Model C
```

should be compared using:

```text
Same Queries
+
Same Context
+
Same Evaluation Criteria
```

This helps distinguish:

```text
Retrieval Quality
```

from:

```text
LLM Generation Quality
```

---

# 25. Human Evaluation

Automated evaluation should be complemented with human evaluation.

Human reviewers can assess:

```text
Correctness
Relevance
Naturalness
Helpfulness
Language quality
Personalization
```

A simple rating scale may be used.

For example:

```text
1 = Poor
2 = Below Average
3 = Acceptable
4 = Good
5 = Excellent
```

Human evaluation should use clearly defined evaluation guidelines so that different reviewers apply similar standards.

---

# 26. Automated Evaluation

Automated evaluation can help test large numbers of examples.

Potential approaches include:

```text
Rule-based checks
Retrieval metrics
Structured validators
LLM-as-a-judge
```

LLM-based evaluation can be useful for some qualitative dimensions, but it should not be treated as unquestionable ground truth.

Where possible, automated evaluation should be combined with known ground truth and human review.

---

# 27. Evaluation Pipeline

A repeatable evaluation pipeline can be:

```text
Evaluation Dataset
       │
       ▼
Run RAG Pipeline
       │
       ▼
Store:
  - Query
  - Retrieved Chunks
  - Scores
  - Final Answer
  - Latency
       │
       ▼
Run Evaluation
       │
       ▼
Calculate Metrics
       │
       ▼
Generate Report
```

This allows different system versions to be compared.

---

# 28. Experiment Tracking

Each experiment should record important configuration information.

For example:

```text
Experiment ID
Date
Embedding Model
Embedding Version
LLM Model
LLM Version
Prompt Version
Chunk Size
Chunk Overlap
Retriever Configuration
Reranker
Top-K
Evaluation Dataset Version
```

This makes results reproducible.

---

# 29. Evaluation Thresholds

The project should eventually define minimum acceptable thresholds.

For example:

```text
Retrieval Recall@K ≥ Target
Groundedness ≥ Target
Answer Quality ≥ Target
Latency ≤ Target
```

The exact thresholds should **not be invented before baseline experiments**.

They should be established after:

```text
Initial Evaluation
      ↓
Understand Baseline
      ↓
Define Practical Targets
      ↓
Track Improvements
```

---

# 30. Regression Testing

Once the system reaches an acceptable quality level, future changes should be tested against the existing evaluation dataset.

For example:

```text
Change Prompt
     │
     ▼
Run Evaluation
     │
     ▼
Compare With Previous Version
```

A change should not be considered an improvement merely because one example became better.

It should improve overall performance without causing unacceptable regressions.

---

# 31. Evaluation Reports

Each evaluation run should produce a report containing:

```text
Overall Results
Retrieval Results
Generation Results
Multilingual Results
Code-Mixed Results
Latency
Failure Cases
Comparison With Previous Version
```

Example:

```text
                 Baseline     New Version

Recall@5            X              Y
MRR                  X              Y
Groundedness         X              Y
Answer Quality       X              Y
Latency              X              Y
```

The exact metrics will depend on the implemented evaluation framework.

---

# 32. Implementation Strategy

Evaluation should be introduced gradually.

## Phase 1 — Create Small Dataset

Start with a manageable set of representative queries.

Include:

```text
Normal
RAG
Multilingual
Code-Mixed
Unanswerable
```

---

## Phase 2 — Evaluate Retrieval

Measure:

```text
Recall@K
Precision@K
MRR
```

---

## Phase 3 — Evaluate RAG Answers

Measure:

```text
Correctness
Relevance
Groundedness
```

---

## Phase 4 — Add Reranker

Compare:

```text
Vector Search
```

against:

```text
Vector Search + Reranking
```

---

## Phase 5 — Expand Multilingual Evaluation

Add more examples for every supported language.

---

## Phase 6 — Add Regression Testing

Run the evaluation suite whenever major ML/RAG components change.

---

# 33. Future Improvements

Potential improvements include:

- Larger evaluation datasets
- Automated evaluation pipelines
- Human evaluation dashboards
- LLM-as-a-judge
- Synthetic test generation
- Adversarial evaluation
- Multilingual benchmarks
- Retrieval tracing
- Failure clustering
- Continuous evaluation
- Production feedback integration

---

# 34. Summary

RAG evaluation should measure the complete pipeline rather than only the final answer.

The evaluation framework is:

```text
                  Evaluation Dataset
                         │
                         ▼
                    User Query
                         │
                         ▼
                      Retrieval
                         │
                         ▼
                     Reranking
                         │
                         ▼
                    RAG Context
                         │
                         ▼
                        LLM
                         │
                         ▼
                    Final Answer
                         │
                         ▼
                    Evaluation
```

The project should evaluate four major areas:

```text
1. Retrieval Quality
2. Context Quality
3. Generation Quality
4. End-to-End Quality
```

Additional evaluation should cover:

```text
Multilingual Queries
Code-Mixed Queries
Memory-Based Personalization
Unanswerable Questions
Out-of-Domain Questions
```

The most important principle is:

> **A RAG system is successful only when it retrieves useful information and uses that information to produce a correct, relevant, and grounded response.**

The evaluation process should therefore compare every major architectural change against a known baseline.

This allows the project to answer an important question objectively:

```text
"Did this change actually make the AI Concierge better?"
```
