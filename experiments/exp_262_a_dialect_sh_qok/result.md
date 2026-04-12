# exp_262: A-Dialect sh→qok Markov Sweep

**Date**: 2026-04-11
**Hypothesis**: H461 — A-dialect's smaller sh→qok gap (Δ=-0.769, exp_255) may allow a viable p_sh_qok mechanism in the 12-mechanism architecture, unlike B-dialect where the same mechanism failed (ss_d regression at p=0.05, N=30).
**Architecture**: A-dialect 12-mechanism (exp_258: exp_239 + p_y_y=0.10 + p_o_o=0.10 + filter_other)

## Setup

A-dialect VMS sh→qok E_mid = 1.741 (N_bigrams=55, MID bigram total=4700)  
sh MID rate: 0.1132, qok MID rate: 0.0594  
Baseline sim (p_sh_qok=0.00): sh→qok = 0.896, Δ = -0.845

Note: Baseline gap (-0.845 at N=5) is slightly larger than exp_255's reported Δ=-0.769, because exp_255 used the 11-mechanism architecture without p_o_o=0.10. The 12-mechanism baseline produces a modestly larger gap due to the additional buffer state introduced by p_o_o.

## Sweep Results (N=5)

| p_sh_qok | Pass/19 | sh→qok | VMS   | Delta  | ss_d% |
|----------|---------|--------|-------|--------|-------|
| 0.00     | 19/19   | 0.896  | 1.741 | -0.845 | 89.1% |
| 0.05     | 18/19   | 1.111  | 1.741 | -0.630 | 91.0% |
| 0.10     | 19/19   | 1.310  | 1.741 | -0.431 | 90.6% |
| 0.15     | 17/19   | 1.354  | 1.741 | -0.387 | 92.2% |
| 0.20     | 18/19   | 1.611  | 1.741 | -0.130 | 87.2% |

Best: p=0.10 (19/19 at N=5). Slope estimate (p=0.00 to p=0.20): Δsh_qok = 0.715 per 0.20 unit p = 3.575 per unit p.

## Full Battery: p_sh_qok=0.10 (N=30)

| Metric         | VMS    | Sim    | %VMS   | PASS |
|----------------|--------|--------|--------|------|
| am_ll          | 3.4993 | 3.5457 | 101.3% | PASS |
| d_ll           | 1.6549 | 1.7083 | 103.2% | PASS |
| y_lf           | 2.1840 | 1.9704 |  90.2% | PASS |
| ss_mean        | 1.5793 | 1.3275 |  84.1% | PASS |
| adj_rate       | 0.0093 | 0.0105 | 112.7% | PASS |
| qok_lf         | 1.0795 | 0.9865 |  91.4% | PASS |
| d_lf           | 1.1060 | 1.0583 |  95.7% | PASS |
| s_lf           | 2.1542 | 2.0702 |  96.1% | PASS |
| ch_ll          | 0.8549 | 0.8616 | 100.8% | PASS |
| ok_ll          | 1.0021 | 1.0516 | 104.9% | PASS |
| qok_ll         | 0.5127 | 0.4999 |  97.5% | PASS |
| ss_d           | 1.2739 | 1.1550 |  90.7% | PASS |
| ss_y           | 1.5874 | 1.6358 | 103.0% | PASS |
| am_lf_enr      | 0.2656 | 0.2857 | 107.6% | PASS |
| am_mid_enr     | 0.5324 | 0.5083 |  95.5% | PASS |
| edy_rate       | 0.0045 | 0.0044 |  99.1% | PASS |
| word_len_mean  | 5.2604 | 4.9511 |  94.1% | PASS |
| qok_ch         | 1.2200 | 1.2125 |  99.4% | PASS |
| global_am_rate | 0.0198 | 0.0197 |  99.4% | PASS |

**TOTAL: 19/19 PASS**

## Non-Battery Structural Check

| Metric    | VMS   | Sim (p=0.10) | Delta  |
|-----------|-------|--------------|--------|
| sh→qok    | 1.741 | 1.345        | -0.396 |
| sh MID rate | 0.1132 | 0.1213   | +0.081 |

Gap closure: baseline Δ=-0.845 → p=0.10 Δ=-0.396 → 53% of original gap closed.

## Interpretation

### Finding 1: p_sh_qok=0.10 Partially Closes A-Dialect sh→qok Gap Without Battery Regression
At p_sh_qok=0.10, the A-dialect 12-mechanism architecture passes 19/19 at N=30 while reducing the sh→qok MID E2 gap from -0.845 to -0.396 (53% closure). The mechanism is analogous to B-dialect's p_qokch=0.12: when the buffer's previous onset is 'sh', the draw_buf function seeks a qok-onset word from the buffer with probability 0.10.

