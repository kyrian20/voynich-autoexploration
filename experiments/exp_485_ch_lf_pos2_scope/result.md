# exp_485: ch-LF → ch at pos2 Scope Test + Pen Baseline Validation

**Questions:** (H_new_BB) Is ch self-chaining at pos2 (F461+F458) herbal-section-specific or universal? (H_new_BC) Are B pharma F450/F451/F452 pen findings valid with correct ws[-2] pen baselines?

---

## 1. ch-LF → ch at pos2: Scope Across All Major Sections

| Section | N_lf | ch@pos2 obs | ch@pos2 rate | E | Flag |
|---------|------|------------|-------------|---|------|
| **A herbal_a** | 178 | 94 | 52.8% vs 33.0% base | **1.60×** | **CONFIRMED (F461)** |
| **B herbal** | 48 | 19 | 40.4% vs 23.3% base | **1.74×** | **CONFIRMED (F458)** |
| B pharma | 158 | 52 | 32.9% vs 25.3% base | 1.30× | below threshold |
| B astro | 85 | 19 | 22.6% vs 15.5% base | 1.46× | below threshold |
| A stars | 21 | 4 | 20.0% vs 15.9% base | 1.26× | N small |
| A cosmo | 65 | 17 | 26.2% vs 24.8% base | **1.06×** | **FLAT** |
| B cosmo | 15 | 2 | 13.3% vs 19.5% base | **0.68×** | **DEPLETED** |

**RESULT: ch-LF → ch at pos2 is HERBAL-SECTION-SPECIFIC.**

The rule is confirmed in both A herbal_a and B herbal, but:
- B pharma: E=1.30× (below 1.5× threshold; N=158 adequate)
- A cosmo: E=1.06× (flat; N=65 adequate)
- B cosmo: E=0.68× (depleted)

This is a content-conditional rule: herbal domain activates ch self-chaining at pos2; non-herbal domains do not. This directly parallels ot-LF→y@pos1 (also herbal-section-specific; confirmed in A herbal_a, directional in B herbal, flat/depleted in B pharma/astro).

**NEW FINDING: F462 — ch-LF → ch at pos2 is herbal-section-specific (scope determination for F461+F458)**

---

## 2. B pharma ch-LF Positional Profile

B pharma ch-LF (N=158, pos1 and pos2):

| position | onset | obs | exp | E | Flag |
|----------|-------|-----|-----|---|------|
| pos1 | ch | 15 | 9.1 | 1.65× | CONFIRMED |
| pos1 | t | 9 | 5.9 | 1.52× | — |
| pos2 | s | 2 | 0.6 | 3.35× | N too small |
| pos2 | ch | 52 | 39.9 | 1.30× | below threshold |

**F449 REPLICATED**: B pharma ch-LF → ch at pos1 (E=1.65×/N=15, CONFIRMED). Essentially identical to F449 (E=1.64×/N=15).

---

## 3. A herbal_a d-LF Full Pen Profile (correct ws[-2] baseline)

**Pen baseline for A herbal_a**: ch(27.0%), d(17.4%), sh(8.9%), cth(6.1%), k(5.4%)

| onset | obs/N | rate | E | Flag |
|-------|-------|------|---|------|
| sch | 2/237 | 0.8% vs 0.4% base | 2.36× | N=2 (insufficient) |
| s | 3/237 | 1.3% vs 0.7% base | 1.77× | N=3 (insufficient) |
| ckh | 6/237 | 2.5% vs 1.7% base | 1.52× | N=6 (dir-E too low; below dir threshold E≥2.0) |
| y | 13/237 | 5.5% vs 4.2% base | 1.31× | — |
| d | 50/237 | 21.1% vs 17.4% base | 1.21× | — |
| sh | 18/237 | 7.6% vs 8.9% base | 0.85× | DEPLETED (confirms F453 retraction) |

**CONFIRMED NEGATIVE**: No onset reaches confirmation threshold (E≥1.5×/N≥10) or directional threshold (E≥2.0×/N≥5) for A herbal_a d-LF pen. The d-LF pen position in A herbal_a is essentially FLAT — no grammar routing rule operating at pen for d-terminal lines. sh is depleted (E=0.85×, confirming the F453 retraction from exp_484).

---

## 4. A herbal_a ch-LF Full Pen Profile (correct ws[-2] baseline)

| onset | obs/N | rate | E | Flag |
|-------|-------|------|---|------|
| ol | 5/154 | 3.2% vs 1.6% base | 2.09× | **dir (N=5, E≥2.0)** |
| ckh | 4/154 | 2.6% vs 1.7% base | 1.55× | N=4 (insufficient) |
| k | 12/154 | 7.8% vs 5.4% base | 1.45× | below threshold |
| ch | 55/154 | 35.7% vs 27.0% base | 1.32× | below threshold |
| sh | 17/154 | 11.0% vs 8.9% base | 1.24× | — |

