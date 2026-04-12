# exp_512: CL Chain Verification + ok-LF Co-occurrence + CL Scope + Pos2 Self-Chain Audit

**Questions addressed:** H_new_CV (d→qot→ch triple), H_new_CU (ok-LF pos2/pen co-occurrence), H_new_CT (CL scope A cosmo/B herbal)

**Incidental discovery:** F461–F467 pos2 self-chaining findings are systematically inflated by 2-word-line baseline inconsistency. Universal pos2 self-chaining (F468) is retracted.

---

## PART 1: H_new_CV — d→qot→ch triple chain (A herbal_a)

| Test | obs | exp | E | Status |
|------|-----|-----|---|--------|
| d→qot→ch (triple) | 4 | 1.39 | 2.87× | (dir) N=4 |
| d→*→ch (any middle) | 50 | 48.73 | 1.03× | FLAT |

**d→qot→ch is (dir) elevated** (E=2.87×/N=4). The triple exceeds the chance level (~1.39 expected) at 2.87×. The path d→qot→ch is the specific route — d→anything→ch overall is FLAT (1.03×), showing the chain is mediated specifically by qot.

After d→qot, next LF: ch=4, d=2, a=1, o=1, y=1, e=1 (N=10 total d→qot transitions).
Before qot→ch, prior LF: d=4, ch=2, others=1 each (N=10 qot→ch transitions ending in ch).

4 of the 10 d→qot transitions continue to ch; 4 of the 10 qot→ch transitions were preceded by d. The chain is structurally coherent but N=4 for the triple falls below dir (need N≥5) or (dir) (need N≥3 — meets). **Status: (dir) at E=2.87×/N=4.**

H_new_CV ANSWERED: d→qot→ch chain is suggestive (E=2.87×) but not confirmed as a unit. The pairwise rules (F490, F491) are confirmed; the triple is directional.

---

## PART 2: H_new_CU — A herbal_a ok-LF pos2/pen co-occurrence

| Rule | obs/N_elig | E | Reproduced? |
|------|-----------|---|-------------|
| pos2=ok | 6/81 (7.4%) | 1.66× | Below CONF — see F467 issue below |
| pen=ok | 12/81 (14.8%) | 2.73× | F485 reproduced (CONF) |
| BOTH | 3/81 | E=3.38× | (dir) |

**ok-LF pos2+pen co-occurrence: E=3.38×/N=3 (dir)** — above baseline, below CONF.

H_new_CU ANSWERED: ok-LF pos2 AND pen both having ok onset is above baseline (E=3.38×/N=3). Directional at E≥2.5×/N≥3. The two rules are positively correlated (not independent). But N=3 is too small for confirmation.

### INCIDENTAL: F467 pos2 reproduction discrepancy → systemic correction

F467 claimed ok-self@pos2 E=4.53×/N=10 (CONF). But with correct len≥3 methodology: **obs=6/81, E=1.66×** — below CONF (N<10 and E<2.0×). This reproduces the same 2-word-line bug that affected F465.

Systematic check (detailed below in PART 4) reveals ALL A herbal_a pos2 self-chaining findings (F461–F467) are inflated by the same artifact.

---

## PART 3: H_new_CT — CL scope in A cosmo and B herbal

### d→qot CL scope

| Section | obs | exp | E | N_pairs |
|---------|-----|-----|---|---------|
| A herbal_a | 13 | 7.92 | 1.64× CONF | 1133 |
| A cosmo | 2 | 1.07 | 1.86× | 441 |
| B herbal | 0 | 0.13 | 0× | 258 |

A cosmo d→qot: E=1.86×/N=2 — above baseline but N too small. Not confirmed.
B herbal d→qot: obs=0. d-LF frequency in B herbal is 13.2%, qot very rare (0.4%). N too small.

### qot→ch CL scope

| Section | obs | exp | E | N_pairs |
|---------|-----|-----|---|---------|
| A herbal_a | 12 | 6.00 | 2.00× CONF | 1133 |
| A cosmo | 3 | 1.36 | 2.20× | 441 |
| B herbal | 1 | 0.16 | 6.10× | 258 |

