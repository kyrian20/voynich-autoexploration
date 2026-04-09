# Experiment exp_053: Currier A Line Structure
Date: 2026-04-09

## Question
Does Currier A have a rigid line-level positional grammar? F057 showed 'd'-stem words mark line endings and -ol/-or words avoid them. Does -or dominate line-initial positions? What is the full suffix positional map?

## Results (Currier A, baseline = 15.9% per slot)

### Suffix Positional Profiles — Currier A

| Suffix | N | First% | Last% | Medial% | First/base | Last/base |
|--------|---|--------|-------|---------|-----------|----------|
| **-or** | 961 | **26.4%** | 4.3% | 69.3% | **1.66** | 0.27 |
| -ain | 217 | **20.7%** | **23.0%** | 56.2% | **1.30** | **1.45** |
| -chy | 405 | **20.7%** | 7.2% | 72.1% | **1.30** | 0.45 |
| -aiin | 1163 | 17.8% | **20.3%** | 61.9% | 1.12 | **1.27** |
| -ar | 440 | 18.4% | 17.0% | 64.5% | 1.16 | 1.07 |
| **-dy** | 607 | 10.0% | **25.4%** | 64.6% | 0.63 | **1.59** |
| **-al** | 348 | 8.6% | **21.6%** | 69.8% | 0.54 | **1.35** |
| -ol | 1352 | 14.5% | 4.8% | 80.7% | 0.91 | 0.30 |
| -ey | 922 | 14.2% | 5.0% | 80.8% | 0.89 | 0.31 |
| -eey | 385 | 16.9% | 3.1% | 80.0% | 1.06 | 0.20 |
| -y | 3210 | 12.6% | 16.4% | 71.0% | 0.79 | 1.03 |

**The -or suffix is line-initial dominant (1.66×).** The -ol suffix is NOT — it is medial/line-final avoiding but NOT especially line-initial. The two most line-final-avoiding suffixes are -eey (0.20) and -ol (0.30).

### The Corrected Line Structure for Currier A

| Slot | Dominant suffix | Ratio |
|------|----------------|-------|
| Line-initial | **-or** (not -ol) | 1.66× |
| Line-initial (word-level) | **y-initial words** (ychor, ycheor, ychol) | 5-6× |
| Line-final | **-dy**, -al, -ain, -aiin | 1.27–1.59× |
| Strongly avoids line-final | -eey (0.20×), -ey (0.31×), -ol (0.30×) |
| Strongly avoids line-initial | -dy (0.63×), -al (0.54×) |

### 'y-' Initial Words Are the Strongest Line-Initial Markers

| Word | First count | P(word|first) | P(word) | Ratio |
|------|------------|--------------|---------|-------|
| ycheey | 6 | 0.4% | 0.06% | **6.27×** |
| ychor | 13 | 0.8% | 0.14% | **5.83×** |
| ycheor | 7 | 0.4% | 0.08% | **5.49×** |
| ychol | 6 | 0.4% | 0.07% | **5.38×** |
| qotcho | 5 | 0.3% | 0.06% | **5.23×** |
| ychey | 5 | 0.3% | 0.06% | **5.23×** |

**Words beginning with 'y' followed by 'ch-' (ychor, ycheor, ychol, ychey) are 5-6× over-represented at line beginnings.** These are essentially 'y' + 'ch' compound words — the 'y' appears to be a line-initial particle.

### '-am' Words Are Strongly Line-Final

The most line-final enriched words include many words ending in '-am': dan, dom, sam, dam, cham, chom — at 3-6× above baseline. The '-am' sequence is not in the suffix paradigm list but functions as a distinctive line-final coda.

### Currier B Contrast

| Suffix | B first/base | B last/base | A first/base | A last/base |
|--------|------------|-----------|------------|-----------|
| -or | **1.84** | 0.80 | **1.66** | 0.27 |
| -ol | **1.46** | 0.65 | 0.91 | 0.30 |
| -aiin | **1.50** | 0.60 | 1.12 | **1.27** |
| -edy | 0.85 | 0.49 | 0.52 | 1.31 |
| -dy | 0.83 | 0.70 | 0.63 | **1.59** |

**In Currier B**, -or AND -ol are BOTH line-initial dominant (1.84 and 1.46). **In Currier A**, only -or is line-initial (1.66) while -ol is medial. In both dialects, -edy and -eedy avoid line endings. The biggest A/B contrast: -aiin is line-initial in B (1.50) but line-final in A (1.27); -dy is line-initial-avoiding in both but more strongly line-final in A (1.59) than B (0.70).

### 30.4% of A Lines Open with -ol/-or Words; They Cluster in Pairs

Lines starting with -ol/-or words: **475/1563 (30.4%)**. After an -ol/-or line-starter, the most common second word is **chol (41), chor (33), shol (17)** — all -ol/-or words. So the line structure for 30% of Currier A lines is: [or-word] [ol-word] [medial words] [d-stem word].

### Summary: Currier A Line Grammar

The data supports a partial line-level template in Currier A:
- **Line-opening slot**: 'y-' prefix words (5-6× enriched) or -or suffix words (1.66×); these frequently cluster: [or-word][ol-word]
- **Line-closing slot**: -dy (1.59×), -al (1.35×), -ain (1.45×), d-stem words generally
- **Medial slot**: -ol (91% medial), -ey (81% medial), -eey (80% medial)
- **Both edges**: -ain concentrates at both first AND last (1.30 and 1.45) — possibly a sentence-boundary marker

## Finding (F060)
Currier A has a partial line-level positional grammar: (1) -or suffix is the primary line-initial marker (1.66×); 'y-'+ch words (ychor, ycheor, ychol) are 5-6× over-represented at line openings — the 'y' prefix may be a line-initial particle. (2) 30% of A lines open with an -ol/-or word immediately followed by another -ol/-or word (template: [or-word][ol-word]...). (3) Line-final slot: -dy (1.59×), -al (1.35×), -ain (1.45×), and '-am' words (dan, dom, dam at 3-6×). (4) -ol and -ey/-eey words are strongly medial — these avoid both line edges. (5) In Currier B, both -or AND -ol are line-initial (1.84 and 1.46); -aiin is line-initial in B (1.50) but line-final in A (1.27) — a major A/B contrast in positional grammar. The '-ain' suffix in both A and B shows a "boundary marker" pattern (above baseline at both edges in A; line-initial in B), suggesting -ain may encode sentence-edge position independent of dialect.
