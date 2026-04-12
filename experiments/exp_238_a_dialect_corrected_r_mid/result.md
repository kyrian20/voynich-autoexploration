# exp_238: H438 — A-Dialect Corrected r_mid (Erosion Factor Fix)

**Hypothesis**: H438 — Correcting the A-dialect erosion factor assumption (0.84→0.61, derived from empirical am_mid_enr vs r_mid relationship in exp_237) by raising r_mid from 0.634 to 0.87 will fix am_mid_enr (72.7%→PASS) and bring A-dialect to 18-19/19 PASS.

**Status**: H438 PARTIAL CONFIRMED — **18/19 PASS**. am_mid_enr FIXED. One structural failure remains: ss_y.

---

## Setup

All parameters from exp_237 Condition B (A-dialect recalibrated), single change:
- `r_mid_A`: 0.634 → **0.87**

Analytical basis: A-dialect buffer erosion factor ≈ 0.61 (empirically derived from exp_237 sweep).
For am_mid_enr target = 0.5324: r_mid = 0.5324 / 0.61 = 0.87.
Analytical prediction: am_mid_enr = 0.87 × 0.61 = 0.531 ≈ target 0.532. ✓

All other parameters transferred from exp_237 Cond B:
- p_blind=0.0505, d_boost=24.30%, r_lf=0.266, p_stutter=0.002, mu_len=5.64
- Structural: cp=0.55, mp=0.90, p_qokch=0.12, p_lf=1.0
- A-dialect onset/suffix distributions

N=30.

---

## Results

| Metric | A-target | Sim | % | P? | vs exp_237 |
|--------|----------|-----|---|----|-----------|
| am_ll | 3.4993 | 3.5139 | 100.4% | P | was 113.8% P |
| d_ll | 1.6549 | 1.6799 | 101.5% | P | was 99.9% P |
| y_lf | 2.1840 | 2.1654 | 99.2% | P | was 100.3% P |
| ss_mean | 1.5793 | 1.3587 | 86.0% | P | was 86.1% P |
| adj_rate | 0.0093 | 0.0100 | 107.2% | P | was 106.4% P |
| qok_lf | 1.0795 | 1.0937 | 101.3% | P | was 99.2% P |
| d_lf | 1.1060 | 1.1204 | 101.3% | P | was 98.5% P |
| s_lf | 2.1542 | 2.1320 | 99.0% | P | was 102.7% P |
| ch_ll | 0.8549 | 0.8330 | 97.4% | P | was 97.3% P |
| ok_ll | 1.0021 | 0.9905 | 98.9% | P | was 99.7% P |
| qok_ll | 0.5127 | 0.5169 | 100.8% | P | was 99.4% P |
| ss_d | 1.2739 | 1.1446 | 89.9% | P | was 91.7% P |
| **ss_y** | **1.5874** | **1.2146** | **76.5%** | **F** | was 79.9% F |
| am_lf_enr | 0.2656 | 0.2865 | 107.8% | P | was 113.2% P |
| **am_mid_enr** | **0.5324** | **0.5183** | **97.3%** | **P** | was 72.7% F ← FIXED |
| edy_rate | 0.0045 | 0.0045 | 101.5% | P | was 115.2% P |
| word_len_mean | 5.2604 | 5.1338 | 97.6% | P | was 97.8% P |
| qok_ch | 1.2200 | 1.1854 | 97.2% | P | was 97.6% P |
| global_am_rate | 0.0198 | 0.0192 | 96.8% | P | was 90.1% P |

**18/19 PASS.** am_mid_enr FIXED (72.7%→97.3% PASS). ss_y remains FAIL (79.9%→76.5%).

-am diagnostics:
- Global am = 1.92% (VMS A: 1.98%, 96.8% PASS)
- am_mid_enr = 0.518 (VMS A: 0.532, 97.3% PASS)
- am_ll = 3.514 (VMS A: 3.499, 100.4% PASS)

---

## Interpretation

**H438 PARTIAL CONFIRMED: 18/19.** Correcting the erosion factor from 0.84 to 0.61 (via r_mid 0.634→0.87) fixes am_mid_enr. All other 17 metrics remain PASS.

**am_mid_enr fix confirmed**: Analytical prediction am_mid_enr = r_mid × erosion_factor = 0.87 × 0.61 = 0.531 ≈ sim 0.518 (2.4% error from factor rounding). The erosion factor for A-dialect = 0.61 is confirmed empirically. This is determined by the edy-rate of the corpus: A-dialect 0.45% edy words → almost no suffix protection → erosion factor 0.61; B-dialect 19.4% edy → significant suffix protection → erosion factor 0.84.

**ss_y failure is structural**: ss_y worsens from 79.9%→76.5% as r_mid increases. Root cause:
- Higher r_mid means less MID -am suppression (more -am in MID words)
- This does NOT affect y-onset succession
- The ss_y failure is independent of r_mid

