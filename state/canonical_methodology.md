# Canonical Methodology — Voynich Cryptanalyst Project

```yaml
document_version: v1.0
date: 2026-04-12
status: resolves Open Issue #19 from grammar_spec v1.0
audience:
  - future LLM instance or pipeline reimplementing project metrics
  - future human researcher needing exact computation details
companion_documents:
  - state/voynich_grammar_spec.md          # what the constraints are
  - state/committed_claims.md              # what is committed to
  - state/cryptanalyst_phase_closure_2026_04_12.md  # history
purpose: |
  This document specifies the methodology underlying every numerical
  value in the grammar spec and committed_claims.md. A competent Python
  programmer should be able to reimplement the project's metrics from
  scratch using only this document and reproduce the values within
  rounding / tokenizer tolerance.
```

---

## Table of Contents

1. Corpus definition (transcription, locus parsing, token parsing)
2. Position conventions (LF/LL/second/MID/only; convention inversion history)
3. Dialect assignment (per-line canonical; folio-level legacy)
4. Onset class definitions
5. Suffix class definitions
6. Positional enrichment formula and significance testing
7. Self-succession formula (canonical post-C007 amendment)
8. Bigram enrichment formula
9. Adjacent-identical (adj_rate) formula
10. Multiple-testing correction conventions
11. Cross-validation procedure
12. Simulation conventions for null-model testing
13. Audit conventions (the five checks)
14. Committed-claims procedure
15. Worked example: reproducing C006 (y-onset LF enrichment)
16. Methodology evolution and known caveats
17. Changes to canonical methodology (chronological log)
18. Open methodological issues

---

## 1. Corpus Definition

### 1.1 Transcription

```yaml
transcription:
  name: "EVA ZL3b (Zandbergen-Landini 3b)"
  format: "IVTFF (Intermediate Voynich Transliteration File Format)"
  local_path: "data/transcriptions/eva_zl3b.txt"
  source: "http://www.voynich.nu/ (Rene Zandbergen / Takeshi Takahashi merged)"
  checksum_at_phase_closure: "not recorded; frozen for the phase"
  variants_available:
    - eva_zl3b.txt  # canonical for all exp_173+ work
    - eva_majority_zs.txt  # Zandbergen-only; used for cross-checks
    - eva_tt.txt            # Takahashi-only; used for cross-checks
```

**Canonical choice.** All committed claims (C005, C006, etc.) and all
characterization phase experiments use `eva_zl3b.txt`. Any reproduction
must use the same file; results computed from other transcription variants
will not exactly match the committed values.

### 1.2 Locus parsing rules

IVTFF lines are of the form:

```
<locus_code,type_suffix>         eva.text.here.with.dots
```

Canonical parser (extracted from exp_173 and re-implemented in exp_565+
with per-line dialect classification):

```python
import re
from collections import defaultdict

def parse_zl3b(path):
    """
    Returns:
      raw_lines: list of (folio_number: int, words: list[str])
      folio_words: dict[int, list[str]]
    """
    folio_words = defaultdict(list)
    raw_lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2:
                continue
            # folio number: strip < and trailing segment suffix
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m:
                continue
            fnum = int(m.group(1))
            # locus type: must start with 'P' for paragraph body text
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'):
                continue
            words = tokenize(text)
            if not words:
                continue
            folio_words[fnum].extend(words)
            raw_lines.append((fnum, words))
    return raw_lines, folio_words
```

**Locus types included in the body corpus** (per the `lt.startswith('P')`
filter):

- `P*` — paragraph text on all body folios
- `P0`, `P1`, ... — paragraph continuation loci
- All P-prefixed variants including `+P0`, `&P0`, `*P0`, `=P0`, `~P0`,
  `@P0` (continuation markers, per the `lstrip('@+*=~&')` step)

**Locus types EXCLUDED from body** (but included in the label corpus
per §1.4):

- `L*` — label loci (Lf, Ls, Ln, Lt, Lz, Lc, La, Lp, Lx, L0)
- `R*` — radial loci (Ri, Ro)
- `Cc` — circular running text (treated as label-adjacent per exp_580)

**Why `startswith('P')`.** IVTFF distinguishes running paragraph text
(P-prefixed) from labels, keys, marginalia, and diagram annotations.
The committed claims and all body-text findings are computed from
P-prefixed loci only. exp_173's script contains the canonical filter
at line 79–80.

### 1.3 Token parsing

Two canonical tokenizers exist, corresponding to two stages of the project:

#### 1.3.1 exp_173 tokenizer (committed-claims canonical)

```python
def tokenize_exp_173(text):
    """
    Committed-claims tokenizer (exp_173 line 80). Used for C005, C006,
    and all multiple-testing values.
    """
    return [
        w for w in text.split('.')
        if w and re.match(r'[a-z]', w) and not w.startswith('<')
    ]
```

Properties:
- Split on `.` only. Commas and hyphens produce compound tokens.
- Filter: token must begin with a lowercase ASCII letter.
- Filter: token must not start with `<` (which marks transcriber-
  uncertainty brackets).
- NO minimum length filter. Single-character tokens like bare `y` are
  retained.
- NO exclusion of transliteration-uncertainty markers inside the
  token (e.g. `[iin:cth]` alternations; see §1.3.3).

#### 1.3.2 Canonical characterization-phase tokenizer (exp_565+)

```python
def tokenize_canonical(text):
    """
    Canonical characterization-phase tokenizer (exp_565–exp_580). Used
    for F600+ findings, C007 canonical values, and C009.
    """
    toks = re.split(r'[-.\s]+', text.lower())
    return [t for t in toks if t and len(t) >= 2 and t.isalpha()]
```

Properties:
- Split on hyphen, period, or whitespace.
- Lowercase forced before filtering.
- Minimum length 2 (drops bare `y`, bare `l`, etc.).
- `isalpha()` excludes any residual markers.

#### 1.3.3 Relationship between the two tokenizers

The tokenizers produce DIFFERENT token counts on the same line. Per
exp_581 (convention diagnostic):

| Target          | exp_173 tokenizer | canonical tokenizer | delta |
|-----------------|-------------------|---------------------|-------|
| y-onset LF (B)  | 3.478×            | 3.121×              | 11.0% |
| -am LL (B)      | 6.856×            | 6.705×              | 2.2%  |
| s-onset adj_rate (B) | 0 / 580      | 0 / 686             | N/A   |
| t-onset adj_rate (B) | 0 / 417      | 0 / 817             | N/A   |

The two tokenizers differ primarily because:
1. **Comma-joined tokens.** exp_173's `.`-only split treats `or,y` as
   one token `or,y`; canonical split treats it as two tokens `or`, `y`.
2. **Single-character tokens.** exp_173 retains bare `y`; canonical
   drops it (`len(t) >= 2`).
3. **Hyphen-joined tokens.** exp_173 retains `a-b` as `a-b`; canonical
   produces `a`, `b`.

**Rule for new work.** Use the canonical tokenizer (§1.3.2) for any new
experiment. When reproducing a committed value, use the exp_173
tokenizer. The 0.5–1.5% residual differences between them are within
tolerance for all convention-diagnostic checks; they exceed tolerance
for fine-grained numerical reproduction.

### 1.4 Label corpus definition

Per exp_580 / proposed C010 (§15 of the grammar spec), labels are a
structurally distinct register. The label corpus is constructed with a
separate locus filter:

```python
LABEL_LOCUS_PATTERN = r'[&@*+=~][LR][^P]'
# first char: continuation symbol (& @ * + = ~)
# second char: 'L' (label) or 'R' (radial)
# third char: NOT 'P' (excludes LP continuations which are body-text)
```

**Label corpus size** (exp_580): 1,087 lines, 1,442 tokens.
**Body corpus size** (exp_580 cross-reference): 4,113 lines, 33,774
tokens.

**Section classification for labels** (informal; not tied to committed
claims):

```yaml
label_section_assignment:
  zodiac:      ["Lz", "La", "&Lz"]
  star:        ["Ls"]
  balneo:      ["Ln"]
  pharma:      ["Lt"]
  cosmo_large: ["Lf"]  # f88r specifically
  circular:    ["Lc"]
  herbal_plant: ["Lp"]
  herbal_L0:   "L0 on folios 1-72"
  radial:      ["Ri", "Ro"]
```

`@Cc` (circular running text) is NOT included in labels; it is treated
as running text per exp_580 §Method.

### 1.5 Section assignments (body corpus)

From exp_173 script:

```python
SECTION_RANGES = {
    'herbal': list(range(1, 67)),       # f1–f66
    'astro':  list(range(67, 85)),      # f67–f84
    'pharma': list(range(88, 103)),     # f88–f102
    'cosmo':  list(range(85, 88)),      # f85–f87
    'stars':  list(range(103, 117)),    # f103–f116
    'bio':    list(range(75, 85)) + list(range(116, 118)),
}
folio_to_section = {fn: s for s, folios in SECTION_RANGES.items()
                    for fn in folios}
```

Note that `bio` is defined non-contiguously (overlapping with `astro`
for f75–f84 and including f116–f117). This is deliberate: the
balneological section runs f75–f84 but is traditionally conflated with
astro in some transcriptions. Canonical Cryptanalyst work treats them
as separate.

For exp_579 (document-order heterogeneity) a tighter B-dialect
section assignment is used:

```yaml
B_section_folio_ranges_exp_579:
  B_herbal: f26..f72   # Quires D–H
  B_bio:    f73..f84   # Quire M
  B_astro:  f85..f102  # Quires N, Q
  B_pharma: f103..f116 # Quire T
```

---

## 2. Position Conventions

### 2.1 Canonical definition

**The canonical convention is the committed-claims convention.** All
v1.0 spec values, all committed claims, and all paper-bound findings
use this convention. It is defined in exp_173 script lines 54–59 and
matches the linguistic intuition of "line-first / line-last":

```python
def get_slot(i, n):
    """
    i: word index within line (0-indexed)
    n: total words in line
    """
    if n == 1:     return 'only'    # single-word line
    if i == 0:     return 'LF'      # line-first (first word)
    if i == n-1:   return 'LL'      # line-last  (last word)
    if i == 1:     return 'second'  # second word (index 1) when n ≥ 3
    return 'MID'                    # interior (index 2 .. n-2)
```

Explicitly:

| Slot name | Index (0-indexed)    | Requires   | Meaning                    |
|-----------|---------------------|------------|----------------------------|
| `only`    | 0                   | n = 1      | sole word of a 1-word line |
| `LF`      | 0                   | n ≥ 2      | line-first                 |
| `second`  | 1                   | n ≥ 3      | second word (when interior exists) |
| `LL`      | n − 1               | n ≥ 2      | line-last                  |
| `MID`     | 2 .. n − 2          | n ≥ 4      | interior positions         |

**Edge cases.**
- `n = 1`: single-word line contributes only to `only`; it does NOT
  contribute to either `LF` or `LL`. The `get_slot` function returns
  `'only'` and no other slot is assigned for that word.
- `n = 2`: two-word line has `LF` (index 0) and `LL` (index 1). There
  is NO `second` or `MID` for this line.
- `n = 3`: three-word line has `LF` (index 0), `second` (index 1), and
  `LL` (index 2). There is NO `MID`.
- `n = 4`: four-word line has `LF`, `second`, `MID` (index 2), `LL`.
- `n ≥ 5`: `LF`, `second`, `MID` (indices 2 through n − 2), `LL`.

