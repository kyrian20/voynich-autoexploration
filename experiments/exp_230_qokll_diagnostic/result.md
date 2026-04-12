# exp_230: H430 — qok_ll Diagnostic

**Date**: 2026-04-11  
**Hypothesis**: H430 — Why does the simulation produce qok_ll=0.764 when VMS-calibrated LL/MID onset distributions predict ≈0.537? Can identifying and fixing the root cause bring qok_ll within ±20% of VMS 0.595?  
**Status**: H430 ANSWERED — ROOT CAUSE IDENTIFIED: non-blind LL fraction uses VMS MID onset (qok=14.19%) instead of VMS LL onset (qok=7.62%), inflating sim LL qok from target 7.62% to actual 9.87%. Fix: use VMS LL onset for non-blind LL fraction + re-calibrate d_boost. Generates H431.

---

## Design

Mechanism isolation: run N=20 simulations per configuration with diagnostic counters tracking actual qok rates at MID, LL, and LF positions separately.

**Configurations tested**:
- A: Full exp_229 (all mechanisms: p_qokch=0.12, p_stutter=0.009, edy fresh-fallback)
- B: No Markov (p_qokch=0.00)
- C: No Stutter (p_stutter=0.000)
- D: No edy fresh (unchanged fallback)
- E: No edy at all (exp_221 baseline)

---

## Key Finding: Diagnostic Clarification of qok_ll Formula

The metric `qok_ll` is computed as:
```
qok_ll = (qok_rate_at_LL) / (qok_rate_global)
```
NOT as `(qok_rate_at_LL) / (qok_rate_at_MID)` as originally assumed.

**VMS reference values**:
- VMS MID qok = 14.19%
- VMS LL qok = 7.62%
- VMS global qok = 12.80%
- VMS qok_ll (theoretical) = 7.62% / 12.80% = **0.595** ✓ matches VMS target

---

## Diagnostic Results

```
Config                                    qok_ll  %VMS  MID_qok  LL_qok  Global_qok  Pred_qok_ll
Full exp_229 (all mechanisms)             0.767  129%   13.83%   9.87%    12.87%      0.767
No Markov (p_qokch=0.00)                  0.760  128%   14.19%  10.02%    13.21%      0.759
No Stutter (p_stutter=0.000)              0.767  129%   13.78%   9.86%    12.86%      0.767
No edy fresh (unchanged fallback)         0.760  128%   14.00%   9.91%    13.06%      0.759
No edy at all (exp_221 baseline)          0.747  126%   14.22%   9.87%    13.23%      0.746
```

**Key observations**:
1. `Pred_qok_ll = LL_qok / Global_qok` exactly matches the observed `qok_ll` in all configurations. The metric formula is confirmed.
2. **LL qok is consistently 9.87-10.02% across ALL mechanism configurations** — the mechanism (Markov, stutter, edy) does not affect LL qok. The root cause is structural to the LL generation, not the MID mechanisms.
3. Global qok is approximately 12.80-13.21% — close to VMS 12.80%.
4. qok_ll ≈ LL_qok / Global_qok ≈ 9.87/12.87 = 0.767 ← matches observed.
5. VMS target: 7.62 / 12.80 = 0.595.

---

## Root Cause: LL Non-Blind Fraction Uses VMS MID Onset

The `cipher_ll_blind` function generates LL words as:
- **Blind fraction (p_blind=0.30)**: onset from `ll_onsets` (VMS LL distribution with 'd' boosted, **qok excluded** → qok=0%)
- **Non-blind fraction (1-p_blind=0.70)**: calls `random_eva_word(onset_weights, ...)` where `onset_weights = onset_weights_mid` (VMS MID distribution, **qok=14.19%**)

Expected sim LL qok = 0.30 × 0% + 0.70 × 14.19% = **9.93%** ← matches observed ~9.87%. ✓

**This is a design error**: the non-blind LL fraction should use VMS LL onset (qok=7.62%), not VMS MID onset (qok=14.19%). The VMS LL non-blind fraction is not modeled with the VMS LL onset distribution — it uses MID onset instead.

Additionally, `build_ll_onsets` excludes qok from the blind fraction: even the blind LL fraction has 0% qok (VMS LL qok = 7.62%). Both issues contribute to the discrepancy.

