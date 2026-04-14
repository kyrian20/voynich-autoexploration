# Voynichese Grammar Specification

```yaml
spec_version: v0.1
date: 2026-04-12
status: first-pass consolidation; awaiting human review
source_phase: Cryptanalyst characterization phase closure (exp_001 through exp_579)
authoritative_synthesis_documents:
  - state/working_position.md          # full human-readable synthesis
  - state/committed_claims.md          # canonical C001–C009
  - state/q007_investigation.md        # Q007 closure
  - state/proposed_c007_amendment.md   # canonical self-succession values
  - experiments/exp_579/result.md      # document-order heterogeneity
  - experiments/exp_575..578/result.md # specificity, parameter stability, Q007
audience: future LLM instance or decipherment pipeline
purpose: |
  Constraints any candidate decipherment mapping or generative theory of
  Voynichese must respect. Each entry is a structural fact with a
  traceable experiment citation, NOT an interpretation.
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
- `exp_dependent: true` marks a value carried over from synthesis prose
  whose underlying experiment ID is partially traceable; flagged in
  Open Issues.

**Citation conventions.** All `F###` finding IDs reference state/findings.md.
All `exp_NNN` IDs reference experiments/exp_NNN_*/result.md. All `C00N`
IDs reference state/committed_claims.md.

**Query patterns this spec supports.**
1. "Given a candidate plaintext mapping for word W, does the resulting
   distribution match the positional profile of W's onset class?"
   → Section 1.
2. "Does the candidate generator produce the right suffix paradigm and
   the A→B suffix transformation?"
   → Section 2.
3. "Does the candidate model generate the bigram matrix and self-
   succession structure?"
   → Sections 4, 5.
4. "Does the candidate model respect the three-register line grammar
   and the paragraph chain grammar of the relevant section?"
   → Sections 6, 7.
5. "Does the candidate decipherment respect the architecturally-known
   ruled-out mechanism classes?"
   → Sections 10, 12.

**What this spec is NOT.** Not a methodological tutorial; not a paper;
not a list of failed approaches. Mechanisms are listed in the "ruled
out" section only when a candidate decipherment must structurally
avoid producing them.

---

## Table of Contents

1. Positional profiles per onset class per dialect
2. Suffix paradigms and A→B suffix transformations
3. Closed paradigm sizes (CP90) per onset class per dialect
4. Onset-class bigram matrices per dialect
5. Self-succession per onset class per dialect
6. Three-register line grammar
7. Paragraph chain grammar by section
8. Cross-dialect structural contrasts
9. Word-internal structure
10. Architecture capabilities and limits (21-mechanism findings)
11. Document-order heterogeneity caveat (exp_579 / C008 qualification)
12. Things explicitly ruled out
13. Committed claims index (C001–C009)
14. Open issues for human review

---

## 1. Positional Profiles per Onset Class per Dialect

```yaml
positional_profiles:
  baseline_definitions:
    pos1:    "first content word of a line (== LF)"
    LF:      "line-first slot"
    MID:     "all interior word positions"
    LL:      "line-last slot"
    pen:     "penultimate position"
    enrichment: "ratio of class rate at slot to class corpus base rate"
    CONF_threshold: "≥1.50× AND obs ≥ 10 (per exp_173 canonical)"
    DEPL_threshold: "≤0.67× AND obs ≥ 10"
    section_qualification: |
      Per exp_579, B-dialect positional metrics are NOT corpus-stationary.
      Positional values for B MUST be reported per section. Full-corpus
      averages mask 2–3× variation across sections (e.g., am_ll ranges
      from 0.053 in B_bio to 0.192 in B_pharma).
```

### 1.1 d-onset

```yaml
d:
  description: "EVA d-initial; daiin/dy/dam/dar template family"
  is_key_dialect_crossing_class: true
  exp: [exp_543, exp_553, exp_554, exp_555, exp_556]

  by_dialect:
    A:
      pos1:
        enrichment: 1.47
        obs: 346
        confidence: subCONF  # near-CONF
        exp: [exp_549, exp_553]
        notes: "A: dominant LINE-OPENER"
      LF:
        enrichment: 1.53
        obs: 360
        confidence: CONF
        exp: [exp_553, exp_557]
        notes: "A: dominant LF class; 18.4% of A lines open with d"
      MID:
        enrichment: 0.73
        confidence: DEPL
        exp: [exp_553]
      LL:
        enrichment: 1.50
        confidence: CONF
        exp: [exp_074, exp_557]
        notes: "A LL d-onset enrichment 1.73× elsewhere; F081"
      role: "TERMINAL + MID-depleted; aiin-body line-closer"

    B:
      by_section:
        B_herbal:
          d_LL_raw_rate: 0.1768
          confidence: CONF
          exp: [exp_579]
        B_bio:
          d_LL_raw_rate: 0.1279
          confidence: CONF
          exp: [exp_579]
        B_astro:
          d_LL_raw_rate: 0.1054
          exp: [exp_579]
        B_pharma:
          d_LL_raw_rate: 0.0655
          exp: [exp_579]
      pos1_full_corpus:
        enrichment: 2.64
        obs: 246
        confidence: CONF
        exp: [exp_543, exp_555]
        notes: "B: dominant LINE-OPENER (19.2% of B lines)"
      LL_full_corpus:
        enrichment: 1.36
        confidence: CONF
        exp: [exp_555, exp_575]
      MID:
        enrichment: 0.67
        confidence: DEPL
        exp: [exp_555]
      role: "OPENER + MID-depleted"
      qualification: |
        Positional rates per exp_579 vary by section. B_herbal d@LL is
        2.7× B_pharma. Architecture calibration uses full-corpus average;
        section-level calibration would diverge.

  cross_dialect_pattern:
    type: A_B_positional_inversion
    description: |
      A: d is the dominant TERMINAL class (LF CONF, ~18% of A lines).
      B: d is the dominant LINE-OPENER (pos1 CONF, ~19% of B lines).
      Both: MID-depleted (A 0.73×, B 0.67×).
    exp: [exp_553, exp_555, exp_557]
    importance: "key dialect-crossing class"
```

### 1.2 y-onset

