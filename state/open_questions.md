# Open Questions
# Cryptanalyst — Voynich Manuscript Investigation
# Questions that require human judgment, domain expertise, missing tools, or a dataset not currently available.
# Format: see skills/write_finding.md for the entry template.

---

## Q021: exp_584 simulation bug — corrected replication needed (exp_585) (exp_584)
**Raised by:** exp_584 (2026-04-13)
**Status:** RESOLVED by exp_585 (2026-04-13). Abstract-token simulation confirms 19/19 VMS positive control, Latin 5/17, Italian 4/17. R = 1.417. STRONG_SPECIFICITY.
**Question:** exp_584's simulation used actual VMS word strings via `pick_word(onset, suffix)`, but many VMS (onset, suffix) combos have only one unique word type (e.g., qok+aiin → always "qokaiin"). On the "modify" path of the copy-buffer, this causes spurious same-word succession, inflating adj_rate, ss_mean, ss_d, ss_y. VMS positive control got 7/17 applicable instead of expected 17/17. The STRONG_SPECIFICITY conclusion (R=1.417) is still valid because the denominator uses exp_575's clean inter-shuffle result and the structural failures in Latin/Italian are unaffected. But a corrected replication is needed to: (a) confirm VMS positive control achieves ~17/17 with abstract-token simulation, (b) get unbiased Latin/Italian PASS counts, (c) satisfy the pre-registration requirement for a clean positive control. exp_585 should use the abstract-token simulation methodology from exp_575 (timm_modify generating synthetic words, not pick_word returning actual VMS strings). Expected: VMS positive control 19/19, Latin ≤ 8/17, Italian ≤ 9/17, R ≥ 1.417.
**Relevant data:** exp_584 result.md; exp_575 simulation code (timm_modify, make_word_sim); exp_314 parameter set.

## Q018: What is the functional/linguistic interpretation of the ok/ot/o onset dominance in labels? (exp_580)
**Raised by:** exp_580 (2026-04-12)
**Status:** Open — requires comparative linguistics or expert judgment
**Question:** Labels are dominated by ok/ot/o onset classes (44% of label tokens). These classes are not elevated in body text MID grammar and are only moderately elevated at specific positions. Are ok/ot/o words a "demonstrative" or "pointing" construction in Voynich — analogous to demonstrative pronouns or determiners that accompany illustrations? The question requires either: (a) comparison to known labeling conventions in Latin, Arabic, Italian herbals (do they use demonstrative constructions as labels?), or (b) successful decipherment to establish the label semantics.
**Relevant data:** F640 (ok=2.85×, ot=2.97×, o=3.55× in labels vs body). All label sections show this pattern. Body text positional grammar is built around y/d/am/qok classes; label text uses a different onset inventory entirely.

## Q019: Are the 547 label-exclusive types (F641) cross-referenceable with botanical or astronomical proper names? (exp_580)
**Raised by:** exp_580 (2026-04-12)
**Status:** Open — requires comparison corpora or external datasets
**Question:** 547 label types appear only in label text and not in body text (53% of label vocabulary). Some of these may be:
- Plant-specific names (for herbal labels): could be matched to Latin/Italian herbals
- Star/constellation names (for astronomical labels): could be matched to Arabic star name transliterations
- Zodiac-specific terms: month names, sign names
Systematic cross-referencing of label-exclusive vocabulary against botanical and astronomical reference corpora would be high-value for the Botanist phase. This requires access to Voynich-adjacent comparison corpora for labels specifically (not body text).

## Q020: Do herbal labels (F640: y/d/a onset profile) and zodiac labels (ot/ok/o onset profile) encode genuinely different types of information? (exp_580)
**Raised by:** exp_580 (2026-04-12)
**Status:** Open — requires further label section analysis
**Question:** Per-section label analysis (F640) shows herbal labels have y/d/a onset profile (similar to herbal body text) while zodiac/star/cosmo labels have ot/ok/o onset profile (distinct from their host body text). This might mean:
(a) Herbal labels are short body-text phrases (plant descriptions) while zodiac labels are proper names (star/constellation identifiers)
(b) Different scribal conventions for label types
The section-specific analysis in exp_580 is preliminary (small N per section). A follow-up experiment focusing on herbal-only vs zodiac-only label vocabularies could test whether the onset difference reflects genuinely different semantic content.