A cosmo qot→ch: E=2.20×/N=3 — above baseline, N too small. Consistent direction with A herbal_a.
B herbal qot→ch: N=1, meaningless.

**Both rules are directionally consistent in A cosmo but not confirmed there (N too small). Both are essentially unobservable in B herbal (qot too rare). These CL rules cannot be determined as A-herbal_a-specific based on this data — A cosmo has consistent direction but insufficient N.**

### NEW CONF: A cosmo ch→ok CL (E=2.01×/N=12, CONF)

| Rule | obs | exp | E | Status |
|------|-----|-----|---|--------|
| ch→ok | 12 | 5.96 | 2.01× | **CONF** |

A cosmo ch-terminal lines are followed by ok-terminal lines at 2.01× the section baseline (N=12, E≥1.5× and N≥10). This is A cosmo's only confirmed CL rule. Compare: A herbal_a ch is a "receiving" class (qot→ch); A cosmo ch is a "sending" class (ch→ok). ch-LF grammar differs between A sections for CL too.

Additional A cosmo directionals: ol→a (E=3.54×/N=7, dir), sh→o (E=3.61×/N=5, dir), a→a (E=2.29×/N=5, dir).

H_new_CT ANSWERED: F490/F491 are directionally consistent in A cosmo but not confirmed (N too small). F490/F491 cannot be declared A-herbal_a-specific yet. A cosmo has its own confirmed CL rule: ch→ok (F492, NEW CONF).

---

## PART 4: Systemic pos2 self-chain correction (incidental from PART 2)

Full A herbal_a pos2 self-chaining re-analysis with consistent len≥3 methodology (both observation eligibility AND baseline computed from len≥3 lines):

| LF class | N_2word | len≥2 E | len≥3 E | N_obs | Original finding | Corrected status |
|----------|---------|---------|---------|-------|-----------------|-----------------|
| d | 18 | 1.72× | 1.12× | 28 | F465 RETRACTED | FLAT |
| ch | 29 | 1.57× | 1.34× | 80 | F461 CONF (E=1.60×) | **BELOW CONF** (E<1.5×) |
| ok | 8 | 3.53× | 1.66× | 6 | F467 CONF (E=4.53×) | **BELOW CONF** (N<10) |
| cth | 9 | 4.26× | 1.72× | 5 | F466 CONF (E=3.46×) | **BELOW CONF** (N<10) |
| o | 7 | 5.42× | 2.29× | 4 | F464 CONF (E=7.03×) | **BELOW CONF** (N<10) |
| sh | 8 | 2.55× | 1.53× | 8 | F463 CONF (E=2.64×) | **BELOW CONF** (N<10) |
| ot | 3 | 3.89× | 1.65× | 2 | — dir | **below** |
| k | 8 | 4.32× | 1.73× | 4 | — dir | **below** |
| y | 4 | 6.25× | 3.81× | 5 | — dir | **dir** (E=3.81×/N=5) |
| qok | 3 | 3.79× | 2.09× | 3 | — | **(dir)** |

**Mechanism:** For any LF class X, 2-word lines trivially have X at ws[1]=LF=X. When the BASELINE is computed from ALL lines (including 2-word lines from other LF classes), the X@pos2 baseline is not inflated by X-LF 2-word lines — but the X-LF OBSERVATION IS. This creates asymmetric upward bias specifically for self-chaining E values. With len≥3 consistently applied to both observation pool and baseline pool, the upward bias is eliminated.

**F468 (universal pos2 self-chaining) is RETRACTED.** The original claim: "ALL A herbal_a LF classes with N_elig≥10 self-chain at pos2 (E≥1.56×)." With correct methodology, NO class meets CONF. Only y-LF (E=3.81×/N=5) meets the directional threshold. The self-chaining tendency is present (all E>1.0×) but not at confirmed levels for any class.

**F461 (ch→ch@pos2, E=1.60×/N=94) must be CORRECTED:** corrected E=1.34×/N=80 — BELOW CONF. The ch self-chaining at pos2 is real but weaker than claimed; it does not survive the 1.5× confirmation threshold with correct len≥3 baseline.

**F463, F464, F466, F467:** All corrected to below CONF (N<10 with len≥3 in most cases). The self-chaining tendency at pos2 is present but modest and unconfirmed.

