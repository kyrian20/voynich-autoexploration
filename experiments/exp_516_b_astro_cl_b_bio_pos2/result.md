# exp_516: B astro CL Survey + B bio pos2 survey

**Questions H_new_DE + H_new_CD**
- H_new_DE: Does F444's B astro ch→qot CL survive section-specific baseline? What CL rules does B astro have?
- H_new_CD: Does B bio have confirmed pos2 rules?

**Method:** B astro: within-folio consecutive LF-onset pairs, section-specific LF baselines. B bio pos2: len≥3, all LF classes.

---

## H_new_CD: CORPUS LIMITATION

**B bio (f117+) is not in the ZL3b corpus.** The corpus contains B-dialect folios up to f116 only. B bio (the balneological/bath section, f117-f170) is absent. H_new_CD cannot be answered from this corpus.

---

## B astro CL Survey: H_new_DE ANSWERED

B astro: 10 folios, 700 lines, 690 within-folio pairs.

B astro LF distribution: ol(14.9%) > ch(12.1%) > l(11.9%) > d(11.3%) > qok(10.7%) > ok(5.3%) > sh(5.0%) > ot(4.3%)

### NEW CONF: F495 — B astro qok-LF → qok-LF at next line (E=1.77×/N=14)

obs=14/exp=7.92 → E=1.77×(CONF, E≥1.5×/N≥10). qok-terminal lines in B astro are followed by qok-terminal lines at 1.77× baseline. B astro's dominant template class (qok, 10.7% of LF lines) shows CL self-succession — the same onset class appears at LF in consecutive lines.

This is the ONLY confirmed CL rule in B astro with section-specific baseline.

### F444 B astro ch→qot CL: CORRECTED (does not survive section-specific baseline)

F444 claimed B astro ch→qot CL (E=1.9×/N=6) from a combined B-dialect mixed-section survey.

With B astro section-specific baseline:
- **ch→qot: E=1.14×/N=3** — FLAT. Below all thresholds.
- **qot→ch: E=1.90×/N=5** — directional in the REVERSED direction (below dir threshold: N=5 but E<2.0)

**F444's B astro ch→qot CL is a mixed-section baseline artifact.** Same correction as B herbal (exp_515). B astro's ch-LF rate (12.1%) was underestimated by the combined B-dialect baseline, inflating the ch→qot apparent enrichment.

### All B astro CL findings (E≥1.5×, obs≥3):

| A→B | obs | exp | E | Status |
|-----|-----|-----|---|--------|
| qok→qok | 14 | 7.92 | 1.77× | **CONF** |
| d→qo | 8 | 2.56 | 3.13× | dir |
| ol→o | 7 | 3.08 | 2.28× | dir |
| ok→sh | 4 | 1.82 | 2.19× | — |
| ok→ok | 4 | 1.93 | 2.07× | — |
| d→y | 4 | 1.45 | 2.77× | (dir) |
| ot→o | 3 | 0.89 | 3.38× | (dir) |
| a→a | 3 | 0.56 | 5.33× | (dir) |
| sh→qot | 3 | 1.08 | 2.77× | (dir) |
| ot→s | 3 | 1.06 | 2.84× | (dir) |
| qot→ch | 5 | 2.63 | 1.90× | — |
| ch→ok | 7 | 4.43 | 1.58× | — |
| qok→sh | 6 | 3.70 | 1.62× | — |
| sh→d | 6 | 3.89 | 1.54× | — |

Notable directionals:
- **d→qo (E=3.13×/N=8, dir)**: d-terminal → qo-terminal. High E. Parallel to d→qot in A herbal_a (F491, but qot not qo). B astro d-LF routes to qo at CL level.
- **ol→o (E=2.28×/N=7, dir)**: ol-terminal → o-terminal.
- **qot→ch (E=1.90×/N=5)**: Just below dir threshold (E<2.0). A herbal_a has qot→ch CONF (F490). B astro shows the same direction but below threshold.
- **sh→d (E=1.54×/N=6)**: sh→d at CL level parallels F441 (B d+aiin→sh CL: shedy→d cross-line).

### A/B CL Inversion Summary (Updated)

| CL pair | A herbal_a | B astro | Status |
|---------|-----------|---------|--------|
| qot→ch | E=1.86×/N=11, CONF (F490) | E=1.90×/N=5 — below dir | SAME direction; A confirmed, B borderline |
| ch→qot | FLAT | E=1.14×/N=3 — FLAT (F444 corrected) | NOT an inversion — both flat |
| qok→qok | — | E=1.77×/N=14, CONF (F495) | B-specific CL self-succession |
| d→qot | E=1.52×/N=13, CONF (F491) | qot very rare — 0 obs | A-specific |

The previously claimed "A/B CL inversion (A qot→ch vs B ch→qot)" rested on F444's ch→qot claim. With section-specific baseline, B astro ch→qot is FLAT. The "inversion" was a mixed-section artifact. Both sections show qot→ch in the SAME direction (A confirmed, B borderline).

---

## Self-Audit

**Target-awareness:** No mechanism parameters, no VMS target calibration. Pure descriptive survey.

**Feature-destroying:** None. Within-folio pairs for CL (correct methodology); len≥3 for pos2 (not applicable here).

**Extrapolation:** "F444 ch→qot does not survive section-specific baseline" is within the tested data — obs=3/exp=2.63, directly computed.

**Negative-result scope:** B bio corpus absence is a data limitation, not a structural conclusion. B bio may have pos2 grammar; we cannot test it.

**Control behavior:** N/A — no control distribution.

**H_new_DE ANSWERED:** F444's B astro ch→qot CL is a mixed-section baseline artifact (E=1.14×/N=3 with section-specific baseline). B astro's ONLY confirmed CL rule is qok→qok self-succession (F495, E=1.77×/N=14, NEW CONF). Directionals: d→qo (E=3.13×/N=8), ol→o (E=2.28×/N=7). The A/B CL "inversion" for ch/qot was an artifact.

**H_new_CD ANSWERED:** B bio is not in the ZL3b corpus. Cannot be tested.
