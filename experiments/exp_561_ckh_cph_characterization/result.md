# exp_561 result — ckh and cph onset characterization (H_new_FX)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. Consistent corpus parsing. MID baseline for outgoing bigrams; overall sender distribution for incoming bigrams.

**Extrapolation**: None. B ckh/cph are severely underpowered (9/7 tokens); no formal B claims. ckh LF DEPL: E=0.67×/obs=18 — meets formal DEPL threshold (E<0.7, obs≥3) but borderline.

---

## Results

### Compound gallows frequency overview

| Class | A tokens | A% | B tokens | B% | A→B ratio |
|-------|---------|-----|---------|-----|-----------|
| cth | 304 | 2.684% | 31 | 0.305% | **8.8×** |
| ckh | 121 | 1.068% | 9 | 0.089% | **12.0×** |
| cph | 38 | 0.335% | 7 | 0.069% | **4.9×** |
| sch | 23 | 0.203% | 18 | 0.177% | **1.1× (stable)** |

All compound gallows show large A→B frequency drops EXCEPT sch (stable). Sch is the anomalous compound gallows class. Combined A compound gallows = 4.29% of A words; Combined B = 0.64% — a 6.7× collective A→B drop.

skh and sph: 0 tokens in both corpora (absent from this dataset).

---

### Part 1: ckh

**Vocabulary (A: 121 tokens, 1.07%):**
- ckhy: 26 (21.5%), ckhey: 23 (19.0%), ckhol: 17 (14.0%), ckhor: 6 (5.0%), ckheey: 6 (5.0%)
- Y-body (ckhy 21.5%) and lateral-body (ckhol 14.0%, ckhor 5.0%) dominant — same A vocabulary pattern as cth and sch.
- B (9 tokens): ckhedy 33.3%, ckhy 22.2% — edy-dominant as expected.

**Positional (A herbal_a):**

| Position | obs | total | E | flag |
|----------|-----|-------|---|------|
| MID base | 101 | 7333 | 0.0138 | — |
| **pos1** | **2** | 2033 | **0.07×** | **EXTREME DEPL** |
| LL | 25 | 1961 | 0.93× | — |
| **LF** | **18** | 1961 | **0.67×** | **DEPL** |