```yaml
y:
  description: "EVA y-initial; line-opener template (y+gallows compound)"
  exp: [exp_545, exp_557, exp_558, exp_559]

  by_dialect:
    A:
      pos1:
        enrichment: 2.78
        obs: 323
        confidence: CONF
        exp: [exp_545, exp_557]
      LF:
        enrichment: 0.62
        confidence: subDEPL
        exp: [exp_557]
        notes: "A LF AVOIDER paradoxically — pos1 ≠ LF in A herbal_a register classification"
      LL: {confidence: depleted, exp: [exp_557]}
      MID: {confidence: depleted, exp: [exp_557]}
    B:
      by_section:
        B_herbal:
          y_LF_raw_rate: 0.1793
          exp: [exp_579]
        B_bio:
          y_LF_raw_rate: 0.0743
          exp: [exp_579]
        B_astro:
          y_LF_raw_rate: 0.1201
          exp: [exp_579]
        B_pharma:
          y_LF_raw_rate: 0.1688
          exp: [exp_579]
      pos1_full_corpus:
        enrichment: 3.54
        obs: 147
        confidence: CONF
        exp: [exp_558, exp_545]
      LF_full_corpus:
        enrichment: 3.506
        p_value: 2.86e-90
        exp: [exp_173]
        commitment: C006
      LF_avoider_role:
        enrichment_full: 0.60
        confidence: subDEPL
        exp: [exp_557]
        note: "y is BOTH dominant pos1 AND LF AVOIDER under different metric definitions; reflects pos1 vs LF alignment subtlety"
      MID: depleted
      LL: depleted

  pattern: definitive_LINE_OPENER
  cross_dialect_constants:
    - "y is LF-depleted (as a body-occurrence metric) in BOTH dialects"
    - "y is dominant pos1 in BOTH dialects (CONF)"
  notes: |
    The simultaneous "LF depleted" and "pos1 enriched" reflects two
    distinct metric definitions. pos1 = first content word; LF includes
    body words at line-first whether or not they begin a line.
```

### 1.3 ch-onset

```yaml
ch:
  description: "EVA ch-initial; most extreme pos1-AVOIDER cross-dialectally"
  exp: [exp_541, exp_547, exp_550, exp_558, exp_566, exp_622, exp_623]

  by_dialect:
    A:
      pos1: {enrichment: 0.32, obs: 154, confidence: DEPL_extreme, exp: [exp_541, exp_622]}
      LF:   {enrichment: 0.81, obs: 373, confidence: subDEPL,      exp: [exp_622]}
      LL:   {enrichment: 0.97, confidence: flat,                    exp: [exp_622]}
      MID:  {role: dominant_MID, exp: [exp_550]}
    B:
      pos1: {enrichment: 0.22, obs: 53,  confidence: DEPL_extreme, exp: [exp_541, exp_622]}
      LF:   {enrichment: 0.80, obs: 194, confidence: subDEPL,      exp: [exp_622]}
      LL:   {enrichment: 0.92, confidence: flat,                    exp: [exp_622]}

  pattern: extreme_pos1_avoider_MID_dominant
  distinguishing_feature: |
    Only major LF class in either dialect with NO CONF opener rule.
    LF is sub-baseline NOT DEPL, distinguishing ch from sh which IS LF DEPL.
  cross_dialect_constants:
    - "ch is pos1-avoider in BOTH dialects (CONF DEPL)"
    - "ch→sh DEPL cross-dialectally (F328)"
  vocabulary_stability: |
    Most dialect-stable vocabulary class. A: chol/chey/chor diverse l/y/r body.
    B: chedy dominant (22%). Both retain y-body dominance.
  exp_vocab: [exp_621]
```

### 1.4 sh-onset

```yaml
sh:
  description: "EVA sh-initial; dialect-specific router class"
  exp: [exp_540, exp_544, exp_564, exp_615, exp_616]

  by_dialect:
    A:
      pos1: {enrichment: 0.77, obs: 148, confidence: subDEPL, exp: [exp_616]}
      LF:   {enrichment: 0.47, obs: 88,  confidence: DEPL,    exp: [exp_616]}
      LL:   {enrichment: 0.85, confidence: subDEPL,            exp: [exp_616]}
      MID_share_approx: 0.75
    B:
      pos1: {enrichment: 0.56, obs: 78,  confidence: DEPL_formal, exp: [exp_616]}
      LF:   {enrichment: 0.39, obs: 54,  confidence: DEPL_strong, exp: [exp_616]}
      LL:   {enrichment: 0.80, confidence: subDEPL,                exp: [exp_616]}
      MID_share_approx: 0.75

  pattern: MID_dominant_LF_avoider
  routing_dichotomy:
    description: "sh is a dialect-specific ROUTER"
    A_routes_to_gallows:
      - {target: "sh→k",  enrichment: 1.75, obs: 31, confidence: CONF, exp: [exp_544]}
      - {target: "sh→t",  enrichment: 1.62, obs: 13, confidence: CONF, exp: [exp_544]}
    B_routes_to_q_class:
      - {target: "sh→qok", enrichment: 2.02, obs: 331, confidence: CONF, exp: [exp_544, exp_620]}
      - {target: "sh→qo",  enrichment: 1.92, obs: 68,  confidence: CONF, exp: [exp_544]}
      - {target: "sh→qot", enrichment: 1.74, obs: 78,  confidence: CONF, exp: [exp_544]}
  cross_dialect_constants:
    - "sh is LF-DEPL in BOTH dialects (CONF)"
    - "sh→ch DEPL in BOTH dialects (A 0.65×/127, B 0.54×/92; F328)"
  vocabulary:
    A: {tokens: 930, types: 236, dominant: "diverse: shol(9%) sho(8%) shey(8%) sheey(6%) shy(5%)", exp: [exp_615]}
    B: {tokens: 954, types: ?,   dominant: "shedy (28.4%); shey(9%) sheedy(6%)", exp: [exp_615]}
```

### 1.5 qok-onset

```yaml
qok:
  description: "EVA qok-initial; q-bench MID class; sh→qok terminus"
  exp: [exp_376, exp_537, exp_565, exp_618, exp_619]

  by_dialect:
    A:
      LF:   {enrichment: 0.51, obs: 82,  confidence: DEPL,    exp: [exp_619]}
      pos1: {enrichment: 0.87, obs: 145, confidence: subBaseline, exp: [exp_619]}
      LL:   {enrichment: 0.83, confidence: subBaseline,        exp: [exp_619]}
      MID_role: dominant
      tokens: 827
      pct_of_A_tokens: 0.0730
    B:
      LF:   {enrichment: 0.53, obs: 112, confidence: DEPL,    exp: [exp_619]}
      pos1: {enrichment: 0.81, obs: 171, confidence: subBaseline, exp: [exp_619]}
      LL:   {enrichment: 1.00, confidence: flat,               exp: [exp_619]}
      MID_role: dominant
      tokens: 1538
      pct_of_B_tokens: 0.1513
      by_section:
        B_astro:  {pct_of_section_tokens: 0.1958, role: "primary driver of A→B doubling", exp: [exp_618]}
        B_pharma: {pct_of_section_tokens: 0.1281, exp: [exp_618]}
        B_herbal: {pct_of_section_tokens: 0.0919, exp: [exp_618]}
        B_bio:    {pct_qok_LF_raw_rate: 0.1475, exp: [exp_579]}

  cross_dialect_pattern:
    A_to_B_frequency_doubles:
      A_pct: 0.0730
      B_pct: 0.1513
      ratio: 2.07
      driver: "B_astro section grammar (qok elevated to ~20% of section tokens)"
      exp: [exp_618]
  qualification: |
    Working_position.md previously listed A pos1 = 1.47×; F619 corrects
    this to canonical 0.87× sub-baseline. The CORRECTED value is used here.
```

