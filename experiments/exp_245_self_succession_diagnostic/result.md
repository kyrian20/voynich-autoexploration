# exp_245: H444 — Self-Succession Under-Reproduction Diagnostic

**Date:** 2026-04-11
**Hypothesis:** H444 — Copy buffer under-reproduces ot→ot, l→l, ok→ok self-succession relative to VMS.

**Status:** H444 OVERTURNED — The copy-buffer architecture does NOT under-produce self-succession in the MID-only context. Buffer is highly auto-correlated: P(buf has X | prev=X) is 2-4× the MID onset rate for all moderate onsets. The theoretical E_mid_sim(X→X) from buffer dynamics alone exceeds VMS E_mid(X→X) for most onsets. The exp_241 MISSED classification was an artifact of using GLOBAL bigram enrichments (normalized by global rates) instead of MID-only enrichments. The simple theoretical formula E = 1 + p_stutter/rate_mid was incorrect — it assumed a stationary buffer.

---

## Key Findings

### 1. Buffer Is Strongly Auto-Correlated

When the previous word has onset X, the buffer (window=20) is significantly enriched in X-onset words relative to the global MID onset rate:

| Onset | Rate_mid | P(buf has X \| prev=X) | Enrichment ratio |
|-------|---------|----------------------|-----------------|
| qok | 14.19% | 21.90% | **1.54×** |
| ch | 17.67% | 24.67% | **1.40×** |
| ot | 7.21% | 21.97% | **3.05×** |
| ol | 5.13% | 15.39% | **3.00×** |
| ok | 7.52% | 16.89% | **2.25×** |
| y | 2.21% | 9.21% | **4.17×** |
| l | 5.37% | 12.98% | **2.42×** |
| d | 4.87% | 12.62% | **2.59×** |
| o | 4.05% | 13.57% | **3.35×** |

This auto-correlation is caused by the copy buffer mechanism itself: words generated from the buffer are added back into the buffer, creating temporal clustering around onset classes. When position i has onset X (likely copied from buffer containing X words), the buffer at position i+1 contains the X word at position i plus residual X words from the earlier copy cascade.

### 2. Simple Theoretical Formula Was Wrong

I predicted E(X→X) = 1 + p_stutter/rate_mid(X), which assumed a stationary buffer. This was incorrect:

| Onset | E_mid_VMS | E_theory (simple) | E_buf_theory (actual) | Delta (actual vs VMS) |
|-------|---------|------------------|----------------------|----------------------|
| qok | 1.169 | 1.042 | **1.334** | SIM > VMS +0.165 |
| ok | 1.322 | 1.080 | **1.756** | SIM > VMS +0.434 |
| ot | 1.887 | 1.083 | **2.195** | SIM > VMS +0.308 |
| ol | 1.785 | 1.117 | **2.206** | SIM > VMS +0.421 |
| y | 2.491 | 1.272 | **2.997** | SIM > VMS +0.506 |
| l | 2.203 | 1.112 | **1.882** | VMS > SIM -0.321 |
| d | 1.540 | 1.123 | **1.988** | SIM > VMS +0.448 |
| o | 1.429 | 1.148 | **2.427** | SIM > VMS +0.998 |

**The simulation OVER-produces MID-only self-succession for most onsets.** Only l (l→l) shows the simulation below VMS.

E_buf_theory computed as: P_stutter + (1-P_stutter) × [CP × P(X in buf|prev=X) + (1-CP) × rate_mid(X)] / rate_mid(X)

### 3. Why exp_241 Showed MISSED for ot→ot (sim 1.287 vs VMS 1.886)

exp_241 used GLOBAL bigrams: E(X→X)_global = P_global(X→X) / P_global(X)².

P_global(X) combines LF, MID, and LL onset rates. For ot:
- ot is concentrated in MID (7.21%), less common at LF/LL
- P_global(ot) < P_mid(ot)
- E_global(ot→ot)_sim uses a denominator of P_global(ot)² ≠ P_mid(ot)²

Additionally, global bigrams include cross-position pairs (LF→MID, MID→LL) where self-succession enrichment is near zero, diluting the MID-MID self-succession signal. For 73% MID-MID pairs and 27% cross pairs:

E_global ≈ 0.73 × E_mid + 0.27 × E_cross ≈ 0.73 × 2.2 + 0.27 × 1.0 ≈ 1.88 ≈ VMS E_global

