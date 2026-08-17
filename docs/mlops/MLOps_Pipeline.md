# MLOps Pipeline

## 1. Purpose

This document defines the MLOps pipeline for the AI Concierge project.

The purpose of the pipeline is to establish a structured lifecycle for:

* Data
* Models
* Experiments
* Evaluation
* Deployment
* Monitoring
* Versioning
* Continuous improvement

The pipeline should make ML and AI components reproducible, testable and maintainable as the project evolves.

---

# 2. MLOps Overview

The overall lifecycle is:

```text
Data
  ↓
Data Validation
  ↓
Preprocessing
  ↓
Experimentation
  ↓
Model Development
  ↓
Evaluation
  ↓
Model / Prompt Validation
  ↓
Versioning
  ↓
Deployment
  ↓
Monitoring
  ↓
Feedback
  ↓
Improvement
```

This lifecycle applies to ML components as well as AI components that require systematic evaluation and version control.

---

# 3. MLOps Architecture

The high-level MLOps architecture is:

```text
                    Data Sources
                         │
                         ▼
                  Data Processing
                         │
                         ▼
                  Data Validation
                         │
                         ▼
                  Experimentation
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        Model Training        Prompt / LLM
              │                 Development
              └──────────┬──────────┘
                         ▼
                    Evaluation
                         │
                         ▼
                     Versioning
                         │
                         ▼
                    Deployment
                         │
                         ▼
                    Monitoring
                         │
                         ▼
                     Feedback
                         │
                         └──────────► Improvement
```

---

# 4. MLOps Goals

The pipeline should provide:

### Reproducibility

An experiment should be reproducible using the recorded configuration, data and model versions.

### Traceability

The deployed model or AI configuration should be traceable to its source artifacts.

### Reliability

Changes should pass appropriate validation before deployment.

### Automation

Repeated processes should gradually be automated through CI/CD and pipeline orchestration.

### Observability

Production behavior should be measurable.

### Continuous Improvement

Evaluation and monitoring results should feed future development.

---

# 5. ML Lifecycle

The ML lifecycle consists of:

```text
Problem Definition
      ↓
Data Collection
      ↓
Data Preparation
      ↓
Experimentation
      ↓
Training / Adaptation
      ↓
Evaluation
      ↓
Model Selection
      ↓
Deployment
      ↓
Monitoring
      ↓
Retraining / Improvement
```

Not every AI component requires model training.

For example, an LLM-based component may involve:

```text
Model Selection
     ↓
Prompt Development
     ↓
RAG Configuration
     ↓
Evaluation
     ↓
Deployment
```

---

# 6. Data Pipeline

The data pipeline prepares data for ML and AI components.

```text
Raw Data
   ↓
Ingestion
   ↓
Validation
   ↓
Cleaning
   ↓
Transformation
   ↓
Dataset Version
   ↓
Training / Evaluation
```

Data processing should be reproducible.

---

# 7. Data Ingestion

Data may originate from:

* Documents
* Structured datasets
* Application events
* Evaluation datasets
* External sources
* Human feedback

The ingestion process should record sufficient metadata to identify:

```text
Source
Timestamp
Version
Processing status
Data format
```

---

# 8. Data Validation

Before data is used, validate:

```text
Schema
Completeness
Data types
Missing values
Duplicates
Invalid records
Unexpected distributions
```

For text data, additional checks may include:

```text
Encoding
Language
Text length
Empty documents
Duplicate documents
Malformed content
```

---

# 9. Data Preprocessing

Typical preprocessing may include:

```text
Raw Data
   ↓
Cleaning
   ↓
Normalization
   ↓
Filtering
   ↓
Transformation
   ↓
Final Dataset
```

Preprocessing should be deterministic where possible.

Any transformation that affects model behavior should be version-controlled.

---

# 10. Dataset Versioning

Datasets should be identifiable by version.

Example:

```text
dataset-v1
dataset-v2
dataset-v3
```

A dataset version should ideally identify:

```text
Dataset Version
Source
Processing Pipeline Version
Creation Date
Schema Version
```

This makes it possible to determine which data produced a particular experiment.

---

# 11. Train / Validation / Test Data

Where supervised ML training is used, data should generally be separated into:

```text
Dataset
  │
  ├── Training
  ├── Validation
  └── Test
```

The test set should not be repeatedly used for model tuning.

For LLM and RAG evaluation, separate evaluation datasets may be used instead of traditional train/validation/test splits.

---

# 12. Experimentation

Experiments should be treated as measurable engineering activities.

Each experiment should record:

```text
Experiment ID
Objective
Dataset Version
Model Version
Configuration
Hyperparameters
Prompt Version
Evaluation Metrics
Results
Conclusion
```

Example:

```text
Experiment
   ↓
Change one or more controlled variables
   ↓
Run evaluation
   ↓
Record results
   ↓
Compare against baseline
```

---

# 13. Experiment Tracking

Experiment tracking should make it possible to answer:

> What was changed, and what effect did it have?

Track relevant parameters such as:

```text
Model
Dataset
Embedding Model
Chunk Size
Top-K
Reranker
Prompt Version
Generation Parameters
Evaluation Dataset
Metrics
```

