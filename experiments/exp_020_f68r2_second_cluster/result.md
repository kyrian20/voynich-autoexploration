# Experiment exp_020: f68r2 — Second @Glyph Cluster Test
Date: 2026-04-09

## Question (H027)
Is f68r2's @231-@234 sequence a second structured @glyph cluster analogous to f57v's @169→@170→@171→@172 distributed cycle?

## Visual Layout (f68r.jpg)
f68r is a **multi-panel fold-out** (3 panels: f68r1, f68r2, f68r3). The middle panel (f68r2) is an astronomical folio:
- A large circle filled with labeled stars (each star has a short label in @Ls locus)
- Inside the large circle at top: smaller circle with a MOON in the center, ring of circular text around it
- Inside the large circle at bottom: smaller circle with a SUN in the center, ring of circular text around it
- $H=4 (Hand 4), $I=A (Astronomical), Quire I

The @231-@234 sequence is in the **bottom ring** (sun circle), in the @Cc locus.

## The @231-@234 Sequence

ZL3b line f68r2.31:
```
<f68r2.31,@Cc> <!09:30>okey.okoaiin.okol.o,ky.oeeeo.r.okey.okeeol.cheo.o.@231;@232;@233;@234;
```

When tokenized by IVTFF dot convention, this gives **11 tokens**:
```
okey | okoaiin | okol | o,ky | oeeeo | r | okey | okeeol | cheo | o | @231;@232;@233;@234;
```

The entire `@231;@232;@233;@234;` is **ONE compound token** — no dot separators between the 4 @glyphs. They are concatenated without any intervening characters.

This is the final element of the circular text: standard Voynich words followed by the 4-@glyph terminus.

## Structural Comparison: f68r2 vs f57v

| Feature | f57v L03 | f68r2 L31 |
|---|---|---|
| Locus | +Cc (inner ring) | @Cc (bottom sun ring) |
| Structure | 17-token repeating cycle × 4 | Single 11-token non-repeating text |
| @glyph placement | Distributed at positions 10, 13, 14, 17 within cycle | Concatenated as one compound terminus token |
| Standard chars between @glyphs | YES (t r and y between them) | NO (all adjacent, no separators) |
| Repeating structure | YES (4 identical cycles) | NO |
| @glyphs as last element | NO (@172 ends each cycle, followed by next 'o') | YES (terminus of entire text band) |
| Total @glyphs | 4 distinct types, distributed throughout | 4 distinct types, concatenated at end |

**These are structurally DIFFERENT patterns.**

## Verdict: H027 Falsified

f68r2 is NOT a second structured @glyph cluster analogous to f57v.

**f57v pattern:** 4 @glyphs distributed at specific invariant positions within a 17-token repeating cycle — structural embedding within a controlled sequence.

**f68r2 pattern:** 4 @glyphs concatenated as a single terminus token at the end of a non-repeating circular text band — terminal annotation or end-marker.

The most plausible interpretations of `@231;@232;@233;@234;` in f68r2:
1. **End-of-ring marker:** 4 non-standard symbols the scribe used to mark the end/completion of the circular text (like a colophon)
2. **Unrecognizable glyphs:** The transcriber found 4 consecutive glyphs they couldn't assign to EVA and encoded them all as @NNN
3. **Astronomical symbols:** 4 symbols with specific astronomical meaning (seasons, directions, etc.) that don't exist in EVA

None of these interpretations requires a deliberate structural parallel to f57v.

## Manuscript-Wide Consecutive @Glyph Search

Only **3 lines** in the entire ZL3b corpus contain 2+ consecutive @NNN glyphs:

| Folio | Locus | Group | Context |
|---|---|---|---|
| f22r | +P0 | `@162;@136;` (×2) | Inside `{c'@162;@136;}` correction bracket |
| f58v | +P0 | `@191;@191;` (×2) | Inside `{@246;k@191;@191;h}` correction bracket |
| f68r2 | @Cc | `@231;@232;@233;@234;` (×4) | At terminus of circular text, no brackets |

The f22r and f58v cases both occur inside `{}` correction/uncertain brackets — they represent transcriber uncertainty about corrected glyphs, not deliberate structural placement. f68r2 is the only case of consecutive @glyphs outside a correction bracket, and it is unique in the manuscript.

## Implication

The f57v pattern (distributed @glyphs within a repeating cycle) is **unique** in the entire ZL3b corpus. f68r2's terminal concatenated @glyphs are structurally distinct and likely represent a different phenomenon. H027 is falsified.

The f57v repeating sequence remains the sole example of a structured @glyph pattern in the manuscript — making it more, not less, anomalous in the manuscript context.
