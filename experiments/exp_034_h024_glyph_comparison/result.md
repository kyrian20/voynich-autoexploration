# Experiment exp_034: f49v @SPECIAL Glyph vs f57v @NNN Comparison (H024)
Date: 2026-04-09

## Hypothesis Tested
H024: f49v's @SPECIAL glyphs in L0 margin markers (@140, @192, @164, @243) are the same physical glyphs as f57v's cosmological wheel special characters (@169, @170, @171, @172).

## ZL3b Evidence

**f49v @NNN codes (all occurrences):**
- @140; at L0 positions 6, 14, 21 (identified by exp_030 as the numeral "5")
- @192; at L0 positions 11, 18
- @164; at L0 position 15
- @243; in body text (P0 line 46): inside "oaiin.cheky.@243;.cho..."

**f57v @NNN codes (repeating cycle):**
- @169;v at cycle position 10 (4 repetitions)
- @170; at cycle position 13 (4 repetitions)
- @171; at cycle position 14 (4 repetitions)
- @172; at cycle position 17 (4 repetitions)
- @255; (lower right corner symbol, not in the cycle)

**Intersection: ZERO**
f49v = {140, 192, 164, 243}
f57v = {169, 170, 171, 172, 255}

These sets are completely disjoint. The ZL3b transcribers assigned distinct @NNN codes to each folio's special glyphs — since @NNN encodes unique physical glyph identities, no glyph is shared between f49v and f57v.

## Additional Context from exp_030
@140 (the most frequent f49v @NNN glyph, appearing 3× in L0 positions) was identified as the **numeral "5"** — a later-hand Arabic numeral annotation. The f49v @NNN codes in the margin (L0 entries) are part of a later-hand numeral annotation layer (numerals 1-5 at lines 2-6), not original Voynich special glyphs.

This sharply distinguishes f49v from f57v: f57v's @169-@172 are original Voynich glyphs in a structured cosmological diagram; f49v's @140/192/164 in the L0 margin are later-hand numerals added by a reader.

## Key Comparison

| Feature | f49v margin (@NNN) | f57v cycle (@NNN) |
|---------|-------------------|-------------------|
| Folio type | Herbal (Hand 1, Currier A) | Cosmo wheel (Hand 1, Currier A) |
| @NNN codes | @140, @192, @164, @243 | @169, @170, @171, @172 |
| Shared with other folios | @169/@172 shared with f66r | None shared with f49v |
| Origin | Later-hand annotation (numerals) | Original Voynich content |
| Locus context | L0 margin markers | Cc (circular text) |

## Verdict
**H024: REFUTED**

f49v and f57v share ZERO @NNN codes. The glyphs are physically different (ZL3b would assign the same @NNN if they were the same glyph). Moreover, f49v's margin @NNN codes are now understood as later-hand Arabic numerals, not original Voynich special characters. The "key-like sequence" characterization of f49v (exp_013) refers to the alternating L0/P0 pattern, not to shared content with f57v's cosmological wheel.

The structural cluster {f49v, f57v, f66r, f76r} identified in exp_013/014 rests on the LINE_MARKER pattern and the ZL3b "SEQ" keyword, not on shared @NNN glyphs. The @NNN connections within this cluster are: f57v↔f66r (share @169/@172), but f49v is isolated from both at the @NNN level.
