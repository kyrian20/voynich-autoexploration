# exp_552 result — k-onset full characterization (H_new_FN)

## Audit

**Target-awareness**: None. Standard 4-part methodology.

**Extrapolation**: None.

---

## Results

### Part 1: Vocabulary

| Metric | A herbal_a | B all |
|--------|-----------|-------|
| N k-onset tokens | 354 (3.1%) | 195 (1.9%) |
| #1 word | keey (6.2%) | keedy (12.3%) |
| #2 word | kar (5.9%) | kedy (11.8%) |
| #3 word | kchy (5.6%) | kaiin (6.7%) |
| ch-bench compounds | ~17% (kchy, kchor, kchol, kchey) | kchedy (5.6%), kchdy (4.1%) |
| edy-body | minimal | keedy+kedy+kchedy ~30% |

A: diverse vocabulary with ch-bench compounds (~17%) and e-body forms (keey, keol). B: edy-body dominant (~30%). A→B vocabulary shift: A=mixed/ch-bench; B=edy-body dominant.

### Part 2: Positional Distribution — K IS A POS1-AVOIDER

| Position | A obs/N | A E | B obs/N | B E | A flag | B flag |
|----------|---------|-----|---------|-----|--------|--------|
| pos1 | 32/1961 | **0.52×** | 4/1279 | **0.16×** | **DEPL** | **DEPL** |
| MID | 196/5539 | 1.13× | 140/6335 | 1.15× | — | — |
| LL | 69/1794 | 1.23× | 22/1266 | 0.91× | — | — |
| LF | 53/1961 | 0.86× | 29/1279 | 1.18× | — | — |

**K is a pos1-AVOIDER** — the opposite of s, t, y. pos1 DEPL in both dialects (A: 0.52×; B: 0.16×). K joins the pos1-avoider cluster alongside a (A: 0.16×; B: 0.26×) and ch (A: 0.38×; B: 0.25×). B k pos1 = 0.16× matches the most extreme pos1-avoidance seen (same as A a). K is a mid-line class (MID=1.13-1.15× in both), appearing throughout lines but avoiding the first position.

**Updated pos1-avoider ranking (A herbal_a):**
| Class | A pos1 E | B pos1 E |
|-------|----------|----------|
| a | 0.16× | 0.26× |
| k | 0.52× | 0.16× |
| ch | 0.38× | 0.25× |

### Part 3: Bigrams

**A herbal_a** (297 k-sender bigrams):
- k→cth CONF (E=1.66×/obs=14)
- k→qok DEPL (0.62×/15)
- k→ot DEPL (0.67×/10)
- k→a DEPL (0.67×/10)
- k→ch ~baseline (1.11×/77)

**B all** (166 k-sender bigrams):
- k→ok CONF (E=1.50×/obs=18)
- k→d CONF (E=1.60×/obs=13)
- k→qok DEPL (0.69×/19)

Cross-dialectal: k→qok DEPL in both. A-specific: k→cth CONF (1.66×/14). B-specific: k→ok CONF + k→d CONF. No strong cross-dialectal CONF bigram for k (unlike o→a or s→sh).

### Part 4: k-LF pos1 Profile

**A herbal_a** (N=53 k-LF lines):
- qok@pos1: obs=9, E=2.36× **dir**
- ok@pos1: obs=5, E=2.06× **dir**
- d@pos1: obs=5, E=0.53× DEPL
- l@pos1: obs=3, E=3.70× **(dir)**

K-LF lines in A are opened by template classes (qok dir, ok dir). d is DEPLETED at pos1 for k-LF. Y=0.80× (near-baseline, contrast with other LF classes).

**B all** (N=29 k-LF lines):
- y@pos1: obs=7, E=2.10× **dir**
- d@pos1: obs=9, E=1.61× sub-CONF

B k-LF: y opens at dir level.

---

## New Findings

**F578: k vocabulary** — A: diverse with ch-bench (~17%) and e-body (keey, keol); B: edy-body dominant (~30%: keedy, kedy, kchedy). A→B shift: A=mixed/ch-bench; B=edy-body.

**F579: k positional — pos1 STRONGLY DEPL cross-dialectally** (A: E=0.52×/obs=32; B: E=0.16×/obs=4). K is a pos1-AVOIDER, opposite of s/t/y openers. MID slightly elevated (1.13-1.15×). No CONF at any position. K joins the pos1-avoider cluster with a and ch. B k pos1 = 0.16× is co-extreme with B a (0.26×) and A a (0.16×).

**F580: k bigrams** — A k→cth CONF (E=1.66×/obs=14); k→qok DEPL both (A: 0.62×; B: 0.69×); k→ot/a DEPL A. B k→ok CONF (1.50×/18); k→d CONF (1.60×/13). No strong cross-dialectal CONF bigram. A k→cth CONF: k routes to compound gallows (like d→cth, F555).

---

## Summary

- **H_new_FN CLOSED**: k-onset is a pos1-AVOIDER (F579: pos1 DEPL A 0.52×/B 0.16×) — opposite of s, t, y (which are pos1-CONF openers). K is a MID class (1.13-1.15×), not a line-opener.
- F578: k vocabulary (A=mixed/ch-bench; B=edy-body)
- F579: k positional (pos1 DEPL — joins a and ch as pos1-avoider cluster)
- F580: k bigrams (A k→cth CONF; B k→ok/d CONF; k→qok DEPL cross-dialectally)
- **Updated positional taxonomy for major onset classes:**
  - OPENERS (pos1 CONF): y, s, t + qot (A), d (B)
  - AVOIDERS (pos1 DEPL): a (0.16×), k (0.52×/0.16×), ch (0.38×/0.25×)
  - MID classes: sh (LF DEPL), k, ch (slightly MID elevated)
  - LF classes: d (A), o (B), a (B)
