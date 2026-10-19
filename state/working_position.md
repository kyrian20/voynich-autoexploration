> **Archived checkpoint warning — 2026-10-19:** this document is a historical snapshot dated 2026-04-12 and ends at exp_579/574. It is retained for provenance and should not be read as the current status. The current canonical checkpoint is [state/current_state.md](current_state.md); the cross-experiment synthesis for exp_589–599 is [research/synthesis/2026-10-19-daiin-position-synthesis.md](../research/synthesis/2026-10-19-daiin-position-synthesis.md). Do not restart from the experiment number in this archived file without checking those newer records.

---

# Working Position — Voynich Manuscript Cryptanalysis
**Date**: 2026-04-12 (through exp_579 — Cryptanalyst phase closure COMPLETE)
**Archive**: state/archive/working_position_2026_04_11.md (through exp_524, 1388 lines)
**Audience**: Researcher picking up this document cold.

---

## 1. PROJECT STATUS

**574 experiments completed.** The project has passed through six phases: characterization (exp_001–169), theory discrimination (exp_170–186), Mode B architecture construction (exp_217–258), paragraph grammar (exp_194–216), Menzerath/word-structure (exp_259–287), word-internal structure (exp_288–301), Menzerath closure and 19/19 architecture (exp_302–314), and corpus grammar characterization (exp_315–574).

**Primary result (as of 2026-04-12):** The 21-mechanism copy-buffer hybrid architecture achieves 19/19 PASS on a B-dialect 19-metric battery (exp_314, N=30). A negative control (exp_574) confirms the 19/19 is VMS-specific — the architecture fails to 10/19 on shuffled corpora. Theory discrimination is complete: all three tested alternative mechanisms fail. The committed claims (C001–C008) have been validated except C007, which requires amendment (proposed_c007_amendment.md, awaiting human approval).

**Phase 12 (exp_525–574):** Full characterization of 20+ onset classes (positional roles, vocabulary, within-line bigrams, across-dialect comparisons), terminal pair analysis (exp_572), C007 reconciliation (exp_573), and architecture specificity negative control (exp_574).

---

## 2. WHAT HAS BEEN RULED OUT

### 2.1 Position-blind ciphers: ruled out as the sole mechanism

**Key result:** -am LL enrichment is 6.5× in VMS B-dialect. Across 1,900 position-blind simulations (400 Naibbe homophonic cipher + 1,500 Timm local-copy at 75 parameter combinations), the maximum achievable is 0.57×. The gap (6.5× vs 0.6×) is structural: position-blind mechanisms cannot produce position-dependent distributions by definition.

**Convergent failure:** Naibbe (substitution cipher) and Timm (local copy) are fundamentally different mechanisms. Both fail at the same four positional metrics (am_ll, y_lf, d_ll, qok_lf_depl), indicating position-blindness as the shared failure cause.

**Statistics:** All four positional metrics survive dual Bonferroni correction (m=175), with p < 10⁻²⁶ for the weakest. Cross-validated 80/20 and leave-one-section-out (exp_172, exp_173).

**What remains open:** Position-sensitive ciphers are NOT ruled out. A target-calibrated position-sensitive cipher (exp_177, Latin Cicero, separate LF/MID/LL tables) achieves am_ll = 5.756× — substantially closer to VMS than position-blind alternatives. However, the calibration was target-aware (LL table explicitly maps Latin clause-final morphemes to EVA -am), and this mechanism produces ss_mean ≈ 1.0× (fails Property 2 entirely). A position-sensitive cipher that also independently generates sequential onset-class memory remains untested.

### 2.2 Pure self-citation: ruled out as the sole mechanism

Timm overproduces exact-word repetition (adj_rate = 0.037 vs VMS 0.009, 4×) at parameters that produce VMS-level self-succession. At parameters that lower adj_rate, ss_mean drops far below VMS. These two constraints pull in opposite directions throughout the 75-combination parameter space — no combination resolves the joint constraint (exp_176). Additionally, VMS MI at lags 2–7 is BELOW the Timm 95% CI: any copy-window mechanism generates elevated MI within the window, but VMS lacks this signature (exp_175; lags 10–12 retracted as sampling artifact).

### 2.3 Pure template-generation: ruled out as the sole mechanism

-am is uniquely 6.5× enriched at LL while edy (most common B-suffix, 18%) is 0.35× depleted at LL. A generic positional slot would not produce this contrast — the slot must have onset-class grammar rules specifying which suffix classes belong at LL. Self-succession also survives position control (residual 1.2–1.8× after removing positional co-occurrence, exp_174), meaning onset-class sequential rules operate independently of positional assignment.

