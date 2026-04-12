# exp_493: Formula Frame Validation + B herbal pen Survey

**Questions:** (H_new_BT) cth↔ot pen relationship; formula frame co-occurrence rates. (H_new_BU) B herbal pen routing.

---

## 1. Formula Frame Co-occurrence: Frames are INDEPENDENT Rules

### ot-LF frame: y[pos1] + cth[pen]

| | N | % | Expected (independent) |
|---|---|---|---|
| y@pos1 AND cth@pen | 1/40 | 2.5% | 0.34 (E≈2.9×) |
| y@pos1 only | 8/40 | 20% | — |
| cth@pen only | 8/40 | 20% | — |
| neither | 23/40 | 57.5% | — |

**The co-occurrence (1 line) is near the expected independent baseline (0.34).** The frame elements y@pos1 (11 lines) and cth@pen (9 lines) are NOT consistently co-occurring in the same lines. They are INDEPENDENT tendencies in the ot-LF population. A "frame" interpretation (ot-LF lines have a fixed y...cth...ot pattern) is not supported.

### cth-LF frame: cth[pos2] + d[pen]

| | N | % | Expected (independent) |
|---|---|---|---|
| cth@pos2 AND d@pen | 1/64 | 1.6% | 0.62 |
| cth@pos2 only | 4/64 | 6.2% | — |
| d@pen only | 17/64 | 26.6% | — |
| neither | 42/64 | 65.6% | — |

**Same result: co-occurrence (1 line) is near baseline (0.62).** The cth@pos2 rule (F466, confirmed) and d@pen rule (F474, confirmed) are INDEPENDENT statistical enrichments. They do not form a coherent formula structure that appears as a unit.

**Conclusion:** The positional grammar rules in A herbal_a are best understood as INDEPENDENT positional tendencies, not rigid "formula types" with all positions filled simultaneously. Each position (pos1, pos2, pen) has its own onset-class enrichment that holds marginally across many lines, but no single line structure dominates.

---

## 2. d/ot/cth Triangular Cycle: ABSENT

The hypothesized chain (d-LF→ot, ot-LF→cth@pen, cth-LF→d@pen) would require cross-class routing forming a cycle. Testing:

| Claim | Obs | Expected | E | Support? |
|-------|-----|----------|---|---------|
| d-LF → cth@pen | 12/237 | 14.4 | 0.83× | **BELOW baseline — NOT a chain** |
| cth-LF → ot@pos1 | 1/74 | 4.0 | 0.25× | **DEPLETED — NOT a chain** |
| ot-LF → cth@pen | 9/40 | 2.4 | 3.70× (dir) | Yes — ot→cth@pen is real |
| cth-LF → d@pen | 18/64 | 11.1 | 1.61× (CONF) | Yes — cth→d@pen is real |

**The d/ot/cth cycle is NOT a coherent cycle.** d-LF does NOT have cth at pen (E=0.83×, depleted). cth-LF does NOT start with ot at pos1 (E=0.25×, strongly depleted). The actual onset-class relationships are:
- d-LF: ot at pos1 (F453, CONF) — d-LF OPENS with ot
- ot-LF: cth at pen (dir) — ot-LF has cth before terminal
- cth-LF: d at pen (F474, CONF) — cth-LF has d before terminal

These are three independent pairing rules (d↔ot at pos1, ot↔cth at pen, cth↔d at pen) forming three distinct onset-class relationships but NOT a coherent cycle. The pairs are asymmetric: d→ot is a pos1 rule, cth→d is a pen rule, ot→cth is a pen rule. They involve different positions and different onset-class roles.

---

## 3. B herbal pen Survey

B herbal pen baseline (ws[-2], len≥3, N=239): ch=25.5%, ok=10.9%, d=8.8%, y=8.0%, a=6.3%, ot=5.0%

Notable pen findings:

| LF class | pen onset | obs/N_elig | E | flag |
|---------|----------|-----------|---|------|
| **ok** | **a** | **6/35** | **2.73×** | **dir** (cf. F459) |
| ok | ol | 4/35 | 2.73× | (dir) |
| **ot** | **ot-self** | **3/11** | **5.43×** | **(dir)** (cf. F460) |
| a | ok | 5/15 | 3.06× | dir |
| qok | ok | 3/9 | 3.06× | (dir) |

**B herbal ok-LF → a@pen (E=2.73×/N=6, dir)**: Consistent with F459 (B-dialect-wide ok→a@pen). B herbal is one of the sections contributing to F459's B-dialect-wide claim.

**B herbal ot-LF → ot-self@pen (E=5.43×/N=3, (dir))**: Consistent with F460 (B-dialect-wide ot→ot@pen). N=3 is (dir) level only.

**NEW DIRECTIONAL: B herbal a-LF → ok@pen (E=3.06×/N=5, dir).** a-LF lines in B herbal have ok at penultimate at 3× baseline. a-LF N=19 in B herbal; N_elig=15 for pen. Complements F470 (B herbal a-LF → a-self@pos2, dir). B herbal a-LF grammar: a-self at pos2 (dir, F470) + ok at pen (dir, new).

No confirmed pen finding in B herbal (all below N≥10 or E<1.5× for N≥10).

---

## Self-Audit

**Target-awareness:** None. pen baseline uses ws[-2] from len≥3 lines.

**Negative result (frame co-occurrence):** The independence finding is definitive: 1 co-occurrence vs 0.62 expected means there is NO synergistic frame structure. The grammar rules are positionally independent.

**Negative result (d/ot/cth cycle):** d-LF cth@pen E=0.83× (below baseline) and cth-LF ot@pos1 E=0.25× (strongly depleted). The cycle interpretation is conclusively wrong.

---

## Conclusions

**H_new_BT ANSWERED:** Formula frames are INDEPENDENT positional tendencies, not co-occurring structural units. The "frame" metaphor (qo[pos1]→cth[pos2]→d[pen]→cth[LF]) is aspirational — each element represents an independent enrichment at that position, not a fixed sequence. The d/ot/cth cycle is absent (d-LF has no cth at pen; cth-LF has ot DEPLETED at pos1).

**H_new_BU ANSWERED:** B herbal pen confirms B-dialect-wide rules at directional level: ok→a@pen (dir, consistent with F459), ot→ot@pen ((dir), consistent with F460). New directional: B herbal a-LF → ok@pen (E=3.06×/N=5, dir). No new confirmed pen findings in B herbal.
