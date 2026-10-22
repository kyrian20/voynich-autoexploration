# Library artifact SHA-256 manifest — 2026-10-22

## Scope and method
This manifest records SHA-256 hashes calculated from raw bytes materialized from the Library folder `/Investigación Voynich/` on 2026-10-22. It is a scoped provenance checkpoint, not a complete Library/GitHub reconciliation. Files were not modified. A matching filename, size, or report title is not evidence that a GitHub counterpart is byte-identical; no equivalence is asserted below unless explicitly checked.

## EXP-623: two distinct Library order analyses
These reports use different null models and must remain separate from GitHub `experiments/exp_623_it2a_ch_sh_specificity_replication/`, which is a ch/sh-context test.

| Library file | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md` | 8916 | `d64bd77fc1e7fab4fe5b3d691f36b442ef878833723ca1aeeb6f0caed37f055d` | Whole-locus word-order permutation report |
| `Informe_Voynich_exp623_control_orden_2026-10-19.md` | 8752 | `7d8d794f36a2da83d4e6886d9986d9f42478ad999cde6ce1aeec3ad4c133af16` | Interior-word shuffle/holdout report |
| `exp623_order_null.py` | 11137 | `ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010` | Endpoint-preserving null implementation |
| `exp623_order_null_summary.json` | 2960 | `841425ae5668b9094d61b63d7290b57f4cc821e1b8acecbc7715a8ead555e692` | Summary output for endpoint-preserving null |
| `exp623_resultados_2026-10-19.json` | 2633 | `f46390e0f3a467f6327c1120c8a8a3eeddf707dc387bb5e6be8d4461780d618b` | Separate recorded results JSON; script association needs content review |
| `exp623_shuffle_holdout.py` | 8563 | `c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070` | Folio holdout with within-locus token permutations |

**Guardrail:** do not combine the two report conclusions or attach either to GitHub EXP-623 without tracing its exact script, inputs, and JSON.

## EXP-590/593: selected Library reports and implementation
| Library file | Bytes | SHA-256 | Role |
|---|---:|---|---|
| `Voynich_Informe_exp590_Auditoria_Modelos_Externos_2026-10-18.md` | 15055 | `427341ce9b6301f26c9d5ce7663073a5ba0cde01c07d3cbce6f2e9f051df4653` | EXP-590 external-model audit report |
| `Voynich_Informe_exp593_Denominadores_Zodiacales_2026-10-18.md` | 7809 | `3a36140a0f1753bdc999260b25f51489093a4860ce5ae7386d8d4b55e76730ef` | EXP-593 zodiac denominator report |
| `Voynich_exp593_resultados.json` | 2346 | `75f92da4edc29c626e24dda581d69d2878f1edc4c07900d8a2d269fccc15d088` | EXP-593 results |
| `voynich_exp593_zodiac_reconciliation.py` | 8784 | `35290a05843f79604524e167b0971be82ce151c144d1907fc9cf2743ccb691f7` | EXP-593 reconciliation script |

## Next verification steps
1. Fetch the GitHub counterpart bytes/content for each candidate pair and compare normalized content or exact SHA-256; do not infer pairing from EXP numbers alone.
2. Trace every EXP-623 Library JSON to its generating script and input corpus hashes.
3. Continue the IVTFF independent-parser/edge-case audit and preserve all historical files.
4. Do not allocate a new experiment ID or promote any result to validated until these provenance checks are complete.


## EXP-623 report/JSON/script association review — 2026-10-22

A content-level read of the JSON metadata, reports, and script docstrings resolves the *intended method pairing*, but not exact execution provenance:

- `LIB-ORDER-2026-10-19-A` (all-token permutation, report `Informe_Voynich_exp623_Control_orden_palabras_2026-10-19.md`) aligns with `exp623_resultados_2026-10-19.json` and the method described by `exp623_shuffle_holdout.py`: the JSON says 20 splits × 50 shuffles and the null permutes all tokens inside each held-out locus. The report says the pilot was exploratory and the Python script was not run in GitHub Actions.
- `LIB-ORDER-2026-10-19-B` (interior-only shuffle preserving first and last, report `Informe_Voynich_exp623_control_orden_2026-10-19.md`) aligns with `exp623_order_null_summary.json` and the method described by `exp623_order_null.py`: the JSON says 10 folio splits × 39 nulls and preserves endpoints. Its JSON explicitly says the Python implementation was not yet run in GitHub Actions; results came from a JavaScript pilot.
- This pairing is supported by protocol/method fields and script descriptions, **not** by a verified rerun of those exact Python files. Keep execution status as exploratory/unreproduced until the source scripts are executed against the recorded corpus versions and the outputs are compared.
- Both JSON files record upstream transcription blob IDs `2a4533ab9bdfa85db9bad602d590978953055df1` (ZL3b) and `4d6d3f2537b1f507a257529b49c94af7d6e03446` (IT2a). These are Git blob identifiers, not SHA-256 hashes of the Library report/script files.
