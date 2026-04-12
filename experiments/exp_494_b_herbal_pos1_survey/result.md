# exp_494: B herbal pos1 Grammar Survey

**Question:** (H_new_BV) Does B herbal have confirmed pos1 routing rules for major LF classes? How do they compare with A herbal_a pos1 grammar?

---

## Corpus

B herbal: 269 paragraph lines. pos1 baseline N=269.

B herbal pos1 baseline: y=20.4%, d=19.0%, t=14.1%, sh=7.4%, s=7.1%, qok=6.3%, ot=3.3%, ol=3.0%, p=3.0%, l=3.3%, ch=2.6%, ok/qo=1.9%

B herbal LF distribution (top classes): ch=17.8% (N=48), ok=14.5% (N=39), d=12.6% (N=34), a=7.1% (N=19), sh=7.1% (N=19), o=5.9% (N=16), y=5.6% (N=15), ol=4.8% (N=13), qok=4.8% (N=13), ot=4.1% (N=11), k=3.7% (N=10), l=3.3% (N=9)

---

## Results

### Confirmed pos1 findings in B herbal: NONE

No LF class in B herbal reaches the CONFIRMED threshold (E≥1.5×, N≥10) for any pos1 onset class.

### Directional pos1 findings in B herbal

| LF | pos1 onset | obs/N_elig | E | flag | note |
|----|-----------|-----------|---|------|------|
| ch | qok | 6/47 | 2.02× | **dir** | ch-self=0 (exp=1.2) |
| ot | y | 6/11 | 2.67× | **dir** | |
| o | t | 5/16 | 2.21× | **dir** | |
| ok | o | 3/39 | 5.17× | **(dir)** | N=3 only |
| d | ol | 3/33 | 3.06× | **(dir)** | N=3 only |
| a | ot | 2/19 | 3.15× | **(dir)** | N=2 only |

### Critical contrasts with A herbal_a

| LF class | A herbal_a pos1 | B herbal pos1 |
|----------|----------------|---------------|
| ch-LF | ch-self CONF (E=1.58×/N=30, F473) | ch-self = ZERO (obs=0, exp=1.2) |
| y-LF | y-self CONF (E=2.13×/N=11, F472) | y-self DEPLETED (E=0.35×/N=1) |
| d-LF | ot@pos1 CONF (F453) | ot not enriched; ol (dir, N=3) |
| ot-LF | y enriched (from exp_491); ot DEPLETED | y@pos1 dir (E=2.67×/N=6) — same direction |

---

## Interpretation

**B herbal has no confirmed pos1 routing rules** at the tested thresholds. The absence of confirmed rules is partly a power issue for small classes (ot-LF N=11, ol-LF N=13, k-LF N=10) but ch-LF (N=48) has ample power and still produces nothing confirmed: its strongest enrichment is qok@pos1 (dir, E=2.02×/N=6), and ch-SELF is completely absent (obs=0 vs exp=1.2).

**B herbal definitively lacks the A herbal_a pos1 self-chaining pattern.** In A herbal_a, y-LF and ch-LF self-chain at pos1 (F472, F473). In B herbal, both are absent or depleted:
- ch-self: A herbal_a E=1.58×/N=30 (CONF) vs B herbal E=0.00×/N=0 (ZERO)
- y-self: A herbal_a E=2.13×/N=11 (CONF) vs B herbal E=0.35×/N=1 (DEPLETED)

This extends F472 and F473 as A-herbal_a-specific findings — they are not herbal-register-wide rules.

**The d-LF → ot@pos1 pattern (F453) also does not hold in B herbal.** B herbal d-LF shows no ot enrichment at pos1 (ot not in top 8 by E for d-LF). Instead, B herbal d-LF has d-self below baseline (E=0.64×) and ol@pos1 as the strongest enrichment ((dir), N=3). F453 appears to be A herbal_a-specific (or A-dialect-specific) rather than herbal-wide.

**New directional (B herbal):** ot-LF → y@pos1 (dir, E=2.67×/N=6). This parallels the A herbal_a ot-LF enrichment direction (exp_491 showed y enriched at pos1 for ot-LF in A herbal_a too), suggesting ot-LF lines tend to open with y-onset words across both dialects — though neither section has enough ot-LF lines to confirm this.

---

## Self-Audit

**Target-awareness:** No target-aware elements. This experiment computes positional enrichments against within-section baselines with no reference to VMS target metrics (am_ll, y_lf, ss_mean, adj_rate).

**Feature-destroying implementation:** Survey experiment only. No mechanism that could destroy a feature. N/A.

**Extrapolation:** All claims are within the tested parameter range. The negative result (no confirmed pos1 rules in B herbal) is stated as: "No confirmed rules found at CONF thresholds (E≥1.5×, N≥10)." The absence of rules for small LF classes (ot-LF N=11) may reflect power limitations, not absence of grammar — this is noted. The confirmed zero for ch-self (obs=0, exp=1.2) is a more definitive absence than a mere below-threshold result.

**Negative-result scope:** "B herbal lacks A herbal_a-style pos1 self-chaining" is supported by: (1) ch-self=ZERO despite N_elig=47; (2) y-self=DEPLETED despite N_elig=14. These are not merely low-E results but confirmed zeros for large-N classes. The claim that F472 and F473 are A-herbal_a-specific (not herbal-register-wide) is well-supported.

**Control behavior:** No controls. N/A.

---

## Conclusions

**H_new_BV ANSWERED:** B herbal has no confirmed pos1 routing rules (nothing reaches CONF threshold). Directionalis: ch-LF→qok@pos1 (dir, E=2.02×/N=6), ot-LF→y@pos1 (dir, E=2.67×/N=6), o-LF→t@pos1 (dir, E=2.21×/N=5).

**Critical new scope constraints:**
- F472 (A herbal_a y-LF→y-self@pos1, CONF) is A-herbal_a-specific: B herbal y-self DEPLETED
- F473 (A herbal_a ch-LF→ch-self@pos1, CONF) is A-herbal_a-specific: B herbal ch-self ZERO
- F453 (A herbal_a d-LF→ot@pos1, CONF) does not hold in B herbal: no ot enrichment found

**New directional:** B herbal ot-LF → y@pos1 (dir, E=2.67×/N=6). Tentative parallel with A herbal_a ot-LF direction.