---

## Interpretation

### Finding 1: qok_ll failure is entirely due to LL qok overproduction

The LL qok is 9.87% (sim) vs 7.62% (VMS) — 30% too high. The global qok is near VMS level (12.87% sim vs 12.80% VMS). The qok_ll gap comes entirely from the LL overproduction, not from global or MID qok rates.

### Finding 2: All tested mechanisms are irrelevant to qok_ll

None of the toggles (Markov, stutter, edy fresh-fallback, edy at all) significantly affect qok_ll. The LL generation is completely independent of these MID mechanisms. This confirms the root cause is structural to the LL generator itself.

### Finding 3: The fix is clean and architectural

The correct fix:
1. Change `cipher_ll_blind`: for the non-blind fraction (70%), use `onset_ll_vms` (VMS LL distribution, qok=7.62%) instead of `onset_weights_mid` (VMS MID, qok=14.19%)
2. Include qok in `ll_onsets`: remove qok exclusion from `build_ll_onsets` (currently `if o not in ('d', 'qok')` → change to `if o != 'd'`)
3. Re-calibrate d_boost for the new non-blind d contribution from VMS LL

Expected LL qok after fix:
- Blind fraction (30%): ll_onsets_fixed has qok ≈ 7.62% (no longer excluded)
- Non-blind fraction (70%): onset_ll_vms has qok = 7.62%
- Total LL qok ≈ 7.62% ← matches VMS

Expected qok_ll = 7.62% / 12.80% = 0.595 ← exact VMS target ← PASS zone [0.476, 0.714]

New d_boost formula with VMS LL non-blind:
d_ll_target = p_blind × d_boost_new / d_global + (1-p_blind) × VMS_LL_d / d_global
→ d_boost_new = d_global × [d_ll_target - (1-p_blind) × (VMS_LL_d/d_global)] / p_blind
= d_global × [1.362 - 0.70 × (LL_d / d_global)] / 0.30

VMS LL d = d_ll_target × d_global = 1.362 × 6.70% = 9.12%.
d_boost_new = 6.70% × [1.362 - 0.70 × 1.362] / 0.30 = 6.70% × [1.362 × (1-0.70)] / 0.30
= 6.70% × 1.362 × 0.30 / 0.30 = 6.70% × 1.362 = 9.12%

So d_boost_new = 9.12% (approximately). Generates H431 — LL onset fix experiment.

---

## Limitations

1. **N=20 for mechanism isolation**: Standard for diagnostic.
2. **Only qok_ll and position-specific qok rates measured**: Other metrics not reported in detail. The fix (H431) will measure the full 18-metric battery.
3. **d_boost recalibration approximate**: The formula assumes the blind fraction's d contribution is independent. In practice, `build_ll_onsets` normalizes after setting d_boost, which may produce slightly different d contribution. H431 will verify empirically.

---

## Self-Audit

**Target-awareness**: Diagnostic only — no calibration. The finding is mechanistic (root cause analysis).

**Feature-destroying implementation**: N/A for diagnostic.

**Extrapolation**: The root cause (non-blind LL uses MID onset) is confirmed by the formula: observed LL qok = 0.30×0% + 0.70×14.19% = 9.93% ≈ observed 9.87%. This is a mathematical derivation, not an extrapolation.

**Negative-result scope**: N/A — diagnostic provides positive result (root cause identified).

**Control behavior**: The `Pred_qok_ll = LL_qok / Global_qok` matches `qok_ll` exactly in all 5 configurations — confirming that the qok_ll formula is as expected and the diagnostic counters are correct.

---

## Conclusion

H430 ANSWERED. qok_ll=0.764 failure root cause: non-blind LL fraction (70% of LL words) uses VMS MID onset (qok=14.19%) instead of VMS LL onset (qok=7.62%), inflating sim LL qok from target 7.62% to 9.87%. The qok exclusion from `ll_onsets` (blind fraction) compounds the issue.

**Fix** (H431): use VMS LL onset for non-blind LL fraction + include qok in ll_onsets + re-calibrate d_boost. Expected result: qok_ll → 0.595 (exact VMS target), PASS. This would fix the qok_ll failure without affecting any MID/LF metrics. Generates exp_231.
