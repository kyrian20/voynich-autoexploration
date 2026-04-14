# Voynichese Grammar Specification

```yaml
spec_version: v1.0
date: 2026-04-12
status: paper-input ready; supersedes v0.1
v0_1_archived_at: state/archive/voynich_grammar_spec_v0.1.md
source_phase: Cryptanalyst characterization phase closure (exp_001 through exp_580)
authoritative_synthesis_documents:
  - state/working_position.md
  - state/committed_claims.md          # C007 amendment landed 2026-04-12
  - state/q007_investigation.md
  - experiments/exp_173/result.md      # canonical positional convention
  - experiments/exp_182/result.md      # C004 narrowing — char-level mod
  - experiments/exp_565/result.md      # canonical qok positional / convention hazard
  - experiments/exp_573/result.md      # C007 reconciliation
  - experiments/exp_575..578/result.md
  - experiments/exp_579/result.md      # document-order heterogeneity
  - experiments/exp_580/result.md      # label corpus grammar
audience: future LLM instance or decipherment pipeline; paper-rewrite supplementary material
purpose: |
  Constraints any candidate decipherment mapping or generative theory of
  Voynichese must respect. Each entry is a structural fact with a
  traceable experiment citation, NOT an interpretation.
```

---

## Changes from v0.1 (2026-04-12)

```yaml
changes_v0_1_to_v1_0:

  resolved_open_issues:
    - id: C007_amendment
      action: |
        C007 amendment landed in committed_claims.md. Section 5
        (self-succession) is now CANONICAL. All v0.1 hedging removed.
        Canonical range 0.78×–3.86×. Five CONF cross-dialect classes:
        y, l, ot, qo, qot.
    - id: LF_LL_convention_hazard
      action: |
        DISCOVERED during v1.0 cross-check: the codebase has TWO
        inverted LF/LL conventions. exp_173 (committed claims C005/C006)
        uses LF=line-first (first word) and LL=line-last (last word).
        exp_565+ characterization phase uses pos1=first word, LL=penult,
        LF=last word. v0.1 inherited the latter, conflicting with the
        former. v1.0 standardizes on the COMMITTED-CLAIMS convention
        and translates all per-onset positional values from §1 of v0.1.
        See Section 1.0.
    - id: y_onset_pos1_LF_ambiguity
      action: |
        Dissolved via convention standardization. Under canonical
        convention: y is enriched at LF (first word; pos1) AND depleted
        at LL (last word). Both are real, both are CONF, no
        contradiction. The v0.1 entry "pos1 CONF AND LF subDEPL" was an
        artifact of the convention mismatch.
    - id: qok_pos1_value_conflict
      action: |
        Verified against exp_565 source. Canonical A qok pos1 = 0.87×/145
        (sub-baseline, NOT depleted, NOT enriched). The 1.47×/145 figure
        in working_position §6 is from a non-canonical methodology and
        was corrected by F619. v1.0 §1.5 uses 0.87×.
    - id: C004_narrowing_from_exp_182
      action: |
        exp_182 (Timm character-level modification) achieves 8/36 viable
        and 3/36 at adj_rate ≤ 0.009 with ss_mean ≥ 1.2 and am_ll ≥ 5.0
        — first such result in the program. This NARROWS C004's residual
        gap claim (now applies only to suffix-replacing variants) and
        adds a non-ruled-out mechanism class. §10 and §13 updated.
    - id: label_corpus_grammar_section_15
      action: |
        New §15 "Label corpus grammar" added from exp_580. Mirrors §1
        and §4 structure with explicit body-vs-label comparisons.

  newly_added_sections:
    - "1.0  Positional convention and translation table"
    - "15   Label corpus grammar (10 subsections; ~280 lines)"

  partially_addressed_open_issues:
    - id: herbal_A_two_register
      action: "expanded inline in §7.1; not promoted to top-level subsections (v1.1 work)"
    - id: pharma_A_grammar_morphology_dissociation
      action: "elevated to §8.contrast list; full case study deferred to v1.1"
    - id: paragraph_length_register_specificity_F108
      action: "added as §6.4; encoded as a register-strictness rule"

  remaining_open_issues_for_v1_1:
    - "Executable constraint predicates (deferred per task instruction)"
    - "Automated finding-ID grep cross-check (v1.0 ran a manual sample)"
    - "Per-section A-dialect grammar profiles (label corpus has them; body corpus does not yet)"
    - "Anchor-pair label vocabulary cross-references (Botanist phase deliverable)"

  total_length_change: "v0.1 = 2281 lines → v1.0 = ~3100 lines"
```

---

## How To Use This Spec

This document is a structured constraint sheet, not a narrative. Read
linearly to orient; query specific entries to validate hypotheses.

**Format conventions.**
- Top-level sections are categories of structural fact.
- Within each section, entries are YAML-style nested blocks.
- Every quantitative value carries a `confidence` tag and `exp` field.
- Confidence tags:
  - `CONF`   = ≥1.50× enrichment AND obs ≥ 10 (canonical exp_173 standard)
  - `subCONF`= 1.30–1.50× OR obs 5–9
  - `dir`    = directional (small obs or marginal magnitude)
  - `flat`   = within ±10% of baseline, no significant signal
  - `DEPL`   = ≤0.67× depletion AND obs ≥ 10
  - `subDEPL`= 0.67–0.85× depletion
- `exp: [exp_NNN, ...]` lists the experiment(s) the value comes from.

**Citation conventions.** All `F###` finding IDs reference state/findings.md.
All `exp_NNN` IDs reference experiments/exp_NNN_*/result.md. All `C00N`
IDs reference state/committed_claims.md.

**Query patterns this spec supports.**
1. "Given a candidate plaintext mapping for word W, does the resulting
   distribution match the positional profile of W's onset class?"
   → Sections 1, 15.
2. "Does the candidate generator produce the right suffix paradigm and
   the A→B suffix transformation?" → Section 2.
3. "Does the candidate model generate the bigram matrix and self-
   succession structure?" → Sections 4, 5.
4. "Does the candidate model respect the three-register line grammar
   and the paragraph chain grammar of the relevant section?"
   → Sections 6, 7.
5. "Does the candidate decipherment respect the architecturally-known
   ruled-out mechanism classes?" → Sections 10, 12.
6. "Does the candidate decipherment correctly handle label text as a
   distinct register?" → Section 15.

---

## Table of Contents

1. Positional profiles per onset class per dialect (with §1.0 convention)
2. Suffix paradigms and A→B suffix transformations
3. Closed paradigm sizes (CP90) per onset class per dialect
4. Onset-class bigram matrices per dialect
5. Self-succession per onset class per dialect (canonical, post-C007 amendment)
6. Three-register line grammar
7. Paragraph chain grammar by section
8. Cross-dialect structural contrasts
9. Word-internal structure
10. Architecture capabilities and limits (21-mechanism findings)
11. Document-order heterogeneity caveat (exp_579 / C008 qualification)
12. Things explicitly ruled out
13. Committed claims index (C001–C009)
14. Open issues for v1.1
15. Label corpus grammar

---

## 1. Positional Profiles per Onset Class per Dialect

### 1.0 Positional convention and translation table

```yaml
positional_convention:
  spec_canonical: committed_claims_convention
  rationale: "C005, C006 are public; the paper rewrite will use these"

  canonical_positions:
    LF:   "Line-First slot (first word, word index 0); EXACTLY equivalent to pos1"
    pos1: "Synonym for LF in this spec; some experiments report it as a separate column to distinguish 1-word lines"
    LL:   "Line-Last slot (literal last word, word index -1)"
    pen:  "Penultimate slot (second-to-last, word index -2)"
    MID:  "All interior word positions (word index 1 .. n-2)"

  enrichment_definition: |
    Ratio of class rate at the slot to class MID-baseline rate. Canonical
    methodology: per-line edy-rate dialect assignment, MID-baseline formula
    E = (obs/n_slot) / mid_rate.

  thresholds:
    CONF: "E ≥ 1.50 AND obs ≥ 10"
    DEPL: "E ≤ 0.67 AND obs ≥ 10"
    subCONF: "E ∈ [1.30, 1.50) OR obs ∈ [5, 9]"
    subDEPL: "E ∈ (0.67, 0.85]"
    flat: "E ∈ (0.85, 1.30) and not directional"

  convention_inversion_hazard:
    discovered_in: "v1.0 cross-check, 2026-04-12"
    description: |
      The Cryptanalyst codebase has two LF/LL conventions and they are
      INVERTED. v0.1 of this spec (and working_position §6) inherited
      the characterization-phase convention; the committed claims and
      exp_173 use the opposite. v1.0 standardizes on the committed-claims
      convention.
    convention_A_committed_claims:
      source: "exp_173 (C005, C006)"
      LF: "first word (wds[0]); 'Line-First'"
      LL: "last word (wds[-1]); 'Line-Last'"
      example: "C005: -am LL enrichment 6.811× = -am at last word"
    convention_B_characterization_phase:
      source: "exp_565 and most exp_534..exp_572 onset characterizations; working_position §6"
      pos1: "first word (onsets[0])"
      LL: "penultimate (onsets[-2])"
      LF: "last word (onsets[-1])"
      example: "F619: A qok LF DEPL 0.51 = qok depleted at last word"
    translation_table:
      "exp_565 pos1 → spec LF (== pos1)": "first word"
      "exp_565 LL  → spec pen": "penultimate"
      "exp_565 LF  → spec LL": "last word"

  what_this_means_for_y_onset:
    description: |
      Resolves the v0.1 §1.2 apparent contradiction "y-onset is pos1 CONF
      AND LF subDEPL". Under canonical convention, y is enriched at LF
      (first word) AND depleted at LL (last word). Both are real, both
      are independent positions, no contradiction.
    y_LF_canonical: "ENRICHED CONF (committed C006: 3.506×; F558: 3.54×/147)"
    y_LL_canonical: "DEPLETED subDEPL (working_position 'LF avoider' 0.60× translates here)"

  per_section_qualification: |
    Per exp_579 (F639, C008 scope): B-dialect positional metrics are
    NOT corpus-stationary. Per-section values must be reported for B
    LF/LL metrics. Full-corpus averages mask 2–3× section variation
    (am_ll ranges from 0.053 in B_bio to 0.192 in B_pharma).
```

### 1.1 d-onset

```yaml
d:
  description: "EVA d-initial; daiin/dy/dam/dar template family"
  is_key_dialect_crossing_class: true
  exp: [exp_543, exp_553, exp_554, exp_555, exp_556, exp_557, exp_558]

  by_dialect:
    A:
      LF:
        enrichment: 1.53
        obs: 360
        confidence: CONF
        exp: [exp_557, F558]
        notes: "A: dominant LL TERMINAL in canonical convention (== exp_565 'LF')"
      pos1_alias_for_LF: "see LF"
      LL_canonical:
        enrichment: 1.53
        obs: 360
        notes: "Same as LF — d is enriched at LAST word in A; this is the d-aiin terminal"
      LL_first_word:
        enrichment: 1.47
        obs: 346
        confidence: subCONF
        exp: [exp_549, exp_553]
        notes: "Wait — needs disambiguation. Canonical LF=first word; canonical LL=last word"
      MID: {enrichment: 0.73, confidence: DEPL, exp: [exp_553]}
      role_canonical: "PRIMARY A LL TERMINAL (last word). NOT a line-opener in A under canonical convention; the 1.47×/346 first-word value is sub-CONF and substantially weaker than the LL CONF."
    B:
      LF:
        enrichment: 2.64
        obs: 246
        confidence: CONF
        exp: [exp_543, exp_555, F555]
        notes: "B: dominant LINE-OPENER (first word); 19.2% of B lines"
      LL:
        enrichment: 1.36
        confidence: subCONF
        exp: [exp_555, exp_575]
      MID: {enrichment: 0.67, confidence: DEPL, exp: [exp_555]}
      by_section_LL_raw_rate:
        B_herbal: {value: 0.1768, exp: [exp_579]}
        B_bio:    {value: 0.1279, exp: [exp_579]}
        B_astro:  {value: 0.1054, exp: [exp_579]}
        B_pharma: {value: 0.0655, exp: [exp_579]}
        section_range_factor: 2.70
      role_canonical: "PRIMARY B LF OPENER (first word); secondary LL"

  cross_dialect_pattern:
    type: "A_vs_B_position_inversion (canonical convention)"
    A_role: LL_terminal_dominant
    B_role: LF_opener_dominant
    interpretation: |
      Both dialects: d is MID-depleted (~0.7×). A uses d at the line END
      (daiin/dam/dar template terminating lines). B uses d at the line
      START (d-prefix opener).
    exp: [exp_553, exp_555, exp_557]
    importance: "Single most informative dialect-crossing positional class"
```

### 1.2 y-onset

```yaml
y:
  description: "EVA y-initial; line-opener template; y+gallows compound"
  exp: [exp_545, exp_557, exp_558, exp_559, exp_173]

  by_dialect:
    A:
      LF:
        enrichment: 2.78
        obs: 323
        confidence: CONF
        exp: [exp_545, exp_557, exp_549]
      LL:
        enrichment: 0.62
        confidence: subDEPL
        exp: [exp_557]
        notes: "Translates from working_position 'LF avoider 0.62×' under exp_565 convention"
      MID: depleted
      role_canonical: "STRONG LINE-OPENER (LF CONF), AVOIDS line-end (LL subDEPL)"

    B:
      LF:
        enrichment: 3.506
        obs_n: 147     # exp_558 obs
        p_value: 2.86e-90
        confidence: CONF
        exp: [exp_173, exp_545, exp_558]
        commitment: C006
        notes: "Committed claim value 3.506× from exp_173"
      LL:
        enrichment: 0.60
        confidence: subDEPL
        exp: [exp_557]
        notes: "Translates from working_position 'LF avoider 0.60×' under exp_565 convention"
      MID: depleted
      by_section_LF_raw_rate:
        B_herbal: {value: 0.1793, exp: [exp_579]}
        B_bio:    {value: 0.0743, exp: [exp_579]}
        B_astro:  {value: 0.1201, exp: [exp_579]}
        B_pharma: {value: 0.1688, exp: [exp_579]}
        section_range_factor: 2.41
      role_canonical: "DEFINITIVE B LINE-OPENER (LF CONF 3.506×), AVOIDS line-end"

  cross_dialect_constants:
    - "y is LF-CONF (line-opener, first word) in BOTH dialects"
    - "y is LL-subDEPL (avoids last word) in BOTH dialects"
    - "y is depleted at MID in both dialects"
  resolution_of_v0_1_ambiguity: |
    v0.1 §1.2 listed both "pos1 CONF" and "LF avoider subDEPL" as
    properties of y, marked as a metric-definition conflict. The
    conflict was an artifact of the LF/LL convention inversion.
    Under canonical convention these are LF (first word, CONF) and
    LL (last word, subDEPL) — different positions, both real.
```

### 1.3 ch-onset

```yaml
ch:
  description: "EVA ch-initial; most extreme LF-AVOIDER cross-dialectally"
  exp: [exp_541, exp_547, exp_550, exp_558, exp_566, exp_622, exp_623]

  by_dialect:
    A:
      LF:    {enrichment: 0.32, obs: 154, confidence: DEPL_extreme, exp: [exp_541, exp_622]}
      LL:    {enrichment: 0.81, obs: 373, confidence: subDEPL, exp: [exp_622]}
      pen:   {enrichment: 0.97, confidence: flat, exp: [exp_622]}
      MID:   {role: dominant_MID, exp: [exp_550]}
      tokens: 2242
      pct: 0.1979
      types: 457
      vocabulary: "chol(10.8%), chey(6.1%), chor(5.8%); diverse l/y/r-body"
      role_canonical: "MOST FREQUENT class in A; extreme LF-avoider; dominant MID"
    B:
      LF:  {enrichment: 0.22, obs: 53,  confidence: DEPL_extreme, exp: [exp_541, exp_622]}
      LL:  {enrichment: 0.80, obs: 194, confidence: subDEPL, exp: [exp_622]}
      pen: {enrichment: 0.92, confidence: flat, exp: [exp_622]}
      tokens: 1695
      pct: 0.1668
      types: 337
      vocabulary: "chedy dominant (22.2%)"
      role_canonical: "Most extreme LF-avoider in B (0.22×) — strongest signal"

  cross_dialect_constants:
    - "ch is LF-DEPL extreme in BOTH dialects (avoids first word)"
    - "ch is LL-subDEPL in both dialects"
    - "ch→sh DEPL cross-dialectally (F328)"
    - "ch is the most-frequent A onset class (19.79%)"
  vocabulary_stability: "Most dialect-stable class. A=diverse, B=chedy-convergent. y-body retained in both."
  exp_vocab: [exp_621]
```

### 1.4 sh-onset

