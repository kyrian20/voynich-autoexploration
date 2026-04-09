# Experiment exp_056: Three-Slot Word Template Analysis
Date: 2026-04-09

## Question (H067)
Can Voynichese word formation be described as [ONSET] + [ROOT] + [SUFFIX] with non-independent onset × suffix preferences? Which onset-suffix combinations are systematically over- or under-represented?

## Results

### KL Divergence from Independence (Onset × Suffix)

**Currier B:**

| Onset | N | KL from independence |
|-------|---|---------------------|
| d | 1479 | **0.254 bits** |
| cth | 58 | 0.402 bits (small n) |
| sh | 1891 | **0.230 bits** |
| ch | 3247 | 0.131 bits |
| qo | 4019 | 0.134 bits |
| o | 4529 | 0.045 bits |
| y | 857 | 0.072 bits |
| other | 5525 | 0.033 bits |

**Currier A:**

| Onset | N | KL from independence |
|-------|---|---------------------|
| d | 1443 | **0.324 bits** |
| cth | 379 | 0.195 bits |
| qo | 1069 | 0.087 bits |
| sh | 898 | 0.090 bits |
| ch | 1945 | 0.074 bits |
| y | 565 | 0.051 bits |
| o | 1517 | 0.016 bits |
| other | 1991 | 0.009 bits |

**Most onset classes have low KL (0.01–0.25 bits)** — they use suffixes close to the marginal distribution. Onsets and suffixes are NOT strongly determined by each other. The system has onset-sensitive preferences but is not a rigid template.

### Strongest Over-Representations

**Currier B:**
- `d+aiin`: 307 observed vs 142.2 expected — **2.16×** (d-stem strongly prefers -aiin)
- `qo+eedy`: 439 observed vs 213.7 expected — **2.05×** (qo- words prefer extended -eedy)
- `other+iin`: 313 vs 104.6 — **2.99×** (non-classified words that end in -iin)
- `cth+ey`: 12 vs 3.5 — **3.40×** (cth- words in B prefer -ey, but n=58 is small)

**Currier A:**
- `d+aiin`: 461 observed vs 171.1 expected — **2.69×** (even stronger in A)
- `d+ain`: 86 vs 31.9 expected — **2.69×** (d-stem prefers -ain as well)
- `qo+chy`: 102 vs 44.1 — **2.31×** (qo-words prefer -chy more than expected in A)
- `other+iin`: 93 vs 40.8 — **2.28×**

### No Systematic Under-Representations Above Threshold
Only `cth+chy` in A shows clear under-representation (0.19×, exp=15.7, obs=3). No onset class completely avoids any suffix class — consistent with a probabilistic template rather than categorical exclusions.

### Template Coverage

The top 20 onset-suffix combinations account for:
- Currier B: **45.8%** of corpus (top 20 combos)
- Currier A: **50.7%** of corpus (top 20 combos)

Top 6 onset-classes × top 6 suffix-classes cover:
- Currier B: **48.5%** of all tokens
- Currier A: **53.8%** of all tokens

The corpus is not dominated by a single template: the top 20 combos cover ~45-51%, meaning the other ~50% is spread across many lower-frequency combinations.

### Most Common Onset-Suffix Combinations

**Currier B top 5**: other+(none) [7.2%], o+edy [2.6%], o+aiin [2.5%], qo+edy [2.5%], o+(none) [2.5%]
**Currier A top 5**: other+(none) [5.9%], d+aiin [4.7%], ch+ol [3.6%], ch+y [3.4%], ch+(none) [3.0%]

The 'd+aiin' = daiin combination is rank 2 in Currier A (4.7% of all A tokens) — reflecting daiin's dominance in A text.

## Finding (F063)
Voynichese word formation shows onset-sensitive suffix preferences with modest effect sizes: KL from independence ranges 0.01–0.32 bits (most onset classes), with the 'd' stem being the most constrained (0.254 bits in B, 0.324 bits in A). The clearest template: d+aiin is 2.16–2.69× over-represented in both dialects. qo+eedy is 2.05× in B (qo- words prefer the extended -eedy variant). No categorical exclusions exist — all onset-suffix combinations occur. Top 6 onset-classes × top 6 suffix-classes cover ~48-54% of the corpus. The word template is probabilistic (onset-sensitive statistical preferences) rather than categorical (rigid slot-filling). The most rigid template slot is the d-stem + -aiin combination, which appears to function as a grammatical form (analogous to a high-frequency auxiliary verb).

## H067 Verdict: PARTIALLY SUPPORTED
The three-slot word template exists but is probabilistic, not categorical. Onset × suffix are statistically non-independent (KL up to 0.32 bits from independence), but the deviations are modest — no complete onset-suffix exclusions. The 'd+aiin' is the clearest example of a template-driven combination (2.7× over-represented). The top 20 onset-suffix combos account for only ~46-51% of the corpus, consistent with a productive morphological system where the template constrains but doesn't fully determine word forms.
