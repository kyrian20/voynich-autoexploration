# EXP-593 expanded-population sensitivity — 2026-11-04

**Status: EXPLORATORY.** This sensitivity keeps the EXP-593 variants, position statistic and max-T family, but expands the page-ID coverage to the broader pattern already used by EXP-590. The historical EXP-593 files remain unchanged.

## Source and population

- Source: `data/transcriptions/eva_zl3b.txt`
- SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- Included lines: 5,376; tokens: 39,594.
- Relative to the restricted EXP-593 population: +1,188 lines and +6,862 tokens.
- Observed: daiin 853 (161 initial, 134 final); dain 212 (49 initial, 27 final); daiiin 21 (2 initial, 6 final).

## Method

For each of 5,000 synchronized replicates, independently select one uniformly random token from each line. For the line-initial count, this has the same distribution as shuffling each line and observing its first token. Standardize each variant against its own null distribution; compare the observed standardized statistic with the replicate-wise maximum across the three variants. Seed: `0x59320261104`, xorshift32. The implementation and complete JSON are adjacent in this maintenance package.

## Results

| Variant | Observed starts | Null mean | Observed z | Empirical p | max-T adjusted p |
|---|---:|---:|---:|---:|---:|
| daiin | 161 | 109.080 | 5.590 | 0.000200 | 0.000200 |
| dain | 49 | 25.934 | 4.949 | 0.000200 | 0.000200 |
| daiiin | 2 | 3.189 | -0.749 | 0.862228 | 0.993401 |

The minimum reportable p with 5,000 replicates and the +1 correction is 0.000200. Thus the first two values are resolution-bound, not precise tail estimates.

## Interpretation and limits

The positional excess for daiin and dain remains in this broader population under this within-line exchangeability null; daiiin does not show an initial-position excess. This is a sensitivity result, not an independent confirmation: the words were selected during earlier exploratory work, the population is a broadened transcriptional view of the same manuscript, and the null preserves each line's token multiset while discarding order. No semantic interpretation follows.

## Self-Audit

**Target-awareness:** The variants and max-T family were carried forward from earlier exploratory work. They were not selected independently for this sensitivity, so these results are conditional on that prior selection and are exploratory.

**Feature-destroying implementation:** The tested feature is line-initial placement. Sampling one token uniformly within each included line preserves that line's token multiset and gives the same line-initial null distribution as shuffling it. The parser uses a broad page-ID rule and removes IVTFF tags and bracketed annotations before tokenizing; this changes the included population and is a limitation, but it does not selectively alter the observed order statistic within retained lines. Full IVTFF conformance remains unestablished.

**Extrapolation beyond the tested grid:** No claim is made about all possible null models, all word forms, language identity, or the manuscript as a whole. The tested set is the three named variants under one specified within-line null.

**Negative-result overreach:** The result for `daiiin` means only that this variant did not show an initial-position excess under this population and null. It does not establish that the form lacks a function or that no alternative mechanism could produce positional concentration.

**Control-comparison interpretation:** Under the null, the expected line-initial count for a word is the sum across retained lines of that word's within-line frequency. The 5,000-replicate null means are 109.080 for `daiin`, 25.934 for `dain`, and 3.189 for `daiiin`; the corresponding observed counts are 161, 49, and 2. The first two exceed the null distribution at its reported resolution floor; the third does not. This is an order-exchangeability comparison, not an independent language or random-text baseline.

This uses a different, explicitly seeded PRNG stream from the canonical EXP-593 Python `random.shuffle` run. It is distribution-equivalent for this statistic, but it is not an exact replay of the historical permutation sequence. Do not replace the archived EXP-593 values or cite this as a translation.
