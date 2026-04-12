# exp_554 result — r-onset full characterization (H_new_FQ)

## Audit

**Target-awareness**: None. Standard 4-part characterization methodology (vocabulary, positional, bigrams, LF pos1) applied to r-onset class, motivated by l→r CONF B (F586).

**Feature-destroying implementation**: None. Standard corpus parsing, MID-baseline for bigrams, overall pos1 distribution as LF pos1 baseline. Consistent with exp_547-553 methodology.

**Extrapolation**: None. A herbal_a results are underpowered (65 r-tokens; only 16 r-LF lines) and reported with appropriate flags. B all results (136 r-tokens; 48 r-LF lines) are better powered.

---

## Results

### Part 1: r-onset vocabulary

**A herbal_a** (65 r tokens, 0.57% of all words):
- raiin: 26.2%, rar: 9.2%, ral: 7.7%, rain: 7.7%, rcheey: 4.6%, ram: 3.1%, ror: 3.1%
- aiin-body dominant (raiin+rain ~34%); lateral forms (ral, rar, ror, rol); some ch-bench (rcheey, rchey)

**B all** (136 r tokens, 1.34% of all words):
- raiin: 18.4%, rol: 7.4%, rain: 5.9%, rchedy: 4.4%, ror: 4.4%, ral: 4.4%, rshedy: 3.7%
- aiin-body still dominant (raiin+rain ~24%); edy-compounds (rchedy, rshedy, rsheedy ~10%); lateral forms persist

A→B: A=aiin-body dominant; B=aiin-body + edy-compounds (~10%) + lateral forms. Low frequency class in both dialects.

### Part 2: r-onset positional distribution

| Position | A obs/total | A E | B obs/total | B E | |
|----------|------------|-----|------------|-----|---|
| pos1 | 1/1961 | 0.09× | 6/1279 | 0.35× | B DEPL |
| MID | 38/5539 | 1.20× | 64/6335 | 0.75× | — |
| LL | 10/1794 | 0.97× | 18/1266 | 1.06× | — |
| LF | 16/1961 | 1.42× | 48/1279 | **2.80× CONF** | B CONF |

**A**: r is extremely rare at pos1 (obs=1; E=0.09× but obs<3, cannot formally flag); LF sub-CONF (1.42×/16). Direction: LF-enriched, pos1-depleted.

**B**: pos1 DEPL (E=0.35×/obs=6); LF CONF (E=**2.80×**/obs=48) — **the strongest B LF enrichment characterized**. Updated B LF CONF ranking: r (2.80×/48) > l (1.85×/145) > ol (1.65×/115) > o (1.58×/57) > a (1.52×/70).

### Part 3: r-onset within-line bigrams

**A herbal_a** (49 r-sender bigrams):
- r→a: obs=8, exp=2.5, E=**3.26×** — **dir**
- r→ot: obs=6, exp=2.5, E=**2.43×** — **dir**
- r→r: obs=2, exp=0.3, E=6.24× — obs too small for threshold
- r→ol DEPL (0.51×/1); r→qok DEPL (0.25×/1) — both small N
- (cross-check) l→r: obs=5, exp=1.2, E=4.02× — **dir** (confirms F586 direction in A)

**B all** (88 r-sender bigrams):
- r→d: obs=7, exp=4.3, E=1.62× — near-CONF (obs<10)
- r→a: obs=5, exp=3.3, E=1.53× — near-CONF (obs<10)
- r→r: obs=2, exp=0.9, E=2.11× — obs too small
- r→ol: obs=3, exp=4.6, E=0.66× — **DEPL**
- r→ot: obs=4, exp=6.5, E=0.62× — **DEPL**
- (cross-check) l→r: obs=17, exp=5.2, E=3.30× — **CONF** (confirms F586 exactly)

**Key reverse coupling test — r→l**:
- A: r→l obs=2, exp=1.1, E=1.87× — elevated but obs<5, cannot claim dir
- B: r→l obs=4, exp=5.1, E=0.79× — BELOW BASELINE

**l→r is DIRECTIONAL, not mutual**: l→r CONF B (3.30×/17) but r→l is flat-to-depleted in B (0.79×). This is structurally different from the o↔a mutual coupling (F566 where both directions are CONF).

### Part 4: r-LF pos1 profile

**A herbal_a** (N=16 r-LF lines — underpowered):
- s@pos1 (dir): E=3.01×/obs=4 — meets (dir) threshold (E≥2.5, obs≥3)
- l@pos1: E=8.17×/obs=2 — too small for threshold
- All other onset classes near/below baseline

**B all** (N=48 r-LF lines):
- qok@pos1: E=1.56×/obs=10 — **CONF**
- y, d, s: near baseline (E=1.08-1.27×, no threshold reached)
- No DEPL signals reaching threshold

