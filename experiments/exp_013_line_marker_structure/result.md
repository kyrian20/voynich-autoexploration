# Experiment exp_013: Line Marker Structure Analysis
Date: 2026-04-09

## Hypothesis Tested
H020: f49v and f76r line-marker sequences encode structured information (key, cipher key, or sequence index).

## Method
Parsed all L0/P0 entries from f49v (26 pairs) and f76r (9 pairs) in eva_zl3b.txt. For each L0 marker, paired with the immediately following P0 body text line. Analyzed: (1) periodicity of marker sequence, (2) character frequency vs. global corpus, (3) correspondence between marker and body text characters, (4) cross-sequence comparison.

## f49v Results (26 marker/body pairs)

### Marker Sequence
`f o r y e @SPECIAL k s p o @SPECIAL y e @SPECIAL @SPECIAL p o @SPECIAL y e @SPECIAL d y e k y`

### Marker Frequency
@SPECIAL(6), y(5), e(4), o(3), k(2), p(2), f(1), r(1), s(1), d(1)

**Notable: 6/26 markers (23%) are non-EVA @SPECIAL glyphs** — same glyph type as found in f66r col2 and f57v circular text.

### Periodicity
No period 1–8 achieves ≥50% match. No periodic structure detected.

### Frequency vs. Corpus
| Marker | In markers | In corpus | Ratio | Direction |
|---|---|---|---|---|
| y | 19% | 9.29% | 2.1x | ↑ over |
| p | 8% | 0.85% | 9.1x | ↑ over |
| f | 4% | 0.23% | 16.5x | ↑ over |
| e | 15% | 10.45% | 1.5x | ≈ normal |
| o | 12% | 12.89% | 0.9x | ≈ normal |

Gallows characters f and p are dramatically overrepresented. Gallows k is near-normal (1.3x).

### Body Text Correspondence
| Test | Result | Expected by chance |
|---|---|---|
| Marker == body first char | 1/26 (4%) | ~6.0% |
| Marker == body last char | 0/26 (0%) | ~6.0% |
| Body first word starts with marker | 1/26 (4%) | ~6.0% |
| Body last word ends with marker | 0/26 (0%) | ~6.0% |

**No systematic correspondence.** Results are at or below chance levels — the markers do not index into their adjacent body text by character or word.

### First 10 Pairs (sample)
```
'f'        → first='k' last='y' word='kshor'    (len=21)
'o'        → first='q' last='y' word='qokchy'   (len=20)
'r'        → first='c' last='y' word='chotchy'  (len=23)
'y'        → first='o' last='m' word='okeodsho' (len=19)
'e'        → first='s' last='r' word='shol'     (len=19)
'@SPECIAL' → first='q' last='y' word='qotchy'   (len=18)
```

## f76r Results (9 marker/body pairs)

### Marker Sequence
`s d q s o l k r s`

### Marker Frequency
s(3), d(1), q(1), o(1), l(1), k(1), r(1)

### Periodicity
Period 4: 56% match, 4 mismatches. Pattern: [s, d, q, s]. Weak signal — with only 9 elements, this is near-random.

### Frequency vs. Corpus
| Marker | In markers | In corpus | Ratio |
|---|---|---|---|
| s | 33% | 3.76% | 8.9x ↑ |
| q | 11% | 3.08% | 3.6x ↑ |
| r | 11% | 3.79% | 2.9x ↑ |
| l | 11% | 5.48% | 2.0x ↑ |

's' is massively overrepresented (8.9x). No @SPECIAL glyphs in f76r markers.

### Body Text Correspondence
| Test | Result | Expected by chance |
|---|---|---|
| Marker == body first char | 1/9 (11%) | ~5.5% |
| Marker == body last char | 0/9 (0%) | ~5.5% |
| Body first word starts with marker | 1/9 (11%) | ~5.5% |
| Body last word ends with marker | 0/9 (0%) | ~5.5% |

Slightly above chance for first char (11% vs 5.5%) but with N=9 this is not significant.

## Cross-Sequence Comparison

| Feature | f49v | f76r |
|---|---|---|
| Total pairs | 26 | 9 |
| @SPECIAL | 6 | 0 |
| Distinct marker types | 10 | 7 |
| Scribe | Hand 1 (A) | Hand 2 (B) |

**Shared markers:** {d, k, o, r, s}
**Only in f49v:** {e, f, p, y, @SPECIAL}
**Only in f76r:** {l, q}

Is f76r a subsequence of f49v? **No**
Is f49v a subsequence of f76r? **No**
Shared 2-grams: **0**
Shared 3-grams: **0**

The two sequences have limited character overlap and no n-gram overlap. They were likely composed independently, not derived from a common sequence template.

## Key Findings
1. **No body text correspondence** — markers don't index adjacent text by first/last char. Ruling out "running heading" or "catchword" function.
2. **Gallows overrepresentation** — both f49v (f: 16.5x, p: 9.1x) and f76r (s: 8.9x, q: 3.6x) show non-random character selection favoring rare manuscript characters.
3. **@SPECIAL glyphs in f49v** — 23% of f49v markers are non-standard glyphs identical to those in f66r col2 and f57v circular text. This links the f49v line markers to the f57v/f66r "key cluster."
4. **Independent sequences** — the two scribes' sequences share some characters but no 2-grams or 3-grams; neither is a subsequence of the other. Different keys or different encoding conventions.
5. **No periodicity** — neither sequence shows strong periodic structure (>50% match), ruling out a simple repeating mnemonic.

## Interpretations
- The markers may be **positional indices** into a cipher system (not into adjacent text, but into a key table elsewhere)
- The overrepresentation of gallows characters is consistent with gallows functioning as a structural marker at a higher level (section/paragraph/line numbering in a gallows-coded system)
- The @SPECIAL glyphs in f49v markers create a three-way link: f49v (line markers) ↔ f66r (column 2 list) ↔ f57v (circular "key-like" text)

## New Hypotheses Generated
- H024: The f49v @SPECIAL glyphs in line markers are the same as those in f57v circular text — both may be using a shared "extended" glyph set not part of standard Voynich orthography
- H025: Gallows characters in line markers may function as section-level indices in a hierarchical cipher structure (body text = content, margin markers = structural labels)
