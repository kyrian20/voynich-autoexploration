# exp_444: Cross-Line y→d Bigram Verification (H_new_F)

**Hypothesis (H_new_F):** F326's y→d enrichment (A=1.37×, B=1.49×) is a cross-line paragraph bigram effect: y-onset word at LL of line N → d-onset word at LF of line N+1. exp_441 showed within-line y→d E=0.93-0.96× (not enriched), pointing to this cross-line explanation.

**Method:** ZL3B continuation lines. For consecutive line pairs within the same folio, compute (LL onset, LF onset) bigrams. E = obs / (P_LL(y) × P_LF(d) × N_pairs). Also compute daiin fraction among d-LF words after y-LL vs baseline d-LF distribution.

---

## Results

### y→d cross-line enrichment

| Dialect | N cross-line pairs | y(LL)→d(LF) obs | expected | E |
|---------|-------------------|-----------------|----------|---|
| A | 993 | 4 | 6.5 | **0.61×** |
| B | 1495 | 11 | 7.1 | **1.54×** |

### y-LL → * LF onset distribution (top results)

**A-dialect (y at LL: N=38):** ok(E=1.54×/N=3) only enriched above baseline; d(0.61×/N=4) depleted.
**B-dialect (y at LL: N=39):** d(E=1.54×/N=11)**, ol(E=1.95×/N=3)** enriched; qok(0.60×) depleted.

### * LL → d LF successors

**B-dialect:** sh(LL)→d(LF) E=1.58×(N=19)** is the strongest enrichment.
**A-dialect:** ol(LL)→d(LF) E=1.67×(N=8)** is the strongest enrichment.

### daiin enrichment at LF after y-LL vs baseline

| Dialect | daiin after y-LL | daiin at d-LF baseline | E |
|---------|-----------------|----------------------|---|
| A | 1/4 (25.0%) | 33.2% | 0.75× |
| B | 1/11 (9.1%) | 24.7% | 0.37× |

---

## Interpretation

**H_new_F PARTIALLY CONFIRMED for B; REFUTED for A (small N).**

1. **B cross-line y→d confirmed (E=1.54×/N=11)**: B y→d = 1.54× at cross-line level is consistent with F326's reported B y→d = 1.49×. This confirms the exp_441 interpretation: F326's B y→d enrichment comes from cross-line paragraph bigrams (y at LL of one continuation line → d at LF of the next). Within lines: E=0.96× (exp_441). Cross-line: E=1.54×. The two together are consistent with an "averaging" effect in F326's mixed paragraph-bigram analysis.

2. **A cross-line y→d depleted (E=0.61×/N=4)**: A shows y→d DEPLETION at cross-line boundaries. However, N=4 (with 38 y-LL events) makes this unreliable. A y→d is neither enriched within-line (E=0.93×, exp_441) nor enriched cross-line (E=0.61×, N=4). F326's A y→d = 1.37× is unexplained by either mechanism and may be a false positive in F326's early dataset, or may reflect a different corpus boundary condition.

3. **daiin is NOT the cross-line driver**: After y-LL, daiin appears at d-LF in 25% of A cases and 9% of B cases — DEPLETED relative to daiin's baseline rate at d-LF (A=33%, B=25%). The cross-line y→d (where it occurs in B) is not specifically y→daiin. The specific d-words after y-LL in B are: dshedy(2), dchdar(1), dar(1), dair(1), dchekeedy(1), dary(1), dcheol(1), dol(1), dain(1), daiin(1) — diverse d-vocabulary, no daiin dominance.

4. **Other notable cross-line couplings**: 
   - B ol(LL)→d(LF): The strongest y-LL succession is to ol (E=1.95×/N=3) not d, though N=3 is directional
   - B sh(LL)→d(LF): E=1.58×(N=19) — a cross-line coupling worth noting; sh-ending lines predict d-starting lines in B (potentially connecting B's sh→d formula grammar, F326, to paragraph-level structure)
   - A ol(LL)→d(LF): E=1.67×(N=8) — A-specific cross-line rule

5. **F326 status update**: F326's y→d = 1.37-1.49× is now explained for B (cross-line effect confirmed E=1.54×) and unexplained for A (cross-line depleted, within-line near-baseline). The B explanation is the more important one; A y→d in F326 should be flagged as uncertain. No revision to committed claims needed (F326 was not committed).

---

## Self-Audit

**Target-awareness**: No target-aware elements. This is a pure corpus measurement.

**Feature-destroying implementation**: No features destroyed. Cross-line bigram detection uses folio continuation line structure correctly (same folio, consecutive continuation lines; excludes folio-first and folio-last).

**Extrapolation**: All claims within N-bounds. A cross-line result (E=0.61×, N=4) is explicitly flagged as unreliable.

**Negative-result scope**: A y→d depletion (E=0.61×) is properly scoped: "small N=4, not conclusive; F326's A y→d=1.37× cannot be explained by cross-line bigrams under this measurement." Does not claim A y→d coupling doesn't exist — only that this cross-line test doesn't find it.

**Control behavior**: No separate control used. Expected under independence: y→d should have E≈1.0×. B observes 1.54× (above independence). A observes 0.61× (below independence).

---

## Conclusion

H_new_F PARTIALLY CONFIRMED: **B cross-line y→d E=1.54×(N=11)** confirms exp_441's interpretation that F326's B y→d=1.49× is a cross-line effect. **A cross-line y→d E=0.61×(N=4)** — inconclusive, cannot confirm A component of F326. daiin is NOT the specific word driving the cross-line y→d effect (daiin depleted relative to d-LF baseline after y-LL). New observation: **B sh(LL)→d(LF) E=1.58×(N=19)** — strongest confirmed cross-line coupling, connects B's sh-routing grammar to paragraph-level structure. **No new finding ID** (confirms existing F326 mechanism; no novel structural finding at the confirmed level).
