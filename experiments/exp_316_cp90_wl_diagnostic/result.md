# exp_316: CP90 Ratios and Word-Length Component Diagnostic with 21-Mechanism Architecture (H519)

**Date:** 2026-04-11
**Hypothesis:** H519 — Diagnostic: (A) CP90 ratios for all 7 major onset classes with 21-mechanism architecture; (B) word-length component breakdown per onset class (H494).
**Result:** H519/H494 ANSWERED. Vocabulary clamping for qok/ok/ot/qot achieves near-exact VMS CP90 ratios (0.94-1.00×). sh/ch/d remain massively over-produced in type diversity (21-39×). Suffix length is the primary word-length component gap (sim 1.781 vs VMS 2.215, −20%), driven by the beta bias mechanism.

---

## Setup

21-mechanism B-dialect architecture (exp_314 baseline). N=30 trials, SEED=316000+99999.
Two measurements:
(A) CP90 = types needed to cover 90% of tokens, per onset class, VMS vs simulation aggregate.
(B) Word-length components: mean onset_len, midfix_len, suffix_len, total_len per onset class and overall.

---

## Results

### A. CP90 Ratios

| Onset | VMS_CP90 | Sim_CP90 | Ratio   | VMS_Types | Sim_Types |
|-------|----------|----------|---------|-----------|-----------|
| qok   | 31       | 31       | 1.00×   | 150       | 175       |
| ok    | 54       | 53       | 0.98×   | 151       | 161       |
| ot    | 57       | 54       | 0.95×   | 156       | 166       |
| qot   | 36       | 34       | 0.94×   | 88        | 92        |
| sh    | 129      | 3363     | 26.07×  | 275       | 8286      |
| ch    | 223      | 4723     | 21.18×  | 467       | 13651     |
| d     | 83       | 3261     | 39.29×  | 150       | 6213      |

**Note on methodology:** N=30 trial aggregate vs single-realization VMS. sh/ch/d are unclamped; each trial generates diverse sh/ch/d words through Timm mutation, accumulating far more unique types in the 30-trial aggregate than VMS's single realization. The effective per-trial comparison would show smaller ratios (earlier exp_302 found sh≈3×, ch≈2.6×, d≈2.2× — likely measured with fewer trials).

### B. Word-Length Components — Overall MID

| Component  | VMS   | Sim   | Ratio |
|------------|-------|-------|-------|
| onset_len  | 2.064 | 1.874 | 0.908× |
| midfix_len | 1.244 | 1.354 | 1.089× |
| suffix_len | 2.215 | 1.781 | 0.804× |
| total_len  | 5.409 | 5.101 | 0.943× |

Suffix length is the primary gap (−20%). The beta bias (beta_scale=1.8) penalizes longer suffixes → shorter mean suffix. This is the expected and designed effect. Onset_len gap (−9%) is driven by onset distribution differences (sim over-produces ch/sh/d relative to qok/qot). Midfix_len is slightly too long (+9%).

### C. Word-Length Components — Clamped Onsets (qok/ok/ot/qot)

All four clamped onset classes show near-exact VMS component matches:

| Onset | onset_len ratio | midfix_len ratio | suffix_len ratio | total_len ratio |
|-------|----------------|-----------------|-----------------|----------------|
| qok   | 1.000×         | 1.002×          | 0.993×          | 0.997×         |
| ok    | 1.000×         | 0.989×          | 1.003×          | 0.999×         |
| ot    | 1.000×         | 0.991×          | 0.999×          | 0.998×         |
| qot   | 1.000×         | 0.972×          | 1.004×          | 0.997×         |

Vocabulary clamping does not distort component lengths — it constrains word types to the VMS lexicon while preserving structural composition.

### D. Word-Length Components — Unclamped Onsets (sh/ch/d)

| Onset | onset_len ratio | midfix_len ratio | suffix_len ratio | total_len ratio |
|-------|----------------|-----------------|-----------------|----------------|
| sh    | 1.000×         | 1.072×          | 0.711×          | 0.933×         |
| ch    | 1.000×         | 0.983×          | 0.678×          | 0.898×         |
| d     | 1.000×         | 1.531×          | 0.720×          | 1.002×         |

