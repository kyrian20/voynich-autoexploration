# exp_233: H433 — Differential -am Suffix Suppression (r_lf ≠ r_mid)

**Date**: 2026-04-11  
**Hypothesis**: H433 — Does applying independent suppression factors r_lf (for LF fresh words) and r_mid (for MID fresh words) simultaneously fix am_lf_enr (332.7%→PASS) and am_mid_enr (144.0%→PASS) without regressing 15 currently passing metrics?  
**Status**: H433 CONFIRMED — 17/18 PASS — NEW PROGRAM BEST (+2 from exp_231). Both am_lf_enr (0.115, 94.0% PASS) and am_mid_enr (0.198, 101.4% PASS) fixed. All 15 prior passes maintained. Only remaining failure: word_len_mean (122.7% — structural). Best combination: r_lf=0.25, r_mid=0.60.

---

## Design

Apply INDEPENDENT suppression factors to fresh LF and fresh MID suffix distributions:
- `suffix_lf_suppressed[am] = r_lf × suffix_global[am]`, other weights renormalized.
- `suffix_mid_suppressed[am] = r_mid × suffix_global[am]`, other weights renormalized.

Used for: (a) fresh LF words via `cipher_lf_vms` — uses `suffix_lf_sup`; (b) fresh MID words via `random_eva_word` — uses `suffix_mid_sup`; (c) `timm_modify` fresh-fallback for MID — uses `suffix_mid_sup`. LL non-blind fraction still uses global suffix unchanged.

Sweep grid: r_lf ∈ {0.25, 0.33, 0.40} × r_mid ∈ {0.60, 0.70, 0.80} = 9 combinations at N=5 each. Best combo selected by tier (prioritize: both am metrics PASS + am_ll PASS) then by combined normalized distance from VMS targets. Full N=30 at best combo. All other parameters identical to exp_231: cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, p_qokch=0.12, p_stutter=0.009, d_boost=9.13%, VMS LL onset for non-blind LL.

---

## Sweep Results

```
r_lf  r_mid  am_lf_enr   %VMS  P?  am_mid_enr   %VMS  P?   am_ll   %VMS  P?  ss_mean  P?
0.25   0.60      0.118   96.0%  P       0.200  102.5%  P    7.024  107.2%  P     1.358   P  ← BEST
0.25   0.70      0.128  104.5%  P       0.230  117.8%  P    6.823  104.2%  P     1.318   P
0.25   0.80      0.117   95.3%  P       0.255  130.9%  F    6.690  102.1%  P     1.381   P
0.33   0.60      0.146  119.4%  P       0.194   99.6%  P    7.021  107.2%  P     1.370   P
0.33   0.70      0.140  114.7%  P       0.230  117.7%  P    6.801  103.8%  P     1.398   F  ← ss_mean
0.33   0.80      0.147  120.4%  F       0.253  129.6%  F    6.648  101.5%  P     1.381   P
0.40   0.60      0.168  136.9%  F       0.195  100.2%  P    7.004  106.9%  P     1.326   P
0.40   0.70      0.159  130.0%  F       0.217  111.2%  P    6.845  104.5%  P     1.354   P
0.40   0.80      0.128  104.6%  P       0.253  129.8%  F    6.634  101.3%  P     1.376   P
```

**Three Tier-0 candidates** (both am metrics PASS + am_ll PASS): (0.25, 0.60), (0.25, 0.70), (0.33, 0.60). Selected by combined normalized distance from VMS: **(0.25, 0.60)** minimizes (am_lf_enr/VMS − 1)² + (am_mid_enr/VMS − 1)² = (96.0%−100)² + (102.5%−100)² ≈ 16 + 6 = 22 (percentage squared units) — closest to center of both pass zones.

Notable observation: (0.33, 0.70) passes both am metrics but ss_mean = 1.398 (just above upper bound 1.397 = 1.164 × 1.20) — FAIL by 0.001. This confirms that ss_mean margin is genuinely tight (margin = 0.028 after full run at best combo).

---

## Full Run Results (N=30, r_lf=0.25, r_mid=0.60)

```
Metric           VMS    E233       %  P?    E231    delta
am_ll           6.550   7.023  107.2% P    6.203   +0.820  ← increases as global am drops
d_ll            1.362   1.404  103.0% P    1.420   -0.016
y_lf            3.324   3.466  104.3% P    3.493   -0.027
ss_mean         1.164   1.368  117.6% P    1.354   +0.014  ← margin now 0.028
adj_rate        0.009   0.010  110.4% P    0.010   -0.000
qok_lf          0.778   0.787  101.2% P    0.771   +0.016
d_lf            2.211   2.273  102.8% P    2.265   +0.008
s_lf            4.638   4.918  106.0% P    4.851   +0.067
ch_ll           0.939   0.862   91.8% P    0.858   +0.004
ok_ll           0.975   0.987  101.2% P    0.988   -0.001
qok_ll          0.595   0.616  103.5% P    0.593   +0.023
ss_d            1.291   1.522  117.9% P    1.505   +0.017  ← no regression (cf. exp_232)
ss_y            1.955   1.919   98.2% P    1.858   +0.061
am_lf_enr       0.122   0.115   94.0% P    0.407   -0.292  ← FIXED (was 332.7% FAIL)
am_mid_enr      0.195   0.198  101.4% P    0.281   -0.083  ← FIXED (was 144.0% FAIL)
edy_rate        0.194   0.189   97.6% P    0.187   +0.002
word_len_mean   5.400   6.627  122.7% F    6.628   -0.001  ← only remaining failure
qok_ch          1.267   1.194   94.2% P    1.189   +0.005

Pass count:  E233=17/18  |  E231 (baseline)=15/18
```

