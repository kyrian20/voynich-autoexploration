# Opus Review — 2026-04-12
## Comprehensive Review of Experiments 200–568

**Reviewer**: Claude Opus 4.6 (independent meta-review)
**Scope**: exp_200 through exp_568 (~370 experiments over ~3 days of autonomous operation)
**Purpose**: Comprehensive assessment of findings, methodology, structural integrity, and strategic direction

---

## EXECUTIVE SUMMARY

The Voynich Cryptanalyst has produced an extraordinary body of work: 568+ experiments, 629+ numbered findings, a 21-mechanism simulation architecture achieving 19/19 battery PASS on both dialects, and the most detailed statistical characterization of Voynich Manuscript word-class grammar I'm aware of in the literature.

**The five most important results (exp_200+):**
1. **Dual constraint** (exp_170–186): VMS requires BOTH position-sensitive grammar AND sequential word-class memory simultaneously — no single mechanism produces both
2. **19/19 architecture** (exp_235–314): Position-aware copy-buffer hybrid reproduces all 19 tested VMS structural metrics within tolerance, with Menzerath r at 104% of VMS
3. **Terminal-layer dialect inversion** (exp_555/557): A-dialect terminals = {d, cth}, B-dialect terminals = {r, l, ol, o, a} with ZERO overlap — the sharpest cross-dialect structural contrast found
4. **Onset-class bigram grammar** (exp_324): Complete 7×7 succession matrix revealing 5 cross-dialect invariant couplings and bidirectional ch↔sh avoidance
5. **Three-register line grammar** (exp_345–353): Folio-opener (gallows LF, long) / continuation (baseline) / folio-closer (anti-gallows, short) — section-invariant scribal layout constraint

**The system is methodologically sound.** Self-audits are being run, committed claims are tracked, bugs are caught and retracted (F446, F458, F465, F470). The main concerns are strategic, not methodological: the last ~35 experiments show narrow focus on onset characterization, and the backlog had bloated to 1,669 lines (now pruned to 166).

---

## PART 1: ARCHITECTURE EVOLUTION (exp_200–314)

### 1.1 Mode B Construction (exp_217–258)

The core architecture is a position-aware copy-buffer hybrid:
- **Cipher component**: generates LF and LL words with position-specific onset distributions
- **Copy buffer**: MID words drawn from a rolling buffer of recent words, modified at character level (Timm modification) with onset preserved
- **Gating**: This decouples positional grammar (cipher component) from sequential memory (buffer recycling)

Key mechanisms added through the construction phase:
- exp_219: onset-preserving modification (cp=0.55, mp=0.90)
- exp_220: VMS LF onset distribution (p_lf=1.0)
- exp_226: edy-suffix preservation with fresh-word fallback
- exp_228: qok→ch Markov bias (p_qokch=0.12)
- exp_231: VMS LL onset distribution with d_boost=9.13%
- exp_234: edy-conditional connector
- exp_235–236: **19/19 PASS achieved** on B-dialect battery

**Assessment**: The architecture is well-motivated — each mechanism addresses a specific VMS structural property, and exp_224 (parameter-count control) confirmed each is individually necessary. The six target-calibrated parameters (p_blind, p_stutter, r_lf, r_mid, d_boost, beta_scale) are explicitly disclosed. This is honest target-aware engineering, not secret overfitting.

### 1.2 A-Dialect Generalization (exp_239–264)

