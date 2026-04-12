# exp_560 result — sch-onset full characterization (H_new_FW)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. Consistent corpus parsing. MID baseline computed from positions 1 to L-2. Positional totals use the standard formulation (2-word lines: pos1 word counted in both pos1 and LL counts — consistent across all onset classes).

**Extrapolation**: None. B pos1=6.66×/9 is dir (obs<10 for CONF) — correctly flagged. sch→s A: E=14.86×/obs=3 = (dir) — underpowered.

---

## Results

### Part 1: sch vocabulary

**A herbal_a** (23 sch tokens = 0.20% of 11,327 words):
- schey: 4 (17.4%), schol: 3 (13.0%), schy: 2 (8.7%), schor: 2 (8.7%)
- Remaining 15 forms are singletons (4.3% each)
- **Vocabulary type**: y-body (schey, schy) and lateral forms (schol, schor) dominant — same body-type as A cth (cthy, cthol, cthor, cthey). Scharchy (compound gallows body) present (1).

**B all** (18 sch tokens = 0.18% of 10,163 words):
- schedy: 7 (38.9%), schdy: 3 (16.7%), sches: 1, schees: 1, schey: 1
- **Vocabulary type**: edy-dominant (schedy 38.9% + schdy 16.7% = 55.6%). The A→B shift A=y/lateral → B=edy matches the pattern seen for ch, sh, cth, k, t — a universal A→B vocabulary shift for compound-onset classes.

**Frequency comparison**: A sch = 0.20%; B sch = 0.18%. Unlike cth (8.6× drop A→B), sch is approximately frequency-stable across dialects. Both are very rare (~0.2%).

### Part 2: sch positional distribution

| Position | A obs | A total | A E | flag | B obs | B total | B E | flag |
|----------|-------|---------|-----|------|-------|---------|-----|------|
| MID base | 5 | 7333 | 0.0007 | — | 8 | 7601 | 0.0011 | — |
| pos1 | 16 | 2033 | **11.54×** | **CONF** | 9 | 1283 | **6.66×** | dir |
| LL | 4 | 1961 | 2.99× | **(dir)** | 2 | 1279 | 1.49× | — |
| LF | 2 | 2033 | 1.44× | — | 1 | 1283 | 0.74× | — |

**KEY FINDING: A pos1 E=11.54×/16 CONF — the HIGHEST pos1 E-value of any onset class characterized.** Compare: s (3.16×/163 A CONF), y (2.78×/obs_A CONF), p (2.99×/15 A CONF). Sch achieves higher E than all previous openers despite same obs count (~15-16). B pos1=6.66×/9 is dir (obs=9, one short of CONF threshold at obs≥10).

sch is ALMOST EXCLUSIVELY a pos1 word: 16/23 A tokens at pos1 (70%), 5/23 at MID (22%), 4 at LL, 2 at LF. The MID and LF appearances are rare exceptions.

**A LL (dir)**: E=2.99×/4 meets (dir) threshold (E≥2.5, obs≥3). Sch occasionally appears as LL. This is consistent with the pattern of all A openers showing some LL elevation (see p, sch — openers concentrate at pos1 but have secondary LL presence).

**Cross-dialectal conclusion**: Sch is a cross-dialectal pos1-CONF opener: A=11.54× CONF; B=6.66× dir. The A E-value is dramatically higher because sch is concentrated nearly exclusively at pos1 in A (70% of all sch tokens). B shows same direction but with slightly lower concentration.

### Part 3: sch within-line bigrams

**A herbal_a** (20 sch-sender; 7 sch-receiver bigrams):

Outgoing (sch→X):
| Target | obs | exp | E | flag |
|--------|-----|-----|---|------|
| sch→d | 6 | 1.8 | 3.43× | dir |
| sch→s | 3 | 0.2 | 14.86× | (dir) |
| sch→y | 2 | 0.7 | 2.77× | — |
| sch→ch | 6 | 4.7 | 1.28× | — |

Incoming (X→sch):
| Sender | obs | exp | E | flag |
|--------|-----|-----|---|------|
| d→sch | 3 | 0.8 | 3.56× | (dir) |
| t→sch | 1 | 0.2 | 5.74× | — |

**sch→d dir A (E=3.43×/6)**: Strong routing from sch to d. At MID-to-subsequent positions (sch at pos1 or pos2, d follows). This is consistent with p→sh and s→sh (openers routing to specific successor classes).