## Q013: RESOLVED (exp_573, 2026-04-12) — C007 self-succession methodology reconciliation complete
**Raised by:** exp_565 (2026-04-11); **Resolved by:** exp_573 (2026-04-12)
**Status:** RESOLVED — see state/proposed_c007_amendment.md

**Summary of resolution**: The discrepancy between C007 (1.24–2.05×) and canonical methodology (B qok=1.03×, A ok=1.42×) is fully explained by two methodological differences:
1. **Dialect assignment**: exp_174 used folio-level edy-rate; canonical uses per-line edy-rate. Per-line classification enlarges A corpus from ~8,453 to 11,327 words (more heterogeneous lines), diluting self-succession signal by −0.46× for A ok.
2. **Formula**: exp_174 used E=obs/(total×rate²); canonical uses E=obs/(n_sender×mid_rate). MID-rate baseline is higher for MID-concentrated classes, reducing E by −0.17–0.20×.

**Additionally**: C007's upper bound "2.05× (ok, A-dialect)" is a misattribution. In exp_174, A ok=1.930× and B qo=2.047×. The 2.05 came from B qo, not A ok.

**Canonical range (obs≥10)**: 0.78× (B sh) – 3.86× (A l). CONF classes (≥1.5×/obs≥10): y, l, ot, qo, qot in both dialects; d (A). Flat/depleted: B qok (1.03×), B ch (0.91×), B sh (0.78×).

**Proposed amendment**: see state/proposed_c007_amendment.md. C007 should state that self-succession is class-specific (range 0.78–3.86×), not universal. The "residuals ≥1.2× across all tested combinations" claim fails for B qok/ch/sh.

## Q012: F470 (B herbal a→a@pos2 dir) not reproduced with len≥3 — possible 2-word contamination
**Raised by:** exp_526 (2026-04-11)
**Status:** RESOLVED — exp_527 (2026-04-11). CONFIRMED contamination: len≥2 eligibility in exp_489 included 4 two-word a-LF lines where pos2=LF=a trivially. With len≥3: obs=2, E=1.54× (below threshold). F470 RETRACTED. B herbal a-LF has no confirmed pos2 rule. Q012 CLOSED.
**Question:** F470 (exp_489) claimed B herbal a-LF → a@pos2 E=3.60×/obs=6/N_elig=19. exp_526 with len≥3 eligibility finds a@pos2 obs=2, E=1.54× (below any threshold), N_elig=16. Discrepancy: obs=6 vs obs=2, N_elig=19 vs 16.

**Probable cause:** exp_489 likely used len≥2 for pos2 eligibility. In 2-word a-LF lines, pos2=LF=a trivially — so 3 extra eligible 2-word lines would inflate obs by up to 3 (the difference between N_elig=19 and N_elig=16). After removing contamination: obs≈2-3, E≈1.5-2.5× — consistent with exp_526 finding (obs=2, E=1.54×). This is the same class of error as Q009 (F458 contamination).

**Impact:** F470 is not committed (not in committed_claims.md). If the contamination explanation is correct, a→a@pos2 in B herbal is below dir threshold. The actual B herbal a-LF pen signals are ok@pen dir (F522) and o@pen (dir) (F522) — not pos2.

**Required:** Re-run exp_489 with explicit len≥3 eligibility for pos2. If obs=2 and E=1.54×, retract F470 directional status.

