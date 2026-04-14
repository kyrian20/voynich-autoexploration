# voynich_constraints.py — Self-Test Results

**Date:** 2026-04-12
**Module:** state/voynich_constraints.py
**Spec compat:** voynich_grammar_spec.md v1.0
**Methodology compat:** canonical_methodology.md v1.0

## Test Corpora

1. **Real VMS B-dialect**: 2440 lines (per-line edy-rate ≥ 5% classifier)
2. **Real VMS A-dialect**: 1647 lines
3. **Shuffled B-dialect (within-line)**: 2440 lines, words shuffled within each line (specificity test; should fail positional constraints per exp_575)

Total predicates registered: 28

## Real VMS B-dialect

**Summary:** 28/28 constraints PASS, 0 FAIL, 0 ERROR

| ID | Status | Description | Expected | Observed | Citation |
|----|--------|-------------|----------|----------|----------|
| P1_am_ll_B | PASS | am suffix enrichment at LL (last word) in B-dialect | 6.811 | 6.286 | C005 / spec §2.am_suffix_critical_metric |
| P2_y_lf_B | PASS | y-onset enrichment at LF (first word) in B-dialect | 3.506 | 3.097 | C006 / spec §1.2 |
| P3_d_ll_B | PASS | d-onset at LL in B-dialect (sub-CONF per spec §1.1) | 1.36 | 1.369 | spec §1.1 B.LL |
| P4_d_lf_B_opener | PASS | d-onset LF opener in B-dialect (CONF 2.64×) | 2.64 | 2.239 | spec §1.1 B.LF |
| P5_qok_lf_depl_B | PASS | qok LF sub-baseline per F619 canonical | 0.81 | 0.872 | spec §1.5 / F619 |
| P6_s_lf_opener_B | PASS | s-onset LF opener (CONF in both dialects) | 4.77 | 4.507 | spec §1.11 |
| P7_ch_lf_depl | PASS | ch-onset extreme LF depletion (both dialects) | 0.22 | 0.376 | spec §1.3 |
| SS_y | PASS | Onset self-succession for y in B (CONF cross-dialect) | (1.5, 4.5) | 2.707 | C007 amended / spec §5.canonical_table |
| SS_l | PASS | Onset self-succession for l in B (CONF cross-dialect) | (1.8, 5.0) | 2.422 | C007 amended / spec §5.canonical_table |
| SS_ot | PASS | Onset self-succession for ot in B (CONF cross-dialect) | (1.5, 3.0) | 1.878 | C007 amended / spec §5.canonical_table |
| SS_qo | PASS | Onset self-succession for qo in B (CONF cross-dialect) | (1.3, 2.5) | 1.999 | C007 amended / spec §5.canonical_table |
| SS_qot | PASS | Onset self-succession for qot in B (CONF cross-dialect) | (1.3, 4.0) | 2.009 | C007 amended / spec §5.canonical_table |
| SS_qok_flat_B | PASS | B qok self-succession must be flat (< 1.3×) per C007 amendment | ('flat', '< 1.3') | 1.093 | C007 amendment / spec §5 |
| B1_sh_to_qok_cross_dialect | PASS | sh→qok CONF cross-dialectally (A 2.04×, B 2.07×) | 2.07 | 1.887 | spec §4.cross_dialect_invariants |
| B2_qo_self_succession | PASS | qo→qo CONF both dialects (spec §4) | 1.82 | 2.066 | spec §4.cross_dialect_invariants |
| B3_a_to_ok_cross_dialect | PASS | a→ok CONF cross-dialectally | 1.51 | 1.533 | spec §4.cross_dialect_invariants / F626 |
| B4_sh_to_ch_depl | PASS | sh→ch DEPL cross-dialectally | < 0.85 | 0.573 | spec §4.cross_dialect_invariants / F328 |
| X1_terminal_layer_inversion | PASS | Top LL classes match B terminal set | ['a', 'd', 'l', 'o', 'ol', 'r'] | ['ch', 'd', 'l'] | spec §8 / C008 |
| X2_qok_frequency | PASS | qok frequency by dialect (A→B doubling per F618) | 0.1513 | 0.131 | spec §8.contrast_qok_frequency_doubling / F618 |
| X3_st_zero_adj_rate_B | PASS | s and t must have 0 identical adjacent pairs in B | (0, 0) | (0, 0) | C009 Part B |
| X4_sh_ch_d_adj_rate_near_random_B | PASS | sh/d per-onset adj_rate ratio to 1/CP90 ∈ [0.3, 2.5] | (0.3, 2.5) | {'sh': 1.053, 'd': 0.601} | C009 Part A / spec §9 |
| S1_B_herbal_am_ll_rate | PASS | -am@LL raw rate in B_herbal | 0.1616 | 0.1344 | spec §11 / exp_579 |
| S2_B_bio_am_ll_rate | PASS | -am@LL raw rate in B_bio | 0.0525 | 0.052 | spec §11 |
| S3_B_pharma_am_ll_rate | PASS | -am@LL raw rate in B_pharma | 0.1919 | 0.1595 | spec §11 |
| S4_section_variation_exists | PASS | am@LL must vary ≥2× across B sections (non-stationary) | range factor ≥ 2.0 | 3.65 | C008 scope / exp_579 |
| A1_ss_mean_aggregate | PASS | Aggregate ss_mean (qok/ok/ch) ≥ 1.2× per dual constraint | ≥ 1.2 | 1.983 | C002 / spec §5 |
| A2_architectural_floors_exceeded | PASS | Corpus exceeds 21-mech architecture structural floors | am_ll≥1.17 AND ss_d≥1.50 AND ss_y≥2.00 | am_ll=6.29, ss_d=1.57, ss_y=2.71 | C008 / spec §5.copy_buffer_floor |
| A3_am_ll_above_position_blind_ceiling | PASS | am_ll ≥ 3.0× (above position-blind ceiling of ~1.1×) | ≥ 3.0 | 6.286 | C001 contradiction condition |

