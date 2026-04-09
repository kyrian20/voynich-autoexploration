# Experiment exp_075: A Grammar by Section (H100, H102, H103, H104)
Date: 2026-04-09

## H100: A {sh vs s} Complementarity Is Section-Sensitive

### Results by A Section

| Onset | Herbal A sh→qo | Pharma A sh→qo | Herbal A s→ch | Pharma A s→ch |
|-------|---------------|---------------|--------------|--------------|
| sh→ch | 0.90× | **0.36×** | — | — |
| sh→qo | 1.27× | **2.44×** | — | — |
| s→ch  | — | — | 1.26× | **1.64×** |
| s→qo  | — | — | 0.66× | **0.54×** |

**Pharma A has a MUCH stronger {sh vs s} complementarity than Herbal A:**
- Pharma A sh→qo = **2.44×** (vs Herbal A: 1.27×; vs B global: 1.97×)
- Pharma A sh→ch = **0.36×** (vs Herbal A: 0.90×; vs B: 0.64×)
- Pharma A s→ch = **1.64×** (vs Herbal A: 1.26×)
- Pharma A s→qo = **0.54×** (vs Herbal A: 0.66×)

**Pharma A sh→qo coupling (2.44×) is STRONGER than Currier B's (1.97×).** The Pharma A section has a more fully developed sequential grammar than even the rest of A. In Pharma A, sh behaves similarly to how sh behaves in B — strongly qo-coupled and ch-avoiding — while Herbal A has a much weaker version.

### H100 Verdict: STRONGLY SUPPORTED — A {sh vs s} Complementarity Is Section-Sensitive

The complementarity is dramatically stronger in Pharma A than Herbal A. Pharma A has the strongest sh→qo coupling of any A section (2.44× vs Herbal A 1.27×) — exceeding even B's 1.97×. This suggests Pharma A may share a sequential grammar structure closer to B than Herbal A does.

---

## H102: A Dominant Onset-Class Trigram Structure

### Top A Onset-Class Trigrams (Count ≥ 20, Sorted by Enrichment)

| Trigram | Count | Enrichment |
|---------|-------|-----------|
| **sh→sh→sh** | 20 | **3.89×** |
| sh→qo→other | 22 | 3.00× |
| sh→qo→qo | 20 | 2.75× |
| other→other→other | 24 | 2.71× |
| qo→qo→qo | 22 | 2.54× |
| **qo→qo→ch** | 40 | **2.54×** |
| ch→ch→k | 25 | 2.43× |
| sh→qo→o | 28 | 2.42× |
| s→ch→ch | 20 | 2.38× |
| ch→k→ch | 23 | 2.24× |
| **ch→ch→ch** | 107 | **2.05×** |

**ch→ch→ch is the dominant A trigram by count (107 tokens, 2.05×).** This is a much stronger structure than any B trigram of similar type, confirming that the ch→ch self-following rule extends to triplets.