### 1.6 qot-onset

```yaml
qot:
  description: "EVA qot-initial; A pivot class for paragraph chain"
  exp: [exp_534, exp_569, exp_630, exp_631]

  by_dialect:
    A:
      pos1: {enrichment: 1.40, obs: 73, confidence: subCONF,  exp: [exp_631, exp_534]}
      LF:   {enrichment: 0.91, confidence: flat, exp: [exp_631]}
      LL:   {enrichment: 0.89, confidence: flat, exp: [exp_631]}
      MID:  {enrichment: 0.92, confidence: flat, exp: [exp_631]}
      tokens: 291
      pct_of_A_tokens: 0.0257
      role: "near-CONF pos1 opener; pivot of paragraph chain"
      qualification: |
        F631 corrects the prior 1.79×/59 CONF reading to canonical
        1.40×/73 sub-CONF.
    B:
      pos1: {enrichment: 0.69, obs: 37, confidence: DEPL, exp: [exp_631]}
      LF:   {enrichment: 0.86, confidence: subBaseline, exp: [exp_631]}
      LL:   {enrichment: 1.07, confidence: flat,         exp: [exp_631]}
      MID:  {enrichment: 1.08, confidence: flat,         exp: [exp_631]}
      tokens: 426
      pct_of_B_tokens: 0.0419
      role: MID_class

  cross_dialect_pattern:
    type: A_B_positional_inversion
    A_role: opener_subCONF
    B_role: pos1_DEPL
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
      pos1: {enrichment: 0.77, obs: 76, confidence: subBaseline, exp: [exp_628]}
      LF:   {enrichment: 1.09, confidence: flat, exp: [exp_628]}
      LL:   {enrichment: 1.15, confidence: flat, exp: [exp_628]}
      MID:  {enrichment: 1.00, confidence: flat, exp: [exp_628]}
      tokens: 548
      pct: 0.0484
      types: 133
    B:
      pos1: {enrichment: 0.26, obs: 22, confidence: DEPL_extreme, exp: [exp_628]}
      LF:   {enrichment: 1.15, confidence: flat, exp: [exp_628]}
      LL:   {enrichment: 1.36, confidence: subCONF, exp: [exp_628]}
      MID:  {enrichment: 1.05, confidence: flat, exp: [exp_628]}
      tokens: 680
      pct: 0.0669
      types: 125

  cross_dialect_pattern:
    - "ot frequency increases A→B (joining MID-class increase cluster: sh, qo, qok, ot)"
    - "ot pos1 DEPL stronger in B (0.26×) than A (0.77×)"
```

### 1.8 ok-onset

```yaml
ok:
  description: "EVA ok-initial; MID class with pos1 DEPL cross-dialectally"
  exp: [exp_536, exp_567, exp_624, exp_625, exp_626]

  by_dialect:
    A:
      pos1: {enrichment: 0.57, obs: 96, confidence: DEPL, exp: [exp_625]}
      LF:   {enrichment: 0.89, confidence: subBaseline, exp: [exp_625]}
      LL:   {enrichment: 0.91, confidence: subBaseline, exp: [exp_625]}
      tokens: 843
      pct: 0.0744
    B:
      pos1: {enrichment: 0.50, obs: 46, confidence: DEPL, exp: [exp_625]}
      LF:   {enrichment: 0.82, confidence: subBaseline, exp: [exp_625]}
      LL:   {enrichment: 1.09, confidence: flat,         exp: [exp_625]}
      tokens: 671
      pct: 0.0660

  cross_dialect_pattern:
    - "MID class with pos1 DEPL in BOTH dialects"
    - "Distinguished from ch by less extreme pos1 DEPL (ok 0.5–0.6 vs ch 0.2–0.3)"
    - "Distinguished from sh by LF NOT DEPL"
```

### 1.9 qo-onset

```yaml
qo:
  description: "EVA qo-initial bare; B-specific morphological prefix"
  exp: [exp_563, exp_613, exp_614]

  by_dialect:
    A:
      LF:   {enrichment: 0.46, obs: 27, confidence: DEPL, exp: [exp_613]}
      pos1: {confidence: subBaseline, exp: [exp_613]}
      LL:   {confidence: subBaseline, exp: [exp_613]}
      tokens: 293
      pct: 0.0259
    B:
      LL:   {enrichment: 0.52, obs: 21, confidence: DEPL, exp: [exp_613]}
      pos1: {enrichment: 1.07, confidence: flat,          exp: [exp_613]}
      tokens: 314
      pct: 0.0309
      by_section: {B_astro_pct: 0.0425}

  cross_dialect_pattern:
    - "MID class (~75% MID share both dialects)"
    - "A avoids LF (DEPL); B avoids LL (DEPL) — boundary-avoidance dialect specific"
    - "qo is NOT an opener (unlike qot in A)"
```

### 1.10 t-onset

```yaml
t:
  description: "EVA t-initial; gallows opener"
  exp: [exp_551]

  by_dialect:
    A:
      pos1: {enrichment: 2.27, obs: 111, confidence: CONF, exp: [exp_549]}
      LF:   {enrichment: 0.96, confidence: flat, exp: [exp_557]}
      role: opener
      stars_section_pos1: {enrichment: 3.67, obs: 16, confidence: CONF, exp: [exp_523, exp_527]}
    B:
      pos1: {enrichment: 3.18, obs: 78, confidence: CONF, exp: [exp_555]}
      role: opener
      by_section:
        B_herbal: {LF_enrichment: 2.34, exp: [exp_467, F447]}
        B_cosmo:  {LF_enrichment: 2.23, exp: [exp_467, F447]}

  cross_dialect_constants:
    - "t is a CONF pos1 opener in both dialects"
    - "adj_rate for t = 0 in B (0/466 tokens) — structural anti-repetition from pos1 placement (exp_577 / C009 Part B)"
```

### 1.11 s-onset

