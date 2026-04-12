# exp_256 Result: H459 — B-Dialect ot→ot Recheck After 'Other' Onset Bug Fix

**Outcome: H459 CONFIRMED (gap exists but smaller). p_ot_ot=0.10 WAS OVER-CALIBRATED; B-dialect reverts to 12 mechanisms.**

---

## Bug Fix Verification

Pre-fix B-dialect MID 'other' rate = 5.99%. Post-fix onset_mid['ot'] = 7.67% (VMS=7.21%,
ratio 1.064 — from renormalization). Sim MID ot rate with fix = 7.37% (VMS=7.21%, ratio 1.02
— excellent match). The fix correctly restores ot onset rates.

---

## ot→ot MID Results After Bug Fix

| Condition | Sim_mid | VMS_mid | Δ | Status |
|---|---|---|---|---|
| Baseline (no p_ot_ot) | 1.726 | 1.887 | -0.161 | Gap persists but SMALL |
| p_ot_ot=0.10 | 2.285 | 1.887 | +0.398 | OVER-PRODUCED |

---

## Key Findings

### 1. True B-Dialect ot→ot Gap = Δ=-0.161 (not Δ=-0.477)
The contaminated exp_246 measurement showed Δ=-0.477. After fixing the 'other' onset bug,
the true gap is only Δ=-0.161. The contamination overstated the gap by 0.316.

BREAKDOWN: exp_246 reported sim=1.410 (contaminated) vs VMS=1.887. After fix, sim=1.726
(ratio 1.02 ot rate match) vs VMS=1.887. The improvement from contaminated to fixed:
1.726-1.410 = +0.316 — exactly what the 'other' onset inflation caused.

### 2. p_ot_ot=0.10 Was Calibrated to Wrong Baseline — Now Over-Produces
p_ot_ot=0.10 was designed to close Δ=-0.477. After fix, the true gap is only -0.161,
and p_ot_ot=0.10 over-shoots by +0.398. The calibration is invalid.

To close the true gap Δ=-0.161, a smaller value would be needed: linear interpolation
between p=0.00 (Δ=-0.161) and p=0.10 (Δ=+0.398) gives p_ot_ot ≈ 0.03 to match VMS.

### 3. Architecture Decision: Remove p_ot_ot, Revert to 12 Mechanisms
Arguments for removing p_ot_ot=0.10:
- It was calibrated to a contaminated gap (the mechanism was motivated by an artifact)
- With correct distributions, p=0.10 over-produces ot→ot by +0.398 (worse than before)
- The true gap (Δ=-0.161) is below the battery's ±20% tolerance (±0.377 around 1.887)
- ot→ot is not a battery metric — the 12-mechanism baseline passes 19/19 regardless

HOWEVER: the gap Δ=-0.161 is real and not zero. A corrected p_ot_ot ≈ 0.03 would close
it. This is left for a future experiment if ot→ot becomes a higher priority.

DECISION: **Remove p_ot_ot from B-dialect architecture. Revert to 12 mechanisms (exp_249).**

B-dialect architecture (12 mechanisms, fixed distributions, pending battery verify):
  p_blind=0.115, p_lf=1.0, cp=0.55, mp=0.90, p_qokch=0.12, p_chqok=0.12, p_stutter=0.006,
  r_lf=0.12, r_mid=0.25, mu_len=8.4, sigma_len=3.0, ll_onsets with d_boost

PENDING: Full 19-metric battery verification of 12-mechanism baseline with fixed 'other'
distributions (onset_mid, onset_lf, onset_ll all filtered). The 19-metric battery was
verified at 19/19 in exp_249 with contaminated distributions; verification needed to confirm
battery still passes after renormalization. → H460 generated.

### 4. B-Dialect ot→ot Structure: Small Genuine Gap After Fix
The fixed baseline (Δ=-0.161) reveals that the copy-buffer architecture weakly under-produces
ot→ot in B-dialect MID — but much less than previously thought. The stars section dominates
ot→ot (78% of pairs from N=88/113, per F252). This section-level structure may explain the
residual gap via a mechanism the corpus-wide buffer doesn't capture (section-local vocabulary
persistence), rather than requiring an explicit ot→ot Markov rule.

---

## Corrections to Prior Findings

**F253 is CORRECTED**: p_ot_ot=0.10 was added to fix a contaminated gap (Δ=-0.477). True gap
after bug fix = Δ=-0.161. p_ot_ot=0.10 now over-produces by +0.398. p_ot_ot removed from
architecture. B-dialect reverts to 12 mechanisms. The 19/19 PASS claim in F253 was valid
(battery doesn't test ot→ot) but the structural characterization was wrong.

**F246 is PARTIALLY CORRECTED**: The B-dialect ot→ot sim=1.410 (global) was contaminated. 
True fixed baseline ot→ot E_mid = 1.726 (not 1.410). The MID gap is Δ=-0.161, not Δ=-0.477.
VMS ot→ot E_mid=1.887 (N=113) is unchanged.

---

## Self-Audit

**Target-awareness**: No new parameters. The fix (filter_other) is principled — removes
non-onset string from onset distribution. Not calibrated to match any specific metric.

**Feature-destroying implementation**: None. Filtering 'other' restores correct onset
frequencies for the test feature (ot→ot). Both p=0.00 and p=0.10 conditions are tested.

**Extrapolation**: The architecture decision (remove p_ot_ot) is based on contamination
diagnosis, not a claim that ot→ot is impossible to model. The corrected gap (Δ=-0.161) could
be closed by a smaller parameter. Not claiming "ot→ot is not real" — only that the previously
calibrated parameter magnitude was wrong.

**Negative-result scope**: The "p_ot_ot=0.10 over-produces" finding is scoped to this
parameter value after bug fix. A smaller p_ot_ot (≈0.03) might close the gap without
overshooting — not tested in this experiment.

**Control behavior**: VMS ot→ot E_mid=1.887 (N=113, stable measurement). Sim ot rate with
fix = 7.37% (VMS=7.21%, ratio 1.02 — excellent). Post-fix onset_mid['ot']=7.67% is slightly
above VMS (1.064× from renormalization) but sim ot rate matches well (buffer dynamics bring
it closer to VMS level). No unexpected control behavior.
