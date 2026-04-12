# Paper Raw Material — Voynich Cryptanalyst
**Date**: 2026-04-10
**Purpose**: Extracted numbers, methodology details, simulation designs, and references for methodology paper draft. Raw material only — not polished prose.

---

## Section 1: Ten Most Important Findings

### Finding 1: -am LL Enrichment (B-dialect)
**Hypothesis**: EVA words ending in the suffix -am are preferentially located at line-final (LL) positions in Currier B-dialect text.
**Experiment**: Characterization experiments (exp_070–080 range); candidate nomination exp_173 (F3).
**Effect size**: 6.811× (or 6.856× by direct recomputation). -am words constitute 13.5% of LL words vs 1.96% of all B-dialect words.
**Sample**: B-dialect corpus, 2,447 lines, 20,490 words. LL slot: 2,431 valid (multi-word lines). 327 -am words at LL.
**P-value**: p = 6.27 × 10⁻¹⁶¹ (one-sided binomial exact test; exp_173 F3). Survives Bonferroni correction at both m=30 (threshold p < 0.001667) and m=175 (threshold p < 0.000286).
**Cross-validation**: Passes random 80/20 holdout (B-dialect, exp_172). Passes all three B-dialect LOSO splits (leave-bio, leave-stars, leave-herbal).
**Null model comparison**: Naibbe cipher (400 sims): 1.008× [0.816, 1.196]. Timm self-citation (100 sims): 0.994× [0.629, 1.432]. Timm parameter sweep (1,500 sims, 75 combos): max 0.572×. Position-sensitive cipher (100 sims, strong calibration): 5.756× [5.458, 5.996] — see caveats in Finding 4.
**Theory**: Rules out all position-blind mechanisms. Requires explanation by position-sensitive encoding or intrinsic positional grammar rule. The -am LL specificity is contrasted with the depletion of the most common B suffix (-edy at 18.3% overall) at LL (0.346×), confirming suffix specificity rather than generic LL slot (exp_174, H3).

---

### Finding 2: y-Onset LF Enrichment (B-dialect)
**Hypothesis**: EVA words with y-initial onset are preferentially located at line-first (LF) positions in B-dialect text.
**Experiment**: Characterization experiments; candidate F6 (exp_173).
**Effect size**: 3.506×. y-onset words constitute 14.3% of LF words vs 4.08% of all B-dialect words.
**Sample**: 2,447 lines, 2,447 LF words. y-onset LF: 350 occurrences.
**P-value**: p = 2.86 × 10⁻⁹⁰ (binomial exact, exp_173 F6). Survives both Bonferroni thresholds.
**Cross-validation**: Passes random B-dialect 80/20 split (exp_172).
**Null model comparison**: Naibbe: 1.011× [0.835, 1.152]. Timm: 1.007× [0.837, 1.175]. Position-sensitive cipher strong: 2.395× [2.253, 2.580] (target-calibrated — see Finding 4). Timm sweep max: 0.526×.
**Theory**: The LF onset profile also shows s-onset enrichment (4.389×), t-onset enrichment (approx. 2×), and cth-onset strong depletion (0.29× in B), confirming a full LF onset grammar rather than just a y/non-y split (exp_174, H4). y-onset is the LF signature of both dialects (A: 2.459× at p = 8.38 × 10⁻⁴⁰).

---

### Finding 3: Onset Self-Succession Enrichment (both dialects)
**Hypothesis**: Onset-class words tend to follow same-onset-class words at rates above what frequency alone predicts.
**Experiments**: Self-succession characterization (exp_164); candidates F11–F16 (exp_173).
**Effect sizes**:
- ok self-succession A: 1.930×, p = 5.93 × 10⁻⁶
- ch self-succession A: 1.427×, p = 8.19 × 10⁻⁷
- qok self-succession A: 1.623×, p = 9.58 × 10⁻⁴ (survives m=30, not m=175)
- qo self-succession B: 2.047×, p = 4.05 × 10⁻⁶
- ch self-succession B: 1.694×, p = 5.88 × 10⁻⁷
- ok self-succession B: 1.462×, p = 2.03 × 10⁻⁴
- Mean across these six: approximately 1.697× (ranging 1.42–2.05×)
**Sample**: Depends on onset class; bigram counts across full-corpus adjacency pairs within lines.
**Cross-validation**: Core self-succession passes B-dialect random split (exp_172).
**Position control**: After controlling for line position (pi→pj transition stratum), self-succession enrichment persists at 1.2–1.8× (exp_174, H1). Position-controlled values: ok-A 1.822×, ch-A 1.334×, qok-A 1.594×, ch-B 1.503×, ok-B 1.362×. Position explains only a small fraction of the effect.
**Null model comparison**: Naibbe: depleted to 0.86–0.96× (all ABOVE VMS, meaning cipher underproduces). Timm: overproduces at 1.532–2.410×. Position-sensitive cipher (exp_177): ~1.00× (no enrichment at all). Hybrid (exp_179): best ss_mean 1.217× at cp=0.5, mp=0.3.
**Theory**: Self-succession is the metric that no tested mechanism reproduces at VMS levels. It is the #1 discriminating finding against all cipher classes. The intermediate VMS level (1.42–2.05×) sits between Naibbe's depletion and Timm's overproduction, ruling out both classes as sole mechanisms.

---