```yaml
s:
  description: "EVA s-initial; pos1 opener; structural anti-repetition"
  exp: [exp_550, exp_325]

  by_dialect:
    A:
      pos1: {enrichment: 3.16, obs: 163, confidence: CONF, exp: [exp_549]}
      LF:   {enrichment: 1.01, confidence: flat, exp: [exp_557]}
      role: opener
    B:
      pos1: {enrichment: 4.77, obs: 165, confidence: CONF, exp: [exp_555]}
      LF:   {confidence: enriched, exp: [exp_557]}
      role: opener
      by_section:
        B_herbal: {s_LF_raw_rate: 0.0707, exp: [exp_579]}
        B_bio:    {s_LF_raw_rate: 0.1716, exp: [exp_579]}
        B_astro:  {s_LF_raw_rate: 0.0588, exp: [exp_579]}
        B_pharma: {s_LF_raw_rate: 0.1190, exp: [exp_579]}

  cross_dialect_constants:
    - "s is CONF pos1 opener in both dialects"
    - "adj_rate for s = 0 in B (0/452 tokens) — structural anti-repetition from pos1 placement (exp_577, C009 Part B)"
    - "VMS section variation: B_bio s@LF is 2.4× B_astro"
```

### 1.12 p-onset

```yaml
p:
  description: "EVA p-initial; gallows; folio-opener marker"
  exp: [exp_556]

  by_dialect:
    A:
      pos1: {enrichment: 2.99, obs: 15, confidence: CONF, exp: [exp_549]}
      role: opener
      folio_opener_LF_share: 0.373
      folio_closer_LF_obs: 0.000  # 0/83 — complete exclusion
      exp_folio: [exp_354, exp_355, F345]
    B:
      pos1: {enrichment: 5.23, obs: 27, confidence: CONF, exp: [exp_555]}
      role: opener_strongest
      folio_opener_marker: true

  cross_dialect_constants:
    - "p is the strongest pos1 opener in B (5.23×)"
    - "p is exclusively folio-opener in A (0% folio-closer)"
```

### 1.13 k-onset (gallows anomaly)

```yaml
k:
  description: "EVA k-initial; gallows class; LF-anomalous"
  exp: [exp_552, exp_393]
  anomaly:
    Q012_open: |
      Unlike p/t/f, k is NOT LF-enriched. Other gallows are folio-opener
      LF markers; k is pos1-flat. Mechanism unresolved.
```

### 1.14 r-onset

```yaml
r:
  description: "EVA r-initial; B terminal class"
  exp: [exp_378, exp_554]

  by_dialect:
    A: {role: undocumented_in_synthesis, exp: []}
    B:
      LF: {enrichment: 2.80, obs: 48, confidence: CONF, exp: [exp_555, exp_557]}
      role: B_TERMINAL_LF

  cross_dialect_pattern:
    - "B q-bench routing: q-bench → r CONF (1.61×/45) for combined qok+qot; non-q-bench → r flat (F633)"
    - "qok→r CONF B (1.57×/30); qot→r CONF B (1.97×/10)"
```

### 1.15 l-onset

```yaml
l:
  description: "EVA l-initial; B lateral terminal"
  exp: [exp_553]

  by_dialect:
    B:
      LF: {enrichment: 1.85, obs: 145, confidence: CONF, exp: [exp_555, exp_557]}
      role: B_TERMINAL_LF
```

### 1.16 ol-onset

```yaml
ol:
  description: "EVA ol-initial; B vowel-onset terminal"
  exp: [exp_553]

  by_dialect:
    A: {self_succession_CONF_only: true, exp: [exp_553]}
    B:
      LF: {enrichment: 1.65, obs: 115, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LF
```

### 1.17 o-onset

```yaml
o:
  description: "EVA o-initial bare; B vowel terminal"
  exp: [exp_547, exp_548]
  by_dialect:
    B:
      LF: {enrichment: 1.58, obs: 57, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LF
```

### 1.18 a-onset

```yaml
a:
  description: "EVA a-initial; B vowel terminal; pos1 avoider both dialects"
  exp: [exp_549]
  by_dialect:
    B:
      LF: {enrichment: 1.52, obs: 70, confidence: CONF, exp: [exp_555]}
      role: B_TERMINAL_LF
  cross_dialect_constants:
    - "a is pos1-avoider in BOTH dialects"
    - "a→ok CROSS-DIALECTAL CONF (A 1.52×/50; B 1.51×/34) (F626)"
```

### 1.19 cth-onset (compound gallows)

```yaml
cth:
  description: "EVA c-th compound gallows; A TERMINAL"
  exp: [exp_384, exp_558, exp_561]

  by_dialect:
    A:
      LF:   {enrichment: 1.67, obs: 88, confidence: CONF, exp: [exp_557, exp_558]}
      pos1: {enrichment: 0.13, confidence: DEPL_extreme, exp: [exp_558]}
      role: PUREST_A_TERMINAL
      tokens: ~1.0  # baseline
    B:
      tokens_relative_to_A: 0.116  # 8.6× drop
      LF: {enrichment: ~baseline_or_split, exp: [exp_558]}

  paragraph_chain_role:
    A_herbal_a: "d → qot → ch → o → sh, with cth as terminal closer; cth-LF pen=d CONF (F474)"

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
      pos1: {enrichment: 11.54, obs: 16, confidence: CONF_extreme, exp: [exp_558]}
      role: OPENER_extreme
      base_rate_pct: ~0.20
      notes: "Highest pos1 E-value of any characterized class"
```

### 1.21 ckh-onset (compound gallows)

```yaml
ckh:
  description: "EVA c-k-h compound gallows"
  exp: [exp_561]

  by_dialect:
    A:
      pos1: {enrichment: 0.07, confidence: near_zero, exp: [exp_561]}
      LF:   {enrichment: 0.67, obs: 18, confidence: DEPL, exp: [exp_561]}
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
      pos1: {enrichment: 0.12, obs: 1, confidence: near_zero, exp: [exp_610]}
      LL:   {enrichment: 1.45, obs: 12, confidence: subCONF, exp: [exp_610]}
      LF:   {enrichment: 0.72, obs: 6, confidence: subDEPL, exp: [exp_610]}
      tokens: 38
      pct: 0.00335
    B:
      tokens: 7
      pct: 0.00069
      A_to_B_drop: 4.9
      vocab: "cphedy 57.1%"
      exp: [exp_610]

  routing:
    - {pair: "cph→d", confidence: dir, enrichment: 2.50, obs: 7, exp: [exp_610, exp_562]}
    - {pair: "cth→cph", confidence: dir, enrichment: 3.02, obs: 3, exp: [exp_602, exp_610]}
```

### 1.23 Three-layer summary by dialect

