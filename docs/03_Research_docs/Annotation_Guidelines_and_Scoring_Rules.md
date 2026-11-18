# Annotation Guidelines and Scoring Rules

## 1. Purpose

This document defines how to label outputs from the baseline top-k vector-memory system and the proposed preference-aware memory controller.

The goal is to make evaluation consistent across systems and scenarios. Annotators should judge the evidence in the conversation history, retrieved memories, and final response—not which system produced the output.

## 2. Files and records

Use these guidelines with `Preference_Memory_Pilot_Dataset.csv`.

Each `scenario_id` identifies one test case. For every scenario, run both systems using the same conversation history and test query. Preserve:
- The exact conversation history and query.
- The memories retrieved by each system.
- The final response from each system.
- The model identifier and generation settings.
- The annotation decisions and brief evidence.

Do not overwrite the original scenario definitions. Enter results in a separate copy of the scoring sheet.

## 3. General annotation rules

1. Read the full conversation history before judging an output.
2. Identify the preference key being tested.
3. Identify the expected value, scope, and validity period.
4. Check the memories retrieved by the system.
5. Read the final response.
6. Score each applicable criterion independently.
7. Record a short explanation for every `No`, `Unclear`, or disputed decision.
8. Do not infer a permanent preference update unless the user's wording supports it.
9. Do not treat retrieval of a stale memory as proof that it influenced the answer.
10. If the scenario is genuinely ambiguous, judge whether the system handled the ambiguity appropriately; do not force an arbitrary active value.

## 4. Allowed annotation values

For binary result columns, use:
- `Yes`: the criterion is clearly satisfied.
- `No`: the criterion is clearly not satisfied.
- `Unclear`: available evidence is insufficient to decide.
- `NA`: the criterion does not apply to this scenario.

Do not leave an evaluated field blank. A blank means the experiment has not yet been annotated; `NA` means it was considered and does not apply.

## 5. Metric definitions and scoring

### 5.1 Stale-memory retrieved

This is a diagnostic field, separate from stale-memory influence.

Mark `Yes` if the system retrieved a preference that was superseded or expired for the current query. Mark `No` if no such memory was retrieved. Mark `NA` if the scenario contains no stale candidate.

### 5.2 Stale-memory influenced

Mark `Yes` only when the final answer demonstrably follows, reflects, or is materially shaped by an outdated preference.

Examples:
- Old preference: concise. New preference: detailed. The answer is deliberately very short because of the old preference → `Yes`.
- Both old and new memories are retrieved, but the answer follows the new detailed preference → `No`.
- The answer is too short, but there is no evidence linking that to the old memory → `Unclear`, with a note.

A stale memory being present in the prompt is not, by itself, enough to mark influence.

### 5.3 Current preference followed

For scenarios with a clearly defined active preference, mark `Yes` if the response follows the expected value and scope. Mark `No` if it does not. Mark `Unclear` if the response gives insufficient evidence.

For ambiguous-conflict scenarios, use `NA` for this metric unless the scenario's expected behaviour is a specific clarification or conflict-handling action. In that case, record the clarification success in the notes or a separate ambiguity-handling field.

### 5.4 Preference update correct

Use this primarily for explicit-update scenarios.

Mark `Yes` if the system:
- Recognizes the update.
- Applies it to the correct preference key.
- Makes the new value active.
- Does not continue applying the superseded value to the same scope.

Mark `No` if it keeps the old value active, applies the update to the wrong key, or changes unrelated preferences.

For stable, ambiguous, temporary, and scope-specific scenarios, use `NA` unless the experiment protocol explicitly defines an update decision to score.

### 5.5 Ambiguity handled correctly

For ambiguous-conflict scenarios, mark `Yes` if the system avoids silently making an unsupported permanent choice and asks a useful clarification or otherwise safely limits its assumption to the current request.

Mark `No` if it silently treats one conflicting statement as a permanent replacement without evidence, or applies an arbitrary value as though the conflict were resolved.

If a current task clearly specifies a local requirement (for example, a professional message), the system may follow that local requirement without changing the user's general preference. Annotate this distinction.

### 5.6 Temporary preference handled correctly

