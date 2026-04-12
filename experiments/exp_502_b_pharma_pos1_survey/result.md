# exp_502: B pharma pos1 Grammar Survey

**Question:** (H_new_CH) What LF classes in B pharma have confirmed pos1 routing rules beyond F449?

---

## B pharma pos1 Grammar

B pharma: 799 lines. pos1 baseline (N=799): d=20.2%, y=17.4%, s=13.0%, sh=6.5%, qok=6.1%, ok/ch=5.5-5.8%, ol=4.6%, o=4.5%, t=3.8%, l=2.6%.

LF distribution: ch(19.8%/N=158), l(11.5%/N=92), a(11.0%/N=88), ot(9.9%/N=79), qok(7.4%), ok(6.1%), o(5.5%), ol/d(4.5-5.1%), r(4.1%), qot(3.6%), sh(2.9%).

---

## Confirmed Findings

### F449 REPRODUCED: ch-LF → ch-self at pos1 (E=1.65×/N=15, CONFIRMED)

B pharma ch-LF lines (N=158, N_elig=158): ch at pos1 E=1.65×(obs=15/158 = 9.5% vs 5.8% baseline; **CONFIRMED N=15, E≥1.5×**). Reproduces F449 from exp_478. ch-self@pos1 is a robust B pharma grammar feature.

### F480 NEW: a-LF → y at pos1 (E=1.50×/N=23, CONFIRMED)

B pharma a-LF lines (N=88, N_elig=88): y at pos1 E=1.50×(obs=23/88 = 26.1% vs 17.4% baseline; **CONFIRMED N=23, E≥1.5×**). B pharma a-terminal lines open with y-onset words at 1.50× baseline. a-self@pos1 is below threshold (E=1.95×/N=3, N<10). a-LF routing: y at pos1 (not self).

---

## Notable Directional Findings

| LF | pos1 onset | obs/N | E | flag |
|----|-----------|-------|---|------|
| sh | sh-self | 6/23 | 4.01× | **dir** |
| t | t-self | 4/11 | 9.68× | (dir) |
| d | l | 4/36 | 4.23× | (dir) |
| ot | t | 6/79 | 2.02× | **dir** |
| qo | sh | 3/13 | 3.55× | (dir) |
| ol | a | 3/41 | 4.18× | (dir) |

**sh-LF → sh-self@pos1 (dir, E=4.01×/N=6):** sh-terminal lines in B pharma self-chain at pos1 at 4.01× baseline. Near confirmation (N=6, needs N≥10 for CONF). B pharma has two confirmed+one directional self-chain: ch (CONF), sh (dir), t (high E/small N).

**ot-LF → t@pos1 (dir, E=2.02×/N=6):** ot-terminal lines in B pharma open with t-onset at pos1 at 2.02× baseline. This is the SAME onset class (ot and t are related — ot is bench+gallows+t, while t is gallows alone). Compare F476 (herbal: ot→y@pos1) — B pharma uses t not y as the ot-LF pos1 partner.

**d-LF → l@pos1 (dir, E=4.23×/N=4):** d-terminal lines route to l-class words at pos1 in B pharma. This adds to the d-LF pos1 diversity across sections: A herbal_a→ot, A cosmo→y, A stars→d-self, B pharma→l (dir). The F423 connection (pharma l-chain) may explain this: l-class words are pharma-prominent and appear at pos1 in d-LF context.

---

## B pharma pos1 Self-Chain Summary

| LF | self@pos1 | N_elig | E | flag |
|----|----------|--------|---|------|
| ch | 15 | 158 | 1.65× | **CONFIRMED (F449)** |
| sh | 6 | 23 | 4.01× | **dir** |
| t | 4 | 11 | 9.68× | (dir) |
| qot | 0 | 29 | ZERO | — |
| qo | 0 | 13 | ZERO | — |
| a | 3 | 88 | 1.95× | (below CONF, N<10) |
| d | 6 | 36 | 0.83× | below baseline |
| l | 3 | 92 | 1.24× | below threshold |

---

## Scope Notes from B pharma pos1

**F476 NOT in B pharma:** ot-LF in B pharma shows y@pos1 = obs=16/79, E=1.16× (near baseline). F476 scope confirmed: herbal sections only. B pharma ot-LF uses t@pos1 (dir, E=2.02×/N=6) instead.

**F449 robustly reproduced:** ch-self@pos1 E=1.65×/N=15 in B pharma ch-LF (N=158). This is the strongest confirmed pos1 self-chain rule in B pharma.

**B pharma multiple pos1 self-chain classes:** ch (CONF), sh (dir), t (dir high E) — B pharma has more pos1 self-chain signals than B herbal (which has none) or B astro (which has none). B pharma is more similar to A herbal_a in having multiple LF classes with pos1 self-chaining.

---

## Interpretation

**H_new_CH ANSWERED: B pharma has at least 2 confirmed pos1 rules and 3+ directional rules.**
1. F449 (ch-self@pos1, CONF): reproduced
2. **F480 NEW (a-LF → y@pos1, CONF, E=1.50×/N=23)**

**F480 scope question:** a-LF → y@pos1 in B pharma. Is this B-pharma-specific or B-dialect-wide? a-LF is the 3rd most common LF class in B pharma (N=88) but is less prominent in B herbal (N=19) and B astro (not checked). A follow-up would test whether a-LF → y@pos1 holds in B herbal and B astro.

**B pharma pos1 grammar is richer than B herbal/astro:** Multiple confirmed+directional rules vs none in herbal/astro. B pharma's larger corpus (N=799) partly explains this, but ch-self (E=1.65×/N=15) is well above threshold and reflects a genuine grammar difference.

**A herbal_a a-LF context:** A herbal_a has a-LF (N=15 in A cosmo, N=34 in A stars — small). If a→y@pos1 is a broader dialect-level rule, testing A cosmo a-LF would be informative. From exp_500 A cosmo: a-LF → a-self@pos1 was ZERO, and qok was the directional (E=2.69×/N=3). So A cosmo a-LF does NOT show y@pos1 enrichment. F480 may be B pharma-specific or broader B-dialect.

---

## Self-Audit

**Target-awareness:** No target-aware elements. All baselines are B pharma pos1 distributions.

**Feature-destroying implementation:** N/A.

**Extrapolation:** All claims within scope. "F449 reproduced" — correct (N=15/158, E=1.65×, same direction as exp_478 result). "F480 confirmed" — N=23/88, E=1.50×, CONFIRMED by both thresholds. "sh-LF dir near confirmation" — correct scope (N=6, directional only).

**Negative-result scope:** "F476 absent in B pharma" — ot-LF N=79, y@pos1 E=1.16× (well-powered negative). Within scope.

**Control behavior:** No controls. N/A.

---

## Conclusions

**F449 REPRODUCED (CONFIRMED):** B pharma ch-LF → ch-self at pos1 (E=1.65×/N=15).

**F480 NEW (CONFIRMED):** B pharma a-LF → y at pos1 (E=1.50×/N=23, CONF). B pharma a-terminal lines open with y-onset words at 1.50× baseline. First confirmed pos1 routing rule for a-LF in any section.

**New H: F480 scope** — does a-LF → y@pos1 extend to B herbal and B astro? B pharma a-LF is N=88; B herbal a-LF is N=19; B astro a-LF is unknown (test in follow-up).
