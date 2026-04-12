# exp_274: s→s Anti-Self-Succession Analysis

**Hypothesis**: H475 — VMS s→s depletion (VMS=0.887, sim 5-8× over-production) is a genuine grammatical rule requiring an anti-Markov mechanism.

**Date**: 2026-04-11

---

## Results

### Section 1: Global E2(s→s) — PREMISE INVALIDATED

| Dialect | E2(s→s) | N_pairs | s-onset rate | Status |
|---------|---------|---------|-------------|--------|
| A | **2.093** | 17 | 2.9% | ENRICHED |
| B | **1.187** | 13 | 2.4% | ENRICHED |

**H475 PREMISE INVALIDATED**: VMS s→s is NOT depleted. Both dialects show s→s ≥ 1.0 (enriched, not depleted). The claim in H475 and F261 that "VMS s→s = 0.887 (depleted)" is incorrect. The simulation "over-production" relative to 0.887 was a false comparison.

### Section 2: MID-Only E2(s→s)

| Dialect | E2_mid(s→s) | N_mid_pairs | Interpretation |
|---------|------------|------------|----------------|
| A | 0.887 | 1 | Near-zero — N=1, statistically meaningless |
| B | 0.000 | 0 | No MID s→s pairs in entire B-dialect corpus |

MID-only s→s is essentially zero — but this is due to extreme rarity (s-onset is only 2-3% of words; MID s→s pairs expected ≈ 5-6 in A-dialect under independence; only 1 observed). This is not grammatical depletion; it is a small-N sampling artifact. B-dialect MID shows zero s→s pairs out of a corpus of 13,849 MID words (s rate ~2% → expected ~5.4 pairs under independence).

**CRITICAL NOTE**: The F261 finding "VMS s→s = 0.887" almost certainly refers to the MID-only E2 for A-dialect (0.887, N=1), not the global E2 (2.09). F261 was an A-dialect experiment; the MID-only computation would match the VMS target used for the sim comparison. The F261 VMS target was MID-only, not global — making the sim comparison (which used global bigrams) methodologically inconsistent.

### Section 3: Section-Stratified E2(s→s)

**A-dialect:**
- Herbal: E2=1.61 (N=5), cosmo: E2=1.54 (N=5) — enriched in both

**B-dialect:**
- Bio: E2=0.66 (N=4), cosmo: E2=1.86 (N=6), recipes: E2=0.74 (N=2)
- Mixed — some sections depleted, some enriched (small N throughout)

No consistent s→s depletion across sections. N values (2-6 per section) are far too small for reliable conclusions.

### Section 4: Lag Analysis (s→s at lag 1, 2, 3)

| Dialect | Lag-1 P(s\|prev=s) | Base P(s) | Enrichment | Lag-2 enr. | Lag-3 enr. |
|---------|-----------|----------|-----------|----------|----------|
| A | 6.07% | 2.90% | **2.09×** | 1.48× | 1.23× |
| B | 2.88% | 2.42% | **1.19×** | 0.91× | 1.00× |

A-dialect s→s persists modestly at lag-2 and lag-3 (monotone decay). B-dialect shows near-baseline at lag-2+. Neither shows depletion (E<1) at any lag.

### Section 5: HHI/null for s→s Word Pairs

| Dialect | N_pairs | HHI/null | Top-5 coverage | Classification |
|---------|---------|----------|---------------|----------------|
| A | 17 | 10.3 | 29% | (Small-N artifact) |
| B | 13 | 6.8 | 39% | (Small-N artifact) |

HHI/null >> 1 is a small-N artifact: with only 17 s→s pairs drawn from 280 s-onset words, even random sampling would produce high HHI/null. The pairs are all unique (each appears once) — HHI_null is very small because s-onset words are rare, inflating the ratio. The LEXICAL classification is not meaningful at N=17.

### Section 6: What Follows s-Onset?

**B-dialect s→X cross-onset enrichment (notable):**
- s→sh: E=1.915 (ENRICHED, N=79)
- s→ol: E=1.721 (ENRICHED, N=41)
- s→other: E=1.701 (ENRICHED, N=44)
- s→qok: E=0.691 (depleted, N=40)
- s→d: E=0.727 (depleted, N=22)

B-dialect: s→sh is strongly enriched (E=1.9). Given that sh→qok is also enriched (E_mid~1.97 from exp_242), this suggests a potential s→sh→qok chain in B-dialect. Cross-onset enrichment more interesting than same-onset.

**A-dialect s→X:**
- s→ch: E=1.20, s→sh: E=1.20, s→s: E=2.09 (self-enriched)
- No strong cross-onset patterns

### Comparison: E2 for All Single-Char Onsets