sh and ch: suffix_len is 29-32% too short (beta bias selects shorter suffixes via Timm modification chain). d: midfix_len is 53% too long (d words undergo extensive Timm modification inserting characters into the d-midfix region); suffix is 28% too short.

---

## Interpretation

**Vocabulary clamping (17th mechanism) works exactly as designed.** qok/ok/ot/qot have CP90 ratios 0.94-1.00× — effectively VMS CP90. Word-length components also match VMS exactly (0.972-1.004× per component). The clamping resolves Q007 for these onset classes.

**sh/ch/d vocabulary explosion is confirmed structural.** The N=30 aggregate measurement shows 21-39× CP90 over-production. Even per-trial, the generation of unclamped sh/ch/d words through Timm mutation creates high type diversity. The vocabulary clamping approach (17th mechanism) cannot be trivially extended to sh/ch because full clamping broke adj_rate in exp_304. However, since sh (275 VMS types) and ch (467 VMS types) have LARGER VMS lexicons than qok (150), partial clamping may be safe — the adj_rate risk is proportionally lower with larger lexicons. H518 (sh/ch/d partial clamping) should start with full VMS-lexicon clamping for sh/ch separately (not combined), monitoring adj_rate impact.

**H494 ANSWERED: Suffix length is the primary word-length component gap.** sim suffix_len = 1.781 vs VMS = 2.215 (−0.434 chars, −20%). The beta bias causes this: beta_scale=1.8 actively shortens suffix selection in the cipher path, and Timm modification of these shorter-suffix words propagates to the copy/modify path. This is a trade-off: the beta mechanism is needed for Menzerath r (104% of VMS), but it produces a 20% suffix shortfall. The midfix is slightly too long (+9%), partially compensating for the suffix shortfall. Total word_len deficit is 5.7% (within battery tolerance).

**Onset distribution mismatch explains onset_len gap.** sim onset_len = 1.874 vs VMS = 2.064 (−9%). Simulation over-produces ch (2976 tokens/trial vs VMS 2447) and d (984 vs 674) while qok is close (2062 vs 1965). The excess ch/d production (shorter onset prefixes: ch=2, d=1) relative to VMS shifts the onset distribution toward shorter onsets.

---

## Limitations

- CP90 methodology: N=30 aggregate (sim) vs single realization (VMS) makes the ratio for unclamped onsets not directly comparable to exp_302's per-trial measurement. The structural finding (vocabulary explosion for sh/ch/d) holds; the magnitude (21-39×) should be interpreted as aggregate over-production. A per-trial measurement would show smaller ratios.
- H518 risk assessment is based on inference (larger VMS lexicons → lower adj_rate risk); actual impact must be tested experimentally.
- d-onset's midfix_len over-production (+53%) is a new finding not previously characterized. It may reflect the d-onset bias mechanic (d_boost) or a Timm modification interaction with the short d-onset.

---

## Self-Audit

**Target-awareness:** No parameters were calibrated using VMS targets in this experiment. It is a pure diagnostic: all architecture parameters are fixed at 21-mechanism values (exp_314). The VMS data is used only as the measurement reference, not for calibration. No target-aware elements.

**Feature-destroying implementation:** This is a diagnostic experiment, not testing a mechanism. No feature-destroying implementation applies.

**Extrapolation:** The claim that sh/ch/d have structural vocabulary over-production is based on the N=30 aggregate measurement. The per-trial estimate would be lower. The result.md explicitly notes this methodological caveat and does not claim "sh CP90 is permanently 26×" — it characterizes the aggregate behavior and notes the N dependency.

**Negative-result scope:** Not a negative result experiment — it is diagnostic. No hypothesis was falsified; H519 and H494 were factual questions with measurable answers.

**Control behavior:** VMS is the reference, not a control. No null model used. All comparisons are VMS corpus vs simulation output.
