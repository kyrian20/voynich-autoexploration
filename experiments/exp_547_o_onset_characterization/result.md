# exp_547 result — o-onset full characterization

## Audit

**Target-awareness**: None. Formal 4-part onset profile (vocabulary, positional, bigrams, o-LF pos1). Prior incidental findings (F502–F507) referenced for comparison, not targeted.

**Feature-destroying implementation**: Standard methodology matching exp_540–545. Positional distribution uses per-word position with LL=penultimate, LF=last, pos1=first, MID=remaining (len≥2 lines). Bigrams count consecutive within-line pairs with MID-position baseline. o-LF pos1 uses overall pos1-onset distribution as baseline. CL Part 5 uses same-folio consecutive line pairing.

**Extrapolation**: None. A herbal_a (n≤56) and B all (edy-filter) only.

---

## Results

### Part 1: Vocabulary

| Metric | A herbal_a | B all |
|--------|-----------|-------|
| N o-onset tokens | 541 (4.8% of words) | 287 (2.8% of words) |
| Top word | or (25.7%) | or (23.0%) |
| #2 word | odaiin (5.4%) | odaiin (4.5%) |
| #3 word | ody (3.0%) | oraiin (3.5%) |
| Dominant body class | ol/or/ar (34.9%) | y-body (31.7%) |
| edy-body | 0.0% | 13.2% |
| y-body | 19.6% | 31.7% |
| aiin-body | 16.6% | 18.5% |
| ch-bench | 9.4% | 16.4% |

**Key**: 'or' dominates both dialects at ~25%. A o-onset = ol/or/ar class dominant (minimal y-body, no edy-body). B o-onset = y-body dominant + edy-body present (13.2%). A→B vocabulary shift in o-class: A=ol/or/ar dominant; B=y-body + edy-body dominant. Parallels overall A=o-body / B=edy-body dialect shift, applied to the o-onset subclass.

### Part 2: Positional Distribution

| Position | A obs/N | A E | B obs/N | B E | A flag | B flag |
|----------|---------|-----|---------|-----|--------|--------|
| pos1 | 131/1961 | 1.40× | 36/1279 | 1.00× | sub-CONF | baseline |
| MID | 232/5539 | 0.88× | 160/6335 | 0.89× | — | — |
| LL | 72/1794 | 0.84× | 33/1266 | 0.92× | — | — |
| LF | 105/1961 | 1.12× | 57/1279 | **1.58×** | — | **CONF** |

**A herbal_a**: FLAT positional distribution. pos1=1.40× (below CONF threshold E<1.5; obs=131 provides power — genuinely sub-CONF). LF=1.12× (near-baseline). No position shows CONF or DEPL. O is the only major characterized class with no CONF positional signal in A herbal_a.

**B all**: LF CONF (E=1.58×/obs=57). pos1=1.00× baseline. B o-onset is a LF-enriched class. Contrasts with d (B d=pos1 CONF; F554) — o and d show partial positional complementarity in B: d opens lines, o closes them.

### Part 3: Within-line Bigrams

**A herbal_a** (435 sender bigrams):

| Target | obs | exp | E | flag |
|--------|-----|-----|---|------|
| o→a | 67 | 21.8 | **3.08×** | **CONF** |
| o→o | 31 | 18.0 | **1.72×** | **CONF** |
| o→ckh | 10 | 6.0 | **1.67×** | **CONF** |
| o→ch | 108 | 101.7 | 1.06× | baseline |
| o→sh | 42 | 41.2 | 1.02× | baseline |
| o→d | 24 | 38.1 | 0.63× | DEPL |
| o→qok | 19 | 35.6 | 0.53× | DEPL |
| o→ot | 13 | 21.9 | 0.59× | DEPL |
| o→k | 7 | 15.7 | 0.45× | DEPL |
| o→cth | 7 | 12.3 | 0.57× | DEPL |
| o→qo | 6 | 13.1 | 0.46× | DEPL |
| o→qot | 5 | 10.2 | 0.49× | DEPL |
| o→l | 3 | 9.5 | 0.32× | DEPL |

**B all** (229 sender bigrams):

| Target | obs | exp | E | flag |
|--------|-----|-----|---|------|
| o→a | 27 | 8.5 | **3.17×** | **CONF** |
| o→o | 13 | 5.8 | **2.24×** | **CONF** |
| o→ch | 53 | 43.6 | 1.21× | — |
| o→qok | 19 | 37.8 | 0.50× | DEPL |
| o→sh | 14 | 24.8 | 0.57× | DEPL |
| o→qot | 7 | 10.3 | 0.68× | DEPL |
| o→l | 5 | 13.2 | 0.38× | DEPL |
| o→qo | 4 | 7.2 | 0.56× | DEPL |

