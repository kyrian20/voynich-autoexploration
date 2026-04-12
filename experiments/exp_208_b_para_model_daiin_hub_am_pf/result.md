# exp_208: B Para-Opening Formula, daiin Hub in A, Complete B Paragraph Model, -am at A pf_ll

**Date:** 2026-04-11
**Hypotheses tested:** H394 (B para-opening formula), H395 (daiin as hub in A), H396 (complete B paragraph model), H397 (-am words at A pf_ll)
**Data:** eva_zl3b.txt — 264 paragraphs (A=163, B=101), A=9651 words, B=18649 words

---

## H394: B Para-Opening Formula — What Precedes the B qo-class Middle Content?

**Hypothesis:** B PS is enriched for pch/p-onset (per F203: pch@PS=22.32×). B first-line body may have a different opener than A's sh-body.

**Result: SUPPORTED**

B PS (n=101):
- p=36(35.64%/19.78×) >> t=18(17.82%/7.13×) > k=13(12.87%/5.61×) > f=3(2.97%/10.26×)
- ch=0.13×, d=0.30×, qok=0.15×, sh=0× — strongly excluded
- Top B PS words: pchedar(3), tchedy(3), pchedal(2) — all p/t-onset with pch- or tch- prefixes; several carry edy-suffix

B first-line body (pos≥1, line_idx=0, n=611):
- o(2.60×), y(1.88×), qo(1.70×), d(1.37×), sh(1.31×), qot(1.31×), f(6.22×, n=11); ch(0.67×), qok(0.60×), ok(0.55×), l(0.51×) depleted

**Key finding:** B PS uses the SAME onset class formula as A PS: p/t/k/f enriched (A: p=23.78×/f=14.35×/t=6.04×/k=3.36×; B: p=19.78×/f=10.26×/t=7.13×/k=5.61×). Both dialects share the same para-opening gallows+ch onset classes. The B first-line body DIFFERS from A: B body = o(2.60×)/y(1.88×)/qo(1.70×) while A body = sh(1.71×)/o(2.12×)/qo(1.69×). In B, y-onset is enriched at first-line body (1.88×), replacing A's sh-enrichment (1.71×). Both share o/qo enrichment at first-line body. Both dialects deplete ch and qok throughout first lines.

---

## H396: Complete B Paragraph Model

**Hypothesis:** B paragraph structure has a 3-register model analogous to A.

**Result: SUPPORTED**

B paragraph para-position analysis:

**FIRST lines (n=712):** f(6.79×), p(3.04×), o(2.33×), y(1.66×), qo(1.55×), k(1.41×); ch(0.59×), qok(0.54×), l(0.43×) depleted.

**MIDDLE lines (n=17470):** All near baseline (0.99–1.03×). No onset class is more than marginally enriched or depleted. B middle lines are essentially uniformly distributed across all onsets.

**LAST lines (n=467):** y(1.51×), s(1.59×), ot(1.33×), ok(1.22×), ch(1.11×) enriched; qot(0.16×), qo(0.45×), qok(0.70×) depleted. qot depletion (0.16×) at B last lines is the sharpest positional grammar constraint in the B last-line register.

Line-by-line (line_idx=0,1,2...):
- Line 0: f/p/o/y/qo enriched; ch/qok/l depleted
- Line 1: d(1.45×)/ot(1.40×)/ok(1.29×)/y(1.36×) enriched; l(0.59×)/qo depleted
- Line 2: cth(2.51×)/y(1.59×)/qot(1.42×)/d(1.38×) enriched
- Line 3: cth(1.61×)/ch(1.25×)/d(1.22×) enriched
- Line 4: cth(2.21×)/t(1.57×)/ot(1.17×) enriched
- Line 5+: all near baseline (~1.0×); cth(0.84×) slightly depleted

**B 3-register paragraph model:**
- Register 1 — First line: PS=p/t/k/f formula (identical onset classes to A) + body=o/y/qo; ch/qok depleted throughout first line
- Register 2 — Middle lines (1–4): Near-uniform distribution; cth mild enrichment at lines 2–4; qo-class present at baseline; no dominant class
- Register 3 — Last line: y/s/ot/ok enriched; qot(0.16×)/qo(0.45×)/qok(0.70×) depleted