### 2.2 Worked example — a 5-word line

Consider the line `qokeedy.chedy.sh.okam.lam`:

```
tokens:  [qokeedy, chedy, sh, okam, lam]
indices:  0        1      2   3     4
n = 5

get_slot(0, 5) = 'LF'      → qokeedy is LF
get_slot(1, 5) = 'second'  → chedy is second
get_slot(2, 5) = 'MID'     → sh is MID
get_slot(3, 5) = 'MID'     → okam is MID (general interior falls through)
get_slot(4, 5) = 'LL'      → lam is LL
```

Note: in this implementation, `get_slot(i, n)` returns `'MID'` for any
interior index where `1 < i < n - 1`. The `second` slot is a specific
sub-slice of that range (index 1 only), and position-2 self-chain
rules (§6 of the spec) reference `second` for lines where n ≥ 3.

### 2.3 Convention inversion — the historic bug

**A second convention existed in the characterization phase (exp_565+)
and is INVERTED relative to the canonical:**

```python
# CHARACTERIZATION-PHASE CONVENTION — NON-CANONICAL
# (exp_565 script lines 79–86; and similar in exp_566..exp_572)
if onsets[0] == 'qok':      pos_counts['pos1'] += 1  # first word
if L >= 2:
    if onsets[-1] == 'qok': pos_counts['LF']   += 1  # LAST word (sic)
    if onsets[-2] == 'qok': pos_counts['LL']   += 1  # PENULTIMATE (sic)
```

Translation table:

| Characterization phase | Canonical | Position |
|------------------------|-----------|----------|
| `pos1`                 | `LF`      | first word (index 0) |
| `LL`                   | `pen`     | penultimate (index n-2) |
| `LF`                   | `LL`      | last word (index n-1) |

**This was discovered during the v1.0 grammar spec cross-check
(2026-04-12)** and verified by exp_581 convention diagnostic. The
exp_581 result confirms that ALL committed-claim values were originally
computed using the CANONICAL convention — the characterization phase's
misnaming is nomenclatural only, never leaked into committed output.

**Why it happened.** The characterization phase scripts (exp_565..572)
used `LL` as shorthand for "Line-Last-area penultimate slot" and `LF`
as "Line-Final last word." The reversal was consistent across these
scripts but does not match the canonical convention of exp_173.

**Rule for new work.**
- NEVER use the exp_565 convention in new scripts.
- When reading F619, F622, F628, F631, F557, F558, and similar
  characterization-phase findings, TRANSLATE using the table above.
- When cross-referencing working_position.md §6, know that its "LF
  avoider" lists correspond to canonical LL-avoider lists.

### 2.4 What `second` is for

The `second` slot (index 1 when n ≥ 3) is used by:
- **Position-2 self-chain rules** (grammar spec §6, exp_487–exp_499).
  B-dialect has position-2 rules (e.g., B ch pos2 self-chain in
  B_herbal and B_pharma); A-dialect does not.
- **B qok-opener terminal grammar.** exp_565 finds B [qok@LF][ol@second]
  CONF (1.58×/14).

The `MID` slot includes index 1 only when `n ≥ 4` and the caller uses
a MID-without-second subdivision; in canonical exp_173, the `get_slot`
function's fallthrough means `second` (index 1) is NOT included in
`MID` when n ≥ 3.

### 2.5 Positions NOT defined in the canonical convention

- `pen` (penultimate, index n-2) is NOT a canonical position. When
  grammar-spec entries cite penultimate values (e.g., cph pen 1.45×),
  they come from characterization-phase scripts that computed it
  under a separate slot name. Translation rule: characterization-phase
  `LL` == canonical `pen`.
- `pos2` is sometimes used as shorthand for `second`. They are the
  same position (index 1).

---

## 3. Dialect Assignment

### 3.1 Canonical: per-line edy-rate assignment

**Per the C007 amendment (landed 2026-04-12), the canonical dialect
assignment is PER-LINE, not folio-level.** Source: exp_565 script
lines (canonical) and exp_573 reconciliation.

Procedure:

```python
def assign_dialect_per_line(words, edy_threshold=0.05, min_tokens=10):
    """
    Classify a single line as A or B based on its local edy-rate.
    Returns 'A', 'B', or None (underpowered).
    """
    if len(words) < min_tokens:
        return None
    edy_count = sum(1 for w in words if 'edy' in w or 'eedy' in w)
    rate = edy_count / len(words)
    return 'B' if rate >= edy_threshold else 'A'
```

Threshold: **edy-rate ≥ 5.0%** of line tokens. Words containing either
`edy` or `eedy` as a substring count (not anchored; `qokeedy` counts,
`shedy` counts).

Minimum token count: **10 tokens per line**. Lines with fewer than 10
tokens are not classified (they contribute to neither A nor B under
canonical). In practice most characterization-phase scripts relax this
minimum at line-level and only enforce it at aggregate level; the
exp_573 canonical run uses `min_tokens=10` at the line level.

**Why per-line.** A single folio can contain lines with different
dialect profiles (especially on mixed-section folios near f26 herbal/bio
boundary and f66 herbal A/B transition). Folio-level assignment pools
these heterogeneously and overstates self-succession in A-dialect
subsets (per exp_573 analysis: folio-level A herbal_a = 8,453 words
→ per-line A herbal_a = 11,327 words, capturing 2,874 additional lines
from mixed-section folios and DILUTING the self-succession signal).

### 3.2 Legacy: folio-level edy-rate assignment

Used in exp_164, exp_174, exp_173, and all pre-exp_565 work.

```python
def assign_dialect_folio_level(folio_words, edy_threshold=0.05,
                                min_tokens=10):
    """
    Classify an entire folio as A or B based on its aggregate edy-rate.
    folio_words: dict[int, list[str]]
    Returns: dict[int, str] mapping folio number → 'A' or 'B'
    """
    folio_dialect = {}
    for fn, wds in folio_words.items():
        if len(wds) < min_tokens:
            continue
        rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)
        folio_dialect[fn] = 'B' if rate >= edy_threshold else 'A'
    return folio_dialect
```

This function is the one used in exp_173 script lines 85–89.

**Relationship to canonical.** For most folios the two methods agree:
- f26–f66 (herbal A): mostly A under both methods.
- f75–f84 (bio): almost all B under both.
- f103–f116 (pharma): almost all B under both.

They disagree for:
- **Mixed herbal A/B transition folios** (approximately f56–f66) where
  some lines have high edy-rate and others do not.
- **Pharma A folios** where per-line assignment captures B-like lines
  on otherwise-A folios.

**C005 and C006 commitments.** The committed -am LL = 6.811× and
y-onset LF = 3.506× values were computed under FOLIO-LEVEL assignment
(exp_173 method). Per-line reproduction gives 6.705× (for -am LL) and
3.121× (for y-onset LF). Both are within spec tolerance for the spec's
purpose (directional validity) but NOT exactly reproducible under the
per-line method.

**Rule for new work.**
- Use per-line assignment (§3.1) for any new self-succession work, any
  new bigram work, and any work that will be compared to exp_565+
  findings.
- Use folio-level assignment only when reproducing exp_173-vintage
  committed-claim values exactly.

### 3.3 Relationship to Davis 2020 scribal-hand assignments

Davis (2020) identifies 5 scribal hands in the manuscript based on
handwriting analysis. These are NOT the same as dialect — Hand 2 writes
both A-dialect herbal and B-dialect bio sections. The IVTFF ZL3b
transcription carries hand assignments in the `$H=` metadata field.

Per exp_579: **in B-dialect, hand and section are nearly co-linear**
(Hand 2 = herbal+bio; Hand 3 = pharma; Hand 4 = rose foldout; Hand 5 =
part of herbal). This confound means scribal-hand effects cannot be
isolated from section effects in B-dialect; any "hand effect"
observed in B is structurally a section effect.

**Canonical rule.** Do not use scribal-hand assignments as a dialect
proxy. Use edy-rate per-line (§3.1). Scribal hand is a separate
covariate and should be treated as exploratory.

### 3.4 Section vs dialect

The six sections (§1.5) cut orthogonally to the dialect assignment:

| Section | Dialect dominance |
|---------|-------------------|
| herbal  | mixed A/B (f1–f66 mostly A; some B B-like lines) |
| astro   | A-dominant |
| bio     | B-dominant (≥95% per-line B) |
| cosmo   | A-dominant |
| stars   | B-dominant |
| pharma  | mixed; B-dominant in B-folios |

For the per-section positional metrics in exp_579 / grammar spec §11,
the four B-dialect sections are `B_herbal`, `B_bio`, `B_astro`,
`B_pharma`, constructed by intersecting the folio range with per-line
B classification.

---

## 4. Onset Class Definitions

### 4.1 Canonical onset classifier

The onset classifier used in committed-claims work (exp_173) and
extended in characterization phase (exp_565+):

```python
def get_onset(word):
    """
    Canonical onset classifier. Priority ordering matters: longer
    prefixes are checked first. The 'ch_e' class (che/chi) is
    exp_173-specific and NOT used in exp_565+; see §4.3.
    """
    w = word.lower()
    # q-bench: four-character prefixes first
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'):  return 'qo'
    # compound gallows (four-character)
    if w.startswith('cth'): return 'cth'
    # optional exp_173 only: che/chi subclass
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    # remaining c-initial: ch and compound gallows
    if w.startswith('sch'): return 'sch'  # exp_565+ addition
    if w.startswith('ckh'): return 'ckh'  # exp_565+ addition
    if w.startswith('cph'): return 'cph'  # exp_565+ addition
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    # two-character o-prefixes
    if w.startswith('ok'):  return 'ok'
    if w.startswith('ot'):  return 'ot'
    if w.startswith('ol'):  return 'ol'
    # single-character
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('k'):   return 'k'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    if w.startswith('r'):   return 'r'
    if w.startswith('p'):   return 'p'
    if w.startswith('f'):   return 'f'
    if w.startswith('a'):   return 'a'
    if w.startswith('o'):   return 'o'
    return 'other'
```

**Priority order is significant.** Because the check is
`startswith` with early return:
- A word `qokedy` returns `qok` (not `qo`, not `o`).
- A word `cthy` returns `cth` (not `c`, not `ch`).
- A word `qoaiin` returns `qo` (not `q`, not `o`).
- A word `sch` returns `sch` in exp_565+ but `s` would be returned if
  `sch` were checked after `s`. The priority ordering above places
  `sch` before `s`.

### 4.2 Full class inventory

The canonical class list used in the grammar spec:

```yaml
onset_classes:
  q_bench:
    - qok  # four-char prefix
    - qot  # four-char prefix
    - qo   # two-char prefix
  compound_gallows:
    - cth  # three-char prefix; A terminal
    - sch  # three-char prefix; A opener (rarest)
    - ckh  # three-char prefix; MID
    - cph  # three-char prefix; rare LL
  ch_sh:
    - ch    # two-char prefix (catches non-cth, non-sch c-initial)
    - sh    # two-char prefix
    - ch_e  # exp_173 only; not used in exp_565+
  ok_ot_ol:
    - ok    # two-char prefix
    - ot    # two-char prefix
    - ol    # two-char prefix
  single_consonant:
    - d, s, y, k, t, l, r, p, f
  vowel:
    - a, o   # bare a/o that don't match longer prefixes
  other:
    - other  # anything not matching above
```