```yaml
three_layer_summary:
  A:
    OPENERS_pos1_CONF:
      - {class: sch, enr: 11.54, obs: 16}
      - {class: p,   enr: 2.99,  obs: 15}
      - {class: s,   enr: 3.16,  obs: 163}
      - {class: y,   enr: 2.78,  obs: 323}
      - {class: t,   enr: 2.27,  obs: 111}
      - {class: qot, enr: 1.40,  obs: 73,  status: subCONF}
      - {class: d,   enr: 1.47,  obs: 346, status: near-CONF}
    MID:    [ch, qok, ok, ot, sh, k, ckh, qo]
    TERMINALS_LF_CONF:
      - {class: cth, enr: 1.67, obs: 88}
      - {class: d,   enr: 1.53, obs: 360}
    LF_AVOIDERS: [y_LF_metric, s_LF_metric, t, qok, sh]
    exp: [exp_557]

  B:
    OPENERS_pos1_CONF:
      - {class: p, enr: 5.23, obs: 27}
      - {class: s, enr: 4.77, obs: 165}
      - {class: y, enr: 3.54, obs: 147}
      - {class: t, enr: 3.18, obs: 78}
      - {class: d, enr: 2.64, obs: 246}
    MID:    [ch, qok, ok, ot, qot, sh, k]
    TERMINALS_LF_CONF:
      - {class: r,  enr: 2.80, obs: 48}
      - {class: l,  enr: 1.85, obs: 145}
      - {class: ol, enr: 1.65, obs: 115}
      - {class: o,  enr: 1.58, obs: 57}
      - {class: a,  enr: 1.52, obs: 70}
    LF_AVOIDERS: [y, qok, sh]
    exp: [exp_555]

  cross_dialect_constants:
    LF_DEPL_in_both: [y_metric, qok, sh]
    pos1_AVOIDER_in_both: [ch, a]
    terminal_layer_inversion:
      A_closes_with: [d, cth]   # aiin-body + compound gallows
      B_closes_with: [r, l, ol, o, a]   # lateral / vowel-initial
      overlap: 0
```

### 1.24 B-dialect section LF taxonomy

```yaml
B_section_LF_taxonomy:
  description: "Per F447 / exp_467; positional metrics MUST be reported per section"
  exp: [exp_467, F447]
  caveat: "exp_579 confirms B positional metrics are not corpus-stationary"

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
    Astronomical marker appears at pos1 in A but at LF in B for the
    same astronomical content.
  A_stars: {t_pos1_enrichment: 3.67, obs: 16, confidence: CONF}
  B_corresponding: {qok_LF_elevated: true}
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
    qo:  ~30   # exp_578 baseline
    sh:  145
    d:   146
    ch:  290
    cth: ~80
    t:   169
    y:   191
    l:   195
    r:   66
    notes: "Canonical CP90 from exp_577 Analysis 1 corpus pass"

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
      - {pair: "sh→qok", A_enr: 2.04, A_obs: 114, B_enr: 2.07, B_obs: 266, confidence_both: CONF, exp: [exp_544, exp_614, exp_620]}
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
      - {pair: "y→ckh", A_enr: ?,    confidence: CONF, exp: [exp_545]}

  B_specific_bigrams:
    methodology: "B bigrams must be filtered to MID positions"
    pairs:
      - {pair: "sh→qok", B_enr: 2.07, B_obs: 266, confidence: CONF, exp: [exp_620, exp_544]}
      - {pair: "sh→qot", B_enr: 1.97, B_obs: 72,  confidence: CONF, exp: [exp_544]}
      - {pair: "qot→qot", B_enr: 1.82, B_obs: 29, confidence: CONF, exp: [exp_534]}
      - {pair: "qot→ot", B_enr: subCONF, exp: [F632]}
      - {pair: "qot→r",  B_enr: 1.97, B_obs: 10, confidence: CONF, exp: [exp_534, F633]}
      - {pair: "qok→r",  B_enr: 1.95, B_obs: 30, confidence: CONF, exp: [F620]}
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
      - {pair: "qok→ch", B_enr: 1.27, B_obs: ?,   confidence: subCONF, exp: [exp_173]}

  bigram_grammar_strength:
    A: {bigram_PPL_reduction: 0.091, exp: [exp_074, F081]}
    B: {bigram_PPL_reduction: 0.133, exp: [exp_074, F081]}
    interpretation: "B sequential grammar 35% stronger than A's"

  position_conditional_rule_for_B:
    description: |
      B bigrams reflect position-aware grammar. Apparent A↔B differences
      may collapse when B is filtered to MID positions only. The
      cross-dialect invariants above ARE position-controlled. Any
      candidate model that ignores this distinction will report spurious
      A/B differences.
    exp: [F076, exp_069, exp_242]

  qok_ch_oscillation_B:
    description: "B sequential alternation pattern"
    pattern: "[p-onset PS] → [o/sh] → [qo↔ch/sh alternation OR d→ch direct] → [closer]"
    transitions:
      - {pair: "sh→qo→ch", B_enr: 3.35}
      - {pair: "qo→ch",    B_enr: 1.31}
      - {pair: "ch→qo",    B_enr: ~baseline}
    after_qo_ch_next_qo: 0.297  # alternation loop
    exp: [F079, F080, exp_072, exp_073]
```

---

## 5. Self-Succession per Onset Class per Dialect

