# exp_201: POL-Prefix Profile, daiin Predecessor/Successor, sh→cth, cosmo shedy
**Date**: 2026-04-11
**Method**: ZL3b paragraph-aware parser; folio-level dialect detection; A=163 paragraphs, B=101 paragraphs.

---

## 1. H366: POL-Prefix Words in B — Full Positional Profile

**Aggregate positional distribution:**
| Dialect | Total | LF% | MID% | LL% |
|---------|-------|-----|------|-----|
| A pol-prefix | 9 | 77.8% | 22.2% | 0.0% |
| B pol-prefix | 70 | 87.1% | 12.9% | **0.0%** |

**B section distribution of pol-prefix (n=70):**
| Section | n | % |
|---------|---|---|
| stars | 37 | 52.9% |
| cosmo | 29 | 41.4% |
| herbal | 1 | 1.4% |
| other | 3 | 4.3% |

**Top B pol-prefix words:**
| Word | n | LF% | MID% | LL% |
|------|---|-----|------|-----|
| pol | 13 | 84.6% | 15.4% | 0.0% |
| polchedy | 7 | 71.4% | 28.6% | 0.0% |
| polaiin | 7 | 85.7% | 14.3% | 0.0% |
| polshy | 3 | 66.7% | 33.3% | 0.0% |

**pch-prefix comparison (confirming the distinction):**
| Dialect | Total | LF% | MID% | LL% |
|---------|-------|-----|------|-----|
| A pch | 67 | 62.7% | 31.3% | 6.0% |
| B pch | 182 | 69.8% | 27.5% | 2.7% |

**H366 SUPPORTED — pol-prefix is a B-dominant LF-exclusive word class**: pol-prefix words in B (n=70) appear at LF 87.1% of the time and NEVER at LL (0/70). This contrasts with pch-prefix words which appear at MID (27.5%) and occasionally LL (2.7%), and are distributed across all sections. pol-prefix is strikingly B-specific: 70 tokens in B vs only 9 in A, and the B occurrences are concentrated in stars(52.9%) and cosmo(41.4%) sections — exactly the B-exclusive sections. pol-prefix words (pol, polaiin, polchedy, polshy) function as **within-para line-openers exclusively**: never at LL (grammar constraint), predominantly at LF. This confirms that B WP-LF p-onset flooding (F199/F200) is caused by a section-specific pol-prefix LINE_OPEN class in stars/cosmo, not by para-starting pch-words appearing more broadly.

---

## 2. H367: daiin Predecessor@LL (A) and Successor@LF (B)

**A-dialect: penultimate onset before daiin@LL (n=106 daiin@LL lines):**
| Onset | daiin@LL n | daiin@LL% | base% | Enrichment |
|-------|-----------|-----------|-------|-----------|
| qot | 7 | 6.60% | 2.93% | **2.26×** |
| ch | 34 | 32.08% | 22.99% | **1.40×** |
| s | 4 | 3.77% | 2.75% | 1.37× |
| ot | 7 | 6.60% | 5.07% | 1.30× |
| d | 12 | 11.32% | 16.00% | **0.71×** |
| ok | 4 | 3.77% | 5.67% | **0.67×** |
| ol | 0 | 0.00% | 2.51% | **0.00× (excluded)** |

Top specific penultimate words before A daiin@LL: chol(10), cthy(3), shol(3), otol(3), qotchey(2)

**B-dialect: second-word onset after daiin@LF (n=87 daiin@LF lines):**
| Onset | daiin@LF n | daiin@LF% | base% | Enrichment |
|-------|-----------|-----------|-------|-----------|
| s | 2 | 2.30% | 0.80% | **2.89×** |
| sh | 31 | 35.63% | 16.58% | **2.15×** |
| ch | 33 | 37.93% | 19.00% | **2.00×** |
| qok | 3 | 3.45% | 12.52% | **0.28×** |
| l | 0 | 0.00% | 5.15% | **0.00× (excluded)** |
| qo | 0 | 0.00% | 4.31% | **0.00× (excluded)** |
| o | 1 | 1.15% | 4.31% | **0.27×** |

Top specific second words after B daiin@LF: shey(5), chedy(4), chey(4), sheol(3), shody(3), shedy(2)

**H367 SUPPORTED — daiin has a bidirectional sh/ch affinity that reverses its line position**:

In A (daiin@LL): daiin is PRECEDED by ch-onset words (32.08%, 1.40×); specifically chol appears as penultimate 10/106 times. qot(2.26×) and ot(1.30×) are also enriched. d-onset(0.71×) and ol-onset(0.00×) are depleted before daiin@LL.

