# exp_287: H491 — Position-Conditional Suffix Length Selection
**Date:** 2026-04-11
**Hypothesis:** H491 — Biasing suffix selection toward shorter suffixes at high word_idx (within-line position) steepens the MID word-length slope beyond the gamma+alpha ceiling
**Script:** script.py
**Architecture base:** exp_286 (gamma=0.30, alpha=0.20, p_ll_mf=0.00, p_lf_mf=0.50, p_mf=0.20) — 15-mechanism B-dialect simulation

---

## Result: H491 CONFIRMED — MAJOR IMPROVEMENT

Suffix length bias (beta=0.30) at word_idx≥2 achieves:
- **MID slope: −0.0504** (VMS=−0.058 = **87% of target**, up from 55% at exp_286)
- **Menzerath r: −0.1013** (VMS=−0.225 = **45% of target**, up from 23%)
- **19/19 PASS** maintained

This is the largest single-mechanism Menzerath r improvement in the simulation history.

---

## Sweep Results

| beta | Pass   | menz_r  | MID slope | word_len_mean | edy_rate |
|------|--------|---------|-----------|---------------|----------|
| 0.00 | 19/19  | −0.0491 | −0.0314   | 5.416         | 0.1686   |
| 0.10 | 19/19  | −0.0715 | −0.0361   | 5.368         | 0.1683   |
| 0.20 | 19/19  | −0.0845 | −0.0444   | 5.327         | 0.1624   |
| 0.30 | 19/19  | −0.1112 | −0.0513   | 5.293         | 0.1665   |
| 0.50 | **17/19** | −0.1302 | −0.0618 | 5.211        | 0.1511   |

beta=0.50 fails 2 metrics — likely edy_rate (0.1511, below 80% boundary) due to long-suffix suppression. beta=0.30 selected as ceiling.

---

## Full Run: beta=0.30, N=30

| Metric          | VMS    | Sim    | %VMS   | Status |
|-----------------|--------|--------|--------|--------|
| am_ll           | 6.5498 | 6.8116 | 104.0% | PASS   |
| d_ll            | 1.3625 | 1.2244 | 89.9%  | PASS   |
| y_lf            | 3.1837 | 2.9124 | 91.5%  | PASS   |
| ss_mean         | 1.1640 | 1.3583 | 116.7% | PASS   |
| adj_rate        | 0.0090 | 0.0091 | 101.2% | PASS   |
| qok_lf          | 0.7450 | 0.7358 | 98.8%  | PASS   |
| d_lf            | 2.1178 | 1.8764 | 88.6%  | PASS   |
| s_lf            | 4.4422 | 4.3629 | 98.2%  | PASS   |
| ch_ll           | 0.9653 | 1.0005 | 103.6% | PASS   |
| ok_ll           | 1.0028 | 1.1201 | 111.7% | PASS   |
| qok_ll          | 0.6121 | 0.6004 | 98.1%  | PASS   |
| ss_d            | 1.5850 | 1.4839 | 93.6%  | PASS   |
| ss_y            | 1.9550 | 1.8182 | 93.0%  | PASS   |
| am_lf_enr       | 0.1225 | 0.1278 | 104.3% | PASS   |
| am_mid_enr      | 0.1954 | 0.2324 | 118.9% | PASS   |
| edy_rate        | 0.1940 | 0.1619 | **83.5%** | PASS |
| word_len_mean   | 5.4000 | 5.2878 | 97.9%  | PASS   |
| qok_ch          | 1.2670 | 1.2340 | 97.4%  | PASS   |
| global_am_rate  | 0.0203 | 0.0193 | 94.9%  | PASS   |

**TOTAL PASS: 19/19**

### Diagnostic metrics
- Menzerath r: sim=−0.1013, VMS=−0.225 (45%)
- MID slope: sim=−0.0504, VMS=−0.058 (87%)
- LF_wl: 5.891 (VMS=5.732, +2.7%)
- MID_wl: 5.246 (VMS=5.409, −3.0%)
- LL_wl: 4.950 (VMS=5.015, −1.3%)

---

## Mechanism Description

At each MID word generation step, if word_idx ≥ IDX_THRESH (=2):
- Suffix weights multiplied by exp(−beta × max(0, len(suffix) − SHORT_THRESH))
- SHORT_THRESH=2 → suffixes ≤2 chars get no penalty; aiin (4) and eedy (4) penalized ~0.73×; edy (3) penalized ~0.86×
- Short suffixes (am, ey, dy, ol, ar, al — all len 2) receive a relative boost

**Effect:** Later words in a line use shorter suffixes → shorter word lengths at high word_idx → steeper downward MID slope → more negative Menzerath r.

**Why this works better than gamma/alpha:** gamma/alpha bias the COPY-BUFFER draw toward shorter LENGTH-LABELED words — but the buffer vocabulary is limited. Beta acts directly on SUFFIX CHOICE, a finer-grained mechanism with more room to operate.

---

## Architecture Update

**16-mechanism B-dialect simulation:**
1-15: All exp_286 mechanisms (gamma=0.30, alpha=0.20, p_mf=0.20, p_lf_mf=0.50, p_ll_mf=0.00, etc.)
16. **beta=0.30** (position-conditional suffix length bias, IDX_THRESH=2, SHORT_THRESH=2)

**Current Menzerath r status: −0.1013 / −0.225 = 45% of VMS target**

**Remaining gap:** 55% of VMS Menzerath r unaccounted for. MID slope at 87% (close to target); remaining Menzerath gap is partly due to LF_wl>MID_wl being the dominant driver. Further closure likely requires either (a) reducing LF_wl below MID_wl (not desirable — would flip sign) or (b) steepening the within-line gradient beyond what suffix selection achieves. The 45% ceiling may be near-architectural for this design.

**Fragile boundary:** edy_rate at 83.5% (just above 80% floor). beta>0.30 will push edy_rate below the pass boundary.

---

## Self-Audit

1. **Validity**: Sweep design is clean (independent metric, clear ceiling at beta=0.50). Full N=30 confirms N=10 direction. ✓
2. **Surprising**: MID slope reached 87% of VMS target — exceeds expectation from exp_286's architectural ceiling framing. The gamma+alpha ceiling (55%) was specific to THAT mechanism; suffix selection is orthogonal and achieves more.
3. **Battery impact**: 19/19 maintained. edy_rate is the fragile metric (83.5%). Monitor in future experiments.
4. **Committed claims**: No committed claims reference MID slope values. Menzerath r is not in C001-C007. ✓
5. **New hypotheses**: H503 — Can a second sweep now that beta=0.30 is established find a further improvement by jointly re-tuning gamma or alpha? The MID slope at 87% with room in edy_rate suggests careful incremental adjustment might still help. Low priority — 45% Menzerath r may be close to the architectural ceiling.

---

## Finding

See F299 in findings.md.
