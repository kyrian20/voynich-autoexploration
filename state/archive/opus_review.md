# Independent Review of working_position.md

**Reviewer**: Opus 4.6
**Date**: 2026-04-10
**Scope**: Assessment of the synthesis document and its six supporting experiments (exp_170–175).

---

## OVERALL ASSESSMENT

The synthesis is the best document in this project. The shift from cataloguing patterns to testing theories is exactly what was needed, and the convergent-failure argument (Naibbe and Timm both fail on the same positional metrics) is genuinely strong. The evidence hierarchy in Section 7 is unusually honest for autonomous agent output.

That said, the document overstates its conclusions in several specific places, contains one likely statistical artifact that it treats as a real finding, uses the word "falsified" too loosely, and leaves the "structured grammar" verdict underdetermined in ways it doesn't fully acknowledge.

---

## 1. VERDICT-BY-VERDICT ASSESSMENT

### 1.1 Cipher hypothesis: "SIGNIFICANTLY WEAKENED" — AGREE, with caveats

The -am LL finding (6.811x in VMS, ~1.0x across 400 Naibbe runs) is devastating for the Naibbe cipher specifically. I agree this is the single most informative result in the entire project.

**Caveats:**

The synthesis correctly notes (Section 4) that "we tested one specific cipher; many cipher variants exist" but then proceeds to argue as though the finding generalizes broadly. The key passage in Section 7 — "No position-blind cipher mechanism can produce line-final suffix specificity of this magnitude" — is a theoretical claim, not an empirical one, and it's actually wrong. A position-sensitive cipher (one that uses different substitution tables depending on line position, which is historically attested in polyalphabetic ciphers) could produce exactly this pattern. The synthesis acknowledges this in the falsification section (experiment 1, Section 8) but doesn't carry that acknowledgment back into the verdict. The honest framing is: "The Naibbe cipher and all position-blind ciphers are ruled out. Position-sensitive ciphers remain viable but untested."

The paragraph-start analysis was broken in exp_170 (2307/2447 B-dialect lines flagged as paragraph starts, acknowledged in the limitations). This means the F101 gallows-at-para-start finding — one of the top 10 robust findings from the characterization phase — was never actually tested against Naibbe. The synthesis quietly drops this metric but doesn't flag the gap.

**Recommendation**: Soften "SIGNIFICANTLY WEAKENED → UNLIKELY" to "SIGNIFICANTLY WEAKENED for position-blind ciphers; position-sensitive ciphers remain open." Flag the untested paragraph-start metric explicitly.

---

### 1.2 Self-citation hypothesis: "FALSIFIED FOR POSITIONAL GRAMMAR" — PARTIALLY AGREE

The positional grammar failure (Timm produces ~1.0x for -am LL and y-onset LF) is convincing and mirrors the Naibbe failure, strengthening the convergent-failure argument.

The self-succession overproduction (Timm 1.53–2.41x vs VMS 1.24–1.69x) and the 4x identical-word-rate excess are good quantitative evidence.

**Problem: No parameter sensitivity analysis.** The Timm simulation used exactly one parameter set: WINDOW=50, COPY_PROB=0.85, MODIFY_PROB=0.25. These are Timm & Schinner's published defaults, but the synthesis treats them as the only possibility. What happens at COPY_PROB=0.5? At MODIFY_PROB=0.6? At WINDOW=10? The claim in Section 4 that "the mechanism cannot simultaneously produce the right amount of self-succession and the right amount of exact word repetition" at "any parameter setting" is asserted without evidence. A parameter sweep showing that no (COPY_PROB, MODIFY_PROB) combination can hit both targets would make this claim defensible. Without it, it's speculation.

The MI analysis (exp_175) adds genuine value: the crossover pattern (VMS above Timm at lag 1, below at lags 2-7) is a qualitatively different MI signature than self-citation predicts. This is the strongest anti-Timm evidence because it's structural, not parametric.

**Recommendation**: Add a parameter sensitivity caveat. The falsification claim is valid for the published parameters and likely robust (the logic about the self-succession/repetition tradeoff is sound), but "any parameter setting" needs a sweep to support it. Also: MODIFY_PROB affects word length — if higher modification rates fix the word-length gap (5.039 → 5.768), do they break something else? This should be checked.

---

### 1.3 Template hypothesis: "FALSIFIED AS SOLE MECHANISM" — AGREE with a reframing concern

