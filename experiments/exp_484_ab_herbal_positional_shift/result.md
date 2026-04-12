# exp_484: A/B Herbal Positional Shift — Line Length Artifact or Grammar Rule?

**Question:** H_new_BA — Does the A herbal_a(pen) vs B herbal(pos2) grammar-pair position difference reflect line length differences or genuine grammar?

**Critical finding:** Baseline bug discovered in exp_479. F453 sh-at-pen and F454 ch/k-at-pen are INCORRECT — inflated by using LF-rate as pen baseline instead of pen-specific baseline. Corrections documented below. New confirmed finding: A herbal_a ch-LF → ch at pos2 (E=1.60×/N=94).

---

## 1. Line Length Distributions

| | A herbal_a | B herbal |
|--|-----------|---------|
| N lines | 975 | 269 |
| Mean words/line | 4.52 | 6.34 |
| Median | 4.0 | 6.0 |
| 3-word lines (pos2=pen) | 16.3% | 10.0% |
| ≥5-word lines | 47.9% | 64.3% |

**B herbal lines are LONGER than A herbal_a** (mean 6.34 vs 4.52 words). This rules out the "B herbal lines are short so pos2≈pen" artifact explanation. If anything, B herbal's longer lines would make pos2 and pen more distinct.

---

## 2. Baseline Bug Discovery: F453 sh-at-pen and F454 ch/k-at-pen INCORRECT

### What the correct baselines are

Position-specific baseline rates in A herbal_a:

| onset | pos1 | pos2 | pen | LF |
|-------|------|------|-----|----|
| ch | 0.104 | 0.330 | 0.270 | 0.188 |
| sh | 0.086 | 0.120 | 0.089 | 0.042 |
| ok | 0.058 | 0.042 | 0.043 | 0.058 |
| ot | 0.054 | 0.026 | 0.045 | 0.044 |
| d | 0.169 | 0.111 | 0.174 | 0.272 |
| y | 0.139 | 0.030 | 0.042 | 0.038 |

**Key observation**: sh's LF rate (0.042 = 4.2%) ≠ sh's pen rate (0.089 = 8.9%). They differ by 2×. exp_479 used sh's LF rate (4.2%) as the pen baseline, inflating E from 0.85× to 1.81×.

**Key observation**: ch's LF rate (0.188 = 18.8%) ≠ ch's pen rate (0.270 = 27.0%). They differ by 1.43×. exp_479 used ch's LF rate as the pen baseline, inflating E from 1.32× to 1.90×.

The bug: exp_479 computed the pen baseline using ws[-1] (the LF word = last word) frequency instead of ws[-2] (the pen = second-to-last word) frequency. This means it asked "does this onset appear at pen more than it appears as a terminal word?" instead of "does this onset appear at pen more than it usually appears at the penultimate position?"

### Corrected E values for F453 and F454 pen findings

**F453 (A herbal_a d-LF) pen:**
- sh at pen: obs=18/237 (7.6%) vs pen baseline 8.9% → E=0.85× (DEPLETED, NOT enriched)
- ch at pen: obs=66/237 (27.8%) vs pen baseline 27.0% → E=1.03× (FLAT)
- **F453's sh at pen claim RETRACTED: actual E=0.85×, not 1.81×**

**F453 (A herbal_a d-LF) pos1 [UNAFFECTED by bug]:**
- ot at pos1: obs=22/254 (8.7%) vs pos1 baseline 5.4% → E=1.59×/N=22 (CONFIRMED ✓)
- The pos1 baseline was computed correctly in exp_479. F453 ot-at-pos1 stands.

**F454 (A herbal_a ch-LF) pen:**
- ch at pen: obs=55/154 (35.7%) vs pen baseline 27.0% → E=1.32×/N=55 (BELOW 1.5× threshold)
- k at pen: obs=12/154 (7.8%) vs pen baseline 5.4% → E=1.45×/N=12 (BELOW 1.5× threshold)
- d at pen: obs=20/154 (13.0%) vs pen baseline 17.4% → E=0.75× (depleted)
- **F454's ch-at-pen and k-at-pen claims RETRACTED: E values below confirmation threshold**

---

## 3. New Finding: A herbal_a ch-LF → ch at pos2 (E=1.60×/N=94, CONFIRMED)

With the correct pos2-specific baseline (ch at pos2 = 33.0% in A herbal_a):
- ch at pos2 in ch-LF lines: obs=94/178 = 52.8% vs baseline 33.0% → E=1.60×/N=94 **CONFIRMED**

This is the correct ch self-chaining signal in A herbal_a ch-LF. ch appears at pos2 (second word of the line) at 1.60× baseline in ch-terminal lines. This is not a pen effect — it's a pos2 effect.

**NEW FINDING: A herbal_a ch-LF → ch at pos2 (E=1.60×/N=94, CONFIRMED)**

This is F461 (see below).

---

## 4. Long-Line Analysis and Position Profile

For lines ≥6 words (where pos2 and pen are clearly distinct):

