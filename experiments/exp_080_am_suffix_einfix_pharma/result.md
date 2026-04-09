# Experiment exp_080: e-Infix Suffix Co-Occurrence (H120), -am Suffix Class (H121), Pharma A Spectrum (H122)
Date: 2026-04-09

## H120: e-Infix Co-Occurs with e-Extended Suffixes — Complete Syllable Template

### B e-Infix Suffix Co-Occurrence

| Onset | e-form top suffixes | non-e top suffixes |
|-------|-------------------|-------------------|
| **sh** | **-edy (29%), -ey (15%), -eey (8%)** | -dy (16%), -ol (11%), -aiin (6%) |
| **ch** | **-edy (24%), -ey (13%), -eey (7%)** | -dy (16%), -ol (8%), -aiin (7%) |
| **k** | **-edy (19%), -eedy (19%), -eey (11%)** | -aiin (11%), -ain (8%), -dy (14%) |
| **o** | -eedy (15%), -eey (13%), -edy (8%) | -edy (11%), -aiin (11%), -eedy (6%) |

**In Currier B: e-infix → -edy/-eedy/-ey/-eey; non-e-infix → -dy/-aiin.** The split is consistent across sh, ch, k onset classes. The e-infix creates a complete syllable template: `{onset}+e+{stem}+{e-suffix}`.

### A e-Infix Suffix Co-Occurrence

| Onset | e-form top suffixes | non-e top suffixes |
|-------|-------------------|-------------------|
| **sh** | **-ey (20%), -eey (13%), -ol (16%)** | -ol (21%), -aiin (9%), -or (11%) |
| **ch** | **-ey (18%), -eey (8%), -ol (14%)** | -ol (19%), -aiin (8%), -or (13%) |
| **k** | **-eey (20%), -ol (19%), -edy (...)** | -aiin (10%), -ol (15%), -or (12%) |

**In Currier A: e-infix → -ey/-eey; non-e-infix → -aiin/-ol/-or.** The same pattern holds: e-infix words take e-extended suffixes (-ey, -eey); non-e forms take vowel-final suffixes (-aiin, -ol, -or).

### Cross-Dialect Template

| Dialect | e-infix form | e-suffix | Non-e form | Non-e suffix |
|---------|------------|---------|----------|------------|
| **B** | she-/che- | -edy/-ey | sh-/ch- | -dy/-aiin |
| **A** | she-/che- | -ey/-eey | sh-/ch- | -aiin/-ol |

**The Voynich e-infix syllable template: words with e-vowel after onset preferentially take e-extended suffixes in both dialects.** This creates morphological word classes defined by e-infix + e-suffix co-occurrence. In B: shedy, chedy, keedy = {onset}e+{e-suffix}. In A: shey, sheey, chey = {onset}e+{e-suffix}.

### H120 Verdict: STRONGLY SUPPORTED — e-Infix Correlates with e-Extended Suffixes Forming Complete Syllable Templates

In both dialects, e-infix onset forms preferentially take e-extended suffixes (-edy/-eedy/-ey/-eey in B; -ey/-eey in A), while non-e onset forms take non-e suffixes (-dy/-aiin in B; -aiin/-ol in A). The e-infix is not an isolated morphological feature — it co-defines a complete syllable template with the suffix class. B shows a sharper split (e-infix→-edy at 24-29%; non-e→-dy at 16%) than A (e-infix→-ey at 18-20%; non-e→-aiin at 8-9%).

---

## H121: -am Suffix Is a Near-Pure B Within-Para Line-Final Marker (Not Para-Final)

### B -am Positional Statistics

- Total B -am tokens: 430 (202 word types)
- **81.6% line-final** (vs base rate ~11.9% for average B word)
- Only 1.6% line-first
- Top -am words: otam (35), dam (31), qokam (22), okam (20), chdam (10), olkam (10), ram (10)

**-am words are near-pure B line-final markers** — 81.6% of -am word occurrences are at line-ends. This is the strongest positional bias of any suffix class identified.

### Para-Final vs Within-Para Distribution

| Context | -am rate |
|---------|---------|
| **Para-interior line-final** | **14.0%** (342/2437) |
| **Para-final** | **7.7%** (10/130) |

**Paradox: -am words are SUPPRESSED at para-final positions** (7.7%) vs within-para line-finals (14.0%). The B para-closing words (o-onset dominated, 40.0%) do NOT preferentially end in -am. The -am suffix marks **within-paragraph line boundaries**, not paragraph-final boundaries.

### Preceding Context for -am Words

Preceding onset: o (117), ch (80), other (70), qo (62), d (26), sh (24). The predecessors are diverse, but o-onset is the most common — consistent with o-onset being enriched at line-ends generally (B line-final: o=1.25×).

### A -am Comparison

