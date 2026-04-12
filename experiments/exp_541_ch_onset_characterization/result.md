# exp_541 result — ch-onset full characterization (H_new_FC)

## Audit

**Target-awareness**: None. Standard characterization methodology identical to exp_540 (sh) and exp_534-537 (template classes). No prior prediction about B ch→t CONF.

**Feature-destroying implementation**: ONSET_PRIORITY places ch at priority 7 (after qok/qot/qo/cth/ckh/cph, before sh). Correct. ch onset extraction: `word.startswith('ch')` via ONSET_PRIORITY loop — correct and consistent with prior experiments.

**Extrapolation**: None. Claims within tested corpus scope.

---

## Part 1: ch Vocabulary

### A herbal_a: 2242 tokens, 457 types
Top words: chol(10.8%), chey(6.1%), chor(5.8%), chy(3.3%), cheey(3.3%), cheol(3.3%), cheor(2.4%), chody(2.4%), chckhy(2.3%), cheody(2.2%).

**A vocabulary body classes:**
| Body class | A ch |
|-----------|------|
| y-body | 42.5% (chey, chy, cheey, chody, etc.) |
| al/ol-body | 35.2% (chol, chor, cheol, cheor, char, chear, etc.) |
| aiin-body | 8.9% (chaiin, chodaiin, etc.) |
| o-body | 6.2% (cho, chody counted in y-body by suffix) |
| other | 6.0% |

**A ch vocabulary summary**: y+ol body dominant (~78% combined). NOT ch-mediated (ch is itself, not prefixed to ch). NOT o-body like sh. A ch is functionally a "y-suffix / ol-suffix" class with a ch onset.

### B all: 1695 tokens, 337 types
Top words: chedy(22.2%), chey(6.8%), cheey(3.5%), chckhy(3.5%), chdy(3.0%), cheol(2.9%), cheedy(2.7%), chol(2.5%).

**B vocabulary body classes:**
| Body class | B ch |
|-----------|------|
| y-body | 36.0% |
| edy-body | 28.6% (chedy, cheedy dominant) |
| al/ol-body | 18.6% |
| aiin-body | 7.6% |
| o-body | 2.1% |

**B ch vocabulary summary**: y-body still dominant (36%) but edy-body gains substantially (28.6%). The A→B dialect shift (edy gains) appears in ch vocabulary as expected, but ch retains y-body dominance in BOTH dialects.

### A/B ch vocabulary contrast:
| Body class | A ch | B ch |
|-----------|------|------|
| y-body | **42.5%** | **36.0%** |
| edy-body | ~0% | **28.6%** |
| al/ol-body | 35.2% | 18.6% |
| aiin-body | 8.9% | 7.6% |
| o-body | 6.2% | 2.1% |

**Ch vocabulary cross-dialect**: ch is y-body dominant in BOTH dialects. Unlike template classes (A=ch-mediated/B=edy-dominated, F541) and sh (A=o-body/B=edy-dominated, F544/F545), ch retains y-suffix affinity across dialects. The edy shift in B ch (28.6%) is present but ch remains y-dominant. Ch has a unique vocabulary fingerprint: the y+ol architecture persists dialect-independent.

---

## Part 2: ch Positional Distribution

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 146/1961 | 7.4% | **0.38×** | 53/1279 | 4.1% | **0.25×** |
| MID | 1715/7333 | 23.4% | 1.18× | 1448/7601 | 19.1% | 1.14× |
| LL | 424/1794 | 23.6% | 1.19× | 224/1266 | 17.7% | 1.06× |
| LF | 373/1961 | 19.0% | 0.96× | 194/1279 | 15.2% | 0.91× |

Baselines: A=19.8%, B=16.7%.

**Cross-dialectal pattern**: ch is pos1-STRONGLY-DEPLETED in BOTH dialects (A: 0.38×; B: 0.25×). This is the most severe pos1 depletion observed for any major onset class — stronger than sh (A: 1.03×; B: 0.70×), stronger than all template classes. **ch virtually never opens lines.** MID is elevated in both dialects (A: 1.18×; B: 1.14×), consistent with ch being a MID-dominant class.

**LF: near-baseline** (A: 0.96×; B: 0.91×) — ch is permitted at line-final positions. This contrasts sharply with sh (LF STRONGLY DEPLETED: A: 0.51×; B: 0.47×). Ch does not avoid LF.