---

## 3. THE DUAL CONSTRAINT

**Voynichese exhibits two structural properties that no single tested mechanism can produce simultaneously.**

**Property 1: Position-sensitive onset-class grammar.** am_ll enrichment (6.5×), y-onset LF enrichment (3.2×), qok LF depletion (0.75×), and d-onset LL enrichment — present in VMS, absent from all position-blind mechanisms (~1.0×), partially reproduced only by target-calibrated ciphers. All four survive Bonferroni m=175 and 80/20 cross-validation.

**Property 2: Sequential word-class memory.** Onset self-succession (ss_mean ≈ 1.16× mean; CONF classes reach 2–4×) and qok→ch enrichment (1.27×) require word-class decisions to be correlated across adjacent words. No tested cipher mechanism produces this at VMS levels while satisfying Property 1.

**Any viable generation mechanism must simultaneously satisfy both.** Position-blind mechanisms fail on Property 1. Position-sensitive substitution fails on Property 2. The only mechanism class that passes both is the position-aware copy-buffer hybrid described in Section 4.

---

## 4. THE 19/19 ARCHITECTURE

### 4.1 Architecture overview

The "Mode B" copy-buffer architecture (exp_217–314) is the first mechanism to jointly satisfy both dual-constraint properties within ±20% across 19 measured B-dialect metrics.

**Core design:** Line-final (LL) and line-first (LF) words are generated by a position-sensitive onset/suffix mechanism; mid-line (MID) words are drawn from a copy buffer and modified (character-level modification, onset preserved). This gating decouples am_ll enrichment (produced by the LL mechanism) from self-succession (produced by buffer recycling of words with shared onset classes).

**21-mechanism finalized B-dialect architecture (19/19 PASS, N=30; exp_314):**

| Parameter | Value | Effect |
|-----------|-------|--------|
| p_blind (conditional) | p_short=0.060 (n≤5), p_long=0.180 (n≥10) | 18th mech: n-conditional blindness |
| max_ll_len | mild_s30: max(3, round(8−0.3×max(0,n−5))), MAX_RETRY=10 | 19th mech: short-line LL word-length filtering |
| beta_eff(n) | 0.50 × 1.8 × n/8.4 [for word_idx≥2] | 20th+21st mech: n-conditional Menzerath scaling |
| vocab_clamp | qok/ok/ot/qot: full VMS type inventory | 17th mech: sparse-midfix onset clamping |
| cp=0.55, mp=0.90 | copy/modify probabilities | core buffer mechanics |
| p_qokch=0.12, p_chqok=0.12 | qok↔ch transition probabilities | onset grammar coupling |
| p_stutter=0.006 | exact-repeat probability | adj_rate calibration |
| r_lf=0.12, r_mid=0.20 | LF/MID randomization rates | position-specific register |
| mu_len=8.4, sigma_len=3.0 | word-length distribution | length calibration |
| p_mf=0.20, p_lf_mf=0.50, p_ll_mf=0.00 | midfix placement probabilities | vocabulary richness |
| gamma=0.30, alpha=0.20, beta_base=0.50, beta_scale=1.8 | Menzerath calibration | word-length-suffix correlation |

**Battery performance (exp_314, N=30):**
- 19/19 PASS (all metrics within ±20% of VMS_REF)
- Menzerath r = −0.234 (104% of VMS −0.225; slight overshoot)
- r_ll = −0.213 (97% of VMS −0.219); r_mid = −0.178 (100% of VMS)
- MID slope = −0.072 (123% — moderate overshoot)

### 4.2 What the 19/19 means

The 19/19 does NOT mean VMS is generated by exactly this mechanism. It means this is the first mechanism class that jointly satisfies both dual constraints within measurement precision.

**What it demonstrates:**
- A position-aware copy-buffer hybrid CAN produce all 19 measured properties simultaneously
- The dual constraint (Properties 1 and 2) does not require a near-impossible parameter coincidence — it is achievable by a class of mechanisms where positional grammar and sequential memory operate through structurally separate components
- The specific onset/suffix distributions and positional grammar of VMS B-dialect are consistent with a relatively compact generative mechanism (21 mechanisms, ~15 calibrated parameters)

**What it does NOT demonstrate:**
- That VMS IS generated by this mechanism
- That no other mechanism class could also achieve 19/19 (untested)
- That the mechanism is the correct interpretation of the text (decipherment not attempted)
- That A-dialect is generated by the same architecture (partially tested: exp_239 achieved 19/19 on A-dialect battery, but with different parameter values)

### 4.3 Known gaps outside the 19-metric battery