The exp_174 residual analysis is the cleanest experiment in the set. Self-succession surviving position control (1.2–1.8x residual) and the -am suffix specificity at LL (6.9x while other suffixes are depleted) are strong evidence that positional slots alone don't explain the data.

**But the "template" being falsified is a straw man version.** The synthesis defines template as "filling fixed positional slots with position-independent fillers from a limited vocabulary." No serious Voynich researcher proposes templates this simple. Stolfi's slot grammar, Zattera's 12-slot model, and Smith's syllable-ranking model are all more sophisticated — they have position-dependent slot contents, conditional character transitions, and constraint propagation. The synthesis falsifies a "generic slot" template but doesn't test whether a "smart template" (with onset-class-aware slot rules) could reproduce the findings. And as the synthesis itself admits: "the template must itself be onset-class-aware, which means it is functionally a grammar."

This is actually the key insight, but the synthesis doesn't fully grapple with its implications. If a sufficiently parameterized template reproduces all findings, and a grammar reproduces all findings, and the two are "functionally equivalent" — then the experiment hasn't discriminated between them. It has shown that the system has more structure than the simplest template, which everyone already knew.

**Recommendation**: Replace "FALSIFIED AS SOLE MECHANISM" with "SIMPLE TEMPLATES INSUFFICIENT; onset-class-aware templates indistinguishable from grammar by this evidence." This is more honest and more useful.

---

### 1.4 Structured grammar: "BEST SUPPORTED" — AGREE it's the last theory standing, but this is weak support

The structured grammar hypothesis is "best supported" primarily because the other three were weakened. It was never directly tested — there is no experiment that generates predictions unique to structured grammar and confirms them. The synthesis acknowledges this ("not a null to falsify, but a framework to elaborate") but then treats it as a positive finding rather than a default.

