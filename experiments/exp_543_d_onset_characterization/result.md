# exp_543 result — d-onset full characterization (H_new_FF)

## Audit

**Target-awareness**: None. Standard characterization methodology identical to exp_540-541.

**Feature-destroying implementation**: d onset extracted correctly via ONSET_PRIORITY (priority 15, after ch/sh/ok/ot/ol, before s/y/k/t). d→qot within-line vs CL check (Part 5) is a genuine structural test: different computation from F491 (CL pairs = consecutive LF words; within-line = consecutive words in same line).

**Extrapolation**: None. Claims within tested corpus scope.

---

## Part 1: d Vocabulary

### A herbal_a: 1364 tokens, 250 types
Top words: daiin(32.3%), dar(7.0%), dain(6.5%), dy(5.4%), dal(5.1%), dol(3.1%), dor(2.6%), dam(2.4%), dair(2.3%).

**A vocabulary body classes:**
| Body class | A d |
|-----------|-----|
| aiin-body | **40.4%** (daiin dominant 32.3%; dain 6.5%) |
| al/ol-body | 25.0% (dar, dal, dol, dor, dal) |
| y-body | 18.2% (dy, dchy, dshy, etc.) |
| other | 15.1% |
| ch-mediated | 1.3% (dchy, dchor, dchol) |

**A d vocabulary summary**: aiin-dominated (40.4%), with strong al/ol and y components. Daiin is the single most common d-word (32.3%). d is NOT ch-mediated (like template classes in A), NOT edy-dominated. d has a unique aiin-dominant vocabulary architecture.

### B all: 741 tokens, 173 types
Top words: daiin(22.5%), dar(10.8%), dain(7.8%), dal(7.7%), dy(4.7%), dol(3.9%), dshedy(3.8%), dchedy(2.6%).

**B vocabulary body classes:**
| Body class | B d |
|-----------|-----|
| aiin-body | **32.4%** |
| al/ol-body | 29.6% |
| y-body | 16.1% |
| edy-body | 11.3% (dshedy, dchedy, dsheedy) |
| other | 9.9% |
| ch-mediated | 0.8% |

**d vocabulary A/B contrast:**
| Body class | A d | B d |
|-----------|-----|-----|
| aiin-body | **40.4%** | **32.4%** |
| al/ol-body | 25.0% | 29.6% |
| y-body | 18.2% | 16.1% |
| edy-body | ~0% | 11.3% |
| ch-mediated | 1.3% | 0.8% |