**A vs B first-line comparison:**
- PS formula: SHARED (p/t/k/f onset classes both dialects)
- First-line body: A=sh-dominant(1.71×)/o/qo; B=o-dominant(2.60×)/y/qo. sh enrichment is A-specific at first-line body; y enrichment is B-specific.
- Both dialects deplete ch/qok throughout first lines.

**A vs B last-line comparison:**
- A last lines: d-onset(1.67×)/daiin(1.88×) dominant
- B last lines: y(1.51×)/s(1.59×)/ot(1.33×)/ok(1.22×)/ch(1.11×); qot(0.16×) and qo(0.45×) excluded
- qot is the B-specific exclusion from para-closing (0.16×); d is the A-specific enrichment (1.67×) and B-specific exclusion (0.16×)

---

## H395: daiin as Central Hub in A — Bridge Between sh-Domain and cth-Domain

**Hypothesis:** daiin functions as register bridge — enriched at end of first lines (transitioning to cth-content), and daiin→cth enrichment may vary by paragraph register.

**Result: PARTIALLY SUPPORTED**

daiin base rate in A: 443/9651 = **4.59%** (computed manually from line-index counts: 25+53+56+42+43+224 = 443).

Note: the script's `daiin_base_rate` was 0.00× due to a bug (tracking onset labels not words); raw counts are used directly for interpretation.

**daiin by position (line-last):**
- WP-LL: 93/1549 = 6.00% → **1.31×** enriched
- PF-LL: 13/163 = 7.98% → **1.74×** enriched
- First-line LL (last word of first para line): 6/163 = 3.68% → **0.80×** depleted

**daiin by paragraph line index:**
- Line 0 (first): 25/1011 = 2.47% → **0.54×** depleted
- Line 1: 53/1111 = 4.77% → **1.04×** (baseline)
- Line 2: 56/1026 = 5.46% → **1.19×** enriched
- Line 3: 42/830 = 5.06% → **1.10×** mildly enriched
- Line 4: 43/760 = 5.66% → **1.23×** enriched
- Line 5+: 224/4913 = 4.56% → **0.99×** (baseline)

**daiin→cth by paragraph register:**
- First-line: 1/19 daiin-bigrams = 5.26%; cth baseline 3.68% → **1.43×**
- Middle lines: 40/283 = 14.13% → **3.84×** (dominant; vastly stronger than first/last)
- Last line: 2/35 = 5.71% → **1.55×**

**sh→daiin by paragraph register:**
- First-line: 6/133 sh-bigrams = 4.51%; daiin base 4.59% → **0.98×** (not enriched)
- Middle lines: 22/675 = 3.26% → **0.71×** depleted
- Last line: 1/19 = 5.26% → **1.14×** (n=1, not meaningful)

**Interpretation:** H395 is PARTIALLY SUPPORTED.

daiin IS enriched at WP-LL (1.31×) and PF-LL (1.74×), confirming its para-closing role. daiin IS depleted at first-lines (0.54×), meaning it does not appear at the register boundary between first-line (sh-domain) and middle-lines. daiin→cth is strongest in MIDDLE lines (3.84×), with first-line and last-line daiin→cth enrichment much weaker (1.43× and 1.55×). This means daiin functions primarily as a MIDDLE-LINE cth-hub, not as a first-to-second-line bridge.

sh→daiin is NOT enriched across any paragraph register (0.71–0.98×). The F205 finding that daiin is the top RAW-COUNT successor of sh (29 instances) reflects daiin's overall high frequency (4.59%), not a specific sh→daiin grammatical preference.

**Revised H395 conclusion:** daiin is the A-dialect cth-hub concentrated in MIDDLE paragraph lines (3.84× cth-attraction there), enriched at line-last positions (WP-LL 1.31×, PF-LL 1.74×), and depleted in first paragraph lines (0.54×). daiin does not bridge sh-domain (first-line) to cth-domain (middle-line) via sh→daiin→cth pipeline — instead, daiin operates independently as a middle-line cth-attractor. The "hub" characterization holds for middle-line grammar but not for inter-register bridging.