A has 176 -am tokens (58.5% line-final vs B's 81.6%). Top A -am words: dam (32), cham (9), otam (7), okam (6) — the same dominant words as B (dam, otam, okam). dam is cross-dialect and appears at line-ends in both A (62.5%) and B (77.4%).

### H121 Verdict: STRONGLY SUPPORTED — -am Suffix Is B's Within-Para Line-Boundary Marker

-am words are at line-ends 81.6% of the time (vs 11.9% average), making them one of the strongest positional markers in the corpus. However, they are SUPPRESSED at para-final positions (7.7% vs 14.0%). The -am suffix specifically marks within-paragraph line boundaries. The B paragraph structure: para-start (p-onset) → [many lines ending in -am words] → para-final (o-onset word, NOT -am). This creates a tripartite positional grammar: [p-onset PARA-START] → [non-am LINE-MID] → [-am LINE-END] → ... → [o-onset PARA-END].

---

## H122: Pharma A — Sequential Grammar at B Level, Morphology Firmly A

### Multi-Feature Comparison

| Feature | Herbal A | Aiin-dom | Y-dom | **Pharma A** | Currier B |
|---------|---------|---------|-------|------------|---------|
| Bigram PPL reduction | 9.9% | 12.7% | 10.2% | **12.9%** | **13.3%** |
| sh→qo enrichment | 1.27× | 1.10× | 1.29× | **2.44×** | 1.97× |
| she-→qo enrichment | 1.52× | 1.18× | 1.59× | **2.91×** | 2.19× |
| -edy suffix rate | 0.13% | 0.00% | 0.18% | **0.47%** | **18.12%** |
| qo-onset rate | 10.1% | 7.9% | 10.9% | **13.2%** | **18.6%** |
| Jaccard with B | 0.100 | 0.055 | 0.096 | **0.070** | — |
| Top qo-words | qotchy/qokchy | qotchy/qokchy | qotchy/qokchy | **qokeol/qokeey** | **qokeedy/qokain** |
| d-onset line-final | 1.71× | 1.64× | 1.74× | **1.64×** | 1.51× |

**Pharma A's sequential grammar features (bigram PPL reduction: 12.9%, sh→qo: 2.44×, she-→qo: 2.91×) are AT or ABOVE B levels.** But its morphological features (-edy: 0.47%, qo-rate: 13.2%, Jaccard with B: 0.070) remain firmly within the A range.

### The Dissociation Pattern

**Feature by feature:**
1. **Bigram PPL** (grammar strength): Pharma A = B (12.9% vs 13.3%) — sequential grammar as strong as B
2. **sh→qo coupling**: Pharma A EXCEEDS B (2.44× vs 1.97×) — sequential grammar STRONGER than B
3. **she-→qo coupling**: Pharma A EXCEEDS B (2.91× vs 2.19×) — morphological qo-coupling even stronger
4. **-edy suffix**: Pharma A = deep A (0.47% vs A's 0.13-0.18%; B's 18.12%) — morphology firmly A
5. **Vocabulary Jaccard with B**: Pharma A is FARTHER from B than Herbal A (0.070 vs 0.100) — vocabulary firmly A
6. **qo-word types**: Pharma A qo-words resemble B (qokeol, qokeey vs B qokeedy, qokeey) — intermediate

**The Pharma A profile is NOT "intermediate" between A and B** — it has B-level or higher sequential grammar, A-level morphology, and a UNIQUE qo-vocabulary that bridges the gap.

### H122 Verdict: STRONGLY SUPPORTED (DISSOCIATION, NOT INTERPOLATION) — Pharma A Has B-Strength Sequential Grammar with A-Type Morphology

Pharma A represents a genuinely anomalous text in the Voynich corpus: its sequential grammar (bigram PPL, sh→qo, she-→qo) equals or exceeds B's, while its suffix morphology (-edy rate: 0.47% vs B 18%) and vocabulary (Jaccard with B: 0.070) firmly belong to Currier A. This is NOT a transitional text interpolating between A and B — it has a distinctive profile where two independent dimensions of grammar (sequential ordering rules vs. word morphology) appear to operate independently. **Sequential grammar and morphological paradigm are dissociated in Voynichese**, at least in the Pharma A section.

---

## Combined Finding (F087)

**H120 STRONGLY SUPPORTED**: e-infix onset forms co-occur with e-extended suffixes in both dialects: B she-→-edy (29%), A she-→-ey (20%). Non-e forms take non-e suffixes: B sh-→-dy (16%), A sh-→-aiin (9%). The e-infix defines a complete syllable template: {onset}+e+{stem}+{e-suffix}. B's e-paradigm words (shedy, chedy, keedy) = e-infix + -edy; A's e-paradigm words (shey, chey) = e-infix + -ey. **H121 STRONGLY SUPPORTED**: B -am suffix words (81.6% line-final, 202 types) are near-pure within-para line-final markers. SUPPRESSED at para-final (7.7% vs within-para 14.0%). -am marks within-paragraph line-boundaries, not paragraph endings. B positional grammar: p-onset para-start → [-am word line-ends] × N → o-onset para-end. dam is cross-dialect (A: 58.5%, B: 77.4% line-final). **H122 STRONGLY SUPPORTED (DISSOCIATION)**: Pharma A has B-level or higher sequential grammar (bigram PPL: 12.9%≈B's 13.3%; sh→qo: 2.44× > B's 1.97×; she-→qo: 2.91× > B's 2.19×) but A-type morphology (-edy: 0.47% vs B 18%; Jaccard with B: 0.070). Sequential ordering rules and morphological paradigm are independently varying properties in Voynichese.
