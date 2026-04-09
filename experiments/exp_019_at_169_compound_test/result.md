# Experiment exp_019: @169;v Compound Test
Date: 2026-04-09

## Question
Is `@169;v` in f57v's L03 repeating sequence a single compound token (17-unit cycle, matching voynich.nu's "4×17 characters") or two separate tokens (18-unit cycle, as incorrectly stated in exp_015)?

## Method
Applied strict IVTFF dot-based tokenization to the raw L03 line from ZL3b, properly handling `[a:b]` uncertainty brackets (internal colons treated as part of the bracket, not separators). Directly inspected the characters immediately before and after `@169;v` in the raw string.

## Raw Evidence

ZL3b line f57v.3 contains: `...k.m.f.@169;v.t.r.@170;...`

The character immediately before `@169;v` is `.` (dot separator).
The character immediately after `@169;v` is `.` (dot separator).

`@169;v` is bounded by dots on both sides — it is **one compound token** between two dot separators.

## Result

| Metric | Value |
|---|---|
| Total tokens in L03 | **68** |
| Expected if 17-unit cycle | 4 × 17 = 68 ✓ |
| Expected if 18-unit cycle | 4 × 18 = 72 ✗ |
| Cycles detected | 4 |
| Tokens per cycle | **17 each** |

```
Cycle 1 (17): o l [d:j] r v x k m f  @169;v  t r @170 @171 y  I  @172
Cycle 2 (17): o l  d    r v x k m f  @169;v  t r @170 @171 y  c  @172
Cycle 3 (17): o l  d    r v x k m p  @169;v  t r @170 @171 y  c  @172
Cycle 4 (17): o l  d    r v x k m p  @169;v  t r @170 @171 y  c  @172
```

## Verdict

**voynich.nu is correct: the f57v repeating cycle is 4 × 17 tokens.**

`@169;v` is a single compound glyph unit in ZL3b — the non-standard `@169` character physically incorporates a 'v' stroke (or is a ligature of a special glyph with 'v'). The semicolon terminates the @NNN code; the 'v' immediately following (with no dot separator) is part of the same compound token.

## Correction to exp_015 (F030)

exp_015 result.md stated "an 18-character sequence" and listed an 18-row table for the cycle. This was incorrect due to naive regex extraction of `@169` which split the compound token. The correct description is a **17-token cycle** with `@169;v` as a single unit at position 10.

### Corrected cycle structure

| Position | Inv/Var | Cycle 1 | Cycles 2-4 |
|---|---|---|---|
| 1 | invariant | o | o |
| 2 | invariant | l | l |
| 3 | [uncertain] | [d:j] | d |
| 4 | invariant | r | r |
| 5 | invariant | v | v |
| 6 | invariant | x | x |
| 7 | invariant | k | k |
| 8 | invariant | m | m |
| 9 | **VARIANT** | f | f(×2), p(×2) |
| 10 | invariant | @169;v | @169;v |
| 11 | invariant | t | t |
| 12 | invariant | r | r |
| 13 | invariant | @170 | @170 |
| 14 | invariant | @171 | @171 |
| 15 | invariant | y | y |
| 16 | **VARIANT** | I | c |
| 17 | invariant | @172 | @172 |

- Position 3: [d:j] is transcriber uncertainty (likely d throughout), not a structural variant
- Truly variant positions: 9 (f→p, cycles 1-2 vs 3-4) and 16 (I vs c)
- **15 invariant / 2 variant** out of 17 positions

## Implications

1. **@169 as a compound glyph:** `@169;v` is a single manuscript glyph that visually incorporates a 'v' stroke. In EVA notation, the `@169` represents the non-standard component, and the attached 'v' indicates the compound includes a standard 'v'-shaped element.

2. **The @glyph cluster is a 4-member sequence:** @169;v → @170 → @171 → @172 (positions 10, 13, 14, 17 of the 17-unit cycle). The @169 "glyph" already includes 'v' as part of its compound form.

3. **The @glyph census count is still correct:** exp_016 counted @169 appearing ×4 (one per cycle) — this is correct since `@169;v` is one token, and re.findall finds @169 within it.

4. **The f57v↔f66r link is unchanged:** f66r column 2 lists `@169` and `@172` as standalone entries. The compound `@169;v` in f57v vs. standalone `@169` in f66r may reflect different usage contexts for the same underlying glyph.
