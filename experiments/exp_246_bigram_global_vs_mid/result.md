# exp_246: Global vs MID-Only Bigram Enrichments — Verification of exp_245 Diagnostic

**Date:** 2026-04-11
**Purpose:** Verify exp_245 prediction that full exp_236 architecture over-produces self-succession in MID context. Directly measure both global and MID-only bigram enrichments from full simulation (N=15 trials, p_sh_qok=0.00 baseline).

**Status:** exp_245 prediction was PARTIALLY CORRECT for some onsets but WRONG for ot→ot. The real picture is complex: some onsets over-produce in MID, some under-produce, some match. Key new finding: ot→ot is a genuine gap (SIM<VMS in both contexts); y→y is massively over-produced in MID (3.65 vs 2.491).

---

## Results Summary

| Pair | VMS_Eg | Sim_Eg | VMS_Em | Sim_Em | Eg | Em |
|------|--------|--------|--------|--------|-----|-----|
| ot→ot | 2.053 | 1.381 | 1.887 | **1.410** | SIM<VMS | SIM<VMS |
| l→l | 2.116 | 1.790 | 2.203 | **2.192** | SIM<VMS | **match** |
| ok→ok | 1.449 | 1.729 | 1.322 | **1.742** | SIM>VMS | SIM>VMS |
| y→y | 1.710 | 1.613 | 2.491 | **3.646** | match | **SIM>>VMS** |
| d→d | 1.057 | 1.290 | 1.540 | **2.232** | SIM>VMS | SIM>VMS |
| qok→qok | 1.286 | 1.345 | 1.169 | **1.298** | match | SIM>VMS |
| ol→ol | 1.640 | 1.880 | 1.785 | **2.304** | SIM>VMS | SIM>VMS |
| o→o | 1.452 | 1.891 | 1.429 | **2.438** | SIM>VMS | SIM>VMS |
| ch→ch | 1.083 | 1.335 | 0.943 | **1.227** | SIM>VMS | SIM>VMS |
| sh→sh | 1.094 | 1.599 | 0.937 | **1.504** | SIM>VMS | SIM>VMS |
| qok→ch | 1.424 | 1.344 | 1.234 | **1.156** | match | match |
| sh→qok | 2.109 | 1.032 | 1.967 | **0.949** | SIM<VMS | SIM<VMS |
| s→sh | 2.144 | 1.169 | 0.999 | **1.092** | SIM<VMS | match |

---

## Key Findings

### 1. exp_245 Prediction Was Wrong for ot→ot

exp_245 predicted Sim_Em(ot→ot) ≈ 2.2 (over-production). Actual: Sim_Em=1.41 (SIM<VMS, under-production). The simplified diagnostic simulation had different buffer dynamics (no Markov rules, different vocabulary) that created higher buffer autocorrelation for ot-onset than the full exp_236 architecture. H444's original claim that the model under-reproduces ot→ot is CONFIRMED — it was a genuine effect, not a measurement artifact.

### 2. y→y is Massively Over-Produced in MID Context (B-Dialect)

Sim_Em(y→y) = 3.646 vs VMS_Em = 2.491 → 146% of target (SIM >> VMS). The y-onset is rare (2.21% MID rate), so when the previous word was y, the buffer is strongly enriched in y (buffer has 9.21% y when prev=y, vs 2.21% global — from exp_245). The cp=0.55 buffer draws in MID positions then heavily produce y→y.

Yet the 19-metric battery ss_y = 1.613 (global, sim) vs 1.710 (global, VMS) → 94.3% — within PASS zone. The battery catches global y→y but misses the MID-specific over-production. **This is a new finding about battery incompleteness.**

### 3. Many Common-Onset Self-Successions Are Over-Produced in MID

SIM>VMS in MID context: ok (1.742 vs 1.322), d (2.232 vs 1.540), ol (2.304 vs 1.785), o (2.438 vs 1.429), ch (1.227 vs 0.943), sh (1.504 vs 0.937). The copy buffer creates too much self-succession for these onsets because it draws from an autocorrelated buffer.

Note: ch→ch and sh→sh in VMS MID are actually DEPLETED (E_mid < 1): VMS has ch→ch E_mid=0.943, sh→sh E_mid=0.937. The VMS avoids consecutive ch or sh in MID positions. The simulation (without anti-repetition constraint) over-produces these.

### 4. ot→ot Is a Genuine Architecture Gap

Both contexts: global (1.381 vs 2.053) and MID (1.410 vs 1.887) — SIM<VMS. The model produces insufficient ot→ot succession. This may reflect a genuine temporal clustering of ot-onset words in VMS that the buffer doesn't capture, or an explicit grammatical rule.

