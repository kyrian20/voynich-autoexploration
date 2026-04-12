# exp_522 result — o-LF pos2/pen grammar + A stars t-LF + H_new_CW resolution

## Audit

**Target-awareness**: No target-aware elements. All measurements are corpus observations.

**Feature-destroying implementation**: The pos1 analysis uses len≥2 (correct), and pos2/pen use len≥3 (correct). This differs from exp_521 which used len≥3 for ALL measurements including pos1. This difference causes F502/F503 E-value corrections (see below).

**Extrapolation**: The ch→o CL finding (CONF) is measured by examining predecessors of o-LF lines. This is equivalent to the standard CL metric (ch→o) viewed from the receiver side. The two perspectives are consistent.

**Negative-result scope**: A stars t-LF analysis is uninformative under current folio-number grouping (N_elig=2). F446 (t-LF elevation) was computed with per-page dialect classification. A stars t-LF grammar (H_new_EJ) is BLOCKED until the section definition is reconciled.

**Control behavior**: All uninvolved LF classes (a, ch, ok) show y@pos1 below baseline in A stars LF survey (E=0.45-0.71×), confirming o-LF y-enrichment is class-specific.

---

## H_new_EI: o-LF pos2 and pen grammar (A herbal_a)

### A herbal_a o-LF pos1/pos2/pen (N_elig pos1=35, pos2/pen=28)

| Position | Class | obs | exp | E | Flag |
|----------|-------|-----|-----|---|------|
| pos1 | y | 9 | 5.0 | 1.81× | below dir |
| pos2 | o-self | 3 | 1.0 | 3.06× | **(dir)** |
| pos2 | cth | 4 | 1.5 | 2.75× | **(dir)** |
| pen | sh | 5 | 2.5 | 1.97× | below dir |

**⚠ F502 CORRECTION — pos1 E-value:**
- With len≥2 filter (correct for pos1): N_elig=35, obs=9, E=1.81×/N=9 — **BELOW DIR** (E<2.0×)
- Previous exp_521 with len≥3 filter: N_elig=28, obs=9, E=2.26×/N=9 (incorrectly claimed dir)
- CONF still holds at POOLED level (see below)

**A herbal_a o-LF pos2 findings (NEW):**
- **o-self at pos2**: E=3.06×/obs=3 → **(dir)** threshold (E≥2.5×/obs≥3). NEW: o-LF lines have o-onset at pos2 at elevated rates. This parallels ot-LF pos2=y ((dir)) and ot-LF pos2=o (marginal).
- **cth at pos2**: E=2.75×/obs=4 → **(dir)**. NEW: cth enriched at pos2 in o-LF lines. Note: cth is enriched at pen for ot-LF (F500, dir) — related structure? Different template.

**A herbal_a o-LF pen:** No confirmed signal. sh: E=1.97×/obs=5 below dir threshold.

### y-opening vs standard pen grammar for o-LF

| Subtype | N | Notable pen | obs | E | Flag |
|---------|---|------------|-----|---|------|
| y-opening (pos1=y) | 9 | o | 2 | 10.23× | E large/N=2 |
| standard (pos1≠y) | 19 | sh | 4 | 2.33× | below dir |

Small N prevents any conclusions. y-opening o-LF subtype pen is fragmented (N=9, max obs=2 for any class). Standard subtype shows sh tendency at pen (E=2.33×/N=4, below dir threshold).

---

## H_new_EI extension: A stars o-LF pos1/pos2

| Position | Class | obs | exp | E | Flag |
|----------|-------|-----|-----|---|------|
| pos1 | y | 7 | 2.8 | 2.50× | **dir** |
| pos2 | o-self | 4 | 1.0 | 4.17× | **(dir)** |

**F503 CORRECTION:** A stars o-LF pos1=y: with correct len≥2 filter, obs=7/N_elig=14 → E=2.50×/obs=7 (dir). Previously F503 stated E=2.31×/obs=6 (from exp_521 with len≥3 filter). The upgraded obs count (7 vs 6) and E (2.50× vs 2.31×) strengthen F503.

**NEW A stars o-LF pos2 = o-self**: E=4.17×/obs=4 ((dir)). A stars o-LF lines show o-self succession at pos2 at 4× baseline. N_elig=13, so this is the 2nd (dir) finding for A stars (after F489 ch→ch@pen CONF for A stars).

**F502 CORRECTED POOLED CONF:**
- A herbal_a: obs=9, exp=5.0 (E=1.81×, below dir alone)
- A stars: obs=7, exp=2.8 (E=2.50×, dir)
- **Pooled: obs=16, exp=7.8, E=2.05×/obs=16 → CONF** (E≥1.5×/obs≥10) ✓
- F502 CONF status preserved; corrected E=2.05× (was 2.45×), corrected obs=16 (was 15)

---

## H_new_EJ: A stars t-LF grammar — BLOCKED

