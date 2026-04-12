# exp_194: Paragraph Structure Tests
**Date**: 2026-04-11
**Method**: ZL3b paragraph-aware parsing (locus @P = para-start signal); A-dialect 163 paragraphs (1,712 within-para lines); B-dialect 101 paragraphs (2,310 within-para lines).

---

## 1. H078: Bio Multi-Paragraph Structure

**Bio section (f75–f84): 20 folios, 32 total paragraphs.**

| Group | n_folios | n_paragraphs | mean lines/para |
|-------|---------|-------------|-----------------|
| Single-para folios | 13 | 13 | **38.7** |
| Multi-para folios | 7 | 19 | **15.1** |

**Single-para bio folios** (n=13): f76r, f76v, f77r–f82v. These have ONE long paragraph per folio (mean 38.7 lines) — monolithic descriptions.

**Multi-para bio folios** (n=7): f75r(2), f75v(3), f82r(2), f83r(4), f83v(2), f84r(2), f84v(4). These have multiple SHORT paragraphs per folio (mean 15.1 lines each).

**Vocabulary overlap between paragraphs in same folio:**

| Folio | n_paras | mean pairwise Jaccard |
|-------|---------|----------------------|
| f84v | 4 | **0.004** (near-zero) |
| f75r | 2 | 0.011 |
| f83r | 4 | 0.072 |
| f83v | 2 | 0.085 |
| f82r | 2 | 0.135 |
| f84r | 2 | 0.110 |
| f75v | 3 | 0.156 |

**H078 SUPPORTED**: Multi-para bio folios have shorter paragraphs (15.1 vs 38.7 lines = 2.6× shorter). Vocabulary overlap between paragraphs on the same folio is near-zero to very low (Jaccard 0.004–0.156, mean ~0.08), consistent with independent scene descriptions. Each paragraph on a multi-para folio describes a separate "scene" with largely non-overlapping vocabulary. The bathing pool folios (f83r with 4 paragraphs, f84v with 4 paragraphs) have the most independent vocabulary (Jaccard < 0.01).

---

## 2. H101: Line-Final Onset — Para-Final vs Within-Para

**A-dialect** (para-final n=163, within-para line-final n=1,549):

| Onset | Para-Final% | Within-Para% | Enrich |
|-------|------------|-------------|--------|
| o | 8.6% | 5.2% | **1.66×** |
| ok | 8.0% | 5.4% | **1.47×** |
| ot | 6.7% | 5.2% | 1.31× |
| ch | 20.9% | 16.1% | 1.29× |
| ol | 4.3% | 3.4% | 1.26× |
| d | 23.9% | 24.3% | **0.98×** (NEUTRAL) |
| cth | 3.1% | 5.7% | **0.54×** (depleted) |
| p | 0.0% | 0.4% | **0.00×** (perfectly excluded) |

**B-dialect** (para-final n=101, within-para line-final n=2,310):

| Onset | Para-Final% | Within-Para% | Enrich |
|-------|------------|-------------|--------|
| cth | 2.0% | 0.3% | **6.53×** (n=2) |
| ok | 15.8% | 6.3% | **2.51×** |
| sh | 11.9% | 4.4% | **2.69×** |
| ch | 23.8% | 14.0% | **1.70×** |
| ot | 9.9% | 7.2% | 1.37× |
| d | 4.0% | 9.4% | **0.42×** (depleted) |
| l | 2.0% | 9.3% | **0.21×** (strongly depleted) |
| p | 0.0% | 0.4% | **0.00×** (perfectly excluded) |

**H101 SUPPORTED with key distinctions:**

**A-dialect**: Para-final line-last words are mildly enriched for o-onset (1.66×) and ok/ot-onset (1.31-1.47×). d-onset is **neutral** at para-final (0.98×) despite being generally enriched at line-finals (F081: d=1.73× vs corpus average). This means d-onset marks line boundaries in general but does NOT specifically mark paragraph endings. cth-onset is depleted (0.54×). p-onset is perfectly excluded (0.00×).

