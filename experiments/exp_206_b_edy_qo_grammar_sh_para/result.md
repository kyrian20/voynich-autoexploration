# exp_206: B edy-Suffix Class (H386), A qo-Grammar sh-Loop (H387), A sh vs cth Para Position (H388), B qo-Grammar (H389)
**Date**: 2026-04-11
**Method**: ZL3b paragraph-aware parser; folio-level dialect detection; A=163, B=101 paragraphs.

---

## 1. H386: B-Dialect edy-Suffix Para-Terminal Class

**B edy-suffix total: 3618/18649 = 19.40% (43× higher than A: 0.45%)**

### B edy-suffix positional profile:
| Cat | edy_n | edy% | base% | Enr |
|-----|-------|------|-------|-----|
| ps | 15 | 0.41% | 0.54% | 0.77× |
| wp_lf | 391 | 10.81% | 12.39% | **0.87×** |
| mid | 2941 | 81.29% | 74.26% | **1.09×** |
| wp_ll | 257 | 7.10% | 12.31% | **0.58×** |
| pf_ll | 14 | 0.39% | 0.50% | **0.77×** |

### Top B edy-suffix words (n≥3):
| Word | n | ps | wp_lf | mid | wp_ll | pf_ll |
|------|---|----|-------|-----|-------|-------|
| chedy | 424 | 0 | 8 | 375 | 37 | 4 |
| shedy | 364 | 0 | 18 | 325 | 17 | 4 |
| qokeedy | 297 | 1 | 35 | 252 | 9 | 0 |
| qokedy | 262 | 0 | 24 | 225 | 12 | 1 |
| otedy | 134 | 0 | 4 | 123 | 6 | 1 |
| lchedy | 107 | 0 | 8 | 83 | 16 | 0 |
| okedy | 103 | 0 | 3 | 91 | 8 | 1 |
| okeedy | 95 | 0 | 9 | 74 | 12 | 0 |
| sheedy | 72 | 0 | 5 | 67 | 0 | 0 |

**H386 NOT SUPPORTED — B edy-suffix class is NOT a para-terminal class; it is MID-dominant (81.29%/1.09×) with DEPLETED pf_ll (0.77×) and wp_ll (0.58×)**:

The B edy-suffix class as a whole is a MID-biased class, NOT a para-terminal class. pf_ll=0.77× (depleted), wp_ll=0.58× (strongly depleted). edy-suffix words actually AVOID line-terminal positions in B overall.

This requires revising two prior findings:
1. **The B cth pf_ll=8.10× finding (F205/H384)**: B cth-words had pf_ll=2/49=4.1% (8.10×). This was based on n=2 pf_ll cases out of 49 B cth-words. Given that the whole edy-suffix class has pf_ll=0.77×, the 8.10× finding is likely **sampling noise from n=2** — not a genuine para-terminal property of B cth-words. The n=49 is too small and the n=2 pf_ll is within the noise range.
2. **The cosmo shedy finding**: F201/F202 showed cosmo B shedy=13.34× PF/WP. This was in the cosmo section specifically. The aggregate shedy across all B shows pfl=4/364 = 1.10% (vs base 0.50% = 2.2×) — much weaker than the cosmo-specific enrichment. The cosmo shedy result was a **section-specific finding** (cosmo only), not a class-wide B property.

**Key correction**: B edy-suffix words are NOT the B-dialect para-terminal formula. They are predominantly MID content words. The edy-suffix class enrichment at MID (1.09×) reflects that edy-suffix words appear throughout the interior of lines and paragraphs in B. The B para-terminal formula remains characterized by the WP-LL class of specific words (chedy/shedy have some WP-LL presence: 37/424=8.7% and 17/364=4.7%), but no edy-suffix word has a dramatic pf_ll enrichment at the class or word level. The F201 cosmo B shedy finding was section-specific, not dialect-wide.

**Revised interpretation of B cth positional claim**: The F205 claim that B cth-words are "pf_ll=8.10× (para-terminal)" is **not supported** when examined in the context of the broader edy-suffix class. The 2 pf_ll cases in 49 B cth-words are noise. The correct interpretation of B cth-words is that they are edy-suffix class words that appear at standard B edy-suffix positions (MID-dominant, line-terminal depleted). The fundamental finding from F205 — that B cth rate is 14× lower than A and B cth-words are edy-suffix forms — remains valid. Only the "pf_ll=8.10× para-terminal" claim needs correction.

---

