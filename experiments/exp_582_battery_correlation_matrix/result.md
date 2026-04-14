# exp_582: Battery Correlation Matrix for 19-Metric Battery

**Date:** 2026-04-12  
**Type:** Verification experiment (paper support)  
**Status:** COMPLETE — EFFECTIVE DIMENSION HIGH (≥16)

---

## Question

What is the effective number of independent constraints measured by the 19-metric battery used in C008 / exp_314 / exp_574? The paper's "19/19 PASS" framing implicitly assumes 19 independent constraints; mechanistic analysis suggests some metrics are linked (self-succession metrics, Menzerath subcomponents, adj_rate/copy-buffer dynamics). This experiment quantifies the actual independence.

---

## Method

**Corpus and architecture:** 21-mechanism architecture at exp_314 parameters (beta_scale=1.8, CP=0.55, MP=0.90, P_STUTTER=0.006, R_LF=0.12, R_MID=0.20, all other parameters as defined in exp_314). B-dialect VMS distributions used as targets. N=200 independent simulation trials, each generating TARGET_LINES=2411 lines.

**Data matrix:** Each trial produces a vector of 19 metric values. N=200 trials → 200×19 data matrix. The variation across trials reflects stochastic variability of the generative model with fixed parameters, not VMS corpus noise.

**Correlation analysis:** 19×19 Pearson correlation matrix computed from the standardized data matrix (numpy `np.corrcoef`).

**PCA:** Eigenvalue decomposition of the 19×19 correlation matrix. Number of components for 95% variance explanations reported.

**Clustering:** Union-find clustering at |r|≥0.7 and |r|≥0.5 thresholds. Effective dimension = number of distinct clusters + singletons.

---

## Results

### Per-trial metric statistics (N=200)

| Metric | Mean | CV% | Notes |
|--------|------|-----|-------|
| am_ll | 6.930 | 2.6% | Low variance (blind mechanism dominates) |
| d_ll | 1.264 | 6.4% | |
| y_lf | 2.955 | 6.7% | |
| ss_mean | 1.330 | 3.6% | |
| adj_rate | 0.0103 | 7.5% | |
| qok_lf | 0.846 | 6.4% | |
| d_lf | 1.924 | 5.9% | |
| s_lf | 4.415 | 5.9% | |
| ch_ll | 0.931 | 5.5% | |
| ok_ll | 1.024 | 8.1% | |
| qok_ll | 0.557 | 7.8% | |
| ss_d | 1.430 | 7.8% | |
| ss_y | 1.662 | 15.9% | Highest variance |
| am_lf_enr | 0.108 | 43.3% | Very high variance (small base) |
| am_mid_enr | 0.216 | 12.4% | |
| edy_rate | 0.169 | 2.6% | Low variance (vocabulary locked) |
| word_len_mean | 5.171 | 0.3% | Near-constant |
| qok_ch | 1.226 | 3.6% | |
| global_am_rate | 0.022 | 4.6% | |

### Correlation matrix highlights

| Category | Pairs | r | Threshold |
|----------|-------|---|-----------|
| Strong | am_ll / am_mid_enr | −0.936 | |r|≥0.5 |
| Moderate | y_lf / ss_y | −0.371 | |r|≥0.3 |
| Moderate | edy_rate / word_len_mean | +0.355 | |r|≥0.3 |
| All other | 168 pairs | <|0.3| | |

**Only 1 pair exceeds |r|=0.5. The correlation structure is nearly diagonal.**

### PCA (eigenvalue decomposition of 19×19 correlation matrix)

| Component | Eigenvalue | CumVar% |
|-----------|-----------|---------|
| PC1 | 2.193 | 11.5% |
| PC2 | 1.787 | 20.9% |
| PC3 | 1.566 | 29.2% |
| PC4 | 1.415 | 36.6% |
| PC5 | 1.353 | 43.8% |
| PC6 | 1.214 | 50.1% |
| PC7 | 1.163 | 56.3% |
| PC8 | 1.057 | 61.8% |
| PC9 | 1.043 | 67.3% |
| PC10 | 0.962 | 72.4% |
| PC11 | 0.877 | 77.0% |
| PC12 | 0.835 | 81.4% |
| PC13 | 0.735 | 85.3% |
| PC14 | 0.687 | 88.9% |
| PC15 | 0.658 | 92.3% |
| **PC16** | **0.537** | **95.2%** ← 95% threshold |
| PC17 | 0.468 | 97.6% |
| PC18 | 0.422 | 99.8% |
| PC19 | 0.029 | 100.0% |

**Components for 95% variance: 16**

The "flat" eigenvalue spectrum (all PCs except PC19 near 1.0) is characteristic of near-independent variables. PC19 (eigenvalue 0.029) corresponds to the near-degenerate direction am_ll + am_mid_enr (the conservation axis).

### Clustering results

At |r|≥0.7: **18 groups** (1 cluster of 2 + 17 singletons)  
At |r|≥0.5: **18 groups** (same structure)  
Only cluster: {am_ll, am_mid_enr}

**Effective independent dimension:**
- PCA (95%): **16**
- Clustering (|r|≥0.7): **18**
- Conservative (min): **16**

---

## Interpretation

### Effective dimension is 16–18, far above the expected 8–13

The pre-experiment expectation was 8–13 independent constraints based on mechanistic reasoning about shared drivers. The actual effective dimension is 16 (PCA) to 18 (clustering). This is a strong positive result: the 19-metric battery captures 16–18 genuinely independent statistical dimensions of simulation behavior.

### Why expected clusters do NOT appear

