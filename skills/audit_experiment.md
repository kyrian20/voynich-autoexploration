# Skill: Audit Experiment

## Purpose
Audit a draft result.md for the three failure modes that have required human-intervention corrections in this project. This skill is invoked AFTER completing result.md but BEFORE updating any state files (findings.md, failed_approaches.md, open_questions.md). It produces a Self-Audit section that is appended to result.md.

## When to Use This Skill

After every experiment, without exception. The audit runs on the draft result.md before state file updates. If the audit identifies a problem, the result.md must be revised before proceeding.

## The Five Checks

### Check 1: Target-Awareness

Does any parameter, substitution table, mapping rule, calibration probability, onset weight, suffix weight, buffer filtering rule, or corpus selection in the mechanism relate to a VMS target metric (am_ll, y_lf, ss_mean, adj_rate, or any other metric reported in the result)?

For each such element, answer:
- What is the element?
- Which VMS metric does it relate to?
- Was it calibrated using knowledge of the VMS value for that metric?
- Would the experiment's result change qualitatively if this element were set without reference to the VMS target?

If any element is target-aware, the result.md must state that the reported metric value is **conditional on this calibration** and that a non-target-aware version of the mechanism would produce a different (typically weaker) result. Do not bury this in limitations — state it in the Interpretation section, adjacent to the claim it qualifies.

**Origin**: exp_177's LL table mapped all Latin clause-final morphemes to EVA -am specifically because -am was the target metric. The resulting 5.756× was conditional on that mapping. This was not disclosed in the original draft.

### Check 2: Feature-Destroying Implementation

Does any implementation detail — the modification operation, buffer insertion policy, position gating rule, seed vocabulary, corpus filter, line-breaking method, or tokenization choice — actively destroy or degrade the specific feature the hypothesis depends on?

For each such detail, answer:
- What is the implementation detail?
- What feature does the hypothesis predict?
- Does this detail destroy, degrade, or suppress that feature?
- Is there a plausible alternative implementation that preserves the feature?

If any implementation detail destroys the feature under test, the experiment is not a fair test of the hypothesis. The result.md must state this prominently in the Interpretation section: "This experiment is unfair to the hypothesis because [detail] destroys [feature]. An alternative implementation preserving this feature ([specific alternative]) is untested and could produce a qualitatively different result."

Do NOT conclude "the hypothesis fails" when the implementation actively works against the hypothesis. Conclude "the hypothesis fails under this implementation."

**Origin**: exp_180's modification operation replaced the onset class of copied tokens — destroying the exact feature (onset self-succession) the hypothesis depended on. The resulting 0/18 was interpreted as structural to copy-buffer architectures. exp_181 reversed this conclusion by preserving onsets.

### Check 3: Extrapolation Beyond the Tested Grid

Does the result.md contain any of the following phrases or their equivalents?
- "no parameter setting"
- "structural"
- "cannot"
- "impossible"
- "architectural limit"
- "inherent to"
- "fundamental"
- "any [mechanism/cipher/model] of class X"

For each such claim, answer:
- What is the exact claim?
- What parameter grid was actually tested?
- Does the grid cover the full plausible range for each parameter?
- Is there a plausible untested region that could change the conclusion?

If the claim exceeds the tested grid, soften the language to: "not reproduced under the tested parameter range [specify range]." Reserve "structural" and "cannot" for claims supported by a logical argument that is independent of the specific parameter values tested — and state the logical argument explicitly.

**Origin**: exp_180 claimed the ss_mean/adj_rate coupling was "structural to copy-buffer architectures" from a grid of MODIFY_PROB ∈ {0.3, 0.4, 0.5} with onset-replacing modification — less than half the parameter space, and the worst-case modification for the hypothesis.

### Check 4: Negative-Result Overreach

If the experiment produced a negative result (the mechanism did not reproduce the VMS target), does the interpretation stay within the scope of this specific mechanism and these specific conditions?

Check whether the result.md claims any of:
- "X requires Y" (from a single failure of one mechanism)
- "no mechanism of class Z can produce X" (from testing one member of class Z)
- "the VMS has intrinsic [property]" (from failing to reproduce it mechanistically)

The valid conclusion from a negative result is: "This mechanism did not produce X under these conditions." The invalid conclusion is: "X requires Y" or "no mechanism of class Z can produce X." The second formulation requires either exhaustive testing of class Z or a logical argument that class Z cannot produce X in principle — and that argument must be stated explicitly and checked against Check 2 (is the negative result actually caused by an implementation detail, not the mechanism class?).

**Origin**: exp_180 concluded "onset-class clustering is intrinsic to the vocabulary structure rather than generated by copying." This was an overreach from one negative result under one modification operation. exp_181 showed that a different modification operation produced viable combinations.

### Check 5: Control-Comparison Interpretation

For every metric where the result.md compares VMS to a control distribution (shuffled text, reference language, null model, or simulated mechanism), answer:
- What is the control?
- How do I expect the control to behave, and why?
- How did the control actually behave?
- If the control behaved unexpectedly, does that change the interpretation of the VMS comparison?

Write an explicit sentence of the form: **"I expect [control] to produce [metric] ≈ [value] because [reason]. The control actually produced [observed value]."** If the control's behavior is surprising — especially if it exceeds VMS on any metric — investigate the surprise before interpreting the VMS result. A control that exceeds the real data on a metric is a red flag for a sampling artifact or a confound in the metric itself.

Additionally: if the control exceeds VMS on any metric, or if the control's value differs from the expected value by more than a factor of 1.5, treat this as a hard flag. Do not proceed with the VMS interpretation until the discrepancy is investigated. A control that behaves unexpectedly is often measuring something different from what you think it is measuring (exp_175 was this exact failure mode: the within-line shuffle's behavior at lags 11-12 was not what anyone expected, and the discrepancy was the signal, not the VMS value).

**Origin**: exp_175's within-line shuffle produced higher MI than real VMS at lags 11-12. This meant the "VMS above Timm at lags 10-12" finding was a sampling artifact, not evidence of long-range structure. The original synthesis treated it as a signal.

## Procedure

1. Read the draft result.md in full.
2. Run each of the five checks. For each check, write the answers to the sub-questions.
3. If any check identifies a problem, revise the result.md before proceeding. The revision must appear in the Interpretation, not buried in Limitations.
4. After all five checks pass (or the result.md has been revised to address them), write the Self-Audit block.

## Output: The Self-Audit Block

Append the following section to result.md, after Limitations and before Conclusion:

```
## Self-Audit

**Target-awareness**: [List all target-aware elements and state whether the result is conditional on them. If none: "No target-aware elements identified."]

**Feature-destroying implementation**: [List any implementation details that destroy or degrade the feature under test. If none: "No feature-destroying implementation details identified."]

**Extrapolation**: [List any claims that exceed the tested parameter grid, and state the actual grid. If none: "All claims are within the tested parameter range."]

**Negative-result scope**: [If negative result: state the scope of the conclusion. If positive result: "N/A — positive result."]

**Control behavior**: [For each control, state expected vs actual behavior. Flag any surprises.]
```

If any check required a revision to result.md, note what was changed in the Self-Audit block: "Revised: [description of change] based on [check name]."

## What This Skill Does NOT Do

This skill does not replace the Opus meta-review. It catches the categories of error that have occurred in this project. It does not catch novel failure modes. The Opus review remains the primary independent check; this skill reduces the load on the review by catching known patterns before they reach the reviewer.