- sh/ch/d onset classes: CP90 over-produced (3.2–4.1×); clamping these breaks adj_rate
- sh→qok enrichment (B: E_mid=1.97×): architecturally unresolved
- Menzerath r: 4% overshoot (104%)
- MID word repetition distances: 2.3× too short
- Short-line LL word-length deficit: sim 5.007 vs VMS 5.684 at n=2–4

---

## 5. ARCHITECTURE SPECIFICITY (exp_574, 2026-04-12)

**Question:** Is the 19/19 evidence that the architecture captures VMS-specific structure, or merely that the architecture has enough parameters to fit any corpus?

**Method:** Fix exp_314 parameters. Test three corpora against VMS_REF:
1. Real VMS B-dialect (positive control)
2. Within-line shuffled VMS (words reordered within each line — destroys positional structure)
3. Word-to-line shuffled VMS (all words redistributed — destroys positional and sequential structure)

**Result:**

| Condition | Pass count | Positional metric pass (11) | Sequential metric pass (5) |
|-----------|-----------|----------------------------|---------------------------|
| Real VMS | 19/19 | 11/11 | 5/5 |
| Intra-shuffle | 10/19 | 5/11 | 5/5 |
| Inter-shuffle | 10/19 | 5/11 | 5/5 |

**9 metrics failing on shuffled:** d_ll (61/66%), y_lf (30/34%), qok_lf (157/139%), d_lf (48/36%), s_lf (22/22%), qok_ll (152/153%), am_lf_enr (75/66%), am_mid_enr (181/190%), global_am_rate (124/126%). All are onset-position distribution metrics.

**10 metrics passing on shuffled:** am_ll (92/91%), ss_mean (115/115%), adj_rate (109/114%), ch_ll (102/104%), ok_ll (111/114%), ss_d (97/90%), ss_y (103/104%), qok_ch (94/94%), edy_rate, word_len_mean.

**Interpretation:**
- Architecture is NOT a flexible universal fitter. It requires real VMS onset-position distributions to pass positional metrics.
- The 10 corpus-independent passes reveal mechanism-driven signals: copy-buffer (ss_mean, ss_d, ss_y, adj_rate) and LL-placement (am_ll) are always active. They do NOT require VMS-specific distributions.
- The 9 shuffled-corpus failures are the VMS-specific component: onset-position skews (y@LF, d@LF, s@LF, qok@LF-depleted, d@LL, qok@LL-depleted) are required by the architecture to pass positional battery metrics.
- **Conclusion:** 19/19 on real VMS is genuinely specific to VMS structure. C003/C004 are not undermined by this result.

**Note:** am_mid_enr overshoots on shuffled (181–190% of VMS_REF). Investigated: when MID onset distributions are flat (shuffled), the MID suffix generation creates excess am@MID enrichment. This confirms the architectural MID mechanism was calibrated to VMS structure — it is itself part of the VMS-specific component.

---

## 6. CORPUS GRAMMAR: ONSET CLASS POSITIONAL TAXONOMY

### 6.1 Complete Positional Architecture

Two structurally distinct dialect architectures have been confirmed (20+ onset classes characterized, exp_534–572):

**A-dialect 3-layer positional structure:**
- **OPENERS** (pos1 CONF): sch(11.54×/16), p(2.99×/15), s(3.16×/163), y(2.78×/323), t(2.27×/111), qot(1.40×/73 sub-CONF), d(1.47×/346 near-CONF)
- **MID** (neutral at pos1 and LF): ch, qok, ok, ot, sh, k, ckh, qo
- **TERMINALS** (LF CONF): cth(1.67×/88), d(1.53×/360) — cth is the purest terminal (pos1 extreme DEPL 0.13×)
- **A LF-AVOIDERS**: y(0.62×), s(1.01×), t(0.96×), qok(0.57×), sh(0.51×)

**B-dialect 3-layer positional structure:**
- **OPENERS** (pos1 CONF): p(5.23×/27), s(4.77×/165), y(3.54×/147), t(3.18×/78), d(2.64×/246)
- **MID** (neutral at pos1 and LF): ch, qok, ok, ot, qot, sh, k
- **TERMINALS** (LF CONF): r(2.80×/48), l(1.85×/145), ol(1.65×/115), o(1.58×/57), a(1.52×/70)
- **B LF-AVOIDERS**: y(0.60×), qok(0.58×), sh(0.47×/0.39×)

**Cross-dialectal CONSTANTS:**
- y, qok, sh are LF-depleted in BOTH dialects
- ch and a are pos1-avoiders in BOTH dialects
- A/B terminal inversion: A closes with {d,cth} (aiin-body + compound gallows); B closes with {r,l,ol,o,a} (lateral/vowel-initial) — zero overlap

