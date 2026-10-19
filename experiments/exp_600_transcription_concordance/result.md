# exp_600 — Results: ZL3b/ZL3a transcription concordance

**Execution date:** 2026-10-19  
**Successful workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39259781970  
**Machine-readable result:** `results.json`

## Why this audit matters

Previous exp_589–599 reports compared ZL3a and ZL3b and observed almost identical statistics. That agreement must not be presented as two independent manuscript samples. This audit aligns each IVTFF text record by its full line identifier before the comma and measures how much the cleaned token sequence actually differs.

The parser was broadened after the first pass to include compound folio identifiers such as `f67r1.3` and nonnumeric Rosettes identifiers such as `fRos.1`. The final run reports zero skipped identifiers and 227 folio headers per version.

## Coverage and alignment

| Measure | ZL3b | ZL3a |
|---|---:|---:|
| Source bytes | 411,671 | 411,710 |
| SHA-256 | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2` |
| Folio headers recognized | 227 | 227 |
| Unique text-line identifiers | 5,385 | 5,389 |
| Duplicate line identifiers | 0 | 0 |
| Unparsed line identifiers | 0 | 0 |

- **5,385 line identifiers align exactly** between the files.
- There are no identifiers present only in ZL3b.
- Four identifiers appear only in ZL3a: `f1r.29`, `f1r.30`, `f1r.31`, and `f89v2.26`.
- All 5,385 aligned records have the same normalized locus type and the same Currier label under this parser. There is one raw locator-code difference (`@Lf` vs `+Lf`) whose normalized locus remains `Lf`.
- The paragraph-start/end marker flags match on every aligned line.

## Payload and cleaned-token agreement

| Measure across 5,385 aligned records | Count | Share |
|---|---:|---:|
| Trimmed raw body-payload string exactly equal | 5,327 | 98.92% |
| Trimmed body-payload string differs | 58 | 1.08% |
| Cleaned token sequence exactly equal | 5,336 | 99.09% |
| Cleaned token sequence differs | 49 | 0.91% |

The 49 cleaned-token-sequence differences break down by Currier metadata: 13 A, 22 B, and 14 records where the header does not supply Currier A/B. By normalized locus, 22 differences fall in P0, 18 in Cc, four in L0, two in Pb, and one each in Lc, Ri, and Ro.

Sequence alignment across the 49 differing rows counted a minimum of 127 substitution edits, two insertions, and 20 deletions. These are token-level alignment edit counts, not claims that every edit is an independent manuscript error.

## Interpretation

**ZL3a and ZL3b are extremely close alternative transcriptions, not independent evidence samples.** Only about 0.91% of aligned rows differ after this conservative token cleanup, and their explicit paragraph-marker flags agree on all aligned keys. That explains why many earlier test statistics matched almost exactly across versions.

The files are not perfectly interchangeable: 49 rows have different cleaned token sequences and four additional identifiers occur only in ZL3a. Those differences could affect particular token counts, so the next audit should measure their effect on the primary `daiin` first-position statistic directly rather than assuming that high overall agreement guarantees every statistic is unaffected.

## Limitations

- The token cleanup is an operational comparison rule; it is not an authoritative interpretation of every IVTFF apparatus convention.
- Same normalized locus and Currier label means those fields match under this parser, not that all transcription choices are identical.
- The files represent alternative transcriptions of the same manuscript. Agreement is version robustness, not independent replication.
- This is a concordance/provenance result, not a linguistic or semantic inference.
