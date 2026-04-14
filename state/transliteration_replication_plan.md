# Transliteration Replication — Project Plan

```yaml
document_type: scoping_plan
document_version: v1.0
date: 2026-04-14
status: scoping gate for transliteration replication sessions
produced_by: planning session (no experiments run)

companion_documents:
  - state/preregistration_transliteration_and_specificity_thresholds.md   # the thresholds
  - state/canonical_methodology.md                                        # ZL3b-native methodology
  - state/voynich_grammar_spec.md                                         # findings to be replicated
  - state/committed_claims.md                                             # C005, C006, C008 anchor
  - data/transcriptions/README.md                                         # files-on-disk inventory

gate_for: "subsequent Sonnet priority sessions executing the replication experiments"
purpose: |
  Specify exactly what new infrastructure is needed, which mappings
  require domain judgment, which of the five pre-registered findings
  are portable to each target transliteration, and how to decompose
  the experimental work into sessions.
```

---

## 0. Executive Summary

Three target transliterations are candidate replication substrates for
the five Section 2 pre-registered findings:

| System       | File on disk                       | Size       | Coverage |
|--------------|------------------------------------|------------|----------|
| EVA ZL3b     | `data/transcriptions/eva_zl3b.txt` | 8510 lines | full     |
| EVA IT2a     | `data/transcriptions/eva_it2a.txt` | 5444 lines | partial  |
| v101 Claston | `data/transcriptions/v101_claston.txt` | 4485 lines | full     |

**EVA-basic is NOT a separate file on disk.** It is a tokenization
variant of the EVA family — same underlying character set as ZL3b/IT2a
but with different rules about what counts as a "letter" vs a
modifier / uncertainty marker / comment. The replication can produce
EVA-basic by applying a stricter tokenizer to ZL3b (or IT2a) rather
than by loading a new file. This is a crucial cost reduction: one new
tokenizer instead of a new corpus.

**Feasibility verdict:**

- **v101 replication: FEASIBLE** but substantial new infrastructure
  (tokenizer, onset classifier, suffix classifier). The central
  question is whether v101's single-glyph-per-character encoding
  collapses or preserves the ZL3b onset class distinctions.
- **EVA-basic replication: FEASIBLE and cheap.** It is a tokenizer
  variant of ZL3b. All onset/suffix classifiers can be reused; the
  only new code is a variant tokenizer.
- **ZL3a replication: DEFERRED.** ZL3a is not on disk. If available
  upstream from voynich.nu, it requires a fetch and the same work as
  ZL3b (the transliteration systems are sibling versions). The
  pre-registration lists ZL3a as "optional" — recommended to defer
  unless v101 or EVA-basic disagree with ZL3b, in which case ZL3a
  becomes the tiebreaker.

**Headline recommendation:** The optimal session sequence is TWO
priority sessions, but not the "one for v101, one for EVA-basic + ZL3a"
decomposition the user initially assumed. The better split is:

1. **Session R1 (EVA-basic)** — cheap, reuses ~90% of existing code,
   executes all five replication findings, produces a confident
   "Retained / Weakened / Failed" classification per finding. Serves
   as the EVA-family replication anchor.

2. **Session R2 (v101)** — the substantial one. Requires new tokenizer,
   onset classifier, and suffix classifier built from the v101
   character set and Claston's mapping table. Highest risk of
   infeasibility for Finding 3 (bigram invariants) and Finding 5
   (systematic suffix transformation) because v101's finer-grained
   glyph set may partition ch/sh/ok/ot/edy differently than EVA.

**ZL3a is held in reserve.** If R1 and R2 produce consistent classifications
for all five findings, ZL3a adds little marginal value. If they disagree,
R3 on ZL3a becomes the tiebreaker per the pre-registered "at least 2 of 3"
logic.

---

## 1. Transliteration System Inventory

### 1.1 EVA ZL3b (baseline)

```yaml
eva_zl3b:
  role: baseline; already used for all committed claims
  primary_reference: "Zandbergen & Landini, EVMT project (ongoing)"
  source_url: "https://www.voynich.nu/data/ZL3b-n.txt"
  local_file: "data/transcriptions/eva_zl3b.txt"
  format: "IVTFF Eva- 2.0 M 5"
  version: "3b dated 13/05/2025"
  size: "8510 lines, ~412 KB"
  coverage: "full manuscript"

  tokenization_conventions:
    alphabet: "26-char lowercase ASCII EVA alphabet (canonical)"
    character_model: "multi-character glyphs; 'ch', 'sh', 'cth' etc. represented as letter sequences"
    word_delimiter: "period ('.')"
    line_continuation: "trailing '-' or '=' depending on locus"
    ligatures: "not explicit; represented via letter pair conventions"
    paragraph_markers: "locus code P0/Pt prefixes"
    line_markers:
      "@Cc" : "circular running text"
      "La, Lz, Lf, Lc, Ln, Lt, Lp, L0" : "label loci"
      "Ri, Ro" : "radial circular labels"
    uncertainty_encodings:
      "[a:b]" : "alternative readings — canonical takes first"
      "{xx}"  : "uncertain span — canonical drops"
      "<!...>" : "non-Voynich annotation (e.g., Tepenecz signature)"

  known_quirks:
    - "Some lines have both `[a:b]` and `{xx}` uncertainty; canonical tokenizer handles [a:b] first"
    - "Single-character tokens like bare 'y' preserved in exp_173 tokenizer but dropped in canonical tokenizer (len≥2 filter)"
    - "Hyphen-joined and comma-joined tokens differ between exp_173 ('.'-only split) and canonical ('[-.\\s]+' split)"
    - "Dialect marker 'edy' / 'eedy' encoded as literal trigraphs / four-graphs"
```

### 1.2 EVA IT2a (secondary EVA variant)

```yaml
eva_it2a:
  role: secondary EVA; same alphabet as ZL3b, different curator
  primary_reference: "Unknown curator; 'IT' = Interlinear Text"
  source_url: "https://www.voynich.nu/data/IT2a-n.txt"
  local_file: "data/transcriptions/eva_it2a.txt"
  format: "IVTFF EvaT 2.0 M 3"
  version: "2a dated 02/02/2023 (modified 25/06/2025)"
  size: "5444 lines, ~342 KB"
  coverage: "partial or interlinear"

  tokenization_conventions: "identical to ZL3b in all material respects"

  known_quirks:
    - "Coverage may differ from ZL3b; verify folio set at session start"
    - "IT2a is sometimes referred to as a 'secondary' EVA but uses the same character set"
    - "Not typically cited as an independent replication target; used in voynich.nu for cross-checking uncertain readings"

  replication_status: |
    NOT RECOMMENDED AS A REPLICATION TARGET on its own. IT2a is an EVA
    variant, not a distinct transliteration system. If v101 is run and
    an EVA cross-check is desired, IT2a can serve as a low-cost
    robustness check by re-running the ZL3b pipeline against the IT2a
    file. But a result replicating under IT2a is NOT independent
    evidence from ZL3b; they are the same character system with
    different curators.
```

### 1.3 v101 (Claston)

```yaml
v101_claston:
  role: independent transliteration system; strongest replication target
  primary_reference: "Glen Claston, Voynich 101 system (early 2000s)"
  source_url: "https://www.voynich.nu/data/voyn_101.txt"
  local_file: "data/transcriptions/v101_claston.txt"
  file_encoding: "latin-1 (NOT UTF-8; contains 0x80–0xFF characters per extended ASCII)"
  format: "IVTFF-compatible; locus codes follow IVTFF conventions"
  size: "4485 lines, ~249 KB"
  coverage: "full manuscript"
  character_inventory_distinct: 172   # per working-tree verification 2026-04-14

  tokenization_conventions:
    alphabet: "single-character glyphs; each Voynich glyph is one character"
    character_model: "FINER-GRAINED than EVA; distinguishes variants that EVA merges"
    word_delimiter: "period ('.')"
    line_continuation: "trailing '-' or '='"
    paragraph_markers: "same IVTFF conventions as EVA files"
    uncertainty_encodings: "unknown — NOT DOCUMENTED in data/transcriptions/README.md; requires session task to confirm"

  known_quirks:
    - "Single-character-per-glyph. Where EVA writes 'ch' (2 chars), v101 writes one character (letter code 1)."
    - "172 distinct characters including ASCII digits, letters, symbols, and extended Latin-1 range (0x80–0xFF). This is the Voynich glyph inventory mapped to ASCII/Latin-1 codepoints."
    - "Claston's mapping table (ZL3b ↔ v101) exists but is not on disk. voynich.nu publishes a conversion table; must be fetched or reconstructed at session start."
    - "No 'multi-character onset' concept. ZL3b's 'qok' (3 chars) would be two v101 glyphs (q + K or similar)."
    - "Gallows variants that EVA merges (e.g., k variants 1, 2, 3) are distinct characters in v101. This is the primary reason to use v101 as a replication substrate — it can detect whether EVA's merging is hiding structural signal."

  known_infrastructure_deltas_from_EVA:
    - "Tokenizer: same period-split behavior but must be applied to the v101 character set"
    - "Onset classifier: MUST be rewritten. EVA's startswith('ch') becomes 'startswith(glyph_code_for_c-h)'. No letter fall-through."
    - "Suffix classifier: same rewrite. EVA's endswith('edy') becomes endswith(glyph_code_sequence_for_e-d-y)."
    - "Dialect classifier: edy-rate must be recomputed as the v101 glyph sequence for 'edy'"
```

