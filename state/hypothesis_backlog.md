# Hypothesis Backlog
# Cryptanalyst — Voynich Manuscript Investigation
# Format: see skills/generate_hypotheses.md for the entry template.
# Contains ONLY open/untested hypotheses. Resolved hypotheses archived in state/archive/hypothesis_backlog_resolved.md.

## H_new_GI: B qot→ot→a chain test — RESOLVED NEGATIVE (exp_571, 2026-04-11)
**Status:** RESOLVED NEGATIVE — F634. qot→ot→a: E=0.40×/1 (NEGATIVE). Chains independent. BUT qot→ot→ot CONF (E=1.58×/11). H_new_GI CLOSED NEGATIVE.

## H_new_GH: B q-bench → r routing universality — RESOLVED PARTIAL (exp_570, 2026-04-11)
**Status:** RESOLVED PARTIAL — F633. qok→r CONF+qot→r CONF+combined CONF; BUT qo→r sub-CONF. B q-bench SPLITS: [qok/qot → r] vs [qo → ol/o/self]. H_new_GH CLOSED.

## H_new_GG: qot-onset full characterization — RESOLVED (exp_569, 2026-04-11)
**Status:** RESOLVED — F630/F631/F632. qot: A→B INCREASES (2.57%→4.19%); A pos1=1.40× sub-CONF (CORRECTS prior 1.79× CONF — qot NOT confirmed opener); B pos1=0.69×/37 DEPL; qot→qot CONF cross-dialectal; B sh→qot CONF, qot→ot CONF, qot→r CONF (new). H_new_GG CLOSED.

## H_new_FZ: A line terminal structure — RESOLVED (exp_572, 2026-04-11)
**Status:** RESOLVED — F635. [c-gallows@LL][d@LF] CONF (E=2.10×/28, F611 confirmed); cth=14/28; word pairs DIVERSE (cthy→daiin tops at 3, no formula). NEW: [d@LL][d@LF] CONF (E=1.57×/68) — d LL→LF self-succession confirmed. H_new_FZ CLOSED.

## H_new_FO: Onset class positional taxonomy synthesis — compute a comprehensive multi-class positional table and update working_position.md with the complete OPENER/AVOIDER/MID/LF taxonomy
**Priority:** medium
**Source:** After exp_547-552, the following classes have been formally characterized: qot, qok, ot, ok, sh, ch, d, y, o, a, s, t, k. The positional taxonomy now shows three clear clusters: (1) OPENERS (pos1 CONF): y, s, t in both dialects; also qot (A), d (B); (2) AVOIDERS (pos1 DEPL): a (most extreme), k, ch; (3) EDGE/LF classes: d (A LF), o (B LF), a (B LF); (4) MID/neutral: sh (LF DEPL), ok, ot, k, o (A). Working_position.md needs updating with this complete taxonomy.
**Description:** This is a state update task, not a new experiment. Update working_position.md section 17.2 (or equivalent) with the complete onset class positional taxonomy table, covering all 13 characterized classes across A herbal_a and B all. Include E-values, obs counts, and class assignments (opener/avoider/MID/LF/neutral). Also update the working model if needed.
**Expected outcome:** A comprehensive taxonomy table that can guide hypothesis generation for the next research phase.
**Cost estimate:** trivial — state update only
**Prerequisites:** none

