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

## X003: H008 — Gallows-as-Group-Initiator Raises h2 to Natural-Language Range
**Experiment:** exp_006_gallows_grouping
**Date:** 2026-04-09
**What was tested:** H008 predicted that treating gallows characters (t, k, p, f) + their following character as a single verbose-cipher unit would raise h2 from ~2.34 toward 3.0-3.5 bits.
**Result:** Gallows + next char grouping raises h2 to only 2.513 (gain: +0.172 bits). Nowhere near natural-language range.
**Why ruled out:** The prediction specified a substantial h2 recovery; +0.17 bits is negligible in context. Even compound gallows treatment gives only +0.19 bits.
**Variants worth trying:** Context-dependent gallows grouping (only when gallows appears after specific characters); also, measuring whether gallows grouping recovers the natural language character distribution (not just h2).

## X004: H007 (Simple) — Adjacent-Pair or Triple Grouping Recovers Natural-Language h2
**Experiment:** exp_006_gallows_grouping
**Date:** 2026-04-09
**What was tested:** H007 (partial) predicted that some simple positional grouping (pairs or triples) would bring h2 into the natural-language range (3.0-3.5 bits).
**Result:** Adjacent pairs: h2 = 3.836 (overshoots NL range). Adjacent triples: h2 = 4.229 (far overshoots). Both exceed natural language h2, which makes them inconsistent with a verbose cipher interpretation (which should recover to NL range, not exceed it).
**Why ruled out:** Overshooting NL range rules out the simple interpretation. The increase in h2 is a mathematical artifact of creating 289 unique bigram types from 30 character types — the token diversity inflates h2 regardless of any underlying language.
**Variants worth trying:** Non-adjacent groupings; interleaved groupings (odd vs even positions); position-within-word-conditional groupings; also, comparing the token frequency distribution to natural language character frequencies as a stricter test.

## X005: H006 — Stolfi Crust Stripping Reveals Natural-Language h2 in Inner Slots
**Experiment:** exp_008_stolfi_slot_entropy
**Date:** 2026-04-09
**What was tested:** H006 predicted that the outer crust characters (grammatical affixes per Stolfi grammar) suppress h2, and that stripping them would expose a higher-entropy core approaching natural-language h2 (~3.4-3.5 bits).
**Result:** Core region h2 = 2.389 — only 0.048 bits above full corpus h2 (2.341). Nowhere near the natural-language target. Gallows-containing words (the "core" in Stolfi's grammar) actually have LOWER h2 (2.271) than the full corpus.
**Why ruled out:** The prediction required a substantial rise toward natural-language h2. The actual rise is negligible. The information is not concentrated in the inner slots.
**Variants worth trying:** A full Stolfi slot grammar parser (position-conditional character class assignment) rather than character-class approximation; testing whether inner-slot entropy rises within word-length-controlled groups.

## X006: F024 — Herbal Single-Char Labels as Object Annotation Layer
**Experiment:** exp_010_label_word_sections → validated in exp_011_single_char_validation
**Date:** 2026-04-09
**What was tested:** F024 proposed that herbal_A labels are dominated by single characters (y, o, f, d, e, s, p, x), implying a distinct annotation system (color codes, part-of-plant labels, scribe shorthand).
**Result:** Raw ZL3b inspection shows all 48 single-char herbal "labels" come from two folios. f49v has a perfectly alternating L0 (single char)/P0 (body text) pattern on every line — these are line margin markers, not plant labels. f66r is a "text only" (no illustration) folio with two columns of items, explicitly noted in the transcription as "individual characters in next column." Neither constitutes object labels.
**Why ruled out:** The finding was an artifact of treating all L0 locus codes as equivalent object labels. The underlying data is correctly transcribed; the analytical interpretation was wrong.
**Variants worth trying:** A proper object-label analysis would need to filter L0 entries to exclude line markers and list/table content. The few genuine plant labels in herbal_A (if any) need to be identified by cross-referencing locus context more carefully.

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
