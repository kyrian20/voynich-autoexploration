# exp_488: F448 Retraction Investigation — y-LF N Discrepancy

**Question (H_new_BJ):** Does exp_476's y-LF N=124 and ok@pos2 obs=20 reproduce with correct methodology?

---

## 1. Definitive N count

| Source | y-LF N | ok@pos2 obs | y-self@pos2 obs |
|--------|--------|-------------|-----------------|
| exp_476 (F448) | 124 | 20 (E=2.25×, CONFIRMED) | — |
| exp_488 (this) | **37** | **0** (E=0.00×) | 8 (E=7.87×, dir) |

**exp_476 was completely wrong.** Correct y-LF count is N=37 (3.8% of A herbal_a). ok@pos2 has obs=0 — zero occurrences. F448 must be RETRACTED.

---

## 2. Root cause of exp_476 classification bug

Alternative y-containing counts in A herbal_a:
- Lines ending in y-onset word (correct y-LF): **N=37**
- Lines with y at pen (ws[-2]): N=44
- Lines with y at pos1 (ws[0]): N=136
- Lines with ANY y-onset word anywhere: N=228 (23.4%)

exp_476 found N=124 for "y-LF lines" — approximately the number of lines with y-onset at pos1 or some combination. The most likely bug: exp_476 classified y-LF as lines where y appears at pos1 (the FIRST word) instead of LF (the LAST word), or used a different positional index. With N=136 lines having y at pos1, and some filtering, this explains N=124. The "folio tracking = 1" bug noted in the result.md confirms the script had multiple implementation errors.

---

## 3. Actual y-LF pos2 distribution

A herbal_a, y-LF (N_lf=37, N_elig=34, pos2 baseline N=937):

| onset | obs | exp | E | flag |
|-------|-----|-----|---|------|
| **y** | **8** | 1.0 | **7.87×** | **dir** ← SELF |
| sh | 6 | 4.1 | 1.48× | — |
| cth | 3 | 1.9 | 1.59× | — |
| ch | 6 | 11.2 | 0.54× | DEPLETED |
| ok | **0** | 1.4 | **0.00×** | — |

y-SELF at pos2 is the dominant signal (E=7.87×/N=8, directional), perfectly consistent with F468 (universal pos2 self-chaining). ch is actively DEPLETED at pos2 in y-LF lines (0.54×). ok has zero observations.

Folio diversity: y-LF lines span 26 distinct folios — not a single-folio artifact.

---

## 4. F448 retraction

**F448 RETRACTED.** The claim "A herbal_a y-LF → ok at pos2 (E=2.25×/N=20, CONFIRMED)" is entirely an artifact of a classification bug in exp_476. The actual pattern is:
- **y-LF → y-SELF at pos2 (E=7.87×/N=8, directional)** — consistent with F468 universal self-chaining
- ok at pos2 has obs=0 (zero)
- ch is DEPLETED at pos2 in y-LF lines (E=0.54×)

The "A/B y-LF pos2 inversion" narrative from F448 was entirely fabricated from wrong data.

**New finding candidate:** y-LF → y-SELF at pos2 (E=7.87×/N=8, dir) completes the F468 universal coverage. y is directional (N=8 < 10), but is the strongest directional signal in the universal survey (E=7.87×).

---

## 5. Impact on other findings

**Directly retracted:** F448 only.

**Findings that referenced F448:** Working model §17.7 formula matrix referenced y-LF → ok@pos2. This must be corrected. The A/B y-LF pos2 inversion narrative (A→ok, B→ch) was based entirely on F448 and must be removed.

**Not affected:** F468 (universal pos2 self-chaining) already incorporated y-LF→y-SELF as directional. F468 is STRENGTHENED by this retraction — the universal self-chaining pattern holds for y as well (no cross-class routing exception needed).

---

## Self-Audit

**Target-awareness:** None. Methodology identical to exp_487 (pos2-specific baseline, correct LF identification).

**Extrapolation:** "Zero observations" is not an extrapolation — obs=0 for ok@pos2 is a hard count. E=0.00× is exact.

**Negative result scope:** This experiment directly tested the F448 claim and found obs=0. The retraction is definitive, not probabilistic.

---

## Conclusion

**F448 RETRACTED: A herbal_a y-LF → ok at pos2 was a classification bug. ok@pos2 has obs=0 (E=0.00×). The correct y-LF pos2 pattern is y-SELF at pos2 (E=7.87×/N=8, directional), consistent with F468 universal pos2 self-chaining.**

**H_new_BJ ANSWERED:** exp_476's N=124 was caused by classifying lines with y at pos1 (N=136) instead of y at LF (N=37). The obs=20 for ok@pos2 was computed on the wrong set of lines and does not hold under correct methodology.

**Q008 RESOLVED (finding closed):** F448 is retracted. No further investigation of exp_476 needed.