## H_new_DV: y-opening as grammar-mode switch — does pos1=y suppress LF-self@pen across all LF classes?
**Source:** inline (2026-04-11) — ok-LF y-opening (N=9): ok-self@pen = 0 (E=0.00×). ok-LF standard (N=37): ok-self@pen E=4.48×/N=7. ot-LF: same pattern (standard → cth@pen; y-opening → ot-self@pen). Hypothesis: y at pos1 is a "grammar mode switch" that suppresses the default LF-self@pen routing, activating instead either LF-self@pen (ot case) or avoiding it (ok case). More precisely: y-opening lines may avoid LF-class self-succession at pen for certain classes.
**Description:** For each A herbal_a LF class with N_elig≥20 and a confirmed pen rule (ok, cth): compare pen rule E in y-opening vs standard subtype. For ok: ok-self@pen in standard=E=4.48× vs y-opening=0. For cth: d@pen in standard vs y-opening (from data: std d=14/54=26%, y-open d=4/10=40% — y-opening may actually ENHANCE d@pen for cth). Test whether the pattern is consistent (y-opening suppresses self-chain at pen) or LF-class-specific.
**Expected outcome:** If y-opening suppresses LF-self@pen universally: ok(seen), ot(NOT suppressed — ot-self@pen ENHANCED in y-opening, which breaks the pattern). So the pattern is NOT universal self-suppression. It may be: y-opening lines use a different "grammar mode" that has different pen routing for each LF class.
**Cost estimate:** small (compare pen distributions by y-opening/standard for all major LF classes)
**Prerequisites:** none

## H_new_AU: B pharma qok-LF → sh at pen: Body-Conditional Test

**Priority:** low
**Status:** open
**Source:** exp_479/480: B pharma qok-LF pen → sh (E=2.34×/N=7, dir). B pharma has qok body-conditional bifurcation (F439: qok+edy→qok-self; qok+aiin→sh within-line). Does the qok pen→sh preferentially occur in qok+aiin-body LF words (since qok+aiin routes to sh within-line)?
**Description:** Split B pharma qok-LF lines by body class of the LF word (edy-body: qokeey/qokedy; aiin-body: qokaiin/qokain). Compute sh at pen for each body class. Expected: qok+aiin-body may show higher sh at pen (consistent with F439 qok+aiin→sh rule); qok+edy-body may show qok-self at pen (consistent with F439 qok+edy→qok-self).
**Expected outcome under competing theories:**
- If qok+aiin-body → sh at pen: extends F439's within-line body-conditional rule to the penultimate position within the same line (the body-conditional rule persists through the line structure)
- If not body-conditional: sh at pen is class-level (all qok-LF lines show sh at pen, regardless of body suffix)
**Cost estimate:** trivial (subset of exp_479/480 data)
**Prerequisites:** none

## H_new_AH: A Stars t-LF → pos2 Formula Rule (t→ot at pos2 E=4.93×/N=3 Directional)
**Status:** open
**Source:** exp_466: A stars t-LF → pos2 routing: ot=4.93×(N=3), ch=2.32×(N=3), qot=2.72×(N=2) — all directional. If t→ot at pos2 is a genuine formula-type rule, it would parallel other formula types (e.g., qok→sh→k) but for A stars specifically.
**Description:** For A stars (f57-72): compute t-LF → pos2 with larger context. Are there ≥5 cases of t→ot (confirming E=4.93×)? What are the complete line structures (t→ot→pos3→...→LL)? Compare A herbal_a t-LF → pos2 (baseline routing without stars elevation).
**Expected outcome:** Either t→ot at pos2 is confirmed (N≥5, E≥3×) making it a stars-specific formula pair, or it's directional (N=3 insufficient). If confirmed: t+ot is a stars formula pair (parallel to formula types in F426).
**Priority:** low (N=3 directional; stars corpus small)

## H_new_AE: A o-onset at LL → s CL (E=2.2×/N=8): Body-Conditional Driver?
**Status:** open
**Source:** exp_464 CL onset matrix: A o→s CL E=2.2×(N=8). 'o'-onset words include 'ol', 'or', 'ok', 'ot' etc. — need onset priority check. Could overlap with ok/ot/ol. Is this a genuine o-onset (bare 'o' words) effect or an onset-classification artifact?
**Description:** Extract A-dialect CL pairs where LL onset = 'o' (after priority list). Verify these are genuinely 'o'-onset words (not misclassified ok/ot/ol). Compute body-class breakdown. Check whether the 8 s-LF cases are diverse (multiple folios, word types).
**Expected outcome:** Either the 'o'→s coupling is confirmed as a genuine class-level rule (bare-o words predict s at next line LF), or it collapses as a classification artifact. If genuine: possible link to 'o' as a paragraph-transitional onset (like A s→qot).
**Priority:** low (N=8, likely artifact; investigate only if other higher-priority hypotheses exhausted)

