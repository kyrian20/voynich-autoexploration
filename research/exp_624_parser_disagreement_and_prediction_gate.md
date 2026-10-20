# EXP-624 planning note — resolve tokenizer disagreement before Currier A/B prediction

Date: 2026-10-20

## Trigger
A review of the existing EXP-602 artifacts found that the independent parser audit is not a successful token-level conformance result, despite agreeing on record keys and counts.

## Verified existing results
- `experiments/exp_602_independent_ivtff_parser_audit/results.json` reports 5,385 common record IDs for ZL3b and 5,389 for ZL3a, with no record-ID disagreements.
- It also reports **1,466 token-list disagreements for ZL3b** and **1,472 for ZL3a**. Therefore, record extraction agreement must not be presented as tokenizer agreement.
- Example disagreements include Parser A extracting a token from an IVTFF square-bracket alternative while Parser B preserves the entire bracket payload as one item; other differences split letter sequences differently around transcription conventions. These need format-aware adjudication against IVTFF 2.0.2, not a majority vote between parsers.
- `experiments/exp_602_heldout_predictive_test` is a held-out **line-initial token-position** test in Currier B/P0. It is not the proposed held-out Currier A-vs-B classifier and must not be counted as one.

## Decision
Do not start the new Currier A/B prediction experiment yet. First resolve the tokenizer disagreement with a small, explicit fixture suite and a written tokenization policy. Keep the original parser audit results immutable as a record of the discrepancy; do not overwrite them to make the audit appear successful.

## Required parser fixtures
1. Ordinary EVA tokens separated by whitespace, period, and comma.
2. Inline IVTFF comments and angle-bracket markers, including `<! ... ?>`, `<%>`, and `<$>`.
3. Square-bracket alternatives such as `[reading:alternative]`, with expected handling documented from the official format.
4. Brace annotations and `@number` markers.
5. Paragraph/line marker variants and slot prefixes.
6. Header metadata proving that `$L=A/B` supplies Currier language while `$Q` and `$I` are not substitutes.
7. Malformed or incomplete annotations: report as unresolved rather than silently inventing tokens.

## Acceptance gates before prediction
- Every fixture has hand-authored expected output and a rationale linked to IVTFF documentation.
- Both parser implementations either agree on normalized tokens or each disagreement has an explicit, documented policy resolution.
- Report row-level token disagreement counts and examples after resolution.
- Validate $L labels from headers and split by folio, keeping every record from a folio in one partition.
- Freeze a small feature set and all controls before evaluation.
- Compare the Currier A/B classifier against majority-class and metadata-only baselines; report balanced accuracy, confusion matrix, folio-level uncertainty, and sensitivity across ZL3b/IT2a without treating them as independent manuscripts.

No new prediction score is reported in this note. It is a reproducibility gate, not a language or decipherment claim.
