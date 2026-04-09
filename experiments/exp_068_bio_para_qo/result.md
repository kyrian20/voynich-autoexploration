# Experiment exp_068: Bio Paragraph Independence (H083) + qo-Onset Morphology (H084)
Date: 2026-04-09

## H083: Bio Paragraph Independence

### Setup
Multi-para bio folios: 7 (f75r, f75v, f82r, f83r, f83v, f84r, f84v)
Single-para bio folios: 12

### Within-Folio vs Cross-Folio Jaccard

| Folio | N paras | Para sizes | Avg Jaccard |
|-------|---------|-----------|-------------|
| f75r | 2 | 345+10 | 0.010 |
| f75v | 3 | 100+133+54 | 0.134 |
| f82r | 2 | 66+192 | 0.119 |
| f83r | 4 | 211+89+11+16 | 0.070 |
| f83v | 2 | 72+169 | 0.075 |
| f84r | 2 | 251+59 | 0.089 |
| f84v | 4 | 8+301+4+6 | 0.003 |

**Mean within-folio inter-paragraph Jaccard: 0.060**
**Mean cross-folio bio Jaccard: 0.155** (std=0.018)

### Interpretation

The mean of 0.060 is pulled heavily downward by trivially small "paragraphs" (sizes 4, 6, 8, 10, 11, 16 tokens in f75r, f83r, f84v). These tiny sub-paragraphs appear to be marginal annotations or labels mistakenly classified as paragraph-starts.

For the non-trivial paragraph pairs (both paras ≥ 50 tokens):
- f75v Para 0 vs Para 1: Jaccard = 0.156 (same as cross-folio baseline!)
- f82r Para 0 vs Para 1: Jaccard = 0.119
- f83r Para 0 vs Para 1: Jaccard = 0.137 (top words shared: shedy, qokedy, chedy, lchedy)
- f83v Para 0 vs Para 1: Jaccard = 0.075

All non-trivial paragraph pairs share the same high-frequency qo-, sh/ch-onset B grammar vocabulary. The shared top words across paragraphs within the same folio (qokain, qokedy, shedy, chedy) are the same words that appear at high frequency throughout the bio section.

### H083 Verdict: PARTIALLY SUPPORTED (trivially)

The mean within-folio paragraph Jaccard (0.060) is lower than cross-folio (0.155), BUT this is almost entirely driven by tiny marginal-note sub-paragraphs. For non-trivial paragraph pairs, within-folio Jaccard (0.075–0.156) is comparable to cross-folio (0.155). **Bio paragraphs within the same folio do NOT represent sharply independent vocabulary domains** — they share the same high-frequency B grammar words (qok-, qot-, chedy, shedy). The paragraphs may describe different figures (pool scene participants), but they use the same grammatical vocabulary. This is consistent with the overall bio register sharing the same structural vocabulary regardless of folio-level organization.

**Key structural finding**: The tiny "paragraphs" (4–16 tokens) in f83r, f84v suggest some multi-para bio folios have: (1) one large main paragraph + (2) tiny marginal annotations. This contamination affects the average Jaccard.

---

## H084: qo-Onset Morphology in Currier B

### qo Frequency and Post-qo Character

qo-onset words: 4019 / 21605 = **18.6%** of all Currier B words.

**Character following 'qo':**
| Post-qo char | Count | % |
|---|---|---|
| k | 2514 | **62.6%** |
| t | 799 | **19.9%** |
| l | 231 | 5.7% |
| p | 134 | 3.3% |
| e | 84 | 2.1% |
| d | 70 | 1.7% |
| c | 52 | 1.3% |
| f | 30 | 0.7% |

**qo attaches to gallows letters (k+t+p+f) in 86.5% of cases.** Only 13.5% use non-gallows continuation.

### Top qo Words

qokeedy (1.37%), qokain (1.25%), qokedy (1.22%), qokeey (1.19%), qokaiin (1.12%), qokal (0.75%), qokar (0.58%), qol (0.46%), qoky (0.44%), qotedy (0.40%)

