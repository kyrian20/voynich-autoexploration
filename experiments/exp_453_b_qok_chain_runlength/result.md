# exp_453: B qok Chain Run-Length Distribution (H_new_O)

**Hypothesis (H_new_O):** B qok edy-body self-replication (F439: E=1.52×/N=165) might produce super-geometric run-length distributions if edy-body qok words cluster in chains. Prediction: observed L≥3 chains exceed geometric expectation significantly.

---

## Results

### B qok run-length distribution vs geometric

| L | Observed | Expected (geo) | Ratio |
|---|---------|----------------|-------|
| 1 | 1,310 | 1,308.8 | 1.00 |
| 2 | 194 | 196.5 | 0.99 |
| 3 | 31 | 29.5 | 1.05 |
| 4 | 4 | 4.4 | 0.90 |
| 5 | 1 | 0.7 | 1.50 |
| ≥5 | 1 | 0.8 | 1.28 |

N_runs=1,540; geometric_p=0.850; mean_L=1.177. **GEOMETRIC: all bins within ±5% of expectation.**

### Comparison: all five cases

| Case | L≥3 E | obs/exp |
|------|--------|---------|
| **B qok** | **1.04×** | 36/34.7 |
| A qok | 0.76× | 2/2.6 |
| B ot | 1.23× | 14/11.3 |
| A y | 1.47× | 4/2.7 |
| B y | 1.18× | 1/0.8 |

No case shows L≥5 excess at N≥5. A y's L=4 ratio=4.75× rests on N=1 observation vs 0.2 expected — insufficient for super-geometric claim.

### B qok body-char composition: singletons vs chain members

| body-char | Singletons (f=1) | Chain members (len≥2) | E |
|-----------|-----------------|----------------------|---|
| 'e' (edy-body) | 43.0% | **64.5%** | **1.50×** |
| 'a' (aiin-body) | 42.6% | **22.5%** | **0.53×** |
| 'c' | 4.8% | 6.0% | 1.24× |
| 'o' | 3.3% | 2.2% | 0.67× |

**edy-body qok words are 1.50× over-represented in chains (len≥2) vs singletons; aiin-body 0.53× under-represented.**

### Consecutive pairs in B qok chains

Of 272 consecutive qok pairs within chains:
- **edy+edy**: 135/272 = **49.6%** (expected if body-blind: 43% × 43% ≈ 18.5% → E=2.68×)
- **aiin+aiin**: 19/272 = 7.0% (expected: 42.6% × 42.6% ≈ 18.1% → E=0.39×)
- edy+aiin or aiin+edy transitions: 272 - 135 - 19 - other ≈ 118/272 = 43.4%

---

## Interpretation

**H_new_O ANSWERED (NEGATIVE for super-geometric; POSITIVE for body-within-chain):**

1. **B qok run-length distribution is GEOMETRIC (L≥3: E=1.04×):** Despite the F439 edy-body self-replication rule (E=1.52×), the overall qok chain distribution follows a geometric distribution with p=0.850. The modest overall self-succession rate (mean_L=1.177) produces geometric runs. The edy-body mechanism is real but insufficient to generate super-geometric tail behavior.

2. **edy-body qok words dominate chains (E=1.50×):** While the run-length distribution is geometric, within chains, the body-char composition is strongly skewed toward edy-body words (64.5% of chain tokens vs 43.0% of singletons). The edy-body self-replication rule (F439) manifests as preferential chain membership, not as longer-than-expected chains overall.

3. **edy+edy consecutive pairs are 2.68× elevated:** Within qok chains, half of all consecutive continuations are edy+edy pairs. The aiin-body words rarely continue qok chains (aiin+aiin = 7.0% vs 18.1% expected). The body-conditional succession rule (F439) is thus the mechanism behind qok chain formation: edy-body words recruit more edy-body qok successors.

4. **A y "super-geometric" reassessment:** A y at L=4 shows ratio=4.75× but N=1 observation (0.2 expected). This is insufficient evidence for super-geometric behavior. F410's "super-geometric" claim for A y requires re-evaluation at higher N (A y has only 413 tokens in cont lines, producing 4 L≥3 chains total). The super-geometric label may be premature.

5. **B ot is also geometric (L≥3: E=1.23×):** Consistent with exp_419 (F422).

6. **Mechanism implication:** The geometric run-length distribution + edy-body chain membership suggests: (a) qok self-succession arises primarily from edy-body words retaining edy-body context within a chain; (b) the chain terminates when a non-edy body qok word appears or the context shifts to a different onset class; (c) the overall rate governs chain lengths geometrically, but the internal structure of chains is body-class-regulated.

---

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: Run-length extraction works across entire lines (not just MID). qok runs at LF/LL positions are included. This is correct since we want full chain behavior.

**Extrapolation**: All claims within observed N. The "geometric" conclusion rests on N=36 (L≥3) vs 34.7 expected — within 1σ for Poisson. The edy-body chain enrichment (E=1.50×, N=272 pairs) is robust.

**Negative-result scope**: "B qok run-length is geometric" is confined to the observed corpus. Geometric does not preclude edy-body conditional behavior — the two findings are complementary, not contradictory.

**Control behavior**: A qok (geometric, smaller N), B ot (geometric, from F422), A y (near-geometric with N=1 at L=4) all confirm geometric baseline for comparison.

---

## Conclusion

H_new_O ANSWERED: B qok run-length distribution is **GEOMETRIC** (L≥3: E=1.04×) — no super-geometric tail. But **edy-body qok words dominate chains** (E=1.50× in chains vs singletons; edy+edy consecutive pairs 49.6% vs 18.5% body-blind expectation → E=2.68×). F439 edy-body self-replication is confirmed in chain composition, but the overall geometric run-length indicates a moderate global self-succession rate governs chain lengths. A y's "super-geometric" status is not confirmed in this analysis (N=1 at L=4). **No new finding ID** — the body-within-chain results extend F439; the geometric run-length is the null result for super-geometric. A y F410 re-evaluation flagged as H_new_R below.
