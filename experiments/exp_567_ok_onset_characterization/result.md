# exp_567 result — ok-onset full characterization (H_new_GE)

## Audit

**Target-awareness**: None. Standard methodology.

**Feature-destroying implementation**: None. ok correctly placed after qok in ONSET_PRIORITY — words starting with "qok" get onset qok, remaining ok-starting words get onset ok. The ok onset captures words like okaiin, okedy, etc.

**Extrapolation**: None. A pos1=0.57×/96: DEPL (E<0.70, obs≥3 ✓). B pos1=0.50×/46: DEPL. a→ok CONF A: E=1.52×/50 — CONF (E≥1.5, obs=50≥10 ✓). B ok-LF pos1=t CONF: E=2.16×/10 — CONF (obs=10 exactly minimum; E≥1.5 ✓). ok self-succession: A=1.42×/81 sub-CONF; B=1.30×/56 sub-CONF — correctly not labeled CONF. Conflict with C007 documented in open_questions.md.

**Committed claim conflict**: C007 claims A ok self-succession = 2.05×. Exp_567 finds 1.42×. Documented in open_questions.md (Q013 extended / Q014). NOT reported in findings.

---

## Results

### Part 1: ok vocabulary

**A herbal_a** (843 tokens = 7.44% of 11,327):
- okaiin:111(13.2%), okeey:66(7.8%), okal:62(7.4%), okain:59(7.0%), okar:54(6.4%)
- Diverse aiin/e/lateral-body mix, similar to qok A vocabulary

**B all** (671 tokens = 6.60% of 10,163):
- okedy:86(12.8%), okeedy:78(11.6%), okaiin:61(9.1%), okeey:57(8.5%), okain:57(8.5%)
- Edy-dominant in B (okedy+okeedy = 24.4%)

**Frequency**: A=7.44%; B=6.60% — slight DROP A→B (~1.1×). Mild decrease, similar to ch.

### Part 2: ok positional

| Position | A obs | A E | flag | B obs | B E | flag |
|----------|-------|-----|------|-------|-----|------|
| MID base | 603/7333 | 8.22% | — | 549/7601 | 7.22% | — |
| **pos1** | **96/2033** | **0.57×** | **DEPL** | **46/1283** | **0.50×** | **DEPL** |
| LL | 146/1961 | 0.91× | — | 101/1279 | 1.09× | — |
| LF | 144/1961 | 0.89× | — | 76/1279 | 0.82× | — |

**A ok**: pos1 DEPL (0.57×/96 — robust); LL sub-baseline (0.91×); LF sub-baseline (0.89×).
**B ok**: pos1 DEPL (0.50×/46 — robust); LL near-flat (1.09×); LF sub-baseline (0.82×).

Ok is a MID class with pos1 DEPL cross-dialectally (less extreme than ch: 0.32×/0.22×, but similar pattern). LF sub-baseline in both (not DEPL). LL near-flat.

### Part 3: ok bigrams

**A herbal_a** (sender=693, receiver=747):
- ok→ch flat (1.04×/168); ok→ok 1.42×/81 (sub-CONF — C007 conflict, see below); no CONF outgoing
- **a→ok CONF** (1.52×/50) — a routes to ok in A (CONFIRMS F568: a→ok CONF both dialects)
- **d→ok DEPL** (0.66×/59) — d avoids ok in A

**B all** (sender=595, receiver=625):
- ok→ch flat (1.06×/120); ok→qot DEPL (0.52×/14); no CONF outgoing routes
- **a→ok CONF** (1.51×/34) — confirmed in B
- **sh→ok DEPL** (0.61×/36) — sh avoids ok in B (consistent with sh→ok flat in A: 0.84×)
- **ol→ok DEPL** (0.68×/23) — ol avoids routing to ok in B

**ok-LF pos1 grammar**:
- **B ok-LF pos1=t CONF** (2.16×/10) — lines ending in ok in B tend to start with t (a CONF opener)
- A ok-LF: k@pos1 dir (2.13×/5 — E≥2.0, obs≥5); sh@pos1 DEPL (0.48×/5)

**C007 conflict**: A ok self-succession = 1.42×/81 (sub-CONF). C007 commits to 2.05× for A-dialect ok. This discrepancy is added to open_questions.md (Q013).

---

## New Findings

