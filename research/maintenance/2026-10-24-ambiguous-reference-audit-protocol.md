# Historical ambiguous EXP reference inventory — 2026-10-24

## Implemented

`scripts/audit_ambiguous_exp_references.py` reads `research/EXPERIMENT_PATH_REGISTRY.json`, validates its collision map, and scans UTF-8 Markdown, RST and TXT for legacy EXP references with the seven ambiguous numeric aliases. It records file, line, alias, excerpt, and a heuristic classification. It does not edit source reports or reinterpret results.

`tests/test_ambiguous_exp_references.py` checks collision-table consistency, lexical boundaries, ignored code files, unique aliases, and nearby explicit canonical paths. `Voynich Check` now invokes these tests and writes `ambiguous-exp-references.json` as a 90-day artifact. The artifact is a triage inventory, not a list of proven errors.

## Mandatory interpretation

`REVIEW_REQUIRED` means an ambiguous numeric reference was detected without exactly one matching canonical path in a short local excerpt. It can be unambiguous in surrounding paragraphs. `EXPLICIT_PATH_NEARBY` is only a heuristic, not verification that a cited statistic came from that experiment.

This scan excludes Python, JSON, PDF, images, binary artifacts, connected Library content, and references using spellings outside the regular expression. It does not certify every historical report or the validity of its statistics. Human/source-level adjudication must inspect each flagged reference against its actual script, corpus, and result.

## Status

Code, tests and CI artifact step committed. A successful CI execution and inventory counts have not yet been independently observed; do not report them as completed. Never silently rewrite archived reports or renumber experiments.
