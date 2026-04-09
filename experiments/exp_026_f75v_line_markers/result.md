# Experiment exp_026: f75v Line Marker Analysis
Date: 2026-04-09

## Key Metadata

f75v: `$Q=M $P=B $F=a $B=1 $I=B $L=B $H=2 $C=2`
- **Hand 2** (same as f76r)
- Currier B
- Biological section
- ZL3b comment: **"last character in first 5 lines aligned vertically reading slors"**

f76r: also Hand 2, Currier B, biological section.

**f75v and f76r share the same scribe (Hand 2).**

## Marker Sequence

f75v has **6 L0 entries** in 6 lines (L2, L4, L6, L8, L9, L11):

| Marker line | Locus | Content | → Body line | Body first char |
|---|---|---|---|---|
| L2 | =L0 | **s** | L3 | s |
| L4 | =L0 | **l** | L5 | d |
| L6 | =L0 | **l** | L7 | q |
| L8 | ~L0 | **o** | L10 | q |
| L9 | +L0 | **r** | L10 | q |
| L11 | =L0 | **s** | L12 | q |

Full sequence: **s, l, l, o, r, s**

**Note on ZL3b transcriber's "slors"**: Lines L8 and L9 are both L0 entries preceding the same body text line (L10). The transcribers counted this as a single 4th-position marker "or" — reading s + l + [or] + s = "slors" (5 positions with 'or' as a compound marker). The actual L0 entry count is 6. This is the only case in the three known line-marker folios where two consecutive L0 entries map to the same body line.

## Sequence Comparison

| Folio | Hand | Currier | Section | Sequence | Unique chars |
|---|---|---|---|---|---|
| f49v | 1 | A | herbal_A | f o r y e @140 k s p o @192 y e @140 @164 p o y e d y k @243 @140 @192 [?] | 13 |
| f75v | **2** | B | **bio** | **s l l o r s** | **4** |
| f76r | **2** | B | **bio** | s d q s o l k r s | 7 |

**f75v character set {l, o, r, s} is a proper subset of f76r's character set {d, k, l, o, q, r, s}.**

All 4 chars in f75v also appear in f76r. The 3 chars in f76r but not f75v are: d, k, q.

## Structural Findings

**1. Same-scribe, same-section line-marker system:** f75v and f76r are by Hand 2, in the biological section. A single scribe (Hand 2) created line-marker sequences on two biological folios. The characters used across both folios are {d, k, l, o, q, r, s} — all standard EVA chars, no @SPECIAL glyphs.

**2. f75v is a proper subset of f76r:** {l, o, r, s} ⊆ {d, k, l, o, q, r, s}. f75v uses only 4 of the 7 chars in f76r. If both sequences draw from a common inventory, f75v's sequence covers roughly half of it.

**3. Repeated characters in f75v:** 'l' appears at L4 AND L6 (twice). 's' appears at L2 AND L11. Repetitions are permitted — the sequence is NOT an inventory of distinct characters.

**4. Two markers for one body line (L8+L9 → L10):** f75v has the unique feature of two consecutive L0 entries ('o' and 'r') both preceding the same body text line. The ZL3b transcribers read this as "or" — a compound marker. No similar compound marker appears in f49v or f76r.

**5. Body correspondence: 16.7% (1/6) vs 9.2% expected.** The single match is the first pair (marker='s', body first char='s'). The 5 other pairs do not correspond. Similar to f49v and f76r (which also showed near-chance body correspondence), the markers do not function as first-char catchwords.

## Implications

1. **Three-folio line-marker system confirmed with scribal structure:** f49v (Hand 1/Currier A/herbal) + f75v (Hand 2/Currier B/bio) + f76r (Hand 2/Currier B/bio). The Hand 2 bio section folios form a sub-cluster within the line-marker group.

2. **The Hand 2 marker characters {d,k,l,o,q,r,s} vs Hand 1 marker characters {f,o,r,y,e,@SPECIAL,k,s,p,d,y} show partial overlap** ({d,k,o,r,s} shared) — consistent with both scribes drawing from a shared repertoire but with different selections.

3. **Whether f75v and f76r form a sequence pair** (like the two columns of f66r) is a testable hypothesis: are the 6 f75v markers and 9 f76r markers parts of a longer sequence? The combined sequence would be 15 markers: {s,l,l,o,r,s} + {s,d,q,s,o,l,k,r,s}. The total char set is {d,k,l,o,q,r,s} — a 7-element EVA subset without any @SPECIAL glyphs.

## New Hypothesis Generated
H030: f75v and f76r line-marker sequences are parts of a longer Hand 2 sequence. The f75v sequence (s,l,l,o,r,s) and f76r sequence (s,d,q,s,o,l,k,r,s) share all 4 f75v chars; if concatenated or otherwise combined, they might form a more complete underlying sequence. The combined set {d,k,l,o,q,r,s} is exactly 7 chars — the same number as f57v's 17-token cycle has invariant positions in specific character slots.

## Updated F033

F033 now corrected: f75v has 6 L0 markers (not 5 as initially stated in exp_022), with the sequence s,l,l,o,r,s. The 'o' and 'r' markers at L8/L9 both precede the same body line (L10) — a compound marker 'or' in ZL3b transcriber's reading.