The exact experiment-tracking platform may be selected later.

---

# 14. Baselines

Every major experiment should have a baseline where practical.

```text
Baseline
   ↓
Experiment A
   ↓
Experiment B
   ↓
Experiment C
```

The baseline provides a reference point for determining whether a change actually improves the system.

---

# 15. Model Development

For trainable models, the model-development lifecycle is:

```text
Dataset
   ↓
Training
   ↓
Validation
   ↓
Evaluation
   ↓
Model Candidate
```

The model candidate should not be deployed until it satisfies the project's evaluation requirements.

---

# 16. Model Selection

Model selection should consider more than accuracy.

Possible criteria include:

```text
Quality
Latency
Cost
Memory Requirements
Throughput
Robustness
Security
Availability
```

For AI systems, additional criteria may include:

```text
Groundedness
Faithfulness
Instruction Following
Tool-use Reliability
Safety
```

The selected model should be documented.

---

# 17. LLM Development

For LLM-based functionality, the development lifecycle may be:

```text
Use Case
   ↓
Model Selection
   ↓
Prompt Design
   ↓
Context / RAG Design
   ↓
Tool Integration
   ↓
Evaluation
   ↓
Versioning
   ↓
Deployment
```

LLMOps is documented separately in:

```text
docs/mlops/LLMOps.md
```

---

# 18. RAG Pipeline Integration

RAG should be treated as part of the ML/AI lifecycle.

```text
Documents
   ↓
Ingestion
   ↓
Chunking
   ↓
Embedding
   ↓
Indexing
   ↓
Retrieval
   ↓
Reranking
   ↓
Context
   ↓
LLM
```

Changes to any retrieval component may affect final system quality and should therefore be evaluated.

---

# 19. Evaluation Gate

Before deployment:

```text
Candidate
    ↓
Evaluation
    │
    ├── Pass → Version → Deploy
    │
    └── Fail → Iterate
```

Evaluation should use predefined criteria rather than subjective judgment alone.

The detailed evaluation strategy is documented under:

```text
docs/mlops/Evaluation_Framework.md
```

---

# 20. Model Versioning

Every production model should be identifiable.

Example:

```text
model-v1
model-v2
model-v3
```

Model metadata may include:

```text
Model Version
Base Model
Training Data Version
Configuration
Evaluation Results
Creation Date
Deployment Status
```

Detailed model-versioning practices are documented in:

```text
docs/mlops/Model_Versioning.md
```

---

# 21. Prompt Versioning

Prompts can materially affect system behavior.

Therefore prompts should be version-controlled.

Example:

```text
prompt-v1
prompt-v2
prompt-v3
```

A prompt version may record:

```text
Prompt ID
Version
Purpose
Model
Changes
Evaluation Results
Status
```

Detailed practices are documented in:

```text
docs/mlops/Prompt_Versioning.md
```

---

# 22. Deployment Pipeline

The MLOps deployment flow is:

```text
Validated Artifact
       ↓
Version Registration
       ↓
Build
       ↓
Staging
       ↓
Evaluation
       ↓
Production
       ↓
Monitoring
```

Deployment should be integrated with the broader application deployment process.

---

# 23. CI/CD Integration

CI/CD should automate repetitive validation.

A typical pipeline:

```text
Git Change
    ↓
CI
 ├── Tests
 ├── Lint
 ├── Type Checks
 ├── Build
 ├── Evaluation
 └── Security Checks
    ↓
Approval
    ↓
Deployment
```

The detailed workflow is documented in:

```text
docs/mlops/CI_CD.md
```

---

# 24. Model Deployment

Model deployment may follow:

```text
Model Candidate
      ↓
Validation
      ↓
Model Registry
      ↓
Deployment Artifact
      ↓
Serving Infrastructure
      ↓
Inference
```

The serving infrastructure depends on the selected deployment architecture.

---

# 25. AI Service Deployment

When using external LLM services, the deployment artifact may consist of:

```text
Model Identifier
Prompt Version
System Configuration
RAG Configuration
Tool Configuration
Generation Parameters
```

This configuration should be version-controlled so that production behavior remains traceable.

---

# 26. Monitoring

After deployment, monitor both system and AI behavior.

### System metrics

```text
Latency
Throughput
CPU
Memory
Errors
Availability
```

### AI metrics

```text
Response Quality
Token Usage
Model Latency
Retrieval Quality
Hallucination Indicators
Tool Failures
Evaluation Scores
```

AI monitoring is documented in:

```text
docs/mlops/Monitoring_AI.md
```

---

# 27. Feedback Loop

Production feedback should feed future development.

```text
Production
    ↓
Monitoring
    ↓
Issues / Feedback
    ↓
Analysis
    ↓
Experiment
    ↓
Evaluation
    ↓
Improved Version
    ↓
Deployment
```

This creates a continuous improvement cycle.

---

# 28. Model Drift

Model behavior can degrade when the environment changes.

Potential causes include:

```text
Data Distribution Change
User Behavior Change
Document Changes
Query Distribution Change
External Model Changes
```

