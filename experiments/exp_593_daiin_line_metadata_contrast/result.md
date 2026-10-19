# exp_593 — Results: daiin and IVTFF locator metadata

**Execution date:** 2026-10-19  
**Status:** successful GitHub Actions run  
**Run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257417694  
**Machine output:** `results.json`

## Format clarification

The official IVTFF 2.0.2 specification defines the locator in a locus identifier as a spatial relation: `@` is used for the first item on a page; `+` typically means the locus is generally below the previous item; `*` means a locus at the start of the line below the previous item but at the left margin while the previous locus was not. These are not paragraph boundary markers. IVTFF paragraph starts/ends use dedicated text comments `<%>` and `<$>`, with paragraph segmentation decisions made by the transcriber. Source: [IVTFF format specification](https://voynich.nu/software/ivtt/IVTFF_format.pdf), Table 8 and §6.9. citeturn999141view0turn999141view1

Accordingly, this experiment is an **IVTFF layout-locator sensitivity test**, not a test of paragraph openings.

## Results

| Currier / locator / P0 | Lines | `daiin` tokens | First observed | Expected first | Ratio | Upper-tail p (Holm) | Lower-tail p (Holm) |
|---|---:|---:|---:|---:|---:|---:|---:|
| A / @ / P0 (page-first item) | 134 | 32 | 0 | 3.772 | 0.00× | 1.0000 | 0.0178 (0.0356) |
| A / + / P0 (generally below previous locus) | 1,359 | 452 | 59 | 63.988 | 0.92× | 1.0000 | 0.2639 (0.2639) |
| B / @ / P0 (page-first item) | 90 | 8 | 0 | 0.805 | 0.00× | 1.0000 | 0.4111 (0.8222) |
| B / + / P0 (generally below previous locus) | 2,245 | 289 | 89 | 30.634 | 2.91× | 0.0002 (0.0004) | 1.0000 (1.0000) |

The primary positive finding remains in Currier B, P0 lines marked `+`: 89 initial `daiin` tokens versus 30.63 expected, about **2.91× enrichment**, with 5,000 within-line random-position simulations and Holm-adjusted upper-tail p=0.0004 within the B locator-category family.

In the Currier-A page-first `@P0` subset, no line begins with `daiin` (0 observed vs 3.77 expected); the lower-tail Monte Carlo p=0.0178, adjusted p=0.0356 across eligible A categories. This is evidence for a first-position deficit in this subset under the chosen tokenization/null. For Currier-B `@P0`, 0 were observed but expectation was only 0.80 and the adjusted lower-tail p=0.822; the sample does not distinguish it from the null.

Currier-A `+P0` shows no meaningful excess or deficit (59 vs 63.99 expected). Categories with fewer than 50 eligible lines were left out of inferential comparisons, so this experiment does not draw conclusions about rare `*` or unmarked P0 rows.

## Interpretation and limits
- The broad Currier-B initial excess from exp_589–592 is localized, in this IVTFF locator stratification, to P0 rows marked `+`, not to the page-first `@` subset.
- This describes a layout relation, not paragraph function. Paragraph boundaries require the actual `<%>`/`<$>` markers and should be tested separately.
- All p-values are Monte Carlo estimates from 5,000 replicates, with Holm adjustment within dialect and tail families.
- This is a positional analysis only. It does not establish the meaning of `daiin` or decipher the manuscript.