### Finding 4: Position-Sensitive Cipher Partial Reproduction (with target-awareness caveat)
**Hypothesis**: A polyalphabetic cipher with separate substitution tables for LF, MID, and LL positions can approach VMS -am LL enrichment.
**Experiment**: exp_177 (position-sensitive cipher); verified in exp_177_verify.
**Effect size achieved**: -am LL = 5.756× [5.458, 5.996] at strong calibration (90% probability for clause-final morpheme detection). y-onset LF = 2.395× [2.253, 2.580]. Self-succession: 0.999× (not reproduced).
**Verification**: Independent re-run with different random seed (exp_177_verify): -am LL = 5.759× [5.580, 6.016], delta = +0.003 from original. Reproducible.
**Sample**: 100 simulations × 2,447 lines × 3 calibration levels. Latin source: Cicero De Officiis, 3,030 pseudo-sentences, 34,977 words.
**CRITICAL CAVEAT**: The LL substitution table was target-aware. ALL Latin clause-final morphemes (-um, -us, -em, -is, -ae, -orum, -bus, -unt, -it, -ant, -at, -am) were mapped to EVA -am specifically, not to corresponding EVA suffix classes. Source comment explicitly labels -am as "the target LL suffix." The onset weights at LL positions were also calibrated to VMS LL onset distributions. This result demonstrates that a maximally-calibrated position-sensitive cipher approaches VMS -am LL; it does not demonstrate that an unmotivated cipher applied to Latin would do so.
**Theory**: Position-sensitivity is a necessary condition for approaching the VMS positional grammar. The jump from position-blind (~1×) to position-sensitive (3.1–5.8×) is the largest single step in the hierarchy of tested mechanisms. The residual gap to VMS (5.756 vs 6.811) and the complete failure on self-succession (0.999×) means position-sensitive substitution alone is insufficient.

---

### Finding 5: Timm Self-Citation — Dual Constraint Failure (parameter sweep)
**Hypothesis**: No parameter combination of the Timm/Schinner self-citation algorithm can simultaneously reproduce VMS self-succession and VMS exact-word-repetition rate.
**Experiment**: exp_176 (parameter sweep); exp_171 (original simulation).
**Effect sizes**: Timm at published defaults (COPY_PROB=0.85, MODIFY_PROB=0.25, WINDOW=50): self-succession 1.532–2.410× (overproduces vs VMS 1.239–1.694×); identical adjacent word rate 0.037 (vs VMS 0.009, 4× excess); -am LL 0.994× (fails completely).
**Parameter sweep**: 75 combinations (COPY_PROB ∈ {0.3, 0.5, 0.7, 0.85, 0.95} × MODIFY_PROB ∈ {0.1, 0.25, 0.4, 0.6, 0.8} × WINDOW ∈ {10, 30, 50}). 20 simulations per combination, 1,500 total simulations. Results: 0/75 combinations produce -am LL enrichment above 0.572× (VMS: 6.811×). 8/75 combinations meet viability criteria on adj_rate + ss_mean simultaneously, but those 8 are the combinations that perform worst on positional metrics.
**The trade-off**: Lower COPY_PROB → lower adj_rate (fewer exact repeats) BUT lower ss_mean (weaker self-succession). Mean ss_mean at COPY_PROB=0.3: 1.220×; at COPY_PROB=0.95: 6.760×. No parameter setting jointly satisfies VMS-level self-succession AND VMS-level adj_rate AND VMS positional grammar.
**Theory**: Rules out self-citation as the sole generation mechanism. The positional grammar failure is inherent to any position-blind mechanism. The adj_rate/ss_mean paradox is structural in the parameter space, not a tuning artifact.

---

### Finding 6: Hybrid Cipher-Copy Dual Constraint Unsatisfiable
**Hypothesis**: Combining position-sensitive cipher (strong calibration) with Timm-style local copying can simultaneously satisfy -am LL ≥ 5.0×, ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015.
**Experiment**: exp_179.
**Result**: 0/16 parameter combinations satisfy all three constraints. Best combination (cp=0.2, mp=0.3): am_ll=4.804, ss_mean=1.075, adj_rate=0.0113. Falls below both am_ll (threshold 5.0) and ss_mean (threshold 1.2) thresholds simultaneously.
**Sample**: 16 combinations (COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6}), 50 simulations each, 800 total runs. Copy buffer: WINDOW=20.
**Structural explanation**: Each 0.1 increase in COPY_PROB produces approximately +0.036 in ss_mean but −0.47 in am_ll. The copy buffer contains predominantly MID-position words; copying at LL positions introduces non-am-suffix words, diluting the LL cipher output proportionally. The linear trade-off means no COPY_PROB value satisfies both constraints simultaneously.
**Theory**: Closes the hybrid mechanism gap identified after Phase 3. The remaining viable mechanism after this elimination sequence is intrinsic structured grammar (or a position-aware hybrid that restricts copying to non-LL positions — which is functionally equivalent to a grammar rule).

---

### Finding 7: qok→ch Bigram Enrichment Survives Position Control
**Hypothesis**: qok-onset words are followed by ch-onset words at above-baseline rates in both dialects, and this preference survives after controlling for line position.
**Experiment**: exp_174 (H2); candidate F9 (exp_173).
**Effect sizes**: B-dialect: 1.211× unconditional (p = 9.15 × 10⁻⁷, F9), 1.248× position-controlled. A-dialect: 1.326× unconditional, 1.242× position-controlled.
**Position-stratum detail**: qok→ch enrichment in B is concentrated in mid-line positions (MID→MID: 1.291×; MID→LL: 1.226×) and absent at LF→second (0.734×) and second→MID (0.740×). This indicates a mid-line sequential grammar rule, not a positional artifact.
**Theory**: Rules out pure template explanation. Demonstrates that sequential grammar rules are position-heterogeneous — they operate within specific position transitions, not uniformly.