## H628_archived: B pos3 Grammar
**Status:** archived
**Source:** F405 (9.3% of B lines are formula-typed at LF-conditional pos2). Do formula lines maintain their structure at pos3, or do they converge to near-Markovian there? For example: p→sh→qot[pos2]→? at pos3: does qot route to a specific class?
**Description:** For B cont lines ≥4 words, compute (pos2, pos3) bigrams and also (LF, pos1, pos2, pos3) 4-grams. Check whether formula-typed lines (p→sh→qot, y→sh→ch, etc.) have distinctive pos3 routing vs baseline.
**Expected outcome:** p→sh→qot→qok(pos3) enriched (qot→qok bigram exists). y→sh→ch→ok(pos3) enriched (ch→ok is the content-response chain). Near-Markovian lines remain Markovian at pos3.
**Cost estimate:** small — extend exp_401 framework

## H627_archived: A Continuation Line Trigram Inventory
**Status:** archived
**Source:** F405 (B grammar 90.7% near-Markovian, 9.3% formula-typed). Is A's formula-typed fraction larger (due to stronger LF routing rules like qot=1.65× LF vs B=0.51×) or smaller? Key comparison: what are A's strongest formula trigrams vs B's?
**Description:** Parallel to exp_401 but for A dialect. Enumerate all (LF, pos1, pos2) trigrams in A continuation lines. Report formula-typed fraction, top trigrams, and compare to B results.
**Expected outcome:** A formula-typed fraction may be higher than B (A has more LF-routing structure per F392). A y→sh→ch depleted (0.62×) vs B enriched (2.88×) — this inversion should appear clearly in A's formula trigrams. A-specific formula types include sh→sh→? (A sh self-chain) and qot→sh→? (A qot LF routing).
**Cost estimate:** small — parallel to exp_401

## H623_archived: B p-Formula Pos3 Grammar — After p→sh→qot at Positions 0-1-2, What Comes at Position 3?
**Priority:** medium
**Status:** UNANSWERABLE with current methodology (exp_539, 2026-04-11). B lines starting with p-onset: N=38 (p-first) or N=14 (p-last). Triple path p[first]→sh[second]→qot[third]: N=1 case in full B corpus — insufficient for analysis. The original N=222 "B p-LF corpus" likely used different corpus parsing (pre-ZL3b or different section definition). Current parsing gives too few p-formula lines for pos3 analysis. Recommend: check archived exp_413 script and corpus source before revisiting.
**Source:** F396 (B p→sh→qot=2.11×, N=8/51). F398 (B ch-pos1 alternative: p→ch→ot=5.28×). We have the first three positions of B p-formula lines. What comes at pos3 (idx=3)? Does qot at pos2 route to a specific class at pos3?
**Description:** For B continuation lines with p[LF]→sh[pos1]→qot[pos2], extract the pos3 onset (if line has ≥4 words). Compute E for each onset class at pos3. Also: for the full B p-LF corpus (N=222), compute the pos3 onset distribution conditioned on pos2 class.
**Expected outcome:** p→sh→qot→[qok or ch at pos3] — qot at pos2 likely routes to qok or ch continuation (the qok/ch MID grammar). Small N (N=8 for the full p→sh→qot path, but N=222 for all B p-LF lines at pos3).
**Cost estimate:** small

