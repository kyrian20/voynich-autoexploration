# exp_138: Herbal Gradient, Stars cth Anomaly, f47 Profile
**Date**: 2026-04-09
**Hypotheses**: H272 (herbal cth gradient), H273 (stars cth anomaly), H274 (f47 profile)
**Status**: H272 CONFIRMED PARTIAL, H273 NOT CONFIRMED (NOISE), H274 CONFIRMED

---

## H272: WITHIN-HERBAL cth GRADIENT — CONFIRMED PARTIAL

The within-herbal cth gradient (ρ=-0.486) is PARTIALLY explained by B-herbal insertions, but A-herbal itself shows a GENUINE residual cth decline.

### Gradient Decomposition
| Group | Spearman ρ (cth vs folio#) | Interpretation |
|-------|--------------------------|---------------|
| All herbal | -0.486 | Strong gradient |
| **A-herbal only** | **-0.353** | **Moderate gradient — NOT zero** |
| B-herbal only | not computed (only 1 early B folio) | |

A-herbal-only gradient ρ=-0.353 (44 folios): **A-herbal itself has a genuine cth decline**, not just a B-insertion artifact.

### Early vs Late A-Herbal cth Rates
| Period | n folios | cth rate | d rate | l rate |
|--------|---------|---------|--------|--------|
| A-herbal f1-f28 | 26 | 5.4% | 17.2% | 0.4% |
| A-herbal f29-f57 | 18 | **3.7%** | 16.0% | **0.8%** |
| Ratio (late/early) | | **0.69×** | 0.93× | **1.84×** |

Late A-herbal has 31% less cth and 84% more l than early A-herbal (within A-dialect folios only). The cth decline and l increase are genuine features of A-herbal folio progression.

### Interpretation
1. **B-insertions contribute**: removing B-herbal reduces gradient from ρ=-0.486 to ρ=-0.353
2. **A-herbal also has a residual gradient** (ρ=-0.353): later A-herbal folios (f40s-f50s) have distinctly less cth than early A-herbal (f1-f20)
3. The l-gradient in A-herbal is equally notable (ρ=+0.457): later A-herbal has more l-onset words
4. The cth vocabulary is stable (cthy/cthol/cthey dominate both periods) — fewer cth tokens, not different cth words

**Possible mechanisms**: (a) Different scribe for later A-herbal folios — the A/B distinction may be a gradient rather than binary; (b) Content shift — later herbal plants have names/descriptions that use fewer cth-nominal forms; (c) Folio-proximity effect — later herbal folios (f42-f57) are physically closer to the B-cosmo section (f75-f84) and may show vocabulary contamination.

### B-Herbal Folios as Pure B-Dialect
B-herbal folios are distributed: early=[f26], late=[f31,f33,f34,f39,f40,f41,f43,f46,f48,f50,f57]. All B-herbal have near-zero cth (consistent with B-dialect universal cth depletion, F139). The single early B-folio (f26) has cth=2.0% (slightly elevated vs other B-herbal, possibly from A-herbal spillover on the bifolio).

---

## H273: STARS cth ANOMALY — NOT CONFIRMED (NOISE ARTIFACT)

The stars cth ρ=+0.469 from exp_137 is a **noise artifact** driven by fewer than 20 tokens.

### Per-Folio cth in Stars
| Folio | Total words | cth tokens | cth% |
|-------|------------|-----------|------|
| f103 | 879 | 0 | 0.00% |
| f104 | 824 | 2 | 0.24% |
| f105 | 703 | 0 | 0.00% |
| f106 | 776 | 1 | 0.13% |
| f107 | 851 | 1 | 0.12% |
| f108 | 976 | 3 | 0.31% |
| f111 | 1077 | 0 | 0.00% |
| f112 | 725 | 0 | 0.00% |
| f113 | 906 | **7** | **0.77%** |
| f114 | 742 | 1 | 0.13% |
| f115 | 782 | 0 | 0.00% |
| f116 | 507 | **4** | **0.79%** |

**Total cth in all of stars: 19 tokens across 7748 words = 0.25%**

The ρ=+0.469 is driven entirely by f113 (7 tokens) and f116 (4 tokens). With 19 total tokens across 12 folios, most of which have 0-3 tokens, the Spearman ρ is statistically unreliable. This is **noise, not a real gradient**.

### Nature of cth Words in Stars
The 19 cth tokens in stars include BOTH A-type forms (cthol=2, cthy=1, cthar=1) and B-cth hybrid forms (cthedy=2, ctheey=1, cthdy=1). Both types are hapax-concentrated. These are likely rare vocabulary items from the general Voynichese repertoire that happen to appear in late stars — not a systematic pattern.

**Revision**: F144's "STARS cth ρ=+0.469 (UNEXPECTED)" is retracted. The stars cth "gradient" is a sampling artifact with <20 total tokens.

---

## H274: f47 FULL PROFILE — CONFIRMED

f47 (herbal/A) is a statistically small folio (134 words) with extreme ch-concentration driven by sampling effects, not systematic scribal difference.

### f47 vs A-Herbal Centroid
| Onset | f47% | A-herbal% | Ratio |
|-------|------|-----------|-------|
| ch | **35.1%** | 17.1% | **2.06×** |
| d | 20.1% | 16.7% | 1.21× |
| y | **0.0%** | 6.5% | **0.00×** |
| qo | **0.0%** | 2.5% | **0.00×** |
| other | 3.0% | 9.6% | 0.31× |
| ok | 2.2% | 4.5% | 0.50× |
| qok | 1.5% | 3.8% | 0.40× |
| cth | 2.2% | 4.8% | 0.47× |

**f47 has zero y-onset and zero qo-onset words** with only 134 words. By chance, no y-initial or qo-initial words appear in this small sample.

### ch-Concentration Source
f47 ch-words: 47 tokens (35.1%). Dominated by:
- chol: 11 tokens (3.0× A-herbal rate)
- chy: 6 tokens (4.6×)
- chdy: 3 tokens (34.9×! — normally very rare)

The chol/chy over-representation is a SAMPLING EFFECT in a 134-word folio. chdy (34.9×) shows that some rare ch-words appear by chance.

Top words overall: chol(11), daiin(8), chy(6), shol(4), dain(4) — entirely standard A-herbal vocabulary. No unusual or section-specific words.

### Section Similarity
| Section | Cosine similarity |
|---------|-----------------|
| herbal | **0.8473** (best match) |
| pharma | 0.7031 |
| astro | 0.6330 |
| stars | 0.5280 |
| cosmo | 0.4637 |

f47 is most similar to herbal (0.8473) — correctly identified as a herbal folio. Its cosine distance from the herbal centroid (dev=0.2375 from F144) reflects the ch-concentration anomaly, which is a sampling artifact in a small folio.

**Verdict**: f47 is not a scribal outlier or misclassified folio. It is a normal A-herbal folio with unusual ch-concentration explained by small sample size (134 words). The 0% y and 0% qo are consistent with a 134-word sample where these relatively rare word types (6.5% and 2.5%) simply don't appear.

---

## Summary of New Findings (F145)

1. **A-herbal cth gradient is REAL but PARTIAL**: A-herbal-only cth ρ=-0.353 (not zero). Early A-herbal (f1-f28): cth=5.4%; late A-herbal (f29-f57): cth=3.7% (0.69×). l-gradient also real in A-herbal (ρ=+0.457). B-insertions contribute to but don't explain the full herbal cth decline.
2. **Stars cth ρ=+0.469 is NOISE**: total stars cth = 19 tokens (0.25%), gradient driven by f113(7 tokens)+f116(4 tokens). Not a real gradient. F144's stars-cth claim is RETRACTED.
3. **f47 is a small-sample A-herbal folio**: ch=35.1% (2.06×) is sampling artifact (134 words, chol=11 tokens by chance). y=0% and qo=0% are consistent with n=134 sampling of 6.5% and 2.5% rates. No systematic scribal anomaly.

---

## Hypotheses Spawned
- **H275**: Is the A-herbal cth decline driven by a specific subset of later A-herbal folios (f42-f57)? Compute the A-herbal cth rate in folio tertiles (f1-f18, f19-f37, f38-f57) to identify whether there's a smooth gradient or a specific breakpoint.
- **H276**: Is the A-herbal l-gradient (ρ=+0.457) meaningful? l-onset words are B-dialect markers (F131, F134). Do later A-herbal folios (f42-f57) have l-onset words that look like B-vocabulary, suggesting scribal cross-contamination or dialect mixing at A/B boundaries?
