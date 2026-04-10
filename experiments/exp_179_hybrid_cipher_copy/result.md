# exp_179: Hybrid Position-Sensitive Cipher + Copy Component
**Date**: 2026-04-10
**Hypothesis**: Does combining exp_177's position-sensitive cipher (strong calibration) with a Timm-style local copy buffer simultaneously satisfy the dual constraint — position-sensitive grammar (-am LL ≥ 5.0×) AND sequential structure (ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015)?
**Status**: OUTCOME 2 — DUAL CONSTRAINT UNSATISFIABLE BY HYBRID MODEL. 0/16 parameter combinations meet all three viability criteria. The am_ll and ss_mean constraints are mutually exclusive in this model's parameter space: raising COPY_PROB to produce ss_mean ≥ 1.2 proportionally dilutes am_ll below 5.0, and raising adj_rate above the threshold simultaneously.

**Configuration**: 16 combinations (COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6}). 50 simulations per combination. 800 total runs. Copy buffer: WINDOW=20 words.

**Viability thresholds**: am_ll ≥ 5.0× AND ss_mean ∈ [1.2, 1.7] AND adj_rate ≤ 0.015.

---

## RESULTS

### Full Parameter Grid

| cp | mp | am_ll | y_lf | ss_mean | adj_rate | viable |
|----|-----|-------|------|---------|----------|--------|
| 0.2 | 0.3 | 4.804 | 2.109 | 1.075 | 0.0113 | no |
| 0.2 | 0.4 | 4.779 | 2.079 | 1.058 | 0.0103 | no |
| 0.2 | 0.5 | 4.777 | 2.111 | 1.050 | 0.0092 | no |
| 0.2 | 0.6 | 4.782 | 2.109 | 1.035 | 0.0081 | no |
| 0.3 | 0.3 | 4.306 | 1.980 | 1.114 | 0.0167 | no |
| 0.3 | 0.4 | 4.330 | 1.972 | 1.090 | 0.0148 | no |
| 0.3 | 0.5 | 4.272 | 1.970 | 1.070 | 0.0130 | no |
| 0.3 | 0.6 | 4.275 | 1.990 | 1.062 | 0.0109 | no |
| 0.4 | 0.3 | 3.826 | 1.832 | 1.163 | 0.0231 | no |
| 0.4 | 0.4 | 3.829 | 1.862 | 1.128 | 0.0201 | no |
| 0.4 | 0.5 | 3.822 | 1.854 | 1.109 | 0.0174 | no |
| 0.4 | 0.6 | 3.841 | 1.877 | 1.087 | 0.0149 | no |
| 0.5 | 0.3 | 3.359 | 1.720 | 1.217 | 0.0315 | no |
| 0.5 | 0.4 | 3.351 | 1.725 | 1.174 | 0.0263 | no |
| 0.5 | 0.5 | 3.363 | 1.711 | 1.142 | 0.0224 | no |
| 0.5 | 0.6 | 3.373 | 1.734 | 1.111 | 0.0190 | no |

**VMS targets**: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009.

### No combination is viable. 0/16 meet all three constraints.

---

## THE STRUCTURAL TRADE-OFF

### am_ll vs ss_mean: mutually exclusive in this model

| COPY_PROB | am_ll mean | ss_mean mean | adj_rate mean |
|-----------|-----------|-------------|--------------|
| 0.2 | **4.785** | 1.054 | 0.0097 |
| 0.3 | 4.296 | 1.084 | 0.0139 |
| 0.4 | 3.830 | 1.122 | 0.0189 |
| 0.5 | 3.361 | **1.161** | 0.0248 |

Each 0.1 increase in COPY_PROB produces approximately:
- am_ll decrease: ~0.47× (cipher table invocations replaced by copies, which dilute the LL-specific -am mapping)
- ss_mean increase: ~0.036× (copies reproduce word-class adjacencies)
- adj_rate increase: ~0.0050 (more exact word repetitions from copying)

**To reach ss_mean ≥ 1.2, COPY_PROB ≥ 0.5 is required.** At COPY_PROB=0.5, am_ll ≈ 3.36× — well below the 5.0× threshold. The highest ss_mean achieved in the grid is 1.217× at (cp=0.5, mp=0.3), and even that undershoots VMS ss_mean of 1.465×.

**To reach am_ll ≥ 5.0, COPY_PROB ≤ 0.2 is required** (the best at cp=0.2 is 4.804×, marginally below threshold). At cp=0.2, ss_mean ≈ 1.035-1.075× — far below the 1.2× threshold. The gap between the best achievable am_ll (4.804 at cp=0.2) and the threshold (5.0) is small; extrapolating, cp ≈ 0.15 might reach 5.0× on am_ll, but would push ss_mean even further below 1.2×.

### adj_rate: a secondary constraint that coincides with ss_mean

At COPY_PROB values that produce any meaningful ss_mean (≥ 1.1), adj_rate also rises:
- cp=0.3, mp=0.6: ss_mean=1.062, adj_rate=0.0109 (passes adj threshold; fails ss threshold)
- cp=0.5, mp=0.6: ss_mean=1.111, adj_rate=0.0190 (fails both adj and ss thresholds)

The adj_rate threshold (≤ 0.015) adds additional constraint in the mid-COPY_PROB range but is not the binding constraint — ss_mean is the binding constraint against am_ll. Even if adj_rate could be reduced independently (e.g., by aggressive modification), the am_ll vs ss_mean trade-off would remain.

### MODIFY_PROB effect: reduces adj_rate and ss_mean, negligible effect on am_ll

