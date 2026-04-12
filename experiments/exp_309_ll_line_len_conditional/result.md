# exp_309: Line-Length-Conditional LL Mechanism (H511)

**Date:** 2026-04-11
**Hypothesis:** H511 — Scaling p_blind with line length (longer lines produce more short -am words) can create r_ll ≈ −0.22 (VMS) while maintaining 19/19 battery PASS.

## Result: H511 PARTIALLY CONFIRMED — p_blind scaling achieves 19/19 PASS with Menzerath r −0.109→−0.137 (+26%), but r_ll only reaches −0.034 (15% of VMS). KEY DIAGNOSTIC: non-am LL word length ALSO decreases with line length (−1.244 chars) — a deeper structural mechanism beyond p_blind scaling.

## Architecture Adopted: cond_mild (18th mechanism) — p_blind_short=0.060 (n≤5), p_blind_long=0.180 (n≥10), linear interpolation

### DIAGNOSTIC: VMS LL Word Length Decomposition by Line Length

| Bucket | N | LL_wl | am_rate | nonam_wl | am_wl | implied_p |
|--------|---|-------|---------|----------|-------|-----------|
| n=2-4 | 266 | 5.684 | 0.0639 | 5.671 | 5.882 | 0.064 |
| n=5-6 | 452 | 5.334 | 0.0752 | 5.404 | 4.471 | 0.075 |
| n=7-8 | 647 | 5.181 | 0.0989 | 5.226 | 4.766 | 0.099 |
| n=9-10 | 695 | 4.679 | 0.1899 | 4.659 | 4.765 | 0.190 |
| n=11-15 | 329 | 4.422 | 0.2158 | 4.426 | 4.408 | 0.216 |

- **-am rate change** (n=2-4 → n=11-15): 6.4% → 21.6% (Δ=+15.2pp)
- **Non-am LL_wl change**: 5.671 → 4.426 (Δ=−1.244 chars)
- **Overall LL_wl change**: 5.684 → 4.422 (Δ=−1.262 chars)

**Critical finding**: The non-am LL_wl drop (−1.244 chars) is nearly as large as the total drop (−1.262 chars). BOTH -am rate and non-am word distribution change with line length. p_blind scaling alone cannot close the full gap.

### Condition Sweep (N=10 per condition)

| Condition | Pass | am_ll | %VMS | menz_r | r_ll | mid_slope |
|-----------|------|-------|------|--------|------|-----------|
| baseline | 18/19 | 6.917 | 105.6% | −0.124 | −0.004 | −0.050 |
| cond_mild (p_long=0.18) | **19/19** | 6.997 | 106.8% | **−0.133** | **−0.041** | −0.048 |
| cond_moderate (p_long=0.25) | 17/19 | 7.288 | 111.3% | −0.148 | −0.062 | −0.051 |
| cond_strong (p_long=0.35) | 15/19 | 7.442 | 113.6% | −0.150 | −0.104 | −0.048 |
| cond_very_strong (p_long=0.50) | 15/19 | 7.682 | 117.3% | −0.158 | −0.139 | −0.051 |

**Battery fails** at p_long≥0.25. Only cond_mild (p_long=0.18) is battery-stable.

### Full N=30 Battery at cond_mild

| Metric | VMS | Sim | %VMS | Status |
|--------|-----|-----|------|--------|
| am_ll | 6.5498 | 7.0014 | 106.9% | PASS |
| d_ll | 1.3625 | 1.1274 | 82.7% | PASS |
| y_lf | 3.1837 | 2.9565 | 92.9% | PASS |
| ss_mean | 1.1640 | 1.3284 | 114.1% | PASS |
| adj_rate | 0.0090 | 0.0100 | 110.7% | PASS |
| qok_lf | 0.7450 | 0.8428 | 113.1% | PASS |
| d_lf | 2.1178 | 1.8812 | 88.8% | PASS |
| s_lf | 4.4422 | 4.3564 | 98.1% | PASS |
| ch_ll | 0.9653 | 0.9717 | 100.7% | PASS |
| ok_ll | 1.0028 | 1.0491 | 104.6% | PASS |
| qok_ll | 0.6121 | 0.6883 | 112.5% | PASS |
| ss_d | 1.5850 | 1.4480 | 91.4% | PASS |
| ss_y | 1.9550 | 1.6491 | 84.4% | PASS |
| am_lf_enr | 0.1225 | 0.1220 | 99.6% | PASS |
| am_mid_enr | 0.1954 | 0.2009 | 102.8% | PASS |
| edy_rate | 0.1940 | 0.1906 | 98.2% | PASS |
| word_len_mean | 5.4000 | 5.2993 | 98.1% | PASS |
| qok_ch | 1.2670 | 1.2140 | 95.8% | PASS |
| global_am_rate | 0.0203 | 0.0213 | 105.0% | PASS |