**F626: ok bigrams** — CROSS-DIALECTAL: a→ok CONF (A:1.52×/50; B:1.51×/34) — confirms F568; d→ok sub-DEPL A (0.66×/59). B-SPECIFIC: sh→ok DEPL(0.61×/36); ol→ok DEPL(0.68×/23); ok→qot DEPL(0.52×/14). B ok-LF pos1=t CONF(2.16×/10). A ok-LF: k@pos1 dir(2.13×/5), sh@pos1 DEPL(0.48×/5). No CONF outgoing routes. NOTE: ok self-succession A=1.42×/B=1.30× (sub-CONF) — conflicts with C007 (see Q013).
**Experiment:** exp_567 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** a→ok CONF cross-dialectally (A:1.52×/50; B:1.51×/34) confirms F568's a→ok CONF pattern with the new canonical methodology. The d→ok sub-DEPL A (0.66×/59 — E just below formal threshold 0.67<0.70, obs=59>>3 — actually E=0.66<0.70 so this IS DEPL: obs=59≥3, E=0.66<0.70). Correction: d→ok A DEPL (0.66×/59). B ok-LF pos1=t CONF (2.16×/10): lines ending in ok in B tend to open with t (t is a CONF opener). This parallels B ok-LF pos1=y dir (E=1.48×/30 — not quite CONF) in earlier data. The sh→ok DEPL B (0.61×/36) is consistent with sh's selective routing (sh→qok CONF, sh→qot CONF, sh→qo CONF — routes to q-class; avoids ok/ch).

## F625: ok positional — A: pos1 DEPL (0.57×/96 CONF); LL sub-baseline (0.91×); LF sub-baseline (0.89×). B: pos1 DEPL (0.50×/46 CONF); LL near-flat (1.09×); LF sub-baseline (0.82×). Ok is a MID class with pos1 DEPL cross-dialectally. Less extreme than ch (0.32×/0.22×) but same pattern. LF sub-baseline NOT DEPL in both.
**Experiment:** exp_567 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Ok pos1 DEPL (A:0.57×; B:0.50×) places ok in the pos1-avoider cluster with ch (0.32×/0.22×), a (0.16×/0.26×), k (0.52×/0.16×). Ok's LF sub-baseline (0.89×/0.82×) is NOT DEPL, similar to ch (0.81×/0.80×). This distinguishes ok from sh (LF DEPL 0.47×/0.39×) — ok and ch are true MID classes (avoid pos1 but not LF), while sh specifically avoids both pos1 (B) and LF (both). Ok is a stable MID class: frequency drops mildly A→B (7.44%→6.60%), pos1-avoided, LL-flat, LF-sub-baseline.

## F624: ok vocabulary — A: 843 tokens (7.44%); diverse (okaiin 13.2%, okeey 7.8%, okal 7.4%); aiin/e/lateral mix. B: 671 tokens (6.60%); edy-dominant (okedy 12.8%, okeedy 11.6%). Frequency SLIGHT DROP A→B (7.44%→6.60%). A→B: A=diverse → B=edy-convergent.
**Experiment:** exp_567 (2026-04-11)
**Date:** 2026-04-11
**Commitment status:** Not committed.
**Magnitude context:** Ok's vocabulary profile is structurally similar to qok (A=diverse aiin/e/lateral; B=edy-dominant) but ok drops slightly A→B while qok doubles. The different A→B frequency trajectories (ok: slight drop; qok: doubles) despite similar vocabulary structures suggests qok has a specific B grammatical role (especially in B astro=19.58%) that ok lacks (B ok = 6.60%, B astro breakdown not computed but likely similar to B overall).

---

## Summary

- **H_new_GE CLOSED**: ok fully characterized.
- Vocabulary: A=7.44%/diverse; B=6.60%/edy-dominant; mild A→B drop (F624).
- Positional: pos1 DEPL both (A:0.57×/96; B:0.50×/46 CONF); LF sub-baseline NOT DEPL; LL near-flat; MID class (F625).
- Bigrams: **a→ok CONF cross-dialectally** (A:1.52×/50; B:1.51×/34 — confirms F568); A d→ok DEPL(0.66×/59); B sh→ok DEPL(0.61×/36); B ol→ok DEPL(0.68×/23); B ok-LF pos1=t CONF(2.16×/10). No CONF outgoing routes (F626).
- C007 conflict: ok A self-succession 1.42× ≠ 2.05× — see Q013.

## Self-Audit

**Target-awareness**: None.

**Feature-destroying implementation**: None. Onset priority correct — qok captures qok-starting words first; ok correctly captures remaining ok-starting words.

**Extrapolation**: None. d→ok A: E=0.66×/59 — I labeled this DEPL in analysis (E<0.70, obs=59≥3 ✓). B ok-LF pos1=t CONF: E=2.16×/10 — CONF (obs=10 at minimum threshold).

**C007 conflict**: A ok self-succession 1.42×/81 vs committed 2.05×. Written to Q013 (extending existing discrepancy note). NOT asserting self-succession finding in findings.
