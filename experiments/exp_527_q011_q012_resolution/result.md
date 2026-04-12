# exp_527 result — Q011 and Q012 Resolution

## Audit

**Target-awareness**: No target-aware elements. All measurements are direct corpus observations.

**Feature-destroying implementation**: Standard methodology. pos1 uses len≥2; pos2 uses len≥3. Section definitions: A stars = 57≤n≤72 not is_b_dialect; A herbal_a = n≤56 not is_b_dialect; B herbal = n≤72 is_b_dialect; A-overall = n≤102 not is_b_dialect.

**Extrapolation**: None.

---

## Q011 RESOLVED: F446 was measuring line-FIRST, not line-FINAL

**Root cause identified**: exp_466, line 71: `lf_w = ws[0]` — uses the **first** word of each line. Our standard LF = last word (`ws[-1]`). F446's "lf" variable meant "line-first" (pos1), not "line-final" (LF in our current terminology.

**Verification**: A stars t-onset at **pos1 (line-FIRST)**:
- obs=16/136, rate=11.8% vs A-overall 5.3% → **E=2.22×/obs=16 (CONF)**
- vs A herbal_a: obs=16, A herbal_a t-rate at pos1=3.2% → **E=3.67×/obs=16 (CONF)**

This matches F446's claim of E=2.12×/N=15 exactly (minor corpus version difference: obs=16 vs 15; E=2.22 vs 2.12). **F446 is CONFIRMED — but it's a pos1 (line-opening) grammar finding, not an LF (line-final) finding.**

**Q011 CONCLUSION**: No measurement error. F446 correctly observed that A stars lines open with t-onset at 2.12-2.22× baseline. The error was categorizing this as "t-LF elevation" when t is actually elevated as a LINE-OPENER. t as a LINE-ENDER is DEPLETED (E=0.51×, confirmed exp_525).

**F446 recategorization**: F446 → A stars t-onset at pos1 (line-FIRST) CONF (E=2.22×/obs=16 vs A-overall; E=3.67× vs A herbal_a). Should be treated as a pos1 grammar finding, parallel to F503 (o-LF pos1=y in A stars).

---

## Part 2: A Stars Pos1 Opening Grammar (New CONF Findings)

A stars pos1 distribution vs A herbal_a and A-overall:

| Onset | A stars obs | A stars % | vs A herbal_a E | vs A-overall E | Signal |
|-------|------------|-----------|----------------|----------------|--------|
| **t** | 16 | 11.8% | **3.67×** | **2.22×** | **CONF** |
| **s** | 13 | 9.6% | **2.10×** | **1.59×** | **CONF** (F524) |
| y | 28 | 20.6% | 1.47× | 1.33× | below CONF |
| d | 28 | 20.6% | 1.21× | 1.09× | baseline |
| ch | 7 | 5.1% | 0.49× | 0.58× | DEPLETED |
| sh | 7 | 5.1% | 0.60× | 0.67× | DEPLETED |
| ot | 1 | 0.7% | 0.13× | — | STRONGLY DEPLETED |

**A stars pos1 pattern**: A stars preferentially opens lines with t-onset (CONF, 3.67× A herbal_a) and s-onset (CONF, 2.10× A herbal_a), while depleting ch, sh, ot, ok, qok at line openings. This is a section-specific pos1 grammar — A stars uses different opening words than A herbal_a.

**New CONF findings**:
- **F523**: A stars → t at pos1 (CONF, E=2.22×/obs=16 vs A-overall; E=3.67× vs A herbal_a)
- **F524**: A stars → s at pos1 (CONF, E=2.10×/obs=13 vs A herbal_a; E=1.59×/obs=13 vs A-overall)

---

## Q012 RESOLVED: F470 Contaminated by 2-Word Lines

**Contamination confirmed**:
- len≥2: obs=6, N_elig=20, E=3.69× — matches F470's claim (obs=6, N_elig=19, E=3.60×)
- len≥3: obs=2, N_elig=16, E=1.54× — BELOW threshold
- 4 contaminating 2-word a-LF lines: all have a trivially at pos2 (LF word = pos2 word in 2-word lines)
- Removing these contaminating lines reduces obs from 6 to 2, eliminating the signal

**Q012 CONCLUSION**: F470 was produced by the same 2-word contamination bug as Q009/F458. With correct len≥3 eligibility: B herbal a→a@pos2 obs=2, E=1.54× — below any threshold. **F470 is RETRACTED**.

**B herbal a-LF pos2 corrected (len≥3, N_elig=16)**: ch E=1.65×/obs=6 (below CONF); no class meets any threshold. B herbal a-LF has NO confirmed pos2 routing rule.

---

## Summary

| Question | Resolution |
|---------|-----------|
| Q011: F446 discrepancy | RESOLVED: exp_466 measured pos1 (ws[0]) not LF (ws[-1]). F446 = pos1 grammar (CONF). No measurement error. |
| Q012: F470 contamination | RESOLVED: len≥2 bug; 4 trivial 2-word lines inflate obs 6→2. F470 RETRACTED. |

**New CONF findings:**
- **F523**: A stars t-onset at pos1 CONF (E=3.67×/obs=16 vs A herbal_a; E=2.22×/obs=16 vs A-overall)
- **F524**: A stars s-onset at pos1 CONF (E=2.10×/obs=13 vs A herbal_a)

**Retracted:**
- **F470**: B herbal a→a@pos2 dir — RETRACTED. Corrected E=1.54×/obs=2 (below threshold).
- **F446** (as LF finding): Recategorized — F446 is a pos1 finding, not an LF finding. t is elevated at A stars pos1, DEPLETED at A stars line-final.

**Note on F446's categorization history**: F446 was categorized in findings.md as "A stars t-LF (line-final) elevation," and motivated several experiments (H_new_EJ, H_new_EN) investigating why t-LF was rare in A stars per current methodology. Those were wasted effort due to the categorization error. The correct finding (A stars t-opener elevation) is now F523 (CONF).
