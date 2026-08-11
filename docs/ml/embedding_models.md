# Embedding Models

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / Embedding Design

---

# Table of Contents

1. Introduction
2. What Are Embeddings?
3. Why AI Concierge Needs Embeddings
4. Embedding Pipeline
5. Documents to Embeddings
6. User Query to Embedding
7. Vector Database
8. Semantic Search
9. Multilingual Embeddings
10. Code-Mixed Embeddings
11. Embedding Model Requirements
12. Candidate Model Categories
13. Model Selection Criteria
14. Embedding Dimensions
15. Similarity Measures
16. Chunking and Embeddings
17. Metadata and Filtering
18. Embedding Storage
19. Query-Time Embeddings
20. Document Re-Embedding
21. Embedding Versioning
22. Embedding Model Configuration
23. Performance Considerations
24. Cost Considerations
25. Evaluation Strategy
26. Embedding Failure Handling
27. Future Improvements
28. Summary

---

# 1. Introduction

Embeddings convert text into numerical vectors that represent the semantic meaning of the text.

AI Concierge uses embeddings primarily for semantic retrieval.

The overall flow is:

```text
Document
   │
   ▼
Text Extraction
   │
   ▼
Chunking
   │
   ▼
Embedding Model
   │
   ▼
Vector
   │
   ▼
Qdrant
```

When a user asks a question:

```text
User Query
   │
   ▼
Embedding Model
   │
   ▼
Query Vector
   │
   ▼
Qdrant
   │
   ▼
Relevant Chunks
```

These chunks are then passed to the RAG/LLM pipeline.

---

# 2. What Are Embeddings?

An embedding is a numerical representation of text.

For example:

```text
Text
 ↓
Embedding Model
 ↓
[0.12, -0.43, 0.81, ...]
```

The vector contains many numerical dimensions.

Texts with similar meanings should generally have vectors that are close to each other in the embedding space.

Conceptually:

```text
"How can I redeem my points?"
            │
            │ semantically similar
            ▼
"How do I use my reward points?"
```

Their vectors should therefore be relatively close.

---

# 3. Why AI Concierge Needs Embeddings

Keyword search looks primarily for matching words.

For example:

```text
Query:
"How can I use my rewards?"
```

A keyword search may prioritize documents containing:

```text
use
rewards
```

Semantic search can recognize that:

```text
"How can I use my rewards?"
```

and:

```text
"What can I do with my accumulated points?"
```

may have similar meanings even though many words differ.

This is important for conversational AI.

---

# 4. Embedding Pipeline

The complete embedding pipeline is:

```text
                    DOCUMENT INGESTION

Document
   │
   ▼
Text Extraction
   │
   ▼
Cleaning
   │
   ▼
Chunking
   │
   ▼
Embedding Model
   │
   ▼
Vector + Metadata
   │
   ▼
Qdrant


                    QUERY TIME

User Query
   │
   ▼
Embedding Model
   │
   ▼
Query Vector
   │
   ▼
Qdrant Search
   │
   ▼
Relevant Chunks
```

The same embedding model should normally be used for both document embeddings and query embeddings within a given vector space.

---

# 5. Documents to Embeddings

During document ingestion, the document is divided into chunks.

Example:

```text
Document
   │
   ▼
Chunk 1
Chunk 2
Chunk 3
Chunk 4
   │
   ▼
Embedding Model
   │
   ▼
Vector 1
Vector 2
Vector 3
Vector 4
```

Each vector is stored along with metadata.

Conceptually:

```text
Vector
  +
Document ID
  +
Chunk ID
  +
Language
  +
Other Metadata
```

---

# 6. User Query to Embedding

When the user asks a question:

```text
User Query
    │
    ▼
Normalize / Prepare Query
    │
    ▼
Embedding Model
    │
    ▼
Query Vector
    │
    ▼
Qdrant
```

The query vector is compared with stored document vectors.

The most semantically relevant chunks are retrieved.

---

# 7. Vector Database

The project uses a vector database to store and retrieve embeddings.

The current architecture uses:

```text
Qdrant
```

The backend communicates with Qdrant.

The frontend should never access Qdrant directly.

```text
Frontend
    │
    ▼
Backend
    │
    ▼
Embedding Service
    │
    ▼
Qdrant
```

---

# 8. Semantic Search

Semantic search works by comparing vectors.

Conceptually:

```text
Query Vector
      │
      ▼
┌─────────────────────────┐
│       Vector Space      │
│                         │
│  Document A ●           │
│                         │
│          ● Query        │
│                         │
│                Document B
│                         │
│                         │
└─────────────────────────┘
```

The system retrieves vectors that are most similar to the query vector.

The retrieved chunks are then used as context for the LLM.

---

# 9. Multilingual Embeddings

AI Concierge is intended to support multiple Indian languages.