Increasing MODIFY_PROB across the grid:
- adj_rate decreases by ~0.002-0.004 per 0.1 MODIFY_PROB increase (modification prevents exact word repetition)
- ss_mean decreases by ~0.013-0.020 per 0.1 MODIFY_PROB increase (modification breaks onset-class self-succession)
- am_ll is essentially unchanged (modification replaces the onset but preserves the suffix, so -am suffixes at LL survive)

This means MODIFY_PROB is not a lever to relax the am_ll vs ss_mean tension. It only reduces both adj_rate and ss_mean together, moving the parameter space in the wrong direction for ss_mean.

---

## INTERPRETATION

### The dual constraint is structurally unsatisfiable by this hybrid mechanism

The hybrid model has a fundamental incompatibility: the copy component that produces ss_mean also replaces cipher-generated words (including specifically-calibrated LL -am words) with copies from the buffer. The buffer is dominated by MID-position words (most words are MID), so copying at LL positions tends to paste non-am-suffix words into LL slots, diluting the -am enrichment.

This is not a parameter-tuning problem — it is inherent to how the two mechanisms interact. For any COPY_PROB > 0:
- A fraction COPY_PROB of LL words are copied from buffer (predominantly non-am-suffix)
- A fraction (1-COPY_PROB) of LL words are generated by the cipher (predominantly -am at strong calibration)
- am_ll enrichment scales approximately as (1 - COPY_PROB) × cipher_am_ll

At cipher_am_ll ≈ 5.756 (strong calibration without copying): am_ll ≈ 5.756 × (1 - COPY_PROB). To reach am_ll ≥ 5.0, COPY_PROB ≤ 0.13. At COPY_PROB ≤ 0.13, ss_mean ≈ 1.0 + very small increment — far below VMS 1.465×. The linear scaling means there is no COPY_PROB value where both constraints are simultaneously satisfied, regardless of MODIFY_PROB.

### What the hybrid model achieves at best

The closest any combination gets to satisfying all three constraints is cp=0.2, mp=0.3:
- am_ll = 4.804× (below threshold 5.0; 0.196× short)
- ss_mean = 1.075× (below threshold 1.2; 0.125× short)
- adj_rate = 0.0113 (within threshold 0.015)

No combination is within reach on both am_ll and ss_mean simultaneously.

---

## IMPLICATIONS FOR THEORY DISCRIMINATION

### The structured-grammar verdict gains strength by elimination

Exp_179 closes the hybrid mechanism gap. The untested hypothesis from Phase 3 was: "a position-sensitive cipher combined with a sequential structuring mechanism might jointly satisfy the dual constraint." The hybrid test shows this fails in the tested parameter space.

The remaining viable mechanisms are:
1. **Hybrid with different architecture**: A mechanism where the copy component selectively avoids LL positions (copies only at MID, applies cipher at LF and LL) could decouple the two metrics. This would require position-aware copying — which is itself equivalent to a grammar specifying that LL positions are not available for copying.
2. **Intrinsic structured grammar**: The VMS positional grammar and sequential memory arise from grammatical rules, not from cipher mechanics. Both properties are natural consequences of a grammar: onset-class rules determine positional placement (Property 1); word-class co-selection rules determine sequential preference (Property 2).

**The simplest uneliminated mechanism is intrinsic structured grammar.** The remaining alternatives either require mechanisms that are functionally equivalent to grammar (position-aware copying, selective constraint application) or have not been operationalized in any existing cipher proposal.

---

## LIMITATIONS

1. **Grid scope**: COPY_PROB swept to 0.5. Higher COPY_PROB values (0.6-0.9) would push ss_mean higher but am_ll lower — extrapolation suggests no viable combination exists at any COPY_PROB, but this is not demonstrated beyond 0.5.

2. **Buffer architecture**: The hybrid uses a uniform buffer (all recent words equally likely to be copied). A position-stratified buffer (copy only from same-position words) or an onset-stratified buffer (copy only same-onset-class words) could produce different ss_mean profiles. These architectures are not tested.

3. **WINDOW size**: WINDOW=20 was used (approximately 2-3 VMS lines). Different window sizes would change the ss_mean profile. Larger windows produce weaker self-succession (copy pool is more diverse); smaller windows produce stronger self-succession but may overproduce adj_rate.

4. **Target-aware calibration carried forward**: The LL cipher table in this hybrid retains the target-aware calibration from exp_177 (all clause-final morphemes → -am). The same limitation documented in exp_177 applies here: the maximum achievable am_ll reflects deliberate calibration, not natural Latin.

---

## CONCLUSION

**The dual constraint (am_ll ≥ 5.0×, ss_mean ∈ [1.2, 1.7]) is unsatisfiable by a hybrid position-sensitive cipher plus copy-buffer model across the tested 16-combination parameter grid.** The fundamental incompatibility is structural: copying at LL positions dilutes the -am enrichment proportionally to COPY_PROB, creating a linear trade-off that no parameter setting can overcome.

This extends the theory elimination sequence:
- Position-blind ciphers (Naibbe, Timm): fail on am_ll
- Position-sensitive cipher (exp_177): fails on ss_mean
- Hybrid position-sensitive + copy (exp_179): fails to jointly satisfy am_ll and ss_mean

**The remaining viable mechanism in the tested hypothesis space is intrinsic structured grammar** — or a position-aware hybrid that selectively excludes LL positions from copying (functionally equivalent to a grammar rule).

---

## FILES

- `script.py`: Hybrid cipher-copy simulation (16 combinations, 50 sims each)
- `data/hybrid_results.json`: Raw results for all 800 simulations
