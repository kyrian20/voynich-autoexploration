# exp_310: Line-Length-Conditional LL Suffix Bias (H512)

**Date:** 2026-04-11
**Hypothesis:** H512 — Can conditioning LL suffix selection on line length close the remaining r_ll gap, targeting the non-am LL_wl decrease of −1.244 chars observed in VMS?

## Result: H512 REFUTED as formulated — VMS non-am LL_wl gradient is NOT driven by suffix length selection. DIAGNOSTIC FINDING: "other" suffix category increases 22.5% → 42.6% in long lines; recognized suffix lengths stay flat (2.97→3.12). Beta_ll suffix bias is mechanistically wrong and achieves only partial improvement (r_ll: 15.7% → 36.1%). 19th mechanism NOT adopted. H513 generated for correct mechanism (word-length-conditional LL selection).

## Critical Diagnostic: VMS Non-am LL Suffix Distribution by Line Length

| Bucket | N | nonam_wl | mean_suf_len | short_suf% | long_suf% | "other"% |
|--------|---|----------|-------------|-----------|----------|---------|
| n=2-4 | 266 | 5.671 | 2.972 | 42.6% | 57.4% | 22.5% |
| n=5-6 | 452 | 5.404 | 2.962 | 41.9% | 58.1% | 26.3% |
| n=7-8 | 647 | 5.226 | 3.057 | 39.1% | 60.9% | 33.6% |
| n=9-10 | 695 | 4.659 | 3.037 | 40.5% | 59.5% | 36.4% |
| n=11-15 | 329 | 4.426 | 3.124 | 38.8% | 61.2% | 42.6% |

**Key finding:** Mean recognized-suffix length stays flat (2.97→3.12) and the short/long suffix ratio barely changes. The VMS non-am LL_wl gradient (−1.245 chars) is NOT driven by shorter recognized suffixes in long lines. Instead:
- The "other" category (words with no recognized suffix) increases from 22.5% to 42.6% (+20pp)
- Top recognized suffixes in long lines: dy (10.5%), al (8.5%), ar (7.4%), aiin (6.2%) — similar to short lines
- "other" words are systematically shorter than recognized-suffix words, pulling down the mean

**Mechanism interpretation:** In long VMS lines, LL words are more often short words that fall outside the recognized suffix patterns. These could be words ending in bare 'y', bare 'n', or other short idiosyncratic endings not in {eedy,edy,aiin,ain,am,ey,ol,or,al,ar,dy}. The mechanism is word-length selection (shorter words preferred at LL in longer lines), not suffix type selection.

## Sweep: Beta_ll Suffix Bias (N=10 per condition, metric-level evaluation)

| Condition | beta_ll_base | menz_r | r_ll | %r_ll | nonam_delta | Notes |
|-----------|-------------|--------|------|-------|-------------|-------|
| baseline | 0.00 | −0.136 | −0.037 | 17.1% | +0.030 | 18-mechanism baseline |
| mild | 0.20 | −0.133 | −0.086 | 39.4% | −0.225 | |
| moderate | 0.40 | −0.127 | −0.100 | 45.7% | −0.370 | |
| strong | 0.60 | −0.124 | −0.133 | 60.6% | −0.505 | |
| vstrong | 0.80 | −0.113 | −0.143 | 65.1% | −0.511 | |
| extreme | 1.20 | −0.102 | −0.148 | 67.3% | −0.551 | |

**Note on pass counts:** Sweep uses per-trial counting (~10-13% of individual trials simultaneously pass all 19 metrics due to variance). The project-standard metric-level battery check (N=30 aggregate) shows all 19 metrics pass for all conditions tested at N=30. See battery section below.

**Observation:** Stronger beta_ll improves r_ll but at the cost of Menzerath r (−0.136→−0.102 at extreme). The beta_ll mechanism simultaneously reduces LL word length everywhere (including in short lines, just less so), which compresses the mean word length overall and reduces the Menzerath gradient. This is a fundamental tension.

## N=30 Battery: mild (beta_ll_base=0.20)

| Metric | VMS | Sim | %VMS | Status |
|--------|-----|-----|------|--------|
| am_ll | 6.5498 | 6.9656 | 106.3% | PASS |
| d_ll | 1.3625 | 1.1498 | 84.4% | PASS |
| y_lf | 3.1837 | 2.9077 | 91.3% | PASS |
| ss_mean | 1.1640 | 1.3082 | 112.4% | PASS |
| adj_rate | 0.0090 | 0.0102 | 113.5% | PASS |
| qok_lf | 0.7450 | 0.8174 | 109.7% | PASS |
| d_lf | 2.1178 | 1.9234 | 90.8% | PASS |
| s_lf | 4.4422 | 4.3451 | 97.8% | PASS |
| ch_ll | 0.9653 | 0.9745 | 101.0% | PASS |
| ok_ll | 1.0028 | 1.0713 | 106.8% | PASS |
| qok_ll | 0.6121 | 0.6801 | 111.1% | PASS |
| ss_d | 1.5850 | 1.4162 | 89.4% | PASS |
| ss_y | 1.9550 | 1.6642 | 85.1% | PASS |
| am_lf_enr | 0.1225 | 0.1250 | 102.1% | PASS |
| am_mid_enr | 0.1954 | 2.077 | 106.3% | PASS |
| edy_rate | 0.1940 | 0.1883 | 97.1% | PASS |
| word_len_mean | 5.4000 | 5.2754 | 97.7% | PASS |
| qok_ch | 1.2670 | 1.2314 | 97.2% | PASS |
| global_am_rate | 0.0203 | 0.0197 | 97.2% | PASS |

