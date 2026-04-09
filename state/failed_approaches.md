# Failed Approaches
# Cryptanalyst — Voynich Manuscript Investigation
# Approaches that have been definitively ruled out by experiment.
# Format: see skills/write_finding.md for the entry template.
# Before adding: check ~/voynich-kb/state/failed_approaches.md for what the Librarian has already established.

---

## X001: H010 — Q-Initial Removal as Path to Higher H_Initial
**Experiment:** exp_002_positional_entropy
**Date:** 2026-04-09
**What was tested:** H010 predicted that stripping q-initial words would raise H_initial toward natural-language levels (~3.5-4.0 bits) by revealing underlying onset diversity hidden by the constrained q-initial slot.
**Result:** H_initial DROPPED from 3.137 to 2.976 after removing q-initial words. Q-initial words contribute entropy as a unique category; without them, the remaining onset distribution is more concentrated on o and c.
**Why ruled out:** The prediction was directionally wrong. Q-initial words increase onset entropy rather than suppressing it.
**Variants worth trying:** Whether "qo" as a unit (treated as a single bigram token) changes the picture of H_initial if the bigram is treated as a single glyph. This is a reformulation worth testing.

## X002: H013 — qo-as-Token Exposes Latent Lexical Structure
**Experiment:** exp_003_label_body_entropy
**Date:** 2026-04-09
**What was tested:** H013 predicted that treating 'qo' as a single prefix token and stripping it would reveal higher-entropy word stems below, indicating qo functions as a separable grammatical particle.
**Result:** Stripping qo changes H_initial by +0.029 bits and H2 by +0.043 bits — negligible.
**Why ruled out:** The effect is too small to indicate structural exposure of latent content. qo is not a separable prefix in any recoverable sense at this level of analysis.
**Variants worth trying:** Whether qo-words form a semantically coherent class (e.g., all appear in specific manuscript sections). This is a distributional question, not an entropy question.

<!-- Additional entries will be added as experiments are completed. -->
<!-- Example format:
## X001: [Hypothesis title]
**Experiment:** exp_NNN_brief_name
**Date:** YYYY-MM-DD
**What was tested:** [The specific prediction the hypothesis made]
**Result:** [What the data actually showed]
**Why ruled out:** [Why this counts as a refutation, not just a negative result]
**Variants worth trying:** [Any genuinely distinct close variants that remain open, or "none"]
-->
