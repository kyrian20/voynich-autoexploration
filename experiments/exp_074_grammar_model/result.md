# Experiment exp_074: Grammar Model — d/sh Complementarity (H097), Bigram PPL (H098), Line-Final (H099)
Date: 2026-04-09

## H097: d/sh Complementarity in Currier A vs B

### Conditional Probabilities

| Dialect | From | →ch | enr_ch | →qo | enr_qo |
|---------|------|-----|--------|-----|--------|
| **B** | **sh→** | 9.6% | **0.64×** | 36.6% | **1.97×** |
| **B** | **d→** | 19.0% | **1.27×** | 14.2% | **0.76×** |
| **A** | **sh→** | 15.8% | 0.80× | 17.2% | 1.58× |
| **A** | **d→** | 21.6% | 1.09× | 10.1% | 0.93× |
| **A** | **s→** | 26.9% | **1.36×** | 6.8% | **0.63×** |

**Currier A DOES have d/sh complementarity, but weaker than B:**
- A sh→ch: 0.80× (vs B: 0.64×) — suppression weaker
- A sh→qo: 1.58× (vs B: 1.97×) — coupling weaker
- A d→ch: 1.09× (vs B: 1.27×) — much weaker enrichment
- A d→qo: 0.93× (vs B: 0.76×) — suppression much weaker

**Critical A finding: s-onset plays the role in A that d plays in B:**
- A s→ch: 1.36× (vs A d→ch: 1.09×) — s is the stronger ch-predictor in A
- A s→qo: 0.63× (matches B d→qo: 0.76×) — s suppresses qo in A as d does in B

In Currier A, the complement of sh is **s** (not d). The A complementary structure is {sh vs s}: sh avoids ch (0.80×) and weakly prefers qo (1.58×); s prefers ch (1.36×) and avoids qo (0.63×).

### H097 Verdict: SUPPORTED — A Has Weaker d/sh Complementarity; A's True Complement of sh is s

The d/sh complementarity is cross-dialect (present in both A and B) but:
1. Both effects are weaker in A (sh→qo: 1.58× vs B 1.97×; d→ch: 1.09× vs B 1.27×)
2. In A, s-onset is the primary complement of sh (A s→ch=1.36×, s→qo=0.63×) — stronger than d in A
3. The qo-hinge mechanism is less developed in A: A sh→qo=1.58× vs B sh→qo=1.97×; A qo→ch=1.24× vs B qo→ch=1.31×

The A grammar has the same STRUCTURE as B (sh avoids ch, some class avoids qo and prefers ch) but at weaker strengths, and with s playing the "d role" in A rather than d itself.

---

## H098: Bigram vs Unigram Onset-Class Perplexity

### Results

| Dialect | Unigram PPL | Bigram PPL | PPL Reduction | Bits Reduction | Relative % |
|---------|------------|-----------|--------------|---------------|-----------|
| **B** | 8.092 | **7.012** | **1.080** | **0.207 bits** | **13.3%** |
| **A** | 8.758 | 7.957 | 0.801 | 0.138 bits | 9.1% |

**B has a 13.3% bigram improvement vs A's 9.1%.** The extra 0.069 bits/bigram in B directly quantifies B's stronger sequential grammar (primarily the sh→qo=1.97× coupling).

### H098 Verdict: SUPPORTED — B's Onset-Class Sequential Grammar Is Quantifiably Stronger Than A's

The bigram model reduces perplexity by 1.080 in B vs 0.801 in A — a 35% larger improvement for B. This is a direct measurement of the additional structural information in B's word-ordering grammar. The onset-class bigram model is a poor predictor overall (baseline PPL ~8 = 3 bits/token, bigram only improves to 7 = 2.8 bits/token) because the vocabulary is highly diverse within onset classes — but the systematic coupling effects (sh→qo, d→ch) are real and quantified.

The ~3 bits/onset-token entropy is consistent with having ~8 effective onset classes (log2(8)=3 bits), confirming that the onset-class distribution is high-entropy (all classes represented), while the bigram structure gives ~0.2 bits of predictive power.

---

## H099: Line-Final Onset Class Distribution and Penultimate Prediction

### B Last-Word Onset Distribution

| Onset | Last-word % | Baseline % | Enrichment |
|-------|------------|-----------|-----------|
| **o** | 28.9% | 23.2% | **1.25×** |
| other | 23.3% | (variable) | — |
| ch | 13.5% | 15.0% | 0.90× |
| **qo** | 11.3% | 18.6% | **0.61×** |
| d | 10.2% | 6.8% | **1.50×** |
| **sh** | 3.7% | 8.8% | **0.42×** |

**qo (0.61×) and sh (0.42×) are strongly suppressed at line-ends** — consistent with their medial roles. o-onset (1.25×) and d-onset (1.50×) are enriched at line-ends.

### A Last-Word Onset Distribution

| Onset | Last-word % | Baseline % | Enrichment |
|-------|------------|-----------|-----------|
| **d** | 25.4% | 14.7% | **1.73×** |
| o | 17.5% | 17.3% | 1.01× |
| ch | 17.2% | 19.8% | 0.87× |

In A, d-onset is strongly enriched at line-ends (25.4%, 1.73×) — consistent with the known -aiin line-end pattern (daiin appears at line ends).

### Penultimate→Last Prediction (Currier B)

| Penultimate onset | Most common last-word onset | P(qo as last) | P(o as last) |
|------------------|-----------------------------|--------------|-------------|
| **sh→** | qo (28.0%) | **28.0%** | 26.4% |
| **d→** | o (30.4%) | 8.2% | **30.4%** |
| **o→** | o (35.0%) | 10.2% | **35.0%** |
| qo→ | o (26.4%) | 12.9% | 26.4% |
| ch→ | o (24.2%) | 12.0% | 24.2% |

**sh as second-to-last word predicts qo as last word (28.0%)** — the sh→qo coupling extends to the line-ending position. When sh is second-to-last, the last word is often qo. This shows the sh-qo coupling holds even at line boundaries.

**d as penultimate predicts o as last (30.4%)** — the d→ch pathway continues: d before line-end often leads to an o-onset last word (not ch, interestingly). The last word in the d-path is more often o than ch.

### H099 Verdict: SUPPORTED

Line-final words in B are NOT randomly distributed. qo (0.61×) and sh (0.42×) are strongly suppressed; o (1.25×) and d (1.50×) are enriched. The penultimate onset class partially predicts the last-word onset:
- sh-penult → qo-last (28.0%): sh→qo coupling extends to line-final
- d-penult → o-last (30.4%): d precedes o-onset line-enders

In A, d-onset is strongly line-final (25.4%, 1.73×) — the daiin/-aiin line-end marker pattern.

---

## Combined Finding (F081)

**H097 SUPPORTED**: d/sh complementarity is cross-dialect but weaker in A. A sh→qo=1.58×, sh→ch=0.80×; B sh→qo=1.97×, sh→ch=0.64×. In A, **s-onset plays the "d role"** (A s→ch=1.36×, s→qo=0.63×) — the complement of sh in A is s, not d. **H098 SUPPORTED**: B bigram model improves 13.3% over unigram (0.207 bits); A only 9.1% (0.138 bits). B's sequential grammar is quantifiably 35% stronger than A's, directly measuring the sh→qo coupling advantage. **H099 SUPPORTED**: B line-final words are non-random: qo (0.61×) and sh (0.42×) are suppressed; o (1.25×) and d (1.50×) are enriched. The sh-penult → qo-last coupling (28.0%) shows the sh→qo rule holds at line boundaries. A line-final words are dominated by d-onset (1.73×), consistent with the -aiin line-end marker pattern.
