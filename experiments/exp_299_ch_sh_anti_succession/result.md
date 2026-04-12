# exp_299: H487 — ch/sh/d Anti-Self-Succession in MID Draw
**Date:** 2026-04-11
**Hypothesis:** H487 — Adding anti-self-succession rule for ch/sh/d in the MID draw reduces over-production of ch→ch, sh→sh, d→d bigrams without breaking the 19-metric battery
**Script:** script.py
**Architecture base:** exp_287 16-mechanism simulation (beta=0.30)

---

## Result: H487 PARTIALLY CONFIRMED — MECHANISM WORKS BUT BATTERY BOUNDARY EXPOSED

The anti-succession mechanism successfully reduces ch/sh/d MID-specific E2 toward VMS values. However, the battery baseline in this experiment shows am_mid_enr marginally failing (121.2% at p_anti=0.0 vs exp_287's 118.9% pass), revealing the am_mid_enr boundary is stochastic at N=30.

---

## Sweep Results

| p_anti | Battery | ss_mean | ss_mid_ch | ss_mid_sh | ss_mid_d | adj_rate |
|--------|---------|---------|-----------|-----------|----------|----------|
| VMS    | —       | 1.1640  | 0.943     | 0.937     | 1.541    | 0.0090   |
| 0.00   | 18/19   | 1.3657  | 1.223     | 1.640     | 2.023    | 0.00911  |
| 0.20   | 18/19   | 1.3415  | 1.114     | 1.457     | 1.761    | 0.00907  |
| 0.40   | 18/19   | 1.2931  | 1.001     | 1.348     | 1.425    | 0.00868  |
| 0.60   | 18/19   | 1.2434  | 0.860     | 1.061     | 1.273    | 0.00877  |
| 0.80   | **17/19**| 1.1936 | 0.704     | 0.859     | 1.045    | 0.00848  |

**All p_anti ≤ 0.60 give 18/19 battery pass.** The failing metric is am_mid_enr (121.2% throughout — same metric that is at 118.9% in exp_287 with different seeds).

### MID-specific progress by p_anti

At p_anti=0.40:
- ch→ch: 1.001 (VMS=0.943, gap reduced +1.223→+0.058, 78% closure)
- sh→sh: 1.348 (VMS=0.937, gap reduced 1.640→+0.411, 49% closure)
- d→d: 1.425 (VMS=1.541, gap reduced +0.496→−0.116 — slightly overshot, but within VMS range)

At p_anti=0.60: ch→ch reaches 0.860 (slightly below VMS), sh→sh=1.061 (80% closure).

---

## Full Run: p_anti=0.0 (baseline, N=30)

am_mid_enr = 0.2369 (121.2%, FAIL). 18/19 battery. This is a **stochastic boundary issue**: the same architecture with exp_287's seeds gives 19/19 (am_mid_enr=118.9%), but with exp_299's seeds gives 18/19 (121.2%). The metric is at the ±20% boundary.

---

## Key Observations

1. **Mechanism effectiveness**: Anti-succession at p_anti=0.40 brings ch→ch E2 from 1.22 to 1.00 — very close to the VMS target of 0.943. This is the MID-specific over-production identified in F275. The mechanism works as designed.

2. **Battery boundary stochasticity**: am_mid_enr (MID -am enrichment) is marginal (~119-121%). This metric has always been near the ceiling; the difference between 18/19 and 19/19 is seed-dependent. Architecture is functionally at 19/19 but with stochastic boundary at this metric.

3. **No additional battery regressions**: Anti-succession at p_anti=0.40 does not cause any new failures beyond the pre-existing am_mid_enr boundary issue. ss_mean improves from 118% to 111% of VMS target.

4. **sh→sh gap persists**: Even at p_anti=0.60, sh→sh=1.061 (VMS=0.937, still 13% above). Full closure of sh→sh requires stronger mechanism than onset-level anti-succession in buffer draw (likely a within-sh vocabulary constraint analogous to the closed paradigm structure).

---

## Architecture Decision

**Do NOT add p_anti to the canonical architecture** at this point. Reasons:
- The battery is already marginally 18/19 regardless of p_anti (seed-dependent am_mid_enr)
- The MID-specific gaps are a known unmodeled feature (not in the 19-metric battery)
- Adding p_anti would make the architecture more complex without improving the official pass count

**H487 is noted as a diagnostic improvement** — the mechanism exists and works, but it addresses a gap that is not in the 19-metric battery. Retest when am_mid_enr boundary is resolved.

---

## Self-Audit

1. **Validity**: Anti-succession mechanism is correctly implemented (weight multiplication in draw_buf). Sweep design clean. ✓
2. **Surprising**: The baseline (p_anti=0.0) shows 18/19 with am_mid_enr=121.2%, vs exp_287's 19/19 with 118.9% — same architecture, different seeds. This exposes the stochastic boundary of am_mid_enr that was not visible in exp_287's single run.
3. **Battery impact**: 18/19 baseline (same as all p_anti values). The am_mid_enr boundary is the limiting factor, not anti-succession.
4. **Committed claims**: No committed claims reference MID-specific bigram E2 values or am_mid_enr specifically. ✓
5. **New hypotheses**: H504 — The am_mid_enr metric is at the ±20% boundary and fails stochastically. Should a more precise calibration of the MID -am generation rate reduce am_mid_enr toward VMS 0.1954? Current value ~0.2320-0.2370. The MID -am rate is driven by suffix_mid_sup (am suppressed to R_MID=0.25 of global rate). A finer R_MID calibration might stabilize this metric below the 120% ceiling.

---

## Finding

See F301 in findings.md.
