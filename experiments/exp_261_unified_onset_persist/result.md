# exp_261: Unified Onset Persistence Rule

**Date**: 2026-04-11
**Hypothesis**: H462 — A single p_persist=0.10 parameter (applied to all onset classes with MID rate < threshold) can replace separate p_y_y=0.10 and p_o_o=0.10, maintaining 19/19 PASS while reducing A-dialect from 12 to 11 mechanisms.
**Architecture**: Exact exp_258 implementation with draw_buf variants.

## Setup

Onset MID rates determine which onsets would receive the persist rule at each threshold:
- y: 5.22%, o: 5.10% — both need persist rules (confirmed by exp_255, exp_258)
- ok: 6.40%, qok: 6.35% — above threshold at thr=0.06; below at thr=0.07
- s: 1.66%, l: 0.56% — always below threshold; VMS s→s=0.887 (DEPLETED), VMS l→l=7.666

**VMS structural reference (MID E2):**
- y→y = 2.853, o→o = 2.801, s→s = 0.887 (depleted), l→l = 7.666

## Sweep Results (N=5)

| Condition                      | Pass/19 | y→y   | o→o   | s→s   | l→l    |
|-------------------------------|---------|-------|-------|-------|--------|
| VMS reference                 | —       | 2.853 | 2.801 | 0.887 | 7.666  |
| Separate p_y_y=p_o_o=0.10     | 19/19   | 2.835 | 3.280 | 3.671 | 7.428  |
| Unified p=0.10, thr=0.055     | 19/19   | 3.180 | 2.875 | 7.887 | 24.800 |
| Unified p=0.10, thr=0.060     | 17/19   | 2.843 | 2.879 | 6.463 | 16.959 |
| Unified p=0.10, thr=0.070     | 18/19   | 2.829 | 3.009 | 7.776 | 24.372 |

Best unified condition: thr=0.055 (19/19). Note: thr=0.055 and thr=0.060 include the same onsets (the gap between y=5.22% and ok=6.35% spans both thresholds).

## Full Battery: Unified p=0.10, thr=0.055 (N=30)

| Metric         | VMS    | Sim    | %VMS   | PASS |
|----------------|--------|--------|--------|------|
| am_ll          | 3.4993 | 3.5902 | 102.6% | PASS |
| d_ll           | 1.6549 | 1.7243 | 104.2% | PASS |
| y_lf           | 2.1840 | 2.0880 |  95.6% | PASS |
| ss_mean        | 1.5793 | 1.3390 |  84.8% | PASS |
| adj_rate       | 0.0093 | 0.0110 | 117.8% | PASS |
| qok_lf         | 1.0795 | 1.0679 |  98.9% | PASS |
| d_lf           | 1.1060 | 1.0879 |  98.4% | PASS |
| s_lf           | 2.1542 | 2.0104 |  93.3% | PASS |
| ch_ll          | 0.8549 | 0.8806 | 103.0% | PASS |
| ok_ll          | 1.0021 | 1.0591 | 105.7% | PASS |
| qok_ll         | 0.5127 | 0.5137 | 100.2% | PASS |
| ss_d           | 1.2739 | 1.1459 |  90.0% | PASS |
| ss_y           | 1.5874 | 1.6261 | 102.4% | PASS |
| am_lf_enr      | 0.2656 | 0.2691 | 101.3% | PASS |
| am_mid_enr     | 0.5324 | 0.5000 |  93.9% | PASS |
| edy_rate       | 0.0045 | 0.0045 | 101.2% | PASS |
| word_len_mean  | 5.2604 | 4.9410 |  93.9% | PASS |
| qok_ch         | 1.2200 | 1.2103 |  99.2% | PASS |
| global_am_rate | 0.0198 | 0.0192 |  96.8% | PASS |

**TOTAL: 19/19 PASS**

## Structural Checks vs Separate Rule

| Metric | VMS   | Unified thr=0.055 | Separate p_y_y+p_o_o |
|--------|-------|-------------------|----------------------|
| y→y    | 2.853 | 2.927 (+0.074)    | 2.765 (-0.088)       |
| o→o    | 2.801 | 2.932 (+0.131)    | 2.804 (+0.003)       |
| s→s    | 0.887 | 7.203 (+6.315) ⚠️ | 4.470 (+3.583)       |
| l→l    | 7.666 | 18.272 (+10.606)⚠️| 7.857 (+0.191) ✓     |

