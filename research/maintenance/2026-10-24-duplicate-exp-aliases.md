# Verified duplicate legacy experiment IDs (2026-10-24)

Source: parsed `research/EXPERIMENT_PATH_REGISTRY.json` on master; 624 entries, 617 unique numeric aliases, seven aliases with two paths each. This verifies registry internal counts only, not completeness against the current filesystem or scientific validity.

| Legacy alias | Canonical path A | Canonical path B |
| --- | --- | --- |
| EXP-177 | `experiments/exp_177_position_sensitive_cipher` | `experiments/exp_177_verify` |
| EXP-594 | `experiments/exp_594_daiin_explicit_paragraph_markers` | `experiments/exp_594_daiin_paragraph_start` |
| EXP-596 | `experiments/exp_596_daiin_position_controls` | `experiments/exp_596_zl3a_zl3b_line_level_audit` |
| EXP-597 | `experiments/exp_597_daiin_frequency_control_words` | `experiments/exp_597_initial_form_next_token_context` |
| EXP-600 | `experiments/exp_600_ivtff_parser_conformance` | `experiments/exp_600_transcription_concordance` |
| EXP-601 | `experiments/exp_601_folio_clustered_confirmation` | `experiments/exp_601_primary_statistic_paired_sensitivity` |
| EXP-602 | `experiments/exp_602_heldout_predictive_test` | `experiments/exp_602_independent_ivtff_parser_audit` |

Correction policy: never infer experiment identity from these bare numeric aliases. Cite full canonical paths and exact source hashes. Do not rename/delete original directories, change frozen reports, or silently attribute one result to the other. New experiments must use nonconflicting canonical paths and a registry audit.
