# Synthesis — exp_589–exp_599: EVA `daiin` positional/context audit

**Date:** 2026-10-19  
**Scope:** exp_589–exp_601, the experiments added after the repository's earlier exp_588 checkpoint.  
**Canonical status:** exploratory corpus-distribution research only; no decipherment or semantic claims.

## Executive assessment

The strongest result is a robust **Currier-B / P0 line-initial positional enrichment** for the literal EVA token `daiin`. It replicates across the checked-in ZL3a and ZL3b files, survives several stratification/sensitivity checks, and is not driven by one folio. But the control-word comparison shows that the pattern is **not unique to `daiin`**: `dain` and `saiin` show even stronger initial enrichment in the same Currier-B P0 analysis. The next-token and second-successor comparisons did not distinguish the three forms with the tests and sample sizes used.

This supports a narrow statement about token position in the analyzed transcription. It does **not** establish that the tokens are natural-language words, share a meaning, play a grammatical role, or reveal a decipherment.

## Evidence by status

### A. Replicated and robust within the selected parser

**1. Overall dialect contrast — exp_589**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
Report: [exp_589 result](../../experiments/exp_589_daiin_position_audit/result.md)

- In the two transcription files, whole-body `daiin` is about 1.51× the line-inventory/length expectation at line start.
- The aggregate hides a dialect split: Currier A is below expectation overall (about 0.88×), while Currier B is about 2.75× expected.
- This is the first-pass primary signal; the later experiments mostly examine its stability and specificity.

**2. Robustness across rough folio-number ranges — exp_590**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
Report: [exp_590 result](../../experiments/exp_590_daiin_section_stratification/result.md)

- All five eligible Currier-B folio-number bins showed positive initial enrichment (about 1.62×–4.10×) after Holm correction.
- These are rough folio-number proxies inherited from the project's earlier script, not authoritative codicological section labels. Treat this as a sensitivity check, not definitive section-specific evidence.

**3. Exact body-locus sensitivity — exp_591**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800  
Report: [exp_591 result](../../experiments/exp_591_daiin_locus_stratification/result.md)

- In Currier-B P0, 89 first-position `daiin` tokens were observed versus 31.53 expected (2.823×; Holm-adjusted p=0.0015 for its eligible B-locus family).
- The dominant P0 group carries the effect. P1 is also positive but much smaller and sparse; Pb did not reach significance.
- Currier-A P0 is below expectation (0.87×), with no evidence of an initial excess.

**4. Not a one-folio artefact — exp_592**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256951171  
Report: [exp_592 result](../../experiments/exp_592_daiin_folio_influence/result.md)

- Leaving out each of 88 folios in turn kept the B/P0 initial enrichment between 2.651× and 2.939×.
- Some folios change the magnitude, but no single omission removes the pattern. This is an influence diagnostic, not another p-value.

**5. Position depends on IVTFF locator/annotation strata — exp_593–595**  
Runs: [exp_593](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257417694), [exp_594](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257721036), [exp_595](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767)  
Reports: [exp_593](../../experiments/exp_593_daiin_line_metadata_contrast/result.md), [exp_594](../../experiments/exp_594_daiin_explicit_paragraph_markers/result.md), [exp_595](../../experiments/exp_595_paragraph_marker_replication/result.md)

- In B/P0 rows carrying the `+` locator, 89 initial hits vs 30.63 expected gave about 2.91× enrichment. The `@` rows are page-first layout items and had too few expected target hits to support a deficit claim.
- The official IVTFF format says `@`, `+`, and `*` are spatial/layout locators, not paragraph-open indicators. Paragraph starts/ends use distinct `<%>`/`<$>` comments; segmentation is the transcriber's decision. Source: [IVTFF format specification, Table 8 and §6.9](https://voynich.nu/software/ivtt/IVTFF_format.pdf).
- Explicit `<%>` markers associate with a Currier-A initial deficit. In Currier B, the 0 observed vs 2.83 expected at explicit starts did not survive adjusted significance; B rows without a start marker show ~3× enrichment.
- exp_595 reproduced the direction and marker counts in ZL3a. Absence of `<%>` must not be relabelled as “definitely a continuation”: annotation coverage may be incomplete and boundaries are transcription-dependent.

### B. The effect is not unique to `daiin`

**6. Common-word controls — exp_596**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258230375  
Report: [exp_596 result](../../experiments/exp_596_daiin_position_controls/result.md)

Currier-B P0, ZL3b:
- `daiin`: 89 first vs 31.53 expected, 2.823×.
- `dain`: 34 first vs 10.71 expected, 3.173×.
- `saiin`: 46 first vs 9.16 expected, 5.023×.
- `aiin` and `chedy` are strongly depleted at line start; `qokaiin` is near expectation.

The control terms were predeclared from the existing exp_589 code, not selected after this run. Comparable direction/effect sizes were reported in ZL3a. The key correction to the research narrative is that `daiin` does **not** have a unique Currier-B start-position signature. The result is a heterogeneous distribution of literal EVA forms.

### C. Non-significant successor-context tests — do not confuse with equivalence

**7. Next token — exp_597**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258573517  
Report: [exp_597 result](../../experiments/exp_597_initial_form_next_token_context/result.md)

- The pairwise Jensen–Shannon divergence tests between successor distributions after `daiin`, `dain`, and `saiin` were not significant after Holm correction (all adjusted p=1.0).
- Sample sizes were 89, 34, and 46 starters. High successor-type diversity and small samples limit power.

