# exp_595 — Cross-transcription replication of paragraph-marker pattern

**Run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767  
**Status:** analysis step and Python compile-check succeeded; generated JSON is present in the repository. Final job status was still finishing when checked.  
**Sources:** ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`; ZL3a SHA-256 `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`.

## Main finding

The exp_594 pattern reproduces almost exactly in ZL3a under the same parser:
- Currier B, lines without explicit `<%>`: ZL3b 97 initial `daiin` hits / 2,056 lines, expected 32.279, enrichment **3.005×**; ZL3a 97 / 2,056, expected 32.383, enrichment **2.995×**. In both, 5,000-draw Monte Carlo upper-tail p=0.0002, Holm-adjusted p=0.0004.
- Currier B, explicit `<%>` lines: 0 first-position hits out of 492 lines in both versions, expected 2.827; lower-tail p≈0.049, Holm-adjusted p≈0.098. This does not meet the adjusted 0.05 threshold.
- Currier A, explicit `<%>` lines: 1 hit / 236 lines, expected 6.993 in both versions; lower-tail adjusted p=0.0124 (ZL3b) and 0.0076 (ZL3a).
- Marker counts are identical across the two files (4,105 eligible lines, 728 starts, 729 ends), and nearly all reported values agree. The B no-start enrichment differs by only 0.00972×.

## Interpretation

The strongest result is now robust across the two checked-in transcriptions: **Currier-B P0 line-initial `daiin` is strongly overrepresented on lines not explicitly marked with `<%>`**. The zero observed B initial hits on marked paragraph-start lines is suggestive but does not survive Holm correction as a lower-tail test.

This does **not** prove that every unmarked line is a continuation: IVTFF paragraph boundaries are transcription decisions, and absence of a marker may reflect incomplete annotation. Nor does the pattern reveal the word's meaning. The two transcriptions share source lineage/annotation conventions, so this is cross-version robustness rather than fully independent external replication.

## Next block (exp_596–599)

1. **exp_596:** paired line-by-line comparison of ZL3a vs ZL3b on matched line IDs; enumerate every token/marker disagreement in the target groups before interpreting the near-identical aggregate statistics.
2. **exp_597:** compare line-initial enrichment of `daiin` against frequency-matched control words, with a predeclared control set and Holm correction.
3. **exp_598:** folio-cluster bootstrap for Currier-B no-start-marker enrichment, resampling folios rather than treating lines as independent.
4. **exp_599:** sensitivity to tokenizer rules (punctuation, uncertain readings, markup), preserving the same folio set and reporting all variants.

All four are API-free and should reuse existing corpus assets, hashes and parser rules. Avoid calling any result a decipherment.
