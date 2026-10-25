# IVTFF row adapter: physical-newline guard (2026-10-25)

**State:** proposed fix on a review branch; no new EXP and no semantic inference.

## Reproducible defect

The frozen lexer `scripts/ivtff_lossless.py` recognizes physical CR/LF when scanning top-level characters, but its angle-bracket branch skips to the closing `>` in one span. Therefore an input such as the Python literal `"a<!hidden\\ncomment>b"` can carry a physical newline inside a comment without the ordinary `physical_newline_in_payload` diagnostic. Projecting that string as one physical row risks accepting malformed input and collapsing a source boundary.

## Repair and scope

The additive `scripts/ivtff_rows.py::tokens_rows` rejects any CR or LF in the raw text of each supplied physical row before token projection; `tokens_scoped_rows` delegates to it and receives the same guard. Non-`Payload` inputs now fail explicitly with `TypeError`. The frozen `scripts/ivtff_lossless.py` remains unchanged to preserve historical provenance and snapshot hashes.

Regression fixtures in `tests/test_ivtff_lossless.py` exercise CR, LF and CRLF embedded inside an angle-bracket comment through both adapter entry points, plus wrong input type. Run: `python tests/test_ivtff_lossless.py`. CI runs this command in `Voynich Check`.

## Evidence and limitations

The implementation and synthetic regression are committed together on this branch; CI success must be checked at the exact head SHA before merging. This is an **adapter-level** guard only: direct users of the frozen `tokens()` API are not protected by it. No corpus, historical result, experiment identifier, held-out partition or scientific claim is changed. The fixture is synthetic; this report does not claim any original transcription contains the malformed construct. Full IVTFF compliance, historical caller migration and corpus/Library reconciliation remain open.

## Next action

Verify complete PR CI and post-merge master CI. Independently inventory historical callers of the frozen lexer before deciding whether a versioned strict reader is needed. Do not mutate the frozen reader merely to make this test pass.