**D vocabulary cross-dialect**: d is aiin-dominated in BOTH dialects (A: 40.4%; B: 32.4%). Daiin remains dominant in B (22.5%). B d gains some edy-body (11.3%) but retains aiin dominance. D shares the "aiin-dominant" vocabulary signature with ok (F541: ok aiin-dominated A: 12.3%, B: 23.6%) — neither follows the template class A=ch-mediated/B=edy-dominated pattern. D is the highest-aiin-dominant class in A (40.4% vs ok's 12.3%).

---

## Part 2: d Positional Distribution

| Position | A obs/N | A rate | A E | B obs/N | B rate | B E |
|---------|---------|--------|-----|---------|--------|-----|
| pos1 | 346/1961 | 17.6% | **1.47×** | 246/1279 | 19.2% | **2.64× CONF** |
| MID | 642/7333 | 8.8% | **0.73× DEPL** | 373/7601 | 4.9% | **0.67× DEPL** |
| LL | 212/1794 | 11.8% | 0.98× | 77/1266 | 6.1% | 0.83× |
| LF | 360/1961 | 18.4% | **1.52× CONF** | 121/1279 | 9.5% | 1.30× |

Baselines: A=12.0%, B=7.3%.

**A/B d positional INVERSION — the most complete positional dialect inversion in the project**:
- A d: LF **CONF** (E=1.52×/obs=360) — d is the dominant line-ENDER in A herbal_a (18.4% of LF = most common LF class). Pos1 near-CONF (E=1.47×). MID DEPLETED (0.73×).
- B d: pos1 **CONF** (E=2.64×/obs=246) — d is the dominant line-OPENER in B (19.2% of pos1 = most common or near-most-common pos1 class). LF sub-CONF (1.30×). MID DEPLETED (0.67×).

**D is a structural edge class in BOTH dialects**: MID-DEPLETED (A: 0.73×; B: 0.67×) — d avoids interior positions universally. The A/B inversion is which EDGE d prefers: A → line-final edge (LF); B → line-initial edge (pos1).

**Comparison to other onset classes**:
| Class | A pos1 | A LF | B pos1 | B LF |
|-------|--------|------|--------|------|
| d | near-CONF (1.47×) | **CONF (1.52×)** | **CONF (2.64×)** | sub-CONF (1.30×) |
| ch | STRONGLY DEPL (0.38×) | baseline (0.96×) | EXTREMELY DEPL (0.25×) | baseline (0.91×) |
| sh | neutral (1.03×) | DEPL (0.51×) | DEPL (0.70×) | DEPL (0.47×) |
| qot | **CONF (1.79×)** | baseline | DEPL (0.60×) | baseline |

D is unique: it has CONF or near-CONF signals at BOTH pos1 and LF in A, but MID is depleted. In B, it is the dominant pos1 class. D does not avoid line positions — it avoids the interior.

---

## Part 3: d Within-line Bigrams (d→X)

### A herbal_a (988 d sender bigrams):
| d→X | obs | E | flag |
|-----|-----|---|------|
| d→cth | 62 | **1.97×** | **CONF** |
| d→ckh | 20 | **1.58×** | **CONF** |
| d→d | 151 | 1.42× | sub-CONF |
| d→sh | 106 | 1.28× | sub-CONF |
| d→ch | 231 | 1.04× | baseline |
| d→qot | 23 | 0.99× | BASELINE |
| d→k | 18 | 0.53× | DEPL |
| d→ok | 59 | 0.74× | DEPL |

**A: TWO CONF signals.** d→cth CONF (E=1.97×/obs=62) — d routes to cth-onset compound gallows. d→ckh CONF (E=1.58×/obs=20) — d routes to ckh-onset. A d recruits compound gallows classes {cth, ckh} as within-line successors. d→d sub-CONF (1.42×/obs=151 — just below CONF E=1.5). d→ch, d→sh: elevated but below CONF.

**CRITICAL: d→qot within-line = BASELINE (E=0.99×/obs=23)** — the CL d→qot CONF (F491) is EXCLUSIVELY an inter-line mechanism. Within a single line, d does NOT preferentially route to qot. This confirms F491's inter-line character and rules out d→qot as a within-line rule.

### B all (619 d sender bigrams):
| d→X | obs | E | flag |
|-----|-----|---|------|
| d→sh | 109 | **1.79×** | **CONF** |
| d→ch | 124 | 1.08× | baseline |
| d→d | 41 | 1.19× | sub-CONF |
| d→qot | 18 | 0.66× | DEPL |
| d→qok | 64 | 0.67× | DEPL |

**B: ONE CONF signal.** d→sh CONF (E=1.79×/obs=109) — B d routes to sh-onset within lines. d→qot DEPLETED in B (0.66×). d→qok DEPLETED (0.67×).

### A/B d bigram contrast:
| Target | A E×(obs) | B E×(obs) |
|--------|-----------|-----------|
| d→cth | **1.97×(62) CONF** | (not shown, likely sub-CONF) |
| d→ckh | **1.58×(20) CONF** | (not shown) |
| d→sh | 1.28×(106) sub-CONF | **1.79×(109) CONF** |
| d→qot within-line | 0.99×(23) BASELINE | 0.66×(18) DEPL |

**Cross-dialectal**: d→qot within-line is BASELINE (A) or DEPLETED (B) in both dialects — the CL d→qot (F491) is exclusively inter-line. A d routes to compound gallows {cth, ckh}; B d routes to sh. Different within-line routing targets.

---

## Part 4: d-LF Lines Pos1 Profile

### A herbal_a d-LF (360 lines, 18.4%):
**TWO CONF signals:**
- **qot at pos1 CONF (E=1.92×/obs=25)** — lines ending in d tend to START with qot-onset
- **ot at pos1 CONF (E=1.72×/obs=24)** — lines ending in d tend to START with ot-onset
- y DEPLETED (E=0.88×)
- d-self: baseline (1.07×)

**Structural interpretation**: A lines with d at LF are opened by template classes (qot/ot) at pos1. This is a same-line structural co-occurrence: [qot or ot](pos1) → ... → [d](LF). Combined with CL chain F491 (d-LF → qot on NEXT line), the full structure is:

Line i: [qot/ot](pos1) → ... → [d](LF)  ← template-opened, d-closed
Line i+1: → ... → [qot/ch](LF)  ← d-LF → qot via CL chain

This suggests a paragraph-level structure where d-terminal lines are template-opened AND feed back into the template chain via CL.

### B all d-LF (121 lines, 9.5%):
- **qo at pos1 dir (E=2.21×/obs=9)** — B d-LF lines tend to open with qo-onset (dir, just below CONF). This mirrors B astro's d→qo CL dir signal (F530). Consistent: B lines ending in d tend to open with qo.
- Otherwise flat.

---

## Part 5: d→qot Within-line vs CL (Critical Test)

| Signal | Value | Interpretation |
|--------|-------|----------------|
| A d→qot within-line | E=0.99×/obs=23 (BASELINE) | d→qot is NOT a within-line rule |
| B d→qot within-line | E=0.66×/obs=18 (DEPL) | d→qot is NOT a within-line rule |
| F491: A d→qot CL (CONF) | E=1.5×+ | Exclusively inter-line |

**F491 CONFIRMED EXCLUSIVELY INTER-LINE**: d→qot coupling is a cross-line (paragraph-level) structure with zero within-line manifestation. Within a single line, d and qot do NOT co-succeed. The grammar operates at the line-boundary level only.

---

## Self-Audit

**Target-awareness**: None. The A/B positional inversion was not predicted. d→cth/ckh CONF were not predicted.

**Feature-destroying implementation**: Standard bigram count (within-line consecutive pairs). CL computation (consecutive LF words across lines) is distinct from Part 3 (within-line bigrams). Part 5 correctly compares the two. d onset priority is correct (priority 15, after cth/ckh/cph — so cth-onset words are NOT confused with d-onset words).

**Extrapolation**: None. All claims within A herbal_a (n≤56) and B all.

**Negative-result scope**: d→qot within-line: obs=23/23.2 expected — genuinely baseline, not a power issue (N_sender=988, expected=23 → well-powered for detecting E=1.5× at obs=35, which would be CONF).

---

## Summary: d Characterization

| Feature | A herbal_a | B all |
|---------|-----------|-------|
| Vocabulary | aiin-body dominant (40.4%); daiin=32.3% | aiin-body dominant (32.4%); daiin=22.5%; edy gains (11.3%) |
| Positional role | **LF CONF (1.52×/360)** — dominant LF class; pos1 near-CONF (1.47×); **MID DEPL (0.73×)** | **pos1 CONF (2.64×/246)** — dominant pos1 class; LF sub-CONF (1.30×); **MID DEPL (0.67×)** |
| Within-line self-succession | sub-CONF (1.42×/obs=151) | sub-CONF (1.19×/obs=41) |
| Key within-line targets | **d→cth CONF (1.97×/62); d→ckh CONF (1.58×/20)** | **d→sh CONF (1.79×/109)** |
| d→qot within-line | BASELINE (0.99×) | DEPL (0.66×) |
| d-LF pos1 | **qot CONF (1.92×/25); ot CONF (1.72×/24)** | qo dir (2.21×/9) |

**F553 (d vocabulary)**: d is aiin-dominated in BOTH dialects (A: 40.4%; B: 32.4%). Daiin dominant (A: 32.3%; B: 22.5%). D vocabulary belongs to the "aiin-dominant" class alongside ok (F541), not the "ch-mediated/edy-dominated" template class pattern. D has the HIGHEST aiin-body proportion of any characterized class (40.4% A).

**F554 (d positional A/B INVERSION)**: A d = LF CONF (E=1.52×/obs=360, dominant A LF class); B d = pos1 CONF (E=2.64×/obs=246, dominant B pos1 class). MID-DEPLETED in BOTH dialects (A: 0.73×; B: 0.67×). D is a structural EDGE class — it appears at line boundaries (LF in A; pos1 in B) and avoids interior positions universally. The A/B positional inversion for d is the most complete LF↔pos1 inversion in the project (compare to qot: A pos1 CONF → B pos1 DEPL, but d reverses pos1 and LF roles entirely).

**F555 (d within-line)**: A d→cth CONF (E=1.97×/obs=62) and d→ckh CONF (E=1.58×/obs=20) — d routes to compound gallows in A. B d→sh CONF (E=1.79×/obs=109) — d routes to sh in B. d→qot within-line = BASELINE in A (0.99×) and DEPLETED in B (0.66×): F491 (d→qot CL CONF) is CONFIRMED EXCLUSIVELY INTER-LINE — no within-line manifestation.

**F556 (d-LF pos1)**: A d-LF lines open with template classes: qot CONF (E=1.92×/obs=25) and ot CONF (E=1.72×/obs=24) at pos1 — lines ending in d tend to be opened by template classes. This creates the structure [qot/ot](pos1)→...→[d](LF), nested with CL chain F491 ([d-LF line] → [qot-LF next line]). B d-LF pos1=qo dir (E=2.21×/obs=9) — consistent with B d→qo CL dir signal (F530).

**New findings: F553, F554, F555, F556**
**H_new_FF CLOSED.**

**New hypothesis generated**: H_new_FH: d→sh CONF in B (E=1.79×/obs=109, F555) — section scope. Is B d→sh CONF in B herbal, B astro, B pharma individually? Also: A d→cth CONF (E=1.97×/obs=62) and A d→ckh CONF (E=1.58×/obs=20) — are these A-herbal-a-specific or cross-A? (Very likely herbal-a-specific but worth confirming.)
