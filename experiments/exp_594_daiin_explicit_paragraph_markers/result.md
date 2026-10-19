# exp_594 — Results: explicit IVTFF paragraph-start markers

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257721036  
**Status:** analysis and compile-check succeeded; generated JSON preserved in the repository after a race-condition push conflict was resolved.

## Format basis

The IVTFF specification says `<%>` marks the start of a paragraph at the beginning of a transliterated line, while `<$>` marks its end. It also explicitly says paragraph segmentation is a transcriber decision; different transliterations can therefore mark divisions differently. Source: [IVTFF format specification, §6.9](https://voynich.nu/software/ivtt/IVTFF_format.pdf). citeturn999141view1

## Results

The parser identified 4,105 paragraph-body lines with at least two clean tokens; 728 carried an explicit start marker and 729 an end marker. The counts do not pair one-to-one (the markers are separate, line-local annotations and some paragraph tagging may be missing).

| Currier / group | Lines | `daiin` tokens | First observed | Expected first | Ratio | Lower-tail p (Holm) | Upper-tail p (Holm) |
|---|---:|---:|---:|---:|---:|---:|---:|
| A / explicit `<%>` | 236 | 59 | 1 | 6.993 | 0.143× | 0.0066 (0.0132) | 0.9990 (1.0000) |
| A / no start marker | 1,321 | 441 | 61 | 64.243 | 0.950× | 0.3511 (0.3511) | 0.6989 (1.0000) |
| B / explicit `<%>` | 492 | 29 | 0 | 2.827 | 0.000× | 0.0544 (0.1088) | 1.0000 (1.0000) |
| B / no start marker | 2,056 | 288 | 97 | 32.279 | 3.005× | 1.0000 (1.0000) | 0.0002 (0.0004) |

All tests use 5,000 within-line random-position draws, conditioning expected first counts on the tokens and length of each line. Holm correction is applied separately within each Currier dialect and tail direction.

## Interpretation

- **Currier B:** explicit paragraph-start-marked lines have no first-token `daiin` (0 observed vs 2.83 expected). The lower-tail p=0.0544 becomes 0.1088 after correction, so the apparent deficit does **not** meet the adjusted 0.05 threshold. Lines without the start marker have a strong initial excess (97 vs 32.28 expected; 3.005×; upper-tail adjusted p=0.0004).
- **Currier A:** explicit `<%>` lines have a marked initial deficit (1 vs 6.99 expected; lower-tail adjusted p=0.0132). A lines without the marker show no significant excess or deficit.
- This extends the observed Currier-A/B differences and suggests the B initial excess is concentrated among lines not explicitly annotated as paragraph starts. It does not prove all unmarked lines are continuations, because paragraph annotations may be incomplete and division decisions are transcription-dependent.
- Crucially, the marker is a property of the **transcription's annotation**, not a decoded Voynich punctuation mark. No semantic meaning is inferred for `daiin`.

## Limitations and next step
The test uses one EVA transcription and a conservative tokenizer. Repeat on ZL3a and compare marker coverage before treating this as a stable cross-transcription fact. If annotation conventions differ, compare only loci where the files' paragraph-marker decisions can be reconciled. This is a positional/annotation finding, not a decipherment.
