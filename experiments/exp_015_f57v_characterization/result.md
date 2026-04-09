# Experiment exp_015: f57v Characterization
Date: 2026-04-09

## Visual Layout (from manuscript image f57v.jpg)

The folio shows a **cosmological wheel diagram** — the page's dominant feature is 4 concentric rings of Voynich text forming a circular band structure. The center of the wheel contains a small illustration: appears to be an anthropomorphic figure (arms extended, possibly bird-like or winged) surrounded by decorative flower-like elements. The wheel occupies roughly the upper 75% of the page. At the bottom, 4 green/blue star-shaped or flower-shaped decorative elements are spaced across the page. In the lower right corner, a small symbol is visible (identified in ZL3b comments as a Saturn symbol, transcribed as @255;).

**ZL3b description confirms:** "Four bands of circular text. Contains various sequences of characters." There is also one outer @L0 label ("start here"), and 8 inner @L0 labels and 4 @Ro (rider) labels inside the innermost ring.

## ZL3b Header
```
<f57v>  <! $Q=H $P=B $F=a $B=1 $I=C $H=1>
```
- $Q=H: Quire H
- $I=C: Illustration type = Cosmological
- $H=1: Hand 1 (Scribe 1, Currier A)
- $P=B: Position B (verso)
- $L field absent (no language designation — unusual)

**Note:** ZL3b inline comments say "Currier's language B, hand 2 (???)" — a discrepancy with the $H=1 header. The transcriber was uncertain about hand attribution. The $H=1 in the header takes precedence (Davis 2020 assigns Hand 1).

## Full Transcription Summary

| Locus | Count | Description |
|---|---|---|
| @L0 | 5 | Labels: 1 outer ("start here" = dairal), 4 inner ring labels |
| @Cc | 1 | First (outermost?) circular band — continuous body text |
| +Cc | 3 | Three more circular bands (inner bands) |
| @Ro | 4 | Rider labels inside innermost ring |

**Total: 13 text lines (28 raw including comment lines)**

### Outer Circular Band (L02, @Cc)
A continuous text line of ~120 tokens — standard Voynich prose with typical word forms (dairal, sal, soeos, okees, soefchees, okey, defo, rkedam, etc.). No @glyph occurrences. This band looks like ordinary Voynich text.

### Inner Circular Bands (L03–L05, +Cc)

#### L03 — The Repeating Sequence
```
o.l.[d:j].r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.I.@172;
o.l.d.r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.c.@172;
o.l.d.r.v.x.k.m.p.@169;v.t.r.@170;.@171;.y.c.@172;
o.l.d.r.v.x.k.m.p.@169;v.t.r.@170;.@171;.y.c.@172;
```
This is the same 18-character unit **repeated exactly 4 times** with controlled variation:

| Position | Cycle 1 | Cycle 2 | Cycle 3 | Cycle 4 |
|---|---|---|---|---|
| 1 | o | o | o | o |
| 2 | l | l | l | l |
| 3 | [d:j]* | d | d | d |
| 4 | r | r | r | r |
| 5 | v | v | v | v |
| 6 | x | x | x | x |
| 7 | k | k | k | k |
| 8 | m | m | m | m |
| 9 | **f** | **f** | **p** | **p** |
| 10 | @169 | @169 | @169 | @169 |
| 11 | v | v | v | v |
| 12 | t | t | t | t |
| 13 | r | r | r | r |
| 14 | @170 | @170 | @170 | @170 |
| 15 | @171 | @171 | @171 | @171 |
| 16 | y | y | y | y |
| 17 | **I** | **c** | **c** | **c** |
| 18 | @172 | @172 | @172 | @172 |

*[d:j] = transcriber uncertainty between 'd' and 'j' in cycle 1

**Invariant positions (16/18):** o, l, r, v, x, k, m, v, t, r, @170, @171, y, @172 are IDENTICAL in all 4 cycles.
**Variant positions (2/18):**
- Position 9: f (cycles 1-2) → p (cycles 3-4). Both are gallows characters.
- Position 17: I (cycle 1) → c (cycles 2-4).

The sequence has the structure: `[o l d r v x k m] [f/p @169 v t r @170 @171 y I/c @172]`
The first 8 positions are standard EVA characters; positions 9-18 include all 4 @glyphs in a fixed order: @169 → @170 → @171 → @172.

#### L04 — Band with scattered @glyph
Largely standard Voynich text. Contains `@172;` once in context: `...tchor.kedar.dal.@172;.daiin.aiin.otal.daro.v`
This is @172 appearing OUTSIDE the repeating sequence, in what looks like normal prose.