A-dialect achieves 19/19 PASS with dialect-specific recalibration. Four structural parameters transfer unchanged (cp, mp, p_qokch, p_lf). Six calibration parameters require dialect-specific values. Three additional Markov rules needed: p_y_y=0.10, p_o_o=0.10, p_sh_qok=0.10 (vs B-dialect's qok↔ch bidirectional coupling).

Key cross-dialect insight: A adj_rate = B adj_rate = 0.00933 to 4 decimal places — the strongest cross-dialect invariant. This is a deep structural property of the manuscript, not a coincidence.

13/19 metrics pass with zero recalibration (B parameters applied to A corpus), confirming the mechanism class is shared. Corpus-split stable: 17–18/19 on both even/odd splits.

### 1.3 Menzerath Closure (exp_302–314)

Five mechanisms added in rapid succession closed the Menzerath r gap from 19% → 104% of VMS:

| Mechanism | # | Menzerath r | Δ |
|-----------|---|------------|---|
| Pre-Phase 7 baseline | 16 | −0.043 (19%) | — |
| Vocabulary clamping | 17 | −0.109 (48%) | +29pp |
| n-conditional p_blind | 18 | −0.137 (61%) | +13pp |
| LL word-length filter | 19 | −0.163 (73%) | +12pp |
| n-conditional MID beta | 20 | −0.203 (90%) | +17pp |
| beta_scale=1.8 | 21 | −0.234 (104%) | +14pp |

**Assessment**: This is the most impressive engineering sequence in the project. Each mechanism targets a specific decomposed component (r_ll, r_mid, Menzerath r) and is motivated by VMS diagnostic data. r_mid=100.1% of VMS is a remarkable exact match. The slight overshoot (104%) is within VMS 95% CI.

**Concern**: beta_scale=1.8 was selected specifically because it gives r_mid=100.1% — this is target-aware calibration at the finest level. The system correctly discloses this. But the total parameter count is now 21 mechanisms with 6+ calibrated values. The model's explanatory power vs. its degrees of freedom should be discussed in any publication.

### 1.4 Residual Architectural Gaps

These gaps are well-documented and honestly characterized:

1. **sh/ch/d vocabulary explosion**: CP90 still 3.2–4.1× over-produced. Clamping these breaks adj_rate (exp_317) or Menzerath r (exp_318). The three-way constraint (CP90 + Menzerath + adj_rate) appears irreducible — VMS requires morphological productivity that the simulation cannot match. This is arguably the most important unsolved problem.

2. **sh→qok B-dialect**: E_mid=1.967× (339 observations). The magnitude is too large for a Markov mechanism without breaking other metrics. Driven by 'she-' body subclass (exp_372). No viable architecture-consistent mechanism identified.

3. **MID word repetition distances**: Simulation produces 41-word median vs VMS 96 words (2.3× too short). Root cause: vocabulary size mismatch.

4. **MID slope overshoot**: 123% of VMS target. Accepted as architectural floor — IDX_THRESH adjustment makes it worse (exp_315).

---

## PART 2: CORPUS CHARACTERIZATION (exp_288–568)

### 2.1 Word-Internal Structure (Phase 6, exp_288–301)

**Three-tier midfix structure**: Onset classes cluster by ZeroMid rate into sparse (qok/ok/ot/cth: ≥66%), moderate (ch/sh/d: 35–60%), and rich (y/o/p/t: <35%). This taxonomizes the VMS vocabulary into template-copying classes vs. vocabulary-rich classes.

**Two-tier vocabulary**: Template words (frequent, short, onset+suffix) coexist with vocabulary-rich words (hapax-dominated, long midfix, complex interior). 69.2% of VMS word types are hapax.

**B-dialect closed paradigms**: Dramatically smaller than A-dialect:
- B-qok: 32 types for 90% token coverage (18.2% of vocabulary)
- A-qok: 71 types (57.3%)
- Bio section is the tightest paradigm (15 qok types for 90%)

**Character-level discoveries** (exp_321–322):
- d-onset body traces daiin template: B0=a(73%), B1=i(40%), B2=i(42%), B3=n(49%)
- y-onset B0 = 80% gallows — y-onset is a y+gallows compound class
- A/B B0 reversal: B uses 'e'-primary (60–73%), A uses 'o'-primary (45–48%) for ch/sh
- No categorical character boundaries — distributional, not exclusive

### 2.2 Onset-Class Bigram Grammar (exp_324–372)

The complete 7×7 onset-class bigram matrix (exp_324) is a landmark result. It reveals:

**Five cross-dialect invariant elevated pairs:**
1. y→y: 2.49× (B), 2.85× (A) — strongest self-succession
2. sh→qok: 1.97× (B), 1.74× (A) — class-level coupling
3. ok→ok: 1.32× (B), 1.96× (A) — ok self-succession
4. y→d: 1.37×/1.38× — later refined: continuation-only artifact (exp_361 shows A=0.96× in continuation)
5. qok→s: 1.36×/1.39× — consistent but small N in A

**One cross-dialect invariant depletion:**
- sh→ch: 0.555× (B), 0.565× (A) — robust, large N (119/70 observations)

**B-dialect specific:**
- ch→sh ALSO depleted (0.567×) — bidirectional ch↔sh mutual avoidance
- d→d enriched (1.54×) — daiin-sequence clustering
- qok→y depleted (0.64×), d→qok depleted (0.59×)

**A-dialect specific:**
- qok↔ok bidirectional coupling (2.03×/1.68×) — absent in B
- sh→sh enriched (1.31×) — sh self-succession in A only
- qok→qok enriched (1.75×) — qok self-succession in A, neutral in B

**Deeper characterization** (exp_326–372):
- ch↔sh avoidance is dual mechanism: folio-level line segregation + within-line sequential grammar (exp_326)
- A-dialect asymmetric: ch→sh normalizes in mixed lines (E=0.954) but sh→ch persists (E=0.742)
- sh→qok driven by 'she-' body subclass (shedy/shey/sheedy): body-conditional rule (exp_372)
- Self-succession is UNIVERSAL among template classes in A (qot=2.60×, ot=1.94×, y=1.92×, ok=1.82×, etc.) with gallows {k,t,f} as exception (exp_369)
- ok→ok is class-level onset memory: 84–86% different ok words in successive pairs (exp_363)

**Assessment**: The bigram matrix is one of the project's strongest contributions. The cross-dialect invariants are statistically robust and the methodology is clean (independence null model, asymmetric enrichments confirm model validity). The one correction needed: y→d was initially reported as cross-dialect invariant but exp_361 showed it's a cross-register artifact (continuation-only E≈1.0).

### 2.3 Three-Register Line Grammar (exp_345–366)

**Discovery (exp_345/351/353)**: VMS has three distinct line registers:

1. **Folio-opener** (first line of each folio): 67–70% gallows-onset LF (p/k/t/f), E=3.28–5.23× vs continuation, 7–8 words, 85% hapax LF vocabulary
2. **Continuation** (middle lines): baseline d/qok/s/y LF distribution
3. **Folio-closer** (last line): anti-gallows LF (E=0.44–0.60×), SHORT (4–5 words), distinct vocabulary

**Key properties:**
- Section-invariant: every section shows the same three-register structure (bio=73% gallows at opener, highest)
- Gallows formula is ONE-WORD constraint (LF only — MID/LL at baseline)
- A-dialect p-onset: 37.3% at folio-first LF → 0/83 at folio-last LF (complete exclusion)
- t=0% at pos1 (second word) of folio-opener in BOTH dialects — universal grammar rule
- ch/sh ratio gradient: opener(1.00/0.82) → cont(1.86/1.15) → closer(15.5/2.0) in A/B

**Assessment**: This is a clean, compelling finding. The section-invariance establishes it as a scribal layout constraint operating above content grammar. The hapax-dominated opener vocabulary (no single formula word, just onset-class constraint) is a nuanced observation that rules out simple template explanations.

### 2.4 Full Onset-Class Characterization (exp_534–568)

The system completed systematic 4-part characterization (positional profile, vocabulary, bigrams, self-succession) for every major onset class. This is comprehensive reference work. Highlights:

**Positional architecture confirmed:**
- **OPENERS** (pos1-CONF): p (B: 5.23×), s (B: 4.77×), y (B: 3.54×), t (B: 3.18×), d (B: 2.64×), sch (A: 11.54× — most extreme)
- **MID classes**: ch, sh, qok, qot, ok, ot, k
- **TERMINALS** (LF-CONF): A={d(1.53×), cth(1.67×)}; B={r(2.80×), l(1.85×), ol(1.65×), o(1.58×), a(1.52×)}

**Terminal-layer dialect inversion** (exp_555/557): ZERO overlap between A and B LF-CONF classes. This is the cleanest dialect discriminant in the project.

**Compound gallows taxonomy** (exp_558/561):
- sch=OPENER (pos1 11.54×), cth=TERMINAL (LF 1.67×), ckh=MID, cph=MID/LL
- All compound gallows → d coupling (cth: 1.97×, ckh: 2.00×, cph: 2.50×, sch: 3.43×)
- Combined compound gallows drop 6.7× from A→B (4.29%→0.64%), except sch (stable)

**Universal edy-suffix as dialect marker**: Across every onset class, A uses -ol/-or/-ey and B uses -edy/-eedy. This is the most systematic vocabulary transformation between dialects.

**qok frequency doubling**: 7.30%→15.13% A→B, driven by B astro section (19.58%). This is larger than previously appreciated.

### 2.5 Positional Bigram Routing Matrices (exp_376–395)

Complete pre_LL→LL routing matrices (A: N=1206, B: N=2161) and LF→pos1 matrices. Key findings:

**A-dialect routing:**
- d→d dominant LL (N=69, E=1.38×)
- ok→ok (2.52×), ot→ot (2.04×), cth→ot (2.33×)
- ch→r (2.18×) — ch routes to r at LL
- ol→ok (2.78×)

**B-dialect routing:**
- sh→qok (2.73×) — sh→qok concentrates at pre_LL→LL
- d→d (2.10×), s→ol (2.98×)
- y→y (6.18× directional)
- qot→r (2.27×), r→sh (2.19× — new)

**'she-' body sh as TRIPLE HUB** (exp_372/373/376):
- Receives d→sh (exp_373: E=1.63×, N=154)
- Receives s→sh (exp_376: E=2.47× at LF→pos1)
- Sends sh→qok (exp_372: E=1.97×)
- The 'she-' body sh subclass is the most connected node in the bigram network

**Position-specific rule differences between dialects** (exp_376):
- B rules are LF/LL position-specific (s→sh at LF→pos1 only: 83% of hits)
- A rules are position-general (sh→qok at MID: 1.90×; A sh→qot position-general)

### 2.6 Paragraph-Level Chain Grammar (exp_490–546)

**A herbal confirmed linear chain**: d → qot → ch → o → sh (unidirectional, no cyclicity):
- d→qot CONF, qot→ch CONF (E=1.77×), ch→o CONF (E=1.60×), o→sh directional (E=3.03×)
- sh is terminal: no backward links to ch
- t is a RELAY off the main chain (receives from d and sh, routes to d/y/ot)
- d→d CL CONF (E=1.77×, N=101) — d-lines self-succeed forming paragraph clusters

**B herbal+pharma** has different chains: d→ok, d→d, ot→ot self-succession
**B astro** has independent network: qok self-chains, ol→qok

**Assessment**: The A herbal chain (d→qot→ch→o→sh) is a major finding. It describes paragraph-level word-class succession — the "rhythm" of word types across consecutive lines. This goes beyond any published characterization I'm aware of.

---

## PART 3: METHODOLOGY AUDIT

### 3.1 Self-Audit Compliance

All experiments from the audit-skill introduction onward include explicit self-audit sections addressing target-awareness, feature-destroying implementation, extrapolation, negative-result scope, and control-comparison. Compliance is near-universal.

**Quality assessment**: The self-audits are genuine, not perfunctory. Examples:
- exp_324 (bigram matrix): "section-level confounds cannot be ruled out without controlling for section composition" — honest acknowledgment
- exp_316 (CP90 diagnostic): "N=30 aggregate vs single-realization VMS makes the ratio not directly comparable" — correct methodological caveat
- exp_356 (register pos1): "B folio-closer by-LF-onset conditional: some N=2-6 (directional only)" — appropriate sample-size flagging

### 3.2 Bug Discovery and Retraction

The system has caught and retracted several findings due to 2-word-line contamination:
- **F465** (d-self@pos2): 2-word artifact. With len≥3: E=1.12× — not confirmed
- **F470** (B herbal a→a@pos2): contaminated. With len≥3: obs=2 — below threshold
- **F446** (t-LF in A stars): categorization error — was measuring pos1, not LF. Recategorized as F523
- **F458** (ch→ch@pos2 in B herbal): inflated by 2-word lines. Corrected to below threshold

**Assessment**: Finding and retracting bugs is a sign of methodological health, not weakness. The 2-word-line contamination class was identified, understood, and systematically checked. This is good practice.

### 3.3 Committed Claims Status

Seven committed claims (C001–C007) from the checkpoint paper. Current status:

| Claim | Status | Notes |
|-------|--------|-------|
| C001 (position-blind fails) | Solid | No challenges |
| C002 (substitution lacks memory) | Solid | No challenges |
| C003 (onset-replacing fails) | Solid | No challenges |
| C004 (suffix-replacing viability) | Narrowed by exp_182 | Character-level modification crosses threshold |
| C005 (-am LL = 6.811×) | Narrowed by exp_208 | WP-LL vs PF-LL decomposition |
| C006 (y-onset LF = 3.506×) | Solid | No challenges |
| C007 (self-succession 1.24–2.05×) | **At risk** | Q013: exp_565 finds B qok=1.03× (vs claimed 1.24×); exp_567 finds A ok=1.42× (vs claimed 2.05×) |

**C007 concern**: This is the most important open discrepancy. The claimed lower bound (1.24× for B qok) and upper bound (2.05× for A ok) both show substantial discrepancies with current canonical methodology. The likely explanation is pre-canonical B classification methodology in exp_164/174, but this needs explicit reconciliation before any further publication. The system correctly flagged this as Q013 and is NOT citing the discrepant values — exactly the right behavior.

### 3.4 Open Questions

| Q# | Status | Importance |
|----|--------|-----------|
| Q001 | Open — Latin entropy baseline needs rerun | Low |
| Q002 | Open — ZL3b L0 overloading scope | Low-Medium |
| Q007 | Open — vocabulary richness gap | **High** |
| Q013 | Open — self-succession methodology discrepancy | **High** |
| Q003–Q006, Q008–Q012 | Closed/Resolved | — |

Q007 (vocabulary richness) and Q013 (self-succession methodology) are the two critical open issues that need resolution before any further publication.

---

## PART 4: STRATEGIC ASSESSMENT

### 4.1 What Has Been Accomplished

The project has established:

1. **A rigorous statistical characterization** of VMS word-class grammar exceeding anything in the published literature. The onset-class taxonomy, positional enrichment profiles, bigram succession rules, and paragraph-level chain grammar are all novel contributions.

2. **A discrimination framework** that rules out three mechanism classes (position-blind ciphers, pure self-citation, template generation without memory) and establishes the dual constraint as the minimum requirement for any viable generation hypothesis.

3. **A constructive proof** (the 21-mechanism architecture) that a position-aware copy-buffer hybrid CAN reproduce all tested VMS structural properties simultaneously.

4. **Cross-dialect structural analysis** revealing both shared invariants (adj_rate equality, y→y self-succession, sh→qok coupling, three-register line grammar) and sharp divergences (terminal-layer inversion, d-onset positional reversal, compound gallows frequency collapse, edy-suffix systematization).

### 4.2 What Has NOT Been Accomplished

1. **No decipherment.** The analysis identifies regularities but does not decode any text.
2. **No source language identification.** No tested language produces VMS positional grammar through any tested cipher.
3. **No vocabulary model.** The simulation over-produces word types 2.2× and cannot match closed paradigm sizes for sh/ch/d without breaking other metrics.
4. **No inter-folio model.** The analysis is primarily within-folio/within-section. Cross-folio sequential structure is uncharacterized.
5. **No unique mechanism identification.** The 19/19 architecture demonstrates feasibility, not uniqueness. Multiple mechanism families could potentially satisfy the same constraints.

### 4.3 Strengths of the Current Approach

- **Hypothesis-driven**: Every experiment tests a specific, pre-registered hypothesis
- **Self-correcting**: Bugs are found and retracted; claims are narrowed when new evidence restricts scope
- **Honest about limitations**: Target-awareness is disclosed; "what the model can't reproduce" is explicitly documented
- **Breadth**: Coverage spans positional grammar, bigram structure, word-internal morphology, paragraph grammar, cross-register variation, cross-dialect comparison, and section-specific analysis
- **Statistical rigor**: Bonferroni correction, cross-validation, sample-size awareness, enrichment ratios with observation counts

### 4.4 Weaknesses and Risks

1. **Narrow recent focus**: The last ~35 experiments (534–568) are all systematic onset characterization. While thorough, this risks diminishing returns. The CLAUDE.md instruction to switch categories after 5 narrow experiments is not being followed.

2. **Working position drift**: The working_position.md was last updated through exp_524 and still has Menzerath confidence as "Very low" despite the 104% closure at exp_314. The confidence table needs updating.

3. **Backlog management**: Chronic issue. Despite repeated pruning (now 4+ times), the backlog bloats because resolved hypotheses accumulate in-place. The structural fix (CLAUDE.md housekeeping rules) partially works but needs enforcement.

4. **21 mechanisms and counting**: The architecture's complexity is a double-edged sword. Each mechanism is individually motivated, but 21 mechanisms with 6 calibrated parameters against 19 metrics leaves limited degrees of freedom. Any publication needs to address the overfitting concern explicitly, even if the mechanisms are well-motivated.

5. **Missing negative controls**: The 19/19 PASS is against VMS targets. But what about randomly shuffled VMS text? What about other historical manuscripts? The architecture should ideally FAIL on non-VMS data to demonstrate specificity. This has not been tested.

6. **C007 at risk**: The self-succession claims need methodology reconciliation before further publication.

### 4.5 Recommended Next Directions

**Immediate (before resuming the loop):**
1. ✅ Prune the backlog (done — 334→21 entries)
2. Update working_position.md confidence table (Menzerath should be "High", not "Very low")
3. Resolve Q013 (re-examine exp_164/174 methodology vs. current canonical)

**Short-term exploration priorities (next loop session):**
1. **Cross-folio sequential structure**: Does word-class grammar persist across folio boundaries? Are there quire-level patterns?
2. **Negative controls**: Run the 21-mechanism architecture against shuffled VMS text, random text, or another manuscript (e.g., Codex Seraphinianus). The architecture should fail on non-VMS data.
3. **Inter-section transition analysis**: How do word-class distributions change at section boundaries? Is the transition gradual or sharp?

**Medium-term:**
1. **Vocabulary model**: The three-way constraint (CP90 + Menzerath + adj_rate) for sh/ch/d is the hardest open problem. May require a fundamentally different approach to word generation — morphological rules rather than character mutation.
2. **A-dialect architecture update**: The A-dialect architecture (13 mechanisms) hasn't been updated with Phase 7's Menzerath mechanisms. Bringing it to 21 mechanisms would be valuable.
3. **Publication preparation**: Not necessarily a paper, but organizing findings into a structured document that could be shared with domain experts would provide external validation.

---

## PART 5: DETAILED FINDINGS INVENTORY

### 5.1 Findings by Category

**Positional Grammar (F293–F302, F345–F366, F383–F395, F568–F629)**
- 3-layer positional architecture: openers → MID → terminals
- 3-register line grammar: opener / continuation / closer
- Terminal-layer dialect inversion: A={d,cth}, B={r,l,ol,o,a}
- Complete per-onset positional profiles for 20+ onset classes

**Bigram Grammar (F324–F342, F369–F395)**
- 7×7 onset-class succession matrix with 5 cross-dialect invariants
- ch↔sh bidirectional avoidance (B-dialect), unidirectional in A
- sh→qok driven by 'she-' body subclass
- Position-conditional bigram rules (B: LF-specific; A: position-general)
- Complete pre_LL→LL and LF→pos1 routing matrices

**Word-Internal Structure (F287–F303, F318–F327)**
- Three-tier midfix structure (sparse/moderate/rich)
- Two-tier vocabulary (template words vs. vocabulary-rich hapaxes)
- d-onset body = daiin template (a+i+i+n character by character)
- y-onset = y+gallows compound class (94% gallows at B0)
- Character zone rules (q onset-exclusive, n suffix-exclusive)

**Paragraph Grammar (F199–F217, exp_490–546)**
- 5-tier paragraph positional system
- A herbal linear chain: d→qot→ch→o→sh
- d→d paragraph self-succession (E=1.77×)
- Section-specific CL networks (B herbal≠B astro≠A herbal)

**Architecture & Simulation (F282–F320)**
- 21-mechanism B-dialect architecture (19/19 PASS)
- Menzerath r closure: 19%→104% via 5 new mechanisms
- Vocabulary clamping resolves CP90 for sparse onsets
- Three-way constraint (CP90+Menzerath+adj_rate) irreducible for sh/ch/d
- Suffix length is primary word-length component gap (−20%)

**Cross-Dialect Contrasts (distributed across all categories)**
- d-onset positional inversion (B: LF-enriched 2.29×, A: LL-enriched 1.68×)
- Compound gallows A-dominant (4.29%→0.64%, 6.7× drop)
- qok frequency doubling (7.30%→15.13% A→B)
- Universal edy-suffix as B-dialect marker
- adj_rate exact cross-dialect match (0.00933)
- A: position-general bigram rules; B: position-specific

### 5.2 Failed Approaches (X001–X009)

All nine failed approaches are from early characterization (exp_001–050 range). No new failed approaches recorded since exp_200. This is because Phase 6+ experiments are characterization (measuring corpus properties) rather than hypothesis-testing (trying mechanisms that might fail). The absence of failed approaches in recent work is expected, not concerning.

### 5.3 Retracted/Corrected Findings

| Finding | Issue | Resolution |
|---------|-------|-----------|
| F446 | Categorization error (pos1 vs LF) | Recategorized as F523 |
| F448 | Not reproduced | Retracted (exp_488) |
| F458 | 2-word contamination | Corrected to below threshold |
| F465 | 2-word artifact | Retracted |
| F470 | 2-word contamination | Retracted |

### 5.4 Key Experiment Cross-References

| Experiment | What it established | Impact |
|-----------|-------------------|--------|
| exp_235–236 | 19/19 PASS (B-dialect) | Architecture proof-of-concept |
| exp_239 | 19/19 PASS (A-dialect) | Cross-dialect generalization |
| exp_273 | Corpus-split stability | Not overfitting |
| exp_314 | 21-mechanism arch, Menzerath 104% | Architecture completion |
| exp_324 | 7×7 bigram matrix | Bigram grammar discovery |
| exp_345 | Folio-opener gallows formula | Three-register discovery |
| exp_351 | Folio-closer structure | Register grammar completion |
| exp_372 | sh→qok = 'she-' body driven | Mechanism refinement |
| exp_389 | Complete routing matrices | Positional bigram closure |
| exp_524 | A herbal CL chain mapped | Paragraph grammar |
| exp_555/557 | Terminal-layer inversion | Sharpest dialect discriminant |
| exp_561 | Compound gallows taxonomy | 4-role positional system |
| exp_562 | Compound gallows → d coupling | Universal coupling rule |

---

## PART 6: FINDINGS THAT MATTER MOST FOR VMS UNDERSTANDING

Stepping back from the technical details, what does this work tell us about the Voynich Manuscript?

### 6.1 The manuscript has real grammatical structure

This is not random, not noise, not a simple cipher artifact. The word-class grammar (onset classes, positional enrichment, sequential succession, paragraph chains) operates at multiple levels simultaneously:
- **Within words**: onset class determines suffix paradigm and midfix complexity
- **Between adjacent words**: class-level succession rules (sh→qok, ch↔sh avoidance, self-succession)
- **Within lines**: 3-layer positional architecture (openers → MID → terminals)
- **Across lines**: paragraph chain grammar (d→qot→ch→o→sh in A herbal)
- **Across folios**: three-register line grammar (opener/continuation/closer)

No known cipher produces this multi-level structure. The dual constraint (position-sensitivity + sequential memory) is the minimum requirement, and even the 21-mechanism simulation — which satisfies 19 metrics — cannot reproduce the full vocabulary structure.

### 6.2 The two dialects are structurally related but deeply different

A and B share:
- The same architecture class (position-aware copy-buffer hybrid)
- Identical adj_rate (0.00933)
- The same three-register line grammar
- The same bigram invariants (y→y, sh→qok, sh→ch avoidance)

But they differ in:
- Terminal-layer classes (zero overlap)
- d-onset function (A terminal vs B opener)
- Compound gallows usage (A=4.29% vs B=0.64%)
- Vocabulary system (A: -ol/-or/-ey vs B: -edy/-eedy)
- Bigram architecture (A: position-general rules; B: position-specific)
- Closed paradigm sizes (B: 3× tighter than A)

The relationship is systematic, not random. The edy-suffix transformation affects every onset class uniformly. This points to either a systematic encoding difference or a genuine linguistic variation — not scribal error or random drift.

### 6.3 The bio section is special

Bio section enforces ch/sh symmetry (0.437–0.571 ratio across all folios), has the tightest closed paradigm (15 qok types for 90%), the highest gallows rate at folio-openers (73%), and unique sh+ckhy compound forms absent elsewhere. Bio is the most formulaic section — a reference standard for "pure" VMS structure with minimal content variation.

### 6.4 The daiin word is mechanistic, not meaningful

daiin accounts for 27.4% of all d-onset tokens. Its dominance is fully explained by the convergence of three VMS properties: d→-aiin body constraint (34.6% A / 22.5% B) × ZeroMid mode × d-onset frequency. It is position-neutral (LF≈MID≈LL). Its ubiquity doesn't require special explanation — it's the expected output of VMS morphological rules applied to the d-onset class. This finding challenges interpretations that treat daiin as a semantically significant "key word."

---

## APPENDIX: NUMBERS AT A GLANCE

- **Experiments completed**: 568+
- **Numbered findings**: 629+
- **Failed approaches**: 9
- **Open questions**: 4 (Q001, Q002, Q007, Q013)
- **Committed claims**: 7 (C001–C007)
- **Claims at risk**: 1 (C007)
- **Retracted findings**: 5
- **Architecture mechanisms**: 21 (B-dialect), 13 (A-dialect)
- **Battery metrics**: 19/19 PASS (both dialects)
- **Menzerath r**: 104% of VMS (B-dialect)
- **Onset classes characterized**: 20+
- **Cross-dialect invariant bigram pairs**: 5 elevated, 1 depleted
- **Largest single enrichment**: sch at pos1 in A (11.54×)
- **Most extreme depletion**: ch at pos1 in B (0.22×)
- **Strongest self-succession**: y→y (2.85× A, 2.49× B)

---

*End of Opus Review — 2026-04-12*
*Reviewer: Claude Opus 4.6 (1M context)*
