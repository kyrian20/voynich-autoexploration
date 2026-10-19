# exp_600 — IVTFF parser conformance audit

## Question
Do the transcription files' page headers and locus identifiers parse consistently under a fresh, independent structural parser, and are there unresolved constructs that could affect previous line-position results?

## Inputs
- ZL3b primary transcription
- ZL3a version-comparison transcription
- IT2a secondary transcription, when present

Each source's byte count and SHA-256 are recorded in results.json.

## Method
The script independently identifies page headers, locus rows, page/locus agreement, locus numbering, slot-marker/type fields, duplicate identifiers, empty bodies, slash-continuation lines, and unparsed angle-bracket constructs. It does not reuse the exp_597 parser implementation.

## Interpretation rule
Any unparsed or unusual construct is a review queue, not automatically an invalid record. Compare findings with René Zandbergen's official IVTFF format documentation before changing the canonical parser. This is a parser/provenance audit, not a new lexical hypothesis and not a decipherment attempt.

## Official reference
René Zandbergen, *IVTFF — Intermediate Voynich MS Transliteration File Format*, version 2.0.2 (8 July 2025): https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
