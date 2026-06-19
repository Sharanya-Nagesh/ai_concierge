# AI Concierge - RAG Design

## Purpose

Define the Retrieval-Augmented Generation (RAG) pipeline used by AI Concierge.

Goals:

* Accurate document-based answers
* Reduced hallucinations
* Source-aware responses
* Efficient retrieval

---

# What is RAG?

Traditional Flow:

```text id="t89cdo"
Question
↓
LLM
↓
Answer
```

Problem:

LLM only knows training data.

---

RAG Flow:

```text id="z4phwa"
Question
↓
Retriever
↓
Relevant Documents
↓
LLM
↓
Answer
```

Benefits:

* Uses user documents
* More accurate
* More trustworthy

---

# RAG Architecture

## Ingestion Pipeline

```text id="p7i1qf"
Document Upload
↓
Parser
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
Qdrant Storage
```

---

# Supported Formats

Version 1:

```text id="g63kgp"
PDF

TXT

DOCX
```

Future:

```text id="5m9u0l"
PPTX

HTML

Markdown
```

---

# Document Parsing

Module:

```text id="7ldmgs"
rag/parser.py
```

Responsibilities:

* Extract text
* Remove noise
* Preserve structure

Libraries:

```text id="y07hiy"
PyMuPDF

pdfplumber
```

---

# Chunking Strategy

Module:

```text id="tlvbka"
rag/chunker.py
```

Version 1 Strategy:

Recursive Chunking

Chunk Size:

```text id="x9t0vc"
500 tokens
```

Chunk Overlap:

```text id="2c2fci"
50 tokens
```

Reason:

* Maintains context
* Better retrieval

---

# Embedding Model

Module:

```text id="q4b2ij"
rag/embeddings.py
```

Version 1:

```text id="9f0mcb"
BAAI/bge-small-en-v1.5
```

Alternative:

```text id="2dj5n0"
text-embedding-3-small
```

Future:

```text id="yph7p6"
bge-large
```

Selection Criteria:

* Speed
* Accuracy
* Cost

---

# Vector Database

Platform:

```text id="1o8q6m"
Qdrant
```

Store:

```json id="6gvxns"
{
  "vector":[],
  "document_id":"123",
  "chunk_id":"456",
  "metadata":{}
}
```

Metadata:

```text id="9n8rzs"
filename

page_number

upload_date
```

---

# Retrieval Flow

User Query

↓

Generate Query Embedding

↓

Similarity Search

↓

Top K Retrieval

↓

Context Construction

↓

LLM

---

# Similarity Search

Metric:

```text id="57dmbw"
Cosine Similarity
```

Top K:

```text id="awuhdk"
5
```

Version 1:

Simple Retrieval

Future:

```text id="ryskql"
Hybrid Search

Reranking
```

---

# Context Builder

Module:

```text id="7l6vup"
rag/context_builder.py
```

Responsibilities:

* Merge chunks
* Remove duplicates
* Respect token budget

Output:

```text id="vh2thj"
Context Block
```

---

# Prompt Template

System Prompt:

```text id="cqyqcm"
Answer using only the provided context.

If information is unavailable,
say you do not know.
```

Context:

```text id="bz9h3z"
Retrieved Chunks
```

Question:

```text id="oq9wnl"
User Query
```

---

# Citation Strategy

Version 1:

```text id="gx22oq"
[Source: filename, page]
```

Example:

```text id="uj1znc"
According to Chapter 2
(Source: NLP.pdf, Page 12)
```

---

# RAG Evaluation

Metrics:

## Recall@K

Measures:

Relevant chunks retrieved.

Target:

```text id="n8rmfw"
>80%
```

---

## Precision@K

Measures:

How relevant retrieved chunks are.

Target:

```text id="jlwm5d"
>75%
```

---

## Faithfulness

Measures:

Response grounded in context.

Target:

```text id="1k9wku"
>90%
```

---

# Hallucination Prevention

Rules:

1. Always retrieve before answering.

2. Never answer beyond context.

3. Use citations.

4. Return "Information not found" when needed.

---

# Future Improvements

## Hybrid Search

Combine:

```text id="xmbij4"
Keyword Search

Vector Search
```

---

## Cross Encoder Reranking

Improve retrieval quality.

---

## Multi-Document Reasoning

Retrieve across documents.

---

## Graph RAG

Knowledge graph augmentation.

---

# Version 1 Scope

Build:

✓ PDF Upload

✓ Text Extraction

✓ Chunking

✓ Embeddings

✓ Qdrant

✓ Retrieval

✓ Citations

Avoid:

✗ Graph RAG

✗ Agentic RAG

✗ Complex Reranking

until core RAG is working reliably.
