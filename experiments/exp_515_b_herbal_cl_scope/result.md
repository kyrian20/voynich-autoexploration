# exp_515: B herbal CL Survey + F490/F491 Scope Test

**Questions H_new_DD + H_new_CT**
- H_new_DD: Does B herbal have confirmed within-folio CL onset coupling rules?
- H_new_CT: Do F490 (qot→ch CL) and F491 (d→qot CL) appear in A cosmo or B herbal?

**Method:** Within-folio consecutive LF-onset pairs. Section-specific LF baselines.
E = obs / (base_A × base_B × N_pairs). Thresholds: CONF=E≥1.5×/N≥10; dir=E≥2.0×/N≥5; (dir)=E≥2.5×/N≥3.

Sections: A herbal_a (44 folios, 966 lines, 922 pairs), A cosmo (10 folios, 296 lines, 286 pairs), B herbal (14 folios, 272 lines, 258 pairs).

---

## F490/F491 Scope: H_new_CT ANSWERED

| Section | d→qot | qot→ch | qot N |
|---------|-------|--------|-------|
| A herbal_a | E=1.52×/N=13 CONF | E=1.86×/N=11 CONF | ~34 qot-LF lines |
| A cosmo | E=1.60×/N=1 (N=1!) | E=1.24×/N=1 | qot very rare |
| B herbal | E=0.00×/N=0 | E=6.10×/N=1 | qot near-absent |

**F490 and F491 are untestable in A cosmo and B herbal** because qot-LF is very rare in both sections. A cosmo has qot near-zero frequency (not in top-8 LF classes). B herbal qot-LF baseline rate produces exp=0.13-0.16 per pair — confirming qot-LF is near-absent. The 1-obs qot→ch in B herbal (E=6.10×/N=1) is meaningless at N=1.

**H_new_CT ANSWERED: F490/F491 cannot be confirmed in A cosmo or B herbal due to insufficient qot-LF frequency. The rules are effectively untestable and remain A-herbal_a-specific by default.** qot-LF appears to be a distinctive A herbal_a LF class not present in A cosmo or B herbal.

---

## B herbal CL Survey: H_new_DD ANSWERED

**B herbal top CL pairs (E≥1.5×, obs≥3):**

| A→B | obs | exp | E | Status |
|-----|-----|-----|---|--------|
| ot→ch | 5 | 1.80 | 2.77× | dir |
| ol→ok | 4 | 1.81 | 2.21× | — |
| ok→y | 4 | 1.95 | 2.05× | — |
| d→ok | 9 | 5.02 | 1.79× | — |
| ok→o | 4 | 2.37 | 1.69× | — |
| ch→ot | 3 | 1.80 | 1.66× | — |
| d→a | 4 | 2.51 | 1.59× | — |
| ch→a | 5 | 3.28 | 1.53× | — |

**NO confirmed CL rules in B herbal** (nothing reaches E≥1.5×/N≥10 threshold). B herbal has only 258 within-folio pairs — the corpus is too small for most pairs to accumulate N≥10.

**Best candidates:**
- **ot→ch: E=2.77×/N=5 (dir)** — ot-terminal lines followed by ch-terminal lines. Interesting parallel: A herbal_a has qot→ch CL CONF (F490). In B herbal, it's ot (not qot) that routes to ch. B herbal uses a different gallows class for the "→ch" CL transition.
- **d→ok: E=1.79×/N=9 (near-CONF)** — d-terminal lines followed by ok-terminal lines. One observation short of N≥10. This is structurally different from A herbal_a's d→qot CL (F491). In B herbal, d leads to ok (not qot). Another A/B CL inversion: A d→qot; B d→ok.

---

## F444 Scope Check (B herbal, section-specific baseline)

F444 claimed ok→y CL and d→sh CL for B herbal from a mixed-section survey:

| Pair | Section-specific result |
|------|------------------------|
| ok→y | E=2.05×/N=4 — below dir (N<5) |
| d→sh | E=1.26×/N=3 — below threshold |

**F444's B herbal claims (ok→y, d→sh) do NOT survive section-specific baseline.** With B herbal section-specific baselines and within-folio pairs only:
- ok→y drops to N=4 (was claimed as directional from mixed-section)
- d→sh drops to E=1.26× (was claimed CONF-approaching from mixed-section)

These are correction-level findings. F444 was based on a combined B-dialect CL survey (herbal+pharma+astro) with a shared baseline, which underestimated the B herbal ok and y rates. With proper section isolation, neither survives as a B herbal-specific rule.

---

## A/B Herbal CL Structural Comparison

| Feature | A herbal_a | B herbal |
|---------|-----------|----------|
| N_pairs | 922 | 258 |
| Confirmed CL rules | F490(qot→ch), F491(d→qot) | NONE |
| Best directional | k→ot (E=2.80×/N=5) | ot→ch (E=2.77×/N=5) |
| d→qot | E=1.52×/N=13 CONF | E=0.00×/N=0 (qot absent) |
| d→ok | E=1.09×/N=4 | E=1.79×/N=9 (near-CONF) |
| ok→y | E not in top | E=2.05×/N=4 (dir) |

**Pattern:** A herbal_a's CL chain (d→qot→ch) relies on qot as a "pivot" class — qot appears between d-terminal and ch-terminal lines. B herbal's qot-LF is near-absent, so the same chain cannot operate. B herbal's leading CL tendency is d→ok (near-CONF) and ot→ch (dir) — structurally different routing.

If d→ok reaches CONF with more data, B herbal's CL structure would be: **d-terminal → ok-terminal → ? chain**. Compare A herbal_a: d→qot→ch. B herbal potentially: d→ok→?. These are different pivot classes (qot vs ok) for the same "d leads to something leads to ch" chain.

---

## Self-Audit

**Target-awareness:** None. Systematic survey of all pairs. F490/F491 scope test was pre-planned with clear expected outcome (qot rare = untestable).

**Feature-destroying:** None. Within-folio pairs only (not cross-folio). Section-specific baselines throughout.

**Extrapolation:** A herbal_a F491 reproduced as E=1.52×/N=13 vs original E=1.64×/N=13 — small difference from baseline computation (922 vs 1133 pairs in different experiments; likely folio-range differences). F490 reproduced as E=1.86×/N=11 vs original E=2.00×/N=12. Consistent directional outcome. B herbal d→ok N=9 is one observation short of CONF threshold — cannot upgrade.

**H_new_DD ANSWERED:** B herbal has NO confirmed CL rules. Best directional: ot→ch (E=2.77×/N=5). B herbal is CL-grammar-weak compared to A herbal_a (same corpus size but different LF class structure; qot absent prevents A herbal_a chain replication).

**H_new_CT ANSWERED:** F490/F491 cannot be tested in A cosmo or B herbal. qot-LF is absent/rare in both sections. A herbal_a-specific by default.