```yaml
self_succession:
  definition: |
    Tendency for consecutive words to share an onset class. Computed as
    enrichment over baseline conditional rate. Canonical methodology:
    per-line edy-rate dialect assignment + MID-baseline formula. The
    archived methodology in exp_174 used folio-level dialect assignment
    + old formula and gives different values; canonical methodology
    SUPERSEDES it.
  exp_canonical: [exp_565, exp_566, exp_567, exp_568, exp_569, exp_573]
  amendment_status: "C007 awaiting human review (state/proposed_c007_amendment.md)"

  canonical_table:
    description: "From exp_573 reconciliation (C007 amendment)"
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

  position_controlled_residuals:
    description: |
      exp_174 position control: enrichment after removing positional
      co-occurrence effects. Holds for CONF classes (y, l, ot, qo, qot
      in both dialects). Does NOT hold for FLAT/DEPL classes
      (B qok 1.03, B ch 0.91, B sh 0.78).
    residual_range: [1.2, 1.8]
    exp: [exp_174]
    qualification: "Per c007 amendment, position-controlled residuals are valid only for CONF classes"

  ss_mean_aggregate:
    VMS_B: 1.465
    role: "Property 2 of dual constraint"
    contradicts_substitution_only: "C002: substitution alone gives ss≈1.0"

  canonical_range:
    description: "Range across class-by-dialect combinations under canonical methodology"
    min: 0.78  # B sh
    max: 3.86  # A l
    note: "ORIGINAL C007 stated 1.24–2.05× — both bounds INCORRECT"
    exp: [exp_573]

  candidate_constraint: |
    Any candidate generator must produce ss CONF for at least the five
    cross-dialect CONF classes (y, l/ol, ot, qo, qot) in BOTH dialects,
    while leaving sh/ch/qok at flat-or-depleted in B.

  copy_buffer_floor:
    description: "Architectural constraint from exp_575 specificity test"
    ss_d_floor:  ~1.50
    ss_y_floor:  ~2.00
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
    LF_gallows_onset_pct: [0.71, 0.80]   # 71–80% of LF tokens are gallows
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
    pos1_distribution_dominant: gallows
    interpretation: "Folio-opener marker register; high information density"
    exp: [exp_343, exp_363]

  register_2_continuation:
    LF_dominant_classes: [d, qok, s, y]
    LL_dominant_classes: [am, l]
    word_count_distribution: standard
    content_grammar: active
    pos1_distribution: "diverse non-gallows openers (s, y, t, d in B)"
    interpretation: "Bulk text register; standard positional grammar applies"
    exp: [F343]

  register_3_folio_closer:
    line_length_words:
      A_mean: 3.94
      B_mean: 4.81
      vs_continuation: 7.8  # ~half length
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
      description: "B has position-2 self-chain rules; A is position-general"
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
      level_3_line:    {form: "y+gallows or d+ch in A", role: within_para_line_opener, pos1_pct: [0.56, 0.86], pos1_PS_pct: 0.00}
      level_2_mid:     {form: "qo+gallows in B, bare ch in A", role: mid_line, LFirst_pct: [0.07, 0.27]}
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
    register_specificity: |
      Para-start grammar STRICTNESS scales with paragraph length. A 10–15
      line paragraphs (herbal): 70.7% PARA, 0% LINE_OPEN — strictest
      grammar. A 2–4 line astro captions: 31% PARA, 8.6% LINE_OPEN
      allowed. The grammar is REGISTER-SPECIFIC.
```

---

## 7. Paragraph Chain Grammar by Section

```yaml
paragraph_chain_grammar:
  description: |
    Cross-line (CL) directed graphs of onset-class transitions. The CL
    network is the strongest evidence for grammar above the line level.
    Critically, CL transitions are DISTINCT from within-line bigrams: a
    CL transition can be CONF while the corresponding within-line bigram
    is NULL or DEPL. Any candidate model must support TWO levels of
    sequential grammar.
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
    description: "t is a CL relay class in A herbal_a, bridging from ch back to d/y/ot"
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
    A: "LINE-CLOSER (LFirst 19.4%, LLast 25.9%); para-final marker"
    B: "LINE-INITIAL CONNECTOR (LFirst 34%, LLast 9.5%); 73.5% daiin[0]→ch/sh"
    exp: [F093, F094]
```

---

## 8. Cross-Dialect Structural Contrasts

