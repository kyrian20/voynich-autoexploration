# EXP-625 — External methods integration plan (2026-10-20)

## Purpose
Convert the external scan into practical, low-cost tests for `kyrian20/voynich-autoexploration`. This is a protocol and prioritization note, not a claim that external findings have been reproduced.

## Immediate principle
Do not copy external conclusions. Reuse only methods, test design, controls, or artifacts whose provenance and exact behavior can be inspected. Keep our current parser discrepancy as a hard gate: EXP-602 records 1,466 ZL3b and 1,472 ZL3a token-list disagreements. Matching record IDs/counts is not token-level conformance.

## Candidate transfer table

| External source | What may be reusable | What must not be assumed | Our action |
|---|---|---|---|
| Pantani/voynich | Pytest fixture design, corpus-reader separation, explicit research-route index, human review workflow | Their proposed operator/border model or their reported metrics | Inspect reader/tokenizer tests and adapt only general fixture ideas after checking IVTFF policy |
| epilectrik/voynich | Pre-registered constraints, rival generators, adversarial controls, explicit rejected-claim ledger | Their “designed non-semantic artifact” conclusion or constraint tiers as independent validation | Extract the final surviving/rejected constraints and map each to existing experiments before proposing any new test |
| VoynichDuctus | Image-first glyph sampling, held-out image crops, explicit control corpora | Claimed “objective” glyph labels, DINO clusters as characters, or its entropy-based semantic diagnosis | Feasibility audit only: source/licence, alignment, label provenance, duplicate leakage and human-annotated held-out set |
| Dominik (Zenodo 23113674) | Frozen rules, held-out folios, alternate-transcription sensitivity | “Functional role” coverage as translation accuracy | Select one observable surface claim and test exact predictions on untouched folios, after code/data audit |
| Parisel (arXiv 2604.25979 v2) | Folio-level evaluation, Beta-Binomial mixture, explicit baseline | 89% reported accuracy as reproduced or directly comparable with our EXP-622/623 | Exact replication candidate only after tokenizer and `$L=A/B` metadata validation |
| Timm (Zenodo 19119470) | Control section/language/page type before interpreting scribal clusters | The alternative scribal account as established | Future image-based blinded audit; no transcription-only conclusion |
| Honeycutt (Zenodo 23068593) | Pre-registered layout/operator predictions against matched comparators | Paduan provenance or genre as established | Defer until comparator corpus and measurable predictions can be specified before inspection |

## Work order

### Gate 0 — tokenizer and header semantics
1. Preserve EXP-602 results as the immutable record of the original disagreement.
2. Build minimal IVTFF fixtures for ordinary tokens, comments/markers, square-bracket alternatives, braces, `@` markers, line/paragraph prefixes and malformed annotations.
3. Link each expected output to the applicable IVTFF specification; unresolved cases remain unresolved, not silently normalized.
4. Validate that Currier labels come from `$L=A/B`; do not infer them from `$Q` or `$I`.
5. Produce row-level before/after disagreement counts and representative diffs.

### Gate 1 — transfer the best external control, not the conclusion
Once Gate 0 passes, inspect the Epilectrik constraint/review ledger and map claims to our existing experiments. For each candidate record: claim ID, exact prediction, unit of analysis, corpus/transcription, split, baseline, rival generator, result, and whether it duplicates a test we already ran. Choose one untested control only after this map exists.

### Gate 2 — choose one confirmatory replication
Use a written decision rule:
- Choose Parisel if its precise features, code-equivalent definition, fitting procedure, and folio split can be reconstructed without ambiguity.
- Choose Dominik if at least one narrow surface claim has an exact, countable prediction and the required data/rules are available.
- Do not run both by default; prevent researcher degrees of freedom and duplicated work.
- Split by folio, not line or token. Report majority-class and metadata-only baselines, balanced accuracy, confusion matrix, and folio-level uncertainty.
- Treat ZL3b and IT2a as alternative transcriptions of one manuscript, not independent manuscripts.

### Gate 3 — image-based paleography as a separate project
Before any DINOv2/clustering run, require a documented image source and licence, verified folio/line/crop alignment, a human-labelled reference sample, and a folio-disjoint evaluation. Report cluster stability and human agreement. A cluster is not automatically a glyph, and a glyph is not automatically a linguistic unit.

## Definition of success
Success is a reproducible test with a clear baseline and falsifiable outcome, including a negative result. External projects' hypotheses remain hypotheses until independently reproduced. Structural predictability is not semantic decipherment.

## External references
- Pantani: https://github.com/Pantani/voynich
- Epilectrik: https://github.com/epilectrik/voynich
- VoynichDuctus: https://github.com/silveremartin-dev/VoynichDuctus
- Dominik: https://zenodo.org/records/23113674
- Parisel: https://arxiv.org/abs/2604.25979
- Timm: https://zenodo.org/records/19119470
- Honeycutt: https://zenodo.org/records/23068593