## H622_archived: A p-Formula Lines sh-Bracket — Do A p-LF Lines Have sh at Both pos1 AND LL?
**Priority:** high
**Status:** archived
**Source:** F403 (A p→sh at pos1=3.60×/N=41; A p→sh at LL=3.60×/N=7) — identical E values at pos1 and LL. F392 (A p LF-enriched at 3.53×). This coincidence suggests A p lines may have sh at BOTH pos1 (LF→pos1 rule) and LL (LF→LL rule), forming a "sh-bracket" around the line interior.
**Description:** For A continuation lines with p at LF: (1) count lines where sh at pos1; (2) count lines where sh at LL; (3) count lines where sh at BOTH pos1 AND LL. Compare to expected overlap under independence (P(pos1=sh)×P(LL=sh)×N). Also check the actual lines to see the p→sh→...→sh structure.
**Expected outcome:** A p lines have sh at both pos1 and LL more often than independence would predict (sh-bracket). If true, A p formula = p[LF]→sh[pos1]→[MID content]→sh[LL].
**Cost estimate:** trivial — small N (A p cont lines = 41)

## H620_archived: B p-Formula Complete Structure
**Status:** archived
**Source:** F396 (B p→sh→qot=2.11×); F398 (B p→ch→ot=5.28×); F403 (B p→ch LL=0.47×, p→s LL=2.05×, p→qo LL=1.89×). We have pos1 routing, pos2 routing for sh/ch, and LL routing. Missing: (1) full MID grammar for p-LF lines; (2) typical line lengths; (3) whether p-LF lines are longer or shorter than average.
**Description:** Extract all B continuation lines with p at LF (N≈222). Compute: word count distribution; full onset sequence positional distribution; MID onset composition; how often each "formula type" (p→sh vs p→ch vs p→other) occurs.
**Expected outcome:** p-LF lines are approximately average length. p→sh=35% / p→ch=8% / p→other=57%. MID is qok/sh-dominated (normal B MID). LL is specifically s/qo/k/o enriched (confirmed F403). 
**Cost estimate:** small — targeted line extraction

## H618_archived: B Continuation Line Opening Trigram Inventory — What Are the Top 20 Most Common (LF, pos1, pos2) Triplets?
**Priority:** medium
**Status:** archived
**Source:** F398/F399 (B has five sh-pos1 grammar types; t is near-Markovian; p/y/s/qok have strong formula-type grammar). The five types characterize sh-pos1 lines only. The full space of B line-opening trigrams is unknown — what proportion of lines fall into formula-typed vs Markovian grammar?
**Description:** Enumerate all (LF, pos1, pos2) trigrams in B continuation lines (≥3 words). Report counts and E values for the top 30 most frequent triplets. Characterize the fraction of lines with formula-typed openings vs near-Markovian openings.
**Expected outcome:** Top triplets include d→sh→qok (near-Markovian, d→sh=most common B sh-pos1 context), d→ch→{various}, s→sh→qok, qok→ch→qok. Formula-typed lines (with strong LF-conditional pos2 enrichment) may represent 20-30% of all lines; most lines are near-Markovian.
**Cost estimate:** medium — tabulate all trigrams and compute E values

