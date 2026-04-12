# exp_235: H435 — p_stutter Recalibration with edy-Conditional Connector

**Date**: 2026-04-11  
**Hypothesis**: H435 — Does recalibrating p_stutter to a lower value fix adj_rate (131.8%→PASS) without regressing any of the 17 currently passing metrics (especially word_len_mean)?  
**Status**: H435 CONFIRMED — **18/18 PASS — FIRST PERFECT SCORE IN THE EXPERIMENTAL PROGRAM** (+1 from exp_234). adj_rate FIXED (131.8%→107.2% PASS) at p_stutter=0.006. All 17 prior passes maintained including word_len_mean (100.2% PASS). ss_mean margin IMPROVED to 0.074. Mode B with 11 mechanisms achieves a complete characterization of VMS B-dialect positional grammar within ±20% tolerance.

---

## Design

Use the full exp_234 architecture (edy-conditional connector: connector only for edy/eedy suffix words) with all exp_233 parameters (cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, p_qokch=0.12, d_boost=9.13%, VMS LL onset for non-blind LL, r_lf=0.25, r_mid=0.60).

Single change: sweep p_stutter ∈ {0.003, 0.004, 0.005, 0.006, 0.007, 0.008} at N=5 each. Select best by: smallest absolute distance from VMS adj_rate=0.009 among values with adj_rate PASS. Full N=30 at best p_stutter.

Analytical prediction from exp_234: natural collision rate ≈ 0.003 (from reduced vocabulary); for adj_rate=0.009: p_stutter × 0.75 = 0.006 → p_stutter ≈ 0.008. (Prediction was slightly high; sweep resolves uncertainty.)

---

## Sweep Results

```
p_stutter  adj_rate   %VMS   P?   word_len   %VMS   P?   ss_mean  P?
0.003        0.0071   78.8%   F      5.425  100.5%   P     1.276   P
0.004        0.0083   91.7%   P      5.421  100.4%   P     1.366   P
0.005        0.0092  102.4%   P      5.409  100.2%   P     1.315   P
0.006        0.0089   98.5%   P      5.421  100.4%   P     1.345   P  ← BEST
0.007        0.0107  118.3%   P      5.419  100.4%   P     1.365   P
0.008        0.0107  119.3%   P      5.419  100.4%   P     1.393   P
```

**Best**: p_stutter=0.006 (adj_rate=0.0089, 98.5% — closest to VMS center within pass zone). At p_stutter=0.003: adj_rate=0.0071 (78.8% — below lower bound 0.0072). The pass zone [0.0072, 0.0108] is achieved at p_stutter ∈ {0.004, 0.005, 0.006, 0.007, 0.008}.

Natural collision rate empirical estimate: at p_stutter=0.003, adj_rate≈0.007 ≈ 0.003(natural) + 0.003×0.75 = 0.005. This implies natural collision ≈ 0.002 (below the rough analytical estimate of 0.003). The actual equilibrium depends on buffer composition and exact word space size.

---

## Full Run Results (N=30, p_stutter=0.006)

```
Metric           VMS    E235       %  P?    E234    delta
am_ll           6.550   7.196  109.9% P    7.152   +0.044
d_ll            1.362   1.381  101.4% P    1.384   -0.003
y_lf            3.324   3.501  105.3% P    3.432   +0.069
ss_mean         1.164   1.323  113.6% P    1.352   -0.029  ← margin now 0.074
adj_rate        0.009   0.010  107.2% P    0.012   -0.002  ← FIXED
qok_lf          0.778   0.804  103.4% P    0.784   +0.020
d_lf            2.211   2.285  103.4% P    2.279   +0.006
s_lf            4.638   4.938  106.5% P    4.978   -0.040
ch_ll           0.939   0.873   93.1% P    0.869   +0.004
ok_ll           0.975   0.985  101.0% P    0.973   +0.012
qok_ll          0.595   0.594   99.8% P    0.592   +0.002
ss_d            1.291   1.522  117.9% P    1.543   -0.021
ss_y            1.955   1.676   85.7% P    1.764   -0.088
am_lf_enr       0.122   0.107   87.8% P    0.119   -0.012
am_mid_enr      0.195   0.176   90.2% P    0.176   -0.000
edy_rate        0.194   0.180   92.9% P    0.181   -0.001
word_len_mean   5.400   5.410  100.2% P    5.418   -0.008  ← maintained
qok_ch          1.267   1.214   95.8% P    1.199   +0.015

Pass count:  E235=18/18  |  E234 (baseline)=17/18
```

