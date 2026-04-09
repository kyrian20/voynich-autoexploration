# Experiment exp_016: Manuscript-Wide @Glyph Census
Date: 2026-04-09

## Summary Statistics

| Metric | Value |
|---|---|
| Total manuscript words | 37,676 |
| Total @glyph occurrences | 114 |
| @glyph fraction | 0.303% of words |
| Distinct @glyph types | 63 |
| Folios with ≥1 @glyph | 64 (of ~240 total folios) |
| Single-folio @glyphs | 44 (70% of types) |
| Multi-folio @glyphs | 19 (30% of types) |

@glyphs are rare: 0.3% of the manuscript. Most are hapaxes or nearly so. The manuscript's text is 99.7% standard EVA.

## Most Frequent @Glyphs

| Glyph | Count | Folios |
|---|---|---|
| @172 | 6 | f57v(5), f66r(1) |
| @175 | 6 | f111r(2), f112v(1), f76v(1), f86v3(2) |
| @169 | 5 | f57v(4), f66r(1) |
| @170 | 5 | f57v(5) |
| @171 | 5 | f57v(5) |
| @192 | 4 | f1r(1), f49v(2), f72r3(1) |
| @140 | 4 | f18v(1), f49v(3) |
| @206 | 4 | f104v(2), f113v(1), f78r(1) |

The most frequent @glyphs are dominated by f57v's repeating sequence (@169-@172, each ×4-5 from the 4-cycle repeat).

## Critical Correction to Earlier Analysis (F029)

**F029 and the exp_013 report incorrectly stated** that "f49v has 6/26 @SPECIAL glyphs identical to those in f66r col2 and f57v circular text." This was an artifact of exp_013's normalization of all @NNN to "@SPECIAL" — masking the actual glyph IDs.

**Actual f49v @glyphs:**
- @140 ×3, @164 ×1, @192 ×2, @243 ×1 (total: 7 tokens, but 6 were in L0 markers)

**f57v @glyphs:** @169, @170, @171, @172

**f66r @glyphs:** @169, @172, @195

**f49v shares NO @glyph IDs with f57v or f66r.** The "cluster" connection via @NNN is only between f57v and f66r. The f49v connection to the cluster is structural (line-marker designation, "key-like" grouping) not via shared non-standard glyphs.

**f76r @glyphs:** @174 ×1 (unique to f76r — appears nowhere else).

## Cluster Folio Breakdown

| Folio | Hand | Total @glyphs | @glyph types | Shared with others |
|---|---|---|---|---|
| f49v | 1 | 7 | @140, @164, @192, @243 | @140(f18v), @192(f1r,f72r3), @243(f19r,f20r) |
| f57v | 1 | 19 | @169, @170, @171, @172 | @169/@172 with f66r only |
| f66r | 5 | 3 | @169, @172, @195 | @169/@172 with f57v only |
| f76r | 2 | 1 | @174 | none (singleton) |

## The @169/@172 Cross-Scribe Link

@169 and @172 are the ONLY @glyphs shared between:
- A Hand 1 folio (f57v) — the cosmological wheel
- A Hand 5 folio (f66r) — the pharmaceutical word-list

Hands 1 and 5 are otherwise in different sections of the manuscript. This cross-hand sharing is notable: of the 19 multi-folio @glyphs, most are shared within the same hand or adjacent hands. @169 and @172 cross from Hand 1 to Hand 5 — the furthest hand-span of any multi-folio @glyph.

@170 and @171 appear ONLY on f57v (Hand 1). They are the "middle" members of the f57v 4-glyph ordered cluster — f66r samples the first and last (@169, @172) but not the middle two.

## Hand Distribution

| Hand | @glyph occurrences | % | Distinct types |
|---|---|---|---|
| Hand 1 | 63 | 55.3% | 37 |
| Hand 2 | 20 | 17.5% | 16 |
| Hand 3 | 15 | 13.2% | 11 |
| Hand 4 | 13 | 11.4% | 11 |
| Hand 5 | 3 | 2.6% | 3 |

Hand 1 dominates @glyph use (55% of occurrences, 37 distinct types). Hand 5 has only 3 @glyph tokens across all its folios — and all 3 are on f66r. This makes f66r's @glyphs (and specifically @169 and @172 shared with f57v) all the more striking: Hand 5 almost never uses @glyphs.

## @Glyph Distribution Across Manuscript

Most @glyphs are isolated events: 44 of 63 types appear on only one folio (70% singleton rate). The "hapax-like" character of @glyphs suggests they represent:
(a) Rare glyphs that the scribe seldom needed
(b) Corrections or emendations that used a special notation
(c) Non-Voynich symbols (like the Saturn @255; on f57v) that required special notation

**f57v is the most @glyph-dense folio in the manuscript:** 19 occurrences vs. the next most @glyph-rich folios:
- f68r2: 5 (Hand 4, @231-@234 — 4 distinct consecutive @glyphs in one line, possibly a related sequence)
- f49v: 7 (Hand 1)
- f19r: 3, f78r: 3, f104v: 3, f66r: 3

**f68r2 is a new observation:** it has 4 consecutive @glyphs (@231, @232, @233, @234) appearing together, similar structurally to f57v's 4-@glyph cluster. This folio is in the astronomical section (Quire Q) and is Hand 4. Worth further investigation.

## Multi-Folio @Glyphs With Cross-Hand Sharing

Only some multi-folio @glyphs cross between scribal hands:
| Glyph | Hands | Folios |
|---|---|---|
| @138 | 1, 2 | f101v, f15v, f26r |
| @145 | 1, 3 | f24r, f105r |
| @146 | 1, 2 | f24v, f84r |
| @150 | 1, 4 | f32r, f68v2 |
| @152 | 1, 2 | f11v, f36r, f82v |
| @154 | 1, 2 | f17r, f40r |
| @167 | 1, 4 | f56r, f68r1, f68r2 |
| **@169** | **1, 5** | **f57v, f66r** |
| **@172** | **1, 5** | **f57v, f66r** |
| @175 | 2, 3 | f76v, f86v3, f111r, f112v |
| @192 | 1, 4 | f1r, f49v, f72r3 |
| @197 | 1, 4 | f70v2, f89r1 |
| @206 | 2, 3 | f78r, f104v, f113v |
| @208 | 2, 3 | f104v, f83r |

@169 and @172 (Hand 1↔Hand 5) span the widest hand gap of any cross-hand shared @glyph in the manuscript.

## Key Findings

1. **@glyphs are rare manuscript-wide (0.3%)** but cluster heavily on specific folios, especially f57v (19 occurrences — by far the densest @glyph folio).

2. **The f49v "cluster" connection is structural, not via shared @glyph IDs.** f49v has @140, @164, @192, @243 — different from f57v's @169-@172 and f66r's @169/@172/@195.

3. **The f57v↔f66r link is confirmed and is the widest cross-hand @glyph sharing in the manuscript:** @169 and @172 are shared between Hand 1 (f57v) and Hand 5 (f66r), which is the maximum hand separation available.

4. **f76r's single @glyph (@174) is unique to that folio** — it doesn't appear anywhere else in the manuscript.

5. **f68r2 (astronomical, Hand 4) has 4 consecutive new @glyphs (@231-@234) in sequence** — a structural analog to f57v's @glyph cluster. This may be a second "structured @glyph sequence" in the manuscript.

6. **@170 and @171 appear ONLY on f57v** — they are not exported to f66r or anywhere else, making them the most "local" of the f57v special glyphs.
