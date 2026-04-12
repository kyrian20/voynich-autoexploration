# exp_376: qok-Onset Full Characterization (H590)

**Date:** 2026-04-11
**Hypothesis:** H590 — qok positional profile and outgoing bigram rules.
**Result:** H590 ANSWERED. qok is MID-enriched, LL-DEPLETED in both dialects (A: MID=1.34×, LL=0.53×; B: MID=1.16×, LL=0.59×). Self-succession: A LF+MID concentrated (LF=1.64×, MID=1.66×), pre_LL near-baseline (0.85×); B MID-concentrated (1.24×), pre_LL depleted (0.78×). Outgoing: A qok→d pre_LL E=2.31× (daiin at LL); A qok→ok MID E=1.73× (bidirectional A {qok,ok} MID coupling confirmed); A qok→sh pre_LL=0.00× (sh absent at LL after qok); B qok→ch MID E=1.25× (B {qok,ch} coupling); B qok→r pre_LL E=3.01× (generalizes B qot→r); B qok→ol pre_LL E=1.88×. Generalized rules emerging: A {qot,qok,ok,ot} pre_LL → daiin at LL; B {qot,qok} pre_LL → r at LL; B {qok,ot,ok} pre_LL → ol at LL.

---

## Key Statistics

### qok Positional Distribution (All Template Classes)
| Class | A LF | A MID | A LL | B LF | B MID | B LL |
|-------|------|-------|------|------|-------|------|
| qot | **1.65×** | 0.81× | 0.72× | 0.51× | 1.14× | 0.88× |
| qok | 1.09× | **1.34×** | **0.53×** | 0.79× | **1.16×** | **0.59×** |
| ok | 0.81× | **1.14×** | 0.96× | 0.49× | **1.12×** | 0.95× |
| ot | 0.91× | 1.03× | **1.24×** | **0.33×** | 1.15× | **1.16×** |

**A-dialect positional taxonomy**: qot=opener(LF-enriched), qok/ok=mid-line(MID-enriched), ot=closer(LL-enriched). qok is the most LL-depleted class (E=0.53×).
**B-dialect**: All four classes MID-enriched; qok and ot most LL-depleted.

### qok Self-Succession by Position
| Position | A qok E | B qok E |
|----------|---------|---------|
| LF→pos1 | 1.64× | 1.19× |
| MID_inner | **1.66×** | **1.24×** |
| pre_LL→LL | 0.85× | **0.78×** (depleted) |
| Overall | 1.54× | 1.17× |

Self-succession peaks at LF+MID in A (unlike ot which peaks at pre_LL). B: MID-concentrated, pre_LL depleted. Same-word rate: A=7.5%, B=17.3%.

### qok Key Outgoing Bigrams
| Rule | Dialect | N | Key Position | E |
|------|---------|---|-------------|---|
| qok→d (daiin) | A | 80/454 | pre_LL→LL | **2.31×** |
| qok→ok | A | 44/454 | MID_inner | **1.73×** |
| qok→ch | A | 110/454 | LF→pos1 | **1.56×** |
| qok→sh | A | 33/454 | pre_LL→LL | **0.00×** (absent) |
| qok→ot | A | 12/454 | all | 0.60× (depleted) |
| qok→ch | B | 453/2162 | LF+MID | 1.34×/1.25× |
| qok→sh | B | 253/2162 | LF+MID | 1.44×/1.31× |
| qok→r | B | 37/2162 | pre_LL→LL | **3.01×** |
| qok→ol | B | 118/2162 | pre_LL→LL | **1.88×** |
| qok→y | B | 26/2162 | all | **0.58×** (depleted) |

---

## Findings

### Finding 1: qok Is MID-Enriched, LL-DEPLETED in Both Dialects — The Most LL-Depleted Template Class

