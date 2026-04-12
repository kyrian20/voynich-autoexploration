# exp_284: H488 — Restore LF Midfix

**Date**: 2026-04-11  
**Hypothesis**: H488 — Restoring LF midfix sampling (dropped in exp_280 rewrite) will close the LF_wl gap (4.854 → VMS 5.732), restore negative Menzerath r, and maintain 19/19.

## Background

- exp_270: Added LF/LL midfix → menz_r=-0.052 (from +0.097), LF/LL_wl gaps closed.
- exp_280: Added MID midfix (p_mf=0.20) but cipher_lf passed `{}, 0.0` — LF midfix omitted. LF_wl=4.854 (0.88 chars short). menz_r flipped to ~+0.097.
- exp_282: Word-index conditioning (gamma=0.30, alpha=0.15) → menz_r=+0.037 (still positive).
- exp_283 (F283): Root cause identified — sim LF_wl < MID_wl (reversed from VMS), causing positive Menzerath r. Fix: restore LF midfix.

## Method

Architecture: 14-mechanism B-dialect sim (exp_257 params + p_mf=0.20 + gamma=0.30 + alpha=0.15).  
Restoration: cipher_lf() now calls `make_word_sim(onset, suffix, rng, lf_nemed, p_lf_mf)` with LF-specific midfix distribution built from VMS B-dialect LF words.  
Also restored: cipher_ll() applies LL midfix at empirical VMS rate (p_ll=0.486).

Empirical VMS rates computed from corpus:
- LF midfix presence: 0.582 (254 unique midfixes)
- LL midfix presence: 0.486 (208 unique midfixes)
- MID midfix presence: 0.448 (528 unique midfixes)

Part 1/2 — Sweep p_lf_mf ∈ {0.00, 0.20, 0.30, 0.40, 0.50}, N=10 each:

| p_lf_mf | PASS  | menz_r  | mid_slope | word_len | lf_wl | mid_wl |
|---------|-------|---------|-----------|----------|-------|--------|
| 0.00    | 19/19 | -0.0225 | -0.0277   | 5.389    | 4.844 | 5.427  |
| 0.20    | 19/19 | -0.0606 | -0.0291   | 5.438    | 5.267 | 5.423  |
| 0.30    | 19/19 | -0.0684 | -0.0274   | 5.466    | 5.481 | 5.426  |
| 0.40    | 19/19 | -0.0917 | -0.0314   | 5.487    | 5.672 | 5.423  |
| 0.50    | 19/19 | -0.0918 | -0.0287   | 5.516    | 5.887 | 5.433  |

Selection criterion: 19/19 AND most negative menz_r → **p_lf_mf=0.50**

Part 3 — Full N=30 at p_lf_mf=0.50:

| Metric        | VMS    | Sim    | %VMS   | Status |
|---------------|--------|--------|--------|--------|
| am_ll         | 6.5498 | 7.0612 | 107.8% | PASS   |
| d_ll          | 1.3625 | 1.1962 | 87.8%  | PASS   |
| y_lf          | 3.1837 | 2.8369 | 89.1%  | PASS   |
| ss_mean       | 1.1640 | 1.3329 | 114.5% | PASS   |
| adj_rate      | 0.0090 | 0.0092 | 102.5% | PASS   |
| qok_lf        | 0.7450 | 0.7548 | 101.3% | PASS   |
| d_lf          | 2.1178 | 1.8342 | 86.6%  | PASS   |
| s_lf          | 4.4422 | 4.3851 | 98.7%  | PASS   |
| ch_ll         | 0.9653 | 1.0177 | 105.4% | PASS   |
| ok_ll         | 1.0028 | 1.1592 | 115.6% | PASS   |
| qok_ll        | 0.6121 | 0.6224 | 101.7% | PASS   |
| ss_d          | 1.5850 | 1.5018 | 94.7%  | PASS   |
| ss_y          | 1.9550 | 1.8230 | 93.2%  | PASS   |
| am_lf_enr     | 0.1225 | 0.1333 | 108.8% | PASS   |
| am_mid_enr    | 0.1954 | 0.1917 | 98.1%  | PASS   |
| edy_rate      | 0.1940 | 0.1683 | 86.7%  | PASS   |
| word_len_mean | 5.4000 | 5.5147 | 102.1% | PASS   |
| qok_ch        | 1.2670 | 1.2342 | 97.4%  | PASS   |
| global_am_rate| 0.0203 | 0.0191 | 94.1%  | PASS   |

**TOTAL: 19/19 PASS**

Diagnostics (not in battery):
- Menzerath r: sim=-0.1077, VMS=-0.225 (48% of target, correct sign)
- MID slope: sim=-0.029, VMS=-0.058 (50% of target)
- LF_wl: 5.889 (VMS=5.732) — 2.7% above
- MID_wl: 5.428 (VMS=5.409) — 0.9% above
- LL_wl: 5.697 (VMS=5.015) — 13.6% above [CONCERN]

