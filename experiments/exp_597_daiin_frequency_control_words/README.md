# exp_597 — Lexical controls for line-initial daiin

## Question
Is the Currier-B line-initial enrichment observed for `daiin` unusually strong compared with a small, predeclared-in-script set of common EVA tokens?

## Protocol
- Corpus: checked-in ZL3b IVTFF transcription; generic P-locus body lines with at least two cleaned tokens.
- Targets: `daiin` plus `aiin`, `chedy`, `dain`, `saiin`, `qokaiin` (frequent controls already counted descriptively in exp_589).
- For each word and Currier dialect, compare observed first-token count with expected count under uniform within-line position, preserving each line's token inventory and length.
- 10,000 Monte Carlo draws per word/dialect; Holm correction for six upper-tail tests separately within A and B.

## Limits
This is a post-hoc sensitivity analysis, not a preregistered semantic taxonomy. The control tokens are not perfectly frequency-, morphology-, or function-matched. Treat as context for specificity, not as proof of a grammatical category or decipherment.
