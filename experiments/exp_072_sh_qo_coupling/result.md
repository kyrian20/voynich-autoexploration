# Experiment exp_072: sh→qo Coupling (H092) + Currier A Sequential Grammar (H091, H093)
Date: 2026-04-09

## H092: sh→qo Coupling Analysis in Currier B

### sh→qo Rate by Section

| Section | sh→qo | sh total | P(qo|sh) | Baseline qo% | Enrichment |
|---------|-------|----------|----------|-------------|-----------|
| Bio | 275 | 585 | **47.0%** | 26.0% | **1.81×** |
| Herbal | 47 | 227 | 20.7% | 10.5% | **1.97×** |
| Special | 258 | 713 | 36.2% | 18.0% | **2.01×** |
| Text | 64 | 193 | 33.2% | 16.2% | **2.05×** |
| Cosmo | 10 | 57 | 17.5% | 12.2% | **1.44×** |
| Astro | 3 | 21 | 14.3% | 6.5% | **2.20×** |

Enrichment ranges from 1.44× (Cosmo) to 2.20× (Astro) — **consistent across ALL sections**. The sh→qo coupling is not driven by one section; it is a universal Currier B grammar feature.

### P(qo next) After Each Onset Class

| From onset | n_qo_next | n_total | P(qo\|X) | Baseline (18.6%) | Ratio |
|-----------|-----------|---------|----------|-----------------|-------|
| **sh→** | 657 | 1796 | **36.6%** | 18.6% | **1.97×** |
| ch→ | 628 | 2902 | 21.6% | 18.6% | 1.16× |
| qo→ | 822 | 3732 | 22.0% | 18.6% | 1.18× |
| o→ | 709 | 4272 | 16.6% | 18.6% | 0.89× |
| d→ | 172 | 1214 | 14.2% | 18.6% | **0.76×** |

sh is the STRONGEST predictor of the next word being qo (1.97×). d-onset words SUPPRESS the next qo (0.76×) — d and qo are in opposite sequential niches.

### Top sh→qo Bigrams

"shedy qokedy" (18), "shedy qokaiin" (17), "shedy qokeedy" (13), "shey qokain" (13), "shedy qokeey" (12), "shedy qokain" (10), "sheedy qokeedy" (8)

All top sh→qo pairs involve **shedy or shey** as the sh-word, followed by a **qok-** form. The coupling is: {shedy/shey} → {qokain/qokaiin/qokedy/qokeedy/qokeey}.

### H092 Verdict: STRONGLY SUPPORTED

sh→qo is a genuine Currier B grammatical coupling (~2× enrichment, uniform across all sections). The specific construction is: shedy/shey → qok+{aiin/ain/edy/eedy/eey}. This is a tight bi-word construction where the sh-word (extended edy/ey suffix) is systematically followed by a qo+k-form.

The sh-qo coupling, combined with the qo→ch coupling (19.6%), creates the B medial alternation loop: **...sh → qo → ch → qo → sh...** with qo as the sequential "hinge" between sh and ch words.

---

## H091/H093: Currier A Sequential Grammar

### A Onset Transition Matrix

| From→ | ch | sh | qo | o | d | ch self |
|-------|----|----|----|----|---|---------|
| **p→** | **23.9%** | 22.9% | 12.8% | 16.5% | 9.2% | — |
| **ch→** | **26.6%** | 7.4% | 8.2% | 15.4% | 16.0% | self: 1.34× |
| **sh→** | 15.8% | **13.3%** | **17.2%** | 14.3% | 10.1% | — |
| **qo→** | **24.6%** | 7.6% | 14.3% | 17.0% | 14.8% | — |
| **d→** | 21.6% | 9.6% | 10.1% | 15.2% | **18.1%** | — |
| **o→** | 22.6% | 9.9% | 8.9% | **22.1%** | 14.0% | — |

