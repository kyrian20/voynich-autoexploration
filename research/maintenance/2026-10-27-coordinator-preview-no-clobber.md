# Coordinator SVG preview: exclusive output creation (2026-10-27)

**Scope:** one concrete file-integrity defect in the coordinator-only visual workflow. No scientific experiment or semantic inference.

## Defect and reproduction

At baseline `master` commit `44ec81a2180b7a51f5398f0cc6ed6ef46ed67563`, `scripts/render_coordinator_mask_preview.py:main` wrote SVG bytes with `Path.write_bytes()`, which opens an existing path in truncating mode. The caller could accidentally pass `--out` equal to `--source`, `--plan`, an existing coordinator SVG, or a reviewed artifact. Since the SVG embeds the full original image bytes, this is an avoidable data-loss and review-provenance hazard. This is a source-code defect; no actual historical file corruption is alleged.

## Repair

The CLI now creates the SVG using `Path.open('xb')` (exclusive creation) rather than overwriting existing files. This rejects existing paths, including source/plan aliases and symlinks, while retaining the exact SVG rendering function and the warning that previews are **not** blinded annotator inputs. The separate flattened PNG exporter already used exclusive creation and was not changed.

## Regression contract

`tests/test_coordinator_mask_preview.py` adds CLI-level tests with synthetic source bytes and an explicitly hashed plan:

1. A fresh SVG is created and contains the coordinator warning; a second invocation cannot replace it.
2. Passing the original source, the plan, or an existing reviewed asset as `--out` raises `FileExistsError` and leaves its bytes unchanged.
3. An output symlink targeting the source is rejected without modifying the source.

Run: `python -m unittest discover -s tests -p 'test_coordinator_mask_preview.py' -v`. The canonical `Voynich Check` already runs this test module. **CI and integration evidence must be added only after the run completes.**

## Provenance and limitations

Original Voynich transcriptions, frozen holdout manifests, label inventory, annotation queues, negative results and scientific ledgers are unchanged. The tests use artificial byte strings, not manuscript images; they validate only file non-overwrite behavior. The coordinator SVG still embeds recoverable original image data, must not be distributed as blinded input, and does not certify masking, image-to-label alignment, independent annotation, or translation. The visual semantic study remains **BLOCKED**.

No EXP ID assigned: this is a software integrity repair, not a new falsifiable language experiment. Scientific assessment remains scheduled for 2026-11-22, without a decipherment promise.