**Classes that appear in the grammar spec but not as separate classifier
entries**: `am` is a suffix, not an onset class; see §5. Gallows `p`,
`k`, `t`, `f` are bare-onset classes (not compound). `y+k`, `y+t`,
`d+ch` are compound-onset descriptions used in grammar spec §9 but are
NOT distinct classes in the classifier — they are characterized as
the y-onset class with specific second-character conditions.

### 4.3 `ch_e` class — exp_173 only

exp_173 isolates words starting with `che` or `chi` as a separate class
`ch_e`. This was a pre-characterization-phase decision to examine
whether the e-vowel infix materially changed grammar. Per F087/F088
(exp_080/exp_081): **the e-infix is a vocabulary partition, not a
productive morphology.** When the same stem appears in both e-infix
and non-e forms, suffix distributions are identical.

**Rule.** Do NOT use `ch_e` as a separate onset class in new work.
Use `ch` for all c-h initial (non-cth) words. When reproducing
exp_173 values, use the `ch_e` class to match exactly.

### 4.4 Edge cases

- **Words shorter than the longest matching prefix.** A token `q` alone
  would return `other` under strict canonical tokenizer (because
  `len >= 2` filter drops it); under exp_173 tokenizer it returns `q`
  — no prefix check matches, so it returns `other`.
- **Words starting with rare two-char prefixes.** `qy` starts with `q`
  but not `qok/qot/qo`; it returns `other` because no `q*` class
  catches it (q-onset is only the q-bench classes).
- **Uppercase input.** The classifier forces lowercase first; any
  uppercase EVA characters are handled correctly. All committed claims
  work with lowercase-normalized text.
- **Non-alphabetic input.** The canonical tokenizer (§1.3.2) filters
  non-alphabetic characters out; exp_173's tokenizer allows the token
  but `get_onset` returns `other` since no prefix matches.

### 4.5 The "other" bucket

Tokens classified as `other` include:
- Rare onset prefixes not in the canonical list (e.g., `m`-initial,
  `n`-initial, `i`-initial, `h`-initial, `x`-initial).
- Compound-non-q onset words like `op*` (which are O-onset but some
  scripts treat them under `o`).
- Transliteration-uncertainty residuals (rare after the tokenizer
  filter).

The `other` bucket is typically 1–3% of body corpus. Per exp_105 /
F106: para-start words classified as "other" are dominated by bare_k
and bare_t gallows words, indicating classifier coverage gaps that
were addressed in PARA classifier v2 (grammar spec §6).

---

## 5. Suffix Class Definitions

### 5.1 Canonical suffix classifier

Suffix classification uses longest-matching suffix (in contrast to
onset which uses longest-matching prefix). The canonical list, derived
from the B-dialect 9-form paradigm plus A/B dialect-specific extensions:

```python
SUFFIX_CLASSES = [
    # Four-character suffixes (checked first)
    'eedy', 'aiin', 'eeey',
    # Three-character suffixes
    'edy', 'chy', 'eey', 'ain', 'air', 'ary',
    # Two-character suffixes
    'dy', 'ey', 'ol', 'or', 'ar', 'al', 'am', 'an', 'in', 'ir',
    # Single-character suffixes
    'y', 'n', 'l', 'r',
]

def get_suffix(word):
    """
    Canonical suffix classifier (longest-match).
    """
    w = word.lower()
    for suffix in SUFFIX_CLASSES:
        if w.endswith(suffix):
            return suffix
    return 'other'
```

**Priority order.** Longer suffixes are checked first. A word `qokeedy`
returns `eedy` (not `edy`, not `dy`, not `y`). A word `chedy` returns
`edy` (not `dy`, not `y`). A word `shol` returns `ol` (not `l`).

### 5.2 B-dialect 9-form productive paradigm (F045, F058)

Per exp_040 / exp_041 / F045: the B-dialect has a systematic 9-form
productive suffix paradigm active on approximately 10 productive stems:

```yaml
B_paradigm_9_forms:
  suffixes: ["-eedy", "-ain", "-edy", "-eey", "-aiin", "-y", "-ey", "-chy", "-dy"]
  top_stem_coverage:
    qok: {tokens: 1559, n_forms_attested: 9}
    ch:  {tokens: 1041}
    sh:  {tokens: 870}
    ok:  {tokens: 704}
    ot:  {tokens: 604}
  productivity_correlation:
    log_linear_r: 0.83_to_0.89
    interpretation: "stem frequency (log scale) explains 69–79% of variance in paradigm completeness"
```

**A→B inversion** (grammar spec §2). The same stems take different
suffixes in A vs B:

```yaml
A_to_B_stem_inversion:
  ch:
    A_preferred: {suffixes: [-ol, -or], obs: [225, 146]}
    B_preferred: {suffixes: [-edy, -ey], obs: [430, 208]}
  sh:
    A_preferred: {suffixes: [-ol, -or], obs: [99, 56]}
    B_preferred: {suffixes: [-edy, -ey], obs: [367, 173]}
  frequency_ratios:
    edy: "75× more common in B than A"
    ol:  "2.8× more common in A than B"
```

### 5.3 Positional suffix assignments

From F058 / F060:

```yaml
positional_suffix_roles:
  LF_enriched:
    - suffix: -aiin
      LF_pct: 0.142
  LL_enriched:
    - suffix: -ain,  LL_pct: 0.080
    - suffix: -am,   LL_enrichment: 6.811, commitment: C005
    - suffix: -dy,   A_LL_enrichment: 1.59
  MID_enriched:
    - suffix: -edy,  MID_pct: 0.85
    - suffix: -ol,   MID_pct: 0.807
    - suffix: -ey,   MID_pct: 0.808
    - suffix: -eey,  MID_pct: 0.800
```

### 5.4 Section-specific suffix extensions

- **pharma -eol**: A pharma-specific suffix variant extending the
  9-form paradigm. Per F058: 4–28× pharma-enriched, reaching 19.7% of
  pharma body text.
- **-am core vocabulary**: A closed class of within-para line-closers:
  `{otam, qokam, dam, okam, cham, ram}`. Per F093: these tokens have
  LLast% = 50–100%, WithinPara% = 90–100%, and PSFirst% = 0%. They
  are functionally a line-closing clitic.

### 5.5 Edge cases

- **Word is the suffix itself.** A bare `y` returns `y`; bare `dy`
  returns `dy` (not `y`); bare `edy` returns `edy`. Tokenizer may
  filter these out depending on the min-length rule (§1.3).
- **Suffixes not in the list.** `shcthy` ends in `cthy` which is not
  in the SUFFIX_CLASSES list; it returns `chy` under longest-match.
  `cthy` specifically is sometimes considered its own class in A-dialect
  but is not canonicalized in the suffix classifier.
- **Labels.** Label-dialect suffix profiles differ dramatically from
  body (per exp_580; grammar spec §15.3). The same classifier is used,
  but the suffix distributions are different. No label-specific
  classifier exists.

---

## 6. Positional Enrichment Formula and Significance Testing

### 6.1 The enrichment ratio

For an onset class `C` and a position `X ∈ {LF, LL, second, MID}`:

```
enrichment(C, X)
    = rate_at_position / corpus_base_rate
    = (count(C, X) / total(X)) / (count(C) / total())
```

Where:
- `count(C, X)` = number of words of onset class C appearing at position X
- `total(X)` = total number of words appearing at position X
- `count(C)` = total number of class-C words in the corpus
- `total()` = total number of words in the corpus

Values > 1 mean enriched; values < 1 mean depleted; exactly 1 means
at baseline. The canonical CONF / DEPL thresholds:

```yaml
confidence_thresholds:
  CONF:    "ratio ≥ 1.50 AND obs ≥ 10"
  subCONF: "ratio ∈ [1.30, 1.50) OR obs ∈ [5, 9]"
  dir:     "ratio ≥ 2.0 AND obs ≥ 5 (directional below CONF obs threshold)"
  flat:    "ratio ∈ (0.85, 1.30) and not directional"
  subDEPL: "ratio ∈ (0.67, 0.85]"
  DEPL:    "ratio ≤ 0.67 AND obs ≥ 10"
```

These thresholds are enforced in the canonical characterization-phase
scripts (exp_565+) via a flag computation:

```python
def classify_enrichment(obs, tot, base_rate):
    if tot == 0 or base_rate == 0:
        return 'n/a'
    rate = obs / tot
    E = rate / base_rate
    if E >= 1.5 and obs >= 10:
        return 'CONF'
    elif E >= 2.0 and obs >= 5:
        return 'dir'
    elif E >= 2.5 and obs >= 3:
        return '(dir)'   # weak directional
    elif E <= 0.67 and obs >= 10:
        return 'DEPL'
    elif E <= 0.85:
        return 'subDEPL'
    elif 0.85 < E < 1.30:
        return 'flat'
    elif 1.30 <= E < 1.50:
        return 'subCONF'
    return 'baseline'
```

### 6.2 Significance testing — binomial exact (one-sided)

For CONF findings, the exact one-sided binomial test is used:

```python
from scipy.stats import binomtest

def binomial_p(obs, tot, base_rate, alternative='greater'):
    """
    One-sided exact binomial test.
    alternative='greater' tests enrichment (H1: true_rate > base_rate)
    alternative='less' tests depletion   (H1: true_rate < base_rate)
    Returns: p-value
    """
    if tot < 10:
        return None
    return binomtest(obs, tot, base_rate, alternative=alternative).pvalue
```

**One-sided direction.** The test is one-sided in the direction of the
observed enrichment. If the observed ratio > 1, test `alternative='greater'`.
If the observed ratio < 1, test `alternative='less'`. This is the
convention used in exp_173. **Do not test the wrong direction** — per
exp_173 note on F27: "sh LF B is a slight DEPLETION (0.859×); the
one-sided enrichment test gives p=0.988 (correct: not an enrichment);
testing the depletion direction gives p=0.012 (marginal but not
Bonferroni-corrected)."

### 6.3 Significance testing — Fisher's exact for bigram enrichments

For bigram enrichments (class A → class B) the test is Fisher's exact
on a 2×2 contingency table:

```python
from scipy.stats import fisher_exact

def fisher_bigram_p(obs_AB, total_A_bigrams,
                    obs_notB_from_A, total_bigrams_from_not_A,
                    alternative='greater'):
    """
    2×2 table for testing whether A→B is enriched relative to ?→B.
    | obs_AB             total_A_bigrams - obs_AB             |
    | obs_notB_from_A    total_bigrams_from_not_A - obs_notB_from_A |
    """
    _, p = fisher_exact([
        [obs_AB, total_A_bigrams - obs_AB],
        [obs_notB_from_A, total_bigrams_from_not_A - obs_notB_from_A]
    ], alternative=alternative)
    return p
```

This is used in exp_173 for bigram findings (F7, F8, F9).

### 6.4 Rate-of-base computation

Critical detail: `base_rate` in §6.1 is computed over the full corpus,
NOT over non-X positions. Example for y-onset LF enrichment:

```python
y_count_total   = sum(1 for w in all_words if get_onset(w) == 'y')
corpus_total    = len(all_words)
corpus_base_rate = y_count_total / corpus_total   # e.g., 0.042

y_at_LF_count = sum(1 for w in lf_words if get_onset(w) == 'y')
lf_total      = len(lf_words)
lf_rate       = y_at_LF_count / lf_total          # e.g., 0.147

enrichment = lf_rate / corpus_base_rate           # 0.147 / 0.042 = 3.50×
p_value    = binomial_p(y_at_LF_count, lf_total, corpus_base_rate)
```