---

### Finding 8: -am LL Enrichment Is Suffix-Specific (Template Falsification)
**Hypothesis**: The -am LL enrichment is suffix-specific rather than a generic LL slot effect.
**Experiment**: exp_174 (H3).
**Effect sizes**: B-dialect LL suffix enrichments: -am 6.856×, -al 0.913×, -aiin 0.386×, -ar 0.476×, -edy 0.346×, -ol 0.593×, -or 0.573×. The most common B-dialect suffix (-edy, 18.3% of all words) is 0.65× DEPLETED at LL.
**Sample**: 2,431 LL words in B-dialect corpus. Counts: -am 327 at LL vs 401 total in corpus; -edy 154 at LL vs 3,752 total.
**Theory**: Pure template models predict near-uniform or vocabulary-proportional LL distribution. The exclusive specificity of -am (6.9×) combined with depletion of the overall most-common suffix (-edy at 0.35×) cannot be explained by a generic slot. The template must have onset-class-aware rules, which is functionally equivalent to grammar.

---

### Finding 9: Within-Line MI Structure Inconsistent with Self-Citation (Robust Lags)
**Hypothesis**: VMS within-line mutual information at lags 1 and 2–7 follows a profile inconsistent with Timm self-citation.
**Experiment**: exp_175 (lags 1 and 2–7 only; lags 10–12 retracted).
**Effect sizes**: Lag 1: VMS-B MI = 0.0850 vs Timm mean = 0.0633 [0.0499, 0.0748]; VMS is ABOVE. Lags 2–7: VMS-B MI = 0.0487–0.0642 vs Timm means = 0.0648–0.0966; VMS is BELOW (below Timm CI) at all six lags.
**Shuffle validation**: Within-line shuffle destroys 63% of lag-1 MI (VMS/shuffled = 2.705), confirming lag-1 structure is genuinely sequential. At lags 2–7, VMS/shuffled ≈ 1.0–1.4, consistent with line-length and position-frequency artifacts rather than structure.
**RETRACTED finding**: Lags 10–12 were originally claimed as ABOVE Timm and cited as long-range structure. The within-line shuffle comparison shows VMS/Within = 0.825 and 0.873 at lags 11–12 (shuffle > real VMS), ruling out genuine structure. Retracted after Phase 2 Opus review.
**Theory**: Any copy-window mechanism must elevate MI within the window at all accessible lags. VMS MI is below Timm's CI at lags 2–7 — the opposite of what self-citation predicts. This is structural evidence against self-citation, not parametric.

---

### Finding 10: Dialect Composition Findings (A/B split is real and robust)
**Hypothesis**: Currier A and B dialects differ systematically in vocabulary, suffix preference, and positional grammar.
**Experiments**: exp_005, exp_023, exp_040, exp_047 (characterization); candidates F17–F19, F23, F24, F28 (exp_173).
**Key effect sizes**:
- edy rate B vs A: B 19.1%, A 4.3%, ratio 59.4× difference; p ≈ 0 (exp_173 F17)
- cth-onset rate A vs B: A 14.9× higher; p = 4.24 × 10⁻¹²⁸ (F18)
- qok-onset rate B vs A: B 2.343× higher; p = 2.07 × 10⁻⁹¹ (F19)
- -ol rate A vs B: A 2.172× higher; p = 4.79 × 10⁻⁹⁸ (F23)
- -or rate A vs B: A 2.995× higher; p = 8.63 × 10⁻¹¹⁸ (F24)
- l-onset rate B vs A: B 9.837× higher; p = 3.47 × 10⁻¹³⁸ (F28)
- Vocabulary Jaccard overlap: 0.148 (59 A, 117 B exclusive stem forms in productive paradigm)
**Dialect assignment**: Folio-level edy rate ≥ 5% with minimum 10 words → B-dialect. Resulting: 40 folios B (2,447 lines, 20,490 words), 59 folios A (1,671 lines, 10,258 words). Total assigned corpus: 4,118 lines, 30,748 words.
**Theory**: Dialects share the same productive stems but select opposite suffix paradigms (A: -ol/-or dominant; B: -edy/-ain dominant). The structured grammar operates in both dialects, with dialect-specific positional grammar signatures (e.g., -am LL enrichment: B 6.811×, A 3.562×; y-onset LF enrichment: B 3.506×, A 2.459×).

---

## Section 2: Methodology Description

### Corpus

The primary corpus is the EVA ZL3b IVTFF transliteration of Beinecke MS 408, downloaded from Voynich.nu. Words are dot-separated within lines; each line is prefixed by a locus string in the format `<fN.lineN,@Ptype>` where fN is the folio identifier, lineN is the physical line number, and Ptype indicates paragraph structure (P0 = paragraph start, P1 = continuation, etc.). All experiments filter to locus types beginning with 'P' and parse words by splitting on '.' and filtering to lowercase EVA character sequences. Words beginning with `<` (transliteration uncertainty markers) are excluded. Total corpus: approximately 33,622 words across 4,795 lines (somewhat dependent on parser implementation; approximately 30,748 words across 4,118 lines after excluding folios with insufficient word counts for dialect assignment).

Dialect assignment is performed at the folio level: the edy-suffix rate (fraction of words containing 'edy' or 'eedy') is computed for each folio, and folios with edy-rate ≥ 5% and at least 10 words are assigned to Currier B; others are assigned to Currier A. This threshold follows Currier (1976) and produces consistent dialect assignments that align with both scribal-hand analyses and prior computational work.