Drift monitoring should be introduced when sufficient production data becomes available.

---

# 29. Data Drift

Data drift occurs when incoming data differs significantly from the data used during development.

Example:

```text
Development Data
       ↓
Production Data
       ↓
Distribution Comparison
       ↓
Potential Drift
```

Drift detection should use measurable statistical or domain-specific criteria.

---

# 30. Performance Monitoring

Performance should be monitored continuously.

Important measurements include:

```text
Request Latency
Retrieval Latency
LLM Latency
End-to-End Latency
Token Consumption
Cost Per Request
Throughput
```

Performance changes should be compared against established baselines.

---

# 31. Cost Monitoring

AI systems may incur variable costs.

Potential cost drivers include:

```text
LLM Tokens
Embedding Generation
Model Inference
Vector Storage
Database Usage
Compute
Network
```

Cost should be monitored alongside quality.

A higher-quality model is not automatically preferable if the improvement is insignificant relative to its additional operational cost.

---

# 32. Reproducibility

A production result should ideally be traceable to:

```text
Code Version
Dataset Version
Model Version
Prompt Version
RAG Configuration
Dependency Version
Environment
Evaluation Version
```

This allows an issue to be reproduced or investigated.

---

# 33. Rollback

If a deployed model or AI configuration causes unacceptable degradation:

```text
Current Version
      ↓
Monitoring Detects Issue
      ↓
Rollback Decision
      ↓
Previous Stable Version
      ↓
Validation
      ↓
Monitoring
```

Rollback should be possible without permanently losing the newer candidate.

---

# 34. Continuous Improvement

The long-term MLOps cycle is:

```text
                    ┌──────────────┐
                    │ Development  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Evaluation   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ Deployment   │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Monitoring  │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Feedback   │
                    └──────┬───────┘
                           │
                           └──────────► Development
```

The system should improve through controlled iteration rather than uncontrolled production experimentation.

---

# 35. MLOps Maturity

The project can gradually evolve through several stages.

## Stage 1 — Manual Development

```text
Manual Experiments
Manual Evaluation
Manual Deployment
```

## Stage 2 — Reproducible Development

```text
Versioned Data
Versioned Models
Versioned Prompts
Recorded Experiments
```

## Stage 3 — Automated Validation

```text
CI
Automated Tests
Automated Evaluation
Automated Builds
```

## Stage 4 — Automated Deployment

```text
CI/CD
Staging
Deployment Automation
Rollback
```

## Stage 5 — Continuous Monitoring

```text
Monitoring
Drift Detection
Quality Evaluation
Cost Monitoring
Feedback Loop
```

The project should progress through these stages incrementally.

---

# 36. Recommended MLOps Workflow

The complete workflow is:

```text
                    Git Change
                        ↓
                 Data / Code / Prompt
                        ↓
                  Experimentation
                        ↓
                     Testing
                        ↓
                   Evaluation
                        ↓
                  Version Artifact
                        ↓
                    CI Pipeline
                        ↓
                     Staging
                        ↓
               Production Validation
                        ↓
                    Deployment
                        ↓
                    Monitoring
                        ↓
                     Feedback
                        ↓
                   Improvement
```

---

# 37. Responsibilities

MLOps responsibilities may span multiple areas.

### Development

Responsible for:

* Implementation
* Experiments
* Tests
* Documentation

### ML / AI

Responsible for:

* Model selection
* Experimentation
* Evaluation
* Model configuration

### Infrastructure

Responsible for:

* Compute
* Deployment
* Networking
* Storage
* Monitoring

### CI/CD

Responsible for:

* Automated validation
* Build
* Release
* Deployment automation

As the project grows, these responsibilities may be separated among different roles.

---

# 38. MLOps Artifacts

Important artifacts include:

```text
Datasets
Models
Model Configurations
Prompts
Embeddings
Evaluation Datasets
Evaluation Results
Experiment Metadata
Container Images
Deployment Configurations
Monitoring Data
```

Artifacts should be versioned or otherwise traceable according to their importance.

---

# 39. Security in MLOps

MLOps processes should protect:

```text
Training Data
Evaluation Data
Model Artifacts
API Keys
Credentials
User Data
Production Logs
```

Security controls should be applied throughout:

```text
Data
 ↓
Training
 ↓
Evaluation
 ↓
Artifact Storage
 ↓
Deployment
 ↓
Monitoring
```

Security requirements are further described in:

```text
docs/system_design/Security.md
```

---

# 40. Final MLOps Principles

The AI Concierge MLOps pipeline follows these principles:

1. **Version everything important.**
2. **Make experiments reproducible.**
3. **Evaluate before deployment.**
4. **Separate experimentation from production.**
5. **Automate repetitive validation.**
6. **Monitor both system and AI behavior.**
7. **Track model, prompt and data versions.**
8. **Measure quality and cost together.**
9. **Maintain rollback capability.**
10. **Use production feedback for controlled improvement.**
11. **Protect data, models and credentials.**
12. **Increase automation gradually as the project matures.**

The goal is to establish an MLOps foundation that can support the AI Concierge from experimentation through reliable, monitored production deployment.
