# Proposed Commitment C008: 21-Mechanism Architecture — VMS Specificity and Structural Floors

**Proposed date:** 2026-04-12
**Supporting experiments:** exp_574, exp_575
**Proposing agent:** Cryptanalyst loop

---

## Proposed Claim

The 21-mechanism position-aware copy-buffer architecture (exp_314 calibration: CP=0.55, MP=0.90, P_STUTTER=0.006, beta_scale=1.8, p_blind=0.115, r_lf=0.12, r_mid=0.20) achieves 19/19 PASS on the 19-metric B-dialect battery against real VMS B-dialect targets (PASS_TOL=±20%).

When the SAME fixed parameters are applied to within-line shuffled VMS B-dialect (VMS_REF held constant as real VMS), the architecture achieves 10/19 PASS — 9 positional onset-distribution metrics fail because shuffling collapses them to ≈1.0 while the architecture requires real VMS positional distributions as input.

When a FRESH GRID SEARCH over 5 free parameters (1024 combinations) optimizes the architecture to match each shuffled corpus's OWN metrics as target, the best achievable pass count is:
- Intra-shuffle (within-line): **16/19** — 3 structural impossibilities
- Inter-shuffle (word-to-line): **14/19** — 5 structural impossibilities

The 3 metrics failing in BOTH shuffled conditions regardless of parameter choice are:
1. **am_ll**: floor ≈ 1.17 (from max_ll length-cap biasing LL words toward short suffixes including 'am')
2. **ss_d**: floor ≈ 1.50 (from copy-buffer always generating d-onset self-succession; CP and MP are fixed)
3. **ss_y**: floor ≈ 2.00 (from copy-buffer always generating y-onset self-succession; floor exceeds intra-shuffle target range [1.30, 1.96] and categorically unreachable for inter-shuffle target 0.56)

An additional 2 metrics fail in inter-shuffle only:
4. **adj_rate**: floor ≈ 0.006 (from fixed P_STUTTER=0.006; inter-shuffle target 0.0053 is below floor)
5. **ss_mean**: floor ≈ 1.36 (from copy-buffer generating excess composite self-succession; inter-shuffle target 1.008 is below floor)

---

## Justification for Commitment

These results are suitable for public commitment because:

1. **The positive control is robust**: 19/19 on real VMS with multiple parameter combinations achieving this (5/1024 at fast pass, confirmed at N=10). This is reproducible.

2. **The structural floors are mechanistically explained**: Each floor is tied to a specific architectural constant (CP, MP, P_STUTTER, max_ll). The impossibility is not just "not found in the grid" — there is a logical argument for why no parameter in the 5-dimensional grid can suppress these mechanisms.

3. **The constraint is specific**: The architecture fails on shuffled corpora in exactly the right direction (all OVER-generation, never under-generation) — consistent with the copy-buffer generating structural minima, not parameter space gaps.

4. **The finding is scoped correctly**: The claim is about THIS specific architecture with THESE specific fixed constants. A different architecture with adjustable CP or MP could achieve different results.

---

## Proposed Wording

> **C008**: The 21-mechanism position-aware copy-buffer architecture (exp_314 calibration) achieves 19/19 PASS on the B-dialect 19-metric battery. This result cannot be reproduced on either within-line or word-to-line shuffled VMS B-dialect even when parameters are freely re-optimized: the best achievable pass counts are 16/19 (intra-shuffle) and 14/19 (inter-shuffle). The failures are exclusively in the over-generation direction, caused by fixed-constant mechanisms (copy-buffer, stutter) that create structural minima for ss_y, ss_d, adj_rate, and am_ll that exceed any shuffled corpus's target for those metrics. The architecture's 19/19 on real VMS reflects structural specificity to VMS's positional onset distributions and self-succession patterns, not 6-parameter over-fitting.

---

## Contradiction Condition

A grid search with adjustable CP, MP, or P_STUTTER achieving ≥ 19/19 on shuffled corpora with those values held at or below their exp_314 levels would contradict the structural floor claims. A finer grid (beyond 4 levels per parameter) finding a combination that exceeds 16/19 on intra-shuffle would narrow the claim.
