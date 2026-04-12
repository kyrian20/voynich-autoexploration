# exp_251: A-Dialect qok→qok Self-Succession Markov Rule — H456
**Date**: 2026-04-11
**Hypothesis**: H456 — Does adding p_qok_qok to A-dialect architecture fix the qok→qok MID E2 gap (VMS=1.750, estimated sim baseline ~1.3)?
**Status**: NEGATIVE — PREMISE INVALIDATED. A-dialect baseline already produces qok→qok MID E2=1.727 (VMS=1.750), a 1.3% gap. No rule needed.

## Key Finding

**The estimated baseline of ~1.3 in H456 was wrong.** The actual A-dialect sim baseline (exp_239 + p_y_y=0.10, no p_qok_qok) produces qok→qok MID E2 = 1.727 (N=30), which is 1.3% below VMS=1.750. This is within normal sampling noise. The "gap" that motivated H456 does not exist.

**Adding p_qok_qok causes overshoot at all tested values:**

| p_qok_qok | Pass/19 (N=5) | qok→qok_mid | Gap from VMS |
|-----------|--------------|-------------|-------------|
| 0.00 (baseline) | 18/19 | 1.690 (N=5) / 1.727 (N=30) | 0.060 / 0.023 |
| 0.05 | 19/19 | 2.140 | 0.390 |
| 0.10 | 18/19 | 2.354 | 0.604 |
| 0.15 | 19/19 | 2.879 | 1.129 |

VMS A-dialect qok→qok MID E2 = **1.750**.

The baseline (N=30) gap is 0.023 (1.3%), which is smaller than measurement noise at N=5 (range: 0.023-0.060). The copy buffer's natural self-succession mechanism already produces the correct qok→qok enrichment.

## Architecture Decision

**Do NOT add p_qok_qok to A-dialect architecture.**

The A-dialect architecture remains at exp_239 parameters (p_qokch=0.12, p_y_y=0.10, p_chqok=0.00). The qok→qok MID E2 is already correctly reproduced by the existing buffer dynamics.

Full N=30 battery at p_qok_qok=0.05 (best sweep value): 19/19 PASS, but qok→qok=2.083 — 19% above VMS. The battery does not test qok→qok directly, so passing 19/19 is consistent with significant structural overshoot. Adding the rule passes the battery but worsens the structural match.

## Baseline Architecture Confirmed (N=30)

VMS A-dialect MID bigram E2 values vs baseline sim (p_qok_qok=0.00):

| Pair | VMS | Sim (N=30) | Gap |
|------|-----|------------|-----|
| qok→qok | 1.750 | 1.727 | 0.023 |
| y→y | 2.853 | 2.854 | 0.001 |
| qok→ch | 0.985 | 1.133 | +0.148 |
| ch→qok | 0.877 | 0.930 | +0.053 |

The qok→ch A-dialect overshoot (1.133 vs VMS=0.985, 15% above) is a persistent feature: p_qokch=0.12 is active and biases qok→ch upward. In VMS A-dialect, qok→ch is near-random (0.985). The battery passes (qok_ch = 96.3% of VMS, within ±20%), so this does not block the architecture.

## Why the Baseline Achieves qok→qok≈1.75

The copy buffer (window=20) naturally elevates self-succession for all onset classes. When a qok word is placed in the buffer, subsequent buffer draws have an elevated probability of selecting another qok word (window memory effect). The qok self-succession mechanism is buffer-intrinsic. The A-dialect has a higher rate of MID words (r_mid=0.87 vs B-dialect r_mid=0.25), so MID-MID copies are more frequent, amplifying the buffer's natural self-succession. This explains why A-dialect qok→qok (1.750) exceeds B-dialect (1.169): higher MID copy rate → stronger natural self-succession.

The p_y_y=0.10 rule was necessary for y→y because y is rare enough that the buffer's natural rate was insufficient. qok is more common, so the buffer's natural rate suffices.

## Revised Understanding of A-Dialect Grammar

The A-dialect grammar taxonomy established in exp_250 should be refined:

