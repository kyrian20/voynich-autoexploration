# exp_537 result — qok-onset full characterization (H_new_EX)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: Standard corpus parsing. ONSET_PRIORITY places qok first (priority 1), correctly partitioning from ok (priority 8), qot (priority 2). No feature destruction.

**Extrapolation**: None. Claims within tested corpus scope.

---

## Part 1: qok Vocabulary

### A herbal_a: 199 tokens, 57 types
Top words: qokchy(17.6%), qoky(10.1%), qokol(8.0%), qokaiin(7.5%), qokchol(6.0%), qokeey(4.5%), qokchor(3.5%), qokor(3.0%), qokar(3.0%), qokcho(2.0%).

**A vocabulary**: ch-mediated: qokchy+qokchol+qokchor+qokcho ≈ 29%. y-body: qoky (10.1%). ol/or: qokol+qokor = 11%. aiin: qokaiin (7.5%). Same architecture as qot (36.5%) and ot (30%).

### B all: 1929 tokens, 143 types
Top words: qokeedy(12.9%), qokain(11.8%), qokeey(11.3%), qokaiin(10.6%), qokedy(10.6%), qokal(6.5%), qokar(5.0%), qoky(3.8%).

**B vocabulary**: edy+eedy: 23.5% (qokedy+qokeedy). ain/aiin: 22.4% (qokain+qokaiin). al/ar: 11.5%. Same architecture as qot (22.2% edy+eedy) and ot (17.1%).

### Complete template class vocabulary taxonomy:
| Class | A dominant pattern | B dominant pattern |
|-------|------------------|------------------|
| qot | ch-mediated (36.5%) | edy+eedy (22.2%) |
| **qok** | **ch-mediated (29%)** | **edy+eedy (23.5%)** |
| ot | ch-mediated (30%) | edy+eedy (17.1%) |
| ok | **aiin-dominated (12.3%)** | **aiin (23.6%) — DIVERGES** |

**F541**: qot/qok/ot share the A=ch-mediated/B=edy-dominated vocabulary architecture. ok DIVERGES: aiin-dominated in both dialects, ch-mediated absent. The vocabulary split is ok vs {qot, qok, ot}.

---

## Part 2: qok Positional Distribution

(These values were also computed in exp_536 Part 5 for comparison.)

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 62/928 | 6.7% | 1.47× | 224/1903 | 11.8% | 0.88× |
| MID | 112/2481 | 4.5% | 0.99× | 1555/10610 | 14.7% | 1.10× |
| LL | 38/829 | 4.6% | 1.01× | 248/1846 | 13.4% | 1.01× |
| LF | 25/966 | 2.6% | **0.57×** | 150/1930 | 7.8% | **0.58×** |

Baselines: A=4.55%, B=13.36%.

**A qok**: pos1 near-CONF (E=1.47×/obs=62) but below threshold. LF DEPLETED (E=0.57×). MID and LL near-baseline.
**B qok**: pos1 near-baseline (E=0.88×). LF DEPLETED (E=0.58×). MID slightly elevated (1.10×).

**qok LF depletion is cross-dialectal**: A E=0.57×; B E=0.58×. This is the ONLY position where qok shows a consistent cross-dialectal signal — qok avoids LF in both dialects. No other template class shows such consistent LF depletion: qot LF=1.01×; ot LF=1.02×; ok LF=1.10×.

---

## Part 3: qok Within-Line Bigrams

### A herbal_a (174 qok sender bigrams):
| qok→X | obs | E | flag |
|-------|-----|---|------|
| qok→qot | 12 | 2.22× | **CONF** |
| qok→qok | 15 | 2.16× | **CONF** |
| qok→y | 11 | 1.57× | **CONF** |
| qok→ch | 46 | 1.01× | baseline |
| qok→sh | 9 | 0.62× | DEPL |
| qok→cth | 6 | 0.53× | DEPL |

**A: THREE CONF within-line signals.** Most striking: **qok→qot CONF** (E=2.22×/obs=12) — directed coupling from qok to qot within lines. This is new: within a line, after a qok-onset word, qot-onset is 2.22× more likely. qok→qok self-succession CONF (2.16×). qok→y CONF (1.57×). qok→ch BASELINE (1.01×) — same as qot→ch baseline.

### B all (1779 qok sender bigrams):
| qok→X | obs | E | flag |
|-------|-----|---|------|
| qok→sh | 208 | 1.26× | 1.26× |
| qok→ch | 389 | 1.17× | 1.17× |
| qok→qok | 278 | 1.15× | 1.15× |
| qok→a | 47 | 0.48× | DEPL |