A qok: MID=1.34×, LL=0.53×. B qok: MID=1.16×, LL=0.59×. qok has the strongest LL depletion of any template class characterized (A: 0.53× vs ot's 0.72×). qok is a PURE MID-LINE class — it operates throughout lines but strongly avoids the LL position. This cross-dialect consistency (both A and B LL=0.53-0.59×) makes qok's LL avoidance the most robust positional constraint found in this series.

### Finding 2: A-Dialect Four-Class Positional Grammar Emerges — qot(opener) / qok+ok(mid) / ot(closer)

Comparing A-dialect positions across all four classes: qot peaks at LF (1.65×, depleted at LL=0.72×); qok peaks at MID (1.34×, strongly depleted at LL=0.53×); ok peaks at MID (1.14×); ot peaks at LL (1.24×). This creates a **SPATIAL GRAMMAR** for A-dialect continuation lines:
1. **LF position**: qot cluster (E=1.65×)
2. **MID position**: qok+ok cluster (E=1.34×/1.14×)
3. **LL position**: ot cluster (E=1.24×)

The four template classes tile the line positions: opener → mid-line → closer. This is a novel structural finding about how onset classes organize across the line.

### Finding 3: A qok→d pre_LL→LL E=2.31× — Generalizes the Pre_LL→Daiin Rule Across Multiple Template Classes

A qok→d at pre_LL→LL: E=2.31× (21/62). Top pairs: qokol→daiin(5), qokeey→daiin(5), qoky→daiin(4). Combined with A qot→daiin pre_LL=2.28× (F377), A ok→d pre_LL=1.58× (F379), A ot→d pre_LL=1.48× (F378): GENERALIZED RULE: **A-dialect template classes at pre_LL → daiin at LL** (E=1.48-2.31× across {qot,qok,ok,ot}). Architecture: any A-dialect template class word at second-to-last position forecasts daiin at LL.

### Finding 4: A qok→sh at pre_LL→LL = 0.00× (Complete Absence) — sh Is Excluded After qok at Pre_LL

A qok→sh: overall E=0.76×, pre_LL→LL E=0.00× (0/62). sh is completely absent at LL after A qok at pre_LL. Combined with A qok LL=0.53× (qok avoids LL itself) and A qok→sh=0.00× at pre_LL: the A-dialect LL position excludes both qok (as position-filler) and sh (as successor-of-qok). Architecture: A LL grammar excludes sh-onset as a LL terminal when the prior word is a template class.

### Finding 5: A qok↔ok MID Bidirectional Coupling Confirmed (A qok→ok MID E=1.73×, A ok→qok MID E=1.68×)

A qok→ok: MID_inner=1.73× (33/296). A ok→qok: MID_inner=1.68× (27/282) from F379. Both directions confirmed MID-concentrated. The A-dialect {qok↔ok} bidirectional coupling (F326: 2.03×/1.68×) is specifically a MID-line coupling. These two classes alternate in mid-line positions.

### Finding 6: B qok→r pre_LL→LL E=3.01× — Generalizes to B {qot,qok} Pre_LL→r Rule

B qok→r at pre_LL→LL: E=3.01× (14/295). Compare B qot→r pre_LL=5.18× (F377). Both B qot and B qok at pre_LL → r at LL. Top pairs: qokeey→rol(2), qokeey→rchedy(2), qokeey→raiin(2) — qokeey is the primary B qok r-predecessor. GENERALIZED B RULE: **{qot,qok} at pre_LL → r at LL** (E=3-5×). Architecture: B-dialect r-onset LL words are selectively preceded by qot/qok at pre_LL.

### Finding 7: B qok→ch E=1.21× (MID=1.25×) and B qok→sh E=1.21× (MID=1.31×) — B {qok↔ch} and {qok→sh} Broadly Elevated in MID

B qok→ch: overall=1.21×, LF=1.34×, MID=1.25×. B qok→sh: overall=1.21×, LF=1.44×, MID=1.31×, pre_LL=0.49× (depleted near line-end). Both ch and sh are elevated successors of B qok in LF+MID positions. This matches F326's B qok↔ch bidirectional coupling and extends it to sh. B qok at pre_LL → sh strongly depleted (0.49×) — sh avoids LL after qok in B, consistent with B LL not being sh-terminal after template classes.

### Finding 8: B qok Vocabulary Is Highly Concentrated — qokeedy+qokain+qokedy = 34.9% of Tokens

B qok top 3: qokeedy(12.5%), qokain(11.5%), qokedy(10.9%) = 34.9% of all B qok tokens. Top 5 = 55.4%. This extreme concentration (higher than B ot: top 3=26.3%, B qot: top 3=30.2%) is consistent with Phase 6 finding (F305: B qok=18.2% of types cover 90% of tokens = smallest closed paradigm). B qok is the most paradigm-concentrated onset class in B-dialect.

---

## Summary

H590 ANSWERED. qok is MID-enriched, LL-depleted in both dialects (A: MID=1.34×, LL=0.53×; B: MID=1.16×, LL=0.59×). A-dialect four-class spatial grammar emerges: qot(LF opener) → qok+ok(MID) → ot(LL closer). A qok→d pre_LL E=2.31× generalizes the template-class→daiin pre_LL rule ({qot,qok,ok,ot} all show E=1.48-2.31× at pre_LL→LL). A qok↔ok MID bidirectional confirmed (1.73×/1.68×). B qok→r pre_LL E=3.01× generalizes B {qot,qok} pre_LL→r rule. B qok→ch/sh broadly elevated in LF+MID (both 1.21-1.44×), depleted at pre_LL. B qok vocabulary highly concentrated (top 3=34.9%).

---

## Self-Audit

**Target-awareness:** None. Pure corpus measurement. PASS.
**Feature-destroying implementation:** Same parsing as exp_373-375. ONSET_LEN=3 correct for 'qok'. PASS.
**Extrapolation:** A qok N=499 (adequate). B qok N=2340 (robust — largest N in this series). A pre_LL self-succession N=3/62 (directional for 0.85×, adjacent to qot pre_LL=0.00× for comparison). A qok→d pre_LL N=21/62 (moderate, consistent with qot/ok analogues). B qok→r pre_LL N=14/295 (moderate). PASS.
**Negative-result scope:** A qok→sh pre_LL E=0.00× (N=0/62, adequate to claim absence). B qok→y E=0.58× (N=26/2162, robust depletion). PASS.
**Control behavior:** A-dialect positional taxonomy (qot/qok/ok/ot spatial tiling) is internally consistent: no class claims both LF-enriched AND LL-enriched; they tile non-overlapping regions. B-dialect generalization (MID-enriched, LL-depleted) consistent across all four classes. PASS.
