# Experiment exp_059: Currier A Line Grammar Violations
Date: 2026-04-09

## Question (H066)
Which Currier A folios violate the 3-tier line grammar (-dy para-start, y-initial continuation, -aiin para-end)? What characterizes the violating folios?

## Corpus-Wide Currier A Baselines (confirmed)
- y-initial at para-starts: 0.0% (complete suppression)
- y-initial at continuation lines: 16.4% (canonical rate)
- -dy PS enrichment: 3.36× (12.7% vs 3.8% baseline)

## Grammar Violators

All 6 grammar violators (by the criteria: y@cont <5% with ≥10 continuation lines) are in the **Herbal (H) section**:

| Folio | Lines | Cont | y@Cont | Section |
|-------|-------|------|--------|---------|
| f42r | 23 | 22 | 4.5% | H |
| f49r | 21 | 20 | 0.0% | H |
| f32r | 19 | 18 | 0.0% | H |
| f8v | 17 | 16 | 0.0% | H |
| f42v | 16 | 14 | 0.0% | H |
| f35r | 15 | 14 | 0.0% | H |

**Zero-grammar-violation folios exist ONLY in the Herbal section** — no violations in Special (S), Pharma (P), or Text (T) sections.

## Complementary Pattern: -aiin Enrichment in Zero-y Folios

The zero-y-initial herbal folios tend to have ELEVATED -aiin rates at line endings:
- f35r: **53.3%** aiin-last (vs herbal mean ~15%)
- f8v: **35.3%**
- f42v: **25.0%**
- f56v: **25.0%** (not a violator but elevated)
- f32r: **21.1%**
- f49r: **19.0%**

The negative correlation between y@cont and aiin_last suggests a **two-register system** within Currier A herbal:
- **High-y-initial register** (y@cont 20-40%, low aiin-last): f6v, f24v, f51r, etc.
- **High-aiin-last register** (y@cont 0%, aiin-last 20-53%): f49r, f32r, f8v, f42v, f35r

## f6v Is the Only High Outlier

f6v has y@cont = 40.0% — the only folio above the mean+2sd threshold (39.7%). This confirms that f6v is statistically unusual but on the high end, not the low end.

## f37v Anomaly

f37v shows dy_ratio = 23.00× (the first word of f37v is a -dy suffix word) and aiin_last = 39.1%. This is a single para-start, so the ratio is from 1 observation — but f37v's high -aiin last rate (39.1%) puts it in the same cluster as the zero-y herbal folios despite not being a strict violation.

## f35r: Both Violations

f35r has 0% y-initial continuation AND 53.3% aiin-last — it is the most extreme violator on both dimensions simultaneously. Over half its lines end in -aiin while none of its continuation lines begin with y-initial words. This is the strongest evidence of a herbal sub-register.

## H066 Verdict: SUPPORTED (with refinement)

The Currier A 3-tier line grammar is violated by a specific cluster of Herbal A folios. The violations are:
1. **Section-specific**: All violations in Herbal (H), none in S, P, or T
2. **Directionally consistent**: Low y@cont correlates with high aiin-last, suggesting an inverted usage of the two continuation markers
3. **Clustered by folio**: f49r, f32r, f8v, f42v, f35r form a coherent group (plus f42r as borderline)
4. **f6v is the outlier on the opposite end**: highest y@cont (40%) — distinct from the violator group

## Finding (F066)
Six Currier A herbal folios violate the canonical line grammar by having near-zero y-initial continuation rates (f49r, f32r, f8v, f42v, f35r: all 0%; f42r: 4.5%). These violations are exclusively in the Herbal section — no violations in Special, Pharma, or Text sections. The violating folios show compensatory elevated -aiin rates at line endings (f35r: 53.3%, f8v: 35.3%, f42v: 25.0%), suggesting a two-register system within herbal A text: a y-initial-dominant register (f6v, f24v, f51r type) and an aiin-dominant register (f49r, f32r, f8v, f42v, f35r type). The aiin-dominant herbal folios may represent a different scribal hand or a different content sub-type (possibly a different plant classification convention). f35r is the most extreme violator on both dimensions (0% y-initial, 53.3% aiin-last). The grammar violations are not random noise — they form a coherent subgroup within the herbal section that systematically substitutes -aiin for y-initial as the line-continuation/continuation-marking strategy.
