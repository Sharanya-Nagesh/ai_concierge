# Prompt Versioning

## 1. Purpose

This document defines the strategy for creating, managing, evaluating and deploying prompt versions used by the AI Concierge system.

Prompts are treated as **version-controlled software artifacts** because changes to prompts can materially affect:

* Response quality
* Instruction following
* Retrieval usage
* Tool selection
* Output structure
* Safety
* Cost
* Latency

The objective is to make prompt changes reproducible, testable and traceable.

---

# 2. Prompt Versioning Overview

The prompt lifecycle is:

```text
Prompt Design
     ↓
Initial Version
     ↓
Local Testing
     ↓
Evaluation
     ↓
Version Registration
     ↓
Staging
     ↓
Production
     ↓
Monitoring
     ↓
Improvement
     ↓
New Version
```

---

# 3. What Is a Prompt Version?

A prompt version represents a specific, identifiable configuration of instructions provided to an LLM.

A prompt may include:

```text
System Instructions
Task Instructions
Output Requirements
Constraints
Context Instructions
Tool Instructions
Fallback Instructions
```

A meaningful change to any of these may require a new version.

---

# 4. Prompt Types

The system may contain several types of prompts.

## System Prompt

Defines the overall behavior and constraints of the assistant.

## Task Prompt

Defines how a specific task should be performed.

## RAG Prompt

Defines how retrieved context should be interpreted and used.

## Tool-Calling Prompt

Defines how the model should decide when and how to use tools.

## Evaluation Prompt

Defines instructions used by an evaluator model.

Each prompt type should be identifiable independently.

---

# 5. Prompt Naming

Prompts should use consistent identifiers.

Example:

```text
assistant-system
rag-answer
tool-selection
evaluation
```

Versions can then be associated with the prompt:

```text
assistant-system-v1
assistant-system-v2

rag-answer-v1
rag-answer-v2
```

---

# 6. Version Numbering

A simple versioning scheme may be:

```text
prompt-v1
prompt-v2
prompt-v3
```

For more detailed releases:

```text
prompt-v1.0.0
prompt-v1.1.0
prompt-v2.0.0
```

Semantic versioning may be used when prompt changes have clearly defined compatibility implications.

---

# 7. Major Prompt Changes

A major version should be considered when the prompt behavior changes substantially.

Examples:

```text
v1 → v2
```

Potential reasons include:

* New task strategy
* Major instruction restructuring
* Significant change in output behavior
* New tool-use strategy
* Major change in safety instructions

---

# 8. Minor Prompt Changes

A minor version may represent an improvement that preserves the overall behavior.

Example:

```text
v1.0 → v1.1
```

Possible changes:

* Clarifying instructions
* Improved wording
* Additional examples
* Small formatting improvements

The change should still be evaluated before deployment.

---

# 9. Patch Prompt Changes

A patch version may represent a small correction.

Example:

```text
v1.1.0 → v1.1.1
```

Examples include:

* Typographical correction
* Formatting correction
* Minor ambiguity fix

Even small changes should be evaluated when they could influence model behavior.

---

# 10. Prompt Metadata

Each prompt version should have metadata.

Recommended fields:

```text
Prompt ID
Version
Purpose
Prompt Type
Associated Model
Author
Created At
Status
Change Description
Evaluation Version
```

---

# 11. Prompt Content

The actual prompt content should be stored in a controlled and versioned location.

A conceptual structure is:

```text
prompts/
├── assistant/
│   ├── v1
│   └── v2
│
├── rag/
│   ├── v1
│   └── v2
│
└── tools/
    ├── v1
    └── v2
```

The exact implementation structure can be finalized during development.

---

# 12. Prompt and Git

Prompt source files should be version-controlled where appropriate.

A Git commit should make it possible to determine:

```text
Application Version
Prompt Version
Code Changes
Configuration Changes
```

Prompt changes should therefore follow the project's normal review workflow.

---

# 13. Prompt Change Workflow

The recommended workflow is:

```text
Prompt Change
      ↓
Local Testing
      ↓
Evaluation Dataset
      ↓
Baseline Comparison
      ↓
Review
      ↓
Version
      ↓
Staging
      ↓
Production
```