**Comparison to sh and template classes at pos1:**
| Class | A pos1 E | B pos1 E |
|-------|----------|----------|
| qot | 1.79× CONF | 0.60× DEPL |
| qok | 1.47× near-CONF | 0.88× |
| ot | 1.29× | 0.34× DEPL |
| ok | 1.10× | 0.49× DEPL |
| **sh** | **1.03× neutral** | **0.70× DEPL** |
| **ch** | **0.38× STRONGLY DEPL** | **0.25× STRONGLY DEPL** |

Ch is the most pos1-excluded major onset class by a large margin. While template classes range from neutral to CONF at pos1 in A, ch is at 0.38×. Even sh (neutral in A at 1.03×) is far above ch.

**LL: slightly elevated** in both dialects (A: 1.19×; B: 1.06×). Ch is enriched at penultimate position in A — a subtle positional affinity not seen for sh.

---

## Part 3: ch Within-line Bigrams (ch→X)

### A herbal_a (1861 ch sender bigrams):
| ch→X | obs | E | flag |
|------|-----|---|------|
| ch→ch | 453 | 1.08× | sub-CONF |
| ch→d | 238 | 1.19× | sub-CONF |
| ch→sh | 117 | **0.75×** | DEPL |
| ch→k | 86 | 1.35× | sub-CONF |
| ch→l | 57 | 1.37× | sub-CONF |
| ch→ot | 77 | 0.81× | DEPL |
| ch→a | 67 | 0.69× | DEPL |
| ch→y | 52 | 0.77× | DEPL |

**A: NO CONF signals.** ch→ch sub-CONF (1.08×/obs=453) — confirms F461/F462 correction that ch self-succession is NOT CONF. ch→sh DEPLETED (0.75×, F328 confirmed). Best elevated signals: ch→k (1.35×) and ch→l (1.37×) — both below CONF. A ch within-line grammar is FLAT: no class strongly recruited or avoided beyond sh.

### B all (1501 ch sender bigrams):
| ch→X | obs | E | flag |
|------|-----|---|------|
| ch→t | 35 | **1.77×** | **CONF** |
| ch→ch | 259 | 0.93× | sub-CONF |
| ch→l | 135 | 1.37× | sub-CONF |
| ch→d | 107 | 1.28× | sub-CONF |
| ch→k | 44 | 1.36× | sub-CONF |
| ch→sh | 86 | **0.58×** | DEPL |
| ch→ot | 101 | 0.91× | DEPL |
| ch→a | 49 | 0.82× | DEPL |
| ch→qot | 81 | 1.23× | sub-CONF |

**B: ONE CONF signal.** ch→t CONF (E=1.77×/obs=35) — NEW. In B, ch recruits t-onset successor words at CONF level. ch→sh DEPLETED (0.58×, F328 confirmed bidirectionally in B). ch→ch sub-CONF (0.93×) — well below CONF. ch→ch is actually near-baseline in B, not even self-successional.

### A/B ch bigram contrast:
| Target | A E×(obs) | B E×(obs) |
|--------|-----------|-----------|
| ch→t | 1.15×(?) | **1.77×(35) CONF** |
| ch→ch | 1.08×(453) sub-CONF | 0.93×(259) sub-CONF |
| ch→sh | 0.75×(117) DEPL | 0.58×(86) DEPL |
| ch→k | 1.35×(86) | 1.36×(44) |
| ch→l | 1.37×(57) | 1.37×(135) |
| ch→d | 1.19×(238) | 1.28×(107) |

**Cross-dialectal conserved**: ch→sh DEPLETED (both: 0.58-0.75×) — F328 confirmed bidirectionally. ch→k and ch→l both show consistent mild elevation (1.35-1.37×) in both dialects — below CONF but structurally consistent. B ch→t CONF is the ONLY confirmed within-line rule for ch, and it is B-specific.

---

## Part 4: ch-LF Lines Pos1 Profile

### A herbal_a ch-LF (373 lines, 19.0%):
**NO CONF signals.** Best: ch-self (E=1.30×/obs=36), ol (E=1.21×/obs=12), d (E=1.15×/obs=76). y DEPLETED (E=0.78×). ok DEPLETED (E=0.70×). A ch-LF pos1 is completely FLAT — no confirmed opener class.

### B all ch-LF (194 lines, 15.2%):
**NO CONF signals.** Best: t (E=1.44×/obs=17), qot (E=1.43×/obs=8), sh (E=1.35×/obs=16), s (E=1.32×/obs=33). d DEPLETED (E=0.78×). B ch-LF pos1 also FLAT.

