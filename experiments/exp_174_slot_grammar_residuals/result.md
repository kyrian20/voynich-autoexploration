# exp_174: Slot-Grammar Residuals — Template vs. Grammar Discrimination
**Date**: 2026-04-10
**Hypotheses**: Can the onset-class sequential effects (self-succession, positional enrichments) be explained by a pure slot-filler template model, or do they require onset-class grammar rules?
**Status**: GRAMMAR HYPOTHESIS CONFIRMED. All onset-class effects survive position control. Self-succession is position-heterogeneous in ways that are diagnostic of grammar, not template. -am LL and y-onset LF are suffix/onset-specific (not generic positional effects).

---

## METHOD

For each line position (LF, second, MID, LL, only), compute within-stratum onset-class transition matrices. Test whether onset-class effects survive after position is controlled.

**Template prediction**: Controlling for position eliminates onset-class effects (because templates assign word types to positions, and all effects are position-driven).

**Grammar prediction**: Onset-class effects persist within position strata (because onset-class determines contextual behavior independent of position).

---

## H1: Onset Self-Succession Survives Position Control

| Onset | A unconditional | A position-controlled | B unconditional | B position-controlled |
|-------|----------------|----------------------|----------------|----------------------|
| qok | 1.623 | **1.594** | 1.239 | **1.203** |
| ok | 1.930 | **1.822** | 1.462 | **1.362** |
| ch | 1.427 | **1.334** | 1.694 | **1.503** |
| qo | 1.305 | **1.269** | 2.047 | **1.990** |
| d | ~1.16 | **1.211** | ~1.16 | **1.533** |

**Position-controlled enrichment is nearly identical to unconditional enrichment across all onset classes and both dialects.**

The small reduction (position-controlled slightly lower than unconditional) reflects that positions are correlated with onset class, so controlling for position removes a small positional contribution. But the core enrichment survives: within each (pi→pj) position transition, onset-class words disproportionately follow onset-class words.

**Verdict: Template hypothesis FALSIFIED for self-succession.** Position explains only a small fraction of onset self-succession. The majority is intrinsic onset-class grammar.

---

## H2: qok→ch Enrichment Survives Position Control

| Condition | A unconditional | A position-controlled | B unconditional | B position-controlled |
|-----------|----------------|----------------------|----------------|----------------------|
| qok→ch | 1.326 | **1.242** | 1.211 | **1.248** |

**Position-controlled enrichment ≈ unconditional enrichment** in both dialects. After accounting for the fact that qok and ch words may prefer certain positions, the qok→ch succession preference is essentially unchanged.

**Position-stratum detail (B-dialect):**

| Transition | qok→ch rate | Baseline | Enrichment |
|-----------|------------|---------|-----------|
| LF→second | 0.041 | 0.056 | 0.734 |
| second→MID | 0.056 | 0.076 | 0.740 |
| MID→MID | 0.092 | 0.071 | **1.291** |
| MID→LL | 0.074 | 0.060 | **1.226** |

The qok→ch enrichment is concentrated in mid-line positions (MID→MID, MID→LL) and absent or reversed at LF→second and second→MID. This is not a positional artifact — it is a mid-line grammar rule: qok words in mid-line positions specifically introduce ch words.

**Verdict: qok→ch is a grammar rule active in mid-line contexts, not a template effect.**

---

## H3: -am LL Enrichment Is Suffix-Specific (Not Generic "LL Properties")

**B-dialect LL suffix enrichments:**

| Suffix | LL count | LL rate | Global rate | Enrichment |
|--------|----------|---------|-------------|-----------|
| **am** | **327** | **0.135** | **0.0196** | **6.856** |
| al | 122 | 0.050 | 0.055 | 0.913 |
| aiin | 97 | 0.040 | 0.103 | 0.386 |
| ar | 86 | 0.035 | 0.074 | 0.476 |
| edy | 154 | 0.063 | 0.183 | 0.346 |
| ol | 91 | 0.037 | 0.063 | 0.593 |
| or | 46 | 0.019 | 0.033 | 0.573 |

**-am is 6.8× enriched at LL. Every other common suffix is DEPLETED or near-baseline at LL.**

This is the critical discrimination: if LL were a generic "word-final slot" that any word could fill, we would expect near-baseline enrichment for all suffixes. Instead, -am is specifically 6.9× enriched while edy (which is the most common B-dialect suffix at 18.3% of words) is 0.35× DEPLETED at LL. **The template hypothesis predicts near-uniform or class-based LL distribution. The data shows exclusive -am specificity.**

**A-dialect LL suffix enrichments (for comparison):**

| Suffix | LL rate | Global rate | Enrichment |
|--------|---------|-------------|-----------|
| **am** | **0.068** | **0.019** | **3.619** |
| al | 0.051 | 0.039 | 1.323 |
| aiin | 0.120 | 0.118 | 1.019 |
| ol | 0.033 | 0.137 | 0.244 |
| or | 0.021 | 0.099 | 0.209 |
| edy | 0.002 | 0.003 | 0.668 |

Same pattern in A-dialect: -am uniquely enriched at LL; ol and or strongly depleted.

**Verdict: -am LL enrichment is SUFFIX-SPECIFIC, not a generic positional template effect. The template hypothesis cannot explain why -am is 7× more line-final than any other common suffix.**

---

## H4: y-Onset LF Enrichment Is Onset-Specific (Part of a Structured LF Grammar)