### 1.4 ZL3a (earlier ZL version)

```yaml
zl3a:
  role: older version of the ZL EVA transliteration
  primary_reference: "Zandbergen & Landini, earlier revision"
  source_url: "https://www.voynich.nu/data/ZL3a-n.txt (presumed)"
  local_file: NOT ON DISK
  local_file_note: "must be fetched from voynich.nu before session R3"
  coverage: "full manuscript (presumed)"

  tokenization_conventions: "EVA family; essentially identical to ZL3b modulo specific corrections"

  known_quirks:
    - "Differs from ZL3b mainly in uncertainty annotations, some corrected readings, and line-break positions"
    - "Does NOT materially change the alphabet or onset/suffix classifier"
    - "Replication under ZL3a is a ROBUSTNESS check against curator-version drift within the EVA family, not an independent-system replication"

  replication_status: |
    DEFER. ZL3a is not on disk. The pre-registration lists it as
    optional. Recommended session policy: only fetch and run ZL3a if
    R1 (EVA-basic) and R2 (v101) disagree on any of the five
    findings. ZL3a is a tiebreaker, not a primary replicator.
```

---

## 2. ZL3b-to-Target Mapping Decisions

This section enumerates how the ZL3b onset classes map to each target
transliteration. The ZL3b onset classifier (`canonical_methodology.md`
§4.1) uses priority-ordered longest-prefix startswith matching on a
lowercase EVA letter sequence.

### 2.1 The ZL3b onset class inventory

Per `canonical_methodology.md` §4.1 and `voynich_grammar_spec.md` §1.1–1.22:

```yaml
zl3b_onset_classes:
  q_bench:
    qok: {prefix: "qok", length: 3}
    qot: {prefix: "qot", length: 3}
    qo:  {prefix: "qo",  length: 2}
  compound_gallows:
    cth: {prefix: "cth", length: 3}
    sch: {prefix: "sch", length: 3}
    ckh: {prefix: "ckh", length: 3}
    cph: {prefix: "cph", length: 3}
  ch_sh:
    ch: {prefix: "ch", length: 2}
    sh: {prefix: "sh", length: 2}
  o_prefixes:
    ok: {prefix: "ok", length: 2}
    ot: {prefix: "ot", length: 2}
    ol: {prefix: "ol", length: 2}
  single_char:
    d: 1
    s: 1
    y: 1
    k: 1
    t: 1
    l: 1
    r: 1
    p: 1
    f: 1
    a: 1
    o: 1
```

Total: 23 classes plus `other`. Priority order matters because longer
prefixes are checked first (qok before qo; cth before ch; sch before s).

### 2.2 Mapping to EVA-basic

```yaml
mapping_EVA_ZL3b_to_EVA_basic:
  relationship: "tokenization variant; same character set"
  definition_EVA_basic: |
    EVA-basic is a strict tokenization that drops all uncertainty
    encodings, transliteration alternations, and non-standard
    annotations. It uses the same 26-char EVA alphabet as ZL3b but
    with a tighter pre-filter:
      - Drop entire tokens containing '[', ']', '{', '}', or ','
      - Drop tokens with non-letter characters after ' / '.strip
      - Keep only tokens of length ≥ 1 whose characters are all from
        the canonical EVA letter set {a, c, d, e, f, g, h, i, k, l, m,
        n, o, p, q, r, s, t, v, x, y}
      - Same period-split word delimiter

  onset_class_mapping: IDENTITY
  suffix_class_mapping: IDENTITY
  priority_order_preserved: true

  expected_differences_vs_ZL3b:
    - "Token count DROPS by ~3–6% (tokens with uncertainty markers filtered out)"
    - "CP90 may drop slightly (uncertain word types removed)"
    - "Onset / suffix class distributions should shift by <1% per class"
    - "Enrichment ratios should replicate within ±3% of ZL3b values — tighter than the pre-registered tolerance"

  mapping_ambiguities: "None. EVA-basic is a strict subset of ZL3b tokens."

  implementation_cost: "TRIVIAL. One new tokenizer function; everything downstream reuses ZL3b classifiers unchanged."

  decision_for_session_R1: |
    EVA-basic tokenizer keeps all tokens whose characters are all in
    the canonical 26-char EVA alphabet AND have no uncertainty markers
    in the source text. The alternative token inside [a:b] is NOT
    taken — the entire token is dropped. This is stricter than the
    exp_173 tokenizer (which takes the first alternative) and yields
    a cleaner-but-smaller corpus.
```

### 2.3 Mapping to IT2a

```yaml
mapping_EVA_ZL3b_to_IT2a:
  relationship: "sibling EVA curator; character set identical"
  onset_class_mapping: IDENTITY
  suffix_class_mapping: IDENTITY
  priority_order_preserved: true

  expected_differences_vs_ZL3b:
    - "Coverage may differ (IT2a is partial or interlinear; unclear if full manuscript is present)"
    - "Some folios may be absent or have fewer lines"
    - "Uncertainty encodings may differ in detail"
    - "Enrichment values should replicate within ~5% of ZL3b where coverage overlaps"

  mapping_ambiguities: "None, modulo coverage differences."

  implementation_cost: "TRIVIAL. Reuse ZL3b loader with a different file path."

  replication_value: |
    LOW. IT2a is not an independent system; running it alongside ZL3b
    tests curator agreement, not transliteration-system agreement.
    Cited in the pre-registration as an optional check, not a primary
    replication target.
```

### 2.4 Mapping to v101

