# exp_463: Paragraph-Level Cross-Line Chain Analysis (H_new_AA)

**Hypothesis (H_new_AA):** Does B have a 3-line chain pattern [d/qok/ok LL → ch LF → ch LL → qot LF]? (Testing B ch "pivot" structure from exp_459.)

---

## Results

**B-dialect CL triples (consecutive 3-line patterns): N=1293**

### Full chain: [d/qok/ok LL] → [ch LF] → [ch LL] → [qot LF]

| step | count | conditional P | baseline P | E |
|------|-------|--------------|------------|---|
| ll1 in {d,qok,ok} | 328/1293 | — | — | — |
| ll1→ch at next LF | 21/328 | 0.064 | ~0.042 | ~1.52× |
| then ch at LL of that line | 13/58 | 0.224 | — | — |
| then qot at next LF | 1/13 | 0.077 | 0.022 | **3.48×** (N=1) |

**Full chain [d/qok/ok → ch → ch → qot]: 1 observed (expected 0.10 if independent).** N=1 is completely directional. The chain exists but cannot be confirmed at current corpus size.

The conditional E at the last step (lf3=qot given lf2=ch AND ll2=ch) = 3.48×(N=1) is consistent with F442 (ch-LL → qot-LF, E=1.56×/N=7) but N is too small for an independent finding.

### Secondary chains (all directional)

- **[ch → qot → qot → ch]**: 0 cases — no qot→qot→ch chain
- **[s → s → s → s]**: 1 case — triple s self-succession exists (N=1, dir)
- **After ok→y CL (N=14 triples): y-LL successors:**
  - y-LL → d: E=1.96×(N=5) — y-terminal lines after ok→y tend to precede d-opening
  - y-LL → t: E=2.60×(N=2, dir)
  - y-LL → y: E=1.13×(N=2) — baseline

### Interpretation

**H_new_AA ANSWERED (NEGATIVE for direct confirmation):** The [d/qok/ok → ch → ch → qot] 3-line chain has N=1 (expected 0.10) — directional but unconfirmable at current corpus size. The corpus is too small (1293 B-dialect triples) to detect specific 3-onset chains reliably.

**New directional: ok→y CL followed by y→d CL (E=1.96×/N=5):** After ok-terminal → y-opening → y-terminal lines, the next line opens with d (1.96×/N=5). This suggests a 3-line pattern: ok-LL → y-LF → y-LL → d-LF. Consistent with ok, y, d all being content-class onset words that cycle through successive lines. N=5 is directional.

**No formal finding:** All multi-step chain patterns are directional (N≤5 for any specific 3-step chain).

---

## Conclusion

H_new_AA ANSWERED (corpus size limit). The B ch "pivot" structure [d/qok/ok → ch → ch → qot] is plausible but unconfirmable at N=1. The corpus has 1293 3-line triples in B-dialect, insufficient for specific 3-onset chain confirmation. NEW directional: ok→y CL followed by y→d CL (1.96×/N=5). No new finding ID.
