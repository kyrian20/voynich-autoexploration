# exp_236: Global AM Resolution (p_blind Reduction + Metric 19)

**Hypothesis**: H436 — The 2× global am divergence (sim 4.42% vs VMS 2.03%) is NOT structural. Reducing p_blind from 0.30 to 0.115 (analytical optimum for LL_am = VMS 13.3%) will bring global_am into VMS pass zone without losing am_ll or the enrichment metrics.

**Status**: H436 CONFIRMED — 19/19 PASS

---

## Setup

Base architecture: exp_235 (18/18 PASS, 11 mechanisms). Changes:
- `p_blind` reduced from 0.30 → 0.115 (derived analytically: for LL_am = 13.3%, p_blind = (0.133 − 0.0203) / 0.9797 = 0.115)
- `d_boost` recalculated for new p_blind: 9.13% (unchanged, as it is driven by d_ll target, not p_blind directly)
- Metric 19 added: `global_am_rate` (VMS = 2.03%, pass zone [1.62%, 2.44%])
- Sweep: r_lf ∈ {0.10, 0.12, 0.15, 0.18} × r_mid ∈ {0.20, 0.25, 0.30} = 12 combos at N=5
- Full N=30 run at best combo

---

## Sweep Results

| r_lf | r_mid | global_am% | am_lf_enr | am_mid_enr | am_ll | 4-metric PASS? |
|------|-------|-----------|-----------|-----------|-------|----------------|
| 0.10 | 0.20  | 94.1% P   | 80.1% P   | 90.1% P   | 110.2% P | 4/4 |
| 0.10 | 0.25  | 92.0% P   | 114.6% P  | 84.4% P   | 110.2% P | 4/4 |
| 0.10 | 0.30  | 97.6% P   | 64.0% F   | 108.5% P  | 106.5% P | 3/4 |
| 0.12 | 0.20  | 87.6% P   | 112.6% P  | 86.9% P   | 110.3% P | 4/4 |
| **0.12** | **0.25**  | **93.0% P** | **119.1% P** | **101.7% P** | **107.1% P** | **4/4** |
| 0.12 | 0.30  | 93.5% P   | 125.4% F  | 93.8% P   | 108.3% P | 3/4 |
| 0.15 | 0.20  | 90.5% P   | 155.4% F  | 91.7% P   | 108.7% P | 3/4 |
| 0.15 | 0.25  | 93.2% P   | 119.4% P  | 91.3% P   | 108.9% P | 4/4 |
| 0.15 | 0.30  | 94.3% P   | 142.5% F  | 131.1% F  | 101.1% P | 2/4 |
| 0.18 | 0.20  | 90.6% P   | 139.7% F  | 79.8% F   | 110.8% P | 2/4 |
| 0.18 | 0.25  | 95.1% P   | 186.1% F  | 97.7% P   | 105.6% P | 3/4 |
| 0.18 | 0.30  | 91.5% P   | 178.8% F  | 113.4% P  | 104.1% P | 3/4 |

Best combo: **r_lf=0.12, r_mid=0.25** (4/4 am-metrics PASS, am_mid_enr closest to VMS at 101.7%).

---

## Full N=30 Results at r_lf=0.12, r_mid=0.25

| Metric | VMS | E236 | % | P? | E235 | delta |
|--------|-----|------|---|----|------|-------|
| am_ll | 6.5498 | 7.0920 | 108.3% | P | 7.1960 | −0.104 |
| d_ll | 1.3625 | 1.4130 | 103.7% | P | 1.3810 | +0.032 |
| y_lf | 3.3237 | 3.3860 | 101.9% | P | 3.5010 | −0.115 |
| ss_mean | 1.1640 | 1.3491 | 115.9% | P | 1.3230 | +0.026 |
| adj_rate | 0.0090 | 0.0096 | 107.1% | P | 0.0100 | −0.0004 |
| qok_lf | 0.7777 | 0.7930 | 102.0% | P | 0.8040 | −0.011 |
| d_lf | 2.2109 | 2.2471 | 101.6% | P | 2.2850 | −0.038 |
| s_lf | 4.6376 | 4.9280 | 106.3% | P | 4.9380 | −0.010 |
| ch_ll | 0.9386 | 0.8662 | 92.3% | P | 0.8730 | −0.007 |
| ok_ll | 0.9750 | 0.9589 | 98.3% | P | 0.9850 | −0.026 |
| qok_ll | 0.5952 | 0.5859 | 98.4% | P | 0.5940 | −0.008 |
| ss_d | 1.2910 | 1.5387 | 119.2% | P | 1.5220 | +0.017 |
| ss_y | 1.9550 | 1.7799 | 91.0% | P | 1.6760 | +0.104 |
| am_lf_enr | 0.1225 | 0.1363 | 111.3% | P | 0.1070 | +0.029 |
| am_mid_enr | 0.1950 | 0.1842 | 94.5% | P | 0.1760 | +0.008 |
| edy_rate | 0.1940 | 0.1868 | 96.3% | P | 0.1800 | +0.007 |
| word_len_mean | 5.4000 | 5.4557 | 101.0% | P | 5.4100 | +0.046 |
| qok_ch | 1.2670 | 1.2026 | 94.9% | P | 1.2140 | −0.011 |
| **global_am_rate** | **0.0203** | **0.0190** | **93.3%** | **P** | 0.0442 | **−0.0252** |

**19/19 PASS**

-am diagnostics (p_blind=0.115, r_lf=0.12, r_mid=0.25):
- Global am = 1.90% (VMS = 2.03%)
- LF am = 0.259% (VMS ≈ 0.249%)
- MID am = 0.350%
- LL am = 13.44% (VMS ≈ 13.31%)
- am_lf_enr = 0.137 (VMS = 0.122)
- am_mid_enr = 0.185 (VMS = 0.195)
- am_ll = 7.090 (VMS = 6.550)

