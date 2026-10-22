# IVTFF tokenization policy and fixture plan — 20 October 2026

Status: **specification-grounded proposal; not yet a completed parser-conformance result**.

## Authoritative reference

René Zandbergen, *IVTFF – Intermediate Voynich MS Transliteration File Format*, issue 2.0.2 (8 July 2025): https://voynich.nu/software/ivtt/IVTFF_format.pdf

Relevant sections:
- §6.3 and Table 6 (PDF pp. 19–20): page variables. $L = A/B means Currier language; $Q means quire; $I means illustration type. Never derive Currier A/B from $Q or $I.
- §6.4 and Table 9 (PDF pp. 20–22): locus identifiers, locator codes and locus types. Generic type P denotes linear paragraph text; L labels, C circumference text and R radial text are distinct categories.
- §6.6 and Table 10 (PDF pp. 23–24): transliterated-text special characters.
- §6.7–6.9 (PDF pp. 24–26): word spaces, text tags and paragraph markers.
- §6.11 (PDF pp. 26–27): minimum format conformance.

## Normative facts relevant to our disagreement

1. A period marks an apparent word space; a comma marks an uncertain apparent word space. They are distinct signals. A tokenization benchmark must state whether both split tokens and report sensitivity to that choice.
2. Square brackets mark an uncertain reading. Alternatives are separated by colons, and the first option is the most likely. The whole bracket payload is not automatically one ordinary word. Preserve the raw form and make downstream handling explicit.
3. Braces represent a ligature of Voynichese characters. They are not interchangeable with arbitrary brace-delimited commentary. Keep raw annotations and document how character-level and word-level views handle them.
4. Inline comments have different meanings: <!…> is a free textual comment; <%> paragraph start; <$> paragraph end; <-> and <~> indicate drawing interruptions and imply a word space; <@X=y> sets a text tag.
5. A slash at the start/end of a line is a continuation marker, not a Voynichese character. Continuation lines require explicit handling.
6. A full comment line starts with #. Locus identifiers and page headers are structural metadata, not text tokens.

## Audit update — 20 October 2026

A concrete implementation defect was found in the independent stateful parser: it searched for `?>` instead of the IVTFF `>` terminator for `<!…>` free-text comments. Protocol v2 fixes that defect and preserves the protocol-v1 JSON in the archive. The new run reduces token-list disagreements to 792 for ZL3b and 805 for ZL3a, but does not resolve them. In particular, uncertain alternatives embedded within a word (for example `cho[?:ch]os`) need a documented primary and sensitivity policy. Until fixtures cover these cases and both implementations have been adjudicated against IVTFF 2.0.2, token-sensitive analyses remain blocked.

## Latest parser audit result — protocol v7

The current cross-implementation audit is `experiments/exp_602_independent_ivtff_parser_audit/results_v7.json` (protocol v6 also had zero disagreements). After fixing the comment terminator, splicing bracket alternatives inline, applying brace/@number normalization inside the chosen alternative, and allowing an empty first alternative, both parsers agree on all token lists in the two audited sources:
- ZL3b: 5,385 common records; zero field disagreements.
- ZL3a: 5,389 common records; zero field disagreements.

The earlier counts (1,466/1,472 in v1; 792/805 in v2; 36/37 in v3/v4; 3/3 in v5) are historical snapshots and remain preserved. Zero disagreements means the two implementations agree under this normalization contract; it is not by itself certification against every clause of IVTFF 2.0.2. Complete the full fixture matrix before using this parser for confirmatory prediction.

## Proposed normalization contract

Every parser should produce two layers, not one destructive token list:

- **Raw layer:** exact source line, locus ID, page header/metadata, raw transliteration payload, parser warnings, and source checksum.
- **Analysis layer:** ordered units with offsets back to the raw payload, plus explicit flags for uncertain reading, uncertain space, ligature, inline comment, paragraph marker, and continuation.