```yaml
mapping_EVA_ZL3b_to_v101:
  relationship: "independent transliteration system; different character model"
  character_model_difference: |
    EVA: multi-character glyphs. 'ch' = 2 EVA letters, 'cth' = 3.
    v101: single-character glyphs. Each Voynich glyph is one
    character (possibly outside ASCII).
  onset_class_mapping: NOT IDENTITY. Every ZL3b class must be mapped
    to a v101 character or character sequence.

  canonical_mapping_source:
    primary: "Glen Claston's conversion table (published on voynich.nu, also appears in Reeds/Child reference databases)"
    status_on_disk: "NOT PRESENT. Must be fetched or reconstructed at session R2 start."

  reconstructed_mapping_attempt_2026_04_14: |
    Based on known Claston conventions (from Voynich Ninja discussions
    and Reeds list archives). THIS IS NOT AUTHORITATIVE. Session R2
    must verify against Claston's published table before running.
    Flagged ambiguities below.

    ZL3b 'q'  → v101 '4'
    ZL3b 'o'  → v101 'o' (literal)
    ZL3b 'k'  → v101 'K' (capital; gallows variant 1)
    ZL3b 't'  → v101 'T' (capital; gallows variant 1)
    ZL3b 'p'  → v101 'P' (capital; platform gallows)
    ZL3b 'f'  → v101 'F' (capital)
    ZL3b 'c'  → v101 'c' (literal)
    ZL3b 'h'  → v101 'h' (literal; only appears in EVA as the 'h' of ch/sh/cth)
    ZL3b 's'  → v101 's' (literal)
    ZL3b 'd'  → v101 '8' (digit)
    ZL3b 'y'  → v101 '9' (digit)
    ZL3b 'a'  → v101 'a' (literal)
    ZL3b 'i'  → v101 'i' (literal; note: EVA 'iin' sequences map to specific v101 characters)
    ZL3b 'n'  → v101 'N' (capital)
    ZL3b 'l'  → v101 'l' (literal)
    ZL3b 'r'  → v101 '2' (digit)
    ZL3b 'e'  → v101 'e' (literal)
    ZL3b 'ch' → v101 'cc' or single character 'C' (AMBIGUOUS — see below)
    ZL3b 'sh' → v101 single character; typically 'S' or a specific variant
    ZL3b 'cth'→ v101 single character (c-t-h ligature)
    ZL3b 'ckh'→ v101 single character (c-k-h ligature)
    ZL3b 'cph'→ v101 single character (c-p-h ligature)
    ZL3b 'sch'→ v101 single character (s-c-h ligature)

  ambiguity_flag_ch_vs_cc: |
    Whether v101 treats EVA 'ch' as a single glyph or as two depends
    on which Claston variant. Some v101 tables use 'cc' (two chars)
    for the 'ch' ligature; others use a single capital character 'C'.
    This decision MATERIALLY affects replication of Findings 1 and 3,
    because the onset 'ch' in ZL3b corresponds to either one or two
    v101 glyphs.
    RESOLUTION TASK FOR SESSION R2: fetch Claston's published table
    and verify. Do not proceed with onset classifier until resolved.

  priority_order_for_v101_classifier:
    description: |
      Under v101's single-character-per-glyph model, the "priority
      ordering" of ZL3b (qok before qo, cth before ch) reduces to
      simpler single-character prefix matching — except for tokens
      that begin with multi-glyph sequences like 'qok' (which is q
      followed by some v101 encoding of 'ok'). The priority order
      concept still applies: a word starting with 'q' THEN glyph 'K'
      → qok class, where 'q' alone → qo class.
    reimplementation_strategy: |
      Rewrite `get_onset()` as a sequential prefix matcher over v101
      glyph codes. The class list is the same (23 classes + other) but
      the match targets are v101 glyph sequences, not EVA letter
      sequences.

  expected_v101_onset_class_resolution:
    class: resolution_under_v101
    qok:  "q (4) + o + K — three v101 chars; classifier looks for this sequence"
    qot:  "q (4) + o + T"
    qo:   "q (4) + o"
    cth:  "single v101 char (e.g., specific ligature code)"
    ckh:  "single v101 char"
    cph:  "single v101 char"
    sch:  "single v101 char"
    ch:   "'cc' or single 'C' — AMBIGUOUS, see above"
    sh:   "single v101 char (e.g., 'S' or specific variant code)"
    ok:   "o + K (two v101 chars)"
    ot:   "o + T (two v101 chars)"
    ol:   "o + l (two v101 chars)"
    d:    "8 (single digit char)"
    s:    "s (single letter)"
    y:    "9 (single digit char)"
    k:    "K (single capital letter)"
    t:    "T (single capital letter)"
    l:    "l (single letter)"
    r:    "2 (single digit char)"
    p:    "P (single capital letter)"
    f:    "F (single capital letter)"
    a:    "a (single letter)"
    o:    "o (single letter)"
    other: "fallback"

  mapping_ambiguities_list:
    - "ch encoding (single vs double glyph in v101)"
    - "Gallows variants: v101 distinguishes k/k2/k3 where EVA merges. Which v101 chars collapse to ZL3b 'k'?"
    - "Benched gallows cth/ckh/cph/sch: may be multiple v101 glyphs each, or each a distinct single glyph"
    - "Rare letters (i, n, m): v101 may distinguish 'iin' vs 'iiin' as different glyphs; ZL3b treats these as letter sequences"
    - "The '9' digit in v101 is the canonical mapping for EVA 'y', but '9' also appears in non-y contexts (variant of 'y'? curator convention?)"
    - "The gallows capitals K/T/P/F may each have 2-3 v101 variants that ZL3b merges. The canonical ZL3b onset class 'k' may correspond to {K, k2, k_alt} in v101."

  domain_judgment_calls_required_at_R2:
    - call: "Which v101 glyph(s) = ZL3b 'ch'?"
      resolution: "Fetch Claston's table; may need multiple v101 codes → single ZL3b class"
    - call: "Which v101 glyph(s) = ZL3b 'k'?"
      resolution: "Same; v101's k-variants collapse to ZL3b k"
    - call: "Do v101 benched gallows (cth/ckh/cph/sch) each map to single glyphs or sequences?"
      resolution: "Verify against Claston's table"
    - call: "How is uncertainty encoded in v101?"
      resolution: "Read the v101 file header and first few body lines for comment conventions"

  implementation_cost: "SUBSTANTIAL. New tokenizer, new onset classifier, new suffix classifier. ~300-500 lines of new code."
```

### 2.5 Summary table: ZL3b onset classes under each target

```yaml
onset_class_portability_summary:
  # Portability: IDENTITY (reuses ZL3b classifier unchanged),
  #              MAPPED (requires target-specific mapping table),
  #              AMBIGUOUS (mapping requires domain judgment),
  #              INDETERMINATE (cannot be cleanly resolved)
  class: {EVA_basic, IT2a, v101}
  qok:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  qot:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  qo:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  cth:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  ckh:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  cph:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  sch:   {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  ch:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  sh:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  ok:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  ot:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  ol:    {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  d:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  s:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  y:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  k:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}   # gallows variants
  t:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  l:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  r:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  p:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  f:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: AMBIGUOUS}
  a:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  o:     {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: MAPPED}
  other: {EVA_basic: IDENTITY, IT2a: IDENTITY, v101: IDENTITY}  # fallback bucket
```

**Key observations:**

1. All onset classes are IDENTITY under EVA-basic and IT2a. No new
   classifier work is needed for either.