**-am rate diagnostics (r_lf=0.25, r_mid=0.60)**:
```
Global am = 4.48%  (VMS global = 2.03%)
LF am     = 0.516% (VMS LF ≈ 0.249%)
MID am    = 0.888%
LL am     = 31.48%
Derived am_lf_enr  = 0.115  (VMS = 0.122)
Derived am_mid_enr = 0.198  (VMS = 0.195)
ss_mean safety: 1.368 (upper bound = 1.397, margin = 0.028)
```

---

## Interpretation

### Finding 1: Differential suppression confirms H433 — 17/18 PASS, new program best

At r_lf=0.25, r_mid=0.60:
- **am_lf_enr = 0.115 (94.0% — PASS)**: LF am = 0.516% (vs VMS LF 0.249%); global am = 4.48%; am_lf_enr = 0.516/4.48 = 0.115. The LF am rate is still higher than VMS LF, but the global am drop from ~5.5% (exp_231) to 4.48% (exp_233) reduces the denominator enough to bring the ratio within the pass zone.
- **am_mid_enr = 0.198 (101.4% — PASS)**: MID am = 0.888%; am_mid_enr = 0.888/4.48 = 0.198. The MID suppression (r_mid=0.60) reduces fresh MID am from ~1.55% to ~0.93%; buffer erosion at equilibrium brings this further to 0.888%.
- Both targets achieved simultaneously because separate r values allow independent calibration of LF and MID positions, avoiding the uniform-r constraint that caused exp_232 to fail.

This is a direct confirmation of the analytical prediction from F232 Finding 5. The predicted values (am_lf_enr≈0.136, am_mid_enr≈0.214) were conservative; the actual best combo achieves closer to VMS center (94.0%, 101.4%).

### Finding 2: No regressions in 15 prior passes

All metrics that passed in exp_231 continue to pass:
- **ss_d**: 1.505→1.522 (PASS, 117.9%); the exp_232 regression (1.562, 121.0% FAIL) is avoided because r_mid=0.60 is less aggressive than exp_232's effective suppression (the compounding effect of r_mid=0.20 uniform).
- **ss_mean**: 1.354→1.368 (PASS, 117.6%); increased by 0.014 from exp_231. **Critical: margin from upper bound now 0.028** (was 0.043 after exp_231, was 0.033 after exp_232 full run). Four consecutive experiments have increased ss_mean (exp_229: +0.060, exp_231: +0.018, exp_232: +0.009, exp_233: +0.014). The ss_mean boundary is now the tightest safety constraint for all future mechanisms.
- **am_ll**: 6.203→7.023 (PASS, 107.2%); global am drop increases am_ll but stays within pass zone [5.24, 7.86].

### Finding 3: word_len_mean is the sole remaining failure

word_len_mean = 6.627 (122.7% FAIL) is structurally unchanged from exp_231 (6.628). Suppressing -am at LF/MID does not affect word length (connector + onset structure determines length; suffix length = 2-4 chars for -am vs 3-4 for -aiin, so the effect is negligible). This confirms word_len_mean is a structural failure requiring a generation model change — the only remaining metric failure.

**Target-awareness note (mandatory per Self-Audit)**: r_lf=0.25 and r_mid=0.60 are both target-calibrated to VMS am_lf_enr (0.122) and am_mid_enr (0.195). The result am_lf_enr=0.115 (PASS) and am_mid_enr=0.198 (PASS) is conditional on these calibrated values. A non-target-aware choice of r_lf and r_mid (e.g., r_lf=r_mid=1.0 as in exp_231) would not achieve the pass zone. The mechanism direction (VMS depletes -am at LF/MID positions) is architecturally motivated by VMS positional grammar constraints; the specific r values are target-derived.

### Finding 4: Mode B now has 10 mechanisms; architecture approaching full characterization

Mode B with differential -am suppression:
1. VMS MID onset distribution for MID fresh words
2. p_blind=0.30 (30% of LL words are blind -am)
3. p_lf=1.0 (LF words always use VMS LF onset)
4. cp=0.55/mp=0.90 (copy and modify probabilities)
5. Onset-preserving modification
6. edy-suffix-preserving modification with fresh-word fallback
7. qok→ch Markov bias (p_qokch=0.12)
8. Stutter mechanism (p_stutter=0.009)
9. VMS LL onset for non-blind LL fraction (d_boost=9.13%)
10. Differential -am suppression (r_lf=0.25 for LF; r_mid=0.60 for fresh MID)

At 17/18, the architecture is one metric from a complete characterization of B-dialect positional grammar.

