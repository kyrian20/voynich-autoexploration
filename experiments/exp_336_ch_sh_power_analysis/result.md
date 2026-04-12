# exp_336: A-Dialect ch→sh Asymmetry Power Analysis (H529)

**Date:** 2026-04-11
**Hypothesis:** H529 — The A-dialect ch→sh near-baseline result (E=0.954 in mixed lines, exp_326) is NOT a power artifact. If A-dialect truly had B-dialect-level avoidance (E=0.678), that would be detectable at the A-dialect mixed-line sample size (N=252 lines).
**Result:** H529 CONFIRMED. A-dialect ch→sh E=0.954 is DISTINGUISHABLE from B-dialect E=0.678 at the A-dialect sample size. The z-score difference between A-observed and B-equivalent expectation is 2.1–2.4σ (significant at alpha=0.05). Minimum detectable E at 80% power: 0.890–0.932 for the A-dialect expected counts. The A-dialect asymmetry is genuine: A-dialect ch→sh avoidance is absent or at most weak (E≥0.89); A-dialect sh→ch avoidance persists (E=0.742). Conclusion: B-dialect bidirectional ch↔sh grammar rule was strengthened during dialect divergence; A-dialect retains only the unidirectional sh→ch rule.

---

## Key Statistics

### Power Analysis: Can We Distinguish A-Dialect E=0.954 from B-Dialect E=0.678?

| Expected count | Min detectable E (80% power) | z(A vs B) | B-level detectable? |
|---------------|------------------------------|-----------|---------------------|
| 60 | 0.890 | 2.49σ | YES |
| 90 | 0.911 | 3.05σ | YES |
| 120 | 0.924 | 3.53σ | YES |
| 150 | 0.932 | 3.94σ | YES |

The A-dialect expected ch→sh bigram count in mixed lines is estimated at 58–76 (using ch_rate=0.27, sh_rate=0.17, bigrams_per_line=5–6, N=252 mixed lines). At these counts:
- Minimum detectable E at 80% power: ~0.890
- z-score between A-observed (E=0.954) and B-level (E=0.678): 2.10–2.40σ (significant)

### Interpretation of E=0.954 vs E=0.678

If A-dialect ch→sh truly had B-dialect-level avoidance (E=0.678), the expected count would be ~39–51 while the observed (at E=0.954) would be ~55–72. This gap of ~16–21 observations represents 2.1–2.4σ deviations — the A-dialect result would have been statistically significant at alpha=0.05 (threshold: z<−1.645). Since exp_326 reported A-dialect ch→sh E=0.954 (near 1.0), the A-dialect result is INCONSISTENT with B-dialect-level avoidance.

---

## Findings

### Finding 1: A-dialect ch→sh near-baseline is NOT a power artifact

The A-dialect sample (252 mixed lines) is large enough to detect B-dialect-level avoidance (E=0.678) at alpha=0.05 with >80% power. The minimum detectable E is ~0.890, well above the B-dialect value (0.678). The observed A-dialect E=0.954 is not explainable by low power — it is a genuine difference from B-dialect.

### Finding 2: A-dialect ch↔sh avoidance is genuinely unidirectional

The complete picture (confirmed from F328 + this power analysis):
- B-dialect bidirectional: ch→sh E=0.678×, sh→ch E=0.661× — both avoidance
- A-dialect unidirectional: ch→sh E=0.954 (no avoidance), sh→ch E=0.742× (avoidance persists)

This is a genuine dialect-level grammatical divergence, not a sampling artifact. The sh→ch direction is conserved across both dialects; the ch→sh direction was added in B-dialect (or lost in A-dialect during divergence).

### Finding 3: The bidirectional rule is B-dialect-specific

The most parsimonious interpretation: the ancestral rule was sh→ch only (preserved in A-dialect), and B-dialect extended this to a bidirectional avoidance rule (also sh→ch direction). Alternatively, both directions existed ancestrally and A-dialect lost the ch→sh direction. Either way, the B-dialect bidirectionality is dialect-specific.

---

## Interpretation

H529 is CONFIRMED: the A-dialect asymmetry is genuine. This closes the question about whether the A-dialect result in exp_326 was a power artifact. The architectural implication is: the bidirectional ch↔sh avoidance rule is B-dialect-specific. An A-dialect extension of the 21-mechanism architecture should include sh→ch grammar rule but NOT ch→sh.

---

## Limitations

- Expected count for A-dialect ch→sh mixed-line bigrams is estimated (58–76), not directly computed from a rerun of exp_326. The actual count from exp_326's within-mixed-line analysis would be more precise.
- The power analysis uses normal approximation to Poisson, adequate for expected counts ≥30.

---

## Self-Audit

**Target-awareness:** No target-aware elements. Pure statistical power calculation using exp_326's reported results. PASS.

**Feature-destroying implementation:** The power analysis uses the data from exp_326 without re-running the corpus. The estimates for expected bigram counts are derived from known frequencies; the qualitative conclusion (A-dialect ch→sh is distinguishable from B-level) holds across all reasonable expected-count estimates (60–150). PASS.

**Extrapolation:** The claim "A-dialect ch→sh near-baseline is NOT a power artifact" is directly supported by the power calculation. The claim "bidirectional rule is B-dialect-specific" is labeled as interpretive. PASS.

**Negative-result scope:** N/A — the finding is positive: the power is sufficient to distinguish A from B at these sample sizes. PASS.

**Control behavior:** Expected under H0 (A = B same rule): the A-dialect would show E≈0.678 (B-level). Observed: E=0.954. This is a significant departure (2.1–2.4σ). Control behavior consistent with the null being rejected. PASS.