- **y→y (p_y_y=0.10)**: Needed because y is rare (~4% global) → buffer self-succession insufficient → explicit rule required
- **qok→qok**: NOT needed; qok is frequent enough (~15-20% MID) → buffer self-succession sufficient
- **The rule-need threshold is onset frequency**: explicit Markov rules are needed when the onset is too rare for the buffer to provide natural self-succession; not needed when buffer dynamics already achieve target enrichment

This is consistent with B-dialect: d→d (d is low-frequency at LF) might need explicit treatment but is not currently modeled.

## Limitations

- N=5 baseline shows 18/19 (one failure), N=30 shows 19/19. The N=5 failure is noise — the baseline is robust at N=30.
- H456 was based on an estimated baseline of ~1.3 drawn from exp_250 wording. That estimate was not directly measured; the correct baseline (1.727) is 32% higher than the estimate.
- qok→ch A-dialect overshoot (1.133 vs VMS=0.985) is unaddressed. Reducing p_qokch for A-dialect might improve this, but p_qokch=0.12 is the only tested value and 19/19 PASS is maintained.

## Self-Audit

**Target-awareness**: No target-aware elements. The qok→qok MID E2 is not a battery metric and was not used to calibrate any parameter. The sweep values (0.05, 0.10, 0.15) were selected without reference to VMS targets.

**Feature-destroying implementation**: In draw_buf, p_qokch is checked before p_qok_qok. Both conditions require prev_onset='qok'. With p_qokch=0.12, approximately 12% of qok triggers are consumed by the ch-redirection before p_qok_qok fires. This reduces the effective p_qok_qok by ~12%. This effect is small and expected. It does not destroy the feature being tested — the rule still fires at the intended conditional probability minus the small p_qokch preemption. No feature-destroying implementation.

**Extrapolation**: No extrapolated claims. The conclusion "baseline already achieves qok→qok≈VMS" is supported by N=30 direct measurement (1.727 vs 1.750). The conclusion "p_qok_qok causes overshoot" is supported by all three sweep values (0.05→2.140, 0.10→2.354, 0.15→2.879). The minimum tested p_qok_qok (0.05) already gives a 22% overshoot; a smaller untested value (p_qok_qok≈0.01-0.03) might achieve closer to VMS, but the baseline gap is only 0.023, making any improvement marginal. Not claiming values below 0.05 would fail; only that they are not needed given the baseline already achieves target.

**Negative-result scope**: H456 is NEGATIVE because the premise (gap exists) was wrong. The specific scope: "The A-dialect baseline sim (exp_239 + p_y_y=0.10) produces qok→qok MID E2=1.727, which is within measurement noise of VMS=1.750. Adding p_qok_qok at tested values 0.05-0.15 overshoots the target by 22-65%. No p_qok_qok rule is warranted for A-dialect." This does not imply qok self-succession rules are unnecessary in all architectures; it is specific to A-dialect buffer dynamics at the current architecture parameters.

**Control behavior**: Baseline (p_qok_qok=0.00) is the control. Expected: buffer self-succession at A-dialect parameters (r_mid=0.87, cp=0.55, window=20) would produce qok→qok enrichment above 1.0. Expected range: 1.3-1.5 (based on exp_250 estimate). Actual: 1.727 (N=30). The control exceeded the expected value — the buffer's natural qok self-succession is stronger than estimated. This was the signal: the buffer already achieves VMS without an explicit rule. This is consistent with exp_245's finding that buffer self-succession enrichment scales with onset frequency and MID copy rate.

## Conclusion

H456 NEGATIVE (premise invalidated). The A-dialect sim baseline already produces qok→qok MID E2=1.727 (VMS=1.750), a 1.3% gap that is within sampling noise. Adding p_qok_qok at any tested value (0.05-0.15) causes significant overshoot (2.083-2.879). The A-dialect architecture remains unchanged at exp_239 parameters. New understanding: onset-specific Markov rules are needed only when onset frequency is too low for buffer self-succession to achieve target enrichment (y at ~4% global needs p_y_y; qok at ~15-20% MID does not).
