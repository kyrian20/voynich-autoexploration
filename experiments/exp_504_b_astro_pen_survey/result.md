# exp_504: B astro pen Grammar Survey

**Question:** (H_new_CE) Is B astro pen routing stronger than its weak pos2? Does F459 (ok→a@pen, B-dialect-wide) reproduce for B astro alone?

---

## B astro pen Grammar

B astro: 700 lines. pen baseline (len≥3, N=662): qok=18.3%, ch=14.2%, sh=13.9%, ol=8.5%, d=8.2%, ok/ot=6.8%, qot=4.8%, l=4.4%, t=2.3%, a/qo/r≈2%.

LF distribution: ol(14.9%/N=104), ch(12.1%/N=85), l(11.9%/N=83), d(11.3%/N=79), qok(10.7%/N=75), ok(5.3%), sh(5.0%), ot(4.3%).

---

## THREE Confirmed Findings

### F481 NEW: qok-LF → sh at pen (E=2.12×/N=20, CONFIRMED)

B astro qok-LF lines (N=75, N_elig=68): sh at pen E=2.12×(obs=20/68 = 29.4% vs 13.9% baseline; **CONFIRMED N=20, E≥1.5×**). B astro qok-terminal lines (dominant LF class) have sh-onset words at penultimate at 2.12× baseline. qok-self@pen is near baseline (E=1.21×/N=15).

### F482 NEW: B astro d-LF → d-self at pen (E=1.96×/N=12, CONFIRMED)

B astro d-LF lines (N=79, N_elig=75): d at pen E=1.96×(obs=12/75 = 16.0% vs 8.2% baseline; **CONFIRMED N=12, E≥1.5×**). B astro d-terminal lines self-chain at penultimate at nearly 2× baseline. d-self@pen appears to be a B astro grammar rule.

### F483 NEW: B astro l-LF → ch at pen (E=1.89×/N=22, CONFIRMED)

B astro l-LF lines (N=83, N_elig=82): ch at pen E=1.89×(obs=22/82 = 26.8% vs 14.2% baseline; **CONFIRMED N=22, E≥1.5×**). B astro l-terminal lines have ch-onset words at penultimate at 1.89× baseline. l-self@pen is near baseline (E=1.11×/N=4).

---

## Notable Directional Findings

| LF | pen onset | obs/N_elig | E | flag |
|----|----------|-----------|---|------|
| qo | sh | 7/23 | 2.19× | **dir** |
| sh | a | 3/32 | 4.43× | (dir) |
| ot | t | 3/30 | 4.41× | (dir) |
| o | ot | 4/19 | 3.10× | (dir) |
| a | ok | 3/20 | 2.21× | (dir) |
| qot | qot-self | 4/22 | 3.76× | (dir) |

**qo-LF → sh@pen (dir, E=2.19×/N=7):** qo-terminal lines use sh at pen — parallel to qok-LF → sh@pen (F481). The q-bench onset class may preferentially precede sh at pen position.

**ot-LF → t@pen ((dir), E=4.41×/N=3):** ot-terminal lines use t-onset at pen. Small N but high E. Compare F460 (ot→ot@pen B-dialect-wide) — in B astro specifically, the ot@pen signal goes to t (not ot-self), though ot-self@pen is also elevated (E=1.96×/N=4, near threshold).

---

## Self-Chain Summary

| LF | self@pen | N_elig | E | flag |
|----|---------|--------|---|------|
| **d** | **12** | **75** | **1.96×** | **CONFIRMED (F482)** |
| qot | 4 | 22 | 3.76× | (dir) |
| ot | 4 | 30 | 1.96× | (N=4, below dir) |
| qok | 15 | 68 | 1.21× | — |
| ch | 8 | 80 | 0.70× | DEPLETED |
| sh | 2 | 32 | 0.45× | DEPLETED |
| l | 4 | 82 | 1.11× | — |
| ol | 12 | 101 | 1.40× | near threshold |