### Agent Loop Architecture

The primary research agent (Sonnet 4.6) operates in a hypothesis-generate–experiment–synthesize loop. In the characterization phase, hypotheses are generated from prior literature and from patterns observed in prior experiments. In the discrimination phase, hypotheses are generated from theory commitments (what does each theory predict?) and from gaps identified in the synthesis document. Each hypothesis is assigned an ID and tracked in `state/hypothesis_backlog.md`. Each experiment gets a numbered directory with a Python script, a result file, and a data subdirectory. The experiment script is self-contained: it loads the corpus, computes metrics, saves results, and prints a summary. The agent writes the result file after reviewing script output.

The meta-review process runs independently after each phase boundary: an Opus 4.6 instance reads the synthesis document (`state/working_position.md`) and the experiment result files without access to the primary agent's intermediate reasoning, and produces a structured review identifying overstatements, missing controls, and logical gaps. The primary agent then addresses each critique in a methodological consolidation phase before the next research phase begins.

All code and results are committed to git after each experiment or small batch of experiments. The git history serves as the reproducibility record: each commit message references the experiment ID, and the result files record the parameters, sample sizes, and random seeds used.

### Characterization Phase Methods

Metrics computed in the characterization phase include: onset-class frequency distributions (initial EVA character sequences classified into approximately 20 onset classes: qok, qot, qo, cth, ch, sh, ok, ot, ol, d, s, y, k, t, l, r, p, f, other); suffix frequency distributions (final EVA character sequences); positional enrichment ratios (rate of a class at position X divided by its overall rate, where positions are LF/second/MID/LL/only); self-succession ratios (rate of class-to-class transition in adjacency vs expected under independence); bigram enrichment (observed transition rate divided by expected under marginal independence); type-token ratio; mean word length; and mutual information at within-line lags.

Onset-class positional enrichment is computed as: (count of class at position X / total words at position X) / (count of class in full corpus / total words in corpus). Position assignment: i=0 is LF; i=n-1 is LL; i=1 and n>2 is 'second'; i=n-1 and i>1 and n>2 is LL (n=1 is 'only'). Self-succession enrichment is: (observed count of bigram XX / total bigrams starting with X) / (overall rate of X), i.e., the observed conditional probability normalized by the marginal probability.

### Null Hypothesis Testing (Simulation-Based)

For each null model (Naibbe, Timm), the procedure is: (1) generate a synthetic corpus of similar size to the VMS (approximately 20,000 tokens for Timm; approximately TARGET_LINES=2,447 lines for Naibbe and position-sensitive cipher); (2) compute the same metrics on the synthetic corpus; (3) repeat 50–100 times with different random seeds; (4) report mean and 95% confidence interval (2.5th–97.5th percentile of the simulation distribution); (5) classify each VMS metric as ABOVE (VMS > upper CI), BELOW (VMS < lower CI), or INSIDE (VMS within CI).

Simulation confidence intervals are empirical percentiles from the simulation distribution, not normal approximations. Line lengths for simulation corpora are drawn from the VMS B-dialect line-length distribution (mean 8.4 tokens, std 3.0, approximately Gaussian, clipped to [2, 20]).

### Multiple Testing Correction

30 candidate findings were nominated post-hoc from the 175 quantitative findings produced in the characterization phase. Two Bonferroni thresholds are reported for transparency:
- m=30 (threshold: p < 0.001667): corrects for the 30 nominated candidates. Appropriate if nominees were pre-specified.
- m=175 (threshold: p < 0.000286): corrects for the full 175-finding search space. Conservative; assumes any finding could have been nominated.
BH-FDR (Benjamini-Hochberg) at q=0.05 is also reported as a secondary correction.

Test types: one-sided binomial exact test for positional enrichment (in the direction of the claim), one-sided Fisher exact test for bigram enrichment. P-values computed in Python using scipy.stats.

### Cross-Validation

Two cross-validation strategies were used (exp_172):
1. Random 80/20 train/test split, stratified by dialect. PASS criterion: test metric magnitude ≥ 50% of train magnitude AND same direction.
2. Leave-one-section-out (LOSO): for each VMS section (herbal/pharma/cosmo for A; bio/stars/herbal for B), the section is used as the test set and the remainder as train.

PASS criterion is deliberately lenient (50% magnitude) to identify genuine collapses rather than sampling noise. The cosmo LOSO failure (10/19) is attributed to sample size (n=32 test lines) rather than finding collapse, consistent with the random split passing at 18/19 for A-dialect.

---

## Section 3: Simulation Designs

### Naibbe Cipher (exp_170)

**Mechanism**: A homophonic substitution cipher in which each plaintext letter maps probabilistically to one of several EVA glyph sequences, based on a 78-card Italian tarocchi deck. The cipher tables were designed by Greshko (2025) to produce EVA output with Currier B statistical properties: high edy-suffix rate, qok/ch onset proportions, l-onset rate. The cipher is position-blind: the EVA output for a plaintext word does not depend on that word's position within the physical line.

**Parameters**: UNAMBIGUOUS=True (deterministic card assignments), RESPACING=17 (respacing interval). Implemented as `naibbe_v2.py` (from Greshko 2025 GitHub repository).

**Plaintext corpora**: Italian (Dante, Divina Commedia) and Latin (Vulgate Bible). Both corpora were processed to produce word sequences.

