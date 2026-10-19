# Experiment 620 — parser audit note (partial)

## Scope and status
This is a targeted parser audit note, **not** a completed independent transcription audit. During the 613–617 workflow, the first implementation counted a digraph at the end of a token as a non-vowel-followed occurrence, even though the outcome is defined as the character *following* the digraph. That was inconsistent with the intended measure.

## Correction made
- Updated the 613–615 and 617 standalone Node scripts to include a `ch`/`sh` occurrence only when a character exists after the digraph.
- Recomputed their result files and reports from the current repository transcription files.
- Corrected ZL3b `$Q=T` `aeiouy` counts are now 2,340 `ch` occurrences and 1,051 `sh` occurrences, agreeing with the counts in exp612.
- The effect direction remains positive in both transcriptions after the correction. For ZL3b, the pooled difference is 5.52 percentage points; for IT2a it is 5.88 points. Narrower `aeiou` results also remain positive.
- exp618's word-type parser already required a following character.

## What remains unchecked
- No independent parser implementation has yet been run against the same files.
- No complete audit of all IVTFF markup edge cases, line continuations, damaged/uncertain tokens, or alternate transcription conventions has been completed.
- The Node scripts are committed as reproducibility artifacts, but this session calculated results in the analysis runtime; the scripts themselves have not been independently executed in GitHub Actions.

## Decision
**Partial pass / audit open.** The specific terminal-digraph inconsistency has been corrected and results recomputed. Do not mark the full independent parser audit complete until a second implementation and edge-case fixtures agree.