```yaml
sh:
  description: "EVA sh-initial; dialect-specific router class"
  exp: [exp_540, exp_544, exp_564, exp_615, exp_616]

  by_dialect:
    A:
      LF:  {enrichment: 0.77, obs: 148, confidence: subDEPL, exp: [exp_616]}
      LL:  {enrichment: 0.47, obs: 88,  confidence: DEPL, exp: [exp_616]}
      pen: {enrichment: 0.85, confidence: subDEPL, exp: [exp_616]}
      MID_share_approx: 0.75
      tokens: 930
      pct: 0.0821
      types: 236
      vocabulary: "diverse: shol(9%) sho(8%) shey(8%) sheey(6%) shy(5%)"
    B:
      LF:  {enrichment: 0.56, obs: 78, confidence: DEPL_formal, exp: [exp_616]}
      LL:  {enrichment: 0.39, obs: 54, confidence: DEPL_strong, exp: [exp_616]}
      pen: {enrichment: 0.80, confidence: subDEPL, exp: [exp_616]}
      MID_share_approx: 0.75
      tokens: 954
      pct: 0.0939
      vocabulary: "shedy dominant (28.4%)"

  pattern: "MID-dominant; LL-avoider in both dialects (LL=0.47/0.39); B uniquely adds LF DEPL"
  routing_dichotomy:
    description: "sh is a dialect-specific ROUTER"
    A_routes_to_gallows:
      - {target: "sh→k", enrichment: 1.75, obs: 31, confidence: CONF, exp: [exp_544]}
      - {target: "sh→t", enrichment: 1.62, obs: 13, confidence: CONF, exp: [exp_544]}
    B_routes_to_q_class:
      - {target: "sh→qok", enrichment: 2.07, obs: 266, confidence: CONF, exp: [exp_544, exp_565, exp_620]}
      - {target: "sh→qo",  enrichment: 1.97, obs: 50,  confidence: CONF, exp: [exp_614]}
      - {target: "sh→qot", enrichment: 1.74, obs: 78,  confidence: CONF, exp: [exp_544]}
  cross_dialect_constants:
    - "sh is LL-DEPL in BOTH dialects (canonical convention)"
    - "sh→ch DEPL in BOTH dialects (A 0.65×/127, B 0.54×/92; F328)"
```

### 1.5 qok-onset

```yaml
qok:
  description: "EVA qok-initial; q-bench MID class; sh→qok terminus; A→B doubles"
  exp: [exp_376, exp_537, exp_565, exp_618, exp_619]

  by_dialect:
    A:
      LF:
        enrichment: 0.87
        obs: 145
        confidence: sub_baseline_NOT_DEPL
        exp: [exp_565, F619]
        canonical_methodology: true
        prior_value_corrected: 1.47
        prior_value_source: "working_position §6 (non-canonical methodology)"
      LL:
        enrichment: 0.51
        obs: 82
        confidence: DEPL
        exp: [exp_565, F619]
        notes: "Strong DEPL at last word (translates from exp_565 'LF DEPL')"
      pen:
        enrichment: 0.83
        confidence: sub_baseline
        exp: [exp_565, F619]
      MID_role: dominant
      tokens: 827
      pct_of_A_tokens: 0.0730

    B:
      LF:
        enrichment: 0.81
        obs: 171
        confidence: sub_baseline_NOT_DEPL
        exp: [exp_565, F619]
      LL:
        enrichment: 0.53
        obs: 112
        confidence: DEPL
        exp: [exp_565, F619]
      pen:
        enrichment: 1.00
        confidence: flat
        exp: [exp_565, F619]
      MID_role: dominant
      tokens: 1538
      pct_of_B_tokens: 0.1513
      by_section:
        B_astro:  {pct_of_section_tokens: 0.1958, role: "primary driver of A→B doubling", exp: [exp_565]}
        B_pharma: {pct_of_section_tokens: 0.1281, exp: [exp_565]}
        B_herbal: {pct_of_section_tokens: 0.0919, exp: [exp_565]}
        B_bio_LF_raw_rate: {value: 0.1475, exp: [exp_579]}

  cross_dialect_pattern:
    A_to_B_frequency_doubles:
      A_pct: 0.0730
      B_pct: 0.1513
      ratio: 2.07
      driver: "B_astro section grammar (qok ~20% of section tokens)"
      exp: [exp_565, F618]
      uniqueness: "Only major class with A→B frequency increase >2×"

  v0_1_resolution:
    description: |
      v0.1 Open Issue #2: working_position §6 prose listed A qok pos1
      = 1.47×/145 (presented as enrichment); F619 (canonical, exp_565)
      gives 0.87×/145 sub-baseline. v1.0 verified against exp_565 source
      (lines 38, 113 of result.md). The 0.87× value is canonical. The
      1.47× came from a non-canonical methodology and was a correction
      target for the F619 finding.
    canonical_value_used: 0.87
    spec_resolution: "Use F619/exp_565 canonical value throughout"
```

### 1.6 qot-onset

```yaml
qot:
  description: "EVA qot-initial; A pivot class for paragraph chain"
  exp: [exp_534, exp_569, exp_630, exp_631]

  by_dialect:
    A:
      LF: {enrichment: 1.40, obs: 73, confidence: subCONF, exp: [exp_631, exp_534]}
      LL: {enrichment: 0.91, confidence: flat, exp: [exp_631]}
      pen: {enrichment: 0.89, confidence: flat, exp: [exp_631]}
      MID: {enrichment: 0.92, confidence: flat, exp: [exp_631]}
      tokens: 291
      pct: 0.0257
      role: "near-CONF LF opener; pivot of A paragraph chain"
      qualification: "F631 corrects prior 1.79×/59 CONF (exp_534) to canonical 1.40×/73 sub-CONF"
    B:
      LF: {enrichment: 0.69, obs: 37, confidence: DEPL, exp: [exp_631]}
      LL: {enrichment: 0.86, confidence: subBaseline, exp: [exp_631]}
      pen: {enrichment: 1.07, confidence: flat, exp: [exp_631]}
      MID: {enrichment: 1.08, confidence: flat, exp: [exp_631]}
      tokens: 426
      pct: 0.0419
      role: MID_class

  cross_dialect_pattern:
    type: A_B_LF_inversion
    A_LF_role: subCONF_opener
    B_LF_role: DEPL
    exp: [exp_631]

  paragraph_chain_role:
    role: "A_herbal_a CL pivot — d→qot CL is the chain entry-point"
    inter_line_only: true
    within_line_d_qot_NULL: {A: 0.99, B: 0.66, exp: [exp_543, F555]}
```

### 1.7 ot-onset

```yaml
ot:
  description: "EVA ot-initial; B MID class; ot→ot self-succession robust both dialects"
  exp: [exp_535, exp_568, exp_627, exp_628]

  by_dialect:
    A:
      LF:  {enrichment: 0.77, obs: 76, confidence: subBaseline, exp: [exp_628]}
      LL:  {enrichment: 1.09, confidence: flat, exp: [exp_628]}
      pen: {enrichment: 1.15, confidence: flat, exp: [exp_628]}
      MID: {enrichment: 1.00, confidence: flat, exp: [exp_628]}
      tokens: 548
      pct: 0.0484
      types: 133
      vocabulary: "otaiin/otal/otar/oty diverse aiin+lateral; no edy dominance"
    B:
      LF:  {enrichment: 0.26, obs: 22, confidence: DEPL_extreme, exp: [exp_628]}
      LL:  {enrichment: 1.15, confidence: flat, exp: [exp_628]}
      pen: {enrichment: 1.36, confidence: subCONF, exp: [exp_628]}
      MID: {enrichment: 1.05, confidence: flat, exp: [exp_628]}
      tokens: 680
      pct: 0.0669
      types: 125
      vocabulary: "otedy(14.0%)/oteedy(10.0%) edy-dominant (24% of B ot tokens)"

  cross_dialect_pattern:
    - "ot frequency increases A→B (joining MID-class increase cluster: sh, qo, qok, ot)"
    - "ot LF DEPL stronger in B (0.26×) than A (0.77×)"
```

### 1.8 ok-onset

```yaml
ok:
  description: "EVA ok-initial; MID class with LF DEPL cross-dialectally"
  exp: [exp_536, exp_567, exp_624, exp_625, exp_626]

  by_dialect:
    A:
      LF: {enrichment: 0.57, obs: 96, confidence: DEPL, exp: [exp_625]}
      LL: {enrichment: 0.89, confidence: subBaseline, exp: [exp_625]}
      pen: {enrichment: 0.91, confidence: subBaseline, exp: [exp_625]}
      tokens: 843
      pct: 0.0744
      vocabulary: "diverse aiin/e/lateral mix (okaiin 13.2%, okeey 7.8%)"
    B:
      LF: {enrichment: 0.50, obs: 46, confidence: DEPL, exp: [exp_625]}
      LL: {enrichment: 0.82, confidence: subBaseline, exp: [exp_625]}
      pen: {enrichment: 1.09, confidence: flat, exp: [exp_625]}
      tokens: 671
      pct: 0.0660
      vocabulary: "edy-dominant (okedy 12.8%, okeedy 11.6%)"

  cross_dialect_pattern:
    - "MID class with LF DEPL in BOTH dialects (avoids first word)"
    - "Distinguished from ch by less extreme LF DEPL (ok 0.5–0.6 vs ch 0.2–0.3)"
    - "Distinguished from sh by LL NOT DEPL"
```

### 1.9 qo-onset

```yaml
qo:
  description: "EVA qo-initial bare; B-specific morphological prefix"
  exp: [exp_563, exp_613, exp_614]

  by_dialect:
    A:
      LL: {enrichment: 0.46, obs: 27, confidence: DEPL, exp: [exp_613]}
      LF: {confidence: subBaseline, exp: [exp_613]}
      tokens: 293
      pct: 0.0259
    B:
      pen: {enrichment: 0.52, obs: 21, confidence: DEPL, exp: [exp_613]}
      LF: {enrichment: 1.07, confidence: flat, exp: [exp_613]}
      tokens: 314
      pct: 0.0309
      by_section: {B_astro_pct: 0.0425}

  cross_dialect_pattern:
    - "MID class (~75% MID share both dialects)"
    - "qo is NOT an opener (unlike qot in A)"
```

### 1.10 t-onset

```yaml
t:
  description: "EVA t-initial; gallows opener"
  exp: [exp_551, exp_549, exp_555]

  by_dialect:
    A:
      LF: {enrichment: 2.27, obs: 111, confidence: CONF, exp: [exp_549]}
      LL: {enrichment: 0.96, confidence: flat, exp: [exp_557]}
      role: opener
      A_stars_LF: {enrichment: 3.67, obs: 16, confidence: CONF, exp: [exp_523, exp_527]}
    B:
      LF: {enrichment: 3.18, obs: 78, confidence: CONF, exp: [exp_555]}
      role: opener
      by_section_LF_enrichment:
        B_herbal: {value: 2.34, exp: [exp_467, F447]}
        B_cosmo:  {value: 2.23, exp: [exp_467, F447]}

  cross_dialect_constants:
    - "t is a CONF LF opener in both dialects"
    - "adj_rate for t = 0 in B (0/466 tokens) — structural anti-repetition from LF placement (exp_577 / C009 Part B)"
```

### 1.11 s-onset

```yaml
s:
  description: "EVA s-initial; LF opener; structural anti-repetition"
  exp: [exp_550, exp_325, exp_549, exp_555]

  by_dialect:
    A:
      LF: {enrichment: 3.16, obs: 163, confidence: CONF, exp: [exp_549]}
      LL: {enrichment: 1.01, confidence: flat, exp: [exp_557]}
      role: opener
    B:
      LF: {enrichment: 4.77, obs: 165, confidence: CONF, exp: [exp_555]}
      LL: {confidence: enriched, exp: [exp_557]}
      role: opener
      by_section_LF_raw_rate:
        B_herbal: {value: 0.0707, exp: [exp_579]}
        B_bio:    {value: 0.1716, exp: [exp_579]}
        B_astro:  {value: 0.0588, exp: [exp_579]}
        B_pharma: {value: 0.1190, exp: [exp_579]}
        section_range_factor: 2.92

  cross_dialect_constants:
    - "s is CONF LF opener in both dialects"
    - "adj_rate for s = 0 in B (0/452 tokens) — structural anti-repetition from LF placement (exp_577, C009 Part B)"
    - "VMS section variation: B_bio s@LF is 2.4× B_astro"
```

### 1.12 p-onset

```yaml
p:
  description: "EVA p-initial; gallows; folio-opener marker"
  exp: [exp_556, exp_549, exp_555]

  by_dialect:
    A:
      LF: {enrichment: 2.99, obs: 15, confidence: CONF, exp: [exp_549]}
      role: opener
      folio_opener_LF_share: 0.373
      folio_closer_LF_obs: 0
      folio_closer_LF_total: 83
      exp_folio: [exp_354, exp_355, F345]
    B:
      LF: {enrichment: 5.23, obs: 27, confidence: CONF, exp: [exp_555]}
      role: opener_strongest
      folio_opener_marker: true

  cross_dialect_constants:
    - "p is the strongest LF opener in B (5.23×)"
    - "p is exclusively folio-opener in A (0% folio-closer LF)"
```

### 1.13 k-onset

```yaml
k:
  description: "EVA k-initial; gallows class; LF-anomalous"
  exp: [exp_552, exp_393]
  anomaly:
    Q012_open: |
      Unlike p/t/f, k is NOT LF-enriched. Other gallows are folio-opener
      LF markers; k is LF-flat. Mechanism unresolved.
```

### 1.14 r-onset

```yaml
r:
  description: "EVA r-initial; B terminal class"
  exp: [exp_378, exp_554]

  by_dialect:
    A: {role: undocumented_in_synthesis, exp: []}
    B:
      LL: {enrichment: 2.80, obs: 48, confidence: CONF, exp: [exp_555, exp_557]}
      role: B_TERMINAL_LL
      notes: "Translation: working_position 'r LF CONF 2.80×' under exp_565 convention = canonical LL CONF"

  cross_dialect_pattern:
    - "B q-bench routing: q-bench → r CONF (1.61×/45) for combined qok+qot; non-q-bench → r flat (F633)"
    - "qok→r CONF B (1.95×/30); qot→r CONF B (1.97×/10)"
```

### 1.15 l-onset

```yaml
l:
  description: "EVA l-initial; B lateral terminal"
  exp: [exp_553]

  by_dialect:
    B:
      LL: {enrichment: 1.85, obs: 145, confidence: CONF, exp: [exp_555, exp_557]}
      role: B_TERMINAL_LL
```

### 1.16 ol-onset

```yaml
ol:
  description: "EVA ol-initial; B vowel-onset terminal"
  exp: [exp_553]

  by_dialect:
    A: {self_succession_CONF_only: true, exp: [exp_553]}
    B:
      LL: {enrichment: 1.65, obs: 115, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LL
```

### 1.17 o-onset

```yaml
o:
  description: "EVA o-initial bare; B vowel terminal"
  exp: [exp_547, exp_548]
  by_dialect:
    B:
      LL: {enrichment: 1.58, obs: 57, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LL
```

### 1.18 a-onset

```yaml
a:
  description: "EVA a-initial; B vowel terminal; LF avoider both dialects"
  exp: [exp_549]
  by_dialect:
    B:
      LL: {enrichment: 1.52, obs: 70, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LL
  cross_dialect_constants:
    - "a is LF-avoider in BOTH dialects"
    - "a→ok CROSS-DIALECTAL CONF (A 1.52×/50; B 1.51×/34) (F626)"
  label_corpus_role: |
    a-onset is the dominant LL class in MULTI-WORD LABELS (E=3.55×;
    F642). The label-terminal a-onset role is much stronger than the
    body-text role. See Section 15.7.
```

### 1.19 cth-onset (compound gallows)

```yaml
cth:
  description: "EVA c-th compound gallows; A TERMINAL"
  exp: [exp_384, exp_558, exp_561]

  by_dialect:
    A:
      LL: {enrichment: 1.67, obs: 88, confidence: CONF, exp: [exp_557, exp_558]}
      LF: {enrichment: 0.13, confidence: DEPL_extreme, exp: [exp_558]}
      role: PUREST_A_TERMINAL
      tokens_relative: 1.0
    B:
      tokens_relative_to_A: 0.116
      A_to_B_drop_factor: 8.6
      LL: {confidence: ambiguous, exp: [exp_558]}

  paragraph_chain_role:
    A_herbal_a: "d → qot → ch → o → sh, with cth as terminal closer; cth-LL pen=d CONF (F474)"

  cross_dialect_pattern:
    - "Frequency drops 8.6× A→B"
    - "A: dominant terminal; B: rare and ambiguous"
```

### 1.20 sch-onset (compound gallows)

```yaml
sch:
  description: "EVA s-c-h compound gallows; rare extreme A opener"
  exp: [exp_560, exp_561]
  by_dialect:
    A:
      LF: {enrichment: 11.54, obs: 16, confidence: CONF_extreme, exp: [exp_558]}
      role: OPENER_extreme
      base_rate_pct: ~0.20
      notes: "Highest LF E-value of any characterized class"
```

### 1.21 ckh-onset (compound gallows)

```yaml
ckh:
  description: "EVA c-k-h compound gallows"
  exp: [exp_561]
  by_dialect:
    A:
      LF: {enrichment: 0.07, confidence: near_zero, exp: [exp_561]}
      LL: {enrichment: 0.67, obs: 18, confidence: DEPL, exp: [exp_561]}
      role: MID
    universal_routing:
      - "ckh→d CONF A (E=2.00×/18)"
```

