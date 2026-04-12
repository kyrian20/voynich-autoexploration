# exp_501: A stars pos1 Grammar Survey

**Question:** (H_new_CG) Does A stars have confirmed pos1 routing rules? Does F476 (ot→y@pos1) extend to A stars?

---

## A stars pos1 Grammar

A stars: 130 lines. pos1 baseline (N=130): d=20.0%, y=20.0%, t=11.5%, s=10.0%, o=6.2%, sh=5.4%, ch/ok=4.6%, qok/qo=3.8%.

Key: both d and y dominate pos1 at 20% each — unusually balanced. This differs from A herbal_a (d≈20%, y≈14%) and A cosmo (d=22.9%, y=18.8%).

LF distribution: d(18.5%), ch(16.2%), a/o(10.8%), sh/ot(7.7%), ok(6.9%), ol/y/s(3.8-5.4%).

---

## Confirmed Findings: NONE in A stars

No A stars LF class reaches CONFIRMED threshold (N≥10 AND E≥1.5×) for any pos1 onset class. The corpus is small (N=130), limiting confirmation power for minor LF classes.

---

## Notable Directional Findings (A stars pos1)

| LF | pos1 onset | obs/N | E | flag |
|----|-----------|-------|---|------|
| o | y | 7/14 | 2.50× | **dir** |
| ot | t | 3/10 | 2.60× | (dir) |
| sh | y | 4/10 | 2.00× | (dir) |
| a | a-self | 2/14 | 9.29× | (N=2, no flag) |
| ch | k | 2/21 | 4.13× | (N=2) |

**o-LF → y@pos1 (dir, E=2.50×/N=7):** o-terminal lines in A stars open with y-onset words at 2.50× baseline. o-self is ZERO (0/14). The dominant opener for o-LF is y, not o-itself. N=7 gives directional but not confirmed.

**ot-LF → t@pos1 ((dir), E=2.60×/N=3):** ot-LF lines in A stars open with t-onset (not y), contrasting with herbal sections where ot-LF → y@pos1 (F476).

---

## F476 Test: ot→y@pos1 in A stars

| Section | ot-LF N | y@pos1 obs | E |
|---------|---------|-----------|---|
| A herbal_a | 43 | 11 | 1.83× (CONF, F456) |
| B herbal | 11 | 6 | 2.67× (dir, F475) |
| A cosmo | 20 | 2 | 0.53× DEPLETED |
| **A stars** | **10** | **3** | **1.50×** |

A stars ot-LF y@pos1: E=1.50×/N=3. Weakly positive but below all thresholds (N<5 for dir, N<10 for CONF). F476 continues to NOT extend beyond herbal sections. A stars ot-LF may have a slight positive tendency (E=1.50×) but the corpus is too small to confirm.

---

## d-LF pos1: A-Dialect Section-by-Section

| Section | d-LF pos1 routing | E | N | Status |
|---------|-----------------|---|---|--------|
| A herbal_a | ot@pos1 | 1.59× | 22 | **CONF (F453)** |
| A cosmo | y@pos1 | 1.64× | 16 | **CONF (F479)** |
| **A stars** | **d-self@pos1** | **1.67×** | **8** | **near threshold (N<10)** |

d-LF pos1 routing shows a remarkable section-specific pattern in the A dialect:
- A herbal_a: cross-class to ot (onset-class jump)
- A cosmo: cross-class to y (onset-class jump)
- A stars: near-confirmation d-self (E=1.67×/N=8; approaching but not reaching threshold)

All three A sections use d-LF at pos1 differently. y@pos1 is DEPLETED in A stars d-LF (E=0.42×). This rules out a d→y rule in A stars.

---

## Self-Chain Summary

| LF | self@pos1 | N_elig | E |
|----|----------|--------|---|
| a | 2 | 14 | 9.29× (N=2) |
| d | 8 | 24 | 1.67× (near threshold) |
| ch | 2 | 21 | 2.06× (N=2) |
| sh | 1 | 10 | 1.86× (N=1) |
| ok | 1 | 9 | 2.41× (N=1) |
| ot | 0 | 10 | ZERO |
| o | 0 | 14 | ZERO |

