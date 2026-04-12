# exp_559 result — A herbal_a line formula test: [cth@LL][d@LF] (H_new_FV)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. Bigram positions computed from word index within line. Baseline uses MID-onset distribution for LL enrichment computation; all-lines baseline for co-occurrence enrichment.

**Extrapolation**: See Part 4 (N=14 formula lines — all pos1 results are directional-only at best).

---

## Results

### Part 1: d-LF lines — cth co-occurrence

**A multi-word lines**: 1961 total; **d-LF lines**: 360 (18.4%).

| Measure | obs | total | rate | baseline | E |
|---------|-----|-------|------|----------|---|
| d-LF lines with any cth (pre-LF) | 47 | 360 | 13.1% | 10.1% | 1.29× |

Position of cth within d-LF lines: cth@MID=32 (68%), cth@LL=14 (30%), cth@pos1=2 (4%).

**Result**: d-LF lines are slightly enriched for cth co-occurrence (E=1.29×) but below CONF threshold (1.5×). When cth appears in a d-LF line, it is usually at MID (68%) rather than at LL (30%).

### Part 2: [cth@LL][d@LF] specifically

Lines with exact [cth@LL][d@LF]: **14** (3.9% of d-LF lines).

E(cth@LL in d-LF lines vs MID baseline) = **1.37×** (obs=14 vs expected=10.2). Sub-CONF (need E≥1.5 for CONF).

LL class distribution for d-LF lines (top classes): ch=91 (25.3%), d=68 (18.9%), qok=26 (7.2%), sh=22 (6.1%), ok=21 (5.8%), ot=20 (5.6%), y=17 (4.7%), k=15 (4.2%), **cth=14 (3.9%)**.

**Result**: [cth@LL][d@LF] exists (14 lines) but is not the dominant LL→LF pattern. Ch and d self-succession dominate the LL slot for d-LF lines.

### Part 3: [cth→d] bigrams — position distribution

Total [cth→d] bigrams in A: **37** (confirming F602 CONF result).

| Position | obs | fraction |
|----------|-----|----------|
| MID→MID+1 | 21 | 56.8% |
| LL→LF | 14 | 37.8% |
| pos1→pos2 | 2 | 5.4% |

Top word pairs: cthol→daiin (6), cthy→daiin (6), cthor→daiin (2), cthor→dain (2); then 21 singletons.

**Result**: Of the 37 confirmed cth→d consecutive bigrams, 14 (38%) occur at LL→LF and 21 (57%) occur at MID positions. The cth→d coupling is distributed across line positions, not concentrated at the terminal. The LL→LF fraction (38%) is slightly above what pure position-frequency would predict (~25-33% for average line length), but not dramatically so.

**Dominant pairs**: cthol→daiin and cthy→daiin each account for 6/37 = 16% of all cth→d bigrams. The d-word is almost exclusively daiin (14/37 = 38% just these two pairs; daiin is the dominant d-class word).

### Part 4: Pos1 profile of [cth@LL][d@LF] formula lines

N=14 formula lines (3+ words): **underpowered**.

| pos1 class | obs | E | flag |
|------------|-----|---|------|
| qot | 3 | 5.92× | (dir) |
| y | 3 | 1.30× | — |
| d | 1 | 0.40× | — |

**Result**: qot at pos1 is (dir) (E=5.92×/obs=3) — consistent with F602's finding that qo/qot prefer cth-terminal lines. However N=14 is too small for firm claims. Direction: [qot opener]...[cth@LL][d@LF] may be a specific A line type but requires larger N.

### Part 5: Inter-line coupling (cth-LF → d-LF successor)

**A lines with LF=cth**: 88; with known successor: 82.

Cth-LF lines followed by d-LF line: **17/82 = 20.7%**.
Baseline A LF=d rate: 18.4%.
E = **1.13×** (flat — essentially baseline).

Successor LF distribution after cth-LF: d=20.7%, ch=19.5%, cth=13.4%, ok=8.5%, ot=6.1%.

