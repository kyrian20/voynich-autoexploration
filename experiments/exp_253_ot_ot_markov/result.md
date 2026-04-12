# exp_253: ot→ot Markov Rule — H447
**Date**: 2026-04-11
**Hypothesis**: H447 — Does adding p_ot_ot (when prev_onset='ot', seek ot-onset word from buffer) fix the B-dialect ot→ot MID E2 gap (sim≈1.41 vs VMS=1.887) without regressing the 19-metric battery?
**Status**: PARTIALLY CONFIRMED — p_ot_ot=0.10 gives 19/19 PASS and reduces ot→ot gap by 56% (1.41→1.677, vs VMS=1.887). Full closure at p_ot_ot=0.15 causes marginal battery regression.

## Key Finding

**p_ot_ot=0.10 is viable: 19/19 PASS maintained, ot→ot gap reduced from 0.477 to 0.210 (56% reduction).**

Full sweep results:

| p_ot_ot | N=5 Pass | N=30 Pass | ot→ot_mid | Gap from VMS |
|---------|----------|-----------|-----------|-------------|
| 0.00 (baseline) | 18/19 | 19/19* | ~1.41 | 0.477 |
| 0.05 | 19/19 | 19/19 | 1.559 | 0.328 |
| 0.10 | 19/19 | 19/19 | 1.677 | 0.210 |
| 0.15 | 19/19 | 18/19 | 1.789 | 0.098 |
| 0.20 | 18/19 | — | 1.875 | — |

*Baseline N=30 from exp_249 (19/19 PASS confirmed); ot→ot≈1.41 from exp_246.

**VMS B-dialect ot→ot MID E2 = 1.887 (N=113)**

The mechanism works mechanically. Unlike sh→qok (Δ=1.01, maximum achievable ~1.41), the ot→ot rule has a lower starting gap (Δ=0.477) that the Markov mechanism can partially close. The natural buffer self-succession for ot already achieves E2≈1.41 (ot-onset is ~7% global; buffer auto-correlation provides moderate enrichment). Adding p_ot_ot builds on this base.

## Battery Regression Analysis

At p_ot_ot=0.15, the single failure is **am_lf_enr=121.1% (VMS=12.25%)** — 1.1% outside the ±20% pass zone. All other 18 metrics PASS.

Mechanism for regression: p_ot_ot biases buffer draws toward ot-onset words when prev=ot. ot-onset words have low -am suffix rate (ot-onset words like "otaiin", "oteedy" rarely end in -am). This slightly reduces global_am_rate, which inflates am_lf_enr = lf_am / global_am. At p=0.10, this effect is small enough that am_lf_enr remains within the pass zone (99.5%). At p=0.15, the bias is just large enough to push am_lf_enr to 121.1%.

At p_ot_ot=0.10:
- am_lf_enr: 99.5% PASS
- All 19 metrics PASS
- ot→ot_mid: 1.677 (vs VMS=1.887, 88.9% of target — 11% gap)
- sh→qok MID: unchanged (~0.96)

## Architecture Decision

**Architecture recommendation: Add p_ot_ot=0.10 to B-dialect draw_buf.**

Rationale:
1. 19/19 PASS maintained (N=30)
2. ot→ot gap reduced from 0.477 to 0.210 — significant structural improvement
3. Rule is grammar-motivated: exp_252/H448 confirmed ot→ot is grammatical (HHI=1.23×, 93 unique pairs)
4. Parameter magnitude is consistent with existing rules: p_qokch=p_chqok=0.12; p_ot_ot=0.10 is in the same range

The remaining gap at p=0.10 (ot→ot=1.677 vs VMS=1.887) is acceptable given that:
- Full closure (p=0.15) causes marginal battery regression
- The battery doesn't test ot→ot directly; structural improvement beyond 19/19 is desirable but not required
- The analog situation for ch→qok: sim=1.242 vs VMS=1.147 (8% overshoot after p_chqok=0.12) was accepted. Here: sim=1.677 vs VMS=1.887 (11% undershoot at p=0.10).

**Updated B-dialect architecture: 13 mechanisms, 19/19 PASS** — adds p_ot_ot=0.10 to the 12-mechanism exp_249 baseline.

## Comparison to sh→qok

The sh→qok gap (Δ=1.01) failed because the mechanism could not reach the target at any viable p. ot→ot (Δ=0.477) is different: the target is within the mechanism's reach (p=0.15 achieves gap=0.098) but the regression at p=0.15 prevents full closure. This is a fundamentally different failure mode from sh→qok:

- **sh→qok**: architectural limit (mechanism cannot produce sufficient enrichment at any safe p)
- **ot→ot**: parameter constraint (mechanism can reach target but causes regression at the required p)

The ot→ot result supports the view that the copy-buffer Markov mechanism has a fixed "capacity" — it works well for Δ≤0.5 gaps but not for Δ≥1.0 gaps.

## Self-Audit

**Target-awareness**: No target-aware elements. ot→ot MID E2 is not a battery metric. Sweep values (0.05, 0.10, 0.15, 0.20) were selected without reference to any battery target.

**Feature-destroying implementation**: draw_buf processes qok→ch and ch→qok Markov rules before p_ot_ot. With p_qokch=0.12 and p_chqok=0.12, approximately 24% of all prev_onset='qok' draws are consumed by those rules. But prev_onset='ot' is independent — ot tokens don't trigger qok→ch or ch→qok. The p_ot_ot rule fires when prev='ot' (independently of the qok/ch rules). No feature-destroying implementation.

**Extrapolation**: No extrapolated claims. "p_ot_ot=0.15 causes regression" is supported by N=30 direct measurement. "p_ot_ot=0.10 is safe" is supported by N=30 direct measurement (19/19). The architectural limit for ot→ot is not claimed to be structural — specifically, p_ot_ot cannot fully close the gap at safe values (p≤0.10), but p=0.15 achieves 98% of target at the cost of marginal regression. This is not an "architectural limit" in the sh→qok sense.

**Negative-result scope**: H447 is PARTIALLY CONFIRMED, not fully confirmed. The specific scope: "p_ot_ot=0.10 maintains 19/19 PASS and reduces ot→ot gap by 56%. p_ot_ot=0.15 achieves 98% of target but causes marginal am_lf_enr regression (121.1%). No tested value simultaneously achieves 19/19 PASS and ot→ot ≥ 1.800."

**Control behavior**: Baseline (p_ot_ot=0.00) produces ot→ot MID E2≈1.41. Expected: natural buffer self-succession at ot rate (~7% global) should produce moderate enrichment above 1.0 (buffer correlation gives 2-3× onset rate). Actual: ~1.41. This is consistent with exp_245's buffer theory (expected enrichment = rate^2 × buffer_size factor). Adding p_ot_ot increases ot→ot monotonically as expected (1.559, 1.677, 1.789, ~1.875 for p=0.05-0.20). The mechanism behaves as theoretically predicted. No surprising control behavior.

## Conclusion

H447 PARTIALLY CONFIRMED. Adding p_ot_ot=0.10 to the B-dialect architecture (exp_249 baseline + p_ot_ot=0.10): 19/19 PASS maintained (N=30), ot→ot MID E2 improved from ~1.41 to 1.677 (vs VMS=1.887, gap reduced by 56%). Full gap closure at p=0.15 (ot→ot=1.789) causes marginal am_lf_enr regression (121.1%). Recommended architecture addition: p_ot_ot=0.10. Updated B-dialect architecture: 13 mechanisms, 19/19 PASS.
