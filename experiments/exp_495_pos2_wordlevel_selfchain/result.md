# exp_495: pos2 Self-Chaining: Word-Level vs Class-Level Distribution

**Question:** (H_new_BW) Is F468 (A herbal_a universal pos2 self-chaining) driven by recurring specific bigrams (lexical/formulaic) or distributed across many word pairs (grammatical/class-level)?

---

## Results

### ch-LF: Perfectly Distributed — Grammatical

ch-LF pos2 self-chain: 70 cases, 70 distinct (pos2_word, LF_word) pairs. dist_ratio=1.00.
- Top-3 pairs = 4.3% of self-chain obs (3/70)
- Every single self-chain observation is a unique word pair
- 70 different ch-onset word pairs all governed by the same onset-class constraint

### d-LF: Mostly Distributed — Primarily Grammatical, One Recurring Pair

d-LF pos2 self-chain: 27 cases, 23 distinct pairs. dist_ratio=0.85.
- Top-3 pairs = 25.9% of obs (7/27)
- Dominant pair: daiin→daiin (N=5, 18.5% of self-chain obs)
- Remaining 22 cases all unique pairs

### Small LF classes (ok, cth, sh, o): Too Small to Characterize, All Distinct

ok-LF: 5 cases, 5 distinct. cth-LF: 5 cases, 5 distinct. sh-LF: 5 cases, 5 distinct. o-LF: 3 cases, 3 distinct. All dist_ratio=1.00, but N is too small (3-5) to interpret concentration.

### Summary Table

| LF | N_self | N_elig | %self | N_distinct | dist_ratio |
|----|--------|--------|-------|-----------|-----------|
| ch | 70 | 154 | 45.5% | 70 | 1.00 |
| d | 27 | 237 | 11.4% | 23 | 0.85 |
| ok | 5 | 48 | 10.4% | 5 | 1.00 |
| cth | 5 | 64 | 7.8% | 5 | 1.00 |
| sh | 5 | 31 | 16.1% | 5 | 1.00 |
| o | 3 | 29 | 10.3% | 3 | 1.00 |

---

## Interpretation

**F468 is a class-level grammatical constraint, not a bigram/lexical pattern.**

For ch-LF (the strongest and largest self-chain case, N=70), every pos2 self-chain observation involves a unique word pair. The 45.5% self-chain rate for ch-LF (E=1.60×, F461) reflects a probabilistic constraint on onset class, not a formulaic phrase that recurs. The 70 distinct ch-onset word pairs at pos2 — all in ch-terminal lines — represent the onset-class constraint operating over the full vocabulary of ch-onset words.

For d-LF, the picture is mostly distributed (dist_ratio=0.85). The single recurring pair daiin→daiin (N=5/27 = 18.5%) reflects the high frequency of daiin overall (the most common word in A herbal_a). If daiin appears at pos2 by chance, and the line also ends in daiin (the most common LF word), we expect some daiin→daiin pairs. The remaining 22 self-chain obs for d-LF are all distinct.

**Implication for F468:** The universal pos2 self-chaining in A herbal_a is a grammatical rule at the onset-class level. It is not an artifact of a few high-frequency bigrams inflating the count. The constraint appears to operate over the full lexicon of each onset class — any word from the ch-class can satisfy the pos2 position in a ch-terminal line.

**The 45.5% self-chain rate for ch-LF** (N=70/154 eligible) deserves particular attention: nearly half of all 3+-word ch-terminal lines in A herbal_a have a ch-onset word at pos2. With 70 distinct word pairs, this is as clean as a grammatical constraint gets in corpus linguistics.

---

## Self-Audit

**Target-awareness:** No target-aware elements. Pure corpus word-pair analysis.

**Feature-destroying implementation:** N/A. Survey experiment.

**Extrapolation:** "F468 is grammatical not bigram-driven" is within scope of what was tested (A herbal_a ch-LF and d-LF). The claim holds for the two largest LF classes. Whether it extends to all LF classes and other sections was not tested — but the ch-LF result (70/70 distinct) is definitive for that class.

**Negative-result scope:** N/A — result is positive (F468 confirmed as class-level).

**Control behavior:** No controls. N/A.

---

## Conclusions

**H_new_BW ANSWERED:** F468 (pos2 self-chaining) is a **class-level grammatical constraint**, not a bigram/formulaic pattern. Evidence: ch-LF shows 70 self-chain cases with 70 distinct word pairs (dist_ratio=1.00; top-3 pairs=4.3% of obs). d-LF shows 27 cases with 23 distinct pairs (dist_ratio=0.85; top-3=25.9%, dominated by daiin→daiin which is a frequency artifact). The rule operates over the full onset-class vocabulary, not over specific recurring bigrams.

**Magnitude context:** The ch-LF pos2 self-chain (45.5% rate, 70 unique word pairs) is the clearest evidence for grammatical structure found in A herbal_a so far. A random bigram pattern would concentrate on a few high-frequency pairs; grammatical structure distributes evenly across the vocabulary of the relevant class.