**Result**: Cth-LF lines are NOT specifically followed by d-LF lines at the inter-line level. E=1.13× is essentially flat. The d↔cth coupling (F602) operates WITHIN lines, not across consecutive lines.

---

## New Findings

**F603: [cth→d] bigram position distribution — A herbal_a** — The confirmed cth→d coupling (F602, E=1.97×/37) is distributed: MID→MID+1=21 (57%), LL→LF=14 (38%), pos1→pos2=2 (5%). The [cth@LL][d@LF] terminal formula exists (14 lines, 3.9% of d-LF lines) but is sub-CONF enriched (E=1.37×/14). The dominant cth→d bigram pairs are cthol→daiin (6) and cthy→daiin (6) — both involving daiin as the d-class word. The d↔cth coupling operates throughout lines, not as a specific terminal formula. Inter-line coupling (cth-LF → d-LF successor) is flat (E=1.13×/17). **H_new_FV RESOLVED NEGATIVE**: The [cth@LL][d@LF] specific formula hypothesis is NOT confirmed — the mutual coupling is a distributed within-line word-adjacency effect, not a terminal slot formula.
**Experiment:** exp_559 (2026-04-11)
**Date:** 2026-04-11
**Finding:** d-LF lines with any cth: E=1.29×/47 (sub-CONF). [cth@LL][d@LF] exact: 14 lines (E=1.37× vs MID base). Total [cth→d] bigrams: 37; position split MID=21, LL→LF=14. Most common pairs: cthol→daiin (6), cthy→daiin (6). Cth-LF lines followed by d-LF successor: E=1.13×/17 (flat). The cth→d CONF bigram (F602) is a real word-adjacency enrichment but it operates position-independently within lines. The [qot pos1]...[cth@LL][d@LF] formula is directional from N=14 formula lines (qot: E=5.92×/3 → underpowered).
**Limitation:** Formula-line pos1 profile: N=14 only. Cth@LL in d-LF lines: E=1.37×/14 is sub-CONF (need E≥1.5). The negative result is solid — the enrichment exists but is well below the level needed to claim a dominant terminal formula.
**Commitment status:** Not committed.
**Magnitude context:** The d↔cth mutual coupling (E=1.97× both directions) is a robust word-adjacency effect (within-line co-occurrence enrichment) but NOT a positional template (specific slot assignment). This contrasts with, e.g., the p-pos1 CONF formula (E=5.23×/27) where p is genuinely slot-restricted. Cth and d co-occur at elevated rates anywhere they appear adjacent — which is consistent with them being semantically/functionally related word classes rather than grammatically slot-constrained partners.

---

## Summary

- **H_new_FV CLOSED (negative)**: [cth@LL][d@LF] terminal formula NOT confirmed.
- [cth→d] coupling (F602, E=1.97×/37) is distributed across line positions (57% MID, 38% LL→LF).
- [cth@LL][d@LF] exists (14 lines) but E=1.37× sub-CONF.
- Inter-line coupling cth-LF → d-LF: flat (E=1.13×).
- The d↔cth mutual coupling is a word-adjacency enrichment, not a terminal slot formula.
- Dominant cth→d pairs: cthol→daiin (6), cthy→daiin (6) — daiin is the primary d-class partner.
- [qot opener]...[cth@LL][d@LF] direction-only from N=14 (requires more data).

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. MID baseline correctly excludes LF and pos1 words. Bigram position logic verified (LL is index L-2, LF is L-1; LL→LF pair is at i=L-2).

**Extrapolation**: None beyond thresholds. The negative result is clearly stated with actual E-values. The [qot pos1] directional result is correctly flagged as underpowered (N=14).

**Negative-result scope**: This is a principled negative — H_new_FV tested a specific formula prediction and found sub-CONF enrichment throughout. The underlying coupling (F602) remains valid; only the "specific terminal formula" interpretation is rejected.

**Control behavior**: No separate control needed — corpus-internal baseline throughout.