**8. Two-token joint pairs — exp_598 (methodologically uninformative)**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258767759  
Report: [exp_598 result](../../experiments/exp_598_two_token_successor_context/result.md)

- The pooled-frequency threshold collapsed 97.1%–100% of two-token contexts into one `<RARE_PAIR>` category.
- Resulting non-significant JSD values contain almost no retained pair information. Do **not** interpret this as evidence of equal contexts; keep exp_598 explicitly marked uninformative because of sparsity.

**9. Marginal successor offsets +1 and +2 — exp_599**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258941188  
Report: [exp_599 result](../../experiments/exp_599_marginal_successor_positions/result.md)

- With the same 169 B/P0 starter lines, none of six pairwise tests (three starter pairs at each of two offsets) was significant after Holm correction in either file.
- The correct interpretation is “no distinguishable difference was detected under this test,” not “the contexts are equivalent.”

### D. The two transcription files are highly concordant

**10. ZL3a/ZL3b line-level concordance — exp_600**  
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259781970  
Report: [exp_600 result](../../experiments/exp_600_transcription_concordance/result.md)

- The corrected parser aligns 5,385 line records by exact IVTFF identifier, with no duplicate or skipped IDs; four IDs appear only in ZL3a.
- Of aligned lines, 5,336 (99.09%) have identical cleaned token sequences; 49 (0.91%) differ. All matched records have the same normalized locus/Currier label under this parser, and paragraph marker flags match.
- This explains the near-identical statistics in prior analyses. ZL3a/ZL3b agreement is version robustness on closely related transcriptions, not replication across independent corpora.
- The next necessary check is to measure how these exact 49 differing rows affect the primary counts directly.

### E. Paired sensitivity of the actual primary statistic — exp_601
Run: [successful workflow](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260083190)  
Report: [exp_601 result](../../experiments/exp_601_primary_statistic_paired_sensitivity/result.md)

The paired analysis uses 2,325 matched eligible Currier-B/P0 lines. Ten rows differ in cleaned-token sequence between ZL3a/ZL3b; two rows have a changed literal first token, but none changes first-position status for the six predeclared tokens. For `daiin`, counts are 295 vs 296 and first counts 88 vs 88; the expected count shifts from 31.279 to 31.384, with enrichment 2.813× vs 2.804×. The tested first-position statistics are therefore insensitive to these version differences. This is a paired comparison of transcriptions of the same manuscript, not independent replication.

## Overall status of the hypothesis

| Claim | Status | Reason |
|---|---|---|
| `daiin` is enriched at line start in Currier B | **Supported, conditional** | Repeats in ZL3a/ZL3b, P0, folio-range strata, locus analyses, and LOFO |
| The result is caused by one folio | **Disfavoured** | LOFO enrichment remains 2.651×–2.939× |
| `daiin` has a unique positional profile | **Not supported** | `dain` and `saiin` have stronger B/P0 enrichment |
| A single semantic or grammatical interpretation follows | **Not tested / not established** | The experiments are token-distribution analyses only |
| Successor contexts of the three forms are equal | **Not established** | Tests were non-significant, but samples are small/sparse |
| Two-token joint contexts are equal | **No valid conclusion** | Rare-pair collapse erased nearly all sequence information |

## Global limitations and independence

1. **The “replication” files are not independent manuscript samples.** ZL3a and ZL3b are distinct transcription files, but they have identical eligible P-locus and starter counts for several analyses and extremely similar token results. Their agreement is a robustness check against file/version differences, not a second independent manuscript.
2. **The analyses share a parser.** A mistake or simplifying choice in IVTFF line extraction, locus filtering, markup cleanup, or Currier-label assignment could affect multiple experiment IDs together. Independent parser validation is needed before stronger claims.
3. **The null is conditional and limited.** The within-line random-position model preserves each line's token inventory and length. It does not model every dependency involving section, handwriting, neighboring lines, transcription uncertainty, or editorial conventions.
4. **Monte Carlo floor.** Many reported p=.0002/.0005 values are the resolution floor of 5,000/2,000 permutations, not exact probabilities. They were adjusted conservatively, but larger simulations would refine the bound rather than change the broad effect-size pattern.
5. **No semantic evidence.** Positional regularity cannot by itself determine whether EVA strings are words, what they mean, or how the manuscript was generated.

## Recommended next work (priority order)

1. **Independent parser and provenance audit.** Inspect line headers and body-locus rules against the official IVTFF format, compare parser outputs with a separately written parser, report retained/excluded line counts by folio/locus and validate Currier A/B labels. Do not rerun the whole family unchanged just to add more experiment IDs.
2. **Independent transcription concordance.** Align ZL3a and ZL3b by exact folio/locus, count token-level disagreements, and identify whether the apparent “replication” uses almost entirely shared token readings. Treat differences as paired transcription variants, not independent observations.
3. **Confirmatory, preregistered test.** Freeze the primary hypothesis (Currier-B P0 initial enrichment), exact parser, primary statistics, and folio/section strata. Use a larger Monte Carlo count and report all outcomes plus sensitivity rules.
4. Only after those checks, consider new contextual analyses. Any linguistic hypothesis must have explicit predictions and negative controls, not just post-hoc interpretation of frequent strings.

## Automation status

These corpus tests run in standard GitHub Actions/Python and do not use OpenAI API credits. The separate LLM agent workflow still requires OpenAI API billing and failed with HTTP 429 when the account had no API funds. Do not rerun that workflow until the user decides to fund it.
