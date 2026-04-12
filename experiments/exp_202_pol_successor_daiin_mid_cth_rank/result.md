# exp_202: pol-Prefix Successor, daiin@MID Adjacency, cth-Introduction Ranking, cosmo B shedy Restriction
**Date**: 2026-04-11
**Method**: ZL3b paragraph-aware parser; folio-level dialect detection; A=163 paragraphs, B=101 paragraphs, cosmo B=32.

---

## 1. H370: pol-Prefix Successor Profile at B@LF

**pol@LF lines with ≥2 words: n=61; baseline B lines ≥2 words: n=2389**

**Successor onset distribution:**
| Onset | pol_n | pol% | base% | Enrich |
|-------|-------|------|-------|--------|
| p | 1 | 1.64% | 0.29% | 5.59× |
| t | 3 | 4.92% | 1.30% | 3.79× |
| ot | 5 | 8.20% | 3.73% | 2.20× |
| ol | 7 | 11.48% | 6.24% | 1.84× |
| qo | 4 | 6.56% | 4.31% | 1.52× |
| sh | 13 | 21.31% | 16.58% | 1.29× |
| ok | 5 | 8.20% | 7.12% | 1.15× |
| qok | 7 | 11.48% | 12.52% | 0.92× |
| ch | 3 | 4.92% | 19.00% | **0.26×** |
| qot | 0 | 0.00% | 3.14% | 0.00× |
| y | 0 | 0.00% | 2.26% | 0.00× |

**Top specific successor words**: shedy(3), sheedy(2), and 9 other hapax successors.

**By pol-word**: pol(n=11)→sh(4)/ol(3); polaiin(n=6)→ot(2)/ol(1)/ok(1); polchedy(n=5)→qok(2)/sh(1)/ol(1); polor(n=2)→sh(2).

**By section**: stars(n=29): sh(6)/ok(4)/qok(3)/l(3); cosmo(n=29): ol(6)/sh(5)/qok(4)/d(2).

**Comparison to daiin@LF B successors (n=87):**
| Onset | daiin% | pol% | base% |
|-------|--------|------|-------|
| sh | 35.63% | 21.31% | 16.58% |
| ch | 37.93% | **4.92%** | 19.00% |
| qok | 3.45% | 11.48% | 12.52% |
| ol | 4.60% | 11.48% | 6.24% |

**H370 SUPPORTED WITH UNEXPECTED RESULT — pol-prefix opens into sh/ol/ot vocabulary, strongly avoids ch (0.26×)**: pol@LF successor profile is substantially different from daiin@LF. daiin@LF is followed by sh(2.15×)+ch(2.00×)=73.6% combined; pol@LF is followed by sh(1.29×, weak) but ch is STRONGLY DEPLETED (0.26×). pol-prefix LINE_OPEN words do not share daiin's bidirectional sh/ch adjacency. Instead, pol introduces ot/ol/sh/qo vocabulary (all weak-to-moderate enrichments). The top successors (shedy, sheedy) are standard B-edy words. pol-prefix and daiin are FUNCTIONALLY DISTINCT LINE_OPEN words: pol opens into diverse B-vocabulary avoiding ch; daiin specifically opens into sh+ch. This is the first grammatical differentiation within the LINE_OPEN tier.

---

## 2. H371: daiin@MID in A — Predecessor and Successor Onset

**daiin@MID: n=256; daiin@LL: n=106; A adjacent pairs baseline: n=7939**

**Predecessor onset (daiin@MID vs daiin@LL vs baseline):**
| Onset | MID_n | MID% | LL_n | LL% | base% | MID_enr | LL_enr |
|-------|-------|------|------|-----|-------|---------|--------|
| ch | 60 | 23.44% | 34 | 32.08% | 19.94% | **1.18×** | **1.61×** |
| qot | 13 | 5.08% | 7 | 6.60% | 3.04% | **1.67×** | **2.18×** |
| cth | 14 | 5.47% | 4 | 3.77% | 3.30% | **1.66×** | 1.14× |
| qok | 22 | 8.59% | 6 | 5.66% | 5.93% | **1.45×** | 0.95× |
| ot | 15 | 5.86% | 7 | 6.60% | 4.30% | **1.36×** | **1.54×** |
| d | 22 | 8.59% | 12 | 11.32% | 12.61% | 0.68× | 0.90× |
| sh | 19 | 7.42% | 10 | 9.43% | 10.42% | 0.71× | 0.91× |
| ol | 5 | 1.95% | 0 | 0.00% | 2.33% | 0.84× | **0.00×** |

