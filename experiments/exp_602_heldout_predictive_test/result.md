# exp_602 — Held-out prediction result

Workflow: https://github.com/kyrian20/voynich-autoexploration/actions/runs/39260149768

Training: 1,797 lines / 60 folios. Held-out: 528 lines / 21 folios. No folio crosses the deterministic split.

For primary target `daiin`, train-only initial probability was 0.03450. Held-out log loss was 0.19917 for the global model and 0.11786 for the per-line token-inventory baseline. Gain (baseline minus model) = -0.08131; folio-cluster 95% interval [-0.11174, -0.05641]. Brier score also favored the baseline. Predeclared controls `dain` and `saiin` showed the same direction.

**Conclusion:** the preregistered positive predictive criterion failed. This does not disprove the positional enrichment; the baseline conditions on each held-out line's token inventory and is a stringent null, not a deployable predictor. Keep the split frozen and do not tune on held-out folios. This is a distributional result, not decipherment.