## Q011: F446 (t-LF elevation in A stars) contradicted by current corpus — investigate exp_466
**Raised by:** exp_525 (2026-04-11)
**Status:** RESOLVED — exp_527 (2026-04-11). Root cause: exp_466 used ws[0] (line-FIRST) not ws[-1] (line-FINAL). F446 was measuring t at pos1 (line-opening), not t as LF (line-final). A stars t at pos1: E=2.22×/obs=16 CONF vs A-overall (E=3.67× vs A herbal_a). No measurement error — categorization error. F446 recategorized as pos1 finding → F523. t is DEPLETED at line-final (E=0.51×, exp_525). Q011 CLOSED.
**Question:** F446 (exp_466) claimed A stars t-LF elevation E=2.12×/N=15. exp_525 finds A stars t-LF N=2/136 = 1.5%, E=0.51× (DEPLETED) vs A herbal_a (2.9%). Both folio-number and per-page methodologies agree on N=2, E=0.51×. This is a complete directional reversal: F446 claimed elevation, current finding shows depletion.

**Possible sources of discrepancy:**
1. Different corpus file used in exp_466 (corpus may have been updated between exp_466 and exp_525)
2. Different A stars section definition in exp_466 (perhaps A stars included more pages)
3. Different methodology for computing E (perhaps global baseline vs section-specific)
4. Script error in exp_466

**Action required:** Examine exp_466 script to determine: (a) which corpus file was used, (b) how A stars was defined, (c) how E was computed. Compare with exp_525 methodology. If exp_466 used a stale corpus or wrong section definition, F446 should be retracted. If exp_466 is internally consistent but differs from exp_525, a deeper corpus audit may be needed.

**Impact:** F446 is cited in hypothesis_backlog.md as motivation for H_new_EJ. With F446 contradicted, t-LF is NOT an elevated LF class in A stars, and H_new_EJ is definitively closed (not "blocked" by methodology). The A stars section does not have a t-LF grammar signature worth investigating.

## ~~Q010: F455 (ok-LF pos1=y CONF) not reproducible under current methodology~~ — CLOSED (2026-04-11). F455 CONFIRMED CONF under standard methodology.