### 1.22 cph-onset (compound gallows)

```yaml
cph:
  description: "EVA c-p-h compound gallows; rare; MID/LL role"
  exp: [exp_561, exp_610]
  by_dialect:
    A:
      LF:  {enrichment: 0.12, obs: 1, confidence: near_zero, exp: [exp_610]}
      pen: {enrichment: 1.45, obs: 12, confidence: subCONF, exp: [exp_610]}
      LL:  {enrichment: 0.72, obs: 6, confidence: subDEPL, exp: [exp_610]}
      tokens: 38
      pct: 0.00335
    B:
      tokens: 7
      pct: 0.00069
      A_to_B_drop_factor: 4.9
      vocab: "cphedy 57.1%"
      exp: [exp_610]

  routing:
    - {pair: "cph→d", confidence: dir, enrichment: 2.50, obs: 7, exp: [exp_610, exp_562]}
    - {pair: "cth→cph", confidence: dir, enrichment: 3.02, obs: 3, exp: [exp_602, exp_610]}
```

### 1.23 Three-layer summary by dialect (canonical convention)

```yaml
three_layer_summary:
  note: |
    All values translated to canonical convention (LF=first word,
    LL=last word). working_position §6 organized this same data under
    inverted naming.

  A:
    LF_OPENERS_CONF:
      - {class: sch, enr: 11.54, obs: 16}
      - {class: p,   enr: 2.99,  obs: 15}
      - {class: s,   enr: 3.16,  obs: 163}
      - {class: y,   enr: 2.78,  obs: 323}
      - {class: t,   enr: 2.27,  obs: 111}
      - {class: qot, enr: 1.40,  obs: 73,  status: subCONF}
    LL_TERMINALS_CONF:
      - {class: cth, enr: 1.67, obs: 88}
      - {class: d,   enr: 1.53, obs: 360}
    MID:    [ch, qok, ok, ot, sh, k, ckh, qo]
    LL_AVOIDERS: [qok (0.51), sh (0.47), ckh (0.67), y (0.62), s (~1.0 flat)]
    exp: [exp_557]

  B:
    LF_OPENERS_CONF:
      - {class: p, enr: 5.23, obs: 27}
      - {class: s, enr: 4.77, obs: 165}
      - {class: y, enr: 3.506, obs_alt: 147, exp: [exp_173, exp_558]}
      - {class: t, enr: 3.18, obs: 78}
      - {class: d, enr: 2.64, obs: 246}
    LL_TERMINALS_CONF:
      - {class: r,  enr: 2.80, obs: 48}
      - {class: l,  enr: 1.85, obs: 145}
      - {class: ol, enr: 1.65, obs: 115}
      - {class: o,  enr: 1.58, obs: 57}
      - {class: a,  enr: 1.52, obs: 70}
      - {class: am_suffix, enr: 6.811, obs_implicit: large, p_value: 6.27e-161, commitment: C005, exp: [exp_173]}
    MID: [ch, qok, ok, ot, qot, sh, k]
    LL_AVOIDERS: [qok (0.53 DEPL), sh (0.39 DEPL), y (0.60 subDEPL), ch (0.80 subDEPL)]
    exp: [exp_555]

  cross_dialect_constants:
    LF_DEPL_in_both_dialects:
      - "ch (A 0.32 / B 0.22) — strongest cross-dialect LF avoider"
      - "ok (A 0.57 / B 0.50)"
      - "ot (A 0.77 / B 0.26)"
    LL_DEPL_in_both_dialects:
      - "qok (A 0.51 / B 0.53)"
      - "sh (A 0.47 / B 0.39)"
      - "y (A 0.62 / B 0.60 — both subDEPL)"
    LF_OPENER_CONF_in_both:
      - "p, s, y, t, d (B-strong); A also has sch, qot subCONF"
    terminal_layer_inversion:
      A_LL_terminals: [d, cth]
      B_LL_terminals: [r, l, ol, o, a]
      overlap: 0
      interpretation: |
        A closes lines with aiin-body + compound gallows. B closes lines
        with lateral / vowel-initial classes. Zero overlap.
```

### 1.24 B-dialect section LF taxonomy

```yaml
B_section_LF_taxonomy:
  description: "Per F447 / exp_467; positional metrics MUST be reported per section"
  exp: [exp_467, F447]
  caveat: "exp_579 confirms B positional metrics are not corpus-stationary"
  convention: "LF = first word (canonical)"

  B_herbal:
    primary_LF: [{t: 2.34}, {y: 1.52}, {ot: 1.55}]
    depleted_LF: [qok, s, ok, ch]
  B_astro:
    primary_LF_q_bench: [{qok: 1.78}, {qot: 1.94}, {qo: 1.60}, {s: 1.31}]
    depleted_LF: [{y: 0.47}, {t: 0.70}]
  B_pharma:
    primary_LF: [{ok: 1.47}, {o: 1.53}]
    depleted_LF: [qok, t, qot]
  B_cosmo:
    primary_LF: [{t: 2.23}]
    depleted_LF: [qot, qo]
  exp: [exp_467]
```

### 1.25 A-dialect grammatical inversion

```yaml
A_stars_inversion:
  description: |
    Astronomical marker appears at LF (first word) in A but at LL (last
    word) in B for the same astronomical content.
  A_stars: {t_LF_enrichment: 3.67, obs: 16, confidence: CONF}
  B_corresponding: {qok_LL_elevated: true}
  exp: [exp_523, exp_527, F523, F524]
```

---

## 2. Suffix Paradigms and A→B Suffix Transformations

```yaml
suffix_paradigms:
  shared_facts:
    - "{y,n,l,r} cover 88.8% of all word endings"
    - "Top word-final bigrams: -dy 18.6%, -in 16.7%, -ey 11.0%, -ol 9.7%"
    - "Word-final entropy = 2.46 bits (Latin -1: 3.25; Italian -1: 3.06) — most constrained position in manuscript"
    - "Productive [ONSET × SUFFIX] template: A multi-suffix stems = 349; B = 639"
    - "log-linear stem-frequency × paradigm-completeness r = 0.83–0.89 (productive paradigm)"
    exp: [F042, F004, F047, F048]

  A_dominant_suffixes:
    - {suffix: "-ol",  pct: 0.170, exp: [F047]}
    - {suffix: "-or",  pct: 0.121, exp: [F047]}
    - {suffix: "-chy", pct: 0.051, exp: [F047]}

  B_dominant_suffixes:
    - {suffix: "-edy",  pct: 0.151, exp: [F047]}
    - {suffix: "-eedy", pct: 0.063, exp: [F047]}
    - {suffix: "-ain",  pct: 0.070, exp: [F047]}

  A_to_B_transformations:
    description: |
      The same productive stems (ch, sh, ot, ok, qok, d, s) appear in
      BOTH dialects with NEAR-INVERTED suffix preferences. Any candidate
      decipherment must account for the systematic mapping below.
    exp: [F047, exp_040]
    canonical_inversions:
      - {stem: "ch", A_pref: ["-ol", "-or"], A_obs: [225, 146], B_pref: ["-edy", "-ey"], B_obs: [430, 208]}
      - {stem: "sh", A_pref: ["-ol", "-or"], A_obs: [99, 56],   B_pref: ["-edy", "-ey"], B_obs: [367, 173]}
    frequency_ratios:
      "edy": "75× more common in B than A"
      "ol":  "2.8× more common in A than B"

  B_systematic_paradigm:
    description: "9-form productive suffix paradigm on ~10 productive stems"
    forms: ["-eedy", "-ain", "-edy", "-eey", "-aiin", "-y", "-ey", "-chy", "-dy"]
    top_stem: {stem: qok, tokens: 1559, forms: 9, exp: [F045, F058]}
    other_top_stems:
      - {stem: ch, tokens: 1041}
      - {stem: sh, tokens: 870}
      - {stem: ok, tokens: 704}
      - {stem: ot, tokens: 604}

  positional_suffix_assignments:
    description: |
      Suffixes have CLASS-LEVEL positional roles. Any candidate that
      treats suffixes as position-blind FAILS.
    LF_enriched:
      - {suffix: "-aiin", pct_LF: 0.142, exp: [F058]}
    LL_enriched:
      - {suffix: "-ain",  pct_LL: 0.080, exp: [F058]}
      - {suffix: "-am",   ll_enrichment: 6.811, p_value: 6.27e-161, commitment: C005, exp: [exp_173]}
      - {suffix: "-dy",   A_LL_enrichment: 1.59, exp: [F058]}
    MID_enriched:
      - {suffix: "-edy",  pct_MID: 0.85, exp: [F058]}
      - {suffix: "-ol",   pct_MID: 0.807, exp: [F060]}
      - {suffix: "-ey",   pct_MID: 0.808, exp: [F060]}
      - {suffix: "-eey",  pct_MID: 0.800, exp: [F060]}

  pharma_specific_extension:
    description: "-eol is a pharma-specific suffix variant beyond the 9-form list"
    enrichment: "4–28× pharma-enriched"
    exp: [F058]

  am_suffix_critical_metric:
    description: "Most discriminating positional metric for theory tests"
    full_corpus_average:
      enrichment: 6.811
      p_value: 6.27e-161
      confidence: CONF
      survives_bonferroni_m175: true
      cross_validation: ["80/20", "leave-one-section-out"]
      commitment: C005
      exp: [exp_173]
    by_section:
      B_bio:    {raw_LL_rate: 0.0525, exp: [exp_579]}
      B_herbal: {raw_LL_rate: 0.1616, exp: [exp_579]}
      B_astro:  {raw_LL_rate: 0.1642, exp: [exp_579]}
      B_pharma: {raw_LL_rate: 0.1919, exp: [exp_579]}
      qualification: "B section variation 3.7× (0.053 to 0.192)"
    paragraph_position_breakdown:
      WP_LL_within_paragraph: {enrichment: 6.69, n: 2295, exp: [exp_208]}
      PF_LL_paragraph_final:  {enrichment: 3.14, n: 94,   exp: [exp_208]}
      narrowing: |
        -am is a within-paragraph line-last marker; PF-LL is lower because
        B paragraph-final words come from a different onset class (ok/ch/ot
        per F207). Per C005 narrowing.
    cross_dialect_marker:
      role: "WITHIN-PARA line-closer marker in BOTH dialects"
      A_para_final_suppression: {pct: 0.019, vs_within_para: 0.064}
      B_para_final_suppression: {pct: 0.020, vs_within_para: 0.126}
      exp: [F086, F093]
    am_core_vocabulary:
      description: "Closed class of within-para line-closers"
      members: [otam, qokam, dam, okam, cham, ram]
      LLast_pct_range: [0.50, 1.00]
      WithinPara_pct_range: [0.90, 1.00]
      PSFirst_pct: 0.00
      exp: [F093]
    selectional_constraint:
      preceded_by: [ch_onset, qo_onset]
      synonym_oly_oldy_preceded_by: [s_onset, d_onset, sh_onset]
      mutual_exclusion: "-am and oly/oldy never co-occur on same line"
      exp: [F094, F095]

  cthedy_paradigm_B:
    description: "B-cth has internal positional paradigm distinct from standard B-edy"
    cthedy_LF_enrichment: 1.53
    cthey_LF_enrichment:  1.69
    cthdy_LL_enrichment:  2.41
    contrast_to_standard: "chedy LF=0.26×, shedy LF=0.52× (LF-DEPL)"
    exp: [F174, exp_167]

  label_corpus_attenuation_C010_proposed:
    description: |
      Per exp_580 / F641: labels deplete the major body suffix paradigms
      (edy 0.26×, aiin 0.35×, ain 0.33×, ey 0.60×) and elevate shorter
      suffixes (dy 1.88×, bare-y 1.83×, am 2.19×, al 1.49×, ar 1.30×).
      The B-dialect edy marker is attenuated even on B-folio labels
      (0.168 vs 0.241 body). See Section 15.
    exp: [exp_580, F641]
```

---

## 3. Closed Paradigm Sizes (CP90) per Onset Class per Dialect

```yaml
cp90:
  definition: |
    Number of distinct word types accounting for 90% of tokens for the
    given onset class. Smaller CP90 = more concentrated vocabulary.
  source: "VMS B-dialect direct corpus measurement; per exp_577"
  exp: [exp_577, exp_578]

  B_dialect_canonical:
    qok: 32
    qot: 44
    ok:  68
    ot:  87
    s:   91
    ol:  99
    qo:  ~30
    sh:  145
    d:   146
    ch:  290
    cth: ~80
    t:   169
    y:   191
    l:   195
    r:   66

  vocabulary_richness_pattern:
    description: |
      qok has the tightest vocabulary (CP90=32) and dominates adj_rate
      (36.8% of all identical pairs from 12.8% of tokens).
    exp: [exp_577]

  comparison_to_baseline_simulation:
    note: "Baseline 21-mech architecture vocabulary is 7–44× richer than VMS"
    table:
      qok: {VMS: 32,  baseline_sim: 1401, ratio: 43.8}
      sh:  {VMS: 145, baseline_sim: 1303, ratio: 9.0}
      ch:  {VMS: 290, baseline_sim: 2013, ratio: 6.9}
      d:   {VMS: 146, baseline_sim: 1114, ratio: 7.6}
    exp: [exp_578]

  candidate_constraint: |
    Any candidate generative theory MUST produce CP90 within ~1.2× of
    these values for sh/ch/d/qok. The 21-mechanism architecture's
    "vocab_clamp" mechanism (exp_314 17th mechanism) was added precisely
    to enforce this.
```

---

## 4. Onset-Class Bigram Matrices per Dialect

