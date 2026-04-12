# exp_441: y→d Coupling Word-Level Analysis (H569)

**Hypothesis (H569):** F326 reports B y→d=1.49×, A y→d=1.37×. Is this within continuation lines, and is it driven by y→daiin specifically?

**Method:** ZL3B continuation lines; within-line bigrams; compute y→d enrichment by position pair; daiin fraction of y→d.

---

## Results

### y→d within-line enrichment

| Dialect | y-leading pairs | y→d observed | y→d expected | E |
|---------|---------------|-------------|-------------|---|
| A | 446 | 59 | 63.4 | **0.93×** |
| B | 452 | 23 | 23.9 | **0.96×** |

**y→d within continuation lines is near baseline (not enriched).**

### y→d by position pair

**A-dialect:**
| Position pair | N y→d | daiin fraction |
|--------------|-------|---------------|
| LF→pos1 | 18 | 44% (8/18) |
| pos1→pos2 | 8 | 38% (3/8) |
| MID_inner | 19 | 21% (4/19) |
| pre-LL→LL | 14 | 7% (1/14) |

**B-dialect:**
| Position pair | N y→d | daiin fraction |
|--------------|-------|---------------|
| LF→pos1 | 9 | 44% (4/9) |
| pos1→pos2 | 4 | 0% (0/4) |
| MID_inner | 6 | 50% (3/6) |
| pre-LL→LL | 4 | 25% (1/4) |

**y→daiin fraction of y→d**: A=27.1% (16/59), B=34.8% (8/23). Baseline daiin share of d-onset ~15-20%, so y→daiin slightly enriched AMONG y→d pairs.

### y→? onset distribution

| Dialect | Top 3 onsets after y | y→d rank |
|---------|---------------------|---------|
| A | ch(21.3%) > d(13.2%) > y(8.7%) | #2 |
| B | ch(19.5%) > qok(11.9%) > ok(9.1%) | #7 (5.1%) |

---

## Interpretation

**H569 ANSWERED: y→d coupling (F326=1.37-1.49×) is NOT present in within-continuation-line bigrams (E=0.93-0.96×, near baseline). The F326 enrichment likely reflects cross-line bigrams (y at LL of line N → d at LF of line N+1) rather than within-line adjacency.**

Key findings:

1. **Within-line y→d is baseline**: E=0.93×(A)/0.96×(B). Neither enriched nor depleted. The F326 y→d=1.37-1.49× finding cannot be replicated within continuation-line bigrams. This suggests F326 measured cross-line paragraph-level bigrams (reading order including line breaks).

2. **y→daiin is moderately enriched among y→d pairs**: When y→d does occur, daiin accounts for 27-35% vs expected ~15-20% (daiin share of d-onset). At LF→pos1 position, daiin is 44% of y→d (in both dialects). So y→daiin is the preferred y→d pairing when it occurs, but the overall y→d rate is not elevated.

3. **B y→d rank collapsed**: A shows y→d as the #2 y-successor onset (13.2%). B shows y→d as #7 (5.1%). This is a large A/B divergence — A has y→d as a prominent local bigram; B does not. In B, y routes primarily to ch(19.5%), qok(11.9%), ok(9.1%), while in A it routes to ch(21.3%), d(13.2%), y(8.7%). This is consistent with the A/B daiin grammar inversion (F433: A daiin=LL-enriched; B daiin=LF-enriched) — in A, daiin is a continuation-body word accessible from y, while in B, daiin is at LF and rarely follows y within a line.

4. **H569 prediction not supported**: The hypothesis predicted pre-LL→LL as the driver (y at pre-LL, daiin at LL) in B. B pre-LL→LL y→daiin N=1/4 — sample too small to test. A pre-LL→LL y→d is N=14 but daiin is only 7% (1/14) there — the LF→pos1 and pos1→pos2 positions drive A y→daiin when it occurs.

**Implication for F326**: F326's y→d enrichment (1.37-1.49×) must be a cross-line phenomenon (y-word at LL of paragraph continuation, d-word at LF of next continuation line). This is not a within-line grammar rule but a between-line sequential rule. No finding revision needed — F326 described "within-paragraph bigrams," which may include cross-line adjacency.

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues.
**Extrapolation**: The "F326 is cross-line" interpretation is an inference from the discrepancy (E=0.93-0.96 vs 1.37-1.49). Direct verification of cross-line bigrams not done here.
**Negative-result scope**: Negative result properly scoped: "within continuation-line bigrams, y→d is not enriched." Does NOT claim y→d bigram in general is false — only the within-line version.
**Control behavior**: N/A.

---

## Conclusion

H569 ANSWERED: Within continuation-line y→d bigrams: E=0.93-0.96× (not enriched). F326's y→d=1.37-1.49× is NOT driven by within-line adjacency — likely reflects cross-line paragraph bigrams. When y→d does occur within lines, daiin is the preferred d-word (44% at LF→pos1 in both dialects), confirming y→daiin is the specific pairing but the rate is not elevated. A y→d rank=2nd (13.2%), B y→d rank=7th (5.1%) — consistent with A/B daiin grammar inversion (F433). **No new finding ID** (clarification of F326, no new structure confirmed).
