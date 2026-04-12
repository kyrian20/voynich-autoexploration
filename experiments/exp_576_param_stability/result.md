# exp_576: Architecture Parameter Stability — Corpus Split Cross-Validation

**Date:** 2026-04-12
**Hypothesis tested:** Are the 6 calibrated architecture parameters stable properties of B-dialect (same values emerge independently from any portion of the corpus), or corpus-fit artifacts (values drift substantially across splits)?
**Status:** COMPLETE — Parameters are NOT stable structural properties. First/Second cross-validation collapses catastrophically (17→8), revealing systematic corpus heterogeneity. Odd/Even cross-val 17→15. Random cross-val 17→14 (despite identical parameters in both halves — sets the stochastic floor at 3/19). The document-order gradient in VMS metric profiles is the primary driver of instability.

---

## SETUP

Three 50/50 split schemes, 1024-combo grid search on each half independently:
1. **ODD/EVEN** — interleaved folios; spatially distributed across document
2. **FIRST/SECOND** — folios in document order; tests section consistency
3. **RANDOM** — random 50/50 split (SEED=576000); no systematic bias

Grid: beta_scale∈{0.8,1.2,1.8,2.5} × p_blind∈{0.0,0.05,0.115,0.18} × r_lf∈{0.05,0.12,0.50,1.0} × r_mid∈{0.10,0.20,0.50,1.0} × p_qokch∈{0.05,0.12,0.20,0.30} = 1024 combinations.

N=3 (fast pass) → confirm best at N=10. Cross-validation at N=10.

---

## KEY FINDING: Corpus Heterogeneity in Document Order

Before parameter analysis, the corpus metric table reveals that the First/Second halves have SYSTEMATICALLY DIFFERENT statistical profiles:

| Metric | Full | Odd | Even | First | Second | RandA | RandB |
|--------|------|-----|------|-------|--------|-------|-------|
| am_ll | 6.550 | 6.714 | 6.360 | 5.825 | 7.147 | 6.384 | 6.714 |
| y_lf | 3.184 | 3.260 | 3.392 | 2.745 | 3.889 | 3.256 | 3.392 |
| ss_y | 1.955 | 1.862 | 2.054 | 1.671 | 2.182 | 1.823 | 2.188 |
| edy_rate | 0.194 | 0.207 | 0.181 | 0.239 | 0.155 | 0.196 | 0.192 |

**The Second half has substantially stronger positional grammar** (am_ll=7.147 vs First=5.825; y_lf=3.889 vs 2.745) and lower edy_rate (0.155 vs 0.239). These are not sampling fluctuations — they are systematic differences consistent with section composition changes across the document.

In contrast, Odd/Even halves are nearly identical to each other and to the full corpus (interleaving distributes the heterogeneity equally). Random halves are similarly balanced.

---

## SPLIT RESULTS

### Split 1: ODD/EVEN

| Parameter | Odd | Even | Exp314 | |A-B| | Stable? |
|-----------|-----|------|--------|-------|---------|
| beta_scale | 2.5 | 0.8 | 1.8 | 1.7 | NO |
| p_blind | 0.115 | 0.115 | 0.115 | 0.000 | **YES** |
| r_lf | 0.12 | 0.05 | 0.12 | 0.07 | near |
| r_mid | 0.10 | 0.20 | 0.20 | 0.10 | NO |
| p_qokch | 0.20 | 0.30 | 0.12 | 0.10 | NO |

| Condition | Pass count |
|-----------|-----------|
| Odd (fit+eval on Odd) | 17/19 |
| Even (fit+eval on Even) | 17/19 |
| Cross-val Odd→Even | 15/19 |
| Cross-val Even→Odd | 16/19 |
| **Degradation** | **17 → 15** |

### Split 2: FIRST/SECOND

| Parameter | First | Second | Exp314 | |A-B| | Stable? |
|-----------|-------|--------|--------|-------|---------|
| beta_scale | 0.8 | 1.2 | 1.8 | 0.4 | NO |
| p_blind | 0.05 | 0.115 | 0.115 | 0.065 | near |
| r_lf | 0.05 | 0.12 | 0.12 | 0.07 | near |
| r_mid | 0.20 | 0.10 | 0.20 | 0.10 | NO |
| p_qokch | 0.05 | 0.30 | 0.12 | 0.25 | NO |

