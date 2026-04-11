# exp_181: Onset-Preserving Modification Variant (Position-Aware Hybrid)
**Date**: 2026-04-10
**Hypothesis**: Does replacing the modification operation in exp_180 from onset-replacing to onset-preserving (suffix-replacing) allow the position-aware hybrid to simultaneously satisfy the dual constraint?
**Addresses**: opus_review_exp180.md points B1, B2, C2.
**Status**: OPUS PREDICTION CONFIRMED — 4/36 VIABLE. Onset-preserving modification breaks the ss_mean/adj_rate coupling identified in exp_180. Modified copies contribute to ss_mean (onset preserved) but not adj_rate (different word), allowing high MODIFY_PROB to drive down adj_rate while ss_mean remains stable. The dual constraint (am_ll ≥ 5.0×, ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015) is satisfiable by this architecture. However, all viable combinations still fall short of VMS measured values on every metric (am_ll 5.76 vs 6.81, ss_mean 1.26-1.39 vs 1.465, adj_rate 0.011-0.015 vs 0.009), and the architectural choices remain partly target-motivated.

**Configuration**: 36 combinations (COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6, 0.7, 0.8}). 50 simulations per combination. 1800 total runs. MID-only buffer: WINDOW=20. Seed base: 181000.

**Viability thresholds**: am_ll ≥ 5.0× AND ss_mean ∈ [1.2, 1.7] AND adj_rate ≤ 0.015.

**VMS targets**: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009.

---

## 1. HEADLINE RESULT

**4 / 36 combinations are viable.** Onset-preserving modification resolves the ss_mean/adj_rate coupling identified in exp_180 under onset-replacing modification.

### Best combination by joint score (am_ll × ss_mean): cp=0.7, mp=0.6
*(Not viable — adj_rate=0.0245 > 0.015. Listed for Opus prediction evaluation.)*
- am_ll = 5.772 [5.464, 6.035] — passes threshold ✓
- y_lf = 2.412 [2.194, 2.714] — flat (position gating) ✓
- ss_mean = 1.574 [1.487, 1.670] — passes threshold ✓
- ss_mean_mid = 1.869 [1.756, 2.054] — MID-only self-succession
- adj_rate = 0.0245 [0.0222, 0.0262] — **fails** adj threshold ✗

### Best viable combination: cp=0.6, mp=0.8
- am_ll = 5.755 [5.567, 5.959] — passes threshold ✓
- y_lf = 2.410 [2.133, 2.725]
- ss_mean = 1.385 [1.309, 1.481] — passes threshold ✓
- ss_mean_mid = 1.581 [1.503, 1.709]
- adj_rate = 0.0144 [0.0129, 0.0161] — **passes** threshold ✓

---

## 2. FULL PARAMETER GRID