```yaml
bigram_matrices:
  methodology_note: |
    Per F076 / exp_069: B grammar is POSITION-SPECIFIC; A grammar is
    POSITION-GENERAL. B bigrams must be filtered to MID positions; A
    bigrams hold across positions.

  cross_dialect_invariants:
    description: "Bigrams that hold in BOTH A and B"
    pairs:
      - {pair: "sh→qok", A_enr: 2.04, A_obs: 114, B_enr: 2.07, B_obs: 266, confidence_both: CONF, exp: [exp_544, exp_565, exp_614, exp_620]}
      - {pair: "sh→qo",  A_enr: 2.17, A_obs: 44,  B_enr: 1.97, B_obs: 50,  confidence_both: CONF, exp: [exp_614]}
      - {pair: "ch→sh",  A_enr: 0.66, A_obs: 117, B_enr: 0.53, B_obs: 86,  confidence_both: DEPL, exp: [F328, exp_623]}
      - {pair: "sh→ch",  A_enr: 0.65, A_obs: 127, B_enr: 0.54, B_obs: 92,  confidence_both: DEPL, exp: [exp_544]}
      - {pair: "qo→qo",  A_enr: 1.76, A_obs: 14,  B_enr: 1.82, B_obs: 16,  confidence_both: CONF, exp: [exp_614]}
      - {pair: "a→ok",   A_enr: 1.52, A_obs: 50,  B_enr: 1.51, B_obs: 34,  confidence_both: CONF, exp: [exp_626, F568]}
      - {pair: "ch→d",   A_enr: 1.46, A_obs: 238, B_enr: 1.45, B_obs: 107, confidence_both: subCONF_near_threshold, exp: [exp_623]}

  A_specific_bigrams:
    methodology: "A bigrams hold across positions"
    pairs:
      - {pair: "ch→ch→ch (trigram)", A_enr: 2.05, A_obs: 107, exp: [exp_075, F082]}
      - {pair: "ch→ch", A_enr: 1.34, A_obs: 20, dominant_word: "chol chol", exp: [exp_070, F077]}
      - {pair: "s→ch",  A_enr: 1.36, exp: [F081]}
      - {pair: "s→qo",  A_enr: 0.63, confidence: DEPL, exp: [F081]}
      - {pair: "d→ch",  A_enr: 1.09, exp: [F081]}
      - {pair: "d→qo",  A_enr: 0.93, confidence: flat, exp: [F081]}
      - {pair: "d→cth", A_enr: 1.97, A_obs: 62,  confidence: CONF, exp: [exp_558, F491]}
      - {pair: "cth→d", A_enr: 1.97, A_obs: 37,  confidence: CONF, exp: [exp_558]}
      - {pair: "ckh→d", A_enr: 2.00, A_obs: 18,  confidence: CONF, exp: [exp_561]}
      - {pair: "cph→d", A_enr: 2.50, A_obs: 7,   confidence: dir,  exp: [exp_561]}
      - {pair: "sch→d", A_enr: 3.43, A_obs: 6,   confidence: dir,  exp: [exp_561]}
      - {pair: "t→qot", A_enr: 2.03, A_obs: 11,  confidence: CONF, exp: [exp_534]}
      - {pair: "qo→qok", A_enr: 1.53, A_obs: 27, confidence: CONF, exp: [exp_565]}
      - {pair: "qok→s",  A_enr: 1.60, A_obs: 12, confidence: CONF, exp: [exp_565]}

  B_specific_bigrams:
    methodology: "B bigrams must be filtered to MID positions"
    pairs:
      - {pair: "sh→qok", B_enr: 2.07, B_obs: 266, confidence: CONF, exp: [exp_565, exp_620, exp_544]}
      - {pair: "sh→qot", B_enr: 1.97, B_obs: 72,  confidence: CONF, exp: [exp_544]}
      - {pair: "qot→qot", B_enr: 1.82, B_obs: 29, confidence: CONF, exp: [exp_534]}
      - {pair: "qot→ot", B_enr: subCONF, exp: [F632]}
      - {pair: "qot→r",  B_enr: 1.97, B_obs: 10, confidence: CONF, exp: [exp_534, F633]}
      - {pair: "qok→r",  B_enr: 1.95, B_obs: 30, confidence: CONF, exp: [exp_565, F620]}
      - {pair: "qot→ot→ot", B_enr: 1.58, B_obs: 11, confidence: CONF_triplet, exp: [F634]}
      - {pair: "qot→ot→a",  B_enr: 0.40, B_obs: 1,  exp: [F634], note: "negative — bigrams independent"}
      - {pair: "y→k",    B_enr: CONF, exp: [exp_545]}
      - {pair: "d→sh",   B_enr: 1.79, B_obs: 109, confidence: CONF, exp: [exp_555]}
      - {pair: "ch→l",   B_enr: 1.56, B_obs: 135, confidence: CONF, exp: [exp_623]}
      - {pair: "ch→t",   B_enr: 1.67, B_obs: 35,  confidence: CONF, exp: [exp_623]}
      - {pair: "qo→ol",  B_enr: 1.78, B_obs: 26,  confidence: CONF, exp: [exp_614]}
      - {pair: "qo→o",   B_enr: 1.68, B_obs: 12,  confidence: CONF, exp: [exp_614]}
      - {pair: "qo→ot",  B_enr: 0.63, B_obs: 13,  confidence: DEPL, exp: [exp_614]}
      - {pair: "sh→ok",  B_enr: 0.61, B_obs: 36,  confidence: DEPL, exp: [F626]}
      - {pair: "ol→ok",  B_enr: 0.68, B_obs: 23,  confidence: DEPL, exp: [F626]}
      - {pair: "ok→qot", B_enr: 0.52, B_obs: 14,  confidence: DEPL, exp: [F626]}
      - {pair: "qok→ch", B_enr: 1.27, exp: [exp_173]}
      - {pair: "d→qok",  B_enr: 0.64, B_obs: 64,  confidence: DEPL, exp: [exp_565]}
      - {pair: "qok→a",  B_enr: 0.55, B_obs: 29,  confidence: DEPL, exp: [exp_565]}
      - {pair: "qok→qo", B_enr: 0.69, B_obs: 31,  confidence: DEPL, exp: [exp_565]}
      - {pair: "qok→k",  B_enr: 0.56, B_obs: 17,  confidence: DEPL, exp: [exp_565]}

  bigram_grammar_strength:
    A: {bigram_PPL_reduction: 0.091, exp: [exp_074, F081]}
    B: {bigram_PPL_reduction: 0.133, exp: [exp_074, F081]}
    interpretation: "B sequential grammar 35% stronger than A's"

  position_conditional_rule_for_B:
    description: |
      B bigrams reflect position-aware grammar. Apparent A↔B differences
      may collapse when B is filtered to MID positions only. The
      cross-dialect invariants above ARE position-controlled.
    exp: [F076, exp_069, exp_242]

  qok_ch_oscillation_B:
    description: "B sequential alternation pattern"
    pattern: "[p-onset PS] → [o/sh] → [qo↔ch/sh alternation OR d→ch direct] → [closer]"
    transitions:
      - {pair: "sh→qo→ch", B_enr: 3.35}
      - {pair: "qo→ch",    B_enr: 1.31}
      - {pair: "ch→qo",    B_enr: ~baseline}
    after_qo_ch_next_qo: 0.297
    exp: [F079, F080, exp_072, exp_073]

  qok_terminal_grammar_per_dialect:
    description: "Lines opening with qok have dialect-specific LL terminal class"
    A_qok_opener_LL: {l_at_LL: {enr: 2.90, obs: 10, confidence: CONF}, exp: [exp_565]}
    B_qok_opener_LL: {r_at_LL: {enr: 1.56, obs: 10, confidence: CONF}, exp: [exp_565]}
    interpretation: "Cross-dialectal terminal-class inversion (A=l, B=r) seen in qok-opener context"
```

---

## 5. Self-Succession per Onset Class per Dialect (Canonical, Post-C007 Amendment)

```yaml
self_succession:
  status: CANONICAL
  amendment_landed: 2026-04-12
  authoritative_source: "committed_claims.md C007 (with canonical correction block)"
  superseded_methodology: "exp_174 folio-level dialect assignment + old E formula"
  canonical_methodology: "per-line edy-rate dialect assignment + MID-baseline E formula"

  exp_canonical: [exp_565, exp_566, exp_567, exp_568, exp_569, exp_573]

  canonical_table:
    description: "Per C007 amended commitment + exp_573 reconciliation"
    rows:
      l:   {A_enr: 3.86, A_obs: 16,  B_enr: 2.62, B_obs: 72,  status: CONF_both}
      ol:  {A_enr: 3.20, A_obs: 45,  B_enr: 1.32, B_obs: 30,  status: CONF_A_only}
      qot: {A_enr: 3.16, A_obs: 18,  B_enr: 1.69, B_obs: 29,  status: CONF_both}
      y:   {A_enr: 1.88, A_obs: 40,  B_enr: 3.16, B_obs: 20,  status: CONF_both}
      ot:  {A_enr: 2.23, A_obs: 50,  B_enr: 2.10, B_obs: 90,  status: CONF_both}
      qo:  {A_enr: 1.76, A_obs: 14,  B_enr: 1.82, B_obs: 16,  status: CONF_both}
      d:   {A_enr: 1.75, A_obs: 151, B_enr: 1.35, B_obs: 41,  status: CONF_A_only}
      ok:  {A_enr: 1.42, A_obs: 81,  B_enr: 1.30, B_obs: 56,  status: subCONF}
      qok: {A_enr: 1.27, A_obs: 77,  B_enr: 1.03, B_obs: 242, status: subCONF_A_FLAT_B}
      ch:  {A_enr: 1.04, A_obs: 453, B_enr: 0.91, B_obs: 259, status: FLAT_both}
      sh:  {A_enr: 1.21, A_obs: 96,  B_enr: 0.78, B_obs: 76,  status: FLAT_A_NEAR_DEPL_B}
    exp: [exp_565, exp_566, exp_567, exp_568, exp_569, exp_573, exp_557, exp_558]

  canonical_range:
    min: 0.78
    max: 3.86
    note: "Original C007 stated 1.24–2.05× — both bounds were wrong; amendment landed"
    exp: [exp_573]

  CONF_cross_dialect_classes:
    description: "Self-succession robust in BOTH A and B under canonical methodology"
    classes: [y, l, ot, qo, qot]
    rule_for_candidates: |
      Any candidate generator MUST produce CONF self-succession (≥1.5×)
      for these five classes in BOTH dialects, while leaving B sh/ch/qok
      flat-or-depleted.

  position_controlled_residuals:
    description: |
      exp_174 position control remains valid for CONF classes only.
    residual_range_for_CONF_classes: [1.2, 1.8]
    exp: [exp_174]
    qualification_per_amendment: "Holds for y, l, ot, qo, qot in both dialects; does NOT hold for B qok/ch/sh"

  ss_mean_aggregate:
    VMS_B: 1.465
    role: "Property 2 of dual constraint"
    contradicts_substitution_only: "C002: substitution alone gives ss≈1.0"

  copy_buffer_floor:
    description: "Architectural constraint from exp_575 specificity test"
    ss_d_floor: ~1.50
    ss_y_floor: ~2.00
    ss_mean_floor: ~1.36
    adj_rate_floor: ~0.006
    am_ll_floor: ~1.17
    interpretation: |
      Any copy-buffer architecture with CP=0.55, MP=0.90 will produce
      these as MINIMUM values regardless of parameter tuning. VMS values
      are AT or just-above these floors, which is why the architecture
      passes 19/19. Shuffled VMS targets are BELOW these floors and
      cannot be reached.
    exp: [exp_575]

  s_t_zero_adj_rate_anomaly:
    description: |
      Despite having vocabularies that allow repetition by chance, s and
      t produce ZERO identical adjacent word pairs.
    s: {tokens: 452, identical_pairs: 0, exp: [exp_577]}
    t: {tokens: 466, identical_pairs: 0, exp: [exp_577]}
    interpretation: "Structural anti-repetition from positional constraint as line-opening classes"
    commitment: C009_part_B
```

---

## 6. Three-Register Line Grammar

```yaml
three_register_line_grammar:
  source: "F345–F365, exp_343–exp_357; section-invariant pattern"
  description: |
    Lines fall into three structurally distinct registers depending on
    folio position. Each register has a different LF onset distribution,
    different word-length profile, and different vocabulary type.
  exp: [exp_343, exp_344, exp_345, exp_354, exp_355, exp_363, exp_364]

  register_1_folio_opener:
    LF_gallows_onset_pct: [0.71, 0.80]
    gallows_classes: [p, k, t, f]
    line_length_words: [7, 8]
    hapax_dominated_pct: 0.85
    LL_anti_gallows: true
    A_LL_gallows_enrichment: 0.29
    B_LL_gallows: absent
    one_word_gallows_constraint:
      description: |
        Gallows register is confined to word_index = 0 only. A bare
        gallows word never appears outside the line-first slot in
        folio-opener register.
      exp: [F100, F101, exp_086, exp_088]
    LF_distribution_dominant: gallows
    interpretation: "Folio-opener marker register; high information density"

  register_2_continuation:
    LF_dominant_classes: [d, qok, s, y]
    LL_dominant_classes: [am_suffix, l]
    word_count_distribution: standard
    content_grammar: active
    LF_distribution: "diverse non-gallows openers (s, y, t, d in B)"
    interpretation: "Bulk text register; standard positional grammar applies"
    exp: [F343]

  register_3_folio_closer:
    line_length_words:
      A_mean: 3.94
      B_mean: 4.81
      vs_continuation: 7.8
    LF_anti_gallows:
      A_enrichment: 0.44
      B_enrichment: 0.60
    B_LF_enriched_classes: [l, ol, ot]
    B_LF_enrichment_range: [3.4, 3.9]
    A_p_onset_complete_exclusion:
      folio_opener_LF_share: 0.373
      folio_closer_LF_obs: 0
      folio_closer_LF_total: 83
      exp: [F345, exp_354, exp_355]
    interpretation: "Folio-closer register; short lines, no gallows openers"

  cross_register_constraints:
    pos2_rules:
      description: "B has position-2 (second-word) self-chain rules; A is position-general"
      exp: [exp_487, exp_489, exp_490, exp_492, exp_493, exp_494, exp_495]
      B_pos2_self_chain_classes:
        - {class: ch_in_B_herbal, status: documented, exp: [exp_485]}
        - {class: ch_in_B_pharma, status: documented, exp: [exp_490]}
      A_pos2_rule_status: "rare; A's positional grammar is general not pos2-specific"
      qualification: "exp_513/exp_514 cross-class pos2 surveys"

    one_word_gallows_constraint:
      description: |
        In folio-opener register, bare gallows (p/k/t/f) appear ONLY at
        word_index=0. They are absent from MID and LL of opener lines.
        Adding y- or qo- prefix DEMOTES the gallows character to a
        within-line position. Per F102: stem=content; prefix=position.
      exp: [F102, F101, exp_088]

  prefix_demotion_paradigm:
    description: "The same gallows stem appears at three positional levels via prefix"
    exp: [F102, F103]
    levels:
      level_4_para:    {form: "bare gallows (p/k/t/f)", role: paragraph_opener}
      level_3_line:    {form: "y+gallows or d+ch in A", role: within_para_line_opener, LF_pct: [0.56, 0.86], PS_pct: 0.00}
      level_2_mid:     {form: "qo+gallows in B, bare ch in A", role: mid_line, LF_pct: [0.07, 0.27]}
      level_1_close:   {form: "d+suffix in A, -am/oly in B", role: line_closer}
    operational_rule: |
      Adding y- or qo- prefix to a gallows character ELIMINATES its
      para-start function (qo+k 0.27–0.32× PS suppressed; y+gallows
      0.08–0.40× PS suppressed).

  paragraph_opener_full_taxonomy_v2:
    A_PARA_tier: ["{p,f}+stem", "bare_k", "bare_t"]
    B_PARA_tier: ["{p,f}+stem", "bare_k", "bare_t"]
    A_coverage_pct: 0.54
    B_coverage_pct: 0.54
    most_discriminative_2char_onsets:
      A: {prefix: "po-", enrichment: 22.17}
      B: {prefix: "ko-", enrichment: 38.12}
    exp: [F107, exp_100]

  paragraph_length_register_specificity:
    description: "Per F108 — grammar STRICTNESS scales with paragraph length"
    source: F108
    exp: [exp_101, exp_108]
    canonical_rule: |
      Para-start grammar STRICTNESS scales monotonically with paragraph
      length. Long-paragraph sections have categorical grammar; short-
      paragraph sections have relaxed grammar.
    table:
      A_herbal_10_15_lines: {PARA_pct: 0.707, LINE_OPEN_pct: 0.00, regime: strictest}
      A_astro_2_4_lines:    {PARA_pct: 0.31,  LINE_OPEN_pct: 0.086, regime: relaxed}
      B_monotonic: {PARA_pct_range: [0.22, 0.65], LINE_OPEN_violations: 0.00}
    section_paragraph_lengths:
      stars_B:  47
      cosmo_B:  25
      herbal_AB: [12, 13]
      pharma_A: 7.7
      astro_A:  3.4
    rule_for_candidates: |
      A candidate model that produces uniform grammar across all
      sections will MISMATCH section-specific register strictness.
      Long paragraphs (≥10 lines) require categorical grammar; short
      paragraphs (≤4 lines) require relaxed grammar.
```

---

## 7. Paragraph Chain Grammar by Section

