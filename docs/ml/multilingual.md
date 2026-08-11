# Multilingual and Code-Mixed Language Support

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / Multilingual Language Design

---

# Table of Contents

1. Introduction
2. Why Multilingual Support Matters
3. Language Support Strategy
4. Initial Language Scope
5. Four-to-Five Language Architecture
6. Language Detection
7. Code-Mixed Conversation
8. Transliteration
9. Language Identification and Routing
10. Multilingual Embeddings
11. Cross-Lingual Retrieval
12. Multilingual RAG
13. Conversation Memory
14. Response Language Selection
15. Language Switching
16. Translation Strategy
17. Prompt Design
18. LLM Requirements
19. Evaluation Dataset
20. Evaluation Metrics
21. Common Failure Cases
22. Fallback Strategy
23. Adding New Languages
24. Architecture
25. Implementation Phases
26. Future Improvements
27. Summary

---

# 1. Introduction

AI Concierge is designed to support conversations across multiple Indian languages.

Users should be able to communicate naturally rather than being forced to use English.

The system should support:

```text
English
+
Indian Languages
+
Code-Mixed Conversations
+
Language Switching
```

The multilingual system is therefore part of the core AI architecture.

---

# 2. Why Multilingual Support Matters

A conversational assistant intended for the Indian market should not assume that every user is most comfortable communicating in English.

A user may prefer:

```text
English
```

or:

```text
An Indian language
```

or:

```text
A mixture of English and an Indian language
```

The system should accommodate these communication patterns.

---

# 3. Language Support Strategy

The project should **not attempt to support every Indian language in the first version**.

Instead, the initial implementation should focus on a manageable set of approximately:

```text
4–5 languages
```

This is feasible if the selected models provide sufficient multilingual capability.

The important principle is:

> **Start with a small number of languages, evaluate them properly, and expand later.**

Supporting fewer languages well is preferable to claiming broad language support without adequate evaluation.

---

# 4. Initial Language Scope

The final language list should be decided based on:

```text
Model capability
Dataset availability
Evaluation feasibility
Project scope
User requirements
Development resources
```

A possible architecture can support:

```text
English
Language 1
Language 2
Language 3
Language 4
```

The exact Indian languages should be finalized during implementation.

The architecture should not hard-code the application around only one language.

---

# 5. Four-to-Five Language Architecture

Supporting 4–5 languages does not necessarily mean maintaining five completely separate AI systems.

The preferred architecture is:

```text
                    User
                      │
                      ▼
                Language Detection
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       English     Language A   Language B
          │           │           │
          └───────────┼───────────┘
                      ▼
              Shared AI Pipeline
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
    Memory           RAG            LLM
       │              │              │
       └──────────────┼──────────────┘
                      ▼
                Response Language
                      │
                      ▼
                    User
```

The same backend architecture can therefore support multiple languages.

---

# 6. Language Detection

The system should determine the language of the user's message where necessary.

Conceptually:

```text
User Message
      │
      ▼
Language Detector
      │
      ▼
Language / Language Distribution
```

For a clearly single-language message:

```text
Message
  ↓
Language A
```

For a code-mixed message:

```text
Message
  ↓
Language A + English
```

Language detection should not unnecessarily delay every request.

If the user has explicitly selected a preferred language, that preference can also be used as an important signal.

---

# 7. Code-Mixed Conversation

Code-mixing is a first-class requirement.

Users may naturally mix:

```text
English + Indian language
```

within the same sentence or conversation.

The system should not automatically translate every message into English unless translation is actually required.

Instead, the preferred approach is:

```text
Original User Message
        │
        ▼
Understand Meaning
        │
        ▼
Retrieve Relevant Context
        │
        ▼
Generate Appropriate Response
```

---

# 8. Transliteration

Users may type an Indian language using Latin characters instead of its native script.

For example, a user may write an Indian-language phrase using:

```text
Latin / English characters
```

rather than the native writing system.

The system should ideally support both:

```text
Native Script
```

and:

```text
Romanized / Transliterated Input
```

where the selected models support it.

---

## Transliteration Pipeline

```text
User Message
     │
     ▼
Detect Language / Script
     │
     ├── Native Script
     │       ↓
     │     Continue
     │
     └── Romanized Input
             ↓
        Language Understanding
             ↓
          Continue
```

Explicit transliteration into native script may be introduced later if evaluation shows that it improves downstream performance.

---

# 9. Language Identification and Routing

Language information can influence multiple components.

```text
Language Detection
       │
       ├── Prompt Configuration
       ├── Embedding Strategy
       ├── RAG Filtering
       ├── Response Language
       └── Evaluation
```

However, language detection should not unnecessarily create separate pipelines when a shared multilingual model can handle the request directly.

---

# 10. Multilingual Embeddings