| cp  | mp  | am_ll               | y_lf  | ss_full             | ss_mid              | adj_rate              | viable |
|-----|-----|---------------------|-------|---------------------|---------------------|-----------------------|--------|
| 0.2 | 0.3 | 5.779 [5.556, 6.026] | 2.363 | 1.077 [1.021, 1.141] | 1.119 [1.036, 1.204] | 0.0085 [0.0075, 0.0097] | no |
| 0.2 | 0.4 | 5.743 [5.548, 5.901] | 2.384 | 1.060 [0.981, 1.128] | 1.094 [1.003, 1.193] | 0.0077 [0.0066, 0.0088] | no |
| 0.2 | 0.5 | 5.791 [5.577, 6.042] | 2.378 | 1.072 [1.002, 1.126] | 1.100 [1.029, 1.190] | 0.0071 [0.0060, 0.0082] | no |
| 0.2 | 0.6 | 5.731 [5.468, 5.992] | 2.387 | 1.065 [1.005, 1.130] | 1.102 [1.005, 1.193] | 0.0065 [0.0055, 0.0075] | no |
| 0.2 | 0.7 | 5.742 [5.499, 5.982] | 2.405 | 1.065 [1.024, 1.107] | 1.099 [1.028, 1.170] | 0.0059 [0.0051, 0.0067] | no |
| 0.2 | 0.8 | 5.754 [5.548, 6.030] | 2.365 | 1.061 [0.983, 1.106] | 1.098 [1.014, 1.164] | 0.0053 [0.0043, 0.0064] | no |
| 0.3 | 0.3 | 5.760 [5.541, 6.072] | 2.373 | 1.124 [1.068, 1.192] | 1.182 [1.090, 1.265] | 0.0123 [0.0109, 0.0145] | no |
| 0.3 | 0.4 | 5.776 [5.512, 6.023] | 2.378 | 1.119 [1.047, 1.176] | 1.188 [1.098, 1.278] | 0.0112 [0.0098, 0.0121] | no |
| 0.3 | 0.5 | 5.767 [5.577, 6.043] | 2.373 | 1.114 [1.027, 1.182] | 1.175 [1.071, 1.258] | 0.0097 [0.0089, 0.0113] | no |
| 0.3 | 0.6 | 5.731 [5.484, 5.952] | 2.400 | 1.119 [1.058, 1.204] | 1.180 [1.090, 1.288] | 0.0089 [0.0076, 0.0099] | no |
| 0.3 | 0.7 | 5.768 [5.575, 5.964] | 2.390 | 1.113 [1.040, 1.195] | 1.182 [1.078, 1.273] | 0.0077 [0.0066, 0.0088] | no |
| 0.3 | 0.8 | 5.712 [5.470, 5.976] | 2.374 | 1.117 [1.053, 1.184] | 1.181 [1.091, 1.281] | 0.0069 [0.0060, 0.0081] | no |
| 0.4 | 0.3 | 5.791 [5.573, 6.013] | 2.381 | 1.171 [1.096, 1.238] | 1.265 [1.178, 1.355] | 0.0165 [0.0154, 0.0186] | no |
| 0.4 | 0.4 | 5.773 [5.570, 6.022] | 2.360 | 1.182 [1.134, 1.236] | 1.273 [1.188, 1.336] | 0.0147 [0.0131, 0.0163] | no |
| 0.4 | 0.5 | 5.742 [5.512, 6.006] | 2.375 | 1.171 [1.097, 1.245] | 1.267 [1.159, 1.357] | 0.0131 [0.0112, 0.0144] | no |
| 0.4 | 0.6 | 5.767 [5.510, 5.979] | 2.364 | 1.172 [1.100, 1.233] | 1.267 [1.162, 1.356] | 0.0116 [0.0106, 0.0129] | no |
| 0.4 | 0.7 | 5.760 [5.520, 5.946] | 2.380 | 1.167 [1.099, 1.239] | 1.257 [1.155, 1.387] | 0.0101 [0.0088, 0.0116] | no |
| 0.4 | 0.8 | 5.776 [5.527, 5.997] | 2.380 | 1.188 [1.102, 1.260] | 1.282 [1.175, 1.395] | 0.0087 [0.0072, 0.0100] | no |
| 0.5 | 0.3 | 5.712 [5.419, 6.095] | 2.378 | 1.261 [1.188, 1.343] | 1.402 [1.293, 1.506] | 0.0222 [0.0200, 0.0243] | no |
| 0.5 | 0.4 | 5.769 [5.518, 6.021] | 2.391 | 1.269 [1.181, 1.360] | 1.408 [1.300, 1.523] | 0.0195 [0.0177, 0.0214] | no |
| 0.5 | 0.5 | 5.777 [5.545, 5.999] | 2.347 | 1.264 [1.201, 1.338] | 1.400 [1.308, 1.481] | 0.0171 [0.0154, 0.0193] | no |
| **0.5** | **0.6** | **5.764 [5.533, 5.985]** | **2.368** | **1.276 [1.187, 1.363]** | **1.414 [1.271, 1.497]** | **0.0147 [0.0133, 0.0163]** | **YES** |
| **0.5** | **0.7** | **5.749 [5.507, 6.046]** | **2.358** | **1.260 [1.172, 1.338]** | **1.389 [1.261, 1.482]** | **0.0126 [0.0114, 0.0138]** | **YES** |
| **0.5** | **0.8** | **5.756 [5.464, 6.009]** | **2.385** | **1.262 [1.167, 1.338]** | **1.404 [1.277, 1.532]** | **0.0111 [0.0094, 0.0125]** | **YES** |
| 0.6 | 0.3 | 5.781 [5.495, 6.016] | 2.376 | 1.388 [1.287, 1.506] | 1.578 [1.469, 1.741] | 0.0292 [0.0269, 0.0314] | no |
| 0.6 | 0.4 | 5.787 [5.500, 6.014] | 2.404 | 1.406 [1.311, 1.481] | 1.611 [1.492, 1.733] | 0.0253 [0.0229, 0.0271] | no |
| 0.6 | 0.5 | 5.747 [5.555, 6.009] | 2.397 | 1.401 [1.333, 1.505] | 1.600 [1.491, 1.783] | 0.0220 [0.0204, 0.0239] | no |
| 0.6 | 0.6 | 5.742 [5.525, 6.017] | 2.392 | 1.379 [1.303, 1.458] | 1.578 [1.484, 1.688] | 0.0189 [0.0171, 0.0207] | no |
| 0.6 | 0.7 | 5.764 [5.548, 5.964] | 2.355 | 1.382 [1.306, 1.479] | 1.580 [1.498, 1.687] | 0.0163 [0.0149, 0.0183] | no |
| **0.6** | **0.8** | **5.755 [5.567, 5.959]** | **2.410** | **1.385 [1.309, 1.481]** | **1.581 [1.503, 1.709]** | **0.0144 [0.0129, 0.0161]** | **YES** |
| 0.7 | 0.3 | 5.765 [5.454, 6.135] | 2.404 | 1.575 [1.485, 1.664] | 1.868 [1.738, 2.000] | 0.0389 [0.0361, 0.0416] | no |
| 0.7 | 0.4 | 5.765 [5.521, 6.033] | 2.442 | 1.573 [1.461, 1.689] | 1.870 [1.711, 2.032] | 0.0332 [0.0306, 0.0359] | no |
| 0.7 | 0.5 | 5.761 [5.482, 6.064] | 2.400 | 1.574 [1.486, 1.690] | 1.866 [1.738, 2.009] | 0.0283 [0.0260, 0.0305] | no |
| 0.7 | 0.6 | 5.772 [5.464, 6.035] | 2.412 | 1.574 [1.487, 1.670] | 1.869 [1.756, 2.054] | 0.0245 [0.0222, 0.0262] | no |
| 0.7 | 0.7 | 5.736 [5.440, 5.965] | 2.414 | 1.581 [1.453, 1.698] | 1.880 [1.705, 2.001] | 0.0213 [0.0191, 0.0236] | no |
| 0.7 | 0.8 | 5.753 [5.533, 5.964] | 2.361 | 1.572 [1.460, 1.664] | 1.869 [1.755, 2.000] | 0.0188 [0.0174, 0.0202] | no |

