# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589–exp_591 executed; exp_592 planned)

## Canonical scientific checkpoint
The earlier project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`. The five pre-registered Section 2 findings are reported retained under the ≥2/3 alternative-transliteration rule; F4 retained in EVA-basic and ZL3a but failed in v101 where the o→sh edge had one observation. These are repository-reported results, not independently rerun as part of exp_589–591.

## Operational status
The scheduled LLM-report workflow needs OpenAI API billing and produced HTTP 429 on 2026-10-19, consistent with the maintainer's statement that no API funds remain. It was not retried. Corpus analyses now run through ordinary GitHub Actions/Python, avoiding the paid API.

## exp_589 — daiin positional audit
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
Results: `experiments/exp_589_daiin_position_audit/result.md` and `results.json`.

Across the body, `daiin` is about 1.51× expected at line start in both ZL3b and ZL3a. The aggregate masks a dialect split: Currier A is below expectation overall (about 0.88×, one-sided p≈0.89), whereas Currier B is about 2.75× expected (p at the 2,000-draw Monte Carlo floor 0.0005). This direction replicates between the two checked-in EVA transcription versions under the selected parser.

## exp_590 — folio-number-range sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
Results: `experiments/exp_590_daiin_section_stratification/result.md` and `results.json`.

Across five coarse Currier-B folio-number bins, enrichment is positive (1.62×–4.10×); all five one-sided Monte Carlo tests remain below 0.05 after Holm adjustment across the B-bin family. Currier A shows opposite directions in its two populated bins (0.72× for f001–f066, 1.68× for f085–f102). The ranges are heuristic folio-number proxies, not authoritative manuscript section labels.

## exp_591 — exact body-locus sensitivity
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256723800  
Results: `experiments/exp_591_daiin_locus_stratification/result.md` and `results.json`.

The Currier-B result persists in the dominant IVTFF body-locus P0: 89 initial `daiin` tokens versus 31.53 expected, 2.823× enrichment, Holm-adjusted p=0.0015 across the three B locus strata with at least 50 lines. P1 is elevated too (4 vs 1.11 expected; adjusted p=0.025) but sparse; Pb is positive but not significant (adjusted p=0.210). Currier-A P0 is below expectation (0.87×, adjusted p=0.902). Locus codes are not assigned semantic interpretations.

## Next experiment: exp_592
Perform leave-one-folio-out influence analysis for Currier-B P0. Test whether the 2.82× line-initial excess remains when each folio is omitted in turn, and report which folios contribute most to observed and expected counts. This addresses whether a few high-leverage folios drive the aggregate. Treat per-folio tail rankings as diagnostics, not new significance claims.

## Research integrity guardrails
- The 21-mechanism copy-buffer hybrid's 19/19 score is fit to a defined metric battery, not proof that it generated the manuscript and not decipherment.
- Keep hypotheses separate from executed results; include source hashes, code, output and workflow URLs.
- Preserve null/negative findings and avoid repeating tests without a specific new question.
- Do not spend OpenAI API credits for corpus analyses that reproducible Python can perform.
- Never infer the meaning of `daiin` from position alone.
