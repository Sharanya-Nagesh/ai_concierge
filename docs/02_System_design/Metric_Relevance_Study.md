# Metric Relevance Study

## 1. Study information

| Item | Description |
|---|---|
| Project | End-to-End, Production-Ready AI Concierge System for Multilingual, Personalized Learning, Planning & Productivity |
| Research focus | Preference updates and stale-memory handling |
| Research question | Does explicit preference-update and supersession logic reduce stale-memory usage and improve personalization accuracy compared with conventional top-k vector-based memory retrieval? |
| Study type | Metric selection and evaluation-design study |
| Status | Initial draft — definitions and protocol to be validated before the main experiment |

## 2. Purpose

This document identifies metrics that measure whether a preference-aware memory controller improves how an AI Concierge handles changing user preferences.

Example:
1. A user says, “I prefer short explanations.”
2. Later, the user says, “From now on, explain concepts in detail.”
3. The user asks, “Explain transformers.”

A conventional top-k vector retrieval system may retrieve both statements. The response may follow the old preference, combine them inconsistently, or fail to reflect the latest instruction.

The proposed approach will explicitly represent preference updates and determine which preference is currently applicable before response generation. This study defines how to evaluate the approaches; it does not assume the proposed approach will perform better.

## 3. Systems being compared

### 3.1 Baseline: conventional top-k vector memory

1. Receive the user's message.
2. Generate an embedding.
3. Retrieve the top-k semantically similar memories.
4. Add retrieved memories to the prompt.
5. Generate the response.

There is no dedicated preference-supersession mechanism. If older and newer preference statements are both retrieved, the language model must interpret them from the supplied context.

### 3.2 Proposed: preference-aware memory controller

The proposed system will investigate a controller that:

1. Identifies preference statements and update intent.
2. Extracts a preference key and value.
3. Determines scope, such as global or task-specific.
4. Represents temporal validity where applicable.
5. Detects explicit corrections and conflicts.
6. Marks a superseded preference as inactive while retaining its history.
7. Retrieves memories that are active and applicable to the current request.
8. Supplies the selected memories to the language model.

This is a proposed experimental design, not a claim about the current implementation.

## 4. Metric selection criteria

A metric is relevant when it measures an outcome directly connected to the research question, can be calculated from collected experiment data, and supports a fair comparison.

Metrics are grouped into:
- **Primary:** directly evaluate preference updates and stale-memory handling.
- **Supporting:** explain memory retrieval quality.
- **Operational:** measure efficiency and practical feasibility.

## 5. Primary metrics

### 5.1 Stale-memory use rate

**Purpose:** Measures how often an answer is influenced by a preference that has been superseded or has expired.

\[
\text{Stale-memory use rate} =
\frac{\text{Risk probes where stale memory influenced the answer}}
{\text{Risk probes where stale memory could be retrieved}}
\times 100
\]

**Why relevant:** Reducing the use of outdated preferences is a central objective of the research question.

**Data required:** risk-probe ID, stale preference in history, whether it was retrieved, whether it influenced the response, and annotation evidence.

**Direction:** Lower is better.

**Important distinction:** Retrieving a stale memory does not necessarily mean the final answer used it. Record retrieval and answer influence separately. Define “influenced” in the annotation guide before evaluating outputs.

### 5.2 Current-preference accuracy

**Purpose:** Measures whether the response follows the active preference, including its scope and validity.

\[
\text{Current-preference accuracy} =
\frac{\text{Probes where the response follows the active preference}}
{\text{Probes with a clearly defined active preference}}
\times 100
\]

**Why relevant:** A system may avoid old preferences but still fail to apply the correct current preference.

**Data required:** expected active preference, scope and validity, system response, and correctness judgement with reason.

**Direction:** Higher is better.

### 5.3 Preference update accuracy

**Purpose:** Measures whether the system correctly handles an update instruction and identifies the preference that should become active.

\[
\text{Preference update accuracy} =
\frac{\text{Update scenarios resolved correctly}}
{\text{Total evaluable update scenarios}}
\times 100
\]

A scenario is resolved correctly when the system recognizes the update, applies it to the correct preference key, preserves scope, supersedes the previous value when replacement is clear, and does not overwrite unrelated preferences.

**Why relevant:** Explicit update and supersession handling is the proposed controller's central mechanism.

**Data required:** update instruction, previous preference, expected active preference, stored state after processing, and correctness judgement.

**Direction:** Higher is better.

## 6. Supporting retrieval metrics

### 6.1 Retrieval precision

\[
\text{Precision} =
\frac{\text{Relevant eligible memories retrieved}}
{\text{All memories retrieved}}
\]

Measures the proportion of retrieved memories that are relevant and eligible for the current query. Higher is better.

### 6.2 Retrieval recall

\[
\text{Recall} =
\frac{\text{Relevant eligible memories retrieved}}
{\text{All relevant eligible memories}}
\]

Measures the proportion of all relevant, eligible memories successfully retrieved. Higher is better.

A system may have high precision by retrieving very few memories; recall checks whether useful active preferences are being missed. Define relevance and eligibility using a labelled gold set. Superseded or expired preferences should not count as eligible for a query where they no longer apply.