**New directional: A herbal_a ch-LF → ol at pen (E=2.09×/N=5, dir).** ol-onset words (bench+l class) appear at pen in ch-LF lines at 2.09× baseline (obs=5/154). Below confirmation threshold but above directional. Not previously noted.

---

## 5. B pharma F450/F451/F452 Validation with Correct Pen Baselines

**B pharma pen baseline (ws[-2] distribution)**: ch(20.9%), qok(12.1%), ot(11.0%), ok(9.3%), l(8.6%), a(8.2%)

### F450 validation: B pharma ot-LF → ot at pen

| onset | obs/N | rate | E | Flag |
|-------|-------|------|---|------|
| **ot** | **15/78** | **19.2% vs 11.0% base** | **1.75×** | **CONFIRMED** |
| k | 5/78 | 6.4% vs 2.4% base | 2.64× | dir |
| sh | 6/78 | 7.7% vs 5.1% base | 1.51× | — |

**F450 VALIDATED but corrected**: E=1.75× (was 1.94× in exp_479). The exp_479 bug slightly inflated F450 (ot's LF rate in B pharma was used as baseline at ~9.7% instead of correct pen rate 11.0% — note this is actually LOWER than pen rate, meaning bug deflated expected → inflated E). With correct baseline E=1.75×, F450 still CONFIRMED (N=15, E≥1.5×).

### F451 validation: B pharma l-LF → l at pen

| onset | obs/N | rate | E | Flag |
|-------|-------|------|---|------|
| **l** | **17/91** | **18.7% vs 8.6% base** | **2.18×** | **CONFIRMED** |
| ol | 5/91 | 5.5% vs 3.4% base | 1.59× | — |

**F451 pen claim VALIDATED and UPGRADED**: E=2.18× (was 1.62× in exp_479). exp_479 used l's LF rate (~11.5%) instead of pen rate (8.6%) → baseline too high → E deflated. Correct E=2.18×/N=17 is stronger.

### F452 validation: B pharma ok-LF → a at pen

| onset | obs/N | rate | E | Flag |
|-------|-------|------|---|------|
| **a** | **11/49** | **22.4% vs 8.2% base** | **2.75×** | **CONFIRMED** |
| qo | 3/49 | 6.1% vs 2.3% base | 2.66× | (dir) |

**F452 VALIDATED and UPGRADED**: E=2.75× (was 2.04× in exp_479). exp_479 used a's LF rate (~11.0%) instead of pen rate (8.2%) → baseline too high → E deflated. Correct E=2.75×/N=11 is substantially stronger.

---

## Summary of Corrections to F450/F451/F452

| Finding | exp_479 E | Correct E | Change | Status |
|---------|-----------|-----------|--------|--------|
| F450: B pharma ot→ot@pen | 1.94×/N=15 | **1.75×/N=15** | slightly inflated → corrected down | CONFIRMED |
| F451: B pharma l→l@pen | 1.62×/N=17 | **2.18×/N=17** | deflated → corrected up | CONFIRMED, stronger |
| F452: B pharma ok→a@pen | 2.04×/N=11 | **2.75×/N=11** | deflated → corrected up | CONFIRMED, stronger |

---

## Self-Audit

**Target-awareness:** None. All baselines are section-specific, position-specific, derived from the corpus.

**Baseline correctness:** Section 3/4/5 use `ws[-2]` for pen baseline throughout — explicitly verified in the code. Section 1 uses `ws[1]` for pos2 baseline. All correct.

**Multiple testing:** The scope test covered 7 sections for ch-LF→ch@pos2. The pattern is clear: only herbal sections show it. The 5-section non-herbal null result is consistent.

**Negative result scope:** A herbal_a d-LF pen = no confirmed signal is scoped to A herbal_a. B herbal d-LF pen (exp_482: ch=1.47×, N=12, below threshold) also shows no pen confirmation, consistent.

---

## Conclusion

**F462 ASSIGNED: ch-LF → ch at pos2 is HERBAL-SECTION-SPECIFIC.** Present in A herbal_a (F461, E=1.60×/N=94) and B herbal (F458, E=1.74×/N=19). Absent in B pharma (E=1.30×), flat in A cosmo (E=1.06×), depleted in B cosmo (E=0.68×). Content-conditional: the herbal domain activates ch self-chaining at pos2. Parallels ot-LF→y@pos1 (also herbal-section-specific). **H_new_BB RESOLVED.**

**F450 CORRECTED: E=1.75× (was 1.94×). F451 CORRECTED: E=2.18× (was 1.62×). F452 CORRECTED: E=2.75× (was 2.04×). All three remain CONFIRMED. H_new_BC (pen validation part) RESOLVED.**

**A herbal_a d-LF pen: no confirmed signal** (confirmed negative, all E<1.5× or N<5 with E<2.0). sh depleted (E=0.85×), consistent with F453 pen retraction. d-LF formula in A herbal_a has confirmed pos1 rule (ot, F453) but no pen rule.

**New directional: A herbal_a ch-LF → ol at pen (E=2.09×/N=5, dir).** Below confirmation threshold.
