# Experiment exp_018: @Glyph Prior Work Check
Date: 2026-04-09

## Method
1. Searched all KB summaries (~50 papers) for: non-standard glyph, rare glyph, @169, @172, key-like, picnic table, EVA exception, f57v/f66r/f49v/f76r margin sequences
2. Read full content of zandbergen_transcr.md and zandbergen_eva_transcription.md
3. Fetched voynich.nu pages: writing.html, transcr.html, folios.html, q07/index.html (f49v), q08/index.html (f57v)

## What the @NNN Notation Actually Is

From `zandbergen_transcr.md` (zandbergen_eva_transcription source):
> "While defining the alphabet, individual rare characters, or rare parts of ligatures, were assigned a 'high ASCII' code, and the way to include them into transliteration files is defined as follows: @185; for ascii code 185."

**@NNN codes = extended ASCII code values.** The codes are not arbitrary enumeration — they correspond to specific positions in the extended ASCII/ISO-8859-1 table:
- @169 = ASCII 169 (© in ISO-8859-1)
- @172 = ASCII 172 (¬ in ISO-8859-1)
- @195 = ASCII 195 (Ã in ISO-8859-1)

The extended ASCII interpretation may be the original assignment method (e.g., using a high-ASCII font slot to encode the glyph in the original transliteration system), but the actual glyph these codes represent is a specific non-standard Voynich character.

## 2025 ZL3b Correction Involving @169

From `zandbergen_transcr.md`:
> "2025 corrections: removed spurious f89v2 label (shine-through); removed 3 f1r loci identified as Marci additions; **corrected Eva high-ASCII @169; added 3 new codes (221–223)**."

The @169 code was explicitly corrected in 2025 — the version we're using (ZL3b, dated 2025-05-13) should contain this correction. This suggests @169 had an encoding issue in earlier versions. The nature of the correction (wrong glyph assigned to this code, or wrong occurrences) is not specified in the KB. **This is potentially important: our analysis of @169 is based on the corrected 2025 version, but any earlier work using the pre-2025 ZL may have had different @169 occurrences.**

## What Voynich.nu Says About Key-Like Sequences (writing.html)

From fetched writing.html:
> "Sequences of single characters or short words appear in circular designs and page margins, termed 'key-like sequences.' These are catalogued in the document's overview table with the keyword 'SEQ'."

**All four cluster folios are explicitly documented as having 'SEQ' features:**

| Folio | Description on voynich.nu writing.html |
|---|---|
| **f49v** | "A vertical sequence of single characters in Voynich script in the left margin, aligned with and just before each line of writing, accompanied by numerals 1-5." |
| **f57v** | "A circular diagram with several sequences of words and characters integrated in this figure." |
| **f66r** | "Sequences of words and characters in the left margin" and writing near a reclining figure. |
| **f76r** | "A vertical sequence of single characters in Voynich script in the left margin." |

**This is confirmed prior work** — Zandbergen has catalogued all four folios as having key-like sequences (SEQ keyword). The features are acknowledged in the literature but not systematically analyzed.

## What Voynich.nu Says About f57v Specifically (q08/index.html)

> "The four times repeating sequence in the second ring from the outside has **4 × 17 characters**. Only in some individual places the repeated characters are not identical."

> "Many special characters that otherwise occur only rarely, making it linguistically distinctive within the manuscript."

> "An additional 'symbol' in the lower right corner of the page, that is not Voynichese writing and also does not look like a quire mark," which "potentially read[s] '17th'."

**Note on count discrepancy:** voynich.nu says 4 × 17 characters; our analysis of ZL3b shows 18 tokens per cycle. The discrepancy may arise from treating `@169;v` as a compound (ligature) = 1 character rather than 2 separate tokens. If @169 is a ligature that includes the following 'v', then the true cycle length is 17. This is consistent with the @169 code representing a compound/ligature glyph.

## What Voynich.nu Says About f49v (q07/index.html)

