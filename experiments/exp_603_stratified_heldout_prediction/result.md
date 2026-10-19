# exp_603 — Stratified held-out prediction

Frozen split: same deterministic folio-hash rule as exp_602. Population: ZL3b, Currier A/B, P0, at least two clean tokens. Features at prediction time: Currier class and line-length bin only. Fixed bins: 2–4, 5–7, 8+ tokens. Each training stratum uses Beta(1,1) smoothing. No held-out target counts are used to estimate probabilities.

Train: 2928 lines / 148 folios. Test: 919 lines / 47 folios.

Positive log-loss gain means stratified model beats global train-only model. Positive Brier gain also favors stratified model.

## daiin

- Held-out initial hits: 37
- Global log loss: 0.168849; stratified: 0.171576
- Log-loss gain: -0.002727; folio-bootstrap 95% CI [-0.005202, -0.000135]
- Brier gain: -0.000203

## dain

- Held-out initial hits: 11
- Global log loss: 0.064885; stratified: 0.064712
- Log-loss gain: 0.000173; folio-bootstrap 95% CI [-0.001160, 0.001890]
- Brier gain: -0.000010

## saiin

- Held-out initial hits: 8
- Global log loss: 0.052005; stratified: 0.051091
- Log-loss gain: 0.000914; folio-bootstrap 95% CI [-0.001515, 0.003611]
- Brier gain: -0.000015

## Interpretation

This tests out-of-sample prediction, not decipherment. Controls are descriptive and should not be treated as independent confirmatory tests. The split and bins were fixed before evaluation. Missing train strata back off to the global rate.