**sh→qo→* chains are enriched in A (2.42-3.00×):** sh→qo→o (2.42×), sh→qo→qo (2.75×), sh→qo→other (3.00×). The A sh-qo link leads to diverse continuations (not back to ch, unlike B's qo→ch loop).

**s→ch→ch (2.38×):** The s→ch coupling extends to triplets — s predicts ch, which then self-follows. This confirms the A grammar rule: s → ch → ch.

**qo→qo→ch (2.54×):** A has a qo self-loop that leads to ch — a weaker version of B's qo→ch→qo alternation.

### B Comparison (Dominant Enriched Trigrams)

| Trigram | Count | Enrichment |
|---------|-------|-----------|
| p→sh→qo | 30 | **6.14×** |
| s→sh→qo | 35 | **4.81×** |
| t→sh→qo | 25 | 3.70× |
| d→sh→qo | 63 | 3.43× |
| **sh→qo→sh** | 80 | **3.40×** |
| **sh→qo→ch** | 135 | **3.35×** |
| qo→sh→qo | 159 | 3.18× |
| **qo→ch→qo** | 198 | **2.31×** |

**B's dominant structure is sh→qo→* (with all onset classes preceding sh→qo)** — the qo-hinge is central. B's main loop is qo↔ch↔qo via sh (qo→sh→qo: 3.18×, sh→qo→ch: 3.35×).

**A's dominant structure is ch→ch→ch** — A has a ch-repetition grammar, not a qo-hinge grammar. A's sh-qo chains (sh→qo→o, sh→qo→qo) don't cycle back to ch as strongly as B does.

### H102 Verdict: SUPPORTED — A Has ch→ch→ch as Dominant Trigram Structure; B Has sh→qo→* Loop

A's dominant enriched trigram is ch→ch→ch (107 tokens, 2.05×). B's dominant structure is sh→qo→ch/sh (>3×). The two dialects have qualitatively different trigram grammars: A uses ch repetition; B uses sh→qo oscillation. A does have sh→qo→* enrichment (2.42-3.00×) but it's weaker and doesn't return to ch the way B does.

---

## H103: Sequential Grammar Differs Between A Registers

### Bigram PPL Reduction by A Register

| Register | Tokens | Unigram PPL | Bigram PPL | Reduction |
|---------|--------|------------|-----------|-----------|
| A global | 9,807 | 8.758 | 7.957 | **9.1%** |
| **Aiin-dominant** | 1,700 | 8.788 | 7.673 | **12.7%** |
| Y-dominant | 5,117 | 8.842 | 7.939 | **10.2%** |

**Aiin-dominant Herbal A has a 12.7% bigram PPL reduction — much closer to B's 13.3% than y-dominant A's 10.2%.** The aiin-dominant register has quantifiably stronger sequential grammar.

### Key Complementarity Differences Between Registers

| Onset | Aiin-dom sh→qo | Y-dom sh→qo | Aiin-dom s→ch | Y-dom s→ch |
|-------|---------------|-------------|--------------|-----------|
| sh→ch | 0.86× | 0.92× | — | — |
| sh→qo | 1.10× | 1.29× | — | — |
| s→ch  | — | — | **1.76×** | 1.06× |
| s→qo  | — | — | 0.88× | 0.61× |

**Paradox in aiin-dom:** sh→qo is only 1.10× in aiin-dom vs 1.29× in y-dom. However, aiin-dom has:
- d→qo = **1.55×** (aiin-dom) vs **0.81×** (y-dom) — d-onset actually PREFERS qo in aiin-dom
- s→ch = **1.76×** (aiin-dom) vs 1.06× (y-dom) — s is a much stronger ch-predictor in aiin-dom
- qo→ch = **1.72×** (aiin-dom) vs 1.15× (y-dom) — qo→ch coupling much stronger in aiin-dom

The aiin-dominant register's sequential grammar is different in character from y-dominant: aiin-dom has a stronger qo→ch link (1.72×) and s→ch link (1.76×), while y-dom has a stronger sh→qo link (1.29×). The two registers use *different pathways* to ch.

### H103 Verdict: SUPPORTED — A Registers Have Different Sequential Grammar Pathways

The aiin-dominant register has stronger overall sequential grammar (12.7% PPL reduction vs y-dom 10.2%). The two registers use different mechanisms: aiin-dom favors qo→ch (1.72×) and s→ch (1.76×) pathways; y-dom favors sh→qo (1.29×). The aiin-dom d→qo=1.55× (opposite to B's d→qo=0.76×) is a critical finding: in the aiin-dominant register, d-onset *leads to* qo (not away from it, as in B).

---

## H104: B Line-Final Onset Distribution Is Largely Universal Across Sections

### B Last-Word Onset Enrichment by Section

| Section | n | qo | sh | o | d | ch |
|---------|---|----|----|---|---|----|
| **S** (Special) | 1084 | 0.61× | 0.34× | 1.15× | 0.85× | 1.12× |
| **B** (Bio) | 745 | 0.89× | 0.44× | 1.28× | **1.76×** | 0.58× |
| **H** (Herbal) | 377 | 0.29× | 0.52× | 1.37× | **2.44×** | 0.95× |
| **T** (Text) | 198 | 0.38× | 0.69× | 1.37× | **1.77×** | 0.74× |
| **C** (Cosmo) | 107 | 0.35× | 0.53× | 1.09× | **1.91×** | 1.06× |
| **A** (Astro) | 56 | 0.10× | 0.00× | 1.39× | **2.87×** | 0.59× |

**Universal B line-final patterns (all sections):**
- qo is ALWAYS suppressed at line-ends (0.10-0.89×) — even in Bio (0.89×) where qo is vocabulary-dominant
- sh is ALWAYS suppressed at line-ends (0.00-0.69×)
- o-onset is ALWAYS enriched at line-ends (1.09-1.39×)
- d-onset is enriched in 5/6 sections (1.76-2.87×), **except Special (0.85×)**

**Special section exception:** d-onset is NOT enriched at line-ends in the Special section (0.85× — slight suppression). "other" onset is 2.03× enriched in Special. Special section has a different line-final grammar from all other B sections.

**Herbal B d-dominance at line-ends (2.44×) rivals A's line-final d pattern (1.73×)**. Both dialects show d-onset enrichment at line-ends, but the effect is stronger in non-bio B sections.

### H104 Verdict: SUPPORTED — B Line-Final Grammar Is Universal Except Special Section

qo and sh suppression at line-ends is universal across ALL B sections. d-enrichment at line-ends holds for 5/6 sections (exceptions: Special section only). o-enrichment is universal. The Special section has anomalously high "other" at line-ends (2.03×) and doesn't show d-enrichment — suggesting Special section has a distinct line-final marker class.

---

## Combined Finding (F082)

**H100 STRONGLY SUPPORTED**: A {sh vs s} complementarity is dramatically section-sensitive. Pharma A sh→qo=2.44× (STRONGER than B's 1.97×!), sh→ch=0.36× (stronger suppression than B's 0.64×), s→ch=1.64×. Herbal A has much weaker coupling (sh→qo=1.27×). **Pharma A has a more fully B-like sequential grammar than Herbal A.** **H102 SUPPORTED**: A's dominant trigram is ch→ch→ch (107 tokens, 2.05×); B's dominant enriched trigrams are sh→qo→ch/sh (>3×). A has ch-repetition grammar; B has sh→qo oscillation grammar. A sh→qo chains (2.42-3.00×) don't cycle back to ch as B does. **H103 SUPPORTED**: Aiin-dominant Herbal A has stronger sequential grammar (12.7% PPL reduction) than y-dominant (10.2%), approaching B's 13.3%. The two registers use different ch-pathways: aiin-dom favors qo→ch (1.72×) and s→ch (1.76×); y-dom favors sh→qo (1.29×). Critical: aiin-dom d→qo=1.55× (OPPOSITE to B's 0.76×) — d leads to qo in aiin-dom, not away from it. **H104 SUPPORTED (universal except Special)**: B line-final qo (0.10-0.89×) and sh (0.00-0.69×) suppression is universal across all sections; o enrichment (1.09-1.39×) is universal; d enrichment (1.76-2.87×) holds for 5/6 sections. Special section is the exception: no d-enrichment, high "other" onset (2.03×) at line-ends.