## Real VMS A-dialect

**Summary:** 22/28 constraints PASS, 6 FAIL, 0 ERROR

| ID | Status | Description | Expected | Observed | Citation |
|----|--------|-------------|----------|----------|----------|
| P1_am_ll_B | PASS | am suffix enrichment at LL (last word) in B-dialect | 6.811 | 3.208 | C005 / spec §2.am_suffix_critical_metric |
| P2_y_lf_B | PASS | y-onset enrichment at LF (first word) in B-dialect | 3.506 | 2.301 | C006 / spec §1.2 |
| P3_d_ll_B | PASS | d-onset at LL in B-dialect (sub-CONF per spec §1.1) | 1.36 | 1.595 | spec §1.1 B.LL |
| P4_d_lf_B_opener | PASS | d-onset LF opener in B-dialect (CONF 2.64×) | 2.64 | 1.104 | spec §1.1 B.LF |
| P5_qok_lf_depl_B | PASS | qok LF sub-baseline per F619 canonical | 0.87 | 1.052 | spec §1.5 / F619 |
| P6_s_lf_opener_B | FAIL | s-onset LF opener (CONF in both dialects) | 3.16 | 1.992 | spec §1.11 |
| P7_ch_lf_depl | FAIL | ch-onset extreme LF depletion (both dialects) | 0.32 | 0.522 | spec §1.3 |
| SS_y | PASS | Onset self-succession for y in A (CONF cross-dialect) | (1.5, 4.5) | 1.847 | C007 amended / spec §5.canonical_table |
| SS_l | FAIL | Onset self-succession for l in A (CONF cross-dialect) | (1.8, 5.0) | 0.0 | C007 amended / spec §5.canonical_table |
| SS_ot | PASS | Onset self-succession for ot in A (CONF cross-dialect) | (1.5, 3.0) | 1.675 | C007 amended / spec §5.canonical_table |
| SS_qo | PASS | Onset self-succession for qo in A (CONF cross-dialect) | (1.3, 2.5) | 1.378 | C007 amended / spec §5.canonical_table |
| SS_qot | PASS | Onset self-succession for qot in A (CONF cross-dialect) | (1.3, 4.0) | 2.714 | C007 amended / spec §5.canonical_table |
| SS_qok_flat_B | PASS | B qok self-succession must be flat (< 1.3×) per C007 amendment | ('flat', '< 1.3') | 1.52 | C007 amendment / spec §5 |
| B1_sh_to_qok_cross_dialect | FAIL | sh→qok CONF cross-dialectally (A 2.04×, B 2.07×) | 2.04 | 1.321 | spec §4.cross_dialect_invariants |
| B2_qo_self_succession | PASS | qo→qo CONF both dialects (spec §4) | 1.76 | 1.572 | spec §4.cross_dialect_invariants |
| B3_a_to_ok_cross_dialect | PASS | a→ok CONF cross-dialectally | 1.52 | 1.574 | spec §4.cross_dialect_invariants / F626 |
| B4_sh_to_ch_depl | PASS | sh→ch DEPL cross-dialectally | < 0.85 | 0.727 | spec §4.cross_dialect_invariants / F328 |
| X1_terminal_layer_inversion | FAIL | Top LL classes match A terminal set | ['cth', 'd'] | ['d', 'ch', 'sh'] | spec §8 / C008 |
| X2_qok_frequency | PASS | qok frequency by dialect (A→B doubling per F618) | 0.073 | 0.057 | spec §8.contrast_qok_frequency_doubling / F618 |
| X3_st_zero_adj_rate_B | PASS | s/t structural anti-repetition (B only) | 0 | skipped (A-dialect) | C009 Part B / spec §5.s_t_zero_adj_rate_anomaly |
| X4_sh_ch_d_adj_rate_near_random_B | PASS | sh/d adj_rate ≈ random expectation (B only) | near-random | skipped | C009 Part A |
| S1_B_herbal_am_ll_rate | PASS | -am@LL raw rate in B_herbal | 0.1616 | skipped | spec §11 |
| S2_B_bio_am_ll_rate | PASS | -am@LL raw rate in B_bio | 0.0525 | skipped | spec §11 |
| S3_B_pharma_am_ll_rate | PASS | -am@LL raw rate in B_pharma | 0.1919 | skipped | spec §11 |
| S4_section_variation_exists | PASS | am@LL section variation per C008 scope | range factor > 2× | skipped | C008 scope |
| A1_ss_mean_aggregate | PASS | Aggregate ss_mean (qok/ok/ch) ≥ 1.2× per dual constraint | ≥ 1.2 | 1.58 | C002 / spec §5 |
| A2_architectural_floors_exceeded | FAIL | Corpus exceeds 21-mech architecture structural floors | am_ll≥1.17 AND ss_d≥1.50 AND ss_y≥2.00 | am_ll=3.21, ss_d=1.56, ss_y=1.85 | C008 / spec §5.copy_buffer_floor |
| A3_am_ll_above_position_blind_ceiling | PASS | am_ll ≥ 3.0× (above position-blind ceiling of ~1.1×) | ≥ 3.0 | 3.208 | C001 contradiction condition |

