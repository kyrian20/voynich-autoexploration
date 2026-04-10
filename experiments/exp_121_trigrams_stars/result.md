# Experiment exp_121: Trigram Phrase Structure (H238) + Stars Catalog Template (H239)
Date: 2026-04-09

## H238: CONFIRMED (PARTIAL) — [W1][daiin][cth-word] Trigrams: W1 Is ch-Onset (1.94×) with -ol Suffix (2.48×); Small n=26; Pre-daiin General Pattern: ch-Onset Dominates (1.33×); d-Onset DEPLETED Before daiin (0.60×); line-First daiin→cth=2.37×

### [W1][daiin][cth-word] Trigram Analysis

In A-dialect text (n=10,760 tokens), there are 304 daiin occurrences (as non-initial words). Of these:
- **26 form trigrams [W1][daiin][cth-word]** = 8.6% of daiin occurrences where a preceding word and cth-following word both exist

This is modest but not random (cth baseline rate ≈ 3.7%, so 8.6% = ~2.3× baseline).

**W1 Onset Distribution:**

| Onset | n | Obs | Base | Enr |
|-------|---|-----|------|-----|
| **ch** | 10 | 0.385 | 0.198 | **1.94×** |
| qot | 2 | 0.077 | 0.027 | **2.82×** |
| d | 5 | 0.192 | 0.150 | 1.28× |
| sh | 2 | 0.077 | 0.093 | 0.82× |
| other | 4 | 0.154 | 0.273 | **0.56×** |

**ch-onset is the most common W1 class** before [daiin][cth], enriched 1.94×. "other" onset is depleted 0.56×. Small n=26 limits confidence.

**W1 Suffix Distribution:**

| Suffix | n | Obs | Base | Enr |
|--------|---|-----|------|-----|
| **-ol** | 9 | 0.346 | 0.140 | **2.48×** |
| **-ey** | 3 | 0.115 | 0.055 | **2.09×** |
| -y | 7 | 0.269 | 0.170 | 1.59× |
| -aiin | 2 | 0.077 | 0.111 | 0.70× |
| -or | 2 | 0.077 | 0.097 | 0.80× |

**-ol suffix is most enriched** (2.48×) in W1 position — consistent with chol (the most common ch+ol word) being the top W1. Top individual W1 words: chy (2), chol (2), shol, chor, cthol — all A-paradigm suffixed words.

### General Pre-daiin Pattern (n=401)

When looking at ALL words preceding daiin in A-dialect (not just trigram context):

| Onset | n | Obs | Base | Enr |
|-------|---|-----|------|-----|
| **ch** | 106 | 0.264 | 0.198 | **1.33×** |
| qot | 19 | 0.047 | 0.027 | **1.74×** |
| cth | 21 | 0.052 | 0.037 | **1.43×** |
| ot | 21 | 0.052 | 0.039 | **1.35×** |
| **d** | 36 | 0.090 | 0.150 | **0.60× ← DEPLETED** |
| s | 10 | 0.025 | 0.030 | 0.84× |

**Key finding**: d-onset words are DEPLETED before daiin (0.60×). ch-onset enriched (1.33×). This is structurally coherent: daiin is a ch-class determiner (ch=1.33×, also cth=1.43× since cth words also precede daiin sometimes). d-onset function words don't stack before daiin.

Top pre-daiin words: **chol (31), shol (9), chor (9), daiin (8), cthy (7), cthol (6), chy (6)** — overwhelmingly A-paradigm ch/sh+ol/or/y suffix words. daiin→daiin chains (8 occurrences) suggest determiner stacking.

### 4-gram [W0][W1][daiin][cth]: n=23, W0 No Clear Pattern

The 4-gram analysis (23 examples) shows W0 has no clear onset preference — W0 is approximately at baseline. This suggests the phrase template is [W1][daiin][cth-noun] (3 words), not longer. No consistent phrase-initial word class found at W0.

### daiin Line-Initial: W2 Distribution

46 lines in A-dialect begin with daiin. The word after line-initial daiin:
- cth: 2.37× enriched (4/46 = 8.7% vs 3.7% baseline) — confirms daiin as cth-determiner even at line start
- sh: 1.86× enriched

### H238 Verdict: CONFIRMED (PARTIAL) — The trigram [W1][daiin][cth-word] exists with n=26 in A-dialect; W1 is preferentially ch-onset (1.94×) with -ol suffix (2.48×), consistent with chol/chy/shol; d-onset is DEPLETED before daiin (0.60×); general pre-daiin: ch-onset=1.33×, top words=chol/shol/chor; phrase template is 3-word [ch-word][daiin][cth-noun], not longer; no consistent W0 pattern (4-gram doesn't extend cleanly)

---

## H239: CONFIRMED (PARTIAL) — Stars Is All-B-Dialect (12/12 folios); Pos-0 Is "other"-Dominated (48%, H Depleted -0.53 bits); d/s-Onset Depleted in 2nd Half (d: 0.75×, s: 0.28×); ot-Onset Enriched in 2nd Half (1.75×); otaiin→ot=3.99× in Stars; NO Repeating Template (All Suffix/Onset Sequences Unique, n=1)

### Stars Section Overview

- **All 12 present stars folios are B-dialect** (A=0, B=12)
- 580 lines, mean 9.73 words/line
- Line lengths clustered at 9-12 words (10=123, 11=135, 12=88)
- Stars is entirely B-dialect — no mixing

### Repeating Template: NOT FOUND

Every suffix sequence and onset sequence is unique (all n=1). **No repeating catalog template** exists at the whole-line level. Stars lines do not follow a fixed word-count or suffix pattern.

However, there IS positional structure:

### Position-Specific Structure

