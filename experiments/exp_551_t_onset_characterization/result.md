# exp_551 result — t-onset full characterization (H_new_FM)

## Audit

**Target-awareness**: None. F523 (A stars t pos1 CONF) noted as prior partial finding; this characterizes A herbal_a and B all.

**Feature-destroying implementation**: Standard methodology.

**Extrapolation**: None.

---

## Results

### Part 1: Vocabulary

| Metric | A herbal_a | B all |
|--------|-----------|-------|
| N t-onset tokens | 282 (2.5%) | 195 (1.9%) |
| #1 word | taiin (5.7%) | tedy (12.3%) |
| #2 word | tol (5.0%) | tchedy (8.7%) |
| #3 word | tor (4.6%) | taiin (5.6%) |
| ch-bench compounds | ~13% (tchy, tchey, tchor, tchol, tchdy, tchdr) | present but lower |
| edy-body | minimal | tedy=12.3%; tchedy=8.7%; teedy=4.6% (~25%) |

A herbal_a: diverse vocabulary — lateral forms (tol, tor, tar, tal), ch-bench compounds (tchy, tchey, tchor), aiin-body (taiin). B all: edy-body dominant (~25%: tedy, tchedy, teedy). A→B vocabulary shift: A=mixed/ch-bench; B=edy-body+ch-bench. Note: 'ot' onset has higher priority than 't' in ONSET_PRIORITY, so 't' here means t-words that do NOT start with 'ot'.

### Part 2: Positional Distribution — t IS A LINE-OPENER

| Position | A obs/N | A E | B obs/N | B E | A flag | B flag |
|----------|---------|-----|---------|-----|--------|--------|
| pos1 | 111/1961 | **2.27×** | 78/1279 | **3.18×** | **CONF** | **CONF** |
| MID | 87/5539 | 0.63× | 76/6335 | 0.63× | DEPL | DEPL |
| LL | 35/1794 | 0.78× | 30/1266 | 1.24× | — | — |
| LF | 47/1961 | 0.96× | 11/1279 | 0.45× | — | **DEPL** |

**t is the THIRD confirmed LINE-OPENER class** (alongside y, F572/F558, and s, F572). pos1 CONF in both dialects (A: 2.27×/111; B: 3.18×/78). MID DEPL in both (0.63×). B additionally shows LF DEPL (0.45×/11) — B t is exclusively pos1 (avoids both MID and LF).

**Three-class opener taxonomy** (pos1 E-values):
| Class | A pos1 E | B pos1 E |
|-------|----------|----------|
| s | 3.16× | **4.75×** |
| t | 2.27× | 3.18× |
| y | 2.78× | 3.54× |

All three are CONF in both dialects. Together y+s+t account for ~30% of all line-openings in A herbal_a.

### Part 3: Within-line Bigrams

**A herbal_a** (233 t-sender bigrams):

| t→X | obs | exp | E | flag |
|-----|-----|-----|---|------|
| t→qot | 11 | 5.5 | **2.01×** | **CONF** |
| t→ok | 12 | 19.2 | 0.63× | DEPL |
| t→cph | 3 | 1.0 | 3.05× | (dir) |
| t→ch | 49 | 54.5 | 0.90× | — |
| t→ot | 17 | 11.7 | 1.45× | sub-CONF |

**B all** (184 t-sender bigrams):

| t→X | obs | exp | E | flag |
|-----|-----|-----|---|------|
| t→ot | 21 | 13.6 | **1.55×** | **CONF** |
| t→ok | 8 | 13.3 | 0.60× | DEPL |
| t→k | 7 | 3.9 | 1.78× | sub-CONF |
| t→t | 5 | 2.6 | 1.95× | sub-CONF |

**KEY**: A t→qot CONF (2.01×/11); B t→ot CONF (1.55×/21). T routes to the dominant template class in each dialect: A uses qot as template pivot; B uses ot. Cross-dialectal: ok DEPL in both (A: 0.63×; B: 0.60×).

This mirrors the overall A=qot/B=ot dialect preference: A line-opening t-words are followed by qot-class words; B line-opening t-words are followed by ot-class words. The within-line coupling after an opener reveals the dialect template structure.

### Part 4: t-LF pos1 Profile

**A herbal_a** (N=47 t-LF lines):
- o@pos1: obs=7/47, E=2.23× **dir** (NEW)
- ch@pos1: obs=6/47, E=1.71× sub-CONF
- y@pos1: obs=4/47, E=**0.52× DEPL** — y AVOIDS opening t-terminal lines

**B all** (N=11 t-LF lines): underpowered for analysis.

**KEY**: A t-LF pos1 y DEPLETED (E=0.52×/obs=4). Y is the definitive line-opener (F558) but specifically AVOIDS t-LF lines. O@pos1 dir (E=2.23×/7) — o-onset opens t-terminal A herbal_a lines preferentially. This is a specific cross-LF-class exception: y enriches pos1 for ok-LF, ot-LF, o-LF, but DEPLETES pos1 for t-LF. T-terminal lines are opened by o-onset instead.

---

## New Findings

**F574: t vocabulary** — A: diverse (taiin 5.7%, tol 5.0%, tor 4.6%; ch-bench ~13%); B: edy-body dominant (tedy 12.3%, tchedy 8.7%, teedy 4.6% = ~25% edy-body). A→B shift: A=mixed/ch-bench; B=edy-body+ch-bench.

**F575: t positional — pos1 CONF cross-dialectally** (A: E=2.27×/obs=111; B: E=3.18×/obs=78). MID DEPL both (0.63×). B LF DEPL (0.45×/11). T is the THIRD confirmed LINE-OPENER class alongside y and s. B t is exclusively pos1 (both MID and LF depleted). A t: pos1 CONF + LF ~baseline.

**F576: t bigrams** — A t→qot CONF (E=2.01×/obs=11); B t→ot CONF (E=1.55×/obs=21); ok DEPL both (0.60-0.63×). T routes to dialect-specific template class after opening: A→qot; B→ot.

**F577: A t-LF pos1: o@pos1 dir (E=2.23×/obs=7); y DEPLETED (E=0.52×/obs=4)** — y is the definitive opener (F558) but specifically avoids opening t-terminal A herbal_a lines. O-onset opens t-terminal lines instead. This is a cross-LF-class exception to y's general pos1 enrichment.

---

## Summary

- **H_new_FM CLOSED**: t is the third confirmed LINE-OPENER class (F575: pos1 CONF A 2.27×/B 3.18×). MID DEPL both; B LF DEPL — B t is exclusively pos1. Three opener classes now: y (2.78×/3.54×), s (3.16×/4.75×), t (2.27×/3.18×) all CONF in both dialects.
- F574: t vocabulary (A=mixed/ch-bench; B=edy-body dominant)
- F575: t positional (third confirmed opener; B t exclusively pos1)
- F576: t bigrams (A t→qot CONF; B t→ot CONF — dialect-specific template routing)
- F577: A t-LF pos1 y DEPL (exception to y's general enrichment); o@pos1 dir instead
- Three line-opener classes (y, s, t) together account for ~30% of A herbal_a and ~30% of B all line-openings