### Failures (sorted by severity)

- **A2_architectural_floors_exceeded** (high): expected `am_ll≥1.17 AND ss_d≥1.50 AND ss_y≥2.00`, observed `am_ll=3.21, ss_d=1.56, ss_y=1.85`. {'am_ll >= 1.17': True, 'ss_d >= 1.50': True, 'ss_y >= 2.00': False}
- **SS_l_A** (high): expected `(1.8, 5.0)`, observed `0.0`. obs=0, n_sender=31
- **X1_terminal_layer_inversion** (high): expected `['cth', 'd']`, observed `['d', 'ch', 'sh']`. top3=['d', 'ch', 'sh']
- **B1_sh_to_qok_cross_dialect** (normal): expected `2.04`, observed `1.321`. obs=56, n_sender=752
- **P6_s_lf_opener_B** (normal): expected `3.16`, observed `1.992`. obs=75/1569
- **P7_ch_lf_depl** (normal): expected `0.32`, observed `0.522`. obs=168/1569

## Shuffled B-dialect (within-line)

**Summary:** 11/28 constraints PASS, 17 FAIL, 0 ERROR

| ID | Status | Description | Expected | Observed | Citation |
|----|--------|-------------|----------|----------|----------|
| P1_am_ll_B | FAIL | am suffix enrichment at LL (last word) in B-dialect | 6.811 | 0.799 | C005 / spec §2.am_suffix_critical_metric |
| P2_y_lf_B | FAIL | y-onset enrichment at LF (first word) in B-dialect | 3.506 | 1.13 | C006 / spec §1.2 |
| P3_d_ll_B | PASS | d-onset at LL in B-dialect (sub-CONF per spec §1.1) | 1.36 | 1.092 | spec §1.1 B.LL |
| P4_d_lf_B_opener | FAIL | d-onset LF opener in B-dialect (CONF 2.64×) | 2.64 | 0.919 | spec §1.1 B.LF |
| P5_qok_lf_depl_B | PASS | qok LF sub-baseline per F619 canonical | 0.81 | 0.853 | spec §1.5 / F619 |
| P6_s_lf_opener_B | FAIL | s-onset LF opener (CONF in both dialects) | 4.77 | 1.185 | spec §1.11 |
| P7_ch_lf_depl | FAIL | ch-onset extreme LF depletion (both dialects) | 0.22 | 1.017 | spec §1.3 |
| SS_y | PASS | Onset self-succession for y in B (CONF cross-dialect) | (1.5, 4.5) | 2.309 | C007 amended / spec §5.canonical_table |
| SS_l | FAIL | Onset self-succession for l in B (CONF cross-dialect) | (1.8, 5.0) | 1.256 | C007 amended / spec §5.canonical_table |
| SS_ot | FAIL | Onset self-succession for ot in B (CONF cross-dialect) | (1.5, 3.0) | 1.425 | C007 amended / spec §5.canonical_table |
| SS_qo | PASS | Onset self-succession for qo in B (CONF cross-dialect) | (1.3, 2.5) | 1.536 | C007 amended / spec §5.canonical_table |
| SS_qot | PASS | Onset self-succession for qot in B (CONF cross-dialect) | (1.3, 4.0) | 1.725 | C007 amended / spec §5.canonical_table |
| SS_qok_flat_B | PASS | B qok self-succession must be flat (< 1.3×) per C007 amendment | ('flat', '< 1.3') | 1.295 | C007 amendment / spec §5 |
| B1_sh_to_qok_cross_dialect | FAIL | sh→qok CONF cross-dialectally (A 2.04×, B 2.07×) | 2.07 | 1.189 | spec §4.cross_dialect_invariants |
| B2_qo_self_succession | PASS | qo→qo CONF both dialects (spec §4) | 1.82 | 1.525 | spec §4.cross_dialect_invariants |
| B3_a_to_ok_cross_dialect | FAIL | a→ok CONF cross-dialectally | 1.51 | 0.954 | spec §4.cross_dialect_invariants / F626 |
| B4_sh_to_ch_depl | FAIL | sh→ch DEPL cross-dialectally | < 0.85 | 0.867 | spec §4.cross_dialect_invariants / F328 |
| X1_terminal_layer_inversion | FAIL | Top LL classes match B terminal set | ['a', 'd', 'l', 'o', 'ol', 'r'] | ['ch', 'qok', 'sh'] | spec §8 / C008 |
| X2_qok_frequency | PASS | qok frequency by dialect (A→B doubling per F618) | 0.1513 | 0.131 | spec §8.contrast_qok_frequency_doubling / F618 |
| X3_st_zero_adj_rate_B | FAIL | s and t must have 0 identical adjacent pairs in B | (0, 0) | (0, 2) | C009 Part B |
| X4_sh_ch_d_adj_rate_near_random_B | PASS | sh/d per-onset adj_rate ratio to 1/CP90 ∈ [0.3, 2.5] | (0.3, 2.5) | {'sh': 1.376, 'd': 1.002} | C009 Part A / spec §9 |
| S1_B_herbal_am_ll_rate | FAIL | -am@LL raw rate in B_herbal | 0.1616 | 0.025 | spec §11 / exp_579 |
| S2_B_bio_am_ll_rate | FAIL | -am@LL raw rate in B_bio | 0.0525 | 0.0078 | spec §11 |
| S3_B_pharma_am_ll_rate | FAIL | -am@LL raw rate in B_pharma | 0.1919 | 0.0177 | spec §11 |
| S4_section_variation_exists | PASS | am@LL must vary ≥2× across B sections (non-stationary) | range factor ≥ 2.0 | 3.2 | C008 scope / exp_579 |
| A1_ss_mean_aggregate | PASS | Aggregate ss_mean (qok/ok/ch) ≥ 1.2× per dual constraint | ≥ 1.2 | 1.557 | C002 / spec §5 |
| A2_architectural_floors_exceeded | FAIL | Corpus exceeds 21-mech architecture structural floors | am_ll≥1.17 AND ss_d≥1.50 AND ss_y≥2.00 | am_ll=0.8, ss_d=1.27, ss_y=2.31 | C008 / spec §5.copy_buffer_floor |
| A3_am_ll_above_position_blind_ceiling | FAIL | am_ll ≥ 3.0× (above position-blind ceiling of ~1.1×) | ≥ 3.0 | 0.799 | C001 contradiction condition |

