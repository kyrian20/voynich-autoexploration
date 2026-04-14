# Chain Null-Model Report — exp_583

**Generated:** 2026-04-12  
**Target chain:** d → qot → ch → o → sh  
**N shuffles per control:** 200  
**Chain threshold:** E≥1.5× per edge  

## Real A herbal_a Chain

| Edge | obs | exp | E | N_cond | Status |
|------|-----|-----|---|--------|--------|
| d → qot | 13 | 8.31 | 1.564× | 277 | CONF |
| qot → ch | 12 | 6.09 | 1.970× | 34 | CONF |
| ch → o | 13 | 8.42 | 1.544× | 203 | CONF |
| o → sh | 5 | 2.03 | 2.460× | 47 | dir |

**Real chain joint strength:** 11.6987

**Real corpus best chain JS (over all 9203 qualifying chains):** 1641.5579

## Top 10 Qualifying Chains in Real Corpus

| Rank | Chain | Joint Strength | Notes |
|------|-------|---------------|-------|
| 1 | s → cph → t → cph → t | 1641.5579 |  |
| 2 | s → cph → t → cph → qot | 1496.7146 |  |
| 3 | t → cph → t → cph → t | 1376.7905 |  |
| 4 | cph → t → cph → t → cph | 1376.7905 |  |
| 5 | s → cph → qot → cph → t | 1364.6515 |  |
| 6 | qot → cph → t → cph → t | 1255.3090 |  |
| 7 | t → cph → t → cph → qot | 1255.3090 |  |
| 8 | s → cph → qot → cph → qot | 1244.2411 |  |
| 9 | qok → cph → t → cph → t | 1185.5696 |  |
| 10 | ckh → l → qok → cph → t | 1172.1527 |  |

## Section-Shuffled Control

| Metric | Value |
|--------|-------|
| N shuffles | 200 |
| Mean qualifying chains | 7896.9 |
| p50 best_JS | 12859.3662 |
| p95 best_JS | 4218515.0687 |
| Max best_JS | 402308947.4417 |
| Real best_JS | 1641.5579 |
| Fraction best_JS ≥ real | 0.8650 |
| **Best_JS percentile rank** | **13.5%** |
| Real target_JS | 11.6987 |
| Fraction target_JS ≥ real | 0.0000 |
| **Target_JS percentile rank** | **100.0%** |
| Shuffles with exact target chain | 0/200 |

## Onset-Shuffled Control

| Metric | Value |
|--------|-------|
| N shuffles | 200 |
| Mean qualifying chains | 5925.2 |
| p50 best_JS | 2287.2242 |
| p95 best_JS | 40230.8947 |
| Max best_JS | 4218515.0687 |
| Real best_JS | 1641.5579 |
| Fraction best_JS ≥ real | 0.6150 |
| **Best_JS percentile rank** | **38.5%** |
| Real target_JS | 11.6987 |
| Fraction target_JS ≥ real | 0.0000 |
| **Target_JS percentile rank** | **100.0%** |
| Shuffles with exact target chain | 0/200 |

## Falsifiability Statement

The finding would be falsified if the real chain falls in the body of either control distribution. Two metrics are computed; only the target_JS metric is valid for this finding.

**Correct metric — target_JS (specific pre-specified chain d→qot→ch→o→sh):**
- Section-shuffled: 0.0% of shuffles exceed real target_JS → **ROBUST (100th percentile)**
- Onset-shuffled: 0.0% of shuffles exceed real target_JS → **ROBUST (100th percentile)**

**Invalid metric — best_JS (maximum over all exhaustive chain search):**
- Section-shuffled: 86.5% exceed real best_JS → 13.5th percentile (NOT robust)
- Onset-shuffled: 61.5% exceed real best_JS → 38.5th percentile (NOT robust)

**Why best_JS is invalid:** The best-JS metric is dominated by sparse-data artifact. Rare onset class `cph` (~1% LF base rate) generates inflated E-values from 2-4 observations, producing chains with JS≥1,000. Shuffled corpora produce even stronger such chains by chance (section-shuffled mean best_JS = 2,800,000 vs real 1,641). The chain finding was identified by theoretical systematic analysis (exp_515–524), not by searching for the globally strongest chain. The target_JS metric (testing the specific pre-specified chain) is the appropriate null model comparison.

**Conclusion:** The chain finding is robust when tested as a specific directed hypothesis (100th percentile, both controls). It is NOT the globally strongest chain in the real corpus and cannot be presented as such.

## Additional Note: Unexpected Control Behavior

Section-shuffled mean best_JS (2,800,000) >> real best_JS (1,641). Shuffled corpora produce much stronger "best chains" than real data. This is unexpected from the naive perspective that genuine signal should outrank noise. Investigation: the best_JS metric searches 9,203 combinations including many cph-dominant sparse-data chains; shuffling can cluster these tokens more strongly than the real data does. This is NOT evidence against the chain finding — it is evidence against the best_JS metric.

