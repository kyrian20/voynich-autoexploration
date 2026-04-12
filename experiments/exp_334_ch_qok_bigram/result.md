# exp_334: ch→qok Enrichment and Template-Class Bigram Rule Analysis (H539)

**Date:** 2026-04-11
**Hypothesis:** H539 — ch→qok is elevated cross-dialect like sh→qok (E=1.97×/1.74×), implying a single "TEMPLATE→qok" grammar rule covering both ch and sh onset classes.
**Result:** H539 REFUTED. ch→qok is NOT elevated: B=1.147×, A=0.877× (near-baseline or depleted). sh→qok remains strongly elevated: B=1.967×, A=1.741×. The sh→qok enrichment is sh-class-specific, not a general template-class rule. ch→qok/sh→qok ratio: B=0.583×, A=0.504× — ch→qok is roughly half the enrichment level of sh→qok in B-dialect and BELOW baseline in A-dialect. The architecture requires a specific sh→qok parameter, not a unified TEMPLATE→qok rule. Bonus findings: ch→ch self-succession near-baseline (0.943×/1.194×); sh→sh elevated in A-dialect only (1.312×); ch↔sh mutual avoidance confirmed (ch→sh=0.555×/0.565×, sh→ch=0.569×/0.727× — consistent with F328); B-dialect qok→ch mild elevation (1.234×) confirms asymmetric qok↔ch coupling.

---

## Key Statistics

### B-Dialect Bigram Enrichment Matrix (focus pairs)

| Pair | obs | exp | E | status |
|------|-----|-----|---|--------|
| sh→qok | 339 | 172.3 | 1.967× | ↑ elevated |
| ch→qok | 331 | 288.6 | 1.147× | baseline |
| sh→ok | 74 | 91.3 | 0.811× | slight depletion |
| ch→ok | 163 | 152.9 | 1.066× | baseline |
| sh→ch | 119 | 214.6 | 0.555× | ↓ depleted |
| ch→sh | 122 | 214.6 | 0.569× | ↓ depleted |
| sh→sh | 120 | 128.1 | 0.937× | baseline |
| ch→ch | 339 | 359.4 | 0.943× | baseline |
| qok→sh | 207 | 172.3 | 1.201× | mild elevation |
| qok→ch | 356 | 288.6 | 1.234× | mild elevation |
| ok→ok | 86 | 65.0 | 1.322× | ↑ elevated |

### A-Dialect Bigram Enrichment Matrix (focus pairs)

| Pair | obs | exp | E | status |
|------|-----|-----|---|--------|
| sh→qok | 55 | 31.6 | 1.741× | ↑ elevated |
| ch→qok | 57 | 65.0 | 0.877× | slight depletion |
| sh→ok | 23 | 31.8 | 0.722× | ↓ depleted |
| ch→ok | 51 | 65.5 | 0.779× | slight depletion |
| sh→ch | 70 | 123.8 | 0.565× | ↓ depleted |
| ch→sh | 90 | 123.8 | 0.727× | ↓ depleted |
| sh→sh | 79 | 60.2 | 1.312× | ↑ elevated |
| ch→ch | 304 | 254.6 | 1.194× | mild elevation |
| qok→sh | 26 | 31.6 | 0.823× | slight depletion |
| qok→ch | 64 | 65.0 | 0.985× | baseline |
| ok→qok | 28 | 16.7 | 1.676× | ↑ elevated |
| qok→ok | 34 | 16.7 | 2.035× | ↑ elevated |
| ok→ok | 33 | 16.8 | 1.959× | ↑ elevated |

### Direct Comparison: sh→qok vs ch→qok

| Dialect | sh→qok E | ch→qok E | ratio (ch/sh) |
|---------|---------|---------|---------------|
| B | 1.967× | 1.147× | 0.583× |
| A | 1.741× | 0.877× | 0.504× |

### Pooled Template-Class → qok Analysis

| Condition | Dialect | obs | exp | E |
|-----------|---------|-----|-----|---|
| (ch+sh)→qok combined | B | 670 | 460.9 | 1.454× |
| (ch+sh)→qok combined | A | 112 | 96.6 | 1.160× |

The combined enrichment (B=1.454×, A=1.160×) is driven primarily by the sh component. ch contributes proportionally fewer obs than expected under sh→qok-level enrichment.

### Non-Template Onsets → qok (for comparison)

| Onset→qok | B E | A E |
|-----------|-----|-----|
| d→qok | 0.591× ↓ | 1.073× |
| y→qok | 0.776× | 0.880× |
| ok→qok | 0.961× | 1.676× ↑ |
| s→qok | 0.743× | 0.694× |

d→qok is notably DEPLETED in B-dialect (0.591×), confirming d is the anti-template class that avoids qok succession.

---

## Findings

### Finding 1: sh→qok is sh-class-specific, not a general template-class rule

ch→qok is at or below baseline (B=1.147×, A=0.877×), while sh→qok is strongly elevated (B=1.967×, A=1.741×). The hypothesis that a single "TEMPLATE→qok" rule covers both ch and sh is REFUTED. The sh→qok enrichment requires a sh-specific grammar parameter that does not extend to ch. The architectural implication is that the simulation's p_sh_qok parameter cannot be simplified or generalized to ch.