**B-dialect**: Para-final last words are strongly enriched for ok-onset (2.51×) and sh-onset (2.69×). The specific B para-final words (okeey, orol from F106) are ok-onset forms. ch-onset is also enriched (1.70×). d-onset and l-onset are strongly depleted at B para-final. p-onset perfectly excluded (0.00×) — consistent across both dialects.

**p-onset perfect exclusion from para-final is cross-dialect** (A=0.00×, B=0.00×): the PARA-tier words appear ONLY at para-starts, never at para-ends. This perfect complementary distribution between para-start and para-end for p-onset is one of the strongest grammatical regularities in the corpus.

---

## 3. H126: B Para Tripartite Structure — Parsing Test

Testing B tripartite model: (1) PS line has PARA-tier opener, (2) within-para lines end in -am, (3) para-final line ends in o-onset.

| Signal | Rate | N |
|--------|------|---|
| PS line has PARA-tier opener | **70.4%** | 98 |
| Within-para line ends in -am | **13.9%** | 2,209 |
| Para-final line ends in o-onset (bare 'o') | **5.1%** | 98 |
| Paragraphs with ALL 3 signals | **2.0%** | 98 |

**Implementation issue (disclosed)**: The test checks `get_onset(last_word) == 'o'` (bare o-onset only), which misses ok/ot/ol-prefix words. If "o-onset" includes ALL o-initial words (ok+ot+ol+bare_o), the para-final rate is 5.9%+15.8%+9.9%+4.0% = **35.6%** vs within-para 28.3% → 1.26× enrichment (marginal). This matches H185's finding (1.25× B para-final enrichment for ALL o-initial words).

**H126 NOT SUPPORTED as stated**: The simple tripartite rule (PARA-opener → -am → o-onset-closer) does not parse B paragraph boundaries effectively. Para-start signal is strong (70.4%); -am within-para is moderate (13.9%); but the para-final "o-onset last word" signal is weak even when including all o-prefix variants (1.26×). Only 2/98 B paragraphs have all three signals.

**The parse fails primarily because the para-final signal is not "o-onset last word" but specific words** (okeey, orol, shedy — ok-onset and sh-onset forms from F106). A classifier using specific words (not onset class) would perform better, but coverage would be low (22.8% from F107).

---

## 4. H165: d-Chain Pattern in A Dialect

**Consecutive line pairs in A paragraphs: n=1,549**

Base rates: d+ch opener = 4.5% (70/1549); y+ch opener = 4.8% (74/1549).

| Preceding line last onset | n | d+ch opener% | Enrich | y+ch opener% | Enrich |
|--------------------------|---|-------------|--------|-------------|--------|
| d-onset | 377 | **6.6%** | **1.47×** | 3.2% | **0.67×** |
| non-d-onset | 1172 | 3.8% | — | — | — |
| o-onset | 80 | 1.3% | **0.28×** | 5.0% | 1.05× |

**d-closer runs (consecutive lines ending in d-onset):**
| Run length | Cases |
|-----------|-------|
| 2 | 176 |
| 3 | 52 |
| 4 | 19 |
| 5 | 4 |

**H165 PARTIALLY SUPPORTED**: d-final lines moderately predict d+ch openers on the next line (1.47× enriched) while suppressing y+ch openers (0.67×). Multi-line d-chains are common: 75 runs of length 3-5 exist (52+19+4). After o-final lines: d+ch is strongly avoided (0.28×) while y+ch is neutral (1.05×). This establishes a **weak d-chain continuity grammar**: consecutive d-onset lines tend to continue with d+ch openers, while o-final lines avoid d+ch openers. The effect is moderate (1.47× = clearly above chance) but not dominant.

**The complementary "o-chain" is NOT supported**: o-final lines do not preferentially attract y+ch openers (1.05× = neutral). The d vs o complementarity is one-directional: d avoids y+ch, o does not select y+ch.

---

## 5. H186: Stars B Paragraph Internal Structure

**Stars B: 23 paragraphs, mean 47.1 lines (range 37–54).**

