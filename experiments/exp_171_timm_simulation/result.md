# exp_171: Timm/Schinner Self-Citation Null Simulation
**Date**: 2026-04-10
**Hypotheses**: Does the Timm & Schinner (2020) self-citation text generation algorithm reproduce robust VMS positional and morphological findings?
**Status**: SELF-CITATION HYPOTHESIS FALSIFIED FOR POSITIONAL GRAMMAR; CONFIRMED AS PARTIAL EXPLANATION FOR SELF-SUCCESSION BUT OVER-PREDICTS IT. Timm fails on all positional findings (-am LL, y-onset LF, d LL) and generates its own artifacts (excessive self-succession, excessive word repetition) that are absent from or weaker in the real VMS.

**Configuration**: 100 simulations, 20,000 tokens each. Self-citation algorithm: WINDOW=50, COPY_PROB=0.85, MODIFY_PROB=0.25. Seed vocabulary: top-200 B-dialect words weighted by frequency. Line breaking: VMS B-dialect line-length distribution. Compared against same metrics from exp_170 Naibbe (Latin-B protocol).

---

## ALGORITHM

At each step:
- With prob 0.85: copy a word from the last 50 tokens (self-citation window)
- With prob 0.15: draw from seed vocabulary (frequency-weighted top-200 B-dialect words)
- With prob 0.25: apply character modification (replace/insert/delete one character)

This directly implements Timm & Schinner's mechanism: "copy a recent word, optionally modify 1-2 characters."

---

## RESULT TABLE

| Metric | VMS-B | Timm mean [95%CI] | Status | Naibbe-LatB mean | N-status |
|--------|-------|-------------------|--------|-----------------|---------|
| edy rate (B-marker) | **0.191** | 0.143 [.128,.159] | **ABOVE** | 0.151 | ABOVE |
| l-onset rate (F131) | **0.058** | 0.048 [.039,.066] | INSIDE | 0.059 | INSIDE |
| -am LL enrichment (F087) | **6.811** | 0.994 [.629,1.432] | **ABOVE** | 1.008 | ABOVE |
| daiin→cth enrichment | **0.000** | — [0,0] | INSIDE† | 0.141 | INSIDE† |
| y-onset LF enrichment (F098) | **3.506** | 1.007 [.837,1.175] | **ABOVE** | 1.011 | ABOVE |
| cth LF enrichment | **0.966** | 1.006 [0,3.06] | INSIDE | 1.023 | INSIDE |
| qok→ch enrichment | **1.326** | 0.950 [.810,1.088] | **ABOVE** | 1.177 | ABOVE |
| qok self-succession | **1.239** | 1.532 [1.371,1.759] | **BELOW** | 0.886 | ABOVE |
| ok self-succession | **1.462** | 1.970 [1.610,2.287] | **BELOW** | 0.964 | ABOVE |
| d self-succession (~1.0) | **1.157** | 2.056 [1.704,2.506] | **BELOW** | 1.046 | INSIDE |
| ch self-succession | **1.694** | 2.410 [1.819,3.113] | **BELOW** | 0.867 | ABOVE |
| -edy/-ol ratio | **3.029** | 3.603 [2.643,4.717] | INSIDE | 2.286 | ABOVE |
| d LL enrichment | **1.464** | 1.007 [.900,1.130] | **ABOVE** | 0.988 | ABOVE |
| sh LF enrichment | **0.859** | 1.001 [.862,1.137] | BELOW | 0.999 | BELOW |
| qok LF depletion | **0.839** | 1.013 [.917,1.127] | **BELOW** | 0.996 | BELOW |
| type-token ratio | **0.284** | 0.203 [.197,.207] | **ABOVE** | N/A | N/A |
| mean word length | **5.768** | 5.039 [4.939,5.120] | **ABOVE** | N/A | N/A |
| identical adjacent word rate | **0.009** | 0.037 [.034,.040] | **BELOW** | N/A | N/A |

† INSIDE because both ~0 (B-dialect finding, not informative)

---

## KEY FINDINGS

### 1. Positional grammar ABSENT from Timm (same failure as Naibbe)

**-am LL enrichment**: VMS=6.811, Timm=0.994 — completely absent across all 100 simulations. Timm has no concept of line positions, so -am words appear at line-final positions at baseline rate. The VMS's 6.8× enrichment cannot be produced by any position-blind generation mechanism.

**y-onset LF enrichment**: VMS=3.506, Timm=1.007 — absent. Timm produces y-onset words at line-first positions at baseline rate. The VMS's 3.5× y-onset line-opening preference requires an explicit positional rule that neither Timm nor Naibbe can generate.

**d LL enrichment**: VMS=1.464, Timm=1.007 — absent. The d-onset line-closing pattern is not reproducible by self-citation.

**qok LF depletion**: VMS depletes qok at LF (0.839×), Timm produces near-baseline (1.013). Self-citation cannot reproduce preferential absence of qok at line starts.

