# Label segmentation: evidence and decision matrix (2026-10-24)

This note audits existing data; it is not a new EXP, translation, or independent transcription.

Source: `research/decipherment/2026-10-22-anchor-candidates.json`, `research/decipherment/2026-10-22-anchor-review/concordances.json`, and `research/decipherment/2026-10-24-f65r-user-image-inspection.md`.

| Locus | ZL3b primary | IT2a primary | Unresolved issue | Permissible inference |
| --- | --- | --- | --- | --- |
| f2r.14 | `ytoail` | no Lp record in packet | transcription coverage | only ZL3b attests this Lp entry in packet |
| f41v.1 | `keer[e:o]dal` -> `keeredal` | `keerodal` | e/o alternative | do not pick vowel to match a proposed name |
| f65r.1 | `otaim,dam.alam` | `otaim.dam.alam` | uncertain boundary between otaim/dam in ZL3b | retain split `otaim/dam/alam` and join `otaimdam/alam` |

The user-supplied f65r screenshot visually suggests grouped marks and a larger right-hand gap, but is not a calibrated or independently blinded paleographic reading. It does not resolve the ZL3b uncertain boundary.

Cross-context: ZL3b split and IT2a each place `otaim` in f65r.1 and f111v.3; ZL3b join leaves only f111v.3 as a standalone `otaim`. These are alternative editorial projections of the same underlying manuscript, not independent biological or linguistic replications.

Decision: zero validated semantic anchors, zero validated phonetic readings. The three Lp candidates are exploratory and selected from previously inspected data.

Next acceptance gate: (1) high-resolution independent transcription of f65r with confidence per glyph and gap; (2) explicitly compare competing segmentation policies; (3) expand sampling beyond the three selected Lp records with predeclared inclusion criteria; (4) only then specify predictive tests with folio-level holdout and negative controls. Keep all exceptions, including absent or disagreeing source records.