**Line-breaking protocols**: Protocol A (sentence-based): one sentence = one simulated line. Protocol B (VMS-length-matched): lines broken to match VMS B-dialect line-length distribution.

**Simulation count**: 100 simulations × 2 plaintext sources (Italian, Latin) × 2 protocols = 400 total runs. Each run: approximately 20,000 tokens.

**Metrics computed**: 16 metrics covering vocabulary composition, positional grammar, sequential grammar, and self-succession (see exp_170/result.md for full table).

**Key limitation**: The paragraph-start metric (F101, gallows-at-para-start enrichment) could not be tested because the VMS B-dialect locus parsing assigned 2,307 of 2,447 B-dialect lines as paragraph starters (P0 type), making the metric equivalent to LF enrichment rather than true paragraph-start enrichment. This metric remains untested against Naibbe.

### Timm/Schinner Self-Citation (exp_171 + exp_176)

**Mechanism**: At each token position, with probability COPY_PROB, copy a word uniformly at random from the preceding WINDOW tokens; with probability (1 - COPY_PROB), draw from a frequency-weighted seed vocabulary. With probability MODIFY_PROB applied to copied words, replace one random character (substitution, insertion, or deletion). This directly implements the Timm & Schinner (2020) algorithm.

**Original simulation (exp_171)**: WINDOW=50, COPY_PROB=0.85, MODIFY_PROB=0.25. Seed vocabulary: top-200 B-dialect words by frequency. 100 simulations × 20,000 tokens each.

**Parameter sweep (exp_176)**: COPY_PROB ∈ {0.3, 0.5, 0.7, 0.85, 0.95} × MODIFY_PROB ∈ {0.1, 0.25, 0.4, 0.6, 0.8} × WINDOW ∈ {10, 30, 50} = 75 combinations. 20 simulations per combination, 1,500 total simulations. Each simulation: 20,000 tokens, broken into lines using VMS B-dialect line-length distribution. Seed vocabulary: same top-200 B-dialect words. Viability criteria: identical adjacent word rate ≤ 0.0135 AND mean self-succession ≥ 1.1.

**Results summary**: 8/75 combinations meet viability criteria on adj_rate + ss_mean. 0/75 approach positional metrics (max -am LL = 0.572×, max y-onset LF = 0.526×). The 8 viable combinations perform worst on positional metrics. Positional grammar failure is parameter-robust.

### Position-Sensitive Cipher (exp_177 + exp_177_verify)

**Mechanism**: Three substitution tables, one per line position class (LF, MID, LL). For each word, the applicable table is used based on whether the word is first, last, or intermediate in its line.

**LF table**: The Latin word is pattern-matched against clause-initial regex patterns: qu-/no-/et-/at- words (Latin conjunctions and particles) → y-onset EVA word; t+vowel-initial → t-onset; s+vowel-initial → s-onset. With probability p (calibration strength), the matched pattern is applied; otherwise, a random EVA word is drawn. Calibration strengths: strong p=0.90, moderate p=0.60, weak p=0.30.

**LL table (TARGET-AWARE)**: The Latin word is matched against LATIN_CLAUSE_FINAL regex: `(am|um|us|em|is|ae|orum|bus|unt|it|ant|at)$`. If matched, with probability p (strong=0.90, moderate=0.50, weak=0.20), generate an EVA word with suffix -am and onset drawn from a VMS-calibrated LL distribution: d=0.40, ok=0.15, qok=0.15, ch=0.10, other=0.20. **The mapping of all 12+ Latin clause-final morpheme classes to a single EVA suffix (-am) is target-aware: the -am suffix was chosen because it is the VMS target metric. A linguistically neutral mapping would use different EVA suffix classes for different Latin morphemes.** The LL onset weights are also calibrated to VMS LL onset distributions.

**MID table**: Uniform random EVA word from the B-dialect onset/suffix frequency distributions.

**Latin source**: Cicero De Officiis (bilingual Latin-English edition). Latin text extracted using English stopword density: paragraphs with < 8% English stopwords are treated as Latin. Result: 3,030 pseudo-sentences, 34,977 Latin words.

**Line construction**: Latin words are shuffled within the extracted set, then assigned to lines with lengths drawn from the VMS B-dialect line-length distribution.

**Simulation count**: 100 simulations per calibration level × 3 levels = 300 total runs. TARGET_LINES=2,447. Verified in independent run (exp_177_verify, n=100, seed base 999999): am_ll=5.759± [5.580, 6.016], delta from original +0.003.

### Hybrid Cipher-Copy (exp_179)

**Mechanism**: At each word position, with probability COPY_PROB, copy a word from a deque buffer of the preceding WINDOW=20 words; with probability MODIFY_PROB applied to copied words, replace the copied word's onset class with a random onset. With probability (1 - COPY_PROB), apply the position-sensitive cipher (strong calibration, same as exp_177).

**The copy buffer is position-blind**: any recent word can be copied to any current position (LF, MID, or LL). This means copying at LL positions introduces non-am-suffix words from the buffer, diluting the cipher's LL specialization.

**Parameter grid**: COPY_PROB ∈ {0.2, 0.3, 0.4, 0.5} × MODIFY_PROB ∈ {0.3, 0.4, 0.5, 0.6} = 16 combinations. 50 simulations per combination, 800 total runs. TARGET_LINES=2,447.

**Viability criteria**: -am LL enrichment ≥ 5.0× AND ss_mean ∈ [1.2, 1.7] AND identical adjacent word rate ≤ 0.015. These thresholds require jointly approximate VMS levels on both the primary positional metric and the primary sequential metric.

