# exp_266: Onset Lag-2/Lag-3 Enrichment Analysis

**Date**: 2026-04-11
**Hypothesis**: H468 — sh→qok enrichment persists at lag-2 and lag-3 in MID positions (if so: longer-range dependency; if lag-1 only: immediate succession rule consistent with Markov buffer class but not magnitude).
**Method**: Compute E_k(x,y) = P(onset_{i+k}=y | onset_i=x) / P(onset_j=y) for MID-MID pairs at lag k=1,2,3. Both A- and B-dialect.

## A-Dialect Results

| Pair     | N_lag1 | E_lag1 | E_lag2 | E_lag3 | Lag2/Lag1 |
|----------|--------|--------|--------|--------|-----------|
| sh→qok   | 55     | 1.625  | 1.081  | 1.101  | 0.666     |
| qok→ch   | 64     | 0.929  | 0.855  | 0.725  | —         |
| y→y      | 32     | 2.799  | 2.543  | 2.848  | 0.908     |
| o→o      | 30     | 2.652  | 1.352  | 0.676  | 0.510     |
| ch→qok   | 57     | 0.880  | 1.033  | 0.987  | —         |
| sh→sh    | 79     | 1.224  | 1.418  | 1.270  | —         |
| d→d      | 82     | 1.456  | 2.026  | 1.968  | —         |

VMS A-dialect total MID onset count: 6,264. Lag-1 bigrams: 4,700.

## B-Dialect Results

| Pair     | N_lag1 | E_lag1 | E_lag2 | E_lag3 | Lag2/Lag1 |
|----------|--------|--------|--------|--------|-----------|
| sh→qok   | 339    | 1.880  | **0.967** | 1.089  | **0.514** |
| qok→ch   | 356    | 1.216  | 0.914  | 1.106  | 0.752     |
| ch→qok   | 331    | 1.132  | 0.946  | 0.969  | 0.836     |
| y→y      | 14     | 2.409  | 3.121  | 0.882  | —(noisy)  |
| d→d      | 42     | 1.631  | 1.782  | 2.135  | —         |
| sh→sh    | 120    | **0.895** | 1.309  | 1.192  | —         |

VMS B-dialect total MID onset count: 13,849. Lag-1 bigrams: ~10,200.

## sh→qok Lag Decay: Detailed Analysis

**B-dialect** (statistically reliable, N=339 at lag-1):
- Lag 1: E=1.880 — strongly enriched
- Lag 2: E=0.967 — at baseline (no enrichment)
- Lag 3: E=1.089 — slightly above baseline but noise (N≈134)

**A-dialect** (smaller N):
- Lag 1: E=1.625 (N=55)
- Lag 2: E=1.081 (N=28) — slight enrichment, noise level
- Lag 3: E=1.101 (N=20) — similar, noise level

## Interpretation

### Finding 1: sh→qok Is a Lag-1 Only Rule (B-Dialect Decisive)
The B-dialect result is clear: sh→qok drops from E=1.880 at lag-1 to E=0.967 at lag-2 (baseline). The Lag2/Lag1 ratio is 0.514 — enrichment halves between lag-1 and lag-2, and lag-2 falls to baseline. This rules out "section clustering" as the mechanism: if sh and qok simply co-occur in the same sections/folios, enrichment would persist at lag-2 and lag-3. The lag-1 specificity confirms sh→qok is a genuine word-adjacency rule — the qok-onset word follows the sh-onset word directly.

A-dialect: similar pattern (E drops from 1.625 to 1.081 at lag-2) but noisier (N=28 at lag-2). Consistent with B-dialect finding.

### Finding 2: Implication for Architecture — Markov Class Is Correct, Magnitude Too Large
The lag-1 specificity means the sh→qok rule IS of the same class as qok→ch (both immediate succession rules). The copy-buffer Markov mechanism is the correct architecture; it simply cannot reproduce the high magnitude (E=1.880 at B-dialect) without battery regression. The mechanism is not wrong — it is insufficient in magnitude for this specific bigram. This distinguishes the sh→qok problem from a fundamentally different mechanism.

### Finding 3: o→o Is Strictly Lag-1; y→y Persists
**o→o** (A-dialect): Lag 1=2.652, Lag 2=1.352, Lag 3=0.676 — strong monotone decay. At lag-3, o→o falls below baseline. This is precisely what the p_o_o=0.10 Markov buffer rule produces — immediate onset recycling with rapid decay.

