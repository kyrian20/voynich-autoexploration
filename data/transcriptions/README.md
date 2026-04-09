# Voynich Transcription Manifest

All transcriptions are in IVTFF (Intermediate Voynich Transliteration File Format) unless noted otherwise. IVTFF lines beginning with `#` are comments; lines beginning with `<fNr>` or `<fNv>` contain folio metadata; lines beginning with `<fN.line, locus>` contain text.

---

## eva_zl3b.txt
**Source:** https://www.voynich.nu/data/ZL3b-n.txt
**System:** EVA (Extensible Voynich Alphabet)
**Authors:** René Zandbergen and Gabriel Landini, updated from EVMT project
**Version:** 3b, dated 13/05/2025
**Format:** IVTFF Eva- 2.0
**Size:** 8510 lines, ~412 KB
**Coverage:** Full manuscript
**Notes:**
- Preferred primary transcription for experiments. Most up-to-date EVA transliteration.
- Includes Currier language (A/B) and hand labels per folio in the folio header line (`$L=` field).
- Locus codes distinguish paragraph body (`P0`), paragraph end (`Pt`), labels (`La`), etc. — useful for H009 (label vs. body text entropy comparison).
- Uncertain characters encoded with `[a:b]` (alternatives) and `{xx}` (uncertain reading).
- Non-Voynich text (e.g., Jacobus de Tepenecz signature on f1r) is annotated with `<!...>`.
- Preprocessing needed before analysis: strip comment lines, metadata headers, and locus markers; handle uncertainty encodings.

## eva_it2a.txt
**Source:** https://www.voynich.nu/data/IT2a-n.txt
**System:** EVA (Extensible Voynich Alphabet)
**Authors:** Unknown (IT = Interlinear Text)
**Version:** 2a
**Format:** IVTFF
**Size:** 5444 lines, ~342 KB
**Coverage:** Partial or interlinear (check header for scope)
**Notes:**
- Secondary EVA transcription. Use ZL3b as primary; consult IT2a when checking uncertain readings.

## v101_claston.txt
**Source:** https://www.voynich.nu/data/voyn_101.txt
**System:** v101 (Voynich 101)
**Authors:** Glen Claston
**Format:** IVTFF-compatible
**Size:** 4485 lines, ~249 KB
**Coverage:** Full manuscript
**Notes:**
- Finer-grained than EVA — distinguishes glyph variants that EVA merges. Useful when gallows character variants are relevant (H008).
- Not directly comparable to EVA without a mapping table. Use for confirmation of EVA-based findings, not as primary corpus.

---

## Preprocessing Notes

To extract clean word sequences from ZL3b for analysis:
1. Remove lines starting with `#`
2. Remove folio header lines starting with `<f` followed by metadata only
3. From text lines, extract the text field after the locus code and whitespace
4. Split on `.` (word separator in EVA) and spaces
5. Strip uncertainty markers: remove `[...:...]` alternatives (keep first option or drop), strip `{...}`, remove `@NNN` glyph codes and `%`, `$` paragraph markers
6. Filter out empty tokens

A preprocessing script is at: `experiments/exp_000_corpus_preprocess/script.py` (to be created before first experiment).