**Untested architecture**: The tested hybrid uses position-blind copying (any position can be copied to any position). A position-aware hybrid that restricts copying to MID positions while applying the cipher exclusively at LF and LL has not been tested. Such a mechanism would decouple am_ll (protected by cipher-only LL generation) from ss_mean (driven by MID copies). Whether this architecture satisfies the dual constraint is an open question.

---

## Section 4: Evidence Tally by Theory

### Theory 1: Position-Blind Cipher Hypothesis (Naibbe formulation)

**Supporting evidence (cipher design)**: Vocabulary composition metrics (edy rate, l-onset rate, qok rate) are within Naibbe CI in 4–6 of 16 condition×metric combinations. These were designed-in targets; they do not independently support the cipher.

**Refuting evidence**:
- -am LL enrichment (F3): VMS 6.811× vs Naibbe ≈1.008×. ABOVE in all 4 conditions (400 simulations). p = 6.27 × 10⁻¹⁶¹.
- y-onset LF enrichment (F6): VMS 3.506× vs Naibbe ≈1.011×. ABOVE in all 4 conditions.
- d LL enrichment (F5): VMS 1.464× vs Naibbe ≈0.988×. ABOVE in all conditions.
- qok LF depletion (F29): VMS 0.839× vs Naibbe ≈0.996×. BELOW in 3/4 conditions (cipher produces near-baseline; VMS depletes). Cipher artifact absent from VMS.
- Onset self-succession (F11–F16): All six self-succession findings have VMS ABOVE the Naibbe CI. Naibbe produces depleted self-succession (0.86–0.96×) while VMS shows enrichment (1.24–1.93×).
- qok→ch enrichment (F9): VMS 1.211× vs Naibbe 1.177–1.196×. ABOVE in all 4 conditions.
- Timm parameter sweep extends falsification: 0/75 parameter combinations of ANY position-blind mechanism approach positional grammar metrics.
- A-dialect extension (exp_178): 7/8 A-dialect positional metrics ABOVE in all 4 Naibbe conditions.

**Overall tally (exp_170)**: 14/16 metrics outside Naibbe CI (informative INSIDE count: 1–2, both trivial). The position-blind cipher hypothesis is ruled out for the tested mechanism and generalized by the parameter-robustness of the positional grammar failure.

**Open gap**: Position-sensitive ciphers remain partially viable. The Naibbe falsification is specific to position-blind mechanisms.

---

### Theory 2: Self-Citation Hypothesis (Timm/Schinner formulation)

**Supporting evidence**: Self-succession exists in VMS (1.24–2.05×) and Timm qualitatively produces it. This is the only class of metric where Timm is closer to VMS than Naibbe.

**Refuting evidence**:
- -am LL enrichment: VMS 6.811× vs Timm 0.994×. ABOVE (fails identically to Naibbe; position-blind).
- y-onset LF enrichment: VMS 3.506× vs Timm 1.007×. ABOVE.
- d LL enrichment: VMS 1.464× vs Timm 1.007×. ABOVE.
- qok LF depletion: VMS 0.839× vs Timm 1.013×. BELOW (wrong direction).
- Self-succession OVERPRODUCTION: Timm 1.532–2.410× vs VMS 1.239–1.694×. BELOW (Timm overproduces by 1.4–2×).
- Identical adjacent word rate: VMS 0.009 vs Timm 0.037. BELOW (4× excess in Timm).
- Parameter sweep (exp_176): 0/75 combinations resolve the positional grammar failure. 8/75 approach adj_rate + ss_mean viability but are the combinations that perform worst on positional grammar.
- MI profile (exp_175): VMS-B MI at lags 2–7 is BELOW Timm CI. Any copy-window mechanism must elevate MI within the window; VMS shows the opposite pattern at lags 2–7.
- qok→ch enrichment: VMS 1.326× vs Timm 0.950×. ABOVE (Timm underproduces sequential preference).

**Overall**: Self-citation cannot simultaneously produce the right self-succession level AND the right adj_rate at any parameter setting. Positional grammar is absent from all 75 tested parameter combinations. The MI profile at lags 2–7 is structurally inconsistent with any copy-window mechanism.

---

### Theory 3: Simple Template Hypothesis (Stolfi slot-grammar formulation)

**Supporting evidence**: The word-level entropy profile (U-shaped: low onset entropy, high interior, low final) is consistent with template structure. The productive suffix paradigm is consistent with slot-based word construction.

**Refuting evidence**:
- -am LL specificity (exp_174, H3): -am 6.856× at LL while -edy (most common suffix) is 0.346× depleted. A generic LL slot would not produce this. The contrast is cross-dialectal (A-dialect: -am 3.619× at LL, -ol 0.244× depleted).
- y-onset LF specificity (exp_174, H4): s-onset 4.389×, y-onset 3.506× enriched at LF; ch 0.29×, ch_e 0.32× depleted at LF. A generic LF slot would not produce onset-class specificity.
- Self-succession survives position control (exp_174, H1): position-controlled self-succession = 1.203–1.990× across six onset×dialect classes, nearly identical to unconditional values. Template model predicts position control eliminates onset-class effects.
- qok→ch enrichment survives position control (exp_174, H2): 1.242–1.248×, essentially unchanged.
- d self-succession position heterogeneity (exp_174): d self-succession varies 9× across position transitions (LF→second: 0.021; MID→LL: 0.180). Template predicts uniform effect; grammar predicts position-heterogeneous rules.