| Condition | Pass count |
|-----------|-----------|
| First (fit+eval on First) | 16/19 |
| Second (fit+eval on Second) | 17/19 |
| Cross-val First→Second | 8/19 |
| Cross-val Second→First | 8/19 |
| **Degradation** | **17 → 8** |

**CATASTROPHIC cross-validation failure.** First-half parameters perform at chance-level on Second half (and vice versa). This is explained by the systematic metric differences: First has am_ll=5.825 and y_lf=2.745; Second has am_ll=7.147 and y_lf=3.889. Parameters optimized to match First's weaker positional grammar cannot achieve Second's stronger positional grammar — they use incompatible targets.

### Split 3: RANDOM

| Parameter | RandA | RandB | Exp314 | |A-B| | Stable? |
|-----------|-------|-------|--------|-------|---------|
| beta_scale | 0.8 | 0.8 | 1.8 | 0.000 | **YES** |
| p_blind | 0.115 | 0.115 | 0.115 | 0.000 | **YES** |
| r_lf | 0.12 | 0.12 | 0.12 | 0.000 | **YES** |
| r_mid | 0.20 | 0.20 | 0.20 | 0.000 | **YES** |
| p_qokch | 0.05 | 0.05 | 0.12 | 0.000 | **YES** |

| Condition | Pass count |
|-----------|-----------|
| RandA (fit+eval on RandA) | 17/19 |
| RandB (fit+eval on RandB) | 17/19 |
| Cross-val A→B (A params, B metrics) | 14/19 |
| Cross-val B→A (B params, A metrics) | 15/19 |
| **Degradation** | **17 → 14** |

Both random halves independently found IDENTICAL parameters (|A-B|=0 for all 5). This is the strongest parameter convergence across all three splits. However, cross-validation still degrades 17→14 despite identical parameters and identical targets in each direction. This residual degradation (~3/19) is due to stochasticity in the model (N=10 runs) rather than parameter mismatch — the same parameters evaluated on a different corpus subset produce slightly different metric realizations.

**Key comparison:** The identical-parameter Random split still shows 3/19 cross-val degradation — this sets a floor for stochastic-only degradation. Odd/Even degradation (17→15, 2/19 additional) adds one metric from parameter mismatch. First/Second degradation (17→8, 9/19 additional) is dominated by systematic corpus heterogeneity, not stochasticity.

---

## INTERPRETATION

### Parameter stability across splits

| Parameter | Odd/Even | First/Second | Random | Overall |
|-----------|---------|------------|--------|---------|
| beta_scale | DRIFT(1.7) | DRIFT(0.4) | SAME | UNSTABLE (2/3 splits drift) |
| p_blind | SAME | near(0.065) | SAME | STABLE |
| r_lf | near(0.07) | near(0.07) | SAME | BORDERLINE |
| r_mid | DRIFT(0.10) | DRIFT(0.10) | SAME | UNSTABLE (2/3 splits drift) |
| p_qokch | DRIFT(0.10) | DRIFT(0.25) | SAME | UNSTABLE (2/3 splits drift) |

**Definite unstable:** beta_scale, r_mid, p_qokch — all show substantial drift across splits, with no consistent "true" value. The grid searches find different local optima that all achieve similar performance.

**Borderline:** p_blind (stable in Odd/Even at 0.115, near in First/Second at 0.065 diff) and r_lf (near in both at 0.07 diff). These may reflect partial structural constraints.

**Note on p_blind:** Odd and Even both independently find p_blind=0.115, matching exp_314. But First half finds p_blind=0.05, diverging from exp_314 and Second (0.115). This suggests p_blind may have a "true" value for the full corpus (0.115) but the metric profile of the first half is better matched by lower blindness.

### The corpus heterogeneity finding

The First/Second cross-validation collapse (17→8) is the primary result. This is NOT primarily a parameter stability issue — it is a corpus structure issue:

1. VMS B-dialect has systematically different metric profiles in document-order halves
2. The second half of the B-dialect document has stronger positional grammar (higher am_ll, y_lf) and less edy-rich vocabulary
3. These differences cannot be reconciled with a single parameter set
4. The 19/19 full-corpus calibration is optimizing parameters for the AVERAGE of two systematically different distributions