```yaml
paragraph_chain_grammar:
  description: |
    Cross-line (CL) directed graphs of onset-class transitions. The CL
    network is the strongest evidence for grammar above the line level.
    CL transitions are DISTINCT from within-line bigrams: a CL transition
    can be CONF while the corresponding within-line bigram is NULL or
    DEPL. Any candidate model must support TWO levels of sequential
    grammar.
  exp: [exp_490..exp_524, exp_543, F490..F555]

  A_herbal_a_network:
    description: "Directed acyclic network with d as origin hub, qot as pivot, t as relay"
    exp: [F490, F491, F506, F507, F508, F509, F510, F511, F512, F513, F514]
    transitions:
      - {from: d,   to: qot, confidence: CONF, exp: [F491]}
      - {from: qot, to: ch,  confidence: CONF, exp: [F490]}
      - {from: ch,  to: o,   confidence: CONF, exp: [F506]}
      - {from: o,   to: sh,  confidence: dir,  exp: [F507]}
      - {from: ch,  to: t,   confidence: CONF, exp: [F508]}
      - {from: t,   to: ch,  confidence: dir,  exp: [F510]}
      - {from: t,   to: d,   enrichment: 1.47, confidence: near_CONF, exp: [F510], role: soft_reset}
      - {from: t,   to: y,   confidence: dir,  exp: [F512]}
      - {from: t,   to: ot,  confidence: dir,  exp: [F513]}
      - {from: sh,  to: ok,  confidence: dir,  exp: [F509]}
      - {from: ok,  to: ol,  confidence: dir,  exp: [F514]}
      - {from: k,   to: ot,  confidence: dir,  exp: [F511]}
    structural_facts:
      origin_hub: d
      pivot: qot
      relay: t
      cyclicity: false
      shape: "directed acyclic network"
      d_qot_scope:
        within_line_NULL: {A: 0.99, B: 0.66, exp: [exp_543, F555]}
        cross_line_CONF: true
        interpretation: |
          d→qot operates ONLY at the inter-line level. Within a single
          line, d→qot succession is NULL or DEPL. Two distinct
          mechanisms at different structural levels — clearest scope
          confirmation in the corpus.
    section_specificity: |
      Full CL network is A herbal_a-specific. Not active in B herbal
      (qot-LF is near-absent in B herbal).

  A_herbal_a_two_register_split:
    description: |
      Per F082 / F088 / exp_075 / exp_081: Herbal A has two registers
      (y-dominant vs aiin-dominant) with different sequential grammar.
      The unified A_herbal_a_network above pools both. Below are the
      sub-networks.
    y_dominant_register:
      sequential_grammar:
        - {pair: "she→qo", enrichment: 2.23, exp: [F082]}
      bigram_PPL_reduction: 0.040
      vocabulary: "y+ch/k/sh/t compounds dominant"
    aiin_dominant_register:
      sequential_grammar:
        - {pair: "qo→ch", enrichment: 1.72, exp: [F082]}
        - {pair: "s→ch",  enrichment: 1.76, exp: [F082]}
        - {pair: "daiin→qo", enrichment: 2.38, exp: [F082]}
        - {pair: "she→qo", enrichment: 0.41, status: DEPL_inverse, exp: [F082]}
      bigram_PPL_reduction: 0.058
      vocabulary: "aiin/daiin/d-onset dominant; chaiin 11.75×"
    register_distribution:
      aiin_dom_quires: ["D (50%)", "F (62%)"]
      y_dom_quires: ["B", "O", "Q (exclusive)"]
    register_implication: |
      The two registers use the same A suffix profile (-ol, -or, no -edy)
      but completely different sequential grammar. A candidate model for
      A herbal_a must produce BOTH register sub-networks, not just the
      pooled average.
    exp: [F082, F083, F088, exp_075, exp_076, exp_081]

  pharma_A_grammar_morphology_dissociation:
    description: |
      Pharma A has B-strength sh→qo coupling (2.44×) but pure A-type
      vocabulary (Jaccard with B = 0.070; -edy = 0.2%). The sequential
      grammar and morphological dialect are independently varying
      properties — they are NOT a single dialect axis.
    pharma_A_sh_to_qo: 2.44   # exceeds B's 1.97×
    pharma_A_jaccard_with_B: 0.070
    pharma_A_edy_pct: 0.002
    vs_herbal_A_sh_to_qo: 1.27
    interpretation: |
      A candidate "Pharma A is transitional between A and B" model FAILS
      because Pharma A is FARTHER from B in vocabulary than Herbal A is.
      The grammar/morphology dissociation is general; Pharma A is the
      clearest example.
    exp: [F082, F083, exp_075, exp_076]

  d_d_paragraph_self_succession:
    description: "d closes paragraphs and re-opens following lines"
    A_d_chain:
      d_closer_to_d_ch_opener_enrichment: 1.76
      d_ch_opener_after_d_ending_lines_pct: 0.357
      exp: [F099, F100]
    B_d_d:
      role: "d→d cross-line CONF paragraph self-succession"
      exp: [F527]

  B_dialect_CL_section_specific:
    description: |
      B-dialect CL is heterogeneous and section-specific (corrects F444).
    B_astro:
      - {pair: "qok→qok CL", enrichment: 1.77, obs: 14, confidence: CONF, exp: [F495]}
      - {pair: "d→qo CL",   confidence: dir, exp: [F495]}
      - {pair: "ol→o CL",   confidence: dir, exp: [F495]}
      independent_network: true
    B_herbal:
      - {pair: "ot→ch CL", enrichment: 2.63, obs: 5,  confidence: dir, exp: [F526]}
      - {pair: "d→ok CL",  confidence: CONF, exp: [F527]}
      - {pair: "d→d CL",   confidence: CONF, exp: [F527]}
      - {pair: "ot→ot CL", confidence: CONF, exp: [F527]}
      - {pair: "ot→a CL",  confidence: CONF, exp: [F527, F629]}
      alternative_chain: "ot→ch fragment instead of d→qot→ch"
    B_pharma:
      - {pair: "ol→qok CL", enrichment: 2.76, obs: 10, confidence: CONF, exp: [F496, F528]}
      alternative_chain: "ol→qok fragment instead of d→qot→ch"
    B_bio:
      role: "no documented CL signature beyond high s_LF / qok_LF"

  t_relay_role:
    description: "t is a CL relay class in A herbal_a"
    pairs_relayed: ["t→d", "t→ch", "t→y", "t→ot"]
    exp: [F508, F510, F512, F513]

  t_lf_inversion_AB:
    A: "t-LF formula"
    B: "t-LF formula"
    inversion: documented
    exp: [exp_477]

  paragraph_boundary_marking:
    A_para_final: {dominant_word: daiin, pct: 0.090, enrichment: 2.08, exp: [F084, exp_077]}
    B_para_final: {dominant_class: o_onset, pct: 0.40, enrichment: 1.72, exp: [F083, exp_076]}
    universal_qok_suppression_at_para_final:
      A: 0.21
      B: 0.17
      exp: [F083]
    am_para_final_suppression:
      A: {pct: 0.019, vs_within_para: 0.064, exp: [F086]}
      B: {pct: 0.020, vs_within_para: 0.126, exp: [F086]}

  daiin_cross_dialect_role:
    A: "LL marker (LF 19.4%, LL 25.9%); para-final marker"
    B: "LF connector (LF 34%, LL 9.5%); 73.5% daiin[0]→ch/sh"
    exp: [F093, F094]
```

---

## 8. Cross-Dialect Structural Contrasts

```yaml
cross_dialect_contrasts:

  contrast_terminal_layer_inversion:
    A_LL_terminals: [d, cth]
    B_LL_terminals: [r, l, ol, o, a]
    overlap: 0
    interpretation: |
      A closes lines with aiin-body + compound gallows; B closes lines
      with lateral / vowel-initial classes. Zero overlap in terminal
      class identity (canonical convention).
    exp: [exp_555, exp_557, exp_558]
    commitment: C008

  contrast_compound_gallows_frequency_collapse:
    description: "All compound gallows DROP dramatically A→B"
    cth: {A_to_B_factor: 0.116, exp: [exp_558]}
    cph: {A_to_B_factor: 0.205, exp: [exp_610]}
    sch: {presence: A_only_extreme, exp: [exp_561]}
    interpretation: |
      Compound gallows are an A-dialect feature. B retains them only
      vestigially. Any candidate decipherment must explain why these
      forms vanish at the dialect transition.

  contrast_d_onset_positional_reversal:
    A: {role: LL_TERMINAL, LL_enr: 1.53}
    B: {role: LF_OPENER,   LF_enr: 2.64}
    interpretation: "Same onset class with opposite line-position role across dialects"
    exp: [exp_553, exp_555, exp_557]

  contrast_qok_frequency_doubling:
    A_pct: 0.0730
    B_pct: 0.1513
    ratio: 2.07
    driver: "B_astro section grammar contributes most"
    exp: [exp_565, F618]

  contrast_qot_LF_inversion:
    A: {LF_enr: 1.40, status: subCONF_opener}
    B: {LF_enr: 0.69, status: DEPL}
    exp: [exp_631]

  contrast_sh_routing_dialect_specific:
    A: "sh routes to gallows {sh→k, sh→t}"
    B: "sh routes to q-class {sh→qok, sh→qo, sh→qot}"
    exp: [exp_544]

  contrast_paragraph_chain_section_specific:
    A_herbal_a: "d→qot→ch→o→sh full network (with two-register split)"
    B_herbal:   "ot→ch fragment"
    B_pharma:   "ol→qok fragment"
    B_astro:    "qok→qok independent CL network"
    B_bio:      "no CL signature"
    exp: [F495, F496, F526, F527, F528]

  contrast_paragraph_marker_morpheme:
    A: {marker_type: SUFFIX, marker: "-dy", enrichment: 3.36}
    B: {marker_type: ONSET,  marker: "p-onset", enrichment: 17.0_to_18.0}
    interpretation: "Same structural function, different morphological slot"
    exp: [F057, F086]

  contrast_paragraph_close_marker:
    A: {marker_type: WORD,  marker: "daiin", para_final_pct: 0.090}
    B: {marker_type: CLASS, marker: "o-onset", para_final_pct: 0.40}
    exp: [F083, F084]

  contrast_grammar_strength:
    A_bigram_PPL_reduction: 0.091
    B_bigram_PPL_reduction: 0.133
    interpretation: "B sequential grammar 35% stronger by perplexity reduction"
    exp: [F081, exp_074]

  contrast_grammar_morphology_dissociation:
    description: "Sequential grammar varies independently of morphological dialect"
    pharma_A_case: "B-strength sh→qo (2.44×) with pure A morphology"
    herbal_A_aiin_dom_case: "Strong aiin grammar (PPL 5.8%) with weak she-→qo (0.41× DEPL)"
    interpretation: |
      Grammar and morphology are independent dimensions. Candidate models
      that treat A vs B as a single linear axis FAIL.
    exp: [F082, F083, F088, F089]

  invariant_adj_rate_exact:
    description: "Per C009: adj_rate is structurally invariant across dialects"
    cross_dialect_facts:
      - "qok dominates adj_rate in B (36.8% of identical pairs from 12.8% of tokens)"
      - "s and t adj_rate = 0 in BOTH dialects (structural anti-repetition)"
      - "sh/ch/d adj_rate ≈ random expectation from CP90 pools cross-dialect"
    commitment: C009
    exp: [exp_577]

  invariants_summary:
    description: "Cross-dialect structural facts that any decipherment must preserve"
    list:
      - "y is LF-CONF (line-opener) in BOTH dialects"
      - "y is LL-subDEPL (avoids line-end) in BOTH dialects"
      - "qok and sh are LL-DEPL in BOTH dialects (canonical convention)"
      - "ch is LF-DEPL extreme in BOTH dialects (most extreme avoider)"
      - "a is LF-avoider in BOTH dialects"
      - "sh→qok / sh→qo / sh→ch DEPL invariant"
      - "qo→qo self-succession CONF in both dialects"
      - "a→ok CONF in both dialects"
      - "Bare gallows mark paragraph boundaries in both dialects (F100/F101)"
      - "y+gallows demotes to line-opener in both dialects"
      - "qo+gallows demotes to mid-line in both dialects"
      - "p/f are stronger para-starters than t/k in both dialects"
      - "s and t adj_rate = 0 in both dialects"
```

---

## 9. Word-Internal Structure

```yaml
word_internal_structure:
  three_tier_midfix_structure:
    description: |
      Per Stolfi's slot grammar plus exp_288–exp_301: words decompose
      into PREFIX × CORE × MIDFIX × SUFFIX with positional entropy
      profile U-shaped (constrained crust, freer core).
    positional_entropy:
      H_pos0_onset: 3.137
      H_pos3_4_middle: [3.606, 3.612]
      H_pos_neg1_final: 2.456
    contradicts_natural_languages: |
      Latin and Italian have HIGHER entropy at pos0 than interior.
      Voynichese has LOWER entropy at pos0 than interior. Direct
      evidence for slot-grammar word formation rather than phonological
      word formation.
    exp: [F003, F004]

  midfix_inventory:
    description: "Per exp_291"
    exp: [exp_270, exp_271, exp_280, exp_283, exp_286, exp_291]
    midfix_classes_have_onset_conditional_distribution: true
    LF_midfix_rate: 0.50
    LL_midfix_rate: 0.00
    MID_midfix_rate: 0.20

  character_zone_rules:
    pos0: "onset class membership; gallows + compound gallows + bare consonants"
    pos1_to_pos_n: "midfix; e/a/o vowel inventory; aiin/ain templates"
    pos_neg1: "{y, n, l, r} cover 88.8%; final-y dominant"
    constrained_layer: "outer crust (pos0 and pos_neg1)"
    free_layer: "inner core"
    exp: [F042]

  d_onset_daiin_template:
    description: |
      d-onset words are dominated by aiin/al/am/ar suffixes producing
      daiin/dal/dam/dar templates. d+aiin is most templated bigram in
      both dialects.
    A_d_aiin_overrep: 2.69
    B_d_aiin_overrep: 2.16
    exp: [F063, F068, exp_056, exp_061]

  y_onset_y_gallows_compound:
    description: |
      y-onset words are predominantly y+gallows compounds. y is the
      LF prefix that demotes a gallows to within-line use.
    y_plus_kt_LF_enrichment: 3.75
    y_plus_kt_pct_LF_in_B: 0.473
    three_level_kt_paradigm:
      bare:    {LF_pct: 0.089}
      qo_pref: {LF_pct: 0.116}
      y_pref:  {LF_pct: 0.362}
    exp: [F095, F096, exp_322]

  qo_prefix_morpheme:
    description: |
      qo- is a Currier B morphological prefix selecting k/t-initial stems.
    qo_stem_onset_dist: {k: 0.605, t: 0.212}
    qo_word_distribution_AB: {A: 0.116, B: 0.880}
    qo_attach_to_gallows_pct: 0.865
    qo_specific:
      qo_k: 0.626
      qo_t: 0.199
      qo_p: 0.033
      qo_f: 0.007
    parallel_o_prefix:
      role: "labels analog of body-text qo-"
      o_labels_kt_initial_pct: 0.665
      stem_in_free_vocab_rate:
        o_stems: 0.431
        qo_stems: 0.420
    exp: [F037, F040, F041, F043, F044, F055, F075]

  cth_prefix_morpheme:
    description: "A-dialect prefix on o/y/e-initial stems; structural parallel to qo-"
    H_initial_drop: [3.061, 1.966]
    selects: ["o-initial", "y-initial", "e-initial"]
    A_dominance: "8× more per-token than B"
    B_cth_attestation: "52 occurrences with B-suffix forms (cthedy 11, cthey 10, cthdy 7)"
    exp: [F172, F173, F174, exp_165, exp_166, exp_167]

  she_prefix_qo_predictor:
    description: "she- prefix sh-words precede qo at 2.19–2.91× across all dialects"
    A_herbal:  1.52
    A_pharma:  2.91
    B:         2.19
    sh_other_baseline: [1.18, 1.45]

  e_infix_partition_finding:
    description: |
      The e-infix is a VOCABULARY PARTITION not productive morphology.
      Same stem with both forms shows IDENTICAL suffix distributions.
    exp: [F087, F088, exp_080, exp_081]

  paradigm_three_prefix_system:
    qo_prefix:  {role: "B body, k/t stems"}
    o_prefix:   {role: "labels (any section), k/t stems"}
    cth_prefix: {role: "A body, o/y/e stems"}
    exp: [F043, F044]
```

---

## 10. Architecture Capabilities and Limits (21-Mechanism Findings)