**A-dialect:**
| Onset | E2 | N | Rate | Status |
|-------|-----|---|------|--------|
| s | 2.09 | 17 | 2.9% | enriched |
| l | 7.14 | 2 | 0.5% | enriched (N too small) |
| p | 0.71 | 1 | 1.2% | depleted (N too small) |
| f | 0.00 | 0 | 0.3% | N=0 |
| k | 1.01 | 13 | 3.6% | near-baseline |
| t | 0.78 | 7 | 3.0% | borderline |
| r | 0.00 | 0 | 0.2% | N=0 |

**B-dialect:**
| Onset | E2 | N | Rate | Status |
|-------|-----|---|------|--------|
| s | 1.19 | 13 | 2.4% | enriched |
| l | 1.95 | 110 | 5.5% | enriched |
| p | 0.50 | 3 | 1.8% | depleted (N too small) |
| f | 0.00 | 0 | 0.3% | N=0 |
| k | 1.12 | 11 | 2.3% | near-baseline |
| t | 1.03 | 12 | 2.5% | near-baseline |
| r | 1.35 | 5 | 1.4% | enriched (N too small) |

Only p and f show E2 < 1 with non-zero N, but N values are 0-3 — too small for any conclusion.

---

## Interpretation

**H475 is invalidated before testing any mechanism.**

VMS s→s = 2.09 (A-dialect) and 1.19 (B-dialect) — both ≥ 1. The simulation doesn't over-produce s→s relative to the actual VMS value; it may over-produce it (sim gives 4-7× while VMS gives 2.09), but the comparison is much less dramatic (2-3.5× over-production vs claimed 5-8×). The gap may be partly explainable by buffer dynamics (s-onset words in the buffer self-succeed at the buffer cycling rate, which is captured in the ss_mean metric).

**F261 discrepancy**: The "VMS s→s = 0.887" in F261/H475 was very likely the MID-only E2 for A-dialect (0.887, N=1) compared to a global-level simulation bigram. This is an apples-to-oranges comparison. The correct comparison is global vs global (2.09 vs 4-7×) or MID vs MID (N=1 vs much higher simulation MID pairs). Since N=1 for MID, neither comparison is meaningful.

**New secondary finding**: B-dialect s→sh is enriched (E=1.9, N=79). This is large enough to be meaningful. Combined with the known sh→qok enrichment (E_mid=1.97 from exp_242), this suggests a B-dialect s→sh→qok chain pattern. This is worth examining.

**Anti-mechanism conclusion**: No anti-s→s Markov mechanism is warranted. The simulation's s→s production should be compared to VMS 2.09 (A) and 1.19 (B), not 0.887.

---

## Limitations

1. N values for s→s pairs are very small (17 A-dialect, 13 B-dialect), making all conclusions tentative.
2. Section-level analysis suffers from even smaller N (2-6 per section per dialect).
3. The F261 discrepancy cannot be definitively resolved without re-running exp_261's VMS computation — adding to open_questions.
4. The s→sh enrichment finding (B-dialect, N=79) is more reliable but not further pursued here.

---

## Self-Audit

**Target-awareness**: Not applicable — this is a pure corpus measurement. No simulation parameters were calibrated to s→s targets. The VMS measurements are direct corpus computations.

**Feature-destroying implementation**: Not applicable — no mechanism was tested.

**Extrapolation**: The claim "F261 VMS s→s = 0.887 is incorrect" is supported by the direct measurement of 2.09 and an explanatory hypothesis (MID-only vs global computation mismatch). This is not an extrapolation — it is a direct finding discrepancy flagged for investigation.

**Negative-result scope**: H475 was testing whether s→s depletion requires an anti-Markov mechanism. The finding that s→s is NOT depleted (VMS E2 > 1) means the hypothesis premise is false. Conclusion: no anti-s→s mechanism needed. This is not an overreach — it follows directly from the measurement.

**Control behavior**: Section-level variation serves as a check. A-dialect shows consistent s→s enrichment across herbal and cosmo (the two sections with sufficient N). B-dialect shows mixed results (bio and recipes slightly depleted, cosmo enriched) — consistent with noise at N=2-6.

---

## Conclusion

**H475 PREMISE INVALIDATED**: VMS s→s is enriched, not depleted. A-dialect E2=2.09 (N=17), B-dialect E2=1.19 (N=13). The F261 VMS s→s = 0.887 appears to be a MID-only computation (N=1, statistically meaningless) mistakenly compared against global simulation bigrams. No anti-s→s mechanism is warranted. The sim over-produces s→s by 2-3× relative to the actual VMS target (not 5-8× as claimed). Secondary finding: B-dialect s→sh enrichment (E=1.9, N=79) is a more meaningful finding worth follow-up as part of the sh→qok chain investigation.
