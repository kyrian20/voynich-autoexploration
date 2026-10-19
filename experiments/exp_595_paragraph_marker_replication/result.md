# exp_595 — Results: explicit paragraph-marker replication

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39257978767  
**Machine output:** `results.json`

## Question
Does the exp_594 paragraph-marker pattern replicate across the two checked-in EVA transcription versions?

## Marker coverage
For both ZL3b and ZL3a, the parser found exactly 4,105 eligible P-locus lines, 728 explicit paragraph-start markers, and 729 paragraph-end markers. The Currier breakdown is also identical: A has 236 explicitly start-marked lines and 1,321 without a start marker; B has 492 start-marked lines and 2,056 without one. The source files have distinct SHA-256 hashes recorded in the JSON; they are not byte-identical files.

## Results by transcription

| Currier / category | ZL3b lines | ZL3b initial ratio | ZL3b Holm p | ZL3a lines | ZL3a initial ratio | ZL3a Holm p |
|---|---:|---:|---:|---:|---:|---:|
| A / explicit `<%>` | 236 | 0.143× | lower tail 0.0124 | 236 | 0.143× | lower tail 0.0076 |
| A / no start marker | 1,321 | 0.950× | no significant deviation | 1,321 | 0.949× | no significant deviation |
| B / explicit `<%>` | 492 | 0.000× | lower tail 0.0976 | 492 | 0.000× | lower tail 0.0984 |
| B / no start marker | 2,056 | 3.005× | upper tail 0.0004 | 2,056 | 2.995× | upper tail 0.0004 |

Expected first-token count in ZL3b/ZL3a is identical for the explicitly marked groups: A 6.993, B 2.827. For unmarked rows it differs slightly between versions: A 64.243/64.279 and B 32.279/32.383.

## Conclusion

**Replicated, with the annotation caveat retained.** In both versions, Currier-A lines explicitly marked as paragraph starts have a deficit of initial `daiin` (1 observed vs 6.993 expected; Holm-adjusted lower-tail p=0.0124 in ZL3b and 0.0076 in ZL3a). Currier-B explicitly marked starts have 0 observed vs 2.827 expected, but do not meet the adjusted threshold (p=0.0976 and 0.0984). In Currier B, lines without a start marker show a robust initial excess of about 3× (97 observed vs roughly 32.3 expected; adjusted upper-tail p=0.0004 in both versions).

The ratios for the key B/no-marker group differ by only 0.00972 (3.00510× vs 2.99538×). That is a close replication under this same operational parser.

## What this does and does not mean
The finding concerns explicit paragraph annotation in these transcriptions. The IVTFF spec says `<%>` marks paragraph start and `<$>` marks paragraph end, but also that paragraph segmentation is the transcriber's decision; alternate transcriptions can differ. See [IVTFF specification §6.9](https://voynich.nu/software/ivtt/IVTFF_format.pdf). Absence of `<%>` is therefore called “no start marker”, not definitively “continuation”. These positional effects do not reveal the meaning of `daiin` and do not constitute a decipherment.

## Next test
Compare `daiin` with predeclared high-frequency controls (`aiin`, `chedy`, `dain`, `saiin`, `qokaiin`) in the same Currier P0 line-position null, adjusting for multiple comparisons. This tests whether the effect is especially strong for `daiin` or part of a broader positional pattern of common tokens.