**Overall**: Pure template generation (position-independent slot-filler) is insufficient. The template must be onset-class-aware and position-heterogeneous, which is functionally equivalent to a grammar.

---

### Theory 4: Structured Grammar / Dual Constraint

**Supporting evidence** (surviving all elimination tests):
- -am LL enrichment (B: 6.811×, A: 3.562×): Bonferroni-corrected (both m=30 and m=175), cross-validated, not reproduced by any position-blind mechanism, partially reproduced only by target-calibrated position-sensitive cipher.
- y-onset LF enrichment (B: 3.506×, A: 2.459×): same status.
- d LL enrichment (A: 1.667×): survives both Bonferroni thresholds.
- Onset self-succession (1.24–2.05× across 6 class×dialect combinations): survives Bonferroni m=175 for most; survives position control; no tested mechanism reproduces at VMS levels.
- qok→ch enrichment (A: 1.326×, B: 1.211×): survives Bonferroni m=175; survives position control; mid-line grammar rule.
- Full LF onset grammar: s-onset 4.389×, y-onset 3.506× enriched; cth-onset 0.29× depleted — structured system, not noise.
- Two-dialect grammar: A and B share stems but select opposite suffix paradigms; each dialect has its own positional grammar signature.
- Internal coherence: -am words at LL + d self-succession concentrated at MID→LL + qok→ch concentrated at mid-line transitions form a mutually consistent positional grammar system (exp_174).

**The dual constraint** (Section 9 of working_position.md): Positional grammar (Property 1) and sequential word-class memory (Property 2) are both robustly established and jointly require a generation mechanism that is both position-aware and sequentially structured. No tested mechanism satisfies both constraints simultaneously.

**Remaining openness**: (a) The "structured grammar" verdict is a characterization of the writing system's statistical structure, not a claim about its origin or content. (b) Position-sensitive ciphers with appropriate sequential mechanisms have not been fully eliminated (the exp_179 hybrid used position-blind copying; position-aware copying was not tested). (c) The verdict is conditioned on the tested hypothesis set; other mechanism classes remain untested.

---

## Section 5: References to Prior Work

### Sources from Librarian KB

**currier_languages_1976** (Currier, 1976) — 22 cites in KB, depth 0.
"Some Important New Statistical Findings." The foundational Currier A/B dialect identification. The dialect assignment method used throughout this project (edy-rate threshold) is derived from Currier's language distinction. Direct methodological dependency: the entire two-dialect framework of the Cryptanalyst phase follows Currier.

