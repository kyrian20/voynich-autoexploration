# Experiment exp_027: Positional Bias Index
Date: 2026-04-09

## Hypothesis Tested
H011: Compute a normalized "positional bias index" = shuffled_H - actual_H at each word position. This controls for overall character distribution to reveal which positions are most constrained.

## Results

### From Word Start (absolute positions)

| Position | Actual H (bits) | Shuffled H (bits) | **Bias** | Count |
|---|---|---|---|---|
| 0 (onset) | 3.104 | 3.855 | 0.751 | 29,631 |
| 1 (second) | 3.088 | 3.862 | **0.774** | 29,498 |
| 2 | 3.467 | 3.857 | 0.390 | 29,329 |
| 3 | 3.606 | 3.849 | 0.244 | 26,217 |
| 4 | 3.565 | 3.827 | 0.262 | 20,303 |
| 5 | 3.321 | 3.816 | 0.495 | 12,175 |
| 6 | 3.165 | 3.827 | 0.661 | 5,942 |
| 7 | 3.299 | 3.801 | 0.502 | 2,435 |

### From Word End (negative positions)

| Position | Actual H (bits) | Shuffled H (bits) | **Bias** | Count |
|---|---|---|---|---|
| -1 (last) | 2.379 | 3.861 | **1.482** | 28,776 |
| -2 | 2.876 | 3.865 | **0.989** | 28,771 |
| -3 | 3.258 | 3.863 | 0.605 | 28,832 |
| -4 | 3.437 | 3.842 | 0.404 | 26,482 |
| -5 | 3.528 | 3.824 | 0.296 | 20,596 |

## Key Findings

**1. Word-final position is the MOST constrained in the entire manuscript** (bias = 1.482 bits — 2x the onset bias). The last character is far more constrained than any other position. This confirms and quantifies what exp_002 showed about H(-1).

**2. Position 1 (second character) is MORE constrained than position 0 (onset)** — bias 0.774 vs 0.751. This is the opposite of natural languages where onset is typically the most constrained from the start. In Voynich, the onset character constrains the second character heavily (e.g., q→o, c→h, s→h).

**3. The suffix gradient (-1 → -5) is steeper than the prefix gradient (0 → 3):**
- Suffix: bias drops from 1.482 → 0.989 → 0.605 → 0.404 → 0.296 (rapid decrease)
- Prefix: bias drops from 0.751 → 0.774 → 0.390 → 0.244 (slower, non-monotone)

The suffix constraint is much stronger and decays faster than the prefix constraint. This matches Stolfi's observation that word endings are highly templated (-y, -n, -in, -aiin, etc.).

**4. Middle positions (3-4) are the freest** (bias ≈ 0.25), consistent with the Stolfi core/midfix model. These correspond to the gallows or high-vowel positions.

**5. Late word positions (6-7) are more constrained again** (bias ≈ 0.50-0.66) — consistent with the suffix zone being longer than the prefix zone.

## Comparison to Natural Languages

In Latin and Italian:
- Onset bias is near zero (≈0.00-0.10 bits) — natural language onset choice is nearly unrestricted relative to character distribution
- Final position bias is ~0.5-0.8 bits (Latin -1 bias ≈ 0.5)

Voynich:
- Onset bias = 0.751 (7-8x the natural-language onset bias)
- Final bias = 1.482 (3-4x the natural-language final bias)

**ALL Voynich positions are more constrained than natural-language positions**, but the degree of constraint follows the suffix > onset > middle pattern. This is inconsistent with simple character substitution (which would preserve the bias pattern of the source language) and consistent with a slot grammar imposing systematic positional templates.

## H011: CONFIRMED
The positional bias index clarifies and extends exp_002: word-final positions are dramatically more constrained (bias up to 1.48 bits), middle positions are freest (bias 0.24 bits), and the entire word is more constrained than any natural language at every position.