### 6.2 Key Onset Class Characterizations

**d-onset (F553–556):** A/B positional INVERSION — A is dominant LF class (LF CONF 1.53×/360, 18.4% of A lines), B is dominant LINE-OPENER (pos1 CONF 2.64×/246, 19.2% of B lines). Both dialects: MID-depleted (A: 0.73×; B: 0.67×). A d→cth CONF (1.97×/62); B d→sh CONF (1.79×/109). d is the key dialect-crossing class.

**y-onset (F557–559):** Definitive LINE-OPENER (pos1 CONF: A 2.78×/323, B 3.54×/147). ALL other positions depleted in both dialects. y→y CONF cross-dialectally (A 1.88×/40, B 3.18×/20). Routes to gallows: y→ckh CONF (A), y→k CONF (B).

**qot-onset (F530–535):** A/B positional INVERSION — A: pos1 CONF (1.40×/73, near-CONF), B: pos1 DEPL (0.69×/37). qot→qot CONF cross-dialectally (A 2.88×/18, B 1.82×/29). B: sh→qot CONF (1.97×/72), qot→ot CONF (1.77×/45), qot→r CONF (1.97×/10). A: t→qot CONF (2.03×/11). F535: d→qot CL chain is INTER-LINE only (d→qot within-line NULL: A 0.99×, B 0.66× DEPL).

**ch-onset (F547–550):** EXTREME pos1-AVOIDER (A: 0.32×/154; B: 0.22×/53 — most extreme B class). ch→sh DEPL cross-dialectally (F328). B ch→l CONF (1.56×/135), ch→t CONF (1.67×/35). Ch-LF has no CONF opener rule in either dialect — the only major LF class with absent opener grammar. ch vocabulary: A y-body dominant (42.5%); B adds edy (28.6%) but retains y as dominant — most dialect-stable vocabulary class.

**sh-onset (F544–546):** A routes to gallows {sh→k CONF 1.75×/31, sh→t CONF 1.62×/13}; B routes to q-class {sh→qok CONF 2.02×/331, sh→qo CONF 1.92×/68, sh→qot CONF 1.74×/78}. sh is a **dialect-specific router** class. sh→ch DEPL cross-dialectally (A 0.65×/127, B 0.54×/92). sh is MID-biased; avoids LF in both dialects.

**qok-onset (F618–620):** LF-DEPL cross-dialectally (A 0.51×/82, B 0.53×/112). A→B frequency DOUBLES (7.30%→15.13%). sh→qok CONF both (A 2.04×/114, B 2.07×/266). B qok→r CONF (1.95×/30). A qo→qok CONF. Self-succession: A 1.27× sub-CONF, B 1.03× flat (CONF classes elsewhere).

**Compound gallows positional taxonomy (F607–610, exp_561):**
- sch: OPENER (pos1 CONF 11.54×/16 A — highest pos1 E-value characterized, extremely rare ~0.20%)
- cth: TERMINAL (LF CONF 1.67×/88; pos1 EXTREME DEPL 0.13×; 8.6× frequency drop A→B)
- ckh: MID (pos1 near-zero 0.07×; LF DEPL 0.67×/18)
- cph: MID/LL (pos1 near-zero; LL sub-CONF 1.45×/12)
- UNIVERSAL: ALL 4 compound gallows route to d within A lines (cth→d CONF 1.97×/37; ckh→d CONF 2.00×/18; cph→d dir 2.50×/7; sch→d dir 3.43×/6)

**Terminal pair findings (exp_572, F635):** [c-gallows@LL][d@LF] CONF (E=2.10×/28; cth=50%); [d@LL][d@LF] CONF (E=1.57×/68 — d self-continuation LL→LF). Word pairs diverse (no formula crystallization).

### 6.3 Self-Succession Under Canonical Methodology

Onset self-succession varies substantially by class and dialect. Under canonical methodology (per-line edy-rate dialect assignment, MID-baseline formula):

| Class | A herbal_a | B all | CONF status |
|-------|-----------|-------|-------------|
| l | 3.86×/16 | 2.62×/72 | CONF both |
| ol | 3.20×/45 | 1.32×/30 | CONF A |
| qot | 3.16×/18 | 1.69×/29 | CONF both |
| y | 1.88×/40 | 3.16×/20 | CONF both |
| ot | 2.23×/50 | 2.10×/90 | CONF both |
| qo | 1.76×/14 | 1.82×/16 | CONF both |
| d | 1.75×/151 | 1.35×/41 | CONF A |
| ok | 1.42×/81 | 1.30×/56 | sub-CONF |
| qok | 1.27×/77 | 1.03×/242 | sub-CONF A; FLAT B |
| ch | 1.04×/453 | 0.91×/259 | FLAT both |
| sh | 1.21×/96 | 0.78×/76 | FLAT A; NEAR-DEPL B |

