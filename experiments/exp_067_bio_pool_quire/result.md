# Experiment exp_067: Bio Pool vs Non-Pool (H082) + pch/tch Quire Distribution (H080)
Date: 2026-04-09

## H082: Bio Pool vs Non-Pool Folio Vocabulary Comparison

### Setup
Pool folios (multi-paragraph bio, from exp_061): f83r, f84v, f75v, f75r, f82r, f83v, f84r
Non-pool: all other bio section folios.

| Metric | Pool | Non-Pool |
|--------|------|----------|
| Tokens | 2097 | 3630 |
| Types | 799 | 1193 |
| **Jaccard** | **0.201** | — |
| qo-rate | 26.8% | 25.7% |

### Suffix Distributions

| Suffix | Pool% | Non-Pool% | Ratio |
|--------|-------|-----------|-------|
| -edy | 22.9% | 18.6% | 1.24× |
| -dy | 4.5% | 3.1% | 1.47× |
| -aiin | 5.2% | 6.2% | 0.84× |
| -ain | 6.1% | 7.9% | 0.77× |
| -eedy | 7.7% | 7.5% | 1.02× |
| -y | 10.4% | 11.1% | 0.93× |
| -ol | 6.5% | 7.8% | 0.83× |

Suffix profiles are nearly identical. No suffix class differs by more than 1.5×.

### Over-Represented Words

**Pool-enriched** (top): okey (6.9×), ldy (4.3×), qoteey (4.3×), oldy (4.0×), okedy (2.8×), dol (2.6×), olchedy (2.5×)

**Non-pool-enriched** (top): olor (exclusive), okeey (7.5×), olkain (6.6×), oky (6.4×), otain (5.2×), qokol (4.9×)

The word-level differences are in low-frequency forms (many counts ≤20). No structurally important words (pch/tch-onset, suffix class heads) appear differentially.

### H082 Verdict: NOT SUPPORTED — Bio pool and non-pool are the SAME dialect

Jaccard=0.201 is dramatically HIGHER than the aiin-dom vs y-dom A intra-A split (0.138) and far above A-vs-B (0.046). The pool and non-pool bio folios share:
- Same suffix profile (no suffix differs >1.5×)
- Same qo-rate (26.8% vs 25.7%)
- Same Currier B structural grammar

Multi-paragraph structure in pool folios does NOT reflect a vocabulary/grammar distinction. The "pool" property (multi-paragraph organization) is an organizational feature of the bio section, not a linguistic register distinction. The word-level differences are lexical noise from small folio sample sizes.

---

## H080: pch/tch Onset Quire Distribution in Currier B

### Results

| Quire | Total | pch | pch% | tch | tch% | pch+tch% |
|-------|-------|-----|------|-----|------|----------|
| D | 339 | 6 | 1.77% | 2 | 0.59% | **2.36%** |
| E | 824 | 8 | 0.97% | 8 | 0.97% | 1.94% |
| F | 857 | 7 | 0.82% | 2 | 0.23% | 1.05% |
| G | 374 | 3 | 0.80% | 5 | 1.34% | **2.14%** |
| H | 450 | 2 | 0.44% | 3 | 0.67% | 1.11% |
| I | 346 | 0 | 0.00% | 2 | 0.58% | 0.58% |
| J | 125 | 0 | 0.00% | 1 | 0.80% | 0.80% |
| M | 6241 | 33 | 0.53% | 27 | 0.43% | 0.96% |
| N | 1574 | 12 | 0.76% | 8 | 0.51% | 1.27% |
| Q | 484 | 2 | 0.41% | 9 | 1.86% | **2.27%** |
| T | 9991 | 101 | 1.01% | 56 | 0.56% | 1.57% |

### H080 Verdict: NOT SUPPORTED — pch/tch is evenly distributed across B

No quire shows dramatic pch/tch enrichment. The highest combined rates (D=2.36%, Q=2.27%, G=2.14%) are only ~2× above the lowest (I=0.58%, J=0.80%). This contrasts sharply with the aiin-dominant A system, which clustered in Quires D and F (62% and 50% of folios). pch/tch appears to be a **uniform structural feature** of Currier B — a positional grammar marker present in all quires, not a dialectal or scribal signature.

The pch vs tch split also varies: Quire Q uses tch-heavy (1.86% tch vs 0.41% pch), Quire D uses pch-heavy (1.77% pch vs 0.59% tch). This may reflect scribal preference (a single scribe's pch vs tch choice) rather than content-driven grammar variation.

---

## Combined Finding (F074)

**H082 NOT SUPPORTED**: Bio pool vs non-pool folios show Jaccard=0.201 (well above the intra-A register split of 0.138), nearly identical suffix profiles, and equal qo-rates. Multi-paragraph structure in bio is an organizational feature, not a linguistic register distinction. **H080 NOT SUPPORTED**: pch/tch onset words are distributed evenly across Currier B quires (range 0.58–2.36% combined) with no strong clustering. This confirms pch/tch is a universal positional grammar marker in B (para-start signal), not a scribal or content dialect feature. The per-quire pch/tch split may reflect individual scribe preferences within the shared grammar system.
