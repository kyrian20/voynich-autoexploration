# Experiment exp_117: 'Other' Suffix Category (H228) + Para Cohesion (H229)
Date: 2026-04-09

## H228: CONFIRMED — 'Other' = Four Distinct Categories: (1) Free Standalone A-Morphemes (ol/aiin/or/ar/al Top 5), (2) Unrecognized -am/-air Suffixes, (3) Short Truncated Forms (-cho/-sho/-eo), (4) Hapax Forms; -am = 9.2% of Other; -air = 5.6%; Extending Suffix List With -am/-air Would Reduce 'Other' by ~15%

### 'Other' Category Composition (6,223 tokens, 20.6% of body)

**Top 20 'other' words reveal four categories:**

| Rank | Word | n | Category | Explanation |
|------|------|---|----------|-------------|
| 1 | ol | 476 | Standalone A-morpheme | The -ol suffix appearing as a free word (no stem prefix) |
| 2 | aiin | 394 | Standalone A-morpheme | Free occurrence of -aiin |
| 3 | or | 300 | Standalone A-morpheme | Free -or |
| 4 | ar | 268 | Standalone A-morpheme | Free -ar |
| 5 | al | 193 | Standalone A-morpheme | Free -al |
| 6 | sho | 108 | Short truncated | sh + -o (no recognized suffix) |
| 7 | ain | 100 | Standalone | Free -ain |
| 8 | dair | 75 | Missing suffix -air | d + -air |
| 9 | cho | 71 | Short truncated | ch + -o |
| 10 | dam | 70 | Missing suffix -am | d + -am |
| 11 | cheo | 66 | Short truncated | ch + -eo |
| 12 | am | 56 | Standalone | Free -am particle |
| 13 | air | 56 | Standalone | Free -air |
| 14 | qo | 47 | Standalone prefix | qo appearing without stem |
| 15 | sheo | 39 | Short truncated | sh + -eo |
| 16 | otam | 34 | Missing suffix -am | ot + -am |
| 17 | aiiin | 34 | Extended -aiin form | aiin + extra i |
| 18 | cheos | 33 | Short + -s | ch + -eos |
| 19 | chos | 32 | Short + -s | ch + -os |
| 20 | ches | 30 | Short + -s | ch + -es |

### Four 'Other' Sub-Categories

**Category 1: Free standalone A-paradigm morphemes** (largest group)
Words: ol (476), aiin (394), or (300), ar (268), al (193), ain (100), air (56)
These words ARE the suffix itself — they have no stem before them. The suffix extractor requires `len(word) > len(suffix)`, which fails for bare `ol`, `aiin`, etc. These are the "free morphemes" previously identified in F118 (A-paradigm suffixes are grammaticalized free words).

**Category 2: Unrecognized suffixes -am and -air**
- -am ending: dam (70), otam (34), okam (25), qokam (24), cham (15), chom (13), om (19), am (56 standalone)
- -air ending: dair (75), otair (19), okair (16), qokair (15), sair (21), aiir (20), aiiin (34)
These represent UNRECOGNIZED suffix patterns. Adding -am and -air to the suffix list would capture ~1,000 tokens (~16% of the 'other' category).

**Category 3: Short truncated/alternative forms**
- -o ending: sho (108), cho (71), she (24), ctho (17) — these are likely ch/sh-onset words with a bare -o ending
- -eo ending: cheo (66), sheo (39), cheeo (18), okeeo (16) — parallel form with longer vowel
- -os/-es/-eos endings: cheos (33), chos (32), ches (30) — plural or variant forms?

**Category 4: Hapax and miscellaneous**
- 74.2% of 'other' word TYPES are hapaxes (vs 68.1% for suffixed words) — more hapax-heavy
- qokeed (18), qokeeo (18), shed (17), ched (16) — malformed B-suffix or alternative endings

### 2-Char Ending Distribution of 'Other' Words

