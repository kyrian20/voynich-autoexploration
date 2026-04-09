# Experiment exp_021: f57v↔f66r Character Overlap Test
Date: 2026-04-09

## Hypothesis Tested
H023: Does the character overlap between f57v's 17-token repeating cycle and f66r column 2 exceed random expectation?

## Key Results

### 1. Standard Single-Char Overlap: SIGNIFICANT

| Set | Characters |
|---|---|
| f57v cycle (14 chars) | I c d f k l m o p r t v x y |
| f66r col2 (11 chars)  | c d f l o p r s t x y |
| **Intersection (10)** | **c d f l o p r t x y** |
| Only in f57v (4) | I k m v |
| Only in f66r (1) | s |

- **Jaccard similarity: 0.667** (10/15 union)
- f66r col2 is almost entirely a subset of f57v's character set — only 's' appears in f66r but not f57v

### 2. Hypergeometric Test: p = 0.0026

| Parameter | Value |
|---|---|
| N (EVA total chars) | 25 |
| K (f57v char count) | 14 |
| n (f66r col2 char count) | 11 |
| Observed overlap | **10** |
| Expected under H0 | 6.16 |
| Excess above expected | +3.84 chars |
| **P(X ≥ 10)** | **0.0026** |

**The overlap significantly exceeds random expectation (p < 0.003).**

### 3. @Glyph Overlap

| Glyph | f57v | f66r | Note |
|---|---|---|---|
| @169 | @169;v (compound, at pos 10) | @169 (standalone, at col2 pos 9) | Same ID, different form |
| @172 | @172 (at pos 17) | @172 (standalone, at col2 pos 23) | Identical |
| @170 | present (pos 13) | absent | f57v only |
| @171 | present (pos 14) | absent | f57v only |
| @195 | absent | present (col2 pos 27) | f66r only |

- 2/4 f57v @glyph IDs (169, 172) appear in f66r col2
- @169 appears IMMEDIATELY AFTER 'f' in f66r col2 (position: ...f @169 x...) — f57v cycle also has 'f' at pos 9 IMMEDIATELY BEFORE @169;v at pos 10 — **same f→@169 adjacency**

### 4. Positional Correspondence: NONE

Spearman rho between f66r column 2 order and f57v cycle position: **ρ = -0.093** (near zero, t = -0.46).

The character ORDER in f66r column 2 does NOT correspond to character order in f57v's cycle. f66r is not a "linearized" or "reordered" version of f57v's cycle.

## Interpretation

**What the overlap shows:** f57v's 17-token cycle and f66r column 2 draw from a shared inventory of graphically simple, standalone EVA characters. The set overlap (10/15 union chars, p=0.003) is statistically significant — this cannot be explained by random character selection from the EVA alphabet.

**What the overlap does NOT show:** f66r column 2 is not a rotated or linearized version of f57v's cycle. The order structure is independent (ρ ≈ 0).

**The 'f → @169' adjacency**: In f57v, positions 9-10 are `f/@169;v` (f precedes the @169 compound). In f66r col2, the same adjacency appears: entry 8 is 'f', entry 9 is '@169'. This is a specific structural echo — the same two elements appear adjacent, in the same order, in both lists. This is not a necessary consequence of character-set overlap; it is an additional positional coincidence.

**The absent chars**: Characters exclusive to f57v (I, k, m, v) include two rare chars (m, v) and the capital-I glyph. The only character in f66r not in f57v is 's'. Both lists are heavily skewed toward the same subset of standalone EVA characters.

**H022 connection**: The shared chars (c, d, f, l, o, p, r, t, x, y) are precisely the "atomic/non-compound-forming" chars identified in H022. Both f57v's cycle and f66r col2 appear to operate within this same non-compound-forming character subset, suggesting they are structurally related — both operating on the same elementary character stratum of the writing system.

## Verdict

**H023 SUPPORTED.** The character overlap between f57v's cycle and f66r column 2 significantly exceeds random expectation (p = 0.003, Jaccard = 0.667). The additional structural echo (f→@169 adjacency) in both lists is a second independent connection. The two lists appear to draw from a shared, constrained character inventory, but organize them differently (no positional correlation).

The f57v↔f66r link identified by ZL3b transcribers ("cf f57v?") is quantitatively supported.

## New Finding Generated
F032: The character sets of f57v's 17-token repeating cycle and f66r column 2 significantly overlap (Jaccard=0.667, p=0.003 vs random). Both draw from the same 10-char subset of standalone EVA characters: {c, d, f, l, o, p, r, t, x, y}. Additionally, the f→@169 adjacency appears in both lists at the same order. The two folios share a character inventory but not a character order.