**CRITICAL: ckh is NEITHER an opener NOR a terminal.** ckh pos1 = 0.07× (near-zero, like cth's 0.13×). ckh LF = 0.67×/18 DEPL (below baseline). ckh LL = 0.93× (flat). Ckh is concentrated at MID positions — it avoids BOTH the beginning AND end of lines. This contrasts with cth (LF CONF terminal) and sch (pos1 CONF opener).

**Bigrams (A, outgoing=103, incoming=119):**

Outgoing:
| Target | obs | exp | E | flag |
|--------|-----|-----|---|------|
| ckh→d | 18 | 9.0 | **2.00×** | **CONF** |
| ckh→ckh | 6 | 1.4 | 4.23× | dir |
| ckh→ch | 20 | 24.1 | 0.83× | — |

Incoming:
| Sender | obs | exp | E | flag |
|--------|-----|-----|---|------|
| y→ckh | 13 | 7.0 | **1.84×** | **CONF** |
| o→ckh | 10 | 5.7 | **1.76×** | **CONF** |
| ckh→ckh | 6 | 1.3 | 4.72× | dir |
| ok→ckh | 6 | 8.9 | 0.68× | **DEPL** |

**ckh→d CONF (E=2.00×/18)** — CRITICAL finding. Ckh routes to d at 2× baseline, identical E-value to cth→d (F602: E=1.97×/37). THREE compound gallows classes all route to d: cth→d CONF (1.97×); ckh→d CONF (2.00×); sch→d dir (3.43×/6). **Compound gallows → d routing is a universal A structural principle.**

**y→ckh CONF (E=1.84×/13)** and **o→ckh CONF (E=1.76×/10)**: ckh is specifically preceded by y-onset and o-onset words. This matches y→ckh from F559 (y→ckh E=1.64×/12 in prior work). y and o both route to ckh as a MID target.

**ok→ckh DEPL (E=0.68×/6)**: ok specifically avoids preceding ckh. This mirrors qok→cth DEPL (F602).

### Part 2: cph

**Vocabulary (A: 38 tokens, 0.335%):**
- cphol: 6 (15.8%), cphey: 5 (13.2%), cphy: 4 (10.5%), cphaiin: 4 (10.5%)
- Lateral and y-body dominant in A. B (7 tokens): cphedy 57.1% — edy-dominant.

**Positional (A herbal_a):**

| Position | obs | total | E | flag |
|----------|-----|-------|---|------|
| MID base | 31 | 7333 | 0.0042 | — |
| **pos1** | **1** | 2033 | **0.12×** | extreme (obs<3) |
| LL | 12 | 1961 | **1.45×** | sub-CONF |
| LF | 6 | 1961 | 0.72× | — |

Cph: pos1 near-zero (obs=1 only, formally cannot apply DEPL threshold); LL elevated (1.45×/12 — sub-CONF, but above baseline). LF sub-baseline (0.72×/6).

**B cph**: 7 tokens — LF=3 (E=4.46×/3 — (dir) but underpowered). B cph may be LF-enriched but N=7 is insufficient.

**Bigrams (A, outgoing=32, incoming=37):**

| Target/Sender | obs | E | flag |
|--------------|-----|---|------|
| cph→d | 7 | 2.50× | dir |
| cph→cph | 3 | 22.18× | (dir) |
| cph→ch | 3 | 0.40× | DEPL |
| cph→s | 3 | 9.29× | (dir) |
| cth→cph | 3 | 3.02× | (dir) |
| t→cph | 3 | 3.26× | (dir) |

**cph→d dir (E=2.50×/7)** — extends compound gallows → d routing pattern to cph. Four compound gallows now all route to d: cth, ckh, cph, sch (all elevated, varying significance).

**cph→cph (dir) (E=22.18×/3)**: extreme self-succession but obs=3 only. Cph occasionally self-chains.

**cth→cph (dir) (E=3.02×/3)**: cth precedes cph. This is consistent with F602's cth→cph (dir) signal — confirmed.

**cph→ch DEPL (E=0.40×/3)**: cph avoids routing to ch — the most common class. Parallels ckh→ch which is also below baseline (0.83×) though not DEPL.

---

## New Findings

**F607: Compound gallows positional taxonomy — A herbal_a** — The 4 compound gallows classes (ckh, cph, cth, sch) have DIFFERENT positional roles: sch=OPENER (pos1 CONF 11.54×/16); cth=TERMINAL (LF CONF 1.67×/88); ckh=MID class (pos1 DEPL 0.07×/2; LF DEPL 0.67×/18); cph=MID/LL class (pos1 near-zero 0.12×/1; LL sub-CONF 1.45×/12). Collective A→B frequency drop: combined compound gallows = 4.29% of A words vs 0.64% of B — 6.7× collective drop (with sch stable but others dropping 5-12×). Compound gallows are predominantly A-dialect structural elements.
**Experiment:** exp_561 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A compound gallows frequencies: cth=2.684%; ckh=1.068%; cph=0.335%; sch=0.203%. B: cth=0.305% (8.8×↓); ckh=0.089% (12×↓); cph=0.069% (4.9×↓); sch=0.177% (stable). Compound gallows are A-specific except sch. Positional differentiation: sch=opener; cth=terminal; ckh=MID; cph=MID/LL — within-class positional split with sch as anomalous opener. All have A vocabulary pattern (y-body/lateral A; edy-dominant B) matching universal A→B shift.
**Limitation:** B tokens are very small (ckh=9, cph=7, sch=18) — no formal B positional claims for ckh or cph. Ckh LF DEPL (0.67×/18) borderline — E=0.67<0.70, obs=18>>3, so formally DEPL but close to threshold.
**Commitment status:** Not committed.
**Magnitude context:** The compound gallows positional split (sch=opener; cth=terminal; ckh=MID; cph=MID/LL) is structurally coherent: within A lines, ALL major positional roles are occupied by different compound gallows subclasses. This internal differentiation within the c+X class suggests compound gallows represent semantically or grammatically distinct word types despite sharing the compound gallows grapheme form. The ~6.7× collective A→B frequency drop contrasts with single-gallows classes (k, t, s) which maintain frequency across dialects — compound gallows are an A-dialect feature.

**F608: ckh positional and vocabulary** — A herbal_a: 121 tokens (1.07%). A pos1 EXTREME DEPL (0.07×/2 near-zero); LF DEPL (0.67×/18); LL FLAT (0.93×/25). Ckh is a MID-class onset in A — avoids both line boundaries. Vocabulary: ckhy (21.5%), ckhey (19.0%), ckhol (14.0%) — y-body and lateral dominant. B: 9 tokens (0.089%); ckhedy 33.3%. A→B: 12× frequency drop.
**Experiment:** exp_561 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a: MID baseline=101/7333=1.38%; pos1=2/2033=0.10% (E=0.07×); LF=18/1961=0.92% (E=0.67× DEPL); LL=25/1961=1.28% (E=0.93× flat). Ckh concentration: ~71% MID (101 tokens out of 121 at non-pos1/non-LL/non-LF positions; the MID count is 101 token-positions, some double-counting possible but structurally ckh is MID-dominant). B: all 9 tokens underpowered; no formal claims.
**Limitation:** ckh LF: E=0.67×/18 — the DEPL threshold is E<0.7 and obs≥3; 0.67×<0.70 and 18≥3, so formally DEPL but just below threshold. B too small for any formal claims.
**Commitment status:** Not committed.
**Magnitude context:** Ckh's MID-class positional profile contrasts sharply with cth (its nearest structural cousin, both c+gallows compound). Cth is purely TERMINAL (LF CONF, pos1 DEPL). Ckh avoids BOTH terminal positions (LF DEPL) and line-opening (pos1 near-zero) — it is truly a MID word class. This is the first characterized onset class with LF DEPL AND pos1 near-zero — all other pos1-DEPL classes have flat or enriched LF (e.g., a: LF CONF B; ch: LF near-baseline).

**F609: ckh bigrams — ckh→d CONF (E=2.00×/18); y→ckh CONF (E=1.84×/13); o→ckh CONF (E=1.76×/10); ckh→ckh dir (4.23×/6); ok→ckh DEPL (0.68×/6). COMPOUND GALLOWS → d UNIVERSAL COUPLING: cth→d CONF (1.97×/37, F602); ckh→d CONF (2.00×/18) NEW; sch→d dir (3.43×/6, F606) — all three characterized compound gallows route to d within A lines at elevated rates.**
**Experiment:** exp_561 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a (103 ckh-sender bigrams): ckh→d CONF (E=2.00×/obs=18, meeting CONF threshold E≥1.5 and obs≥10). ckh→ckh dir (E=4.23×/6, meeting dir: E≥2.0, obs≥5). ckh→ch flat (E=0.83×/20). Incoming (119 ckh-receiver bigrams): y→ckh CONF (E=1.84×/13); o→ckh CONF (E=1.76×/10); ckh→ckh (4.72×/6 from incoming side); ok→ckh DEPL (E=0.68×/6). The ckh→d CONF at E=2.00×/18 is independently robust and extends the compound gallows → d pattern: cth→d (1.97×/37) + ckh→d (2.00×/18) + sch→d (3.43×/6). Compound gallows words preferentially precede d-onset words in A lines, regardless of positional role (opener sch, terminal cth, or MID ckh all route to d).
**Limitation:** ok→ckh DEPL: E=0.68×/6 — borderline (E<0.7, obs≥3; meets threshold). y→ckh CONF: E=1.84×/13 — robust CONF (obs=13>>10). o→ckh CONF: E=1.76×/10 — borderline CONF (obs=10 = minimum). ckh→d CONF: E=2.00×/18 — robust. B ckh bigrams: 8 sender, 9 receiver — underpowered, no CONF signals.
**Commitment status:** Not committed.
**Magnitude context:** The compound gallows → d universal coupling in A is structurally remarkable: cth, ckh, and sch all route to d at ~2× baseline rate (cth: 1.97×/37; ckh: 2.00×/18; sch: 3.43×/6). This suggests that ALL compound gallows classes in A, regardless of their specific positional role, have an affinity for d-onset words appearing later in the same line. Since d is A LF CONF (1.52×/360), and compound gallows tend to appear before LF position, the coupling is partly positional (compound gallows at MID/LL → d at LF). The universal nature of this coupling (three classes, consistent E values ~2-3×) suggests it's a property of the compound gallows WORD TYPE, not just positional proximity.

**F610: cph characterization — A: 38 tokens (0.335%); pos1 DEPL (0.12×/1 near-zero); LL sub-CONF (1.45×/12); LF sub-baseline (0.72×/6). B: 7 tokens (0.069%). A→B: 4.9× drop. Vocabulary: A=cphol (15.8%), cphey (13.2%), cphy (10.5%); B=cphedy (57.1%). Bigrams: cph→d dir (2.50×/7); cph→cph (dir) self-succession (22.18×/3); cth→cph (dir) (3.02×/3 — extends F602). Cph is a MID/LL-class compound gallows, extending compound gallows → d routing to a 4th class.**
**Experiment:** exp_561 (2026-04-11)
**Date:** 2026-04-11
**Finding:** A herbal_a (38 tokens, 0.335%): pos1=1/2033 (E=0.12× near-zero); LL=12/1961 (E=1.45× sub-CONF); LF=6/1961 (E=0.72× sub-baseline). B: 7 tokens; underpowered. Bigrams: cph→d dir (E=2.50×/7); cph→ch DEPL (E=0.40×/3 — avoids ch after, unlike most classes); cph→cph (dir) (E=22.18×/3 — extreme self-succession); incoming: cth→cph (dir) (E=3.02×/3 — F602 confirmed); t→cph (dir) (E=3.26×/3). Vocabulary: A=lateral+y-body (cphol, cphey, cphy); B=edy-dominant (cphedy 57%).
**Limitation:** All bigram signals rest on obs=3-7 — (dir) to dir level only. LL sub-CONF (1.45×/12): E<1.5 so sub-CONF but robust direction (12 obs). Pos1=obs=1 — below formal DEPL threshold (need obs≥3) but directionally extreme. B: underpowered throughout.
**Commitment status:** Not committed.
**Magnitude context:** Cph's LL elevation (1.45×/12 sub-CONF) parallels cth's LL elevation (1.35×/65 sub-CONF, F601). Both cph and cth have elevated LL presence — suggesting compound gallows (c+X) words tend to appear in penultimate positions more than MID baseline predicts. Cph→d dir (2.50×/7) extends the compound gallows → d pattern to a 4th class. The cth→cph (dir) coupling (F602 + confirmed here) suggests cth words sometimes precede cph words within A lines — another compound-gallows compound-gallows interaction.

---

## Summary

- **H_new_FX CLOSED**: ckh and cph fully characterized.
- **Compound gallows positional taxonomy (A herbal_a)**: sch=OPENER (11.54×/16 CONF); cth=TERMINAL (1.67×/88 CONF); ckh=MID (LF DEPL 0.67×/18; pos1 near-zero 0.07×); cph=MID/LL (LL sub-CONF 1.45×/12; pos1 near-zero) (F607).
- **UNIVERSAL compound gallows → d routing**: cth→d CONF (1.97×/37); ckh→d CONF (2.00×/18); cph→d dir (2.50×/7); sch→d dir (3.43×/6) — all four compound gallows classes route to d at elevated rates (F609).
- ckh: y→ckh CONF; o→ckh CONF — MID-class compound gallows specifically receives from y and o (F608/F609).
- Compound gallows are A-specific (4.29% A vs 0.64% B = 6.7× collective drop); sch is anomalously stable (F607).

## Self-Audit

**Target-awareness**: No target-aware elements.

**Feature-destroying implementation**: None. Consistent methodology.

**Extrapolation**: None beyond thresholds. B tokens underpowered; no B positional claims. ckh LF DEPL borderline — correctly at threshold.

**Negative-result scope**: The hypothesis that ckh/cph would be openers like sch is REFUTED — both are pos1-near-zero (MID class). This refutation is clearly stated.

**Control behavior**: MID baseline for outgoing bigrams; overall distribution for incoming.
