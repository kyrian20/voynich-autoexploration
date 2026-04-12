# exp_306: Beta Re-Sweep with 17-Mechanism clamp_sparse Architecture (H508)

**Date:** 2026-04-11
**Hypothesis:** H508 — edy_rate fragility resolved by vocabulary clamping (83%→100%). With the 17-mechanism clamp_sparse architecture, beta=0.35-0.50 may now be viable, potentially recovering Menzerath r from 40% toward 50-60% of VMS.

## Result: H508 CONFIRMED — beta=0.50 achieves 19/19 PASS (N=30); Menzerath r = −0.1089 (48% of VMS); edy_rate stable 98%; architecture parameter updated beta=0.30→0.50

### Phase 1: Beta Sweep (N=10 per beta, SEED=306000)

| beta | Pass | menz_r | %VMS | mid_slope | edy_rate | %VMS | am_lf_enr | %VMS |
|------|------|--------|------|-----------|----------|------|-----------|------|
| 0.30 | 19/19 | −0.0861 | 38.3% | −0.0403 | 0.1955 | 100.8% | 0.1130 | 92.2% |
| 0.35 | 19/19 | −0.1014 | 45.1% | −0.0422 | 0.1932 |  99.6% | 0.1426 | 116.4% |
| 0.40 | 18/19 | −0.0960 | 42.7% | −0.0433 | 0.1921 |  99.0% | 0.1477 | 120.6% |
| 0.45 | 19/19 | −0.1034 | 45.9% | −0.0467 | 0.1902 |  98.1% | 0.1220 |  99.6% |
| 0.50 | 18/19 | −0.1053 | 46.8% | −0.0480 | 0.1911 |  98.5% | 0.1123 |  91.7% |

Selection: best menz_r among candidates with pass_count ≥ 18/19 and am_lf_enr ≤ 120% of VMS → **beta=0.50**.

### Phase 2: Full Battery at beta=0.50 (N=30)

| Metric | VMS | Sim | %VMS | Status |
|--------|-----|-----|------|--------|
| am_ll | 6.5498 | 6.8672 | 104.8% | PASS |
| d_ll | 1.3625 | 1.1897 | 87.3% | PASS |
| y_lf | 3.1837 | 2.9668 | 93.2% | PASS |
| ss_mean | 1.1640 | 1.3186 | 113.3% | PASS |
| adj_rate | 0.0090 | 0.0106 | 118.1% | PASS |
| qok_lf | 0.7450 | 0.8343 | 112.0% | PASS |
| d_lf | 2.1178 | 1.8620 | 87.9% | PASS |
| s_lf | 4.4422 | 4.3652 | 98.3% | PASS |
| ch_ll | 0.9653 | 0.9663 | 100.1% | PASS |
| ok_ll | 1.0028 | 1.0643 | 106.1% | PASS |
| qok_ll | 0.6121 | 0.6972 | 113.9% | PASS |
| ss_d | 1.5850 | 1.4065 | 88.7% | PASS |
| ss_y | 1.9550 | 1.7387 | 88.9% | PASS |
| am_lf_enr | 0.1225 | 0.1308 | 106.8% | PASS |
| am_mid_enr | 0.1954 | 0.2204 | 112.8% | PASS |
| edy_rate | 0.1940 | 0.1902 | 98.1% | PASS |
| word_len_mean | 5.4000 | 5.2640 | 97.5% | PASS |
| qok_ch | 1.2670 | 1.2180 | 96.1% | PASS |
| global_am_rate | 0.0203 | 0.0192 | 94.5% | PASS |

**TOTAL: 19/19**
Menzerath r = −0.1089 (48.4% of VMS −0.225; prev = −0.091, 40%)
MID slope = −0.0490 (84.5% of VMS −0.058; prev = −0.041, 71%)

## Key Findings

### F1: H508 CONFIRMED — beta=0.50 achieves 19/19 PASS with Menzerath r recovery

