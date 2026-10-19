# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_596 completed; exp_597 running)

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

## exp_595 — explicit paragraph-marker replication (completed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767  
Report: `experiments/exp_595_paragraph_marker_replication/result.md`.

The same marker coverage was observed in both ZL3b and ZL3a: 4,105 eligible P-locus lines, 728 explicit starts, 729 ends; Currier group counts were identical. The key contrast replicated: Currier-A explicit starts had 1 first `daiin` vs 6.993 expected (adjusted lower-tail p=0.0124 in ZL3b, 0.0076 in ZL3a). Currier-B explicit starts had 0 vs 2.827 expected but this deficit did not survive correction (p=0.0976/0.0984). B lines without an explicit start marker had ~3.0× initial enrichment (97 vs ~32.3 expected; adjusted upper-tail p=0.0004 in both versions). The marker definition remains transcription-dependent; lines lacking a marker are not assumed to be definite continuations.

## exp_596 — common-word positional controls (completed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258230375  
Report: `experiments/exp_596_daiin_position_controls/result.md`.

In Currier-B P0, initial enrichment is not unique to `daiin`: daiin is 2.823× (89 vs 31.529 expected; Holm-adjusted upper-tail p=0.0012), but `dain` is 3.173× and `saiin` 5.023×, also adjusted p=0.0012. `aiin` and `chedy` are strongly below expectation; `qokaiin` is near expectation. The direction and magnitude replicate almost exactly in ZL3a (daiin ratio 2.813×, dain 3.173×, saiin 5.023×). In Currier-A P0, daiin is below expectation (0.860×) and not significant; aiin is depleted. These findings concern literal EVA token distribution, not shared meaning.

## Next step: exp_597
Test next-token context after line-initial `daiin`, `dain`, and `saiin` in Currier-B P0, with controls for starting token frequency and within-line token inventory. Use a predeclared top-context list plus full entropy/distribution distances, and report both transcriptions. No semantic interpretation is permitted from context distribution alone.

## Research integrity guardrails
- The 21-mechanism copy-buffer hybrid's 19/19 score is fit to a defined metric battery, not proof that it generated the manuscript and not decipherment.
- Keep hypotheses separate from executed results; include source hashes, code, outputs and workflow URLs.
- Preserve null/negative results and avoid duplicating tests without a specific question.
- Do not spend OpenAI API credits for corpus analyses that reproducible Python can perform.
- Never infer the meaning of `daiin` from position alone.

## exp_595 — cross-transcription paragraph-marker replication (results available)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767  
Report: `experiments/exp_595_paragraph_marker_replication/result.md`.

The explicit-paragraph-marker analysis reproduces almost exactly in ZL3a vs ZL3b. For Currier-B P0 lines without explicit `<%>`, both versions have 97 line-initial `daiin` hits in 2,056 lines: 3.005× expected in ZL3b and 2.995× in ZL3a; Holm-adjusted Monte Carlo p=0.0004 in both (5,000 draws). On explicitly marked B paragraph starts, both have 0/492 initial hits vs 2.827 expected; lower-tail p≈0.049, adjusted ≈0.098 (not significant at 0.05). Currier-A marked starts show 1/236 vs 6.993 expected; lower-tail adjusted p=0.0124 in ZL3b and 0.0076 in ZL3a. Marker counts and patterns match exactly across these files, so this is cross-version robustness, not independent external replication. Unmarked lines are not assumed to be true continuations; IVTFF annotation is transcription-dependent.

## Next block: exp_596–599
- exp_596: paired ZL3a/ZL3b line-level token and marker disagreement audit.
- exp_597: predeclared frequency-matched control words for line-initial enrichment, with multiple-testing correction.
- exp_598: folio-cluster bootstrap for Currier-B no-start-marker enrichment.
- exp_599: tokenizer/uncertain-reading sensitivity variants.

These analyses should run without OpenAI API credit and should preserve source hashes, scripts, results, and null findings.

## exp_596 — paired ZL3a/ZL3b line-level audit
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258473051  
Report: `experiments/exp_596_zl3a_zl3b_line_level_audit/result.md`.

The two versions align one-to-one on all 4,130 generic P-locus records, with no unmatched or duplicate keys, no dialect-label disagreement, no paragraph-marker disagreement, and no change in line-initial `daiin` status. There are 24 cleaned token-sequence disagreements. This confirms the exp_594/595 positional pattern is not caused by marker or line-key misalignment; it is version-level robustness, not independent replication.

## exp_597 — lexical-control specificity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258527666  
Status at checkpoint: compile-check passed; Monte Carlo analysis was running. Compares `daiin` with `aiin`, `chedy`, `dain`, `saiin`, and `qokaiin` using 10,000 within-line position draws per token and dialect, with Holm correction for upper-tail tests. Controls are exploratory and not perfectly matched by function or morphology.

## Next steps
- exp_598: folio-cluster bootstrap for Currier-B/no-start-marker enrichment.
- exp_599: tokenizer/uncertain-reading sensitivity variants.
- Consolidate positional findings and limitations into a human-review report before adding further tests.
