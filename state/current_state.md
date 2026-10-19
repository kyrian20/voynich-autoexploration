# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_594 completed; outputs and protocol caveats saved)

## Canonical scientific checkpoint
The earlier project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`. It reports five pre-registered Section 2 findings retained under the ≥2/3 alternative-transliteration rule; F4 retained in EVA-basic and ZL3a but failed in v101 where the o→sh edge had one observation. These are repository-reported findings, not independently rerun as part of exp_589–594.

## API and automation status
The scheduled LLM-report workflow hit HTTP 429 on 2026-10-19 because the OpenAI API has no funds available, as reported by the maintainer; it was not retried. The new corpus-analysis workflows run standard Python in GitHub Actions and require no OpenAI API credit. Their JSON is uploaded as a 90-day artifact; because simultaneous GitHub Actions jobs can race when auto-committing to `master`, the generated outputs were also persisted manually through the GitHub connector when needed.

## exp_589 — daiin positional audit
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
Report: `experiments/exp_589_daiin_position_audit/result.md`.

Across the body, `daiin` is about 1.51× expected at line start in both ZL3b and ZL3a. Currier A is below expectation overall (about 0.88×), whereas Currier B is about 2.75× expected (Monte Carlo p at the 2,000-draw resolution floor 0.0005). The direction replicates between the two checked-in EVA transcription versions under the selected parser.

## exp_590 — folio-number-range sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
Report: `experiments/exp_590_daiin_section_stratification/result.md`.

Across five coarse Currier-B folio-number bins, enrichment is positive (1.62×–4.10×); all five one-sided Monte Carlo tests remain below 0.05 after Holm adjustment. Two populated Currier-A bins differ (0.72× for f001–f066, 1.68× for f085–f102). Bins are approximate folio-number proxies, not authoritative codicological section labels.

## exp_591 — exact IVTFF body-locus sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800  
Report: `experiments/exp_591_daiin_locus_stratification/result.md`.

The Currier-B result persists in dominant locus P0: 89 initial `daiin` tokens vs 31.53 expected, 2.823×, Holm-adjusted p=0.0015 across eligible B-locus groups. P1 is elevated but sparse; Pb is not significant. Currier-A P0 is below expectation (0.87×, adjusted p=0.902). Locus codes are literal IVTFF categories, not grammar interpretations.

## exp_592 — leave-one-folio-out influence
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256951171  
Report: `experiments/exp_592_daiin_folio_influence/result.md`.

In Currier-B P0, 2,345 lines have 89 observed first-position `daiin` tokens vs 31.529 expected (2.823×). Omitting each of 88 folios in turn leaves enrichment between **2.651× and 2.939×**; omitting f108v has the largest decrease, but the effect persists. This is an influence analysis, not another significance test.

## exp_593 — IVTFF locator categories
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257417694  
Report: `experiments/exp_593_daiin_line_metadata_contrast/result.md`.

The official IVTFF definition clarifies that `@` is used for the first item on a page; `+` generally locates an item below the previous one; `*` marks a line-start locus below a preceding item that was not at the margin. These are spatial locator codes, **not paragraph-opening markers**. In B/P0 rows marked `+`, 89 initial hits vs 30.634 expected give a 2.905× enrichment (Holm-adjusted upper-tail p=0.0004); B/P0 rows marked `@` have 0 vs 0.805 expected and no significant deficit. A/P0 rows marked `@` have 0 vs 3.772 expected, with lower-tail adjusted p=0.0356. Lower-tail and upper-tail results are separately corrected within dialect.

## exp_594 — explicit paragraph-boundary markers
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257721036  
Report: `experiments/exp_594_daiin_explicit_paragraph_markers/result.md`.

IVTFF uses dedicated `<%>` and `<$>` comments for paragraph start/end; the format specification says paragraph segmentation is a transcriber decision. In ZL3b, 4,105 eligible P-locus lines include 728 explicit start markers and 729 end markers. For Currier A, explicitly start-marked rows have a first-position deficit (1 observed vs 6.993 expected; Holm-adjusted lower-tail p=0.0132), while unmarked rows do not show a significant positional deviation. For Currier B, start-marked rows have 0 vs 2.827 expected; lower-tail p=0.0544, adjusted 0.1088 (not significant). B rows without a start marker show 97 vs 32.279 expected (3.005×; adjusted upper-tail p=0.0004). **Caveat:** absence of `<%>` is not treated as definitive continuation because tagging may be incomplete and segmentation varies by transcriber. This finding is annotation-conditioned, not semantic.

## Next step: exp_595
Replicate the explicit `<%>`/`<$>` paragraph-marker analysis in ZL3a using the exact same counting rules. Compare marker coverage and section/locus counts before pooling anything. If the markers do not correspond between ZL3a and ZL3b, report that mismatch rather than claiming replication. Preserve null results. This cross-transcription replication matters more than extending the number of tests on ZL3b alone.

## Research integrity guardrails
- The 21-mechanism copy-buffer hybrid's 19/19 score is fit to a defined metric battery, not proof that it generated the manuscript and not decipherment.
- Keep hypotheses separate from executed results; include source hashes, code, outputs and workflow URLs.
- Preserve null/negative results and avoid duplicating tests without a specific question.
- Do not spend OpenAI API credits for corpus analyses that reproducible Python can perform.
- Never infer the meaning of `daiin` from position alone.