Both conditions pass the 19-metric battery. But structurally:
- **s→s**: VMS shows depletion (0.887 < 1.0 — anti-self-succession for s-onset). Unified rule amplifies to 7.203; separate rule amplifies to 4.470. Both wrong, but unified is 7× further.
- **l→l**: VMS = 7.666. Separate rule achieves 7.857 (within 2.5% — MATCH). Unified rule produces 18.272 (2.4× VMS).

## Interpretation

### Finding 1: Unified Rule Passes Battery But Degrades Structural Matches
The unified persist rule (threshold=0.055, capturing y, o, and 12 other rare onsets) passes 19/19. However, it massively over-produces s→s (7.203 vs VMS 0.887, 8.1× VMS) and l→l (18.272 vs VMS 7.666, 2.4× VMS). The separate rule (p_y_y + p_o_o) achieves l→l = 7.857 ≈ VMS without a dedicated l→l Markov rule, through buffer self-succession dynamics. Applying a persist rule to l-onset (MID rate 0.56%) artificially amplifies the already-sufficient l→l enrichment by a factor of 2.

### Finding 2: The Separate Two-Parameter Architecture Is Better
The separate p_y_y=0.10 + p_o_o=0.10 approach is architecturally superior because it targets exactly the onsets that need persistence enrichment, without disturbing rare onsets (s, l) that achieve their VMS E2 through natural buffer dynamics. The unified rule cannot distinguish between:
- y and o: low frequency, under-enriched by buffer alone, need explicit persist rule
- l: low frequency, correctly enriched by buffer dynamics (VMS l→l matched without rule)
- s: low frequency, VMS shows DEPLETION (s→s=0.887 < 1.0) — persist rule actively wrong direction

### Finding 3: The Onset-Persistence Insight Remains Valid
The theoretical finding from exp_258 — that explicit Markov rules are needed when onset frequency is too low for buffer self-succession to achieve the target — is confirmed here, but with a necessary refinement: low frequency alone is insufficient criterion. The onset's VMS target E2 must also exceed what buffer dynamics naturally produce. For l-onset, buffer dynamics already match VMS l→l. For s-onset, VMS shows depletion that no persist rule should address.

## Limitations

- s→s over-production (4.470 vs VMS 0.887) in BOTH conditions: this is a pre-existing structural gap not addressed by either approach. The s-onset depletion in VMS suggests an anti-s-self-succession mechanism; not pursued here.
- Only threshold values 0.055–0.070 tested; there may be no threshold that captures exactly y and o without other low-frequency onsets.

## Self-Audit

**Target-awareness**: No target-aware calibration in this test. Both conditions are pre-parameterized from prior experiments. N/A.

**Feature-destroying implementation**: No feature-destroying details. The unified rule is a fair test of the hypothesis.

**Extrapolation**: "The separate two-parameter architecture is better" — this is within the tested conditions (unified thr=0.055 vs separate p=0.10). Not extrapolating to untested parameter combinations.

**Negative-result scope**: H462 NEGATIVE under unified threshold approach. The conclusion is: "a unified onset-persistence threshold rule does not improve upon separate p_y_y and p_o_o parameters." This does not rule out other unification approaches (e.g., a rule that explicitly lists y and o but not l/s).

**Control behavior**: "Separate p_y_y+p_o_o" serves as the control (known good condition from exp_258). It achieves 19/19 PASS and l→l=7.857 ≈ VMS (excellent). The l→l structural match in the control is better than expected (we did not explicitly model l→l); the explanation is that l-onset rarity combined with buffer dynamics naturally produces VMS-level l→l enrichment. Behavior expected and consistent.

## Conclusion

H462 NEGATIVE. The unified onset persistence rule (single p_persist for all onsets below a frequency threshold) passes 19/19 PASS but produces structurally inferior results: s→s 8× VMS, l→l 2.4× VMS. The separate p_y_y=0.10 + p_o_o=0.10 approach is superior — it achieves s→s 5× VMS (also over, but less so) and l→l ≈ VMS (+0.191). A-dialect architecture remains at 12 mechanisms with two separate onset-persistence parameters.