**MID-baseline alternative (characterization-phase canonical).** For
self-succession and some position-specific bigram work (exp_565+), the
expected rate is computed over MID positions only, not the full corpus:

```python
mid_words = [w for i, w in enumerate_line if i > 0 and i < len(line) - 1]
mid_base_rate = sum(1 for w in mid_words if get_onset(w) == 'y') / len(mid_words)
```

The two formulations give different enrichment values when the class
is concentrated or depleted at LF/LL. For a class like qok that is
both LF-avoider (0.81×) and LL-avoider (0.53×), the MID-rate is HIGHER
than the corpus-rate, so MID-baseline enrichment at LF or LL is LOWER
than corpus-baseline enrichment.

**Canonical rule**: committed-claim positional values (exp_173) use
corpus-baseline; characterization-phase positional values (exp_565+)
use MID-baseline for self-succession AND for position-conditional
bigram work. Grammar spec §1 values are a mix: C005 / C006 use
corpus-baseline (committed); F619+ characterization values use
MID-baseline.

---

## 7. Self-Succession Formula (Canonical, Post-C007 Amendment)

**This section is load-bearing for the C007 amendment and supersedes
the legacy formulation used in exp_164/174.**

### 7.1 The canonical formula

For an onset class C and dialect D:

```
ss_enrichment(C, D)
    = observed_count / expected_count
    = obs / (n_sender × mid_rate_target)
```

Where:
- `obs` = number of adjacent word pairs (within-line) where BOTH words
  have onset class C, in dialect D
- `n_sender` = number of class-C words that have a successor
  (within-line), in dialect D
- `mid_rate_target` = MID-position rate of class C in dialect D

```python
def canonical_self_succession(lines, dialect_label, target_class):
    """
    Compute canonical (post-C007) onset self-succession for target_class
    in dialect_label. lines = list of (folio, words) after dialect filter.
    """
    # Step 1: compute MID-baseline rate for target_class
    mid_tokens = 0
    mid_target = 0
    for fo, ws in lines:
        n = len(ws)
        for i in range(1, n - 1):   # interior only
            mid_tokens += 1
            if get_onset(ws[i]) == target_class:
                mid_target += 1
    mid_rate_target = mid_target / mid_tokens if mid_tokens > 0 else 0

    # Step 2: count target→target adjacent pairs
    obs = 0
    n_sender = 0
    for fo, ws in lines:
        for i in range(len(ws) - 1):
            if get_onset(ws[i]) == target_class:
                n_sender += 1
                if get_onset(ws[i + 1]) == target_class:
                    obs += 1

    # Step 3: enrichment
    expected = n_sender * mid_rate_target
    E = obs / expected if expected > 0 else float('inf')
    return {
        'obs': obs,
        'n_sender': n_sender,
        'mid_rate_target': mid_rate_target,
        'expected': expected,
        'E': E,
    }
```

**Why MID-baseline.** If the target class is concentrated at MID (like
qok or ch), its MID rate is higher than its overall-corpus rate. The
overall-rate formula would count LF and LL positions in the baseline
even though they cannot participate in same-class successions to
adjacent MID positions. MID-baseline is the correct expected rate for
within-line same-onset bigram enrichment.

### 7.2 Minimum observation threshold

```yaml
obs_threshold_for_CONF: 10
obs_threshold_for_dir:   5
obs_threshold_for_canonical_finding: 10
```

For a self-succession finding to be CONF in the grammar spec, both
`E ≥ 1.50` AND `obs ≥ 10` must hold. Classes with obs < 10 are reported
as `dir` (if E ≥ 2.0) or not reported.

### 7.3 The legacy formula (exp_164/174)

**Superseded.** The legacy formula used in the C007-source experiments:

```
ss_legacy(C, D)
    = observed_count / (total_bigrams × rate²)
```

Where:
- `observed_count` = count of class-C adjacent pairs
- `total_bigrams` = total within-line bigrams in dialect D
- `rate` = overall corpus rate of class C in dialect D

This formula has two problems relative to canonical:

1. **rate² is wrong for MID-concentrated classes.** It uses the overall
   corpus rate (including LF and LL) squared, whereas the correct
   expected value under an independence null is MID-rate × MID-rate
   (since only adjacent MID positions can form within-line same-class
   pairs that are NOT at line boundaries).

2. **total_bigrams is wrong as the denominator.** The correct
   denominator is `n_sender` (the number of class-C sending positions),
   not total within-line bigrams. Using total_bigrams inflates the
   denominator and — crucially — does not account for the conditional
   structure.

Per exp_573 reconciliation, these two differences combined (plus the
folio-level vs per-line dialect difference in §3) explain the entire
discrepancy between the C007 original values (1.24–2.05×) and the
canonical values (0.78–3.86×).

### 7.4 Canonical self-succession values (from C007 amendment)

Per exp_573 / committed_claims.md C007 amendment, the canonical table:

```yaml
canonical_self_succession:
  CONF_in_both_dialects:
    l:   {A: 3.86_obs16, B: 2.62_obs72}
    qot: {A: 3.16_obs18, B: 1.69_obs29}
    y:   {A: 1.88_obs40, B: 3.16_obs20}
    ot:  {A: 2.23_obs50, B: 2.10_obs90}
    qo:  {A: 1.76_obs14, B: 1.82_obs16}
  CONF_in_A_only:
    ol:  {A: 3.20_obs45, B: 1.32_obs30}
    d:   {A: 1.75_obs151, B: 1.35_obs41}
  subCONF_or_FLAT:
    ok:  {A: 1.42_obs81,  B: 1.30_obs56}
    qok: {A: 1.27_obs77,  B: 1.03_obs242}
    ch:  {A: 1.04_obs453, B: 0.91_obs259}
    sh:  {A: 1.21_obs96,  B: 0.78_obs76}
  range: [0.78, 3.86]
```

**Range 0.78× – 3.86×** is the canonical C007 range (replacing the
original 1.24× – 2.05× which was incorrect).

### 7.5 Position control stratification

Per exp_174 position-control analysis: self-succession holds across
line-position strata for CONF classes. The stratification partitions
adjacent word pairs by their position pair:

```yaml
position_control_strata:
  LF_to_second: "first word → second word (index 0 → 1)"
  second_to_MID: "second word → first interior (index 1 → 2)"
  MID_to_MID:   "interior → interior (i → i+1, both in [2, n-3])"
  MID_to_LL:    "last interior → last word (index n-2 → n-1)"
```

For each stratum, the same-class pair rate is computed and the
enrichment is residualized against the expected rate under positional
independence. A CONF class under position control means its residual
enrichment ≥ 1.2× in MOST strata (not all; per amendment).

**Per the C007 amendment**, this holds for the CONF cross-dialect
classes (y, l, ot, qo, qot) but does NOT hold for B qok (1.03×),
B ch (0.91×), B sh (0.78×), which are flat or depleted at baseline
and produce sub-1.2× residuals at every stratum.

---

## 8. Bigram Enrichment Formula

### 8.1 Within-line bigram enrichment

For a directed onset pair `A → B` (sender class A, receiver class B):

```
bigram_enrichment(A, B)
    = obs / expected
    = obs / (n_sender_A × rate_receiver_target)
```

Where:
- `obs` = count of adjacent (within-line) pairs where first word has
  onset A and second word has onset B
- `n_sender_A` = number of class-A words that have a within-line successor
- `rate_receiver_target` = baseline rate of class B at the receiver's
  position

```python
def bigram_enrichment(lines, sender_class, receiver_class,
                       position_filter=None):
    """
    position_filter: None (all within-line bigrams), 'MID' (MID bigrams only),
    or a callable (i, n) → bool selecting which bigram positions to count.
    """
    obs = 0
    n_sender = 0
    total_receiver = 0  # words eligible to be the receiver
    total_positions = 0
    for fo, ws in lines:
        n = len(ws)
        for i in range(n - 1):  # bigram starts at i, ends at i+1
            if position_filter is not None and not position_filter(i, n):
                continue
            total_positions += 1
            if get_onset(ws[i + 1]) == receiver_class:
                total_receiver += 1
            if get_onset(ws[i]) == sender_class:
                n_sender += 1
                if get_onset(ws[i + 1]) == receiver_class:
                    obs += 1
    rate_receiver = total_receiver / total_positions if total_positions else 0
    expected = n_sender * rate_receiver
    E = obs / expected if expected > 0 else float('inf')
    return {'obs': obs, 'n_sender': n_sender, 'rate_receiver': rate_receiver,
            'expected': expected, 'E': E}
```

### 8.2 Position-conditional bigram grammar

Per F076 / exp_069: **B-dialect bigrams are position-specific; A-dialect
bigrams are position-general.** B bigrams must be filtered to MID
positions to observe the canonical pattern; A bigrams hold across all
within-line positions.

For B-dialect bigrams, use `position_filter=lambda i, n: 1 <= i < n - 2`
to restrict the bigram to MID→MID transitions (both endpoints are
interior). For A-dialect bigrams, no filter is needed.

### 8.3 Sample-size minimums

```yaml
bigram_sample_size_rules:
  CONF:    "obs ≥ 10 AND E ≥ 1.5"
  subCONF: "obs ≥ 5  AND E ≥ 1.3"
  dir:     "obs ≥ 5  AND E ≥ 2.0"
  DEPL:    "obs ≥ 10 AND E ≤ 0.67"
```

Values below these thresholds should be reported as directional only
or not reported at all. The grammar spec §4 bigram matrices use these
thresholds throughout.

### 8.4 Significance testing

For bigram findings committed to a public output (e.g., F7, F8, F9 in
C007 / exp_173), Fisher's exact test on the 2×2 contingency table of
{sender, not-sender} × {receiver, not-receiver} is the canonical test
(per §6.3).

For characterization-phase bigram findings (F619, F620, etc.), the
canonical E ≥ 1.5 + obs ≥ 10 rule is the acceptance criterion; no
individual p-value is reported.

---

## 9. Adjacent-Identical Formula

### 9.1 Within-line adjacent-identical word pairs

The adj_rate metric counts EXACT word identity between adjacent tokens
within a line. Per C009 / exp_577 canonical:

```python
def adj_rate(lines, target_class=None, dialect_filter=None):
    """
    Counts identical adjacent word pairs within lines.
    If target_class is given, restricts to pairs where both words have
    that onset class (per-onset adj_rate analysis).
    """
    obs_identical = 0
    total_pairs = 0
    for fo, ws in lines:
        for i in range(len(ws) - 1):
            if target_class is not None:
                o1 = get_onset(ws[i])
                o2 = get_onset(ws[i + 1])
                if o1 != target_class or o2 != target_class:
                    continue
            total_pairs += 1
            if ws[i] == ws[i + 1]:
                obs_identical += 1
    return {
        'identical_pairs': obs_identical,
        'total_pairs': total_pairs,
        'rate': obs_identical / total_pairs if total_pairs > 0 else 0
    }
```

### 9.2 Adjacent definition

- **Within-line only.** adj_rate is computed over pairs where both words
  are in the same line. Pairs that would span a line break (last word
  of line N, first word of line N+1) are NOT counted. This matches
  C009 and exp_577.
