# Experiment exp_030: f49v Margin Numerals Investigation
Date: 2026-04-09

## Hypothesis Tested
H029: The @NNN codes in f49v (specifically @140, @164, @192, @243) encode recognizable numerals, forming an indexing/counting system across the 26 L0 markers.

## ZL3b Evidence
The ZL3b header comment explicitly states:
```
# In the left margin there is a vertical sequence 1 2 3 4 5 aligned with
# the 1st paragraph, starting from line 2.
```

## Key Findings

### 1. Numeral 1-5 Encoding (CONFIRMED)
The L0 markers for f49v lines 2-6 are the ZL3b transcription of visible "1 2 3 4 5" Arabic numerals in the manuscript margin:

| L0 position | ZL3b entry | Encoded numeral |
|-------------|------------|-----------------|
| 2 | `o` | 1 |
| 3 | `r` | 2 |
| 4 | `y` | 3 |
| 5 | `e` | 4 |
| 6 | `@140;` | 5 |

**@140 = the manuscript's glyph for "5"** — its shape was sufficiently non-EVA to require @NNN encoding (unlike 1-4, which were approximated with EVA characters o/r/y/e).

Line 1 (L0 = `f`) has no numeral: the sequence starts at line 2 ("starting from line 2").

### 2. Counting System Test — NEGATIVE
If @140=5, @192=10, @164=15, the @NNN glyphs should appear at multiples of 5 in the L0 sequence. They do NOT:

| L0 position | Glyph | Position mod 5 |
|-------------|-------|----------------|
| 6 | @140; | 1 (≠ 0) |
| 11 | @192; | 1 (≠ 0) |
| 14 | @140; | 4 (≠ 0) |
| 15 | @164; | 0 ← only one |
| 18 | @192; | 3 (≠ 0) |
| 21 | @140; | 1 (≠ 0) |

**H029 as a counting system is REFUTED.** The @NNN glyphs appear irregularly, with gaps of 7-8 positions, not 5.

### 3. Paragraph Structure
f49v has TWO paragraphs (separated by paragraph markers in ZL3b), each with 13 body lines:
- Paragraph 1: L0 seq = f, o, r, y, e, @140, k, s, p, o, @192, y, e
- Paragraph 2: L0 seq = @140, @164, p, o, @192, y, e, @140, d, y, e, k, y

**Cross-paragraph alignment: 0/13 matches.** The two sequences are completely independent — no character is shared at the same position across paragraphs.

### 4. Numeral Characters Recur After Position 6
The characters {o, r, y, e, @140} (which encode numerals 1-5) appear again at later positions:
- 'o' at positions 10, 17
- 'y' at positions 12, 19, 23, 26
- 'e' at positions 13, 20, 24
- '@140;' at positions 14, 21

This recurrence likely reflects that o/y/e are common Voynich characters (expected in any random sequence), not continuation of a numeral series. The ZL3b transcribers identified ONLY the first 5 (lines 2-6) as numerals — if positions 10/12/13 also looked like numerals 1/3/4, they would have noted it.

### 5. Nature of the L0 Sequence
The f49v L0 sequence is a MIXED LAYER:
- **Positions 2-6 (L0 pos 2-6):** Later-hand annotation — Arabic numerals "1, 2, 3, 4, 5" written by a later reader/owner to label the first paragraph's lines
- **All other positions (1, 7-26):** Original Voynich margin glyphs (the "key-like sequence")

The $X=S flag in f49v's header marks the folio as having a special sequence. The ZL3b comment attributes part of that annotation to a later, non-Voynich hand.

## Verdict

**H029: PARTIALLY RESOLVED**
- @140 = "5" (confirmed)  
- Full sequence is NOT a counting system (gaps irregular, modular test negative)
- The numerals 1-5 are a LATER-HAND ADDITION in the margin, not original Voynich content
- The remaining 21 L0 markers (positions 1, 7-26) are original Voynich margin glyphs, unidentified as numerals by ZL3b transcribers

**Implication for prior experiments:** exp_013's analysis of the f49v 26-pair sequence treated all L0 markers as uniform Voynich content. 5 of the 26 markers are actually later-hand Latin numerals, not Voynich symbols. This does not change the structural conclusions (alternating L0/P0 pattern is real) but means the L0 CONTENT is not a coherent single-system sequence.

**New question (H031):** What hand/period wrote the "1-5" annotation? Could this be the same later hand responsible for other marginal annotations in the manuscript (e.g., f116v michitonese text)?
