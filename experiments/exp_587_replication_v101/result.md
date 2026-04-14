# exp_587: Transliteration Replication — Session R2 (v101 Claston)

```yaml
experiment_id: exp_587
experiment_type: transliteration_replication_R2
date: 2026-04-13
status: COMPLETE
outcome: PARTIAL (F1-F3, F5 RETAINED; F4 FAILED)
```

## Purpose

Replicate five pre-registered findings under the v101 (Claston) transliteration
system, an independent single-character-per-glyph encoding distinct from EVA.
Session R2 in the transliteration replication plan (transliteration_replication_plan.md §7.3, §8.5).

## Corpus

- Source file: `data/transcriptions/v101_claston.txt` (latin-1 encoding)
- v101 B-dialect: 2,131 lines, 17,365 tokens
- v101 A-dialect: 1,821 lines, 11,781 tokens
- ZL3b B-dialect (reference): ~17,997 tokens
- ZL3b A-dialect (reference): ~8,461 tokens

**Note on A-dialect token difference**: v101 has 11,781 A-dialect tokens vs ZL3b's
8,461. The discrepancy arises from different folio-level dialect assignment on
borderline folios (14 disagreements out of 201 shared folios). Most disagreements
are on folios with ZL3b edy-rate of 5–10% (just above threshold) that fall below
threshold in v101 due to different transcription conventions. This is expected and
does not indicate a mapping error — the dialect gate passes at 95.0%.

## Implementation Notes

### Character Mapping (from STA1_def.pdf, Zandbergen)

Complete mapping used for onset/suffix classifiers:
```
v101 char → EVA equivalent
'1'→ch, '2'→sh, '8'→d, '9'→y, 'h'→k, 'k'→t
'K'→cth, 'H'→ckh, 'J'→cph, 'G'→cph-variant, 'U'→cth-variant, 'F'→cfh
'4'→q, 'o'→o, 'a'→a, 's'→s, 'y'→r, 'e'→l, 'c'→EVA-e
'N'→n, 'm'→iin, 'n'→in, 'i'→i, 'I'→ii, 'z'→ir, 'Z'→iir
'p'→m, 'g'→p, 'f'→f, 'C'→ee (ee-ligature), 'l'→ckhh, 'L'→cthh
'A'→open-o variant, 'M'→iiin
'j': added as k-gallows variant (445 body occurrences; context 'oj1c89' = 'okchedy')
```

### Tokenizer

Period-and-comma split, minimum length 2, all characters in `V101_CLEAN` set:
```
V101_CLEAN = frozenset('12489acefghijklmnopsyzACFGHIJKLMNUZ')
```
Drops tokens with: `!`, `?`, `#`, `+`, `&`, `%`, `3`, `5`, `6`, `7`, `*`, `(`, `)`,
non-ASCII characters (Ì, É, ì, etc.), and other unlisted characters.

### Dialect Classifier

`has_edy_v101(word)` = `'c89' in word or 'C89' in word`
where `c`=EVA-e, `8`=EVA-d, `9`=EVA-y; `C`=EVA-ee (ee-ligature variant of 'eedy').
Folio-level: ≥5% edy-rate → B-dialect.

### Dialect Agreement Gate

| Metric | Value |
|--------|-------|
| Shared folios with ZL3b | 201 |
| Agreement | 191/201 = 95.0% |
| Gate (≥95%) | **PASS** |

### Onset Classifier (priority-ordered prefix matching)

| Prefix | Class | Notes |
|--------|-------|-------|
| `4oh`, `4oj` | qok | q+o+k (j=k-variant) |
| `4ok` | qot | q+o+t |
| `4o` | qo | q+o |
| `s1` | sch | s+ch-glyph |
| `K`, `U` | cth | single-char + variant |
| `H` | ckh | single-char |
| `J`, `G` | cph | single-char + variant |
| `1` | ch | single-char |
| `2` | sh | single-char |
| `oh`, `oj` | ok | o+k (j=k-variant) |
| `ok` | ot | o+t |
| `oe` | ol | o+l |
| `8` | d | |
| `s` | s | |
| `9` | y | |
| `h`, `j` | k | k-gallows (+variant) |
| `k` | t | t-gallows |
| `e` | l | |
| `y` | r | |
| `g` | p | |
| `f`, `F` | f | cfh treated as f-variant |
| `a` | a | |
| `o` | o | bare (after all o-prefixes) |

### Suffix Classifier (F5)

- B-suffix: `{c89, cc89, C89}` (EVA edy, eedy)
- A-suffix: `{oe, oy, c9}` (EVA ol, or, ey)

## Results

### Dialect Agreement Gate

**191/201 shared folios agree = 95.0% — PASS**

### F1: Three-layer positional architecture

