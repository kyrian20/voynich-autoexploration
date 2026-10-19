# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (exp_589 executed successfully; diagnostic result recorded)

## Canonical scientific checkpoint
The earlier project checkpoint remains exp_588, summarized in `state/transliteration_replication_final_summary.md`. It reports the five pre-registered Section 2 characterization findings retained under the ≥2/3 alternative-transliteration rule; F4 retained in EVA-basic and ZL3a but failed in v101, where the o→sh edge had only one observation. These are repository-reported results, not independently rerun as part of exp_589.

## Operational status
The scheduled LLM-report workflow needs OpenAI API billing and produced HTTP 429 on 2026-10-19, consistent with the maintainer's statement that no API funds remain. That workflow was not rerun. The corpus experiment is independent of the paid API and ran successfully in GitHub Actions.

## exp_589 — daiin positional audit
**Status: executed successfully on master; results recorded** in `experiments/exp_589_daiin_position_audit/result.md` and `results.json`. Run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39256111019

The API-free Python script tested body-text first-token frequency in ZL3b and ZL3a with 2,000 within-line Monte Carlo permutations. In both transcriptions, all-body `daiin` was about 1.51× the expectation. The dialect split is decisive in direction: Currier A was below expectation (about 0.88×, p≈0.89), while Currier B was about 2.75× expected (p at the simulation floor 0.0005). The output reports counts, file hashes, parsing counts and seeds.

**Conclusion is narrow and conditional:** the initial-position excess is robust between these two EVA transcript versions for Currier B, not Currier A, under the chosen tokenizer and within-line exchangeability null. The 0.0005 value is the resolution floor of only 2,000 simulations, not a precise p-value. This says nothing by itself about the semantic meaning of `daiin` or whether the manuscript is deciphered.

## Known limitations and next step
The first-pass null preserves each line's token inventory and length but does not yet stratify by section, paragraph role, folio, or uncertain-transcription patterns. Next experiment: predeclare stratification by section and line/locus subtype, report every stratum, and check whether the Currier B initial excess persists without any single section or line class dominating. Preserve negative/null results. Do not repeat the basic aggregate test without a specific reason.

## Research integrity guardrails
- The 21-mechanism copy-buffer hybrid's 19/19 score is compatibility with a particular metric battery, not proof it is the manuscript's actual generative mechanism and not decipherment.
- Do not promote hypotheses or proposed analyses to validated findings before execution.
- Keep corpus/version hashes, protocols, result files and run links together.
- Avoid paid OpenAI API calls for corpus analyses when reproducible Python is sufficient.