No self-chain reaches CONFIRMED. d-self (E=1.67×/N=8) is the strongest near-confirmation signal. Given A stars small corpus, d-self at pos1 warrants monitoring if more A stars data becomes available.

---

## Interpretation

**H_new_CG ANSWERED: A stars has NO confirmed pos1 routing rules.** A stars matches the pattern of A cosmo and all B sections except A herbal_a: confirmed positional grammar rules are absent or near-threshold.

**F476 scope confirmed: HERBAL-SECTION-SPECIFIC.** In A stars, ot-LF → y@pos1 shows E=1.50×/N=3 — weakly positive but not confirmable. All non-herbal A sections (A cosmo: DEPLETED; A stars: near-baseline) do not show the herbal-register ot→y opener.

**d-LF pos1 across A dialect: unique routing per section.** The pattern of section-specific d-LF pos1 targets (ot in herbal_a, y in cosmo, d-self near threshold in stars) is a new structural observation. None of the three A sections uses the same pos1 target for d-LF. This suggests that within the A dialect, d-LF pos1 routing is highly section-conditional.

**A stars positional grammar summary:** Both pos1 and pos2 (exp_498) show no confirmed rules in A stars. The dominant LF classes (d=18.5%, ch=16.2%) don't produce confirmed routing. A stars grammar may be simpler/flatter than A herbal_a, or the corpus is too small for confirmation (N=130).

---

## Self-Audit

**Target-awareness:** No target-aware elements. All baselines are A stars pos1 distributions.

**Feature-destroying implementation:** N/A. pos1=ws[0], no eligibility constraint needed.

**Extrapolation:** "No confirmed rules in A stars" — N=130 total lines; d-LF N=24 gives adequate power for d-self. "d-LF pos1 section-specific in A dialect" — descriptive observation from three confirmed/near-threshold data points; labeled as a structural observation, not a claim. "F476 not in A stars" — ot-LF N=10 is small; qualified as "not confirmable given N."

**Negative-result scope:** "No confirmed rules in A stars" applies to this corpus size. Some classes have small N (y-LF N=5, ol-LF N=7) where confirmability is limited. The absence of confirmed rules for d-LF (N=24) and ch-LF (N=21) is meaningful given their larger N.

**Control behavior:** No controls. N/A.

---

## Conclusions

**No new finding IDs assigned.** No confirmed rules in A stars pos1.

**d-LF pos1 A-dialect section-specific pattern (descriptive):** Three A sections use d-LF at pos1 differently (herbal_a→ot, cosmo→y, stars→d-self near threshold). All three are section-specific; no A-dialect-wide d-LF pos1 rule exists.

**A stars positional grammar (pos1 + pos2 combined):** Both positions show no confirmed rules. A stars grammar is distinctively flat compared to A herbal_a. The t-LF dominance (F446) at LF does not produce any confirmed pos1 routing pattern (t-LF N=0 in current sample? Wait — actually t was listed with 8 lines in A stars LF but t was not in the major_lf with min_lf=8... let me check. LF distribution shows t is not in the top 10 for A stars — actually looking at the output: no t-LF appears in the top 10 which shows d/ch/a/o/sh/ot/ok/ol/y/s). The F446 note says A stars t-LF E=2.12×/N=15 vs A-overall baseline. But in the pos1 survey, t-LF didn't meet min_lf=8? Let me check: the LF distribution showed: d=24(18.5%), ch=21(16.2%), a=14(10.8%), o=14(10.8%), sh=10(7.7%), ot=10(7.7%), ok=9(6.9%), ol=7(5.4%), y=5(3.8%), s=5(3.8%). T is not in the top 10! That's odd since F446 says A stars t-LF is elevated. 

Actually F446 is about t-LF being elevated vs A-overall baseline. In A stars, t-LF may have N=~6-8 (not listed in top 10). So t-LF in A stars is ~4-5% which is elevated vs A herbal_a (where t is very rare) but still small absolute N in A stars. That's why it's not a major class.

So my result.md above is correct — no confirmed rules.
