# Experiment exp_129: p+r Line Bracket (H256) + raiin vs aiin (H257)
Date: 2026-04-09

## H256: NOT CONFIRMED — p+r Co-occurrence Is Only 1.29× Enriched vs Independence (13 Observed vs 10.1 Expected); p and r Do NOT Form a Mandatory Line-Bracket; B-Lines: p-start=12.0%, r-end=3.5%, Both=0.5%; Stars/Cosmo Show Same Weak Trend

### p+r Co-occurrence (B-dialect)

| Lines | Count | Rate |
|-------|-------|------|
| Total B-dialect lines (n≥2) | 2,433 | — |
| With p-start | 293 | 12.0% |
| With r-end | 84 | 3.5% |
| With BOTH | 13 | 0.5% |

**Independence test**: P(p-start)=0.120 × P(r-end)=0.035 = 0.0042 expected = **10.1 lines** by chance. Observed: **13 lines**. Enrichment = **1.29×** — marginal, not statistically compelling.

By section (B-dialect):
- Stars: p-start=14.7%, r-end=4.2%, both=0.6% (7/1083 lines)
- Cosmo: p-start=8.9%, r-end=4.4%, both=0.6% (5/779 lines)
- Herbal: p-start=11.9%, r-end=0.7%, both=0.4% (1/278 lines)

Sample p+r lines are structurally interesting but rare:
- f80 [cosmo]: `pchedy dolfchedy qokeedy qotedy qotolfchedy roly`
- f113 [stars]: `polchor cheody qotedy lkeches keeol lkcheol lkchedy kotchy lpchedy qopchedy ro`
- f115 [stars]: `polor sheedy qoteedy qokechy lraly shey sheot shedy chteey lky raram`

### H256 Verdict: NOT CONFIRMED — p and r do NOT form a mandatory line-bracket pair; 1.29× enrichment (13 vs 10.1 expected) is not statistically significant; p-start and r-end are independently distributed within B-dialect lines; p and r are each individually enriched at their respective positions (p=line-start, r=line-end) but do not preferentially co-occur in the same lines; the "line-bracket" model is incorrect — p and r are independent positional markers

---

## H257: CONFIRMED PARTIAL — raiin and aiin Differ in Section/Dialect Distribution (raiin=B-Stars/Cosmo 85%, aiin=More Distributed); Pre-raiin: s-Onset=3.25× (STRONGEST PREDICTOR), l=1.73×, ch=1.68×; Post-raiin: ot=2.36×, sh=1.81×; raiin Is NOT the B-Stars Equivalent of daiin (No Strong Post-raiin cth Enrichment)

### raiin vs aiin Profile

| Metric | raiin | aiin |
|--------|-------|------|
| n | 61 | 462 |
| B-dialect | 93.4% | 78.6% |
| Stars | **63.9%** | 45.5% |
| Cosmo | 21.3% | 8.7% |
| Herbal | 3.3% | **21.4%** |
| Line-start | 0.0% | 1.3% |
| Line-mid | 90.2% | 88.5% |
| Line-end | 9.8% | 10.2% |

**Key difference**: raiin is almost entirely B-stars/cosmo (85.2%), while aiin is distributed across stars (45.5%), herbal (21.4%), and cosmo (8.7%). raiin is the **B-stars/cosmo particle form** of aiin.

### Pre-Word Onset Enrichment vs Corpus Baseline

| Onset | raiin_pre | aiin_pre |
|-------|-----------|---------|
| **s** | **3.25×** | 2.08× |
| ol | 1.83× | 1.42× |
| l | 1.73× | 1.39× |
| ch | 1.68× | 0.92× |
| qok | 1.07× | 0.29× |
| d | 0.17× | 0.67× |
| **other** | **0.13×** | **2.21×** |

**raiin is strongly preceded by s-onset (3.25×)**. s-onset = "extreme topic opener" (F126/F130, H=1.449, 48.5% first-line position). The [s-word][raiin] pattern in B-stars suggests raiin appears at the start of content sequences following topic-opening s-words.

