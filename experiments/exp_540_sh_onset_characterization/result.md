# exp_540 result — sh-onset full characterization (H_new_FD)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: Standard corpus parsing. ONSET_PRIORITY places sh (priority 8) after qok/qot/qo/cth/ckh/cph/ch — correctly partitioning sh from those classes.

**Extrapolation**: None. Claims within tested corpus scope.

---

## Part 1: sh Vocabulary

### A herbal_a: 366 tokens, 102 types
Top words: sho(17.5%), shol(14.5%), shor(7.9%), shy(7.4%), shey(3.8%), sheey(3.3%), shody(2.7%), shaiin(1.9%), shodaiin(1.6%), sheor(1.6%).

**A vocabulary**: o-body dominant: sho+shol+shor = ~40%. y-body: shy+shey+sheey = ~14.5%. aiin-body: shaiin(1.9%). ch-mediated: minor. A sh is dominated by o-suffix forms — completely different from template class vocabulary.

### B all: 1283 tokens, 224 types
Top words: shedy(21.0%), shey(10.1%), sheey(5.5%), sheedy(4.2%), shckhy(3.6%), sheol(3.4%), shol(2.9%), sheckhy(2.0%), shdy(1.9%), shy(1.9%).

**B vocabulary**: edy-body: shedy+sheedy = 25.2% — dominant. y/eey-body: shey+sheey+shy = ~17.5%. ckhy compounds: shckhy+sheckhy = 5.6% (bio/cosmo-specific, F352). B sh is edy-dominated, similar to template classes in B, but with stronger edy proportion.

### A/B sh vocabulary contrast:
| Body class | A sh | B sh |
|-----------|------|------|
| o-body | ~40% (sho/shol/shor) | ~4% (shol only) |
| edy/eedy | ~3% | **25.2%** |
| y/eey | ~14.5% | ~17.5% |
| aiin | ~2% | ~1% |

A sh is o-body dominated; B sh is edy-body dominated. Complete vocabulary inversion paralleling dialect-level A=o-body / B=edy-body shift.

---

## Part 2: sh Positional Distribution

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 80/928 | 8.6% | 1.03× | 119/1903 | 6.3% | **0.70×** |
| MID | 245/2481 | 9.9% | 1.18× | 1083/10610 | 10.2% | 1.15× |
| LL | 75/829 | 9.0% | 1.08× | 150/1846 | 8.1% | 0.91× |
| LF | 41/966 | 4.2% | **0.51×** | 81/1930 | 4.2% | **0.47×** |

Baselines: A=8.37%, B=8.88%.

**Cross-dialectal pattern**: sh is LF-STRONGLY-DEPLETED in BOTH dialects (A: 0.51×; B: 0.47×). sh avoids line-final position universally. MID is slightly elevated in both (A: 1.18×; B: 1.15×). A sh is pos1-neutral (1.03×); B sh is pos1-DEPLETED (0.70×/obs=119 — strong exclusion from line opening in B).

**Template class comparison (F539)**: Template classes have pos1 ranging from 1.79× (qot CONF) to 1.10× (ok neutral). sh at 1.03×(A)/0.70×(B) is BELOW all template classes at pos1. sh is a MID-biased class, not a line opener.

---

## Part 3: sh Within-Line Bigrams

### A herbal_a (325 sh sender bigrams):
| sh→X | obs | E | flag |
|------|-----|---|------|
| sh→sh | 41 | 1.52× | **CONF** |
| sh→k | 31 | 1.75× | **CONF** |
| sh→t | 13 | 1.62× | **CONF** |
| sh→ch | 62 | 0.73× | DEPL |
| sh→d | 38 | 0.67× | DEPL |

**A: THREE CONF signals.** sh→sh self-succession CONF (1.52×). sh→k CONF (1.75×/obs=31). sh→t CONF (1.62×/obs=13). sh→ch DEPLETED (0.73×, from ch↔sh avoidance F328). sh→d DEPLETED (0.67×). A sh routes specifically to gallows-type classes (k, t) and self-succeeds.

### B all (1202 sh sender bigrams):
| sh→X | obs | E | flag |
|------|-----|---|------|
| sh→qok | 331 | 2.02× | **CONF** |
| sh→qo | 68 | 1.92× | **CONF** |
| sh→qot | 78 | 1.74× | **CONF** |
| sh→ch | 132 | 0.59× | DEPL |
| sh→sh | 106 | 0.95× | sub-CONF |
| sh→ot | 75 | 0.87× | DEPL |