A prompt should not be modified directly in production without an appropriate validation process.

---

# 14. Baseline Prompt

A stable prompt should serve as the baseline.

```text
Baseline Prompt
      ↓
Candidate Prompt
      ↓
Evaluation
      ↓
Comparison
```

The candidate should demonstrate acceptable behavior relative to the baseline.

---

# 15. Prompt Evaluation Dataset

Prompt changes should be evaluated using representative test cases.

A dataset may contain:

```text
Input
Expected Behavior
Reference Answer
Evaluation Criteria
Category
```

The dataset should contain both common and difficult cases.

---

# 16. Prompt Regression Testing

Prompt regression testing verifies that an improvement in one scenario does not cause unexpected degradation elsewhere.

```text
Prompt v1
   ↓
Regression Dataset
   ↓
Results

Prompt v2
   ↓
Same Regression Dataset
   ↓
Results
   ↓
Comparison
```

A new prompt should not be promoted solely because it performs better on one example.

---

# 17. Prompt Evaluation Metrics

Depending on the task, evaluation may consider:

```text
Correctness
Relevance
Instruction Following
Groundedness
Consistency
Safety
Output Format
Tool Selection
```

For RAG applications, retrieval-related metrics may also be evaluated separately.

---

# 18. Prompt and Model Association

Prompt behavior depends partly on the model receiving it.

Therefore, record the model used during evaluation.

```text
Prompt v3
    +
Model A
    ↓
Evaluation Result
```

A prompt that performs well with one model may not behave identically with another.

---

# 19. Prompt and Model Compatibility

When changing the model:

```text
Model A
    ↓
Model B
```

existing prompts should be re-evaluated.

The workflow is:

```text
Existing Prompt
      ↓
New Model
      ↓
Regression Evaluation
      ↓
Compatibility Decision
```

---

# 20. Prompt and RAG Association

RAG prompts depend on the structure and quality of retrieved context.

Relevant variables include:

```text
Retrieved Documents
Chunk Structure
Metadata
Context Ordering
Citation Format
Retrieval Strategy
```

A RAG prompt should therefore be evaluated when the retrieval pipeline changes significantly.

---

# 21. Prompt and Memory Association

If the prompt uses memory:

```text
Memory
   ↓
Prompt Construction
   ↓
LLM
```

Changes to memory formatting or selection can affect prompt behavior.

Therefore, prompt evaluation should include representative memory scenarios when memory is part of the system.

---

# 22. Prompt and Tool Association

Tool-using prompts should be evaluated for:

```text
Tool Selection
Argument Generation
Tool Ordering
Error Handling
Termination
```

Example flow:

```text
User Request
     ↓
Prompt
     ↓
LLM
     ↓
Tool Decision
     ↓
Tool
```

A prompt change that modifies tool-selection behavior should be treated as a potentially significant release.

---

# 23. Structured Output Prompts

When a prompt requires structured output, the expected schema should be explicitly defined.

Conceptually:

```text
Prompt
  ↓
LLM
  ↓
Structured Output
  ↓
Schema Validation
```

If the output does not satisfy the schema:

```text
Invalid Output
     ↓
Retry / Repair
     ↓
Validation
```

The retry mechanism should be bounded.

---

# 24. Prompt Templates

Reusable prompts should use templates rather than duplicating similar instructions throughout the application.

Conceptually:

```text
Template
   +
Variables
   ↓
Rendered Prompt
```

Example variables may include:

```text
User Query
Retrieved Context
Conversation Summary
Tool Results
```

The template itself should be versioned.

---

# 25. Variable Validation

Variables inserted into prompts should be validated before prompt construction.

```text
Input
 ↓
Validation
 ↓
Prompt Template
 ↓
Rendered Prompt
```

This reduces the possibility of malformed context being passed to the model.

---

# 26. Context Ordering

The order of prompt components can influence model behavior.

A prompt may conceptually contain:

```text
System Instructions
       ↓
Task Instructions
       ↓
Retrieved Context
       ↓
Memory
       ↓
User Input
```