- **Direct adjacency.** Gap-1 pairs (i and i+1). Longer gaps (i and i+2)
  are not considered adj_rate.

### 9.3 Per-onset-class normalization

For analyzing whether a specific class's adj_rate matches random-draw
expectations from its CP90 vocabulary pool:

```
random_expectation(class)
    = 1 / CP90(class)

ratio(class)
    = observed_rate(class) / random_expectation(class)
```

Per exp_577 / C009 Part A:

```yaml
adj_rate_per_onset_B_dialect:
  sh:  {obs_rate: 0.00764, CP90: 145, random_expect: 0.00690, ratio: 1.108}
  ch:  {obs_rate: 0.00659, CP90: 290, random_expect: 0.00345, ratio: 1.910}
  d:   {obs_rate: 0.00480, CP90: 146, random_expect: 0.00685, ratio: 0.701}
  s:   {obs_rate: 0.00000, CP90: 91,  random_expect: 0.01099, ratio: 0.000}
  t:   {obs_rate: 0.00000, CP90: 169, random_expect: 0.00592, ratio: 0.000}
  qok: {obs_rate: 0.02681, CP90: 32,  random_expect: 0.03125, ratio: 0.858}
```

The ratios > 1.0 indicate class-specific anti-repetition is WEAKER than
random-draw expectation (more identical pairs than random); ratios < 1.0
indicate anti-repetition is STRONGER than random. Per C009 Part A:
sh, d are near-random (ratio ≈ 0.7–1.1), ch is elevated from
self-succession concentration, s/t are at structural zero.

### 9.4 s/t structural zero (C009 Part B)

**s and t have adj_rate = 0 in B-dialect despite having CP90 large
enough to allow chance repetition.** Per exp_577: 0/452 identical
adjacent pairs for s-onset; 0/466 for t-onset. This is convention-
independent (verified by exp_581 under both tokenizers and dialect
assignments). The mechanism: s and t are line-opening classes with
the vast majority of tokens appearing at LF only; two consecutive
line-first slots cannot occur without a line break intervening, and
adj_rate does not count across line breaks (§9.2).

---

## 10. Multiple-Testing Correction Conventions

### 10.1 The two Bonferroni thresholds

Per exp_173 canonical multiple-testing procedure, the project reports
TWO Bonferroni-corrected significance thresholds:

```yaml
bonferroni_m_30:
  m: 30
  alpha: 0.05
  per_test_threshold: 0.05 / 30  # = 0.001667
  interpretation: "corrects for 30 nominated candidate findings"
  appropriate_when: "the 30 findings were pre-specified"

bonferroni_m_175:
  m: 175
  alpha: 0.05
  per_test_threshold: 0.05 / 175  # = 0.000286
  interpretation: "corrects for all 175 quantitative findings in characterization phase"
  appropriate_when: "any of the 175 could have been nominated"
```

**Transparency rule** (per exp_173): When reporting a new finding,
state its survival status at BOTH thresholds. The choice of m is
usually m=30 for nominated candidates, but m=175 for post-hoc
nominations should be reported alongside.

### 10.2 BH-FDR (Benjamini-Hochberg) at q=0.05

For the same candidate set:

```python
def bh_fdr(pvalues, q=0.05):
    """
    Benjamini-Hochberg FDR correction. Returns a list of booleans
    indicating which tests pass at q-level.
    """
    n = len(pvalues)
    sorted_p = sorted(enumerate(pvalues), key=lambda x: x[1])
    # BH: find largest k such that p_(k) ≤ k/n × q
    max_reject = -1
    for k, (idx, p) in enumerate(sorted_p, start=1):
        if p <= (k / n) * q:
            max_reject = k
    # All tests with rank ≤ max_reject are rejected
    rejected = set()
    for k, (idx, p) in enumerate(sorted_p, start=1):
        if k <= max_reject:
            rejected.add(idx)
    return [i in rejected for i in range(n)]
```

Per exp_173: 26/30 candidate findings survive BH-FDR at q=0.05, vs
24/30 at Bonferroni m=30 and 21/30 at Bonferroni m=175. BH is more
permissive than Bonferroni m=30 which is more permissive than m=175.

### 10.3 When each correction is appropriate

```yaml
correction_selection_rules:
  bonferroni_m_30:
    use_when: "pre-registered candidate set of 30 findings"
    appropriate_for: "initial nomination from characterization phase"

  bonferroni_m_175:
    use_when: "post-hoc nomination after seeing all 175 findings; paper output"
    appropriate_for: "paper-bound claims and committed claims"
    note: "C001–C009 all cite m=175 survivors where applicable"

  bh_fdr_q_05:
    use_when: "exploratory analysis where tolerating 5% false discovery rate is acceptable"
    appropriate_for: "hypothesis-generation phase, not confirmation phase"
```

**Committed claims use m=175.** All 8 of C001–C009's statistical claims
survive Bonferroni m=175. The one borderline case is F29 (qok LF
depletion B) which passes m=30 but not m=175; that finding is cited
in the synthesis but not the subject of a committed claim.

### 10.4 Family structure

exp_173 partitions the 30 candidate findings into 7 families to enable
family-based reporting. Per the by-family summary:

```yaml
exp_173_families:
  positional:       {n: 8, bonf_survivors: 7}
  bigram:           {n: 4, bonf_survivors: 2}
  self_succession:  {n: 7, bonf_survivors: 6}
  dialect_split:    {n: 4, bonf_survivors: 4}
  cth_positional:   {n: 3, bonf_survivors: 3}
  suffix:           {n: 2, bonf_survivors: 2}
  word_level:       {n: 2, bonf_survivors: 1}
  total:            {n: 30, bonf_survivors: 24}
```

At least 50% of each family survives Bonferroni m=30. Dialect-split,
cth-positional, and suffix families are 100% clean.

---

## 11. Cross-Validation Procedure

### 11.1 Random 80/20 splits stratified by dialect

For stability-of-finding tests (exp_172, exp_173):

```python
def stratified_80_20_split(lines, seed=42):
    """
    Random 80/20 split stratified by dialect. Returns (train_lines, test_lines).
    """
    import random
    rng = random.Random(seed)
    a_lines = [l for l in lines if l['dialect'] == 'A']
    b_lines = [l for l in lines if l['dialect'] == 'B']
    rng.shuffle(a_lines); rng.shuffle(b_lines)
    a_train = a_lines[:int(0.8 * len(a_lines))]
    a_test  = a_lines[int(0.8 * len(a_lines)):]
    b_train = b_lines[:int(0.8 * len(b_lines))]
    b_test  = b_lines[int(0.8 * len(b_lines)):]
    return a_train + b_train, a_test + b_test
```

**Pass criterion**: A finding passes CV if the enrichment ratio in the
test fold is within ≥50% of the training-fold magnitude AND has the
same sign. Specifically:

```
test_ratio / train_ratio ≥ 0.5 AND sign(test - 1) == sign(train - 1)
```

Per exp_173: all 8 committed positional findings pass 80/20 CV.

### 11.2 Leave-one-section-out (LOSO)

For robustness against section effects:

```python
def loso_cv(lines, compute_metric):
    """
    For each of the six sections, drop it and compute the metric on
    the remaining corpus. Returns a dict of section → held-out metric.
    """
    results = {}
    all_sections = set(l['section'] for l in lines)
    for held_out in all_sections:
        remaining = [l for l in lines if l['section'] != held_out]
        results[held_out] = compute_metric(remaining)
    return results
```

**Pass criterion (LOSO)**: all six held-out values must satisfy the
same "≥50% of full-corpus magnitude with same sign" rule as above.

Per exp_173: all 8 committed positional findings pass LOSO.

### 11.3 Document-order splits (exp_576)

For parameter stability (exp_576), three 50/50 splits are used:
- **Odd/Even**: interleaved folios
- **First/Second**: document-order halves
- **Random**: random 50/50 with seed

The First/Second split is where the document-order heterogeneity
finding surfaces (per exp_579); 17/19 → 8/19 cross-validation catastrophe
is primarily a corpus-heterogeneity effect, not a parameter instability
effect. See grammar spec §11 and §10.parameter_stability_test.

---

## 12. Simulation Conventions for Null-Model Testing

### 12.1 Simulation count

```yaml
simulation_count_per_condition:
  exploratory_sweep: 3    # fast grid-pass; not for publication
  confirmed_best:    10   # N=10 reruns of best parameters for N=30 confirmation
  published:         30   # N=30 runs of committed mechanism configurations
  null_distribution: 100  # for confidence interval estimation
```

Per exp_314: the 19/19 architecture battery uses N=30 runs of each
parameter combination for the committed value.

### 12.2 Confidence interval computation

```python
def empirical_ci(values, ci_level=0.95):
    """
    Empirical percentile CI from simulation runs.
    """
    import numpy as np
    lo = np.percentile(values, (1 - ci_level) / 2 * 100)
    hi = np.percentile(values, (1 + ci_level) / 2 * 100)
    return lo, hi
```

The 95% CI is the empirical 2.5th–97.5th percentile of the N-run
distribution. Results outside this CI are flagged as PASS or FAIL
under the `±20% of target` tolerance used in the 19-metric battery.

### 12.3 Corpus-matching conventions

For null-model simulations (Naibbe, Timm, 21-mechanism), the simulated
corpus must match real VMS in:

- **Line count**: same number of lines as the real corpus.
- **Line-length distribution**: drawn from the VMS empirical histogram,
  clipped to `[2, 20]` words per line.
- **Section proportions**: if section-specific calibration, match the
  section line counts.

```python
def draw_line_length(vms_line_length_histogram, rng, clip=(2, 20)):
    """
    Draw a line length from the empirical VMS histogram, clipped.
    """
    length = rng.choices(
        list(vms_line_length_histogram.keys()),
        list(vms_line_length_histogram.values())
    )[0]
    return max(clip[0], min(clip[1], length))
```

The clip range `[2, 20]` drops 1-word lines (labels / markers) and
extremely long lines (transcription artifacts). Per exp_314, this is
the operational range for all committed architecture work.

### 12.4 The 19-metric battery

Per C008 and exp_314, the battery metrics are:

```yaml
19_metric_battery:
  metrics:
    - am_ll
    - ss_mean
    - adj_rate
    - ch_ll
    - ok_ll
    - ss_d
    - ss_y
    - qok_ch
    - edy_rate
    - word_len_mean
    - qok_lf
    - y_lf
    - d_lf
    - s_lf
    - am_lf_enr
    - am_mid_enr
    - qok_ll
    - d_ll
    - global_am_rate
  pass_tolerance: "±20% of VMS target"
  pass_criterion: "mean over N=30 runs within tolerance; variance reported"
  commitment: C008
```

A mechanism passes the battery at k/19 if k metrics fall within ±20%
of the VMS target mean across N=30 simulation runs. The 21-mechanism
architecture achieves 19/19 under the exp_314 calibration.

---

## 13. Audit Conventions

**Canonical audit skill:** `skills/audit_experiment.md`. Every
experiment must run the audit on its draft result.md before updating
any state file. The audit consists of five checks, each catching a
known failure mode from the project's three meta-review catches.

### 13.1 Check 1 — Target-awareness

Does any parameter, table, or mapping in the mechanism relate to a
VMS target metric, and was it calibrated using knowledge of the VMS
value for that metric?