**y→y** (A-dialect): Lag 1=2.799, Lag 2=2.543, Lag 3=2.848 — enrichment persists at ALL lags. This indicates y-onset words form CLUSTERS of multiple consecutive appearances (not just lag-1 pairs). Consistent with exp_252's finding that y→y is concentrated in specific sections (stars, cosmo). The y-onset clustering creates persistent multi-lag enrichment beyond what the p_y_y=0.10 rule was designed to capture.

### Finding 4: B-Dialect sh→sh Depleted at Lag-1, Enriched at Lag-2
B-dialect sh→sh: Lag 1=0.895 (depleted — consistent with F246: VMS MID sh→sh < 1, anti-self-succession). But sh→sh at lag-2=1.309 — enriched after one intervening word. This suggests sh-onset words avoid immediate repetition but tend to reappear 2 words later. A "spacing rule" pattern: sh words cluster but with one-word gaps. Not currently modeled.

### Finding 5: d→d Increases at Lag-2 (Both Dialects)
d→d at lag-2 > lag-1 in both dialects (A: 1.456→2.026; B: 1.631→1.782). This could reflect:
1. d-onset words are LL-concentrated — but this analysis is MID-only, so LL effects shouldn't contaminate
2. Buffer dynamics: when d-onset appears, the buffer retains d-onset words; after one word from another class, the buffer still has d-onset words available → lag-2 d→d enriched via buffer persistence

### Synthesis: sh→qok Architecture
The sh→qok rule is:
- A genuine lag-1 word-adjacency rule (not section clustering)
- The same class as qok→ch (immediate succession, buffer-Markov architecture)
- Too large in magnitude for the Markov buffer to reproduce without regression
- B-dialect gap (E=1.880) vs. A-dialect gap (E=1.625) consistent with B having larger mechanism

The copy-buffer Markov mechanism cannot fully close the sh→qok gap because the target enrichment (E≈1.9) requires p_sh_qok≈0.42 (from exp_243 slope 2.25 E/unit p), which causes ss_d regression. The mechanism is architecturally correct but magnitude-limited.

## Limitations

- A-dialect lag-2/lag-3 N values are small (N=20-28) — results are noisy
- B-dialect y→y N=14 at lag-1 — extremely small; lag-2 and lag-3 y→y values unreliable
- Lag-k computation uses within-line MID pairs only; cross-line effects not captured
- No simulation baseline computed here — comparison to sim E_k would require running exp_264 sim at lag-2/3

## Self-Audit

**Target-awareness**: Pure corpus analysis. No simulation targets. N/A.

**Feature-destroying implementation**: N/A — pure measurement, no mechanism.

**Extrapolation**: "sh→qok is lag-1 only" based on B-dialect (N=339 lag-1, N=149 lag-2). Lag-2 E=0.967 is very close to baseline. This is a reliable conclusion for B-dialect. A-dialect is noisier but consistent. "Section clustering ruled out" is supported by lag-2 dropping to baseline — if section clustering were the mechanism, lag-2 would remain enriched. This is a logical argument, not just extrapolation.

**Negative-result scope**: H468 is NEGATIVE for "long-range dependency beyond lag-1" (for sh→qok in B-dialect). The conclusion is "sh→qok is lag-1 in B-dialect." Does not rule out lag-2 in A-dialect (sample too small). Does not rule out other onset pair long-range effects (y→y does persist at lag-2/3).

**Control behavior**: qok→ch and ch→qok are the comparison pairs. Expected: Markov rules should be primarily lag-1. Actual: qok→ch Lag2/Lag1 = 0.752 (B), 0.921 (A — but at lag-1 it's 0.929, below baseline). The lag-2 ratios for qok→ch and ch→qok are in the 0.75-0.84 range, consistent with lag-1 dominant. sh→qok shows the same pattern in B-dialect (0.514), confirming it is lag-1 dominant. Controls behave as expected.

## Conclusion

H468 NEGATIVE for long-range dependency. B-dialect sh→qok is lag-1 only: E=1.880 at lag-1, E=0.967 at lag-2 (baseline). Section clustering is ruled out as the mechanism. sh→qok is a word-adjacency immediate succession rule — the same architectural class as qok→ch — but with ~1.7× higher magnitude than qok→ch in B-dialect. The Markov buffer mechanism is architecturally correct for sh→qok but is magnitude-limited: achieving E=1.880 would require p≈0.42, which causes battery regression. SECONDARY FINDINGS: o→o is lag-1 only (confirming Markov buffer model); y→y persists at all lags (y-onset clustering in specific sections); B-dialect sh→sh shows depletion at lag-1 but enrichment at lag-2 (spacing pattern, unmodeled).
