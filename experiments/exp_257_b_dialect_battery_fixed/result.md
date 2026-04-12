# exp_257 Result: H460 — B-Dialect 19-Metric Battery Verification With Fixed 'Other' Onset Distributions

**Outcome: H460 CONFIRMED — 19/19 PASS. B-dialect 12-mechanism architecture validated with fixed distributions.**

---

## Battery Result (N=30)

| Metric | VMS | Sim | %VMS | Status |
|---|---|---|---|---|
| am_ll | 6.5498 | 7.0573 | 107.7% | PASS |
| d_ll | 1.3625 | 1.3715 | 100.7% | PASS |
| y_lf | 3.3237 | 3.3302 | 100.2% | PASS |
| ss_mean | 1.1640 | 1.2908 | 110.9% | PASS |
| adj_rate | 0.0090 | 0.0101 | 112.1% | PASS |
| qok_lf | 0.7777 | 0.6758 | 86.9% | PASS |
| d_lf | 2.2109 | 2.2480 | 101.7% | PASS |
| s_lf | 4.6376 | 4.9001 | 105.7% | PASS |
| ch_ll | 0.9386 | 0.9238 | 98.4% | PASS |
| ok_ll | 0.9750 | 1.0452 | 107.2% | PASS |
| qok_ll | 0.5952 | 0.5619 | 94.4% | PASS |
| ss_d | 1.2910 | 1.4972 | 116.0% | PASS |
| ss_y | 1.9550 | 1.7404 | 89.0% | PASS |
| am_lf_enr | 0.1225 | 0.1455 | 118.9% | PASS |
| am_mid_enr | 0.1950 | 0.1901 | 97.5% | PASS |
| edy_rate | 0.1940 | 0.1841 | 94.9% | PASS |
| word_len_mean | 5.4000 | 5.2831 | 97.8% | PASS |
| qok_ch | 1.2670 | 1.2183 | 96.2% | PASS |
| global_am_rate | 0.0203 | 0.0187 | 92.0% | PASS |

**TOTAL: 19/19 PASS**

---

## Non-Battery Structural Check
ot→ot MID E2: Sim=1.749, VMS=1.887, Δ=-0.138 (confirms exp_256's corrected gap estimate)

---

## Implementation Note: d_boost Formula Fix

The first run (with incorrect `d_ll_non_blind = onset_ll['d']` raw rate) produced 18/19 FAIL
(d_ll=165.3%). The correct formula requires passing `onset_ll['d'] / d_global` (the enrichment
ratio, not raw rate) to compute_d_boost — matching the exp_249 formula convention. After fix:
d_ll = 100.7% PASS.

The fix is required for any future experiment that uses the d_boost mechanism with filter_other.
Document: compute_d_boost expects d_ll_non_blind = onset_ll['d'] / d_global (NOT onset_ll['d']).

---

## Key Findings

### 1. B-Dialect 12-Mechanism Architecture Validated With Fixed Distributions
The 'other' onset fix (filter_other applied to onset_mid, onset_lf, onset_ll) does not break
any of the 19 battery metrics. All pass at N=30 with fixed distributions. The architecture is
stable and correct.

### 2. ot→ot Gap Confirmed Small (Δ=-0.138 at N=30)
Consistent with exp_256 (Δ=-0.161 at N=15). The small remaining gap doesn't affect battery
status. The gap was previously reported as Δ=-0.477 in exp_246 (contaminated baseline) and
Δ=-0.161 after fix in exp_256. N=30 result (Δ=-0.138) is within sampling noise of N=15.

### 3. Architecture Status: B-Dialect 12 Mechanisms, Fixed Distributions Required
Final B-dialect architecture (12 mechanisms, fixed 'other' distributions):
  p_blind=0.115, p_lf=1.0, cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_stutter=0.006
  r_lf=0.12, r_mid=0.25, mu_len=8.4, sigma_len=3.0, ll_onsets with d_boost

IMPORTANT: All future B-dialect experiments must apply filter_other to onset distributions
AND use the correct d_boost formula: compute_d_boost(d_global, d_ll_target,
onset_ll['d']/d_global, P_BLIND).

---

## Self-Audit

**Target-awareness**: No new parameters. filter_other and d_boost formula are mechanical
corrections, not calibrations. 19/19 PASS result is not conditional on any target-specific
calibration.

**Feature-destroying implementation**: The initial d_boost formula bug caused d_ll FAIL by
over-producing d at LL. This was diagnosed and fixed. The correct implementation preserves
the d enrichment mechanism.

**Extrapolation**: The 19/19 PASS claim is scoped to the tested architecture (12 mechanisms,
exp_249 params, filter_other applied, correct d_boost formula) at N=30 seeds SEED+trial×100.
No claims about other seed sets or different architectures.

**Negative-result scope**: N/A — positive result.

**Control behavior**: d_ll = 100.7% (VMS=1.3625, Sim=1.3715) — excellent match after formula
fix. All other metrics behave as expected. No unexpected control anomalies.
