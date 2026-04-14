# Non-Voynich Target Corpora for Architecture Specificity Test

**Date:** 2026-04-13
**Experiment:** exp_584 (Non-Voynich Architecture Specificity Test)
**Pre-registration:** state/preregistration_transliteration_and_specificity_thresholds.md

## Purpose

The 21-mechanism position-aware copy-buffer hybrid architecture achieves 19/19 PASS on the
B-dialect battery (exp_314, C008). These three non-VMS corpora test whether that score is
specific to VMS structure or reachable on structurally-matched natural language corpora.

---

## Corpus 1: Medieval Latin (Cicero De Officiis)

**Source:** Cicero, *De Officiis* (On Duties), bilingual Latin/English Gutenberg edition
**File:** `data/reference_corpora/latin/cicero_de_officiis_latin.txt`
**Raw size:** ~114,000 words (bilingual: Latin text + English translation)

**Extraction method:**
The Gutenberg file interleaves Latin sections with English translations. Latin paragraphs
are identified using an English stopword filter: paragraphs where <8% of words match a
common English stopword list are classified as Latin and retained. This method, previously
used in exp_177 and exp_184, reliably extracts Latin text with minimal English contamination.

**Extracted Latin words:** ~32,700 words (after filtering)
**Segmentation:** 2,458 pseudo-lines matching the B-dialect empirical line-length histogram
(SEED=584001; same target line count as VMS B-dialect corpus)
**Approximate tokens:** ~21,500 words after segmentation

**Character-onset class mapping (onset class → character pattern):**
- "qok"    → words starting with 'q' (qui, quod, quam, quid, quando...)
- "d"      → words starting with 'd' (de, dicere, dum, dicit...)
- "s"      → words starting with 's' (sed, si, sunt, sit, sic...)
- "y"      → words starting with 'y' or 'i' (iam, inde, in, ita...)
- "ch"     → words starting with 'c', 'g', or 'k' (causa, genus, consult...)
- "ok"     → words starting with 'o' (omnis, officium, opus...)
- "l"      → words starting with 'l' (lege, licet, labor...)
- "am_on"  → words starting with 'a' (autem, ac, atque...)
- "r"      → words starting with 'r' (res, ratio, rerum...)
- "other"  → all other initials

**Character-suffix class mapping (suffix class → word-final pattern):**
- "am"  → words ending in 'um', 'am', 'em', 'im' (Latin accusative/genitive morphemes)
- "edy" → words ending in 'edy', 'odi', 'idi' (expected near-absent in Latin: ~0.07%)
- "aiin"→ words ending in 'ant', 'unt', 'ino', 'ina' (verb forms and -ino derivatives)
- "other" → all other word endings

**Structural properties observed:**
- Positional onset enrichments: essentially flat (all ≈1.0, no systematic LF/LL preference)
- Self-succession rate (ss_mean ≈ 0.98): near-baseline (no word repetition structure)
- Adjacent identical pairs (adj_rate ≈ 0.0003): near-zero
- global_am_rate ≈ 0.176: high (Latin accusative morphology)
- word_len_mean ≈ 5.70 (slightly longer than VMS 5.24)

**Why Latin is a good comparison corpus:**
Classical Latin prose has relatively free word order with no systematic positional structure
analogous to VMS's onset class enrichments at LF/LL. The copy-buffer and stutter mechanisms
driving VMS's self-succession have no analog in Latin prose. If the architecture cannot
match Latin's flat structural metrics, this demonstrates structural specificity.

---

## Corpus 2: VMS-Matched Synthetic (Random Word Order)

**Source:** VMS B-dialect corpus, words randomly redistributed across line boundaries
**Method:** "Inter-shuffle" from exp_575 (SEED=574002; words pooled and redistributed)
**Result already known:** 14/19 total PASS after 6-param refit (exp_575)

**Applicable PASS (17 applicable metrics):**
- 2 non-applicable metrics (word_len_mean, edy_rate) both PASS for inter-shuffle
  (same VMS words used, just shuffled positions)
- 5 applicable metrics fail: am_ll, ss_mean, adj_rate, ss_d, ss_y
- Applicable PASS = 17 - 5 = **12/17**

**Why this corpus:**
The inter-shuffle destroys all positional structure while preserving VMS word type frequencies.
It tests whether the architecture's positional enrichment mechanisms are essential for 19/19.
Result: 5 hard structural floors prevent the architecture from matching flat distributions.

---

## Corpus 3: Morphologically Complex Non-Latin (Dante's Divina Commedia, Italian)

**Source:** Dante Alighieri, *La Divina Commedia*, Project Gutenberg edition (Italian text)
**File:** `data/reference_corpora/italian/dante_divina_commedia.txt`
**Raw size:** ~100,971 words (Italian text after Gutenberg header removal)

**Extraction method:**
Gutenberg header stripped (from `*** START OF THE PROJECT GUTENBERG EBOOK ***`).
Gutenberg footer stripped (to `*** END OF THE PROJECT GUTENBERG EBOOK ***`).
All alphabetic tokens (including Italian accented characters) retained, lowercase.
Words ≥2 characters, not all-caps (section headers), alphabetic only.