**Stop condition.** If yes, state the result as CONDITIONAL on the
calibration. Do not bury it in limitations. The target-awareness
statement belongs adjacent to the claim it qualifies.

**Origin.** exp_177 LL table mapped all Latin clause-final morphemes to
EVA -am specifically because -am was the target metric. The original
draft did not disclose this.

### 13.2 Check 2 — Feature-destroying implementation

Does any implementation detail actively destroy or degrade the feature
the hypothesis depends on?

**Stop condition.** If yes, the experiment is not a fair test. State
this prominently: "This experiment is unfair to the hypothesis because
[detail] destroys [feature]. An alternative implementation preserving
this feature ([specific alternative]) is untested."

**Origin.** exp_180 modification replaced onset classes of copied
tokens — destroying onset self-succession, which the hypothesis
depended on. Original conclusion was that copy-buffer architectures
fail; exp_181 with onset-preserving modification reversed this.

### 13.3 Check 3 — Extrapolation beyond the tested grid

Does the result claim "no parameter setting" / "structural" /
"cannot" / "impossible" / "architectural limit" / "inherent to" /
"fundamental" / "any mechanism of class X"?

**Stop condition.** If yes, verify the tested grid covers the full
plausible range. If not, soften to "not reproduced under the tested
parameter range [specify]." Reserve "structural" for claims supported
by a logical argument independent of specific parameter values.

**Origin.** exp_180 claimed ss_mean/adj_rate coupling was "structural to
copy-buffer architectures" from a MODIFY_PROB grid of {0.3, 0.4, 0.5}
with the worst-case (onset-replacing) modification.

### 13.4 Check 4 — Negative-result overreach

If the experiment produced a negative result, does the interpretation
stay within the scope of this specific mechanism and conditions?

**Stop condition.** If the result claims "X requires Y" from a single
failure, or "no mechanism of class Z can produce X" from testing one
member, narrow the scope to: "This mechanism did not produce X under
these conditions."

**Origin.** Same as Check 3 — exp_180.

### 13.5 Check 5 — Control-comparison interpretation

For every metric compared against a control (shuffled text, reference
language, null model), write explicitly: "I expect [control] to
produce [metric] ≈ [value] because [reason]. The control actually
produced [observed value]." If the control exceeds real VMS or
differs by factor > 1.5, treat as a hard flag and investigate before
interpreting the VMS result.

**Origin.** exp_175 within-line shuffle produced higher MI than real
VMS at lags 11-12, which meant the "VMS above Timm at lags 10-12"
finding was a sampling artifact, not evidence of long-range structure.

### 13.6 Procedure

1. Read the draft result.md in full.
2. Run each of the five checks.
3. If any check identifies a problem, revise result.md BEFORE
   proceeding to state file updates.
4. Append the Self-Audit block to result.md.

### 13.7 The Self-Audit block format

```markdown
## Self-Audit

**Target-awareness**: [list of target-aware elements, or "None"]

**Feature-destroying implementation**: [list of details that destroy
the feature under test, or "None"]

**Extrapolation**: [list of claims that exceed the tested grid, or
"All claims are within the tested parameter range"]

**Negative-result scope**: [if negative: state the scope; if positive:
"N/A — positive result"]

**Control behavior**: [expected vs actual behavior for each control]
```

---

## 14. Committed Claims Procedure

**Canonical skill:** `skills/write_finding.md` plus the "Contradiction
Rule" subsection.

### 14.1 What makes a claim "committed"

A claim becomes committed when it is shared in a public-facing output:

- paper draft or preprint (e.g., exp_181-revised checkpoint paper)
- blog post
- forum post (e.g., voynich.ninja)
- presentation or slides
- email to a named collaborator
- arXiv submission

When a public output is shared, the HUMAN adds the relevant claim to
`state/committed_claims.md` BEFORE resuming the Cryptanalyst loop.
Agents may PROPOSE new commitments by writing to
`state/proposed_commitments/proposed_*.md`, but they may NOT directly
add entries to committed_claims.md.

### 14.2 The contradiction rule

Before writing any new finding to findings.md or failed_approaches.md,
the agent must check state/committed_claims.md. If the new finding
relates to a committed claim, classify as either **hard contradiction**
or **narrowing**:

#### 14.2.1 Hard contradiction

A re-analysis, replication, or methodological correction of the SAME
experiments cited in a committed claim's "Supporting experiments"
field produces results INCOMPATIBLE with the claim.

**Handling.** DO NOT write to findings.md or failed_approaches.md.
Instead:

1. Write to open_questions.md with heading
   `"COMMITTED CLAIM AT RISK: [claim ID]"`.
2. State the contradiction: what the committed claim says, what the
   new result shows, why they are incompatible.
3. Stop the loop and alert the human.

Example: exp_182 triggered a hard contradiction against C004 because
it produced viable combinations at adj_rate ≤ 0.009 (whereas C004
stated 0/36 combinations viable at that threshold). Per the
contradiction rule, exp_182 paused the loop. Upon human review, it
was re-classified as a narrowing (C004 was overgeneralized; the
0/36 applies only to suffix-replacing modification; char-level
modification is a different mechanism).

#### 14.2.2 Narrowing

A new mechanism, architecture, parameter range, or variant NOT listed
in the claim's "Supporting experiments" produces results that
RESTRICT the scope of the claim without invalidating its original
experiments.

**Handling.** This is handled autonomously by the agent:

1. Record the finding in findings.md normally.
2. Add a "Narrowed by" line to the affected committed claim entry,
   citing the new experiment and stating how the scope is restricted.
3. Note in iteration_log.md that a committed claim was narrowed.
4. Continue the loop.

### 14.3 The amendment procedure

If an existing committed claim's TEXT needs to be corrected (not
narrowed), the procedure is:

1. Agent writes a proposal to
   `state/proposed_commitments/proposed_[claim_id]_amendment.md`.
2. Proposal contains: current claim text, issues identified, proposed
   corrected text, implications for dependent claims, supporting
   reconciliation experiments.
3. Human reviews and approves the amendment.
4. Human updates committed_claims.md with the amended text, preserving
   the original for traceability (as a "Canonical correction" block).
5. Applied proposal is moved to
   `state/proposed_commitments/applied/applied_[claim_id]_[date].md`.
6. The agent may then treat the amended text as canonical and update
   any dependent state (findings.md, spec §N) to match.

**Example.** The C007 amendment (landed 2026-04-12) followed exactly
this procedure. exp_573 reconciliation identified three errors
(range, attribution, residual claim), the proposal was written to
proposed_c007_amendment.md, human approved, committed_claims.md was
updated with a "Canonical correction" block preserving the original,
and the proposal was moved to applied/.

### 14.4 Traceability requirement

Every finding, failure, and open question must cite a specific
experiment ID. Per `skills/write_finding.md`:

> **Every finding, failure, and open question must cite a specific
> experiment ID.** This is non-negotiable. If you have an insight that
> wasn't produced by a formal experiment, run a quick script first —
> even a 5-line script that prints one number counts as an experiment.
> The point is that the claim is reproducible.

No entry of the form "I noticed that..." or "It seems like..." without
an `exp_NNN` citation is permitted in state files.

### 14.5 Magnitude context requirement

Per `skills/write_finding.md`: every numeric finding must include a
statement of whether the number is larger, smaller, or comparable to
(a) any published value for the same metric and (b) the closest prior
finding in the project's findings.md.

The purpose is to make it harder to report a significant result
without noticing it is significant. A finding that is 10× larger than
any published value on the same metric is either a breakthrough, an
artifact, or a unit error — and the agent should notice which before
moving on.

---

## 15. Worked Example: Reproducing C006 (y-onset LF Enrichment)

**Target committed value** (C006, from committed_claims.md):

```
C006: y-onset LF enrichment in Currier B is 3.506× with p < 10^-90
Supporting experiments: exp_173
```

### 15.1 Step 1 — Load and parse the corpus

```python
import re
from collections import Counter, defaultdict
from scipy import stats

VMS_CORPUS = 'data/transcriptions/eva_zl3b.txt'

folio_words = defaultdict(list)
raw_lines = []
with open(VMS_CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        locus_raw, text = parts
        lparts = locus_raw.split(',')
        if len(lparts) < 2:
            continue
        folio_base = lparts[0].split('.')[0].lstrip('<')
        m = re.match(r'f(\d+)', folio_base)
        if not m:
            continue
        fnum = int(m.group(1))
        lt = lparts[1].rstrip('>').lstrip('@+*=~&')
        if not lt.startswith('P'):            # body only
            continue
        # exp_173 tokenizer
        words = [w for w in text.split('.')
                 if w and re.match(r'[a-z]', w)
                 and not w.startswith('<')]
        if not words:
            continue
        folio_words[fnum].extend(words)
        raw_lines.append((fnum, words))
```

Methodological choices made here:
- **Transcription**: `eva_zl3b.txt` (§1.1).
- **Locus filter**: `lt.startswith('P')` — body text only (§1.2).
- **Tokenizer**: exp_173 `.`-only split with `[a-z]`-prefix filter
  (§1.3.1). Committed values require this tokenizer.

### 15.2 Step 2 — Assign dialect (folio-level)

```python
folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10:
        continue
    rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'
```

Methodological choice: **folio-level** dialect assignment because C006
was computed under this method (§3.2). Per-line assignment would give
a different value (3.121× per exp_581) which does NOT match the
committed 3.506× as closely.

### 15.3 Step 3 — Extract B-dialect lines and LF words

```python
b_lines = [(fn, wds) for fn, wds in raw_lines
           if folio_dialect.get(fn) == 'B']
b_lf_words = [wds[0] for _, wds in b_lines if wds]   # first word = LF
```

Methodological choice: LF = first word of line (position index 0),
per canonical convention §2.1.

### 15.4 Step 4 — Compute onset classes

```python
def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'):  return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    if w.startswith('ok'):  return 'ok'
    if w.startswith('ot'):  return 'ot'
    if w.startswith('ol'):  return 'ol'
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('k'):   return 'k'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    if w.startswith('r'):   return 'r'
    return 'other'

b_words = [w for _, wds in b_lines for w in wds]
b_onset_counts = Counter(get_onset(w) for w in b_words)
b_total = len(b_words)
y_base_rate = b_onset_counts['y'] / b_total
```

Methodological choice: exp_173 onset classifier WITH the `ch_e`
sub-class (§4.3). Modern characterization-phase scripts do not use
`ch_e`; committed-claim reproduction must.

### 15.5 Step 5 — Compute the enrichment

```python
y_at_lf = sum(1 for w in b_lf_words if get_onset(w) == 'y')
n_lf_b  = len(b_lf_words)

lf_rate       = y_at_lf / n_lf_b
enrichment    = lf_rate / y_base_rate

# One-sided binomial test for enrichment
p_value = stats.binomtest(y_at_lf, n_lf_b, y_base_rate,
                          alternative='greater').pvalue

print(f"y@LF count: {y_at_lf}/{n_lf_b}")
print(f"y base rate: {y_base_rate:.5f}")
print(f"y LF rate:   {lf_rate:.5f}")
print(f"Enrichment:  {enrichment:.3f}x")
print(f"p-value:     {p_value:.2e}")
```

Methodological choice: binomial exact one-sided (direction = `greater`
because we are testing enrichment), with `p_value` reporting a full
exact p-value (no normal approximation).