2. Under v101, twelve classes are cleanly MAPPED (single substitution
   of ZL3b prefix for v101 character/sequence) and ten are AMBIGUOUS
   (require Claston's table to resolve).

3. The AMBIGUOUS classes are concentrated in the compound gallows
   (cth, ckh, cph, sch) and the bare gallows (k, t, p, f) — exactly
   the classes whose v101 distinctions might reveal structure hidden
   by EVA's merging.

---

## 3. Suffix Class Mapping

### 3.1 ZL3b productive suffix inventory

Per `canonical_methodology.md` §5.1 and `voynich_grammar_spec.md` §2:

```yaml
zl3b_suffixes:
  four_char: [eedy, aiin, eeey]
  three_char: [edy, chy, eey, ain, air, ary]
  two_char: [dy, ey, ol, or, ar, al, am, an, in, ir]
  one_char: [y, n, l, r]
```

Longest-match priority; same priority-ordering logic as onsets.

### 3.2 Mapping to EVA-basic

```yaml
suffix_mapping_EVA_basic:
  relationship: IDENTITY
  suffix_classifier_reuse: "100% — same function"
  expected_A_to_B_transformation_detectable: YES
  implementation_cost: NONE
```

### 3.3 Mapping to IT2a

```yaml
suffix_mapping_IT2a:
  relationship: IDENTITY
  suffix_classifier_reuse: "100%"
  expected_A_to_B_transformation_detectable: YES
  implementation_cost: NONE
```

### 3.4 Mapping to v101

```yaml
suffix_mapping_v101:
  relationship: MAPPED
  suffix_classifier_reuse: "requires rewrite"
  expected_A_to_B_transformation_detectable: AMBIGUOUS
  implementation_cost: SUBSTANTIAL

  critical_suffix_mappings:
    -edy: "EVA 3 chars (e, d, y) → v101 3 chars ('e', '8', '9') — sequence match"
    -eedy: "EVA 4 chars → v101 4 chars ('e', 'e', '8', '9')"
    -aiin: "EVA 4 chars → v101 probably 'aiiN' or a single 'iin' glyph code — AMBIGUOUS"
    -ain:  "EVA 3 chars → v101 'aiN' or similar — AMBIGUOUS"
    -ol:   "EVA 2 chars → v101 'ol'"
    -or:   "EVA 2 chars → v101 'o2' (since r → 2)"
    -ey:   "EVA 2 chars → v101 'e9'"
    -dy:   "EVA 2 chars → v101 '89'"
    -y:    "EVA 1 char → v101 '9'"

  key_ambiguity_aiin_family: |
    EVA writes 'daiin' as 5 characters (d, a, i, i, n). v101 writes
    the 'aiin' suffix as potentially one glyph ('aiiN' ligature) or
    multiple depending on Claston's table. If v101 treats 'aiin' as a
    single glyph, the suffix classifier must be rewritten so that
    single glyph IS the -aiin class, and longest-match is not
    applicable in the character-by-character sense.

  A_to_B_transformation_detectability:
    finding_5_replication: |
      Finding 5 says: "Systematic -edy suffix transformation (A:
      -ol/-or/-ey; B: -edy/-eedy)". Under v101:
      - -ol / -or / -ey map to two-character v101 sequences (o-l, o-2, e-9)
      - -edy / -eedy map to three- and four-character v101 sequences
      - Both sets are detectable IF the v101 tokenizer preserves
        end-of-word character sequences (which it should, since words
        are still period-delimited)
    verdict: |
      A→B transformation IS detectable under v101. The distinct
      suffixes remain as character sequences and a rewritten
      longest-match suffix classifier can recognize them. Replication
      of Finding 5 is FEASIBLE under v101 but requires a rewritten
      suffix classifier and a verification step that the -edy/-ol
      distinction is preserved at the character level.

  domain_judgment_calls:
    - "Does v101 encode 'aiin' as a single glyph? If yes, replication of -aiin as a class is straightforward. If no, check whether 'aiin' is 'aiN' or 'aiiN' in v101 and update the longest-match list accordingly."
    - "Does v101 encode 'edy' as a single glyph or as three sequential glyphs?"
    - "Are there v101-specific suffixes (glyph variants) that EVA merges into one suffix? If so, the per-v101 classifier may find MORE suffix classes than ZL3b has."
```

### 3.5 Summary: suffix classifier reuse

```yaml
suffix_classifier_reuse_summary:
  EVA_basic: {reuse_pct: 100, new_code_lines: 0}
  IT2a:      {reuse_pct: 100, new_code_lines: 0}
  v101:      {reuse_pct: 0,   new_code_lines: "~100"}
```

---

## 4. Dialect Assignment Under Target Transliterations

The canonical dialect classifier (`canonical_methodology.md` §3.1) is:

```python
def assign_dialect_per_line(words, edy_threshold=0.05, min_tokens=10):
    if len(words) < min_tokens:
        return None
    edy_count = sum(1 for w in words if 'edy' in w or 'eedy' in w)
    return 'B' if edy_count / len(words) >= 0.05 else 'A'
```

The classifier uses `'edy' in w` as a substring test.

### 4.1 Under EVA-basic and IT2a

```yaml
dialect_classifier_EVA_basic_and_IT2a:
  change_required: NONE
  edy_token_pattern: "substring 'edy' unchanged"
  expected_dialect_assignments: "identical to ZL3b on overlapping folios"
  folio_coverage_note: |
    If IT2a has partial coverage, some folios classifiable under ZL3b
    will be unclassified under IT2a. This is a coverage gap, not a
    dialect-assignment disagreement.
```

### 4.2 Under v101

```yaml
dialect_classifier_v101:
  change_required: SUBSTANTIAL
  edy_token_pattern_change: |
    EVA 'edy' = characters [e, d, y]
    v101  'edy' = characters [e, 8, 9]  (using presumed mapping)
  new_classifier_code: |
    def assign_dialect_per_line_v101(words, edy_threshold=0.05, min_tokens=10):
        if len(words) < min_tokens:
            return None
        edy_count = sum(1 for w in words
                         if 'e89' in w   # v101 'edy'
                         or 'ee89' in w) # v101 'eedy'
        return 'B' if edy_count / len(words) >= 0.05 else 'A'

  expected_behavior_vs_ZL3b: |
    Should classify essentially the same folios as ZL3b to A vs B,
    assuming the v101 'edy' sequence faithfully corresponds to the
    EVA 'edy' sequence. This is the single most important
    verification task for session R2.

  verification_task_for_R2: |
    COMPUTE at session start: per-folio dialect assignment under both
    ZL3b and v101 classifiers. Report the agreement rate. If agreement
    is <95% on folios present in both files, halt R2 and escalate —
    the mapping table is wrong. If ≥95%, proceed.

  corner_case: |
    If v101's 'edy' encoding is a single glyph rather than a sequence
    (e.g., Claston merges 'edy' into one character), the classifier
    becomes:
        edy_count = sum(1 for w in words if '<single_glyph_code>' in w)
    This is simpler but requires knowing the glyph code.
```

### 4.3 Expected A/B folio split under target transliterations

```yaml
expected_A_B_split:
  ZL3b_baseline:
    A_folios_approx: 82    # herbal A + portions of astro
    B_folios_approx: 75    # bio + pharma + stars + cosmo + some herbal
  EVA_basic:
    agreement_with_ZL3b_expected: "≥99%"
    reason: "same character set, stricter token filter only drops a few noisy tokens"
  IT2a:
    agreement_with_ZL3b_expected: "≥95% on overlap"
    reason: "sibling curator; slight reading differences should not change dialect"
  v101:
    agreement_with_ZL3b_expected: "≥95%"
    reason: "independent transliteration but 'edy' pattern should survive"
    risk: "if 'edy' is merged into a single glyph and that glyph is ALSO used for non-edy meanings, the classifier needs rewriting"
```

---

## 5. Position Conventions

### 5.1 LF / LL definitions are transliteration-neutral

Per `canonical_methodology.md` §2.1:

```python
def get_slot(i, n):
    if n == 1:     return 'only'
    if i == 0:     return 'LF'
    if i == n-1:   return 'LL'
    if i == 1:     return 'second'
    return 'MID'
```

**This function operates on a line's tokens, not characters.** Position
is defined by tokenization, not by character choice. All three target
transliterations (EVA-basic, IT2a, v101) use period-delimited word
tokens. The `get_slot` function is reusable unchanged across all
targets.

```yaml
position_convention_portability:
  EVA_basic: {reuse: full, notes: "identical"}
  IT2a:      {reuse: full, notes: "identical"}
  v101:      {reuse: full, notes: "identical"}

  exceptions_identified: "None"

  caveat: |
    LF and LL are tokenization-dependent. If a target transliteration
    has different rules about what constitutes a "line" — e.g., if
    v101 joins lines across page breaks differently than EVA — the
    per-line word count (n in get_slot) will differ. This is a corpus
    loader issue, not a position convention issue.

  verification_task: |
    At R2 start, verify v101's line-count matches ZL3b's within ±2% on
    shared folios. Any larger discrepancy indicates a line-handling
    difference that must be resolved before computing positional
    metrics.
```

### 5.2 Paragraph / label / radial distinctions

```yaml
locus_code_portability:
  EVA_basic: "IVTFF conventions preserved; body filter `lt.startswith('P')` unchanged"
  IT2a:      "IVTFF conventions preserved; check for coverage gaps on label loci"
  v101:      "IVTFF conventions preserved; verify label locus codes in v101 header at R2 start"
  risk: |
    v101's locus codes may use a different convention from EVA.
    Claston may have used his own locus annotation. Needs verification.
```

---

## 6. Metric Portability

### 6.1 The five pre-registered findings

From `preregistration_transliteration_and_specificity_thresholds.md`:

1. **Three-layer positional architecture** (openers / mid / terminals)
   — ≥75% class-category agreement in ≥2 of 3 target systems

2. **Terminal-layer dialect inversion** (A = {d, cth}; B = {r, l, ol, o, a})
   — zero-overlap holds in ≥2 of 3 target systems

3. **Bigram matrix cross-dialect invariants** (y→y, sh→qok, ok→ok,
   qok→s, sh→ch depletion) — ≥4 of 5 replicate at CONF in ≥2 of 3
   target systems

4. **A-herbal paragraph chain** (d → qot → ch → o → sh) — exceeds 95th
   percentile of section-shuffled AND onset-shuffled null distributions
   in ≥2 of 3 target systems

5. **Systematic -edy suffix transformation** (A: -ol/-or/-ey; B: -edy/-eedy)
   — ≥75% of onset classes show the transformation in ≥2 of 3 target
   systems

### 6.2 Finding 1 — Three-layer positional architecture

```yaml
finding_1_portability:
  description: "Classify each of 23 onset classes as opener / mid / terminal based on LF and LL enrichment per dialect"
  EVA_basic:
    portability: FULL
    expected_replication: "Retained with agreement ≥95%"
    rationale: "same classifier, same positional convention, small token filter difference"
    risk: LOW

  IT2a:
    portability: FULL
    expected_replication: "Retained with agreement ≥90%"
    rationale: "coverage may limit some rare classes but core opener/mid/terminal holds"
    risk: LOW (coverage only)

  v101:
    portability: PARTIAL
    expected_replication: "Retained with agreement ≥75% — but contingent on mapping table resolution"
    rationale: |
      The class count is the same (23) but the mapping from v101 glyphs
      to these classes MUST be established before the classification
      can run. If Claston's table has a clean bijection for the core
      classes (qok, qot, qo, d, y, s, t, k, p, f, r, l, ol, o, a, ch,
      sh) the replication proceeds. The compound gallows (cth, ckh,
      cph, sch) are the risk: v101 may distinguish these as different
      glyphs than EVA assumes, producing MORE classes, or merge them
      differently.
    risk: MEDIUM
    contingency: |
      If v101 has more compound-gallows classes than EVA, the
      agreement calculation uses the SHARED class set. If v101 has
      fewer, some classes cannot be scored.
  recommended: "REPLICATE under all three targets"

finding_1_threshold_application: |
  The pre-registered threshold is "≥75% class category agreement in
  ≥2 of 3 alternative transliterations (at least 15 of 20 classes
  receive the same category assignment)." The "20 classes" language
  reflects a reduced set excluding the four compound gallows plus
  'other'. Under v101 the class count may differ slightly; the
  session should report the agreement rate on the shared class set
  and note any v101-specific classes separately.
```

### 6.3 Finding 2 — Terminal-layer dialect inversion

```yaml
finding_2_portability:
  description: "Zero overlap between A-terminal set {d, cth} and B-terminal set {r, l, ol, o, a}, with d as A-terminal and ≥1 B-terminal class confirmed"
  EVA_basic: {portability: FULL, expected: "Retained", risk: LOW}
  IT2a:      {portability: FULL, expected: "Retained", risk: LOW}
  v101:
    portability: PARTIAL
    expected_replication: "Retained, contingent on mapping"
    rationale: |
      Terminal sets in v101 should match EVA once the mapping is
      established. The A-terminals {d, cth} map to specific v101
      characters; the B-terminals {r, l, ol, o, a} likewise. The
      zero-overlap test can be computed under v101 once the classifier
      is in place.
    risk: MEDIUM
    key_risk: "v101 may split 'cth' across multiple glyphs, splitting the A-terminal set and changing the overlap calculation"
  recommended: "REPLICATE under all three targets"
```

### 6.4 Finding 3 — Bigram matrix cross-dialect invariants

```yaml
finding_3_portability:
  description: "y→y, sh→qok, ok→ok, qok→s bigrams CONF cross-dialectally; sh→ch DEPL cross-dialectally"
  EVA_basic: {portability: FULL, expected: "Retained", risk: LOW}
  IT2a:      {portability: FULL, expected: "Retained", risk: LOW}
  v101:
    portability: CONDITIONAL
    expected_replication: "Retained if sh→qok mapping is clean; at risk otherwise"
    rationale: |
      Each of the five bigrams requires BOTH the sender and receiver
      class to be correctly identified in v101. The sh→qok bigram is
      the highest-risk: sh and qok are both multi-glyph onsets under
      the canonical ZL3b model and may have v101 variants. If the
      v101 classifier produces multiple sub-classes of ZL3b-sh or
      ZL3b-qok, the bigram can fragment and its enrichment is diluted
      across sub-bigrams.
    risk: MEDIUM-HIGH
    mitigation: |
      The session R2 task should FIRST compute the v101 character
      distribution at line-first and line-last positions to verify
      that the expected onset classes dominate where expected. If
      sh maps to a glyph that accounts for ≥80% of what should be the
      sh-onset tokens, the replication proceeds. If sh fragments across
      3+ glyphs, replication requires a glyph-class table.
  recommended: "REPLICATE under all three targets"
```

### 6.5 Finding 4 — A-herbal paragraph chain

```yaml
finding_4_portability:
  description: "Directed chain d → qot → ch → o → sh exceeds 95th percentile of section-shuffled AND onset-shuffled null distributions (200 controls each), with all four edges at E ≥ 1.5×"
  EVA_basic: {portability: FULL, expected: "Retained", risk: LOW}
  IT2a:      {portability: PARTIAL, expected: "Depends on A-herbal coverage in IT2a", risk: MEDIUM}
  v101:
    portability: CONDITIONAL
    expected_replication: "Retained if five classes (d, qot, ch, o, sh) have clean v101 mappings"
    rationale: |
      The chain is a 4-edge inter-line succession pattern. Each edge
      requires correctly identifying the sender and receiver onset
      class. The null distributions are shuffles of the same corpus,
      so they inherit any v101 class-partitioning issues. If v101
      correctly maps d/qot/ch/o/sh, the chain detection is structurally
      identical to ZL3b and the replication proceeds. If any of these
      five classes fragments under v101 (most likely 'ch', per §2.4),
      the chain may weaken OR appear as multiple sub-chains.
    risk: MEDIUM-HIGH
    specific_concern: |
      'ch' is one of the highest-risk classes under v101 mapping. If
      v101 distinguishes ch variants that EVA merges, the chain
      might weaken on d → qot → ch_variant_1 but strengthen on
      d → qot → ch_variant_2, and the "Retained" threshold is
      ambiguous to apply.
  recommended: "REPLICATE under EVA-basic and v101; DEFER ZL3a unless needed"
```

### 6.6 Finding 5 — Systematic -edy suffix transformation

```yaml
finding_5_portability:
  description: "A uses -ol/-or/-ey; B uses -edy/-eedy on the same stems (≥75% of onset classes show the transformation)"
  EVA_basic: {portability: FULL, expected: "Retained", risk: LOW}
  IT2a:      {portability: FULL, expected: "Retained", risk: LOW}
  v101:
    portability: CONDITIONAL
    expected_replication: "Retained if suffix classifier correctly identifies -edy/-eedy vs -ol/-or/-ey under v101 encoding"
    rationale: |
      The transformation test requires (a) identifying the same stem
      in both dialects and (b) measuring the suffix distribution per
      stem per dialect. Under v101, 'stem' is defined by
      onset-prefix-strip, which depends on correct onset classification.
      The suffix distributions themselves are detectable if the v101
      suffix classifier is correct.
    risk: MEDIUM
    specific_concern: |
      'edy' as a character sequence under v101 may differ from EVA.
      If v101 uses a single glyph for 'edy' (treating it as a
      morphological unit), the classifier needs one rule; if v101 uses
      three characters, another rule.
  recommended: "REPLICATE under EVA-basic and v101; ZL3a only if EVA-basic disagrees"
```

### 6.7 Summary: portability matrix

```yaml
finding_portability_matrix:
  headers: [finding, EVA_basic, IT2a, v101, recommended]
  rows:
    - [F1_three_layer_architecture,     FULL, FULL,    PARTIAL_MAPPING_REQUIRED, "R1+R2 both"]
    - [F2_terminal_layer_inversion,     FULL, FULL,    PARTIAL_MAPPING_REQUIRED, "R1+R2 both"]
    - [F3_bigram_invariants,            FULL, FULL,    CONDITIONAL_ON_MAPPING,   "R1+R2 both"]
    - [F4_paragraph_chain,              FULL, PARTIAL, CONDITIONAL_ON_MAPPING,   "R1+R2 both"]
    - [F5_suffix_transformation,        FULL, FULL,    CONDITIONAL_ON_MAPPING,   "R1+R2 both"]
  notes: |
    All five findings are FULLY portable to EVA-basic. Finding 4 is
    partially portable to IT2a due to possible coverage gaps. All
    five findings are CONDITIONALLY portable to v101, contingent on
    resolving the mapping ambiguities flagged in §2.4.

    The pre-registered rule "≥2 of 3 transliterations agree" can be
    satisfied by (EVA-basic, v101) agreeing, even if IT2a is skipped
    and ZL3a is deferred. The minimum viable replication is EVA-basic
    + v101.
```

---

## 7. Infrastructure Work List

### 7.1 Component inventory

```yaml
existing_infrastructure:
  canonical_tokenizer_ZL3b:
    file: "state/canonical_methodology.md §1.3.2 and state/voynich_constraints.py"
    lines: "~10 LoC"
    reusable_for: [EVA_basic (with variant), IT2a (direct), v101 (replaced)]
  onset_classifier_ZL3b:
    file: "state/voynich_constraints.py get_onset()"
    lines: "~30 LoC"
    reusable_for: [EVA_basic (direct), IT2a (direct), v101 (replaced)]
  suffix_classifier_ZL3b:
    file: "state/voynich_constraints.py get_suffix()"
    lines: "~15 LoC"
    reusable_for: [EVA_basic (direct), IT2a (direct), v101 (replaced)]
  dialect_classifier_ZL3b:
    file: "state/voynich_constraints.py assign_dialect_per_line()"
    lines: "~10 LoC"
    reusable_for: [EVA_basic (direct), IT2a (direct), v101 (adapted)]
  corpus_loader_ZL3b:
    file: "state/voynich_constraints.py load_vms_corpus()"
    lines: "~60 LoC"
    reusable_for: [EVA_basic (direct with tokenizer parameter), IT2a (direct), v101 (replaced)]
  validator_predicates:
    file: "state/voynich_constraints.py register()/validate()/..."
    lines: "~800 LoC"
    reusable_for: "ALL targets — transliteration-neutral, operates on classified tokens"
```

### 7.2 Session R1 work list (EVA-basic)

```yaml
session_R1_infrastructure:
  target: EVA-basic
  new_code_required:
    - component: eva_basic_tokenizer
      description: |
        Variant of canonical tokenizer that drops all tokens containing
        uncertainty markers ([, ], {, }) and all tokens with non-letter
        characters after filtering.
      estimated_loc: ~20
      effort: TRIVIAL
    - component: eva_basic_corpus_loader
      description: |
        Calls load_vms_corpus(tokenizer=tokenize_eva_basic). The
        existing load_vms_corpus takes a path argument but hard-codes
        the canonical tokenizer; the R1 task is to parameterize the
        loader with a tokenizer argument.
      estimated_loc: ~5 (refactor) + reuse ~60 LoC
      effort: TRIVIAL
  reused_code:
    - onset_classifier_ZL3b  # unchanged
    - suffix_classifier_ZL3b  # unchanged
    - dialect_classifier_ZL3b  # unchanged
    - validator_predicates  # unchanged
  new_scripts:
    - experiments/exp_NNN_replication_eva_basic/script.py
  session_workload: "LOW — ~1 hour of Sonnet time"
  estimated_total_new_LoC: "~50 (mostly tokenizer variant + script harness)"
```

### 7.3 Session R2 work list (v101)

```yaml
session_R2_infrastructure:
  target: v101
  prerequisite_domain_knowledge:
    - "Claston's ZL3b ↔ v101 character mapping table (fetch from voynich.nu or Voynich Ninja forum at session start)"
    - "v101 uncertainty / alternation conventions (read v101 file header and first 20 body lines at session start)"
    - "v101 locus code conventions (verify body/label/radial filter still applies)"
  new_code_required:
    - component: v101_tokenizer
      description: |
        Period-split word tokenizer operating on v101 character set.
        Must handle latin-1 encoding. Must filter out uncertainty
        markers (convention TBD at R2 start).
      estimated_loc: ~30
      effort: MODEST
    - component: v101_onset_classifier
      description: |
        Priority-ordered longest-prefix matcher over v101 glyph codes.
        The class list is the same 23 ZL3b classes, but each class is
        defined by a v101 glyph or sequence. Cases like compound gallows
        may require character classes rather than exact matches.
      estimated_loc: ~50
      effort: MODEST
      depends_on: [claston_mapping_table]
    - component: v101_suffix_classifier
      description: |
        Longest-match suffix classifier over v101. Same suffix list as
        ZL3b but with v101-encoded endings.
      estimated_loc: ~30
      effort: MODEST
      depends_on: [claston_mapping_table]
    - component: v101_dialect_classifier
      description: |
        Per-line edy-rate classifier adapted to v101's encoding of 'edy'
        (likely 'e89' trigraph or single glyph).
      estimated_loc: ~15
      effort: TRIVIAL
      depends_on: [claston_mapping_table]
    - component: v101_corpus_loader
      description: |
        Same IVTFF parsing logic as ZL3b loader, but with latin-1
        encoding, v101 tokenizer, v101 dialect classifier. Must verify
        v101 file header and body filter logic at load time.
      estimated_loc: ~80
      effort: MODEST
    - component: v101_validator_compat_layer
      description: |
        Thin adapter that ensures validator predicates see
        canonically-named onset classes. If v101 classes are named
        differently (e.g., class 'ch_v101_variant_1' instead of 'ch'),
        a pre-validation step renames. Most predicates should work
        unchanged if the classifier outputs canonical class names.
      estimated_loc: ~20
      effort: TRIVIAL
  reused_code:
    - validator_predicates  # unchanged but requires canonical-name output
    - get_slot  # unchanged (tokenization-neutral)
  new_scripts:
    - experiments/exp_NNN_replication_v101/script.py
  session_workload: "HIGH — estimated 3-5 hours of Sonnet time"
  estimated_total_new_LoC: "~250-350"
  session_prerequisites:
    - "Claston mapping table is resolved (FIRST 30 minutes of session)"
    - "v101 header and body filter verified (FIRST 10 minutes)"
    - "v101 dialect classifier validated against ZL3b on shared folios (FIRST 20 minutes)"
  failure_mode_abort_condition: |
    If the v101 dialect classifier disagrees with ZL3b on >5% of
    folios at session start, HALT session R2 and report. The mapping
    is wrong and no replication can proceed.
```

### 7.4 Session R3 work list (ZL3a, deferred)

```yaml
session_R3_infrastructure:
  target: ZL3a
  defer_rationale: "Only needed if R1 and R2 produce disagreements that require a tiebreaker"
  prerequisites:
    - "Fetch ZL3a from voynich.nu (not on disk)"
  new_code_required:
    - component: zl3a_corpus_loader
      description: "Near-identity with ZL3b loader; different file path"
      estimated_loc: ~5
      effort: TRIVIAL
  reused_code: "100%"
  session_workload: "LOW — ~1 hour"
  estimated_total_new_LoC: ~20
```

### 7.5 Infrastructure work summary

```yaml
infrastructure_work_summary:
  total_new_code_required:
    session_R1: ~50 LoC
    session_R2: ~250-350 LoC
    session_R3_if_needed: ~20 LoC
    total: ~320-420 LoC
  effort_distribution:
    tokenizer_variants: "LOW for EVA-basic, MODEST for v101"
    onset_classifiers: "ZERO for EVA-basic/IT2a, MODEST for v101"
    suffix_classifiers: "ZERO for EVA-basic/IT2a, MODEST for v101"
    dialect_classifier: "ZERO for EVA-basic/IT2a, TRIVIAL for v101"
    corpus_loader: "TRIVIAL refactor for all (add tokenizer parameter)"
    validator: "ZERO — transliteration-neutral"
  refactor_required_to_voynich_constraints_py:
    description: |
      Current load_vms_corpus() hard-codes canonical ZL3b tokenizer.
      Refactor to accept a tokenizer argument:
          def load_vms_corpus(path, dialect="B",
                              tokenizer=tokenize_zl3b,
                              onset_classifier=get_onset_zl3b,
                              dialect_classifier=assign_dialect_per_line_zl3b,
                              body_only=True, ...)
      This makes the loader transliteration-neutral.
    effort: TRIVIAL (~15 LoC refactor, no behavior change for default)
    recommended: "DO at start of session R1"
```

---

## 8. Recommended Session Sequence

### 8.1 Rejection of the default "R1 = v101, R2 = EVA-basic + ZL3a" plan

The task prompt's default assumption was two sessions: one for v101,
one for EVA-basic and optionally ZL3a. This plan RECOMMENDS a
different decomposition:

### 8.2 Proposed sequence

```yaml
recommended_sequence:
  R1_EVA_basic:
    goal: "Replicate all 5 findings under EVA-basic; establish 'R1 agreement with ZL3b' baseline"
    duration_estimate: "1 session, ~1 hour"
    deliverables:
      - "state/replication_eva_basic_results.md"
      - "experiments/exp_NNN_replication_eva_basic/"
      - "voynich_constraints.py refactored to accept tokenizer argument"
    gate_decision: |
      IF EVA-basic replicates all 5 findings at ≥95% agreement with ZL3b,
      R1 is a success and confidence in ZL3b is strengthened before
      undertaking R2's larger effort. IF EVA-basic produces surprising
      disagreements, HALT and investigate; something about the tokenizer
      variants is affecting the findings and we need to understand why
      before proceeding to v101.

  R2_v101:
    goal: "Replicate all 5 findings under v101; the hard session"
    duration_estimate: "1 session, 3-5 hours"
    prerequisites:
      - "R1 complete and at least partially successful"
      - "Claston mapping table fetched"
      - "v101 uncertainty / locus conventions documented"
    deliverables:
      - "state/replication_v101_results.md"
      - "experiments/exp_NNN_replication_v101/"
      - "state/v101_character_mapping.md (documents the Claston mapping used)"
    gate_decision: |
      IF v101 replicates all 5 findings at ≥75% class agreement (per
      pre-registration threshold) in combination with R1, the
      replication section of the paper writes up as "Retained" for all
      five findings. IF v101 partially replicates, some findings are
      "Weakened" per the pre-registered thresholds. IF v101 fully
      contradicts ZL3b, the paper's Section 2 requires substantial
      revision.

  R3_ZL3a_conditional:
    goal: "Tiebreaker replication under ZL3a if R1 and R2 disagree"
    trigger: "R1 and R2 disagree on any of the five findings"
    duration_estimate: "1 session, ~1 hour"
    defer_if: "R1 and R2 agree on all five findings — then ZL3a adds nothing"

  R4_IT2a_optional:
    goal: "EVA-family curator robustness check (OPTIONAL; not required for pre-registration)"
    trigger: "If R1 and R2 both succeed and there is spare session time"
    duration_estimate: "~30 minutes"
    value: "Low — not independent replication"
    recommended: "SKIP unless the paper reviewer specifically requests it"
```

### 8.3 Rationale for EVA-basic-first

```yaml
rationale_R1_before_R2:
  reason_1_cost: |
    EVA-basic replication is ~50 LoC of new code and ~1 hour of
    session time. v101 replication is ~300 LoC and ~4 hours. Running
    the cheap session first reduces the total risk of the expensive
    session.
  reason_2_baseline_validation: |
    If EVA-basic replication fails or produces surprises, this
    indicates a bug in the existing ZL3b pipeline or a tokenizer
    sensitivity that v101 will also exhibit. Better to find this
    under the simpler target first.
  reason_3_gate_for_R2: |
    A successful R1 gives the session R2 agent confidence that the
    underlying pipeline is correct, so any R2 failures can be
    attributed to the v101 mapping rather than to the pipeline.
  reason_4_minimum_viable_replication: |
    Per the pre-registered "≥2 of 3 transliterations" rule, the
    minimum viable replication is EVA-basic + v101. IT2a is optional
    and ZL3a is not on disk. R1 + R2 is the smallest session count
    that can produce a "Retained" classification.
```

### 8.4 Session R1 skeleton

```yaml
session_R1_skeleton:
  opening_tasks:
    - "Read state/transliteration_replication_plan.md (this file) §1–§8"
    - "Read state/preregistration_transliteration_and_specificity_thresholds.md"
    - "Read state/canonical_methodology.md §§1–5"
    - "Read voynich_constraints.py"
  refactor_task:
    - "Refactor load_vms_corpus() to accept a tokenizer argument"
  new_code_task:
    - "Implement tokenize_eva_basic() per §2.2 definition"
    - "Create experiments/exp_NNN_replication_eva_basic/script.py"
  experiment_tasks:
    - "Compute each of the five findings under EVA-basic"
    - "Compare per-finding outputs to ZL3b canonical values"
    - "Classify each finding as Retained / Weakened / Failed per pre-registered thresholds"
  reporting_task:
    - "Write experiments/exp_NNN_replication_eva_basic/result.md"
    - "Write state/replication_eva_basic_results.md summary"
    - "Run audit_experiment.md skill before finalizing"
  post_session_gate:
    - "Commit R1 results"
    - "Decide: proceed to R2 or investigate anomalies"
```

### 8.5 Session R2 skeleton

```yaml
session_R2_skeleton:
  opening_tasks:
    - "Read state/transliteration_replication_plan.md (this file) §2.4, §3.4, §4.2, §7.3"
    - "Read state/replication_eva_basic_results.md (R1 output)"
    - "Fetch Claston mapping table from voynich.nu"
    - "Read v101 file header and first 20 body lines"
  verification_tasks_30_minutes:
    - "Verify Claston mapping table against known ch/sh/qok/cth glyphs"
    - "Verify v101 locus codes use same IVTFF conventions"
    - "Document v101 uncertainty encoding conventions"
    - "Build v101 onset classifier and verify against ZL3b at a sample of 20 folios"
    - "Build v101 dialect classifier and compare A/B assignment to ZL3b"
  gate_abort_condition:
    - "IF v101 dialect classifier disagrees with ZL3b on >5% of folios: HALT and report"
  new_code_tasks:
    - "tokenize_v101()"
    - "get_onset_v101()"
    - "get_suffix_v101()"
    - "assign_dialect_v101()"
    - "load_vms_corpus variant with v101 classifier chain"
    - "experiments/exp_NNN_replication_v101/script.py"
  experiment_tasks:
    - "Compute each of the five findings under v101"
    - "Report per-finding Retained/Weakened/Failed per pre-registration"
    - "Note class-level disagreements with ZL3b"
  reporting_task:
    - "experiments/exp_NNN_replication_v101/result.md"
    - "state/replication_v101_results.md"
    - "state/v101_character_mapping.md (the Claston table as used)"
    - "Run audit_experiment.md"
```

---

## 9. Known Risks

### 9.1 Critical risks (could abort replication)

```yaml
critical_risks:

  risk_1_claston_table_unavailable:
    description: |
      Claston's ZL3b↔v101 mapping table is required for session R2
      and is not on disk. If voynich.nu has taken it offline, or if
      the Voynich Ninja thread link has rotted, R2 cannot proceed.
    probability: LOW (table has been stable for ~20 years)
    impact: BLOCKING (R2 cannot start without it)
    mitigation: |
      At R2 session start, verify the table is fetchable BEFORE
      beginning any other work. If unavailable, try:
        - Voynich Ninja forum archives
        - Reeds' mailing list archives
        - The Voynich 101 source distribution files
      If none work, reconstruct partially from v101 character
      frequencies and known EVA word mappings, but flag as
      reconstructed.

  risk_2_v101_dialect_split_disagrees_with_ZL3b:
    description: |
      The v101 dialect classifier might disagree with ZL3b on >5% of
      folios if the mapping from v101's 'edy' encoding to EVA's 'edy'
      is wrong.
    probability: LOW-MEDIUM
    impact: BLOCKING (replication tests different A/B splits give different findings)
    mitigation: |
      At R2 start, run both classifiers and compute per-folio agreement.
      If <95%, halt and debug. Often the cause is one character in
      the 'edy' encoding being wrong in the classifier.

  risk_3_ch_glyph_ambiguity_v101:
    description: |
      v101 may encode 'ch' as one glyph or as two. The choice affects
      which finding values are computed and whether class boundaries
      match ZL3b. If the encoding is ambiguous (e.g., Claston uses both
      'cc' and 'C' in different contexts), the classifier has to make
      a choice.
    probability: MEDIUM
    impact: MODERATE (causes one or two findings to be reported with "mapping-conditional" caveats)
    mitigation: |
      Document the encoding choice in state/v101_character_mapping.md.
      Report findings with explicit note about the choice. The
      pre-registration allows "mapping-conditional" replication if the
      choice is documented.

  risk_4_v101_file_encoding_corruption:
    description: |
      The v101 file uses latin-1 encoding with extended-ASCII
      characters. If the file has been corrupted or re-encoded during
      repository operations, some glyph codes may be missing or
      altered.
    probability: LOW
    impact: BLOCKING if corruption is severe
    mitigation: |
      At R2 start, verify file encoding (`file -i data/transcriptions/v101_claston.txt`)
      and sample check the first 100 body characters against the
      voynich.nu online v101 file. Re-fetch if any discrepancy.
```

### 9.2 Moderate risks (could weaken replication outcomes)

```yaml
moderate_risks:

  risk_5_finding_4_chain_weakens_under_v101:
    description: |
      The A-herbal paragraph chain d → qot → ch → o → sh requires
      five classes to map cleanly. If v101 fragments 'ch' into
      multiple glyph classes, the chain may weaken below the 95th
      percentile threshold.
    probability: MEDIUM
    impact: finding 4 moves from "Retained" to "Weakened"
    mitigation: |
      Pre-registration allows "Weakened" classification. No action
      needed beyond reporting honestly.

  risk_6_suffix_edy_encoding_v101:
    description: |
      If v101 encodes 'edy' as a single glyph AND that glyph is also
      used for non-edy forms, the suffix classifier may overcount or
      undercount edy-suffixed words.
    probability: LOW
    impact: finding 5 reported with caveat
    mitigation: |
      Verify edy-glyph usage at R2 start by sampling tokens containing
      the glyph and confirming ≥95% are dialect-B indicators.

  risk_7_IT2a_coverage_gaps_affect_finding_4:
    description: |
      IT2a has "partial or interlinear" coverage per the README. If
      A-herbal folios are absent or partial, the paragraph chain
      cannot be tested there.
    probability: HIGH (if IT2a is run)
    impact: finding 4 not replicable under IT2a
    mitigation: |
      SKIP IT2a as a replication target unless specifically needed;
      IT2a is not in the recommended sequence per §8.2.

  risk_8_eva_basic_stricter_tokenizer_drops_too_much:
    description: |
      If the EVA-basic tokenizer's uncertainty-marker filter drops
      more than 10% of tokens, statistical power for rare findings
      (especially finding 4 paragraph chain) may drop.
    probability: LOW
    impact: finding 4 confidence interval widens
    mitigation: |
      At R1 start, compute the token-count delta between ZL3b and
      EVA-basic. If >5% delta, tighten the EVA-basic tokenizer
      definition to preserve more of the corpus.
```

### 9.3 Operational risks (workflow-level)

```yaml
operational_risks:

  risk_9_R1_and_R2_disagree:
    description: "EVA-basic and v101 produce different Retained/Weakened/Failed classifications for the same finding"
    probability: LOW-MEDIUM
    impact: ZL3a tiebreaker required (R3)
    action: "Run R3 as tiebreaker per §8.2"

  risk_10_session_overrun:
    description: "R2 exceeds estimated 3-5 hours due to mapping-table debugging"
    probability: MEDIUM
    impact: R2 incomplete; paper timeline slips
    mitigation: "Budget 6 hours for R2 with an abort checkpoint at 4 hours if the v101 classifier is still not producing ZL3b-matching dialect assignments"

  risk_11_validator_incompatibility:
    description: "voynich_constraints.py validator predicates may hard-code ZL3b class names (e.g., 'ch' as a literal string) and require per-class refactoring for v101 output"
    probability: HIGH
    impact: R2 new-code estimate grows by ~50 LoC
    mitigation: |
      The v101_validator_compat_layer (§7.3) renames v101 output
      classes to canonical ZL3b names before the validator runs. The
      validator itself stays unchanged.

  risk_12_audit_skill_not_applicable:
    description: "The audit_experiment.md skill applies to new experiments but the replication sessions are run as verifications. Audit Check 1 (target-awareness) is trivially satisfied (no target calibration), Check 2 (feature-destroying) requires verifying the v101 classifier doesn't drop 'ch' tokens the pipeline needs."
    probability: LOW
    impact: audit runs to completion but adds 20 minutes per session
    action: "Run the audit at end of R1 and R2 per the skill"
```

### 9.4 Risk summary table

```yaml
risk_summary_table:
  headers: [risk, probability, impact, session, blocking]
  rows:
    - [Claston_table_unavailable, LOW, BLOCKING, R2, YES]
    - [v101_dialect_disagrees, LOW-MEDIUM, BLOCKING, R2, YES]
    - [ch_glyph_ambiguous_v101, MEDIUM, MODERATE, R2, NO]
    - [v101_file_corruption, LOW, BLOCKING, R2, YES]
    - [finding_4_chain_weakens_v101, MEDIUM, MODERATE, R2, NO]
    - [suffix_edy_encoding_v101, LOW, MODERATE, R2, NO]
    - [IT2a_coverage_gaps, HIGH, LOW, R4, NO]
    - [eva_basic_filter_too_strict, LOW, LOW, R1, NO]
    - [R1_R2_disagreement, LOW-MEDIUM, TRIGGERS_R3, R1+R2, NO]
    - [session_overrun, MEDIUM, MODERATE, R2, NO]
    - [validator_hardcoding, HIGH, LOW, R2, NO]
    - [audit_skill_time, LOW, LOW, all, NO]
```

---

## 10. Pre-Session Checklist

Before beginning session R1 or R2, verify:

```yaml
pre_session_checklist:
  common_both_sessions:
    - "state/canonical_methodology.md readable and current"
    - "state/voynich_grammar_spec.md v1.0 readable"
    - "state/voynich_constraints.py runs its self-test successfully"
    - "state/preregistration_transliteration_and_specificity_thresholds.md frozen (do not edit)"
    - "committed_claims.md has C005, C006, C008 in current form"

  R1_specific:
    - "data/transcriptions/eva_zl3b.txt on disk and readable"
    - "load_vms_corpus refactor plan understood (§7.5)"

  R2_specific:
    - "data/transcriptions/v101_claston.txt on disk and readable"
    - "v101 file encoding verified (latin-1)"
    - "Claston ZL3b↔v101 mapping table source identified (URL, local backup, or reconstruction plan)"
    - "Network access available for Claston table fetch"
    - "v101 locus-code conventions documented (by reading file header)"

  R3_specific:
    - "ZL3a fetched from voynich.nu and placed in data/transcriptions/eva_zl3a.txt"
    - "ZL3a header and format verified as IVTFF-compatible"
```

---

## 11. Out of Scope

The following are explicitly NOT in scope for the transliteration
replication sessions, per the pre-registration and this plan:

- Running new characterization experiments (the five findings are
  fixed by the pre-registration)
- Modifying canonical methodology for the new transliterations (the
  methodology adapts to each target but the ZL3b canonical remains
  canonical)
- Updating committed_claims.md (replication results will be cited in
  the paper, not committed as new claims)
- Architecture specificity re-testing under alternative transliterations
  (C008 is ZL3b-based and the specificity test is orthogonal to
  transliteration replication)
- Label corpus replication (labels are §15 of the grammar spec and
  are a separate concern)
- Section-stratified replication (exp_579 is ZL3b-based; section
  metrics at the per-transliteration level are a v1.2+ task)
- Running experiments in this scoping session (this is a plan, not
  an execution)

---

## 12. References and Cross-Links

```yaml
references:
  internal:
    - state/canonical_methodology.md
    - state/voynich_grammar_spec.md (v1.0)
    - state/committed_claims.md
    - state/preregistration_transliteration_and_specificity_thresholds.md
    - state/voynich_constraints.py
    - data/transcriptions/README.md

  external:
    - "Zandbergen & Landini, EVMT project: https://www.voynich.nu/"
    - "Claston, Voynich 101 system: https://www.voynich.nu/v101/ (presumed)"
    - "IVTFF specification: https://www.voynich.nu/docs/ivtff_1v5.pdf"
    - "Zattera 2022 (v101 descendant): see Voynich Ninja forum for source"

  experiments_referenced_by_plan:
    - exp_173   # committed claims source
    - exp_579   # document-order heterogeneity
    - exp_585   # pre-registered specificity canonical
```

---

```yaml
end_of_plan:
  version: v1.0
  date: 2026-04-14
  next_action: "Begin session R1 (EVA-basic replication)"
  gate_status: "READY — all scoping decisions documented; no blocking issues identified"
  approvals_required:
    - "Human confirmation of session sequence (§8.2)"
    - "Human confirmation that Claston table fetch is acceptable for R2"
    - "Human confirmation that R3 ZL3a and R4 IT2a may be deferred"
```