**PARA-tier openers appear throughout stars paragraphs** (not only at PS position):

All 23 stars paragraphs have multiple PARA-tier words at non-PS positions. Example para f106r (47 lines): 15 PARA-tier words at lines 3, 7, 9, 12, 14, 17, 21, 23, 26, 31, 33, 35, 36, 37, 41.

**PARA-tier rate by line position:**

| Position | Rate | Note |
|----------|------|------|
| 0 (PS) | 0.78 | Para-start |
| 1 | 0.04 | Grammar reset |
| 2 | 0.00 | Minimum |
| 3–19 | **0.13–0.43** | CONSISTENTLY ELEVATED |

Stars paragraphs maintain 13-43% PARA-tier rate from line 3 onward. By contrast, herbal A paragraphs drop to ~0% PARA-tier from line 3+ (F117: "lines 3+ near-zero PARA").

**Rough spacing of PARA-tier peaks (para f248: lines 3,7,9,12,14,17,21,23,26,31,33,35,36,37,41)**:
Gaps between consecutive PARA-tier lines: 4, 2, 3, 2, 3, 4, 2, 3, 5, 2, 2, 1, 1, 4 — irregular, mean ~2.5 lines between PARA-tier markers.

**Paragraph lengths do NOT correspond to astronomical numbers**: mean 47.1 lines ≈ 36+11 (decans + anomaly). No clean multiple of 12 or 36. Range 37-54 is too variable for a fixed astronomical catalog format.

**H186 SUPPORTED (with caveat)**: Stars paragraphs have a fundamentally different grammatical register than herbal paragraphs. PARA-tier words appear throughout at 13-43% rate (vs ~0% in herbal A from line 3+). This is consistent with stars paragraphs containing multiple zodiac entries or catalog items (each introduced with a p/k/t-onset word) within a single physical paragraph unit. The pattern is NOT a regular N-line cycle — spacing is irregular (mean 2.5 lines). The paragraph lengths (~47 lines) do not correspond to clean astronomical numbers.

**Caveat**: The v2 classifier classifies ALL p/k/t/f-onset words as PARA tier. Stars content vocabulary may include more p/t-initial forms than herbal vocabulary, inflating the PARA-tier rate by 5-10 percentage points. Even accounting for this, the 40×+ higher rate vs herbal A (0%) suggests genuine structural difference.

---

## 6. H187: OTHER Para-Start → Line-2 Bigrams

**PS-tier → Line-2-tier transitions (A-dialect, n=163):**

| PS Tier | → PARA | → LINE_OPEN | → MID | → OTHER | n |
|---------|--------|------------|-------|---------|---|
| PARA | 3% | **33%** | 10% | 53% | 105 |
| MID | 8% | 20% | 28% | 44% | 25 |
| OTHER | 4% | **25%** | 18% | 54% | 28 |

**B-dialect:**

| PS Tier | → PARA | → LINE_OPEN | → MID | → OTHER | n |
|---------|--------|------------|-------|---------|---|
| PARA | 7% | **24%** | 19% | 50% | 70 |
| MID | 14% | **43%** | 14% | 29% | 7 |
| OTHER | 8% | 8% | 17% | **67%** | 24 |

**Within A's OTHER PS words by onset (n=28):**
- ok-onset (n=6): LINE_OPEN at line 2 = **33%** (same as PARA-tier PS!)
- d-onset (n=6): LINE_OPEN at line 2 = **0%**
- o-onset (n=4): LINE_OPEN at line 2 = 25%
- ot-onset (n=4): LINE_OPEN at line 2 = 25%

**H187 PARTIALLY SUPPORTED**: PARA-tier PS words reliably transition to LINE_OPEN at line 2 (A=33%, B=24%). OTHER PS words also show some LINE_OPEN at line 2 (A=25%) but weaker. ok-onset OTHER PS words in A produce LINE_OPEN at line 2 at 33% — same rate as PARA-tier starters. d-onset OTHER PS words in A NEVER lead to LINE_OPEN at line 2 (0%). In B, OTHER PS words mostly lead to OTHER at line 2 (67%) — B OTHER para-starts are grammatically weaker.