**raiin is NOT preceded by "other"-onset words (0.13×)**, while aiin IS (2.21×). aiin commonly follows particle words and miscellaneous forms; raiin does not. This is the most discriminating pre-context difference.

**ch-onset is enriched before raiin (1.68×)** but not before aiin (0.92×). In B-stars, ch-onset words (content words) precede raiin.

### Post-Word Onset Enrichment vs Corpus Baseline

| Onset | raiin_post | aiin_post |
|-------|------------|---------|
| ot | **2.36×** | 1.88× |
| sh | 1.81× | 0.96× |
| ch | 1.75× | 1.51× |
| ok | 0.30× | **2.70×** |

**Post-raiin: ot-onset=2.36×** (strongest); **post-aiin: ok-onset=2.70×**. raiin is followed by ot-onset words; aiin is followed by ok-onset words. This mirrors the dialectal split: ot=B-paradigm nominal class, ok=o-prefixed k-stem. Both are enriched but in different ratios.

raiin is **NOT followed by cth-onset** (post-raiin cth not in top 8). daiin→cth=4.89× (F125) — daiin is the A-dialect pre-cth determiner. raiin does NOT have this function. raiin is a B-stars particle that precedes ch/sh/ot-content, not cth-nouns.

### raiin vs aiin Top Post-Words

Post-raiin: chey(3), qokeey(2), ar(2), otedy(2) — B-paradigm content words
Post-aiin: ol(10), chey(10), okal(9), okaiin(8), otar(8) — function words and B-content

### Structural Interpretation

- **aiin**: A general medial particle across A/B dialects and sections; precedes ok-class words (2.70×); preceded by "other" (misc particles, 2.21×); the most general particle.
- **raiin**: B-dialect stars/cosmo particle; preceded by s-onset (3.25×=topic openers), ch-onset (1.68×); followed by ot-class words (2.36×), sh-class (1.81×). Functions as a medial particle in B-stars syntactic context.

The relationship: raiin = r-prefix + aiin. Since r-prefix marks a B-stars particle form, raiin = "the B-stars/cosmo form of the aiin particle". Both are medial particles but in different syntactic environments.

### H257 Verdict: CONFIRMED PARTIAL — raiin and aiin differ significantly in section/dialect (raiin=B-stars/cosmo 85%; aiin=distributed); pre-raiin: s-onset=3.25× (strongest predictor), l=1.73×, ch=1.68×; pre-aiin: other=2.21× (not pre-raiin); post-raiin: ot=2.36×, sh=1.81×; post-aiin: ok=2.70×; raiin is NOT a pre-cth determiner like daiin — it's a B-stars medial particle appearing after s-topic-openers and before ot/sh content words; aiin is a more general medial particle; the r-prefix transforms aiin into a B-stars-specific particle form with altered syntactic environment

---

## Combined Finding (F136)

**H256 NOT CONFIRMED (F136)**: p and r do NOT form a mandatory line-bracket pair in B-dialect. Co-occurrence is only 1.29× enriched vs independence baseline (13 observed vs 10.1 expected in B-dialect). p-start and r-end are independent positional phenomena that happen to be concentrated in the same lines by chance at near-random rates. The "p-opener / r-closer = complete line frame" model is incorrect.

**H257 CONFIRMED PARTIAL (F136)**: raiin = B-stars/cosmo medial particle (63.9% stars, 21.3% cosmo, 93.4% B-dialect). Key context differences from aiin: pre-raiin = s-onset (3.25×, topic openers), ch-onset (1.68×), NOT "other"-onset (0.13×); post-raiin = ot-onset (2.36×), sh-onset (1.81×). raiin is NOT the B-stars equivalent of daiin (no strong cth enrichment after raiin). raiin functions as a B-stars medial particle in the pattern [s-topic-opener][B-content][raiin][ot/sh-content], analogous to aiin's role in A-dialect content sequences but with different onset class targets.
