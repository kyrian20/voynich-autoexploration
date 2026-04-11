# exp_180: Position-Aware Hybrid Cipher-Copy
**Date**: 2026-04-10
**Hypothesis**: Does a position-aware hybrid — where copying is restricted to MID positions only, and the position-sensitive cipher governs LF and LL positions exclusively — simultaneously satisfy the dual constraint (am_ll ≥ 5.0×, ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015)?
**Status**: OUTCOME 3 — DUAL CONSTRAINT UNSATISFIED BY POSITION-AWARE HYBRID. 0/18 viable. The am_ll signal is successfully protected by position gating (flat ~5.76-5.80× across all COPY_PROB values), but the MID-only copy buffer cannot simultaneously produce ss_mean ≥ 1.2× and adj_rate ≤ 0.015: the same copying that raises ss_mean also raises adj_rate, and no parameter setting separates the two. The failure mode is structurally different from exp_179 (which failed on am_ll vs ss_mean), but the escape hatch is closed.

**Configuration**: 18 combinations (COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5, 0.6, 0.7} × MODIFY_PROB ∈ {0.3, 0.4, 0.5}). 50 simulations per combination. 900 total runs. MID-only buffer: WINDOW=20 MID-position tokens. Seed base: 180000.

**Viability thresholds**: am_ll ≥ 5.0× AND ss_mean ∈ [1.2, 1.7] AND adj_rate ≤ 0.015.

**VMS targets**: am_ll=6.811, y_lf=3.506, ss_mean=1.465, adj_rate=0.009.

---

## 1. HEADLINE RESULT

**0 / 18 combinations are viable.**

The best combination by joint score (am_ll × ss_mean) is **cp=0.7, mp=0.3**:
- am_ll = 5.800 [5.199, 6.279] — passes viability threshold (≥ 5.0) ✓
- y_lf = 2.399 [2.178, 2.573] — below VMS (3.506) but above position-blind baseline
- ss_mean = 1.252 [1.180, 1.351] — passes ss_mean threshold (≥ 1.2) ✓
- adj_rate = 0.0363 [0.0328, 0.0388] — **fails** viability threshold (≤ 0.015) ✗

No combination simultaneously satisfies am_ll ≥ 5.0, ss_mean ≥ 1.2, and adj_rate ≤ 0.015. The am_ll constraint is met by all 18 combinations; the binding incompatibility is between ss_mean and adj_rate.

---

## 2. FULL PARAMETER GRID

