# Current State — Voynich Cryptanalyst

**Last updated:** 2026-10-19 (repository audit; exp_589 implementation submitted for review in PR #1; execution pending)

## Canonical research checkpoint
The latest pre-existing scientific checkpoint remains **exp_588**, summarized in `state/transliteration_replication_final_summary.md` and earlier content of this file. The 2026-04-13 checkpoint reports all five pre-registered Section 2 findings retained under the registered ≥2/3 transliteration criterion; F4 retained in EVA-basic and ZL3a but failed in v101 where the o→sh edge count was one. Treat this as a repository-reported result until independently rerun.

## Operational status
The scheduled LLM report workflow needs OpenAI API billing and hit HTTP 429 on 2026-10-19. No LLM workflow retry was initiated. New corpus experiments are separated from that workflow so they can run with standard GitHub Actions and Python without OpenAI API credits.

## New experiment exp_589
A deterministic test has been prepared in feature branch `exp-589-daiin-audit` and submitted as PR #1 to examine whether body-text token `daiin` is overrepresented at line-initial position when expected counts are conditioned on each line's own token composition and length. It applies 2,000 within-line permutations, separately for ZL3b and ZL3a and for Currier A/B subsets, and records SHA-256 source-file hashes.

**Status: implementation on feature branch; PR #1 open; results not yet generated or reviewed.** No outcome is currently claimed. Results are conditional on the parser's conservative tokenization, and positional bias cannot establish meaning or decipherment.

## Guardrails
- Never label a hypothesis or proposed experiment as validated.
- Do not infer the generative architecture is the manuscript's actual authoring mechanism or a decipherment.
- Do not overwrite older experiment records; append new, traceable experiment IDs.
- Do not call the paid OpenAI API for these corpus analyses.
- Next step: review the GitHub Actions result from `.github/workflows/voynich-corpus-experiments.yml`, validate counts/hashes/parser coverage, then decide whether to retain or reject the positional-affinity hypothesis.