**Successor onset (daiin@MID vs baseline):**
| Onset | MID_n | MID% | base% | Enrich |
|-------|-------|------|-------|--------|
| cth | 34 | 13.28% | 4.36% | **3.05×** |
| d | 50 | 19.53% | 14.35% | 1.36× |
| qok | 17 | 6.64% | 5.27% | 1.26× |
| ch | 48 | 18.75% | 21.85% | 0.86× |
| sh | 14 | 5.47% | 10.01% | **0.55×** |

**Top predecessor words before daiin@MID**: chol(17), daiin(7), chor(7), cthol(5), qokol(5), otchol(4), shol(4), shy(4), ol(4).
**Top successor words after daiin@MID**: cthy(9), daiin(8), cthol(5), dain(5), chy(5), dal(4), dar(4), chol(4).

**H371 SUPPORTED — ch-predecessor of daiin exists at both MID and LL; daiin@MID successor is cth(3.05×)**:

Predecessor: ch-onset is enriched before daiin at BOTH MID (1.18×) and LL (1.61×) positions — the ch adjacency is not LL-exclusive but is position-general, stronger at LL. cth-onset (1.66×) and qot-onset (1.67×) are also enriched before daiin@MID. Top specific predecessors: chol(17) and chor(7) dominate — confirming the ch/cth-onset adjacency at the word level.

Successor: The most striking finding is daiin@MID successor enrichment — cth at 3.05× (n=34). This means the [daiin→cth] construction established in F165 operates primarily as a WITHIN-LINE (MID position) construction. daiin is followed by cthy(9) and cthol(5) specifically. sh is actually DEPLETED after daiin@MID (0.55×), showing that the B-dialect daiin→sh/ch succession (F201) is a dialect-specific, position-specific property, not a cross-dialect adjacency. In A, daiin@MID is followed by cth (not sh/ch).

**Structural interpretation**: In A, daiin functions as a within-line cth-introducer: the dominant A construction is [ch-word][daiin][cth-word] — daiin serves as a grammatical bridge between ch-onset vocabulary and cth-onset vocabulary within a line. The enrichment is position-specific: daiin@LL in A is a ch-word follower but NOT a cth-word introducer (it IS line-final, so no successor within the line). The cross-dialect contrast is: A daiin@MID→cth(3.05×); B daiin@LF→sh/ch(2.15×/2.00×) — entirely different successor profiles.

---

## 3. H372: Unified cth-Introduction Construction Ranking

**A-herbal baseline: bigrams=4562, cth-successor=269 (5.90%)**
**All A-dialect baseline: bigrams=7939, cth-successor=346 (4.36%)**

**Construction ranking (All A-dialect):**
| Construction | n_pred | cth_n | cth% | base% | Enrich |
|-------------|--------|-------|------|-------|--------|
| ychor_stem | 15 | 2 | 13.33% | 4.36% | **3.06×** |
| daiin | 337 | 43 | 12.76% | 4.36% | **2.93×** |
| d_onset | 1001 | 73 | 7.29% | 4.36% | **1.67×** |
| k_onset | 305 | 18 | 5.90% | 4.36% | 1.35× |
| sh_nonshe | 536 | 26 | 4.85% | 4.36% | 1.11× |
| ch_onset | 1583 | 76 | 4.80% | 4.36% | 1.10× |

**A-herbal ranking:**
| Construction | n_pred | cth_n | cth% | base% | Enrich |
|-------------|--------|-------|------|-------|--------|
| ychor_stem | 10 | 2 | 20.00% | 5.90% | **3.39×** |
| daiin | 225 | 37 | 16.44% | 5.90% | **2.79×** |
| d_onset | 646 | 58 | 8.98% | 5.90% | 1.52× |
| k_onset | 218 | 14 | 6.42% | 5.90% | 1.09× |
| sh_nonshe | 384 | 23 | 5.99% | 5.90% | **1.02×** |
| ch_onset | 1021 | 59 | 5.78% | 5.90% | 0.98× |

**Top specific cth-predecessor words (All A, n_total≥5, by enrichment):**
| Word | total | cth_n | cth% | enr |
|------|-------|-------|------|-----|
| chkaiin | 5 | 2 | 40.00% | 9.18× |
| ytchor | 6 | 2 | 33.33% | 7.65× |
| shaiin | 14 | 4 | 28.57% | 6.56× |
| okchol | 7 | 2 | 28.57% | 6.56× |
| okaiin | 33 | 5 | 15.15% | 3.48× |
| ychor | 15 | 2 | 13.33% | 3.06× |
| daiin | 337 | 43 | 12.76% | 2.93× |
| okeol | 32 | 4 | 12.50% | 2.87× |