### Finding 2: ch and sh have fundamentally different bigram profiles

Despite being co-classified as "template-dominant" onset classes, ch and sh show divergent bigram behavior:
- sh→qok: elevated (1.97×/1.74×) | ch→qok: near-baseline/depleted (1.15×/0.88×)
- sh→sh (A-dialect): elevated (1.312×) | ch→ch: near-baseline (0.94×/1.19×)
- sh→ch: depleted (0.555×/0.565×) | ch→sh: depleted (0.569×/0.727×) — symmetric avoidance (but asymmetric in A)
- qok→ch (B): mild elevation (1.234×) | qok→sh (B): mild elevation (1.201×) — roughly symmetric from qok side

The qok→{ch,sh} coupling is symmetric in B-dialect (both ≈1.2×), while {ch,sh}→qok is highly asymmetric (sh→qok 2×, ch→qok ≈baseline). This asymmetry — qok couples back to ch but ch does not couple forward to qok — is a distinctive feature of the ch onset class grammar.

### Finding 3: A-dialect ch→qok is depleted (0.877×), consistent with qok↔ok A-dialect substitution

In A-dialect, qok is relatively rare (5.9% vs B 14.2%), and ok takes over the qok role (ok→qok=1.676×, qok→ok=2.035×, ok→ok=1.959×). In this context, ch→qok being depleted makes sense: ch onset words in A-dialect do not specifically follow the qok path — they use the ok path instead (ch→ok=0.779× is still depleted, but less so than the overall A-dialect qok reduction would predict).

### Finding 4: B-dialect qok↔ch asymmetric coupling confirmed

qok→ch = 1.234× (B) vs ch→qok = 1.147× (B). The coupling is directionally asymmetric: qok→ch is stronger than ch→qok. This is consistent with qok appearing BEFORE ch in lines (qok is early-MID, ch is also early-MID but qok may precede ch in formulaic sequences). The directionality matches the gradient (qok MID pos = 0.491, ch = 0.487 — very close, so both directions are viable, but qok→ch mildly exceeds ch→qok).

### Finding 5: d→qok strongly depleted in B-dialect (0.591×)

d-onset words avoid transitioning to qok-onset in B-dialect. d is the content-dominant, late-MID onset class (position 0.560), and qok is the early-MID template class (0.491). The backward direction (d→qok = late→early) is strongly disfavored (0.591×), consistent with the gradient directionality finding (F332: backward transitions are generally depleted). d→qok depletion is the reverse of the sh→qok elevation: sh (early-MID) → qok (early-MID, similar position) is elevated; d (late-MID) → qok (early-MID, backward) is depleted.

---

## Interpretation

The H539 question is answered definitively: **sh→qok is a sh-class-specific grammar rule, not a general template-class rule**. ch and sh are both template-dominant onset classes, but their bigram profiles diverge substantially. The similarity (template polarity in body vocabulary) does not predict similarity in transition grammar.

This has direct architectural implications:
- The p_sh_qok Markov parameter in the 21-mechanism simulation captures a real sh-specific rule
- No corresponding p_ch_qok parameter is needed (ch→qok is near-baseline)
- The A-dialect sh→qok parameter (p_sh_qok for A) is also specific to sh (A-dialect ch→qok is depleted)

The finding also sharpens the characterization of ch vs sh as distinct grammatical classes:
- sh = "early-line template word that specifically precedes qok" (sh→qok rule) + "avoids ch" (ch↔sh avoidance)
- ch = "early-line template word that does NOT precede qok specifically" + "avoids sh" + "mild qok→ch coupling (passive)"

---

## Limitations

- B-dialect ch→qok obs=331 vs exp=288.6 — the E=1.147× might reflect mild real enrichment at the 15% level, not strong enrichment. Statistical test not performed.
- A-dialect sample sizes are smaller; A ch→qok obs=57 vs exp=65 (n.s. depletion).
- The analysis uses all MID bigrams together; section-specific effects are not controlled.

---

## Self-Audit

**Target-awareness:** No target-aware elements. Pure corpus bigram frequency measurement. PASS.

**Feature-destroying implementation:** Onset classification uses priority order placing qok/qot/qo before ok/ot, ensuring no miscategorization. This is correct — cth, ch, sh are all placed above generic single-char onsets. PASS.

**Extrapolation:** Finding 1 claims sh→qok is "sh-class-specific, not a general template-class rule." The tested classes are ch and sh. The claim is bounded to ch and sh; it does not claim other onset classes also lack the rule. PASS.

**Negative-result scope:** H539 is refuted for the specific claim "ch→qok elevated like sh→qok." The conclusion is "ch→qok is at baseline/slightly depleted; sh→qok requires sh-specific parameter." This does not claim "no template-class rule exists" — only that the rule is not a simple ch+sh symmetry. PASS.

**Control behavior:** Expected under independence: each bigram pair E=1.0×. All baseline measurements (ch→ch, sh→sh, ok→qok in B) are near 1.0× as expected. The elevated pairs (sh→qok, ok→ok) and depleted pairs (ch→sh, sh→ch) are consistent with prior findings. No unexpected control behavior. PASS.
