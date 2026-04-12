# exp_448: Cross-Line Inversion Correlation (H_new_K)

**Hypothesis (H_new_K):** Onset pairs depleted at within-line (pLL→LL) systematically show enrichment at cross-line (LL→LF). If this is a general rule, Spearman rho(within_E, CL_E) should be significantly negative.

**Method:** Full 19×19 pLL→LL and LL→LF bigram matrices. Spearman correlation between within-line E and cross-line E across all pairs with expected N≥2. Direct test: within-depleted (E<0.8) pairs → mean CL E.

---

## Results

### Spearman correlation

| Dialect | rho(within, CL) | N pairs |
|---------|----------------|---------|
| A | **0.000** | 163 |
| B | **−0.042** | 215 |

### Direct test: within E<0.8 → mean cross-line E

| Dialect | N(within<0.8) | Mean CL E | N(within≥0.8) | Mean CL E |
|---------|--------------|-----------|---------------|-----------|
| A | 44 | **0.94×** | 74 | **1.09×** |
| B | 74 | **1.01×** | 109 | **0.95×** |

**Within-depleted pairs have LOWER mean CL E in A and slightly HIGHER in B — no consistent inversion direction.**

### Inversion count

| Dialect | Inversion pairs (CL>1.3/within<0.85) | Same-dir pairs | Total strong |
|---------|--------------------------------------|----------------|-------------|
| A | 9 (18%) | 7 (14%) | 49 |
| B | 22 (27%) | 7 (8%) | 83 |

### Confirmed inversion cases (CL>1.3, within<0.8, N large)

**B-dialect notable inversions:**
- ok→y: within=0.32×(N=1) → CL=1.64×(N=21)
- l→sh: within=0.48×(N=2) → CL=1.63×(N=19)
- d→qok: within=0.66×(N=6) → CL=1.56×(N=26)
- ch→ol: within=0.59×(N=18) → CL=1.55×(N=16)
- sh→d: within=0.61×(N=8) → CL=1.58×(N=19)
- ol→ot: within=0.59×(N=4) → CL=2.89×(N=9)

**A-dialect notable inversions:**
- cth→sh: within=0.45×(N=1) → CL=1.93×(N=12)
- ol→d: within=0.27×(N=2) → CL=1.67×(N=8)
- cth→ok: within=0.54×(N=2) → CL=1.74×(N=6)
- sh→d: within=0.75×(N=17) → CL=1.46×(N=13)

---

## Interpretation

**H_new_K REFUTED: The systematic inversion hypothesis is false. Within-line depletion does NOT predict cross-line enrichment at the population level (Spearman rho≈0).**

Key findings:

1. **No systematic correlation (rho≈0)**: With N=163-215 pairs and rho=0.000-0.042, there is no measurable relationship between within-line E and cross-line E across the full onset-pair space. The pattern observed for specific pairs (B sh→d, B ok→y, B d→qok) does NOT generalize.

2. **Direct test is negative**: Within-depleted pairs (E<0.8) have mean CL E = 0.94-1.01×, indistinguishable from within-non-depleted pairs (0.95-1.09×). There is no tendency for within-depleted pairs to have elevated CL E.

3. **Individual inversions are real but sparse**: 9 (A) and 22 (B) inversion pairs exist out of 49/83 "strong" pairs. This is a minority (18-27%), not a majority. The specific inversions identified in F438 (B sh→d, B d→qok, B ok→y, B ch→ol) are genuine features of the cross-line grammar, but they're independent coupling rules, not instances of a general inversion principle.

4. **Low within-N drives apparent inversions**: Many inversion cases have N=0-2 within-line observations. When s never appears at pLL position (s→s within=0.00×/N=0 in B), it's not that s "avoids" being followed by s at LL; it's that s rarely appears at the penultimate position. The cross-line s→s enrichment (E=2.20×) reflects s's LF-preferred role (F294: s=11.6× LF-enriched), not an inversion of a within-line rule.

5. **Cross-line enrichment is driven by positional biases, not inversion**: Cross-line E is high when LL onset is a natural LL class AND the LF onset of the next line is a natural LF class. For example: B ok→y is enriched cross-line because ok is LL-enriched (F294) and y is LF-enriched. Their cross-line pairing is a consequence of each class occupying its preferred position, creating the appearance of a structural coupling.

6. **Same-direction pairs also exist (7 in both dialects)**: B y→y (within=4.60×, CL=1.62×) and A s→s (within=1.46×, CL=2.57×) are enriched in BOTH within-line and cross-line contexts — class self-succession is a tendency that operates at both scales.

**Revised interpretation of F438 inversion cases**: The B sh→d, d→qok, ch→ol inversions are genuine but should be understood as: (a) the LL onset (sh, d, ch) has a within-line grammar that routes elsewhere at pLL→LL; (b) the LF onset (d, qok, ol) has a strong LF positional preference; (c) their cross-line pairing is driven by LF-onset positional assignment, not by the LL onset's within-line depletion of that class. The inversion is a SIDE EFFECT of strong LF/LL positional preferences, not a causal mechanism.

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues.
**Extrapolation**: rho=0.000 is within-sample measurement on N=163 pairs. No causal inference beyond the correlation finding.
**Negative-result scope**: The null result (rho≈0) is properly scoped: "within-depletion does NOT predict cross-line enrichment at the population level." Does not claim individual inversion cases are artifacts — they are real. Only the GENERAL RULE is refuted.
**Control behavior**: N/A.

---

## Conclusion

H_new_K REFUTED: Spearman rho(within_E, CL_E) = 0.000-0.042 (not negative). Within-line depletion does NOT systematically predict cross-line enrichment. Individual inversion cases (B sh→d/d→qok/ch→ol/ok→y, A cth→sh) are real but represent independent coupling rules, not a general mechanism. Cross-line enrichments are better explained by positional biases: LF-enriched onset classes (y, s, d, qok) appear at LF regardless of the previous line's LL class, creating cross-line pairings with LL classes that happen to avoid those onsets within-line. **No new finding ID** (negative result refuting H_new_K; confirms individual inversion cases are independent rules within F438).
