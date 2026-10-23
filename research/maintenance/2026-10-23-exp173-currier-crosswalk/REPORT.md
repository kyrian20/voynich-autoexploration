# EXP-173 Currier crosswalk — 23 October 2026

Status: descriptive sensitivity audit, not a new EXP or global validation. Starting commit: 7dbb1842415a6c17305e0b4981752bfde0a95920.

Historical parser: P-only rows, dot-delimited tokens, edy/eedy >= 0.05 on combined numeric folio. Comparison: explicit page-header $L=A/B. No metadata imputation, no corpus substitution.

Corpus SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc. Historical script Git blob: 3fb1eeb92c301d3caf841499571f5e1a8b590bcc.

Results: 4118 historical rows, 4023 with $L; 1557 A-to-A, 2441 B-to-B, 25 A-to-B on f55r/f55v. Unknown metadata: 95 rows across ten pages.

Historical B: 2447 lines, 20490 tokens, 402 -am words, 327 line-final -am; enrichment F3=6.8112949758766455. y onset: 836 total, 350 first; F6=3.5056596985274417.

Metadata B: 2466 lines, 20652 tokens, 406 -am words, 331 line-final -am; F3=6.827646135222274. y onset: 851 total, 355 first; F6=3.493557028942621.

Intersection: legacy B F3=6.8167071239460215, F6=3.5152404437021394; metadata B F3=6.827646135222274, F6=3.493557028942621.

Interpretation: historical descriptive ratios recovered; replacing labels does not reverse these effects. No significance tests or folio-cluster uncertainty computed. Historical p-values and complete IVTFF coverage remain unvalidated. No decipherment.

Artifacts: scripts/audit_exp173_currier_crosswalk.py, tests/test_exp173_currier_crosswalk.py, results.json in this directory. Six pure fixture tests passed locally. Full Python snapshot check awaits a complete checkout. Snapshot Git blob: 13993410970f4a5d1af08663d24795e2f32adc20.

Commands: python tests/test_exp173_currier_crosswalk.py ; python scripts/audit_exp173_currier_crosswalk.py --check research/maintenance/2026-10-23-exp173-currier-crosswalk/results.json

Self-audit: target-awareness: retrospective F3/F6 selection, no tuning. Feature destruction: legacy parser retained and limited. Extrapolation: only these descriptive metrics. Negative scope: no general theory rejected. Control: legacy reconstruction expected and observed F3=6.8112949758766455 and F6=3.5056596985274417; synthetic fixtures distinguish $L from $Q.

Next: preregister IVTFF-complete paired folio comparison, within-folio control, clustered uncertainty and explicit claim thresholds before inferential tests. Preserve committed claims for human adjudication.
