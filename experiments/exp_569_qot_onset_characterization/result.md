# exp_569: qot-onset full characterization (H_new_GG)

**Date:** 2026-04-11
**Hypothesis tested:** H_new_GG — qot-onset full characterization
**Status:** RESOLVED — F630 (vocabulary), F631 (positional), F632 (bigrams)

---

## PART 1: VOCABULARY

A herbal_a: 291/11327 (2.57%), 69 types.
Top-15: qotchy(39=13.4%), qoty(28=9.6%), qotaiin(23=7.9%), qotol(18=6.2%), qotar(16=5.5%), qotor(14=4.8%), qoteey(13=4.5%), qotal(13=4.5%), qotchor(11=3.8%), qotchol(10=3.4%), qotchey(7=2.4%), qotain(7=2.4%).

B all: 426/10163 (4.19%), 72 types.
Top-15: qotedy(57=13.4%), qoteedy(56=13.1%), qotain(39=9.2%), qotal(33=7.7%), qotaiin(31=7.3%), qotar(26=6.1%), qoty(24=5.6%), qoteey(15=3.5%), qotey(15=3.5%), qotol(11=2.6%), qotchedy(11=2.6%).

A vocabulary: ch-body dominant (qotchy 13.4% + qotchor/qotchol/qotchey = ~10% more ch-bench forms). Unlike other classes where aiin-body leads in A, qot leads with ch-bench body in A.

A→B: frequency INCREASES (2.57%→4.19%, ~1.6×); edy convergence (qotedy+qoteedy = 26.5% of B qot tokens). Same direction as qo (2.59%→3.09%), qok (7.30%→15.13%), ot (4.84%→6.69%).

**→ F630**

---

## PART 2: POSITIONAL DISTRIBUTION

A herbal_a (baseline=2.57%):
- pos1: obs=73, E=1.40× (sub-CONF; **CORRECTS prior 1.79×/59 CONF from F539**)
- MID: obs=131, E=0.92× (flat)
- LL: obs=41, E=0.89× (flat)
- LF: obs=46, E=0.91× (flat)

B all (baseline=4.19%):
- pos1: obs=37, E=0.69× DEPL (confirmed; prior data showed 0.60×)
- MID: obs=286, E=1.08× (flat)
- LL: obs=57, E=1.07× (flat)
- LF: obs=46, E=0.86× (sub-baseline, NOT DEPL)

Key findings:
- **A qot pos1 = 1.40×/73: sub-CONF — CORRECTS prior 1.79×/59 (F539)**. Like qok (corrected 1.47→0.87) and ot (corrected 1.29→0.77), canonical methodology lowers the E-value. At 1.40×, qot is elevated but below the 1.5× CONF threshold. Qot is NOT confirmed as an A CONF opener.
- B pos1 = 0.69×/37 DEPL: confirmed.
- All other positions near-flat in both dialects. Qot has a nearly flat positional profile — no strong enrichment in any slot.

**→ F631**

---

## PART 3: BIGRAMS

### Outgoing from qot (MID-baseline)

A herbal_a (sender=243):
- qot→qot: obs=18, E=2.88× **CONF** (strong self-succession)
- qot→o: obs=5, E=0.43× DEPL
- qot→a: obs=5, E=0.47× DEPL
- qot→ol: obs=5, E=0.52× DEPL
- qot→sh: obs=14, E=0.70× (near-DEPL, NOT DEPL by threshold)

B all (sender=380):
- qot→ot: obs=45, E=1.77× **CONF** (confirms F629)
- qot→qot: obs=29, E=1.82× **CONF**
- qot→r: obs=10, E=1.97× **CONF** (new)
- qot→sh: obs=24, E=0.67× DEPL
- qot→ok: obs=14, E=0.56× DEPL
- qot→y: obs=8, E=0.65× DEPL
- qot→a: obs=8, E=0.58× DEPL
- qot→qo: obs=6, E=0.51× DEPL

### Incoming to qot (overall-baseline)

