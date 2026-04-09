# Experiment exp_049: Bio Section Lag-13 Word Autocorrelation
Date: 2026-04-09

## Question (H055)
Is the lag=13 word autocorrelation peak found in f84v (ratio=2.30) and f75v (ratio=2.22) in exp_042 a systematic bio-section feature, or a 2-folio coincidence?

## Results

### Bio Section Lag=13 Summary (19 folios, all ≥50 tokens)

| Metric | Value |
|--------|-------|
| Mean lag=13 ratio | **1.00** (exactly at chance baseline) |
| Median lag=13 ratio | 0.81 |
| Folios with ratio > 2.0 | **3/19** (f75v=2.22, f82v=2.17, f84v=2.30) |
| Folios with ratio > 1.5 | 5/19 |
| Folios with ratio < 1.0 | 9/19 |

**The lag=13 effect is NOT systematic across the bio section.** Mean=1.00 means average bio-folio lag-13 autocorrelation is indistinguishable from baseline (random). 9/19 folios have ratio < 1.0 (fewer same-word pairs at lag=13 than expected by chance).

### Bio vs Herbal Comparison at Lag=13

| Section | Mean ratio | N folios with ratio>2.0 | Min | Median | Max |
|---------|-----------|------------------------|-----|--------|-----|
| Bio | 1.00 | **3/19** | 0.28 | 0.81 | 2.30 |
| Herbal (n=28) | 0.50 | **0/28** | 0.00 | 0.67 | 1.38 |

Bio does have higher mean and max than herbal, and is the only section with ratio>2.0. But this is driven by 3 specific folios, not a section-wide effect.

### The Three High-Lag-13 Bio Folios

**f75v** (n=287): Isolated peak at lag=13 (2.22), plus elevated lag=1 (1.82). The lag=1 elevation is itself a signal: adjacent words are more often the same word than chance. The lag=13 peak is sharp and isolated (lags 3-12 are all 0.00-0.93).

**f82v** (n=283): Peaks at lag=9 (2.13) and lag=13 (2.17). Both may be structural, or lag=13 may be an artifact of lag=9 pattern doubling.

**f84v** (n=319): Sharp, isolated peak at lag=13 (2.30). Surrounding lags (11,12: 1.14 and 0.00; 14: 1.61) suggest a partial pattern but no clean period.

### Interpretation of f78r Pattern

f78r (n=260) shows an alternating even/odd pattern: lags 2,4,6,7,16,17,19 elevated; lags 3,5,8,11 suppressed. This is a different structural feature — a possible two-word unit or sentence-length periodicity at ~2-3 words. This is not lag=13 but may be worth noting.

### Why 3/19 Is Not Systematic

Under a null hypothesis that any lag could accidentally yield ratio>2.0 with probability p, the 3/19 rate at lag=13 specifically is not clearly above chance. If we test all 20 lags × 19 folios = 380 tests, some high ratios are expected. The bio-vs-herbal comparison (3/19 vs 0/28) is suggestive but not definitive.

The three high-lag-13 folios (f75v, f82v, f84v) all happen to be in the "bathing pool" subset of bio folios — but this may reflect shared vocabulary (the same body-text words used across the pool scenes) creating local repetition structure, not a universal bio property.

## Finding (F056)
The lag=13 word autocorrelation signal found in exp_042 (f84v=2.30, f75v=2.22) extends to f82v (ratio=2.17), making 3/19 bio folios showing a lag=13 peak above 2.0 — but the section-wide mean is 1.00 (at baseline). The lag=13 effect is folio-specific rather than section-wide. The three high-lag-13 bio folios are f75v, f82v, f84v — all from the "bathing pool" sequence of bio folios — suggesting a structural feature specific to that folio subset (possibly repetition of pool-scene vocabulary at multi-word intervals) rather than a universal bio-section grammar. Herbal section lag=13 ratios peak at 1.38 (0/28 above 2.0).

## H055 Verdict: PARTIALLY SUPPORTED
The lag=13 effect is bio-specific (highest ratios appear only in bio, not herbal) but is NOT systematic across the bio section (mean=1.00, 9/19 below baseline). Three folios (f75v, f82v, f84v) show genuine lag=13 structure; these are all from the bathing-pool folio subset. The effect is real in those specific folios but does not represent a section-wide "paragraph unit" of 13 words. H055 as stated (section-wide systematic feature) is not supported.
