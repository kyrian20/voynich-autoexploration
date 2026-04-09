# Experiment exp_073: Medial Trigrams (H095) + d→qo Suppression (H094) + daiin Predecessor (H096)
Date: 2026-04-09

## H094: d→qo Suppression and Complementary Sequential Slots

### Conditional Probabilities: P(ch|X) and P(qo|X) by Onset Class in B

| From onset | P(ch\|X) | enr_ch | P(qo\|X) | enr_qo |
|-----------|----------|--------|----------|--------|
| **d→** | **19.0%** | **1.27×** | 14.2% | **0.76×** |
| **sh→** | 9.6% | **0.64×** | **36.6%** | **1.97×** |
| qo→ | 19.6% | **1.31×** | 22.0% | 1.18× |
| k→ | 17.8% | 1.18× | 18.7% | 1.00× |
| o→ | 17.0% | 1.13× | 16.6% | 0.89× |
| ch→ | 16.4% | 1.09× | 21.6% | 1.16× |
| s→ | 17.9% | 1.19× | 10.6% | **0.57×** |
| **p→** | 8.6% | **0.57×** | 15.1% | 0.81× |

**d and sh are in PERFECT COMPLEMENTARY sequential roles:**
- **sh**: avoids ch (0.64×) → prefers qo (1.97×)
- **d**: prefers ch (1.27×) → avoids qo (0.76×)

**s also suppresses qo** (0.57×) — s-onset and d-onset are the two classes that avoid being followed by qo.

**Two paths to ch in B medial grammar:**
1. **sh → qo → ch** (indirect path: sh avoids ch directly, but sh→qo→ch via the qo hinge)
2. **d → ch** (direct path: d leads directly to ch at 1.27×)

What follows d: o(274), **ch(231)**, sh(181), qo(172)
What precedes d: qo(230), o(208), **ch(199)**

d is sandwiched between qo/o (before) and ch/sh (after). The d-onset words appear at the midpoint between a qo prefix and a ch-onset word.

### H094 Verdict: STRONGLY SUPPORTED — d and sh are Perfect Complements

d directly precedes ch (1.27×) and avoids qo (0.76×). sh avoids ch (0.64×) and prefers qo (1.97×). This creates two grammatically distinct pathways to ch-onset words in B medial text:
1. sh → qo → ch (with qo as intermediary)
2. d → ch (direct)

The B medial grammar is more complex than previously understood. The "qo hinge" (sh→qo→ch) is ONE path; there is also a direct d→ch path. Both contribute to ch-onset word transitions. The suppression of qo after d (0.76×) and s (0.57×) means these classes bypass the qo hinge and connect directly to ch.

---

## H095: Medial Trigram Structure

### Key Statistics

- Total B trigram types: 16,424
- qo+ch trigrams: **667 tokens, 663 types** (99.4% unique!)
- qo+sh trigrams: **360 tokens, 355 types** (98.6% unique!)
- sh+qo+ch trigrams: **135 tokens, 131 types** (97.0% unique!)

**Top qo+ch+X trigrams** (max count = 2): "qol cheey chey" (2), "qokaiin chedy qokeedy" (2)
**Top qo+sh+X trigrams** (max count = 2): "qokar shedy shedy" (2), "qokar shedy qokain" (2)

### Third Word After qo+ch

| Next onset | Count | % |
|-----------|-------|---|
| **qo** | 198 | **29.7%** |
| o | 130 | 19.5% |
| ch | 112 | 16.8% |
| other | 99 | 14.8% |
| d | 41 | 6.1% |

After qo+ch, the next word is most often **qo again (29.7%)** — confirming the qo↔ch alternation loop.

### H095 Verdict: STRONGLY REFUTED at the Word Level, CONFIRMED at the Class Level

The medial three-slot structure (qo+ch/sh+word) operates at the **onset-class level** but is **completely free at the word level** — 99.4% of specific qo+ch+word trigrams are unique. The sequential grammar constrains which onset CLASS follows which, but within each class, any word may appear. This is consistent with natural language syntax: grammatical structure exists at the category level (noun phrase, verb phrase) but vocabulary within categories is essentially unconstrained.

**Critical implication**: Voynichese has grammatical structure at the onset-class level (sequential constraints like sh→qo: 1.97×, qo→ch: 1.31×) but lexical freedom at the word level (specific trigrams are near-unique). This is structurally consistent with a natural language where the "words" within grammatical categories can vary freely.

---

## H096: daiin Specifically as ch-Predecessor in A

### Results

| Predecessor | P(ch next) | Ratio vs baseline (19.8%) |
|------------|-----------|--------------------------|
| daiin | 21.0% (69/328) | **1.06×** |
| other d-words | 21.8% (157/719) | **1.10×** |
| all d-words | ~21.5% | ~1.09× |

By section:
- Herbal A: P(ch|daiin) = 22.2% (1.07×)
- Pharma A: P(ch|daiin) = 18.8% (0.98×)

daiin→sh in A: 7.9% (0.87× baseline sh-rate: 9.2%).

### H096 Verdict: NOT SUPPORTED

daiin is NOT specifically enriched as a ch-predecessor. P(ch|daiin)=21.0% (1.06×) vs P(ch|other-d)=21.8% (1.10×). The d-class enrichment for ch-following (~1.09×, well below the B d→ch of 1.27×) is uniformly distributed across all d-words in A. daiin appears before ch at the rate expected for a high-frequency d-class word. There is no daiin-specific sequential grammar role.

---

## Combined Finding (F080)

**H094 STRONGLY SUPPORTED**: d and sh are in perfect complementary sequential roles in Currier B: sh avoids ch (0.64×) and prefers qo (1.97×); d prefers ch (1.27×) and avoids qo (0.76×). The B medial grammar has TWO paths to ch: (1) sh → qo → ch (indirect) and (2) d → ch (direct). s-onset also suppresses qo (0.57×), joining d in the "direct-to-ch" class. This creates a complete sequential grammar for B medial text: {sh/ch} words → qo words → {ch/sh} words (with d providing a direct bypass). **H095 STRONGLY REFUTED AT WORD LEVEL**: Specific medial trigrams (qo+ch+X, qo+sh+X) are 99.4% unique — the sequential grammar operates at onset-class level only, not word level. The text has grammatical structure in onset sequences but complete lexical diversity in word choices. This is structurally consistent with natural language. **H096 NOT SUPPORTED**: daiin specifically shows no elevated ch-predecessor role (1.06× — near baseline). The d-class ch-enrichment (1.27× in B, ~1.10× in A) is uniformly distributed across all d-words.