## 2. H387: A qo-Onset Grammar — sh→qo→sh Loop?

**A qo-class (qo+qot+qok) successor profile (n=954 combined bigrams):**
| Onset | n | % | base% | Enr |
|-------|---|---|-------|-----|
| ch | 229 | 24.0% | 21.9% | 1.10× |
| d | 142 | 14.9% | 14.3% | 1.04× |
| qok | 76 | 8.0% | 5.3% | **1.51×** |
| sh | 72 | 7.5% | 10.0% | **0.75×** |
| ok | 72 | 7.5% | 5.9% | **1.27×** |
| qot | 35 | 3.7% | 2.6% | **1.42×** |
| cth | 33 | 3.5% | 4.4% | **0.79×** |
| l | 13 | 1.4% | 0.5% | **2.58×** |

**sh depleted after combined qo-class: 0.75× (72/954 = 7.5% vs base 10.0%)**

**Sub-class breakdown (→sh):**
- qo → sh: 0.87× (near-baseline)
- qot → sh: 0.66× (depleted)
- qok → sh: 0.74× (depleted)

**[sh][qo][sh] triple test:**
- A [sh][qo-onset] pairs: 130 (sh precedes qo-class)
- Expected [sh][qo][sh] triple (independent): 9.8
- Actual [sh][qo][sh]: 10 (1.02× — exactly at baseline)

**H387 NOT SUPPORTED — qo-class does NOT re-introduce sh; the sh→qo relationship is ONE-DIRECTIONAL; no sh↔qo loop**:

While sh-onset words in A enriched qo-class successors (qo: 1.90×, qot: 1.64×, qok: 1.49× — exp_205 H382), the relationship is NOT bidirectional. qo-class words in A DEPLETE sh successors (0.75× combined). The [sh][qo][sh] triple is at exactly baseline (1.02×, no enrichment). There is no sh↔qo bidirectional grammar cluster.

qo-class in A is a **ch-adjacent self-clustering class**: qo-class successors include ch(1.10×), qok-self(1.51×), qot-self(1.42×), ok(1.27×). qo-class words introduce further qo-class content and ch-onset words, NOT sh-onset.

The directional relationship is: sh → qo (enriched 1.49-1.90×) but qo does NOT → sh (0.75×). This means the sh→qo connection is one-directional and the qo words are a separate grammar cluster that does not feed back to sh.

Additional notable finding: qo-class → l is strongly enriched in A (2.58×, n=13). This is a previously uncharacterized relationship.

---

## 3. H388: A sh vs cth Paragraph Position

**A sh-onset by paragraph line index:**
| LineIdx | total | sh_n | sh% |
|---------|-------|------|-----|
| 0 (first line) | 1011 | 147 | **14.54%** |
| 1 | 1111 | 85 | 7.65% |
| 2 | 1026 | 76 | 7.41% |
| 3 | 830 | 76 | 9.16% |
| 4 | 760 | 58 | 7.63% |
| 5+ (later) | 4913 | 474 | 9.65% |

**A cth-onset by paragraph line index:**
| LineIdx | total | cth_n | cth% |
|---------|-------|-------|------|
| 0 (first line) | 1011 | 10 | **0.99%** |
| 1 | 1111 | 52 | 4.68% |
| 2 | 1026 | 37 | 3.61% |
| 3 | 830 | 23 | 2.77% |
| 4 | 760 | 35 | 4.61% |
| 5+ (later) | 4913 | 198 | 4.03% |

**A sh vs cth by paragraph position (first/middle/last line):**
| ParaPos | total | sh_n | sh% | sh_enr | cth_n | cth% | cth_enr |
|---------|-------|------|-----|--------|-------|------|---------|
| first | 1011 | 147 | 16.05% | **1.53×** | 10 | 2.82% | **0.27×** |
| middle | 7998 | 744 | 81.22% | 0.98× | 333 | 93.80% | **1.13×** |
| last | 642 | 25 | 2.73% | 0.41× | 12 | 3.38% | 0.51× |

**Overall A sh rate**: ~10.0%; **Overall A cth rate**: ~3.68%

**H388 SUPPORTED WITH MAJOR FINDING — sh and cth are PARA-LEVEL SEGREGATED in A: sh enriched at first paragraph line (1.53×) and depleted at last (0.41×); cth is STRONGLY DEPLETED at first paragraph line (0.27×) and enriched in middle lines (1.13×)**:

This is the paragraph-level analog of the line-level positional findings. At the FIRST LINE of A-dialect paragraphs:
- sh-onset words: 14.54% (base ~10%) = **1.53× enrichment**
- cth-onset words: 0.99% (base ~3.68%) = **0.27× depletion**

cth is 73% depleted at paragraph openings. sh is 53% enriched at paragraph openings.

At paragraph middle lines:
- sh is near-baseline (0.98×)
- cth is modestly enriched (1.13×)

This establishes:
1. **sh occupies the PARAGRAPH-OPENING niche in A** — the first line of paragraphs is sh-dominant. This parallels the WP-LF/PS enrichment of sh-words and is the paragraph-level grammatical role of sh.
2. **cth is a PARAGRAPH-INTERIOR class in A** — cth-words appear almost exclusively in middle lines (93.80%/1.13×). The first paragraph line has barely any cth content (0.27×).
3. **Combined picture**: A-dialect paragraph structure: **[sh-dominant first line] → [cth-containing middle lines] → [sh/cth-neutral last line]**. The ch→daiin→cth grammar chain operates in the middle lines; the paragraph opens with sh-dominated content.

This is consistent with the A-dialect grammar as: sh-words are the paragraph-opening vocabulary (greeting/topic markers?), cth-words are interior grammar elements, and the two classes are segregated by paragraph position as well as by bigram neighborhood (cth depleted before/after sh).

---

## 4. H389: B-Dialect qo-Onset Grammar

**B qo-class rate: 20.15% (vs A: 10.98%) — B has 1.84× higher qo-class rate**

### B qo-class positional profile:
| Cat | qo_n | qo% | base% | Enr |
|-----|------|-----|-------|-----|
| ps | 5 | 0.13% | 0.54% | **0.25×** |
| wp_lf | 350 | 9.32% | 12.39% | **0.75×** |
| mid | 3080 | 81.98% | 74.26% | **1.10×** |
| wp_ll | 317 | 8.44% | 12.31% | **0.69×** |
| pf_ll | 5 | 0.13% | 0.50% | **0.26×** |

### B qo-class successor profiles:
| Onset | qo(570) | qot(660) | qok(2204) | Combined | Enr |
|-------|---------|----------|-----------|----------|-----|
| qo | 7.2%(2.09×) | 2.6%(0.75×) | 2.5%(0.72×) | — | — |
| qot | 4.6%(1.06×) | 9.2%(2.16×) | 4.3%(1.01×) | — | — |
| qok | 12.5%(0.94×) | 11.8%(0.89×) | 15.5%(1.17×) | — | — |
| sh | 8.4%(0.87×) | 7.6%(0.78×) | 11.7%(1.20×) | 10.3%(~1.06×) | ~1.06× |
| ch | 17.5%(1.02×) | 19.4%(1.13×) | 20.8%(1.21×) | — | ~1.13× |
| cth | 0.2%(0.68×) | 0.5%(1.76×) | 0.1%(0.35×) | — | <<0.3% |

**H389 SUPPORTED — B qo-class is strongly MID-biased (81.98%/1.10×), 1.84× higher rate than A, strongly depleted at PS/PF-LL (0.25×/0.26×); sub-class strong self-clustering (qo→qo:2.09×, qot→qot:2.16×); qok→sh(1.20×) while qo→sh(0.87×) and qot→sh(0.78×) — sh-introduction is specific to qok-onset, not qo-class generally**:

B qo-class (3757 tokens = 20.15%) is:
1. **MID-dominant**: 81.98% MID (1.10× enrichment); PS=0.25× (essentially PS=0); PF-LL=0.26× (essentially PF-LL=0). qo-class words NEVER open or close paragraphs in B.
2. **Sub-class self-clustering**: qo→qo (2.09×), qot→qot (2.16×) — strong tendency to cluster within sub-class.
3. **qok→sh specific**: qok introduces sh (1.20×); qo and qot deplete sh (0.87×, 0.78×). The B qok→sh pattern is a distinctive successor relationship not seen in qo or qot. qok self-clusters strongly (qok→qok: 1.17×, qok→ch: 1.21×, qok→sh: 1.20×).
4. **A vs B qo-class comparison**: A qo-class is also MID-biased but with notable WP-LF presence (19.34%/1.20×); B qo-class suppresses WP-LF more strongly (9.32%/0.75×). In A, qo-class words sometimes open lines; in B, they almost never do.
5. **cth excluded from B qo-class vicinity**: B qo-class words rarely precede cth (qo: 0.68×, qok: 0.35×, qot: 1.76× at n=3 = marginal). cth is essentially absent from B qo-class neighborhoods, consistent with cth being an A-specific grammar class.