The embedding model should support the languages selected for the project.

The goal is to represent semantically similar content in a compatible vector space.

For example:

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

This may enable cross-lingual retrieval.

However, cross-lingual retrieval must be evaluated rather than assumed.

---

# 11. Cross-Lingual Retrieval

The system should ideally support scenarios where the language of the query differs from the language of the stored information.

For example:

```text
User Query
   │
   │ Language A
   ▼
Embedding
   │
   ▼
Qdrant
   │
   ▼
Document
   │
   │ Language B
   ▼
Retrieved Context
```

The LLM can then use the retrieved information to generate a response in the user's preferred language.

This capability is particularly useful when the available knowledge base is not duplicated into every supported language.

---

# 12. Multilingual RAG

The RAG pipeline should be language-aware but should avoid unnecessary duplication.

Preferred architecture:

```text
User Query
     │
     ▼
Language Understanding
     │
     ▼
Query Embedding
     │
     ▼
Vector Search
     │
     ▼
Relevant Documents
     │
     ▼
Reranking
     │
     ▼
LLM Context
     │
     ▼
Response
```

The retrieved documents may be:

```text
Same language as query
```

or:

```text
Different language from query
```

depending on retrieval quality.

---

# 13. Conversation Memory

Memory should preserve meaning independently of the language used.

For example:

```text
Conversation Turn 1
English

Conversation Turn 2
Indian Language

Conversation Turn 3
Code-Mixed
```

The system should still maintain a coherent conversation.

Conceptually:

```text
Conversation
     │
     ▼
Language-Aware Processing
     │
     ▼
Normalized Semantic Representation
     │
     ▼
Memory
```

Memory should not depend on storing everything in one language.

---

# 14. Response Language Selection

The system should determine the appropriate response language using signals such as:

```text
Current user language
Recent conversation language
Explicit user preference
Code-mixing pattern
Application context
```

A simple strategy is:

```text
User writes in Language A
        ↓
Respond in Language A
```

If the user switches:

```text
Language A
    ↓
Language B
    ↓
Respond in Language B
```

For code-mixed conversations, the system may preserve a natural level of code-mixing where appropriate.

---

# 15. Language Switching

Users should be able to switch languages naturally.

Example:

```text
Conversation
     │
     ├── English
     │
     ├── Indian Language A
     │
     └── English + Language A
```

The backend should not treat language switching as a new conversation.

The same:

```text
Conversation ID
Memory
User Context
```

should continue to apply.

---

# 16. Translation Strategy

Translation should be used selectively.

The system should distinguish:

```text
Understanding a language
```

from:

```text
Translating a language
```

An LLM that already understands multiple languages does not necessarily need an explicit translation step.

Preferred architecture:

```text
Multilingual Input
       │
       ▼
Multilingual Model
       │
       ▼
Understand Directly
```

Translation may be introduced when:

```text
A component does not support the language
```

or:

```text
Cross-language processing improves retrieval
```

or:

```text
A specific downstream model requires one language
```

---

# 17. Prompt Design

Prompts should clearly communicate language behavior.

The system prompt may define rules such as:

```text
Respond in the user's preferred language.

Preserve the user's intended meaning.

Do not translate unnecessarily.

If the user intentionally mixes languages,
respond naturally while maintaining clarity.

Do not fabricate information when context is unavailable.
```

The exact prompt wording will be finalized during prompt engineering and evaluation.

---

# 18. LLM Requirements

The selected LLM should be evaluated for:

```text
Language understanding
Language generation
Code-mixed understanding
Code-mixed generation
Context retention
Instruction following
Native-script handling
Romanized input handling
Cross-lingual reasoning
```

Performance may vary significantly between languages.

Therefore, evaluation should be performed separately for each target language.

---

# 19. Evaluation Dataset

A multilingual evaluation dataset should be created.

It should contain examples across:

```text
Language A
Language B
Language C
Language D
Language E
English
```

and:

```text
Code-mixed queries
```

It should also include different types of conversations.

---

## Query Categories

```text
Simple Questions
Follow-up Questions
Contextual Questions
Recommendation Requests
RAG Questions
Ambiguous Questions
Out-of-Domain Questions
Code-Mixed Questions
```

---

## Example Dataset Structure

```text
{
    "query": "...",
    "language": "...",
    "is_code_mixed": true,
    "expected_intent": "...",
    "expected_response_language": "...",
    "relevant_context": "..."
}
```

The dataset should contain synthetic or appropriately licensed data.

---

# 20. Evaluation Metrics

Multilingual performance should be evaluated using multiple dimensions.

## Language Detection

```text
Accuracy
Precision
Recall
F1
```

---

## Retrieval

```text
Recall@K
MRR
nDCG
```

---

## Response Quality