The internal coherence argument (Section 7, #2) is the strongest positive case: the positional enrichments, self-succession patterns, and sequential grammar form a mutually consistent system. But internal coherence is a necessary condition for any real structure, not a sufficient condition for grammar specifically. A sufficiently complex template system (or a position-sensitive cipher of a language with the right clause-boundary morphology) would also show internal coherence.

**What would actually support "structured grammar" over the remaining alternatives**: Evidence of semantic coherence (different topics use different grammatical distributions in ways correlated with illustration content), productivity (novel word forms following morphological rules), or agreement phenomena (long-range dependencies between grammatical categories within a line). Exp_175's lag-1 MI excess over Timm is suggestive of adjacent-word grammar, but the high-lag findings are problematic (see Section 2 below).

**Recommendation**: Reframe from "BEST SUPPORTED" to "LEAST REFUTED / DEFAULT." Be explicit that structured grammar was never positively tested — it survives by not being the target of any simulation. This is an important distinction for intellectual honesty.

---

## 2. METHODOLOGICAL ISSUES

### 2.1 exp_170 (Naibbe): Mostly sound, one major gap

**Sound**: 400 runs (100x2x2) is adequate. Two plaintext languages and two line-breaking protocols is the right design. The bidirectional check (Naibbe artifacts not in VMS) is a good addition.

**Gap**: Protocol A (sentence-based line breaks) produces lines of 40-80 tokens vs VMS's 8.4-token mean. The synthesis notes this in limitations but doesn't adequately address it: positional enrichment metrics are meaningless when "line-first" means "sentence-first" in a 60-token line. Protocol A results should be de-emphasized or dropped for positional metrics. Protocol B (VMS-length-matched) is the informative condition. The synthesis reports both equally.

**Minor**: The daiin→cth metric being "INSIDE" is correctly identified as uninformative (it's an A-dialect finding tested on B-dialect simulations), but it still appears in the INSIDE count, inflating the "cipher-consistent" tally slightly.

### 2.2 exp_171 (Timm): Parameter sensitivity is the fatal gap

As noted above: one parameter set, no sweep. The seed vocabulary (top-200 B-dialect words by frequency) is also a choice that affects results — seeding with the full B-dialect vocabulary at empirical frequencies would be more faithful to the model.

The paragraph structure (PARA_SIZE=10, fixed) is crude. VMS paragraphs vary in length. This doesn't affect the main conclusions (positional grammar failure) but undermines the paragraph-start comparisons.

### 2.3 exp_172 (Cross-validation): Lenient pass criterion

The PASS criterion (test magnitude >= 50% of train magnitude, same direction) means a finding can lose half its effect size and still "pass." In most validation frameworks, a 50% drop in effect size would raise serious concerns about overfitting. A stricter criterion (e.g., test CI overlaps train point estimate) would be more informative.

The B-dialect LOSO results (11-13/19 per fold) are actually mediocre — about 60-70% of findings generalize across sections. The synthesis frames this as "mostly above-threshold" but 30-40% failure rates in LOSO should prompt more reflection on which specific findings are section-dependent and why.

**The leave-cosmo dismissal is too quick.** "n=32 test lines" is noted as a sample-size artifact, and that's fair, but it also means the cosmo section was never properly validated. If cosmo has different structural properties (which it might — it's a distinct content type), that's informative, not dismissable.

### 2.4 exp_173 (Multiple testing): Scoping issue remains

The correction used m=30 (the nominated candidates), not m=175 (the total number of findings that were ever computed). This is the same issue I flagged in my critique of Sonnet's proposal. The synthesis says "30 candidate findings, 7 families" without acknowledging that these 30 were selected post-hoc from 175+. With m=175, the Bonferroni threshold would be p < 0.000286 instead of p < 0.001667. Looking at the actual p-values, most survivors have p < 10^-6, so only the marginal survivors (F29 at p=1.39e-3, F13 at p=9.58e-4) might be affected. The core findings would survive either threshold. But the principle matters: reporting m=30 when you looked at 175 is a methodological error that should be corrected.

The BH-FDR implementation appears correct (standard step-up procedure). BH is the more appropriate correction here given the correlated test structure.

### 2.5 exp_174 (Slot-grammar residuals): Best experiment in the set

The design is clean: within-stratum position control is the right approach. The product-of-marginals method (not HMM) is exactly what I recommended. The five hypothesis tests are well-chosen and clearly stated.

One concern: the position taxonomy (LF, second, MID, LL, only) conflates all non-boundary positions into "MID." If there are finer-grained positional effects (positions 3, 4, 5 differ from each other), the MID category would absorb them and the residual analysis would miss position-driven effects that a finer-grained template could capture. This likely doesn't change the core conclusion (-am specificity and onset-class LF filtering are too sharp for any template) but it weakens the self-succession residual finding — a 5-position template might reduce the 1.2-1.8x residuals closer to baseline.

### 2.6 exp_175 (Long-range MI): Contains a likely artifact

**The lags 10-12 "ABOVE Timm" finding is almost certainly a finite-sample bias artifact, and the synthesis treats it as a real finding.**

Here's why: MI estimates are positively biased when sample sizes are small (the Miller 1955 correction addresses this, but the script doesn't use it). At lag 10, you're only counting word pairs that are 10 positions apart within the same line — which means only lines with 11+ tokens contribute. B-dialect lines average 8.4 tokens. The number of contributing lines drops sharply: at lag 10, maybe 200-300 lines contribute; at lag 12, maybe 50-100. With 19 onset classes (361 possible pairs), most cells in the joint distribution are empty. The MI estimate in this regime is dominated by sampling noise and is biased upward.

The within-line shuffle comparison is supposed to control for this, but look at the actual numbers: at lag 12, VMS-B = 1.4567, shuffle-within = 1.6694, shuffle-across = 1.6837. The shuffled controls have HIGHER MI than VMS at lag 12. This means the "genuine long-range structure" the synthesis claims at lag 12 is actually weaker than shuffled noise. The synthesis reports VMS as "ABOVE Timm" at lag 12 but fails to note that VMS is BELOW its own shuffled controls.

The lag-1 finding (VMS-B = 0.085 vs Timm = 0.063, ABOVE CI) is robust — it's computed from the full corpus and the signal is clear (within-line shuffle destroys 63%). The lags 2-7 BELOW Timm finding is also robust (large sample, consistent pattern). But the lags 10-12 finding should be retracted or heavily caveated.

