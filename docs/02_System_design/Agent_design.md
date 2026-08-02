# AI Concierge - Agent Design

## Purpose

This document defines the multi-agent architecture used in AI Concierge.

Goals:

* Modular reasoning
* Easier debugging
* Better maintainability
* Agent-level observability
* Extensible architecture

---

# Why Multi-Agent?

Instead of one giant prompt:

```text id="r8l1v2"
User Query
↓
LLM
↓
Response
```

We use:

```text id="43u4ws"
User Query
↓
Intent Agent
↓
Memory Agent
↓
Retrieval Agent
↓
Tool Agent
↓
Response Agent
↓
Final Answer
```

Benefits:

* Better separation of responsibilities
* Easier testing
* Easier upgrades

---

# Agent Orchestrator

Location:

```text id="6d8wsh"
agents/orchestrator.py
```

Responsibilities:

* Coordinate agents
* Route requests
* Merge outputs
* Track execution flow

Input:

```json id="5p0jew"
{
  "user_id":"123",
  "message":"Summarize Chapter 2"
}
```

Output:

```json id="fwymvc"
{
  "response":"..."
}
```

---

# Intent Agent

## Purpose

Classify user intent.

Location:

```text id="q6fuh4"
agents/intent_agent.py
```

Supported Intents:

```text id="v6h7jx"
CHAT

DOCUMENT_QA

TOOL_CALL

RECOMMENDATION

PROFILE_UPDATE

MEMORY_QUERY
```

Examples

Input:

```text id="jfwgik"
What is transformer architecture?
```

Output:

```json id="1vxt1j"
{
  "intent":"CHAT"
}
```

Input:

```text id="krq7ql"
Summarize my uploaded PDF
```

Output:

```json id="prnls5"
{
  "intent":"DOCUMENT_QA"
}
```

---

# Memory Agent

## Purpose

Retrieve relevant user memory.

Location:

```text id="w6c2fz"
agents/memory_agent.py
```

Responsibilities:

* User profile retrieval
* Conversation retrieval
* Conversation summaries

Input:

```json id="2fz1jw"
{
  "user_id":"123"
}
```

Output:

```json id="9jqf52"
{
  "response_style":"detailed",
  "interests":["AI"]
}
```

Memory Sources:

* User Preferences
* Recent Conversations
* Long-Term Summaries

---

# Retrieval Agent

## Purpose

Retrieve relevant document context.

Location:

```text id="1uz97w"
agents/retrieval_agent.py
```

Responsibilities:

* Query vector database
* Rank retrieved chunks
* Return context

Input:

```text id="zy3u4s"
Explain chapter 2
```

Output:

```json id="56jzgu"
{
  "chunks":[
      "...",
      "...",
      "..."
  ]
}
```

---

# Tool Agent

## Purpose

Execute external tools.

Location:

```text id="x1rvrv"
agents/tool_agent.py
```

Supported Tools:

```text id="tn4vk5"
Calculator

Web Search

Weather

Future APIs
```

Example

Input:

```text id="lrxw2w"
Calculate 25% of 400
```

Output:

```json id="cnqhy6"
{
  "result":100
}
```

---

# Response Agent

## Purpose

Generate final response.

Location:

```text id="vr70yr"
agents/response_agent.py
```

Responsibilities:

* Merge contexts
* Build prompt
* Call LLM
* Format output

Inputs:

```json id="q1l2rh"
{
  "memory":{},
  "documents":[],
  "tool_output":{},
  "user_query":"..."
}
```

Output:

```json id="5r40g7"
{
  "response":"..."
}
```

---

# Agent Communication Flow

```text id="a4d0t6"
User Query

↓

Intent Agent

↓

Memory Agent

↓

Retrieval Agent (optional)

↓

Tool Agent (optional)

↓

Response Agent

↓

User Response
```

---

# Prompt Design

Each agent has:

```text id="tubj3s"
System Prompt

Input Schema

Output Schema
```

Never allow free-form outputs between agents.

Always use structured JSON.

---

# Agent Evaluation

Metrics:

## Intent Agent

* Classification Accuracy

Target:

```text id="k3n25t"
>95%
```

---

## Retrieval Agent

Metrics:

```text id="7cyrqy"
Recall@K

Precision@K
```

---

## Response Agent

Metrics:

```text id="zz1k2n"
Faithfulness

Relevance

Completeness
```

---

# Future Agents

## Recommendation Agent

Provides personalized suggestions.

---

## Planning Agent

Breaks tasks into subtasks.

---

## Reflection Agent

Evaluates generated answers.

---

# Version 1 Agent Scope

Build:

✓ Intent Agent

✓ Memory Agent

✓ Retrieval Agent

✓ Tool Agent

✓ Response Agent

Avoid unnecessary complexity until V2.
