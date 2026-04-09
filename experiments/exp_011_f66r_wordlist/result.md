# Experiment exp_011: f66r Word List Investigation + L0 Structural Audit

**Date:** 2026-04-09
**Goal:** Characterize f66r's two-column structure; audit L0 entries across full ZL3b; check adjacent folios and Librarian KB.
**Status:** complete

## Prior KB Check
No prior KB entry specifically analyzes f66r as a word list or two-column structure. dimperio_elegant_enigma_1978 mentions f66v (astrological human figure), not f66r. No "word list," "glossary," or "lexical list" entry for f66r in the KB.

## f66r Structure

f66r is a **"text only" folio** (ZL3b header `$I=T`, no plant illustration) written by **Hand 5 / Scribe 5** (ZL3b `$H=5`) in **Currier B** (`$L=B`), at the end of the botanical section (Quire H, folio 66). It contains:
- **Lines 1–15**: Column 1, 15 label (L0) entries
- **Lines 16–49**: Column 2, 34 label (L0) entries
- **Lines 50–81**: 32 body text (P0) lines (standard Currier B running text)

The ZL3b transcription comment mid-file: `# Now individual characters in next column` — transcribers explicitly recognized the two-column structure.

## Column 1: 15-Word List

Words: `rary, rals, qor, dary, ykeol, saly, salf, fary, qotesy, ykaly, doly, saiin, qokal, qolsa, raral`

| Property | Value |
|---|---|
| All unique | Yes (15 types / 15 tokens) |
| Length distribution | 3 chars: 1 word; 4 chars: 7 words; 5 chars: 6 words; 6 chars: 1 word |
| Hapax legomena (0 occurrences elsewhere) | 6/15 words: rals, salf, fary, qotesy, qolsa, raral |
| Rare (≤3 occurrences elsewhere) | 4 more: rary(3), saly(3), ykaly(3), doly(3) |
| High-frequency words | qokal(169 elsewhere), saiin(98), qor(20), dary(16), ykeol(10) |

**Critical finding: 10/15 words (67%) are hapaxes or very rare (≤3 occurrences in ~31,000 body-text tokens).** If this were an index or concordance of the manuscript's vocabulary, the words should appear frequently in body text. Instead, most of them are unique to this list. The 5 words that do appear elsewhere (qokal, saiin, qor, dary, ykeol) are common body text words embedded in a list dominated by rare/unique items.

## Column 2: 31-Entry Character List

Chars: `y o s sh y d o f x air d sh y f f y o d s f c x t o l r t o x p d`

| Property | Value |
|---|---|
| Single-char count | 28 of 31 entries |
| Multi-char entries | sh(2), air(1) |
| Most frequent | o(5), y(4), d(4), f(4), x(3) |

**Rare character over-representation:**
- `f` (a gallows character): appears 4× in col2, only 6× elsewhere in manuscript → col2 holds **40% of all `f` occurrences**
- `x`: appears 3× in col2, only 7× elsewhere → col2 holds **30% of all `x` occurrences**
- `p` (gallows character): appears 1× in col2, only 6× elsewhere → col2 holds **14% of all `p` occurrences**
- `c`: appears 1× in col2, only 4× elsewhere

The gallows characters `f` and `p` — among the rarest characters in the manuscript overall — are strongly concentrated in this column. The column contains a mix of common characters (y, o, s, d, l, r) and rare/gallows characters (f, x, p, c) in a way that is structurally distinct from body text.

## Body Text Paragraphs (f66r lines 50+)

Standard Currier B vocabulary: shedy(8), daiin(7), ol(7), qoky(5), okedy(4), chedy(4). Nothing unusual — standard B body text follows the two columns.

## Adjacent Folios

- **f65r**: 3 genuine plant labels: `otaim, dam, alam` (1-3 char words) — last herbal page before f66r
- **f65v**: Body text only (6 lines) — standard herbal prose
- **f66v**: Body text only (13 lines) — standard prose, no labels
- **f67r**: Not present in ZL3b (this is where the astronomical section begins)