### Effect of COPY_PROB on metrics (mean across MODIFY_PROB)

| cp  | am_ll mean | ss_mean mean | ss_mid mean | adj_rate mean |
|-----|-----------|-------------|------------|--------------|
| 0.2 | 5.757 | 1.067 | 1.102 | 0.0068 |
| 0.3 | 5.752 | 1.118 | 1.181 | 0.0094 |
| 0.4 | 5.768 | 1.175 | 1.269 | 0.0124 |
| 0.5 | 5.755 | 1.265 | 1.403 | 0.0162 |
| 0.6 | 5.763 | 1.390 | 1.588 | 0.0210 |
| 0.7 | 5.759 | 1.575 | 1.870 | 0.0275 |

**am_ll remains flat** across all COPY_PROB values (5.712–5.800), confirming position gating fully decouples am_ll from the copy component. y_lf also remains flat at ~2.36–2.44 across all 36 combinations (Opus C1: confirmed — MID-only buffer protects both LF and LL signals).

---

## 3. DIRECT COMPARISON TO exp_180 (exp_180 vs exp_181 at matched combinations)

For each (COPY_PROB, MODIFY_PROB) combination tested in both experiments (all 18 exp_180 combinations at MODIFY_PROB ∈ {0.3, 0.4, 0.5}):