ch-self@pen DEPLETED (E=0.70×/N=8 from N=80): ch does NOT self-chain at pen in B astro. Compare B astro ch-LF → ok@pos2 (F478, dir) — ch at pos2 routes cross-class, not self.

sh-self@pen DEPLETED (E=0.45×/N=2): sh-LF lines actively avoid sh at pen.

---

## F459 in B astro Alone

F459 (ok→a@pen, B-dialect-wide, E=2.79×/N=19 combined): B astro ok-LF → a@pen obs=2/35, E=2.70×/N=2 — consistent direction but N=2 insufficient for directional threshold. B astro contributes to the combined F459 signal but can't be confirmed in isolation.

## F460 in B astro

F460 (ot→ot@pen, B-dialect-wide, E=2.24×/N=25 combined): B astro ot-LF → ot-self@pen E=1.96×/N=4. Directional but N<5 for threshold. Consistent with F460 direction.

---

## Interpretation

**H_new_CE ANSWERED: B astro pen grammar is MUCH STRONGER than pos2.** B astro pos2: NO confirmed rules (exp_498). B astro pen: THREE confirmed rules (F481, F482, F483). The asymmetry between B astro pos2 (weak) and pen (strong with 3 CONF) is striking.

**B astro pen grammar specialization:** B astro's dominant LF class (qok, F431) has a confirmed pen rule: qok-LF → sh@pen (F481). The qok-centered grammar is deeper than previously known — not just LF dominance but also a specific penultimate word class.

**New finding scope questions:**
- F481 (qok→sh@pen): Is this B astro-specific or broader? B pharma/B herbal qok-LF pen patterns not yet tested.
- F482 (d-self@pen): B astro-specific or B-dialect? F460 (ot-self@pen) is B-dialect-wide; d-self@pen may be similarly broad.
- F483 (l→ch@pen): Is this B astro-specific? l-LF pen is not well-characterized in other B sections.

**ch and sh at pen:** ch-self@pen is DEPLETED (E=0.70×) and sh-self DEPLETED (E=0.45×). But qok-LF uses sh at pen (F481) and ch-LF uses qo at pen (dir). The pen position for ch and sh-LF lines actively avoids self-chaining — these onset classes appear at pen in OTHER LF classes' contexts (sh in qok-LF lines, ch in l-LF lines) but NOT in their own LF context.

---

## Self-Audit

**Target-awareness:** No target-aware elements. All baselines are B astro pen distributions from the same corpus.

**Feature-destroying implementation:** len≥3 eligibility for pen (ws[-2]) is correct. 2-word lines have ws[-2]=ws[0]=pos1 word, not pen. Eligibility filter correctly applied.

**Extrapolation:** All three confirmed findings within scope (N≥10, E≥1.5×). "B astro pen is stronger than pos2" is supported by 3 confirmed vs 0 confirmed — within scope.

**Negative-result scope:** F459 not reproduced in B astro alone — within scope (N=2, noted as insufficient). "ch-self@pen DEPLETED" — N=80 elig, E=0.70×, well-powered negative.

**Control behavior:** No controls. N/A.

---

## Conclusions

**F481 NEW (CONFIRMED):** B astro qok-LF → sh at pen (E=2.12×/N=20). B astro's dominant LF class (qok, F431) routes to sh at penultimate. New pen grammar rule for B astro's signature class.

**F482 NEW (CONFIRMED):** B astro d-LF → d-self at pen (E=1.96×/N=12). d-terminal lines in B astro self-chain at penultimate. Parallels F460 structure (ot→ot@pen) for d class.

**F483 NEW (CONFIRMED):** B astro l-LF → ch at pen (E=1.89×/N=22). l-terminal lines in B astro have ch-onset at penultimate. First confirmed pen rule for l-LF in any section.

**Key observation:** B astro pen grammar (3 confirmed rules) is dramatically richer than B astro pos2 grammar (0 confirmed). The line-position structure concentrates in pen rather than pos2 for B astro.
