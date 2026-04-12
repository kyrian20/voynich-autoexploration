# exp_258: A-Dialect o→o Markov Rule

**Date**: 2026-04-11
**Hypothesis**: H458 — Adding a p_o_o Markov rule (analogous to p_y_y) to the A-dialect architecture closes the o→o MID-position E2 gap (Δ=-0.815 at baseline).
**Architecture base**: exp_239 + p_y_y=0.10 + filter_other (11 mechanisms, 19-metric battery)

## Setup

The A-dialect architecture from exp_255 (filter_other applied) has a genuine o→o MID bigram gap:
- Baseline (p_o_o=0.00): Sim=1.986, VMS=2.801, Δ=-0.815

A p_o_o rule was added to draw_buf: when prev_onset='o', with probability p_o_o, attempt to draw an o-onset word from the copy buffer (identical structure to p_y_y rule).

Swept p_o_o ∈ {0.00, 0.05, 0.10, 0.15, 0.20} at N=5 trials each.
Best-value N=30 run at p_o_o=0.10.

Note: a prior run of this script had a bug in VMS_REF['am_mid_enr'] (hardcoded 0.195, the B-dialect value). This caused a spurious am_mid_enr = 264.3% FAIL at baseline. Fixed to corpus-computed value before the final run reported here.

## Sweep Results

| p_o_o | Pass/19 | o→o_mid Sim | VMS   | Δ      |
|-------|---------|-------------|-------|--------|
| 0.00  | 19/19   | 1.986       | 2.801 | -0.815 |
| 0.05  | 19/19   | 2.484       | 2.801 | -0.318 |
| 0.10  | 19/19   | 2.829       | 2.801 | +0.028 |
| 0.15  | 19/19   | 3.189       | 2.801 | +0.387 |
| 0.20  | 18/19   | 3.303       | 2.801 | +0.501 |

p_o_o=0.10 is a clear winner: smallest |Δ|, 19/19, and well-separated from the next values.

## Full Battery: p_o_o=0.10, N=30

| Metric         | VMS    | Sim    | %VMS   | PASS |
|----------------|--------|--------|--------|------|
| am_ll          | 3.4993 | 3.5501 | 101.5% | PASS |
| d_ll           | 1.6549 | 1.6880 | 102.0% | PASS |
| y_lf           | 2.1840 | 2.0212 |  92.5% | PASS |
| ss_mean        | 1.5793 | 1.3364 |  84.6% | PASS |
| adj_rate       | 0.0093 | 0.0106 | 113.5% | PASS |
| qok_lf         | 1.0795 | 1.0324 |  95.6% | PASS |
| d_lf           | 1.1060 | 1.0518 |  95.1% | PASS |
| s_lf           | 2.1542 | 2.1478 |  99.7% | PASS |
| ch_ll          | 0.8549 | 0.8572 | 100.3% | PASS |
| ok_ll          | 1.0021 | 1.0020 | 100.0% | PASS |
| qok_ll         | 0.5127 | 0.5258 | 102.6% | PASS |
| ss_d           | 1.2739 | 1.1211 |  88.0% | PASS |
| ss_y           | 1.5874 | 1.6412 | 103.4% | PASS |
| am_lf_enr      | 0.2656 | 0.2552 |  96.1% | PASS |
| am_mid_enr     | 0.5324 | 0.5153 |  96.8% | PASS |
| edy_rate       | 0.0045 | 0.0043 |  95.5% | PASS |
| word_len_mean  | 5.2604 | 4.9540 |  94.2% | PASS |
| qok_ch         | 1.2200 | 1.1824 |  96.9% | PASS |
| global_am_rate | 0.0198 | 0.0190 |  95.8% | PASS |

**TOTAL: 19/19 PASS**

## Structural Check

- o→o MID E2: Sim=2.848, VMS=2.801, Δ=+0.047 — **MATCH**
- Sim o MID rate: 0.0492 (VMS: 0.0477) — onset rate well-matched
- Baseline for reference: Sim=1.986, VMS=2.801

## Interpretation

The p_o_o=0.10 Markov rule closes the o→o MID bigram gap without disturbing the 19-metric battery. The mechanism is calibrated against the VMS o→o E_mid target (see Self-Audit: target-aware element).

The o→o gap was genuine (confirmed by exp_255 post-bug-fix baseline) and is now resolved. The solution is structurally identical to the p_y_y rule already in the architecture, consistent with both being onset-class persistence mechanisms using the copy buffer.

Note: p_o_o was selected by finding the value that reproduced the VMS o→o E_mid. The reported Δ=+0.047 is conditional on this calibration. A blind selection of p_o_o would not guarantee this specific match.

## Updated A-Dialect Architecture

11 mechanisms + filter_other + p_o_o=0.10 = **12 active mechanisms**:

1. Copy buffer (selective onset draw)
2. Word-level suffix substitution
3. Latin-derived LL enrichment (am_ll)
4. d-onset LL boost
5. Blind copy (P_BLIND)
6. y-onset LF concentration
7. qok-onset LF concentration
8. Position-gated ch/ok/qok LL
9. ss-onset mean/dispersion / adj-rate
10. ss→d successor enrichment
11. p_y_y=0.10 (y→y Markov rule)
12. p_o_o=0.10 (o→o Markov rule) — **NEW**

## Limitations

- p_o_o was calibrated against o→o E_mid. The mechanism adds one free parameter per architecture.
- o→o gap and y→y gap have now both been patched with Markov rules. This suggests a more parsimonious mechanism (a general onset-persistence rule with a single shared probability) could unify both. Not tested here.
- Battery tested at A-dialect positions only; positional breakdown not checked.

## Self-Audit

**Target-awareness**: p_o_o=0.10 was selected because it best reproduces the VMS o→o E_mid=2.801. The reported o→o Δ=+0.047 is conditional on this calibration. Stated in Interpretation.

**Feature-destroying implementation**: No feature-destroying details identified. The p_o_o rule directly promotes o-onset repetition at buffer draw time, which is precisely the feature under test.

**Extrapolation**: No claims that exceed the tested grid. Sweep covers p_o_o ∈ {0.00, 0.05, 0.10, 0.15, 0.20}; the optimal value falls within this range with clear monotonic behavior.

**Negative-result scope**: N/A — positive result.

**Control behavior**: No explicit shuffled control. The baseline (p_o_o=0.00) serves as the internal control and produces E2=1.986 > 1.0, as expected (copy buffer and non-uniform onset distribution generate some self-succession naturally). The remaining gap of 0.815 is what p_o_o=0.10 closes. This behavior is expected and not surprising.

## Conclusion

H458 resolved. p_o_o=0.10 reproduces o→o MID E2 (Δ=+0.047) while maintaining 19/19 PASS on the full A-dialect battery. A-dialect architecture advances to 12 mechanisms.
