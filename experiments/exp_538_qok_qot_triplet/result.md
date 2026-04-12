# exp_538 result — qok→qot CONF triplet structure and scope (H_new_FA)

## Audit

**Target-awareness**: None. Standard characterization methodology.

**Feature-destroying implementation**: Standard corpus parsing. Triplet extraction correct (range(len-2) ensures a third word exists).

**Extrapolation**: None. Claims within tested sections.

---

## Part 1: qok→qot→X Triplets (A herbal_a)

qok→qot pairs with successor: N=8 (of 12 total qok→qot bigrams; 4 cases have qot at LF with no successor).

| qok→qot→X | obs | E |
|-----------|-----|---|
| ch | 2/8 | 1.06× |
| d | 2/8 | 1.26× |
| t | 1/8 | 4.25× |
| k | 1/8 | 2.40× |
| qok | 1/8 | 3.16× |
| ot | 1/8 | 2.67× |

**No triplet chain**: 8 cases spread across 6 targets. No target reaches dir threshold (need obs≥5 AND E≥2.0×, or obs≥3 AND E≥2.5×; only t/k/qok/ot qualify on E but all have obs=1 — too small). qok→qot does NOT form a directed within-line chain. The bigram is a terminal-ish pair — 4/12 cases (33%) have qot at LF (line-ending), and of the 8 pairs with successors, targets are diverse.

**Sample lines**: qokchy qotchol chol cthy; qokchy qotchy tol tod ckhy; qokchy qoty kchaiin shear cthor. Pattern: qokchy (ch-mediated qok) → qot-word → diverse continuation.

---

## Part 2: Asymmetry Confirmed

- qot→qok: obs=8/141, E=1.42× (sub-CONF) 
- qok→qot: obs=12/174, E=2.22× CONF

**DIRECTED coupling confirmed**: qok→qot is CONF while qot→qok is sub-CONF (1.42×). The coupling flows specifically qok→qot, not bidirectionally.

---

## Part 3: Scope — A-herbal_a SPECIFIC

| Section | qok→qot obs/N | E | Flag |
|---------|--------------|---|------|
| A herbal_a | 12/174 | 2.22× | **CONF** |
| A stars | 0/71 | 0.00× | STRONGLY DEPL |
| A cosmo | 1/156 | 0.53× | DEPL |

**qok→qot is A-HERBAL-A SPECIFIC**. It is absent in A stars (ZERO) and depleted in A cosmo. This is NOT a general A-dialect rule — it is confined to the herbal section.

---

## Summary: H_new_FA Assessment

F542 is CONFIRMED with scope clarification:
- **qok→qot CONF** (E=2.22×/obs=12) in A herbal_a — directed coupling
- **Does NOT form a triplet chain** — no concentrated target after qok→qot
- **A-herbal_a-SPECIFIC** — absent in A stars, depleted in A cosmo
- **Asymmetric**: qok→qot CONF but qot→qok sub-CONF (1.42×)

The qok→qot coupling is a local A-herbal_a-specific within-line pairing between the two dominant template class openers. It may reflect a body-form specificity (qokchy-class → qotchy-class) but N=12 is insufficient to test this.

**F542 scope clarification**: Add "A-herbal_a-specific (A stars: ZERO; A cosmo: DEPLETED)" to scope. No new finding ID — F542 updated.

**H_new_FA CLOSED POSITIVE (with scope limitation).**