### 5. l→l: Global Gap From Positional Composition

l→l global: SIM<VMS (1.790 vs 2.116). l→l MID: match (2.192 vs 2.203). This is the expected pattern for a feature that's driven by MID-only grammar: the global gap reflects dilution from cross-position pairs. The l→l rule IS correctly reproduced in MID context.

### 6. sh→qok Gap Confirmed

Both contexts under-produced: global (1.032 vs 2.109) and MID (0.949 vs 1.967). Consistent with exp_242, exp_243, exp_244.

### 7. qok→ch Reproduced Correctly

Match in both global (1.344 vs 1.424) and MID (1.156 vs 1.234). The Markov mechanism correctly captures this rule.

### 8. s→sh: Cross-Position Artifact Pattern Confirmed

Global: SIM<VMS (1.169 vs 2.144). MID: match (1.092 vs 0.999). The global enrichment of s→sh in VMS (2.144) is a cross-position artifact — when measured in MID-only context, both VMS and sim show E≈1.0 (no enrichment). Consistent with exp_242.

---

## Interpretation

### The 19-Metric Battery Is Incomplete for Bigram Structure

The battery uses global bigrams with global onset rates for self-succession metrics (ss_d, ss_y, ss_mean using qok/ok/ch). These metrics:
- Match global E_global ≈ VMS for y→y (sim 1.613 vs VMS 1.710)
- But miss that MID-only E_mid(y→y) is massively over-produced (3.646 vs 2.491)
- Similarly, many MID over-productions (d, ol, o, ch, sh) are not captured by global battery metrics

A complete validation would require MID-only bigram metrics. These are not in the current battery.

### Architecture Bigram Classification

| Type | Examples | Status |
|------|---------|--------|
| Over-produced (MID): | ok, d, ol, o, ch, sh | Buffer over-clustering for common onsets |
| Over-produced (MID, severe): | y→y (E=3.65 vs 2.49) | Rare onset → strong buffer clustering |
| Under-produced (both): | ot→ot | Genuine architecture gap |
| Approximately correct (MID): | l→l, qok→ch, qok→qok | Reproduced correctly |
| Under-produced (architecture gap): | sh→qok | High-magnitude cross-onset rule |

### ot→ot: Genuine Gap Requiring Investigation

The model consistently under-produces ot→ot (MID: 1.41 vs 1.887). This is a real effect. The buffer autocorrelation should produce some ot self-succession, but apparently not enough. Possible explanations:
- ot words are highly vocabulary-diverse, reducing repeated buffer draws
- VMS has section-level ot clustering that global buffer doesn't capture
- The VMS ot→ot succession is partly driven by a specific vocabulary subset

---

## Self-Audit

**Target-awareness**: No target-aware elements. Simulation uses frozen exp_236 parameters. Bigram enrichments computed from simulation output, not calibrated to any target.

**Feature-destroying implementation**: No feature-destroying details. Both global and MID-only bigrams correctly computed. The distinction (global uses all consecutive pairs; MID-only uses only pairs where both indices are in 1..n-2) is correctly implemented.

**Extrapolation**: All claims are within the tested simulation output. The comparison to exp_245 prediction is clearly labeled ("exp_245 prediction was wrong for ot→ot"). No "structural" or "cannot" claims.

**Negative-result scope**: The exp_245 prediction being wrong for ot→ot means the simplified diagnostic had incorrect buffer dynamics — this is a limitation of the exp_245 methodology, not a claim about the architecture in general.

**Control behavior**: VMS values serve as the reference. The qok→ch Markov rule matches in both global and MID contexts — this serves as a positive control showing the simulation correctly reproduces known rules.

---

## Conclusions

1. **exp_245 prediction partially wrong**: ot→ot is genuinely under-produced (not over-produced). Simplified diagnostic had different buffer dynamics.
2. **ot→ot is a genuine architecture gap** (MID: 1.41 vs 1.887) — real under-production in both global and MID contexts.
3. **y→y massively over-produced in MID** (3.65 vs 2.49) — battery ss_y metric doesn't catch this because it uses global rates.
4. **Many onset self-successions over-produced in MID**: ok, d, ol, o, ch, sh. VMS ch→ch and sh→sh are actually DEPLETED in MID (E<1).
5. **sh→qok gap confirmed**: both contexts under-produced.
6. **Battery incompleteness confirmed**: 19-metric battery misses MID-specific bigram structure (over and under-production in MID-only context).
7. **Next**: Add H447 (ot→ot mechanism investigation) and update open_questions with battery incompleteness finding.