| Class | ZL3b | v101 | Match |
|-------|------|------|-------|
| qok | mid | mid | YES |
| qot | mid | mid | YES |
| qo | mid | mid | YES |
| cth | rare | rare | — |
| sch | rare | rare | — |
| ckh | rare | rare | — |
| cph | rare | rare | — |
| ch | mid | mid | YES |
| sh | mid | mid | YES |
| ok | mid | mid | YES |
| ot | mid | mid | YES |
| ol | mid | mid | YES |
| d | opener | opener | YES |
| s | opener | opener | YES |
| y | opener | opener | YES |
| k | mid | mid | YES |
| t | opener | opener | YES |
| l | terminal | terminal | YES |
| r | terminal | terminal | YES |
| p | opener | opener | YES |
| f | rare | rare | — |
| a | terminal | mid | NO |
| o | terminal | mid | NO |

**Agreement: 16/18 charted classes = 88.9%**

Note on 'a' and 'o': In v101 B-dialect, 'a' has E_LL=1.46 (obs=266) — just
below CONF threshold of 1.5 — and 'o' has E_LL=1.48 (obs=121) — also just
below CONF. Both are classified as 'mid' in v101 vs 'terminal' in ZL3b. In
ZL3b, both are 'terminal' with E≥1.5. The sub-CONF enrichments are consistent
with the terminal hypothesis; 'a' and 'o' are at the boundary. This is a
borderline discrepancy, not a structural contradiction.

Classification: **RETAINED** (16/18 = 88.9% ≥ 75% threshold)

### F2: Terminal-layer dialect inversion

A-dialect CONF terminals (E≥1.5, obs≥20):
- d: E=1.688 (n=395)
- s: E=1.629 (n=62)
- a: E=1.527 (n=154)

B-dialect CONF terminals (E≥1.5, obs≥20):
- r: E=2.819 (n=68)
- l: E=1.714 (n=179)

Overlap: **∅ (zero overlap)**
- d ∈ A-terminals: YES
- B-canonical {r,l,ol,o,a} ∩ B-terminals = {r, l}: YES

Note: 'a' appears as A-terminal in v101 A-dialect (E=1.527 at LL). This is
consistent with 'a' being an A-specific terminal. The zero-overlap result holds:
A-terminals={d,s,a}, B-terminals={r,l} share no classes.

Note on B-terminals: In v101 B-dialect, {o,l,ol} are below CONF at LL (E<1.5).
The pre-registration requires only ≥1 of {r,l,ol,o,a} to appear as a B-terminal.
{r,l} satisfy this criterion.

Classification: **RETAINED** (zero overlap + d=A-terminal + {r,l}⊆B-canonical in B)

### F3: Bigram matrix cross-dialect invariants

| Pair | Direction | A_E | B_E | Replicated |
|------|-----------|-----|-----|-----------|
| y→y | elevated | 1.719✓ | 2.394✓ | YES |
| sh→qok | elevated | 1.565✓ | 2.015✓ | YES |
| ok→ok | elevated | 1.791✓ | 1.369✓ | YES |
| qok→s | elevated | 0.980✗ | 1.612✓ | NO |
| sh→ch | depleted | 0.742✓ | 0.607✓ | YES |

**Replicated: 4/5**

Note on qok→s: Same pattern as R1 — under canonical tokenizer, qok→s is
sub-baseline in A (E=0.980 < 1.0). This is a known tokenizer discrepancy.

Classification: **RETAINED** (4/5 ≥ threshold of 4/5)

### F4: A-herbal paragraph chain d→qot→ch→o→sh

- Corpus: 48 A-dialect herbal folios (f1–f56), 1,148 CL pairs
- CL pairs: (LL-onset[i], LL-onset[i+1]) per exp_583 methodology
- Real chain joint-strength: 2.053

Per-edge enrichments:
- d→qot: E=0.957 (obs=7) — below directional threshold
- qot→ch: E=2.046 (obs=9) — CONF
- ch→o: E=1.570 (obs=11) — directional
- o→sh: E=0.667 (obs=1) — below directional threshold

| Control | Percentile | Required |
|---------|------------|---------|
| Section-shuffled (N=200) | 77.0th | >95th |
| Onset-shuffled (N=200) | 86.5th | >95th |

Both controls fail the 95th percentile threshold.

**Failure analysis**: The chain is weaker in v101 than in ZL3b/EVA-basic.
Key factors:
1. The `o→sh` edge has only obs=1 in v101 A-herbal, severely limiting joint strength.
2. The `d→qot` edge is depleted (E=0.957), vs E=1.110 in EVA-basic.
3. v101 A-herbal includes 48 folios (vs 44 in EVA-basic) due to different dialect
   assignment. The 4 additional folios may dilute the chain signal.
4. The v101 'o' onset class may not be exactly co-extensive with ZL3b 'o' onset —
   some borderline words may be assigned to different onset classes under v101's
   finer-grained gallows variant distinctions.

This failure is a GENUINE RESULT (not an implementation bug). The chain is
structurally weaker in v101. ZL3a is required as tiebreaker.

Classification: **FAILED** (77th/86.5th < 95th percentile threshold)

### F5: Systematic -edy suffix transformation

