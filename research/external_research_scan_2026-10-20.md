# External Voynich research scan — 2026-10-20

Purpose: record potentially relevant external research discovered through a fresh web scan, distinguish claims from independently verified results, and identify concrete replication opportunities. This is a search snapshot, not a claim that the survey is exhaustive or that each source is peer-reviewed.

## Highest-priority computational leads

### 1. Matthew Dominik — structural morphology with protected holdouts (Zenodo, 2026-10-03)
- Record: https://zenodo.org/records/23113674
- Related earlier release: https://zenodo.org/records/22049207
- The abstract reports a frozen morphology/CORE inventory, held-out combinatorics, alternate-transcription replication, host/right-edge coupling and an explicit failure to recover ordinary lexical meanings.
- Reported coverage figures (98.4314% of positions in a 1,609-line constrained benchmark assigned a functional role) are explicitly a conditional benchmark-maturity measure, not plaintext translation accuracy.
- Why relevant: protected holdouts, frozen rules, alternate-transcription sensitivity and a stopping rule against semantic overreach match the reproducibility standards we want.
- Main risk: the headline percentages depend on the author's benchmark and role taxonomy. They should not be treated as independent confirmation until data, exact rules, split boundaries and code are audited.
- Replication target: choose a small, predeclared subset of surface CORE/host/right-edge claims; reconstruct counts from the cited transcription, freeze the vocabulary on calibration folios, and test exact predictions on untouched folios. Do not attempt to reproduce the English rendering as ground truth.

### 2. Epilectrik — frozen structural model / negative-control programme (GitHub; review dated 2026-09-27)
- Repository: https://github.com/epilectrik/voynich
- The repository describes a Currier-B/H-transcription study with numbered constraints, evidence tiers and a September 2026 adversarial review. It states that some central claims failed when tested against external controls and rival generators.
- Why relevant: its explicit rival-generator and external-control approach may reveal failure modes missing from our current null models.
- Main risk: repository claims are not automatically validated; inspect the strategic review and change log before adopting any conclusion.
- Replication target: extract its final surviving constraints and rejected claims, map each to our existing experiments, and select one untested rival-generator control rather than copy its interpretation.

### 3. Pantani — route-based statistical toolkit with visual review (GitHub)
- Repository: https://github.com/Pantani/voynich
- Describes a reproducible EVA toolkit with route-based analysis, human-in-the-loop visual review and a large pytest suite.
- Why relevant: could provide useful independent implementation patterns, test fixtures and page/folio visualization for checking our own parsing and token-position claims.
- Main risk: the README's reported metrics and hypotheses are project claims, not independent scholarly consensus.
- Replication target: inspect tokenizer and fixture tests first; compare only well-defined normalized outputs. Do not import their proposed operator/template interpretation as a premise.

### 4. VoynichDuctus — image-based computational palaeography (GitHub)
- Repository: https://github.com/silveremartin-dev/VoynichDuctus
- Describes image processing, DINOv2-based glyph clustering, quill-kinematic modelling and information-theoretic diagnostics on manuscript images rather than relying only on EVA transliteration.
- Why relevant: offers a different evidence channel that might test allograph and scribal-variation questions without assuming that EVA categories are visually homogeneous.
- Main risk: sophisticated methods in a README do not establish valid ground truth. Must verify image alignment, training labels, data splits and evaluation against expert-annotated samples.
- Replication target: begin with a narrow feasibility audit—identify image source, licensing, crop/line alignment, and held-out human-labelled glyph sample. Do not launch a broad computer-vision pipeline until those prerequisites are clear.

## Additional hypotheses to track, not treat as established

### 5. E. M. Honeycutt III — operational page-architecture / Paduan medical-computational context
- Latest record: https://zenodo.org/records/23068593 (2026-09-30)
- Proposes that page architecture and operator classes fit an operational medical-reference tradition in a Paduan context; explicitly does not claim decipherment.
- Why relevant: suggests a historical-comparator route, particularly section architecture and functional notation.
- Main risk: a provenance/genre hypothesis is not demonstrated by the manuscript's statistical structure alone. Claims about historical location and genre are inferences; keep them separate from measured corpus facts.
- Replication target: only test concrete, pre-registered page-layout or operator-frequency predictions against a defined, matched comparator corpus. Avoid selecting comparators after seeing which resemble Voynich.

### 6. Torsten Timm — critique of the five-scribe hypothesis (Zenodo, 2026)
- Record: https://zenodo.org/records/19119470
- Argues that common diagnostic glyph criteria for five scribes fail and that apparent scribal categories may partly recapitulate Currier A/B or page-type differences.
- Why relevant: supports controlling for language, section and page function before attributing lexical differences to scribal hand.
- Main risk: competing paleographic interpretation; it requires direct inspection of images and criteria, not transcription-only inference.
- Replication target: use a blinded image sample and compare the stated diagnostic glyphs across pages while controlling for section and Currier labels.

### 7. Christophe Parisel — quantitative Currier distinction (already tracked in EXP-622)
- Record: https://arxiv.org/abs/2604.25979
- Reports a Beta-Binomial mixture with 89% held-out folio-label accuracy and a proposed folio-level switch related to vowels following ch/sh. Already tracked in our EXP-622 note; EXP-622/623 tested a different matched context-specificity estimand and did not reproduce a significant following-vs-preceding interaction.
- Next meaningful comparison is not another near-duplicate ch/sh test: reproduce the paper's exact feature definitions, mixture fitting, fold assignment and baseline, after the tokenizer/Currier-$L$ audit passes.

## Recommended order of work
1. Resolve the already-documented tokenization disagreement in our EXP-602 parser audit. No new lexical or classifier conclusions until the token policy is settled.
2. Audit external code/data and map each candidate claim to what our repository already tests. Keep a source ledger with exact version/date, corpus, split, features, metric and replication status.
3. Prioritize the lowest-cost independent replication: either the exact Parisel folio-level feature model or a narrow Dominik surface-morphology held-out claim. Decide which only after checking available code/data and preventing overlap with existing tests.
4. Treat image-based paleography and historical-provenance work as separate workstreams with their own ground truth; do not mix them into token-level language claims.
5. Preserve negative results and avoid treating two transcriptions of the same manuscript as independent samples.

## Evidence policy
- A paper's abstract/README is a lead, not validation.
- Preprints and self-published repositories must be labelled as such.
- Report the exact evaluation unit (token, line, folio, image crop), split and baseline.
- Do not describe structural regularity as recovered meaning or decipherment.
