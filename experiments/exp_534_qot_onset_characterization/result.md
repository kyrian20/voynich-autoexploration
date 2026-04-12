# exp_534 result — qot-onset full characterization (H587)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: Standard corpus parsing. A herbal_a = n≤56, A-dialect. B all = all B-dialect lines. Position types: pos1=line first, MID=intermediate, LL=penultimate, LF=last.

**Extrapolation**: None.

---

## Part 1: qot Vocabulary

### A herbal_a: 174 tokens, 44 types
Top words: qotchy (20.7%), qoty (10.9%), qotor (7.5%), qotol (7.5%), qotchor (5.7%), qotaiin (5.2%), qotchol (4.6%), qoteey (4.0%), qotchey (3.4%), qotcho (2.9%).

**A vocabulary pattern**: ch-mediated forms dominate (qotchy+qotchor+qotchol+qotchey+qotcho = 36.5% combined). qotchy alone is 20.7% — the dominant A qot word. y-body forms: qoty (10.9%). ol/or forms: qotol+qotor = 15%.

### B all: 508 tokens, 82 types
Top words: qotedy (11.2%), qoteedy (11.0%), qotain (8.7%), qotaiin (8.5%), qotal (8.3%), qotar (8.1%), qoty (6.1%), qoteey (3.9%), qotey (3.1%).

**B vocabulary pattern**: edy/eedy (B-dialect marker) = 22.2%; aiin/ain bodies = 17.2%; al/ar bodies = 16.4%; y-body = 6.1%. The B qot vocabulary is dominated by edy-body and aiin/al/ar forms — completely different from A.

### A/B vocabulary divergence:
| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Dominant class | qotchy (ch-mediated, 20.7%) | qotedy+qoteedy (edy-body, 22.2%) |
| aiin-body | qotaiin (5.2%) | qotaiin+qotain (17.2%) |
| al/ar-body | qotol+qotor (15%) | qotal+qotar (16.4%) |
| edy-body | rare | 22.2% |

---

## Part 2: qot Positional Distribution

| Position | A herbal_a obs/N | A rate | A E | B all obs/N | B rate | B E |
|---------|-----------------|--------|-----|------------|--------|-----|
| pos1 | 59/829 | 7.1% | **1.79×** | 39/1846 | 2.1% | **0.60×** |
| MID | 52/1652 | 3.1% | 0.79× | 348/8764 | 4.0% | 1.13× |
| LL | 30/928 | 3.2% | 0.81× | 69/1903 | 3.6% | 1.03× |
| LF | 33/966 | 3.4% | 0.86× | 52/1930 | 2.7% | 0.77× |

Baselines: A=4.0% of all words, B=3.5%.

**Critical finding**: qot has OPPOSITE positional profiles in A vs B:
- **A herbal_a**: qot is a LINE-OPENER — elevated at pos1 (E=1.79×/obs=59, **CONF**)
- **B all**: qot is a MID class — depleted at pos1 (E=0.60×), elevated at MID (E=1.13×)

F533: A herbal_a qot is a CONF pos1 opener (E=1.79×/obs=59).
F534: B-dialect qot is a MID class (pos1 DEPLETED E=0.60×).

---

## Part 3: qot Within-Line Bigrams

### A herbal_a (141 qot sender bigrams):
| qot→X | obs | E | flag |
|-------|-----|---|------|
| qot→qot | 12 | 2.74× | **CONF** |
| qot→y | 9 | 1.59× | 1.59× |
| qot→t | 6 | 1.73× | 1.73× |
| qot→qok | 8 | 1.42× | 1.42× |
| qot→ch | 39 | 1.06× | baseline |

**A: qot→qot self-succession CONF** (E=2.74×/obs=12). Within-line qot→ch is NEAR-BASELINE (E=1.06×) — the qot→ch link is an INTER-LINE (CL) phenomenon (F490), NOT a within-line bigram. The within-line qot grammar is self-succession and mild routing to y/t.

### B all (456 qot sender bigrams):
| qot→X | obs | E | flag |
|-------|-----|---|------|
| qot→ot | 52 | 1.58× | **CONF** |
| qot→qot | 33 | 1.93× | **CONF** |
| qot→r | 12 | 1.78× | **CONF** |
| qot→d | 32 | 1.34× | 1.34× |
| qot→ch | 102 | 1.20× | 1.20× |

**B: qot→ot CONF** (E=1.58×/obs=52) and **qot→qot CONF** (E=1.93×/obs=33). Also **qot→r CONF** (E=1.78×/obs=12). B qot has rich within-line successor grammar.

### Key distinction: qot→ch is baseline in BOTH dialects within-line
qot→ch succession within lines is near-baseline (A: E=1.06×; B: E=1.20×). The famous qot→ch link (F490) operates at the BETWEEN-LINE level (CL), not within lines. This is an important structural clarification.

---

## Part 4: qot-LF Lines

### A herbal_a qot-LF (33 lines, 3.4%):
- pos1=qot self: E=3.17×/obs=7 (dir) — qot-LF lines self-open with qot
- pos1=sh: E=1.87×/obs=5 (near-dir)
- No other class above threshold

### B all qot-LF (52 lines, 2.7%):
- No pos1 class above threshold (d: E=1.38×/obs=13; s: E=1.46×/obs=10 — both below CONF)

**A herbal_a qot-LF has pos1 self-chaining**: qot-terminal lines tend to start with qot (E=3.17×/obs=7, dir). This connects to Part 3: qot→qot within-line self-succession CONF + qot-LF→qot pos1 dir = qot is a self-clustering class in A herbal_a.

---

## Summary: qot Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Dominant words | qotchy (ch-mediated) | qotedy/qoteedy (edy-body) |
| Positional role | **LINE-OPENER** (pos1 CONF) | MID class (pos1 DEPL) |
| Within-line self-succession | CONF (E=2.74×/obs=12) | CONF (E=1.93×/obs=33) |
| Within-line key targets | qot→y (1.59×), qot→t (1.73×) | qot→ot CONF (1.58×), qot→r CONF (1.78×) |
| qot→ch within-line | baseline (E=1.06×) | baseline (E=1.20×) |
| qot-LF pos1 rule | qot-self dir (E=3.17×) | flat |
| Cross-line chain | d→qot→ch (F491/F490 CONF) | absent |

**Key clarification (F535)**: The qot→ch CL chain (F490, F491) is an INTER-LINE (paragraph-level) structure. Within lines, qot→ch succession is near-baseline in both dialects. qot's within-line grammar is self-succession + dialect-specific routing (A: y/t; B: ot/r).

**New findings: F533, F534, F535**
**H587 CLOSED.**
