# exp_285: H489 — LL Midfix Rate Sweep

**Date**: 2026-04-11  
**Hypothesis**: H489 — Reducing p_ll_mf (LL midfix presence rate, empirical=0.486) brings LL_wl from 5.697 to VMS 5.015 AND improves Menzerath r toward VMS -0.225.

## Background

- exp_284 (F284): p_ll_mf at empirical rate (0.486) produces LL_wl=5.697 vs VMS 5.015 (13.6% excess). Hypothesis: this excess inflates menz_r, so reducing p_ll_mf should bring LL_wl to target AND improve menz_r.

## Method

Architecture: 15-mechanism B-dialect (exp_284 best): p_lf_mf=0.50 (LF midfix), p_mf=0.20 (MID midfix), gamma=0.30, alpha=0.15, + 12 base mechanisms.  
Sweep: p_ll_mf ∈ {0.00, 0.10, 0.20, 0.30, 0.40, 0.486}, N=10 each.  
Selection: 19/19 AND LL_wl closest to VMS 5.015.  
Full N=30 at best p_ll_mf.

| p_ll_mf | PASS  | menz_r  | lf_wl | mid_wl | ll_wl | word_len |
|---------|-------|---------|-------|--------|-------|----------|
| 0.000   | 19/19 | -0.0395 | 5.879 | 5.427  | 4.939 | 5.423    |
| 0.100   | 19/19 | -0.0556 | 5.878 | 5.424  | 5.097 | 5.439    |
| 0.200   | 19/19 | -0.0648 | 5.888 | 5.429  | 5.241 | 5.461    |
| 0.300   | 19/19 | -0.0866 | 5.883 | 5.420  | 5.402 | 5.473    |
| 0.400   | 19/19 | -0.0941 | 5.883 | 5.433  | 5.559 | 5.501    |
| 0.486   | 19/19 | -0.1027 | 5.897 | 5.416  | 5.683 | 5.505    |

LL_wl crossover: VMS 5.015 is between p_ll=0.00 (4.939) and p_ll=0.10 (5.097).  
Selected best: **p_ll_mf=0.000** (LL_wl=4.939, closest to VMS 5.015 by 0.076).

Full N=30 at p_ll_mf=0.000:

| Metric         | VMS    | Sim    | %VMS   | Status |
|----------------|--------|--------|--------|--------|
| am_ll          | 6.5498 | 7.0022 | 106.9% | PASS   |
| d_ll           | 1.3625 | 1.2091 | 88.7%  | PASS   |
| y_lf           | 3.1837 | 2.8717 | 90.2%  | PASS   |
| ss_mean        | 1.1640 | 1.3554 | 116.4% | PASS   |
| adj_rate       | 0.0090 | 0.0093 | 103.5% | PASS   |
| qok_lf         | 0.7450 | 0.7523 | 101.0% | PASS   |
| d_lf           | 2.1178 | 1.8409 | 86.9%  | PASS   |
| s_lf           | 4.4422 | 4.3602 | 98.2%  | PASS   |
| ch_ll          | 0.9653 | 1.0099 | 104.6% | PASS   |
| ok_ll          | 1.0028 | 1.0954 | 109.2% | PASS   |
| qok_ll         | 0.6121 | 0.6200 | 101.3% | PASS   |
| ss_d           | 1.5850 | 1.5007 | 94.7%  | PASS   |
| ss_y           | 1.9550 | 1.7511 | 89.6%  | PASS   |
| am_lf_enr      | 0.1225 | 0.1195 | 97.6%  | PASS   |
| am_mid_enr     | 0.1954 | 0.2035 | 104.1% | PASS   |
| edy_rate       | 0.1940 | 0.1682 | 86.7%  | PASS   |
| word_len_mean  | 5.4000 | 5.4249 | 100.5% | PASS   |
| qok_ch         | 1.2670 | 1.2164 | 96.0%  | PASS   |
| global_am_rate | 0.0203 | 0.0190 | 93.4%  | PASS   |

**TOTAL: 19/19 PASS**

Diagnostics:
- Menzerath r: -0.0431 (VMS=-0.225, 19% of target)
- MID slope: -0.030 (VMS=-0.058, 52%)
- LF_wl: 5.885 (VMS=5.732, +2.7%)
- MID_wl: 5.427 (VMS=5.409, +0.8%)
- LL_wl: 4.948 (VMS=5.015, -1.3%) — SUBSTANTIALLY IMPROVED from +13.6% to -1.3%

## Interpretation

**H489 NEGATIVE (opposite of predicted)**: Reducing p_ll_mf does NOT improve Menzerath r — it worsens it monotonically. At p_ll_mf=0.00: menz_r=-0.039. At p_ll_mf=0.486 (empirical): menz_r=-0.103. Higher LL_wl → more negative menz_r. The LL_wl "excess" in exp_284 was genuinely contributing to the negative Menzerath signal, not an artifact inflating it.

**Mechanism**: Menzerath's Law arises from positional length differences. In the model:
- LF_wl=5.88 (long)
- MID_wl=5.43 (medium)
- LL_wl varies with p_ll_mf

