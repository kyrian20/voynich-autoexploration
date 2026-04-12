# exp_241: H442 — Onset Bigram Structure: Completeness Analysis

**Hypothesis**: H442 — qok→ch (B) and y→y (A) are the only onset-succession pairs needing explicit Markov rules; the copy buffer naturally captures all other significant bigram pairs within ±20%.

**Status**: H442 PARTIALLY ANSWERED — **Markov rules correctly captured (qok→ch, y→y); but model has significant cross-onset grammar gaps not in the 19-metric battery**. Self-succession pairs with high VMS enrichment (ot→ot, l→l, etc.) are also under-reproduced. Model is battery-complete (19/19) but NOT full-bigram-matrix-complete.

---

## Setup

Full onset bigram enrichment matrix computed for A and B dialects.
Enrichment E(X→Y) = P(X,Y) / (P(X) × P(Y)) — deviation from independence.
Threshold: onset rate ≥ 1%, |E - 1| > 20%.

Simulation: N=10 per dialect (exp_236 B params, exp_239 A params), full-length runs.
Classification: CAPTURED (sim E within ±20% of VMS E), OVERCAPTURED (sim > VMS by >20%), MISSED (sim below VMS by >20%).

---

## Key Bigram Enrichments

### Known Markov Rules — VMS Values

| Rule | Dialect | VMS E | Sim E | Ratio | Captured? |
|------|---------|-------|-------|-------|-----------|
| qok→ch | B | 1.267 | 1.234 | 97.4% | CAPTURED |
| y→y | A | 1.587 | 1.609 | 101.4% | CAPTURED |
| qok→ch | A | 1.220 | 1.278 | 104.8% | CAPTURED |
| y→y | B | 1.955 | 1.700 | 87.0% | CAPTURED (close to 80% threshold) |

The two Markov rules in the model are correctly reproduced. Notably, y→y is enriched in B-dialect VMS (1.955×) but the model captures it with E=1.700 via natural copy buffer dynamics without p_y_y — consistent with the observation that B-dialect doesn't need p_y_y=0 (it passes ss_y without it).

### Top Missed Pairs (VMS-enriched, simulation misses)

**B-dialect top misses (cross-onset):**
| Pair | VMS E | Sim E | Note |
|------|-------|-------|------|
| p→o | 2.680 | 1.000 | p-onset followed by o-onset; p is rare (1.8%) |
| sh→qok | 1.905 | 0.969 | sh→qok; largest missed cross-onset |
| s→sh | 1.915 | 1.032 | s→sh |
| p→sh | 2.055 | 1.050 | |
| ot→ot | 1.886 | 1.287 | Self-succession missed |
| l→l | 1.949 | 1.575 | Self-succession missed |

**A-dialect top misses (cross-onset):**
| Pair | VMS E | Sim E | Note |
|------|-------|-------|------|
| p→sh | 2.522 | 1.006 | Both dialects show p→sh enrichment |
| o→o | 2.161 | 1.415 | Self-succession missed |
| sh→qo | 1.803 | 1.009 | |
| ot→ot | 1.862 | 1.244 | Self-succession missed |

### Quantitative Summary

| Dialect | Significant VMS pairs | Captured | Overcaptured | Missed |
|---------|-----------------------|----------|--------------|--------|
| B | 137 | 27 (20%) | 71 (52%) | 39 (28%) |
| A | 134 | 25 (19%) | 65 (49%) | 42 (31%) |

---

## Interpretation

**H442 finding: The model is battery-complete (19/19) but NOT full-bigram-matrix-complete.**

The completeness question has two answers:
1. **For the 19-metric battery**: COMPLETE. qok→ch and y→y are correctly captured; ss_mean (qok/ok/ch), ss_d, ss_y are measured and pass; qok_ch is measured and passes.
2. **For the full onset bigram matrix**: INCOMPLETE. The model misses ~28-31% of significantly enriched VMS bigram pairs.

**Root cause of missed pairs**:

(a) **Cross-onset grammar misses (sh→qok, p→sh, s→sh)**: The copy buffer propagates onset structure through self-succession (same-onset redraws from buffer) but does NOT encode cross-onset grammar. The VMS sh-onset word class appears to preferentially precede qok-onset words in B-dialect — a grammatical successor rule not modeled. Similarly p→sh, s→sh suggest onset-class successor preferences not captured by the copy buffer.

(b) **Self-succession misses (ot→ot, l→l, o→o)**: The copy buffer produces enriched self-succession for high-rate onset classes (qok, ok, ch, d) but under-reproduces it for moderate-rate classes. At E(ot→ot)=1.886 vs sim 1.287, the buffer is not achieving sufficient ot-onset resampling. This suggests the copy buffer's self-succession mechanism is onset-rate-dependent in a way the simulation captures only imperfectly.

