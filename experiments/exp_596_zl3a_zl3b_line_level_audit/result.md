# exp_596 — Results: paired line-level ZL3a/ZL3b audit

**Run:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258473051  
**Outcome:** script compiled and audit ran; result saved in `results.json`.

## Alignment and annotation
- ZL3a and ZL3b each contain **4,130** generic P-locus records for this parser.
- All **4,130/4,130** records matched one-to-one by folio header plus complete IVTFF locus identifier; no unmatched or duplicate keys.
- No Currier A/B label disagreements.
- No explicit paragraph-start/end marker disagreements.
- No disagreements in whether the first cleaned token is `daiin`.
- There are **24 cleaned token-sequence disagreements**, so the files are close but not byte-identical.

The source SHA-256 values are recorded in `results.json`: ZL3a `56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2`; ZL3b `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.

## Positional strata
| Dialect / marker | Lines | Initial `daiin` | Expected | Enrichment |
|---|---:|---:|---:|---:|
| A / explicit `<%>` | 236 | 1 | 6.993 | 0.143× |
| A / no start marker | 1,321 | 61 | 64.244 (ZL3b: 64.243) | 0.949× |
| B / explicit `<%>` | 492 | 0 | 2.827 | 0× |
| B / no start marker | 2,056 | 97 | 32.383 (ZL3b: 32.279) | 2.995× (ZL3b: 3.005×) |

## Conclusion
The exp_594/595 pattern is **not an artefact of line-key misalignment or changed paragraph markers** between these two files. The initial-`daiin` classification is identical on every paired line; the small enrichment differences in B/no-start-marker reflect a tiny difference in the underlying token sequences. This is version-level robustness only, not independent replication from a separate transcription project.

This experiment says nothing about the meaning of `daiin`. It validates the comparison mechanics and documents the remaining 24 line-level token differences.