C007 amendment: The committed C007 range "1.24–2.05×" is incorrect (see proposed_c007_amendment.md). Canonical range is 0.78×–3.86× across onset-class-by-dialect combinations. The attribution "2.05× (ok, A-dialect)" is a misattribution — in exp_174 this value belongs to B qo=2.047×, not A ok.

---

## 7. GRAMMAR BEYOND THE WORD LEVEL

### 7.1 Line-Level Formula Structure

**Three-register line grammar** (F345–365, section-invariant):
- **Register 1 — Folio-opener lines:** 71–80% gallows-onset LF (p/k/t/f), long lines (~7–8 words), hapax-dominated (85%); ANTI-GALLOWS LL (A: 0.29×; B absent); gallows register confined to word_index=0 only
- **Register 2 — Continuation lines:** d/qok/s/y dominant at LF; am/l dominant at LL; standard word-count distribution; content-grammar active
- **Register 3 — Folio-closer lines:** SHORT (B=4.81 words, A=3.94 vs ~7–8 continuation); ANTI-GALLOWS LF (B: 0.60×, A: 0.44×); B: l/ol/ot enriched at LF 3.4–3.9×; A-dialect p-onset: 37.3% folio-opener LF → 0/83 folio-closer LF (complete exclusion). Pattern section-invariant across all characterized sections.

**B-dialect section LF taxonomy (F447, exp_467):**

| Section | Primary LF marker(s) | Depleted |
|---------|---------------------|----------|
| B herbal | t(2.34×) + y(1.52×) + ot(1.55×) | qok, s, ok, ch |
| B astro | q-bench triplet: qok(1.78×)+qot(1.94×)+qo(1.60×)+s(1.31×) | y(0.47×), t(0.70×) |
| B pharma | ok(1.47×) + o(1.53×) | qok, t, qot |
| B cosmo | t(2.23×) | qot=0, qo depleted |

**A stars grammatical inversion** (exp_527, F523/F524): Astronomical marker appears at pos1 in A (t pos1 CONF 3.67×/16), at LF in B (qok LF elevated). Stars-type astronomical content encodes the astronomical marker at opposite ends of the line in the two dialects.

### 7.2 Cross-Line (Paragraph) Grammar

**A herbal_a cross-line (CL) network** (F490–514, exp_515–524):

The A herbal_a CL structure is a directed acyclic network, NOT cyclic:
```
d ——→ qot (F491, CONF) ——→ ch (F490, CONF) ——→ o (F506, CONF) ——→ sh (F507, dir)
 \                                                                  \
  ——→ t (F508, CONF) ←——(F510, dir)—————————————————————————————
               |——→ d (E=1.47×, nearly CONF) [soft reset]
               |——→ y (dir, F512)
               |——→ ot (dir, F513)

sh ——→ ok (F509, dir) ——→ ol (F514, dir)
k ——→ ot (F511, dir)
```

d is the origin hub; qot is the "pivot" class that enables the chain (qot-LF is near-absent in other sections); t is the relay class. The chain is NOT active in B herbal (qot-LF absent) — the full CL network is A herbal_a-specific.

**Key scope finding (F555, exp_543):** d→qot operates ONLY at the inter-line level. Within a single line, d→qot succession is NULL (A: E=0.99×; B: E=0.66× DEPL). This is the clearest scope confirmation: zero within-line signal, strong CL signal — two distinct mechanisms at different structural levels.

**B-dialect CL (corrected from F444):** B-dialect CL is heterogeneous and section-specific. Confirmed signals:
- B astro: qok→qok CL (F495, E=1.77×/14 CONF), d→qo dir, ol→o dir
- B herbal: ot→ch (F526, dir, E=2.63×/5); d→ok CONF (F527), d→d CONF, ot→ot CONF, ot→a CONF (pooled herbal+pharma)
- B pharma: ol→qok (F496, E=2.76×/10 CONF); ol→qok confirmed F528

### 7.3 Within-Line Formula Structure (Section-Specific)

**A herbal_a formula matrix (exp_481–487):**

