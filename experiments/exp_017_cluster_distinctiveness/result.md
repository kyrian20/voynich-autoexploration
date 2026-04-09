# Experiment exp_017: Cluster Distinctiveness Analysis
Date: 2026-04-09

## Method
Compared the four cluster folios (f49v, f57v, f66r, f76r) against 10 control folios from the same sections, using:
- Character frequency KL divergence vs. manuscript-wide distribution
- Word frequency KL divergence (top-500 words)
- Word length KS test vs. pooled controls
- Type-token ratio (TTR)
- Cross-cluster KL divergence (are cluster folios similar to each other?)

**Note on parsing:** Used all-locus parsing (not P0 only) to capture f57v's circular text, which has no P0 locus. This means f57v's "words" are dominated by single-character tokens from its repeating sequence.

## Basic Statistics

| Folio | N_words | N_unique | TTR | MeanLen | Type |
|---|---|---|---|---|---|
| f49v | 150 | 105 | 0.700 | 5.10 | CLUSTER |
| f57v | 181 | 80 | 0.442 | **2.47** | CLUSTER |
| f66r | 344 | 246 | 0.715 | 4.88 | CLUSTER |
| f76r | 569 | 259 | 0.455 | 4.78 | CLUSTER |
| f1r | 209 | 160 | 0.766 | 4.62 | control |
| f2v | 55 | 44 | 0.800 | 5.16 | control |
| f3r | 110 | 87 | 0.791 | 5.12 | control |
| f4r | 61 | 47 | 0.770 | 5.31 | control |
| f5r | 54 | 45 | 0.833 | 4.93 | control |
| f76v | 393 | 227 | 0.578 | 5.37 | control |
| f77r | 332 | 177 | 0.533 | 5.33 | control |
| f78r | 293 | 162 | 0.553 | 4.82 | control |
| f99r | 193 | 143 | 0.741 | 4.94 | control |
| Pooled controls | ~1,748 | — | 0.456 | 5.09 | — |

## Key Finding: The "Cluster" Is NOT Statistically Homogeneous

The four cluster folios do not form a coherent statistical cluster:

### f57v Is Extreme
- **KL(char)=0.768** vs. manuscript-wide — by far the highest of any folio examined (controls: 0.06-0.23)
- **Mean word length = 2.47** — drastically below controls (~5.1)
- **KS statistic = 0.584** (p<0.05) — word length distribution is completely different
- **Top "words":** r(13), v(12), o(12), l(12), y(9), d(9), k(7), x(7) — all single characters from the repeating sequence
- **TTR = 0.442** — low, because the same ~12 characters repeat 4 times

All of this is explained by the repeating 18-character sequence: f57v's "text" is dominated by the circular sequence, which consists of single-character tokens. f57v's statistical distinctiveness is entirely a consequence of its structural role as a cosmological wheel with a specialized repeating inscription.

### f66r and f76r Are Statistically Normal
- **f76r: KL(char)=0.0365** — the LOWEST divergence from corpus of all folios examined; more "typical" than any control
- **f66r: KL(char)=0.0634** — similarly low
- Both are **indistinguishable from Currier B controls** (f76v=0.0734, f77r=0.0643, f78r=0.0673)
- f76r and f66r have low cross-divergence: **KL(f76r||f66r)=0.048** — they're very similar to each other

The Currier B body text on these folios is statistically normal. The "key-like" sequence labels (which are a small fraction of total words) do not meaningfully shift the overall character distribution.

### f49v Is Intermediate
- KL(char)=0.129 — slightly elevated vs. corpus but within normal range for herbal folios
- Mean length = 5.10, similar to controls
- Top words include single-char markers (y×5, e×4, s×4, o×3, d×3) but also normal body text (daiin×9, shol×3, chor×5)

The single-character line markers on f49v are a minority of the word count (26 markers among 150 total words = 17%), so they don't dramatically shift the distribution.

## Cross-Cluster Divergence

| Pair | KL(A||B) | KL(B||A) |
|---|---|---|
| f49v ↔ f57v | 0.649 | 2.239 |
| f49v ↔ f66r | 0.218 | 0.300 |
| f49v ↔ f76r | 0.321 | 0.193 |
| f57v ↔ f66r | 1.487 | 0.313 |
| f57v ↔ f76r | 2.373 | 0.454 |
| **f66r ↔ f76r** | **0.173** | **0.048** |

f66r and f76r are the most similar cluster pair (both Currier B, Hand 2 and Hand 5). f57v diverges maximally from everything, especially f76r.

For comparison, cross-control divergences: f1r↔f2v=0.286, f2r↔f4r=0.113, f3r↔f4r=0.580 — so the cluster folios are no more similar to each other than random controls.

## Word Frequency Analysis

### Top 10 Words Per Cluster Folio

| f49v | f57v | f66r | f76r |
|---|---|---|---|
| daiin (9) | r (13) | daiin (8) | shedy (28) |
| y (5) | v (12) | shedy (8) | chedy (23) |
| chol (5) | o (12) | ol (7) | chey (12) |
| chor (5) | l (12) | y (5) | dain (10) |
| e (4) | y (9) | o (5) | shey (10) |
| s (4) | d (9) | qoky (5) | qokeey (9) |
| shol (3) | k (7) | d (4) | qokey (9) |
| o (3) | x (7) | f (4) | ol (9) |
| d (3) | s (6) | okedy (4) | sain (8) |
| oaiin (3) | m (5) | chedy (4) | ain (8) |

f57v's vocabulary is effectively single-character tokens from the repeating sequence. f66r shows Currier B patterns (shedy, chedy, daiin) but with moderate hapax rate — consistent with being a word-list folio with unusual vocabulary. f76r shows typical Currier B body text (shedy, chedy dominate).

## Word Length Distributions (KS test vs pooled controls)

| Folio | KS stat | Significance | Mean Length |
|---|---|---|---|
| f49v | 0.144 | p<0.05 | 5.10 |
| f57v | **0.584** | p<0.05 | 2.47 |
| f66r | 0.064 | p≥0.05 | 4.88 |
| f76r | 0.071 | p<0.05 | 4.78 |

Only f57v has a dramatically different word length distribution. f66r's distribution is statistically indistinguishable from controls. f49v and f76r show minor differences (p<0.05 but KS<0.15).

## Conclusions

1. **The "cluster" is not defined by shared statistical properties.** f57v is extreme (cosmological repeating sequence), while f66r and f76r are statistically normal Currier B folios. There is no coherent statistical signature that unites these four folios.

2. **The cluster is defined by structural/editorial features**, not text statistics:
   - f49v: line-marker L0/P0 alternation (structural)
   - f57v: repeating @glyph sequence in circular text (structural)
   - f66r: two-column word-list (structural) + @169/@172 (shared with f57v)
   - f76r: key-like L0 markers noted by ZL3b transcribers (editorial designation)

3. **f66r and f76r are the most statistically similar pair** — both Currier B, similar word distributions. Their similarity is dialect-driven, not cluster-driven.

4. **f57v's statistical distinctiveness is entirely explained** by its cosmological wheel structure: the dominant text is a repeating sequence of single-character tokens. This is a local structural effect, not a global manuscript-level anomaly.

5. **Statistical methods cannot detect this cluster** — the cluster must be identified through structural analysis (locus patterns, transcription comments, @glyph identity) rather than character/word frequency analysis.

## Implication for Cluster Hypothesis
The four-folio cluster should be understood as a **structural/editorial** grouping, not a statistically homogeneous text category. Any hypothesis about the cluster must be grounded in its structural features (@glyph sharing, line-marker patterns, key-like designation) rather than statistical regularities.
