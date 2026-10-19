# exp612 — ch/sh stratification by Currier class and IVTFF $I label

## Status
Computed from the repository's current transcription files in this session. This is a descriptive stratification, not a causal or linguistic decoding result.

## Method
For each transcription, tokenize the IVTFF line bodies after removing markup. For each occurrence of `ch` or `sh) followed by a character, record whether that next character is in EVA vowel set `aeiouy`. Compare only matched folio × exact token length × exact digraph-position cells containing both contexts, then stratify by the folio's IVTFF `$Q` label (Currier class) and `$I` label. Sparse labels are shown but must not be over-interpreted. Repeated tokens and section/template composition remain potential confounds; no p-value is claimed.

## Dataset integrity
- ZL3b source SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` (recorded in exp611)
- IT2a source SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` (recorded in exp611)

## Main finding
The ch/sh vowel-rate difference varies considerably by Currier label. In the large `$Q=T` stratum, sh exceeds ch by about 5.52 percentage points in ZL3b (89.15% vs 83.63%) and 5.88 points in IT2a (88.91% vs 83.03%). Other labels show smaller differences or sparse counts. This is consistent with a recurring descriptive contrast, but does not isolate whether the cause is lexical templates, section, transcription conventions, or a distinct distributional rule.

## Key controls / limitations
- Exact length and position matching is applied within folio before aggregation.
- A and B are reported separately from other Q labels; IVTFF Q labels are not all Currier A/B classes, so all labels are retained as given rather than relabelled.
- The within-cell observations are not independent; a clustered bootstrap/permutation at folio level is required before inferential claims.
- The `$I` label is treated as metadata, not assumed to mean a scribal hand without independent validation.

## Decision
**Partial support only.** The effect is not a uniform constant across labels. Next priority is a folio-clustered permutation/bootstrap within sufficiently populated strata and an out-of-sample check; do not claim a translation or causal explanation.
