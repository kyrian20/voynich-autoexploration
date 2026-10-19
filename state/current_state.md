# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_599 completed; synthesis and next priorities recorded)

## Canonical status and source of truth
Read the full synthesis first: `research/synthesis/2026-10-19-daiin-position-synthesis.md`. It separates replicated descriptive findings, annotation-sensitive outcomes, non-significant comparisons, and a methodologically uninformative experiment.

The pre-existing project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`; it has not been independently rerun in this session. Its reported 21-mechanism generator score of 19/19 is compatibility with a defined metrics battery, not proof of the manuscript's generative mechanism and not decipherment.

## API / automation status
The paid OpenAI API LLM workflow returned HTTP 429 because no API funds were available, as reported by the maintainer; it was not retried. New corpus experiments are plain Python/GitHub Actions and do not use API credits. Workflow run reports and machine-readable JSONs are kept with each experiment. Some simultaneous output-commits raced, so their artifacts/results were recovered and saved manually where necessary.

## Main finding from exp_589–599
A conditional line-initial excess for `daiin` is robust in Currier B, particularly P0 body-locus lines:
- exp_589: whole-body ~1.51× in both ZL3b and ZL3a; Currier B ~2.75× vs Currier A ~0.88×.
- exp_591: Currier-B P0 has 89 observed initial `daiin` tokens vs 31.53 expected (2.823×).
- exp_592: leaving each of 88 represented folios out in turn keeps the ratio 2.651×–2.939×.
- exp_590: positive effects persist across five coarse folio-number bins. They are heuristic bins, not official section labels.

## Critical controls and caveats
- exp_593: the signal in B/P0 is concentrated in rows with IVTFF `+` locator (89 vs 30.634 expected, ~2.91×). The official IVTFF spec defines `@`, `+`, and `*` as spatial/layout locators, not paragraph-start labels.
- exp_594–595: explicit paragraph start marker `<%>` is associated with an initial-token deficit in Currier A; B rows without a start marker show ~3× enrichment. The pattern repeats in ZL3a, but marker absence is not definitive continuation; segmentation is a transcriber decision.
- exp_596: `daiin` is not unique. In Currier-B P0, `dain` is ~3.17× initial and `saiin` ~5.02×, while `aiin` and `chedy` are depleted. These are distributions of EVA strings, not semantic roles.
- exp_597: next-token successor distributions after `daiin`, `dain`, `saiin` are not statistically distinguishable under the JSD/permutation test (adjusted p=1.0).
- exp_598: **uninformative due to sparsity**. The rare-pair collapse merged 97.1%–100% of joint contexts into one bucket, so its null result is not evidence of context equivalence.
- exp_599: marginal successor distributions at offsets +1 and +2 are also nonsignificant after Holm correction; this does not establish equivalence.

## Experiment reports and runs
- exp_589 — [report](experiments/exp_589_daiin_position_audit/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019)
- exp_590 — [report](experiments/exp_590_daiin_section_stratification/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097)
- exp_591 — [report](experiments/exp_591_daiin_locus_stratification/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800)
- exp_592 — [report](experiments/exp_592_daiin_folio_influence/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256951171)
- exp_593 — [report](experiments/exp_593_daiin_line_metadata_contrast/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257417694)
- exp_594 — [report](experiments/exp_594_daiin_explicit_paragraph_markers/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257721036)
- exp_595 — [report](experiments/exp_595_paragraph_marker_replication/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767)
- exp_596 — [report](experiments/exp_596_daiin_position_controls/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258230375)
- exp_597 — [report](experiments/exp_597_initial_form_next_token_context/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258573517)
- exp_598 — [report](experiments/exp_598_two_token_successor_context/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258767759)
- exp_599 — [report](experiments/exp_599_marginal_successor_positions/result.md) · [run](https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258941188)

## Next work: parser/provenance audit before more hypothesis tests
1. Cross-check IVTFF line extraction and locus parsing against the official spec with an independently written parser.
2. Align ZL3a and ZL3b by exact folio/locus; report token-level disagreements so similarity is not misdescribed as independent replication.
3. Freeze the Currier-B/P0 primary test, run a larger permutation budget, and predeclare section/folio sensitivity choices before inspecting outcomes.
4. Avoid expanding the number of daiin tests until parser coverage and source alignment are validated.

## Research integrity
- Keep observations, hypotheses, null results, and method failures distinct.
- Include source-file SHA-256, exact filter/token rules, output JSON, and workflow run with each experiment.
- Do not promote the 19/19 mechanism fit or positional effects into a decipherment.
- Never infer the meaning of `daiin` from position or local context alone.
