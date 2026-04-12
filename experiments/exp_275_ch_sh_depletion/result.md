# exp_275: ch→ch and sh→sh Depletion — MID Position Analysis
**Hypothesis:** H476
**Date:** 2026-04-11
**Status:** PARTIALLY CONFIRMED (B-dialect specific depletion; A-dialect shows enrichment)

---

## Summary

H476 posited that ch→ch and sh→sh are depleted in VMS MID position and that the simulation over-produces both. Both are **confirmed for B-dialect only**. A-dialect shows the opposite — enrichment. Section breakdown reveals strongest depletion in the bio section. Simulation over-produces both for B-dialect, with sh→sh showing the largest gap.

---

## Key Results

### E2_mid by Dialect

| Pair | A-dialect VMS | A-dialect Sim | Gap | B-dialect VMS | B-dialect Sim | Gap |
|------|--------------|--------------|-----|--------------|--------------|-----|
| ch→ch | 1.1939 (N=304) | 1.1636 | −0.030 (match) | 0.9433 (N=339) | 1.1426 | +0.199 |
| sh→sh | 1.3120 (N=79) | 1.4009 | +0.089 | 0.9367 (N=120) | 1.5540 | **+0.617*** |
| d→d | — | — | — | 1.5405 | 2.3511 | **+0.811*** |

*: Substantial simulation over-production gap.

**A-dialect**: ch→ch enriched (1.19), sh→sh enriched (1.31). Simulation matches A-dialect well (gaps −0.03 and +0.09).  
**B-dialect**: ch→ch depleted (0.94), sh→sh depleted (0.94). Simulation substantially over-produces both.

### B-Dialect Section Breakdown (most depleted)

**ch→ch by section:**
| Section | E2_mid |
|---------|--------|
| bio | 0.567 |
| cosmo | 0.848 |
| recipes | 0.961 |
| herbal | 0.946 |
| astro | 1.034 |

**sh→sh by section:**
| Section | E2_mid |
|---------|--------|
| bio | 0.517 |
| cosmo | 0.746 |
| astro | 0.819 |
| herbal | 0.956 |
| recipes | 1.229 |

Bio section shows strongest depletion for both; recipes is near-baseline or slightly enriched for sh→sh.

### sh→X Successor Analysis (B-dialect MID)

| Successor | E2_mid | N |
|-----------|--------|---|
| qok | 1.880 | enriched |
| ch | 0.530 | depleted |
| sh | 0.937 | depleted |

sh words are strongly avoided after sh (anti-self-succession) but strongly prefer to precede qok (the known sh→qok enrichment from exp_242/262).

### ch→X Successor Analysis (B-dialect MID)

| Successor | E2_mid |
|-----------|--------|
| qok | 1.132 | enriched |
| sh | depleted |
| ch | 0.943 | depleted |

ch-onset words also avoid self-succession and show the known ch→qok enrichment (exp_249).

---

## Interpretation

**H476 PARTIALLY CONFIRMED:** The depletion is B-dialect specific, not universal.

- **A-dialect**: Both ch→ch (1.19) and sh→sh (1.31) are ENRICHED. Simulation matches A-dialect well. No architecture gap for A-dialect.
- **B-dialect**: Both ch→ch (0.94) and sh→sh (0.94) are DEPLETED (E < 1). Simulation over-produces by +0.20 (ch) and +0.62 (sh). This is a real architecture gap for B-dialect — not captured by the 19-metric battery.
- **Mechanism**: The depletion appears grammatical, not lexical — anti-self-succession for high-frequency onset classes. sh and ch words preferentially follow qok (the sh→qok and ch→qok enrichments), and qok preferentially follows ch (qok→ch enrichment). The ch/sh ↔ qok interplay may structurally crowd out ch→ch and sh→sh successions. Section concentration in bio (strongest depletion) suggests possible compositional contribution, but herbal (largest section) also shows depletion (ch→ch=0.946, sh→sh=0.956).
- **sh→sh gap (+0.617) is most significant**: simulation produces sh→sh 1.55 vs VMS 0.94, a 65% over-production. This is substantially larger than the ch→ch gap (+0.20).
- **d→d also over-produced** (gap +0.81), consistent with the buffer's tendency to repeat the last drawn onset.

---

## Architecture Status

The B-dialect 12-mechanism architecture does NOT reproduce B-dialect ch→ch or sh→sh depletion. These are genuine MID-specific bigram gaps outside the 19-metric battery. The 19/19 B-dialect battery PASS is unaffected — battery metrics are global and do not measure MID-only pair depletion for specific onset classes.

The mechanism for anti-self-succession of high-frequency onsets in B-dialect (ch and sh) is structurally opposite to the buffer's natural behavior (which produces enrichment). A negative Markov bias (p_ch_ch_suppress or p_sh_sh_suppress parameter) could reduce these, but was not tested here. Given that adding p_chqok and p_qokch already partially addresses the ch/qok coupling, the ch→ch and sh→sh depletion may be an indirect effect of this coupling — words already "used" for qok-transitions are less available for same-onset succession — but this is mechanistically unresolved.

---

## Finding

→ F275 added to findings.md. H476 RESOLVED (PARTIALLY CONFIRMED — B-dialect specific).

---

## Self-Audit

**Target-awareness**: No target-aware elements identified. This experiment is a measurement study comparing VMS corpus E2_mid values against frozen simulation output (B-dialect parameters from exp_257). No parameter was set using knowledge of ch→ch or sh→sh targets. Result is observational and unconditional.

**Feature-destroying implementation**: No feature-destroying implementation details identified. MID-only bigram filtering is the correct scope for H476 (which posited depletion specifically in MID position). Section-level breakdown used the same MID-only corpus subset.

**Extrapolation**: All claims are within the tested scope. No "structural," "cannot," or "no parameter setting" claims about untested grid regions. The phrase "structurally opposite to the buffer's natural behavior" describes a direction of effect (buffer auto-correlation produces enrichment; VMS shows depletion) — not a claim that anti-succession is impossible to reproduce. The mechanism is explicitly stated as "unresolved."

**Negative-result scope**: N/A — result is partially positive (depletion confirmed for B-dialect; mechanism characterization done). The architecture gap claim (sim over-produces) is valid — it is a direct measurement comparison under the fixed architecture, not an extrapolation.

**Control behavior**: Expected behavior: the copy-buffer (with onset Markov rules but no anti-succession mechanism) should produce ch→ch and sh→sh enrichment through buffer auto-correlation. Actual behavior: Sim B ch→ch=1.143 (enriched), sh→sh=1.554 (enriched) — consistent with expectation. Sim A ch→ch=1.164, sh→sh=1.401 — also enriched, consistent with A-dialect showing enrichment in VMS. The control behavior is as expected; no surprises that require investigation. The large sh→sh gap (Sim 1.554 vs VMS 0.937) is the primary new finding, not a measurement artifact.

## Next Steps

- H477: Word repetition distance distribution (tests buffer memory depth, medium priority)
- H466: B-dialect fine-grained p_sh_qok sweep (low priority)
- Potential: negative Markov bias experiment for ch→ch and sh→sh in B-dialect (low priority — battery-passing architecture not affected)