### Finding 2: Full Closure Unreachable Without Battery Regression
The slope is approximately 3.575 units of E2 per unit of p. From p=0.10 (sh→qok=1.310), reaching VMS target 1.741 requires an additional Δ=0.431, implying p≈0.22. However, p=0.15 fails at N=5 (17/19) and p=0.20 fails at N=5 (18/19). Full closure at A-dialect is architecturally limited — the same slope that would close the gap also produces battery regression.

### Finding 3: A-Dialect Permits p=0.10 Where B-Dialect Did Not
In B-dialect, p_sh_qok=0.05 caused ss_d regression at N=30 (18/19) — the mechanism was unusable. In A-dialect, p_sh_qok=0.10 holds 19/19 at N=30. The difference reflects A-dialect's lower ss_d target (VMS A-dialect ss_d=1.274 vs B-dialect ss_d=1.585): A-dialect has more headroom before ss_d is disrupted by the sh→qok Markov selection. This is consistent with A-dialect's generally lower self-succession structure compared to B-dialect.

### Architecture Decision
Adding p_sh_qok=0.10 to A-dialect architecture is warranted: 19/19 PASS (N=30), genuine sh→qok gap closure (53%), mechanism is analogous to other successful onset-succession rules in this system. A-dialect advances to 13 mechanisms.

## Limitations

- N=5 sweep: p=0.05 showed 18/19 (failed by 1); full N=30 run at p=0.05 was not performed. It is possible p=0.05 is also viable at N=30 and would provide better structural balance.
- Baseline gap at p=0.00 measured as -0.845 (N=5), slightly larger than exp_255's -0.769 (different architecture). True baseline at N=30 not separately measured.
- sh→qok count in VMS A-dialect is N=55 (low). MID E2 = 1.741 may have ±0.2 sampling noise.
- A-dialect sh→qok gap is genuine (confirmed cross-experiment: exp_254, exp_255, exp_262), but its magnitude is uncertain at N=55.

## Self-Audit

**Target-awareness**: p_sh_qok=0.10 was selected because it maximized passes at N=5 while improving sh→qok E2. The sh→qok E2 target (1.741) was known before sweep; the parameter was chosen to move toward this target. This is target-aware calibration for a non-battery metric. The 19/19 battery PASS is NOT conditional on this calibration (the 19 battery metrics do not include sh→qok). The structural improvement claim (53% gap closure) IS conditional on calibrating p toward the VMS sh→qok target.

**Feature-destroying implementation**: No feature-destroying implementation details identified. The draw_buf modification (seek qok-onset when prev_onset='sh') directly implements the sh→qok onset-succession bias the hypothesis predicts.

**Extrapolation**: Finding 2 claims "full closure unreachable without battery regression." The tested range is p ∈ {0.00, 0.05, 0.10, 0.15, 0.20} at N=5. p=0.15 failed at N=5 (17/19); p=0.20 failed at N=5 (18/19). Untested: p ∈ (0.10, 0.15). It is possible that p≈0.12–0.13 provides full closure at N=30. Revised claim: "full closure not achieved at p=0.10 (best 19/19 value at N=5); higher p values (0.15, 0.20) fail N=5 battery." Reserve "unreachable" for future tests if finer grid is negative.

**Negative-result scope**: N/A — positive result (19/19 PASS with structural improvement).

**Control behavior**: The control is the baseline (p=0.00, 19/19 PASS, sh→qok=0.896). Expected: baseline passes 19/19 (confirmed), sh→qok under-produced (0.896 vs VMS 1.741 — expected from exp_255's -0.769 gap). Actual baseline: 0.896, gap -0.845 — slightly larger than expected from exp_255, consistent with the architectural difference (p_o_o=0.10 added in exp_258 modifies buffer state, slightly reducing sh→qok through competition for the buffer qok slot). No surprises.

## Conclusion

H461 PARTIALLY CONFIRMED. p_sh_qok=0.10 achieves 19/19 PASS (N=30) while reducing A-dialect sh→qok MID E2 gap by 53% (Δ: -0.845 → -0.396). Full closure (VMS=1.741) is not achieved at p=0.10 (sim=1.345); higher p values regress the battery. A-dialect architecture advances to 13 mechanisms: add p_sh_qok=0.10. This contrasts with B-dialect where the same mechanism failed at p=0.05 (exp_243) — A-dialect has more headroom because its ss_d target is lower (1.274 vs B's 1.585), allowing sh-onset Markov selection without disrupting d-onset self-succession.