The mechanistic prediction assumed that metrics driven by the same mechanism would correlate. This prediction is wrong because correlation depends on *variance*, not just shared mechanism:

**Self-succession metrics (ss_mean, ss_d, ss_y):** All driven by the copy-buffer, but each samples a different onset class's token pool. Trial-to-trial variation in copy frequency affects each class's pool independently → near-zero cross-correlations. The moderate negative y_lf/ss_y correlation (−0.37) arises because y-onset tokens concentrated at LF are less available for MID y→y succession — a different mechanistic link than shared copy-buffer.

**qok metrics (qok_lf, qok_ll, qok_ch):** All involve qok onset. Despite shared onset class, positional placement (LF vs LL) and bigram context (qok→ch) are controlled by different distributional parameters and fluctuate independently.

**am group (am_lf_enr, am_mid_enr, am_ll, global_am_rate):** Only am_ll and am_mid_enr are correlated (r=−0.94). This reflects a conservation law: the blind LL mechanism commits -am tokens to LL with probability p_blind_n per line. When more lines trigger this (stochastically higher p_blind_n activations), am_ll rises and am_mid_enr falls because fewer -am tokens remain for MID positions. global_am_rate varies too little (CV=4.6%) to be detected; am_lf_enr has too much random variation (CV=43%) to show this conservation.

**adj_rate:** The stutter mechanism (P_STUTTER=0.006, fixed) is independent of the copy-buffer mechanism that drives ss_*. Although both generate word repetitions, they operate on different tokens and different moments of the simulation.

### The one mechanically-linked pair

am_ll and am_mid_enr are genuinely mechanically linked (conservation of -am tokens across positions). Collapsing them to a single constraint is correct. Effective dimension becomes 18 under clustering.

The additional reduction from 18 to 16 under PCA is attributable to the moderate correlations (y_lf/ss_y at −0.37, edy_rate/word_len_mean at +0.35), which together remove roughly 2 units of variance.

### Implication for the paper

The "19/19 PASS" framing is well-justified. The paper should report:

> "The 19-metric battery captures approximately 16 independent constraints (PCA: 16 components for 95% variance; correlation clustering: 18 groups at |r|≥0.7), with only one mechanically-linked pair (am_ll / am_mid_enr, r=−0.94 reflecting position conservation). The effective independent dimension substantially exceeds the 8–13 range where the framing would require qualification."

The paper does NOT need to add a substantial qualification of the "19/19" framing beyond acknowledgment of the one correlated pair. The framing is accurate.

---

## Limitations

1. **Trial variance, not corpus variance:** The correlation matrix measures stochastic simulation variance, not variance across VMS sections. The independence structure could differ if measured across VMS subsets. However, the relevant question for the battery (does the architecture have 19 distinguishable constraints?) is about simulation behavior, not VMS statistics.

2. **Fixed parameters across trials:** All 200 trials use identical parameters. Parameter sensitivity (how metrics respond to parameter changes) could show different correlation structure than stochastic variance does. A parameter-sweep correlation matrix might find different clusters (e.g., all am-metrics would correlate positively if p_blind_n were varied).

3. **N=200 may miss weak correlations:** At N=200, correlations below ~|r|=0.14 are not reliably detectable (p<0.05 threshold at N=200 is |r|≈0.14). The 168 "near-zero" correlations are bounded by this detection limit. However, weak correlations (|r|<0.14) have negligible impact on effective dimension estimates.

4. **am_lf_enr high variance (CV=43%):** This metric's high variance is due to a small base rate (-am at LF is a rare event). This high noise floor means correlations involving am_lf_enr are attenuated by noise, potentially masking real mechanistic links. If am_lf_enr were measured on larger corpora, its correlation with global_am_rate might emerge.

---

## Self-Audit

**Target-awareness:** The 21-mechanism architecture parameters (CP, MP, R_LF, R_MID, beta_scale, etc.) were calibrated using VMS target metrics in exp_314. The correlation matrix measures simulation-internal variance given these fixed calibrated parameters. The claim "effective dimension ≈ 16" is therefore conditional on these parameters: a differently calibrated architecture (e.g., higher P_STUTTER) would show different correlation structure. This conditionality does NOT invalidate the paper implication — the paper uses these specific parameters, so the simulation-internal correlation structure at these parameters is the relevant quantity.

**Feature-destroying implementation:** The experiment uses the exp_314 simulation code exactly. No implementation detail destroys any feature under test. The correlation matrix computation uses standard Pearson correlation on the per-trial metric vectors. No issues identified.

**Extrapolation:** The effective dimension estimate (16–18) is derived from the N=200 simulation runs at fixed parameters. The claim is: "under exp_314 parameters with N=200 trials, the effective dimension is 16 (PCA) to 18 (clustering)." No claim is made about other parameter settings or other architectures. All claims are within the tested range.

**Negative-result scope:** N/A — this is a characterization experiment, not a mechanism test. The "negative" aspect is the absence of expected correlations (ss_mean/ss_d/ss_y not correlated). This absence is within scope: it shows that under fixed parameters, these metrics vary independently. The claim is not "these metrics can never be correlated under any architecture" — only that they are independent under these parameters.

**Control behavior:** No explicit control corpus in this experiment. The "control" expectation (effective dimension 8–13) was based on mechanistic reasoning about shared drivers. The actual result (effective dimension 16–18) contradicts this expectation. Investigation: the mechanistic reasoning was wrong about which properties generate cross-trial correlation. Specifically, "shared mechanism" does not imply "correlated across trials" when the shared mechanism's variance is low relative to other sources of trial-to-trial variation. No methodology revision needed — the finding stands.
