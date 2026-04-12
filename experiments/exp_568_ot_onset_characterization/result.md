# exp_568: ot-onset full characterization (H_new_GF)

**Date:** 2026-04-11
**Hypothesis tested:** H_new_GF — ot-onset full characterization
**Status:** RESOLVED — F627 (vocabulary), F628 (positional), F629 (bigrams)

---

## PART 1: VOCABULARY

A herbal_a: 548/11327 (4.84%), 133 types.
Top-15: otaiin(48=8.8%), otal(47=8.6%), otar(39=7.1%), oty(39=7.1%), otain(37=6.8%), otol(32=5.8%), oteey(26=4.7%), otchy(23=4.2%), otchol(20=3.6%), otam(16=2.9%), oteol(14=2.6%), otchey(13=2.4%), otchor(12=2.2%), otor(9=1.6%), otey(7=1.3%)

B all: 680/10163 (6.69%), 125 types.
Top-15: otedy(95=14.0%), oteedy(68=10.0%), otaiin(56=8.2%), otain(47=6.9%), otar(45=6.6%), oteey(42=6.2%), otal(38=5.6%), oty(33=4.9%), otchedy(19=2.8%), otey(18=2.6%), otam(15=2.2%), otol(13=1.9%), otchdy(11=1.6%), otor(10=1.5%), oteol(8=1.2%)

A→B: frequency INCREASES (4.84%→6.69%); A=diverse aiin+lateral body → B=edy-dominant (otedy 14.0%+oteedy 10.0%=24.0% of B ot tokens). Same convergence pattern as other MID classes (qok, qo, sh increase or stabilize A→B).

**→ F627**

---

## PART 2: POSITIONAL DISTRIBUTION

A herbal_a (baseline=4.84%):
- pos1: obs=76, E=0.77× (sub-baseline; NOT DEPL — **CORRECTS prior 1.29×**)
- MID: obs=269, E=1.00× (flat)
- LL: obs=100, E=1.15× (sub-CONF elevation)
- LF: obs=103, E=1.09× (near-flat, NOT depleted)

B all (baseline=6.69%):
- pos1: obs=22, E=0.26× **EXTREME DEPL**
- MID: obs=445, E=1.05× (flat)
- LL: obs=115, E=1.36× (sub-CONF elevation)
- LF: obs=98, E=1.15× (near-flat, NOT depleted)

Key findings:
- A pos1=0.77×/76: sub-baseline (NOT DEPL by E<0.70 threshold) — corrects working_position.md value of 1.29×
- B pos1=0.26×/22: EXTREME DEPL — the most extreme B pos1-avoider alongside ch (0.22×)
- LF NOT DEPL in both: ot is a MID class in B, not a pos1-avoider (unlike ch) in A

**→ F628**

---

## PART 3: BIGRAMS

### Outgoing from ot (MID-baseline)

A herbal_a (sender=445):
- ot→ot: obs=50, E=2.32× **CONF** (strong self-succession)
- ot→a: obs=38, E=1.94× **CONF**
- ot→qok: obs=24, E=0.74× (near-DEPL, below 0.70 threshold? E=0.74×, NOT DEPL)
- ot→s: obs=6, E=0.51× DEPL
- ot→y: obs=18, E=0.68× DEPL

B all (sender=582):
- ot→ot: obs=90, E=2.31× **CONF** (strong self-succession)
- ot→a: obs=32, E=1.53× **CONF**
- ot→qok: obs=65, E=0.74× (near-DEPL, NOT DEPL by threshold)
- ot→d: obs=29, E=0.68× DEPL
- ot→s: obs=7, E=0.44× DEPL
- ot→k: obs=6, E=0.54× DEPL

### Incoming to ot (overall-baseline)

A herbal_a (receiver=472):
- ot→ot: obs=50, E=2.19× **CONF** (self-succession confirmed)
- l→ot: obs=15, E=1.51× **CONF**
- o→ot: obs=13, E=0.58× DEPL
- k→ot: obs=10, E=0.68× DEPL
- qo→ot: obs=6, E=0.49× DEPL

B all (receiver=658):
- ot→ot: obs=90, E=2.04× **CONF** (self-succession confirmed)
- qot→ot: obs=45, E=1.63× **CONF**
- t→ot: obs=21, E=1.66× **CONF** (confirms F576)
- l→ot: obs=28, E=0.69× DEPL
- qo→ot: obs=13, E=0.64× DEPL
- s→ot: obs=11, E=0.62× DEPL

Self-succession summary: A=2.30× E (obs=50); B=2.26× E (obs=90) — strong cross-dialectal.

### ot-LF pos1 profile

A herbal_a (103 ot-LF lines):
- t@pos1: obs=10, E=1.75× **CONF**
- l@pos1: obs=7, E=4.61× dir
- s@pos1: obs=13, E=1.49× (sub-CONF, near threshold)
- ch@pos1: obs=5, E=0.64× DEPL
- sh@pos1: obs=4, E=0.53× DEPL

B all (98 ot-LF lines):
- y@pos1: obs=22, E=1.96× **CONF**
- qok@pos1: obs=6, E=0.46× DEPL
- s@pos1: obs=6, E=0.47× DEPL
- sh@pos1: obs=3, E=0.50× DEPL

**→ F629**

---

## AUDIT NOTES

1. **Threshold check**: ot→qok E=0.74×/24 (A) and 0.74×/65 (B) — above DEPL threshold (0.70×). NOT reported as DEPL; previously the summary claimed DEPL — that was an error (used incorrect threshold). Reported as near-DEPL only.

2. **Prior value correction**: working_position.md listed A pos1=1.29× (near-CONF). Actual canonical result: 0.77×/76 (sub-baseline, NOT DEPL). Correction required.

3. **Consistency with F576**: B t→ot CONF (1.66×/21) confirmed from F576 (1.55×/21 prior — slight E-value difference due to corpus boundary, directionally identical CONF).

4. **A ot→y DEPL (0.68×/18)**: E=0.68 < 0.70, obs=18 ≥ 3. This qualifies as DEPL. ot avoids routing to y in A, consistent with y being an opener class (openers tend to be downstream-depleted from MID classes).

5. **B ot-LF pos1 cth (dir)**: obs=2, E=3.74× — below obs=3 minimum for (dir). Not reported.

---

## SUMMARY

H_new_GF RESOLVED. Ot-onset is characterized:

**F627 (vocabulary)**: A=4.84% diverse; B=6.69% edy-dominant (24% of B ot tokens are edy-types). Frequency INCREASES A→B — joins the MID-class increase cluster (with qo 2.59%→3.09%, sh 8.21%→9.39%).

**F628 (positional)**: A pos1=0.77×/76 sub-baseline NOT DEPL (corrects prior 1.29×); B pos1=0.26×/22 EXTREME DEPL. LF NOT DEPL in both (unlike sh which is LF DEPL). Ot is a MID class in B, nearly flat in A.

**F629 (bigrams)**: Strong cross-dialectal self-succession (A:2.32×/50; B:2.31×/90); ot→a CONF cross-dialectal (A:1.94×/38; B:1.53×/32); B: t→ot CONF, qot→ot CONF; A: l→ot CONF. MID routing class with lateral/terminal-avoidance in B.