So the sim actually MATCHES VMS for global E(ot→ot) ≈ 1.88 — consistent with the exp_241 VMS value of 1.886. The sim value of 1.287 from exp_241 was computed with a different normalization (global rates vs MID rates, with different global rates in sim vs VMS due to different LF/LL compositions).

### 4. Cross-Onset: sh→qok Gap Confirmed

The theoretical E(sh→qok) from buffer dynamics = ~1.0 (buffer has qok at global rate after sh). VMS E_mid = 1.967. This is a +0.967 gap — genuine grammatical rule unexplained by buffer dynamics (consistent with exp_243 and exp_244 findings).

---

## Interpretation

### The H444 premise was based on a measurement artifact from exp_241

The exp_241 "MISSED" classification for ot→ot, l→l, ok→ok self-succession was based on comparing global E values with mismatched denominators (sim global rate vs VMS global rate differ due to different LF/LL compositions). When evaluated on the correct basis (MID-only enrichment with MID rates), the simulation likely OVER-produces self-succession for most onsets.

### The copy-buffer mechanism correctly captures self-succession via buffer autocorrelation

The key mechanism is not p_stutter (which contributes only 0.006/rate ≈ 4-27% of the enrichment) but the buffer autocorrelation. When onset X appears at position i:
1. Word i is added to the buffer
2. At position i+1, the buffer is enriched in X (word i is there, plus earlier X words from copy cascades)
3. Drawing from the enriched buffer produces X with 2-4× higher probability than global rate
4. This creates genuine MID-level self-succession enrichment

### The architecture gap is cross-onset, not self-succession

The genuine architecture gap is for **cross-onset succession rules with large magnitude** (sh→qok: Δ=+0.97, ot→ot_VMS is actually well-matched). The architecture handles:
- ✓ Self-succession via buffer autocorrelation (naturally produced)
- ✓ Low-magnitude cross-onset rules via Markov parameters (qok→ch Δ=+0.18)
- ✗ High-magnitude cross-onset rules (sh→qok Δ=+0.97, requires mechanism beyond onset-Markov)

---

## Limitations

1. E_buf_theory is computed from a simplified diagnostic simulation (no Markov rules, simplified modification). The full exp_236 architecture may have different buffer composition.
2. The comparison to exp_241 is analytical — a direct verification would require running exp_236 with MID-only self-succession tracking.
3. L→l shows sim < VMS (E_buf_theory=1.882 vs VMS 2.203). This might be a genuine gap for l-onset, or might be due to the simplified simulation.

---

## Self-Audit

**Target-awareness**: No target-aware elements. This is a purely analytical/diagnostic experiment with no simulation parameters calibrated to VMS targets.

**Feature-destroying implementation**: No feature-destroying implementation details. The buffer composition logging correctly samples from the actual buffer state before each draw. The simplified diagnostic (no Markov rules) may have different buffer composition than exp_236 — this is a limitation, not a feature-destroying issue.

**Extrapolation**: The claim "exp_241 MISSED classification was an artifact" is stated as a hypothesis for why the global E values differ from MID-only E values. It is supported by the analytical calculation (E_global ≈ 1.88 from E_mid ≈ 2.2 and cross-pair dilution) but has NOT been directly verified by running exp_236 with MID-only tracking. The correct formulation is: "the buffer autocorrelation analysis predicts that E_mid_sim(ot→ot) ≈ 2.2, which would match VMS E_mid = 1.887 (overshooting) rather than underproducing it."

**Negative-result scope**: H444 is "overturned" in the sense that the premise (under-production of self-succession) is likely incorrect based on this analysis. This is a clarification of exp_241's measurement context, not a full experimental refutation. Direct verification recommended (exp_246: run full exp_236 with MID-only bigram tracking).

**Control behavior**: No external controls. The buffer composition from the simplified diagnostic is the primary data source.

---

## Conclusions

1. **H444 OVERTURNED (with caveat)**: Buffer autocorrelation (not p_stutter) is the primary driver of self-succession enrichment in the simulation. Buffer is 2-4× enriched in X when prev=X.
2. **Theoretical formula corrected**: E(X→X) = 1 + p_stutter/rate is wrong (assumes stationary buffer). Actual E_buf_theory is 1.3-3.0×, matching or exceeding VMS for most onsets.
3. **exp_241 MISSED classification needs reinterpretation**: Likely a global vs MID measurement artifact. Direct verification needed (exp_246).
4. **True architecture gap**: Cross-onset high-magnitude rules (sh→qok), not self-succession.
5. **Next**: exp_246 — run full exp_236 architecture with both global and MID-only self-succession tracking to verify this interpretation.