For lines of length n, mean_wl ≈ (LF_wl + (n-2)×MID_wl + LL_wl) / n. Longer LL_wl makes short lines (few MID words, heavy LF/LL weight) have higher mean_wl than long lines → more negative r. When LL_wl < MID_wl (as at p_ll=0.00 giving LL=4.94 < MID=5.43), short lines are NOT longer-than-average → weaker negative r.

**Key insight**: The VMS has LL_wl=5.015 and r=-0.225, but the simulation at LL_wl=4.948 gives only r=-0.043. In VMS, the STRONG Menzerath r cannot be primarily explained by LF/LL midfix effects — the primary driver must be the within-line gradient (MID words getting progressively shorter at higher word-index within a line), which our simulation only captures at 50% of target. The simulation's menz_r at empirical LL_wl (5.68, r=-0.103) was partly compensating for the missing MID slope.

**Revised Menzerath r decomposition**:
- MID slope contribution: -0.030 (achieves ~52% of VMS -0.058)
- LL_wl anchor contribution at empirical rate: approximately -0.060 (compensatory, not genuinely reproducing VMS mechanism)
- LL_wl anchor at VMS-accurate rate (p_ll≈0.05): approximately -0.010
- Total at VMS-accurate LL: -0.039 to -0.056 (17-25% of VMS target)

The primary remaining gap is the within-line gradient, not LL adjustment.

**Architecture decision**: 
- p_ll_mf=0.00 achieves LL_wl closest to VMS 5.015 (4.948, -1.3% gap vs VMS). This is the correct empirical target.
- The trade-off: menz_r becomes -0.043 (from -0.108 at p_ll=0.486). This is a real deficit — the simulation at VMS-accurate LL_wl achieves only 19% of Menzerath r target.
- Architecture recommendation: use p_ll_mf=0.00 for positional accuracy; accept menz_r=-0.04 as the true current capability; identify MID slope improvement as the path to closing the Menzerath gap.

## Limitations

1. The crossover LL_wl ≈ 5.015 occurs between p_ll=0.00 (4.94) and p_ll=0.10 (5.10). Exact crossover at p_ll≈0.05 not tested. N=10 sweep only.
2. The LL midfix distribution (build_midfix_dist from VMS LL words) may extract midfixes that are systematically too long, causing LL_wl over-production at empirical rates. This would explain why even p_ll=0.486 (correct empirical rate) gives LL_wl=5.68 >> VMS 5.015.
3. Menzerath r decomposition is model-based, not analytically derived.

## Follow-up Hypotheses

- H490: MID slope improvement — current -0.030 vs VMS -0.058 (50%); mechanisms beyond gamma/alpha needed. At VMS-accurate LL_wl, each unit of MID slope improvement maps more directly to menz_r improvement.
- H491: LL midfix distribution may need correction — extracted midfixes may be too long; investigate whether build_midfix_dist applies correctly to LL words with -am suffix (which contributes to misclassification of suffix vs midfix boundary).

## Self-Audit

**Target-awareness**: LL midfix distribution built empirically from VMS data (appropriate — modeling VMS structure). p_ll_mf selected by LL_wl target closeness (not a battery metric). 19/19 holds at all p_ll_mf values. Result NOT conditional on specific p_ll_mf for battery; conditional for menz_r diagnostic.

**Feature-destroying implementation**: Reducing p_ll_mf reduces LL word length, which is the feature under test. No feature destruction. The finding (opposite direction to prediction) is valid — LL_wl reduction worsens menz_r as explained by the positional length mechanism.

**Extrapolation**: No "structural" claims. The result is stated as a model mechanism (LL_wl anchor effect on menz_r within the tested range). The crossover at p_ll≈0.05 is an interpolation, not tested.

**Negative-result scope**: H489 predicted reducing p_ll_mf improves menz_r. Result: opposite direction (reducing p_ll_mf worsens menz_r). Conclusion is correctly scoped: in this 15-mechanism model, LL_wl reduction worsens menz_r. The path to closing the Menzerath r gap is MID slope improvement, not LL adjustment.

**Control behavior**: Sweep baseline (empirical p_ll=0.486) reproduces exp_284 result (menz_r≈-0.103, LL_wl≈5.68). Monotonic behavior across the sweep is a coherent signal confirming the mechanism. No anomalies.

## Conclusion

H489 NEGATIVE (opposite direction). LL_wl reduction worsens Menzerath r. The LL_wl "excess" in exp_284 was compensatory for the missing MID slope gradient, not an artifact. Architecture correction: p_ll_mf=0.00 gives LL_wl=4.948 (closest to VMS 5.015), with 19/19 PASS and menz_r=-0.043. Updated architecture: 15 mechanisms with p_ll_mf=0.00 (LL midfix removed). The Menzerath r gap is primarily a MID slope problem — menz_r at VMS-accurate LL_wl is only -0.043 (19% of target). H490 generated (MID slope improvement as primary path to Menzerath r).
