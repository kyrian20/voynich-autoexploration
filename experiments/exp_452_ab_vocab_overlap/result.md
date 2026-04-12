# exp_452: A/B Shared Word-Type Vocabulary Overlap (H_new_N)

**Hypothesis (H_new_N):** A and B dialects are dialectal variants of a common system (high overlap in frequent words, divergence in hapaxes) rather than distinct systems (low overlap at all frequency tiers). If dialectal: f≥20 words should be ≥60% shared; hapaxes should be ≤30% shared.

---

## Results

### Overall overlap

| | A | B |
|---|---|---|
| Word types | 2,213 | 2,937 |
| Shared types | 796 (36.0% of A) | 796 (27.1% of B) |
| Dialect-only types | 1,417 | 2,141 |
| Token coverage from shared types | 74.9% | 67.7% |

### Frequency-stratified overlap

| Tier | A types | A→B overlap | B types | B→A overlap |
|------|---------|-------------|---------|-------------|
| Hapax (f=1) | 1,506 | **20.8%** | 1,894 | **13.8%** |
| Rare (f=2-4) | 436 | 56.2% | 626 | 38.7% |
| Medium (f=5-19) | 207 | 84.1% | 296 | 64.9% |
| Frequent (f≥20) | 64 | **100.0%** | 121 | **82.6%** |
| Very frequent (f≥100) | 3 | 100.0% | 19 | 89.5% |

**All 64 high-frequency A word types (f≥20) appear in B. 100/121 high-frequency B types appear in A.**

### Onset class Jaccard index (type-level)

| Onset | A types | B types | Shared | Jaccard | Notes |
|-------|---------|---------|--------|---------|-------|
| ok | 113 | 148 | 52 | 0.249 | highest |
| qok | 98 | 142 | 47 | 0.244 | |
| sh | 179 | 221 | 74 | 0.227 | |
| ch | 350 | 427 | 136 | 0.212 | largest shared count |
| y | 214 | 215 | 72 | 0.202 | |
| cth | 56 | 16 | 10 | 0.161 | B uses 10/56 A-cth words; 62.5% of B-cth in A |
| l | 34 | 231 | 20 | **0.082** | B-specific pharma class |
| r | 7 | 73 | 4 | **0.053** | B-specific LL class |
| p | 14 | 29 | 1 | **0.024** | near-B-exclusive formula class |

### Top B-exclusive high-frequency words

qokeedy (248), qokedy (206), otedy (95), qotedy (57), qoteedy (56), lchey (41), lkaiin (34), olchedy (30), lshedy (29), olkain (28) — **dominated by edy-class suffix forms and l-onset compounds**.

### Top A-exclusive high-frequency words

kchor (15), qotchor (11), qotchol (10), cthody (10) — small N. A-biased shared words include cthol (A=44/B=1), cthy (A=75/B=3), chor (A=125/B=19).

### Top shared words by combined frequency

daiin (611), chedy (376), ol (305), chol (285), shedy (271), qokeey (254), chey (253), qokain (230), qokaiin (227), aiin (220)...

Note: daiin (A=380, B=231) is shared but A-biased (1.65:1 ratio); chedy (A=4, B=372) is shared but heavily B-biased.

---

## Interpretation

**H_new_N CONFIRMED (dialectal variants pattern):**

1. **Core vocabulary is shared**: 100% of A's high-frequency words (f≥20) appear in B. 82.6% of B's high-frequency words appear in A. The 75% token-level overlap means that 3 in 4 word tokens in A are words that also exist in B. This is strong evidence for a shared base vocabulary.

2. **Hapaxes are dialect-specific**: Only 20.8% of A hapaxes and 13.8% of B hapaxes overlap. Rare forms diverge. This is consistent with productive morphology creating diverse rare forms using dialect-specific suffix preferences (A: ch-midfix forms; B: edy-class).

3. **l, r, p are near-B-exclusive (Jaccard 0.024-0.082)**: B l (pharma F423), B r (LL-enriched F382), and B p (formula class F427) have essentially unique vocabularies. A has very few l-words (34 types, mostly hapaxes), no p-formula, and almost no r. These are B-specific grammatical classes.

4. **B-specific vocabulary is edy-class concentrated**: Top B-exclusive high-freq words are all edy-suffix words (qokeedy/qokedy/otedy/qotedy). The A/B suffix divergence (A prefers ol/or/ch-body; B prefers edy) manifests directly as vocabulary separation.

5. **cth is A-dominant with B using a subset**: B has only 16 cth types (vs A's 56), and 62.5% of B-cth types appear in A. B uses a simplified subset of A's cth vocabulary.

6. **Dialectal variant model confirmed**: A and B share core grammar and vocabulary, diverging in: (a) suffix preferences for rare words (B: edy; A: ol/ch); (b) presence/absence of B-specific classes (l, r, p); (c) vocabulary richness differences (B has 33% more word types than A despite having only 87% more tokens — B is less repetitive in rare words).

---

## Self-Audit

**Target-awareness**: No target-aware elements. Descriptive analysis.

**Feature-destroying implementation**: Standard corpus parsing. Hapax/rare tiers defined by within-dialect frequency, which is appropriate for this comparison.

**Extrapolation**: Claims confined to observed overlap statistics. The "dialectal variant" interpretation is a qualitative label — the specific mechanism (same scribal hand vs different but related system) is not testable from overlap alone.

**Negative-result scope**: N/A — positive result (confirms H_new_N).

**Control behavior**: No external control. Baseline is independent frequency tiers.

---

## Conclusion

H_new_N CONFIRMED. **F440 (new finding):** A/B vocabulary overlap is frequency-stratified: f≥20 words are 100%/82.6% shared; hapaxes are 20.8%/13.8% shared. Token coverage: 74.9% (A) / 67.7% (B) from shared word types. All 64 high-freq A words appear in B. l (Jaccard=0.082), r (0.053), p (0.024) are near-B-exclusive onset classes. B-exclusive vocabulary is edy-class dominated. Pattern is consistent with A and B being dialectal variants of a common system with shared core vocabulary and dialect-specific suffix/morphology preferences.