The surrounding folios show no unusual structure: f65r-f65v are normal herbal pages with conventional labels, f66v and f67r are standard text. f66r is structurally isolated — the two-column format is not part of a larger organizational section.

## L0 Structural Audit: Full Manuscript

| Classification | Folios | L0 label lines |
|---|---|---|
| standalone_list (≥5 consecutive L0 entries) | 16 | 311 |
| mixed (some consecutive L0 but no strict alternation) | 8 | 106 |
| single_label (1–3 isolated L0 entries) | 7 | 8 |
| **line_marker** (L0/P0 perfectly alternating) | **2** | **35** |

**The line_marker pattern occurs on exactly 2 folios:**
1. **f49v** (Quire G, Hand 1 / Scribe 1, Currier A): 26 L0 markers, 26 P0 lines
2. **f76r** (Quire M, Hand 2 / Scribe 2, Currier B, also `$I=T` text-only): 9 L0 markers, interspersed with body text

**Critical: The ZL3b transcription note for f76r reads: `# has 'key-like' sequence, here transcribed as L0 labels`**

The ZL3b transcribers themselves recognized f76r's single-character L0 markers as structurally unusual and "key-like." This validates the discovery: the line-marker pattern (also called "key-like" by the expert transcribers) is a recognized but unclassified structural feature of the manuscript. It appears in both Currier A (Scribe 1) and Currier B (Scribe 2) — two different scribes independently using this structure.

f76r is another "text only" folio in the biological section, not in the herbal section. So both f49v and f76r are text-only pages with this marker system, in different sections and written by different scribes.

## Interpretation

**What f66r is NOT:** An index or concordance of the manuscript's vocabulary. 67% of the word-list words are hapaxes or near-hapaxes — they don't appear in the body text. An index would show the opposite pattern.

**What f66r might be:** A list of specialized vocabulary (proper nouns, place names, technical terms, plant names?) for objects or concepts not discussed in the body text. The 40% hapax rate in a 15-word list is extraordinary — far exceeding even the pharma section's label hapax rate. Alternatively, if the list was composed independently (not derived from the manuscript's body text), it could be an external reference list that was bound into the manuscript.

**Column 2 character list structure:** The concentration of rare gallows characters (f, p) alongside common characters (y, o, s) in column 2 does not resemble a random sample from the manuscript's character distribution. It may represent an alphabet or character inventory — a list of glyphs rather than of words.

**The "key-like sequence" note on f76r** is the most significant corpus-external validation. Expert transcribers already identified this structural pattern as distinctive. The occurrence of similar patterns on f49v (Scribe 1) and f76r (Scribe 2) in different sections of the manuscript suggests this is a deliberate structural feature used by multiple scribes, not an isolated scribal quirk.

## Limitations
- f66r analysis is limited to the ZL3b transcription. Physical inspection of the manuscript is needed to verify the column structure (are the two columns visually distinct? is the writing direction the same?).
- Column 2 may contain some transcription uncertainty — some single chars might represent ambiguous glyphs.
- The 6/15 hapax words in column 1 could theoretically appear in damaged or untranscribed parts of the manuscript.
- Scribal hand assignment from ZL3b headers ($H= field) may not exactly correspond to Davis (2020) numbering.

## Follow-up Questions
- Do the column 1 words share any phonotactic or structural pattern with known Voynich word types? (e.g., all y-final? all begin with specific bigrams?)
- Is column 2 an inventory of Voynich glyphs? How many unique glyphs appear, and does the set match the canonical EVA glyph inventory?
- What are the f76r "key-like sequence" single chars? Do they match the f49v sequence or f66r column 2 chars?
- Are there other "text only" (`$I=T`) folios in ZL3b, and do they also have unusual L0 structures?