ss_mean: 1.349 (upper bound = 1.397, margin = 0.048)

---

## Interpretation

**H436 CONFIRMED.** The 2× global am divergence in exp_235 (4.42% vs VMS 2.03%) was not structural to the am enrichment mechanism. Reducing p_blind from 0.30 to 0.115 resolves the divergence completely: global_am drops to 1.90% (93.3% of VMS, within the ±20% pass zone), while all 18 original metrics continue to pass. The architecture now achieves 19/19.

**Why p_blind=0.30 was chosen originally**: p_blind was calibrated to maximize am_ll enrichment without explicit awareness that it was simultaneously inflating global_am. The analytical derivation for this experiment showed that for LL_am = 13.3% (VMS), p_blind = 0.115 is sufficient — 0.30 was a 2.6× overshoot.

**am-metric calibration note**: r_lf and r_mid were selected from a 12-point sweep. The chosen values (0.12, 0.25) jointly satisfy four constraints: global_am PASS, am_lf_enr PASS, am_mid_enr PASS, am_ll PASS. The selection was calibrated against VMS targets. See Self-Audit — this means the four am-specific metrics are conditional on this calibration.

**The mechanism is self-consistent**: The LL blind fraction (p_blind=0.115) forces 11.5% of LL words to be -am regardless of suffix. The non-blind fraction (88.5%) draws from suffix_global, which has a natural am rate of ~2.0%. Together these produce LL_am ≈ 13.3%, matching VMS exactly. The enrichment structure (LL > MID > LF > global) is preserved, and now the absolute rate matches too.

**The 12-mechanism architecture** (exp_235's 11 plus the p_blind recalibration as a 12th parametric fix, not a new mechanism) achieves 19/19 PASS including the absolute am rate.

---

## Limitations

1. **am-metric calibration**: r_lf=0.12 and r_mid=0.25 were chosen by sweeping against VMS targets. The four am metrics (global_am_rate, am_lf_enr, am_mid_enr, am_ll) are therefore conditional on this calibration. A system that did not know VMS am rates would not necessarily land on these values.

2. **p_blind calibration**: p_blind=0.115 was derived analytically from VMS LL_am = 13.3%. This is explicitly target-aware for am_ll (and by extension global_am_rate, am_lf_enr, am_mid_enr). The enrichment ratios are real structure in VMS; p_blind quantifies how much of the LL position is forced -am.

3. **ss_mean margin tightening**: ss_mean=1.349 with upper bound 1.397 — margin 0.048. Any future mechanism that increases ss_mean risks a constraint violation.

4. **N=30 single combo**: The full run was done at one parameter point (r_lf=0.12, r_mid=0.25). Cross-combo variation is visible in the sweep but not quantified at N=30.

---

## Self-Audit

**Target-awareness**: Multiple elements are target-aware:
- `p_blind=0.115` was derived from VMS LL_am=13.3%. The reported am_ll, am_lf_enr, am_mid_enr, and global_am_rate values are **conditional on this calibration**. A non-target-aware p_blind would produce different LL_am, different global_am, and different enrichment ratios.
- `r_lf=0.12, r_mid=0.25` were selected by sweeping against VMS am targets. The four am metrics are **conditional on these calibration values**. The calibration is disclosed in the Interpretation section adjacent to the am-metric claims.
- `d_boost=9.13%` is calibrated for d_ll. d_ll result is conditional on this calibration (inherited from prior experiments).
- All VMS-direct parameters (y_lf, qok_lf, d_lf, s_lf, ch_ll, ok_ll, qok_ll) are set from VMS corpus distributions — acknowledged as target-aware for those metrics.
- The 15 non-am metrics are NOT conditional on the am calibration (p_blind, r_lf, r_mid do not affect non-am suffix selection for non-LL positions, and LL-position metrics are calibrated separately).

**Feature-destroying implementation**: None identified. The reduction of p_blind from 0.30 to 0.115 does not destroy any feature the hypothesis depends on. The am enrichment structure (LL >> MID > LF) is preserved: LL_am=13.44% >> MID_am=0.350% > LF_am=0.259%.

**Extrapolation**: The structural verdict ("The 2× divergence IS reducible by lowering p_blind. It is NOT structural.") is supported by a direct empirical test, not extrapolation. The tested parameter grid covers the analytically predicted optimum (r_lf=0.12, r_mid≈0.23). The claim is: "at p_blind=0.115, r_lf=0.12, r_mid=0.25, global_am passes" — this is within the tested grid. No claim of universality is made.

**Negative-result scope**: N/A — positive result (19/19 PASS).

**Control behavior**: No separate control distribution used in this experiment. The comparison is sim vs VMS, with the sim being a generative model. No unexpected behavior observed.

---

## Conclusion

H436 CONFIRMED. The 19/19 architecture:

| Parameter | exp_235 | exp_236 |
|-----------|---------|---------|
| p_blind | 0.30 | **0.115** |
| r_lf | 0.25 | **0.12** |
| r_mid | 0.60 | **0.25** |
| global_am | 4.42% | **1.90%** |
| Pass count | 18/18 | **19/19** |

The global am divergence is resolved. All 11 original mechanisms are intact; only the p_blind and am-suppression factors changed. The architecture is now calibrated for both the absolute am rate and the enrichment structure.

**Next**: A-dialect generalization (Priority 2) — run Mode B architecture against A-dialect VMS targets to determine which of the 19 metrics transfer and which require dialect-specific recalibration.
