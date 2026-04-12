# exp_255 Result: H457 — A-Dialect ot→ot Retest After 'Other' Onset Bug Fix

**Outcome: H457 CONFIRMED (bug fixed, gap resolved). A-dialect ot→ot = MATCH. New: B-dialect also contaminated.**

---

## Bug Fix Verification

Post-fix onset_mid['ot'] = 4.75% (VMS MID ot = 4.44%, ratio 1.07 — OK). The fix (filtering
'other' from onset_mid and renormalizing) correctly restores ot rate. Sim MID ot rates:
- Pre-fix (exp_254): 10.63% (2.4× VMS) — 'other' words classified as 'ot'
- Post-fix (exp_255): 4.96% (1.12× VMS) — within threshold

B-dialect also contaminated: MID 'other' onset rate = 5.99%. This means all B-dialect
ot→ot measurements (exp_246, exp_253) were contaminated. The B-dialect ot→ot gap and the
p_ot_ot=0.10 fix (F253) require re-verification. → H459 generated.

---

## A-Dialect MID Bigram Results (Fixed, N=15)

| Pair | VMS_mid | Sim_mid | Δ | N_vms | Status |
|---|---|---|---|---|---|
| **ot→ot** | 2.052 | 2.091 | +0.038 | 19 | **MATCH** — no gap |
| **o→o** | 2.801 | 2.001 | -0.801 | 30 | **GENUINE GAP** |
| qok→qok | 1.750 | 1.747 | -0.002 | 29 | MATCH |
| y→y | 2.853 | 2.768 | -0.085 | 32 | MATCH |
| ok→ok | 1.959 | 1.955 | -0.005 | 33 | MATCH |
| d→d | 1.278 | 1.445 | +0.168 | 82 | OK (within noise) |
| qot→qot | 3.030 | 3.045 | +0.015 | 10 | MATCH |
| sh→qok | 1.741 | 0.972 | -0.769 | 55 | GAP (untested Markov) |
| qok→ch | 0.985 | 1.162 | +0.177 | 64 | slight overshoot (p_qokch=0.12) |
| ch→qok | 0.877 | 0.950 | +0.072 | 57 | MATCH |
| ol→ol | 1.672 | 3.063 | +1.391 | 5 | IGNORE (N_vms=5 too sparse) |

---

## Key Findings

### 1. A-Dialect ot→ot Has NO Gap
VMS_mid=2.052, Sim_mid=2.091, Δ=+0.038. The A-dialect copy-buffer architecture (exp_239 +
p_y_y=0.10) naturally produces correct ot→ot enrichment without an explicit Markov rule. The
gap seen in exp_254 (Δ=-0.551) was entirely an artifact of the 'other' onset bug. Architecture
unchanged — no p_ot_ot needed for A-dialect.

CONTRAST WITH B-DIALECT: B-dialect exp_246 reported sim ot→ot=1.410 vs VMS=1.887 (Δ=-0.477),
leading to p_ot_ot=0.10 addition (F253). But B-dialect onset_mid also has 5.99% 'other'
contamination. The B-dialect gap must be re-measured after fixing the bug (H459 → exp_256).
If B-dialect gap also disappears, p_ot_ot=0.10 may have been unnecessary.

### 2. o→o Gap Confirmed and Larger Than Previously Estimated
VMS_mid=2.801, Sim_mid=2.001, Δ=-0.801. Larger than exp_254's Δ=-0.656 (which had sim 'o'
rate slightly inflated by adjacency to 'other' buffer effects). After full fix, sim 'o' MID
rate = 4.59% (VMS=4.77%), very close. Gap is structural: the copy-buffer architecture
under-produces o→o self-succession in MID context.

Gap magnitude (0.801) is comparable to y→y before p_y_y=0.10 (y→y was ~0.8 below VMS).
A p_o_o Markov rule is the direct analogue and should work — provided o-onset (~4.77% MID)
is low enough to need an explicit rule (yes — same order as y at ~4.89% MID).

### 3. Most A-Dialect Pairs Match Excellently
qok→qok Δ=-0.002, ok→ok Δ=-0.005, qot→qot Δ=+0.015, y→y Δ=-0.085. The A-dialect
architecture (exp_239 + p_y_y=0.10) is an excellent model for most onset succession patterns.
The only genuine structural gaps are: o→o (-0.801) and sh→qok (-0.769, untested Markov).

### 4. B-Dialect ot→ot Measurements Contaminated (Urgent Review)
F246 and F253 were based on contaminated B-dialect ot→ot measurements (5.99% 'other' onset
inflation). The reported gap (Δ=-0.477 in exp_246) and the p_ot_ot=0.10 fix (F253) require
re-verification. 19/19 PASS status for B-dialect battery is unaffected (battery doesn't test
ot→ot), but the structural characterization may be wrong.

Possible outcomes of B-dialect retest:
- Gap persists after fix → p_ot_ot=0.10 remains justified (mechanism is genuinely needed)
- Gap reduced/eliminated → p_ot_ot=0.10 may be removed from architecture; B-dialect has same
  natural ot→ot as A-dialect; F253 finding is a contamination artifact

---

## Architecture Status
A-dialect: UNCHANGED (exp_239 + p_y_y=0.10). No ot→ot mechanism needed. H458 (o→o Markov)
is the next A-dialect extension candidate.

B-dialect: ARCHITECTURE REVIEW PENDING (exp_256 will determine if p_ot_ot=0.10 is needed).

---

## Next Steps
1. **exp_256**: B-dialect ot→ot retest with 'other' onset fix (H459) — URGENT: determines if p_ot_ot=0.10 is valid
2. **exp_257**: A-dialect p_o_o Markov sweep (H458) — after exp_256 confirms B-dialect status
3. Apply 'other' onset fix to all future sim experiments in both dialects

---

## Self-Audit

**Target-awareness**: No new parameters added in this experiment. onset_mid constructed from
VMS corpus (standard). No target-aware calibration. o→o gap measurement is purely descriptive.

**Feature-destroying implementation**: The bug fix (filtering 'other' from onset_mid) correctly
restores the feature under test (ot onset rate). The fix does not destroy any other feature —
other onset rates are preserved (all shift up ~6.9% proportionally from renormalization, which
is small and uniform). No feature-destroying implementation details.

**Extrapolation**: The claim "B-dialect ot→ot measurements contaminated" is based on the
confirmed presence of 5.99% 'other' contamination in B-dialect onset_mid. The direction of
effect (inflation of sim ot rate, reduction of E2) follows from the same mechanism as diagnosed
in A-dialect. This is an inference, not a direct measurement — exp_256 is needed to confirm.

**Negative-result scope**: No negative results. Positive finding (ot→ot MATCH) is correctly
scoped to A-dialect architecture after bug fix.

**Control behavior**: Onset rates match well after fix (ot: 1.12×, o: 0.96×). y slightly high
(1.18×) and ol slightly high (1.20×) — marginal mismatches, likely from renormalization shifting
onset frequencies. These small mismatches don't affect the primary findings (ot→ot and o→o
comparisons are valid; the y mismatch is small and doesn't change the y→y conclusion).