| cp  | mp  | E180 ss | E181 ss | Δss     | E180 adj | E181 adj | Δadj    |
|-----|-----|---------|---------|---------|----------|----------|---------|
| 0.2 | 0.3 | 1.051   | 1.077   | +0.026  | 0.0083   | 0.0085   | +0.0002 |
| 0.2 | 0.4 | 1.022   | 1.060   | +0.038  | 0.0075   | 0.0077   | +0.0002 |
| 0.2 | 0.5 | 1.029   | 1.072   | +0.043  | 0.0068   | 0.0071   | +0.0003 |
| 0.3 | 0.3 | 1.078   | 1.124   | +0.046  | 0.0120   | 0.0123   | +0.0003 |
| 0.3 | 0.4 | 1.061   | 1.119   | +0.058  | 0.0108   | 0.0112   | +0.0004 |
| 0.3 | 0.5 | 1.045   | 1.114   | +0.069  | 0.0092   | 0.0097   | +0.0005 |
| 0.4 | 0.3 | 1.097   | 1.171   | +0.074  | 0.0158   | 0.0165   | +0.0007 |
| 0.4 | 0.4 | 1.088   | 1.182   | +0.094  | 0.0140   | 0.0147   | +0.0007 |
| 0.4 | 0.5 | 1.063   | 1.171   | +0.108  | 0.0121   | 0.0131   | +0.0010 |
| 0.5 | 0.3 | 1.144   | 1.261   | +0.117  | 0.0212   | 0.0222   | +0.0010 |
| 0.5 | 0.4 | 1.123   | 1.269   | +0.146  | 0.0185   | 0.0195   | +0.0010 |
| 0.5 | 0.5 | 1.094   | 1.264   | +0.170  | 0.0156   | 0.0171   | +0.0015 |
| 0.6 | 0.3 | 1.204   | 1.388   | +0.184  | 0.0278   | 0.0292   | +0.0014 |
| 0.6 | 0.4 | 1.156   | 1.406   | +0.250  | 0.0234   | 0.0253   | +0.0019 |
| 0.6 | 0.5 | 1.108   | 1.401   | +0.293  | 0.0198   | 0.0220   | +0.0022 |
| 0.7 | 0.3 | 1.252   | 1.575   | +0.323  | 0.0363   | 0.0389   | +0.0026 |
| 0.7 | 0.4 | 1.190   | 1.573   | +0.383  | 0.0332   | 0.0332   | +0.0030 |
| 0.7 | 0.5 | 1.148   | 1.574   | +0.426  | 0.0248   | 0.0283   | +0.0035 |

**Pattern**: Onset-preserving modification raises ss_mean by +0.026 to +0.426 across matched combinations, with the gain increasing with both COPY_PROB and MODIFY_PROB. adj_rate increases very slightly (+0.0002 to +0.0035), because modified copies now occasionally produce the same word even after suffix replacement (probability ≈ suffix collision rate, ~17%). The ss_mean gain is 10–120× larger than the adj_rate increase in absolute terms.

---

## 4. EVALUATION OF OPUS PREDICTION B1

### The prediction

Opus review B1: "Under onset-preserving modification, modified copies contribute to ss_mean (onset preserved) but not adj_rate (different word). This should allow high MODIFY_PROB to simultaneously produce elevated ss_mean and low adj_rate."

### The result: CONFIRMED

The mechanism predicted by Opus operates exactly as described. The clearest demonstration comes from the within-COPY_PROB profile across MODIFY_PROB:

**At cp=0.5 (most informative example):**

| mp  | ss_mean | adj_rate |
|-----|---------|----------|
| 0.3 | 1.261   | 0.0222   |
| 0.4 | 1.269   | 0.0195   |
| 0.5 | 1.264   | 0.0171   |
| 0.6 | 1.276   | 0.0147 ← viable |
| 0.7 | 1.260   | 0.0126 ← viable |
| 0.8 | 1.262   | 0.0111 ← viable |

**ss_mean is constant across the entire MODIFY_PROB range** (range: 1.260–1.276, a 1.3% spread). **adj_rate decreases by 2× from mp=0.3 to mp=0.8** (0.0222 → 0.0111). This is the decoupling Opus predicted: increasing MODIFY_PROB eliminates exact-word repetitions (adj_rate drops) without affecting onset-class succession (ss_mean flat).

