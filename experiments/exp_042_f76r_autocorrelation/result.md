# Experiment exp_042: f76r Autocorrelation and Periodic Structure
Date: 2026-04-09

## Question (H054)
Does f76r have higher word-level autocorrelation / periodic structure than normal bio text, consistent with its "key-like sequence" ZL3b designation and lowest-manuscript TTR=0.466?

## Results

### Summary Comparison Table

| Folio | Tokens | TTR | H2 | Baseline | Max ACF ratio | Sig. lags |
|-------|--------|-----|-----|---------|--------------|-----------|
| **f76r** | 514 | 0.545 | 1.427 | 0.0095 | **1.85** | none |
| f75v | 287 | 0.603 | 1.099 | 0.0115 | 2.22 *** | lag=13 |
| f77r | 296 | 0.561 | 1.325 | 0.0159 | 1.56 | none |
| f77v | 305 | 0.541 | 1.463 | 0.0180 | 1.73 | none |
| f78r | 260 | 0.638 | 1.010 | 0.0122 | 1.94 | none |
| f80r | 405 | 0.548 | 1.385 | 0.0127 | 1.83 | none |
| f84r | 310 | 0.613 | 1.135 | 0.0120 | 1.45 | none |
| **f84v** | 319 | 0.539 | 1.372 | 0.0142 | **2.30** *** | lag=13 |

**f76r does NOT have the highest autocorrelation among bio folios.** Max ACF ratio=1.85 at lag=2 — below the 2.0 significance threshold. Two comparison folios (f84v, f75v) have higher peak ACF ratios, both peaking at lag=13.

### f76r Word Frequency (Explaining Low TTR)

f76r's low TTR (exp_039: TTR=0.466 manuscript-wide lowest) is **not due to periodic structure** — it's due to high frequency of a small standard Currier B vocabulary:
- shedy: 25 tokens (4.9%)
- chedy: 19 tokens (3.7%)
- chey: 11 tokens (2.1%)
- dain/shey/sain/qokeey/qokey: 8-10 tokens each

This is normal Currier B bio section vocabulary. f76r simply has a high concentration of these common words. The word-level H2=1.427 bits is in the normal range for bio section folios.

### Key Finding: f76r Body Text Is Structurally Normal Bio Text

The ZL3b designation "has 'key-like' sequence, here transcribed as L0 labels" refers to the LINE MARKER sequence (L0 locus entries), **not to the body text** (P0 locus entries). This experiment confirms that f76r's P0 body text has:
- Normal word autocorrelation (max ratio 1.85, not significant)
- Normal consecutive-line Jaccard similarity (mean=0.045)
- Standard Currier B bio vocabulary (shedy/chedy/chey etc.)

The "key-like" structural anomaly in f76r is entirely in the L0 line marker layer (already characterized in exp_013/exp_026), not in the body prose.

### Surprise Finding: f75v and f84v Both Peak at Lag=13

Both f75v (ratio=2.22***) and f84v (ratio=2.30***) show significant autocorrelation at lag=13. These are different folios in the bio section (f75v=line-marker folio/Hand 2; f84v=normal bio folio). The lag=13 coincidence could reflect:
- Bio section prose organized in ~13-word paragraph units
- Or could be noise at this sample size (both have 9-10 matches at lag=13/305-319 comparisons)
The lag=13 signal in bio text warrants further investigation but is not the focus of this experiment.

## Finding (F049)
f76r body text has no significant word-level autocorrelation (max ACF ratio=1.85, below significance threshold). Its lowest-TTR status in the manuscript is due to concentration of standard Currier B high-frequency words (shedy/chedy/chey), not periodic phrase structure. The ZL3b "key-like sequence" designation refers to the L0 line marker layer, not the body prose. Notably, f75v and f84v (bio section) both show significant autocorrelation at lag=13 — a possible bio-section structural feature requiring further investigation (H055 candidate).

## H054 Verdict: NOT SUPPORTED
f76r body text lacks periodic structure. It is structurally normal Currier B bio text with high concentration of common words. The "key-like" anomaly is in the L0 line markers, which were already characterized in exp_013/exp_026.
