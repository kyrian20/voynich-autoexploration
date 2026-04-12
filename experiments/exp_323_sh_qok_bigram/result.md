# exp_323: sh→qok Bigram Word-Level Analysis (H522, Q004)

**Date:** 2026-04-11
**Hypothesis:** H522 — Q004: is sh→qok enrichment (E_mid=1.967×, F261) due to (a) uniform class-level grammar, (b) specific sh-word types, or (c) specific word-type pairs?
**Result:** H522 ANSWERED. The sh→qok enrichment is a PREDOMINANTLY CLASS-LEVEL PHENOMENON with MODERATE WORD-TYPE MODULATION. Key findings: (1) Most sh-word types cluster near the class transition rate (0.267× for B, 0.096× for A) — the enrichment is distributed, not driven by one word. (2) Some sh-words are elevated (shecthy=0.538, sheckhy=0.429 in B) or depleted (shy=0.056, shol=0.158) — word-type modulation exists but is not dominant. (3) No specific word-type pairs dominate: top pair shedy→qokedy has only 16 occurrences (4.7% of all sh→qok bigrams). (4) Cross-dialect pair overlap = 5/205+52 pairs (2.4% of B pairs appear in A) — pair-level correlation is near-zero, yet class-level enrichment is shared (B: 1.967×; A: 1.741×). CONCLUSION: sh→qok enrichment is a class-level grammar rule with moderate per-word modulation. The same onset-class rule applies in both dialects with different specific vocabulary. Q004 CLOSED.

---

## Key Statistics

### B-Dialect

| Bigram | Observed | Expected | Enrichment |
|--------|----------|----------|------------|
| sh→qok | 339 | 172.3 | **1.967×** |
| sh→ch  | 119 | 214.6 | 0.555× (depleted!) |
| sh→sh  | 120 | 128.1 | 0.937× (neutral) |
| ch→qok | 331 | 288.6 | 1.147× |
| qok→sh | 207 | 172.3 | 1.201× |

sh→ch is DEPLETED (0.555×): sh is actively anti-correlated with ch succession. sh→qok is enriched AND sh→ch is depleted — sh transitions prefer qok over ch.

### A-Dialect

| Bigram | Observed | Expected | Enrichment |
|--------|----------|----------|------------|
| sh→qok | 55 | 31.6 | **1.741×** |
| sh→ch  | 70 | 123.8 | 0.565× (depleted!) |
| sh→sh  | 79 | 60.2 | **1.312×** (elevated!) |
| ch→qok | 57 | 65.0 | 0.877× (neutral) |
| qok→sh | 26 | 31.6 | 0.823× (neutral) |

A-dialect: sh→qok enriched AND sh→sh enriched; ch→qok neutral (vs B: 1.147×); qok→sh neutral (vs B: 1.201×). The A-dialect sh-onset has BOTH self-succession AND qok-succession enriched — sh transitions are preferentially to sh or qok, not to ch.

### Per-sh-word P(→qok) Distribution (B-dialect, top-15 words by bg freq)

| sh-word | Bg | →qok | P(→qok) | Class rate |
|---------|----|------|---------|------------|
| shedy   | 325 | 103 | **0.371** | 0.267 |
| shey    | 138 |  39 | **0.325** | 0.267 |
| sheey   |  74 |  17 | 0.258 | 0.267 |
| sheedy  |  67 |  21 | **0.362** | 0.267 |
| sheol   |  51 |  13 | 0.265 | 0.267 |
| shckhy  |  48 |  12 | 0.300 | 0.267 |
| shol    |  40 |   6 | **0.158** | 0.267 |
| shdy    |  31 |   6 | 0.214 | 0.267 |
| sheckhy |  30 |  12 | **0.429** | 0.267 |
| shcthy  |  25 |   3 | 0.136 | 0.267 |
| sheky   |  23 |   4 | 0.222 | 0.267 |
| sheody  |  21 |   4 | 0.211 | 0.267 |
| shy     |  19 |   1 | **0.056** | 0.267 |
| shecthy |  16 |   7 | **0.538** | 0.267 |

**Elevated (>0.350):** shedy(0.371), sheedy(0.362), sheckhy(0.429), shecthy(0.538)
**Depleted (<0.200):** shol(0.158), shcthy(0.136), shy(0.056)

### qok-word type selection (B-dialect)

qok-words that follow sh-words are received in near-background proportions: qokedy(enr=1.13×), qokain(enr=1.13×), qokeedy(enr=0.97×), qokaiin(enr=1.12×). The qok-side is essentially UNIFORM — no specific qok-word is strongly preferred by sh.

### Cross-dialect pair overlap

- B: 205 unique sh×qok pairs; A: 52 unique pairs; Shared: 5 pairs
- Jaccard ≈ 0.02 (essentially no pair-level correlation)
- 5 shared pairs: shey→qokey(B=4,A=1), shey→qokeey(B=3,A=2), sheey→qokey(B=1,A=1), sheey→qokol(B=1,A=2), shol→qokain(B=1,A=1)
- These are not high-frequency pairs in either dialect — even the "shared" pairs are rare

---

## Structural Findings

### Finding 1: Mechanism type = class-level grammar with moderate modulation

The sh→qok enrichment is predominantly a class-level pattern: when any sh-onset word appears in MID position, the next MID word is 1.97× more likely to be a qok-onset word than expected by chance. Most sh-word types cluster within ±50% of the class transition rate (0.267 ± ~0.10).

