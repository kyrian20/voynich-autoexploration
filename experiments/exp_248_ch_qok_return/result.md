# exp_248: ch→qok Return Pattern — qok→ch→qok Second-Order Analysis
**Date**: 2026-04-11
**Hypothesis**: H453 — qok→ch→qok return pattern investigation
**Status**: RESOLVED — exp_247 BUG DISCOVERED; qok→ch→qok gap largely explained; ch→qok E2=1.147 identified as real but modest structural gap

## Question

exp_247 reported qok→ch→qok 2nd_order=1.483 (VMS) vs Sim_2nd=0.320 — a dramatic gap suggesting a second-order Markov rule. This experiment investigates:
1. Is ch→qok itself enriched as a binary MID bigram?
2. Is qok→ch→qok section-concentrated or lexically specific?
3. Does adding p_chqok to the simulation fix the gap?

## Critical Bug Discovery

**exp_247's Sim_2nd values were computed incorrectly due to a key-collision bug.** The simulation accumulator used `(x, y, 'E2_YZ')` as the key for E2(y→z), but multiple KEY_TRIGRAMS sharing the same (x,y) prefix wrote to the SAME key, causing double/triple-counting.

For qok→ch→(qok or sh): two KEY_TRIGRAMS shared key ('qok','ch','E2_YZ'), so the accumulator summed E2(ch→qok) + E2(ch→sh) ≈ 0.989 + 0.569 = 1.558 per trial instead of 0.989. Similarly, ('qok','ch','E2_XY') was written twice, doubling E2(qok→ch) to ~2.32.

**Corrected values (from exp_248 clean computation):**
- exp_247 reported: Sim_2nd = 0.320 (WRONG due to bug)
- Corrected: Sim_2nd = 1.367 (from N=10 clean baseline simulation)
- VMS_2nd = 1.483 (CORRECT — VMS computation was not affected by the bug)
- Corrected gap: VMS 1.483 vs Sim 1.367 — modest gap, not dramatic

**All exp_247 Sim_2nd values for KEY_TRIGRAMS are affected.** The VMS_2nd values are correct.

## Part 1: ch→X Binary MID Bigrams

Full ch→X enrichment matrix (B-dialect, MID-only):
- ch→qok: E2=1.147, N=331 — ch IS enriched toward qok (simulation baseline: 0.989)
- ch→r: E2=1.553 (N=39), ch→t: E2=1.482 (N=47), ch→k: E2=1.443 (N=71) — also enriched
- ch→sh: E2=0.569, N=122 — strongly depleted (sh is rare after ch)
- ch→ch: E2=0.943, N=339 — self-succession depleted (ch→ch < 1.0 in VMS MID)
- ch→o: E2=0.655, N=54 — depleted
- ch→ot: E2=0.920, N=135 — depleted

**KEY: ch→qok E2=1.147** is a real feature of VMS (simulation baseline: 0.989). This is a structural gap — the simulation under-produces ch→qok by ~16%.

**What precedes ch?** qok→ch is strongest (E2=1.234, the known Markov rule). Other enrichments: r→ch (1.473), k→ch (1.138), ok→ch (1.132). sh→ch: E2=0.555 — strongly depleted.

## Part 2: Section Distribution

