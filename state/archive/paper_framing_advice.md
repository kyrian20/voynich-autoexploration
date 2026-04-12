# Paper Framing Advice

---

## 1. FRAMING

**Option (b): Substance paper about the dual-constraint result.** The methodology is supporting evidence, not the headline.

Here's why:

**(a) Methodology paper** has a ceiling problem. "We ran an AI agent that did 184 experiments on the Voynich manuscript" is interesting as a story but thin as a contribution. The methodology isn't novel — hypothesis-driven experimentation, simulation-based null testing, and cross-validation are standard. The fact that an agent did them autonomously is cool but doesn't constitute a methodological advance that a methods-focused reviewer would credit. You'd be competing with papers that introduce new frameworks, not papers that apply existing ones at scale. And the honest version of the methods claim is "an LLM rediscovered known results for 100 experiments, then found some novel things in the next 80" — which undercuts the autonomy narrative.

**(c) Hybrid** dilutes both contributions. Reviewers in DH/CL venues care about the Voynich result. Reviewers in AI venues care about the agent methodology. Trying to serve both audiences means neither gets enough depth. You'd spend 4 pages on agent architecture that the Voynich audience doesn't care about, and 4 pages on EVA transcription conventions that the AI audience doesn't care about.

**(b) Substance paper** is where the real contribution lives. The dual-constraint result — Voynichese requires both position-sensitivity AND sequential word-class memory, and no tested mechanism produces both — is a genuine advance in Voynich studies. It's specific, falsifiable, and engages directly with the two most serious computational proposals in the field (Greshko 2025, Timm & Schinner 2020). The convergent-failure argument (two completely different position-blind mechanisms fail on the same four metrics, confirmed across 1,900 simulations and a 75-point parameter sweep) is methodologically rigorous in a way that prior Voynich statistical work often isn't.

The agent methodology belongs in a "Methods" section and maybe a paragraph in the discussion ("this work was conducted by an autonomous research agent, demonstrating the viability of..."). It adds novelty and interest without needing to carry the paper's central claim.

One caveat: if you want to write a paper primarily about AI-assisted research methodology and just need a demonstration domain, that's a different paper — and the Voynich work is a good demo case for it. But that paper would go to an AI venue and the Voynich content would be abbreviated. Decide which paper you're writing.

---

## 2. VENUE RANKING

**#1: Cryptologia**

The paper's primary interlocutors are Greshko (2025, Naibbe cipher) and Timm & Schinner (2020, self-citation). Both published in Cryptologia. The dual-constraint result directly extends Greshko's work — he showed a cipher CAN reproduce vocabulary statistics; you show it CANNOT reproduce positional grammar and self-succession simultaneously. This is a natural response paper in the same venue. Cryptologia reviewers will understand EVA notation, substitution ciphers, and the Voynich literature without lengthy preamble. The journal has a history of rigorous Voynich papers (not just crank submissions). Turnaround is reasonable.

Risks: Cryptologia is niche (impact factor ~0.5). If you want broader visibility, pair this with an arXiv preprint.

**#2: Digital Scholarship in the Humanities (DSH)**

DSH publishes computational approaches to historical texts and manuscripts. The dual-constraint result, framed as "computational discrimination among competing theories of an undeciphered manuscript," fits their scope. The methodology (simulation-based null testing, cross-validation, multiple-testing correction) is more rigorous than most DSH computational papers, which would be a strength. The agent angle could be a secondary contribution that DSH reviewers would find novel.

Risks: DSH reviewers may not have deep Voynich background. You'd need more context setting. Also, DSH review cycles can be long (6-12 months).

**#3: arXiv preprint (cs.CL or cs.CY) with later venue decision**

Put it on arXiv immediately. The Voynich community (voynich.ninja forum, independent researchers, Greshko himself) will read it and provide informal review. This gets the result into circulation fast, establishes priority on the dual-constraint finding, and lets you gauge reception before committing to a journal. You can then submit to Cryptologia or DSH with revisions informed by community feedback.

Risks: None, really. arXiv preprints are standard practice. The only cost is that some journals have preprint policies (Cryptologia allows them; DSH allows them).

**Not recommended:**
- ACL workshops (LChange, LaTeCH-CLfL): Too short for this work (8-page limit). The convergent-failure argument needs space. Also, ACL reviewers would want NLP novelty, not historical cryptanalysis.
- JOCCH: Possible but more focused on cultural heritage computing infrastructure than on analytical results.
- NeurIPS workshops: Would force the AI-methodology framing, which I've argued against.

---

## 3. STRONGEST SINGLE CLAIM

> Simulation-based null testing of three competing generative models for the Voynich Manuscript — the Greshko (2025) Naibbe homophonic cipher, the Timm & Schinner (2020) self-citation algorithm, and a position-independent template filler — reveals that Voynichese exhibits two jointly necessary structural properties, position-sensitive onset-class grammar and sequential word-class memory, that no tested model can reproduce simultaneously, constraining viable generation hypotheses to mechanisms that are both position-aware and sequentially structured.

This sentence:
- Names the interlocutors (Greshko, Timm & Schinner) — shows it engages with real literature
- Specifies what was tested (three models, by name) — no overclaiming
- States the finding precisely (two properties, jointly necessary) — falsifiable
- States the constraint (position-aware + sequentially structured) — actionable
- Doesn't claim decipherment, source language, or "grammar" as a vague label
- Is defensible: every clause maps to a specific experiment with specific numbers