| cp  | mp  | am_ll               | y_lf                | ss_mean             | adj_rate              | viable |
|-----|-----|---------------------|---------------------|---------------------|-----------------------|--------|
| 0.2 | 0.3 | 5.766 [5.505, 6.020] | 2.370 [2.204, 2.539] | 1.051 [0.993, 1.122] | 0.0083 [0.0072, 0.0095] | no |
| 0.2 | 0.4 | 5.727 [5.520, 5.917] | 2.381 [2.233, 2.600] | 1.022 [0.946, 1.090] | 0.0075 [0.0065, 0.0086] | no |
| 0.2 | 0.5 | 5.790 [5.573, 5.994] | 2.386 [2.167, 2.563] | 1.029 [0.959, 1.082] | 0.0068 [0.0058, 0.0079] | no |
| 0.3 | 0.3 | 5.763 [5.494, 6.048] | 2.376 [2.250, 2.523] | 1.078 [1.008, 1.157] | 0.0120 [0.0105, 0.0139] | no |
| 0.3 | 0.4 | 5.767 [5.520, 6.048] | 2.384 [2.209, 2.605] | 1.061 [1.000, 1.117] | 0.0108 [0.0096, 0.0123] | no |
| 0.3 | 0.5 | 5.769 [5.460, 6.070] | 2.376 [2.159, 2.521] | 1.045 [0.981, 1.105] | 0.0092 [0.0079, 0.0105] | no |
| 0.4 | 0.3 | 5.766 [5.452, 6.051] | 2.384 [2.169, 2.543] | 1.097 [1.017, 1.156] | 0.0158 [0.0145, 0.0173] | no |
| 0.4 | 0.4 | 5.738 [5.404, 6.086] | 2.354 [2.127, 2.484] | 1.088 [1.033, 1.144] | 0.0140 [0.0125, 0.0155] | no |
| 0.4 | 0.5 | 5.752 [5.413, 6.005] | 2.366 [2.168, 2.497] | 1.063 [1.001, 1.155] | 0.0121 [0.0103, 0.0132] | no |
| 0.5 | 0.3 | 5.705 [5.360, 5.999] | 2.379 [2.136, 2.549] | 1.144 [1.083, 1.211] | 0.0212 [0.0194, 0.0236] | no |
| 0.5 | 0.4 | 5.788 [5.554, 6.124] | 2.385 [2.237, 2.570] | 1.123 [1.062, 1.239] | 0.0185 [0.0167, 0.0204] | no |
| 0.5 | 0.5 | 5.771 [5.477, 6.017] | 2.365 [2.113, 2.623] | 1.094 [1.000, 1.160] | 0.0156 [0.0141, 0.0176] | no |
| 0.6 | 0.3 | 5.776 [5.220, 6.211] | 2.355 [2.149, 2.617] | 1.204 [1.084, 1.292] | 0.0278 [0.0261, 0.0304] | no |
| 0.6 | 0.4 | 5.763 [5.392, 6.286] | 2.394 [2.130, 2.682] | 1.156 [1.099, 1.217] | 0.0234 [0.0207, 0.0255] | no |
| 0.6 | 0.5 | 5.800 [5.374, 6.338] | 2.381 [2.174, 2.616] | 1.108 [1.044, 1.175] | 0.0198 [0.0185, 0.0216] | no |
| 0.7 | 0.3 | 5.800 [5.199, 6.279] | 2.399 [2.178, 2.573] | **1.252** [1.180, 1.351] | 0.0363 [0.0328, 0.0388] | no |
| 0.7 | 0.4 | 5.768 [5.264, 6.240] | 2.363 [2.130, 2.587] | 1.190 [1.090, 1.278] | 0.0302 [0.0273, 0.0318] | no |
| 0.7 | 0.5 | 5.770 [5.163, 6.306] | 2.385 [2.195, 2.637] | 1.148 [1.076, 1.204] | 0.0248 [0.0226, 0.0267] | no |

### Effect of COPY_PROB on metrics (mean across MODIFY_PROB)

| cp  | am_ll mean | ss_mean mean | adj_rate mean |
|-----|-----------|-------------|--------------|
| 0.2 | 5.761 | 1.034 | 0.0075 |
| 0.3 | 5.766 | 1.061 | 0.0107 |
| 0.4 | 5.752 | 1.082 | 0.0140 |
| 0.5 | 5.755 | 1.120 | 0.0184 |
| 0.6 | 5.779 | 1.156 | 0.0237 |
| 0.7 | 5.779 | 1.197 | 0.0304 |

**The am_ll profile is flat** across all COPY_PROB values (range: 5.705–5.800). Position gating fully decouples am_ll from the copy component. ss_mean and adj_rate both increase monotonically with COPY_PROB.

### Per-onset self-succession at best combination (cp=0.7, mp=0.3)

| Onset | ss mean | VMS target |
|-------|---------|-----------|
| qok   | 1.153   | 1.623 (A), 1.239 (B) |
| ok    | 1.288   | 1.930 (A), 1.462 (B) |
| ch    | 1.314   | 1.427 (A), 1.694 (B) |
| sh    | 1.247   | — |
| d     | 1.226   | — |
| y     | 1.297   | — |

All onset classes show elevated self-succession at cp=0.7, mp=0.3, but all fall below VMS B-dialect targets for the primary three onset classes.

---

## 3. COMPARISON TO exp_179

For each COPY_PROB value also tested in exp_179, at MODIFY_PROB=0.3:

| cp  | E179 am_ll | E180 am_ll | Δam_ll  | E179 ss_mean | E180 ss_mean | Δss_mean |
|-----|-----------|-----------|---------|-------------|-------------|---------|
| 0.2 | 4.804     | 5.766     | +0.962  | 1.075       | 1.051       | −0.024  |
| 0.3 | 4.306     | 5.763     | +1.457  | 1.114       | 1.078       | −0.036  |
| 0.4 | 3.826     | 5.766     | +1.940  | 1.163       | 1.097       | −0.066  |
| 0.5 | 3.359     | 5.705     | +2.346  | 1.217       | 1.144       | −0.073  |

**Two observations:**

1. **Position gating protects am_ll** exactly as predicted. At cp=0.5 (where exp_179's am_ll collapsed to 3.359), exp_180 maintains 5.705 — a +2.346 improvement. The flat am_ll profile across COPY_PROB in exp_180 confirms complete decoupling of the two mechanisms.

2. **Position gating reduces ss_mean** relative to exp_179. At all matched COPY_PROB values, exp_180's ss_mean is 0.024–0.073 lower than exp_179's. The restriction to MID-only copying reduces self-succession generation because (a) LF and LL tokens — which in exp_179 were copied into the buffer and could be re-copied with onset-class clustering — are now excluded, and (b) each line's LF and LL positions act as sequential "resets" (independently cipher-generated) that break onset-class continuity.

The position-aware architecture successfully trades the exp_179 binding constraint (am_ll vs ss_mean) for a different failure mode (ss_mean vs adj_rate), but does not escape the dual constraint.

---

## 4. INTERPRETATION

### (a) Does the position-aware hybrid satisfy the dual constraint?

**No.** 0/18 combinations are viable. The position gating achieves its intended effect: am_ll is fully protected (5.705–5.800 across all 18 combinations, uniformly above the 5.0 threshold). This is the key structural improvement over exp_179. However, the dual constraint still fails — the binding constraints shift from am_ll vs ss_mean (exp_179) to **ss_mean vs adj_rate** in exp_180.

The fundamental problem: in a MID-only copy buffer, every copy event that reproduces an onset class (producing ss_mean enrichment) is equally a potential exact-word reproduction (producing adj_rate enrichment). The VMS shows ss_mean ≈ 1.465× alongside adj_rate ≈ 0.009 — a combination of high onset-class clustering with low exact-repetition rate. A copy buffer cannot produce this combination because the mechanism that produces sequential onset clustering (copying the same word or a word with the same onset) is the same mechanism that produces exact repetitions. MODIFY_PROB provides partial relief (modified copies preserve onset-class succession while reducing exact repetitions) but insufficient relief: even at the maximum MODIFY_PROB=0.5 in the grid, the combination with ss_mean ≥ 1.2 (cp=0.7) has adj_rate=0.0248 — still more than 1.6× the 0.015 threshold.

Stated quantitatively: to reach ss_mean ≥ 1.2, the grid requires COPY_PROB ≥ 0.6. At COPY_PROB=0.6, the minimum adj_rate across MODIFY_PROB settings is 0.0198 (at mp=0.5). The 0.015 adj_rate threshold is not reached at any MODIFY_PROB setting compatible with ss_mean ≥ 1.2.

### (b) N/A — no combination is viable.

### (c) Why does it fail despite the position gating?

The MID-only buffer restriction successfully addresses the am_ll dilution problem from exp_179, but it introduces a new constraint: the buffer is now smaller per unit time. In a line of length L, approximately (L−2) words are MID words and contribute to the buffer; only (L−2) positions use the buffer. At L≈8.4 (the empirical B-dialect mean), roughly 6.4 MID words per line enter the buffer. This is adequate for onset-class self-succession generation, but the self-succession generated in MID positions comes at the cost of higher adj_rate.

The deeper issue is that VMS's self-succession signal is inconsistent with Timm-style copying at any adj_rate threshold consistent with VMS. The VMS adj_rate of 0.009 (0.9% exact adjacent repetitions) is essentially at the level of a corpus without deliberate copy mechanism — it is barely above what would be expected from random draws given the vocabulary distribution. Yet VMS ss_mean ≈ 1.465 is elevated. This combination — elevated onset-class clustering without elevated exact-word repetition — is inconsistent with a copy mechanism at any copy probability, because the copy mechanism cannot distinguish "copy onset class" from "copy exact word." The VMS combination suggests the onset-class clustering is intrinsic to the vocabulary structure (certain onset classes appear in similar syntactic/semantic contexts) rather than generated by copying.

This conclusion was already reached in exp_179 but is now strengthened: it survives the position-aware architectural improvement.

---

## 5. HONESTY CHECK

**Target-aware elements in this experiment:**

1. **LL cipher table (explicitly target-aware, inherited from exp_177)**: ALL Latin clause-final morphemes (-um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at) are mapped to EVA -am specifically. The code comment from exp_177 labels -am as "the target LL suffix." The LL onset weights (d: 0.40, ok: 0.15, qok: 0.15, ch: 0.10) are calibrated to VMS LL onset distribution. This target-awareness is disclosed in the exp_177 result and carried forward unchanged.

2. **LF cipher table (partially target-aware, inherited from exp_177)**: Latin clause-initial patterns (qu-, no, et, at) are mapped to y-onset knowing y-onset is the VMS LF enrichment target.

3. **MID cipher table (NOT target-aware)**: `cipher_mid()` is a uniform random EVA word from ONSET_WEIGHTS × SUFFIX_WEIGHTS. No VMS MID metric was used to calibrate this table. The MID table is effectively the same as the Timm/Naibbe baseline vocabulary. This is noted explicitly in the code comment: "NOT calibrated to any VMS MID-position target metric."

4. **Buffer filtering rule (architecturally motivated, arguably target-motivated)**: The choice to restrict the copy buffer to MID-position tokens was made knowing that (a) the VMS dual constraint requires decoupling am_ll from copying, and (b) this decoupling is achieved by keeping LF/LL tokens in the cipher-only domain. The filtering rule was designed to satisfy a known dual constraint target, not to hit a specific numeric VMS value. This is a form of **structural target-awareness** — the architecture was designed to escape the exp_179 failure — which is methodologically appropriate (we are testing whether the mechanism works) but should be acknowledged. A researcher proposing this cipher architecture as a VMS hypothesis would need to justify the MID-only restriction independently of the VMS data.

5. **Surprise check**: The best combination (cp=0.7, mp=0.3) achieves am_ll=5.800 and ss_mean=1.252. Both are below VMS levels (6.811 and 1.465), and neither jointly reaches VMS. The am_ll=5.800 is consistent with the exp_177 strong-calibration baseline (5.756), as expected from position gating. No result is surprisingly strong — no combination reaches am_ll ≥ 6.5× AND ss_mean ≥ 1.4× simultaneously. The buffer filtering and position assignment logic were inspected during script development; no bug was found.

---

## 6. LIMITATIONS

This experiment tests one specific position-aware architecture. Untested variants include:

1. **MID + LF copying, LL cipher only**: Copying at LF (not LL) would add LF tokens to the buffer, potentially increasing ss_mean by including y/t/s-onset cluster contributions. This might also dilute y_lf enrichment if copies at LF override the y-onset cipher.

2. **Position-stratified buffer**: A buffer segmented by position (copy MID-from-MID, copy LF-from-LF, etc.) might generate stronger self-succession at boundary positions. This is architecturally equivalent to separate onset-class grammars per position — functionally a grammar rule.

3. **Onset-class-filtered buffer**: A buffer that copies only words of the same onset class as the current position's random draw. This would produce high ss_mean with lower adj_rate (modified copies that preserve onset). However, this requires knowing the onset class of the "would-be" generated word, which is circular — equivalent to a structured grammar rule for onset-class selection.

4. **Different WINDOW sizes**: WINDOW=20 was used (exp_177/exp_179 default). Smaller windows (5-10) produce stronger self-succession at the cost of higher adj_rate; larger windows weaken both. This is not expected to resolve the ss_mean vs adj_rate trade-off, only shift its position.

5. **Non-uniform MODIFY_PROB across onset classes**: MODIFY_PROB was applied uniformly. A class-conditional modification rate (e.g., modify qok-onset copies at higher rate than ok-onset copies) might allow differential adj_rate control. This adds a parameter per onset class and is not operationalized.

6. **Hybrid with high-MODIFY_PROB + very high COPY_PROB beyond 0.7**: Extrapolating the grid, COPY_PROB=0.8-0.9 would increase ss_mean further but adj_rate would likely reach 0.04-0.06, widening the gap to the 0.015 threshold.

None of these variants are expected to resolve the fundamental VMS combination of high ss_mean with low adj_rate, which requires onset-class clustering that is not driven by word-level copying.

---

## 7. REPRODUCIBILITY

**Main run**: 18 combinations × 50 simulations, seed base 180000. Seed formula: `180000 + sim_i * 1000 + int(cp * 100) + int(mp * 10)`.

**Verification run**: 10 simulations at best combination (cp=0.7, mp=0.3), seed base 180999. Seed formula: `180999 + sim_i`.

**Verification results** (vs main run mean):
- am_ll: verify=5.6319 vs main=5.7998 (Δ=−0.1679)
- ss_mean: verify=1.2321 vs main=1.2519 (Δ=−0.0198)
- adj_rate: verify=0.0364 vs main=0.0363 (Δ=+0.0001)

The am_ll delta (−0.168) is within expected variance for n=10 (the main run CI at cp=0.7, mp=0.3 is [5.199, 6.279], a width of ≈1.08; the verify mean is well inside this CI). The ss_mean delta (−0.020) is similarly within expected variance. The adj_rate is effectively identical. **The experiment is reproducible.**

---

## CONCLUSION

**The position-aware hybrid closes the exp_179 am_ll dilution problem but fails the dual constraint through a different mechanism.** Position gating successfully decouples am_ll from COPY_PROB: am_ll is uniformly 5.7–5.8× across all 18 combinations, compared to 3.4–4.8× in exp_179's matched combinations. The architectural improvement works as intended.

However, the new failure mode — ss_mean vs adj_rate incompatibility in the MID-only buffer — means 0/18 combinations are viable. The ss_mean vs adj_rate trade-off is inherent to any copy mechanism: copying produces onset-class clustering and exact-word repetition simultaneously, and MODIFY_PROB cannot fully decouple them. The VMS combination of ss_mean ≈ 1.465× with adj_rate ≈ 0.009 requires onset-class sequential structure that is not copy-driven.

**Cumulative theory-elimination sequence:**

| Experiment | Mechanism | am_ll failure | ss_mean failure | adj_rate failure | Viable |
|------------|-----------|--------------|-----------------|------------------|--------|
| exp_170/171 | Position-blind cipher/copy | ~1.0× (vs 5.0 threshold) | Overproduce (Timm) or ~0.86-0.96 (Naibbe) | Timm: 0.037 | 0/all |
| exp_177 | Position-sensitive cipher (strong) | 5.756× ✓ | ~1.0× ✗ | ~0.003 ✓ | 0/1 |
| exp_179 | Position-blind hybrid | 3.4-4.8× (diluted by copies at LL) ✗ | 1.035-1.217× ✗ | varies | 0/16 |
| **exp_180** | **Position-aware hybrid** | **5.7-5.8× ✓ (flat)** | **1.034-1.252× ✗** | **>0.015 at high cp ✗** | **0/18** |

**The remaining uneliminated mechanism is intrinsic structured grammar** — or a mechanism that produces onset-class sequential clustering through semantic/syntactic word-class constraints rather than through a copy buffer. A copy buffer cannot produce VMS-level self-succession without also producing VMS-inconsistent exact-repetition rates.

---

## FILES

- `script.py`: Position-aware hybrid simulation (18 combinations × 50 sims = 900 runs; verification 10 sims at best combo)
- `data/position_aware_results.json`: Raw results for all 900 + 10 verification simulations