Therefore, the embedding model should ideally represent semantically similar text across supported languages in a compatible vector space.

Conceptually:

```text
English Query
      │
      ▼
Embedding
      │
      ▼
Vector Space
      ▲
      │
Embedding
      │
      ▼
Indian-language Document
```

This can enable cross-lingual retrieval where the query and document use different languages.

However, this capability must be **evaluated rather than assumed**.

---

# 10. Code-Mixed Embeddings

Users may combine languages within a single message.

For example, a query might contain:

```text
English + Indian language
```

or:

```text
Indian language + English
```

The embedding model should be evaluated for its ability to represent such code-mixed text meaningfully.

Pipeline:

```text
Code-Mixed Query
       │
       ▼
Embedding Model
       │
       ▼
Query Vector
       │
       ▼
Semantic Retrieval
       │
       ▼
Relevant Context
```

Code-mixed retrieval should be included in the evaluation dataset.

---

# 11. Embedding Model Requirements

The selected embedding model should ideally provide:

```text
Strong semantic representation
Multilingual support
Indian-language support
Code-mixed robustness
Good retrieval quality
Reasonable inference speed
Suitable vector dimensions
Stable API/model behavior
```

The model should be evaluated specifically on the project's target languages.

---

# 12. Candidate Model Categories

The project can consider several embedding model categories.

## Multilingual Embedding Models

These models are designed to represent multiple languages.

Advantages:

```text
Multilingual retrieval
Potential cross-lingual search
Single embedding pipeline
```

---

## Monolingual Models

A model specialized for one language may sometimes provide stronger performance for that language.

However, maintaining separate models can increase system complexity.

```text
Language A → Model A
Language B → Model B
Language C → Model C
```

This approach should only be considered if evaluation demonstrates a significant benefit.

---

## General-Purpose Embedding Models

These models may provide broad semantic retrieval capabilities across multiple domains and languages.

They should be evaluated against project-specific requirements rather than selected solely based on benchmark popularity.

---

# 13. Model Selection Criteria

The embedding model should be evaluated using:

| Criterion | Importance |
|---|---|
| Multilingual retrieval | High |
| Indian-language retrieval | High |
| Code-mixed retrieval | High |
| Semantic similarity | High |
| Retrieval accuracy | High |
| Latency | Medium/High |
| Memory usage | Medium |
| Vector dimensions | Medium |
| Cost | High |
| Ease of deployment | Medium |

---

# 14. Embedding Dimensions

An embedding model produces vectors with a fixed number of dimensions.

For example:

```text
Text
 ↓
Embedding Model
 ↓
[0.12, 0.45, -0.21, ...]
```

The vector might contain hundreds or thousands of dimensions depending on the model.

The selected dimension affects:

```text
Storage
Memory
Search performance
Index size
Infrastructure cost
```

The exact dimensionality will depend on the selected embedding model.

---

# 15. Similarity Measures

The vector database needs a method for measuring similarity.

Common approaches include:

```text
Cosine Similarity
Dot Product
Euclidean Distance
```

For semantic text retrieval, cosine similarity is a common choice.

Conceptually:

```text
Query Vector
      │
      ▼
Compare with Stored Vectors
      │
      ▼
Similarity Score
      │
      ▼
Rank Results
```

The similarity metric must be compatible with the selected embedding model and Qdrant collection configuration.

---

# 16. Chunking and Embeddings

Embedding quality depends partly on how documents are chunked.

Consider:

```text
Very Large Chunk
      ↓
Too much unrelated information
      ↓
Less precise retrieval
```

versus:

```text
Very Small Chunk
      ↓
Insufficient context
      ↓
Incomplete information
```

Therefore:

```text
Chunking Strategy
       +
Embedding Model
       ↓
Retrieval Quality
```

Chunk size and overlap should be experimentally evaluated.

The exact values should not be permanently fixed before testing.

---

# 17. Metadata and Filtering

Vectors should be stored with useful metadata.

Possible metadata includes:

```text
document_id
chunk_id
source
language
document_type
created_at
user_id / tenant_id
```

Metadata enables filtering before or during vector retrieval.

For example:

```text
Query
  │
  ▼
Vector Search
  │
  ├── User/Tenant Filter
  ├── Language Filter
  └── Document Filter
  │
  ▼
Relevant Results
```

Security-related filters must be enforced by the backend.

---

# 18. Embedding Storage

A vector record can conceptually contain:

```text
{
    "vector": [...],
    "document_id": "...",
    "chunk_id": "...",
    "metadata": {...}
}
```

The exact Qdrant schema will be defined in the database/vector-store implementation.

The vector itself should not be exposed directly to the frontend unless there is a specific requirement.

---

# 19. Query-Time Embeddings

Every semantic search request requires converting the query into a vector.

Example:

```text
User:
"How can I redeem my points?"
       │
       ▼
Embedding Model
       │
       ▼
Query Vector
       │
       ▼
Qdrant
```

The query embedding must be generated using a model compatible with the stored document vectors.

---

# 20. Document Re-Embedding

If the embedding model changes, previously stored vectors may no longer be compatible.

For example:

```text
Old Embedding Model
        │
        ▼
Old Vectors
```

Changing the model:

```text
New Embedding Model
        │
        ▼
New Vector Space
```

The old and new vectors should not simply be mixed in the same vector space.

A re-embedding process may therefore be required.

---

## Re-Embedding Pipeline

```text
Existing Documents
       │
       ▼
Extract Chunks
       │
       ▼
New Embedding Model
       │
       ▼
New Vectors
       │
       ▼
New / Updated Collection
```

---

# 21. Embedding Versioning

Embedding configuration should be versioned.

For example:

```text
Embedding Model
Embedding Model Version
Embedding Dimension
Similarity Metric
Chunking Version
```

Conceptually:

```text
Embedding Configuration
        │
        ├── Model
        ├── Version
        ├── Dimension
        ├── Metric
        └── Chunking Strategy
```

This makes retrieval experiments reproducible.

---

# 22. Embedding Model Configuration

Embedding configuration should be externalized.

Example:

```text
EMBEDDING_PROVIDER=
EMBEDDING_MODEL=
EMBEDDING_DIMENSION=
EMBEDDING_BATCH_SIZE=
```

The actual variables will be finalized during implementation.

The embedding service should read configuration rather than hard-coding model identifiers throughout the application.

---

# 23. Performance Considerations

Embedding generation can become expensive during large-scale document ingestion.

Potential optimizations include:

```text
Batch embedding
Caching
Asynchronous processing
Parallel processing
Avoiding duplicate embeddings
```

Example:

```text
100 Chunks
   │
   ▼
Batch Embedding
   │
   ▼
Vectors
```

Rather than sending one request for every chunk when the selected model/provider supports batching.

---

# 24. Cost Considerations

Embedding costs may arise from:

```text
Document ingestion
Query processing
Re-indexing
Model API calls
Infrastructure
```

Caching can reduce repeated computation.

For example:

```text
Same Document
      │
      ▼
Already Embedded?
      │
 ┌────┴─────┐
 ▼          ▼
Yes        No
 │          │
 ▼          ▼
Reuse     Embed
Vector
```

---

# 25. Evaluation Strategy

Embedding models should be evaluated using retrieval datasets.

A synthetic evaluation dataset can contain:

```text
Query
Relevant Document
Relevant Chunk
Language
Query Type
```

Possible query categories:

```text
English
Indian language
Code-mixed
Paraphrased
Short query
Long query
Conversational follow-up
```

---

## Retrieval Metrics

Potential metrics include:

```text
Recall@K
Precision@K
MRR
nDCG
```

The project should select metrics appropriate to the final retrieval architecture.

---

# 26. Embedding Failure Handling

Embedding generation may fail because of:

```text
Model unavailable
Provider timeout
Rate limit
Invalid input
Service failure
Resource exhaustion
```

The backend should handle these failures through the general error-handling strategy.

For document ingestion:

```text
Embedding Failure
       │
       ▼
Retry if appropriate
       │
       ▼
Still failing?
       │
       ▼
Mark Processing as FAILED
```

For query-time retrieval:

```text
Embedding Failure
       │
       ▼
Retry / Fallback
       │
       ▼
Unable to retrieve
       │
       ▼
Safe Response
```

---

# 27. Future Improvements

Potential future enhancements include:

- Better multilingual embedding models
- Improved Indian-language retrieval
- Specialized code-mixed embeddings
- Hybrid search
- Sparse + dense retrieval
- Domain-specific embedding models
- Fine-tuned embedding models
- Query rewriting
- Multi-vector retrieval
- Cross-encoder reranking

These should be introduced based on evaluation results.

---

# 28. Summary

Embeddings form the semantic retrieval layer of AI Concierge.

The core architecture is:

```text
                DOCUMENT
                    │
                    ▼
                 Chunking
                    │
                    ▼
             Embedding Model
                    │
                    ▼
                  Vector
                    │
                    ▼
                 Qdrant
                    ▲
                    │
               Query Vector
                    ▲
                    │
                User Query
```

The embedding model must be evaluated specifically for:

```text
English
Indian languages
Multilingual retrieval
Code-mixed queries
Semantic similarity
Retrieval accuracy
Latency
Cost
```

The project should begin with a strong multilingual embedding model and evaluate whether it performs sufficiently well for the selected Indian languages and code-mixed conversations.

If evaluation reveals weaknesses, the architecture should allow the embedding model to be replaced or improved without redesigning the entire RAG system.

The embedding model, vector dimension, similarity metric, and chunking strategy should all be versioned so that experiments remain reproducible.