**B: THREE CONF signals — all q-class.** sh→qok CONF (2.02×/obs=331, re-confirms F372). sh→qo CONF (1.92×/obs=68, NEW). sh→qot CONF (1.74×/obs=78, NEW). sh routes to the ENTIRE qo-prefix family in B. sh→ch DEPLETED (0.59×, F328 confirmed). sh→sh sub-CONF (0.95×) — B sh does NOT self-succeed (contrast A where sh→sh CONF).

### A/B sh bigram INVERSION:
| Target | A E×(obs) | B E×(obs) |
|--------|-----------|-----------|
| sh→qok | 0.86× (14) DEPL | **2.02× (331) CONF** |
| sh→qot | not elevated | **1.74× (78) CONF** |
| sh→qo | not elevated | **1.92× (68) CONF** |
| sh→k | **1.75× (31) CONF** | not elevated |
| sh→t | **1.62× (13) CONF** | not elevated |
| sh→sh | **1.52× (41) CONF** | 0.95× sub-CONF |
| sh→ch | 0.73× DEPL | 0.59× DEPL |

**Complete A/B bigram inversion**: A sh routes to {self, k, t} (gallows cluster); B sh routes to {qok, qo, qot} (q-prefix template cluster). The routing targets are COMPLETELY DIFFERENT between dialects. The ONLY cross-dialectal conserved feature is sh→ch DEPLETION.

---

## Part 4: sh-LF Lines

### A herbal_a sh-LF (38 lines, 3.9%):
No CONF signals. Best: sh-self at pos1 (E=1.83×/obs=6), ok (E=1.84×/obs=4), qot (E=1.48×/obs=4) — all below CONF (need obs≥10 with E≥1.5×). A sh-LF has flat pos1 grammar.

### B all sh-LF (80 lines, 4.1%):
- **sh: E=2.00×/obs=10 → CONF** — B sh-terminal lines open with sh!
- y: E=0.55×/obs=6 — DEPLETED
- qok: E=0.64×/obs=6 — DEPLETED

**B sh-LF pos1=sh CONF** (E=2.00×/obs=10): B lines ending in sh tend to START with sh. This creates a sh-bracket in B: sh[pos1]→...→sh[LF]. Combined with B sh→sh being sub-CONF within-line, the bracket operates at the LINE LEVEL (not word-to-word level). B sh-LF lines also avoid y and qok at pos1.

---

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: sh priority in ONSET_PRIORITY is 8, correctly below qok/qot/qo/cth/ckh/cph/ch and above ok/ot. Standard.

**Extrapolation**: None.

**Negative-result scope**: N/A — positive results throughout.

**Control behavior**: Within-corpus baselines used.

---

## Summary: sh Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Vocabulary | o-body dominant (sho+shol+shor ~40%) | edy-body dominant (shedy+sheedy 25.2%) |
| Positional role | MID-biased (1.18×); LF DEPL (0.51×) | MID-biased (1.15×); pos1 DEPL (0.70×); LF DEPL (0.47×) |
| Within-line self-succession | **CONF (1.52×/obs=41)** | sub-CONF (0.95×/obs=106) |
| Key within-line targets | **k CONF (1.75×), t CONF (1.62×)** | **qok CONF (2.02×), qo CONF (1.92×), qot CONF (1.74×)** |
| sh→ch | DEPLETED (0.73×) | DEPLETED (0.59×) |
| sh-LF pos1 | flat | **sh self-bracket CONF (2.00×/obs=10)** |

**A/B sh INVERSION (F546)**: The most striking finding is a complete A/B routing inversion. A sh routes to gallows (k, t) and self-succeeds. B sh routes to q-class template words (qok, qo, qot) and does NOT self-succeed. The only conserved cross-dialectal feature is sh→ch depletion. sh is a dialect-specific "router" class that connects fundamentally different word clusters in A vs B.

**sh in template class context**: Unlike template classes (qot/qok/ot/ok with E≥1.10× at pos1), sh is pos1-neutral (A: 1.03×) or pos1-DEPLETED (B: 0.70×). sh is clearly a MID class, not a line-opener. sh LF-depletion (both dialects: ~0.50×) is similar to template class qok (also LF-depleted cross-dialectally, 0.57/0.58×).

**New findings: F544, F545, F546**
**H_new_FD CLOSED.**