**H372 SUPPORTED — Ranking: ychor_stem(3.06×) > daiin(2.93×) >> d_onset(1.67×) > k_onset(1.35×) > sh_nonshe(1.11×) ≈ ch_onset(1.10×)**:

1. **ychor_stem is the strongest cth-introducer** (3.06-3.39×) but has tiny n (n=15/10) — unreliable magnitude. Specific ychor-words (ytchor, ychor, tchor, kchor) range 13-33% cth-successor rates.
2. **daiin is the dominant cth-introducer** by both enrichment (2.93×) and absolute n (337 cases, 43 cth-successions). daiin drives the d_onset enrichment — non-daiin d-onset words are near baseline (estimated ~5.0% vs 5.90% baseline in A-herbal).
3. **d_onset enrichment (1.52-1.67×) is primarily driven by daiin**. Other d-onset words (dain, dal, dar, dam, dy) have near-baseline cth rates — they are not cth-introducers.
4. **sh_nonshe enrichment (1.02-1.11×) is NOT SIGNIFICANT within A-dialect**. F201's finding of "sh = 6th cth-introduction construction at 1.72×" was measured vs corpus-wide baseline (including B-dialect and all sections). Within A-herbal where sh→cth bigrams occur (n=23), the enrichment vs A-herbal baseline is only 1.02× — NOISE LEVEL. The sh→cth enrichment in F201 is an artifact of cross-section baseline comparison (A-herbal has ~3.7× more cth than average corpus).
5. **ch_onset is NOT a cth-introducer** (1.10× in A, essentially baseline). F165's "ch-word→cth construction" may refer to specific ch-form words (like chkaiin=9.18×, okchol=6.56×) rather than ch-onset in general.

**KEY CORRECTION**: F201's characterization of "sh-onset as 6th cth-introduction construction (1.72×)" is NOT supported when measured within the appropriate A-dialect control. sh→cth bigrams appear primarily in A-herbal because A-herbal has a high baseline cth rate (~5.9%), not because sh specifically introduces cth. This result should be recorded in open_questions.md or as a narrowing of F201.

---

## 4. H373: cosmo B shedy/chedy — PF-LL Restriction vs WP-LL Elevation

**cosmo B: 32 paragraphs; PF-LL total=32; WP-LL total=747**

| Word | PF_n | PF% | WP_n | WP% | PF/WP enr |
|------|------|-----|------|-----|-----------|
| shedy | 4 | 12.50% | 7 | 0.94% | **13.34×** |
| chedy | 3 | 9.38% | 15 | 2.01% | **4.67×** |
| orol | 2 | 6.25% | 1 | 0.13% | **46.69×** |
| qokaiin | 2 | 6.25% | 5 | 0.67% | 9.34× |
| lshedy | 1 | 3.12% | 1 | 0.13% | 23.34× |
| shey | 0 | 0.00% | 5 | 0.67% | 0.00× |

**cosmo B shedy/chedy position breakdown:**
- shedy: total_LL=11, PF=4 (36.4%), WP=7 (63.6%)
- chedy: total_LL=18, PF=3 (16.7%), WP=15 (83.3%)

**All B shedy/chedy LL breakdown:**
- All B shedy: total_LL=21, PF=4(19.0%), WP=17(81.0%)
- All B chedy: total_LL=41, PF=4(9.8%), WP=37(90.2%)

**Folio detail highlights**: shedy appears at WP-LL in f75r(lines 0,15-chedy,29-chedy), f76r(line 8), f79r(line 0), f80v(line 31), f81r(line 2), f82v(line 22), f83r(line 12); chedy appears at WP-LL in f75r(15,29), f76r(10,31), f76v(30), f77r(4,14), f77v(3,24), f78r(35), f79v(5), f80v(5), f83r(3,22), f84v(22) — chedy appears across nearly ALL cosmo B paragraphs at WP-LL positions.

**H373 SUPPORTED — shedy is PF-restricted (13.34×); chedy is a general cosmo B LL word with weak PF elevation (4.67×)**:

The PF/WP enrichment analysis reveals a sharp distinction:
- **shedy** (PF/WP=13.34×): only 36.4% of cosmo B shedy@LL occurrences are at PF — the remaining 63.6% appear at WP-LL. shedy is elevated specifically at PF-LL, but also appears throughout paragraph interiors. This confirms shedy as a genuine para-closing formula in cosmo B, though not exclusively restricted to PF.
- **chedy** (PF/WP=4.67×): only 16.7% of cosmo B chedy@LL occurrences are at PF. chedy appears 15 times at WP-LL vs 3 times at PF-LL. chedy is a GENERAL cosmo B line-final word that is modestly more common at para-final positions, NOT a para-closing formula.