Potential evaluation dimensions:

```text
Correctness
Relevance
Groundedness
Fluency
Language appropriateness
Instruction following
```

---

## Code-Mixed Evaluation

Additional criteria:

```text
Meaning preservation
Language identification
Naturalness
Context retention
Appropriate language switching
```

---

# 21. Common Failure Cases

The system should specifically test for:

### Failure 1 — Wrong Language Detection

```text
Indian Language
      ↓
Incorrectly classified
      ↓
Wrong processing strategy
```

---

### Failure 2 — Unnatural Translation

The system may translate a naturally code-mixed sentence unnecessarily.

---

### Failure 3 — Language Drift

The user communicates in one language, but the assistant unexpectedly switches to another language.

---

### Failure 4 — Weak Retrieval

The query is understood correctly but relevant documents are not retrieved.

---

### Failure 5 — Script Confusion

Romanized input may be interpreted incorrectly.

---

### Failure 6 — Uneven Language Quality

The model may perform strongly in one language and poorly in another.

This is one reason each supported language should be evaluated independently.

---

# 22. Fallback Strategy

If the system cannot confidently process a particular language:

```text
Language Detection
       │
       ▼
Low Confidence
       │
       ▼
Fallback Strategy
```

Possible fallback behavior includes:

```text
Ask the user to rephrase
```

or:

```text
Continue using a supported common language
```

or:

```text
Use a translation component
```

The fallback should be transparent rather than pretending to understand something it does not.

---

# 23. Adding New Languages

New languages should be added incrementally.

```text
New Language
     │
     ▼
Check Model Support
     │
     ▼
Create Evaluation Data
     │
     ▼
Test Language Detection
     │
     ▼
Test Embeddings
     │
     ▼
Test RAG
     │
     ▼
Test LLM Responses
     │
     ▼
Add to Supported Languages
```

A language should not be marked as officially supported until it passes the project's minimum evaluation criteria.

---

# 24. Architecture

The complete multilingual architecture is:

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │ Language /      │
                  │ Script Analysis │
                  └────────┬────────┘
                           │
                           ▼
                    User Message
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Memory          RAG          Intent
             │             │             │
             └─────────────┼─────────────┘
                           ▼
                          LLM
                           │
                           ▼
                  Response Language
                           │
                           ▼
                         USER
```

The important architectural principle is:

> **Language support should be a capability of the shared AI pipeline, not five completely independent applications.**

---

# 25. Implementation Phases

## Phase 1 — English Baseline

Implement:

```text
English
RAG
Memory
LLM
Basic conversation
```

This establishes the baseline system.

---

## Phase 2 — Add One Indian Language

Evaluate:

```text
Language Detection
Embeddings
RAG
LLM Response
```

---

## Phase 3 — Expand to 3 Languages

Compare:

```text
Language Quality
Retrieval Quality
Latency
```

---

## Phase 4 — Expand to 4–5 Languages

Only add languages that can be adequately evaluated.

---

## Phase 5 — Code-Mixed Support

Evaluate:

```text
English + Indian Language
Indian Language + English
Multiple-language conversation
Romanized input
Language switching
```

---

## Phase 6 — Optimization

Improve:

```text
Prompting
Retrieval
Reranking
Memory
Latency
Fallbacks
```

---

# 26. Future Improvements

Potential future enhancements include:

- More Indian languages
- Better Romanized-language support
- Language-specific rerankers
- Language-specific embedding models
- Multilingual query rewriting
- Speech input
- Speech output
- Multilingual ASR
- Multilingual TTS
- Automatic language preference learning
- Language-aware personalization
- Better code-mixed evaluation datasets

These should be introduced only when justified by project requirements and evaluation results.

---

# 27. Summary

Multilingual and code-mixed conversation is a core capability of AI Concierge.

The recommended strategy is:

```text
Start Small
    ↓
Support 4–5 Languages
    ↓
Use Shared Multilingual Components
    ↓
Evaluate Each Language
    ↓
Add Code-Mixed Support
    ↓
Expand Gradually
```

The system should support:

```text
Multiple Indian Languages
        +
English
        +
Code-Mixed Conversations
        +
Language Switching
        +
Native Scripts
        +
Romanized Input
```

The architecture should avoid creating a completely separate AI pipeline for every language.

Instead:

```text
                Shared AI Pipeline
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
   Language A       Language B      Language C
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                  Shared RAG
                       │
                       ▼
                     LLM
```

The project should begin with approximately 4–5 carefully selected languages, validate their performance, and expand only when the system can demonstrate acceptable quality.

Most importantly, **multilingual support should be measured, not merely claimed**.

Every supported language should be evaluated for:

```text
Understanding
Retrieval
Generation
Code-mixing
Language switching
Groundedness
Response quality
```
