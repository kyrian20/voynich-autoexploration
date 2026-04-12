# Committed Claims
# Claims that have been committed to in public-facing outputs.
# Format: claim, supporting experiments, public output, last verified date.

## Updating This File

**Adding claims**: ONLY the human adds new claims. When a public-facing output is shared (paper draft, blog post, forum post, presentation, email to a named collaborator, arXiv submission), the human adds the relevant claims here before resuming the loop. If the human has shared an output and not yet updated this file, the loop is in an unsafe state: contradictions against the un-recorded claims will not be caught. When in doubt, pause the loop and update the file. Agents may PROPOSE new commitments by writing to state/proposed_commitments.md, but may not add new claim entries here.

**Narrowing claims**: The agent MAY add a "Narrowed by" line to an existing claim when a new experiment restricts the claim's scope without invalidating the original experiments. This is the only edit the agent is permitted to make to this file. See skills/write_finding.md "The Contradiction Rule" for the full procedure.

---

## C001: Position-blind generative mechanisms fail on Voynich positional grammar
**Claim**: No tested position-blind mechanism (Naibbe homophonic cipher, Timm self-citation at any of 75 parameter combinations) reproduces the VMS positional grammar findings (-am LL enrichment, y-onset LF enrichment). Maximum -am LL across all position-blind mechanisms: 1.1× (vs VMS 6.811×).
**Supporting experiments**: exp_170, exp_171, exp_176
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Contradiction condition**: A position-blind mechanism producing -am LL ≥ 3.0× or y-onset LF ≥ 2.0× would contradict this claim.

---

## C002: Position-sensitive substitution alone cannot account for sequential word-class memory
**Claim**: A position-sensitive cipher (separate LF/MID/LL substitution tables, calibrated to Latin morphological features at up to 90% detection probability) produces ss_mean ≈ 1.00 (vs VMS 1.465). Substitution ciphers produce independent word draws per position, generating no self-succession.
**Supporting experiments**: exp_177
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Contradiction condition**: A substitution-only cipher producing ss_mean ≥ 1.15 without a copy component would contradict this claim.

---

## C003: Onset-replacing position-aware hybrid fails on ss_mean / adj_rate coupling
**Claim**: A position-aware hybrid with MID-only copying and onset-replacing modification produces 0/18 viable combinations. The modification operation replaces the onset class, destroying the feature (onset self-succession) that the copy mechanism is supposed to produce. The 0/18 result is specific to onset-replacing modification; onset-preserving modification (exp_181) produces 4/36 viable combinations.
**Supporting experiments**: exp_180
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Contradiction condition**: A re-analysis showing that onset-replacing modification does NOT destroy onset self-succession, or onset-replacing modification producing viable combinations under an extended grid, would contradict this claim.

---

## C004: Onset-preserving (suffix-replacing) position-aware hybrid reaches joint lenient viability but remains above VMS adj_rate
**Claim**: The onset-preserving, suffix-replacing variant (exp_181 architecture) produces 4/36 viable combinations under lenient thresholds (am_ll ≥ 5.0×, ss_mean ∈ [1.2, 1.7], adj_rate ≤ 0.015). Best viable: cp=0.6, mp=0.8 yields am_ll=5.755, ss_mean=1.385, adj_rate=0.0144. Under VMS-level adj_rate (≤ 0.009), 0/36 combinations of the suffix-replacing variant are viable.
**Supporting experiments**: exp_181
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-11
**Narrowed by**: exp_182 (Timm character-level modification) achieves VMS-level adj_rate viability (3 combinations at adj_rate ≤ 0.009 with ss_mean ≥ 1.2 and am_ll ≥ 5.0). The residual gap claim applies only to the suffix-replacing modification; character-level modification crosses the adj_rate threshold.
**Contradiction condition**: A re-analysis of the exp_181 suffix-replacing architecture producing viable combinations at VMS-level adj_rate (≤ 0.009) would contradict this claim. Results from architectures using different modification operations (as in exp_182) narrow rather than contradict it.

---

## C005: -am LL enrichment in Currier B is 6.811× with p < 10^-161
**Claim**: The EVA suffix -am appears at line-last position in B-dialect at 6.811 times its corpus-wide base rate. Statistical significance: p = 6.27 × 10^-161 (survives both m=30 and m=175 Bonferroni correction).
**Supporting experiments**: exp_173
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Narrowed by exp_208 (2026-04-11)**: The B LL enrichment is driven by within-paragraph LL (WP-LL: 6.69×, n=2295) rather than paragraph-final LL (PF-LL: 3.14×, n=94). The 6.811× claim reflects the pooled LL (both WP-LL and PF-LL combined); the distinction was not available at time of commitment. -am is a within-paragraph line-last marker; PF-LL shows lower enrichment because B paragraph-final words (ok/ch/ot onset from F207) are not -am suffix words.
**Contradiction condition**: A re-analysis using a different transcription system or corrected line-break identification producing -am LL enrichment < 5.0× would contradict this claim. A demonstration that the enrichment is an artifact of EVA tokenization conventions would invalidate it.

---

## C006: y-onset LF enrichment in Currier B is 3.506× with p < 10^-90
**Claim**: Words beginning with y-onset appear at line-first position in B-dialect at 3.506 times their corpus-wide base rate. Statistical significance: p = 2.86 × 10^-90 (survives both Bonferroni thresholds).
**Supporting experiments**: exp_173
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Contradiction condition**: A re-analysis producing y-onset LF enrichment < 2.0× or demonstrating the enrichment is a transcription artifact would contradict this claim.

---