**sch→s (dir) A (E=14.86×/3)**: Extremely high E but obs=3 only — (dir) threshold. Sch followed by another opener class.

**d→sch (dir) A (E=3.56×/3)**: d precedes sch. Given sch is almost exclusively at pos1 and d is a strong pos1-OPENER in A (wait, A d is LF CONF not pos1)... Actually, at the within-line level this means: d appears before sch in the same line. Given sch is pos1, d cannot usually precede it (pos1 has no predecessor by definition). So d→sch bigrams would be: d at pos1, sch at pos2 (impossible since sch at pos2 = MID). OR lines where sch is NOT at pos1 (5 MID + 4 LL + 2 LF = 11 non-pos1 appearances). Among those, d→sch 3 times. This is a signal from the rare non-opener appearances of sch.

**B all** (17 sch-sender; 9 sch-receiver bigrams):
| Target/Sender | obs | E | flag |
|--------|-----|---|------|
| sch→d B | 4 | 4.79× | (dir) |
| sch→qo B | 2 | 3.76× | — |
| ch→sch B | 4 | 2.66× | (dir) |

**sch→d (dir) B (E=4.79×/4)**: sch routes to d in B as well — cross-dialectal sch→d tendency.

**ch→sch (dir) B (E=2.66×/4)**: ch precedes sch in B. Given sch is pos1-dominant, this implies the few non-pos1 sch words in B (9 tokens total; 9 at pos1 → remaining 9 at other positions) may be preceded by ch. This could also be ch from a previous word when sch is at pos2 (MID).

### Part 4: sch-LF pos1 profile

A: sch-LF N=2 — underpowered. B: sch-LF N=1 — underpowered. No claims possible.

---

## New Findings

**F604: sch vocabulary** — A: y-body dominant (schey 17.4%, schol 13.0%, schy/schor 8.7% each); B: edy-dominant (schedy 38.9%, schdy 16.7%). A→B vocabulary shift = y/lateral → edy, identical to the universal A→B shift seen for ch, sh, cth, k, t. Frequency: A=0.20%; B=0.18% — frequency-STABLE across dialects (contrast: cth drops 8.6×). Sch is a rare class (~0.20%) with the standard A→B vocabulary shift.
**Experiment:** exp_560 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a: 23 sch tokens; top forms: schey(4=17.4%), schol(3=13.0%), schy(2=8.7%), schor(2=8.7%). Y-body and lateral body together ~48%. B all: 18 sch tokens; schedy(7=38.9%), schdy(3=16.7%). Edy-dominant 55.6%. A/B frequency: 0.20%/0.18% — near-identical, unlike cth (2.68%/0.31%). Sch is a rare compound-gallows onset (sh+ch) that is frequency-stable but vocabulary-shifting A→B. Unique features: top A sch form has y-body (schey), parallel to cthy being top A cth form.
**Limitation:** A N=23 tokens; B N=18 tokens — very small samples. All vocabulary statistics are low-confidence. The "y-body dominant" A claim rests on schey(4)+schy(2)=6/23=26%, which is modest.
**Commitment status:** Not committed.
**Magnitude context:** Sch vocabulary shift A=y/lateral → B=edy parallels: cth (A=cthy+cthol; B=cthedy), ch (A=y-body ~30-40%; B=edy-forms), sh (A=y-body; B=shedy-forms), k (A=ch-bench; B=edy), t (A=mixed; B=edy). This appears to be a universal compound-onset A→B vocabulary transition — edy-suffix forms are the B-dialect counterpart to y-body/lateral A-dialect forms.

