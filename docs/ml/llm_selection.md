# LLM Selection

> **Project:** AI Concierge  
> **Version:** 1.0  
> **Status:** Draft  
> **Document Type:** ML / LLM Design

---

# Table of Contents

1. Introduction
2. Why an LLM is Required
3. Role of the LLM
4. What the LLM Should Not Do
5. LLM Architecture
6. Model Selection Requirements
7. Multilingual Requirements
8. Code-Mixed Conversation Requirements
9. Context Handling
10. RAG and LLM Relationship
11. Agent and LLM Relationship
12. Structured Output
13. Model Parameters
14. Primary and Fallback Models
15. Model Selection Criteria
16. Candidate Model Categories
17. Provider Abstraction
18. Model Configuration
19. Prompt and Model Separation
20. Cost Considerations
21. Latency Considerations
22. Privacy Considerations
23. LLM Failure Handling
24. Model Evaluation
25. Model Versioning
26. Future Fine-Tuning
27. Final Selection Strategy
28. Summary

---

# 1. Introduction

The Large Language Model (LLM) is the conversational reasoning component of AI Concierge.

It converts:

```text
User Message
     +
Conversation Context
     +
Retrieved Information
     +
User Preferences
     +
Application Instructions
```

into:

```text
Natural Language Response
```

The LLM is therefore responsible for understanding and generating natural language, while other components provide data, retrieval, memory, tools, and application logic.

---

# 2. Why an LLM is Required

Traditional rule-based chatbots generally depend on predefined patterns.

For example:

```text
User says X
    ↓
Rule X
    ↓
Response X
```

This becomes difficult when users communicate naturally.

An LLM allows the system to handle:

```text
Natural language
Multilingual conversations
Code-mixed language
Follow-up questions
Different writing styles
Conversational context
Complex requests
```

---

# 3. Role of the LLM

The LLM is responsible for:

- Understanding user intent
- Understanding conversational context
- Generating natural responses
- Following system instructions
- Using retrieved context
- Producing structured outputs when required
- Supporting multilingual conversations
- Handling code-mixed input
- Reasoning over information provided by the application

---

## Example

A user may ask:

```text
"Can you suggest something for me?"
```

The meaning depends on:

```text
Previous conversation
+
User profile
+
Available rewards
+
Current context
```

The LLM helps interpret the request using this information.

---

# 4. What the LLM Should Not Do

The LLM should not independently control important application state.

For example, the LLM should not directly:

```text
Modify the database
Delete user data
Access arbitrary files
Retrieve another user's information
Call unrestricted APIs
Change account settings
```

Instead:

```text
LLM
 │
 ▼
Request / Tool Call
 │
 ▼
Backend Validation
 │
 ▼
Authorized Service
 │
 ▼
Result
```

The backend remains the final authority.

---

# 5. LLM Architecture

The LLM sits within a larger AI pipeline.

```text
                         User
                          │
                          ▼
                    Chat Interface
                          │
                          ▼
                     Backend API
                          │
                          ▼
                    Conversation
                     Processing
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Memory        RAG        Tools
              │           │           │
              └───────────┼───────────┘
                          ▼
                         LLM
                          │
                          ▼
                    Response Validation
                          │
                          ▼
                       Backend
                          │
                          ▼
                         User
```

The LLM is therefore one component of the AI system rather than the entire system.

---

# 6. Model Selection Requirements

The selected model should satisfy the project's functional requirements.

Important requirements include:

```text
Strong conversational ability
Multilingual support
Code-mixed language support
Good instruction following
Reasonable context length
Structured output support
Good latency
Reasonable cost
Reliable API availability
```

---

# 7. Multilingual Requirements

AI Concierge is intended to support multiple Indian languages.

The LLM should therefore be evaluated for its ability to:

- Understand Indian languages
- Generate Indian-language responses
- Switch languages appropriately
- Maintain conversational context across languages
- Handle transliterated input where possible

The system should not assume that a model performs equally well in every language.

---

## Language Strategy

The initial implementation should support a limited set of languages rather than attempting to support every Indian language immediately.

The selected languages should be chosen based on:

```text
Project scope
Dataset availability
Model capability
Evaluation feasibility
User requirements
```

Additional languages can be added later.

---

# 8. Code-Mixed Conversation Requirements

Code-mixed conversation is an important feature of AI Concierge.

Users may naturally combine languages within the same conversation.

For example, a user might write a sentence containing:

```text
English + Indian language
```

or:

```text
Indian language + English
```

The system should attempt to preserve the user's conversational style where appropriate.

---

## Code-Mixed Pipeline