Section map bug: all VMS B-dialect lines were assigned to "other" section (folio numbering format didn't match the section classifier). Section analysis inconclusive for this experiment. 

**Global result**: 69 qok→ch→qok trigrams, 356 qok→ch bigrams. Return rate = 69/356 = 0.194 vs expected qok MID rate = 0.142. Return enrichment = 1.366× — moderate and consistent with ch→qok E2=1.147.

## Part 3: Lexical Analysis

qok→ch→qok word triples: 69 total, **67 unique**. HHI/null=1.03× — NEAR-RANDOM. The pattern is maximally spread across word triples — purely a grammatical onset probability pattern, not lexical co-clustering.

ch→qok binary pairs: 331 total, 206 unique. HHI/null=2.72×, top-5=19.9%. Moderate concentration driven by chedy→qokXXX pairs (chedy is the most common ch-word). Top pair: chedy→qokeey (5.4%), chedy→qokain (4.5%).

## Part 4: p_chqok Simulation Sweep

| p_chqok | ch→qok E2 | qok→ch E2 | qok→ch→qok E3 | E3_pred | 2nd_ord | qok→qok E2 |
|---------|-----------|-----------|----------------|---------|---------|-----------|
| 0.00    | 0.989     | 1.162     | 1.572          | 1.150   | 1.367   | 1.335     |
| 0.05    | 1.073     | 1.165     | 1.652          | 1.251   | 1.321   | 1.240     |
| 0.10    | 1.194     | 1.196     | 1.797          | 1.428   | 1.258   | 1.191     |
| 0.15    | 1.303     | 1.223     | 1.934          | 1.594   | 1.213   | 1.187     |
| 0.20    | 1.399     | 1.213     | 2.000          | 1.696   | 1.179   | 1.150     |

VMS reference: ch→qok=1.147, qok→ch=1.234, qok→ch→qok 2nd_ord=1.483, qok→qok=1.169

**Best match for ch→qok E2:** p_chqok≈0.10 (sim=1.194 vs VMS=1.147 — slight overshoot; ~0.08 would be optimal).

**Effect on qok→ch:** p_chqok=0.10 gives qok→ch=1.196 vs VMS=1.234 — slight improvement (current battery: ~97% of target, still passing).

**Effect on qok→qok:** p_chqok=0.10 reduces qok→qok from 1.335 to 1.191, approaching VMS=1.169. This is an IMPROVEMENT — the baseline over-produces qok→qok self-succession in MID.

**2nd_order:** Adding p_chqok reduces 2nd_order from 1.367 toward ~1.18. This moves AWAY from VMS=1.483. The second-order structure is not fixed by this approach — VMS has genuine 2nd_order enrichment in qok→ch→qok that a ch→qok binary Markov rule cannot reproduce.

## Interpretation

**H453 REVISED — original premise was based on a bug:**

The exp_247 Sim_2nd=0.320 for qok→ch→qok was computed with a key-collision bug. The corrected value (exp_248 clean computation) is Sim_2nd=1.367, reducing the VMS-sim gap from 1.163 (dramatic) to 0.116 (modest). H453's premise of a "dramatic gap requiring explanation" is incorrect.

**What remains real:**
1. ch→qok E2=1.147 in VMS vs sim 0.989 — a genuine 16% enrichment gap. ch has a mild positive bias toward qok-onset words in VMS.
2. qok→ch→qok 2nd_order: VMS=1.483 vs Sim=1.367 — modest gap. With N=69, this is 1-2 standard errors above the simulation baseline — real but not strongly significant.
3. Adding p_chqok≈0.08-0.10 would match ch→qok E2, improve qok→ch slightly, and improve qok→qok (moving it toward VMS=1.169 from over-produced 1.335). No obvious regression risk from the bigram metrics alone.

**Architecture decision:** p_chqok≈0.08-0.10 is a viable new Markov parameter. It is the "return" complement of qok→ch (p_qokch=0.12). However, adding it requires a full 19-metric battery test (H454).

## Limitations

- Section distribution analysis failed due to folio-number format mismatch
- Sim_2nd at p_chqok=0.10 is 1.258 — further from VMS=1.483 than baseline (1.367). The qok→ch→qok second-order structure is not reproduced by this mechanism
- qok→qok improvement is in MID bigrams only; global battery metrics may differ

## Self-Audit

**Target-awareness**: No target-aware elements. p_chqok sweep is novel parameter space. Bug correction is a computation fix, not a calibration.

**Feature-destroying implementation**: No feature-destroying details. The p_chqok rule correctly biases post-ch selection toward qok-onset words; this tests the feature being investigated.

**Extrapolation**: "H453 REVISED" does not overclaim. The bug discovery is supported by specific evidence: key accumulation trace shows 2-3× inflation of E3_pred in exp_247. The corrected simulation value (1.367) from exp_248's clean independent computation serves as verification.

**Negative-result scope**: The original H453 premise (dramatic 1.483 vs 0.320 gap) was based on a bug. The real gap (1.483 vs 1.367) is modest and does not require a new mechanism. The ch→qok E2 gap (1.147 vs 0.989) is real and suggests a viable new parameter (H454).

**Control behavior**: Baseline simulation (p_chqok=0.00) ch→qok E2=0.989 — expected to be ~1.0 since no rule biases post-ch selection toward qok. Actual: 0.989 ≈ 1.0 ✓. Adding p_chqok increases ch→qok monotonically as expected. qok→qok decreases as p_chqok increases — expected since after ch draws a qok word, the buffer qok concentration remains roughly the same, but the mechanism redirects some ch-following words to qok rather than buffer-random.

## Conclusion

exp_247 had a simulation bug inflating E3_pred for KEY_TRIGRAMS with shared (x,y) prefixes. Corrected: qok→ch→qok Sim_2nd=1.367 (not 0.320). VMS Sim_2nd=1.483 — modest gap of ~0.12. H453's dramatic-gap premise is invalidated.

Real finding: ch→qok E2=1.147 in VMS vs 0.989 in sim — a genuine 16% enrichment. Adding p_chqok≈0.08-0.10 would match this, improve qok→ch and qok→qok simultaneously. Full battery test needed (H454).

F247 requires correction in findings.md for all Sim_2nd values.
