# Model Versioning

## 1. Purpose

This document defines the strategy for versioning, tracking, evaluating and managing ML and AI model artifacts used by the AI Concierge project.

The objective is to ensure that every deployed model can be traced back to:

* Its source model
* Relevant data
* Configuration
* Evaluation results
* Application version
* Deployment state

Model versioning is an essential part of reproducibility, rollback and continuous improvement.

---

# 2. Model Versioning Overview

The model lifecycle is:

```text
Model Selection
      ↓
Configuration
      ↓
Evaluation
      ↓
Model Version
      ↓
Validation
      ↓
Deployment
      ↓
Monitoring
      ↓
Improvement
      ↓
New Version
```

A new version should be created whenever a change can materially affect model behavior.

---

# 3. What Constitutes a Model Version

A model version may represent:

* A newly trained model
* A fine-tuned model
* A changed model configuration
* A changed embedding model
* A changed reranker
* A newly selected external LLM
* A model artifact with updated weights

For external LLM providers, the version should identify the provider's model identifier and relevant configuration.

---

# 4. Version Naming

A consistent naming scheme should be used.

Example:

```text
model-v1
model-v2
model-v3
```

For more detailed releases:

```text
model-v1.0.0
model-v1.1.0
model-v2.0.0
```

The exact versioning convention should remain consistent across the project.

---

# 5. Semantic Versioning

Where semantic versioning is appropriate:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

A major change that significantly changes behavior or compatibility.

Example:

```text
v1.0.0 → v2.0.0
```

### MINOR

A backward-compatible improvement.

Example:

```text
v1.0.0 → v1.1.0
```

### PATCH

A small correction or compatible change.

Example:

```text
v1.1.0 → v1.1.1
```

The project may use simpler version identifiers for experimental models.

---

# 6. Model Metadata

Each model version should have associated metadata.

Recommended metadata:

```text
Model ID
Version
Model Type
Base Model
Training / Adaptation Method
Dataset Version
Configuration Version
Created At
Evaluation Version
Status
Deployment Environment
```

For externally hosted models, also record:

```text
Provider
Provider Model Identifier
Provider Version Information
```

---

# 7. Model Lineage

Model lineage describes how a model was produced.

```text
Source Data
     ↓
Dataset Version
     ↓
Processing Version
     ↓
Training / Adaptation
     ↓
Model Version
     ↓
Evaluation
     ↓
Deployment
```

The lineage should allow engineers to determine the origin of a deployed model.

---

# 8. Dataset Association

A model should be associated with the dataset version used to produce it.

Example:

```text
Dataset
dataset-v3
      ↓
Training
      ↓
model-v2
```

This relationship should be recorded rather than relying on filenames alone.

---

# 9. Configuration Association

Model behavior can depend on configuration.

Relevant configuration may include:

```text
Hyperparameters
Tokenizer
Embedding Configuration
Generation Parameters
Quantization
Inference Configuration
```

The model version should identify the configuration used during evaluation and deployment.

---

# 10. Model Evaluation Association

A model should not be considered production-ready merely because it exists.

Its evaluation results should be associated with the model version.

```text
model-v3
    ↓
evaluation-v5
    ↓
Metrics
    ↓
Deployment Decision
```

This makes deployment decisions traceable.

---

# 11. Model Status

A model version can have a lifecycle status.

Recommended states:

```text
Experimental
Candidate
Validated
Staging
Production
Deprecated
Archived
```

Example:

```text
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
     ↓
Archived
```

---

# 12. Experimental Models

Experimental models are models under active development.

They may:

* Have incomplete evaluation
* Change frequently
* Be unsuitable for production
* Be used only for experimentation

Experimental models should not be treated as production artifacts.

---

# 13. Candidate Models

A candidate model has completed initial development and is ready for formal evaluation.

```text
Experimental
     ↓
Candidate
     ↓
Evaluation
```

A candidate may be promoted to `Validated` only after satisfying the relevant evaluation requirements.

---

# 14. Validated Models

A validated model has passed the project's required evaluation criteria.

Validation may include:

```text
Quality
Latency
Resource Usage
Reliability
Security
Compatibility
```

A validated model is eligible for staging.

---

# 15. Production Models

A production model is actively serving application traffic.

Only approved and validated model versions should be promoted to production.

The active production version should be clearly identifiable.

---

# 16. Deprecated Models

A deprecated model is no longer recommended for new deployments.

It may remain available temporarily for:

* Rollback
* Reproducibility
* Historical analysis
* Existing deployments

Deprecated models should eventually be archived according to retention requirements.

---

# 17. Archived Models

Archived models are retained for historical or compliance purposes but are no longer actively deployed.

An archived model should remain identifiable even if it is removed from active infrastructure.

---

# 18. Model Registry

A model registry provides a centralized record of model versions.

Conceptually:

```text
Model Registry
│
├── model-v1
├── model-v2
├── model-v3
└── model-v4
```

Each entry should contain metadata and references to associated artifacts.

The specific registry technology can be selected based on project infrastructure.

---

# 19. Registry Information

A registry entry may contain:

```text
Model Name
Version
Artifact Location
Dataset Version
Configuration
Evaluation Results
Status
Created At
Updated At
Deployment Information
```

---

# 20. Model Artifact Storage

Model artifacts may include:

```text
Model Weights
Tokenizer
Configuration
Metadata
Supporting Files
```

Artifacts should be stored in a reliable location with controlled access.

Large model files should generally not be stored directly in the normal Git source repository.

---

# 21. Git and Model Artifacts

Git should track:

```text
Source Code
Configuration
Model Metadata
Version References
```

Large binary model artifacts should use an appropriate artifact-storage or model-versioning mechanism.

The repository should contain enough information to identify which model artifact belongs to a particular release.

---

# 22. Model Version and Git Commit

A model deployment should ideally be traceable to the application commit that uses it.

Example:

```text
Application
commit: abc123

Model
model-v4

Evaluation
evaluation-v7
```

This provides a complete release reference.

---

# 23. Model Version and Prompt Version

For LLM-based applications, model behavior depends on prompts as well as the model.

Therefore:

```text
Model Version
      +
Prompt Version
      +
RAG Configuration
      +
Application Version
```

should be identifiable for a production release.

A model version alone may not fully describe production behavior.

---

# 24. Embedding Model Versioning

Embedding models should also be versioned.

Example:

```text
embedding-v1
embedding-v2
```

A change in embedding model can affect:

```text
Embedding Vectors
Retrieval Results
Similarity Scores
RAG Quality
```

Therefore, embedding-model changes should be treated as potentially significant system changes.

---

# 25. Vector Index Compatibility

If the embedding model changes:

```text
Embedding Model A
       ↓
Existing Index
```

may not be compatible with:

```text
Embedding Model B
```

A migration strategy may therefore require:

```text
New Embedding Model
      ↓
Re-embedding
      ↓
New Vector Index
      ↓
Evaluation
      ↓
Deployment
```

The compatibility of the existing index should be verified before switching models.

---

# 26. Fine-Tuned Model Versioning

If a base model is fine-tuned:

```text
Base Model
    ↓
Dataset Version
    ↓
Training Configuration
    ↓
Fine-Tuning
    ↓
Fine-Tuned Model
```

The resulting model should retain references to:

```text
Base Model Version
Dataset Version
Training Configuration
Training Run
Evaluation Results
```

---

# 27. Model Configuration Versioning

Configuration can affect model behavior even when model weights remain unchanged.

Examples:

```text
Temperature
Max Tokens
Quantization
Batch Size
Context Length
Generation Parameters
```

Significant configuration changes should therefore be versioned or recorded with the release.

---

# 28. Model Comparison

When comparing models, use a consistent evaluation process.

```text
Evaluation Dataset
       │
       ├── Model A
       ├── Model B
       └── Model C
```

Compare:

```text
Quality
Latency
Cost
Resource Usage
Reliability
```

The winning model should be selected based on the project's requirements rather than one metric alone.

---

# 29. Baseline Model

A baseline model should be maintained for meaningful comparisons.

```text
Baseline
   ↓
Candidate Model
   ↓
Comparison
```

A candidate should demonstrate sufficient improvement or other meaningful advantages over the baseline before replacing it.

---

# 30. Model Promotion

The promotion process is:

```text
Experimental
      ↓
Candidate
      ↓
Evaluation
      ↓
Validated
      ↓
Staging
      ↓
Production
```

Each transition should have clearly defined criteria.

---

# 31. Promotion Gates

Possible promotion gates include:

```text
Evaluation Threshold
Regression Tests
Latency Requirement
Resource Requirement
Security Validation
Integration Tests
```

For LLMs, additional gates may include:

```text
Groundedness
Instruction Following
Tool Reliability
Safety
```

---

# 32. Staging Validation

Before production:

```text
Validated Model
      ↓
Staging
      ↓
Integration Testing
      ↓
AI Evaluation
      ↓
Performance Validation
      ↓
Production
```

The staging environment should approximate production behavior as closely as practical.

---

# 33. Canary Deployment

For higher-risk model changes, a canary strategy may be used.

```text
New Model
    ↓
Small Traffic Portion
    ↓
Monitor
    ↓
Acceptable?
 ┌──┴──┐
Yes    No
 ↓      ↓
Expand  Rollback
```

This reduces the risk associated with introducing a new model version to all users simultaneously.

---

# 34. A/B Testing

Two model versions may be compared using controlled traffic.

```text
User Traffic
      │
      ├── Model A
      │
      └── Model B
```

Compare:

```text
Quality
Latency
Cost
User Outcomes
Error Rate
```