```yaml
cross_dialect_contrasts:

  contrast_terminal_layer_inversion:
    A_terminals: [d, cth]
    B_terminals: [r, l, ol, o, a]
    overlap: 0
    interpretation: |
      A closes lines with aiin-body + compound gallows; B closes lines
      with lateral / vowel-initial classes. Zero overlap in terminal
      class identity.
    exp: [exp_555, exp_557, exp_558]
    commitment: C008

  contrast_compound_gallows_frequency_collapse:
    description: "All compound gallows DROP dramatically A→B"
    cth: {A_to_B_factor: 0.116, exp: [exp_558]}     # 8.6× drop
    cph: {A_to_B_factor: 0.205, exp: [exp_610]}     # 4.9× drop
    sch: {presence: A_only_extreme, exp: [exp_561]}
    interpretation: |
      Compound gallows are an A-dialect feature. B retains them only
      vestigially. Any candidate decipherment must explain why these
      forms vanish at the dialect transition.

  contrast_d_onset_positional_reversal:
    A: {role: TERMINAL, LF_enr: 1.53, pos1_enr: 1.47}
    B: {role: OPENER,  LF_enr: 0.36_via_LL_inverse, pos1_enr: 2.64}
    note: "Same onset class with opposite line-position role across dialects"
    exp: [exp_553, exp_555, exp_557]

  contrast_qok_frequency_doubling:
    A_pct: 0.0730
    B_pct: 0.1513
    ratio: 2.07
    driver: "B_astro section grammar contributes most"
    exp: [exp_618]

  contrast_qot_pos1_inversion:
    A: {pos1_enr: 1.40, status: subCONF_opener}
    B: {pos1_enr: 0.69, status: DEPL}
    exp: [exp_631]

  contrast_sh_routing_dialect_specific:
    A: "sh routes to gallows {sh→k, sh→t}"
    B: "sh routes to q-class {sh→qok, sh→qo, sh→qot}"
    exp: [exp_544]

  contrast_paragraph_chain_section_specific:
    A_herbal_a: "d→qot→ch→o→sh full network"
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

  invariant_adj_rate_exact:
    description: "Per F101 / F102: adj_rate is structurally invariant across dialects"
    cross_dialect_facts:
      - "qok dominates adj_rate in B (36.8% of identical pairs from 12.8% of tokens)"
      - "s and t adj_rate = 0 in BOTH dialects (structural anti-repetition)"
      - "sh/ch/d adj_rate ≈ random expectation from CP90 pools cross-dialect"
    commitment: C009
    exp: [exp_577]

  invariants_summary:
    description: "Cross-dialect structural facts that any decipherment must preserve"
    list:
      - "y is LF-depleted (body metric) in BOTH dialects"
      - "y is dominant pos1 in BOTH dialects"
      - "qok and sh are LF-depleted in BOTH dialects"
      - "ch and a are pos1-avoiders in BOTH dialects"
      - "sh→qok / sh→qo / sh→ch DEPL is invariant"
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
      H_pos0_onset: 3.137_bits
      H_pos3_4_middle: [3.606, 3.612]
      H_pos_neg1_final: 2.456_bits
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
    free_layer: "inner core (pos2..pos_n-1)"
    exp: [F042]

  d_onset_daiin_template:
    description: |
      d-onset words are dominated by aiin/al/am/ar suffixes producing
      daiin/dal/dam/dar templates. d+aiin is most templated bigram in
      both dialects.
    A_d_aiin_overrep: 2.69
    B_d_aiin_overrep: 2.16
    exp: [F063, F068, exp_056, exp_061]
    daiin_role: "A's primary grammatical particle; cross-dialect line-position reversal"

  y_onset_y_gallows_compound:
    description: |
      y-onset words are predominantly y+gallows compounds. y is the
      LINE-OPENER prefix that demotes a gallows to within-line use.
    y_plus_kt_LFirst_enrichment: 3.75
    y_plus_kt_pct_LFirst_in_B: 0.473
    three_level_kt_paradigm:
      bare:    {LFirst_pct: 0.089}
      qo_pref: {LFirst_pct: 0.116}
      y_pref:  {LFirst_pct: 0.362}
    exp: [F095, F096, exp_322]

  qo_prefix_morpheme:
    description: |
      qo- is a Currier B morphological prefix selecting k/t-initial stems.
    qo_stem_onset_dist: {k: 0.605, t: 0.212}
    qo_stem_onset_for_o_labels: {k_t: 0.665}
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
    e_infix_universal:
      description: "e-vowel after onset class predicts higher qo-following rate in both dialects across all 5 tested onset classes"
      exp: [F086, exp_079]

  e_infix_partition_finding:
    description: |
      Despite the e-vowel coupling effect, the e-infix is a VOCABULARY
      PARTITION not a productive morphology. When the same stem appears
      with both e-infix and non-e contexts, suffix distributions are
      IDENTICAL. 70–98% of stems appear exclusively in one or the other.
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
      vocab_clamp_helps_for: [qok, d]  # qok +0.464%, d +0.420%
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
      mechanism: "s and t are line-opening pos1 classes; appearing only at line-firsts means consecutive identical pairs are structurally impossible"
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
      ratio_to_VMS: 0.43  # 2.3× too short
      exp: [working_position section 4.3]

    sh_ch_d_CP90_overproduction:
      ratio_range: [3.2, 4.1]
      note: "clamping breaks adj_rate (per Q007)"
      exp: [working_position section 4.3]

  what_architecture_demonstrates:
    - "A position-aware copy-buffer hybrid CAN produce all 19 measured properties simultaneously"
    - "The dual constraint is achievable by mechanisms with structurally separate positional and sequential components"
    - "VMS B-dialect grammar is consistent with a compact ~21-mechanism / ~15-parameter generative process"
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
      am_ll: 3.66   # bio to pharma
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
    max_am_ll_achievable: 0.57
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
      6.5× LL-enriched while edy (most common B-suffix at 18%) is 0.35×
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

  6_copy_buffer_over_same_onset_words_at_VMS_adj_rate_levels:
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

  7_fixed_filler_adjacent_pair_verbose_cipher:
    description: "Adjacent-pair grouping under fixed-filler verbose cipher"
    paired_h2_VMS: 3.836
    natural_language_max_h2: 3.723  # Hebrew
    exp: [F020, F022]

  8_simple_gallows_grouping_or_crust_stripping:
    description: "Mechanical character grouping schemes for verbose cipher reversal"
    h2_distance_to_natural_language: ">1.0 bits"
    exp: [X003, X005]

  not_ruled_out_summary:
    - "Position-sensitive cipher with INDEPENDENT sequential word-class memory (untested combination)"
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
    title: "Onset-preserving variant reaches lenient viability but above VMS adj_rate"
    summary: "4/36 viable lenient; 0/36 at VMS-level adj_rate"
    supporting_exp: [exp_181]
    narrowed_by: "exp_182 character-level mod achieves 3 combos at adj_rate ≤ 0.009"
    spec_sections: [10.architecture_21mech, 5.copy_buffer_floor]
    status: VALID

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
    title: "Onset self-succession ranges from 1.24× to 2.05× and survives position control"
    status: REQUIRES_AMENDMENT
    issues:
      - "Range bounds are wrong: canonical methodology gives 0.78–3.86×"
      - "Upper bound 2.05× misattributed: in exp_174 this value is B qo→qo, not A ok→ok"
      - "Residuals ≥1.2× fails for B qok (1.03×), B ch (0.91×), B sh (0.78×)"
    proposed_amendment: state/proposed_c007_amendment.md
    proposed_corrected_range: [0.78, 3.86]
    surviving_core: "Position-controlled self-succession holds for CONF classes (y, l, ot, qo, qot in both dialects)"
    supporting_exp: [exp_164, exp_174]
    reconciling_exp: [exp_565, exp_567, exp_573]
    spec_sections: [5.canonical_table, 5.canonical_range]

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
      A: "sh/ch/d adj_rate consistent with random draws from CP90 pools (sh 1.11×, d 0.70×, ch 1.91×)"
      B: "s/t adj_rate = 0 structural; line-opening positional constraint"
      C: "Baseline 21-mechanism architecture overproduces adj_rate 1.41–1.79× above VMS for sh/ch/d due to copy-buffer + self-succession coupling"
    supporting_exp: [exp_577, exp_578]
    spec_sections: [10.sh_ch_d_three_way_constraint, 5.s_t_zero_adj_rate_anomaly]
    status: VALID

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
    must_NOT_produce:
      - "Position-blind output (would fail C001)"
      - "ss_mean = 1.0× (would fail C002)"
      - "Copy-buffer over same-onset words at VMS adj_rate levels (would fail C009 part C)"
      - "Uniform B-dialect (would fail exp_579 / C008 scope)"
      - "Onset-replacing modification destroying ss (would fail C003)"
```

---

## 14. Open Issues for Human Review