| Section | LF class | pos2 | pos3 | pen-1 | pen |
|---------|---------|------|------|-------|-----|
| A herbal_a | ch-LF (N=43) | 1.20× | 1.19× | 1.02× | 1.12× |
| B herbal | ch-LF (N=24) | 1.25× | 1.15× | 1.34× | 1.47× |
| A herbal_a | d-LF (N=86) | 0.97× | 1.16× | **1.60×** | 0.52× |
| B herbal | d-LF (N=21) | 1.36× | 0.00× | 0.84× | 0.71× |

For long lines: ch elevation is relatively uniform across all internal positions (E≈1.1-1.5× throughout). The pos2 signal for ch dominates for all-length lines simply because N is much higher. No evidence of a specific pen preference for ch in long ch-LF lines in either section.

**Interesting**: A herbal_a d-LF (≥6 words): pen-1 (= ws[-3]) shows E=1.60× for sh — but this is N=11/86 with obs=11. Below confirmation threshold. This directional signal at the antepenultimate (pen-1) position is intriguing but not confirmed.

---

## 5. Corrected A/B Comparison

With corrected baselines:

| Rule | A herbal_a | B herbal | Status |
|------|-----------|---------|--------|
| ch-LF → ch at pos2 | **CONF E=1.60×/N=94 (NEW)** | **CONF E=1.74×/N=19 (F458)** | Cross-dialectal conserved |
| ch-LF → ch at pen | E=1.32×/N=55 (below threshold) | E=1.43×/N=15 (below threshold) | Not confirmed in either |
| d-LF → sh at pos2 | E=1.09× (FLAT) | **CONF E=1.73×/N=10 (F457)** | B-specific |
| d-LF → sh at pen | E=0.85× (DEPLETED) | E=0.93× (flat) | Not enriched in either |

The "A uses pen, B uses pos2" narrative from §17.8 was incorrect — it was based on the flawed F454 pen finding. The correct picture:
- **ch self-chaining at pos2 is cross-dialectally conserved** (both A and B herbal confirm it)
- **d/sh pairing at pos2 is B-herbal-specific** (not present in A herbal_a at pos2 or pen)

The positional shift between A and B is not about A(pen) vs B(pos2) — that was a baseline artifact. The real distinction is that B herbal d-LF has sh at pos2 while A herbal_a d-LF shows no sh enrichment at any position (using correct baselines).

---

## Self-Audit

**Target-awareness:** None. All baselines are position-specific, section-specific, and derived from the corpus itself.

**Feature-destroying implementation:** Position-specific baselines (pos1_base from ws[0], pos2_base from ws[1], pen_base from ws[-2]) computed separately for each position. This is the correct approach. exp_479 had a bug where pen_base was accidentally computed from ws[-1] (the LF word distribution) instead of ws[-2].

**Extrapolation:** F453 sh at pen and F454 ch/k at pen retracted. The retraction is not extrapolation — it is a correction of computed E values using the proper baseline. The ch at pos2 finding is directly computed with N=94, E=1.60× — clearly above threshold.

**Negative-result scope:** d-LF → sh at pen: "not enriched in A herbal_a" (E=0.85×, N=237) is a negative result properly scoped to A herbal_a. F457 (B herbal d-LF → sh at pos2) is unaffected (was computed with pos2-specific baseline in exp_482).

**Control behavior:** N/A.

---

## Corrections to F453 and F454

### F453 Correction:
- **RETAIN**: d-LF → ot at pos1 (E=1.59×/N=22, CONFIRMED) — unaffected by baseline bug
- **RETRACT**: d-LF → sh at pen (E=1.81× → actual E=0.85×, DEPLETED)

### F454 Correction:
- **RETRACT**: ch-LF → ch at pen (E=1.90× → actual E=1.32×, below threshold)
- **RETRACT**: ch-LF → k at pen (E=1.81× → actual E=1.45×, below threshold)
- **RETAIN below-threshold signal**: ch at pen E=1.32×/N=55 (directional, below confirmation)
- **RETAIN**: d depletion at pen (E=0.75×) still valid directionally

### New Finding F461:
- A herbal_a ch-LF → ch at pos2 (E=1.60×/N=94, CONFIRMED) — this is the real ch self-chaining signal

---

## Conclusion

H_new_BA ANSWERED: The A/B positional shift was an artifact of the exp_479 baseline bug. B herbal is longer, not shorter, so line-length cannot explain a "B uses pos2" effect. With corrected baselines: BOTH A and B herbal confirm ch self-chaining at pos2 (E=1.60×/1.74×); d-LF → sh at pos2 is B-specific (not A herbal_a). The "A:pen vs B:pos2" narrative from §17.8 is INCORRECT and should be revised.

**F461 ASSIGNED: A herbal_a ch-LF → ch at pos2 (E=1.60×/N=94, CONFIRMED).** Cross-dialectal: parallels F458 (B herbal ch-LF → ch at pos2). ch self-chaining at pos2 is conserved across A and B herbal sections.

**F453 CORRECTION: sh at pen retracted (E=0.85×). F454 CORRECTION: ch and k at pen retracted (E=1.32×/1.45×, below threshold).**