## C007: Onset self-succession ranges from 1.24× to 2.05× and survives position control
**Claim**: Onset self-succession (the tendency for consecutive words to share an onset class) ranges from 1.24× (qok, B-dialect) to 2.05× (ok, A-dialect) across six class-by-dialect combinations. This self-succession survives position control (within-stratum analysis controlling for line-position effects), with residuals ≥ 1.2× across all tested onset-by-dialect combinations.
**Supporting experiments**: exp_164, exp_174
**Public output**: exp_181-revised checkpoint paper (2026-04-10)
**Last verified**: 2026-04-10
**Contradiction condition**: A re-analysis showing that position control reduces self-succession residuals to < 1.1× for the majority of onset-by-dialect combinations would contradict this claim. A demonstration that self-succession is an artifact of line-length confounding would invalidate it.
**Known issue (pending amendment)**: proposed_c007_amendment.md documents three errors: (1) range "1.24–2.05×" is wrong — canonical range is 0.78–3.86× across onset-class-by-dialect combinations; (2) "2.05× (ok, A-dialect)" is a misattribution — exp_164 shows this value is B ot→ot=2.05×, and B l→l=2.13× exceeds the stated maximum; (3) "residuals ≥1.2× for all" fails for B qok/ch/sh. Amendment awaiting human approval.

---

## C008: 21-Mechanism Architecture — 19/19 VMS Specificity and Structural Floors
**Claim**: The 21-mechanism position-aware copy-buffer architecture (exp_314 calibration: CP=0.55, MP=0.90, P_STUTTER=0.006, beta_scale=1.8, p_blind=0.115, r_lf=0.12, r_mid=0.20) achieves 19/19 PASS on the B-dialect 19-metric battery against real VMS B-dialect targets (PASS_TOL=±20%). When the same fixed parameters are applied to shuffled VMS B-dialect, the architecture achieves 10/19 — positional onset-distribution metrics fail because shuffling collapses them to ≈1.0. When a fresh 1024-combination grid search re-optimizes the architecture to match each shuffled corpus's OWN metrics as target, the best achievable pass counts are 16/19 (within-line shuffle) and 14/19 (word-to-line shuffle). The failures are exclusively in the over-generation direction: fixed constants create structural minima for ss_y (≥2.0×), ss_d (≥1.5×), adj_rate (≥0.006), and am_ll (≥1.17×) that exceed any shuffled corpus target for those metrics. The 19/19 on real VMS reflects structural specificity to VMS positional onset distributions and self-succession patterns, not 6-parameter over-fitting.
**Scope qualification (exp_579, 2026-04-12)**: The 19/19 PASS is calibrated on full B-dialect corpus metrics, which pool four sections (B_herbal ~14%, B_bio ~33%, B_astro ~15%, B_pharma ~39%) with systematically different positional grammar profiles (am_ll ranges from 0.053 in bio to 0.192 in pharma). Section composition explains 97–107% of the document-order metric gradient in B-dialect (exp_576: First half am_ll=5.825 vs Second half 7.147; 23% shift). C008 is a statement about the full-corpus aggregate; individual sections require different parameter values per section and may score differently under section-specific metrics.
**Supporting experiments**: exp_314, exp_574, exp_575, exp_576, exp_579
**Public output**: Proposed for next public-facing output following checkpoint paper (2026-04-10)
**Last verified**: 2026-04-12
**Contradiction condition**: A grid search with adjustable CP, MP, or P_STUTTER achieving ≥19/19 on shuffled corpora with those values held at or below exp_314 levels would contradict the structural floor claims. A finer grid exceeding 16/19 on intra-shuffle would narrow the claim. A re-analysis showing section-composition explains <50% of the document-order gradient would narrow the scope qualification.

---

## C009: VMS adj_rate Structure — Near-Random for sh/ch/d; Zero for s/t; Copy-Buffer Overproduces
**Claim**: (Part A) For B-dialect, the adjacent-identical-word rate (adj_rate) for sh and d is consistent with random draws from their vocabulary pools: sh 1.11× random expectation (1702 tokens, CP90=145), d 0.70× (1249 tokens, CP90=146). ch is elevated at 1.91× random expectation due to 15% ch→ch self-succession concentrating ch tokens — not a VMS anti-repetition failure. VMS does not employ a special anti-repetition mechanism for sh/ch/d. (Part B) s-onset and t-onset adj_rate = 0 in B-dialect (s: 0/452 tokens; t: 0/466 tokens). This structural zero arises from their positional constraint as line-opening classes. (Part C) The baseline 21-mechanism architecture overproduces adj_rate 1.41–1.79× above VMS for sh/ch/d even without vocabulary clamping (sh: 1.081% vs VMS 0.764%; ch: 1.020% vs 0.659%; d: 0.861% vs 0.480%). This overproduction is caused by copy-buffer + same-onset self-succession coupling (sh→sh=9.2%, ch→ch=15.0%, d→d=8.6%). Vocabulary clamping to VMS levels does not fix or amplify sh/ch overproduction.
**Supporting experiments**: exp_577, exp_578
**Public output**: Proposed for next public-facing output following checkpoint paper (2026-04-10)
**Last verified**: 2026-04-12
**Contradiction condition**: A re-analysis showing s or t adj_rate > 0 in B-dialect (non-zero identical adjacent pairs) would contradict Part B. A copy-buffer architecture with ≥8% same-onset self-succession achieving ≤1.0× VMS adj_rate for sh/ch/d without architectural changes would contradict Part C. A demonstration that ch's 1.91× ratio reflects a distinct production mechanism (not self-succession concentration) would require amendment to Part A.