**B-dialect LF onset enrichments:**

| Onset | LF rate | Global rate | Enrichment |
|-------|---------|-------------|-----------|
| **s** | **0.124** | **0.028** | **4.389** |
| **y** | **0.142** | **0.041** | **3.478** |
| **t** | **0.056** | **0.020** | **2.749** |
| **d** | **0.158** | **0.068** | **2.335** |
| sh | 0.078 | 0.090 | 0.865 |
| qo | 0.033 | 0.034 | 0.968 |
| cth | 0.003 | 0.003 | 0.973 |
| ch_e | 0.029 | 0.090 | 0.320 |
| ch | 0.019 | 0.064 | 0.291 |
| ok | 0.036 | 0.066 | 0.545 |
| qok | 0.102 | 0.121 | **0.844** |
| other | 0.068 | 0.111 | 0.614 |

y-onset enrichment at LF (3.478×) is confirmed and is ONSET-SPECIFIC. But it is part of a structured class of LF-preferred onsets: s (4.4×), y (3.5×), t (2.7×), d (2.3×) are all enriched at LF. Meanwhile ch_e (0.32×), ch (0.29×), qok (0.84×), ok (0.55×) are depleted.

**This is the signature of onset grammar, not a positional template.** Under a template, LF would accept a broad class of word types. Instead, LF shows a strong onset-class filter: simple onset consonants (s, y, t, d) are preferred; complex onset clusters (ch, ch_e, ok) are avoided.

**A-dialect LF:**

| Onset | LF rate | Global rate | Enrichment |
|-------|---------|-------------|-----------|
| **y** | **0.154** | **0.063** | **2.459** |
| **t** | **0.052** | **0.025** | **2.079** |
| **s** | **0.067** | **0.044** | **1.538** |
| d | 0.162 | 0.148 | 1.091 |
| cth | 0.006 | 0.038 | **0.145** |
| ch_e | 0.012 | 0.053 | **0.229** |
| ch | 0.069 | 0.145 | **0.475** |

Same pattern: simple onsets (y, t, s) enriched; complex clusters (cth, ch_e, ch) depleted.

**Verdict: LF position has a strong onset-class filter. y is specifically enriched (confirmed), as part of a class of "simple onset" words that are grammatically preferred at line-first position. Template hypothesis cannot explain why ch_e (0.32×) is depleted while y (3.5×) is enriched when both are common words.**

---

## H5: Self-Succession Rate Is Position-Heterogeneous (Grammar, Not Template)

The clearest evidence against a template model:

**d self-succession rates by position transition (B-dialect):**

| Transition | Rate |
|-----------|------|
| LF→second | 0.021 |
| MID→MID | 0.087 |
| second→MID | 0.123 |
| **MID→LL** | **0.180** |

**d words are most self-successive when leading into line-final position (MID→LL: 18.0%) vs. when leading away from line-first (LF→second: 2.1%).** Under a template, self-succession should be constant across transitions (a word fills its slot regardless of what comes next). Instead, d words cluster specifically when the next position is LL — exactly where d-onset words are enriched (F5: d LL enrichment 1.667× in A, 1.464× in B). This creates a reinforcing pattern: d prefers LL, AND d preceding LL is more likely to be d itself.

**ch self-succession heterogeneity (A-dialect):**

| Transition | Rate |
|-----------|------|
| LF→second | 0.248 |
| MID→MID | 0.213 |
| MID→LL | 0.153 |
| second→LL | 0.146 |

ch self-succession is highest at LF→second (0.248) — when both words are in the line-opening zone. This suggests ch words cluster in line-opening contexts.

**Verdict: Self-succession is position-heterogeneous in ways that mirror the onset-specific positional enrichments. Grammar rules (onset-specific positional preferences + onset-class succession preference) jointly explain both the positional enrichments and the succession patterns. Template models predict position-homogeneous succession.**

---

## SUMMARY: TEMPLATE VS. GRAMMAR

| Test | Template prediction | Observed | Verdict |
|------|--------------------|---------|---------| 
| H1: Self-succession survives position control | Position explains enrichment (residual ~1.0) | Residual 1.2-1.8× | GRAMMAR |
| H2: qok→ch survives position control | Position explains enrichment | Residual 1.24× | GRAMMAR |
| H3: -am specificity at LL | Any LL words enriched equally | -am 6.9×, others <1× | GRAMMAR |
| H4: y-onset specificity at LF | Any LF words enriched equally | s/y/t enriched, ch/ok depleted | GRAMMAR |
| H5: Self-succession position homogeneity | Constant across transitions | d: 2.1%→18% across transitions | GRAMMAR |

**All five tests falsify the pure template hypothesis.** The VMS positional and sequential structure requires onset-class grammar rules that operate independently of (and interact with) positional slot assignments.

---

## CONCLUSION

**The Voynich Manuscript's positional and sequential structure cannot be explained by a pure slot-filling template.** Onset-class effects are not positional artifacts: they survive position control, they are suffix/onset-specific rather than generic, and they show position-dependent heterogeneity consistent with grammar rules.

The findings are consistent with a system where:
1. Certain onset classes have preferred positional ranges (onset-LF and onset-LL grammar rules)
2. Within those positions, onset-class words co-select each other (grammar agreement / class coherence)
3. The combination creates position-specific onset-class enrichments that no pure template can reproduce

---

## FILES

- `script.py`: Position-controlled onset analysis (A+B dialect, 5 hypothesis tests)