| LF class | N | pos1 | pos2 | pen | Status |
|----------|---|------|------|-----|--------|
| d | 254 | ot(1.59×/22, CONF) | flat | sh DEPL(0.85×) | F453 only |
| ch | 178 | ch-self(1.58×/30, CONF)+sch(dir) | ch-self below CONF (1.34×/80) | ch/k below threshold | F473 pos1 CONF |
| cth | 74 | qo(dir, 3.59×/6) | cth-self below CONF | d(1.61×/18, CONF) | F474 pen CONF |
| y | 37 | y-self(2.13×/11, CONF) | y-self(3.81×/5, dir) | o(dir) | F472 pos1 CONF |
| ok | 32 | y(1.62×/12, provisionally dir; Q010) | ok(dir) | — | F455 flagged |
| ot | ~25 | y(1.83×/11; CONF at pooled 1-72) | — | — | F456 CONF |

**B pharma penultimate grammar (F449–452):** B pharma uniquely shows onset persistence at penultimate position. ch persists at pos1; ot/l persist at pen; ok closes with a-suffix class at pen. Creates "entry" (pos1) and "exit" (pen) onset signatures.

---

## 8. COMMITTED CLAIMS AND OPEN QUESTIONS

### 8.1 Committed Claims Status

| Claim | Status | Notes |
|-------|--------|-------|
| C001: Position-blind mechanisms cannot reach am_ll>0.7× | VALID | 1,900 simulations, max 0.57×; exp_574 specificity test not new evidence for C001 |
| C002: Substitution alone produces ss≈1.0× | VALID | exp_574 confirms: shuffled corpus produces ss_mean≈1.00–1.25× — architecture's ss from copy-buffer mechanism, not distributions |
| C003: 19/19 PASS on B-dialect battery | VALID | exp_314; now confirmed VMS-specific by exp_574 |
| C004: Copy-buffer hypothesis | VALID | exp_574 confirms copy-buffer generates ss_mean/ss_d/ss_y regardless of corpus; the mechanism is real |
| C005: Dual-dialect structure | VALID | per-line edy-rate methodology canonical |
| C006: Menzerath holds for VMS B | VALID | r=−0.225; architecture reproduces at 104% |
| C007: Onset self-succession range 1.24–2.05× | **REQUIRES AMENDMENT** | See proposed_c007_amendment.md. Canonical range: 0.78–3.86×. Three errors: wrong bounds, attribution error (2.05 belongs to B qo not A ok), "residuals ≥1.2× for all" fails for B qok/ch/sh |
| C008: A/B dialect differentiation | VALID | Complete terminal-class inversion, onset-class vocabulary shifts confirmed |

### 8.2 Theory Assessment

| Theory | Likelihood | Basis |
|--------|-----------|-------|
| Position-sensitive writing system with sequential class grammar | HIGH | Only class surviving all discrimination tests; 19/19 architecture |
| Natural language encoded in VMS | POSSIBLE | Structured grammar consistent with natural language; no decipherment |
| Artificial language (constructed with rules) | POSSIBLE | Grammar is compact and rule-like, consistent with construction |
| Glossographic production (medical/herbal notation) | POSSIBLE | Section-specific grammar consistent with domain encoding |
| Position-blind substitution cipher alone | RULED OUT | 1,900 simulations; structural impossibility |
| Pure self-citation (Timm alone) | RULED OUT | Joint ss_mean/adj_rate constraint unsatisfiable |
| Meaningless gibberish | LOW | Grammar is too structured and cross-dialectally consistent |

**Menzerath confidence:** HIGH (per Opus review 4.4/2). r=−0.225 (p<0.001). Architecture reproduces at 104%. Confirmed across word-length bins.

### 8.3 Open Questions

**Q013:** RESOLVED (exp_573). C007 methodology discrepancy explained.

**Active open questions:**
- **Q014:** Why does am_mid_enr overshoot on shuffled corpora (181–190%)? The architectural MID mechanism may need recalibration. Not critical for main results.
- **Q015:** F455 (A herbal_a ok-LF → y at pos1) is provisionally DIRECTIONAL — cannot reproduce at CONF with strict section definition (exp_521). Resolution requires methodological clarity on section boundaries.
- **Q011:** RESOLVED (exp_527) — F446 is pos1 grammar, not LF.
- **Q010:** F455 methodology uncertainty — see above.
- **Q012:** k-onset gallows anomaly (k NOT LF-enriched unlike p/t/f). H606 open.
- **Q016:** B p→sh→{pos2} full grammar. H607 open.

### 8.4 Priority Session Results (exp_575–578, 2026-04-12)

**Priority 1 — Architecture specificity via refit shuffle (exp_575):**