**TOTAL: 19/19** (metric-level, N=30 aggregate)
Menzerath r: −0.131 (58.1% of VMS −0.225)
r_ll: −0.079 (36.1% of VMS −0.219)
MID slope: −0.052 (88.8% of VMS −0.058)
nonam_LL_delta (long−short): −0.213 chars (VMS: −1.244, 17% of target)

## N=30 Battery: baseline (beta_ll_base=0.00)

| Summary metric | Value |
|---------------|-------|
| All 19 metrics | PASS |
| Menzerath r | −0.144 (63.8% of VMS) |
| r_ll | −0.034 (15.7% of VMS) |
| MID slope | −0.052 (89.4% of VMS) |
| nonam_delta | +0.006 chars (essentially 0) |

## Non-am LL_wl by Bucket: Simulation vs VMS (mild condition, N=30)

| Bucket | VMS_nonam_wl | Sim_nonam_wl |
|--------|-------------|-------------|
| n=2-4 | 5.671 | 4.990 |
| n=5-6 | 5.404 | 4.948 |
| n=7-8 | 5.226 | 4.895 |
| n=9-10 | 4.659 | 4.808 |
| n=11-15 | 4.426 | 4.738 |

**Observation:** The beta_ll mechanism creates a very small gradient in sim nonam_wl (4.990→4.738, Δ=−0.252) vs VMS (5.671→4.426, Δ=−1.245). The mechanism is working in the right direction but is ~5× too weak. Crucially, the sim nonam_wl is lower than VMS for short lines (4.990 vs 5.671) because beta_ll also biases short-line LL words toward shorter suffixes. This means the mechanism depresses LL word length across the board rather than creating a large gradient.

## Key Findings

### F1: VMS non-am LL_wl gradient is driven by "other"-category words, not suffix length selection

The recognized-suffix mean length stays flat (2.97→3.12) across line lengths. The VMS gradient (−1.244 chars) is explained by "other"-suffix (unrecognized ending) words increasing from 22.5% to 42.6% as line length increases. These "other" words are systematically shorter than recognized-suffix words. The suffix-length bias mechanism (beta_ll) targets the wrong phenomenon and cannot reproduce the gradient at full scale.

### F2: Beta_ll suffix bias is battery-stable but mechanistically incorrect

beta_ll_base=0.20 passes 19/19 battery (metric-level) and improves r_ll from 15.7% to 36.1% of VMS. However, it achieves this by incorrectly biasing recognized suffixes shorter (not by generating "other"-category words). The improvement is real but the mechanism is wrong — it depresses LL word length across all lines rather than creating a strong gradient. This explains why nonam_delta achieves only 17% of VMS target.

### F3: Correct mechanism target (H513): line-length-conditional word-length filter for LL words

The VMS LL word distribution shows that short lines use longer LL words (nonam_wl=5.671) while long lines use shorter LL words (nonam_wl=4.426) that more often fall in the "other" category. A word-length cap that decreases with line length — rejecting LL words above a threshold and redrawing from a shorter word distribution — would directly target this. Implementation: max_ll_len(n) = {n≤5: 8, n≥10: 5, interpolated}. Reject and redraw LL non-blind words exceeding max_ll_len(n), drawing instead from a shorter-word cipher path. This directly targets the "other" category increase.

## Architecture Decision

**19th mechanism NOT adopted.** Beta_ll is mechanistically wrong (targets recognized suffix length, not "other"-category word frequency). The Menzerath r comparison is also unreliable (different seeds prevent clean baseline comparison). The diagnostic finding (F1) is the primary result of this experiment — it identifies the correct target for H513.

**Current architecture remains: 18-mechanism with cond_mild p_blind.**
**Parameters unchanged:** same as exp_309.

## Self-Audit

**Target-awareness:** VMS "other" suffix rate by line length bucket was used diagnostically (not for calibration). The beta_ll_base=0.20 condition was chosen by sweep result; no target metric was directly fit. The r_ll and Menzerath r reported are free predictions given the architecture parameters.

**Feature-destroying implementation:** The beta_ll mechanism biases ALL line lengths (including short lines) toward shorter suffixes, just with different strengths. This means for short lines, the mechanism slightly suppresses longer-suffix words (like eedy, aiin) that VMS actually uses more there. The mechanism works against the natural VMS pattern at short-line LL positions, explaining the compressed gradient. An alternative (word-length filter with no-bias in short lines) would be more faithful to the VMS pattern.

**Extrapolation:** "Beta_ll is mechanistically wrong" is based on the diagnostic showing recognized suffix lengths stay flat across line lengths (clear measurement). "Word-length filter will work better" (H513) is an extrapolation — the correct mechanism must generate shorter total words (including onset contribution), not just shorter suffixes.

**Negative-result scope:** H512 fails under the suffix-length-bias parameterization. A word-length filter or onset-conditional LL generation is untested. The diagnostic shows the VMS mechanism is word-length-conditional (including "other"-suffix words), not suffix-length-conditional. This does not rule out all suffix-based mechanisms — for example, a combined onset+suffix selection that systematically produces shorter total words (e.g., shorter onset classes preferred at LL in long lines) could work.

**Control behavior:** Baseline (beta_ll_base=0.00) gives menz_r=−0.144 and r_ll=−0.034 (N=30, different seed from exp_309). The exp_309 baseline gave menz_r=−0.137 (same architecture, different seed), confirming seed-dependent variance of ~0.007. The discrepancy between baseline conditions prevents reliable comparison of Menzerath r between baseline and mild.