```yaml
open_issues:
  flagged_during_consolidation: 2026-04-12
  audience: human researcher reviewing this spec before v1.0

  conflicts_in_findings:

    issue_1_C007_self_succession:
      severity: HIGH
      description: |
        C007 in committed_claims.md states "1.24–2.05× across six
        class-by-dialect combinations" and "residuals ≥1.2× across all
        tested onset-by-dialect combinations." Both statements are
        WRONG under canonical methodology. exp_573 reconciliation gives
        canonical range 0.78–3.86×, with B qok=1.03 (FLAT), B ch=0.91,
        B sh=0.78 falling below the 1.2× residual threshold.
      proposed_amendment: state/proposed_c007_amendment.md
      action_required: Human approval of revised C007 text
      spec_handling: |
        Section 5 uses CANONICAL values per amendment. This may diverge
        from any public output that cited the original C007 range. Any
        such public output needs an erratum.

    issue_2_qok_pos1_value:
      severity: MEDIUM
      description: |
        working_position.md Section 6.2 lists A qok pos1 = 1.47×/145
        (presented as enrichment). F619 (canonical methodology) gives
        A qok pos1 = 0.87×/145 sub-baseline. The two are incompatible.
        The spec uses the canonical F619 value.
      action_required: Update working_position.md to match F619 OR confirm methodology divergence
      spec_handling: Section 1.5 uses 0.87×

    issue_3_qot_A_pos1:
      severity: LOW
      description: |
        F539 reported A qot pos1 = 1.79×/59 CONF. F631 corrects to
        1.40×/73 sub-CONF under canonical methodology. The spec uses F631.
      action_required: confirm
      spec_handling: Section 1.6 uses 1.40×/73 sub-CONF

    issue_4_y_LF_simultaneous_DEPL_and_CONF:
      severity: MEDIUM
      description: |
        y-onset is simultaneously listed as "definitive LINE-OPENER pos1
        CONF" AND "LF AVOIDER" in working_position.md Section 6. The
        spec interprets this as two distinct metric definitions: pos1 =
        first content word at line index 0; LF = body word occurring
        at line-first regardless of line opening status. Confirm the
        distinction is intentional and not a synthesis bug.
      action_required: clarify pos1 vs LF metric definitions
      spec_handling: Section 1.2 documents both with note

    issue_5_ot_pos1_discrepancy:
      severity: LOW
      description: |
        F628 corrects prior A ot pos1 from 1.29× to 0.77× sub-baseline.
        Spec uses corrected value.

    issue_6_ok_self_succession_C007_conflict:
      severity: LOW
      description: |
        F626 notes "ok self-succession A=1.42× conflicts with C007 (see
        Q013)." Q013 marked RESOLVED in working_position 8.3 but the
        canonical 1.42× is sub-CONF (below the 1.50× CONF threshold)
        while the original C007 listed it as CONF. Resolved by adopting
        C007 amendment.

  claims_not_tracing_cleanly:

    issue_7_C005_narrowing_scope:
      severity: LOW
      description: |
        C005 narrowing notes that -am enrichment is driven by WP-LL not
        PF-LL. However, the headline 6.811× is the POOLED value. Any
        candidate test should distinguish whether the candidate is being
        evaluated against WP-LL (6.69×, n=2295) or PF-LL (3.14×, n=94).
        Confirm which is the canonical contradiction-condition target.
      action_required: clarify in C005 contradiction condition

    issue_8_19_metric_battery_full_list:
      severity: LOW
      description: |
        The 19-metric battery is referenced in C008 but the canonical
        ordered list is not in committed_claims.md. The spec
        reconstructs it from exp_575 corpus metrics table. Confirm the
        list is correct and authoritative.
      spec_handling: Section 10.battery_performance_19_metrics lists 19 metrics

    issue_9_C004_narrowing_extent:
      severity: LOW
      description: |
        C004 narrowing cites exp_182 (Timm character-level modification
        achieves 3 combos at adj_rate ≤ 0.009). The spec does not
        independently catalog these combinations. Confirm whether the
        narrowing is to be interpreted as "C004 fully superseded" or
        "C004 holds for suffix-replacing variant only."

  potentially_missing_categories:

    issue_10_label_corpus_grammar:
      severity: MEDIUM
      description: |
        The label corpus (Lf/Ls/Ln/Lt/Lc/Lz, 732 entries, F038/F039)
        has its own structural rules: TTR near 1.0, H2 gradient, o-onset
        dominant, no qo-/ch- onset words. The spec does not catalog
        these as a register because they sit outside the line grammar.
        For decipherment work using anchor pairs (Botanist phase output),
        the label grammar will need its own section.
      recommendation: Add Section 15 "Label register grammar" in v1.0

    issue_11_anomalous_folios:
      severity: LOW
      description: |
        f49v, f57v, f66r, f75v, f76r have anomalous structures (key-like
        sequences, line-marker sequences, foreign glyphs). They are
        probably not part of the running text grammar. The spec does
        not exclude them. Confirm whether they should be excluded from
        constraint checks.
      exp: [F026, F030, F032, F033]

    issue_12_two_register_herbal_A:
      severity: MEDIUM
      description: |
        Herbal A has two registers (y-dominant vs aiin-dominant) with
        different sequential grammar (y-dom uses sh→qo coupling;
        aiin-dom uses qo→ch and s→ch). The spec captures the A network
        as one entity but the within-A register split is structurally
        important for paragraph chain validation.
      exp: [F050, F082, F085]
      recommendation: Expand Section 7.A_herbal_a_network to two sub-networks

    issue_13_section_specific_paragraph_lengths:
      severity: LOW
      description: |
        F108: paragraph lengths vary by section (stars B = 47 lines,
        cosmo B = 25, herbal = 12–13, pharma A = 7.7, astro A = 3.4).
        Grammar STRICTNESS scales with paragraph length. The spec does
        not encode this register-specificity. Recommended for v1.0.

    issue_14_pharma_A_grammar_dissociation:
      severity: MEDIUM
      description: |
        Pharma A has B-strength sh→qo coupling (2.44×) but pure A
        morphology. The spec lists this only in passing (Section 1.10).
        The grammar/morphology dissociation is a load-bearing finding
        for theory discrimination — it shows sequential grammar and
        morphological paradigm vary independently. Recommended for
        elevation in v1.0.
      exp: [F082, F083, exp_075, exp_076]

  findings_stronger_or_weaker_than_synthesis:

    issue_15_architecture_specificity_strength:
      severity: LOW
      description: |
        exp_575 result.md (lines 142–175) qualifies the C008 specificity
        claim more strongly than C008's text reflects. Per exp_575: "the
        architecture's specificity is driven by the fixed-constant
        mechanisms (copy buffer, stutter), not by the 6 calibrated
        parameters." The spec includes this caveat in Section 10. C008
        as written presents the specificity as harder than this caveat
        suggests.

    issue_16_t_pos1_A_value:
      severity: LOW
      description: |
        A t pos1 = 2.27×/111 (CONF) per exp_549. A stars t pos1 = 3.67×/16
        per exp_523. These are different sub-corpora (full A vs A stars
        section), not in conflict. Spec preserves both. No action.

    issue_17_compound_gallows_routing_universality:
      severity: LOW
      description: |
        F611 / exp_561 reports "ALL 4 compound gallows route to d within
        A lines." The cph→d evidence is dir at obs=7. sch→d at obs=6.
        These are weaker than CONF. Spec marks the universality with
        weaker confidence than the synthesis presents. Confirm the
        universality claim.

  next_consolidation_pass_recommendations:
    primary_focus: |
      Resolve C007 amendment FIRST. Until C007 is settled, Section 5
      cannot be marked as canonical. Then add: (1) full label register
      grammar as Section 15, (2) Herbal A two-register split inside
      Section 7, (3) section-specific paragraph length / register
      specificity rules, (4) explicit constraint test predicates (e.g.,
      Python-style functions a pipeline can call).
    secondary_focus: |
      Verify spec values against findings.md by running an automated
      cross-check: every value in this spec should grep to a finding ID.
    tertiary_focus: |
      Catalog the F600+ findings (F610–F639) into the spec sections
      where they fit. Many late-phase characterization findings are
      summarized only briefly here and deserve expansion.
```

---

```yaml
end_of_spec:
  version: v0.1
  date: 2026-04-12
  next_version_targets: [resolve C007, add label grammar, expand Herbal A two-register, encode paragraph-length register]
  reviewed_by: pending_human
```
