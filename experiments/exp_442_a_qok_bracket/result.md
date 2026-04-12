# exp_442: A-qok ch-Midfix in Bracket Lines (H_new_A)

**Hypothesis (H_new_A):** A-dialect ch-midfix qok forms (qokchy/qokchol/qokchor) are concentrated in bracket lines (where pos1 and LL share the same onset class), consistent with a template-filling role in structured line frames.

**Method:** ZL3B continuation lines, A-dialect only. Identify bracket lines (same onset class at pos1 and LL); compute ch-midfix rate among qok tokens in bracket vs non-bracket lines.

---

## Results

| Context | qok tokens | ch-midfix N | ch-midfix rate |
|---------|-----------|-------------|----------------|
| Bracket lines | 29 | 4 | **13.8%** |
| Non-bracket lines | 194 | 19 | **9.8%** |
| Enrichment E | — | — | **1.41×** |

### Bracket type distribution (top)

| Bracket type | Lines |
|-------------|-------|
| ch→ch | 70 |
| d→d | 26 |
| sh→sh | 13 |
| ok→ok | 8 |
| qo→qo | 7 |
| y→y | 4 |
| d→sh | 3 |

### Top qok words in bracket MID positions

qoky(3), qokeey(3), qokal(3), qokchy(2), qokain(2), qokeedy(2)

---

## Interpretation

**H_new_A: DIRECTIONAL / INCONCLUSIVE.** E=1.41× is consistent with the hypothesis direction but the bracket sample is too small (N=4 ch-midfix tokens in bracket lines) for a reliable estimate.

Key observations:

1. **N=4 is insufficient**: The 13.8% bracket rate is based on 4/29 tokens. A single additional or missing token changes the rate by 3.4 percentage points. Cannot distinguish true enrichment from sampling noise.

2. **Dominant bracket type is ch→ch (70 lines), not the specific bracket types from F413**: F413 identified d→sh and y→y as the A-dialect bracket structures. The exp_442 bracket definition (same onset at pos1 AND LL) captures the broader homogeneous-bracket set, dominated by ch→ch (70 lines). Only 4 d→sh lines appear; y→y = 4 lines. The ch-midfix qok question is most meaningful in d→sh or y→y brackets (where ch-onset is not the bracketing element), but these are too rare to test separately.

3. **Non-bracket baseline is already 9.8%** (19/194): The A-dialect global ch-midfix rate (F434: ~13% of A qok tokens overall) is partly in this non-bracket set. The 9.8% non-bracket rate vs 13.8% bracket rate suggests ch-midfix qok is slightly redistributed toward bracket lines, but the difference is not significant.

4. **qokchy=2 in bracket MID**: The most specific ch-midfix form (qokchy) appears twice in bracket MID — once in a ch→ch bracket and once in a d→d bracket. This is consistent with qokchy being a MID-position template word rather than a bracket-specific form.

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues. Bracket detection uses pos1/LL onset classes; qok ch-midfix detection uses standard onset/midfix extraction.
**Extrapolation**: E=1.41× with N=4 is reported as directional only; no firm claim made.
**Negative-result scope**: Inconclusive result properly scoped. Does NOT claim ch-midfix qok avoids bracket lines — only that the enrichment is directional and unverifiable at this sample size.
**Control behavior**: N/A.

---

## Conclusion

H_new_A DIRECTIONAL: A-qok ch-midfix forms show E=1.41× enrichment in bracket lines (13.8% vs 9.8%), but N=4 bracket tokens makes this unreliable. The dominant A-dialect bracket type is ch→ch (70 lines), which swamps the specific d→sh/y→y brackets from F413 and dilutes the signal. **No new finding ID** — directional result only, bracket sample too small.