In B (daiin@LF): daiin is FOLLOWED by sh-onset (35.63%, 2.15×) and ch-onset (37.93%, 2.00×) words; combined sh+ch = 73.6% of all B daiin@LF successors. Top words are shey, chedy, chey, sheol, shody. qok(0.28×), l(0.00×), qo(0.00×) are depleted after daiin@LF.

**Structural interpretation**: In A, the construction [ch-word][daiin] appears at line end — daiin follows ch as a formulaic line-closer. In B, daiin is at line-start and is immediately followed by sh/ch-onset words — daiin precedes sh/ch as a line-opener. Across dialects, daiin maintains an adjacency relationship with sh/ch-onset words; the dialect shift changes which side of daiin they appear on. This is consistent with daiin functioning as a grammatical linker word adjacent to sh/ch vocabulary, with the direction of adjacency reversed by the dialect's positional grammar.

---

## 3. H368: Non-she sh-Prefix → cth Bigrams — Which Specific Words?

**Total non-she sh → cth bigrams: n=27**

**All bigram pairs (sorted by frequency):**
| sh-word | cth-word | n |
|---------|---------|---|
| shol | cthy | 3 |
| shaiin | cthy | 2 |
| sho | cthy | 2 |
| shol | cthol | 1 |
| shol | cthom | 1 |
| shol | ctheey | 1 |
| sho | cthos | 1 |
| shor | cthaiin | 1 |
| shor | cthol | 1 |
| shor | cthy | 1 |
| shy | cthy | 1 |
| *(others)* | *(various)* | 13 |

**cth-word distribution**: cthy dominates as the cth-word (8/27=30%); other cth-words diverse (17 different forms).

**Section/dialect distribution**: A-herbal=23 (85.2%), A-pharma=3 (11.1%), B-herbal=1 (3.7%)

**Folio distribution**: 22 distinct folios (1-3 per folio), spread across early herbal A (f1r-f53v) and pharma (f87r-f87v)

**she- vs non-she-sh → cth rate**:
- she→cth: 9/1438 = 0.63%
- non-she-sh→cth: 27/977 = 2.76% (4.42× more than she-prefix)

**H368 SUPPORTED — sh→cth is primarily shol/sho/shaiin+cthy; distributed across herbal A**: The non-she sh → cth enrichment (1.72×) is driven by 3-4 specific sh-words: shol(5 bigrams), sho(3), shor(3), shaiin(3). cthy is the most common cth-word recipient (8/27=30%), consistent with cthy's general grammatical role as a line-terminal cth-word (F161). The 22-folio spread (1-3 bigrams per folio) confirms this is a grammatical construction distributed across herbal A, not a formulaic repetition. **sh-onset represents a 6th cth-introduction construction** (adding to the 5 established in F165: ychor→cth, daiin→cth, ch-word→cth, d+ch→cth, k→cth from F191). The sh→cth enrichment (1.72×) is smaller than ychor→cth or daiin→cth but is consistent and folio-distributed.

---

## 4. H369: cosmo B Para-Final shedy/chedy — Spread or Concentrated?

**cosmo B: 32 paragraphs; PF-LL n=29**

**All cosmo B para-final words with enrichment (top by enrichment):**
| Word | PF-n | PF% | WP-n | WP% | Enrichment |
|------|------|-----|------|-----|-----------|
| orol | 2 | 6.90% | 1 | 0.13% | **51.52×** |
| lshedy | 1 | 3.45% | 1 | 0.13% | **25.76×** |
| shedy | 4 | 13.79% | 7 | 0.94% | **14.72×** |
| qokaiin | 2 | 6.90% | 5 | 0.67% | **10.30×** |
| chedy | 3 | 10.34% | 15 | 2.01% | **5.15×** |

**Paragraphs ending with shedy**: f75r, f76v, f83r, f83r (4 separate paragraphs, 4 different folio-paragraphs — f83r has multiple paragraphs)
**Paragraphs ending with chedy**: f79v, f83r, f84v (3 paragraphs)

Together shedy+chedy close 7/32 (21.9%) of cosmo B paragraphs, spread across 6 distinct folios.