| Ending | n | % | Interpretation |
|--------|---|---|---------------|
| in | 828 | 13.3% | -ain/-aiin tails |
| am | 575 | 9.2% | **-am suffix — should be added to suffix list** |
| ol | 476 | 7.6% | Standalone ol |
| ir | 453 | 7.3% | -air tails (-air suffix) |
| ho | 373 | 6.0% | -ho/-cho/-sho short forms |
| eo | 365 | 5.9% | -eo variant (cheo, sheo) |
| or | 300 | 4.8% | Standalone or |
| os | 273 | 4.4% | -os variant forms |
| ar | 268 | 4.3% | Standalone ar |
| es | 235 | 3.8% | -es variant forms |
| al | 193 | 3.1% | Standalone al |
| ed | 178 | 2.9% | -ed (shed=17, ched=16 — B-suffix products) |

**Final character distribution of 'other' words**: r (17%), o (15%), n (15%), l (13%), m (12%), s (12%), d (7%) — this is different from suffixed words which end primarily in y/n/l/r.

### Length Distribution: 'Other' vs Suffixed

'Other' words are dramatically shorter:
- Length 2: 25.6% of other vs 1.3% of suffixed
- Length 3: 12.9% of other vs 8.5% of suffixed
- Length 4: 23.2% of other vs 17.0% of suffixed
- Length 5+: 37.8% of other vs 73.2% of suffixed

The short skew confirms that most 'other' tokens are free morphemes (2-4 chars) rather than long compound words.

### Onset Class Enrichment in 'Other'

| Onset | other% | suf% | Ratio |
|-------|--------|------|-------|
| ol | 9.63 | 3.07 | **3.14×** enriched |
| other | 45.36 | 24.50 | 1.85× |
| qok | 3.97 | 10.76 | **0.37×** depleted |
| ok | 3.49 | 6.77 | 0.52× depleted |
| ch | 12.02 | 18.31 | 0.66× depleted |

**ol-onset is 3.14× enriched in 'other'** — because many ol-words are short forms (ol=476, ols=17, lo=16). **qok is 0.37× depleted** — qok words almost always have recognized B-suffixes.

### Section Distribution

Cosmo has the lowest 'other' rate (12.8%) — cosmo B-dialect is the most "suffixed" section. Astro has the highest (28.1%) but is small. Herbal/stars/pharma all cluster around 22-23%.

### H228 Verdict: CONFIRMED — 'Other' Category Has FOUR Components: (1) Free A-morphemes (ol/aiin/or/ar/al = top 5, ~1,700 tokens); (2) Unrecognized -am Suffix (9.2% of other, ~570 tokens) and -air Suffix (7.3%, ~450 tokens); (3) Short Truncated Forms (-o/-eo/-os, ~700 tokens); (4) Hapax Residual (74.2% hapax rate). Adding -am and -air to Suffix List Would Reduce 'Other' by ~1,000 Tokens (~16%); ol-onset 3.14× Enriched; qok 0.37× Depleted

---

## H229: CONFIRMED — Adjacent Paragraphs Share Vocabulary at 1.85× Rate of Non-Adjacent Paragraphs; daiin Repeats in 106 Paragraphs; Stars Has Highest Within-Para Repetition (0.476 Rep Rate); Overall Within-Para Rep Rate = 0.278

### Paragraph Statistics

- Total paragraphs: 258
- Mean size: 117.3 words
- Largest: 599 words; Smallest: 3 words

### Discourse Cohesion: Adjacent vs Non-Adjacent Overlap

| Metric | Value |
|--------|-------|
| Within-para word repetition rate | 0.278 (27.8% of tokens repeat within para) |
| Adjacent-para Jaccard overlap | **0.084** |
| Non-adjacent-para Jaccard overlap | **0.045** |
| **Adjacent/non-adjacent ratio** | **1.85×** |

**Adjacent paragraphs share vocabulary at 1.85× the rate of non-adjacent paragraphs.** This is a genuine discourse coherence signal — paragraphs that are neighbors in the text are more similar to each other than distant ones. This is consistent with what is expected for natural language text: adjacent paragraphs discuss related topics.