At cp=0.7, the decoupling is even more striking:

| mp  | ss_mean | adj_rate |
|-----|---------|----------|
| 0.3 | 1.575   | 0.0389   |
| 0.4 | 1.573   | 0.0332   |
| 0.5 | 1.574   | 0.0283   |
| 0.6 | 1.574   | 0.0245   |
| 0.7 | 1.581   | 0.0213   |
| 0.8 | 1.572   | 0.0188   |

ss_mean range: 1.572–1.581 (0.6% spread over 50 percentage points of MODIFY_PROB). adj_rate drops by 52% from mp=0.3 to mp=0.8. The decoupling is essentially complete.

**Quantifying the improvement:** At matched adj_rate ≈ 0.015 (reading across experiments):
- exp_180 achieves this adj_rate at approximately (cp=0.4, mp=0.4) where ss_mean ≈ 1.088.
- exp_181 achieves the same adj_rate at approximately (cp=0.5, mp=0.6) where ss_mean ≈ 1.276, or at (cp=0.6, mp=0.8) where ss_mean ≈ 1.385.
- The ss_mean improvement at matched adj_rate is approximately +0.19–0.30×, confirming Opus's prediction.

### The implication for exp_180's "structural failure" claim

exp_180 concluded: "the copy mechanism cannot distinguish 'copy onset class' from 'copy exact word.'" This claim was overstatement specific to onset-replacing modification. Under onset-preserving modification, the mechanisms ARE distinguishable: MODIFY_PROB controls adj_rate while COPY_PROB controls ss_mean, and the two parameters operate on largely orthogonal parts of the metric space. The original claim should be narrowed to: "under onset-replacing modification, the copy mechanism cannot decouple onset-class succession from exact-word repetition."

### The remaining gap

Even with the decoupling, 4/36 combinations are viable and none reproduce VMS values:
- VMS am_ll=6.811 vs viable combination max am_ll ≈ 5.76 (84% of VMS)
- VMS ss_mean=1.465 vs viable combination max ss_mean ≈ 1.39 (95% of VMS)
- VMS adj_rate=0.009 vs viable combination min adj_rate ≈ 0.011 (viable threshold = 0.015)

The position-aware hybrid with onset-preserving modification enters the "not ruled out" zone but does not positively reproduce the VMS combination.

---

## 5. WITHIN-MID-ONLY SELF-SUCCESSION (Opus D4)

The ss_mid metric computes self-succession from within-line MID→MID consecutive bigrams only, excluding (a) LF↔MID transitions, (b) MID↔LL transitions, and (c) cross-line LL→LF transitions. These boundary bigrams are always between independently cipher-generated positions and dilute the ss_mean signal from the copy buffer.

**Key finding**: ss_mid is consistently 4–19% higher than ss_full at the same parameter combination.

| cp  | mp  | ss_full | ss_mid | ss_mid/ss_full |
|-----|-----|---------|--------|----------------|
| 0.5 | 0.6 | 1.276   | 1.414  | 1.108 |
| 0.6 | 0.3 | 1.388   | 1.578  | 1.137 |
| 0.6 | 0.8 | 1.385   | 1.581  | 1.142 |
| 0.7 | 0.3 | 1.575   | 1.868  | 1.186 |
| 0.7 | 0.8 | 1.572   | 1.869  | 1.189 |

At cp=0.7, ss_mid ≈ 1.869 — substantially above VMS ss_mean=1.465. This means the copy buffer IS generating strong onset-class self-succession within its operating domain; the full-corpus metric is diluted by the boundary positions. In an 8.4-word line, approximately 73% of within-line bigrams are MID→MID (where the buffer operates), and approximately 60% of all bigrams (including cross-line) are potentially MID→MID. The remaining 40% are boundary bigrams from cipher-generated positions.

This boundary dilution effect means: a model that could apply onset-preserving copying more broadly (not just MID) would produce higher full-corpus ss_mean. But such a model would risk diluting the positional signals — which is precisely why the position gating was introduced.

---

## 6. HONESTY CHECK

**Target-aware elements:**

1. **LL cipher table (explicitly target-aware, inherited from exp_177)**: All Latin clause-final morphemes → EVA -am. Onset weights calibrated to VMS LL distribution. Fully disclosed in exp_177 and carried forward.