> "26 stand-alone Voynich characters (labels)... Most of the Voynichese characters in the sequence on the left are the common set, but there are **a few rare ones** as well."

> "The numbers 1-5 written to the left of lines 2-6."

This confirms:
1. 26 markers (matching our count exactly)
2. The @SPECIAL glyphs are acknowledged as "rare characters"
3. There are Latin numerals 1-5 accompanying the margin sequence — these may be additional annotations (possibly written by a different hand) not captured as @SPECIAL in ZL3b

## KB Search Results

Only 4 KB entries contain relevant terms:

1. **zandbergen_eva_transcription.md**: Documents the @NNN notation system — "extended via @code notation for rare glyphs"
2. **zandbergen_transcr.md**: Documents the 2025 correction to @169; confirms EVA @NNN = ASCII code values
3. **zandbergen_writing.md**: Mentions "rare characters" concentrating on specific pages; asks what f49v margin sequences represent
4. **guy_statistical_1991.md**: Reference to "anomalous character-level statistics" — unrelated

**No KB entry specifically:**
- Analyzes the @169/@172 cross-folio or cross-scribe connection
- Studies the f57v repeating sequence beyond noting it exists
- Examines the f57v↔f66r structural relationship
- Provides an enumeration of what specific @NNN codes represent as manuscript glyphs

## The "Jim Reeds X1-X128 Document" — Critical Reference

From the transcription page fetch:
> "Jim Reeds produced a document with an overview of these rare characters, calling them 'X1' to 'X128'."

This document would enumerate the rare/extended EVA characters systematically. It is NOT in the KB registry and has not been located. If it were available, it would identify what manuscript glyphs correspond to @169, @172, @195, etc.

## Key Finding: "Key-like" Is a Zandbergen Term of Art

The four-folio cluster is acknowledged in Zandbergen's writing system analysis under the 'SEQ' keyword. This means:
1. The "key-like sequence" designation is not our discovery — Zandbergen coined it
2. Zandbergen recognizes both f49v and f76r as having the same structure ("vertical sequence of single characters in the left margin")
3. The features have been documented but not quantitatively analyzed in any KB source

## What Has NOT Been Done Before (Confirmed Novel Work)

The following are absent from all KB sources and voynich.nu pages fetched:

1. **@169/@172 cross-hand analysis:** No source notes that @169 and @172 are the widest-spanning cross-scribe shared @glyphs in the manuscript (Hand 1↔Hand 5).

2. **f57v repeating sequence structural analysis:** voynich.nu notes it exists (4×17 chars) but does not break down which positions vary, what the variant characters are, or what the @glyph cluster @169→@170→@171→@172 means structurally.

3. **The @glyph cluster as an ordered 4-tuple:** No source identifies @169→@170→@171→@172 as a fixed-order group.

4. **f57v↔f66r shared @glyph analysis:** voynich.nu cross-references these folios ("cf f57v?" in ZL3b) but no source quantifies the overlap or analyzes what it means.

5. **Manuscript-wide @glyph census:** The distribution of all 63 @glyph types across 64 folios has not been computed in any KB source.

## The "17th" Symbol Mystery

The voynich.nu description says the Saturn symbol in the f57v lower right corner "potentially reads '17th'." This is the @255; symbol in ZL3b. Combined with the "4×17 characters" description, the number 17 may have structural significance for f57v — possibly indicating the cycle length (17 characters per repeating unit if @169;v is a compound) or a dating marker ("17th" century? calendar reference?).

## Summary

Prior work acknowledges the four cluster folios as having 'SEQ' (key-like sequence) features. The f57v repeating sequence is noted as "4×17 characters with some individual variation." @NNN notation is documented as EVA extended ASCII. The 2025 ZL correction modified @169. No prior work performs: cross-folio @glyph census, @169/@172 cross-hand analysis, positional analysis of the f57v repeating sequence variants, or characterization of @169→@172 as a fixed-order 4-tuple.