**Suffix entropy by position:**
| Position | H(suffix) | Δ | Top suffix |
|----------|-----------|---|-----------|
| pos 0 | 3.573 | -0.156 | aiin=0.18, other=0.16 |
| pos 1 | **3.481** | **-0.248** | other=0.27, ey=0.11 |
| pos 10 | 3.506 | -0.223 | other=0.25, am=0.13 |
| pos 11 | **2.928** | **-0.801** | other=0.40, am=0.16 |
| pos 12 | **2.533** | **-1.196** | other=0.45, am=0.12 |
| pos 13 | **1.491** | **-2.238** | other=0.64, am=0.18 |

**Line-final positions (11-13) are highly constrained**: H drops sharply. "other" dominates at 40-64%, and **-am appears at 12-18%** at late positions (but very small n). This suggests line endings in stars tend to be "other"-class words (free morphemes not recognized by suffix taxonomy).

**Onset entropy by position:**
| Position | H(onset) | Δ | Top onset |
|----------|----------|---|-----------|
| pos 0 | **2.431** | **-0.532** | other=0.48, d=0.16, s=0.13 |
| pos 1 | 2.775 | -0.188 | other=0.31, ch=0.21, sh=0.18 |
| pos 2-8 | ≈3.0 | ≈0 | (near baseline) |
| pos 11 | 2.298 | -0.666 | other=0.55 |
| pos 12 | **1.624** | **-1.339** | other=0.67 |

**Pos 0 is most constrained** (-0.532 bits): 48% "other", 16% d-onset, 13% s-onset. Stars lines begin with "other" class words or d/s-function words — NOT ch/sh/qok content words.

### Line-Halves: ot Enriched in 2nd Half, s/sh Depleted

| Onset | 1st half rate | 2nd half rate | Enr |
|-------|--------------|--------------|-----|
| **ot** | 0.057 | 0.100 | **1.75×** |
| **qot** | 0.035 | 0.052 | **1.51×** |
| **s** | 0.030 | 0.008 | **0.28× ← STRONGLY DEPLETED** |
| **sh** | 0.100 | 0.058 | **0.58×** |
| d | 0.047 | 0.035 | 0.75× |

**s-onset is concentrated in 1st half** (depleted 0.28× in 2nd half). ot-onset migrates to **2nd half** (1.75×). This suggests stars lines follow a structure: [topic/function words][content cluster][ot-onset phrase-final cluster].

### otaiin in Stars

- **57 total otaiin occurrences** in stars (7.30‰, confirmed from exp_120)
- Distributed across positions 0-10, peak at pos 4-7 (mid-line)
- **After otaiin → ot-onset = 3.99×** (16/53 = 30.2% vs 7.6% baseline) ← confirms exp_120 finding
- After otaiin → "other" depleted (0.62×)
- Sample: `otaiin otaiin`, `otaiin oteedy`, `otaiin otal`, `otaiin otar` — chains of ot-onset words

### ot/ok Run Lengths

Stars has 671 ot/ok-onset runs: 553 length-1, 93 length-2, 20 length-3, 5 length-4. Consecutive ot-pairs appear 93 times (~16% of runs have length≥2), consistent with otaiin acting as a determiner for the following ot-word, producing [otaiin][ot-noun] adjacent pairs.

### Folio-Level Consistency

All 12 stars folios show nearly identical pos-0 structure: "other" dominates (23-31 lines per folio), d-onset second (4-15), s-onset third. f108 is slightly d-dominant (15 d-onset vs 13 other). All consistent — stars is internally homogeneous at the folio level.

### H239 Verdict: CONFIRMED (PARTIAL) — Stars Is Entirely B-Dialect (all 12 folios); NO Repeating Line Template (all sequences unique); BUT Positional Structure Confirmed: Pos-0 Highly Constrained (H=-0.532, other/d/s dominant, NOT ch/sh content words); 2nd-Half ot-Enrichment (1.75×) Suggests [Opener][Content][ot-Phrase-Final] Template; s-Onset Strongly 1st-Half (0.28× in 2nd half); otaiin→ot=3.99× Confirmed as ot-Determiner; Line Endings (-am at pos 11+) Are "Other"-Class Words

---

## Combined Finding (F128)

**H238 CONFIRMED PARTIAL (F128)**: The trigram [W1][daiin][cth-word] exists in A-dialect (n=26); W1 is preferentially ch-onset (1.94×) with -ol suffix (2.48×). The full phrase structure is: [ch-word with -ol/-y/-ey suffix][daiin][cth-noun]. However, the pre-trigram word (W0) shows no consistent onset class — the template appears to be exactly 3 words, not 4. Pre-daiin general pattern (n=401): ch=1.33×, d-onset DEPLETED (0.60×). Top pre-daiin words: chol (31), shol (9), chor (9). The structural model is: **chol/shol/chor → daiin → cthy/cthor/cthol** = an A-dialect NP template: [ch-paradigm modifier][determiner daiin][cth-head noun].

**H239 CONFIRMED PARTIAL (F128)**: Stars section is entirely B-dialect (12/12 folios = 100%). No repeating whole-line suffix/onset template exists (all 580 lines are unique). However, stars lines have consistent positional structure: pos-0 is highly constrained (H=-0.532 bits; 48% "other", 16% d-onset, 13% s-onset), contrasting with ch/sh content words which dominate mid-line. Second half of lines: ot-onset enriched (1.75×), s-onset strongly depleted (0.28×). Line endings (pos 11+): "other"-class dominant with -am suffix. The pattern suggests: **[d/s-function][ch/sh-content cluster][ot-phrase-final cluster][other-line-closer]**. otaiin→ot=3.99× in stars (confirmed). Stars lines are catalog entries that start with function/topic words, develop through B-content cluster, and close with ot-onset nominal phrases.