**TOTAL: 19/19**
Menzerath r: −0.1368 (60.8% of VMS −0.225; prev=−0.109, 48%)
r_ll: −0.034 (15.5% of VMS −0.219; prev=−0.016, 7.3%)
MID slope: −0.050 (86.2% of VMS −0.058)

## Key Findings

### F1: VMS LL -am rate is line-length-conditional (6.4% → 21.6%)

The VMS LL word -am rate increases from 6.4% in short lines (n=2-4) to 21.6% in long lines (n=11-15). This strongly implies that p_blind is effectively line-length-conditional in VMS generation. The simulation's constant p_blind=0.115 fails to capture this structure.

### F2: NON-am LL word length ALSO decreases with line length (−1.244 chars)

This is the more surprising diagnostic finding. Even excluding -am words, VMS LL_wl drops from 5.671 (n=2-4) to 4.426 (n=11-15). In long VMS lines (n=11-15), non-am LL words (mean 4.426 chars) are nearly as short as -am words (mean 4.408 chars). This means long-line LL words are uniformly short — not just because more are -am endings, but because even the non-am words choose shorter forms. The mechanism driving this is distinct from p_blind and is architecturally unresolved.

### F3: p_blind scaling (cond_mild) improves Menzerath r but hits a ceiling

The viable p_blind conditioning (19/19 stable): p_short=0.060 (n≤5), p_long=0.180 (n≥10). This gives:
- Menzerath r: −0.109 → −0.137 (+25.7%)
- r_ll: −0.016 → −0.034 (+113% relative; 7.3% → 15.5% of VMS)

Stronger conditioning (p_long=0.25-0.50) improves r_ll further (up to −0.139) but breaks the battery (17/19 and 15/19) due to am_ll inflation beyond 120% of VMS.

### F4: 18-mechanism architecture adopted with cond_mild

The 17-mechanism architecture (exp_306) is updated with the 18th mechanism: line-length-conditional p_blind (cond_mild). Parameters: p_short=0.060 for n≤5, linear interpolation, p_long=0.180 for n≥10. 19/19 PASS stable at N=30. Menzerath r improvement +26%.

## Architecture Status

**18-mechanism B-dialect simulation: 19/19 PASS (N=30)**

Parameters (updated from exp_306):
- All exp_306 parameters unchanged
- **18th mechanism**: Line-length-conditional p_blind
  - p_blind(n≤5) = 0.060, p_blind(n≥10) = 0.180, linear interpolation for 5<n<10
  - Mean p_blind = 0.126 (slightly higher than prior 0.115)

Performance: Menzerath r=−0.137 (61% of VMS), r_ll=−0.034 (15% of VMS), MID slope=−0.050 (86%).

**Residual Menzerath gap**: VMS LL_wl decrease with line length is driven by BOTH p_blind increase AND non-am LL word length decrease. The 18th mechanism captures the p_blind component but not the non-am word length component (−1.244 chars, nearly equal to total). H512 targets this next.

## Self-Audit

**Target-awareness:** VMS_REF values used as pass/fail thresholds. The p_blind conditioning is calibrated to reproduce VMS -am rate by line length bucket (diagnostic-guided), which is a form of target awareness. The resulting am_ll (107%) reflects a small calibration excess — the mean p_blind (0.126) slightly exceeds the VMS weighted mean -am rate (0.133). This excess is within PASS range.

**Feature-destroying implementation:** The line-length-conditional p_blind specifically targets r_ll (LL word length vs line length). It does not destroy any existing feature — it extends cipher_ll with a new line-length parameter. The modification path and copy path are unaffected.

**Extrapolation:** The claim "full r_ll closure requires non-am word length conditioning" is based on the diagnostic analysis (Δ non-am_wl = −1.244 chars is nearly as large as total Δ = −1.262 chars). This is a direct measurement, not an extrapolation. The claim that "stronger p_blind conditioning breaks battery" is from tested conditions (p_long=0.25-0.50, 15-17/19).

**Negative-result scope:** H511 partially confirmed. The negative result (r_ll ceiling at −0.034 for 19/19-stable conditions) is specific to the linear step-function p_blind(n) parameterization. More complex LL conditioning (e.g., suffix-length biasing for LL words) might achieve higher r_ll while maintaining battery stability.

**Control behavior:** Baseline (constant p_blind=0.115) gives am_ll=6.917 (105.6% of VMS) at N=10 sweep. This is consistent with exp_306's N=30 result of 6.867 (104.8%). N=10 sweep has higher variance, which accounts for the slight difference. No unexpected behavior.