The A transition matrix is remarkably **FLAT**. The largest enrichment is ch→ch self-following (26.6% vs baseline 19.8% = 1.34×). No single transition reaches >1.35× enrichment.

### P(ch next) After Each Onset Class in A

| From onset | P(ch\|X) | Ratio vs baseline (19.8%) |
|-----------|----------|--------------------------|
| ch→ | 26.6% | **1.34×** |
| k→ | 25.9% | **1.31×** |
| qo→ | 24.6% | **1.24×** |
| p→ | 23.9% | 1.20× |
| o→ | 22.6% | 1.14× |
| d→ | 21.6% | 1.09× |
| sh→ | 15.8% | **0.80×** |

In Currier A, ch follows all onset classes at roughly equal rates (~20-26%). The ONLY notable patterns:
- **ch→ch self-following: 1.34×** (confirmed F077 "chol chol" construction)
- **sh→ch is SUPPRESSED: 0.80×** — sh words do NOT precede ch in A (opposite of B: in B, d→ch is suppressed 0.76×, not sh)

### What Follows sh in A?

After sh in A: qo (17.2%), ch (15.8%), o (14.3%), sh (13.3%), d (10.1%)

**sh→qo enrichment in A: 17.2% / 11% baseline ≈ 1.56×** — A also has sh→qo coupling, but much weaker than B (1.56× vs 1.97×). In A, sh→ch is stronger than in B (15.8% vs 9.6% in B).

### Top Predecessors of ch in A (by section)

| Section | Top 5 predecessors |
|---------|-------------------|
| Herbal (H) | ch (24.3%), o (15.3%), qo (12.0%), d (11.8%), other (8.1%) |
| Pharma (P) | ch (23.6%), o (20.6%), qo (15.8%), d (14.6%), y (5.8%) |
| Special (S) | o (28.2%), ch (19.4%), qo (15.5%), y (8.7%), d (7.8%) |

In all A sections, the dominant ch predecessor is **ch itself** (self-following) or **o-onset words** (not daiin specifically). There is no A-specific predecessor class analogous to B's sh→qo coupling.

### H091/H093 Verdict: SUPPORTED — A and B Have Structurally Different Sequential Grammars

Currier A has NO dominant predecessor class for ch analogous to B's sh→qo coupling. The A sequential grammar is:
- **Flat transitions**: no single transition exceeds 1.34×
- **ch→ch self-following**: the only notable enrichment (1.34×), creating the "chol chol" type construction
- **sh→ch suppressed** (0.80×): opposite of B where d→ch is suppressed
- **sh→qo weakly present** (1.56×): A also has this coupling but at half the strength of B (1.97×)

The A and B sequential grammars are fundamentally different:
- **B**: tight sh↔qo alternation (sh→qo=1.97×, qo→ch=1.05×); qo is the "hinge" morpheme
- **A**: flat transitions; ch→ch self-following (1.34×) is the only structure; no qo-hinge function

This is a new dimension of A/B distinction beyond morphology (suffix paradigm) and onset positional grammar: **the word-to-word sequential coupling rules are different**.

---

## Combined Finding (F079)

**H092 STRONGLY SUPPORTED**: sh→qo coupling is ~2× enriched across ALL Currier B sections (1.44-2.20×). The specific construction: shedy/shey → qok+suffix. This is a universal B grammatical coupling, not a section artifact. sh is the STRONGEST predictor of qo following (1.97×); d suppresses qo following (0.76×). **H091/H093 SUPPORTED**: Currier A has NO dominant predecessor class for ch comparable to B's sh→qo coupling. A's transition matrix is flat; ch→ch self-following (1.34×) is the only notable sequential effect. A also has weak sh→qo coupling (1.56×) — a cross-dialect shared feature but much weaker. The A/B sequential grammar distinction: B uses qo as a sequential "hinge" between sh and ch words; A lacks this qo-hinge function and has flat inter-word coupling.
