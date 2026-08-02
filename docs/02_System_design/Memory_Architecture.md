# Memory Architecture

> Project: AI Concierge – Personalized AI Assistant

> Version: 1.0

> Status: Draft

---

# Table of Contents

1. Introduction
2. Why Memory Matters
3. Memory Types
4. Memory Storage Architecture
5. Memory Retrieval Pipeline
6. Memory Ranking
7. Memory Lifecycle
8. Memory Categories
9. Memory Extraction
10. Future Enhancements

---

# 1. Introduction

Memory enables AI Concierge to remember important user information across conversations, making interactions personalized and context-aware.

Unlike conversation history, memories persist between sessions and evolve over time.

---

# 2. Why Memory Matters

Without memory, the assistant forgets previous interactions.

With memory, it can:

- Remember long-term goals
- Personalize recommendations
- Avoid repetitive questions
- Continue previous discussions
- Build user-specific context

---

# 3. Memory Types

## Working Memory

- Current conversation only
- Temporary
- Stored in RAM

Example:

> "Summarize this PDF."

---

## Short-Term Memory

Stores recent conversations.

Retention:

- Last 10–20 conversations

Purpose:

- Maintain conversational continuity

---

## Long-Term Memory

Stores persistent user facts.

Examples:

- Preferred language
- Career goals
- Learning preferences
- Interests
- Projects

Stored in PostgreSQL + Qdrant.

---

## Episodic Memory

Remembers significant past events.

Examples:

- Completed AI-900 certification
- Uploaded a research paper
- Finished MLOps roadmap

---

## Semantic Memory

Stores factual knowledge extracted from user interactions.

Examples:

- User prefers Python
- User likes concise explanations
- User studies NLP

---

# 4. Memory Storage Architecture

```text
Conversation

↓

Memory Extractor

↓

Importance Scoring

↓

Store Metadata → PostgreSQL

↓

Generate Embedding

↓

Store Vector → Qdrant
```

---

# 5. Memory Retrieval Pipeline

```text
User Query

↓

Embedding Generation

↓

Semantic Search (Qdrant)

↓

Retrieve Top Memories

↓

Rank Memories

↓

Inject into Prompt

↓

LLM Response
```

---

# 6. Memory Ranking

Each memory is ranked using:

- Semantic similarity
- Importance score
- Recency
- Frequency of access
- User feedback

Final score determines which memories are included in the LLM prompt.

---

# 7. Memory Lifecycle

Conversation

↓

Extract Candidate Memories

↓

Assign Importance

↓

Store

↓

Retrieve When Relevant

↓

Update or Merge

↓

Delete (if obsolete)

---

# 8. Memory Categories

- Career
- Education
- Skills
- Projects
- Preferences
- Hobbies
- Languages
- Certifications
- Goals
- Custom Notes

---

# 9. Memory Extraction

The Memory Extractor identifies information worth remembering.

Examples:

User: "I'm preparing for Azure AI-900."

→ Store as Career/Education memory.

---

User: "I prefer explanations with diagrams."

→ Store as Preference memory.

---

User: "My project uses Qdrant."

→ Store as Project memory.

Low-value conversational details are discarded.

---

# 10. Memory Update Strategy

If a new memory conflicts with an existing one:

- Compare timestamps
- Compare confidence
- Update existing memory if newer
- Merge complementary information
- Keep history for audit (future)

---

# 11. Memory Expiration

Not all memories last forever.

Examples:

Temporary

- Current semester
- Current assignment

Permanent

- Preferred language
- Career aspirations
- Long-term interests

Future versions may automatically archive stale memories.

---

# 12. Privacy & User Control

Users can:

- View memories
- Edit memories
- Delete memories
- Disable memory collection
- Export memory data

---

# 13. Future Enhancements

- Hierarchical memory
- Graph-based memory
- Multi-modal memory (images, audio)
- Memory summarization
- Memory conflict resolution using LLMs
- Shared team memory
- Adaptive forgetting algorithms

---

# Summary

The AI Concierge memory system combines working, short-term, long-term, episodic, and semantic memory to create a personalized user experience. Structured metadata is stored in PostgreSQL, while semantic embeddings are indexed in Qdrant for fast retrieval. Intelligent extraction, ranking, and retrieval ensure that only the most relevant memories are incorporated into AI responses, enabling context-aware conversations across sessions.