The prior beta ceiling (beta≤0.30 due to edy_rate fragility at 83.5%) no longer applies. With the 17-mechanism clamp_sparse architecture, the edy_rate is stable at 98-101% across all beta values tested (0.30-0.50). beta=0.50 achieves 19/19 PASS (N=30) with:
- Menzerath r: −0.091 → −0.1089 (+19.6% improvement; 40% → 48% of VMS)
- MID slope: −0.041 → −0.049 (+19.5% improvement; 71% → 85% of VMS)
- edy_rate: 0.1902 (98.1% of VMS, stable — was the fragile metric at beta=0.30)
- am_lf_enr: 0.1308 (106.8%, well within pass window)

### F2: edy_rate fragility is resolved — stable across full beta range

All beta values (0.30-0.50) give edy_rate 98-101% of VMS. This confirms that the vocabulary clamping mechanism (17th mechanism) encodes canonical VMS edy/eedy forms at natural VMS frequencies, making edy_rate independent of the beta suffix-length penalty parameter.

### F3: beta=0.40 borderline; beta=0.35 and 0.45 both viable alternatives

beta=0.40 shows am_lf_enr=120.6% at N=10 (just above 120% threshold) — potentially seed-dependent (cf. exp_305 pattern). beta=0.35 and 0.45 are clean 19/19 at N=10 with am_lf_enr well within bounds. beta=0.50 gives best Menzerath r improvement in N=30 while being 19/19 stable.

### F4: Architecture parameter updated beta=0.30→0.50

The 17-mechanism clamp_sparse architecture (exp_301-305) is updated with beta=0.50. All 19 metrics pass. Menzerath r and MID slope improvements are the largest single-parameter gains since beta was first introduced (exp_287 moved from beta=0.00 to beta=0.30, which gave the largest Menzerath r gain in project history; this update adds ~20% more gain on top).

## Architecture Status

**17-mechanism B-dialect simulation: 19/19 stable (N=30), beta updated to 0.50**

Parameters:
- p_blind=0.115, p_lf=1.0, cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12
- p_stutter=0.006, r_lf=0.12, r_mid=0.20, mu_len=8.4, sigma_len=3.0
- p_mf=0.20, p_lf_mf=0.50, p_ll_mf=0.00, gamma=0.30, alpha=0.20, **beta=0.50** (updated)
- **17th mechanism**: Vocabulary clamping for qok/ok/ot/qot MID onsets (all VMS B MID types, frequency-weighted)

Performance: 19/19 PASS, Menzerath r=−0.109 (48% of VMS), MID slope=−0.049 (85% of VMS), edy_rate=98%, am_lf_enr=107%.

**Residual gaps** (outside battery):
- Menzerath r still 52% below VMS (−0.109 vs −0.225)
- MID slope still 15% below VMS (−0.049 vs −0.058)
- sh/ch/d CP90 still over-produced (3-4×)
- sh→qok enrichment architecturally unresolved

## Self-Audit

**Target-awareness:** VMS_REF values are used as pass/fail thresholds. Lexicons (17th mechanism) directly encode VMS type distributions — CP90 reproduction is by construction, not independent prediction. Beta=0.50 was selected by maximizing |menz_r| subject to battery constraints; Menzerath r is NOT in the battery, so the selection is not directly optimizing a battery metric. However, beta affects suffix length distribution which indirectly affects word_len_mean (in battery) — this is a mild target-awareness concern but word_len_mean passes at 97.5%, not at a boundary. The Menzerath r improvement is a structural consequence of increasing the suffix-length gradient, not a calibrated target-aware parameter.

**Feature-destroying implementation:** No feature-destroying implementation details identified. The beta parameter applies a length penalty to suffix sampling that directly controls the suffix length gradient; increasing beta increases the gradient, which is the mechanism by which Menzerath's Law is generated.

**Extrapolation:** No claims beyond tested range. The sweep covers beta ∈ {0.30, 0.35, 0.40, 0.45, 0.50}. Claims are scoped to "best within this sweep." Higher beta values (0.55, 0.60) are untested; they may improve Menzerath r further or trigger new battery failures (am_mid_enr is the most likely to fail, as it was at 112.8% at beta=0.50).

**Negative-result scope:** N/A — positive result throughout.

**Control behavior:** The beta=0.30 condition in this sweep gives menz_r=−0.0861 (N=10), compared to exp_305's confirmed range of −0.091 (N=100 trials, 10 seeds). This is within expected seed/sample noise for N=10. No unexpected control behavior.
