# User Flow

> **Project:** AI Concierge – Personalized AI Assistant

> **Version:** 1.0

> **Status:** Draft

---

# Table of Contents

1. Introduction
2. Design Goals
3. Overall User Journey
4. Authentication Flow
5. Dashboard Flow
6. Chat Flow
7. Document Upload Flow
8. RAG Question Answering Flow
9. Planner Flow
10. Recommendation Flow
11. Memory Flow
12. Settings Flow
13. Error Handling
14. Future User Flows

---

# 1. Introduction

This document describes how users interact with AI Concierge from the moment they open the application until they complete their tasks. It focuses on navigation, user actions, and system responses.

---

# 2. Design Goals

The user experience should:

- Minimize clicks to complete tasks
- Provide clear feedback
- Keep navigation intuitive
- Reduce cognitive load
- Support multilingual interactions
- Make AI features discoverable
- Ensure consistency across modules

---

# 3. Overall User Journey

```text
Open Application
        │
        ▼
Login / Register
        │
        ▼
Dashboard
        │
 ┌──────┼────────┬───────────┬────────────┐
 ▼      ▼        ▼           ▼            ▼
Chat Documents Planner Recommendations Memory
        │
        ▼
Settings / Logout
```

---

# 4. Authentication Flow

## Login

```text
Landing Page
      │
      ▼
Enter Email & Password
      │
      ▼
Validate Credentials
      │
 ┌────┴────┐
 │         │
Success   Failure
 │         │
 ▼         ▼
Dashboard Error Message
```

### Future Support

- Google Sign-In
- GitHub Login
- Microsoft Login

---

# 5. Dashboard Flow

The dashboard acts as the central hub.

### Sections

- Welcome message
- Recent conversations
- Planner progress
- Uploaded documents
- Recommendations
- Quick actions

### User Actions

- Start new chat
- Upload document
- Continue planner
- View recommendations
- Open settings

---

# 6. Chat Flow

```text
Open Chat
      │
      ▼
Type Message
      │
      ▼
Send
      │
      ▼
Router Agent
      │
 ┌────┼────────────┐
 ▼    ▼            ▼
Chat RAG      Planner
 │    │            │
 └────┴────────────┘
      │
      ▼
Generate Response
      │
      ▼
Display Response
```

### Features

- Conversation history
- Typing indicator
- Streaming responses
- Markdown rendering
- Code block formatting
- Citation display (for RAG)

---

# 7. Document Upload Flow

```text
Documents Page
       │
       ▼
Click Upload
       │
       ▼
Choose File
       │
       ▼
Validate File
       │
 ┌─────┴─────┐
 │           │
Valid      Invalid
 │           │
 ▼           ▼
Process    Show Error
 │
 ▼
Extract Text
 │
 ▼
Chunk Document
 │
 ▼
Generate Embeddings
 │
 ▼
Store Metadata + Vectors
 │
 ▼
Ready for Search
```

### Supported Formats

- PDF
- TXT
- DOCX (Future)
- PPTX (Future)

---

# 8. RAG Question Answering Flow

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Vector Search
      │
      ▼
Retrieve Top-K Chunks
      │
      ▼
Re-rank Results
      │
      ▼
Construct Prompt
      │
      ▼
LLM Generates Answer
      │
      ▼
Display Answer + Citations
```

### Example

User:

> "What are the eligibility criteria for Platinum Rewards?"

System:

- Searches uploaded documents
- Retrieves relevant sections
- Generates answer
- Shows source document and page number

---

# 9. Planner Flow

```text
Planner
    │
    ▼
Create Goal
    │
    ▼
Generate Roadmap
    │
    ▼
Weekly Tasks
    │
    ▼
Mark Progress
    │
    ▼
Update Completion Status
```

### Features

- Goal creation
- Weekly milestones
- Progress tracking
- AI-generated suggestions

---

# 10. Recommendation Flow

```text
Conversation History
        │
        ▼
Analyze Preferences
        │
        ▼
Recommendation Engine
        │
        ▼
Display Suggestions
```

Examples:

- Learning resources
- Reward offers
- Planner adjustments
- Relevant documents

Each recommendation includes a short explanation of why it was suggested.

---

# 11. Memory Flow

```text
Conversation
      │
      ▼
Extract User Preference
      │
      ▼
Store Long-Term Memory
      │
      ▼
Future Conversation
      │
      ▼
Retrieve Relevant Memory
      │
      ▼
Personalized Response
```

### Example

User:

> "I prefer Kannada and English."

The system remembers this preference and prioritizes those languages in future interactions.

---

# 12. Settings Flow

Users can manage:

- Profile information
- Preferred language
- Theme (Light/Dark/System)
- Notification preferences
- Privacy settings
- Memory management
- Account security

---

# 13. Error Handling

Examples of user-facing errors:

| Scenario | System Response |
|----------|-----------------|
| Invalid login | Show authentication error |
| Unsupported file | Display validation message |
| Upload failure | Retry option |
| No RAG results | Inform user that no relevant information was found |
| Network issue | Suggest retry |
| LLM timeout | Display fallback message |

Error messages should be clear, actionable, and avoid exposing internal system details.

---

# 14. Future User Flows

Potential future interactions include:

- Voice conversations
- Image-based document search
- Real-time collaborative chat
- Calendar integration
- Email summarization
- Multi-device synchronization
- Plugin ecosystem
- Offline document search

---

# Summary

The AI Concierge user flow is designed to guide users through authentication, conversational AI, document management, planning, recommendations, and memory features with minimal friction. Each workflow provides clear feedback and logical navigation while supporting advanced capabilities such as RAG-based question answering, multilingual conversations, and personalized assistance. The modular flow design also allows new features to be added without disrupting the overall user experience.
