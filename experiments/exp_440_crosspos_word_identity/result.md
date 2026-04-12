# exp_440: Cross-Position Word Identity vs Onset-Class Overlap (H496)

**Hypothesis (H496):** Decompose cross-position token sharing into: (a) identical word types, (b) same onset class different word, (c) different onset class. Is cross-position sharing driven by word-identity or onset-class matching?

---

## Results

### A-dialect

| Pair | Type overlap | Token overlap | Identical word | Same-onset diff | Diff-onset |
|------|-------------|--------------|----------------|-----------------|-----------|
| LF↔MID | 43.1% of LF types in MID | 65.9% LF tokens | 60.6% of MID | 39.3% of MID | **0.1%** |
| MID↔LL | 22.6% of MID types in LL | 65.0% MID tokens | 67.3% of LL | 32.7% of LL | **0.0%** |
| LF↔LL | 21.8% of LF types in LL | 44.8% LF tokens | 43.0% of LL | 56.8% of LL | **0.1%** |

### B-dialect

| Pair | Type overlap | Token overlap | Identical word | Same-onset diff | Diff-onset |
|------|-------------|--------------|----------------|-----------------|-----------|
| LF↔MID | 45.1% of LF types in MID | 69.4% LF tokens | 66.5% of MID | 33.4% of MID | **0.1%** |
| MID↔LL | 19.8% of MID types in LL | 70.4% MID tokens | 70.0% of LL | 30.0% of LL | **0.0%** |
| LF↔LL | 21.8% of LF types in LL | 49.1% LF tokens | 42.0% of LL | 57.8% of LL | **0.2%** |

### Top shared types driving identical-word overlap

**A LF↔MID top shared**: daiin(LF=78,MID=208), chol(15,192), chor(12,103), or(18,61), sho(30,44)
**B LF↔MID top shared**: chedy(7,325), shedy(14,239), qokeedy(33,208), qokain(32,182), daiin(86,125)
**B LF↔LL top shared**: daiin(86,20), saiin(46,4), chedy(7,40), qokain(32,13), ol(14,27)

---

## Interpretation

**H496 ANSWERED: Cross-position token sharing is dominated by identical word types (60-70% of tokens). "Different onset class" words are essentially absent (<0.2%) from cross-position overlap.**

1. **Diff-onset word rate ≈ 0%**: When a word appears in position p2 (MID or LL), its onset class is almost always present in p1's onset class set. This is trivially true — all major onset classes appear at all positions, so "onset class not in p1" is a near-null event. This metric does not discriminate.

2. **Identical-word overlap dominates MID**: 60.6%(A)/66.5%(B) of MID tokens are words that ALSO appear at LF. This is high — MID is the body of the line, and the most common MID words (chol, chor, chedy, shedy, qokeedy) are also LF-valid words. The identical-word overlap is driven by a few dominant words: in B, chedy(325 MID), shedy(239 MID), qokeedy(208 MID), qokain(182 MID) all appear at LF as well (chedy=7, shedy=14, etc.).

3. **LF↔LL different pattern**: Only 43-42% of LL tokens are identical to LF words; 57-58% are same-onset different words. LL uses more specifically terminal word types (dy, dam, dal, oly) that share onset classes with LF words (d-onset, ol-onset) but are different specific words. This reflects the LL grammar rule: LL prefers specific sub-vocabulary within each onset class.

4. **Key structural implication**: The "onset-class first, then word selection" hypothesis (H496 expected outcome) is partially supported at LL but not at MID:
   - **MID**: grammar operates primarily via identical word reuse (not onset-class-driven word selection), since 60-67% identical
   - **LL**: grammar operates more via onset-class-constrained word selection (57-58% same-onset-diff), i.e., the LL grammar specifies "d-onset word" and then selects from the LL-specific d-word vocabulary

5. **Daiin is the primary cross-position bridge word**: daiin appears at LF(A=78,B=86), MID(A=208,B=125), and LL(A=93,B=20). In A, daiin is the top word at all three positions, driving 78+208+93=379 tokens of identical-word overlap.

---

## Limitations

- "Diff-onset" metric is trivially near-zero because all onset classes appear at all positions; this metric does not test the hypothesis as stated.
- The "identical word" rate at MID includes cases where the word at MID is also LF-eligible but was selected independently (not copied from LF). Can't distinguish copying from independent selection at this level.

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues.
**Extrapolation**: All claims within scope of measured data.
**Negative-result scope**: N/A.
**Control behavior**: N/A.

---

## Conclusion

H496 ANSWERED: Cross-position sharing is dominated by identical word types (60-67% of MID tokens; 43% of LL tokens are identical to LF words). Onset-class-different tokens are 0% of cross-position sharing. LF↔LL: 57-58% same-onset-diff-word (LL grammar selects specific sub-vocabulary within onset class); LF↔MID: 33-39% same-onset-diff-word (MID largely reuses LF vocabulary directly). Daiin is the primary cross-position bridge word. **No new finding ID** (descriptive, extends exp_265; no novel structural finding beyond F-series).
