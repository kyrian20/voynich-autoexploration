# exp_592 — Results: leave-one-folio-out influence for Currier-B P0 daiin

**Execution date:** 2026-10-19  
**Status:** completed successfully in GitHub Actions  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256951171  
**Output:** `results.json`

## Question
Can a single folio account for the line-initial `daiin` excess found in Currier-B P0?

## Overall result
Across 2,345 Currier-B P0 lines with at least two clean tokens:
- Observed line-initial `daiin`: **89**
- Expected by within-line inventory/length null: **31.529**
- Enrichment: **2.823×**
- Excess observed over expected: **57.471**

The sensitivity procedure omitted each of the 88 represented folios one at a time, recalculating counts and enrichment. The enrichment stayed elevated for every omission; the range was **2.651× to 2.939×**. It therefore does not depend on any one folio being present.

## Most influential folios
| Omitted folio | Initial hits on folio | Expected on folio | Enrichment after omission | Change from full ratio |
|---|---:|---:|---:|---:|
| f108v | 8 | 0.980 | 2.651× | −0.171× |
| f103v | 7 | 0.868 | 2.674× | −0.148× |
| f84v | 0 | 1.252 (implied from full vs omission) | 2.939× | +0.117× |
| f77r | 5 | 0.695 | 2.724× | −0.099× |
| f81v | 0 | 1.017 (implied from full vs omission) | 2.917× | +0.094× |

The top two influence folios, f108v and f103v, account for 15 of 89 first hits (about 16.9%). Omitting f108v lowers the ratio from 2.823× to 2.651×, but leaves a substantial excess. Omitting f103v leaves 2.674×. Thus a handful of folios affect the magnitude, but neither a single folio nor the two strongest together are enough to explain away the aggregate signal.

Per-folio rankings are post hoc descriptive diagnostics. Some folios have comparatively few lines, so the ratios from individual folios are noisy and are not evidence of semantic meaning.

## Interpretation
**The Currier-B P0 initial-position excess is not a single-folio artifact.** It remains between roughly 2.65× and 2.94× after every leave-one-folio-out omission. This supports the robustness of the positional statistic within this transcript and operational parser.

This is not an additional significance test: LOFO ratios show influence, not independent p-values. The expected count is conditional on each line's own token inventory and length, as in exp_589–591.

## Limitations
- Single transcription ZL3b in this experiment; the independent ZL3a comparison is exp_589.
- The line-position null does not model all possible dependencies involving section, paragraph, handwriting, or transcription uncertainty.
- No semantic or decipherment claim follows from the positional effect.

## Suggested next research step
Explore whether the same line-initial `daiin` behavior associates with paragraph position (first line of folio/paragraph vs continuation) or other neighbouring onset classes, using predeclared comparisons and controls. Keep each new question separate from the already tested first-token overrepresentation.
