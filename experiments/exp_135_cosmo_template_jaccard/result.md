# exp_135: Cosmo Line-Element Template + Cross-Section Jaccard Matrix
**Date**: 2026-04-09
**Hypotheses**: H264 (Cosmo Line Template), H265 (Cross-Section Jaccard Matrix)
**Status**: BOTH CONFIRMED

---

## H264: Cosmo Line-Element Template — CONFIRMED

Cosmo has a formal positional grammar analogous to Stars', with distinct opener, second-slot, and closer enrichments.

### Cosmo Line Template
| Position | Enriched Onsets | Depleted Onsets | Notes |
|----------|----------------|-----------------|-------|
| FIRST    | p(4.67×), s(4.10×), y(3.78×), t(2.59×), d(1.81×) | ch_e(0.23×), ot(0.23×), sh(0.47×) | Strong functional-word openers |
| SECOND   | sh(1.75×), qo(1.50×), ch_e(1.26×) | — | sh as second-slot filler (same as Stars) |
| MID      | ot(1.22×), ch(1.19×), ok(1.18×), ch_e(1.17×) | — | Content-word body |
| LAST     | r(2.19×), l(2.16×), ol(1.69×), d(1.40×), other(1.52×) | sh(0.34×), qok(0.59×) | -l/-r terminal onsets |

### Cosmo Suffix Grammar
- **LAST position**: -am (7.87×!), -dy (2.22×), -y (2.04×) enriched at line end
- **FIRST position**: -eey (1.29×), -ol (1.25×), -aiin (1.27×), -ain (1.09×) enriched at line start

### Stars Template (reference, from F138)
| Position | Enriched Onsets |
|----------|----------------|
| FIRST    | s(5.78×), y(4.80×), d(3.56×), t(1.91×), cth(1.89×) |
| SECOND   | sh(1.93×) |
| LAST     | r(2.46×), l(1.45×), other(1.55×) |
| LAST suffix | -am (7.48×) |

### Key Structural Parallels (Cosmo ≈ Stars)
1. **OPENER class**: s/y/d/t dominate first position in both (cosmo adds p; stars adds cth)
2. **sh = SECOND SLOT**: 1.75× in cosmo, 1.93× in stars — shared positional grammar
3. **-am CLOSER**: 7.87× in cosmo, 7.48× in stars — both sections end lines with -am at nearly identical enrichment rates
4. **r/l LAST onsets**: r(2.19× cosmo, 2.46× stars), l(2.16× cosmo, 1.45× stars)

### Cosmo-Specific Features
- **p = rare but strong opener**: 4.67× enrichment at first (absent from stars template)
- **t = stronger opener in cosmo**: 2.59× vs 1.91× in stars
- **-y/-dy closers**: cosmo has -y(2.04×) and -dy(2.22×) at line end, supplementing -am; stars has only -y(1.60×)
- **cth absent from cosmo first**: consistent with B-herbal/cosmo depletion of cth (confirmed F139)

### Top Cosmo Line-Opening Words
qokeedy(24), qokain(22), qokedy(21), dshedy(18), daiin(17), sol(15), saiin(15)

### Top Cosmo Line-Closing Words
oly(20), ol(17), qoky(14), dy(12), chedy(10), oldy(9), lchedy(8), daiin(8)

**Cosmo template**: **[s/y/p/t/d OPENER (2.6–4.7×)][sh 2nd (1.75×)][l/r/ol CLOSER][-am/-y/-dy SUFFIX CLOSER]**

---

## H265: Cross-Section Vocabulary Jaccard Matrix — CONFIRMED

### 5×5 Jaccard Similarity Matrix
|         | herbal | astro  | cosmo  | pharma | stars  |
|---------|--------|--------|--------|--------|--------|
| herbal  | 1.0000 | 0.0461 | 0.1022 | 0.1209 | 0.1199 |
| astro   | 0.0461 | 1.0000 | 0.0508 | 0.0725 | 0.0434 |
| cosmo   | 0.1022 | 0.0508 | 1.0000 | 0.1077 | **0.1371** |
| pharma  | 0.1209 | 0.0725 | 0.1077 | 1.0000 | 0.1106 |
| stars   | 0.1199 | 0.0434 | **0.1371** | 0.1106 | 1.0000 |

