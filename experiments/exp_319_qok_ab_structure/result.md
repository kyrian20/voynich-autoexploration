# exp_319: qok A vs B Internal Structure Analysis (H498)

**Date:** 2026-04-11
**Hypothesis:** H498 — The A-qok midfix richness (exp_288: A MLen=1.34, B MLen=0.52, 2.6× difference) is driven by one or two high-frequency long-midfix forms, or alternatively by uniformly distributed richness across many types.
**Result:** H498 ANSWERED. A-qok midfix richness is DISTRIBUTED across many types, not concentrated in a few forms. Primary drivers: (1) higher 'e' vowel midfix rate (25.5% vs 13.7% in B), (2) more 'ch' compound midfix forms, (3) broader suffix diversity (ol/ey/dy/or vs edy/eedy dominance in B). 50 A-only qok types (of 99 A-types) encode unique midfix × suffix combinations.

---

## Key Statistics

| Metric | A-dialect | B-dialect |
|--------|-----------|-----------|
| Tokens (MID) | 372 | 1965 |
| Types | 99 | 150 |
| CP90 (types) | 62 (62.6% of types) | 31 (20.7% of types) |
| ZeroMid rate | 42.2% | 72.1% |
| Mean midfix length | 1.099 chars | 0.450 chars |
| Shared types | 49 of 99 A-types (49.5%) |

---

## Mechanism of A-qok Midfix Richness

**1. 'e' vowel midfix (primary driver)**
- A-qok: 25.5% of valid tokens have 'e' midfix (qokeey, qokeol, qokeody, qokeor)
- B-qok: 13.7% have 'e' midfix (mostly qokeey)
- The 'e' midfix extends qok words by 1 char: qok+e+[suffix]. A uses this pattern almost 2× more than B.

**2. 'ch' compound midfix (secondary driver)**
- A: qokchol (12), qokchey (4), qokchor (3), qokchody (2) — 'ch' forms appear frequently
- B: qokchdy (42) — concentrated in one form; qokchedy (33) — the 'c' midfix is a parsing artifact
- Net effect: A has more diverse ch-extended qok forms (qokch+ol, qokch+or, qokch+ey) vs B's single dominant ch pattern

**3. Suffix diversity**
- A: ol (20.7%), ey (15.1%), dy (8.1%), or (6.5%), ar (6.2%), al (5.9%), aiin (5.6%) — 7 frequent suffixes
- B: ey (16.6%), edy (14.0%), eedy (13.2%), ain (11.9%), aiin (10.6%) — 5 suffixes dominate 66%
- A's broader suffix distribution × broader midfix distribution = combinatorial vocabulary expansion

**4. Distribution pattern: gradual not spiky**
- Top-3 B forms (qokeedy/qokedy/qokain) cover 35.5% of tokens — high concentration
- Top-3 A forms (qokeey/qokol/qokeol) cover only 24.7% — more distributed
- A CP90=62 types (62.6% of types): 1.3× more types needed for 90% coverage vs B's 31 (20.7%)
- The richness is uniformly distributed, not concentrated in 1-2 forms

---

## Cross-Dialect Analysis

**Shared types (49/99 A-types = 32.7% of B-types):**
- Core shared forms: qokeey, qokaiin, qokal, qokar, qokey, qokor, qokol (all zero-midfix or 'e' midfix)
- A ranks qokol (8.33%) and qokeol (7.26%) highly; B ranks these low (1.93%, 0.66%)
- B ranks qokeedy (12.82%), qokedy (11.45%), qokain (11.25%) highest — all absent from top-20 A list

**A-only types (50/99 A-types):**
- Includes qokchol (12), qokeos (5), qokchor (3), qokchody (2) — medium-frequency ch-midfix forms
- Many A-only forms have unrecognized suffixes (classified 'other'): qoky, qokchy, qokaly, qokoiin
- Long-midfix A-only: qokchol (ch+ol), qokchor (ch+or), qokchody (cho+dy), qokchodal (chod+al)

**No folio concentration:** A-qok midfix richness is distributed across herbal, astro, bio, and stars sections. No single section dominates. High-midfix forms appear in f16/f22 (herbal), f96/f102r1 (bio/stars). The richness is NOT a scribal artifact from a few pages.

---

## Interpretation

**A-qok and B-qok are structurally different paradigms** sharing a core vocabulary (~49 types) but diverging in:
1. Midfix frequency: A uses 'e' vowel extension 2× more; A has more productive 'ch' compound forms
2. Suffix: B concentrates on edy/eedy/ain/aiin; A uses ol/ey/dy/or/ar/al
3. Paradigm closure: A-CP90=62 (62.6% of types); B-CP90=31 (20.7% of types) — A's paradigm is open, B's is closed

**H498 conclusion:** The A-qok midfix richness is NOT driven by a few dominant forms. It is an intrinsic property of the A-dialect writing system: A-qok words use the 'e' vowel extension and 'ch' compound extension more pervasively, combined with broader suffix variation, creating a vocabulary ~2× richer per token than B-qok. This is consistent with exp_295's finding that A-dialect has larger closed paradigms overall (A-qok CP90%=57.3% of types vs B-qok=18.2%).

**Mechanistic implication for simulation:** The simulation currently models both dialects with the same midfix distribution (sampled from B-dialect corpus). To accurately model A-qok, a dialect-specific midfix weighting would be needed — specifically increasing 'e' midfix probability and 'ch' midfix for qok-onset words in the A architecture.

---

## Limitations

- Midfix calculation excludes words with 'other' suffix (109 A tokens, 220 B tokens = 29-31% excluded). The mean midfix lengths (A=1.099, B=0.450) are lower than exp_288's values (1.34, 0.52) because exp_288 likely used different suffix parsing.
- 'qokchy' and 'qoky' are classified as 'other' suffix — their midfixes are uncounted but they are frequent forms (A: 25 and 20 tokens). Including them would reduce ZeroMid rate and change midfix distribution.
- Section analysis uses rough folio number → section mapping; bio/herbal sections not perfectly delineated.

---

## Self-Audit

**Target-awareness:** Pure corpus analysis — no VMS targets used for calibration. All observations are direct measurements of the VMS corpus.

**Feature-destroying implementation:** No simulation mechanism involved. The midfix extraction is the same algorithm used in prior experiments (strips onset, strips suffix, applies edy connector adjustment). No feature-destroying elements.

**Extrapolation:** The finding that A-qok richness is "distributed" (not concentrated) is based on the CP90 analysis (62 types for 90% coverage) and inspection of top-20 forms. This is within the measured data. The mechanistic interpretation (two drivers: 'e' vowel and 'ch' compound) is based on the midfix frequency table and is within scope of the measurements.

**Negative-result scope:** N/A — positive characterization result.

**Control behavior:** B-dialect serves as within-experiment contrast. Both dialects are measured with the same algorithm. No separate null model needed; the comparison is A vs B within VMS.
