# Experiment exp_036: Word-Final Character Inventory
Date: 2026-04-09

## Question
What specific characters dominate the word-final position (the most constrained position in the manuscript, bias=1.482 bits from exp_027)?

## Results

### Top Final Characters
| Rank | Char | Count | % |
|------|------|-------|---|
| 1 | 'y' | 13,303 | 41.1% |
| 2 | 'n' | 5,494 | 17.0% |
| 3 | 'l' | 5,080 | 15.7% |
| 4 | 'r' | 4,827 | 14.9% |
| 5 | 'o' | 999 | 3.1% |

**Top 3 chars cover 73.8%; top 5 cover 91.8%** of all word endings.

### Final Position Entropy
- Word-final H = **2.460 bits** (vs shuffled 3.86 = bias 1.48 bits)
- Currier A: H = 2.682 bits (more diverse — l/r/o more common)
- Currier B: H = 2.324 bits (more constrained — y dominant at 45.5%)

### Currier A vs B Final Distribution
| Char | A% | B% | Difference |
|------|----|----|------------|
| 'y' | 31.8% | 45.5% | B +13.7% |
| 'l' | 19.3% | 14.0% | A +5.4% |
| 'r' | 17.3% | 13.9% | A +3.4% |
| 'n' | 16.3% | 17.4% | ≈equal |
| 'o' | 5.3% | 2.0% | A +3.3% |

### Top Word-Final Bigrams
| Bigram | Count | % |
|--------|-------|---|
| ...dy | 6,023 | 18.6% |
| ...in | 5,395 | 16.7% |
| ...ey | 3,572 | 11.0% |
| ...ol | 3,153 | 9.7% |
| ...ar | 2,284 | 7.1% |
| ...or | 1,952 | 6.0% |
| ...hy | 1,866 | 5.8% |
| ...al | 1,735 | 5.4% |

Top 8 bigrams cover **79.3%** of all word endings.

### Section Variation
- Bio: 'y'=54%, 'l'=18%, 'n'=14% (most y-heavy)
- Astro: 'y'=48%
- Herbal: 'y'=36%, 'r'=17%, 'n'=17%, 'l'=15%
- Pharma: 'y'=33%, 'l'=24%

## Finding (F042)
The word-final inventory is dominated by {y, n, l, r} (88.8% coverage). The most common word-final bigrams are ...dy (18.6%), ...in (16.7%), ...ey (11.0%), ...ol (9.7%). Currier B has 'y' dominant at 45.5% vs A at 31.8%; A is more balanced across l/r/n/y. These patterns directly match Stolfi's predicted suffix templates: -y, -in/-ain, -ol/-al, -ar/-or are the canonical Voynich word endings. Bio section most y-heavy (54%); pharma most l-heavy (24%).