**CORRECTION TO F201**: F201 characterized both shedy and chedy as "section-level closing formulas" in cosmo B. This overstates chedy. The accurate characterization: shedy (14.72× PF/WP-LL enrichment by F201's measure, 13.34× by within-cosmo B measure) is the primary para-closing formula. chedy (5.15× in F201, 4.67× within cosmo B) is a general cosmo B LL word with mild PF elevation — a "closing word class" rather than a dedicated closing formula. In all-B context: chedy is even less PF-specific (9.8% of chedy@LL are PF), while shedy is 19.0% PF.

---

## Self-Audit

**Target-awareness**: None. All comparisons are corpus-internal (enrichment ratios, onset distributions, position breakdown percentages).

**Feature-destroying implementation**:
- H370: pol-prefix detection = `startswith('pol') and len≥3`. Second-word extraction = `line[1]` when `len(line)≥2`. Correct.
- H371: daiin@MID = positions 1..n-2 where line[j]=='daiin'. Predecessor = line[j-1], successor = line[j+1]. Correct.
- H372: Construction classifiers: ychor_stem = `pred.startswith('ychor')`; daiin = `pred == 'daiin'`; ch_onset = `get_onset(pred) == 'ch'`; k_onset = `get_onset(pred) == 'k'`; sh_nonshe = `get_onset(pred) == 'sh' AND NOT (startswith('she') OR startswith('shee'))`; d_onset = `get_onset(pred) == 'd'`. These are parallel to exp_201's definitions.
- H373: PF-LL = last word of last line; WP-LL = last words of non-last lines with ≥2 words. Direct word lookup in PF and WP counters. Correct.

**Extrapolation claims**:
- H370: "pol opens into diverse B-vocabulary avoiding ch" — based on n=61 pol@LF lines. ch depleted to 0.26× (only 3/61 = 4.9% vs baseline 19.0%) — highly significant at n=61.
- H371: "daiin@MID successor cth=3.05×" — n=34 out of 256 MID occurrences. 13.28% cth vs 4.36% baseline. Reliable.
- H372: "sh_nonshe is not a cth-introducer within A-dialect" — based on sh_nonshe in A-herbal (n=384, cth_n=23, rate=5.99%) vs baseline 5.90%. Difference of 0.09% = noise. Clear.
- H373: "chedy is a general LL word" — based on chedy@WP-LL=15 vs PF-LL=3 in cosmo B. Clear ratio.

**Corrections identified**:
- F201 characterization of "sh = 6th cth-introduction construction (1.72×)": the 1.72× was measured vs corpus-wide baseline. Within A-dialect (correct control), sh_nonshe enrichment = 1.11× (all A) or 1.02× (A-herbal) — at or below significance. F201 finding stands for the corpus-level comparison but the "6th cth-introduction construction" claim requires qualification: sh-onset appears after cth words at a rate that reflects herbal A's high cth density, not a specific sh→cth grammatical construction.
- F201 characterization of cosmo B "shedy+chedy = section-level formula": accurate for shedy (genuinely PF-enriched at 13.34×) but chedy is primarily a general cosmo B LL word, not specifically a para-closer.

---

## CONCLUSION

| H | Result | Key Finding |
|---|--------|-------------|
| H370 | SUPPORTED | pol@LF successor: sh(1.29×, weak), ol(1.84×), ot(2.20×); ch STRONGLY DEPLETED (0.26×); pol ≠ daiin as LINE_OPEN — daiin follows with sh+ch(2.15×/2.00×), pol avoids ch; pol and daiin are functionally distinct LINE_OPEN words |
| H371 | SUPPORTED | A daiin@MID predecessor: ch(1.18×, MID) vs ch(1.61×, LL) — ch-adjacency is position-general, stronger at LL; daiin@MID successor: cth(3.05×)/cthy(9)/cthol(5) — daiin→cth construction is within-line (MID), not line-boundary; A daiin@MID≠B daiin@LF (different successor profiles) |
| H372 | SUPPORTED | cth-intro ranking (all A): ychor_stem(3.06×) > daiin(2.93×) >> d_onset(1.67×, daiin-driven) > k_onset(1.35×) > sh_nonshe(1.11×) ≈ ch_onset(1.10×); sh_nonshe is NOT a significant cth-introducer within A-dialect; F201's 1.72× was vs cross-section corpus baseline (artifact) |
| H373 | SUPPORTED | cosmo B shedy=13.34× PF/WP (genuinely PF-enriched); chedy=4.67× PF/WP (general LL word, weak PF elevation); chedy@WP-LL=15 vs PF-LL=3 (16.7% para-final); F201 overstated chedy as para-closing formula |