### Key Findings

**1. Cosmo-Stars is the closest pair overall (J=0.1371)** — consistent with shared positional grammar (H264), both being B-dialect dominant, and parallel onset profiles.

**2. All pairwise similarities are low (0.04–0.14)** — sections are highly distinct vocabulary communities.

**3. Astro is the most isolated section** (smallest Jaccard with all others): astro-stars=0.0434 (lowest non-diagonal value), astro-herbal=0.0461.

**4. Herbal-pharma ≈ herbal-stars** (0.1209 vs 0.1199) — marginally true but essentially equivalent.

### Section Vocabulary Sizes
| Section | Types | Exclusive Types | % Exclusive |
|---------|-------|-----------------|-------------|
| herbal  | 3517  | 2488            | 70.7% |
| stars   | 3459  | 2350            | 67.9% |
| cosmo   | 1790  | 1015            | 56.7% |
| pharma  | 1553  | 845             | 54.4% |
| astro   | 341   | 132             | 38.7% |

**Astro has the lowest exclusive fraction (38.7%)** — most astro words are shared with other sections, consistent with astro being heterogeneous (f67=true astro, f68/f70=A-herbal-like).

### Universal Vocabulary (all 5 sections)
71 word types appear in all 5 sections. Top 5:
- **daiin** (641 total): onset=d, the most universal word
- **ol** (318): onset=ol
- **chol** (290): onset=ch
- **qokeey** (276): onset=qok
- **chey** (258): onset=ch_e

All 71 universal words are among the most frequent corpus items — the "function word" core.

### Absent-from-One-Section Analysis
- **Absent from herbal: 0 types** — any word in 4 other sections is also in herbal (herbal is superset by coverage)
- **Absent from astro: 162 types** — astro missing many common words (small section)
- **Absent from cosmo: 31 types** — includes chor, sho, cthy, cthol, cheo (cth/ch words)
- **Absent from pharma: 12 types** — includes qotal, chal, otchey
- **Absent from stars: 5 types** — dchy, daly, cphey, alchey, sam (stars is superset by coverage after herbal)

### B-Dialect Jaccard
Cosmo-Stars similarity is even higher in B-dialect alone: **J=0.1523** (vs 0.1371 full corpus).
Herbal-Cosmo also high in B: **J=0.1512**.

Cosmo's B-dialect vocabulary is strongly tied to both stars and herbal, suggesting B-cosmo may be scribal output bridging B-herbal insertions and the stars section.

---

## Summary of New Findings (F142)

1. **Cosmo template = Stars template**: Both share [s/y/d/t OPENER][sh SECOND][-am LAST] grammar; cosmo adds -y/-dy closers and depletes cth at first (consistent with B-dialect)
2. **-am CLOSER is pan-section**: 7.87× in cosmo, 7.48× in stars — previously thought stars-exclusive (F138), now revised
3. **Cosmo-Stars is the most similar pair (J=0.1371)** supporting a B-dialect affinity cluster
4. **71-word universal vocabulary core** dominated by d-onset and ol words
5. **cth absent from cosmo** (0 cthol/cthy in cosmo vocabulary) — consistent with B-herbal cth depletion

---

## Hypotheses Spawned
- **H266**: Is -am a SENTENCE-FINAL rather than LINE-FINAL marker? (occurs at 7.87×/7.48× enrichment in both cosmo and stars — test whether -am concentrates at paragraph-final lines too)
- **H267**: Does the 71-word universal core constitute a closed functional vocabulary? (test whether these 71 words behave differently from section-exclusive words in terms of positional distribution)
- **H268**: What is the positional distribution of the 31 cosmo-absent words (chor, sho, cthy, cthol, cheo)? Are they concentrated in specific folio ranges indicating scribe-specific vocabulary?