**qo-class grammar comparison A vs B:**
- Both dialects: qo-class is MID-biased, self-clustering, ch-adjacent
- A-specific: qo-class introduces cth at moderate level (A qo→cth: 1.23×, qok→cth: 0.44×)
- B-specific: qok→sh enrichment (1.20×); B qo-class much more MID-concentrated and PS/PF-LL depleted; B has 1.84× higher qo-class rate overall

---

## Self-Audit

**Target-awareness**: No target-aware elements identified. All comparisons are corpus-internal positional profiles and bigram frequencies.

**Feature-destroying implementation**: No feature-destroying implementation details. One clarification: the paragraph position analysis (H388) classifies by line index within paragraph, which is the correct level for testing paragraph-level segregation. Line_idx=0 = first paragraph line; this is where PS words appear, but the sh/cth pattern holds across the entire first line (not just the PS position), which is the correct comparison.

**Extrapolation**: H386 conclusion restates prior findings (F205's "B cth pf_ll=8.10×") as likely noise. This is justified by: (a) the edy-suffix class shows pf_ll=0.77× (depleted), making the cth pf_ll=8.10× anomalous; (b) n=2 pf_ll cases out of 49 B cth-words is insufficient for a reliable claim. The conclusion "the 8.10× was noise" is within the scope of this data. H388: "sh-dominant first line" is well-supported (n=147 sh in first lines). H389: "qo-class never opens/closes paragraphs" is directional — n=5 PS instances out of 3757 qo tokens (0.13%) is reliable near-zero.

**Negative-result scope**: H386 NOT SUPPORTED: "B edy-suffix class is not collectively para-terminal" — this is correctly scoped to the aggregate class. Individual words might have section-specific para-terminal roles (shedy in cosmo B). H387 NOT SUPPORTED: "no sh→qo→sh loop" — correctly scoped to the within-line triple count and qo-class successor profile in A.

**Control behavior**: No external controls. All baselines are corpus-internal. sh rate of 10% in A and cth rate of 3.68% in A are consistent with prior experiments. No surprises in baseline values. The first-line sh rate (14.54%) vs non-first (7.41-9.65%) is a striking gradient — check: total first-line words = 1011 out of total A words 9651 = 10.5% of words are in first paragraph lines, which is reasonable (A=163 paragraphs × ~6 words per first line ≈ 978 words, consistent with 1011). No flags.

**Correction note**: This experiment requires updating F205's claim that B cth-words are "pf_ll=8.10× para-terminal." The correct statement is: B cth-words are edy-suffix class words that appear at standard B edy-suffix positions (MID-dominant); the earlier pf_ll=8.10× was n=2 sampling noise. This is a scope correction to F205, not a finding-level contradiction.

---

## CONCLUSION

| H | Result | Key Finding |
|---|--------|-------------|
| H386 | NOT SUPPORTED | B edy-suffix class: pf_ll=0.77× (DEPLETED), wp_ll=0.58× — edy-suffix is MID-dominant (81.29%/1.09×), NOT para-terminal; F205 B cth pf_ll=8.10× was n=2 noise; cosmo shedy para-terminal was section-specific; B edy-suffix is a B-defining MID content-word class, not a para-closing class |
| H387 | NOT SUPPORTED | A qo-class → sh: 0.75× (DEPLETED); [sh][qo][sh] triple: 1.02× (baseline); sh→qo is one-directional; qo-class introduces ch(1.10×)/qok(1.51×)/ok(1.27×) in A, not sh; no sh↔qo loop |
| H388 | SUPPORTED (MAJOR) | A first-line sh=14.54%(1.53×), cth=0.99%(0.27×); A paragraph structure: [sh-dominant first line] → [cth-containing middle lines (93.80%/1.13×)] → [neutral last line]; sh and cth are paragraph-level SEGREGATED in A |
| H389 | SUPPORTED | B qo-class: 20.15% rate (1.84× more than A); ps=0.25×/pf_ll=0.26× (never opens/closes paragraphs); MID=81.98%/1.10×; qo→qo(2.09×)/qot→qot(2.16×) strong self-clustering; qok→sh(1.20×) but qo→sh(0.87×)/qot→sh(0.78×) — sh-introduction is qok-specific; B qo-class is a MID-dominant self-clustering class distinct from A's qo-class role |
