# exp_592 — Leave-one-folio-out influence audit

**Question:** Does the Currier-B P0 initial-position enrichment for `daiin` (exp_591: 89 observed first tokens vs 31.53 expected; 2.82×) remain when each folio is omitted in turn?

## Protocol
- Corpus: checked-in `data/transcriptions/eva_zl3b.txt`; SHA-256 recorded in output.
- Filter: Currier B, exact IVTFF body locus P0, minimum two clean tokens per line.
- For a set of lines, expected first-position `daiin` is the sum of each line's `daiin` count divided by that line's token count. This preserves the line-wise inventory/length null used in exp_589–591.
- Deterministically omit one folio at a time and recompute observed, expected, enrichment and excess. Also rank folios by observed first counts and observed-minus-expected excess.
- No p-values are added: LOFO differences and per-folio rankings are influence diagnostics, not independent significance tests.

## Interpretation rules
A strong enrichment that remains across all leave-one-out subsets suggests no single folio is sufficient to explain the pooled signal. The minimum/maximum leave-one-out enrichment and folios with greatest impact must be reported. Per-folio ranks are post hoc and must not be treated as discoveries or semantic evidence.