Fresh 1024-combo grid search optimizing to each shuffled corpus's OWN metrics as target (not fixed VMS_REF). Results:
- Real B-dialect: 19/19 (positive control confirmed)
- Intra-shuffle (within-line): best achievable = **16/19** — 3 structural impossibilities (am_ll floor ≈1.17, ss_d floor ≈1.5, ss_y floor ≈2.0)
- Inter-shuffle (word-to-line): best achievable = **14/19** — 5 structural impossibilities (same 3 plus adj_rate floor ≈0.006, ss_mean floor ≈1.36)

These floors arise from fixed constants (CP=0.55, MP=0.90, P_STUTTER=0.006, max_ll) — not searchable parameters. The 19/19 on real VMS reflects genuine structural specificity. Proposed commitment C008 written (state/proposed_commitments/proposed_c008_arch_specificity.md).

**Priority 2 — Parameter stability across corpus splits (exp_576):**

Three 50/50 splits with independent 1024-combo grid search on each half:
- **Corpus heterogeneity (key finding):** VMS B-dialect has systematic document-order heterogeneity. First half: am_ll=5.825, y_lf=2.745; Second half: am_ll=7.147, y_lf=3.889 (23% and 42% higher). Odd/Even and Random halves are nearly identical — the gradient is document-order-specific.
- **Cross-validation results:** Odd/Even: 17→15 (acceptable, 2/19 degradation). First/Second: 17→8 CATASTROPHIC (incompatible target metrics between halves). Random: 17→14 (identical parameters in both halves — the 3/19 degradation is the stochastic floor from N=10 variability).
- **Parameter stability:** beta_scale, r_mid, p_qokch unstable across 2/3 splits. p_blind stable (always 0.115). r_lf near-stable. Random split found IDENTICAL optimal parameters in both halves (|A-B|=0 for all 5), suggesting a stable local optimum for balanced B-dialect samples.
- **Interpretation:** The exp_314 calibration values are full-corpus averages, not stable structural constants. The architecture generalizes for balanced splits (15/19 Odd/Even cross-val); the First/Second catastrophic failure is corpus heterogeneity, not parameter degeneracy. The 19/19 result stands as a valid average-case calibration. F638 written.

**Priority 3 — Q007 three-way constraint diagnosis (exp_577, exp_578):**

Q007 states: the architecture cannot simultaneously achieve VMS sh/ch/d vocabulary restriction (CP90=145/290/146) AND low adj_rate. Two-experiment diagnosis:

*exp_577 (VMS corpus analysis):* VMS adj_rate for sh/ch/d is near-random expectation from their CP90 pools (sh: 1.108×, d: 0.701×, ch: 1.910×). VMS has no special anti-repetition mechanism for sh/ch/d. s and t classes have ZERO identical adjacent pairs — structural anti-repetition from their positional constraint as line openers.

*exp_578 (copy-buffer amplification test):* The Q007 failure exists in the BASELINE simulation (before any vocabulary clamping): sim adj_rate already 1.41–1.79× above VMS for sh/ch/d. Vocabulary clamping does NOT amplify sh/ch adj_rate (slight decrease under All7_clamp). The failure is caused by **copy-buffer + self-succession coupling**: sh (9%), ch (15%), d (8.6%) self-succession rates cause the copy-buffer to systematically over-repeat words for these classes regardless of vocabulary size.

**Q007 diagnosis:** The constraint is a copy-buffer architecture artifact — any copy-buffer mechanism with ≥8% same-onset self-succession will overproduce adjacent identical pairs for that class. VMS's near-random adj_rate is incompatible with a copy-buffer that operates on same-onset successors.

Full synthesis: state/q007_investigation.md.

### 8.5 exp_579 — Document-Order Heterogeneity Driver (2026-04-12)

**Question:** What drives the B-dialect document-order gradient found in exp_576 (First half am_ll=5.825 vs Second half 7.147)?

**Method:** Three candidate drivers tested: (A) scribal hand transitions, (B) section composition, (C) genuine linguistic drift. Metrics computed by folio quartile and by section. Section composition prediction model: predicted quartile metric = Σ(section_fraction × section_mean).

**Results:** Section composition explains 97–107% of the observed half-shift for all five primary metrics (am_ll 107%, y_lf 107%, d_ll 99%, s_lf 101%, qok_lf 96%). Enrichment factors match exp_576 targets within 5–8%. The gradient is step-wise, not monotonic: Q2 dips due to bio domination (bio has lowest am_ll=0.053); Q3–Q4 elevate due to pharma domination (pharma has highest am_ll=0.192). First half = 65% bio + 28% herbal; Second half = 77% pharma + 23% astro. Scribal hand NOT isolable as independent driver — hand×section co-linear in B-dialect. Within B_astro, Hand 4 (rose foldout) anomalous from diagram-label content only. F639 written.