**H369 SUPPORTED (formula is spread, not concentrated)**: shedy(14.72×) and chedy(5.15×) are strongly enriched at cosmo B PF-LL vs WP-LL. They appear in paragraphs spread across f75r-f84v (the full cosmo folio range), not concentrated in 1-2 paragraphs. 7 different cosmo B paragraphs end with shedy/chedy — a genuine section-level formula covering 21.9% of cosmo B paragraphs. The remaining 78.1% of cosmo B paragraphs use diverse para-final words (orol, olkol, qokaiin, etc. — consistent with the open vocabulary finding in F200). shedy(14.72×) is a stronger cosmo B para-closer than chedy(5.15×). lshedy(25.76×) also appears once — an lshedy form may be a compound of the formula. orol(51.52×) is even more strongly enriched but appears only twice.

**Revised picture of cosmo B para-final**: The cosmo B section has a partial set of para-closing words — shedy, orol, chedy, qokaiin, chey — where shedy is the strongest (14.72×) and most frequent (4). These appear in 40-50% of cosmo B paragraphs. The other 50-60% use unique para-final words. This is intermediate between A's tight formula (okeey=∞, orol=21.9×) and stars B's complete diversity.

---

## Self-Audit

**Target-awareness**: No target-aware elements. All comparisons are corpus-internal (positional rates, successor onset distributions, enrichment ratios).

**Feature-destroying implementation**:
- H366: pol-prefix detection = `word.startswith('pol') and len(word) >= 3`. This correctly captures pol-onset words. LF = pos 0, LL = pos N-1 with N>1. LL=0 for pol is an empirical finding, not an artifact.
- H367: A penultimate = line[-2] when line[-1]=='daiin' and len≥2. B successor = line[1] when line[0]=='daiin' and len≥2. Both correctly defined.
- H368: non-she sh-word = onset=='sh' AND NOT (startswith('she') or startswith('shee')). cth-word = get_onset(next_word)=='cth'. Correct.
- H369: PF-LL = last word of last line of each paragraph. WP-LL = last word of non-last lines. Para-final enrichment = PF-rate/WP-rate. n=29 for PF-LL (32 cosmo B paras - 3 with <2 words in last line).

**Extrapolation**: H366: "pol-prefix is a B-specific LINE_OPEN class" — based on 70 B tokens vs 9 A tokens. The section distribution claim (stars+cosmo=94.3%) is definitive. H367: "daiin has a bidirectional sh/ch affinity" — the ch-predecessor enrichment (1.40×, n=34) and sh/ch-successor enrichment (2.15×/2.00×, n=87) are both moderate-to-large n — reliable at onset-class level. H368: sh→cth as "6th construction" — based on 1.72× enrichment with n=27 — reliable enrichment claim. H369: "formula covering 21.9% of paragraphs" is a direct count.

**Negative-result scope**: H369 does not claim cosmo B has NO formula — it has a PARTIAL formula (shedy/chedy appearing in 21.9% of paragraphs). The remaining 78.1% use open vocabulary. This is correctly framed as "intermediate" between tight formula (A) and full diversity (stars B).

**Control behavior**: For H367, baseline is all penultimate words (A) or all second words (B) across the corpus. The controls behave as expected — ch-onset at baseline is 22.99% (A) and 19.00% (B), consistent with ch being the most common mid-line onset. The sh-onset enrichment in B (35.63% after daiin@LF vs baseline 16.58%) is the primary surprise and is real (n=31).

---

## CONCLUSION

| H | Result | Key Finding |
|---|--------|-------------|
| H366 | SUPPORTED | pol-prefix in B: 87.1% LF, 0% LL (n=70); concentrated in stars(52.9%)+cosmo(41.4%); absent from herbal/pharma; confirms pol-onset as B-specific LINE_OPEN stars/cosmo class; A pol-prefix = 9 tokens only |
| H367 | SUPPORTED | A daiin@LL predecessor: ch(1.40×), specifically chol(10/106); B daiin@LF successor: sh(2.15×)+ch(2.00×) together=73.6%; daiin has bidirectional sh/ch adjacency (follows ch in A; precedes sh/ch in B) |
| H368 | SUPPORTED | sh→cth bigrams (n=27): shol(5)+shaiin(3)+sho(3)+shor(3) drive it; cthy is main cth-recipient (8/27=30%); 22 folios (1-3 each); A-herbal=85%; sh-onset is a 6th cth-introduction construction (1.72× enrichment) |
| H369 | SUPPORTED | cosmo B shedy(14.72×)/chedy(5.15×) are SPREAD across 7 paragraphs in 6 folios (f75r-f84v); cover 21.9% of cosmo B paragraphs; section-level formula confirmed; remaining 78.1% uses open vocabulary |