(c) **Overcaptured pairs**: The model produces enrichment for many pairs the VMS doesn't have (71/137 overcaptured in B). This suggests the copy buffer creates a general smooth background of moderate succession enrichment across all onset pairs, while VMS has a sparser, more concentrated grammar (strong enrichment for specific pairs, strong depletion for others).

**The 19-metric battery is incomplete as a validation set**: The battery tests 5 self-succession metrics (ss_mean covering qok/ok/ch, ss_d, ss_y) and 1 cross-succession metric (qok_ch). It does not test: sh→qok, p→sh, s→sh, l→l, ot→ot, o→o, and many other VMS-elevated pairs. The model's 19/19 PASS is valid for those 19 metrics but does not imply full bigram structural match.

**Assessment of "additional Markov rules needed"**: 

The top missed cross-onset pairs in BOTH dialects are:
- p→sh (B: 2.055, A: 2.522 — strong cross-dialect enrichment)
- sh→qok (B: 1.905 — B-specific)
- s→sh (B: 1.915)

If these represent genuine grammatical rules, they would require p_X→Y Markov parameters. The p→sh enrichment is present in BOTH dialects at similar magnitude, suggesting it is a corpus-level property rather than noise. However, adding these rules would increase target-calibrated parameters and is not motivated by 19-metric battery failures.

---

## Limitations

1. **Low-count pairs are noisy**: Several highly "enriched" pairs (p→o: count=38, l→r: count=26) have small absolute counts; E estimates are unstable at these counts.
2. **N=10 simulation**: Simulation E estimates are based on N=10 simulations. Higher N would give more stable estimates.
3. **"Overcaptured" interpretation**: OVERCAPTURED doesn't mean the model fails — it means the simulation has higher bigram enrichment than VMS for those pairs. These don't affect the 19-metric battery.
4. **Onset class "other"**: The "other" category contains words not matching any onset class (5-6% of words). The strong other→other enrichment (2.261 in B, 1.997 in A) may be an artifact of rare words clustering in specific positions.

---

## Self-Audit

**Target-awareness**: No target-calibrated parameters in this experiment. Pure corpus and simulation analysis. The simulation uses exp_236/exp_239 frozen parameters.

**Feature-destroying implementation**: The bigram analysis uses global word sequence (not separated by line position). This is the standard approach but note: LF words precede MID words, creating spurious cross-position bigrams. The VMS bigram enrichments include LF→MID and MID→LL transitions, not just MID→MID. This is a limitation: the grammar rules may be position-specific (within-MID succession only) but the analysis collapses all positions.

**Extrapolation**: The claim "model is battery-complete but not bigram-matrix-complete" is supported by the direct comparison. The claim "cross-onset grammar misses suggest additional Markov rules are needed" is within the tested scope. No structural claims beyond the tested grid.

**Negative-result scope**: The model's incomplete bigram coverage does not mean it is incorrect as a structural description — it means the 19-metric battery is an incomplete test. The specific missed pairs (sh→qok, p→sh, s→sh) may or may not reflect genuine grammatical structure vs. positional confounds.

**Control behavior**: No separate control. Expected: copy buffer should produce moderate self-succession enrichment for all onset classes (and this is observed for qok, ok, ch, d which are in the battery). The unexpected finding is that self-succession for ot, l, o is under-reproduced. This suggests the copy buffer's self-succession mechanism is more effective for the high-rate onset classes the buffer is explicitly trained to enrich via the onset preservation rule.

---

## New Hypotheses Generated

**H443**: Cross-dialect p→sh enrichment (B: 2.055, A: 2.522) is a consistent bigram grammar rule not modeled. Does adding a p_p→sh parameter to draw_buf (analogous to qok→ch) reproduce this pattern without regressing the 19-metric battery?

**H444**: Self-succession under-reproduction for ot/l/o. Is the copy buffer's self-succession mechanism onset-rate-dependent? Does the buffer equilibrium produce less ot→ot enrichment because ot-onset words are more heavily modified (losing onset — but onset is preserved!). Diagnostic: compare buffer composition ot-onset rate vs MID ot-rate vs global ot-rate in simulation output.

**H445**: Position-confounded bigram analysis. The current analysis uses global word sequence (mixing LF→MID and MID→LL transitions). Is sh→qok enrichment driven by LL-position qok words being preceded by MID sh words (a cross-position grammar rule), or is it genuine within-MID succession? Run position-filtered bigram analysis (MID→MID only).

---

## Conclusion

H442 PARTIALLY ANSWERED — the model is battery-complete but not full-bigram-matrix-complete.

**Key facts**:
1. Known Markov rules (qok→ch, y→y) are correctly captured
2. 28-31% of significantly enriched VMS bigram pairs are missed by the simulation
3. Top missed patterns: sh→qok (B), p→sh (both dialects), s→sh (B), ot→ot and l→l self-succession (both)
4. The 19-metric battery does not cover these missed pairs — the 19/19 PASS result is valid but incomplete
5. Cross-dialect p→sh enrichment (present in both at similar magnitude) is the most candidate for a genuine third Markov rule