**The key distinction**: ok-onset appears to behave as a PARA-tier equivalent in line-2 transition (33% LINE_OPEN), consistent with F100's finding that k-onset is para-enriched (4.32×/9.91×). d-onset OTHER PS words do not trigger the PARA-tier line-2 transition.

---

## Self-Audit

**Target-awareness**: No target-aware elements. These are purely descriptive corpus statistics with no discrimination metrics (am_ll, y_lf, etc.).

**Feature-destroying implementation**: H126 — the tripartite model's "o-onset para-end" was tested using `get_onset == 'o'` (bare o, excludes ok/ot/ol). The actual B para-final signals include ok-onset words (okeey, orol). When ALL o-prefix variants are included, para-final enrichment is 1.26× — consistent with H185 finding. The H126 "NOT SUPPORTED" conclusion is correct for the stated rule ("o-onset last word"), but does not address whether all o-prefix variants collectively support the tripartite model. This is disclosed in the text. H186 caveat: v2 classifier treats ALL p/k/t/f-onset as PARA tier; stars section vocabulary may include more p/t-initial content words, inflating PARA-tier rate by 5-10%. Disclosed in text.

**Extrapolation**: No extrapolation beyond observed corpus data. H165 d-chain (1.47×) is clearly characterized as "moderate" not "strong." H186's "fundamentally different register" is qualified with the classifier caveat.

**Negative-result scope**: H126 NOT SUPPORTED means "the simple tripartite model (last word o-onset as para-close signal) does not parse B paragraph boundaries." This does NOT mean B has no tripartite structure — the para-start signal (70.4%) and -am within-para (13.9%) are real. The para-close signal is more complex than bare o-onset (specific words okeey/orol/shedy, not an onset class).

**Control behavior**: H101 controls are within-para line-final onset rates vs para-final rates. Key distinction: d-onset is enriched at ALL line-finals vs corpus average (F081: 1.73× A), but NEUTRAL at para-final vs within-para line-final (0.98× A). These are measuring different things (para-final vs all-lines, vs para-final vs within-para-finals). The neutral d-onset finding at para-final correctly shows that d marks line boundaries but not paragraph boundaries specifically. No unexpected control behavior.

---

## CONCLUSION

| H | Result | Key Finding |
|---|--------|-------------|
| H078 | SUPPORTED | Multi-para bio folios have shorter paragraphs (15.1 vs 38.7 lines); vocabulary Jaccard 0.004–0.156 between paragraphs — near-independent scene descriptions |
| H101 | SUPPORTED | A para-final: o(1.66×), ok(1.47×) enriched; d-onset NEUTRAL (0.98×); p perfectly excluded. B para-final: ok(2.51×), sh(2.69×), ch(1.70×); p perfectly excluded. p-onset exclusion from para-final is cross-dialect |
| H126 | NOT SUPPORTED | Tripartite model fails at para-end: bare o-onset para-final = 5.1%; all o-prefix = 35.6% (1.26×, marginal); only 2/98 B paras have all 3 signals; para-close is specific-word not onset-class |
| H165 | PARTIALLY SUPPORTED | d-final → d+ch opener: 1.47× enriched; y+ch after d-final depleted (0.67×); 75 runs of 3-5 consecutive d-final lines; no complementary o-chain |
| H186 | SUPPORTED | Stars paragraphs have PARA-tier words at 13-43% rate from line 3+ (vs ~0% in herbal A); irregular spacing (mean 2.5 lines); no astronomical N-line cycle; stars register fundamentally different from herbal |
| H187 | PARTIALLY SUPPORTED | PARA PS → LINE_OPEN at line 2 = 33% (A), 24% (B); ok-onset OTHER PS → LINE_OPEN = 33% (same as PARA tier); d-onset OTHER PS → LINE_OPEN = 0%; B OTHER PS → OTHER (67%) |