**ss_mean safety**: 1.323 (upper bound = 1.397, margin = 0.074) — substantially improved from exp_233's 0.028.

---

## Interpretation

### Finding 1: 18/18 PASS — complete characterization of VMS B-dialect positional grammar

All 18 metrics pass at ±20% tolerance. This is the first perfect score in the experimental program (235 experiments over Phase 3-5). Mode B with 11 mechanisms achieves a full characterization of VMS B-dialect positional grammar under the current 18-metric battery.

**Target-awareness note (mandatory per Self-Audit)**: p_stutter=0.006 is target-calibrated to VMS adj_rate=0.009. This is the second recalibration of p_stutter (first: exp_229 set p_stutter=0.009 for the connector-inclusive word space; second: this experiment recalibrates to p_stutter=0.006 for the edy-conditional connector word space). The adj_rate result (0.010, 107.2% PASS) is conditional on this calibration.

### Finding 2: adj_rate fixed — p_stutter=0.006 correctly compensates vocabulary reduction

At p_stutter=0.006, adj_rate=0.010 (107.2% PASS). The sweep confirms the exp_234 diagnosis: the natural collision rate in the edy-conditional connector word space is ~0.002 (empirically: p_stutter=0.003 gives adj_rate≈0.007, so natural≈0.007−0.002=0.005... actually this is consistent with natural≈0.005 rather than 0.002). The analytical model was imprecise but the sweep makes the recalibration direct.

The mechanism: p_stutter=0.009 (exp_233) was calibrated for the larger word space (connector adds 6 possible words per onset+suffix pair). With no connector for non-edy words, the vocabulary per onset+suffix pair collapses to 1 word. This increases natural collision rate. p_stutter=0.006 reduces the deliberate stutter contribution, bringing the total adj_rate back to the pass zone.

### Finding 3: ss_mean margin substantially improved — architectural stability increased

ss_mean = 1.323 (113.6% PASS), margin = 0.074 (was 0.028 after exp_233, was 0.044 after exp_234). The margin is now 3× what it was at the most constrained point (after exp_233). Two factors contributed:
1. edy-conditional connector slightly reduces ss_mean (−0.016 from exp_233→exp_234)
2. Lower p_stutter reduces stutter-induced same-onset pairs (−0.029 from exp_234→exp_235)

The ss_mean boundary is now relaxed — future investigations of variants have more headroom.

### Finding 4: Complete mechanism architecture at 18/18

Mode B with 11 mechanisms:
1. VMS MID onset distribution for MID fresh words
2. p_blind=0.30 (30% of LL words blind -am)
3. p_lf=1.0 (LF words always use VMS LF onset)
4. cp=0.55/mp=0.90 (copy and modify probabilities)
5. Onset-preserving modification
6. edy-suffix-preserving modification with fresh-word fallback
7. qok→ch Markov bias (p_qokch=0.12)
8. Stutter mechanism (p_stutter=0.006)  ← recalibrated from 0.009
9. VMS LL onset for non-blind LL fraction (d_boost=9.13%)
10. Differential -am suppression (r_lf=0.25 for LF; r_mid=0.60 for fresh MID)
11. edy-Conditional connector (connector only for edy/eedy suffix words)  ← NEW

### Finding 5: What 18/18 means and doesn't mean

**What it means**: The Mode B architecture with these 11 mechanisms reproduces all 18 B-dialect positional grammar metrics within ±20% tolerance. This is a complete characterization in the sense that no metric in the battery currently discriminates VMS from the simulation.

**What it doesn't mean**: 
- (a) The simulation is the correct model of how VMS was generated — it is one of potentially many mechanisms that could produce these statistics.
- (b) The architecture is unique — other parameter combinations or mechanism designs may also achieve 18/18.
- (c) The specific parameter values (p_stutter, r_lf, r_mid) are first-principles derived — 4 parameters (p_stutter, r_lf, r_mid, d_boost) are target-calibrated.
- (d) The simulation would generalize to A-dialect or quire-level variations — these are unverified open questions.
- (e) There are no remaining structural differences — there may be other metrics not in the current battery that would discriminate VMS from the simulation.

**The 18/18 result is best interpreted as**: "The Mode B architecture is not falsified by this 18-metric battery. The architecture reproduces all tested positional grammar properties of VMS B-dialect within ±20% tolerance."

---

## Limitations

