# Open Questions
# Cryptanalyst — Voynich Manuscript Investigation
# Questions that require human judgment, domain expertise, missing tools, or a dataset not currently available.
# Format: see skills/write_finding.md for the entry template.

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
