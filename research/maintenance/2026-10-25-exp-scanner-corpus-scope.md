# Scope correction: EXP reference scanner vs frozen corpora — 2026-10-25

## Confirmed incident
The historical-reference scanner previously traversed every UTF-8-like `.txt` file, including the **frozen source corpora** under `data/transcriptions/` and `data/reference_corpora/`. The archived Voynich Check artifact from run [40137054729](https://github.com/kyrian20/voynich-autoexploration/actions/runs/40137054729) listed two files as unreadable under this report-oriented scan: `data/transcriptions/v101_claston.txt` and `data/reference_corpora/latin/caesar_gallic_wars.txt`. This is not, by itself, evidence of damaged corpus bytes or a failed historical experiment. The corpus integrity and identity overlays are separate controls.

## Implemented correction
`scripts/audit_ambiguous_exp_references.py` now excludes the two **entire raw corpus trees** from the historical-document reference inventory, reports their exact excluded paths as `excluded_raw_corpora`, and refuses to dereference symlinks while scanning selected documents. It reports skipped symlinks and treats them as incomplete selected-document coverage. It continues to report unreadable UTF-8 files **outside** those raw-corpus trees, with no fallback that could silently alter characters.

New tests cover a deliberately non-UTF-8 transcription, a non-UTF-8 reference corpus, an ordinary historical document, and a symlink to another file. Existing unreadable-document and lexical boundary tests remain. No original corpus, frozen result, claim ledger, or historical reference has been edited.

## Interpretation and remaining work
The scanner now measures references in *documents*, not arbitrary frozen input bytes. This removes two category errors from its unreadable-document count; it **does not** certify the original encoding, identity or fitness for language comparison of those corpora. In particular, the Caesar file remains excluded as a Latin baseline under `research/CORPUS_IDENTITY_REVIEW.json` because its recorded work is an English translation. The v101 byte-level encoding and IVTFF/transcription parser conformance remain separate open provenance tasks.

This is a code-and-regression change, not a new Voynich decipherment experiment. Verification gate: PR CI must run `test_ambiguous_exp_references.py` and publish the revised `ambiguous-exp-references.json` artifact before this incident can be marked closed.