---

## 4. BIGGEST RISK TO RECEPTION

**The hostile reviewer will say: "You tested three toy models and declared victory for the hypothesis that wasn't tested."**

This is the most dangerous critique because it's partially correct. The paper tests Naibbe (one specific cipher), Timm (one specific algorithm, with parameter sweep), and a position-independent template (one specific null model). It then concludes that "structured grammar" survives by elimination. A careful reviewer will note:

1. The Naibbe cipher is one of thousands of possible ciphers. Ruling out one cipher is not ruling out ciphers.
2. The position-sensitive cipher (exp_177) gets to 84% of VMS on the key metric. With a different source language or higher detection probability, it might close the gap entirely.
3. "Structured grammar" was never directly tested — it's the complement of three negatives, not a positive result.
4. The template model tested is a straw man (simple slot-filler). Zattera's 12-slot model or Smith's syllable-ranking model are more sophisticated and untested.

**Preemptive defenses:**

- Frame the contribution as "constraining the hypothesis space" rather than "confirming a theory." The paper narrows; it doesn't solve.
- Emphasize the convergent-failure argument: two completely different position-blind mechanisms fail on the same metrics. This is evidence about the mechanism CLASS (position-blind), not about specific models.
- Report the position-sensitive cipher result (exp_177) prominently and honestly. Show that 84% of -am LL is achieved but 0% of self-succession is achieved. Let the reader see the dual-constraint for themselves.
- Include a "Limitations and Untested Hypotheses" section that explicitly lists: running-key ciphers, transposition ciphers, book ciphers, nomenclators, position-sensitive ciphers of non-Latin languages, structured glossolalia, hybrid models. Don't hide the gaps.
- The strongest preemption: run the hybrid cipher-copy simulation before submission. If you can show that even a purpose-built hybrid (position-sensitive cipher + Timm copy component) can't satisfy both constraints simultaneously, the elimination argument becomes much harder to attack. If it CAN satisfy them, that's an even more interesting result — you've identified a specific mechanism class.

**Secondary risk**: A Voynich specialist reviewer who knows the rediscovery problem. The characterization phase (exp_001-165) substantially rediscovered known results (Stolfi slot grammar, Currier A/B, positional preferences). If the paper presents these as novel, a reviewer who knows the field will be unimpressed. Defense: cite prior work aggressively (Currier 1976, Stolfi 2000, Smith 2015, Zattera 2022, Timm & Schinner 2020, Greshko 2025) and be explicit about which results are confirmatory vs. novel. The novel contribution is the dual-constraint discrimination, not the characterization.

---

## 5. WHAT TO LEAVE OUT

**Cut the characterization phase almost entirely.** Experiments 1-165 are the agent's learning curve. Most rediscover known results. The paper should reference them as "175 characterization experiments establishing the analysis pipeline (see supplementary materials)" and move on. Don't present F001-F175 individually. Don't walk through the morphological system discovery. Don't describe the suffix paradigm in detail. All of this is in Stolfi (2000), Zattera (2022), and others. Cite them and move on.

**Cut the A-dialect Naibbe analysis (exp_178).** It's exploratory (B-dialect cipher tested against A-dialect targets), acknowledged as such, and adds little beyond what exp_170 already shows. It's a completeness exercise, not a contribution.

**Cut the MI analysis beyond lag 1.** The lag-1 finding (VMS above Timm, shuffle destroys 63%) is clean. The lags 2-7 finding (VMS below Timm) is interesting but secondary — the Timm falsification already rests on the parameter sweep and adj_rate/ss_mean trade-off. The lags 10-12 retraction is a distraction in a paper (it shows the agent made and corrected an error, which is fine in an internal document but awkward in a publication). Report lag-1 MI as a secondary confirmation. Drop the rest.

**Cut the cross-validation details.** Report it as: "Core findings replicate on 80/20 random holdout and leave-one-section-out splits (18/19 A-dialect, 11-15/19 B-dialect; see supplementary materials)." The split-by-split tables are important for the internal record but would consume a page of the paper for a finding that's essentially "yes, these are real patterns."

**Cut any discussion of what Voynichese "means."** The paper cannot determine whether VMS encodes natural language, is a constructed language, or is meaningless structured text. Don't speculate. End at the structural constraint and stop.

**Include:**
- The dual-constraint result (position-sensitivity + sequential memory) as the main finding
- The convergent-failure argument (Naibbe + Timm + parameter sweep → position-blind class ruled out)
- The position-sensitive cipher result (exp_177) showing partial reproduction and the self-succession asymmetry
- The slot-grammar residual analysis (exp_174) showing templates are insufficient
- Bonferroni/BH-FDR correction at m=175 for the core metrics
- Enough methodological detail for reproducibility (all code is already in experiments/)
- A brief note on the autonomous agent methodology in the Methods section
- A supplementary materials appendix (or GitHub repo) with the full 184 experiments

The paper should be 8,000-10,000 words for Cryptologia or DSH. The temptation will be to make it 15,000 because there's so much material. Resist. The dual-constraint result, the convergent failure, and the position-sensitive partial reproduction are three tightly connected findings that tell one story. Everything else is context or supplementary.

---

*Framing advice completed 2026-04-10.*