For each statistical study, declare one uncertainty policy before inspecting results:
- **primary:** use the first alternative in a bracketed uncertain reading;
- **exclude_uncertain:** omit uncertain spans from the analysis;
- **sensitivity:** report both and compare.

Do not silently choose a policy based on which result looks better. If a case cannot be interpreted under the specification, return an unresolved diagnostic instead of inventing a token.

## Minimal fixture suite to implement

| Fixture | Input feature | Expected assertion |
|---|---|---|
| F01 | fachys.ykal | Period creates two analysis units under the declared baseline |
| F02 | or,y | Comma is preserved as an uncertain-space flag; sensitivity policy is explicit |
| F03 | [x:y] | Alternatives split on colon; primary alternative is x; raw payload remains intact |
| F04 | {...} | Ligature span is marked and preserved, not treated as an arbitrary comment |
| F05 | foo<!note>.bar | Inline comment is removed from analysis units without merging foo and bar across the explicit period |
| F06 | foo<->bar and foo<~>bar | Drawing interruption contributes a word boundary |
| F07 | <%>foo...<$> | Paragraph markers are structural, not tokens |
| F08 | Continuation line with / at end and / at start | Markers are removed and joined payload remains traceable |
| F09 | Header with conflicting $Q=A and $L=B | Currier class is B, exclusively from $L |
| F10 | $Q=A without $L | Currier class is unknown, not A |
| F11 | Malformed/unclosed [ or { | Unresolved diagnostic; no silent repair |

The examples are fixture specifications, not claims that these exact strings occur in the manuscript.

## Acceptance gate

- Each fixture is executable and has a hand-reviewed expected output.
- Each expected behavior cites the relevant IVTFF section.
- Both current parser implementations are run against the same fixtures.
- Differences are reported by class and with raw examples before changing production results.
- Re-run ZL3b and ZL3a comparisons only after policy adjudication; preserve the old 1,466 / 1,472 disagreement report as historical evidence.
- ZL3b and IT2a are alternative transcriptions of one manuscript, not independent manuscript samples.

## Current status

CI now checks transcription files, Python syntax, regression tests for $L metadata semantics, and the corpus-level Currier metadata audit. **This does not yet resolve the token-level parser disagreement.** The next code change should implement F01–F11 in a dedicated tokenizer test suite before any Currier A/B prediction experiment is run.

## Auditoría adicional de pérdida de información — 2026-10-22

La lectura conjunta de la política declarada y las funciones actuales `tokens_regex` / `tokens_scanner` identifica una limitación concreta que debe resolverse antes de considerar cerrada la conformidad:

- Ambas implementaciones eliminan el contenido delimitado por llaves de la secuencia de tokens. La expresión regular sustituye `{…}` por espacio; el escáner vacía la palabra y salta hasta `}`.
- Sin embargo, la especificación IVTFF 2.0.2 §6.6 describe las llaves como una ligadura de caracteres Voynichese, no como comentario genérico. Por tanto, la eliminación puede perder información de grafemas y alterar límites de palabras. El hecho de que ambos parsers coincidan no detecta este sesgo compartido.
- La prueba actual de regresión solo demuestra que ambas implementaciones producen la misma salida para ejemplos con llaves; no valida que esa salida conserve correctamente la lectura.

**Decisión:** no cambiar silenciosamente el normalizador de producción ni regenerar resultados anteriores. Mantener bloqueados los análisis de tokenización que puedan verse afectados por spans con llaves hasta crear fixtures adjudicadas contra §6.6 y una política de sensibilidad explícita: conservar el span bruto y offsets, evaluar por separado una vista que preserve la ligadura y la política histórica que la excluye, e informar cuántas líneas/tokens/resultados cambian. El resultado de cero discrepancias de EXP-602 v7 se debe describir solo como acuerdo entre implementaciones bajo una política compartida de pérdida de llaves.

Esta observación no demuestra que ningún resultado anterior sea falso; delimita una fuente de incertidumbre de tokenización aún no evaluada.