B r-LF pos1=qok CONF (1.56×/10): qo-class specifically opens r-terminal B lines. This parallels B ot-LF pos1=t CONF (F540) and B l-LF pos1=ch CONF (F586) — LF-class-specific pos1 grammar.

---

## New Findings

**F587: r vocabulary** — A: aiin-body dominant (raiin 26.2%, rain 7.7%); lateral forms (rar, ral, ror, rol); ch-bench (rcheey). B: aiin-body (raiin 18.4%, rain 5.9%) + lateral forms + edy-compounds (rchedy, rshedy ~8%). A→B: A=aiin-body dominant; B=aiin-body + edy-suffix compounds. R is a low-frequency onset class (A: 0.57%; B: 1.34% of words). The edy-suffix transformation in B (rcheey→rchedy) parallels the cross-class A→B edy-suffix pattern.

**F588: r positional — B LF CONF (E=2.80×/obs=48) — STRONGEST B LF enrichment characterized; pos1 DEPL B (0.35×/6); A direction consistent but underpowered.** B r is the most LF-enriched onset class found. A r: pos1 obs=1 (E=0.09× — cannot formally flag due to obs<3), LF 1.42×/16 (sub-CONF). B LF CONF ranking updated: r (2.80×/48) > l (1.85×/145) > ol (1.65×/115) > o (1.58×/57) > a (1.52×/70). R joins the B LF-enriched class cluster alongside l, ol, o, a — all of these are "lateral/liquid" onset classes (r, l, ol) or vowel-initial classes (o, a). No template class (qot, ot, qok, ok) or opener class (s, t, y) is LF-enriched in B.

**F589: r bigrams — l→r CONF B (E=3.30×/obs=17) CONFIRMED (F586 replication); l→r dir A (E=4.02×/obs=5); r→l NOT elevated in B (0.79×/4) — l→r is DIRECTIONAL; A r→a dir (3.26×/8); A r→ot dir (2.43×/6); B r→ol DEPL (0.66×/3); B r→ot DEPL (0.62×/4). B r-LF pos1: qok CONF (1.56×/10).** The l→r coupling (F586, now F589) is directional: l sends to r at 3.3-4.0× baseline; r does NOT send back to l at elevated rate in B (0.79×). This is structurally different from the symmetric o↔a coupling. R→a: A dir (3.26×/8), B near-CONF (1.53×/5) — potentially a cross-dialectal r→a coupling, but obs insufficient for formal CONF in either dialect. B r→ot DEPL and r→ol DEPL suggest r avoids template/lateral targets in B.

---

## Summary

- **H_new_FQ CLOSED**: r-onset characterized.
- r vocabulary: aiin-body dominant in A; aiin-body + edy-compounds in B. Low-frequency class (0.57% A, 1.34% B) (F587).
- r positional: B LF CONF 2.80×/48 — **strongest B LF enrichment found**; B pos1 DEPL (0.35×/6); A direction consistent but underpowered (F588).
- r bigrams: l→r CONF B CONFIRMED (F586 exact replication); l→r is DIRECTIONAL (r→l flat in B); A r→a dir; B r→ol/ot DEPL; B r-LF pos1=qok CONF (F589).
- **Synthesis**: B LF cluster = r(2.80×)>l(1.85×)>ol(1.65×)>o(1.58×)>a(1.52×) — all lateral/liquid or vowel-initial onset classes. No opener (s,t,y) or template class is B LF-enriched. This cluster is structurally coherent.
- **New hypothesis**: l→r coupling is directional and r is the MOST LF-enriched class. The sequence [l-word][r-word] likely places the r-word at or near LF. Is there a direct l→r→LF formula? Characterize lines ending in r (which begin with qok) for within-line structure.

## Self-Audit

**Target-awareness**: No target-aware elements. Standard baseline tests using corpus-internal MID distribution (bigrams) and overall pos1 distribution (LF pos1 profile).

**Feature-destroying implementation**: No feature-destroying details. Corpus parsing consistent with exp_547-553. l→r cross-check uses the same MID baseline as exp_553, replicating F586 exactly.

**Extrapolation**: All claims within tested data. A results are noted as underpowered (65 tokens, 16 r-LF lines). B results (48 r-LF lines for pos1 profile; 88 r-sender bigrams) are better powered but moderate. No structural claims made. A r pos1=0.09× with obs=1 reported as directional only (cannot flag formally).

**Negative-result scope**: N/A — positive results (B LF CONF, l→r CONF confirmed, B r-LF pos1=qok CONF).

**Control behavior**: No separate control distribution. Baseline is within-corpus: MID-position onset distribution for bigrams; overall pos1 distribution for LF pos1 profile. These baselines are standard and consistent across exp_540-554.