## 7. Operational metrics

### 7.1 Response latency

\[
\text{Latency} = t_{\text{response complete}} - t_{\text{request received}}
\]

Record measurement boundaries and whether embedding, memory retrieval, and model generation are included. Lower is better, provided quality is not sacrificed.

### 7.2 Token usage and API cost

Record input tokens, output tokens, embedding tokens or requests where applicable, number of model calls, and estimated provider cost at experiment time. This measures the operational overhead of the proposed controller.

## 8. Metric priority

| Metric | Priority | Connection to the research question |
|---|---|---|
| Stale-memory use rate | Primary | Directly measures stale-memory influence |
| Current-preference accuracy | Primary | Measures correct use of the active preference |
| Preference update accuracy | Primary | Measures update and supersession correctness |
| Retrieval precision | Supporting | Measures relevance of retrieved memories |
| Retrieval recall | Supporting | Measures coverage of eligible memories |
| Response latency | Operational | Measures time overhead |
| Token usage/API cost | Operational | Measures cost overhead |

The primary metrics determine whether the proposed method addresses the research problem. Supporting and operational metrics explain trade-offs.

## 9. Initial experiment scenarios

| Category | Scenario | Expected behaviour |
|---|---|---|
| Stable preference | User repeatedly expresses the same preference | Preserve and apply it |
| Explicit update | “Use short answers” followed by “From now on, use detailed answers” | Make the newer preference active |
| Contradictory preference | Two different values for the same preference without clear update intent | Do not silently assume which wins; apply a defined conflict policy |
| Temporary preference | “Keep answers short today” | Apply only within the stated validity period |
| Scope-specific preference | “Use detailed explanations for NLP, but short answers for general questions” | Apply the preference for the relevant scope |

For the initial pilot, prepare approximately 10–15 scenarios per category (50–75 total). This is for testing the protocol and implementation, not a claim that the dataset is large enough for definitive publication-level conclusions.

Each scenario should specify conversation history, preference key/value, instruction type, expected active preference, superseded or expired preferences, test query, expected behaviour, and applicable metrics.

## 10. Fair comparison protocol

1. Use the same scenario histories and queries for both systems.
2. Keep the language model and model version the same.
3. Keep generation settings and system-level response instructions the same.
4. Keep embedding model and vector-store settings the same where applicable.
5. Define and report the memory-context or prompt-token budget.
6. Record retrieved memories and final responses, not only aggregate scores.
7. Use the same annotation guide for both systems.
8. Blind annotators to system identity where practical.
9. Report scenario counts and excluded or unscorable cases.
10. Preserve raw outputs and experiment configuration for reproducibility.

The proposed controller may use structured metadata unavailable to the baseline; that is part of the intervention. Other differences should be controlled or documented.

## 11. Analysis plan

Because both systems are evaluated on the same scenarios, the comparison is paired.

Report baseline and proposed scores for each primary metric, absolute differences, scenario-level disagreements, confidence intervals where appropriate, and error categories with representative failures.

For binary outcomes, such as whether an update was handled correctly, McNemar's test may be appropriate because the same scenarios are evaluated by both systems. If discordant pairs are few, consider the exact version rather than relying only on the asymptotic chi-square approximation.

Do not make statistical-significance claims from the pilot alone without checking sample size and test assumptions.

## 12. Threats to validity and limitations

- **Annotation subjectivity:** Whether a memory influenced a response may not always be obvious. Use explicit annotation rules and, where feasible, independent annotators.
- **Dataset coverage:** A small pilot cannot represent all real user preference changes.
- **Language-model variability:** Record model identifiers and settings; repeat runs where appropriate.
- **Prompt sensitivity:** Control and report prompt budgets and instructions.
- **Synthetic scenario bias:** Hand-authored scenarios may be cleaner than real conversations. Treat the pilot as an initial evaluation.
- **Scope ambiguity:** If a user does not clarify whether a preference replaces a global preference or applies to one task, the system should not silently assume a broad update.
- **Temporal ambiguity:** Expressions such as “today,” “for this session,” and “from now on” require consistent validity rules.

## 13. Expected outputs

At the end of this study, the project should have:
1. A justified set of primary, supporting, and operational metrics.
2. Written scoring and annotation rules.
3. A pilot scenario specification.
4. A controlled comparison protocol.
5. A clear list of data to log during implementation and experiments.

This document defines the evaluation plan. It contains no experimental results and makes no claim that the proposed method is superior.

## 14. References to verify during the literature review

These related works can inform the design of preference-update and temporal-validity mechanisms. Verify the full papers and exact claims before using them to justify a novelty claim.

- PAMU, ACL Findings 2026: https://aclanthology.org/2026.findings-acl.38/
- Temporal Semantic Memory (TSM), ACL Findings 2026: https://aclanthology.org/2026.findings-acl.1496/
- Memora/FAMA, arXiv: https://arxiv.org/abs/2604.20006

The existence of related preference-update and temporal-memory work means the contribution must be framed narrowly and supported by a careful comparison, rather than claiming that preference updates in AI memory have not been studied.