## H615_archived: B f→pos1
**Status:** archived
**Source:** F392 (f: A=2.69×/B=1.67× LF-enriched in INVARIANT_LF+). F364 ({p,f}→sh vs {k,t}→ch in A at MID; F358 shows A gallows→sh multi-position). exp_393 (B f cont lines: LF=9/42=21% — low, N small). B f is LF-enriched but weakly. Does B f→sh at pos1 like p (p→sh=5.90×)? Or is f's LF concentration weaker and less directed?
**Description:** Extract B and A continuation lines with f at LF. Compute pos1 distribution. Compare f→sh rate to p→sh and to baseline.
**Expected outcome:** f→sh elevated but weaker than p (E=1.5-2.5× vs p's 5.90×). Small N (B f LF=9) makes this directional only.
**Cost estimate:** trivial — N small (B f LF=9, A f LF=9)

## H614_archived: Cross-Section A y-Chain Frequency
**Status:** archived
**Source:** F395 (both A length-4 y-chains in herbal f19 and bio f67r2; A length-3 runs at f44/f67r2/f86v5/f86v5 — suggestive of section clustering). If y-chains are section-specific, that would constrain the mechanism (the scribal practice that generates y-chains is section-associated).
**Description:** For A-dialect, compute y-chain length distribution separately for each section (herbal/pharma/bio/cosmo/text). Compare y-chain frequency (total run count and length≥3 count) per section, normalized by token count.
**Expected outcome:** y-chains (length≥3) concentrated in herbal/bio sections. Text/pharma sections may have near-geometric chain lengths. If true, y-chains are a section-grammar property.
**Cost estimate:** small — extends exp_391 by adding section tracking

## H586_archived: A sh→qot Cross-Onset Coupling (E=1.63×, N=29) — Positional Decomposition
**Priority:** medium
**Status:** open
**Source:** exp_367 8×8 bigram matrix (A-dialect continuation lines): sh→qot E=1.63× (N=29). Mirrors B d→sh (E=2.58× peak at pos1→pos2, exp_371/F373). Is A sh→qot position-general or concentrated at specific position pairs?
**Description:** For A-dialect continuation lines, compute: P(next=qot | prev=sh-onset) vs baseline P(qot) at each position pair (LF→pos1, pos1→pos2, MID_inner, pre_LL→LL). Identify top sh-word → qot-word pairs. Determine if effect is driven by specific sh words (shedy, shey, etc.) or is sh-class-general.
**Expected outcome:** A sh→qot may be position-general (E=1.5-2.0× at all positions) consistent with other A-dialect position-general rules (A d→cth E=1.51-1.76×). Alternatively, it may peak at pre-LL→LL (consistent with A qot LF-enrichment suggesting qot is a "start-of-cluster" word, so sh appearing late in a line forecasts qot at LL/next-line LF).
**Cost estimate:** small — inline positional bigram analysis

## H585_archived: B s→sh Cross-Onset Coupling (E=1.98×, N=75) — Positional Decomposition
**Priority:** medium
**Status:** open
**Source:** exp_367 8×8 bigram matrix (B-dialect continuation lines): s→sh E=1.98× (N=75). B s→ol E=1.78× (N=39) also elevated. Both are the strongest unconfirmed cross-onset couplings remaining after exp_371 (which confirmed B d→sh and A d→cth).
**Description:** For B-dialect continuation lines, compute: P(next=sh | prev=s-onset) at each position pair (LF→pos1, pos1→pos2, MID_inner, pre_LL→LL). Baseline: global P(next=sh-onset). Identify top s-word → sh-word pairs. Also check B s→ol (E=1.78×, N=39) by position. Determine: is s→sh position-general or position-specific?
**Expected outcome:** B s→sh may be LF-driven: s-onset is LF-enriched in B (E~1.5×), and sh-onset appears at pos1 (successor to LF). If s→sh peaks at LF→pos1, this is a B LF-formula coupling. If MID-concentrated, it's a content grammar rule. Also check: are specific s-words (sain, shor, saiin) the drivers, or is it s-class-general?
**Cost estimate:** small — inline positional bigram analysis

## H513_FORMER: Line-Length-Conditional LL Word-Length Filter — Can a Word-Length Cap That Decreases with Line Length Reproduce the VMS Non-am LL_wl Gradient?
**Priority:** RESOLVED — exp_310 (F312) identified that the VMS non-am LL_wl gradient is driven by "other"-suffix (short unrecognized-ending) words becoming more frequent in long lines (22.5%→42.6%). The correct mechanism is word-length conditioning, not suffix-length conditioning. In long lines, VMS LL words are preferentially shorter (nonam_wl 4.426 at n=11-15 vs 5.671 at n=2-4). This is the primary remaining r_ll gap (simulation r_ll=−0.034, VMS=−0.219).
**Status:** open
**Source:** exp_310 (F312): diagnostic reveals "other"-category increase with line length is the VMS mechanism.
**Description:** Implement a word-length filter for LL non-blind words: for lines of length n, set max_ll_len(n) = base_len − slope × max(0, n − n_ref). After generating an LL word (onset+suffix), if len(word) > max_ll_len(n), redraw up to MAX_RETRY times. If all draws exceed max_ll_len, use the shortest generated word. Parameters to sweep: base_len ∈ {7, 8}, slope ∈ {0.2, 0.3, 0.4}, n_ref ∈ {5, 6}. Targets: nonam_delta from +0.006 → at least −0.600 (50% of VMS −1.244); r_ll from −0.034 → at least −0.100 (46% of VMS). Battery constraints: word_len_mean must stay 80-120% of VMS 5.40 (currently 98.1%, LL words are ~16% of all words, so −0.5 chars in LL_wl reduces word_len_mean by ~0.08 chars — safe); ch_ll/ok_ll/qok_ll/d_ll must stay within ±20% (onset selection unaffected by length filter). Alternative: use a VMS-derived short LL word lexicon (draw directly from VMS LL words of length ≤5 for lines n≥10). Diagnostic first: measure VMS LL word length distribution by line length bucket including "other" words (onset types of short LL words).
**Cost estimate:** medium — rejection-sampling mechanism in LL path; diagnostic VMS LL word length bucket analysis
**Prerequisites:** exp_310 (F312: VMS mechanism identified as word-length-conditional); 18-mechanism architecture with cond_mild p_blind

## H441: Erosion Factor Analytical Derivation — Can the Empirical Erosion Factors (B: 0.84, A: 0.61) Be Derived From First Principles of the Modification Operation?
**Priority:** low — theoretical consolidation
**Status:** open
**Source:** F238, F239: A-dialect erosion factor = 0.61 empirically derived; B-dialect = 0.84. Both are edy-rate-dependent: B 19.4% edy → higher protection → 0.84; A 0.45% edy → less protection → 0.61. The relationship has not been derived analytically.
**Description:** Derive: given modification operation (onset-preserving, edy-preserving, fresh fallback for no-middle edy words) and edy_fraction f_edy, what is the expected equilibrium erosion factor? Specifically: a word drawn from buffer is modified with probability mp=0.90; modification preserves onset and edy suffix; non-edy words have full stem modifiable → -am in stem often destroyed; edy words have protected suffix → -am if present in stem still destroys it, but edy words rarely end in -am anyway. Derivation: (a) fraction of buffer words with -am suffix = q (some equilibrium); (b) modification erodes -am by changing one char in stem region; (c) erosion rate per modification = f(-am in modifiable stem region); (d) replenishment rate = fresh word probability (1-cp) + (cp × (1-mp)) unchanged words. Set up fixed-point equation. Compare analytical erosion factor vs empirical (0.84 B, 0.61 A).
**Cost estimate:** low — mathematical derivation, possibly a short script to verify
**Prerequisites:** exp_236, exp_239 (both done — provide both dialect data points)

---

## H031: The f49v Numeral "1-5" Annotation Is by the Same Hand as Other Known Later Annotations (e.g., f116v)
**Priority:** low
**Status:** open — requires manuscript image access (BLOCKED computationally)
**Source:** exp_030_f49v_numerals

---

## H134: The Aiin-Dom Register Corresponds to Specific Early Quires (f1-f16 = Quires 1-3), Suggesting a Scribal or Section Break in Herbal A
**Priority:** medium
**Status:** open — requires quire codicology data (BLOCKED computationally)
**Source:** F089 (exp_082)

---

## H139: The A and B Positional Grammar Models Predict a Consistent Sentence/Phrase Structure (Subject/Verb/Object Analogues)
**Priority:** medium
**Status:** open — high difficulty; requires theoretical framework beyond current structural analysis
**Source:** F090 (exp_083)