### Finding 5: ss_mean margin now binding constraint for future mechanisms

ss_mean = 1.368, upper bound = 1.397, margin = 0.028. Four consecutive mechanisms have increased ss_mean (total increase = +0.092 since exp_228's 1.276). Any future mechanism that adds same-onset bigram self-succession — including any stutter-like repetition, buffer enrichment, or onset-correlating modification — risks pushing ss_mean over the threshold. This must be the primary safety check for any candidate exp_234 mechanism.

---

## Limitations

1. **r_lf and r_mid are target-calibrated**: Both values were selected via sweep to minimize distance to VMS am_lf_enr and am_mid_enr targets. The result is conditional on this calibration — see Target-awareness note and Self-Audit.
2. **N=5 for sweep**: Small sample per combination; sweep results are rough estimates. The full N=30 run confirms the sweep result (am_lf_enr=0.118 sweep vs 0.115 full; both PASS).
3. **ss_mean margin = 0.028**: The tightest constraint in the architecture. At (0.33, 0.70), ss_mean=1.398 was a FAIL by 0.001 — confirming the boundary is active. Future mechanisms must treat ss_mean as the binding constraint.
4. **Global am still diverges from VMS**: global am = 4.48% vs VMS 2.03%. The mechanism achieves the correct enrichment ratios (am_lf_enr, am_mid_enr, am_ll) by manipulating the positional rates, not by fixing the global am structural divergence. The p_blind mechanism remains the root cause of the global am divergence.

---

## Self-Audit

**Target-awareness**: Two target-calibrated parameters: r_lf=0.25 (calibrated to VMS am_lf_enr=0.122) and r_mid=0.60 (calibrated to VMS am_mid_enr=0.195). Both were selected by sweep to minimize combined distance from VMS targets. The result (am_lf_enr=0.115 PASS, am_mid_enr=0.198 PASS) is conditional on this calibration. A non-target-aware version of the mechanism would produce different (typically worse) metric values. This is stated in Interpretation Finding 3, adjacent to the metric claims.

**Feature-destroying implementation**: No feature-destroying implementation details identified. The suppression modifies only the suffix distribution for fresh LF and MID words. Onset structure (affecting ss_mean, ss_d, ss_y, qok_lf, d_lf, etc.) is unaffected. The edy-preservation mechanism (affecting edy_rate) is unaffected — `timm_modify_edy_preserving_fresh_fallback` still preserves the edy suffix; only the fresh-fallback word uses `suffix_mid_sup` which has slightly reduced -am weight (having no effect on edy endings since edy words don't end in -am). The qok→ch Markov and stutter mechanisms are unaffected.

**Extrapolation**: No claims beyond the tested parameter grid. The claim that word_len_mean is "structural" is supported by exp_227's logical argument (removing connector fixes word_len but breaks edy_rate — an architectural incompatibility) and is not a grid extrapolation. The claim that differential suppression is "the correct parameter space" is supported by the F232 analytical argument (uniform r is structurally unable to satisfy two independently constrained ratios with buffer erosion asymmetry) and confirmed by the sweep's tier-0 candidates.

**Negative-result scope**: N/A — positive result.

**Control behavior**: The comparison baseline is exp_231 (15/18). At exp_231 parameter settings (no -am suppression): am_lf_enr=0.407, am_mid_enr=0.281 — both FAIL. Expected behavior of exp_233 suppression mechanism: reduced LF and MID am rates → lower enrichment ratios → closer to VMS. Observed: am_lf_enr=0.115 (−0.292 from baseline), am_mid_enr=0.198 (−0.083 from baseline) — both PASS, exactly as predicted by mechanism. am_ll increases (6.203→7.023) as expected: global am drops from ~5.5% to 4.48%, inflating am_ll = LL_am / global_am. All other metrics behave as expected (onset-related metrics unchanged; edy_rate unchanged; ss_mean slightly increased from LF/MID composition change). No surprises.

---

## Conclusion

H433 CONFIRMED — 17/18 PASS — NEW PROGRAM BEST (+2 from exp_231's 15/18). Differential -am suppression (r_lf=0.25 for LF, r_mid=0.60 for fresh MID) simultaneously fixes am_lf_enr (332.7%→94.0% PASS) and am_mid_enr (144.0%→101.4% PASS). All 15 prior passes maintained, including ss_d (no regression from exp_232's 121.0% FAIL). Only remaining failure: word_len_mean (122.7% — structural, requires generation model change).

**Architecture at 17/18**: Mode B with 10 mechanisms achieves 17/18 on the 18-metric battery. The architecture is one metric (word_len_mean) from a complete characterization. The structural divergence (global am = 4.48% vs VMS 2.03%) remains unresolved at the root-cause level, but all downstream enrichment ratios are now reproduced within ±20%.

**ss_mean is now the binding safety constraint**: margin = 0.028. Any future mechanism must be verified to not add same-onset bigram inflation before full deployment.

**word_len_mean**: the single remaining structural failure. exp_227 established that removing the connector (onset+suffix model) fixes word_len_mean but breaks edy_rate. An alternative generation model — VMS-vocabulary sampling or variable-length connector — remains untested as a path to 18/18.