1. **Four target-calibrated parameters**: p_stutter=0.006 (adj_rate), r_lf=0.25 (am_lf_enr), r_mid=0.60 (am_mid_enr), d_boost=9.13% (d_ll). The 18/18 result is conditional on these calibrations. A non-target-aware parameter selection would not necessarily achieve 18/18.
2. **18-metric battery scope**: The battery covers onset-class enrichment (LF/MID/LL), suffix enrichment (-am at LL), bigram structure (ss_mean/ss_d/ss_y/qok_ch), adjacent word repetition, and word length. It does not cover within-word structure (character n-grams), vocabulary distribution (type-token ratio), inter-line grammar, or cross-folio variation.
3. **Global am divergence**: global am = 4.42% vs VMS 2.03%. All enrichment ratios are correct, but the absolute global rate remains 2×VMS due to the p_blind mechanism. This is a structural property not captured by the current metric battery.
4. **N=30; single Latin corpus (Cicero De Officiis)**: Results are stable across the 30 runs but corpus dependence is not tested in this experiment.

---

## Self-Audit

**Target-awareness**: p_stutter=0.006 is target-calibrated to VMS adj_rate=0.009 (second recalibration; first was exp_229's p_stutter=0.009). The adj_rate result (0.010, PASS) is conditional on this calibration. All other parameter calibrations are inherited: r_lf=0.25 (calibrated to am_lf_enr in exp_233), r_mid=0.60 (calibrated to am_mid_enr in exp_233), d_boost=9.13% (calibrated to d_ll in exp_231). The edy-conditional connector mechanism is NOT target-calibrated — the connector condition is architecturally motivated by the edy-preservation requirement. The word_len_mean fix is a structural consequence, not a calibration. This is stated in Finding 1.

**Feature-destroying implementation**: No feature-destroying implementation details. The edy-conditional connector preserves the modifiable middle region for edy words (edy_rate=0.180, 92.9% PASS). Onset distributions are unchanged. The stutter mechanism at p_stutter=0.006 still generates adj_rate in the pass zone. The -am suppression is unchanged from exp_233.

**Extrapolation**: The claim "18/18 PASS — complete characterization" is qualified in Finding 5 with explicit scope limitations. The metric battery is finite; the characterization is relative to the current 18 metrics. No claim is made that the simulation is unique or causally correct.

**Negative-result scope**: N/A — positive result.

**Control behavior**: Comparison baseline is exp_234 (17/18). At exp_234's parameter settings (p_stutter=0.009 with edy-conditional connector): adj_rate=0.012 (FAIL), word_len_mean=5.418 (PASS). Expected behavior of p_stutter reduction: adj_rate decreases (less deliberate repetition), all other metrics stable. Observed: adj_rate=0.010 (PASS, −0.002), word_len_mean=5.410 (PASS, −0.008), ss_mean=1.323 (PASS, −0.029). ss_mean decrease is slightly larger than expected from stutter reduction alone (stutter adds same-onset pairs; at 0.003 fewer stutter per step, ss_mean decreases by ~0.03 — consistent). All behaviors expected and explained.

---

## Conclusion

H435 CONFIRMED — 18/18 PASS — FIRST PERFECT SCORE IN THE EXPERIMENTAL PROGRAM (+1 from exp_234's 17/18). p_stutter recalibration from 0.009 to 0.006 fixes adj_rate (131.8%→107.2% PASS) in the edy-conditional connector word space. All 17 prior passes maintained. ss_mean margin improved to 0.074 (from 0.028 after exp_233).

**Mode B with 11 mechanisms achieves a complete characterization of VMS B-dialect positional grammar within ±20% tolerance on the current 18-metric battery.** This is the culmination of the Phase 5 characterization loop: from 0/18 (exp_171) to 18/18 over ~65 experiments.

**Target-calibrated parameters**: p_stutter=0.006, r_lf=0.25, r_mid=0.60, d_boost=9.13%. The result is conditional on these four target calibrations. The other 7 mechanisms are architecturally motivated: VMS MID onset (exp_221), p_blind=0.30 (exp_209), p_lf=1.0 (exp_220), cp/mp=0.55/0.90 (exp_221), onset-preserving mod (exp_219), edy-preserving fresh-fallback (exp_226), qok→ch Markov (exp_228), VMS LL onset (exp_231), edy-conditional connector (exp_234).

**Next open question**: Does this architecture generalize? Key tests: (a) A-dialect corpus; (b) quire-level stability; (c) additional metrics beyond the current 18; (d) whether the global am divergence (4.42% vs VMS 2.03%) can be resolved without destroying the 18/18 result.