**KEY FINDING: o→a CONF cross-dialectally** (A: E=3.08×/obs=67; B: E=3.17×/obs=27). This is the dominant o bigram signal by far and is remarkably conserved across dialects. Within-line, an o-onset word is followed by an a-onset word at ~3× baseline rate. a-onset words include: ar, al, am, ain, aiin, etc. The o→a coupling is the strongest cross-dialectally conserved within-line bigram found for any onset class in this project.

Also conserved: o→o CONF both dialects (A: 1.72×/31; B: 2.24×/13) — o self-succession. A-specific: o→ckh CONF (E=1.67×/obs=10).

**DEPL cluster**: o strongly avoids q-class (qot, qo, qok) and simple gallows (k, l, cth) in both dialects. o→ch is FLAT (not depleted) — unlike sh which avoids ch. The DEPL targets are the template classes, which o-onset specifically rejects as successors.

### Part 4: o-LF pos1 Profile

**A herbal_a** (N=105 o-LF lines):

| Onset | obs/N | E | flag |
|-------|-------|---|------|
| y | 26/105 | **1.50×** | **CONF** |
| t | 9/105 | 1.51× | CONF |
| d | 19/105 | 1.03× | — |
| sh | 8/105 | 1.04× | — |
| qot | 1/105 | 0.26× | — |

**B all** (N=57 o-LF lines):

| Onset | obs/N | E | flag |
|-------|-------|---|------|
| y | 10/57 | **1.53×** | **CONF** |
| t | 6/57 | 1.73× | sub-CONF |
| l | 4/57 | 2.19× | sub-CONF |
| d | 11/57 | 1.00× | — |
| s | 4/57 | 0.54× | DEPL |

**y@pos1 CONF in both dialects** (A: E=1.50×/obs=26; B: E=1.53×/obs=10) — formally confirms F502/F503 at correct methodology (len≥2 pos1 baseline). This is consistent with y=LINE-OPENER (F558): y@pos1 is enriched for MULTIPLE LF classes (ok, ot, o all show y@pos1 CONF). t@pos1 is elevated in both dialects but below CONF (A: 1.51×/9; B: 1.73×/6) — directional pattern.

### Part 5: o-LF CL (Reference)

**A herbal_a** (93 CL sender pairs): o→sh CL (E=1.92×/obs=8 — sub-CONF here, consistent with F507 direction); o→y CL dir (E=2.05×/obs=7 — NEW directional); o→o CL (E=1.81×/obs=9 — sub-CONF). F507 (o→sh CONF) established in original experiment with larger N; this analysis consistent with direction.

**B all** (53 CL sender pairs): o→ot CL (E=1.97×/obs=8 — sub-CONF); mostly flat.

---

## New Findings

**F561: o vocabulary** — A o=ol/or/ar dominant (34.9%), y-body=19.6%, no edy-body; B o=y-body dominant (31.7%), ol/or/ar=27.2%, edy-body=13.2%. 'or' is top word both dialects (~25%). A→B shift: A=o-lateral-body / B=y+edy-body. Parallels overall dialect pattern.

**F562: o positional** — A herbal_a FLAT (pos1=1.40× sub-CONF; all positions 0.84–1.40×, none CONF or DEPL). B all LF CONF (E=1.58×/obs=57). O is positionally undistinctive in A; LF-enriched in B. Only characterized major class with no CONF positional signal in A herbal_a. B o LF CONF + B d pos1 CONF = partial complementarity: d opens B lines, o closes them.

**F563: o→a CONF cross-dialectally** (A: E=3.08×/obs=67; B: E=3.17×/obs=27) — dominant o bigram signal, conserved across dialects. Within a line, o-onset word is followed by a-onset word at ~3× baseline rate. Also: o→o CONF both dialects (A: 1.72×/31; B: 2.24×/13). A o→ckh CONF (1.67×/10). DEPL: o avoids q-class template (qot, qo, qok) and k, l, cth in both dialects.

**F564: o-LF pos1=y CONF cross-dialectally** (A: E=1.50×/obs=26; B: E=1.53×/obs=10) — formally confirms F502/F503 at standard methodology. y is the only CONF pos1 class for o-LF in both dialects.

---

## Summary

- **F561**: o vocabulary: A=ol/or/ar body dominant; B=y-body+edy-body (shift matches dialect pattern)
- **F562**: o positional: A FLAT (no CONF position — unique among characterized major classes); B LF CONF (1.58×/57)
- **F563 KEY NEW**: o→a CONF cross-dialectally (A: 3.08×/67; B: 3.17×/27) — dominant o bigram signal; also o→o CONF both dialects; DEPL: q-class template, k, l, cth
- **F564**: o-LF pos1=y CONF both dialects (A: 1.50×/26; B: 1.53×/10) — confirms F502/F503

**New hypothesis**: o→a cross-dialectal CONF at E≈3.1× is a strong, conserved coupling. What is the nature of the o+a phrase pair? What specific a-onset words follow o? Does this coupling persist across all B sections? Is a-onset a post-o particle/article class?