**B: NO CONF signals.** B qok is within-line inert — all successors near-baseline or depleted. qok→a DEPLETED (E=0.48×/obs=47) is notable. B qok self-succession sub-CONF (1.15×/obs=278, needs E≥1.5× for CONF). Contrast with B qot→qot CONF (1.93×) and B ot→ot CONF (2.12×).

### Complete template class →ch within-line summary:
| Class | A E×(obs) | B E×(obs) |
|-------|-----------|-----------|
| qot→ch | 1.06×(39) BASELINE | 1.20×(102) BASELINE |
| **qok→ch** | **1.01×(46) BASELINE** | **1.17×(389) BASELINE** |
| ot→ch | 0.77×(30) DEPLETED | 0.85×(129) DEPLETED |
| ok→ch | 1.11×(50) BASELINE | 1.12×(189) BASELINE |

**F543 key finding**: ot is the ONLY template class that depletes →ch within lines. qo-prefixed classes (qot, qok) and ok are all baseline for →ch. The ot→ch avoidance is a unique ot-specific structural property.

### Template class self-succession cross-dialectal matrix:
| Class | A self-succession | B self-succession |
|-------|-----------------|-----------------|
| qot | CONF (2.74×/obs=12) | **CONF (1.93×/obs=33)** |
| qok | CONF (2.16×/obs=15) | 1.15×/obs=278 — sub-CONF |
| ot | CONF (1.79×/obs=11) | **CONF (2.12×/obs=124)** |
| ok | CONF (2.10×/obs=18) | 1.24×/obs=87 — sub-CONF |

**Two-tier pattern**: qot and ot have CONF self-succession in BOTH dialects. qok and ok have CONF self-succession in A only. Within-line self-succession persists cross-dialectally for qot/ot but not for qok/ok.

---

## Part 4: qok-LF Lines

### A herbal_a qok-LF (24 lines, 2.5%):
- ot: E=2.92×/obs=4 → (dir) — qok-terminal lines start with ot-onset
- No CONF signals (N=24 too small)

### B all qok-LF (147 lines, 7.6%):
- p: E=2.38×/obs=7 → dir — qok-terminal lines start with p-onset
- y: E=0.64×/obs=13 — DEPLETED at pos1
- d: E=0.68×/obs=18 — DEPLETED at pos1

**B qok-LF pos1=p dir** (E=2.38×/obs=7): B lines ending in qok tend to start with p-onset. p is the gallows-formula opener (B p-formula: p→sh→qot/ch). This suggests B qok-LF lines may be formula-typed (p-class formula lines that end in qok).

---

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: None. ONSET_PRIORITY correctly prioritizes qok over ok (qok=priority 1, ok=priority 8). No structural artifacts.

**Extrapolation**: None.

**Negative-result scope**: B qok flat bigrams — the conclusion is "qok within-line grammar is A-specific" (A has three CONF signals; B has none). This is scope-appropriate.

**Control behavior**: No controls. Within-corpus baselines throughout.

---

## Summary: Complete Template Class Quad

### Vocabulary:
qot/qok/ot = A:ch-mediated / B:edy-dominated (vocabulary parallel F538+F541)
ok = DIVERGES (aiin-dominated both dialects)

### Positional roles (A herbal_a):
| Class | pos1 E | LF E | Role |
|-------|--------|------|------|
| qot | 1.79× CONF | 1.01× | LINE OPENER |
| qok | 1.47× near-CONF | 0.57× DEPL | opener tendency |
| ot | 1.29× sub-CONF | 1.01× | NEUTRAL |
| ok | 1.10× neutral | 1.10× | NEUTRAL |

qok is the ONLY template class with consistent LF depletion cross-dialectally (A: 0.57×, B: 0.58×).

### Within-line bigrams (A):
| Class | →self | →ch | Key cross-class |
|-------|-------|-----|----------------|
| qot | CONF (2.74×) | BASELINE | qot→y (1.59×) |
| qok | CONF (2.16×) | BASELINE | **qok→qot CONF (2.22×)**, qok→y CONF (1.57×) |
| ot | CONF (1.79×) | DEPLETED | ot→qo dir (2.24×) |
| ok | CONF (2.10×) | BASELINE | ok→qo (1.67×) |

**Key new coupling**: A qok→qot CONF (E=2.22×/obs=12). This creates a within-line directed path: qok-class word → qot-class word. Combined with qot self-succession CONF, the pattern qok→qot→qot is possible within lines.

**F542**: A qok within-line grammar: qok→qot CONF (E=2.22×/obs=12, NEW directed coupling), qok→qok CONF (E=2.16×/obs=15), qok→y CONF (E=1.57×/obs=11). B qok flat (no CONF). qok→ch BASELINE in both dialects.

**New findings: F541, F542, F543**
**H_new_EX CLOSED.**
