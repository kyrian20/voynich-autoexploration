# External knowledge acquisition log — 2026-10-20

Purpose: convert external Voynich research into an auditable knowledge base. This is a methods synthesis, not a claim that any external result has been independently reproduced by this repository.

## Sources reviewed

### A. Seeton / Voynich-public
URL: https://github.com/seeton/Voynich-public
The project reports an executable multiscale surface model, while explicitly stating it has not decoded meaning and has not distinguished the competing broad interpretations. It reports a strong physical-line boundary, predictable high-consensus spaces, transfer of a first-order morphology-transition kernel across domains and Currier A/B, and remaining failure of a generative model on long-range token concentration. Its held-out type-frequency result is explicitly limited and fails its registered occurrence-coverage gate.
Transferable lesson: keep descriptive prediction separate from semantics; retain failed gates and negative results; test joint distributions, not only marginal token frequencies. These are the authors' reported results and require independent reproduction.

### B. Voynich Studies — A Workshop Cipher
URL: https://voynich.site/paper-1-mechanism?lang=en
The page reports a generative mechanism study using ZL3b-n and robustness checks against Takahashi IT2a-n, fixed-seed scripts, natural-language controls, and target statistics including token counts, entropy, word length, repetition and boundary mutual information.
Transferable lesson: define target statistics before model fitting; compare natural-text controls and rival mechanisms; use a second transcription as a robustness check; map every reported number to a script. Reproducing statistics does not identify the historical mechanism.

### C. Frank Masciopinto — voynich-manuscript-decipher
URL: https://github.com/Frank-Masciopinto/voynich-manuscript-decipher/
The repository documents analyses of character statistics, Currier A/B, scribal hand, section effects, word structure, control corpora and cipher/generator families. It warns that statistics are not decipherment and that the manuscript remains undeciphered.
Transferable lesson: include scribal hand and section as potential confounds; compare slot/affix models with simpler within-word bigrams and controls; separate proxy image metrics from evidence about written units.

### D. VoynichStats — Temkin
URL: https://github.com/mjtemkin/VoynichStats
The repository reports tests of immediate repetition and word-class ordering asymmetry with bootstrap and frequency-matched controls. Its alphabet/corpus differs from EVA ZL, so raw counts are not directly comparable.
Transferable lesson: port hypotheses and statistical designs, not raw counts. Match tokenization, alphabet and inclusion rules before comparing effect sizes.

### E. ZL3b-IVTFF and source verification
URLs: https://www.voynich.nu/data/ZL3b-n.txt ; https://github.com/Aspect-Research/voynich-autoexploration/blob/master/data/transcriptions/README.md ; https://github.com/noah-chelednik/voynich-data/blob/main/reports/source_verification_report.md
ZL3b uses IVTFF folio metadata and locus-coded lines; Currier language and hand labels are metadata in folio headers. Locus codes distinguish body text, paragraph endings and labels. An independent source verification report gives SHA-256 bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc.
Transferable lesson: parse metadata fields rather than assuming fixed positions; stratify body text vs labels; preserve uncertainty and locus information; record exact source hash. Do not redistribute transcription files unless source terms permit it.

## Implications for our pipeline

1. EXP-593 uses a simple alphabetic-token regex after stripping IVTFF tags and uncertain spans. This is a first pass, but can lose distinctions, collapse locus types and diverge from standard tokenization.
2. Check Currier class extraction against the actual metadata field (including $L=). A high unknown-class rate makes A/B claims unreliable.
3. EXP-593 shuffles tokens within each line. This preserves each line's token multiset and length but destroys order. Report the randomization unit and compare alternative nulls only as separately preregistered tests.
4. For family-wise correction, compare each observed statistic with the same per-permutation maximum statistic over the prespecified family. Check identical statistic definitions and report Monte Carlo uncertainty and minimum attainable p-value.
5. Counts from different alphabets/corpora are not directly comparable. Compare effect sizes only under matched tokenization and scope.
6. Positional preference alone does not imply meaning. Structural claims require held-out-folio prediction and comparisons with natural-language, cipher and synthetic-generator controls.

## Proposed reproducible tasks (do not allocate IDs until register audit completes)

- Audit A: validate header parsing and Currier A/B coverage; output metadata tag counts.
- Audit B: compare line/locus/token counts with a trusted IVTFF parser and published totals; record differences.
- Audit C: implement independent tokenization and compare EXP-593 counts by folio and locus.
- Replication D: reproduce one preregistered immediate-repetition statistic from Temkin, documenting alphabet and corpus mismatch.
- Replication E: build a fixed target-statistic suite inspired by Voynich Studies: token count, character/glyph entropy, word length, adjacent repetition, Zipf slope and boundary mutual information; compare ZL3b, another transcription and controls.
- Validation F: held-out-folio test with splits fixed before feature selection; report effect sizes, uncertainty and negative outcomes.

## Status
Sources reviewed at public documentation/README level on 2026-10-20. This file records knowledge acquired from external documentation, not full execution of every project's source code. No decipherment claim is made.
