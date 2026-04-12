# exp_532 result — B astro qo/qok CL chain analysis (H_new_EV + H_new_EW)

## Audit

**Target-awareness**: None. Standard CL methodology.

**Feature-destroying implementation**: Within-folio CL pairs plus within-folio line triplets for chain extension testing. B astro 690 pairs, 10 folios.

**Extrapolation**: None.

---

## H_new_EV: B astro qo-LF Chain — CLOSED NEGATIVE (d→qo is TERMINAL)

qo-LF as sender (N_cond=23): NO signals above any threshold.

Top qo-LF sender signals (all below threshold):
- qo→qo: E=2.65×/obs=2 (below (dir) — obs<3)
- qo→y: E=2.34×/obs=1 (noise)
- qo→sh: E=1.74×/obs=2
- qo→ok: E=1.65×/obs=2

qo as RECEIVER:
- d→qo: E=3.08×/obs=8 (dir) — strongly driven by d
- s→qo: E=2.43×/obs=2 (below threshold)
- qo→qo self: E=2.65×/obs=2 (below threshold)

d→qo→? triplets (N=8):
- d→qo→qo: obs=2, E=7.61× (strong but N=2 — noise)
- d→qo→o: obs=1, E=4.17× (noise)
- d→qo→ol: obs=2, E=1.68×
- No class exceeds (dir) threshold

**H_new_EV CONCLUSION**: qo-LF is NOT a chain pivot in B astro. It is a CL TERMINAL:
- d sends to qo at elevated rate (dir, E=3.08×)
- qo does NOT continue to a specific target — its sender profile is flat/near-baseline
- The d→qo→? triplet analysis shows no chain continuation
- The qot/qo functional analog hypothesis is **REFUTED**: unlike A herbal_a where d→qot starts a chain (qot→ch→o→sh), in B astro d→qo terminates. qo is a low-frequency (3.3% LF) terminal class, not a relay.

**Why different?** In A herbal_a, qot is the 4th most common LF class (~5.5% LF) and acts as a pivot. In B astro, qo is 3.3% LF with N_cond=23 — borderline power. Even if qo had a chain target at E=2.5×, we'd only expect obs≈1-2 per target, insufficient for (dir). Power limitation partially explains the flat profile. BUT: d→qo receivers do not cluster on one target (8 obs spread across 6 different classes) — this pattern is unlike a chain pivot where receivers concentrate.

---

## H_new_EW: B astro qok-LF Chain — CLOSED NEGATIVE (self-succession only)

qok as sender (N_cond=75): Only signal above threshold:
- **qok→qok: CONF (E=1.74×/obs=14)** — self-succession only (F495)

Near-signals below any threshold:
- qok→qot: E=1.70×/obs=4 (below dir)
- qok→sh: E=1.60×/obs=6 (below dir)
- qok→l: E=1.46×/obs=13 (below CONF)

qok as RECEIVER: strong senders:
- qok→qok: CONF E=1.77×/obs=14 (self is dominant)
- k→qok: E=2.84×/obs=3 ((dir)) — k-LF lines follow qok at elevated rate

qok→qok→? triplets (N=14):
- qok→qok→sh: obs=2, E=2.86× (below threshold: obs<3)
- qok→qok→l: obs=3, E=1.81× (below threshold: E<2.5)
- qok→qok→qot: obs=1, E=2.27×
- No class reaches (dir) threshold

**H_new_EW CONCLUSION**: B astro qok-LF has NO chain beyond self-succession. qok→qok is an ISOLATED CONF self-succession signal, NOT the start of a multi-step chain. B astro's qok grammar is fundamentally different from A herbal_a's d-LF:
- A herbal_a: d acts as a hub sending to qot (CONF), t (CONF), with both continuing in chains
- B astro: qok self-succeeds (CONF) but does NOT have confirmed routing to any other class

**Additional finding**: k→qok (dir) E=2.84×/obs=3 — k-LF lines are followed by qok-LF at elevated rate. This is the inverse of the qok self-succession: k sends to qok, then qok self-succeeds. The k→qok→(qok self) micro-pattern exists but is below threshold at N=3.

---

## B Astro CL Grammar Summary (incorporating F495 + exp_531 + exp_532)

B astro CL structure is fundamentally different from A herbal_a:

| Feature | A herbal_a | B astro |
|---------|-----------|---------|
| CL CONF self-succession | d→d (E=2.15×) | qok→qok (E=1.74×) |
| Main CONF chain | d→qot→ch→o→sh (5-link) | NONE — only self-succession |
| Directed non-self signals | d→qo (dir), ol→o (dir) | (same, but isolated, no chain) |
| Structure type | Multi-link directed chain | Isolated self-succession |

B astro CL grammar = isolated signals + self-succession, NOT a directed chain.

---

## Summary

| Question | Resolution |
|---------|-----------|
| H_new_EV: d→qo chain extension | CLOSED NEGATIVE: qo-LF is terminal, no chain continuation |
| H_new_EW: qok chain extension | CLOSED NEGATIVE: self-succession only, no multi-step chain |

**No new findings at (dir) or above.** (All results below threshold or previously documented in F495.)

**Structural insight**: B astro lacks A herbal_a's directed chain grammar. The two sections have very different CL structures despite both being high-LF-count sections.
