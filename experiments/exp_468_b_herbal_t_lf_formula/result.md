# exp_468: B Herbal t-LF Formula Structure

**Question:** Is B herbal t-LF → ch at pos1 (E=4.09× from exp_467) a confirmed formula type? What is the complete B herbal t-LF line grammar?

---

## Critical Correction to exp_467

**exp_467's "B herbal t-LF → ch E=4.09×" was a methodology error.** The exp_467 script computed `E = (cnt/total_t_pos1) / (b_overall_lf['ch'] / b_overall_total)`, using the **LF** base rate (ch at LF = 4.5%) instead of the **pos1** base rate (ch at pos1 ≈ 24% in B herbal). This inflated E by ~5×.

**Corrected E**: ch at pos1 in B herbal t-LF lines = 7/37 = 18.9%; B herbal pos1 ch base rate = 23.6%. **E = 0.80× — ch is at BASELINE or slightly below.** No formula-type routing to ch from t-LF.

---

## Corrected B Herbal t-LF Formula Analysis

**B herbal t-LF lines: N=37** (of 233 total B herbal lines ≥3 words)

### t-LF → pos1 routing (correctly computed vs B herbal pos1 baseline)
- **qok: E=2.22×(N=6)** — elevated
- t: E=1.80×(N=2, dir)
- ot: E=1.80×(N=2, dir)
- ch: E=0.80×(N=7) — baseline (not elevated)
- sh: E=0.92×(N=6) — baseline
- d: E=1.11×(N=3) — baseline

### t-LF → pos2 routing (vs B herbal pos2 baseline)
- **o: E=2.62×(N=5)** — elevated
- **k: E=2.36×(N=3, dir)**
- ok: E=1.51×(N=6) — mild
- sh: E=1.17×(N=5) — baseline
- ch: E=0.62×(N=5) — slightly depleted

### t-LF → LL routing (vs B herbal LL baseline)
- **o: E=1.97×(N=5)** — elevated
- **ol: E=1.94×(N=4)** — elevated
- sh: E=1.57×(N=4)
- y: E=1.57×(N=3)
- ch: E=0.63×(N=4) — depleted

### B herbal LF-class formula comparison

| LF class | N | pos1 top | LL top |
|----------|---|----------|--------|
| t | 37 | qok(2.22×/6) | o(1.97×/5), ol(1.94×/4) |
| y | 46 | y(2.81×/5) | ot(3.04×/6) |
| ot | 7 | ok(4.44×/2,dir), qo(5.55×/1,dir) | y(5.55×/2,dir), t(8.32×/1,dir) |
| p | 8 | o(4.85×/2,dir), k(4.85×/2,dir) | ok(1.66×/2), sh(1.82×/1) |
| sh | 18 | qok(2.28×/3), k(2.16×/2) | ch(1.62×/5), l(2.88×/2) |
| d | 45 | ch(1.32×/14), sh(1.26×/10) | ok(1.33×/9) |

---

## Interpretation

**No B herbal t-LF formula type confirmed** (exp_467's t→ch was a baseline error). The B herbal t-LF lines are diverse with no strong formula-type routing.

**B herbal t-LF → qok at pos1 (E=2.22×/N=6)**: directional, not confirmed as formula type (N<5 threshold for formula types per F416/F426). Could be part of a broader t→qok rule in B herbal.

**B herbal t-LF line endings**: mildly elevated o(1.97×), ol(1.94×) at LL — consistent with the o/ol terminal class that appears in many B contexts (B astro ol-LF 1.56×; the o/ol cluster appears terminal-appropriate).

**y-LF formula structure in B herbal**: y→y self-succession at pos1 (E=2.81×/N=5); ot elevated at LL (E=3.04×/N=6) — the y→ot terminal is a B herbal-specific pattern. Compare: within-line formula types y→sh→ch and y→o→ch (F426) — these are pharma/bio formulas. B herbal y-LF has a different LL endpoint (ot, not ch/qok).

**p-LF in B herbal (N=8, directional)**: pos1 = o or k (the p→o and p→k routing, consistent with B p-formula structure but very small N in herbal).

---

## Self-Audit

**Target-awareness**: None. Onset-level counts with section-specific baselines.

**Feature-destroying implementation**: No issues. The key correction from exp_467: using pos1-specific baseline for pos1 routing analysis (not LF base rate). This is the standard correct procedure.

**Extrapolation**: ot-LF and p-LF in B herbal are N=7-8 — all directional. y-LF ot-terminal (E=3.04×/N=6) is just-directional.

**Negative-result scope**: "No B herbal t-LF formula type" is specific to t-LF in B herbal. It does not preclude formula types elsewhere. The B herbal t-LF elevation (2.34×, F447) reflects onset-class concentration at LF, not formula-type routing.

**Control behavior**: B herbal pos1 and pos2 distributions used as section-specific baselines (correct procedure parallel to exp_429 which used section-specific LF rates for F431).

---

## Conclusion

**The exp_467 B herbal t-LF → ch routing was a baseline error; corrected E=0.80× (baseline).** B herbal t-LF → qok at pos1 is directional (E=2.22×/N=6). No B herbal t-LF formula type confirmed at standard thresholds. B herbal y-LF → ot at LL (E=3.04×/N=6) is an unexpected directional finding — y-terminal lines in B herbal end with ot more than expected. No new finding ID (all results directional; the primary purpose was to correct exp_467).
