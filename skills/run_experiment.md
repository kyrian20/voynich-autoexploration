# Skill: Run Experiment

## Purpose
Design, execute, and record a single falsifiable experiment against the Voynich corpus or reference corpora. This skill covers the full lifecycle: from pre-registration through result recording.

## Experiment Directory Structure

Every experiment lives at:
```
experiments/exp_NNN_brief_name/
├── script.py       # Required: the actual code, runnable without modification
├── result.md       # Required: structured finding (see template below)
└── data.json       # Optional: numerical outputs worth preserving for future reference
```

**Experiment ID assignment:** `NNN` is a zero-padded three-digit integer. Check `experiments/` for the highest existing ID and increment by one. IDs are never reused. The `brief_name` is 2-4 words joined by underscores, describing the test (not the result): `positional_entropy`, `currier_alignment`, `gallows_grouping`.

## Pre-Registration Rule

**Write out what you expect to find BEFORE running any code.** This is mandatory. The pre-registration goes in `result.md` under "Expected Outcomes" before the experiment runs. Filling it in after the fact defeats the purpose and is prohibited.

**The Expected Outcomes section must include a sentence of the form: "This experiment is an UNFAIR test of the hypothesis if [condition]"** — listing any implementation detail or parameter choice that could bias the result against the hypothesis being tested (e.g., a modification operation that destroys the feature the hypothesis depends on, a parameter range that excludes the region where the hypothesis would succeed, a corpus filter that removes the signal). If no such condition applies, write "No unfairness conditions identified." The point is to force examination of the exp_180 failure mode — where an implementation detail made the experiment unfair to the hypothesis — before running the experiment, not after.

## Procedure

### 1. Pre-register
Before writing `script.py`, write `result.md` up to and including the "Expected Outcomes" section. Leave "Result," "Interpretation," "Limitations," and "Follow-up Questions" blank.

### 2. Write the script
- Target: runs in under 10 minutes on a modern laptop
- Self-contained: include data loading, computation, and printed output in one file
- Clear output: print labeled numerical results, not just plots
- Control corpora: always run the same measurement on at least one reference language and one random-text control
- Reproducible: set random seeds where applicable; note any external data dependencies at the top

```python
# experiments/exp_NNN_brief_name/script.py
# Experiment: [one-line description]
# Hypothesis tested: [which hypothesis from hypothesis_backlog.md]
# Data: [file paths used]
# Dependencies: numpy, scipy, ... (install with: pip install ...)

import numpy as np
...

if __name__ == "__main__":
    ...
    print(f"Voynich h2: {voynich_h2:.4f}")
    print(f"Latin h2:   {latin_h2:.4f}")
    print(f"Random h2:  {random_h2:.4f}")
```

### 3. Execute and capture output
Run the script. Copy the full stdout into `result.md` under "Raw Output."

### 3b. Audit the draft result
After filling in the Interpretation and Limitations sections but before finalizing, run the audit_experiment skill (skills/audit_experiment.md) on the draft result.md. This produces a Self-Audit section appended to the result. If the audit identifies a target-awareness issue, feature-destroying implementation, extrapolation beyond the grid, negative-result overreach, or unexpected control behavior, revise the result.md to address it before proceeding to step 4.

### 4. Complete result.md
Fill in all remaining sections.

### 5. Save data.json (if applicable)
If the experiment produced a table of numbers (e.g., per-position entropy values, per-length values, alignment scores), save them as structured JSON. Future experiments may need to compare against these numbers without re-running.

```json
{
  "experiment": "exp_NNN_brief_name",
  "date": "YYYY-MM-DD",
  "voynich": { ... },
  "latin": { ... },
  "random": { ... }
}
```

## result.md Template

```markdown
# Experiment exp_NNN: [Brief Title]

**Date:** YYYY-MM-DD
**Hypothesis:** [ID and statement from hypothesis_backlog.md]
**Status:** pre-registered | complete

## Hypothesis
[Precise statement of the claim being tested. One or two sentences. Should be falsifiable.]

## Method
[What statistical test or computation was used. What data was used. How control corpora were incorporated.]

## Expected Outcomes
[What would each major competing theory predict? Fill this in BEFORE running the experiment.]

| Theory | Predicted result |
|--------|-----------------|
| Natural language in cipher | ... |
| Glossographic/received text | ... |
| Constructed artificial language | ... |
| Hoax / meaningless text | ... |

## Raw Output
```
[paste full stdout here]
```

## Result
[One sentence summary of what the numbers show.]

## Interpretation
[What does this result mean for the hypothesis space? Be precise: did this test confirm, refute, or fail to discriminate? What are the implications for other hypotheses?]

## Limitations
- [List confounds, data quality issues, scope restrictions]
- [Flag if the test would produce the same result on control cases where the answer is known]

## Follow-up Questions
- [Questions this experiment raised that should become new hypotheses]
```

## What Counts as a Complete Experiment

An experiment is complete when:
- `script.py` is saved and can be re-run from scratch to reproduce the output
- `result.md` has all sections filled
- State files have been updated (findings.md, failed_approaches.md, or open_questions.md as appropriate)
- A one-line entry has been added to `iteration_log.md`

An experiment is NOT complete if you ran the analysis in a scratch session and forgot to save the script, or if result.md stops at "Raw Output" with no interpretation.

## Choosing the Right Statistical Test

| Question type | Appropriate test |
|---------------|-----------------|
| Is this entropy value surprising? | Compare to control distribution; use a shuffled-text baseline |
| Are two distributions the same? | KL divergence, KS test, or chi-squared |
| Do two subcorpora align? | Cross-entropy, cosine similarity of embeddings, or edit distance on frequency vectors |
| Is a pattern statistically significant? | Permutation test against null model |
| Does a transformation improve entropy? | Direct before/after comparison with control |

When in doubt, use the permutation test: shuffle the data, measure the statistic, repeat 1000 times, and report where the observed value falls in that null distribution.

## Control Text Standards

Always include:
1. **At least one natural language** from `data/reference_corpora/` (Latin or Italian preferred, since Voynich's historical context makes them the most relevant baseline)
2. **A random control** generated by sampling from Voynich's own character frequency distribution with no sequential structure. This controls for frequency effects.

The relevant question is almost never "what is Voynich's h2?" but "how does Voynich's h2 compare to what we'd expect from a natural language, and from pure noise?"