2. **LF cipher table (partially target-aware, inherited from exp_177)**: Latin clause-initial patterns mapped to y-onset knowing y-onset is the VMS LF target. Disclosed.

3. **MID cipher table**: Uniform random EVA word from ONSET_WEIGHTS × SUFFIX_WEIGHTS. Not calibrated to any VMS MID metric.

4. **Buffer filtering (MID-only, structurally target-motivated)**: Same as exp_180. The restriction was designed knowing that VMS has both position-sensitive grammar AND self-succession, and these need to be generated by separate mechanisms. This is architectural target-motivation, not numeric calibration.

5. **Suffix replacement distribution**: The new suffix is drawn from SUFFIX_WEIGHTS — the global EVA vocabulary distribution. **Is this target-aware?** This distribution reflects overall VMS vocabulary, but is not calibrated to any specific VMS position metric (am_ll, ss_mean, adj_rate). The -am suffix has weight 0.020 in this distribution. When a MID word's suffix is replaced with -am, this slightly raises overall am rate, which would slightly REDUCE am_ll enrichment (more -am words at MID dilute the LL signal). The suffix distribution is not protecting any target metric; if anything, it slightly opposes the am_ll signal. **Not a target-awareness concern.**

6. **Surprise check**: The best combination by joint score (cp=0.7, mp=0.6) achieves am_ll=5.772 and ss_mean=1.574. Both are within the known simulation ranges for strong calibration and high-COPY_PROB MID-only copying. ss_mid at this combination (1.869) is above VMS ss_mean (1.465), but this is the undiluted within-MID metric — the full-corpus metric (1.574) is below VMS. No bug signal. The buffer filtering and position assignment logic were inspected; no error found.

7. **Viability threshold generosity**: As noted in exp_180, the adj_rate threshold (0.015) is 1.67× VMS (0.009). Even the "viable" combinations have adj_rate 0.011–0.015, which is 22–67% above VMS. If the threshold were set to VMS level (≤ 0.009), only cp=0.2 combinations would pass adj_rate — but those have ss_mean ≈ 1.06, far below the 1.2 ss_mean threshold. Under VMS-level adj_rate, 0/36 combinations would be viable.

---

## 7. LIMITATIONS

1. **Grid does not close the cp=0.7 band**: At cp=0.7, ss_mean ≈ 1.575 across all MODIFY_PROB values, and adj_rate decreases from 0.0389 to 0.0188 as mp goes from 0.3 to 0.8. To bring adj_rate below 0.015 at cp=0.7 would require mp ≈ 0.88+ (extrapolating linearly). This is not tested but would likely be viable by the threshold — though the required adj_rate would still be above VMS (0.009).

2. **Suffix collision rate**: Modified copies produce the same word as the original when the randomly drawn suffix matches the original suffix. For the most common suffix ('edy', weight 0.183), 18.3% of modifications produce no change; overall expected collision rate is ~17%. This means ~17% of "modified" copies still contribute to adj_rate. This is the residual coupling that prevents adj_rate from going to zero at high MODIFY_PROB.

3. **Character-level Timm modification not tested**: The original Timm/Schinner algorithm uses single-character replace/insert/delete. This is not quite onset-preserving (the modification can fall on the onset) and not quite suffix-preserving (it can fall anywhere). A test using the exact Timm modification would determine whether the original algorithm's properties place it between exp_180 (onset-replacing) and exp_181 (suffix-replacing) in the ss/adj trade-off space.

4. **Cross-line boundary dilution is structural**: The 40% dilution of ss_mean from boundary bigrams (cipher-generated positions at LF/LL) cannot be resolved by any parameter setting. The position-aware architecture intrinsically limits full-corpus ss_mean to be lower than within-MID ss_mean. For the best viable combination (cp=0.6, mp=0.8), the dilution factor is 1.581/1.385 ≈ 1.14. The VMS ss_mean of 1.465 would require full-corpus ss ≥ 1.465, which requires ss_mid ≥ 1.67 (at this dilution factor) — achieved only at cp ≥ 0.7, where adj_rate is still above threshold.