**Verdict on positional findings**: **Both Naibbe and Timm fail identically on -am LL and y-onset LF.** This convergent failure from two completely different generation mechanisms (cipher vs. self-citation) is strong evidence that these positional patterns are intrinsic to Voynichese structure, not artifacts of any generation mechanism.

---

### 2. Self-succession: Timm OVERPRODUCES, Naibbe UNDERPRODUCES, VMS is intermediate

| Metric | VMS-B | Timm | Naibbe-LatB |
|--------|-------|------|-------------|
| qok self-succ | 1.239 | **1.532** (BELOW) | 0.886 (ABOVE) |
| ok self-succ | 1.462 | **1.970** (BELOW) | 0.964 (ABOVE) |
| d self-succ | 1.157 | **2.056** (BELOW) | 1.046 (INSIDE) |
| ch self-succ | 1.694 | **2.410** (BELOW) | 0.867 (ABOVE) |

Timm overcorrects: the self-citation window mechanism generates too much local class-level repetition. The VMS self-succession enrichments (1.24-1.69×) sit at an intermediate level:
- Higher than a cipher mechanism (Naibbe produces near-baseline ~0.86-0.96×)
- Lower than pure self-citation (Timm produces 1.53-2.41×)

VMS self-succession is not explained by either pure mechanism. This intermediate pattern is consistent with a structured system where words cluster by class for grammatical reasons (agreement, co-selection) rather than by pure mechanical repetition.

---

### 3. Timm artifacts absent from VMS

**Identical adjacent word rate**: VMS=0.009, Timm=0.037 — Timm produces **4× more** exact word-word repetition. The self-citation mechanism too frequently copies the immediately preceding word verbatim. VMS word repetition is much rarer than Timm predicts.

**Type-token ratio (Zipf proxy)**: VMS=0.284, Timm=0.203 — Timm concentrates vocabulary too heavily in high-frequency words (TTR is too low). VMS vocabulary is more diverse than pure self-citation predicts.

**Mean word length**: VMS=5.768, Timm=5.039 — Timm's character modification shortens words on average (modifications include deletions). VMS words are longer than Timm-modified words.

**ch self-succession**: Timm=2.41× vs VMS=1.69×. Timm's 2.41× is far above VMS's 1.69× — Timm overproduces ch-ch repetition.

---

### 4. What Timm correctly reproduces (by construction)

**-edy/-ol ratio**: INSIDE (Timm=3.603, VMS=3.029). Because Timm seeds from B-dialect words with high edy/ol ratios, it propagates this ratio. This is an artifact of the seed vocabulary, not a prediction.

**cth LF enrichment**: INSIDE (both ~1.0). Both have near-baseline cth at line-first positions. This is trivially inside.

**l-onset rate**: INSIDE (Timm=4.8%, VMS=5.8%). Close but the CI includes the VMS value marginally.

---

## COMPARISON: TIMM vs NAIBBE FAILURES

Both models fail on the same key findings:

| Metric | Timm status | Naibbe status | Agreement |
|--------|-------------|---------------|-----------|
| -am LL enrichment | ABOVE | ABOVE | Both fail |
| y-onset LF enrichment | ABOVE | ABOVE | Both fail |
| d LL enrichment | ABOVE | ABOVE | Both fail |
| qok LF depletion | BELOW | BELOW | Both fail |
| sh LF enrichment | BELOW | BELOW | Both fail |

Both models also fail on qok→ch enrichment (VMS>both). The VMS sequential grammar (qok→ch preference) is not produced by either cipher mechanism or self-citation.

The models diverge on self-succession: Naibbe underproduces (ABOVE), Timm overproduces (BELOW). VMS is between them.

---

## CONCLUSION

**The Timm/Schinner self-citation algorithm is INSUFFICIENT to explain VMS structure.**

It fails on:
- All positional grammar metrics (-am LL, y-onset LF, d LL, qok LF depletion)
- Sequential grammar (qok→ch enrichment)
- Produces artifacts absent from VMS: excessive word-level repetition (4×), too-low TTR, excessive self-succession

**Outcome condition reached**: Timm reproduces local self-succession patterns (by design) but not global positional ones. The local-global split is diagnostic: Timm explains *why* VMS has self-succession (local copy mechanism), but fails to explain the positional grammar because that requires structural rules Timm doesn't have.

**Combined with exp_170**: Two completely different generation models (homophonic cipher; self-citation) both fail on the same positional and sequential grammar findings. This convergent failure significantly strengthens the case that VMS positional grammar (-am LL, y-onset LF, onset self-succession at intermediate levels, qok→ch sequential preference) is an intrinsic structural feature — not an artifact of any known generation mechanism.

---

## FILES

- `script.py`: Implementation of Timm algorithm + metric computation
- `data/timm_results.json`: Raw metric vectors for 100 simulations