```text
Code-Mixed User Message
          │
          ▼
Language Understanding
          │
          ▼
Intent Detection
          │
          ▼
Memory / RAG / Tools
          │
          ▼
LLM
          │
          ▼
Code-Mixed or Preferred-Language Response
```

The exact response-language policy should be configurable.

---

# 9. Context Handling

The LLM should receive only the context required for the current request.

Potential context includes:

```text
Current User Message
Recent Conversation
Relevant Long-Term Memory
Retrieved Documents
User Preferences
Tool Results
System Instructions
```

Conceptually:

```text
System Instructions
       +
Conversation Context
       +
Relevant Memory
       +
RAG Context
       +
Tool Results
       +
Current User Message
       │
       ▼
      LLM
```

The system should avoid sending unnecessary information because excessive context can increase:

- Token usage
- Cost
- Latency
- Noise

---

# 10. RAG and LLM Relationship

The LLM should not be expected to know private or application-specific information by itself.

RAG provides relevant external context.

```text
User Question
      │
      ▼
Retriever
      │
      ▼
Relevant Documents
      │
      ▼
Context
      │
      ▼
LLM
      │
      ▼
Grounded Response
```

The LLM is responsible for using the retrieved context to formulate the response.

The retriever is responsible for finding relevant information.

---

# 11. Agent and LLM Relationship

The LLM may also act as the reasoning component of an agent.

Conceptually:

```text
User Request
     │
     ▼
    LLM
     │
     ▼
Determine Required Action
     │
     ▼
Select Tool
     │
     ▼
Backend Tool
     │
     ▼
Tool Result
     │
     ▼
    LLM
     │
     ▼
Final Response
```

Tool access must remain controlled by the backend.

---

# 12. Structured Output

Certain backend operations should use structured LLM output instead of unrestricted text.

Examples:

```text
Intent classification
Tool selection
Recommendation metadata
Language detection
Response classification
```

Conceptually:

```text
LLM
 │
 ▼
Structured Output
 │
 ▼
Schema Validation
 │
 ├── Valid → Continue
 │
 └── Invalid → Retry / Fallback
```

Structured output reduces ambiguity between the LLM and backend services.

---

# 13. Model Parameters

LLM parameters should be configurable.

Potential parameters include:

```text
Temperature
Maximum output tokens
Context length
Timeout
Top-p
```

The exact parameters depend on the selected provider/model.

---

## Temperature

Temperature influences response variability.

Conceptually:

```text
Lower temperature
    ↓
More predictable responses

Higher temperature
    ↓
More varied responses
```

For structured tasks, a lower temperature may be preferable.

For natural conversation, a moderate value may be appropriate.

The final values should be determined experimentally.

---

# 14. Primary and Fallback Models

The system may use a primary model and a fallback model.

```text
User Request
     │
     ▼
Primary LLM
     │
 ┌───┴────┐
 ▼        ▼
Success  Failure
 │        │
 ▼        ▼
Response Fallback LLM
```

Fallback behavior should be used for appropriate temporary failures.

A fallback model should not silently produce significantly different behavior without considering the application requirements.

---

# 15. Model Selection Criteria

Models should be evaluated using multiple criteria.

| Criterion | Importance |
|---|---|
| Multilingual understanding | High |
| Code-mixed understanding | High |
| Instruction following | High |
| Response quality | High |
| Context length | Medium/High |
| Structured output | High |
| Latency | High |
| Cost | High |
| Availability | High |
| Deployment complexity | Medium |

The exact priorities may change during implementation.

---

# 16. Candidate Model Categories

The project can evaluate several model categories.

## Hosted Commercial Models

Advantages:

```text
Strong performance
Easy integration
Managed infrastructure
```

Disadvantages:

```text
API cost
External dependency
Potential data/privacy considerations
```

---

## Open-Source / Open-Weight Models

Advantages:

```text
More control
Potential self-hosting
Customization possibilities
```

Disadvantages:

```text
Infrastructure requirements
Model hosting cost
More operational complexity
```

---

## Small Language Models

Advantages:

```text
Lower latency
Lower resource requirements
Lower cost
```

Disadvantages:

```text
Potentially lower reasoning ability
Potentially weaker multilingual performance
```

The final model should be selected based on evaluation rather than model popularity alone.

---

# 17. Provider Abstraction

The backend should avoid coupling application logic directly to one LLM provider.

Instead:

```text
Application
    │
    ▼
LLM Service Interface
    │
 ┌──┼──────────────┐
 ▼  ▼              ▼
Provider A      Provider B
                   Provider C
```

This makes it easier to:

- Change providers
- Add fallback models
- Compare models
- Test different models
- Reduce vendor lock-in

---

# 18. Model Configuration

Model configuration should be stored outside business logic.

Example:

```text
LLM_PROVIDER=
LLM_MODEL=
LLM_TEMPERATURE=
LLM_MAX_TOKENS=
LLM_TIMEOUT=
```

These settings belong in the configuration system documented in:

```text
docs/backend/configuration.md
```

The application should be able to change the selected model without rewriting the conversational service.

---

# 19. Prompt and Model Separation

Prompts should not be tightly coupled to model-specific implementation.

Conceptually:

```text
Prompt Templates
       │
       ▼
LLM Service
       │
       ▼
Selected Model
```

This makes it possible to evaluate the same prompt strategy across different models.

Prompt design is documented separately in:

```text
docs/ml/prompt_engineering.md
```

---

# 20. Cost Considerations

LLM cost depends on factors such as:

```text
Input tokens
Output tokens
Model
Request frequency
Context size
Provider pricing
```

The system should minimize unnecessary context.

For example:

```text
Entire Conversation
        ↓
Potentially Large Context
        ↓
Higher Cost
```

Instead:

```text
Relevant Conversation
        +
Relevant Memory
        +
Relevant RAG Context
        ↓
Smaller Context
        ↓
Lower Cost
```

---

# 21. Latency Considerations

LLM latency affects the user experience.

Total response time may include:

```text
API Processing
      +
Memory Retrieval
      +
Embedding
      +
Vector Search
      +
Reranking
      +
LLM Generation
```

Therefore, model selection should consider both:

```text
Response Quality
```

and:

```text
Response Latency
```

---

# 22. Privacy Considerations

The system may process:

```text
Conversation data
User preferences
Documents
Memory
Recommendations
```

Therefore, the LLM provider must be evaluated for:

- Data handling
- Retention policies
- Privacy requirements
- Enterprise controls where applicable

Sensitive information should not be sent to an external provider unnecessarily.

---

# 23. LLM Failure Handling

LLM failures are handled by the backend error-handling system.

Potential failures include:

```text
Timeout
Rate limit
Provider unavailable
Invalid request
Model unavailable
Context too large
```

The general flow is:

```text
LLM Request
     │
     ▼
Failure
     │
 ┌───┼───────────┐
 ▼   ▼           ▼
Retry Fallback  Safe Error
```

Not every failure should trigger a retry.

---

# 24. Model Evaluation

Model selection must be based on evaluation.

The evaluation should include:

```text
General conversation
Multilingual conversation
Code-mixed conversation
RAG responses
Instruction following
Structured output
Safety
Latency
Cost
```

---

## Example Evaluation Dataset

A synthetic evaluation dataset can contain:

```text
Question
Expected Language
Expected Intent
Relevant Context
Expected Response Properties
```

The dataset should not contain private user information.

---

# 25. Model Versioning

The exact model identifier should be recorded.

For example:

```text
Provider
Model Name
Model Version
Configuration
Prompt Version
```

This allows results to be reproduced.

Conceptually:

```text
Experiment
   │
   ├── Model Version
   ├── Prompt Version
   ├── Parameters
   └── Evaluation Dataset
```

---

# 26. Future Fine-Tuning

Fine-tuning is **not required for the initial version**.

The first implementation should prioritize:

```text
Prompt Engineering
+
RAG
+
Memory
+
Tool Integration
```

Fine-tuning can be considered later if evaluation shows a consistent model limitation.

Potential future use cases include:

```text
Better Indian-language responses
Better code-mixed understanding
Domain-specific response style
Intent classification
Specialized structured outputs
```

Fine-tuning should be considered only after collecting a sufficiently useful and legally appropriate dataset.

---

# 27. Final Selection Strategy

The project should not select a model solely because it is the most powerful model available.

Instead:

```text
Candidate Models
      │
      ▼
Create Evaluation Dataset
      │
      ▼
Test Multilingual Performance
      │
      ▼
Test Code-Mixed Performance
      │
      ▼
Test RAG Performance
      │
      ▼
Measure Latency
      │
      ▼
Measure Cost
      │
      ▼
Compare Results
      │
      ▼
Select Primary Model
      │
      ▼
Select Fallback
```

The final choice should be documented after experimentation.

---

# 28. Summary

The LLM is the conversational reasoning component of AI Concierge, but it is not the authority over application data or actions.

The architecture is:

```text
                    AI Concierge
                         │
                         ▼
                       LLM
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      Memory            RAG             Tools
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                   Backend Rules
                         │
                         ▼
                    Final Response
```

The selected model should be evaluated for:

```text
Multilingual capability
Code-mixed capability
Instruction following
RAG compatibility
Structured output
Latency
Cost
Privacy
Reliability
```

The initial project should prioritize **integration and evaluation before fine-tuning**.

The final model choice will be recorded after comparing candidate models on a controlled evaluation dataset.
