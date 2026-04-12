# exp_254 Result: H450 — A-Dialect MID-Only Bigram Tracking

**Outcome: PARTIALLY ANSWERED — 'other' onset bug invalidates ot→ot; o→o gap confirmed real**

---

## Bug Discovered: 'other' Onset String Collision

The simulation uses string labels as onset keys in `onset_mid`. A-dialect MID words include
6.48% (406/6264) with unrecognized onsets, stored as key `'other'` in `onset_mid`. When the
sim draws `'other'` as an onset, `make_word_sim` concatenates it literally, producing words
beginning with 'other'. Since 'ot' appears before 'o' in `ONSET_ORDER`, `get_onset('other...')
= 'ot'`.

Result: sim global ot = 9.89% (VMS = 4.48%), sim MID ot = 10.63% (VMS = 4.44%). The ~6%
excess matches `onset_mid['other'] = 0.0648` exactly.

Composition of 'other' onset words: 'c'-starting (cph*, ckh*, etc.): 44%; 'a'-starting: 44%;
'e', 'q' words: 12%.

**Fix for future experiments**: filter `'other'` from `onset_mid` and renormalize before passing
to sim. Or remap 'c'-onset words to a recognized category.

---

## Valid Results (not affected by 'other' bug)

| Pair | VMS_mid | Sim_mid | Δ | N_vms | Status |
|---|---|---|---|---|---|
| qok→qok | 1.750 | 1.672 | -0.078 | 29 | MATCH — confirms exp_251 |
| y→y | 2.853 | 2.986 | +0.133 | 32 | slight MID overshoot; p_y_y=0.10 calibrated to global |
| ok→ok | 1.959 | 1.918 | -0.041 | 33 | MATCH |
| d→d | 1.278 | 1.458 | +0.180 | 82 | slight overshoot; within noise |
| o→o | 2.801 | 2.145 | -0.656 | 30 | GENUINE GAP — sim 'o' rate correct (4.63% vs 4.77%) |
| sh→qok | 1.741 | 0.968 | -0.773 | 55 | same architectural limit as B-dialect |
| qok→ch | 0.985 | 1.148 | +0.163 | 64 | slight overshoot from p_qokch=0.12 |
| ch→qok | 0.877 | 0.958 | +0.081 | 57 | MATCH (p_chqok=0.00 correct for A-dialect) |

## Invalid Results (contaminated by 'other' bug)

| Pair | Note |
|---|---|
| ot→ot | sim ot rate 2.4× inflated; E2 comparison meaningless |

---

## Key Findings

### 1. o→o Gap is Real (VMS=2.801, Sim=2.145, Δ=-0.656)
The sim 'o' onset rate matches VMS (sim_MID=4.63%, VMS_MID=4.77%), confirming the gap is
not an artifact. The A-dialect has a strong o→o self-succession pattern (E2=2.801) that the
copy-buffer architecture under-produces by 0.656. This is comparable to y→y gap before p_y_y
was added (which fixed y→y). A p_o_o Markov rule may be warranted.

### 2. y→y Slight MID Overshoot (+0.133)
p_y_y=0.10 was calibrated to match global same-sentence y succession rate. MID context has
slightly higher y→y (2.853 vs global) and sim overshoots slightly. Could reduce p_y_y to ~0.08
to fix MID, but global effect unknown.

### 3. sh→qok Gap Present in A-Dialect (Δ=-0.773, untested whether closeable)
VMS_mid=1.741 (N=55), Sim_mid=0.968, Δ=-0.773. The 'other' bug doesn't affect sh or qok
onset classification. This confirms sh→qok gap is not specific to B-dialect. B-dialect Δ=1.01
exceeded the practical Markov-rule limit; A-dialect Δ=0.773 is below that threshold and may
be partially reducible by a p_sh_qok Markov rule — not tested in this experiment.

### 4. qok→ch Slight Overshoot in A-Dialect
p_qokch=0.12 produces E_mid=1.148 vs VMS=0.985. A-dialect has near-random qok→ch enrichment
at MID position. B-dialect MID qok→ch is 1.234 (exp_246). The rule at p=0.12 may be
over-strong for A-dialect MID context; global target for A-dialect is different.

---

## Next Steps

1. **exp_255**: Fix 'other' onset bug, re-run to get clean ot→ot MID comparison for A-dialect
2. **H453** (o→o Markov): p_o_o Markov rule for A-dialect? VMS_mid=2.801, gap=0.656 — matches
   y→y gap magnitude before p_y_y was added
3. **qok→ch A-dialect calibration**: VMS MID=0.985 (near random) vs VMS global=1.220; consider
   reducing p_qokch for A-dialect or noting the A/B difference

---

## Self-Audit

**Target-awareness**: p_y_y=0.10 calibrated to global same-sentence y succession rate in prior
experiment (not to MID-only y→y E2=2.853). Result notes this. No other target-aware elements:
onset_mid is a corpus measurement, no new parameters added. The o→o and ot→ot gap measurements
are purely descriptive. Result is not conditional on any target-aware calibration.

**Feature-destroying implementation**: The 'other' onset string collision actively destroys the
ot→ot test by inflating sim ot rate 2.4×. Explicitly flagged and the result is marked invalid.
Fix: filter 'other' from onset_mid before sim. No other features are destroyed.

**Extrapolation**: Revised — original draft claimed sh→qok was an "architectural limit" for
A-dialect, but A-dialect Δ=0.773 is below the B-dialect threshold (Δ=1.01) where Markov rules
become ineffective. The claim was softened to "untested whether closeable." All other claims are
within the observed data range.

**Negative-result scope**: sh→qok under-production conclusion scoped to "sim under-produces
under current A-dialect architecture without a sh→qok rule." No claim that no mechanism can fix
it. (Revised from original.)

**Control behavior**: Sim 'o' onset rate = 4.63% MID vs VMS 4.77% — expected and correct. Sim
'qok', 'ch', 'sh', 'd', 'y', 'ok' rates all match VMS within ±1%. Ot discrepancy (9.89% vs
4.48%) was the identified bug, fully diagnosed. No unexplained control anomalies.

---

## Architecture Status
A-dialect parameters unchanged (exp_239 + p_y_y=0.10). No updates from this experiment.