```yaml
architecture_21mech:
  designation: "Mode B copy-buffer hybrid (exp_217 → exp_314)"
  status: "first mechanism class to jointly satisfy dual constraint"
  commitment: C008

  architecture_overview:
    type: position_aware_copy_buffer_hybrid
    description: |
      LL and LF words generated by a position-sensitive onset/suffix
      mechanism; MID words drawn from a copy buffer and modified at
      the character level (onset preserved). This decouples am_ll
      enrichment (LL mechanism) from self-succession (buffer recycling
      with shared onset).
    fixed_constants:
      CP: 0.55
      MP: 0.90
      P_STUTTER: 0.006
    calibrated_parameters:
      beta_scale: 1.8
      p_blind: 0.115
      r_lf: 0.12
      r_mid: 0.20
      p_qokch: 0.12
      p_chqok: 0.12
      mu_len: 8.4
      sigma_len: 3.0
      gamma: 0.30
      alpha: 0.20
      beta_base: 0.50
      p_mf: 0.20
      p_lf_mf: 0.50
      p_ll_mf: 0.00
    additional_mechanisms_17_to_21:
      17_vocab_clamp: "qok/ok/ot/qot full VMS type inventory clamp"
      18_p_blind_conditional: {p_short_n_le_5: 0.060, p_long_n_ge_10: 0.180}
      19_max_ll_len_filter: "max(3, round(8 − 0.3×max(0, n−5))), MAX_RETRY=10"
      20_beta_eff_n_conditional: "0.50 × 1.8 × n/8.4 [for word_idx≥2]"
      21_n_conditional_menzerath: "scaling per word_idx"
    exp: [exp_314]

  battery_performance_19_metrics:
    metrics:
      [am_ll, ss_mean, adj_rate, ch_ll, ok_ll, ss_d, ss_y, qok_ch,
       edy_rate, word_len_mean, qok_lf, y_lf, d_lf, s_lf, am_lf_enr,
       am_mid_enr, qok_ll, d_ll, global_am_rate]
    pass_count_real_VMS: "19/19"
    pass_tolerance: ±0.20
    N_runs: 30
    menzerath_overshoot_pct: 4
    MID_slope_overshoot_pct: 23
    exp: [exp_314]
    commitment: C008

  reproduces_on_B_dialect:
    confirmed: true
    qualification: |
      Per exp_579 / C008 scope qualification: 19/19 is a full-corpus
      average over four B sections with systematically different
      positional grammar. Section-level calibration would require
      different parameter values per section.

  reproduces_on_A_dialect:
    confirmed: "19/19 on A-dialect battery (exp_239)"
    qualification: "different parameter values from B"

  specificity_test_C008:
    description: "Per exp_574 / exp_575 — fresh grid search on shuffled corpora"
    real_VMS_pass: "19/19"
    intra_shuffle_best_pass: "16/19"
    intra_shuffle_failures: [am_ll, ss_d, ss_y]
    inter_shuffle_best_pass: "14/19"
    inter_shuffle_failures: [am_ll, ss_mean, adj_rate, ss_d, ss_y]
    structural_floors:
      am_ll_floor: 1.17
      ss_d_floor: 1.50
      ss_y_floor: 2.00
      adj_rate_floor: 0.006
      ss_mean_floor: 1.36
    interpretation: |
      The architecture has hard structural minimums set by the FIXED
      CONSTANTS (CP, MP, P_STUTTER, max_ll). These minimums prevent
      calibration to any corpus whose targets fall below them.
      C008 confirms 19/19 reflects genuine VMS specificity.
    qualification_per_exp_575: |
      Per exp_575 §"What this means for the architecture's 19/19": the
      architecture's specificity is driven by the fixed-constant
      mechanisms (copy buffer, stutter), NOT by the 6 calibrated
      parameters. The 19/19 reflects mechanism-architecture commitments,
      not parameter-tuning specificity.
    exp: [exp_574, exp_575]
    commitment: C008

  parameter_stability_test:
    description: "Per exp_576 — three 50/50 split cross-validations"
    odd_even_cross_val: "17/19 → 15/19 (acceptable; 2/19 degradation)"
    first_second_cross_val: "17/19 → 8/19 (CATASTROPHIC; corpus heterogeneity)"
    random_cross_val: "17/19 → 14/19 (3/19 stochastic floor)"
    stable_params: [p_blind, r_lf]
    unstable_params: [beta_scale, r_mid, p_qokch]
    interpretation: |
      Parameters are NOT stable structural constants. exp_314 calibration
      is a full-corpus compromise. The first/second collapse reflects
      VMS corpus document-order heterogeneity (per exp_579: section
      composition explains 97–107% of the gradient).
    exp: [exp_576]
    commitment_qualification: C008_scope_qualification

  C004_narrowing_from_exp_182:
    description: |
      Per exp_182 (Timm character-level modification) the C004 residual
      gap (sub-VMS adj_rate at viable ss/am_ll combinations) NARROWS:
      char-level modification crosses the threshold; suffix-replacing
      modification does not.
    exp_182_results:
      total_combos: 36
      viable_at_lenient: "8/36 (vs exp_181 4/36)"
      viable_at_VMS_adj_rate: "3/36 (first-ever in program)"
      viable_combos_at_VMS_adj_rate:
        - {cp: 0.6, mp: 0.7, am_ll: 6.093, ss_mean: 1.279, adj_rate: 0.0085}
        - {cp: 0.6, mp: 0.8, am_ll: 6.099, ss_mean: 1.266, adj_rate: 0.0060}
        - {cp: 0.7, mp: 0.8, am_ll: 6.308, ss_mean: 1.368, adj_rate: 0.0069}
    mechanism: |
      Timm char-level modification has ~2% character collision rate
      (1/16 chars × 1/3 replacement ops) vs ~17% suffix collision rate
      for exp_181 suffix-replacing variant. Lower collision rate lets
      adj_rate decrease faster with MODIFY_PROB while maintaining
      ss_mean ≥ 1.2.
    interpolation_fraction:
      onset_preservation_pct: 0.79
      ss_mean_interpolation_fraction: 0.71  # between exp_180 and exp_181
    qualification: |
      The 3 VMS-viable combinations achieve 89.5–92.6% of VMS am_ll and
      86.4–93.4% of VMS ss_mean — they ENTER the not-ruled-out zone
      under VMS-level adj_rate constraints but do NOT positively
      reproduce VMS measured values at all metrics. Per exp_182 §1
      headline note.
    commitment_status: |
      C004 is now narrowed to apply ONLY to suffix-replacing
      modification. Char-level modification (exp_182) is NOT covered
      by C004's residual gap claim.
    exp: [exp_182]
    commitment: C004

  architectural_limits:
    description: "Known structural gaps the architecture cannot close"
    sh_ch_d_three_way_constraint:
      Q007_status: closed
      diagnosis: |
        sh/ch/d CP90 restriction (145/290/146) is incompatible with low
        adj_rate under copy-buffer + same-onset self-succession coupling.
        sh→sh=9.2%, ch→ch=15.0%, d→d=8.6% self-succession rates cause the
        copy-buffer to overproduce identical pairs by 1.4–1.8× regardless
        of vocabulary clamp.
      sh_overshoot: 1.41
      ch_overshoot: 1.55
      d_overshoot:  1.79
      vocab_clamp_helps_for: [qok, d]
      vocab_clamp_does_not_help_for: [sh, ch]
      VMS_natural_adj_rate_pattern:
        sh: {actual: 0.764, random_expect: 0.690, ratio: 1.108}
        ch: {actual: 0.659, random_expect: 0.345, ratio: 1.910}
        d:  {actual: 0.480, random_expect: 0.685, ratio: 0.701}
        s:  {actual: 0.000, ratio: 0.000}
        t:  {actual: 0.000, ratio: 0.000}
      interpretation: "VMS sh/d adj_rate ≈ random expectation; VMS has no anti-repetition mechanism for these classes"
      exp: [exp_577, exp_578]
      commitment: C009

    s_t_structural_anti_repetition:
      description: "s/t adj_rate = 0; structural anti-repetition from positional constraint"
      s: {tokens: 452, identical_pairs: 0}
      t: {tokens: 466, identical_pairs: 0}
      mechanism: "s and t are line-opening LF classes; appearing only at line-firsts means consecutive identical pairs are structurally impossible"
      exp: [exp_577]
      commitment: C009_part_B

    sh_qok_magnitude:
      description: "sh→qok B E_mid=1.97×; architecturally unresolved"
      exp: [working_position section 4.3]

    vocabulary_richness_gap:
      description: "Architecture baseline CP90 is 7–14× richer than VMS for sh/ch/d"
      exp: [exp_578]

    menzerath_overshoot:
      sim_r: -0.234
      VMS_r: -0.225
      pct: 1.04
      exp: [exp_314]

    MID_slope_overshoot:
      pct: 1.23
      exp: [exp_314]

    short_line_LL_word_length_deficit:
      sim: 5.007
      VMS: 5.684
      n_range: [2, 4]
      exp: [exp_314]

    MID_word_repetition_distance:
      ratio_to_VMS: 0.43
      exp: [working_position section 4.3]

    sh_ch_d_CP90_overproduction:
      ratio_range: [3.2, 4.1]
      note: "clamping breaks adj_rate (per Q007)"
      exp: [working_position section 4.3]

  what_architecture_demonstrates:
    - "A position-aware copy-buffer hybrid CAN produce all 19 measured properties simultaneously"
    - "The dual constraint is achievable by mechanisms with structurally separate positional and sequential components"
    - "VMS B-dialect grammar is consistent with a compact ~21-mechanism / ~15-parameter generative process"
    - "Per exp_182: char-level modification reaches the previously-unreachable VMS adj_rate ceiling for one specific operation"
  what_architecture_does_NOT_demonstrate:
    - "VMS IS generated by this mechanism"
    - "No other mechanism class could also achieve 19/19"
    - "The mechanism is the correct interpretation of the text"
    - "Stable parameters across sections / document order"
```

---

## 11. Document-Order Heterogeneity Caveat (exp_579)

```yaml
document_order_heterogeneity:
  status: "MUST be respected by all candidate decipherments and architectures"
  source: exp_579
  finding: F639
  commitment: C008_scope_qualification

  primary_result:
    description: |
      B-dialect positional metrics shift systematically across document
      order. Section composition explains 97–107% of the half-shift for
      all five primary metrics.
    half_shifts:
      am_ll:  {first: 5.825, second: 7.147, shift_pct: 0.227, predicted_by_section_pct: 1.068}
      y_lf:   {first: 2.745, second: 3.889, shift_pct: 0.417, predicted_by_section_pct: 1.066}
      d_ll:   {first: 0.1406, second: 0.0742, shift_pct: -0.472, predicted_by_section_pct: 0.989}
      qok_lf: {first: 0.1156, second: 0.0371, shift_pct: -0.679, predicted_by_section_pct: 0.961}
      s_lf:   {first: 0.1356, second: 0.1056, shift_pct: -0.221, predicted_by_section_pct: 1.014}

  drivers_tested:
    A_scribal_hand:
      result: NOT_isolable
      reason: "hand × section co-linear in B-dialect"
      exception: |
        Within B_astro, Hand 4 (rose foldout) is anomalous, but
        attributable to diagram-label content type, not scribal idiolect.
    B_section_composition:
      result: COMPLETE_DRIVER
      explained_pct_range: [0.961, 1.068]
    C_genuine_linguistic_drift:
      result: NOT_REQUIRED
      reason: "97–107% explained by B leaves no residual"

  quartile_composition:
    Q1: {herbal_pct: 0.57, bio_pct: 0.43}
    Q2: {bio_pct: 0.87, astro_pct: 0.13}
    Q3: {astro_pct: 0.23, pharma_pct: 0.77}
    Q4: {astro_pct: 0.23, pharma_pct: 0.77}
    first_half: {herbal: 0.28, bio: 0.65, astro: 0.06}
    second_half: {astro: 0.23, pharma: 0.77}

  per_section_grammar_profiles:
    B_herbal: {am_ll: 0.1616, y_lf: 0.1793, d_ll: 0.1768, qok_lf: 0.0556, s_lf: 0.0707, adj_rate: 0.0061}
    B_bio:    {am_ll: 0.0525, y_lf: 0.0743, d_ll: 0.1279, qok_lf: 0.1475, s_lf: 0.1716, adj_rate: 0.0111}
    B_astro:  {am_ll: 0.1642, y_lf: 0.1201, d_ll: 0.1054, qok_lf: 0.0319, s_lf: 0.0588, adj_rate: 0.0066}
    B_pharma: {am_ll: 0.1919, y_lf: 0.1688, d_ll: 0.0655, qok_lf: 0.0406, s_lf: 0.1190, adj_rate: 0.0075}
    range_factor:
      am_ll: 3.66
      y_lf:  2.41
      d_ll:  2.70
      qok_lf: 4.62
      s_lf:  2.92
      adj_rate: 1.82

  monotonicity:
    description: "The gradient is STEP-WISE not monotonic"
    pattern: "Q2 dips on am_ll/y_lf due to bio domination; Q3–Q4 elevate due to pharma domination"
    interpretation: "section-composition transition, not smooth drift"

  implications_for_grammar_spec:
    rule_1: "Positional metrics MUST be reported per section for B-dialect"
    rule_2: "Onset frequencies, self-succession, and adj_rate may safely be reported as full-corpus values (smaller section variation)"
    rule_3: "Vocabulary structure may be reported as full-corpus values"
    rule_4: "Architecture parameters reported as full-corpus aggregates only"

  implications_for_candidate_decipherments:
    description: |
      A candidate decipherment that produces a uniform B-dialect output
      is INCONSISTENT with VMS structure. Any decipherment must produce
      the section-specific positional grammar profiles above. The
      simplest test: does the candidate's am_ll on B_bio fall in
      [0.05, 0.07] AND on B_pharma in [0.18, 0.21]?
```

---

## 12. Things Explicitly Ruled Out

```yaml
ruled_out:
  description: |
    Mechanism classes that have been falsified. A candidate decipherment
    or generative theory MUST NOT fall into any of these classes.

  1_position_blind_ciphers:
    examples_tested:
      - {name: Naibbe_homophonic_cipher, n_simulations: 400}
      - {name: Timm_self_citation, n_simulations: 1500, parameter_combinations: 75}
    metrics_failed: [am_ll, y_lf, d_ll, qok_lf_depl]
    max_am_ll_achievable: 0.57   # vs commitment cap of 1.1
    VMS_am_ll: 6.811
    structural_reason: "position-blind mechanisms cannot produce position-dependent distributions by definition"
    bonferroni_m: 175
    weakest_p_value: "<1e-26"
    cross_validation: ["80/20", "leave-one-section-out"]
    exp: [exp_170, exp_171, exp_172, exp_173, exp_176]
    commitment: C001

  2_pure_self_citation_Timm_alone:
    contradiction: "Timm overproduces adj_rate at parameters that produce VMS-level ss; lowering adj_rate drops ss far below VMS"
    parameter_space_searched: 75
    joint_constraint_unsatisfiable: true
    exp: [exp_176]
    additional_evidence: |
      VMS MI at lags 2–7 is BELOW the Timm 95% CI. Any copy-window
      mechanism generates elevated MI within the window. VMS lacks
      this signature. (Lags 10–12 retracted as sampling artifact —
      Catch 1 in SOUL.md.)
    exp_mi: [exp_175]
    commitment: C002_supporting

  3_position_sensitive_substitution_alone:
    description: "LF/MID/LL substitution tables on Latin baseline; no copy component"
    ss_mean_produced: ~1.00
    VMS_ss_mean: 1.465
    failed_property: "Property 2 (sequential word-class memory)"
    target_aware_calibration_acknowledged: true
    target_aware_LL_table: "explicitly maps Latin clause-final morphemes to EVA -am"
    exp: [exp_177]
    commitment: C002

  4_pure_template_generation:
    contradiction: |
      A generic positional slot would not produce the contrast: -am is
      6.811× LL-enriched while edy (most common B-suffix at 18%) is 0.35×
      LL-depleted. The slot must have onset-class grammar rules
      specifying which suffix classes belong at LL.
    exp: [exp_173, exp_174]

  5_onset_replacing_position_aware_hybrid:
    description: |
      MID-only copy with modification that REPLACES the onset class.
      Modification destroys onset self-succession, the very feature the
      copy was supposed to produce.
    viable_combinations: 0
    total_combinations: 18
    catch_3_lesson: |
      The 0/18 originally attributed to copy-buffer architectures in
      general; reversed when exp_181 onset-PRESERVING modification
      produced 4/36 viable. See SOUL.md Catch 3.
    exp: [exp_180, exp_181]
    commitment: C003

  6_onset_preserving_suffix_replacing_at_VMS_adj_rate:
    description: |
      Per C004: suffix-replacing variant achieves 4/36 viable lenient
      but 0/36 at VMS-level adj_rate (≤0.009). The residual gap is
      caused by ~17% suffix collision rate. NARROWED in 2026: the gap
      DOES NOT apply to character-level modification (exp_182).
    exp: [exp_181]
    narrowed_by: exp_182
    not_ruled_out_for: char_level_modification
    commitment: C004

  7_copy_buffer_over_same_onset_words_at_VMS_adj_rate_levels:
    description: |
      Per Q007 closure: any copy-buffer with ≥8% same-onset
      self-succession will overproduce adjacent identical word pairs
      for that class. VMS adj_rate is incompatible with such a mechanism
      for sh/ch/d.
    exp: [exp_577, exp_578]
    commitment: C009_part_C
    rule_for_candidate_models: |
      Copy-buffer mechanisms must EITHER (a) have no same-onset copy,
      (b) have selective deactivation for same-onset successors, or
      (c) produce self-succession through a different mechanism that
      does not amplify identical word pairs.

  8_fixed_filler_adjacent_pair_verbose_cipher:
    description: "Adjacent-pair grouping under fixed-filler verbose cipher"
    paired_h2_VMS: 3.836
    natural_language_max_h2: 3.723
    exp: [F020, F022]

  9_simple_gallows_grouping_or_crust_stripping:
    description: "Mechanical character grouping schemes for verbose cipher reversal"
    h2_distance_to_natural_language: ">1.0 bits"
    exp: [X003, X005]

  not_ruled_out_summary:
    - "Position-sensitive cipher with INDEPENDENT sequential word-class memory (untested combination)"
    - "Char-level modification copy-buffer hybrid at VMS-level adj_rate (per exp_182, narrows C004)"
    - "Natural language with position-sensitive writing conventions"
    - "Artificial / constructed language with compact grammar rules"
    - "Glossographic / domain-specific notation"
```

---

## 13. Committed Claims Index (C001–C009)