**Extracted Italian words:** ~100,000 words
**Segmentation:** 2,458 pseudo-lines matching B-dialect histogram (SEED=584002)
**Approximate tokens:** ~21,500 words after segmentation

**Character-onset class mapping:** identical to Latin (same scheme, applied to Italian):
- "qok"  → words starting with 'q' (que, quando, quello, quanto...)
- "d"    → words starting with 'd' (di, del, dal, dove, dunque...)
- "s"    → words starting with 's' (si, se, su, suoi, son...)
- "y/i"  → words starting with 'i' (il, in, io, ivi...)
- "ch"   → words starting with 'c' (che, col, come, così...)
- "ok"   → words starting with 'o' (or, ora, ogni...)
- "l"    → words starting with 'l' (la, le, lo, lei...)
- "am_on"→ words starting with 'a' (al, alla, anche, amor...)
- "other"→ all other initials

**Character-suffix class mapping:** identical to Latin.
Note: Italian accusative morphology differs from Latin (Italian -o/-a/-e are very common
endings but do NOT map to the "am" suffix class; Italian essentially lacks Latin-style
accusative -um/-am endings). This means Italian global_am_rate ≈ 0 (near-zero).

**Structural properties:**
- Positional enrichments: essentially flat (Italian word order more fixed than Latin
  but still no systematic VMS-like positional structure)
- Self-succession: slightly above baseline for Italian (some repeated words in poetry)
- word_len_mean ≈ 4-5 chars (Italian words tend to be shorter)

**Why Italian:**
Italian is morphologically complex (verb inflection, noun case/gender agreement) while
having no etymological or structural relationship to VMS. The Divina Commedia is medieval
(≈1308-1320) — contemporary with early VMS hypotheses — making it a culturally relevant
comparison. If the architecture cannot match Italian's structural metrics, it confirms
specificity beyond Latin.

---

## Applicable Metrics (17 of 19)

The following VMS battery metrics are applicable to character-mapped non-VMS corpora:

| Metric | Applicable? | Notes |
|--------|-------------|-------|
| am_ll | YES | Enrichment of 'am' suffix class at LL |
| d_ll | YES | Enrichment of 'd' onset class at LL |
| y_lf | YES | Enrichment of 'y/i' onset class at LF |
| ss_mean | YES | Word self-succession rate |
| adj_rate | YES | Adjacent identical pairs |
| qok_lf | YES | Enrichment of 'q' onset class at LF |
| d_lf | YES | Enrichment of 'd' onset class at LF |
| s_lf | YES | Enrichment of 's' onset class at LF |
| ch_ll | YES | Enrichment of 'c/g/k' onset class at LL |
| ok_ll | YES | Enrichment of 'o' onset class at LL |
| qok_ll | YES | Enrichment of 'q' onset class at LL |
| ss_d | YES | 'd' onset self-succession rate |
| ss_y | YES | 'y/i' onset self-succession rate |
| am_lf_enr | YES | 'am' suffix enrichment at LF |
| am_mid_enr | YES | 'am' suffix enrichment at MID |
| qok_ch | YES | 'ch' → 'qok' adjacency enrichment |
| global_am_rate | YES | Fraction of all words ending in 'am' suffix |
| **edy_rate** | **NO** | VMS-specific suffix; near-absent in Latin/Italian |
| **word_len_mean** | **NO** | Vocabulary-dependent; Latin ~5.7, Italian ~4.5, VMS ~5.2 |

Total applicable: **17/19**

---

## Methodology Note: Simulation Always Uses VMS Distributions

The 21-mechanism simulation ALWAYS generates word sequences using VMS B-dialect word
distributions (EVA onset classes: qok, ch, sh, ok, d, s, y, ...; VMS word vocabulary).
The metrics computed on the simulation output use VMS onset/suffix classification functions.

For each non-VMS target corpus:
1. The target corpus provides METRIC TARGETS using character-mapped onset/suffix classes
2. The simulation generates VMS-style words and computes VMS-label metrics
3. The grid search finds parameters minimizing the discrepancy between:
   - Simulation's VMS-label metric values
   - Target corpus's character-mapped metric values

These are comparable because both measure the same structural properties (positional
enrichment ratios, succession rates) — just using different label systems for word classes.
The enrichment ratio (freq at position / overall freq) is a dimensionless structural
statistic that is comparable across vocabularies.

**Key prediction:** The architecture cannot match Latin/Italian flat positional enrichments
(≈1.0) because:
1. The VMS onset distributions are already biased at LF/LL (e.g., y is biased toward LF),
   so any simulation using VMS distributions will inherit these biases
2. The copy-buffer creates floors on ss_mean, ss_d, ss_y that exceed flat targets
3. The blind-LL mechanism creates a floor on am_ll above 1.0

Therefore, the architecture is expected to achieve fewer PASS on Latin/Italian than on
the VMS corpus, confirming structural specificity.