5. **A-dialect not tested**: All targets are B-dialect. The A-dialect has lower am_ll (3.562×, amply within reach) and similar ss_mean profile. An A-dialect calibrated test might show easier viability but was not a focus of this experiment.

6. **MID cipher table generates random EVA words without onset clustering**: The 30% of MID tokens generated by the cipher (when copying doesn't fire) are random EVA words with no sequential structure. If the MID cipher were calibrated to match observed MID-position onset distribution, ss_mean might increase slightly. This would constitute additional target-awareness and is not pursued here.

---

## 8. REPRODUCIBILITY

**Main run**: 36 combinations × 50 simulations, seed base 181000. Seed formula: `181000 + sim_i * 1000 + int(cp * 100) + int(mp * 10)`.

**Verification run**: 10 simulations at best combination by joint score (cp=0.7, mp=0.6), seed base 181999.

**Verification results:**
- am_ll: verify=5.768 vs main=5.772 (Δ=−0.004)
- ss_mean: verify=1.584 vs main=1.574 (Δ=+0.009)
- adj_rate: verify=0.0248 vs main=0.0245 (Δ=+0.0003)

All deltas are within expected variance for n=10. **The experiment is reproducible.**

---

## CONCLUSION

**The Opus meta-review prediction is confirmed: onset-preserving modification breaks the ss_mean/adj_rate coupling identified in exp_180.** 4/36 combinations satisfy all three viability thresholds simultaneously. The key mechanism: modified copies preserve onset class (contributing to ss_mean) but produce a different word (not contributing to adj_rate). MODIFY_PROB now operates as an adj_rate lever without meaningfully affecting ss_mean — a nearly perfect decoupling demonstrated by the flat ss_mean profile across MODIFY_PROB at each COPY_PROB level.

**The "structural failure" claim from exp_180 is partially retracted.** The correct claim is: under onset-replacing modification, the ss_mean/adj_rate coupling is structural. Under onset-preserving modification, the coupling is broken and the dual constraint becomes satisfiable within the tested grid.

**The remaining question is whether the mechanism is a plausible VMS explanation.** Two concerns:

1. **Quantitative gap**: Viable combinations produce am_ll ≈ 5.76 (84% of VMS 6.811), ss_mean ≈ 1.26–1.39 (86–95% of VMS 1.465), and adj_rate ≈ 0.011–0.015 (122–167% of VMS 0.009). The mechanism is "within the viability zone" by generous thresholds, but does not reproduce VMS measured values. Under VMS-level adj_rate (≤ 0.009), 0/36 combinations remain viable.

2. **Architectural target-motivation**: The position-aware architecture was designed knowing the dual constraint; the MID-only buffer restriction is not an independent architectural choice but a direct response to the known failure mode of position-blind copying. A complete VMS cipher hypothesis would need to justify the position-aware copy restriction on linguistic grounds.

**Updated cumulative sequence:**

| Experiment | Mechanism | am_ll | ss_mean | adj_rate | Viable |
|------------|-----------|-------|---------|----------|--------|
| exp_170/171 | Position-blind cipher/copy | ~1.0 | ~0.9/2.4 | 0.003/0.037 | 0/all |
| exp_177 | Position-sensitive cipher | 5.756 | 1.0 | 0.003 | 0/1 |
| exp_179 | Position-blind hybrid | 3.4–4.8 | 1.04–1.22 | 0.008–0.032 | 0/16 |
| exp_180 | Position-aware hybrid (onset-replacing) | 5.71–5.80 | 1.03–1.25 | 0.007–0.036 | 0/18 |
| **exp_181** | **Position-aware hybrid (onset-preserving)** | **5.71–5.80** | **1.06–1.58** | **0.005–0.039** | **4/36** |

The first viable combinations in the tested hypothesis space appear in exp_181. The "escape hatch" from exp_180 is open — but the VMS target values remain outside reach, and the adj_rate constraint is met only under a generous threshold already 1.67× VMS.

---

## FILES

- `script.py`: Onset-preserving modification variant (36 combinations × 50 sims = 1800 runs; 10-sim verification at best combo)
- `data/onset_preserving_results.json`: Raw results for all 1800 + 10 verification simulations
