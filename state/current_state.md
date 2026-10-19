# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_592 executed; findings saved)

## Canonical scientific checkpoint
The earlier project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`. It reports five pre-registered Section 2 characterization findings retained under the ≥2/3 alternative-transliteration rule; F4 retained in EVA-basic and ZL3a but failed in v101 where the o→sh edge had one observation. These are repository-reported findings, not independently rerun as part of exp_589–592.

## Operational status
The scheduled LLM-report workflow needs OpenAI API billing and produced HTTP 429 on 2026-10-19, consistent with the maintainer's statement that no API funds remain. It was not retried. Corpus analyses use standard Python/GitHub Actions and do not need API credits.

## exp_589 — daiin positional audit
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
Report: `experiments/exp_589_daiin_position_audit/result.md`.

Across the body, `daiin` is about 1.51× expected at line start in both ZL3b and ZL3a. Currier A is below expectation overall (about 0.88×), whereas Currier B is about 2.75× expected (Monte Carlo p at the 2,000-draw resolution floor 0.0005). The direction replicates between the two checked-in EVA transcription versions under the selected parser.

## exp_590 — folio-number-range sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
Report: `experiments/exp_590_daiin_section_stratification/result.md`.

Across five coarse Currier-B folio-number bins, enrichment is positive (1.62×–4.10×); all five one-sided Monte Carlo tests remain below 0.05 after Holm adjustment. The two populated Currier-A bins differ (0.72× for f001–f066, 1.68× for f085–f102). The bins are rough numerical proxies, not authoritative codicological section labels.

## exp_591 — exact IVTFF body-locus sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800  
Report: `experiments/exp_591_daiin_locus_stratification/result.md`.

The Currier-B result persists in dominant locus P0: 89 initial `daiin` tokens vs 31.53 expected, 2.823×, Holm-adjusted p=0.0015 across eligible B-locus groups. P1 is elevated too (4 vs 1.11 expected; adjusted p=0.025), but sparse; Pb is not significant (adjusted p=0.210). Currier-A P0 is below expectation (0.87×, adjusted p=0.902). Locus codes remain literal IVTFF codes without semantic interpretation.

## exp_592 — leave-one-folio-out influence (executed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256951171  
Report: `experiments/exp_592_daiin_folio_influence/result.md`.

Within Currier-B P0, 2,345 lines have 89 observed first-position `daiin` tokens versus 31.529 expected (2.823×; excess 57.471). Leave-one-folio-out recomputation across 88 represented folios leaves the ratio between **2.651× and 2.939×** for every omission. Omitting f108v has the largest decrease (2.651×); omitting f103v yields 2.674×. Thus the effect is not caused by any one folio, although a few folios contribute to its magnitude. LOFO is an influence diagnostic, not an independent significance test.

## Next experiment: exp_593
Test whether Currier-B P0 line-initial `daiin` is concentrated in folio/paragraph-opening lines versus continuation lines. Use IVTFF locus/line metadata only where parseable; document ambiguities, count all eligible line classes, and compare against a null controlling for within-line token inventory and length. A significant association must survive a predeclared comparison and multiple-testing control. Do not infer semantic meaning.

## Research integrity guardrails
- The 21-mechanism copy-buffer hybrid's 19/19 score is fit to a defined metric battery, not proof that it generated the manuscript and not decipherment.
- Keep hypotheses separate from executed results; include source hashes, code, outputs and workflow URLs.
- Preserve null/negative findings and avoid duplicating tests without a specific question.
- Do not spend OpenAI API credits for corpus analyses that reproducible Python can perform.
- Never infer the meaning of `daiin` from position alone.