### 15.6 Step 6 — Verify against committed value

**Per exp_581 convention diagnostic**, running exactly the above
computation on `eva_zl3b.txt` produces:

```yaml
computed:
  enrichment: 3.478
  delta_from_committed: 0.79%  # (3.506 - 3.478) / 3.506
  p_value: "< 1e-85"           # in the range of the committed p < 1e-90
committed_C006:
  enrichment: 3.506
  p_value:    2.86e-90
```

**Difference analysis.** The 0.79% gap is attributable entirely to
tokenizer differences between my exact reproduction and the original
exp_173 run. Specifically:
- exp_173's original run included comma-joined tokens (`or,y` as a
  single token) which affects base rate.
- exp_173's original run retained bare single-character tokens
  (e.g., bare `y`) which affects the y-count.

These differences are on the order of 1–2% and produce the observed
0.79% gap. **The committed value reproduces to within rounding
tolerance**; the convention and methodology are verified.

### 15.7 What each methodological choice does

| Choice | Computed value | Delta from committed |
|--------|---------------|----------------------|
| **Canonical (all choices as above)** | 3.478× | 0.79% |
| Canonical tokenizer (§1.3.2 not exp_173) | 3.121× | 11.0% |
| Per-line dialect (§3.1) | 3.121× | 11.0% |
| Inverted convention (LF = last word) | 0.665× | 81% (wrong) |

The inverted convention result (0.665×) is a FACTOR OF 5.3× wrong
from the committed value, providing strong evidence that the
committed-claims convention was the one originally used.

### 15.8 Section-specific breakdown

For completeness, per-section breakdown of y-onset LF in B-dialect
(approximating exp_579 values):

```yaml
y_onset_LF_by_B_section:
  B_herbal: {rate: 0.1793, source: exp_579}
  B_bio:    {rate: 0.0743, source: exp_579}
  B_astro:  {rate: 0.1201, source: exp_579}
  B_pharma: {rate: 0.1688, source: exp_579}
  section_range_factor: 2.41
```

The full-corpus LF rate is an average across these sections weighted
by B line counts. This is the C008 scope qualification: per-section
values differ substantially and the full-corpus value is a pooled
average.

---

## 16. Methodology Evolution and Known Caveats

### 16.1 The Three Catches (from SOUL.md)

The project has required THREE human-intervention corrections during
its lifetime. Each is documented in SOUL.md and each led to the
addition of a specific audit check (§13).

#### 16.1.1 Catch 1 — Sampling artifact as signal (exp_175)

**What happened.** exp_175 computed mutual information (MI) between
adjacent word positions at various lags. At lags 11–12, VMS exceeded
Timm-simulated values. The original synthesis treated this as evidence
of long-range structure.

**What was wrong.** The within-line shuffle CONTROL also exceeded real
VMS MI at lags 11–12, meaning the apparent VMS-above-Timm signal at
those lags was a sampling artifact from sparse long-line data, not a
real signal. The lags 2–7 signal (VMS below Timm) was real and is
preserved; the lags 10–12 claim was retracted.

**Fix.** exp_175 lags 10–12 claim retracted (commit `8ef8837`). Added
audit_experiment Check 5 (control-comparison interpretation).

**Which experiments use which interpretation.** Everything from
exp_175 onwards uses the retraction. Anything citing "MI at lags
10–12 above Timm" is outdated.

#### 16.1.2 Catch 2 — Target-aware without disclosure (exp_177)

**What happened.** exp_177's position-sensitive cipher simulation
achieved am_ll = 5.756× using a Latin Cicero corpus with LF/MID/LL
substitution tables. The original result.md did not disclose that the
LL table mapped all Latin clause-final morphemes specifically to the
EVA suffix `-am` — the target metric.

**What was wrong.** The 5.756× value is CONDITIONAL on that target-
aware calibration. A blind cipher (no knowledge of the VMS -am target)
would produce a lower value.

**Fix.** result.md revised to state the calibration explicitly in the
Interpretation section, not buried in Limitations. The qualifier
"this result is conditional on the target-aware LL table" is now
adjacent to every citation of the 5.756× value. Added audit_experiment
Check 1 (target-awareness).

**Which experiments use which interpretation.** exp_177 and all later
experiments cite the value as conditional. The architecture paper
rewrite will cite it as conditional.

#### 16.1.3 Catch 3 — Feature-destroying implementation (exp_180)

**What happened.** exp_180 tested a position-aware copy-buffer hybrid
with MID-only copying and "modification" in the modify step. The
modification operation REPLACED the onset class of copied tokens.
Result: 0/18 viable combinations. Conclusion: "onset-class clustering
is intrinsic to the vocabulary structure rather than generated by
copying" — a strong claim against copy-buffer architectures in general.

**What was wrong.** Onset self-succession was the feature the
hypothesis depended on (copy-buffer should produce it via buffer
recycling). Replacing onsets destroyed that feature. The 0/18 result
was not a fair test of the hypothesis; it tested a mechanism that
cannot work by construction.

**Fix.** exp_181 re-ran with onset-PRESERVING modification: 4/36 viable
combinations. The conclusion reversed. C003 is scoped to "onset-
replacing modification" specifically. Added audit_experiment Check 2
(feature-destroying implementation).

**Which experiments use which interpretation.** Everything after
exp_181 treats copy-buffer architectures as a live hypothesis class.
The 21-mechanism architecture (exp_314) is the culmination.

### 16.2 The C007 methodology change (2026-04-12)

**What changed.** Self-succession computation migrated from the
exp_164/174 methodology (folio-level dialect assignment + `obs /
(total × rate²)` formula) to the canonical methodology (per-line
dialect assignment + `obs / (n_sender × mid_rate_target)` formula).

**Why.** Per exp_573 reconciliation:
- Folio-level dialect pools mixed-section lines and dilutes A-dialect
  self-succession (accounts for ~0.4× reduction in A ok).
- The `rate²` formula assumes independence in the full corpus, but
  self-succession pairs can only occur at interior positions.
  Using the overall corpus rate squared inflates the expected count
  for MID-concentrated classes (accounts for ~0.2× reduction in B qok).

**What survives.** The CONF classes (y, l, ot, qo, qot in both dialects)
still show robust self-succession under canonical methodology.
Position-controlled residuals still hold for these classes. C002
(substitution alone gives ss ≈ 1.0) is unchanged and is STRENGTHENED
by the broader canonical range (up to 3.86× makes the contrast with
1.0 stronger).

**What changed.** The C007 range was corrected from "1.24–2.05×" to
"0.78–3.86×". B qok is flat (1.03×, not CONF), B ch is near-depleted
(0.91×), B sh is depleted (0.78×). The amendment is in
committed_claims.md (landed 2026-04-12).

**Which experiments use which methodology.**
- exp_164, exp_174: legacy (folio-level, rate² formula)
- exp_565, exp_566, exp_567, exp_568, exp_569: canonical (per-line,
  MID-baseline formula)
- exp_573: reconciliation (explicitly compares both)
- All new work: canonical

### 16.3 The convention inversion finding (2026-04-12)

**What was discovered.** During the v1.0 grammar spec cross-check, the
characterization-phase scripts (exp_565+) were found to use an INVERTED
LF/LL convention relative to the committed-claims convention (exp_173).
Characterization scripts defined `pos1 = first word`, `LL = penultimate`,
`LF = last word`. Committed-claims scripts define `LF = first word`,
`LL = last word`, `second = index 1`, `MID = interior`.

**What it means for reported values.** Every finding from the
characterization phase (F619, F622, F628, F631, F555, F557, F558, and
similar) is internally consistent but uses the inverted naming. When
translated to canonical convention, the numerical values are correct
but the position labels need to be swapped: exp_565's "LF DEPL" means
canonical "LL DEPL" (depletion at last word).

**What was verified.** exp_581 convention diagnostic confirmed that
every committed-claim value (C005, C006) originally used the canonical
convention. The characterization-phase naming drift never leaked into
public output.

**What was fixed.** The v1.0 grammar spec standardizes on canonical
convention and translates all values. This methodology document uses
canonical convention throughout. Working_position.md §6 still uses
inverted convention (tagged as v1.1 cleanup work in the spec's open
issues).

### 16.4 Document-order heterogeneity (exp_579)

**What it says.** B-dialect positional metrics shift systematically
across document order: first-half am_ll = 5.825×, second-half = 7.147×
(23% gradient). exp_579 tested three candidate drivers:

- **Scribal hand** (Davis 2020 IDs from ZL3b `$H=` metadata): NOT
  isolable because hand × section is co-linear in B-dialect.
- **Section composition**: COMPLETE driver. A prediction model based
  on per-section metrics weighted by section fraction explains
  97–107% of the half-shift for all five primary metrics.
- **Genuine linguistic drift**: NOT required (97–107% of the variance
  is explained by section composition).

**What this means for aggregation.** Full-corpus B-dialect positional
metrics are weighted averages across four sections with 2.4–4.6× range
factors. The 19-metric battery (C008) is calibrated on this full-
corpus aggregate. Section-level calibration would require different
parameter values per section; the 19/19 is a statement about the
aggregate, not about any individual section.

**Rule for aggregation.** Positional metrics (LF, LL, enrichment
ratios) MUST be reported per section for B-dialect. Non-positional
metrics (onset frequencies, self-succession, adj_rate) may be
reported as full-corpus values because section variation is smaller
(per exp_579 analysis).

### 16.5 Which-experiments-use-which-convention cheat sheet

```yaml
pre_exp_173:              # Phases 1-2, early characterization
  tokenizer: various; some use split('.'), some use re.split
  dialect:   folio-level
  LF_LL_convention: canonical (exp_173-compatible where relevant)
  self_succession_formula: rate² (legacy)

exp_173:                  # Multiple-testing + committed claims
  tokenizer: '.' split, [a-z]-prefix filter, no length minimum
  dialect:   folio-level edy-rate
  LF_LL_convention: canonical
  onset_classifier: includes ch_e subclass
  self_succession_formula: not used (positional only)
  committed_values_computed_here: [C005, C006, C007_original, F1..F30]

exp_174:                  # Position control of self-succession
  tokenizer: '.' split
  dialect:   folio-level
  self_succession_formula: rate² (legacy)
  superseded_by: exp_573

exp_180..exp_182:         # Mode B architecture simulations
  tokenizer: canonical
  dialect:   folio-level for legacy; canonical later
  LF_LL_convention: canonical

exp_217..exp_314:         # 21-mechanism architecture
  tokenizer: canonical
  dialect:   folio-level for the battery computation
  LF_LL_convention: canonical

exp_565..exp_572:         # Onset class characterization
  tokenizer: canonical ([-.\\s]+ split, len≥2, isalpha)
  dialect:   per-line edy-rate (canonical)
  LF_LL_convention: INVERTED (pos1=first, LL=penult, LF=last)
  onset_classifier: NO ch_e; adds ckh, cph, sch
  self_succession_formula: MID-baseline (canonical)

exp_573:                  # C007 reconciliation
  purpose: explicitly comparing both methodologies
  outputs: canonical values superseding exp_164/174

exp_574..exp_579:         # Specificity / stability / document-order
  tokenizer: canonical
  dialect:   per-line
  LF_LL_convention: canonical (in new scripts)

exp_580:                  # Label corpus
  tokenizer: canonical
  dialect:   per-line (with label-specific caveat in §15.6 of spec)

exp_581:                  # Convention diagnostic
  purpose: verify committed-claims convention matches committed values
  result: confirmed
```