A herbal_a (receiver=218):
- qot→qot: obs=18, E=3.21× **CONF** (incoming self-succession perspective)
- t→qot: obs=11, E=2.03× **CONF** (confirms F576)
- o→qot: obs=5, E=0.48× DEPL
- a→qot: obs=5, E=0.52× DEPL
- ol→qot: obs=3, E=0.35× DEPL

B all (receiver=389):
- sh→qot: obs=72, E=1.97× **CONF** (confirms F617)
- qot→qot: obs=29, E=1.78× **CONF** (incoming self-succession)
- d→qot: obs=18, E=0.63× DEPL
- ok→qot: obs=14, E=0.55× DEPL
- a→qot: obs=3, E=0.21× DEPL (extreme)
- s→qot: obs=4, E=0.38× DEPL
- qo→qot: obs=8, E=0.67× DEPL
- o→qot: obs=7, E=0.64× DEPL

Self-succession: A=2.93×; B=1.86×

### qot-LF pos1 profile

A herbal_a (48 qot-LF lines):
- qot@pos1: obs=7, E=4.06× dir
- sh@pos1: obs=7, E=2.00× dir
- ot@pos1: obs=4, E=2.23× dir (but obs=4 — underpowered)
- y@pos1: obs=5, E=0.63× DEPL

B all (46 qot-LF lines):
- y@pos1: obs=3, E=0.57× DEPL (minimum obs)
- d@pos1: obs=13, E=1.47× (sub-CONF)
- s@pos1: obs=9, E=1.51× (sub-CONF at obs=9 — below 10 threshold)

**→ F632**

---

## AUDIT NOTES

1. **A qot pos1 correction**: 1.40×/73 — sub-CONF. F539 value (1.79×/59) was from pre-canonical methodology. Canonical result lowers E-value below threshold. Working_position.md must be updated.

2. **B qot pos1 DEPL confirmed**: E=0.69×/37 (prior 0.60×). DEPL threshold = 0.70×; E=0.69 < 0.70. The B pos1 DEPL is confirmed but the magnitude is less extreme than before.

3. **B qot→r CONF (1.97×/10)**: New finding. B qot routes to r (the strongest B LF class). Parallel to B qok→r CONF (1.95×/30, F620). Both q-bench template classes route to r in B.

4. **A qot-LF pos1**: The dir signals (qot 4.06×/7, sh 2.00×/7) are below CONF threshold (obs=7 < 10). Not formally CONF but directionally suggestive. qot-LF lines in A tend to open with qot or sh at pos1 — the only A LF class where the LF class itself appears at pos1 at dir rate.

5. **A t→qot CONF confirmed**: E=2.03×/11 (F576: 2.01×/11 — essentially identical). Robust.

6. **B sh→qot CONF confirmed**: E=1.97×/72 (F617: 1.77×/72 — same obs, slight E difference due to baseline methodology). Both CONF.

7. **qot→ch in A flat (E=1.19×/57)**: qot does NOT strongly route to ch in A despite ch being the most frequent A class. This is structurally notable — qot is neutral toward ch.

---

## SUMMARY

H_new_GG RESOLVED. Qot-onset is characterized:

**F630 (vocabulary)**: A=2.57% ch-body dominant (qotchy 13.4%); B=4.19% edy-dominant. A→B INCREASES (~1.6×). Qot A vocabulary unusually ch-dominated compared to other classes.

**F631 (positional)**: A pos1=1.40×/73 sub-CONF (CORRECTS prior 1.79×/59 CONF — qot is NOT a confirmed A opener); B pos1=0.69×/37 DEPL (confirmed). All other positions near-flat in both. Qot is a flat/neutral class in A, B MID class.

**F632 (bigrams)**: Strong cross-dialectal self-succession (A:2.88-3.21×/18; B:1.82-1.86×/29); B: sh→qot CONF(1.97×/72, confirms F617), qot→ot CONF(1.77×/45, confirms F629), qot→r CONF(1.97×/10 new); A: t→qot CONF(2.03×/11, confirms F576); qot→a/o/ol DEPL cross-dialectally; B: extensive outgoing DEPL (qot→sh/ok/y/a/qo DEPL).
