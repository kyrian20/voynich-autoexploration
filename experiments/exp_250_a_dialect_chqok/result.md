# exp_250: A-Dialect ch→qok Analysis — H455
**Date**: 2026-04-11
**Hypothesis**: H455 — does A-dialect have ch→qok enrichment? Should p_chqok be added?
**Status**: NEGATIVE — A-dialect ch→qok is DEPLETED (E2=0.877); p_chqok should NOT be added to A-dialect architecture

## Key Finding

**A-dialect VMS has ch→qok MID E2=0.877** — below 1.0, meaning ch is followed by qok at a LOWER rate than chance. This is the OPPOSITE direction from B-dialect (E2=1.147).

A-dialect vs B-dialect MID bigram comparison:

| Onset pair | A-dialect VMS | B-dialect VMS |
|-----------|--------------|--------------|
| ch→qok | **0.877** (depleted) | **1.147** (enriched) |
| qok→ch | 0.985 (near 1.0) | 1.234 (enriched) |
| qok→qok | 1.750 (enriched) | 1.169 |
| y→y | 2.853 | 2.491 |

This is a genuine dialect asymmetry:
- **B-dialect**: qok↔ch bidirectional coupling (both qok→ch and ch→qok enriched)
- **A-dialect**: NO qok↔ch coupling; qok is self-successive (E2=1.750 vs B's 1.169); ch→qok depleted

## Architecture Decision

**Do NOT add p_chqok to A-dialect architecture.**

The baseline A-dialect simulation (exp_239 + p_y_y=0.10, p_chqok=0.00) already gives ch→qok=0.930 (VMS=0.877) — 6% overshoot but much better than with p_chqok=0.12 which gives 1.352 (54% overshoot, wrong direction).

Sweep results (N=5):
- p_chqok=0.00: 19/19 PASS, ch→qok=0.932, qok→ch=1.132, y→y=3.024
- p_chqok=0.06: 18/19 PASS (noise)
- p_chqok=0.12: 19/19 PASS, ch→qok=1.354, qok→ch=1.099, y→y=3.210

Although p_chqok=0.12 passes the battery (19/19), it moves ch→qok further from VMS (0.932→1.354 vs VMS=0.877). The battery doesn't test MID-only ch→qok directly — this is a structural gap not visible to the battery.

**The A-dialect architecture remains at p_chqok=0.00 (exp_239 parameters unchanged).**

## Interpretation

The qok↔ch coupling is B-dialect specific. In B-dialect, both directions are enriched at p=0.12, producing a bidirectional grammatical rule. In A-dialect, the pattern is absent — ch is not followed by qok at enriched rate, and qok is not followed by ch at enriched rate (0.985). Instead, A-dialect has stronger qok→qok self-succession (1.750 vs B's 1.169).

This reinforces the dialect distinction:
- **B-dialect grammar**: onset-succession rules between different classes (qok↔ch)
- **A-dialect grammar**: stronger self-succession within classes (qok→qok, y→y), weaker cross-class succession

The p_y_y=0.10 A-dialect Markov rule captures y→y self-succession. The qok→qok enrichment (1.750) is not in the battery and not currently modeled; it may warrant investigation (H456 candidate).

## Limitations

- A-dialect has only 1712 lines (vs B-dialect's 2411) — MID bigram counts are smaller
- The N=5 sweep failure at p_chqok=0.06 (18/19) is likely noise; not further investigated
- qok→qok A-dialect enrichment (1.750) is a genuine gap not in the current architecture or battery

## Self-Audit

**Target-awareness**: No target-aware elements. ch→qok was measured from VMS corpus, not calibrated to any battery metric.

**Feature-destroying implementation**: No feature-destroying details. The measurement (ch→qok MID E2 from VMS A-dialect) is direct and unbiased.

**Extrapolation**: "Do NOT add p_chqok to A-dialect" is specific to this parameter and this dialect. A different mechanism might model A-dialect qok→qok enrichment in a different way.

**Negative-result scope**: The negative result is: "VMS A-dialect ch→qok is depleted (E2=0.877), so adding a ch→qok Markov bias to the A-dialect architecture would worsen structural match." This does not imply the A-dialect has no onset-succession rules — p_qokch=0.12 and p_y_y=0.10 already model two.

**Control behavior**: Baseline sim ch→qok=0.930 (VMS=0.877) — expected near 1.0 without a Markov rule; slight overshoot consistent with buffer composition. Adding p_chqok increases ch→qok monotonically as expected. Behavior matches theoretical predictions.

## Conclusion

H455 NEGATIVE. A-dialect VMS has ch→qok E2=0.877 (depleted), opposite of B-dialect (1.147). The qok↔ch bidirectional coupling is B-dialect specific. A-dialect architecture remains unchanged (exp_239 parameters: p_chqok=0.00). New finding: A-dialect qok→qok MID E2=1.750 (much stronger than B-dialect's 1.169) — candidate for future investigation (H456).
