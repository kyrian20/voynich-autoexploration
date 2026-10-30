# Guard of visual-pilot locator/folio consistency across all partitions

Date: 2026-10-26. **Status: maintenance fix awaiting CI and review.** No EXP number, no new semantic test, no holdout scoring.

## Reproducible defect and bounded fix

At master `6150bd9181ccae3bf6188e652aef5f9b22ed1326`, `scripts/select_visual_pilot_v2.py` checked the `id`/`folio` relationship only for records whose numeric leaf belonged to `train`. `check_inventory_provenance` checked edition, declared source SHA-256 and duplicate keys for all rows, but not the row's own locator/folio correspondence.

Synthetic counterexample (same source declarations as the existing `VisualPilotIntegrityTests.fixture`): set the IT2a test row `folio=f70r` and `id=f2r.99`, leaving `source_sha256` and `occurrence_id` unchanged. The previous selector silently returned the normal train selection. The same bypass affected development rows. This is an **input validation gap**, not evidence that the frozen inventory contains corrupted records.

The fix validates a nonempty, whitespace-exact `folio` and a nonempty `folio + "." + locus_suffix` relationship on **every** inventory record before any selection. No record is promoted into training. The old train-specific check remains as defense in depth.

## Regression plan and immutable data

Four test methods were added to `tests/test_visual_annotation_queue.py`:

1. A test row with a locator from another folio must raise.
2. A development row with a mismatched locator must raise.
3. Empty locus suffix and absent folio in a nontraining row must raise.
4. A valid named `fRos.0a` record must remain excluded, with the original train selection unchanged.

The pre-existing regression `test_archived_pilot_selection_is_unchanged` compares the entire output against the frozen `pilot-selection-v2.json`; it must continue to pass. The canonical CI executes this test file and the corpus integrity checks. No original transcriptions, v2 holdout manifest, inventory gzip, frozen selection, experimental outputs, or historical scripts are changed.

**Reproduction commands** (to be confirmed by a completed CI run):

```sh
python -m unittest discover -s tests -p 'test_visual_annotation_queue.py' -v
python -m unittest discover -s tests -v
python scripts/audit_repository_operations.py
python scripts/check_corpus_integrity.py
```

No randomness is involved; seed: not applicable. Synthetic fixture source hashes are deterministic placeholders, not claims of authentic corpus hashes. The real-source and frozen-selection tests are separate.

## Scope limits and follow-up

This check only validates *declared* folio/locator consistency. It does **not** independently verify that every inventory row was extracted from the indicated source line, that its `raw_line_sha256` matches the raw corpus line, or that the editorial IVTFF transcription is correct. Source-file SHA-256 checks do not, by themselves, authenticate a potentially fabricated inventory row. A separate source-line reconciliation is required before using this inventory for any semantic inference.

The visual pilot and held-out folios remain **BLOCKED** for semantic validation; the test leaves were previously exposed. No new decipherment rule, translation, image alignment or semantic conclusion is asserted. This is a narrow repair, not a repository-wide cleanup.