**Key structural finding**: ch-LF is a MAJOR LF class (A: 19.0%, B: 15.2%) — likely the most common or near-most-common LF class in A herbal_a (competing with d). Yet ch-LF has NO confirmed pos1 opener rules in either dialect. This contrasts with all other characterized LF classes:
- ok-LF: A y CONF (F455), B t CONF (F540)
- ot-LF: A y CONF (F456)
- o-LF: A y dir (F502), B y (dir) (F507)
- d-LF: d→qot chain (F491)

**Ch-LF is the only major LF class with completely flat pos1 grammar in both dialects.**

---

## Self-Audit

**Target-awareness**: None. B ch→t CONF was unexpected.

**Feature-destroying implementation**: Standard. ONSET_PRIORITY correctly places ch above sh; bigram counts iterate over within-line pairs (not cross-line). Body class analysis is approximate (simple suffix matching) — "other" category (6%) may include borderline cases, but major categories are unambiguous.

**Extrapolation**: None.

**Negative-result scope**: A ch within-line: NO CONF signals in 1861 bigrams with obs ranging from 44 to 453 — this is a clean negative (power is sufficient). ch-LF pos1 flat: 373 and 194 lines respectively — sufficient power to detect CONF (need obs=10 at E=1.5×, expected=6.7 baseline). The flat result is genuine.

**Control behavior**: ch→sh depletion independently confirms F328 in both dialects from the ch-sender perspective. ch→ch sub-CONF independently confirms F461/F462 correction. Both are positive methodology controls.

---

## Summary: ch Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Vocabulary | y+ol dominant (77.7%); edy ~0% | y-dominant (36%); edy gains (28.6%) |
| Positional role | **pos1 STRONGLY DEPL (0.38×)**; MID elevated (1.18×); LF near-baseline (0.96×) | **pos1 EXTREMELY DEPL (0.25×)**; MID elevated (1.14×); LF near-baseline (0.91×) |
| Within-line self-succession | sub-CONF (1.08×/obs=453) | sub-CONF (0.93×/obs=259) |
| Key within-line targets | none at CONF (ch→k/l at 1.35-1.37×, sub-CONF) | **ch→t CONF (1.77×/obs=35)** |
| ch→sh | DEPL (0.75×) | DEPL (0.58×) |
| ch-LF pos1 | **FLAT** (no CONF) | **FLAT** (no CONF) |

**F547 (ch positional)**: ch pos1-STRONGLY-DEPLETED in BOTH dialects (A: 0.38×; B: 0.25×) — the most pos1-avoidant major class. MID elevated (1.14-1.18×). LF near-baseline (0.91-0.96×) — ch is a MID/LF class, not a line opener. Ch is the ONLY major onset class with near-baseline LF AND strong pos1 depletion simultaneously (sh has LF depletion AND pos1 neutrality in A; template classes have LF near-baseline but pos1 elevation in A).

**F548 (ch within-line)**: B ch→t CONF (E=1.77×/obs=35) — ch routes to t-onset in B (NEW). A ch has NO CONF within-line signals (1861 bigrams, N sufficient). Ch→sh DEPLETED cross-dialectally (A: 0.75×; B: 0.58×, F328 bidirectionally confirmed). Ch→ch sub-CONF in both dialects (A: 1.08×; B: 0.93×) — corrected F461/F462 confirmed: ch→ch is NOT self-succession CONF.

**F549 (ch vocabulary)**: Ch is y-body dominant in BOTH dialects (A: 42.5% y+35.2% ol; B: 36.0% y+28.6% edy). Ch vocabulary is the most dialect-stable of characterized classes: while template classes invert A→B (ch-mediated↔edy-dominated), ch retains y-body dominance across dialects. The y-body affinity is a structural property of ch independent of dialect.

**F550 (ch-LF flat)**: Ch-LF pos1 is flat in BOTH dialects (no CONF or dir signals; A: 373 lines; B: 194 lines). Ch-LF is the ONLY major LF class with completely absent pos1 grammar. All other characterized LF classes (ok, ot, o, d) have at least one confirmed pos1 opener rule. Ch-LF lacks this structure in both dialects.

**New findings: F547, F548, F549, F550**
**H_new_FC CLOSED.**

**New hypothesis generated**: H_new_FE: B ch→t CONF (E=1.77×/obs=35) — section scope and A analog. Is B ch→t B-herbal-specific or B-dialect-wide? Does ch→t appear at (dir) level in A herbal_a? Also: A ch→k (1.35×/86) and ch→l (1.37×/57) are consistently elevated in both dialects — are these structural near-CONF signals worth testing for section scope?
