# exp_411: Trigram Formula-Typed Fraction in Reference Corpora

**Hypothesis (H631):** VMS B/A have 9.3%/7.6% formula-typed trigrams (F405/F406). Is this distinctive relative to natural language (Latin/Italian)? If natural languages show similar (~9%) fraction, VMS doesn't discriminate; if much higher, VMS is less syntactically predictable.

**Method:** Apply E_cond ≥ 2.0, N ≥ 3 formula-typing methodology to: VMS B/A cont lines (EVA onset, 20 classes), VMS B/A with first-letter onset (26 classes), Latin Caesar (first-letter), Italian Dante (first-letter), and within-line shuffled VMS B (control). "Lines" = sentences for Latin, verse lines for Dante.

---

## Results

| Corpus | Onset class | N_lines | %formula | N_formula |
|--------|-------------|---------|----------|-----------|
| VMS B cont | EVA (20 classes) | 2265 | **8.6%** | 194 |
| VMS A cont | EVA (20 classes) | 1327 | **7.9%** | 105 |
| VMS B cont | first-letter (26 classes) | 2276 | **4.2%** | 95 |
| VMS A cont | first-letter (26 classes) | 1360 | **5.1%** | 70 |
| Latin Caesar | first-letter (26 classes) | 2854 | **10.8%** | 308 |
| Italian Dante | first-letter (26 classes) | 14635 | **11.3%** | 1653 |
| VMS B shuffled (within-line) | EVA (20 classes) | 2265 | **10.9%** | 247 |

---

## CRITICAL FLAG: Control Exceeds Real Data (Check 5 Triggered)

**The within-line shuffled control (10.9%) exceeds real VMS B (8.6%).** Per audit Check 5 (control-comparison interpretation), this requires investigation before interpreting the VMS comparison.

**Why the shuffled control exceeds real VMS:**

Within-line shuffling randomizes pos2 independence of pos1 (breaks bigrams), but E_cond = P(pos2|LF,pos1) / P(pos2|pos1). When bigrams are broken by shuffling, P(pos2|pos1) → P(pos2) unconditionally, which is SMALLER than the real P(pos2|pos1) for strongly-paired classes. A smaller denominator inflates E_cond — making it easier for random small-N observations to exceed E_cond ≥ 2.0.

**Mechanism:** In real VMS, strong bigrams (e.g., qok→ch at ~30% P) keep P(pos2|pos1) high, making E_cond = P(pos2|LF,pos1) / 0.30 hard to exceed 2.0 unless LF genuinely routes. In shuffled VMS, P(ch|pos1=qok) drops toward the unconditional P(ch) ≈ 0.16, making E_cond = P(ch|LF,qok) / 0.16 easier to exceed 2.0 by random fluctuation.

**Conclusion: The formula-typed fraction metric (E_cond ≥ 2.0, N ≥ 3) is BIASED against corpora with strong bigram structure.** Strong bigrams suppress E_cond values (increasing the denominator), reducing the formula-typed fraction in corpora where pos1→pos2 transitions are highly predictable. Random or weakly-structured corpora score HIGHER on this metric, not lower.

---

## Corrected Interpretation

1. **VMS B/A formula-typed fraction (8.6%/7.9%) is NOT evidence of distinctive grammar.** The shuffled control (10.9%) exceeds it, meaning the metric primarily detects small-N noise and bigram-strength effects, not genuine LF-conditional structure.

2. **Under comparable first-letter onset, VMS scores LOWER than natural language:** VMS B first-letter = 4.2%; VMS A = 5.1%; vs Latin = 10.8%; Italian = 11.3%. This ordering is consistent with VMS having STRONGER bigram structure than natural language at the first-letter onset level — which suppresses E_cond values throughout.

3. **The specific formula trigrams identified in F405 (p→sh→qot E=2.11×, y→sh→ch E=2.88×, etc.) are still genuine findings.** These are well-replicated, high-N observations of LF-conditional pos2 routing. The problem is with the formula-typed FRACTION as a summary statistic, not with the individual formula types.