#### L05 — Band with @170 and @171
Mixed text. Contains `@170` and `@171` in context:
- `m.aiin.d.@170;.c.f.s.y.l.k.x.l.r.@171;,ar.o.r`
These appear as standalone characters interspersed in normal Voynich text.

## @Glyph Occurrence Summary

| Glyph | Total | In L03 repeating | Outside repeating |
|---|---|---|---|
| @169 | 4 | 4 | 0 |
| @170 | 5 | 4 | 1 (L05) |
| @171 | 5 | 4 | 1 (L05) |
| @172 | 5 | 4 | 1 (L04) |
| **Total** | **19** | **16** | **3** |

**@169 is the most constrained:** it appears ONLY inside the repeating sequence, always in the fixed context `k.m.f/p → @169 → v.t.r.@170`. Never appears outside this structural role.

**@170, @171, @172 each appear once outside the repeating sequence** — in other circular bands (L04, L05) where they occur as isolated characters in otherwise standard Voynich text.

## @Glyph Context Structure

The invariant context for each @glyph in the repeating sequence:
```
... k . m . f/p . @169 . v . t . r . @170 . @171 . y . I/c . @172 . o . l . d ...
```
This is a perfectly regular 4-@glyph cluster embedded in a repeating cycle. The @glyphs form a GROUP of 4 consecutive special characters (@169, @170, @171, @172), always in this order, always with the same flanking characters on each side.

## f57v vs f66r @Glyph Comparison

| Glyph | f57v | f66r |
|---|---|---|
| @169 | ×4 (in repeating sequence only) | ×1 (column 2, line L24) |
| @170 | ×5 (4 in sequence + 1 outlier) | absent |
| @171 | ×5 (4 in sequence + 1 outlier) | absent |
| @172 | ×5 (4 in sequence + 1 outlier) | ×1 (column 2, line L38) |
| @195 | absent | ×1 (column 2, line L42) |

**Shared:** @169 and @172.
**Only f57v:** @170 and @171 (these are the "middle" @glyphs in the f57v sequence; f66r skips them).
**Only f66r:** @195 (a fifth distinct special glyph not in f57v).

The f66r cross-reference ("cf f57v?") is on line L38, where @172 appears. This is exactly one of the shared glyphs.

In f57v, @169 and @172 are always the FIRST and LAST of the 4-glyph cluster. In f66r, they appear as isolated column entries (not in sequence with each other).

## Key Structural Findings

1. **The "key-like" quality is in L03.** The repeating 18-character sequence (4 cycles, positions 1-18) is the structural anomaly ZL3b flagged. It's unlike any other Voynich text: a short sequence repeated 4 times with controlled variation at exactly 2 positions.

2. **The @glyph cluster @169→@170→@171→@172 is a fixed ordered 4-tuple.** It appears in the same relative order in every cycle. This suggests these 4 glyphs function as a set (possibly 4 positions in a mapping table, 4 elements of an ordered series, or 4 numerals).

3. **The variant characters at positions 9 and 17 (f/p and I/c) are both gallows-class or gallows-adjacent.** The f/p switch is a gallows transposition; the I/c switch is uncertain (I may be a capital i or a distinct character). The 4 cycles show: (f,I), (f,c), (p,c), (p,c) — possibly 3 distinct combinations.

4. **@169 is exclusively structural** — it appears only inside the repeating sequence, always in the same fixed context. It is the most "special" of the special glyphs, never used in ordinary text flow.

5. **@170, @171, @172 also appear as outliers** in other bands (L04, L05), suggesting they can occur in ordinary text as well as in the repeating structure. @169 cannot.

6. **f66r samples @169 and @172 but not @170/@171.** If f66r column 2 is listing "available" special glyphs, it has only 2 of the 4 from f57v's ordered cluster, plus @195 (not in f57v). The f66r list is not a subset of the f57v sequence.

## Open Questions From This Experiment
- What are @169, @170, @171, @172 physically? They resist EVA representation. Are they alchemical symbols? Roman numerals? Greek letters? The @255; Saturn symbol in the f57v corner confirms the folio contains non-Voynich symbol systems — the @glyphs may be from the same repertoire.
- The I (capital) vs c variation at position 17: is this a scribal slip, an intentional distinction, or transcription uncertainty?
- Does the 4-cycle repeating structure map onto the physical structure of the wheel (one cycle per quadrant)?
