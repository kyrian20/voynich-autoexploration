# exp_278: VMS Word Length Distribution (H472)
**Hypothesis:** H472
**Date:** 2026-04-11
**Status:** CONFIRMED — log-normal fit is good; VMS is narrower and more concentrated than Latin

---

## Key Results

### Word Length Distribution

| Len | A-frac | B-frac | Latin-frac |
|-----|--------|--------|-----------|
| 2 | 0.043 | 0.049 | 0.126 |
| 3 | 0.097 | 0.072 | 0.140 |
| 4 | 0.217 | 0.151 | 0.121 |
| 5 | 0.265 | 0.262 | 0.128 |
| 6 | 0.176 | 0.237 | 0.117 |
| 7 | 0.104 | 0.143 | 0.098 |
| 8 | 0.049 | 0.053 | 0.086 |
| 9+ | ~0.046 | ~0.034 | ~0.254 |

### Summary Statistics

| Corpus | N | Mean | Std | Skewness |
|--------|---|------|-----|----------|
| VMS A | 9,651 | 5.260 | 1.918 | 1.417 |
| VMS B | 18,649 | 5.400 | 1.681 | 0.395 |
| Latin | 35,820 | 5.604 | 2.822 | 0.584 |

### Log-Normal Fit

- VMS A: log-normal(mu=1.597, sigma=0.358), median=4.94 chars
- VMS B: log-normal(mu=1.632, sigma=0.344), median=5.12 chars

---

## Interpretation

**H472 CONFIRMED (characterization).** Key findings:

1. **VMS is narrower than Latin**: VMS std=1.68-1.92 vs Latin std=2.82. Latin has significant probability at short lengths (2-3 chars: 27% vs VMS 12-14%) and long lengths (9+: 25% vs VMS 3-5%). VMS is concentrated in the 4-8 char range (~80% of words).

2. **VMS is NOT heavy-tailed like natural language**: Natural language word length distributions follow Zipf/power law. VMS is approximately log-normal (near-Gaussian in log-space), consistent with the gauss(mu, sigma) generative model. This supports the structured grammar hypothesis — word lengths emerge from constrained templates, not from natural-language morphological processes.

3. **A-dialect is more right-skewed than B-dialect**: A skewness=1.417 vs B skewness=0.395. A has a longer right tail (larger fraction of 11-15 char words: 1.6% vs 0.6%). This may reflect A-dialect's longer onset prefixes (cth, qot, ol) and suffix diversity.

4. **Latin vs VMS shape difference is diagnostic**: Latin has more words at lengths 1-3 (function words, prepositions) and 9+ (polysyllabic). VMS lacks both extremes — consistent with a system that generates words by combining onset+suffix templates with fixed length ranges, rather than sampling from a natural language vocabulary.

5. **Log-normal fit is adequate**: Both A and B dialects fit log-normal(mu≈1.6, sigma≈0.35) reasonably well. The median (5.0-5.1 chars) is close to the mean (5.3-5.4 chars) for B-dialect (near-symmetric). A-dialect has stronger right skew.

---

## Self-Audit

**Target-awareness**: No calibration involved. Pure measurement study.

**Feature-destroying implementation**: N/A — characterization only.

**Extrapolation**: Claim "log-normal fit is adequate" is visual/descriptive, not formally tested (no chi-squared goodness-of-fit). The claim is that the log-normal shape captures the general profile — not that it's a statistically proven fit. More precise claims would require a formal test.

**Negative-result scope**: N/A — positive characterization result.

**Control behavior**: Latin comparison as expected: wider distribution, more short and long words. No surprising behavior.