A/B testing should follow defined evaluation criteria and appropriate privacy requirements.

---

# 35. Rollback

A stable previous model should remain available when practical.

```text
Production
    ↓
Issue Detected
    ↓
Switch to Previous Stable Version
    ↓
Validate
    ↓
Monitor
```

Rollback should be tested rather than assumed to work.

---

# 36. Model Rollback vs Application Rollback

A model may sometimes be rolled back independently of application code.

```text
Application v5
    +
Model v4
```

could potentially replace:

```text
Application v5
    +
Model v5
```

However, compatibility must be verified.

If the model and application are tightly coupled, the complete release may need to be rolled back.

---

# 37. Model Compatibility

Before deployment, verify compatibility with:

```text
Application
Tokenizer
Inference Framework
Hardware
API Contract
RAG Pipeline
Agent
Memory
```

A model that performs well independently may still fail when integrated into the application.

---

# 38. Model Monitoring

After deployment, monitor:

```text
Latency
Error Rate
Resource Usage
Token Usage
Cost
Quality Metrics
```

For AI applications, also monitor:

```text
Retrieval Quality
Tool-Calling Errors
Groundedness
User Feedback
Evaluation Scores
```

---

# 39. Model Drift

Model behavior may degrade over time due to changes in:

```text
Input Distribution
User Behavior
Knowledge Sources
Application Context
External Provider Behavior
```

Monitoring should identify significant changes where sufficient data is available.

---

# 40. Model Re-evaluation

A production model should be re-evaluated when significant changes occur.

Triggers may include:

```text
New Model Version
New Dataset
Prompt Change
RAG Change
Embedding Change
Provider Change
Major Application Change
Observed Quality Degradation
```

---

# 41. Model Retirement

A model may be retired when:

* A better version replaces it
* It is no longer supported
* It is too expensive
* It has unacceptable performance
* It is incompatible with the current system

Retirement process:

```text
Production
    ↓
Replacement Validated
    ↓
New Model Deployed
    ↓
Old Model Deprecated
    ↓
Archived
```

---

# 42. Reproducibility

A historical model result should ideally be reproducible using:

```text
Model Version
Dataset Version
Code Commit
Configuration
Prompt Version
RAG Configuration
Dependency Versions
Evaluation Version
```

This is especially important when investigating regressions.

---

# 43. Model Audit Trail

Important model events should be recorded.

Examples:

```text
Model Created
Model Evaluated
Model Promoted
Model Deployed
Model Rolled Back
Model Deprecated
Model Archived
```

The audit trail should identify:

```text
Version
Timestamp
Environment
Action
Result
```

---

# 44. Model Security

Model artifacts should be protected against:

```text
Unauthorized Modification
Unauthorized Access
Artifact Replacement
Credential Exposure
Malicious Files
```

Access should follow the principle of least privilege.

---

# 45. External LLM Versioning

For externally hosted LLMs, the project may not control the underlying model artifact.

Therefore, record:

```text
Provider
Model Identifier
Provider Version / Snapshot Information
Request Configuration
Prompt Version
Application Version
Evaluation Results
```

If the provider changes model behavior, the application should be re-evaluated where appropriate.

---

# 46. Model Release Record

Each production release should ideally have a record similar to:

```text
Release:
    Application: vX.Y.Z
    Model: model-vX
    Prompt: prompt-vX
    RAG: rag-vX
    Evaluation: evaluation-vX
    Environment: production
    Status: active
```

This provides a compact representation of the deployed AI configuration.

---

# 47. Model Versioning Workflow

The complete workflow is:

```text
Model Change
      ↓
Experiment
      ↓
Evaluation
      ↓
Candidate Version
      ↓
Regression Testing
      ↓
Validation
      ↓
Registry
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

# 48. Model Versioning Checklist

Before creating a production model version:

```text
☐ Model identified
☐ Version assigned
☐ Source/base model recorded
☐ Dataset version recorded
☐ Configuration recorded
☐ Evaluation completed
☐ Regression tests passed
☐ Artifact stored
☐ Model registry updated
☐ Application compatibility verified
☐ Staging validation completed
☐ Rollback version available
```

---

# 49. Final Model Versioning Principles

The project follows these principles:

1. **Every production model must be identifiable by version.**
2. **Model lineage should be traceable.**
3. **Dataset and configuration versions should be associated with models.**
4. **Model changes must be evaluated before deployment.**
5. **Embedding models should be versioned separately.**
6. **LLM configurations should include model and prompt versions.**
7. **Production models should have a rollback path.**
8. **Model artifacts should be stored separately from normal source code when appropriate.**
9. **Model status should be explicit.**
10. **Production behavior should be reproducible as far as practical.**
11. **Model changes should be monitored after deployment.**
12. **Old production versions should remain available long enough to support rollback and investigation.**

The goal is to make every model used by the system traceable, reproducible, evaluable and safely deployable.