**This matters because the synthesis uses lags 10-12 to argue for "genuine long-range structure" (Section 4, self-citation verdict; Section 6, MI structure point 5; Section 7, #1 evidence for grammar). Remove this claim and the MI evidence says: strong adjacent-word structure (lag 1), rapid decay (lags 2-7 below Timm), and nothing reliable beyond that.** That's still useful — it's evidence for local grammar and against copy-window mechanisms — but it doesn't support "grammar depth" claims.

---

## 3. HONESTY OF LIMITATIONS

### What the synthesis gets right

- Section 5 ("WHAT CANNOT YET BE DETERMINED") is good. The acknowledgment that structural analysis cannot determine whether the grammar encodes natural language or is an artificial system is important and correctly stated.
- The confidence table (Section 6) appropriately assigns "Low" to both "VMS is a natural language" and "VMS is a homophonic cipher of any natural language."
- The falsification section (Section 8) is unusually thoughtful, especially the position-sensitive cipher scenario.

### What's NOT being claimed that SHOULD be more explicit

1. **The project has not tested any cipher more sophisticated than Naibbe.** The synthesis implies broad cipher refutation but tested one model. Polyalphabetic ciphers, nomenclators, book ciphers, and especially position-sensitive ciphers remain untested. This should be a bullet in Section 5.

2. **The Timm test used one parameter set.** This should be stated as a limitation, not buried in the experiment config.

3. **The cross-validation pass rate for B-dialect LOSO (60-70%) is mediocre.** The synthesis frames this as "above threshold" but doesn't discuss what the 30-40% failure rate means — specifically, which findings are section-dependent and whether that section-dependence is evidence for or against grammar.

4. **The A-dialect was never tested against Naibbe.** Naibbe was designed for B-dialect, so this is expected, but most of the strongest findings (y-onset LF in A, cth LF depletion in A, d LL in A) are A-dialect findings that were compared against a B-dialect simulation. The synthesis should note this asymmetry.

### What IS being claimed that is shakier than admitted

1. **"VMS long-range structure exceeds Timm's window" (Section 4, point 3; Section 7)** — this is the lag 10-12 artifact discussed above. The claim should be retracted or heavily caveated.

2. **"Self-citation falsified at any parameter setting" (implied in Section 4)** — no parameter sweep was performed. The claim is plausible but unproven.

3. **24/30 survive Bonferroni** — uses m=30, not m=175. The number surviving at m=175 would be ~22/30 (nearly the same, but the principle matters).

4. **"Convergent failure" across Naibbe and Timm** — this is strong evidence, but both models are position-blind. The convergence demonstrates that position-blind mechanisms fail. It does not demonstrate that all generation mechanisms fail. A position-sensitive mechanism (cipher or template) was never tested.

---

## 4. SUBCATEGORIES WITHIN "STRUCTURED GRAMMAR"

The synthesis concludes "structured grammar is best supported" but acknowledges (Section 5) that this doesn't distinguish between:

1. **Natural language with unusual typology** — a language where -am is a clause-final particle, y-onset marks clause-continuation, etc.
2. **Constructed/artificial language** — a designed system with deliberate positional rules.
3. **Position-sensitive cipher** — a cipher that uses different tables/rules at line-first vs mid-line vs line-final positions, encoding a natural language that itself lacks these positional properties.
4. **Structured glossolalia** — production by someone who internalized positional rules and produces text that follows them without encoding meaning.
5. **Hybrid: self-citation + grammar** — a scribe who follows grammatical rules but also tends to copy from nearby text (producing the intermediate self-succession levels).

**Can the current evidence discriminate among these?**

| Evidence | NL | Constructed | Pos-Cipher | Struct-Gloss | Hybrid |
|----------|-----|-------------|------------|-------------|--------|
| -am LL 6.8x | + (clause-final morpheme) | + (designed rule) | + (position-aware encoding) | + (internalized rule) | + |
| y-onset LF 3.5x | + (clause-initial class) | + (designed rule) | + (position-aware encoding) | + (internalized rule) | + |
| Self-succession 1.2-1.7x | + (topical continuity) | 0 (no clear prediction) | 0 | - (overproduction expected) | + (explains intermediate level) |
| Suffix paradigm productivity | + (morphological paradigm) | + (designed paradigm) | + (source NL paradigm) | - (no productive morphology expected) | + |
| A/B dialect split | + (two registers) | + (two designed variants) | + (two source languages or keys) | 0 (possible with two glossolalia modes) | + |
| Lag-1 MI > Timm | + (grammar) | + (grammar) | + (source grammar preserved) | + (rule-following) | + |

**The answer is no — the evidence does not discriminate among these subcategories.** Every robust finding is consistent with all five subcategories. The synthesis's Section 5 acknowledges this but understates the problem: the "structured grammar" verdict is really just "has structure" — it's the complement of the three rejected hypotheses, not a positive identification.

The most promising discriminator would be **semantic coherence** (does grammatical category distribution correlate with illustration content?), but this requires external data (plant identification, illustration classification) that the project doesn't have. The second-best would be **productivity testing**: can the grammar model predict novel forms that actually appear in the corpus? This was proposed in my earlier critique (absent-cell prediction test) but wasn't implemented.

---

## 5. FOR PUBLICATION

### Changes to framing

1. **Title/abstract**: Frame as "ruling out two generation mechanisms" rather than "supporting structured grammar." The negative results (Naibbe fails, Timm fails) are the actual findings. The positive conclusion (grammar) is a default, not a discovery.

2. **Use "position-blind mechanisms" not "cipher hypothesis"**: The paper tested one cipher. It ruled out a class (position-blind generation). Say that.

3. **Drop or caveat lags 10-12**: The long-range MI claim doesn't survive scrutiny. Lead with lag-1 and the lag 2-7 crossover, which are solid.

4. **Report m=175 Bonferroni alongside m=30**: Show that the core findings survive either threshold. This inoculates against reviewer criticism.

5. **The convergent-failure argument is the paper's strongest contribution.** Two completely different mechanisms (homophonic cipher, local copy), both position-blind, fail on the same four metrics. This is publishable and novel. Frame the paper around this.

### Additional experiments before publication

1. **Timm parameter sweep**: Vary COPY_PROB from 0.3 to 0.95 and MODIFY_PROB from 0.1 to 0.8 in a grid. Show that no parameter combination simultaneously matches VMS self-succession AND identical-word rate AND positional enrichment. This closes the parameter sensitivity gap.

2. **Position-sensitive cipher simulation**: Design a cipher with LF/MID/LL substitution tables. Test whether it can reproduce -am LL and y-onset LF while maintaining other VMS statistics. This directly addresses the open "position-sensitive cipher" alternative. If it fails, the cipher space is more thoroughly explored. If it succeeds, the "grammar" verdict is actually a "cipher of a language with clause-boundary morphology" verdict, which is a much more interesting conclusion.

3. **Absent-cell paradigm test**: For stems with >= 5 suffix types, compute expected frequency of unattested stem-suffix combinations from marginals. Count how many high-expected-frequency cells (expected n > 3) are truly absent. This discriminates constructed/template from natural language: NL should show smooth filling; constructed/template should show categorical gaps.

4. **Naibbe on A-dialect metrics**: Either modify the Naibbe tables to target A-dialect vocabulary (if possible) or explicitly acknowledge the A-dialect gap as a limitation. The strongest positional findings (cth LF depletion at 0.159, d LL enrichment at 1.667) are A-dialect.

5. **Finer-grained position taxonomy in exp_174**: Replace the 5-category system (LF, second, MID, LL, only) with actual ordinal position (1, 2, 3, ..., n) within lines of fixed length (e.g., analyze 8-token lines separately, 9-token lines separately). This tests whether the "MID" category is hiding finer-grained positional effects that a more sophisticated template could capture.

---

## 6. SUMMARY SCORECARD

| Aspect | Assessment |
|--------|------------|
| Cipher verdict | **Agree** (for position-blind ciphers; position-sensitive untested) |
| Self-citation verdict | **Mostly agree** (parameter sensitivity gap; core logic is sound) |
| Template verdict | **Agree with reframing** (simple templates falsified; onset-aware templates = grammar by another name) |
| Structured grammar verdict | **Agree it's the default** (but never positively tested; subcategories undiscriminated) |
| Convergent failure argument | **Strong and novel** — the paper's best contribution |
| exp_170 methodology | Sound (Protocol A should be de-emphasized for positional metrics) |
| exp_171 methodology | Adequate (parameter sweep needed for strong claims) |
| exp_172 methodology | Lenient pass criterion; B-dialect LOSO rates (60-70%) underexamined |
| exp_173 methodology | m=30 vs m=175 scoping error (core findings survive either) |
| exp_174 methodology | Strongest experiment; minor concern about MID conflation |
| exp_175 methodology | Lag-1 and lag 2-7 findings sound; **lags 10-12 likely artifact — retract or caveat** |
| Synthesis honesty | Good on what it can't determine; understates simulation limitations |
| Publication readiness | 70% — needs parameter sweep, position-sensitive cipher test, MI correction |

---

*Review completed 2026-04-10 by Opus 4.6. This document annotates working_position.md; it does not replace it.*
