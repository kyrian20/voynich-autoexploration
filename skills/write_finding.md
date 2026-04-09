# Skill: Write Finding

## Purpose
Record a result from a completed experiment into the appropriate state files. A finding is only useful if it is discoverable, traceable to its source, and phrased so a future iteration can act on it without re-reading the experiment.

## The Three State Files

### findings.md — What we've established
Use this for results that positively constrain the hypothesis space: measurements that held up, patterns that were confirmed, structural features that are now characterized. A finding is a fact about the text (or about the relationship between the text and reference corpora) that survived methodological scrutiny.

**When to add here:** the experiment produced a clear, replicable result that can be stated as a fact. The result does not need to be dramatic — "Voynich h2 at word-initial position is 3.1 bits vs. 2.0 bits overall" is a finding even if its interpretation is uncertain.

### failed_approaches.md — What we've ruled out
Use this for hypotheses that were definitively refuted: tests that the text failed, transformations that did not recover natural-language entropy, alignments that produced no signal. A failed approach is not a mistake — it is a narrowing of the hypothesis space, which is the job.

**When to add here:** the experiment produced a clear negative result, meaning the hypothesis made a prediction and the data did not support it. Be specific: the failure is of *this hypothesis under this test*, not of all related ideas. If there's a close variant worth trying, add it to the backlog instead.

### open_questions.md — What needs human judgment
Use this for results that can't be resolved computationally: methodological choices that require domain expertise, results that are ambiguous between theories with no cheap discriminating test, and situations where the next step requires a tool or dataset that isn't available. Also use this to flag when an experiment suggests the agenda itself needs to shift.

**When to add here:** you are genuinely stuck and the path forward requires input. Don't add things that are just "the next experiment" — those belong in hypothesis_backlog.md.

## How to Write a Finding

Every finding entry must include:
1. **A precise factual statement** — one or two sentences, no hedging beyond what the data warrants
2. **The experiment ID** — always traceable back to the script that produced the result
3. **The date**
4. **A brief note on limitations** — one line is fine; the full treatment is in result.md

**Template for findings.md:**
```markdown
## F[NNN]: [Brief Title]
**Experiment:** exp_NNN_brief_name
**Date:** YYYY-MM-DD
**Finding:** [Precise statement of the fact established]
**Limitation:** [Most important caveat]
```

**Template for failed_approaches.md:**
```markdown
## X[NNN]: [Hypothesis title]
**Experiment:** exp_NNN_brief_name
**Date:** YYYY-MM-DD
**What was tested:** [The specific prediction the hypothesis made]
**Result:** [What the data actually showed]
**Why ruled out:** [Why this counts as a refutation, not just a negative result]
**Variants worth trying:** [Any genuinely distinct close variants that remain open, or "none"]
```

**Template for open_questions.md:**
```markdown
## Q[NNN]: [Question]
**Raised by:** exp_NNN_brief_name
**Date:** YYYY-MM-DD
**Question:** [Precise statement of what needs to be resolved]
**Why this can't be resolved computationally:** [What's blocking it]
**What it would take to resolve it:** [Tool, dataset, expertise, or human decision needed]
```

## Numbering

Use sequential integers within each file. Check the existing highest number and increment:
- Findings: F001, F002, ...
- Failed approaches: X001, X002, ...
- Open questions: Q001, Q002, ...

## The Traceability Rule

**Every finding, failure, and open question must cite a specific experiment ID.** This is non-negotiable. If you have an insight that wasn't produced by a formal experiment, run a quick script first — even a 5-line script that prints one number counts as an experiment. The point is that the claim is reproducible.

No entry of the form "I noticed that..." or "It seems like..." without an exp_NNN citation. If you can't point to a script that produced the number, you don't have a finding.

## The Utility Rule

Write findings so a future iteration can use them without reading result.md. Ask yourself: if I read only findings.md, would I know:
- What was measured?
- What the number was?
- What corpus was used?
- What the important caveat is?

If the answer to any of these is no, the finding is incomplete. A finding like "entropy was measured" is useless. A finding like "Voynich second-order character entropy (EVA, full corpus, Takahashi transcription) is 2.01 bits/character vs. 3.47 bits/character for Latin Vulgate — a difference of 1.46 bits that replicates the published range of ~2.0 in Bowern (2021)" is useful.

## After Writing

After updating state files:
1. Append to `iteration_log.md`: one line with timestamp, experiment ID, and a 10-word summary
2. Add any follow-up hypotheses to `hypothesis_backlog.md` (see `generate_hypotheses.md`)
3. If a finding implies the backlog priority should change, update the affected backlog entries' priority fields
