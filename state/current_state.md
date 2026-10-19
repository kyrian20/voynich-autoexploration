# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589 and exp_590 executed; results saved)

## Canonical scientific checkpoint
The earlier project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`. It reports five pre-registered Section 2 characterization findings retained under the ≥2/3 alternative-transliteration rule; F4 retained in EVA-basic and ZL3a but failed in v101 where the o→sh edge had one observation. These are repository-reported findings, not independently rerun as part of exp_589/590.

## Operational status
The scheduled LLM-report workflow needs OpenAI API billing and produced HTTP 429 on 2026-10-19, consistent with the maintainer's statement that no API funds remain. It was not rerun. The corpus experiments use Python in GitHub Actions and do not need OpenAI API credits.

## exp_589 — daiin positional audit (executed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019  
Result: `experiments/exp_589_daiin_position_audit/result.md`; machine output: `results.json`.

Across the whole body, `daiin` is about 1.51× expected in first position in both ZL3b and ZL3a. The aggregate masks a dialect split: Currier A is below expectation overall (about 0.88×; one-sided p about 0.89), Currier B is about 2.75× expected (Monte Carlo p at the resolution floor 0.0005). This pattern is robust between the two checked-in EVA transcription versions under the script's conservative tokenization.

## exp_590 — folio-range sensitivity analysis (executed)
Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256487097  
Result: `experiments/exp_590_daiin_section_stratification/result.md`; machine output: `results.json`.

Within five coarse Currier-B folio-number bins, the first-position enrichment remains positive (1.62×–4.10×), and all five Monte Carlo results remain below 0.05 after Holm adjustment across the five-bin B family. The two populated Currier-A ranges differ: f001–f066 is below expectation (0.72×), while f085–f102 is above expectation (1.68×; adjusted p=0.031 in its secondary two-test family). Thus Currier A does not exhibit a uniform aggregate pattern.

**Important caveat:** exp_590 bins are heuristic ranges by folio number inherited from an older simplified script, not authoritative codicological section labels. Treat the result as a robustness check, not as definitive section-by-section scholarship.

## Next active experiment: exp_591
Analyze exact IVTFF body-locus subtypes (P0/P1/Pb/Pc/Pr) separately within Currier A and B. Determine whether the Currier-B first-position excess persists in the dominant locus category (P0), and do not overinterpret sparse subtypes. Apply Holm correction within predeclared B and A families. Report all groups, including null results.

## Research integrity guardrails
- A 21-mechanism generator's 19/19 score is compatibility with a defined metric battery, not proof that it generated the manuscript and not decipherment.
- Do not promote hypotheses or proposed analyses to validated findings before execution.
- Keep corpus/version hashes, protocols, outputs and workflow URLs together.
- Do not spend OpenAI API credits for analyses that reproducible Python can perform.
- Never infer the meaning of `daiin` from its positional distribution alone.
