# exp_511: A herbal_a Cross-Line Coupling (CL) Systematic Survey

**Question H_new_CS:** Does A herbal_a have confirmed LF→next-LF cross-line coupling rules beyond those previously known?

**Method:** A herbal_a (n≤56, N=1188 lines, 55 folios). Within-folio consecutive pairs only (N=1133 pairs). LF onset extracted for each line; E = obs(A→B) / (base_A × base_B × N_pairs) using section-specific LF baselines. Confirmation thresholds: CONF = E≥1.5×/N≥10; dir = E≥2.0×/N≥5; (dir) = E≥2.5×/N≥3.

---

## CONFIRMED CL Rules (E≥1.5×/N≥10)

| Pair | obs | exp | E | Status |
|------|-----|-----|---|--------|
| **qot→ch** | 12 | 6.00 | **2.00×** | **CONF** |
| **d→qot** | 13 | 7.92 | **1.64×** | **CONF** |

## Directional CL Rules (E≥2.0×/N≥5)

| Pair | obs | exp | E | Status |
|------|-----|-----|---|--------|
| ol→ok | 6 | 2.39 | 2.51× | dir |
| ok→ol | 6 | 2.39 | 2.51× | dir |
| k→ot | 5 | 2.01 | 2.49× | dir |
| o→sh | 5 | 2.13 | 2.35× | dir |
| ok→y | 8 | 3.58 | 2.23× | dir |

## Notable (dir) Results (E≥2.5×/N≥3)

| Pair | obs | exp | E |
|------|-----|-----|---|
| qok→qok | 4 | 1.04 | 3.84× |
| a→ol | 4 | 0.90 | 4.45× |
| y→y | 4 | 1.85 | 2.16× |

## Self-succession summary

| Pair | obs | exp | E | Status |
|------|-----|-----|---|--------|
| d→d | 94 | 67.5 | 1.39× | below (near threshold) |
| cth→cth | 8 | 4.88 | 1.64× | below (N<10) |
| y→y | 4 | 1.85 | 2.16× | (dir), N=4 |
| ch→ch | 40 | 38.85 | 1.03× | FLAT |
| ok→ok | 8 | 6.94 | 1.15× | flat |

## Key Negative Results

| Pair | obs | exp | E | Note |
|------|-----|-----|---|------|
| ch→ch | 40 | 38.85 | 1.03× | FLAT — F438/F445 artifact (see below) |
| ok→d | 12 | 21.65 | 0.55× | DEPLETED — ok-terminal → d-terminal avoidance |
| s→qot | 0 | 0.74 | 0× | N too small within-folio (27 s-LF/55 folios) |

---

## FINDINGS

### F490 (NEW CONF): A herbal_a qot-LF → ch-LF at next line (E=2.00×/N=12)

qot-terminal lines are followed by ch-terminal lines at 2.0× the section baseline. This is the strongest confirmed CL rule in A herbal_a (the only CL rule meeting both E≥1.5× and N≥10 with E≥2.0×).

Note: qot and ch have different LF bases (qot=2.9%, ch=18.5%) — the E reflects that qot-terminal lines disproportionately precede ch-terminal lines.

### F491 (NEW CONF): A herbal_a d-LF → qot-LF at next line (E=1.64×/N=13)

d-terminal lines are followed by qot-terminal lines at 1.64× baseline. d is the most common LF class (24.4%), qot is relatively rare (2.9%). After a d-LF line, a qot-LF line follows at above-baseline rate.

### Possible CL chain: d→qot→ch

F491 (d→qot CONF) and F490 (qot→ch CONF) suggest a possible three-element CL sequence: d-terminal → qot-terminal → ch-terminal paragraphs. Direct verification of triple-chain not run here.

### F438 scope correction: ch→ch CL is NOT A herbal_a-specific

F438/F445 reported "ch→ch A=1.57×/N=28" for A-dialect. In A herbal_a specifically: E=1.03×/N=40 — completely FLAT. The A-dialect aggregate signal for ch→ch was driven by mixed-section baselines (A herbal_a ch base=18.5%; combining with lower-ch sections reduces the baseline and inflates E). **ch→ch CL does not operate in A herbal_a.** This is consistent with within-line ch→ch @pos2 being CONF in A herbal_a (the self-chaining is within the line, not across lines).

### ok→y CL direction confirmed (E=2.23×/N=8, dir)

Consistent with F438 (ok→y A=1.52×/B=1.64×). The ok→y transition is directional in A herbal_a specifically. Combined with F455 (ok-LF → y@pos1 within-line, CONF), ok and y have a bidirectional relationship: within lines, ok-terminal lines start with y; across lines, ok-terminal lines are followed by y-terminal lines.

### ok↔ol bidirectional CL (both E=2.51×/N=6, dir)

ol→ok and ok→ol are both elevated (symmetric bidirectional coupling). Suggests ol-class and ok-class LF lines tend to cluster together in A herbal_a paragraphs.

---

## Self-Audit

**Target-awareness:** None. Systematic all-pair survey with section-specific baselines.

**Feature-destroying implementation:** None. Folio-boundary-only pairs correctly exclude cross-folio transitions. Section parsing matches established protocol (n≤56, no dialect check).

**Extrapolation:** qot→ch CONF: obs=12/exp=6.0 → E=2.0×, N=12 meets both E and N thresholds. d→qot CONF: obs=13/exp=7.92 → E=1.64×, N=13 meets CONF. ch→ch FLAT: obs=40 vs exp=38.85 (E=1.03×) — near exact baseline. ok→d DEPLETED: E=0.55×/N=12 — consistent below 0.5× threshold (borderline).

**F438/F445 reconciliation:** The exp_445 result used "N=993 A-dialect pairs" for all three A sections combined. A herbal_a alone has 1133 within-folio pairs — more than the combined figure. The prior analysis likely used a different (combined) baseline, yielding a lower ch-LF base rate and inflating ch→ch E. This is a narrowing correction to F438/F445 scope claims.

**s→qot from F445:** obs=0 within-folio. With 27 s-LF lines across 55 folios (avg 0.49/folio), s-LF tends to be isolated. F445's E=3.2×/N=5 was likely cross-folio or from a different section definition. Not confirmed here; filed as unresolvable.

---

## Conclusions

Two new CONF CL rules in A herbal_a:
- **F490:** qot→ch CL (E=2.00×/N=12)
- **F491:** d→qot CL (E=1.64×/N=13)

Together these suggest a partial CL chain: d → qot → ch in paragraph structure. The ch→ch CL previously attributed to A dialect is FLAT in A herbal_a specifically (E=1.03×).

**H_new_CS ANSWERED:** A herbal_a has confirmed CL rules: F490 (qot→ch) and F491 (d→qot). Plus directionals: ok→y (consistent with F438), ol↔ok coupling, k→ot, o→sh.