**Raised by:** exp_521 (2026-04-11)
**Status:** CLOSED — RESOLVED (inline, 2026-04-11)
**Resolution**: F455 IS reproducible at CONF under standard len≥2 pos1 methodology. Root cause of exp_521 discrepancy: exp_521 used len≥3 filter for pos1 (INCORRECT — pos1 standard uses len≥2). With len≥2: A herbal_a ok-LF (N_elig=51) → y@pos1: obs=11, exp=7.25 (baseline 14.2%), E=1.52× → **CONF** (obs≥10, E≥1.5×). With len≥3: obs=9, E=1.32× (below CONF — this was exp_521's result). F455 is CONF at the correct standard methodology. F455 also confirmed: s@pos1 dir (E=2.22×/obs=5, same as F516). Q010 CLOSED — F455 restored to CONF status.

## ~~Q009: F458 Potentially Inflated~~ — CLOSED (2026-04-11). Confirmed: 6 two-word ch-LF B herbal lines have ch at ws[1]=LF=ch trivially. len≥2→obs=19; len≥3→obs=13. F458 corrected to BELOW THRESHOLD (E=1.38×/N=13). ch→ch@pos2 is A-herbal_a-specific, not B herbal confirmed.

## Q009: F458 Potentially Inflated — 2-Word Line Contamination Bug?
**Raised by:** exp_497_b_herbal_pos2_survey (2026-04-11)
**Status:** CLOSED — Confirmed 2026-04-11
**Question:** F458 (exp_482) claimed B herbal ch-LF → ch@pos2 (E=1.74×/N=19, CONFIRMED). exp_497 with len≥3 eligibility finds obs=13/41, E=1.38× — below threshold. Discrepancy: 19 vs 13 observations, N_elig=48 vs 41. The 7 missing eligibles are 2-word B herbal ch-LF lines; in 2-word lines, ws[1]=ws[-1]=LF word. If exp_482 used len≥2 eligibility, those 7 lines would trivially have ch at "pos2" (= the LF word), inflating the ch→ch@pos2 count by up to 7. This is the same class of error as the F453/F454 pen baseline bug (wrong position used as baseline). If confirmed, F458 needs correction: E=1.38×/N=13 (below CONF threshold). ch→ch@pos2 in B herbal would be BELOW CONFIRMED, consistent with B herbal's general lack of confirmed pos2 self-chaining.

**Required:** Check exp_482 script eligibility criterion for pos2. Re-run with len≥3. If obs=19 is confirmed only with len≥2 (contamination), retract CONFIRMED status and note as below-threshold.

## ~~Q008: F448 Potentially Incorrect~~ — CLOSED by exp_488 (2026-04-11)
**Closed:** F448 RETRACTED. ok@pos2 obs=0. exp_476 classified y at pos1 lines as y-LF. See exp_488_f448_retraction/result.md.

## Q008: F448 Potentially Incorrect — y-LF → ok at pos2 Not Reproduced
**Raised by:** exp_487_pos2_selfchain_survey (2026-04-11)
**Status:** Open — requires investigation of exp_476 methodology
**Question:** F448 (exp_476) claimed A herbal_a y-LF → ok at pos2 (E=2.25×/N=20, CONFIRMED). exp_487 directly computed the full pos2 distribution for y-LF in A herbal_a and found ok at pos2 has obs≤1 (below min threshold of 2). The actual y-LF pos2 signature is y-SELF at pos2 (E=7.87×/N=8, directional), consistent with the universal self-chaining pattern. If F448 is wrong, the y-LF → y-SELF finding replaces it and F448 should be retracted.

**Possible causes of the discrepancy:**
1. exp_476 may have used a different LF-identification method (e.g., included lines where y appears near-final but not strictly terminal)
2. exp_476 may have used a different baseline (A-herbal_a-overall rather than pos2-specific)
3. exp_476 may have used a different word-splitting rule that inflated N
4. The "N=20" in F448 may refer to total y-LF lines tested, not obs count (possible transcription error in writing the finding)

**Required:** Re-run exp_476 methodology to verify: (a) how y-LF lines were selected, (b) what baseline was used for ok at pos2, (c) whether the obs=20 claim is reproducible. If not reproducible, retract F448 and assign new finding for y-LF → y-SELF at pos2 (directional, pending N=8 upgrade to confirmed status).

---

## Q007: B-Dialect Vocabulary Richness Gap — Simulation Over-Produces 2.2× Unique MID Types; Phase 6 Identifies Closed Paradigm as the Constraint
**Raised by:** exp_280/281 (2026-04-11); Phase 6 exp_295 updates the characterization
**Status:** Open — root cause identified (Timm character mutation at MP=0.90 generates too many unique words); Phase 6 provides new target constraints
**Question:** The simulation generates ~6,400 unique MID word types at optimal parameters vs VMS ~2,929 (2.2× over-production). Phase 6 (exp_295) reveals that the B-dialect VMS MID vocabulary is dominated by closed paradigms: B-qok 32 word types cover 90% of tokens (18.2% of vocabulary); B-ok 33.8%; B-ot 39.0%; B-sh 43.3%. The simulation does not match these paradigm sizes.

**Why reducing MP doesn't help:** MP<0.90 breaks the battery (exp_281). The over-production is structural to character mutation at the current MP level.

**Phase 6 new constraint:** For the simulation to match VMS, the buffer vocabulary must produce word-type concentration matching the closed paradigm sizes per onset class. This requires either: (1) a more constrained midfix generation (matching VMS midfix inventory), or (2) a word-type-level reuse mechanism (buffer explicitly returns previously-generated words from closed paradigm). Neither is currently implemented.

**Required:** Design a mechanism that simultaneously: (a) maintains the 19/19 battery pass, (b) reduces unique MID word types to ~2,900, (c) produces per-onset-class closed paradigm sizes matching VMS (18-47% of types cover 90% of tokens). H491 (suffix-length conditioning) does not address vocabulary richness.

---

## ~~Q006: Menzerath r Structural Gap~~ — CLOSED by Phase 7 (exp_302–314)
**Raised by:** exp_282 (2026-04-11)
**Closed:** 2026-04-11 (exp_314: 21-mechanism architecture, Menzerath r=104% of VMS)
**Status:** CLOSED — 5 new mechanisms (17th-21st) closed the gap from 19% → 104% of VMS. r_mid=100% (exact), r_ll=97%, menz_r=−0.234 (within VMS 95% CI). See working_position.md Section 8.1 update and F306-F316 for full closure documentation.

---

## Q005: What Was the Source of F261's VMS s→s = 0.887 Claim? — ANSWERED by exp_330
**Raised by:** exp_274 (2026-04-11)
**Closed:** 2026-04-11 (exp_330: A-dialect MID s→s = 0.887× directly observed)
**Status:** CLOSED — exp_330 (F332) measures A-dialect MID s→s = 0.887× (the F261 value). B-dialect MID s→s = 0.000× (zero adjacent s-onset bigrams observed in B MID). The Q005 explanation was correct: F261's VMS s→s = 0.887 was the A-dialect MID-only computation. The B-dialect value is zero (not 0.887), and the global value would be somewhere between these. The F261 claim is correct for A-dialect MID; it was being compared to B-dialect simulation (which is why the discrepancy appeared — wrong dialect comparison). No committed claims are affected. The B-dialect s→s = 0 finding is a new structural constraint: s-onset words in B-dialect MID never appear adjacent to each other.
**Question:** F261 reported VMS s→s = 0.887 (depleted) and sim s→s = 4.47-7.20 (5-8× gap). exp_274 measures global A-dialect s→s = 2.09 (enriched) and B-dialect s→s = 1.19 (enriched). The most likely explanation is that F261's VMS "s→s" was the MID-only A-dialect computation (E2_mid = 0.887, N=1) rather than the global computation. But this should be verified by re-running exp_261's VMS reference computation. The discrepancy is not a committed claim (C001-C007 don't reference s→s), so no public output is affected. Resolution would: (1) confirm or deny the MID-vs-global explanation, (2) update F261 if the claim is wrong.
**Why this needs attention:** F261 also reported l→l = 7.666 (VMS) which matches exp_274's l→l ~ 7.14 — so F261 is internally partially correct. The s→s claim stands out as the one inconsistency. If it was a MID-only vs global mismatch, F261 should be corrected.
**Required:** Re-run exp_261's VMS ss computation code to check what corpus subset and measurement method it used.

---

## Q004: What Mechanism Generates sh→qok Enrichment — CLOSED by exp_323
**Raised by:** exp_243 (2026-04-11)
**Closed:** 2026-04-11 (exp_323: class-level grammar rule confirmed; cross-dialect pair overlap 2%)
**Status:** CLOSED — exp_323 (F325) identifies the mechanism as a CLASS-LEVEL grammar rule: when any sh-onset word appears in MID position, P(next=qok) ≈ 0.267 (B-dialect), 1.967× expected. This is NOT lexical co-clustering (cross-dialect pair overlap ≈ 2%; same class enrichment in A and B with near-zero specific pair overlap). The enrichment is achieved passively by the copy buffer (sh and qok co-populate the buffer from same text sections). NEW FINDING: sh→ch is DEPLETED 0.555× in both dialects — sh transitions prefer qok and avoid ch. A-dialect sh→sh=1.312× (self-succession elevated); B-dialect bidirectional qok↔sh coupling present, A-dialect absent.
**Further refined by F372 (exp_370, 2026-04-11):** sh→qok is driven by a specific sh-WORD SUBCLASS ('she-' body sh words: shedy/shey/sheedy/sheol in B; sheody/sheol/sheey in A), not a uniform sh-class rule. The qok word distribution after sh is baseline-proportional — sh selects INTO qok-class uniformly. shol/shor/shody have LOW qok rates (E=0.2-0.8×). Architecture implication: implement as body-conditional rule (sh+e-body → elevated qok successor), not a global sh-onset class memory rule.

---

## Q003: ~~COMMITTED CLAIM AT RISK — C004 Contradiction from exp_182 (Timm Char Modification)~~ RESOLVED
**Raised by:** exp_182_timm_char_modification
**Date raised:** 2026-04-11
**Date resolved:** 2026-04-11
**Resolution:** Human applied Option A (2026-04-11): C004 narrowed to apply only to the exp_181 suffix-replacing architecture. A "Narrowed by" annotation citing exp_182 has been added to committed_claims.md by the human. The finding has been recorded in findings.md (F177) and the loop has resumed. The contradiction rule was updated in write_finding.md and SOUL.md to distinguish hard contradictions from narrowings: this case is a narrowing (new mechanism restricts scope, original exp_181 results still hold). The C004 contradiction condition text was written too broadly; the narrowed claim preserves the specific result that 0/36 exp_181 suffix-replacing combinations pass VMS adj_rate, while acknowledging that character-level modification is a distinct architecture that does pass.

---

## ~~Q004: HUMAN DIRECTIVE — Discrimination Priority (2026-04-11)~~ RESOLVED
**Raised by:** Human + Opus review of exp_182–186
**Date:** 2026-04-11
**Date resolved:** 2026-04-11
**Resolution:** All three items completed. H408 (parameter-count control) → exp_224. H409 (corpus split) → exp_223/273. H410 (expanded battery) → exp_217, leading to the full Mode B 19/19 architecture (exp_235–257). The discrimination thread reached its natural conclusion with 19/19 PASS on both dialects. Phase 5 (architecture construction) is complete. Direction now shifts to Phase 6 (word-internal structure).

Standing instruction preserved: when resolving backlog hypotheses, move them to state/archive/hypothesis_backlog_resolved.md instead of marking RESOLVED in the active backlog.

---

## Q002: ZL3b L0 Overloading — Scope and Impact on Published Label Analyses
**Raised by:** exp_011_single_char_validation (f49v/f66r inspection)
**Date:** 2026-04-09
**Question:** ZL3b encodes three structurally different things under the L0 locus code: (1) true object labels, (2) line margin markers (f49v: single chars alternating with P0 body text), (3) list/table column entries (f66r two-column word list). This conflation caused 83% of herbal "labels" in exp_010 to be misclassified. Two questions: (a) What fraction of L0 entries across the FULL ZL3b manuscript (all folios, all sections) fall into each of the three structural categories? (b) Do published analyses that use ZL3b label data account for this, or are they similarly affected? Notable papers using label analysis: Montemurro & Zanette (2013) semantic structure, Zandbergen's ZL3b documentation, Bowern & Lindemann's statistical analysis.
**Why this can't be resolved by current tooling:** Requires either reading ZL3b documentation on the L0 locus code variants, or auditing all L0 entries programmatically (which is H021). May also require contacting the ZL3b authors (Zandbergen) or checking whether the IVTFF format specification distinguishes these subcategories.
**What it would take to resolve it:** Run H021 (L0 structural audit); also check whether ZL3b has sub-locus distinctions (e.g., Lx, La, Lb, L0 variants) that already encode the structural distinction we discovered empirically.

## Q001: What is the word-initial entropy of actual medieval Latin?
**Raised by:** exp_001_word_initial_entropy
**Date:** 2026-04-09
**Question:** The exp_001 Latin baseline was mistakenly the Douay-Rheims Bible in English (Gutenberg #8300) rather than actual Latin. The "Caesar" file (Gutenberg #10657) was also an English translation. What is the correct word-initial entropy for medieval Latin, and how does Voynich's 3.137 bits compare? Virgil's Aeneid and Caesar's De Bello Gallico in Latin are now available (downloaded 2026-04-09) but the comparison has not been re-run.
**Why this can't be resolved computationally:** It can — the real Latin files exist and the script needs to be re-run pointing at the correct files.
**What it would take to resolve it:** Run exp_001's analysis substituting Virgil/Caesar Latin for the Douay-Rheims file. This is a cleanup task, not a new hypothesis; integrate into exp_002.