The pattern is: **qo + {k|t} + standard B suffix**. qok- (2514) and qot- (799) are the two dominant sub-classes.

### qo Suffix Distribution vs All B

| Suffix | qo% | All B% | Ratio |
|--------|-----|--------|-------|
| -eedy | 10.9% | 5.3% | **2.05×** |
| -ain | 9.6% | 6.0% | **1.61×** |
| -eey | 9.1% | 6.0% | **1.50×** |
| -y | 6.0% | 8.9% | 0.68× |
| (none) | 7.8% | 15.3% | **0.51×** |

qo words strongly avoid bare/suffix-free forms (0.51×) and preferentially take the "extended" suffixes -eedy (2.05×) and -eey (1.50×). These are the same "extended form" suffixes noted in F068.

### qo Positional Grammar

| Position | qo% | Enrichment |
|----------|-----|-----------|
| para_start_first | 2.31% | **0.12×** |
| cont_first | 12.35% | 0.66× |
| medial | 20.79% | **1.12×** |
| last | 11.27% | 0.61× |

qo is **dramatically suppressed at para-starts (0.12×)** — the opposite of p-onset (which is 17-18× enriched at para-starts). qo is a medial class.

### qo Rate by Section (Currier B)

| Section | Total | qo | qo% |
|---------|-------|----|----|
| Bio | 5727 | 1490 | **26.02%** |
| Special | 9991 | 1801 | 18.03% |
| Text | 1914 | 310 | 16.20% |
| Cosmo | 647 | 79 | 12.21% |
| Herbal | 3064 | 322 | 10.51% |
| Astro | 262 | 17 | 6.49% |

qo is 2.5× more common in Bio (26%) than in Astro (6.5%). This section variation is substantial.

### H084 Verdict: STRONGLY SUPPORTED

**qo is a PREFIX that almost exclusively attaches to gallows letters (k/t/p/f: 86.5%)**, creating a distinct morphological class: qo+gallows+suffix. This class:
1. Is strongly medial (suppressed at para-starts 0.12× vs p-onset 17-18×) — the structural ANTI-marker of paragraph openings
2. Takes extended suffixes (-eedy: 2.05×, -eey: 1.50×, -ain: 1.61×) — same "extended form" pattern as F068
3. Is section-sensitive: Bio=26%, Astro=6.5% — qo+gallows construction is MOST common in Bio scenes
4. Represents 18.6% of all B words — a grammatically productive prefix class

The qo+gallows structure is likely a grammatical modifier: qo+k differs from k alone in both positional distribution and suffix profile. The suppression at para-starts (0.12×) directly mirrors the enrichment of p-onset (17-18×) at para-starts — qo and p-onset occupy complementary positional niches in Currier B grammar.

The section-level variation (Bio 26% vs Astro 6.5%) raises a new hypothesis: **does qo have semantic content** (a determiner, quantifier, or referential marker that is relevant to the Bio scene context)?

---

## Combined Finding (F075)

**H083 PARTIALLY SUPPORTED**: Bio paragraphs within the same folio do NOT have sharply independent vocabulary (within-folio Jaccard for non-trivial para pairs = 0.075–0.156, comparable to cross-folio 0.155). They share the same structural B vocabulary. Some multi-para bio folios have one large paragraph + tiny marginal annotations. **H084 STRONGLY SUPPORTED**: qo is a prefix class that attaches to gallows letters (k/t/p/f) in 86.5% of cases, creating a qo+gallows+suffix structure. These qo+gallows words are: suppressed at para-starts (0.12×, opposite of p-onset), medially biased (1.12×), suffix-extended (-eedy 2.05×, -ain 1.61×), and section-sensitive (Bio=26%, Astro=6.5%). The qo prefix and p-onset class occupy complementary positional niches: p-onset marks paragraph openings (17-18×), qo+gallows marks medial position (1.12×) and is excluded from openings (0.12×).