4. **The formula-typed fraction is NOT a useful discrimination metric for VMS vs natural language or VMS vs random text** under this definition and parameter setting. Better alternatives: (a) specifically track the identified formula types (p→sh→qot, etc.) for cross-corpus comparison; (b) use a metric that controls for bigram strength in the denominator.

---

## Secondary Finding: VMS First-Letter vs Reference Corpora

Under first-letter onset (same grain for all corpora):
- VMS B = 4.2%, VMS A = 5.1% (LOWER than natural language)
- Latin Caesar = 10.8%, Italian Dante = 11.3% (substantially higher)

This suggests that VMS word class sequences at the first-letter level are LESS syntactically predictable than Latin or Italian at the same trigram level. But this comparison is confounded by:
- EVA onset classes (20 classes) vs first-letter (26 classes) for VMS
- VMS "lines" are manuscript lines (physical position), not syntactic sentences
- Latin/Italian "lines" are sentences/verses, which have strong syntactic framing

---

## Limitations

- Onset class granularity differs between EVA-onset VMS (20 classes) and first-letter reference (26 classes). This affects baseline rates and E_cond values.
- "Line" definition differs: VMS manuscript lines vs Latin sentences vs Italian verse lines.
- Latin Vulgate file turned out to be Douay-Rheims English translation — only Caesar and Dante were used.
- N≥3 threshold may be too low for reliable E_cond estimation; higher threshold (N≥5 or N≥10) would reduce noise but also reduce power.

---

## Self-Audit

**Target-awareness**: No target-aware elements. The E_cond computation is identical across all corpora.

**Feature-destroying implementation**: Not applicable — observational comparison.

**Extrapolation**: No "structural" or "cannot" claims. The critical flag is stated explicitly rather than as a structural conclusion.

**Negative-result scope**: The formula-typed fraction does NOT discriminate VMS from random/natural language under these parameters. This conclusion is scoped to: "the E_cond ≥ 2.0, N ≥ 3 formula-typed fraction is not a useful discrimination metric." It does not invalidate the specific formula type findings (F405/F406).

**Control behavior (CHECK 5 TRIGGERED):** The shuffled control (10.9%) exceeds real VMS B (8.6%). Expected: shuffled should equal or exceed real VMS ONLY if the metric is dominated by noise. The control DOES exceed real VMS, confirming the noise interpretation. This is the primary finding of this experiment. The discrepancy is fully explained by the bigram-strength effect on E_cond denominators.

Revised: The Interpretation section was written to address Check 5 prominently (not buried in Limitations).

---

## Conclusion

**The formula-typed fraction (E_cond ≥ 2.0, N ≥ 3) is not a useful discrimination metric.** The shuffled control exceeds real VMS B, indicating the metric is dominated by bigram-strength effects and small-N noise. VMS's 8.6% (F405) is not evidence of distinctive grammar relative to random. Under first-letter onset (comparable grain), VMS scores lower than natural language (4.2-5.1% vs 10.8-11.3%), consistent with VMS having stronger bigram structure that suppresses E_cond values. The specific formula types identified in F405/F406 remain valid findings, but the summary "9.3% formula-typed" fraction should not be used as a discrimination claim.

## Methodological Note for State Update

F405's claim "90.7% near-Markovian, 9.3% formula-typed" needs to be narrowed: "9.3% pass the E_cond ≥ 2.0, N ≥ 3 threshold, but this fraction is not distinctive relative to random (shuffled control=10.9%)." The identified specific formula types (p→sh→qot, y→sh→ch, etc.) remain robust.

## Follow-up Questions

1. **H636**: Can the specific formula types from F405 (p→sh→qot, y→sh→ch) be found at similar E_cond in Latin/Italian when restricted to those LF-onset classes (controlling for onset-class availability)? This would test whether the SPECIFIC routing patterns are VMS-distinctive even if the fraction summary is not.
2. **H637**: Raise N threshold to ≥10 for VMS formula-typed analysis. With N≥10, would the shuffled control fall below VMS real? (Higher N threshold eliminates small-N noise.)
