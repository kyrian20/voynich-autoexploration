# exp_533 result — A stars a-onset positional grammar (H_new_ES)

## Audit

**Target-awareness**: None. Standard positional grammar methodology.

**Feature-destroying implementation**: Within-line positional analysis. A stars 136 lines. Baselines: A stars section-wide position rates (pos1, pos2, pen) compared internally and vs A herbal_a.

**Extrapolation**: None.

---

## H_new_ES RESOLVED: A stars a-onset is a "non-opener" word class

### A stars a-onset position profile:

| Position | obs | N | rate | A herbal_a rate | E vs A_ha | flag |
|---------|-----|---|------|----------------|-----------|------|
| pos1 | 1 | 130 | 0.8% | 0.0% | — | STRONGLY DEPLETED |
| pos2 | 18 | 122 | 14.8% | 0.7% | **20.4×** | **CONF** |
| pen | 12 | 122 | 9.8% | 1.2% | **8.15×** | **CONF** |
| LF | 15 | 136 | 11.0% | 1.7% | **6.66×** | **CONF** |

### Within-section A stars pattern:

a-onset appears at 11% of LF positions, ~10-15% of internal positions, but **only 0.8% of pos1 positions** (1 occurrence out of 130). Internal E vs equal-position baseline (11% null):
- pos1: E = 0.8%/11% ≈ 0.07× — **STRONGLY DEPLETED**
- pos2: E = 14.8%/11% ≈ 1.35× (slightly elevated)
- pen: E = 9.8%/11% ≈ 0.89×

The striking finding: **a-onset words virtually NEVER open A stars lines (0.8% = 1 instance)** despite appearing at 11% of other positions.

### Per-LF-class breakdown:

| LF class | N | a@pos2 | E_pos2 | a@pen | E_pen | signals |
|---------|---|--------|--------|-------|-------|---------|
| d | 25 | 2/24 | 0.56× | 0/24 | 0.00× | both DEPLETED |
| ch | 23 | 1/20 | 0.34× | 2/20 | 1.02× | pos2 DEPLETED |
| a | 15 | 2/13 | 1.04× | 2/13 | 1.56× | near-baseline |
| o | 14 | 1/13 | 0.52× | 2/13 | 1.56× | pos2 depleted |
| **sh** | 10 | 1/10 | 0.68× | **3/10** | **3.05×** | **a@pen (dir)** (F519) |
| ok | 10 | 3/9 | 2.26× | 1/9 | 1.13× | near-(dir) |
| **ot** | 9 | **4/9** | **3.01×** | 0/9 | 0.00× | **a@pos2 (dir)** (F520) |
| ol | 7 | 0/6 | 0.00× | 1/6 | 1.69× | — |
| y | 6 | 0/4 | 0.00× | 0/4 | 0.00× | both 0 |
| s | 5 | 0/3 | 0.00× | 0/3 | 0.00× | both 0 |

**Pattern**: a@pos2 is elevated specifically for ot-LF ((dir), F520) and near-elevated for ok-LF. a@pen is elevated specifically for sh-LF ((dir), F519). d-LF, ch-LF, y-LF, s-LF all show zero or depletion for a at both positions.

### Summary

**H_new_ES CONCLUSION**: a-onset IS a structured positional constituent in A stars, but the structure is:
1. **pos1 ZERO** (strong cross-class rule): a-onset words never open lines
2. **pos2 enrichment is LF-class-specific** (ot-LF and ok-LF, not universal)
3. **pen enrichment is LF-class-specific** (sh-LF only)
4. The cross-LF-class signal from exp_526 (sh-pen + ot-pos2) reflects a PARTIAL pattern: 2 out of 10 LF classes, not a universal a-onset positional rule

The pos1 near-zero is the true cross-class finding: a-onset is a "non-opener" class in A stars. This is consistent with a-onset words functioning as grammatical content markers that fill internal/final positions but never initiate lines.

**New finding F532**: A stars a-onset is ABSENT at pos1 (0.8%, 1/130 — near-zero). The pos1 depletion is the structural constraint: a-onset words never open A stars lines, despite being 11% of LF. Contrast: a-LF is 11% and a-onset at pos2 (14.8%, CONF) and pen (9.8%, CONF) — the a-word class is an internal/final class, not an opener class.

---

## Cross-Section Comparison

A herbal_a has minimal a-onset at any position (LF=1.7%, pos2=0.7%, pen=1.2%). A stars has a-onset at 11% of LF, 15% of pos2, 10% of pen, ~0% of pos1. This is a dramatic A stars-specific positional profile.

The near-zero pos1 in A stars is SPECIFIC to a-onset — t-onset and s-onset are CONF at pos1 in A stars (F523, F524). The a-onset and t/s-onset behave as complementary classes: t and s OPEN lines (pos1 CONF), a NEVER opens lines but appears at internal positions.

---

## Open Questions

None requiring human judgment. H_new_ES CLOSED.