The exact ordering should be documented and evaluated rather than changed arbitrarily.

---

# 27. Prompt Injection Considerations

User input and retrieved documents should be treated as potentially untrusted content.

The system should distinguish:

```text
Trusted Instructions
        ↓
System / Application Logic

Untrusted Content
        ↓
User Input / Retrieved Content
```

Prompt changes should be tested against representative prompt-injection scenarios.

---

# 28. Prompt Safety Evaluation

Prompt evaluation should include safety-related cases where applicable.

Potential tests include:

```text
Unsafe Requests
Instruction Conflicts
Prompt Injection
Sensitive Information Requests
Tool Abuse Attempts
```

The purpose is to verify that the prompt continues to enforce the intended behavior.

---

# 29. Prompt Cost Considerations

Prompt length contributes to input-token usage.

A larger prompt may increase:

```text
Input Tokens
Latency
Cost
Context Usage
```

Prompt optimization should therefore consider both quality and efficiency.

The objective is not necessarily to create the shortest prompt, but to achieve the required behavior efficiently.

---

# 30. Prompt Latency

Longer prompts can increase processing time.

Latency should be evaluated when prompt changes significantly increase:

```text
System Instructions
Examples
Retrieved Context
Conversation History
```

Prompt optimization should consider the complete end-to-end latency.

---

# 31. Few-Shot Examples

Prompts may contain examples to guide model behavior.

Conceptually:

```text
Instructions
     ↓
Example 1
Example 2
Example 3
     ↓
User Input
```

Examples should be:

* Relevant
* Representative
* Correct
* Consistent with expected behavior

Examples should be version-controlled as part of the prompt.

---

# 32. Prompt Testing Categories

A regression dataset should ideally cover:

```text
Normal Cases
Edge Cases
Ambiguous Cases
Out-of-Scope Cases
Failure Cases
Safety Cases
Tool-Calling Cases
RAG Cases
```

This provides broader coverage than testing only common requests.

---

# 33. Prompt Comparison

Two prompt versions can be compared using the same evaluation set.

```text
                 Evaluation Dataset
                        │
             ┌──────────┴──────────┐
             ↓                     ↓
         Prompt v1             Prompt v2
             ↓                     ↓
        Evaluation              Evaluation
             │                     │
             └──────────┬──────────┘
                        ↓
                    Comparison
```

The comparison should consider multiple relevant metrics.

---

# 34. Prompt Promotion

The recommended lifecycle is:

```text
Draft
 ↓
Experimental
 ↓
Candidate
 ↓
Validated
 ↓
Staging
 ↓
Production
 ↓
Deprecated
```

Each transition should have defined criteria.

---

# 35. Prompt Status

Recommended statuses are:

```text
Draft
Experimental
Candidate
Validated
Staging
Production
Deprecated
Archived
```

The status should make it clear whether a prompt is safe for production use.

---

# 36. Production Prompt

The production prompt should be explicitly identifiable.

For example:

```text
assistant-system
Active Version: v3
Status: Production
```

The application should not depend on an ambiguous "latest prompt" reference without controlled version resolution.

---

# 37. Prompt Rollback

If a new prompt causes degradation:

```text
Production Prompt v4
        ↓
Issue Detected
        ↓
Rollback
        ↓
Prompt v3
        ↓
Monitoring
```

The previous stable version should remain available for rollback.

---

# 38. Prompt Release Record

A production AI release should identify:

```text
Application Version
Model Version
Prompt Version
RAG Version
Evaluation Version
Deployment Environment
```

Example:

```text
Application: v2.3.0
Model: model-v4
Prompt: assistant-system-v3
RAG: rag-v2
Evaluation: evaluation-v6
Environment: production
```

This creates a traceable AI configuration.

---

# 39. Prompt Monitoring

Prompt changes should be monitored after deployment.

Monitor relevant signals such as:

```text
Quality
Error Rate
Tool Failures
Latency
Token Usage
Cost
User Feedback
```

Unexpected degradation should trigger investigation.

---

# 40. Prompt Drift

Prompt drift can occur when other system components change.

Potential causes include:

```text
Model Change
RAG Change
Memory Change
Tool Change
Application Change
Provider Change
```

Therefore, a prompt should be periodically re-evaluated when its surrounding system changes significantly.

---

# 41. Prompt Retirement

A prompt may be retired when:

* It is replaced by a newer version.
* The associated model is retired.
* The task is removed.
* The architecture changes.
* It no longer satisfies quality requirements.

Retirement workflow:

```text
Production
   ↓
Replacement Validated
   ↓
New Prompt Deployed
   ↓
Old Prompt Deprecated
   ↓
Archived
```

---

# 42. Prompt Audit Trail

Important prompt events should be recorded:

```text
Prompt Created
Prompt Modified
Prompt Evaluated
Prompt Approved
Prompt Deployed
Prompt Rolled Back
Prompt Deprecated
Prompt Archived
```

Each event should ideally record:

```text
Version
Timestamp
Change
Environment
Result
```

---

# 43. Prompt Security

Prompt files and configurations should be protected from unauthorized modification.

Security controls should include:

```text
Access Control
Code Review
Version Control
Secret Separation
Change Tracking
```

Secrets should never be embedded directly into prompts.

---

# 44. Prompt Documentation

Each important production prompt should have documentation describing:

```text
Purpose
Expected Inputs
Expected Behavior
Output Format
Associated Model
Dependencies
Evaluation Criteria
Known Limitations
```

This helps developers understand the prompt without reading implementation details alone.

---

# 45. Prompt Change Record

For significant changes, record:

```text
Version:
Previous Version:
Reason:
Changes:
Expected Improvement:
Evaluation:
Result:
Decision:
```

Example:

```text
Version: v2
Previous Version: v1

Reason:
Improve instruction following.

Changes:
Clarified task boundaries and output requirements.

Evaluation:
Regression evaluation completed.

Result:
Accepted.

Decision:
Promote to staging.
```

---

# 46. Prompt Versioning Workflow

The complete workflow is:

```text
Requirement
    ↓
Prompt Design
    ↓
Draft
    ↓
Local Testing
    ↓
Evaluation
    ↓
Candidate Version
    ↓
Regression Testing
    ↓
Validation
    ↓
Version Registration
    ↓
Staging
    ↓
Production
    ↓
Monitoring
    ↓
Feedback
    ↓
Next Version
```

---

# 47. Prompt Versioning Checklist

Before promoting a prompt:

```text
☐ Prompt purpose documented
☐ Version assigned
☐ Changes documented
☐ Associated model identified
☐ Variables validated
☐ Regression tests passed
☐ Safety cases evaluated
☐ RAG behavior evaluated where applicable
☐ Tool behavior evaluated where applicable
☐ Cost considered
☐ Latency considered
☐ Version registered
☐ Staging validation completed
☐ Rollback version available
```

---

# 48. Relationship With Other MLOps Documents

Prompt versioning connects directly with:

```text
docs/mlops/MLOps_Pipeline.md
docs/mlops/LLMOps.md
docs/mlops/CI_CD.md
docs/mlops/Model_Versioning.md
docs/mlops/Monitoring_AI.md
docs/mlops/Evaluation_Framework.md
```

It also interacts with:

```text
docs/system_design/RAG_Design.md
docs/system_design/Memory_Architecture.md
docs/system_design/Agent_Design.md
```

---

# 49. Final Prompt Versioning Principles

The project follows these principles:

1. **Treat prompts as version-controlled artifacts.**
2. **Give every production prompt an explicit version.**
3. **Evaluate prompt changes before deployment.**
4. **Maintain a regression dataset for important behaviors.**
5. **Associate prompts with the model and AI configuration used with them.**
6. **Test prompts with RAG, memory and tools when applicable.**
7. **Consider quality, latency and cost together.**
8. **Protect prompts and configurations from unauthorized changes.**
9. **Maintain rollback capability.**
10. **Record significant prompt changes and their evaluation results.**
11. **Avoid relying on uncontrolled "latest" prompt behavior in production.**
12. **Continuously improve prompts using measured production feedback.**

The goal is to make prompt behavior as traceable and manageable as application code and model artifacts.
