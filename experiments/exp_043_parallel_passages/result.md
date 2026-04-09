# Experiment exp_043: Cross-Folio Parallel Passages
Date: 2026-04-09

## Question (H052)
Are there repeated word bigrams/trigrams ("parallel passages") across different folios? Does Bio section have the highest cross-folio repetition? Are there cross-section phrase connections?

## Results

### Bigram Level (2-word sequences)

- **Total distinct word bigram types**: 27,926
- **Bigrams on 2+ distinct folios**: 1,594 (5.7%)
- **Bigrams on 10+ distinct folios**: 18

The most widespread bigram is **"chol daiin" on 24 folios** (crossing herbal+pharma sections). Top bigrams are dominated by standard Currier B high-frequency word pairs.

### Trigram Level (3-word sequences)

- **Total distinct word trigram types**: 30,910
- **Trigrams on 2+ distinct folios**: 73 (0.24%)
- **Trigrams on 3+ distinct folios**: only 4

**The manuscript is overwhelmingly unique at the trigram level.** Only 0.24% of all 3-word sequences appear on more than one folio. The most widespread trigram is "ol shedy qokedy" on 4 bio folios — a formulaic bio phrase. True "parallel passages" (repeated 3+ word sequences) are extremely rare.

### Within-Section Cross-Folio Repetition

| Section | Folios | Pairs | Bigrams/pair | Trigrams/pair |
|---------|--------|-------|-------------|--------------|
| **bio** | 20 | 190 | **6.0** | **0.17** |
| special | 23 | 253 | 2.9 | 0.04 |
| herbal | 116 | 6,670 | 0.2 | 0.002 |
| pharma | 38 | 703 | 0.2 | 0.004 |
| astro | 9 | 36 | 0.03 | 0.0 |

**Bio section is 30× more formulaic than herbal at the bigram level and 85× more formulaic at the trigram level.** This directly confirms H052's prediction and is consistent with bio's lowest section mean TTR (0.552, exp_039).

### Cross-Section Phrase Sharing

Top cross-section bigram pairs:
- **bio ↔ special**: 1,404 shared bigrams (highest of any cross-section pair)
- herbal ↔ pharma: 577 shared bigrams
- herbal ↔ special: 476 shared bigrams

Top cross-section trigram pairs:
- **bio ↔ special**: 17 shared trigrams (dominant)
- pharma ↔ special: 3 shared trigrams
- herbal ↔ pharma: 2 shared trigrams

**bio↔special is the most connected cross-section pair at both bigram AND trigram level.** This aligns with exp_038's finding that the -aiin suffix concentrates in the Special section (57%) and -edy concentrates in bio (42%) — these sections share morphological paradigm preferences AND phrase-level vocabulary.

### Cross-Section Trigrams (Interesting Cases)

- "chey qol chedy" — 3 folios, bio+special
- "or aiin cheol" — 3 folios, pharma+special
- "chol daiin chol" — 2 folios, herbal+pharma
- "okedy okedy qokedy" — 2 folios, bio+herbal (repeated word!)

The repeated-word trigram "okedy okedy qokedy" is notable: the same word appears twice in succession, crossing bio and herbal sections.

## Finding (F050)
**Bio section is the most formulaic section by cross-folio n-gram repetition**: 6.0 shared bigrams/pair (30× herbal's rate) and 0.17 shared trigrams/pair (85× herbal's rate). The full manuscript has only 73/30,910 trigrams (0.24%) appearing on 2+ folios — "parallel passages" at 3+ word level are extremely rare. The most cross-section connected pair is bio↔special (1,404 shared bigrams, 17 shared trigrams), consistent with exp_038's finding that these sections share morphological suffix preferences. Herbal section is the least formulaic: 0.002 shared trigrams/pair, consistent with its highest folio-level TTR (exp_039).

## H052 Verdict: SUPPORTED
Bio section has the highest cross-folio phrase repetition at both bigram and trigram levels. The manuscript overwhelmingly avoids exact phrase repetition beyond 2 words — only 0.24% of trigrams are repeated cross-folio — which is inconsistent with a template-generated text (which would produce much higher trigram repetition rates). The bio↔special cross-section connection at phrase level is a new finding with direct implications for the suffix paradigm (H034/F045).