Mark `Yes` if the temporary instruction is applied within its stated scope and the normal preference remains applicable outside that scope. Mark `No` if the temporary instruction is incorrectly made permanent or ignored within its valid scope.

For this pilot, the test query must make the intended validity window clear. If a scenario does not actually test what happens after expiry, do not claim that expiry behaviour has been tested.

### 5.7 Scope handled correctly

Mark `Yes` if the system applies the preference to the relevant subject/task and does not generalize it beyond the stated scope. Mark `No` if it applies the scoped preference in an unrelated context or ignores it in the relevant context.

## 6. Category-specific guidance

| Category | Main criterion | Important caution |
|---|---|---|
| `stable_preference` | Current preference followed | Tests ordinary preference use, not update handling |
| `explicit_update` | Update correct; current preference followed; stale-memory influence | Old preference may be retrieved without influencing the answer |
| `ambiguous_conflict` | Ambiguity handled correctly | Do not invent a gold active value where the user did not specify one |
| `temporary_preference` | Temporary instruction handled within scope | The pilot must include a post-expiry query to test actual expiry |
| `scope_specific_preference` | Scope handled correctly | Judge the scope stated in the conversation, not a guessed global rule |

## 7. Recommended annotation procedure

For stronger reliability:
1. Have two annotators independently label at least a subset of the outputs.
2. Hide system identity from annotators where practical.
3. Compare disagreements.
4. Resolve disagreements using the written rules, not by preferring one system.
5. Report agreement and explain how disagreements were resolved.

If only one annotator is available, re-annotate a sample after a time gap and report this as a limitation. Do not describe single-person repeated annotation as independent inter-annotator agreement.

## 8. Aggregation formulas

Let:
- `N_risk` = number of eligible stale-memory risk probes.
- `N_stale_influence` = number of those probes where stale memory influenced the answer.
- `N_active` = number of probes with a clearly defined active preference.
- `N_followed` = number where the current preference was followed.
- `N_updates` = number of evaluable explicit-update scenarios.
- `N_update_correct` = number of explicit updates resolved correctly.

Then:

**Stale-memory use rate**

`100 × N_stale_influence / N_risk`

**Current-preference accuracy**

`100 × N_followed / N_active`

**Preference update accuracy**

`100 × N_update_correct / N_updates`

Calculate each system's metrics separately. Report the numerator and denominator alongside every percentage. Exclude `Unclear` and `NA` from the relevant numerator and denominator, but report their counts separately. Do not silently discard difficult cases.

For precision and recall, compare retrieved memories against a scenario-specific gold list of relevant, eligible memories. A gold list must be prepared before evaluating system outputs.

## 9. Important pilot-dataset limitations to resolve

The current 50-row CSV is a first draft. Before using it for formal results:

1. **Stable preference keys:** Some stable scenarios currently share a generic `response_style` key. Replace these with specific keys such as `detail_level`, `programming_language`, `comparison_format`, and `unit_preference`.
2. **Stale-risk labels:** The current `stale_memory_risk_probe` field marks explicit updates as `Yes`, but does not yet identify all temporary or expiry probes. Revisit labels after adding post-expiry test turns.
3. **Temporary scenarios:** A single query inside the temporary period tests the override, not whether the original preference returns after expiry. Add a second query after the validity window.
4. **Scope-specific scenarios:** Include paired in-scope and out-of-scope queries to test both correct application and non-leakage.
5. **Ambiguous conflicts:** Score clarification/conflict handling rather than forcing a single active preference.
6. **Scenario wording:** Review all gold labels manually before execution. The expected behaviour column is guidance, not a substitute for a precise scoring rubric.

## 10. Reporting checklist

Before reporting results, confirm:
- [ ] Both systems received identical scenario histories and queries.
- [ ] Model identifiers and settings were recorded.
- [ ] Retrieved memories and final answers were saved.
- [ ] All scored outputs used the same annotation rules.
- [ ] `Yes`, `No`, `Unclear`, and `NA` were used consistently.
- [ ] Numerators and denominators are reported with percentages.
- [ ] Pilot results are not presented as definitive benchmark evidence.
- [ ] Limitations and failure examples are included.