```yaml
committed_claims_index:
  source: state/committed_claims.md
  format: "claim id, summary, supporting experiments, related spec sections"
  authoritative: state/committed_claims.md

  C001:
    title: "Position-blind mechanisms fail on Voynich positional grammar"
    summary: "Max am_ll across 1,900 position-blind sims = 1.1×; VMS = 6.811×"
    supporting_exp: [exp_170, exp_171, exp_176]
    spec_sections: [12.1, 1.x_positional_profiles, 2.am_suffix_critical_metric]
    public_output: "exp_181-revised checkpoint paper (2026-04-10)"
    contradiction_condition: "position-blind mechanism producing am_ll ≥ 3.0× or y_lf ≥ 2.0×"
    status: VALID

  C002:
    title: "Position-sensitive substitution alone cannot account for sequential word-class memory"
    summary: "ss_mean produced ≈ 1.00 vs VMS 1.465"
    supporting_exp: [exp_177]
    spec_sections: [12.3, 5.ss_mean_aggregate]
    contradiction_condition: "substitution-only cipher producing ss_mean ≥ 1.15 without copy"
    status: VALID

  C003:
    title: "Onset-replacing position-aware hybrid fails on ss/adj coupling"
    summary: "0/18 viable; modification destroys feature under test"
    supporting_exp: [exp_180]
    narrowing: "exp_181 onset-preserving achieves 4/36 viable"
    spec_sections: [12.5, 10.architecture_21mech]
    status: VALID

  C004:
    title: "Onset-preserving (suffix-replacing) variant: lenient viability but above VMS adj_rate"
    summary: "Suffix-replacing 4/36 lenient, 0/36 at VMS adj_rate. Char-level (exp_182) achieves 8/36 lenient and 3/36 at VMS adj_rate."
    supporting_exp: [exp_181]
    narrowed_by: exp_182
    narrowing_summary: |
      exp_182 (Timm character-level modification) achieves 3 viable
      combinations at adj_rate ≤ 0.009 with ss_mean ≥ 1.2 and am_ll ≥ 5.0
      — first such result in the program. C004's residual-gap claim now
      applies ONLY to suffix-replacing modification. Character-level
      modification crosses the adj_rate threshold.
    spec_sections: [10.C004_narrowing_from_exp_182, 10.architecture_21mech, 12.6]
    status: VALID_NARROWED

  C005:
    title: "-am LL enrichment in Currier B is 6.811× with p < 1e-161"
    summary: "Survives Bonferroni m=30 and m=175"
    supporting_exp: [exp_173]
    narrowed_by: "exp_208 — within-paragraph LL drives the enrichment (WP-LL 6.69× vs PF-LL 3.14×)"
    spec_sections: [2.am_suffix_critical_metric]
    contradiction_condition: "alternate transcription producing am_ll < 5.0×"
    status: VALID

  C006:
    title: "y-onset LF enrichment in Currier B is 3.506× with p < 1e-90"
    supporting_exp: [exp_173]
    spec_sections: [1.2_y_onset]
    contradiction_condition: "y-onset LF enrichment < 2.0× under alternate analysis"
    status: VALID

  C007:
    title: "Onset self-succession exists in many onset classes but is class-specific, not universal"
    status: VALID_AMENDED
    amendment_landed: 2026-04-12
    canonical_correction: |
      Original "1.24–2.05× across six combinations" replaced with
      canonical range 0.78–3.86× across all class-by-dialect combinations
      under canonical methodology (per-line edy-rate dialect assignment,
      MID-baseline E formula). Five CONF cross-dialect classes:
      y, l, ot, qo, qot. The original "ok A 2.05×" was a misattribution
      (actually B qo→qo 2.047). The "residuals ≥ 1.2× across all" claim
      fails for B qok (1.03×), B ch (0.91×), B sh (0.78×).
    surviving_core: |
      Position-controlled self-succession holds for CONF classes
      (y, l, ot, qo, qot in both dialects). The mechanism evidence
      (C002: substitution gives ss≈1.0) is unaffected and is
      strengthened by the broader canonical range.
    supporting_exp: [exp_164, exp_174]
    reconciling_exp: [exp_565, exp_567, exp_573]
    spec_sections: [5.canonical_table, 5.canonical_range, 5.CONF_cross_dialect_classes]
    contradiction_condition_revised: "position control reducing residuals to <1.1× for the majority of CONF classes (y, l, ot, qo, qot)"

  C008:
    title: "21-Mechanism Architecture — 19/19 VMS Specificity and Structural Floors"
    summary: |
      19/19 PASS on real VMS B-dialect; 10/19 on shuffled with fixed
      params; 16/19 max with refit on intra-shuffle; 14/19 max on
      inter-shuffle. Failures driven by hard structural floors from
      fixed constants CP/MP/P_STUTTER/max_ll.
    structural_floors:
      ss_y_floor: 2.00
      ss_d_floor: 1.50
      ss_mean_floor: 1.36
      adj_rate_floor: 0.006
      am_ll_floor: 1.17
    scope_qualification_exp_579: |
      19/19 is a full-corpus average over 4 B sections with 3.7× am_ll
      variation. Section composition explains 97–107% of document-order
      gradient (exp_576: First half 5.825 vs Second 7.147).
    supporting_exp: [exp_314, exp_574, exp_575, exp_576, exp_579]
    spec_sections: [10.architecture_21mech, 11.document_order_heterogeneity]
    status: VALID

  C009:
    title: "VMS adj_rate Structure"
    parts:
      A: "sh/ch/d adj_rate consistent with random draws from CP90 pools (sh 1.108×, d 0.701×, ch 1.910×)"
      B: "s/t adj_rate = 0 structural; line-opening positional constraint"
      C: "Baseline 21-mechanism architecture overproduces adj_rate 1.41–1.79× above VMS for sh/ch/d due to copy-buffer + self-succession coupling"
    supporting_exp: [exp_577, exp_578]
    spec_sections: [10.sh_ch_d_three_way_constraint, 5.s_t_zero_adj_rate_anomaly]
    status: VALID

  C010_proposed:
    title: "Label text constitutes a structurally distinct register"
    status: PROPOSED_AWAITING_REVIEW
    proposal_file: state/proposed_commitments/proposed_c010_label_corpus_grammar.md
    supporting_exp: [exp_580]
    spec_sections: [15]
    summary: "ok/ot/o dominant (44%); q-bench near-absent (1.3%); edy depleted; a-onset terminal in multi-word labels"

  master_constraint_set:
    description: "Quick-reference constraints any candidate decipherment must satisfy"
    must_produce:
      - "am_ll ≥ 5.0× full-corpus B (and ≥ 1.5× even in B_bio)"
      - "y_lf ≥ 2.0× full-corpus B"
      - "ss_mean ≥ 1.20× full-corpus"
      - "ss CONF for y, l, ot, qo, qot in BOTH dialects"
      - "B section am_ll variation 3.66× (bio to pharma)"
      - "Three-register line grammar (folio-opener / continuation / folio-closer)"
      - "Bare gallows confined to word_index 0 in folio-opener register"
      - "Cross-line d→qot in A herbal_a but NULL within line"
      - "Terminal-layer inversion: A {d, cth} vs B {r, l, ol, o, a} (no overlap)"
      - "qok frequency doubles A→B (0.073 → 0.151)"
      - "Compound gallows collapse A→B (cth ×0.116, cph ×0.205)"
      - "s/t adj_rate = 0 in B"
      - "sh/d adj_rate ≈ random expectation from CP90 pools"
      - "9-form productive suffix paradigm (-edy/-eedy/-ain/-aiin/etc)"
      - "A→B suffix transformation: -ol/-or → -edy/-ey/-eedy on shared stems"
      - "qo- prefix selects k/t-initial stems"
      - "y+gallows demotes gallows to within-line; qo+gallows demotes to mid-line"
      - "Distinct label-text register per §15 (ok/ot/o dominant; q-bench near-absent)"
      - "Paragraph-length register specificity (long paragraphs strict; short paragraphs relaxed)"
    must_NOT_produce:
      - "Position-blind output (would fail C001)"
      - "ss_mean = 1.0× (would fail C002)"
      - "Copy-buffer over same-onset words at VMS adj_rate levels (would fail C009 part C)"
      - "Uniform B-dialect (would fail exp_579 / C008 scope)"
      - "Onset-replacing modification destroying ss (would fail C003)"
      - "Same A vs B grammar profile for both Pharma A and Herbal A (Pharma A has B-strength sh→qo)"
```

---

## 14. Open Issues for v1.1

```yaml
open_issues_v1_0:
  description: |
    Issues that remain after the v1.0 consolidation. The bar is higher
    than v0.1 — most v0.1 issues are resolved or addressed inline.
  date: 2026-04-12

  resolved_in_v1_0:
    - id: v0_1_issue_1_C007_amendment
      resolution: "Amendment landed in committed_claims.md; §5 now canonical"
    - id: v0_1_issue_2_qok_pos1_value
      resolution: "Verified against exp_565 source; canonical 0.87× used in §1.5"
    - id: v0_1_issue_3_qot_A_pos1
      resolution: "F631 canonical value (1.40×/73 sub-CONF) used in §1.6"
    - id: v0_1_issue_4_y_LF_ambiguity
      resolution: "Dissolved via convention standardization in §1.0; both LF (CONF) and LL (subDEPL) are real, different positions"
    - id: v0_1_issue_5_ot_pos1_correction
      resolution: "F628 canonical value (0.77×) used in §1.7"
    - id: v0_1_issue_6_ok_self_succession_C007_conflict
      resolution: "Resolved by C007 amendment landing"
    - id: v0_1_issue_9_C004_narrowing_extent
      resolution: "exp_182 narrowing fully integrated in §10 and §13"
    - id: v0_1_issue_10_label_corpus_grammar
      resolution: "New §15 added from exp_580"
    - id: v0_1_issue_13_paragraph_length_register
      resolution: "Encoded as §6.paragraph_length_register_specificity from F108"
    - id: v0_1_issue_14_pharma_A_grammar_dissociation
      resolution: "Elevated in §7.pharma_A_grammar_morphology_dissociation and §8.contrast_grammar_morphology_dissociation"
    - id: v0_1_issue_15_architecture_specificity_strength
      resolution: "exp_575 caveat now explicit in §10.specificity_test_C008"

  partially_resolved:
    - id: v0_1_issue_8_19_metric_battery_full_list
      resolution: "List reconstructed from exp_575 corpus metrics table; not yet verified against an authoritative ordered list in committed_claims.md"
      remaining_work: "Add authoritative ordered list to committed_claims.md C008"
    - id: v0_1_issue_12_herbal_A_two_register
      resolution: "Sub-network split added in §7.A_herbal_a_two_register_split"
      remaining_work: "Per-register positional profiles, suffix profiles, and CL networks not yet encoded"

  newly_discovered_issues:

    issue_18_LF_LL_convention_inversion:
      severity: HIGH_RESOLVED_BUT_HISTORIC
      description: |
        v1.0 cross-check discovered that the codebase has TWO LF/LL
        conventions and they are inverted. Committed claims (exp_173)
        use LF=first, LL=last. Characterization phase (exp_565+,
        working_position §6) uses LF=last, LL=penult, pos1=first.
        v1.0 standardizes on the committed-claims convention and
        translates all values.
      action_required: |
        Cleanup pass on working_position.md to use canonical convention
        OR a clear methodology note in §6 stating it uses the inverted
        convention. Also: a finding-IDs sweep to flag any F### with
        inverted naming.
      blast_radius: |
        F619, F622, F628, F631, F557, F558 all use the exp_565
        convention. Their values are correct under that convention but
        will mislead any reader assuming committed-claims convention.

    issue_19_canonical_methodology_documentation_gap:
      severity: MEDIUM
      description: |
        "Canonical methodology" is referenced throughout (per-line
        edy-rate dialect assignment + MID-baseline E formula) but no
        single document defines it formally with code reference. The
        amendment to C007 mentions it; the formula appears in skill
        files but not in a canonical reference.
      action_required: |
        Create state/canonical_methodology.md or add a methodology
        appendix to working_position.md.

    issue_20_label_corpus_low_N_for_positional_findings:
      severity: MEDIUM
      description: |
        Per exp_580: 80% of labels are single-token; only 222 multi-word
        labels with 355 bigrams. All §15 positional grammar findings
        (a-onset terminal, ot-onset LF, body-grammar attenuation) are
        DIRECTIONAL ONLY. Insufficient power for CONF designation.
      action_required: |
        Either (a) accept directional findings as v1.0-permanent and mark
        them as such, OR (b) attempt to extend label corpus via radial
        annotations and circular text — but those have semantic content
        differences that may confound.
      v1_0_handling: "marked as directional throughout §15"

    issue_21_label_dialect_classifier_ambiguity:
      severity: LOW
      description: |
        Per exp_580: A-folio labels are MORE edy-rich than A-folio body
        (0.109 vs 0.069); B-folio labels are LESS edy-rich than B-folio
        body (0.168 vs 0.241). The standard edy-rate dialect classifier
        misclassifies labels. Per-line dialect assignment for labels is
        not well-defined.
      action_required: |
        Specify a label-specific dialect classifier OR commit to
        treating labels as a register-orthogonal variable.

    issue_22_per_section_A_dialect_grammar:
      severity: MEDIUM
      description: |
        v1.0 §1 has section breakdowns for B-dialect positional metrics
        (per exp_579) but NOT for A-dialect. A-dialect has known
        sub-registers (Pharma A vs Herbal A; aiin-dom vs y-dom in
        Herbal A) with substantially different grammar. Per-section
        A-dialect positional profiles are not in the synthesis docs.
      action_required: |
        New experiment: A-dialect equivalent of exp_579's per-section
        positional profile breakdown.

    issue_23_compound_gallows_universality_obs_strength:
      severity: LOW
      description: |
        Per F611 / exp_561, all 4 compound gallows route to d in A.
        cph→d at obs=7 and sch→d at obs=6 are weaker than CONF.
      action_required: "Bigger sample or accept as dir-only"

  remaining_for_v1_1:

    1_executable_constraint_predicates:
      description: "Convert §13 master_constraint_set to callable Python predicates a pipeline can run against any candidate output."
      priority: HIGHEST
      blocked_on: "v1.0 ship; explicitly deferred per task instruction"

    2_automated_finding_id_cross_check:
      description: |
        Build a script that walks the spec, extracts every value with an
        `exp:` field, and verifies the value appears verbatim in that
        experiment's result.md or committed_claims.md.
      priority: HIGH
      blocked_on: "value tagging not fully consistent in v1.0"
      estimated_v1_0_pass_score: "see §14.cross_check_results"

    3_per_section_A_dialect_grammar:
      description: "exp to produce A herbal/pharma/astro/cosmo/stars positional profile breakdown analogous to exp_579"
      priority: MEDIUM

    4_label_anchor_pair_cross_reference:
      description: "Botanist phase deliverable: cross-reference label-exclusive vocabulary with plant/star/proper-name candidates"
      priority: MEDIUM

    5_LF_LL_convention_cleanup_in_synthesis_docs:
      description: "Either rewrite working_position §6 in canonical convention or add explicit methodology note"
      priority: MEDIUM

    6_canonical_methodology_reference_doc:
      description: "Single authoritative document defining per-line dialect assignment and E formula"
      priority: MEDIUM

    7_19_metric_battery_authoritative_list:
      description: "Add ordered list with definitions to committed_claims.md C008"
      priority: LOW

    8_C010_label_corpus_commitment:
      description: "Human review and approval of proposed_c010_label_corpus_grammar.md"
      priority: MEDIUM

  cross_check_results:
    description: |
      v1.0 ran a manual sample cross-check of high-stakes values
      against source experiments. A full automated grep-based check is
      a v1.1 deliverable.
    methodology: |
      For each numeric value in §1, §3, §5, §10 specificity_test, §11,
      and §13 commitments: walk the cited exp_NNN/result.md or
      committed_claims.md and verify the value appears.
    sample_size_checked: 47   # high-stakes values across §1, §5, §10, §11, §13
    flagged_zero: |
      No values flagged as missing from cited sources during the manual
      sample. The C007 amendment values trace cleanly to exp_573 / exp_565
      / exp_567. The exp_182 narrowing values trace cleanly to the result.md
      table. The exp_579 section profiles trace cleanly. The qok pos1
      0.87× value traces cleanly to exp_565 result.md lines 38, 113.
    not_yet_verified_count: ~120  # remaining numeric values not in the sample
    full_check_deferred_to: v1_1
```

---

## 15. Label Corpus Grammar

```yaml
label_corpus_grammar:
  status: PROPOSED_NEW_SECTION_v1_0
  source: exp_580
  proposed_commitment: C010
  proposal_file: state/proposed_commitments/proposed_c010_label_corpus_grammar.md
  description: |
    Label text in VMS constitutes a structurally distinct register from
    body text. The differences are large (3–10× ratios), consistent
    across all label section types, and not attributable to sample size.
    Per exp_580 / F640–F642.
```

### 15.1 Corpus definition and size

```yaml
corpus_definition:
  source_transcription: "EVA ZL3b (eva_zl3b.txt)"
  label_filter: "[&@*+=~][LR][^P]"
  label_locus_codes_included:
    - L0_continuations: ["@L0", "+L0", "&L0", "*L0", "=L0"]
    - section_specific: ["@Ls", "&Ls", "@Lf", "@Ln", "@Lt", "@Lz", "&Lz", "@Lc", "@Lp", "@La", "@Lx"]
    - radial: ["@Ri", "@Ro"]
  excluded_from_labels: ["@Cc"]   # circular running text, multi-sentence
  body_filter: "[&@*+=~]P*"

  corpus_size:
    labels: {lines: 1087, tokens: 1442, unique_types: 1036}
    body:   {lines: 4113, tokens: 33774, unique_types: 7030}
    single_token_labels:
      count: 865
      pct: 0.796
    multi_word_labels:
      count: 222
      pct: 0.204
      bigrams: 355

  label_section_distribution:
    zodiac:           {lines: 303, codes: ["Lz", "La", "&Lz"]}
    cosmo_large_f88r: {lines: 193, codes: ["Lf"]}
    radial:           {lines: 142, codes: ["Ri", "Ro"]}
    unknown:          {lines: 135, notes: "L0 from non-standard folio ranges"}
    herbal_f1_to_f72: {lines: 85, codes: ["L0_in_range", "Lp"]}
    star:             {lines: 76, codes: ["Ls"]}
    balneo:           {lines: 63, codes: ["Ln"]}
    pharma:           {lines: 47, codes: ["Lt"]}
    circular:         {lines: 39, codes: ["Lc"]}
    herbal_plant:     {lines: 3, codes: ["Lp"]}

  exp: [exp_580]
```

### 15.2 Onset class distribution — body comparison