---

## H397: -am Suffix at A/B pf_ll vs WP-LL

**Hypothesis:** -am enrichment may be specifically concentrated at PARAGRAPH-FINAL LL beyond normal WP-LL enrichment.

**Result: NOT SUPPORTED**

A-dialect -am (base rate=1.979%):
- LF: 0.526% (0.27×) — depleted
- MID: 1.054% (0.53×) — depleted
- WP-LL: 6.955% (**3.51×**) — strongly enriched
- PF-LL: 6.623% (**3.35×**) — strongly enriched

A: WP-LL (3.51×) ≈ PF-LL (3.35×). -am enrichment is equal at regular line-last and paragraph-final line-last. There is no paragraph-level -am formula.

B-dialect -am (base rate=2.032%):
- LF: 0.249% (0.12×) — strongly depleted
- MID: 0.397% (0.20×) — strongly depleted
- WP-LL: 13.595% (**6.69×**) — very strongly enriched (consistent with C005: 6.811×)
- PF-LL: 6.383% (**3.14×**) — enriched but LESS than WP-LL

B: WP-LL (6.69×) >> PF-LL (3.14×). In B, -am is significantly LESS enriched at paragraph-final lines than at regular line-last. The PF-LL dilution in B may reflect that B paragraph-closing words (ok/ch/ot onset from F207/H392) are not -am suffix words.

A -am by line index:
- Line 0 (first): 0.35× depleted (consistent with first-line sh/o vocabulary)
- Line 1: 1.05× (baseline)
- Line 2: 1.82× (enriched — but this is line-wide, -am concentrated at LL of each line)
- Line 3: 0.49× (depleted)
- Line 4: 0.66× (depleted)
- Line 5+: 1.09× (baseline)

No consistent progression. The -am by-line pattern is complex and does not suggest a paragraph-level -am rule.

Top A WP-LL -am words: dam(25), otam(7), cham(6), am(5) — dam is the dominant A WP-LL -am word.
Top A PF-LL -am words: am(2), then 8 words with pf_ll=1 each — no concentrated formula.
Top B WP-LL -am words: am(30), otam(21), dam(19), qokam(19), okam(14) — diverse -am words.
Top B PF-LL -am words: cheam(1), oram(1), okeoam(1), cphedam(1), cheokam(1), okam(1) — no formula.

**Interpretation:** -am is a uniform LL class in both dialects. In A, it appears equally at WP-LL and PF-LL (no paragraph-level specificity). In B, it is LESS enriched at PF-LL than WP-LL — the B para-closing vocabulary (ok/ch/ot onset words) dominates PF-LL and dilutes -am. The committed claim C005 (-am LL enrichment in B) is a LINE-LEVEL phenomenon, not a paragraph-level one. -am does NOT function as a paragraph-closing marker in either dialect.

---

## Limitations

H394: B PS n=101 — onset enrichments reliable (top 3: p/t/k have n=13-36). Top B PS word pchedar(n=3) is low-count. The k-onset enrichment (5.61×) is lower than A's k (3.36×) — note the rank order differs slightly from A (in A: p>f>k>t; in B: p>f>t>k at PS, i.e., f and t have swapped relative positions compared to F198). This warrants checking against F198's B PS data (F198 reported k=9.91× as highest; discrepancy likely because F198 measured all PS words while this experiment measures onset enrichments differently — F198 used a 5-position tier classifier, this uses raw line position).

H395: daiin base rate was not computed by the script (bug: `a_total_words` tracks onset labels, not words); manually computed as 443/9651=4.59%. The enrichment values and conclusions are manually derived from raw counts and are correct. sh→daiin n=133 (first line), 675 (middle), 19 (last) — last-line n too small for reliable sh→daiin measurement.

H396: B "middle lines" bucket (n=17470) dominates because most B words are in lines 5+. Lines 2-4 show cth enrichments (2.51×/1.61×/2.21×) but n is modest (711-758 words per line). B cth is rare (0.26% base) so small absolute counts (cth n=3-5 per line) drive these enrichments — treat as directional only.

