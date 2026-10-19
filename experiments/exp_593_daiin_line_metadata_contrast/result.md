# exp_593 — Results: IVTFF locator-stratified daiin position audit

**Execution:** GitHub Actions completed successfully on 2026-10-19  
**Run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257587334  
**Machine output:** `results.json`  
**Corpus SHA-256:** `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

## Results

| Currier class / P0 locator | Lines | daiin tokens | Initial observed | Expected | Enrichment | Holm-adjusted p (upper tail) |
|---|---:|---:|---:|---:|---:|---:|
| A / @ | 134 | 32 | 0 | 3.772 | 0.00× | 1.000 |
| A / + | 1,359 | 452 | 59 | 63.988 | 0.92× | 1.000 |
| B / @ | 90 | 8 | 0 | 0.805 | 0.00× | 1.000 |
| B / + | 2,245 | 289 | 89 | 30.634 | 2.91× | 0.0004 |

Only categories with at least 50 lines were included. The P0 B/+ subset carries the initial-position excess (89 observed vs 30.63 expected; 2.91×; Holm-adjusted Monte Carlo p=0.0004, with 5,000 permutations). This matches the direction of exp_591–592, but this is not an independent replication: it is a stratification of the same ZL3b transcript and overlaps the previous tests.

The A/@ subset has zero initial occurrences where 3.77 are expected; the lower-tail Holm-adjusted p is 0.0356. Treat this as exploratory because this experiment's families are exploratory and it was not a pre-registered primary contrast. The A/+ subset has no significant upper- or lower-tail deviation. B/@ has only 90 lines and eight target tokens; its estimates are sparse.

## Crucial interpretation guardrail
The IVTFF specification describes `@`, `+`, and `*` as spatial locator codes, not paragraph-start/continuation labels. In this file, `@` is used for the first item on a page, `+` generally places an item below the previous item, and `*` indicates a particular left-margin line relationship. The experiment does **not** test paragraph markers `<%>` and `<$>`; therefore it cannot answer whether paragraph-opening lines differ from continuation lines.

Reference: https://voynich.nu/software/ivtt/IVTFF_format.pdf (Table 8 and §6.9; format issue 2.0.2, 2025-07-08).

## Limitations
- Within-line token-inventory/length null; 5,000 Monte Carlo draws; minimum p resolution 1/5,001.
- Only ZL3b was used.
- Locator-stratification p-values are secondary/exploratory and do not establish a meaning for `daiin`.
- The previous script's docstring called this a paragraph-opening test; that wording was inaccurate. The actual analysis is locator-stratified and is described correctly here.

## Next step
Build exp_594 to test actual `<%>` paragraph-start markers by parsing raw IVTFF line content before token cleaning, validating marker placement and counts, and comparing paragraph-opening with non-opening lines within Currier-B P0. Do not use `@`, `+`, or `*` as proxies for paragraph boundaries.