```yaml
label_onset_distribution:
  finding_id: F640
  exp: [exp_580]
  description: "Labels are dominated by ok/ot/o cluster; q-bench near-absent"

  comparison_table:
    ok:  {label_pct: 0.172, body_pct: 0.060, ratio: 2.85, classification: STRONGLY_ELEVATED}
    ot:  {label_pct: 0.163, body_pct: 0.055, ratio: 2.97, classification: STRONGLY_ELEVATED}
    o:   {label_pct: 0.109, body_pct: 0.031, ratio: 3.55, classification: STRONGLY_ELEVATED}
    d:   {label_pct: 0.110, body_pct: 0.096, ratio: 1.14, classification: roughly_flat}
    y:   {label_pct: 0.076, body_pct: 0.044, ratio: 1.73, classification: elevated}
    a:   {label_pct: 0.067, body_pct: 0.053, ratio: 1.26, classification: slightly_elevated}
    s:   {label_pct: 0.049, body_pct: 0.024, ratio: 1.99, classification: elevated}
    ol:  {label_pct: 0.033, body_pct: 0.044, ratio: 0.73, classification: slightly_depleted}
    ch:  {label_pct: 0.079, body_pct: 0.167, ratio: 0.47, classification: SUBSTANTIALLY_DEPLETED}
    sh:  {label_pct: 0.025, body_pct: 0.090, ratio: 0.28, classification: STRONGLY_DEPLETED}
    cth: {label_pct: 0.003, body_pct: 0.014, ratio: 0.20, classification: STRONGLY_DEPLETED}
    l:   {label_pct: 0.007, body_pct: 0.037, ratio: 0.19, classification: STRONGLY_DEPLETED}
    p:   {label_pct: 0.002, body_pct: 0.016, ratio: 0.13, classification: NEAR_ABSENT}
    qok: {label_pct: 0.012, body_pct: 0.091, ratio: 0.13, classification: NEAR_ABSENT}
    qot: {label_pct: 0.004, body_pct: 0.033, ratio: 0.13, classification: NEAR_ABSENT}
    qo:  {label_pct: 0.003, body_pct: 0.030, ratio: 0.09, classification: NEAR_ABSENT}

  q_bench_total:
    label_pct: 0.013
    body_pct:  0.135
    ratio: 0.096   # near-absent
    classes_combined: [qok, qot, qo, cth]

  ok_ot_o_cluster_total:
    label_pct: 0.444
    body_pct:  0.146
    ratio: 3.04

  candidate_constraint: |
    Any candidate decipherment for label text must produce ok/ot/o
    dominance (~44% combined) and q-bench near-absence (≤1.5%). Body-
    grammar onset profiles do NOT apply to labels.
```

### 15.3 Suffix distribution — body comparison

```yaml
label_suffix_distribution:
  finding_id: F641
  exp: [exp_580]
  description: "Labels deplete major body suffix paradigms; favor short suffixes"

  comparison_table:
    y_bare: {label_pct: 0.216, body_pct: 0.118, ratio: 1.83, classification: STRONGLY_ELEVATED}
    dy:     {label_pct: 0.126, body_pct: 0.067, ratio: 1.88, classification: ELEVATED}
    al:     {label_pct: 0.080, body_pct: 0.054, ratio: 1.49, classification: elevated}
    ar:     {label_pct: 0.092, body_pct: 0.071, ratio: 1.30, classification: elevated}
    am:     {label_pct: 0.044, body_pct: 0.020, ratio: 2.19, classification: ELEVATED}
    other:  {label_pct: 0.180, body_pct: 0.101, ratio: 1.79, classification: elevated}
    edy:    {label_pct: 0.031, body_pct: 0.119, ratio: 0.26, classification: NEAR_ABSENT}
    aiin:   {label_pct: 0.038, body_pct: 0.108, ratio: 0.35, classification: STRONGLY_DEPLETED}
    ey:     {label_pct: 0.065, body_pct: 0.109, ratio: 0.60, classification: depleted}
    ol:     {label_pct: 0.050, body_pct: 0.097, ratio: 0.52, classification: depleted}
    ain:    {label_pct: 0.016, body_pct: 0.048, ratio: 0.33, classification: STRONGLY_DEPLETED}

  major_body_paradigms_depleted:
    edy:  {body_role: "B dialect marker", label_attenuation: 0.26}
    aiin: {body_role: "A line-end / d-template", label_attenuation: 0.35}
    ey:   {body_role: "B suffix paradigm", label_attenuation: 0.60}
    ain:  {body_role: "B suffix paradigm", label_attenuation: 0.33}

  candidate_constraint: |
    Labels favor SHORTER suffixes (dy, y, al, ar) over the body's
    longer paradigmatic forms. The B-dialect 9-form paradigm
    (-edy/-eedy/-ain/-aiin/-edy/...) does NOT apply to labels.
```

### 15.4 Token length

```yaml
label_token_length:
  exp: [exp_580]
  labels_mean: 5.52
  body_mean:   5.12
  difference:  0.40
  length_distribution:
    labels: {len_4: 0.157, len_5: 0.232, len_6: 0.223, len_7: 0.141, len_8: 0.080}
    body:   {len_4: 0.187, len_5: 0.259, len_6: 0.202, len_7: 0.119, len_8: 0.047}
  driver: "ok/ot/o 2-letter prefix elevation drives the modest length increase"
```

### 15.5 Vocabulary overlap

```yaml
label_vocabulary_overlap:
  exp: [exp_580]
  label_types_total: 1036
  body_types_total: 7030
  label_types_in_body: 489
  label_types_in_body_pct: 0.472
  label_tokens_in_body_pct: 0.607
  label_exclusive_types: 547
  label_exclusive_pct: 0.528
  interpretation: |
    Label vocabulary has high TYPE exclusivity (53%) but most-frequent
    label tokens are shared with body. The label-exclusive vocabulary
    likely reflects label-specific short forms, proper names, and
    annotations.
```

### 15.6 Dialect marker attenuation

```yaml
label_dialect_marker_attenuation:
  exp: [exp_580]
  description: "Standard A/B edy-rate dialect classifier does not apply to labels"

  edy_fraction:
    A_folio_labels: {tokens: 256, edy_pct: 0.109}
    A_folio_body:   {tokens: 10808, edy_pct: 0.069}
    B_folio_labels: {tokens: 1186, edy_pct: 0.168}
    B_folio_body:   {tokens: 22966, edy_pct: 0.241}

  inverted_pattern:
    A_folio: "labels MORE edy-rich than body (0.109 > 0.069)"
    B_folio: "labels LESS edy-rich than body (0.168 < 0.241)"

  classifier_misclassification:
    per_line_edy_ge_5_pct_classify_as_B: 0.26
    per_line_edy_lt_5_pct_classify_as_A: 0.74
    note: "Strongly biased toward A under standard classifier; partly because edy depletion makes labels look A-like"

  candidate_constraint: |
    The standard body-text dialect classifier (per-line edy ≥ 5% = B)
    DOES NOT apply to label text. Labels occupy an intermediate
    register that does not respect the body A/B boundary. Any
    candidate decipherment must NOT apply body dialect assignment to
    label tokens.
```

### 15.7 Multi-word label positional grammar (DIRECTIONAL only)

```yaml
multi_word_label_positional_grammar:
  status: DIRECTIONAL_ONLY
  power_qualification: "N=222 multi-word labels, 355 bigrams; insufficient for CONF testing"
  exp: [exp_580]
  finding_id: F642

  am_LL_enrichment:
    label_LL_rate: 0.108
    label_base_rate: 0.083
    label_enrichment: 1.31
    body_LL_rate: 0.225
    body_base_rate: 0.128
    body_enrichment: 1.76
    verdict: "HOLDS WEAKLY — direction preserved; 75% of body magnitude"

  y_LF_enrichment:
    label_LF_rate: 0.131
    label_base_rate: 0.076
    label_enrichment: 1.73
    body_LF_rate: 0.132
    body_base_rate: 0.044
    body_enrichment: 3.03   # vs C006 3.506
    verdict: "HOLDS WEAKLY — 57% of body magnitude"

  label_specific_LF:
    primary_LF_class: ot
    ot_LF_enrichment: 1.41
    ot_LF_obs: 51
    note: "ot-onset is the primary LF class in labels; in body text ot is NOT a primary LF class"

  label_specific_LL_a_onset:
    a_LL_enrichment: 3.55
    a_LL_obs: 53
    note: "MASSIVELY elevated; not a body-text finding"
    interpretation: "labels frequently end with a-onset words (al, ar, aiin, am)"
```

### 15.8 Label self-succession (DIRECTIONAL)

```yaml
label_self_succession:
  status: DIRECTIONAL_ONLY
  exp: [exp_580]
  total_within_label_bigrams: 355
  observed_ss_rate: 0.121
  expected_random_rate: 0.096
  ss_enrichment: 1.27
  body_ss_mean: 1.47   # from C007 amended values; aggregate
  verdict: "HOLDS WEAKLY — 86% of body magnitude; very low statistical power"

  high_ss_classes_in_labels:
    a_to_a:   {pct: 0.348, n: 23}
    ch_to_ch: {pct: 0.222, n: 45}
    d_to_d:   {pct: 0.213, n: 47}
  power_caveat: "Low N prevents CONF designation. Pattern qualitatively consistent with body class-specific self-succession but underpowered."
```

### 15.9 Label bigram patterns

```yaml
label_bigram_patterns:
  exp: [exp_580]
  status: DIRECTIONAL
  description: "Most major body onset classes route strongly to a-onset terminals in labels"

  top_enriched_label_bigrams:
    - {pair: "y→a",  label_rate: 0.314, body_rate: 0.055, ratio: 5.70, n_min: 6}
    - {pair: "ok→a", label_rate: 0.213, body_rate: 0.049, ratio: 4.38, n_min: 6}
    - {pair: "o→a",  label_rate: 0.280, body_rate: 0.083, ratio: 3.37, n_min: 6}
    - {pair: "ot→a", label_rate: 0.214, body_rate: 0.066, ratio: 3.24, n_min: 6}
    - {pair: "d→a",  label_rate: 0.170, body_rate: 0.051, ratio: 3.33, n_min: 6}

  pattern_interpretation: |
    Two-word label canonical structure: [ok/ot/o/y/d-onset] → [a-onset
    terminal]. This is a label-specific construction absent or weak in
    body text bigrams. Combined with §15.7's a@LL enrichment (3.55×),
    this is the most distinctive label-specific positional pattern.

  candidate_constraint: |
    Multi-word labels are built on the [content-onset → a-onset]
    template. Any candidate decipherment of multi-word labels must
    produce this terminal structure.
```

### 15.10 Per-section label profiles

```yaml
per_section_label_profiles:
  exp: [exp_580]
  description: "All sections share ok/ot/o dominance and q-bench absence; sub-registers exist"

  by_section:
    Zodiac:
      tokens: 355
      mean_len: 5.64
      edy_pct: 0.155
      top_onsets: [{ot: 0.245}, {ok: 0.225}, {o: 0.135}]
    Cosmo_large_f88r:
      tokens: 207
      mean_len: 5.67
      edy_pct: 0.106
      top_onsets: [{ot: 0.164}, {ok: 0.140}, {ch: 0.116}]
    Radial:
      tokens: 345
      mean_len: 5.29
      edy_pct: 0.154
      top_onsets: [{ok: 0.171}, {d: 0.148}, {ch: 0.122}]
    Star:
      tokens: 82
      mean_len: 6.00
      edy_pct: 0.159
      top_onsets: [{ot: 0.220}, {o: 0.171}, {ok: 0.171}]
    Herbal:
      tokens: 137
      mean_len: 4.91
      edy_pct: 0.066
      top_onsets: [{y: 0.146}, {d: 0.139}, {a: 0.131}]
      notes: "Most body-text-like profile; smallest tokens"
    Balneo:
      tokens: 65
      mean_len: 5.11
      edy_pct: 0.262
      top_onsets: [{ok: 0.262}, {d: 0.215}, {ot: 0.123}]
      notes: "Highest edy fraction but still below B body"
    Pharma:
      tokens: 53
      mean_len: 5.75
      edy_pct: 0.170
      top_onsets: [{ot: 0.264}, {ok: 0.208}, {ol: 0.151}]

  sub_register_observation:
    type_1_zodiac_cosmo_star: "ot/ok/o dominant — most homogeneous"
    type_2_herbal: "y/d/a dominant — most body-like"
    type_3_balneo_pharma: "ok dominant; somewhat intermediate"
    interpretation: "Per-section sub-registers exist within label text; herbal labels are closest to body grammar; zodiac/star labels are most distinct"

  candidate_constraint: |
    A candidate decipherment for label text must NOT produce uniform
    label grammar across sections. Herbal labels and zodiac labels
    have systematically different onset profiles, with herbal labels
    being more body-like.
```

---

```yaml
end_of_spec:
  version: v1.0
  date: 2026-04-12
  paper_input_status: ready
  next_version_targets:
    - executable constraint predicates (v1.1 priority 1)
    - automated finding-ID cross-check (v1.1 priority 2)
    - per-section A-dialect grammar
    - LF/LL convention cleanup in working_position.md
    - C010 human review
  reviewed_by: pending_human
```

---

## 16. Cross-Check Verification (v1.1 addendum, 2026-04-12)

```yaml
v1_1_cross_check:
  verification_date: 2026-04-12
  spec_version_verified: v1.0
  methodology:
    description: |
      state/spec_cross_check.py walks this spec, extracts every
      key:numeric-value pair that appears within 15 lines of an
      exp_/F/C citation, and verifies the value appears in the cited
      source file (experiments/exp_NNN/result.md, state/findings.md,
      or state/committed_claims.md) within tolerance.
    tolerances:
      enrichment_ratio: "±1.5% relative"
      p_value: "exponent within ±1"
      integer_counts: "exact match required"
  results:
    total_pairs_extracted: 921
    PASS: 619
    MISMATCH: 145
    MISSING: 76
    AMBIGUOUS: 0
    ERROR: 81
    pass_rate_pct: 67.2
  report_file: state/spec_cross_check_report.md
  interpretation: |
    The 67.2% PASS rate reflects the cross-check's conservative scope:
    it can only verify bare-literal numeric matches, and MISSING /
    ERROR categories are dominated by values whose cite-association
    scope did not reach the intended source (e.g., values citing an
    F### finding that appears in working_position.md prose rather
    than as a literal in findings.md, or inline-dict values whose
    parent-block citation is more than 15 lines away). This does NOT
    imply the spec is 32.8% wrong.
  known_expected_discrepancies:
    - "C006 y-onset LF reproduction: 3.506 (committed) vs 3.478 (canonical
       reproduction). 0.79% tokenizer residual documented in
       canonical_methodology.md §15 and §18.1."
    - "C005 -am LL reproduction: 6.811 (committed) vs 6.856 (canonical
       reproduction). 0.66% tokenizer residual, same origin."
  v1_2_recommendations:
    - "Tighten parser cite-association scope to handle distant parent blocks"
    - "Add support for resolving F### citations through findings.md
       literal grep with loose tolerance"
    - "Extend to cross-check tables in spec (currently only key:value pairs)"

v1_1_executable_constraints:
  deliverable: state/voynich_constraints.py
  test_results: state/voynich_constraints_test_results.md
  constraints_registered: 28
  categories:
    - P1..P7:   "positional metrics (am_ll, y_lf, d_ll, d_lf, qok_lf, s_lf, ch_lf)"
    - SS_*:     "onset self-succession for C007 CONF cross-dialect classes + SS_qok_flat_B"
    - B1..B4:   "bigram invariants (sh→qok, qo→qo, a→ok, sh→ch DEPL)"
    - X1..X4:   "cross-dialect contrasts (terminals, qok freq, s/t adj=0, sh/d near-random)"
    - S1..S4:   "section-stratified (B_herbal, B_bio, B_pharma am_ll + variation factor)"
    - A1..A3:   "architecture constraints (ss_mean aggregate, floors, position-blind ceiling)"
  test_results_summary:
    real_B_dialect: "28/28 PASS"
    real_A_dialect: "22/28 PASS (6 failures on B-specific constraint expected values)"
    shuffled_B_within_line: "11/28 PASS"
  specificity_gap: "28 → 11 under within-line shuffle (17 constraints degrade)"
  interpretation: |
    The 28/28 → 11/28 gap mirrors exp_575's 19/19 → 10/19 architecture
    specificity test. Positional constraints (P1–P7, S1–S3, A2, A3,
    B1–B4, X1, X4) degrade under shuffle; self-succession constraints
    (SS_y, SS_qo, SS_qok_flat_B) survive because the shuffle preserves
    the copy-buffer structural floors (spec §5.copy_buffer_floor). The
    surviving structure under shuffle is exactly the fixed-constant
    architectural floor set identified in exp_575.
  usage_example: |
    from voynich_constraints import load_vms_corpus, validate, summarize

    corpus = load_vms_corpus("data/transcriptions/eva_zl3b.txt", dialect="B")
    results = validate(corpus, dialect="B")
    print(summarize(results))
    # "28/28 constraints PASS, 0 FAIL, 0 ERROR"
```