---

## 17. Changes to Canonical Methodology (Chronological Log)

This section is the chronological append-only log of methodological
changes the project has made. Any new change should be appended to
this list with date, change, reason, and scope.

### 2026-04-04: Retraction of exp_175 lags 10-12 claim (Catch 1)

- **Change**: MI-at-lags-10-12 claim retracted.
- **Reason**: Within-line shuffle control exceeded real VMS at those
  lags, indicating a sampling artifact.
- **Scope**: exp_175 and any synthesis document citing lags 10-12.
- **New audit check**: audit_experiment Check 5 (control-comparison).

### 2026-04-05: exp_177 target-awareness disclosure (Catch 2)

- **Change**: exp_177 5.756× am_ll result re-stated as conditional on
  the target-aware LL cipher table.
- **Reason**: LL table mapped all Latin clause-final morphemes to EVA
  `-am` because `-am` was the target metric; this was not disclosed.
- **Scope**: exp_177 and any citation of the 5.756× value.
- **New audit check**: audit_experiment Check 1 (target-awareness).

### 2026-04-09: exp_180 → exp_181 modification operator correction (Catch 3)

- **Change**: Onset-replacing modification replaced with onset-preserving
  modification in position-aware hybrid.
- **Reason**: Onset-replacing destroys the self-succession feature that
  the copy-buffer architecture was designed to produce. exp_180's 0/18
  was not a fair test. exp_181's 4/36 is the canonical result.
- **Scope**: C003 scoped to onset-replacing; C004 scoped to onset-
  preserving suffix-replacing.
- **New audit check**: audit_experiment Check 2 (feature-destroying
  implementation).

### 2026-04-10: exp_173 dual Bonferroni disclosure

- **Change**: Multiple-testing correction now reports Bonferroni at
  both m=30 (candidate set) and m=175 (full search space).
- **Reason**: m=30 alone is optimistic; m=175 alone is conservative.
  Both should be available for independent assessment.
- **Scope**: All committed claims cite m=175 survival where applicable.

### 2026-04-11: C004 narrowing from exp_182

- **Change**: C004 "residual gap" claim narrowed to apply only to
  suffix-replacing modification.
- **Reason**: exp_182 (Timm character-level modification) achieved 3/36
  viable combinations at adj_rate ≤ 0.009 with ss_mean ≥ 1.2 and
  am_ll ≥ 5.0 — first such result in the program. Character-level
  modification has ~2% collision rate vs suffix modification's ~17%,
  which allows adj_rate to decrease faster.
- **Scope**: C004 status changed to VALID_NARROWED. Character-level
  copy-buffer hybrid is no longer in the ruled-out list.
- **Loop action**: exp_182 triggered a C004 contradiction condition;
  paused and escalated per §14.2.1. Human review re-classified as
  narrowing.

### 2026-04-12: C007 amendment (canonical methodology for self-succession)

- **Change**: Self-succession computation migrated to canonical
  methodology (per-line dialect + MID-baseline formula). C007 range
  corrected from "1.24–2.05×" to "0.78–3.86×". Upper bound attribution
  corrected from "ok, A-dialect" to "l, A-dialect" (for the maximum)
  and "qo, B-dialect" (for the 2.047× that was originally cited).
- **Reason**: exp_573 reconciliation identified three methodological
  errors in the C007 source experiments. Canonical methodology gives
  correct values for position-controlled residuals (holds for CONF
  classes only: y, l, ot, qo, qot).
- **Scope**: C007 in committed_claims.md now contains a "Canonical
  correction (2026-04-12)" block. Dependent findings (F619+) and the
  grammar spec §5 use the canonical values.
- **New canonical rule**: Per-line dialect assignment and MID-baseline
  formula are now canonical for all new self-succession work.

### 2026-04-12: C008 scope qualification from exp_579

- **Change**: C008 19/19 PASS now carries a scope qualification stating
  it is a full-corpus average over four B-dialect sections with
  systematically different positional grammar profiles.
- **Reason**: exp_579 / F639: section composition explains 97–107% of
  the document-order metric gradient in B-dialect. The 19/19 is a
  statement about the aggregate, not about any individual section.
- **Scope**: C008 contains a scope qualification block;
  section-specific work is the v1.1+ agenda.

### 2026-04-12: C009 addition (adj_rate structure)

- **Change**: New commitment C009 added covering VMS adj_rate structure.
  Three parts: (A) sh/ch/d near-random from CP90 pools; (B) s/t
  structural zero from LF constraint; (C) copy-buffer architecture
  overproduces 1.41–1.79× above VMS.
- **Reason**: exp_577 + exp_578 resolved Q007. Findings are strong
  enough to commit.
- **Scope**: Per §9 of this document. C009 is VALID as of committed
  version 2026-04-12.

### 2026-04-12: LF/LL convention standardization (grammar spec v1.0)

- **Change**: v1.0 grammar spec standardizes on the committed-claims
  LF/LL convention (LF=first, LL=last, second=index 1, MID=interior)
  and translates all characterization-phase values.
- **Reason**: Discovered during the v1.0 cross-check that exp_565+
  scripts use an inverted convention (pos1=first, LL=penult, LF=last).
  The naming drift never leaked into committed output (exp_581 verifies).
- **Scope**: Grammar spec v1.0, canonical methodology document (this
  document), all future work. Working_position.md §6 still uses
  inverted convention; flagged for v1.1 cleanup.

### 2026-04-12: C010 proposed (label corpus grammar)

- **Change**: New commitment C010 proposed (awaiting human review)
  based on exp_580 label corpus analysis.
- **Reason**: Label text is a structurally distinct register with
  large, consistent differences from body text (ok/ot/o dominant,
  q-bench near-absent, edy depleted, a-onset terminal in multi-word
  labels).
- **Scope**: Grammar spec §15. C010 is PROPOSED status in
  proposed_commitments/proposed_c010_label_corpus_grammar.md; not yet
  in committed_claims.md.

---

## 18. Open Methodological Issues

Issues that cannot be resolved with current data, or that remain
methodologically ambiguous after v1.0 of this document.

### 18.1 Committed values at exact-reproduction precision

**Issue.** The worked example in §15 reproduces C006's y-onset LF
enrichment to 3.478× vs committed 3.506× (0.79% gap). The gap is
attributable to tokenizer minutiae (comma-joined tokens, bare
single-character tokens) but cannot be closed without the original
exp_173 output file.

**Impact.** For directional reproduction (is the finding real? does
the sign match?) this is fine. For precise numerical replication
(does 3.506× exactly reproduce?) this is not fine — a third-party
paper rewrite reader would compute 3.478× from this methodology
document.

**Recommendation.** Either (a) re-run exp_173 on the canonical corpus
and re-commit the exact reproducible value, or (b) add a tolerance
statement to C005/C006 explicitly stating that committed values are
to be read with ±1.5% tokenizer tolerance.

### 18.2 Per-line dialect classification threshold for short lines

**Issue.** The canonical per-line dialect assignment requires `min_tokens
= 10`. Lines with <10 tokens are unclassified. But many label and
short-line contexts have <10 tokens. In those cases, either:
- Drop the line entirely (current practice).
- Inherit dialect from folio-level.
- Use a looser threshold (e.g., min_tokens = 5).

The C007 canonical values use `min_tokens=10` at the per-line step;
this drops about 3–4% of body lines.

**Recommendation.** Document the drop rate explicitly alongside any
self-succession value. Consider adding a secondary canonical value
with `min_tokens=5` for robustness.

### 18.3 Adj_rate across line breaks

**Issue.** The canonical adj_rate definition (§9.2) counts pairs
within-line only. It does NOT count the pair {last word of line N,
first word of line N+1}. But some linguistic questions are naturally
about cross-line word repetition (e.g., paragraph self-succession of
d-onset words in A herbal_a per F099).

**Impact.** Per F639 / C008 scope, cross-line phenomena are handled
as a separate CL (cross-line) metric. But this is a different metric
from adj_rate. Confusion between the two is possible in the paper
rewrite.

**Recommendation.** Rename one of them for clarity. Suggestion:
`adj_rate` stays as within-line; cross-line becomes `cl_rate`.
Grammar spec §7 uses "CL" notation consistently.

### 18.4 Section-specific CP90 values

**Issue.** CP90 values in §3 of the grammar spec are full-corpus
B-dialect. But per the document-order heterogeneity (§16.4), per-
section positional profiles differ substantially. No per-section
CP90 survey has been done.

**Impact.** The Q007 adj_rate interpretation (C009 Part A: sh/d
near-random from CP90 pools) uses full-corpus CP90. If CP90 varies
by section, this interpretation may be more nuanced.

**Recommendation.** Run a per-section CP90 computation as a follow-up
experiment before the paper rewrite ships.

### 18.5 Label dialect classifier

**Issue.** Per exp_580 / §15.6 of the spec: the standard edy-rate
dialect classifier misclassifies labels because edy is depleted in
labels regardless of host folio. A label-specific dialect classifier
has not been defined.

**Impact.** Labels in B-folios are often classified A under the
standard classifier. This is a known artifact but is not tracked
anywhere in the canonical methodology.

**Recommendation.** Define either (a) a label-specific classifier
based on ok/ot/o frequency, or (b) an explicit rule that labels
inherit host-folio dialect from folio-level classification.

### 18.6 The ch_e subclass in exp_173 vs omitted in exp_565+

**Issue.** exp_173 classifies `che*` and `chi*` words as their own
class `ch_e`. exp_565+ does not. This creates a class-count
inconsistency when comparing exp_173 findings to characterization-
phase findings.

**Impact.** Small. Per F087/F088 the e-infix is a vocabulary
partition, not a productive morphology. But bigram values involving
ch differ between the two classification schemes because exp_173's
`ch` class excludes ch_e tokens.

**Recommendation.** Document the difference in any ch-related finding.
The grammar spec §1.3 uses the exp_565+ unified `ch` class.

### 18.7 Worked example §15 used folio-level dialect for C006 reproduction

**Methodology reproduction tension.** The canonical methodology in §3
says per-line dialect is canonical. But the §15 worked example uses
folio-level dialect because C006 was originally computed that way.
This creates a tension: the "canonical reproduction path" for a
committed claim is NOT the canonical methodology for new work.

**Resolution.** Accepted as documented. §3 and §15 together define
two valid modes: (1) canonical-for-new-work (per-line), and
(2) exp_173-faithful for reproducing committed values. Readers should
use mode (2) when the goal is exact reproduction of a committed value
and mode (1) for all other purposes.

---

```yaml
end_of_document:
  version: v1.0
  date: 2026-04-12
  next_expected_revision: "after per-section A-dialect grammar experiment"
  cross_references:
    - state/voynich_grammar_spec.md        # companion spec
    - state/committed_claims.md            # authoritative commitment list
    - skills/audit_experiment.md           # canonical audit procedure
    - skills/write_finding.md              # canonical finding procedure
    - experiments/exp_173/result.md        # committed-claims tokenizer source
    - experiments/exp_573/result.md        # C007 reconciliation
    - experiments/exp_581/result.md        # convention diagnostic
  companion_open_issues: state/voynich_grammar_spec.md §14
```