## Interpretation

**H488 CONFIRMED**: Restoring LF midfix to cipher_lf resolves the architectural regression introduced in exp_280. Key results:

1. **Position ordering corrected**: LF_wl=5.889 > MID_wl=5.428 (VMS: LF=5.732 > MID=5.409). The reversed ordering (sim LF < MID) that was the structural cause of positive Menzerath r is eliminated.

2. **Menzerath r flipped**: -0.108 (from +0.037 at exp_282). Correct sign, 48% of VMS -0.225. The remaining gap (-0.108 vs -0.225) is a remaining diagnostic gap, not a battery failure.

3. **19/19 maintained at all tested p_lf_mf values**: Adding LF midfix does not disturb any battery metric. Battery PASS is robust to the choice of p_lf_mf in [0.00, 0.50].

4. **LL_wl excess**: LL_wl=5.697 (VMS=5.015), a 0.68-char excess. LL midfix at empirical rate 0.486 makes LL words too long. This is a new diagnostic concern — LL_wl is not in the 19-metric battery, so it does not cause failures, but it may be contributing to the Menzerath r gap by making LL words longer (which also pushes r toward negative). The 48% Menzerath r may be partly driven by LL_wl excess rather than purely by LF ordering.

**Note on p_lf_mf calibration**: p_lf_mf=0.50 was selected as the value producing most negative menz_r. The VMS empirical LF midfix presence rate is 0.582, so p_lf_mf=0.50 is slightly below empirical. The 19/19 battery result holds at all tested values and is NOT conditional on the specific p_lf_mf; the Menzerath r diagnostic is conditional on p_lf_mf=0.50.

## Limitations

1. Menzerath r gap: -0.108 vs VMS -0.225 (48%). Further gradient mechanisms may be needed.
2. LL_wl=5.697 vs VMS 5.015: LL midfix at empirical rate produces words that are too long. The interaction between LL midfix and Menzerath r needs investigation — if LL words are too long, this inflates the long-line/short-word-length correlation in a way that may partially mask the true gap.
3. MID slope: -0.029 vs VMS -0.058 (50%). The within-line gradient mechanism (exp_282) closes half the gap.
4. p_lf_mf sweep only went to 0.50 (below empirical 0.582). Results at p_lf_mf=0.582 (full empirical) were not tested.

## Follow-up Questions

1. Does reducing p_ll_mf (LL midfix rate below empirical 0.486) bring LL_wl=5.697 down to VMS 5.015 AND further improve Menzerath r?
2. Is the Menzerath r gap (-0.108 vs -0.225) mainly due to LL_wl excess or to insufficient LF/MID gradient?
3. Would testing p_lf_mf=0.582 (VMS empirical rate) produce lf_wl≈5.732 while maintaining 19/19?

## Self-Audit

**Target-awareness**: The LF, LL, and MID midfix distributions are built from VMS B-dialect words (empirical measurement). p_lf_mf=0.50 was selected as the most negative menz_r among 19/19 values; menz_r is a *diagnostic* metric NOT in the 19-metric battery. The 19/19 PASS result is NOT conditional on this calibration — all tested p_lf_mf values give 19/19. The Menzerath r value (-0.108) is conditional on p_lf_mf=0.50, as stated in Interpretation.

**Feature-destroying implementation**: LF midfix sampling adds characters between onset and suffix in LF words, directly lengthening them. This is the correct implementation of the feature. No implementation detail destroys or degrades the hypothesized effect.

**Extrapolation**: No "cannot" or "structural" claims made. The remaining Menzerath r gap (-0.108 vs -0.225) is described as a "diagnostic gap," not an architectural limit. Higher p_lf_mf values (>0.50) not tested.

**Negative-result scope**: N/A — positive result.

**Control behavior**: No explicit shuffled/reference control. Baseline (p_lf_mf=0.00 with LL midfix active) gives menz_r=-0.022 — already slightly negative due to LL midfix extending LL words. LF midfix adds to this, pushing to -0.108. The monotonic improvement in menz_r with increasing p_lf_mf is a coherent signal confirming the causal mechanism. LL_wl=5.697 vs VMS 5.015 is a new diagnostic concern flagged in Interpretation and Follow-up.

## Conclusion

H488 CONFIRMED. LF midfix restoration closes the LF_wl gap (4.854→5.889 vs VMS 5.732), flips Menzerath r from +0.037 to -0.108 (correct sign), and maintains 19/19. Architecture now has 15 mechanisms: 12 (exp_257) + p_mf=0.20 (MID midfix) + gamma=0.30 (buffer length bias) + alpha=0.15 (onset bias) + p_lf_mf=0.50 (LF midfix). New diagnostic concern: LL_wl=5.697 vs VMS 5.015 (LL midfix rate may need reduction, H489).