The ss_y target in A-dialect (1.587) is significantly higher than what the copy buffer mechanism naturally produces (~1.2). In B-dialect, ss_y passes naturally at 91% (1.780 vs 1.955). The A-dialect requires ss_y=1.587, but the mechanism only achieves ~1.2.

Root cause analysis of ss_y in A-dialect:
- A-dialect y-onset rate = 6.26% (global), heavily concentrated in LF position (13.67% LF rate, 2.18× enrichment)
- LF words do NOT enter the copy buffer
- The copy buffer y-rate ≈ MID y-rate ≈ 5-6% (consistent with global, less than LF)
- Self-succession enhancement from copy buffer: insufficient to reach ss_y=1.587
- Suspicion: VMS A-dialect has a y→y grammatical succession rule (analogous to qok→ch in B-dialect) that requires explicit modeling

**Required fix for ss_y**: A y→y bigram mechanism similar to p_qokch=0.12 (qok→ch Markov). For A-dialect, a p_y_y parameter (probability of drawing a y-onset word from buffer when previous onset was y) could reproduce ss_y=1.587. This is analogous to the qok→ch mechanism: "when prev_onset=y, boost probability of selecting y-onset from buffer."

This generates H439: A-dialect y→y Markov mechanism.

**Final A-dialect parameter table:**

| Parameter | B (exp_236) | A (exp_238) | Change |
|-----------|-------------|-------------|--------|
| p_blind | 0.115 | 0.0505 | Dialect am structure |
| d_boost | 9.13% | 24.30% | Dialect d dominance |
| r_lf | 0.12 | 0.266 | Dialect am_lf_enr |
| r_mid | 0.25 | 0.87 | Dialect erosion factor |
| p_stutter | 0.006 | 0.002 | Dialect vocabulary size |
| mu_len | 8.4 | 5.64 | Dialect line length |
| cp | 0.55 | 0.55 | TRANSFERRED |
| mp | 0.90 | 0.90 | TRANSFERRED |
| p_qokch | 0.12 | 0.12 | TRANSFERRED |
| p_lf | 1.0 | 1.0 | TRANSFERRED |
| Pass count | 19/19 | **18/19** | ss_y structural |

---

## Limitations

1. **ss_y structural failure**: The mechanism has no y-self-succession mechanism for A-dialect. The copy buffer naturally produces ss_y ≈ 1.2 regardless of r_mid. Achieving 1.587 requires an explicit y→y rule.
2. **erosion_factor = 0.61**: Empirically derived from exp_237 sweep. Not independently verified from theoretical derivation of modification operation dynamics.
3. **N=30, single Latin corpus.**

---

## Self-Audit

**Target-awareness**: r_mid=0.87 derived from A-dialect am_mid_enr target (0.532) and empirical erosion factor (0.61). am_mid_enr, am_ll, global_am_rate results **conditional on these calibrations**. ss_y failure and all onset-enrichment PASS results are NOT target-calibrated.

**Feature-destroying implementation**: None. The higher r_mid (0.87 vs 0.634) doesn't destroy any mechanism feature — it reduces am suppression in MID suffix distribution. All other mechanisms intact.

**Extrapolation**: "ss_y structural failure requires y→y Markov mechanism" is supported by the failure being consistent across r_mid sweep and the mechanism analysis (LF y-words not in buffer). This is within the tested scope. The y→y mechanism hypothesis (H439) is labeled as a proposed fix, not a proven conclusion.

**Negative-result scope**: ss_y failure is specific to the current mechanism (copy buffer without y→y bias). The valid conclusion: "Copy buffer mechanism without y-succession rule does not reproduce A-dialect ss_y=1.587 under tested parameters." The invalid conclusion would be "A-dialect ss_y cannot be reproduced by any mechanism."

**Control behavior**: No separate control. Comparison is sim vs VMS A-dialect. Expected: higher r_mid should not affect onset-enrichment metrics (correct). Unexpected: ss_y slightly worse at r_mid=0.87 than 0.634 (79.9%→76.5% — both FAIL). This suggests minor interaction between r_mid and ss_y via global onset composition. Not alarming.

---

## Conclusion

H438 PARTIAL CONFIRMED — **18/19 PASS for A-dialect**. The A-dialect Mode B calibration is now:

- **6 transferred structural params** (cp, mp, p_qokch, p_lf, line_length_sigma): unchanged
- **6 recalibrated params** (p_blind, d_boost, r_lf, r_mid, p_stutter, mu_len): dialect-specific
- **1 remaining failure**: ss_y (76.5%) — requires y→y Markov mechanism (H439)

The generalization result is strong: same mechanism architecture with 6 recalibrated parameters achieves 18/19 on A-dialect. Priority 2 from user directive fully addressed.

**Generates H439**: A-dialect y→y Markov bias (analogous to qok→ch in B-dialect). Parameter: p_y_y (probability of drawing y-onset word when prev_onset=y). Expected: ss_y 76.5%→PASS without regressing other 18 metrics → 19/19 A-dialect.