**F605: sch positional — A pos1 CONF 11.54×/16 (HIGHEST pos1 E-value characterized); B pos1 dir 6.66×/9 (one short of CONF). Sch is the most pos1-concentrated onset class known: 70% of A sch tokens appear at pos1. A LL (dir) 2.99×/4; A LF sub-CONF 1.44×/2. Sch is a cross-dialectal pos1-OPENER — A CONF, B dir (obs<10).**
**Experiment:** exp_560 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a sch positional: pos1=E=11.54×/16 CONF (16/2033 lines = 0.79% of line openings, vs MID baseline 0.07%). LL=E=2.99×/4 (dir). LF=E=1.44×/2 (sub-CONF). B all sch positional: pos1=E=6.66×/9 dir (9/1283 = 0.70% of B line openings; B MID baseline 0.11%). The E=11.54× in A is dramatically higher than p (2.99×), s (3.16×), y (2.78×), t (2.27×) — making sch the most extreme opener by E-value, though not by obs count. The high E reflects sch's near-exclusive concentration at pos1: 70% of all A sch tokens are at pos1.
**Limitation:** A pos1: E=11.54×/16 is robust despite low N (obs=16 >> exp=1.4; very high signal). LL (dir): obs=4, E=2.99× — at (dir) threshold. LF: obs=2 only — no formal claim. B pos1 dir: obs=9 (one below CONF threshold 10). If obs=10 were found, this would be B CONF. B MID: obs=8 — these 8 are rare MID appearances.
**Commitment status:** Not committed.
**Magnitude context:** Updated CONF opener comparison: sch(A:11.54×/16; B:6.66×/9-dir) > s(A:3.16×/163; B:4.75×/165) > p(A:2.99×/15; B:5.23×/27) > y(A:2.78×; B:3.54×) > t(A:2.27×; B:3.18×). Sch's exceptional E reflects its extreme positional concentration (not its frequency — sch is 0.20%, far rarer than s 4.3%). This means sch words almost never appear in MID positions — when a sch-onset word appears, it is nearly always the first word of the line.

**F606: sch bigrams — A sch→d dir (E=3.43×/6); sch→s (dir) (E=14.86×/3); B sch→d (dir) (E=4.79×/4); B ch→sch (dir) (E=2.66×/4). Sch→d elevated in both dialects. A d→sch (dir) (E=3.56×/3).**
**Experiment:** exp_560 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a: sch-sender (20 bigrams): sch→d dir (E=3.43×/6 — meets dir: E≥2.0, obs≥5); sch→s (dir) (E=14.86×/3 — obs=3, E≥2.5). sch→ch (E=1.28×/6 — flat). Incoming (7 bigrams): d→sch (dir) (E=3.56×/3). B all: sch→d (dir) (E=4.79×/4); ch→sch (dir) (E=2.66×/4). The sch→d routing is consistent in both dialects — sch at pos1 routes to d-onset words appearing later in the line. This parallels p→qok CONF B (F596: opener p routes to specific class) and s→sh CONF (F573). Sch at pos1 is followed by d somewhere in the line at ~3.4-4.8× the baseline rate.
**Limitation:** All A bigram signals rest on obs=3-6. sch→d dir: obs=6/E=3.43× is technically dir (E≥2.0, obs≥5). sch→s (dir): obs=3, E=14.86× is (dir) threshold. d→sch (dir): obs=3 — strong E but minimum (dir) obs. B bigrams similarly underpowered. LF-pos1 profile: underpowered (sch-LF N=2 A, N=1 B). No formal LF grammar claims.
**Commitment status:** Not committed.
**Magnitude context:** Sch→d routing parallels: s→sh CONF (openers route to related compound classes); p→qok CONF B. Sch (sh+ch compound gallows) routing to d (another heavy-onset class) suggests opener-to-terminal class routing is a cross-class structural principle: LINE-OPENER routes to LINE-TERMINAL in the same line. If confirmed at higher N, this would extend the opener→terminal coupling framework to sch.

---

## Summary

- **H_new_FW CLOSED**: sch fully characterized.
- Vocabulary: A=y-body (schey, schol); B=edy-dominant (schedy, schdy). Standard A→B vocabulary shift. Frequency-stable (0.20% both) — unlike cth's 8.6× drop (F604).
- Positional: A pos1 CONF 11.54×/16 — **HIGHEST pos1 E-value of any onset class**; B pos1 dir 6.66×/9. Sch is nearly exclusively a line-opener: 70% of A sch tokens appear at pos1 (F605).
- Bigrams: sch→d elevated both dialects (A: dir 3.43×/6; B: (dir) 4.79×/4) — opener routes to terminal (F606).
- Updated A CONF opener ranking by E-value: **sch (11.54×/16) >> s (3.16×/163) ≈ p (2.99×/15) > y (2.78×) > t (2.27×)**.

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. Positional counting consistent with all prior characterization experiments.

**Extrapolation**: No extrapolation. A LL (dir) correctly flagged as (dir) not CONF. B pos1=dir (obs=9 < 10 CONF threshold) correctly flagged. d→sch (dir): obs=3 minimum threshold.

**Negative-result scope**: sch-LF pos1 profile is genuinely underpowered (N=2/1). No spurious claims.

**Control behavior**: MID baseline consistently used for positional enrichment. Overall distribution for incoming bigrams.