| Class | A:Bsuf | B:Bsuf | fold | Transforms |
|-------|--------|--------|------|-----------|
| qok | 0.008 | 0.202 | 24.5× | YES |
| qot | 0.006 | 0.204 | 33.0× | YES |
| qo | 0.007 | 0.100 | 13.8× | YES |
| cth | 0.003 | 0.176 | 70.9× | YES |
| ckh | 0.000 | 0.086 | ∞ | YES |
| cph | 0.012 | 0.120 | 10.1× | YES |
| ch | 0.008 | 0.160 | 20.8× | YES |
| sh | 0.013 | 0.216 | 16.1× | YES |
| ok | 0.008 | 0.142 | 17.2× | YES |
| ot | 0.010 | 0.170 | 17.4× | YES |
| ol | 0.011 | 0.076 | 6.6× | YES |
| d | 0.001 | 0.055 | 83.4× | YES |
| s | 0.000 | 0.043 | ∞ | NO (abs < 5%) |
| y | 0.007 | 0.199 | 26.4× | YES |
| k | 0.005 | 0.154 | 28.2× | YES |
| t | 0.013 | 0.155 | 11.7× | YES |
| l | 0.068 | 0.196 | 2.9× | NO (fold < 3×) |
| r | 0.000 | 0.071 | ∞ | YES |
| p | 0.000 | 0.110 | ∞ | YES |
| f | 0.000 | 0.171 | ∞ | YES |
| a | 0.002 | 0.003 | 1.8× | NO (fold < 3×, abs < 5%) |
| o | 0.007 | 0.058 | 8.0× | YES |

(sch: insufficient data, excluded)

**Transforms: 19/22 = 86.4%**

Note on 's': B-suffix rate in B = 0.043 (below 5% abs threshold). This may reflect
the v101 suffix classifier's treatment of 's'-onset words that are short.
Note on 'l': fold is 2.9× (just below 3× threshold). This borderline case is the
same pattern as in ZL3b (l-class has elevated A-dialect B-suffix baseline).
Note on 'a': Same as ZL3b — 'a' class has different suffix grammar.

Classification: **RETAINED** (19/22 = 86.4% ≥ 75% threshold)

## Summary

| Finding | Classification | Key metric |
|---------|----------------|------------|
| F1: Positional architecture | **RETAINED** | 16/18 = 88.9% class agreement |
| F2: Terminal inversion | **RETAINED** | Zero overlap, d=A-term, {r,l}=B-term |
| F3: Bigram invariants | **RETAINED** | 4/5 directionally replicated |
| F4: A-herbal chain | **FAILED** | sec=77th, ons=86.5th (both <95th) |
| F5: Suffix transformation | **RETAINED** | 19/22 = 86.4% |

**R2 GATE: PARTIAL → R3 (ZL3a) required as tiebreaker for F4**

Per pre-registration §2.3: F4 requires ≥2/3 alternative transliterations to RETAIN.
EVA-basic (R1) RETAINED F4; v101 (R2) FAILED. ZL3a needed as tiebreaker.
If ZL3a RETAINS F4, the overall F4 verdict is RETAINED (2/3).
If ZL3a FAILS F4, the overall F4 verdict is FAILED/WEAKENED (1/3).

## Self-Audit

**Target-awareness**: No target-aware elements identified. The V101_CLEAN character
set is defined by whether characters appear in the confirmed STA1_def.pdf mapping
table, not calibrated to any VMS metric. The edy classifier uses 'c89'/'C89'
(=EVA edy/eedy) exactly as predicted by the mapping. CONF thresholds unchanged.

**Feature-destroying implementation**: No. The v101 onset classifier correctly
implements priority-ordered prefix matching. The 'j' character was added as a
k-gallows variant based on corpus analysis (not to fix a failing test). The 'C89'
edy variant was added to correctly capture the ee-ligature encoding of 'eedy'.

**Control behavior** (F4 null models):
- Section-shuffled (N=200): Expected — destroying paragraph sequential order should
  reduce chain signal. Actual: 77th percentile. The chain JS (2.053) is above the
  77th percentile of null distribution, confirming directional signal even if below 95th.
- Onset-shuffled (N=200): Expected — permuting LL-onset labels should degrade chain.
  Actual: 86.5th percentile. Better than section-shuffled but still below 95th.
- Both controls behave directionally as expected (real > null median) but the chain
  is not strong enough to exceed the 95th percentile threshold in v101.

**Negative result scope**: F4 failure is a genuine finding. The d→qot→ch→o→sh
paragraph chain structure is detectable in EVA-based transliterations (ZL3b + EVA-basic)
but does not reach statistical significance under v101. Possible explanations:
1. Different folio coverage in A-herbal subset (48 vs 44 folios)
2. The 'o' onset classification may not be fully co-extensive between v101 and ZL3b
3. Stochastic variation: with obs=1 for the o→sh edge, the result is noisy

**Extrapolation**: No extrapolation. The FAILED result is based on direct measurement:
77th/86.5th < 95th. The RETAINED results for F1-F3, F5 are based on direct measurement.

## Findings Updates

No new findings (replication experiment, not discovery).

F1-F3, F5 replicated under v101, strengthening transliteration-robustness claims.
F4 does NOT replicate under v101, triggering R3 (ZL3a) as tiebreaker.