**dimperio_elegant_enigma_1978** (D'Imperio, 1978) — 12 cites in KB, depth 1.
"The Voynich Manuscript — An Elegant Enigma." The field's foundational reference monograph. Provides the comprehensive survey of prior cipher hypotheses and statistical observations that the Cryptanalyst phase used to situate its findings. The 175 characterization experiments partially re-derived results catalogued by D'Imperio.

**stolfi_word_grammar_2000** (Stolfi, 2000) — 1 cite in KB, depth varies.
"A Grammar for Voynichese Words." Stolfi's slot grammar (crust-core-crust word structure, gallows at position 1, etc.) is the explicit target of the template-generation hypothesis in exp_174. The entropy profile findings in the characterization phase (U-shaped positional entropy) confirmed Stolfi's slot structure predictions. The slot-grammar residual analysis (exp_174) tests whether Stolfi's template can explain the onset-class findings.

**timm_schinner_selfcitation** (Timm & Schinner, 2020) — 3 cites in KB, depth 0.
"A possible generating algorithm of the Voynich manuscript." Direct source of the Timm algorithm implementation (COPY_PROB, MODIFY_PROB, WINDOW parameters; copy-window mechanism). Experiments exp_171 and exp_176 directly test this algorithm. The Timm algorithm description in the KB archives was used to verify the implementation.

**greshko_naibbe_2025** (Greshko, 2025) — 0 cites from other sources, depth 0.
"The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext." The primary source for the Naibbe cipher mechanism and implementation (`naibbe_v2.py`). Experiment exp_170 directly implements and tests this cipher. The paper's calibration targets (edy rate, l-onset rate) define the cipher's designed-in vocabulary metrics.

**bowern_lindemann_stats** (Bowern & Lindemann, 2021) — 3 cites in KB, depth 0.
"The Linguistics of the Voynich Manuscript." Provides a rigorous statistical overview of VMS properties including entropy, type-token ratio, and Zipfian structure. Cited in the characterization phase to contextualize entropy findings. The Bowern & Lindemann work is the closest methodological predecessor to this project.

**davis_scribes_2020** (Davis, 2020) — 9 cites in KB, depth 0.
"Scribe identification in the Voynich Manuscript." The scribal hands analysis (5 scribes identified). Relevant to dialect assignment: the question of whether Currier A/B reflects two scribes or two encodings is contextualized by Davis's scribe identification. The Cryptanalyst does not attempt scribe-level analysis; Davis is referenced as context for the dialect findings.

**montemurro_zanette_semantic_2013** (Montemurro & Zanette, 2013) — 8 cites in KB, depth 0.
"Keywords and Co-Occurrence Patterns in the Voynich Manuscript." The MI and semantic network analysis. The MI methodology in exp_175 is methodologically adjacent to Montemurro & Zanette's work (though they use a different MI formulation). Their finding of non-random word co-occurrence patterns is background context for the sequential grammar findings.

**schinner_hoax_2007** (Schinner, 2007) — 4 cites in KB.
"The Voynich Manuscript: Evidence of the Hoax Hypothesis." The hoax/random-text hypothesis. Directly relevant to the self-citation tests: Timm & Schinner (2020) is an extension of the Schinner hoax framework. Exp_171/176 test the self-citation mechanism that Schinner and Timm propose.

**zandbergen_eva_transcription** (Zandbergen, 2023) — 4 cites in KB.
The EVA transliteration standard documentation at Voynich.nu. The ZL3b IVTFF transcription used throughout the project is derived from this resource. The dot-separated word format and locus conventions are defined here.

**zattera_slot_grammar_2022** (Zattera, 2022) — 1 cite in KB, depth 0.
"A New Transliteration Alphabet Brings New Evidence of Word Structure and Multiple Languages in the Voynich Manuscript." A more recent slot grammar proposal with 12 slots. Contextualizes the template hypothesis testing in exp_174.

**stolte_radiocarbon_2011** (Stolte et al., 2011) — 5 cites in KB.
The radiocarbon dating study establishing the vellum date as 1404–1438 CE. Background context for all analyses — establishes the manuscript's physical period.

---

## Section 6: Figures and Tables the Paper Would Need

### Figure 1: Mechanism Comparison — -am LL Enrichment
A horizontal bar chart or dot plot showing -am LL enrichment across all tested mechanisms: Naibbe (all 4 conditions), Timm at published defaults, Timm parameter range (best of 75), position-sensitive cipher (weak/moderate/strong), hybrid cipher-copy (best of 16), and VMS B-dialect. Include 95% CI bars for simulation means. The vertical dotted line at VMS 6.811 should be visually prominent. This is the paper's hero figure.

### Figure 2: The Dual Constraint — Two-Dimensional Scatter Plot
X-axis: -am LL enrichment. Y-axis: ss_mean self-succession. One point per tested mechanism/parameterization (or one point per simulation, but overlapping would be dense). Show: Naibbe cluster (low am_ll, low ss_mean), Timm cluster by COPY_PROB level (low am_ll, varies in ss_mean), position-sensitive cipher (high am_ll, low ss_mean), hybrid cipher-copy (16 parameter combos as a curve), and VMS target point. The VMS point should be visually isolated from all tested mechanisms — this is the "no mechanism reaches this region" visualization.

### Figure 3: Timm Parameter Space Heatmaps
Two heatmaps, one for -am LL enrichment and one for ss_mean, with COPY_PROB on one axis and MODIFY_PROB on the other (collapsed across WINDOW, or shown for best WINDOW). Show: VMS target line (horizontal) and the "viable zone" region (where adj_rate ≤ 0.0135 AND ss_mean ≥ 1.1). Illustrate visually that the viable zone and the region approaching VMS ss_mean are mutually exclusive from the region approaching VMS am_ll.

### Figure 4: Hybrid Cipher-Copy Trade-off
X-axis: COPY_PROB. Y-axis: either am_ll or ss_mean (overlay both with secondary y-axis). Show how am_ll decreases and ss_mean increases as COPY_PROB increases. Add horizontal lines at VMS targets and at viability thresholds. The crossing point (where the two curves are equidistant from their respective thresholds) illustrates why no COPY_PROB satisfies both simultaneously.

### Figure 5: LF Onset Grammar — Enrichment Profile
Grouped bar chart showing LF onset enrichment for all major onset classes (qok, qo, cth, ch, sh, ok, d, s, y, k, t, l, other) for both A and B dialects. Shows the full LF grammar: y/s/t enriched, cth/ch depleted, qok depleted. This supports the "onset-class grammar" claim more completely than just reporting the y-onset finding.

### Figure 6: LL Suffix Specificity
Bar chart showing LL suffix enrichment for the top suffix classes in B-dialect: -am (6.9×), -al, -aiin, -ar, -edy (all depleted). Add a horizontal line at 1.0× (baseline). The visual contrast between -am and all other suffixes makes the "exclusive LL specialization" argument vivid.

### Figure 7: Self-Succession Comparison Across Mechanisms
Grouped bars or dot plot. For each onset class (qok, ok, ch) and each dialect (A, B): show self-succession enrichment in VMS alongside Naibbe (all conditions), Timm (best parameter), position-sensitive cipher, hybrid cipher-copy best. Illustrates: Naibbe depletes, Timm overproduces, position-sensitive cipher produces ~1.0, VMS sits in between, hybrid at best reaches low end of the range.

### Table 1: Candidate Findings with Statistical Detail
Full table of the 30 candidate findings with effect size, p-value, m=30 survival, m=175 survival, BH-FDR survival, cross-validation pass/fail. This is the primary results table.

### Table 2: Mechanism Failure Matrix
Rows = mechanisms (Naibbe-LatB, Timm-defaults, Timm-best75, PS-cipher-strong, Hybrid-best). Columns = metrics (-am LL, y-onset LF, d LL, ss_mean, adj_rate). Cell content: mechanism mean [95% CI] and ABOVE/BELOW/inside status relative to VMS. This is the core discrimination table.

### Table 3: Theory Verdict Summary
Rows = four theories. Columns = verdict, primary falsifying finding, strongest supporting experiment, open gaps. One-page summary for the discussion section.

### Table 4: Simulation Design Specifications
Rows = four null models (Naibbe, Timm single, Timm sweep, PS-cipher, Hybrid). Columns = n_simulations, parameter space, plaintext corpus, line-breaking protocol. Compact reproducibility reference.

---

*All experiment data is in `~/voynich-cryptanalyst/experiments/expN/data/`. All scripts are reproducible with the random seeds documented in each result.md file.*