The within-para word repetition rate (27.8%) means that for a typical token in a paragraph, that specific word appears at least twice in the same paragraph. This is high — in natural language, longer paragraphs have lower TTR — consistent with the TTR decay with size seen in the data.

### Within-Para Repetition by Section

| Section | Mean rep rate | n_paras |
|---------|--------------|---------|
| stars | **0.476** | 25 |
| cosmo | 0.409 | 39 |
| herbal | 0.272 | 116 |
| pharma | 0.209 | 52 |
| astro | **0.062** | 26 |

**Stars has the highest within-para repetition rate (0.476)** — nearly half of tokens in a stars paragraph repeat the same words. This fits the stars section's content (star catalogs with repeated entries using the same vocabulary for each star). **Astro has the lowest (0.062)** — most astro paragraphs are short and diverse.

### Most-Repeated Words Within Paragraphs

| Word | Paras with ≥3 occ | Onset | Suffix |
|------|-------------------|-------|--------|
| daiin | **106** | d | aiin |
| ol | 55 | ol | other |
| chedy | 55 | ch | edy |
| chol | 49 | ch | ol |
| aiin | 47 | other | other |
| or | 42 | other | other |
| shedy | 42 | sh | edy |
| qokeedy | 37 | qok | eedy |
| chey | 34 | ch | ey |
| qokaiin | 34 | qok | aiin |
| qokedy | 33 | qok | edy |
| ar | 32 | other | other |
| qokeey | 30 | qok | eey |

**daiin appears 3+ times in 106 out of 258 paragraphs (41%)** — confirming daiin is a high-frequency function word that appears repeatedly in most paragraphs. It's the single most paragraph-ubiquitous word.

### Onset Repetition Within Paragraphs

Mean onset class repetition rate = 0.947 — essentially EVERY token in a paragraph shares its onset class with at least one other token. This reflects the limited onset class vocabulary (10-12 classes), but it also means paragraphs don't "use up" onset classes — they consistently revisit the same onset classes throughout.

### H229 Verdict: CONFIRMED — Adjacent Paragraphs Share Vocabulary at 1.85× Non-Adjacent Rate (Genuine Discourse Coherence); daiin Appears 3+ Times in 41% of Paragraphs (High-Frequency Function Word); Within-Para Rep Rate = 0.278; Stars Highest Rep Rate (0.476 — Star Catalog Repetition); Astro Lowest (0.062)

---

## Combined Finding (F124)

**H228 CONFIRMED (F124)**: The 'other' suffix category (20.6% of tokens) consists of four components: (1) Free standalone A-paradigm morphemes: ol (476), aiin (394), or (300), ar (268), al (193) — the top 5 'other' words are all free morphemes from F118's free-morpheme asymmetry finding; (2) Unrecognized -am suffix (~570 tokens; 9.2% of other) and -air suffix (~450 tokens; 7.3%) — these are legitimate suffix patterns not in the current list; (3) Short truncated forms (-o/-eo/-os endings; ~700 tokens); (4) Hapax residual (74.2% of types hapax). Adding -am and -air to suffix list would recover ~1,000 tokens. ol-onset is 3.14× enriched in 'other' (short bare-form ol words); qok is 0.37× depleted (qok words almost always suffixed).

**H229 CONFIRMED (F124)**: Voynich paragraphs show genuine discourse cohesion: adjacent paragraphs have 1.85× higher Jaccard overlap than non-adjacent (0.084 vs 0.045). Within-para word repetition rate = 27.8%. Stars has highest within-para repetition (0.476) — consistent with catalog-style repeated star entries. daiin is the most ubiquitous within-para repeated word (106/258 paragraphs ≥3 occurrences = 41%). This discourse structure is evidence against a random-generation or simple hoax theory — random text would show no distance-decay in paragraph similarity.