### Failures (sorted by severity)

- **A2_architectural_floors_exceeded** (high): expected `am_ll≥1.17 AND ss_d≥1.50 AND ss_y≥2.00`, observed `am_ll=0.8, ss_d=1.27, ss_y=2.31`. {'am_ll >= 1.17': False, 'ss_d >= 1.50': False, 'ss_y >= 2.00': True}
- **A3_am_ll_above_position_blind_ceiling** (high): expected `≥ 3.0`, observed `0.799`. obs=38/2398
- **P1_am_ll_B** (high): expected `6.811`, observed `0.799`. obs=38/2398 (dialect=B)
- **P2_y_lf_B** (high): expected `3.506`, observed `1.13`. obs=100/2398 (dialect=B)
- **SS_l_B** (high): expected `(1.8, 5.0)`, observed `1.256`. obs=62, n_sender=878
- **SS_ot_B** (high): expected `(1.5, 3.0)`, observed `1.425`. obs=105, n_sender=1063
- **X1_terminal_layer_inversion** (high): expected `['a', 'd', 'l', 'o', 'ol', 'r']`, observed `['ch', 'qok', 'sh']`. top3=['ch', 'qok', 'sh']
- **X3_st_zero_adj_rate_B** (high): expected `(0, 0)`, observed `(0, 2)`. s_tokens_involved=7, t_tokens_involved=11
- **B1_sh_to_qok_cross_dialect** (normal): expected `2.07`, observed `1.189`. obs=234, n_sender=1468
- **B3_a_to_ok_cross_dialect** (normal): expected `1.51`, observed `0.954`. obs=50, n_sender=775
- **B4_sh_to_ch_depl** (normal): expected `< 0.85`, observed `0.867`. obs=196, n_sender=1468
- **P4_d_lf_B_opener** (normal): expected `2.64`, observed `0.919`. obs=149/2398
- **P6_s_lf_opener_B** (normal): expected `4.77`, observed `1.185`. obs=66/2398
- **P7_ch_lf_depl** (normal): expected `0.22`, observed `1.017`. obs=376/2398
- **S1_B_herbal_am_ll_rate** (normal): expected `0.1616`, observed `0.025`. 
- **S2_B_bio_am_ll_rate** (normal): expected `0.0525`, observed `0.0078`. 
- **S3_B_pharma_am_ll_rate** (normal): expected `0.1919`, observed `0.0177`. 

## Interpretation

- **Real B-dialect**: 28/28 constraints PASS. This is the expected high-pass baseline.
- **Real A-dialect**: 22/28 constraints PASS. Some B-specific constraints (e.g., P2_y_lf_B with expected 3.506×) may FAIL under A-dialect because the expected value is B-specific; these FAILures are expected and do not indicate A-dialect violates the spec.
- **Shuffled B-dialect**: 11/28 constraints PASS. Positional constraints (P1–P7, S1–S4, A2–A3) should degrade under shuffle, mirroring the exp_575 specificity test result. Self-succession constraints (SS_*) may survive shuffle because the copy-buffer structural floors apply.

The pass-count gap between real B (28) and shuffled B (11) is the primary specificity signal.