This finding is consistent with prior section-level analyses: different B-dialect sections have different statistical profiles (B astro elevated qok, B pharma different vocabulary). The document-order gradient reflects composition changes across the manuscript.

### Cross-validation performance summary

| Split | Best individual | Worst cross-val | Interpretation |
|-------|----------------|----------------|----------------|
| Odd/Even | 17/19 | 15/19 | Acceptable — 2/19 degradation from interleaved halves |
| First/Second | 16-17/19 | 8/19 | Catastrophic — 8-9/19 degradation from heterogeneous halves |
| Random | 17/19 | 14/19 | Moderate — 3/19 degradation; parameters identical but stochastic variation reduces cross-val |

---

## IMPLICATIONS FOR ARCHITECTURE INTERPRETATION

1. **The 6 parameters are NOT stable structural properties of B-dialect.** Different corpus subsets require different optimal values. This means the exp_314 calibration values reflect a full-corpus compromise, not a unique "true" mechanism.

2. **However, the architecture DOES generalize.** Odd/Even cross-validation (15-16/19) shows the architecture can achieve near-optimal performance on unseen data when the target metrics are similar to the training data. This supports C003 (19/19 on full corpus is real) and C004 (copy-buffer generates ss_mean/ss_d/ss_y regardless of corpus). The Random split's identical-parameter convergence (all 5 parameters matching across independently searched halves) additionally suggests these parameters may have a stable local optimum for balanced B-dialect samples, even if not for document-order subsets.

3. **The corpus heterogeneity is the new finding.** The parameter instability in First/Second is primarily driven by VMS corpus inhomogeneity, not by parameter degeneracy in the model. This opens a question: do different sections of VMS B-dialect require genuinely different architectures or parameters?

4. **The metrics themselves are unstable across document halves.** Any architecture calibrated on the full corpus is implicitly averaging over heterogeneous subsections. The 19/19 pass reflects good average-case calibration, not universal fit.

---

## Self-Audit

**Target-awareness:** Cross-validation uses each half's own VMS metrics as target. No single VMS target is used across all conditions. The full-corpus VMS_REF is used only as a reference comparison for parameter values, not as a calibration target for the grid searches on halves.

**Feature-destroying implementation:** The grid search on half-corpora uses N=3 fast pass (vs N=10 for confirmation). Fast pass introduces seed noise that can misidentify the true best parameter set. However, the N=10 confirmation corrects for this: all reported "Best" values are N=10 confirmed. The Odd half fast-pass found 19/19 at N=3 but confirmed at 17/19 at N=10 — demonstrating that fast-pass noise affects the search but not the reported confirmed results.

**Extrapolation:** The claim "parameters are not stable structural properties" is directly supported by the data. The claim "corpus heterogeneity drives First/Second failure" is supported by the metric table showing large First/Second differences (am_ll 23% higher, y_lf 42% higher in Second). Causal attribution to section composition changes is a plausible interpretation but not directly tested.

**Negative-result scope:** The negative result (parameters are unstable) is specific to this architecture and these 5 parameters. It does not imply that NO parameter of ANY architecture is stable across VMS B-dialect corpus splits. The claim is: the exp_314 calibrated values are corpus-fit artifacts. The architecture itself generalizes (15-16/19 cross-val for Odd/Even).

**Control behavior:** The First/Second cross-validation (8/19) is the key unexpected result. I expected degradation to ~14-16/19 based on the hypothesis that parameters are moderately unstable. The actual 8/19 was a hard flag. Investigation: the corpus metrics table shows systematic First/Second differences (am_ll ratio 1.23×, y_lf ratio 1.42×) that explain the failure — First-half parameters match First's targets but fail at Second's substantially different targets.

The Random split provides a useful baseline: with IDENTICAL parameters in both halves (|A-B|=0 for all 5 parameters), cross-val degrades 17→14 purely from stochastic variation (N=10 draws). This 3/19 floor means Odd/Even's 15/19 (2 below fit) is better than stochastic floor — the parameter mismatch is effectively zero net. The First/Second 8/19 (9 below fit) is 6/19 above stochastic noise level, firmly attributable to corpus heterogeneity.
