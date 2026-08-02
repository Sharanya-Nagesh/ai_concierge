# RAG Architecture

> **Project:** AI Concierge – Personalized AI Assistant

> **Version:** 1.0

> **Status:** Draft

---

# Table of Contents

1. Introduction
2. What is RAG?
3. Why RAG?
4. High-Level Architecture
5. RAG Pipeline
6. Document Ingestion Pipeline
7. Chunking Strategy
8. Embedding Generation
9. Vector Database Design
10. Retrieval Pipeline
11. Re-ranking
12. Prompt Construction
13. Answer Generation
14. Citation Generation
15. Hybrid Retrieval
16. Performance Optimization
17. Security Considerations
18. Future Enhancements

---

# 1. Introduction

Retrieval-Augmented Generation (RAG) enables the AI Concierge to answer questions using user-provided documents instead of relying solely on the knowledge stored in a Large Language Model (LLM).

Instead of memorizing documents, the system retrieves the most relevant content at query time and provides grounded, context-aware responses.

---

# 2. What is RAG?

RAG combines two capabilities:

- **Retrieval:** Find relevant information from a knowledge base.
- **Generation:** Use an LLM to generate a natural language response based on the retrieved information.

This approach reduces hallucinations, improves factual accuracy, and enables the AI to answer questions about private or domain-specific documents.

---

# 3. Why RAG?

Using RAG offers several advantages:

- Answers are grounded in uploaded documents.
- Supports private and proprietary knowledge.
- Reduces hallucinations.
- Provides citations to source documents.
- Keeps information up to date without retraining the LLM.
- Scales to large document collections.

---

# 4. High-Level Architecture

```text
             User Uploads PDF
                     │
                     ▼
           Document Processing Service
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
  PostgreSQL                Qdrant Vector DB
 (Metadata)                 (Embeddings)
        │                         ▲
        └────────────┬────────────┘
                     │
                     ▼
               User Question
                     │
                     ▼
              Query Embedding
                     │
                     ▼
            Semantic Vector Search
                     │
                     ▼
            Top-K Relevant Chunks
                     │
                     ▼
              Prompt Construction
                     │
                     ▼
                  LLM Response
                     │
                     ▼
         Answer + Citations Returned
```

---

# 5. End-to-End RAG Pipeline

```text
Upload Document

↓

Extract Text

↓

Clean Text

↓

Chunk Document

↓

Generate Embeddings

↓

Store Metadata (PostgreSQL)

↓

Store Embeddings (Qdrant)

↓

User Query

↓

Generate Query Embedding

↓

Retrieve Similar Chunks

↓

Re-rank Results

↓

Construct Prompt

↓

Generate Answer

↓

Return Response with Citations
```

---

# 6. Document Ingestion Pipeline

Each uploaded document follows these steps:

### Step 1 – File Validation

- Verify file type
- Check file size
- Scan for corruption
- Generate unique document ID

---

### Step 2 – Text Extraction

Supported formats:

- PDF
- DOCX (Future)
- TXT
- Markdown
- PPTX (Future)

Libraries:

- PyMuPDF
- pdfplumber
- python-docx

---

### Step 3 – Text Cleaning

The extracted text is normalized by:

- Removing extra whitespace
- Removing headers/footers (optional)
- Preserving section headings
- Maintaining page numbers
- Normalizing Unicode

---

# 7. Chunking Strategy

Large documents are divided into smaller chunks before embedding.

### Chunk Size

```
500–800 tokens
```

### Chunk Overlap

```
100–150 tokens
```

### Why Overlap?

Overlap preserves context across chunk boundaries.

Example:

```text
Chunk 1
-------------------------
Attention mechanism...
Encoder architecture...
Self-attention begins...

Chunk 2
-------------------------
Self-attention begins...
Scaled dot-product...
Multi-head attention...
```

---

### Chunk Metadata

Each chunk stores:

- Chunk ID
- Document ID
- Page Number
- Section Title
- Chunk Index
- Token Count

---

# 8. Embedding Generation

Each chunk is converted into a dense vector representation.

### Example Models

- BAAI/bge-large-en-v1.5
- BAAI/bge-m3 (multilingual)
- nomic-embed-text
- multilingual-e5-large

---

### Embedding Pipeline

```text
Chunk

↓

Tokenizer

↓

Embedding Model

↓

768 / 1024 / 1536 Dimensional Vector

↓

Qdrant
```

---

# 9. Vector Database Design

The project uses **Qdrant** as the vector database.

Each vector contains:

```text
Vector

+

Metadata
```

Metadata includes:

- document_id
- chunk_id
- page_number
- filename
- section
- token_count

---

# 10. Retrieval Pipeline

When a user asks a question:

```text
User Question

↓

Embedding Model

↓

Query Vector

↓

Qdrant Similarity Search

↓

Top 10 Chunks

↓

Re-ranking

↓

Top 5 Chunks

↓

Prompt Builder
```

---

# 11. Re-ranking

Initial retrieval may include less relevant chunks.

A re-ranking model improves relevance before sending context to the LLM.

Possible models:

- bge-reranker-large
- cross-encoder/ms-marco-MiniLM
- jina-reranker-v2

Benefits:

- Better answer quality
- Improved citation accuracy
- Reduced irrelevant context

---

# 12. Prompt Construction

The retrieved chunks are combined into a structured prompt.

Example structure:

```text
System Prompt

+

Conversation History

+

Relevant Memories

+

Retrieved Chunks

+

User Question
```

Only the highest-ranked chunks are included to stay within the model's context window.

---

# 13. Answer Generation

The LLM receives:

- User query
- Retrieved context
- Conversation history
- Long-term memory (if relevant)

The model generates a response grounded in the supplied documents.

If no relevant context is found, the assistant should clearly indicate that the answer could not be determined from the uploaded documents instead of fabricating information.

---

# 14. Citation Generation

Each retrieved chunk contains metadata such as:

- Document Name
- Page Number
- Section

Example response:

```text
According to Chapter 4, self-attention computes relationships between all input tokens.

Source:
Transformers.pdf
Page 42
Section: Self-Attention
```

This improves transparency and user trust.

---

# 15. Hybrid Retrieval

Future versions may combine multiple retrieval methods:

```text
User Query

↓

Keyword Search (BM25)

+

Vector Search

↓

Score Fusion

↓

Re-ranking

↓

LLM
```

Benefits:

- Better exact-match retrieval
- Improved semantic retrieval
- More robust search performance

---

# 16. Performance Optimization

Techniques include:

- Batch embedding generation
- Asynchronous document processing
- Embedding cache
- Query cache
- Parallel retrieval
- Metadata filtering
- Incremental indexing

---

# 17. Security Considerations

- User documents are isolated by user ID.
- Vector searches are scoped to the authenticated user.
- Uploaded files are validated before processing.
- Metadata does not expose sensitive information.
- Original documents can be permanently deleted upon user request.

---

# 18. Future Enhancements

Potential improvements include:

- Graph RAG
- Agentic RAG
- Multi-modal RAG (images, tables, diagrams)
- Knowledge Graph integration
- Incremental document updates
- Multi-vector retrieval
- Adaptive chunking
- Context compression
- Query rewriting
- Self-reflection and answer verification
- Multi-document reasoning

---

# Summary

The AI Concierge uses a Retrieval-Augmented Generation (RAG) architecture to answer questions based on user-uploaded documents. Documents are validated, processed, chunked, embedded, and indexed in Qdrant, while metadata is stored in PostgreSQL. At query time, the system retrieves the most relevant document chunks, optionally re-ranks them, constructs a context-rich prompt, and generates grounded responses with citations. This architecture improves factual accuracy, reduces hallucinations, and enables personalized knowledge retrieval without retraining the language model.