Cross-class pos2 rules (F457 B herbal d→sh; F477 B herbal ok→o; F478 B astro ch→ok) are NOT affected by this bug (the 2-word-line artifact only inflates self-chaining, not cross-class routing).

---

## Self-Audit

**Target-awareness:** None for PARTS 1-3. PART 4 is methodological correction, not discovery.

**Feature-destroying:** None. Consistent len≥3 for both eligibility and baseline in PART 4. CL pairs use within-folio consecutive pairs throughout.

**Extrapolation:** PART 1 triple E=2.87×/N=4: correct computation — 4 triples out of 1078, baseline=1.39. PART 2 co-occurrence E=3.38×/N=3: correct (p_pos2=6/81, p_pen=12/81, expected=0.89). PART 3 A cosmo ch→ok: obs=12/441, baseline = ch_rate × ok_rate = 9.1%×14.8% = 1.35%, exp=5.96, E=2.01×. PART 4: verified by independent script computing len≥2 vs len≥3 for each LF class — table values match.

**Scope of retraction:** F468 universal rule retracted. F461, F463, F464, F466, F467 all corrected below CONF. F465 was already retracted. ch@pos2 tendency in A herbal_a is present (E=1.34×/N=80) but not confirmed. Need to verify if F469 (B astro sh→sh@pos2) and F471 (B astro ol→ol@pos2) are similarly affected.

---

## Findings Summary

| Finding | Status |
|---------|--------|
| F492 NEW CONF: A cosmo ch→ok CL (E=2.01×/N=12) | Confirmed |
| d→qot→ch triple (E=2.87×/N=4) | (dir) — consistent with F490+F491 chain |
| ok-LF pos2+pen co-occur (E=3.38×/N=3) | (dir) — below CONF |
| F461 ch-LF ch@pos2 CORRECTED | Below CONF (E=1.34×/N=80) |
| F463 sh-LF sh@pos2 CORRECTED | Below CONF (E=1.53×/N=8) |
| F464 o-LF o@pos2 CORRECTED | Below CONF (E=2.29×/N=4) |
| F466 cth-LF cth@pos2 CORRECTED | Below CONF (E=1.72×/N=5) |
| F467 ok-LF ok@pos2 CORRECTED | Below CONF (E=1.66×/N=6) |
| F468 universal pos2 self-chaining RETRACTED | No LF class meets CONF pos2 self-chain |
| F469 B astro sh→sh@pos2 CORRECTED | Below CONF (E=1.33×/N=8, corrected from 1.59×/N=10) |
| F471 B astro ol→ol@pos2 CORRECTED | Below CONF (E=1.29×/N=12, corrected from 1.54×/N=15) |

## ADDENDUM: B astro F469/F471 inline verification (H_new_CW)

B astro (N=700 lines) pos2 self-chain audit with consistent len≥3 methodology:

| LF class | N_2word | len≥2 E | len≥3 E | N_obs | Original | Corrected |
|----------|---------|---------|---------|-------|---------|----------|
| sh | 2 | 1.57× | **1.33×** | 8 | F469 CONF | **BELOW CONF** |
| ol | 3 | 1.57× | **1.29×** | 12 | F471 CONF | **BELOW CONF** |
| ch | 4 | 1.47× | 1.22× | 15 | — | flat |
| qok | 7 | 1.31× | 0.89× | 11 | — | flat/depleted |
| d | 1 | 1.98× | **1.60×** | 4 | — | near-threshold (N<10) |

**F469 (B astro sh→sh@pos2, CONF E=1.59×/N=10) → CORRECTED: E=1.33×/N=8, BELOW CONF.** Only 2 two-word sh-LF lines in B astro (fewer than A herbal_a), but the artifact still drops E from 1.57× to 1.33×.

**F471 (B astro ol→ol@pos2, CONF E=1.54×/N=15) → CORRECTED: E=1.29×/N=12, BELOW CONF.** ol-LF is large (N=104) with 3 two-word lines.

H_new_CW ANSWERED: F469 and F471 are also below CONF with correct methodology. The 2-word-line artifact was systemic across ALL sections tested. No pos2 self-chain finding survives correction in any section.
