# Independent byte-level verification of PR #287 IVTFF receipt — 2026-11-16

## Scope and provenance

- PR: https://github.com/kyrian20/voynich-autoexploration/pull/287 (draft, not merged at verification).
- Exact CI run: https://github.com/kyrian20/voynich-autoexploration/actions/runs/43789138871
- Workflow head: `afe0aaabef28cd6dde1b57dc29d83312db7d7e10`.
- Artifact: `ivtff-minimum-format-43789138871`, ID `14191233024`, ZIP size 940 bytes.
- GitHub-advertised SHA-256: `9f316ae1993389803d7b0af7b66db0bf6e2dbd45279e7a4547d8326786c31fd6`.
- Downloaded original via GitHub connector; **do not commit the ZIP**. The artifact remains in GitHub Actions.

## Independently executed verification

The downloaded ZIP's locally recalculated SHA-256 **matches** the advertised digest. ZIP contains exactly:

- `ivtff-minimum-format.json` (1480 bytes), SHA-256 `ee9d6200204e21ca68159a6684c42d1f320e72b47f36e8ba8c12e2121117fd3f`.
- `ivtff-minimum-format.sha256` (116 bytes), SHA-256 `d3b031d5a82f90238e30b4911ac218f952fccdbbb15a68910e319f3b72a0124f`.

The manifest records the same JSON SHA-256; its pathname is an ephemeral GitHub runner path and is not evidence of a local source file. The JSON reports `PASS` for all three listed corpora, with no reported file-level errors:

| Source | Reported SHA-256 | Bytes | Physical lines |
| --- | --- | ---: | ---: |
| eva_zl3b.txt | bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc | 411671 | 8510 |
| zl3a.txt | 56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2 | 411710 | 8513 |
| eva_it2a.txt | 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5 | 342104 | 5444 |

## Reproduction and falsification

Download artifact ID `14191233024` from the linked run. Run:

```bash
python research/maintenance/verify_pr287_ivtff_artifact.py github-actions-artifact-14191233024.zip
```

Exit 0 and `VERIFIED_RECEIPT_ONLY` require the fixed ZIP digest, exact two-member manifest, matching inner SHA-256, exactly three unique expected corpus source/digest pairs, and PASS with empty errors. A modified ZIP, tampered inner JSON, or duplicate/missing source must fail. Local verification also ran four cases: original positive; one flipped ZIP byte; modified JSON with unchanged inner checksum and newly computed outer digest; duplicate corpus record with recomputed inner and outer digests. **4/4 passed locally**, Python unittest harness was temporary and is not claimed as CI. The published verifier retains the same decision rules but must be independently reviewed.

## Limits and next decision

This verifies the **integrity of the downloaded receipt** and the identity hashes *reported in that receipt*, not independently the three corpus bytes, full IVTFF grammar, provenance of historical runs, or scientific claims. It does not establish that the PR #287 code is correct, reviewed, or safe to merge. Original corpora, frozen results, and committed claims were not modified. The next gate is independent review of #287 against #278 and exact-head CI for any future merge candidate; avoid merging duplicate stacked PRs. No linguistic meaning or decipherment is inferred.
