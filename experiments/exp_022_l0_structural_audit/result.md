# Experiment exp_022: ZL3b L0 Structural Audit
Date: 2026-04-09

## Hypothesis Tested
H021: Classify all ZL3b L0 locus entries into structural types (true label, line marker, list entry), identify other folios with unusual L0 structures, and produce a cleaned label corpus.

## Scope Correction: L0 Is One of Many Label Locus Codes

ZL3b has multiple label-type locus codes beyond L0:

| Locus | Approx. Count | Likely Meaning |
|---|---|---|
| L0 (all prefixes) | 160 | Generic label / object label |
| Lf (all prefixes) | ~193 | Figure/pharmaceutical labels |
| Lz (all prefixes) | ~299 | Zodiac labels? |
| Ls (all prefixes) | ~75 | Label short |
| Lc (all prefixes) | ~40 | Circular label |
| Ln (all prefixes) | ~33 | Label near |
| Lt (all prefixes) | ~20 | Label text |
| Other (La, Lp, Lx) | ~10 | Miscellaneous |

**Implication:** exp_003's "label corpus" of ~1065 tokens almost certainly combined multiple L* locus codes, not just L0. The present audit covers L0 only (160 entries). A complete label classification requires auditing all L* variants.

## L0 Classification Results

| Type | Count | % |
|---|---|---|
| LINE_MARKER (L0 immediately precedes P0) | 43 | 26.9% |
| LIST_ENTRY (L0 adjacent to other L0s, no interspersed P0) | 108 | 67.5% |
| TRUE_LABEL (standalone L0) | **9** | **5.6%** |

**Of 160 L0 entries, only 9 (5.6%) are unambiguous object labels.**

## LINE_MARKER Folios

| Folio | Section | Markers | Notes |
|---|---|---|---|
| f49v | herbal_A* | **26** | Confirmed: perfectly alternating L0/P0 (exp_011) |
| f76r | bio | **9** | Confirmed: "key-like" sequence (exp_013) |
| **f75v** | **bio** | **5** | **NEW: third line-marker folio** |
| f66r | astro* | 1 | Terminal entry after list (probably closing marker) |
| f11v | herbal_A | 1 | Single case: 'dd' — may be misclassified |
| f67r2 | cosmo | 1 | Single case: 'oran' — may be misclassified |

*ZL3b section assignment (f49v folio-level) differs from section heuristic above.

### f75v — NEW Line-Marker Folio

f75v has 5 L0/P0 pairs at lines 2, 4, 6, 9, 11:
```
L2: 's' → *P0
L4: 'l' → *P0
L6: 'l' → *P0
L9: 'r' → *P0
L11: 's' → *P0
```
Markers: s, l, l, r, s — a 5-element sequence using only standard EVA chars.

**This is the third folio with a line-marker structure.** f75v is biological section, same as f76r. f75v was not previously identified as anomalous.

### Line-Marker Sequence Summary

| Folio | Section | Count | Sequence (partial) |
|---|---|---|---|
| f49v | herbal_A | 26 | f o r y e @140 k s p o @192 y e @140 @164 p o y e d y k @243 @140 @192 [?] |
| f76r | bio | 9 | s d q s o l k r s |
| f75v | bio | 5 | s l l r s |

**Note:** f75v and f76r are both in the biological section, both have short sequences, and both start with 's'. f75v's 5-char sequence {s, l, r} is almost entirely contained within f76r's 9-char sequence {s, d, q, s, o, l, k, r, s}.

## LIST_ENTRY Folios

| Folio | Section | Entries | Notes |
|---|---|---|---|
| f66r | astro | 48 | Known two-column list (exp_011) |
| f69r | cosmo | 22 | **NEW: large cosmo label list** |
| f67r2 | cosmo | 19 | **NEW: large cosmo label list** |
| f67v1 | cosmo | 12 | **NEW: large cosmo label list** |
| f57v | astro | 4 | 3 text-locus L0 entries + 1 (cosmological ring labels) |
| f68v3 | cosmo | 2 | Small list block |
| f75v | bio | 1 | Single adjacent-L0 entry in marker context |

**The cosmo section (f67r2, f67v1, f69r) has extensive L0 list blocks totaling 53 entries — not previously characterized.**

## TRUE_LABEL Entries

Only 9 standalone L0 TRUE_LABEL entries in the entire manuscript:

| Folio | Section | Content |
|---|---|---|
| f2r | herbal_A | 'ios an on' |
| f57v | astro | 1 entry |
| f67r2 | cosmo | 7 entries (ykshy, aram, dolchsody, okal, okain, opcholdy, ofar, oeoldan, ytoaiin, yfain) |

After excluding f49v and f66r (known problematic), herbal_A has only 1 TRUE_LABEL entry: f2r ('ios an on' — 3 tokens). **The herbal_A "label corpus" essentially does not exist in L0.**

## Implications

1. **Prior exp_003 label analysis used a multi-L* corpus.** The 1065 "label tokens" combined L0, Lf, Ls, Lz, Lc, and other locus codes. The structural contamination finding (X007) applies specifically to L0; the Lf/Lz/Ls entries may or may not have the same problem and need separate auditing.

2. **f75v is a third line-marker folio.** All three line-marker folios (f49v, f75v, f76r) have biological or herbal content. f75v was not previously in the structural anomaly group. Its 5-marker sequence overlaps with f76r's sequence.

3. **Cosmo section has extensive L0 list blocks (f67r2, f67v1, f69r).** These 53 entries are visually the labels on the circular zodiac/cosmo diagrams — probably genuine label content but in list format due to diagram structure.

4. **True L0 object labels are extremely rare (9 total).** The L0 locus is not primarily an object-label locus in ZL3b — it is primarily a list/structure locus.

## New Findings Generated
- F033: f75v is a third line-marker folio with 5 L0/P0 pairs (s, l, l, r, s). The biological section has two line-marker folios (f75v, f76r), both starting with 's', with f75v's sequence nearly contained in f76r's.
- F034: ZL3b's L0 locus contains only 9 unambiguous object labels out of 160 L0 entries (5.6%). 67.5% are list entries and 26.9% are line markers. The majority of Voynich "label text" is in other L* locus codes (Lf, Lz, Ls, Lc, Ln, Lt) not audited here.

## Updated H021 Status
**TESTED — PARTIALLY COMPLETE.** L0 classification done. Remaining: audit of Lf, Ls, Lz, Lc, Ln, Lt locus codes to characterize the full label corpus and determine whether contamination from line-markers or lists exists in those categories.