H397: A PF-LL n=151 (adequate for onset/suffix class estimates); am at A PF-LL n=10 — rate reliable (6.62%), magnitude has CI. B PF-LL n=94 adequate. B WP-LL n=2295 highly reliable (am=312, 13.6%). The by-line-index -am analysis is uninterpretable because it counts all positions at each line depth, not just LL; the pattern reflects mixture of positions, not a clear signal.

---

## Self-Audit

**Target-awareness:** No target-aware elements identified. This is a descriptive characterization experiment with no simulation parameters. Positional enrichments are computed against within-corpus baselines.

**Feature-destroying implementation:** No feature-destroying implementation details identified. The parse_corpus() function is the established working version. The daiin base rate bug (tracking onset labels not words) did not affect the raw counts used in interpretation; all enrichments were manually derived from correct raw numbers.

**Extrapolation:** No extrapolation beyond tested data. Claims are: (a) B PS uses p/t/k/f onset formula (n=101 paragraphs — reliable); (b) daiin→cth is strongest in middle lines (3.84× from 40/283 daiin-bigrams); (c) sh→daiin is not enriched (0.71-0.98× from n=133-675); (d) -am WP-LL ≈ PF-LL in A (3.51× vs 3.35×). No structural claims beyond the tested data.

**Negative-result scope:** H397 "not supported" is scoped to: -am does not specifically concentrate at paragraph-final (pf_ll) beyond normal line-last enrichment in either dialect. The C005 committed claim (-am LL enrichment in B, 6.811×) is a line-level claim and is not contradicted — confirmed at WP-LL = 6.69× (consistent with C005). The H395 partial non-support (sh→daiin→cth pipeline not established) is scoped to: sh→daiin is not an enriched bigram (0.71-0.98×). The finding that daiin is top raw-count sh-successor was correctly reported in F205 as a count, not an enrichment.

**Control behavior:** No controls used in this experiment. Enrichments are vs within-corpus onset/word baselines. Expected behavior: paragraph-level grammar should show non-uniform onset distributions at first/middle/last positions — observed and confirmed for both dialects. The B middle-line near-uniform distribution was somewhat unexpected (qo-class ~1.0× despite being MID-dominant by the 5-tier classifier); however, the 5-tier classifier classifies position within the line (LF/MID/LL/etc.), while paragraph line-index (first/second/etc.) is a different dimension. B qo-class is MID (within-line position) dominant but is not concentrated at specific paragraph LINE INDICES.

---

## Conclusion

**H394 SUPPORTED:** B PS uses the SAME p/t/k/f onset class formula as A (p=19.78×/t=7.13×/k=5.61×/f=10.26×). The dialects share para-opening onset grammar despite differing suffix paradigms. B first-line body differs: o(2.60×)/y(1.88×)/qo(1.70×) vs A's sh(1.71×)/o(2.12×)/qo(1.69×). y-onset enrichment at first-line body is B-specific; sh enrichment is A-specific.

**H396 SUPPORTED:** B 3-register paragraph model: [First line: p/t/k/f PS + o/y/qo body; ch/qok depleted] → [Middle: near-uniform; cth mildly elevated at lines 2–4] → [Last line: y/s/ot/ok enriched; qot(0.16×)/qo(0.45×) excluded]. B middle lines are dramatically less structured than A middle lines (which have cth enrichment 1.13×). B's paragraph grammar is concentrated at boundary registers (first-line and last-line); middle lines are unstructured.

**H395 PARTIALLY SUPPORTED:** daiin is enriched at WP-LL (1.31×) and PF-LL (1.74×); depleted at first para lines (0.54×); daiin→cth is strongest in MIDDLE lines (3.84×). However, sh→daiin is NOT enriched (0.71-0.98×). daiin is a middle-line cth-hub, not a first-to-second-line register bridge. The "hub" characterization holds for middle-line grammar but not for inter-register bridging.

**H397 NOT SUPPORTED:** -am is equally enriched at A WP-LL (3.51×) and PF-LL (3.35×) — no paragraph-level formula. In B, -am is LESS enriched at PF-LL (3.14×) than WP-LL (6.69×). -am is a line-last class; it does not mark paragraph endings specifically.
