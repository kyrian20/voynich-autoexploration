# Open Questions
# Cryptanalyst — Voynich Manuscript Investigation
# Questions that require human judgment, domain expertise, missing tools, or a dataset not currently available.
# Format: see skills/write_finding.md for the entry template.

---

## Q001: What is the word-initial entropy of actual medieval Latin?
**Raised by:** exp_001_word_initial_entropy
**Date:** 2026-04-09
**Question:** The exp_001 Latin baseline was mistakenly the Douay-Rheims Bible in English (Gutenberg #8300) rather than actual Latin. The "Caesar" file (Gutenberg #10657) was also an English translation. What is the correct word-initial entropy for medieval Latin, and how does Voynich's 3.137 bits compare? Virgil's Aeneid and Caesar's De Bello Gallico in Latin are now available (downloaded 2026-04-09) but the comparison has not been re-run.
**Why this can't be resolved computationally:** It can — the real Latin files exist and the script needs to be re-run pointing at the correct files.
**What it would take to resolve it:** Run exp_001's analysis substituting Virgil/Caesar Latin for the Douay-Rheims file. This is a cleanup task, not a new hypothesis; integrate into exp_002.