**Committed claim qualification:** The 19/19 PASS (C008) is a full-corpus average over these heterogeneous sections. Section-level calibration would require different parameters per section. See C008 scope qualification.

### 8.6 exp_584 — Architecture Non-VMS Specificity Test (2026-04-13)

**Pre-registered test of C008 (architecture specificity to VMS structure)**. Three non-VMS corpora: Medieval Latin (Cicero De Officiis, 32K words), Italian (Dante Divina Commedia, 89K words), VMS inter-shuffle (from exp_575). 17/19 applicable metrics (excluding word_len_mean and edy_rate as pre-registered).

**Results (6-param grid, 512 combos):**
- Latin (Cicero): 8/17 applicable PASS
- Italian (Dante): 9/17 applicable PASS
- Inter-shuffle (exp_575): 12/17 applicable PASS
- VMS (exp_314): 17/17 applicable PASS (used for R numerator)

**Specificity ratio R = 17/12 = 1.417 ≥ 1.3. PRE-REGISTERED CLASSIFICATION: STRONG_SPECIFICITY.**

**Structural failures driving Latin/Italian below VMS:** y_lf (VMS LF distribution biases y-onset → sim always produces y_lf ≈ 3.5×, Latin target ≈ 1.0×), s_lf (same mechanism), global_am_rate (VMS vocabulary has ≈2% am-suffix; Latin target 18% is unreachable), ss_mean/adj_rate/ss_d/ss_y (copy-buffer floors exceed flat targets — same structural argument as exp_575 inter-shuffle).

**Corrected replication (exp_585) confirms:** VMS positive control 19/19 PASS (17/17 applicable). Latin 5/17, Italian 4/17 applicable PASS (even fewer than buggy exp_584's 8/17 and 9/17). R_6param = 17/12 = 1.417 confirmed. Both C008 and exp_585's own VMS applicable give identical R. Q021 RESOLVED.

**C008 status: RETAINED, strengthened by R = 1.417.**

### 8.7 Cryptanalyst Phase Closure (2026-04-12)

**Housekeeping session (2026-04-12) complete.** Three commitments applied: C008 (19/19 specificity + structural floors), C009 (adj_rate structure), and the C003 scope qualification (incorporated within C008). Proposal files moved to state/proposed_commitments/applied/. Commitments audit written (state/commitments_audit_2026_04_12.md). Key audit finding: committed_claims.md C007 has three known errors — amendment in proposed_c007_amendment.md, awaiting separate human approval.

**Cryptanalyst loop is at its closure point.** 579 experiments completed. The pending items for human review are: (1) proposed_c007_amendment.md — C007 range and attribution correction. No new experiments are queued. Next phase is Grammar Spec consolidation as directed.

**Canonical committed claim numbering** (committed_claims.md) differs from working_position.md informal numbering: working "C003=19/19 PASS" = committed **C008**. Use committed_claims.md as authoritative.

### 8.8 Transliteration Replication — Section 2 Findings Confirmed (2026-04-13, exp_586–588)

**Pre-registered replication of all 5 Section 2 findings across 3 alternative transliteration systems.** Pre-registration: ≥2/3 systems must RETAIN each finding.

| Finding | EVA-basic (R1) | v101 Claston (R2) | ZL3a (R3) | Overall |
|---------|---------------|------------------|-----------|---------|
| F1: Three-layer positional architecture | 18/18 RETAINED | 16/18 RETAINED | 18/18 RETAINED | **RETAINED** |
| F2: Terminal dialect inversion | RETAINED | RETAINED | RETAINED | **RETAINED** |
| F3: Bigram cross-dialect invariants | 4/5 RETAINED | 4/5 RETAINED | 4/5 RETAINED | **RETAINED** |
| F4: A-herbal paragraph chain | 96th/97.5th RETAINED | 77th/86.5th **FAILED** | 97.5th/96.5th RETAINED | **RETAINED** (2/3) |
| F5: -edy suffix transformation | 20/21 RETAINED | 19/22 RETAINED | 20/21 RETAINED | **RETAINED** |

**ALL 5 FINDINGS RETAINED.** The F4 partial exception (v101 failure) is attributed to low observation counts on the o→sh chain edge (obs=1 in v101's A-herbal corpus vs obs=4 in ZL3b/ZL3a). v101 infrastructure documented in experiments/exp_587_replication_v101/result.md; full cross-session analysis at state/transliteration_replication_final_summary.md.

**Paper implication:** Section 2 characterization findings are transliteration-robust. Draft claim: "All five Section 2 findings replicated in ≥2/3 alternative transliterations; four replicated in all three systems."