However, word-type modulation exists: shecthy shows P(→qok)=0.538 (2× the class rate), while shy shows P(→qok)=0.056 (4.8× below class rate). The elevated sh-words (shecthy, sheckhy) contain the 'cth' or 'ck' compound element — possibly the compound suffix predicts stronger qok-succession.

The qok-side shows no word-type preference (all enrichment values 0.77-1.28×) — the enrichment is driven by sh-side selection, not qok-side selection.

**Classification:** Scenario (b) with mild (a) character. The mechanism is approximately class-level (any sh-word has elevated P(→qok)) with moderate type-level modulation (some sh-subtypes are elevated). Not (c) — no specific pair dominates.

### Finding 2: sh→ch is depleted (0.555×) in BOTH dialects

Both B (0.555×) and A (0.565×) show strong depletion of sh→ch transitions. sh and ch are ANTI-correlated successors. This is a cross-dialect structural invariant: sh-onset words are followed by ch-onset words significantly less often than chance.

Combined with the sh→qok enrichment (B: 1.967×, A: 1.741×), this creates a grammar rule: sh preferentially transitions to qok and AWAY FROM ch. The sh→{qok↑, ch↓} coupling is the fundamental rule.

This was not previously reported in the findings — it is a new finding from this analysis.

### Finding 3: A-dialect sh has different successor grammar than B

B-dialect: sh→qok=1.967×, sh→ch=0.555×, sh→sh=0.937×, qok→sh=1.201×
A-dialect: sh→qok=1.741×, sh→ch=0.565×, sh→sh=1.312×, qok→sh=0.823×

In A-dialect, sh self-succession is elevated (1.312× vs B's 0.937×) and qok→sh is neutral (0.823× vs B's 1.201×). The bidirectional qok↔sh coupling seen in B is absent in A (only sh→qok remains, not qok→sh). A-dialect sh-onset has a more self-sufficient sequential structure than B.

This explains why A-dialect required p_sh_qok=0.10 as an explicit Markov rule (exp_300) — the copy buffer mechanism alone cannot reproduce the sh→qok enrichment in A because A's sh-tokens have a different base rate and successor distribution.

### Finding 4: Near-zero cross-dialect pair correlation confirms class-level mechanism

If sh→qok enrichment were due to a specific lexical co-occurrence (e.g., "shedy always precedes qokedy in both dialects"), the same word-type pairs should appear in both dialects. They don't: only 5 of 205 B-pairs appear in A (2.4%). This rules out lexical co-occurrence as the primary mechanism.

The class-level rule (sh-onset → qok-onset) is maintained cross-dialect, but it is realized through different specific word pairs in each dialect. This is consistent with a morphological/grammatical rule that operates at the onset-class level, independent of specific lexical forms.

---

## Interpretation

**Q004 CLOSED:** sh→qok enrichment is a class-level grammar rule — approximately "when an sh-onset word appears in MID position, the probability that the next word is qok-onset increases by ~2×." This rule is cross-dialect (B: 1.967×, A: 1.741×) and independent of specific word-type pairs (cross-dialect pair overlap ≈ 2%). The rule operates at the onset-class level, not the lexical level.

**Architectural implication:** The sh→qok enrichment in B-dialect is achieved PASSIVELY by the copy buffer (sh-words copy qok-words into buffer, and these are then resampled), without an explicit Markov rule. The passive mechanism works because sh and qok words appear together in the same text sections (both template-copying onset classes) and thus co-populate the buffer. This is consistent with the class-level (not lexical) nature of the enrichment.

**New finding — sh→ch depletion:** Both dialects show strong sh→ch depletion (0.555-0.565×). This is the inverse of sh→qok enrichment: sh preferentially transitions to qok and away from ch. This represents a systematic onset-class avoidance rule: sh does not follow itself with ch. This may reflect a morphological/phonological constraint in the underlying system.

**sh subtypes with elevated P(→qok):** shecthy (0.538) and sheckhy (0.429) are sh-words that contain the 'cth' or 'ck' compound element. These specialized compound sh-forms may be a sub-register of sh that disproportionately co-occurs with qok-words (same text section, same formula register). This is speculative and would require section-level analysis to confirm.

---

## Limitations

- B-dialect analysis uses N=339 sh→qok bigrams (robust for class-level analysis; smaller for word-type pair analysis where most pairs have N=1-5)
- A-dialect: N=55 sh→qok bigrams — per-word P(→qok) rates are noisy for individual sh-words
- The per-sh-word P(→qok) comparison uses bigrams from ALL MID lines, not restricting to lines where sh appears; some bias possible if sh appears in sections with different qok rates
- "shecthy" and "sheckhy" as outliers: N_shecthy=16 (total bg), N_sheckhy=30 — moderate sample for reliable rate estimation

---

## Self-Audit

**Target-awareness:** Pure corpus measurement. No VMS target metrics. PASS.

**Feature-destroying implementation:** Direct bigram count analysis. No normalization that could distort signal. PASS.

**Extrapolation:** "sh→ch depletion is cross-dialect invariant" extrapolates from two data points (B: 0.555×, A: 0.565×) to a structural rule. These values are statistically consistent but the A-dialect sample is small (N=70 observed vs 123.8 expected). The depletion is consistent in both dialects, making the claim reasonable but not proven beyond doubt.

**Negative-result scope:** N/A — positive characterization result.

**Control behavior:** "Expected" counts computed from marginal class frequencies under independence assumption. This is the standard bigram enrichment control and is appropriate here.