A stars t-LF: N_elig=2 for pos1 (only 2 lines with t at LF and len≥2). The full LF survey shows t-LF not in top classes for A stars (N<3 threshold).

**Root cause:** The folio-number grouping used in exp_516–522 groups all pages of a folio number together. In the f57-72 range, some folio numbers contain BOTH A and B dialect pages (e.g., f57r is B-dialect while f57v is A-dialect). When combined, the edy rate crosses 5% → the folio number is excluded from A stars. This means many A-dialect pages in the f57-72 range are excluded.

F446 (t-LF elevation, E=2.12×/N=15) was computed with per-PAGE dialect classification, which correctly includes f57v, f58r, f58v, and other A-dialect pages that share folio numbers with B-dialect pages.

**Resolution needed:** A stars section needs to be re-defined using per-page classification. H_new_EJ remains BLOCKED until this is done. This also means F503 and the A stars o-LF results above may be missing some A-dialect lines from the 57-72 range.

---

## H_new_CW: B astro F469/F471 2-word-line artifact check — RESOLVED

| LF class | len filter | N_elig | obs | E | Flag |
|----------|-----------|--------|-----|---|------|
| sh-LF pos2=sh | len≥2 | 34 | 8 | 1.26× | below CONF |
| sh-LF pos2=sh | len≥3 | 32 | 8 | 1.33× | below CONF |
| ol-LF pos2=ol | len≥2 | 104 | 12 | 1.25× | below CONF |
| ol-LF pos2=ol | len≥3 | 101 | 12 | 1.29× | below CONF |

**F469 and F471 should be RETRACTED.** Neither reaches CONF under current methodology:
- F469 (B astro sh→sh@pos2): E=1.33×/N=8 — below CONF (was claimed E=1.59×/N=10 CONF from exp_490)
- F471 (B astro ol→ol@pos2): E=1.29×/N=12 — below CONF (was claimed E=1.54×/N=15 CONF from exp_490)
- The 2-word-line correction has minimal effect (N_elig drops by only 2-3). The discrepancy with exp_490's higher N comes from different corpus parsing or baseline methodology, not the 2-word-line bug specifically. Both findings are BELOW CONF at current methodology regardless of filter.

Note: F469/F471 were already noted as "corrected below CONF" in working_position.md (Section 13.5), consistent with this result.

---

## o-LF cross-line coupling (A herbal_a) — NEW CONF FINDING

| Direction | obs | exp | E | Flag |
|-----------|-----|-----|---|------|
| **ch-LL → o-LF (ch sends, o receives)** | **10** | **6.4** | **1.57×** | **CONF** |
| o-LL → sh-LF (o sends, sh receives) | 4 | 1.3 | 3.03× | (dir) |

**ch→o CL: CONF (E=1.57×/obs=10).** The confirmed A herbal_a CL chain extends:

**d → qot → ch → o** (d→qot: F491 CONF; qot→ch: F490 CONF; ch→o: NEW CONF)

And the chain may continue: **o → sh** (dir, E=3.03×/obs=4).

This is a 4-link chain in the A herbal_a paragraph cross-line grammar. Each link is independently confirmed at CONF or dir threshold. The chain represents a recurring paragraph-level sequence in A herbal_a: lines ending in d-onset → qot-onset → ch-onset → o-onset words form a recurrent trajectory.

**Caution:** ch is a common LF class (18.8% baseline in A herbal_a). E=1.57× reflects enrichment above this baseline. The finding is robust (CONF level) but the signal is weaker than the earlier chain links (F490: E=2.00×; F491: E=1.64×; ch→o: E=1.57×).

---

## Summary

| Hypothesis | Result |
|-----------|--------|
| H_new_EI: o-LF pos2/pen grammar | NEW: pos2=o-self (dir), pos2=cth (dir); pen: no signal; F502 E-value corrected (2.45→2.05×, obs 15→16; CONF preserved) |
| H_new_EI ext: A stars o-LF | F503 corrected (E=2.50×/obs=7, stronger); A stars o-LF pos2=o-self (dir) NEW |
| H_new_EJ: A stars t-LF grammar | BLOCKED — folio-number grouping excludes most A stars lines; F446 not reproducible with current section definition |
| H_new_CW: F469/F471 artifact check | RESOLVED — F469 and F471 BELOW CONF under current methodology; RETRACT both |
| o-LF CL coupling | **NEW CONF: ch→o (E=1.57×/obs=10)** extends d→qot→ch chain; NEW (dir): o→sh |

**New finding IDs assigned:** F504 (o-LF pos2=o-self A herbal_a, dir), F505 (o-LF pos2=cth A herbal_a, dir), F506 (ch→o CL A herbal_a CONF), F507 (o→sh CL A herbal_a dir). F503 corrected. F502 corrected. F469/F471 RETRACTED.
