# Guard against invalid null-model parameters in the partial Zhang–Sheng audit

**Date:** 2026-11-01. **Class:** bounded integrity/parameter validation repair; no new experiment or decipherment claim.
**Base:** `master` `8dc31bb784223f46ad56df911a9968d4a0716528`.
**Affected code:** `research/maintenance/2026-11-01-zs-wordpair-audit/wordpair_audit.py::metric`.

## Concrete defect and falsification

Before this change, `shuffles=0` and negative integer values skipped the `for _ in range(shuffles)` null-model loop without raising an error. The expected co-line pair matrix remained zero and the subsequent standardized score used `(observed - 0) / sqrt(0.5)` instead of a randomized expectation. This can produce misleading numerical outputs (or undefined correlations) without having executed a single shuffle. `top_k=-1` silently selected all but one type, while `top_k=0` or malformed types could fail late; `seed=True` was silently interpreted as integer 1.

**Acceptance criterion (defined before CI):** the metric must reject zero, negative, boolean, non-integral, string and null shuffle counts; reject invalid vocabulary sizes and non-integer seeds **before computing statistics**. Historical valid integer parameters must remain accepted. The existing frozen 54-row archive and two-row replay must remain untouched and pass their current CI contracts.

## Repair and tests

At the entry to `metric()`, use strict `type(...) is int` checks: `shuffles > 0`, `top_k > 0`, integer `seed`. This is deliberately narrower than redesigning the paper's unknown formula or the historical page-block split.

Two regression methods in `tests/test_zs_wordpair_source_lock.py` cover invalid counts, vocabulary sizes and seeds, including booleans. The tests require no NumPy, no corpus mutation, no new random runs and no scientific-cycle state changes.

Commands to verify on the PR commit (and again after merge):
```sh
python -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -O -m unittest discover -s tests -p 'test_zs_wordpair_source_lock.py' -v
python -m unittest discover -s tests -p 'test_zs_wordpair_archive_contract.py' -v
python scripts/check_corpus_integrity.py
```

## Preservation and limits

No corpus, seed, archived result, holdout manifest, committed claim or experimental interpretation is modified. The historical archive used 20 shuffles and positive vocabulary sizes, so this repair **does not recalculate or rehabilitate** its 54 scores. It addresses malformed future invocations only. The physical-leaf overlap in historical page halves, incomplete Zhang–Sheng replication, IVTFF adjudication and EXP-170 source provenance remain separate open matters.

**Verification status:** source and regression changes proposed on a branch; record the actual PR and post-merge CI IDs before claiming closure. This repair does not establish any Voynich plaintext.
