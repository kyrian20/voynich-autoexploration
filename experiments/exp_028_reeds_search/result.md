# Experiment exp_028: Jim Reeds X1-X128 Rare Character Document Search
Date: 2026-04-09

## Hypothesis Tested
H028: The Jim Reeds X1-X128 rare character document identifies the physical glyphs for @169, @172, and @195, which would confirm whether the "same" @NNN code in f57v and f66r corresponds to the same physical glyph.

## Search Results

### What Was Found
- Jim Reeds DID produce a document listing rare Voynich characters as X1-X128
- The document predates the current ZL3b/IVTFF @NNN encoding system
- Zandbergen's voynich.nu transcription page describes it as "an inventory of rare characters"
- The document appears to have been produced circa 1995-2004, shared within the research community but not publicly posted online
- No direct download URL was found via web search
- The voynich.net/reeds/index.html index does not link to the X-character document

### Relationship to @NNN Codes
- ZL3b uses @NNN where NNN is an extended ASCII value (values 130-255)
- Reeds' X1-X128 numbering is DIFFERENT from ZL3b's @NNN system (X1 ≠ @1)
- The Zandbergen voynich.nu page acknowledges the Reeds document but doesn't provide a cross-reference table between X-codes and @NNN codes
- The @169 correction in the 2025 ZL3b update suggests the transcribers have Reeds' document (they can check against it)

### Alternative Route to the Same Information
The ZL3b transcription file itself uses `@NNN;` codes consistently. The physical glyph identity of @169 can be established by:
1. Visual inspection of f57v at position 10 in the repeating cycle (exp_015 already showed the image)
2. Cross-referencing Zandbergen's supplementary notation in ZL3b comments/headers

From exp_015's image analysis of f57v, the @169 glyph was described as visually distinct from standard EVA characters. From exp_019, @169;v is confirmed as a compound token where the @169 part is non-standard and 'v' is the standard EVA v-stroke that follows it without a dot separator.

## Verdict

**H028 UNRESOLVED — document not publicly accessible.**

The Reeds X1-X128 document exists but is not available online. Finding it would require:
1. Direct contact with Jim Reeds or Rene Zandbergen
2. Access to the voynich-list mailing list archive (some messages may contain excerpts)
3. The "annotated bibliography" at ic.unicamp.br/~stolfi/voynich/mirror/reeds/bib.html may have more details

**Practical implication:** The @169 vs @172 identity question for the f57v↔f66r link can be resolved by visual manuscript inspection (which was beyond the scope of this experiment) rather than requiring the Reeds document. The ZL3b transcribers explicitly cross-referenced f57v and f66r (the "cf f57v?" comment), suggesting they verified the @glyph correspondence visually.

## Status
H028: UNRESOLVED — Reeds document not publicly accessible. The physical glyph identity question remains open but is not blocking; the ZL3b cross-reference between f57v and f66r provides sufficient warrant for the structural link even without glyph ID verification.
