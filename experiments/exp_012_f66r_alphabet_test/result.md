# Experiment exp_012: f66r Column 2 Alphabet Inventory Test
Date: 2026-04-09

## Hypothesis Tested
H020 sub-question: Is f66r column 2 an inventory of the Voynich character alphabet?

## Method
Compared f66r column 2 entries (34 tokens from lines L16–L49, manually enumerated from raw transcription) against the full EVA character inventory extracted from the 34,180-word body corpus (173,266 characters). Checked both single-character coverage and common compound forms (ch, sh, ee, aiin, etc.).

## Column 2 Contents
- 34 entries, 16 unique
- Sequence: y o s sh y d o f @169 x air d sh y f f y o d s f c @172 x t o @195 l r t o x p d
- Breakdown:
  - Special glyphs (@NNN;): @169, @172, @195 (3 entries, each once)
  - Compound forms: sh (×2), air (×1)
  - Single-char EVA: c d f l o p r s t x y (11 types, 28 tokens)

## EVA Corpus Inventory
- 25 distinct single characters in body text
- Most frequent: o(12.89%), e(10.45%), h(9.42%), y(9.29%), a(7.44%), c(6.96%), d(6.85%), i(6.34%), k(5.74%), l(5.48%)
- 12 compound forms with ≥100 occurrences: ch(7.78%), qo(4.01%), sh(3.27%), ee(3.03%), aiin(2.83%), ain(1.27%), cth(0.66%), ckh(0.64%), ii(0.30%), eee(0.27%), cph(0.15%), iii(0.13%)

## Coverage Results
| Category | In Column 2 | Total in Corpus | Coverage |
|---|---|---|---|
| Single chars | 11 | 25 | 44.0% |
| Common compounds (≥100 occ.) | 1 (sh only) | 12 | 8.3% |
| Special @NNN; | 3 | unknown (not in EVA) | — |

### In both col2 AND body corpus (single chars)
c, d, f, l, o, p, r, s, t, x, y

### In col2 but RARE or ABSENT in body
- @169, @172, @195 (special glyphs — no EVA representation)
- 'air' (0 occurrences in body text — unrecognized compound)
- 'x' (22 occurrences, 0.01% — extremely rare)

### In body (>100 occurrences) but ABSENT from col2
e (18,108 / 10.45%), h (16,313 / 9.42%), a (12,887 / 7.44%), i (10,985 / 6.34%),
k (9,952 / 5.74%), n (5,812 / 3.35%), q (5,338 / 3.08%), m (937 / 0.54%),
g (121 / 0.07%)

## Verdict: NOT a comprehensive alphabet inventory
- MODERATE coverage (44% single chars, 8.3% compounds)
- The 8 absent common characters include the TOP 5 most frequent EVA characters: e, h, a, i, k
- Missing characters are not random — they include all characters that commonly form compound clusters (e→ee/eee, h→ch/sh/cth/ckh, a→ain/aiin, i→ii/iii, k→k itself)
- Column 2 could be listing characters that are NOT components of common compound forms — i.e., the "simple" characters that stand alone

## Key Structural Pattern in Present/Absent Characters
**Present:** o, y, d, s, c, l, r, t, f, p, x — these are common EVA characters that primarily occur as simple, standalone units
**Absent:** e, h, a, i, k, n, q — these are characters that frequently fuse into compound clusters (ee, ch, sh, aiin, ck, etc.)
**Interpretation:** Column 2 may list "indivisible" glyph units that don't participate in compound formation — not an alphabet inventory but a list of "atomic" graphemes.

## f57v Connection (New Finding from raw ZL3b)
- f66r L38 has ZL3b comment "cf f57v?" — transcribers explicitly cross-referenced these
- f57v (cosmological folio, Scribe 1) contains a circular text (Cc locus) with a REPEATING sequence: `o.l.[d:j].r.v.x.k.m.f.@169;v.t.r.@170;.@171;.y.I.@172;` (repeated 3–4 times)
- This repeating sequence contains @169; and @172; — the SAME special glyphs as f66r column 2
- Shared chars with f66r col2: @169, @172, o, l, r, x, f, t, y (substantial overlap)
- ZL3b header for f57v: "has 'key-like' sequences" (same designation as f76r)
- This connection makes f57v a high-priority investigation target

## New Hypotheses Generated
- H022: f66r column 2 lists graphically "atomic" or "indivisible" Voynich characters (non-compound-forming subset)
- H023: f57v circular text and f66r column 2 share special glyphs (@169, @172) and may both encode the same underlying inventory or cipher key — in two different formats (circular vs. linear)
