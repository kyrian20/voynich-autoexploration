# Experiment exp_070: k+-dy Particle (H087) + ch-ch/sh-sh Bigrams (H088)
Date: 2026-04-09

## H087: k+-dy Particle Analysis

### Setup
k+-dy words: 71 tokens, k+other-suffix: 440 tokens (Currier B)

**Top k-dy words:** kchdy(15), keody(11), keeody(4), kcheody(4), koldy(4), kshdy(3)
**Top k-other words:** keedy(34), kar(34), kaiin(32), kedy(30), kain(23)

Note: the top k-dy words are morphologically complex (k+ch/sh+dy compound forms), not simple k+dy forms. 'kedy' (30 tokens) appears in the k-other category because `suffix_group('kedy')` returns 'edy' (not 'dy') — kedy ends in -edy.

### Positional Comparison

| Position | k-dy% | Enrichment | k-other% | Enrichment |
|----------|-------|-----------|---------|-----------|
| first | 7.0% | 0.59× | 8.0% | 0.67× |
| medial | 76.1% | 1.00× | 80.9% | 1.06× |
| **last** | **16.9%** | **1.43×** | 11.1% | 0.95× |
| para_first | 4.2% | 7.02× | 2.7% | 4.53× |

k-dy words are notably **more line-final** (16.9% vs 11.1%, 1.43× enrichment) compared to k+other-suffix words (0.95× — essentially baseline). This suggests k-dy words serve as line-closing particles more than k+other words.

### Context Analysis

**Left context (word before k-dy):** k-dy preferentially follows other gallows words — k (2.79×) and t (2.63×). Sequence: gallows → k-dy.

**Right context (word after k-dy):** k-dy is followed by ch (1.79×), d (1.72×), qo (1.56×), p (2.65×). Notably, k and y **never** follow k-dy (0.00×).

The sequential pattern: [k or t] → k-dy → [ch or qo or d] — suggesting k-dy appears in a specific slot between a gallows word and a medial/content word.

### H087 Verdict: WEAKLY SUPPORTED

k-dy words are slightly more line-final (1.43×) than k+other-suffix (0.95×), suggesting a mild "closing" function. The context constraints (follows gallows, precedes ch/qo) are real but not dramatic. k-dy is not a strongly positionally-restricted particle — it's primarily a morphologically complex form (k+ch/sh+dy) that inherits some positional preferences from its components. The 7.02× para_first enrichment is unexpectedly high but based on only ~3 para_first instances (4.2% × 71 = ~3 tokens).

**Key finding**: The top k-dy forms (kchdy, keody, kcheody) are NOT simple k+dy — they contain ch/sh nuclei (kchdy = k+ch+dy, kcheody = k+che+ody). These are compound morphological forms embedding both a gallows and a ch/sh component.

---

## H088: ch-ch and sh-sh Self-Following Bigram Constructions

### Currier A

| Metric | ch→ch | sh→sh |
|--------|-------|-------|
| Rate | 26.6% (446/1678) | 13.3% (109/818) |
| Baseline (random) | 19.8% | 9.2% |
| **Enrichment** | **1.34×** | **1.46×** |

**Top ch-ch pairs in A:** "chol chol" (20), "chor chol" (8), "chol chor" (6), "chol chy" (6), "cheol chol" (4)

The dominant pattern is `chol` as the first word: chol appears in the most common ch-ch bigrams. "chol chol" with 20 occurrences is a specific repetitive construction — not just random adjacency.

**Position of second ch word in ch-ch pair:** 383/446 = 86% medial. ch-ch bigrams are almost exclusively medial constructions.

**Words before ch in A:** daiin(69), chol(67), chor(44), ol(26), or(25) — ch most commonly follows daiin and other ch-onset words.

### Currier B

| Metric | ch→ch | sh→sh |
|--------|-------|-------|
| Rate | 16.4% (477/2902) | 9.1% (164/1796) |
| Baseline (random) | 15.0% | 8.8% |
| **Enrichment** | **1.09×** | **1.04×** |

In B, self-following enrichment is near-zero (1.04-1.09×). ch-ch and sh-sh are essentially random co-occurrence in B.

**Top B ch-ch pairs:** "chedy chedy" (7), "chdy chdy" (4), "chedal chedy" (4) — low counts, no "chol chol"-equivalent dominant pair.

**CRITICAL FINDING — Words before ch in B:** qokain(86), qokaiin(78), daiin(74), ol(67), aiin(51)

**qo+gallows words are the MOST COMMON predecessors of ch-onset words in B.** qokain (86) and qokaiin (78) together precede ch more than daiin (74). This is a direct sequential constraint: in Currier B text, qo+gallows words are systematically followed by ch-onset words.

Similarly, **words before sh in B:** daiin(52), qokain(45), qokaiin(39), ol(39), qokal(31) — again, qo+gallows words are the primary predecessors of sh-onset words.

### H088 Verdict: SUPPORTED for A, NOT SUPPORTED for B

**Currier A**: ch-ch self-following is 1.34× enriched; "chol chol" (20 tokens) is a specific repeated construction. sh-sh is 1.46× enriched. The A two-word ch/sh constructions are primarily medial. This likely reflects an A grammatical pattern where paired ch/sh words form a compound phrase.

**Currier B**: Self-following is near-random (1.04-1.09×). No dominant bi-word ch construction exists. The B ch-grammar is different from A's.

**New finding (serendipitous)**: In Currier B, the word before ch is most often a qo+gallows word (qokain, qokaiin). This reveals a sequential rule in B text: **qo+gallows (medial) → ch (medial)** is the dominant word-order pattern. The sequential grammar in B is: [p-onset para-start] → [qo+gallows medial] → [ch medial] → [short suffix line-closer].

---

## Combined Finding (F077)

**H087 WEAKLY SUPPORTED**: k-dy words (top forms: kchdy, keody — morphologically complex k+ch/sh+dy compounds) are slightly more line-final (1.43×) than k+other words (0.95×), and follow gallows words (k: 2.79×, t: 2.63×). Not a clear grammatical particle — more likely a morphological subclass with mild positional preferences. **H088 SUPPORTED FOR A, NOT FOR B**: Currier A has genuine ch-ch self-following enrichment (1.34×) with "chol chol" (20 tokens) as a specific bi-word construction. B has near-random self-following (1.04-1.09×). **Serendipitous finding**: In Currier B, qo+gallows words (qokain, qokaiin) are the most common predecessors of ch-onset words (qokain→ch: 86 tokens, qokaiin→ch: 78), establishing a sequential positional grammar rule: qo+gallows → ch → [suffix] in medial position.
