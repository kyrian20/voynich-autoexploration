# EXP-602 identifier collision adjudication — 2026-10-22

## Scope and decision

The repository contains two distinct experiment directories using the same numeric label:

- `experiments/exp_602_independent_ivtff_parser_audit/`
- `experiments/exp_602_heldout_predictive_test/`

They are different studies, not duplicate exports. Do not rename either directory or assign a canonical numeric EXP-602 until commit history and every external reference have been reconciled. For current documentation and discussion, use the temporary, path-qualified aliases:

- **GH-602-PARSER-AUDIT** — independent IVTFF parser/tokenizer agreement.
- **GH-602-HELDOUT-PREDICTION** — held-out folio positional prediction.

These aliases are descriptive labels, not a renumbering of the historical record.

## Evidence by artifact

### GH-602-PARSER-AUDIT

Primary artifacts:
- `README.md`
- `script.py`
- `results.json` (protocol v1)
- `results_v2.json` through `results_v7.json`

The current `results_v7.json` states that Parser A and Parser B have the same record keys and zero field mismatches for both ZL3b (5,385 records; 227 folio headers) and ZL3a (5,389 records; 227 folio headers). The primary six-token Currier-B/P0 summaries also match between the two parsers in v7. Earlier versions are retained as history and must not be described as current results.

Interpretation is narrow: this supports implementation agreement under the declared normalization policy. It does not independently certify every IVTFF convention, the transcription itself, or linguistic/semantic hypotheses. ZL3a and ZL3b are related transcriptions, not independent manuscript witnesses.

### GH-602-HELDOUT-PREDICTION

Primary artifacts:
- `README.md`
- `script.py`
- `results.json`
- `result.md`

The fixed folio-hash split has 1,797 training lines / 60 folios and 528 held-out lines / 21 folios. For primary target `daiin`, log-loss gain (conditional inventory baseline minus train-only global model) is −0.0813058, with folio-cluster bootstrap 95% interval [−0.1117409, −0.0564076]. The predeclared positive-prediction criterion therefore fails. Controls `dain` and `saiin` show the same direction.

The baseline conditions on each held-out line's token inventory, so it is a diagnostic conditional null rather than a deployable predictor. This result does not erase descriptive positional enrichment, but it does not demonstrate out-of-sample predictive improvement or decipherment. Keep the split frozen; do not tune on these held-out folios.

## Reconciliation rules

1. Preserve both directories, all result versions, and workflow history.
2. Cite the path-qualified aliases above until commit chronology, all cross-references, and any Library-side records have been reconciled.
3. Do not combine the parser-audit counts with the held-out prediction metrics; they answer different questions and use different protocols.
4. Before the next predictive experiment, independently validate IVTFF line-ID coverage and Currier metadata parsing, then freeze the population and source hashes.
5. Do not allocate a new EXP number until the global experiment register and historical references have been reconciled.
6. Treat all findings as structural/statistical only; neither experiment deciphers the manuscript.

## Reproducibility pointers

- Parser audit directory: `experiments/exp_602_independent_ivtff_parser_audit/`
- Held-out prediction directory: `experiments/exp_602_heldout_predictive_test/`
- Repository register: `research/EXPERIMENT_REGISTER.md`
- Next-test protocol: `research/next_decisive_test_plan_2026-10-22.md`
