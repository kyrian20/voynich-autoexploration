# exp_593 — daiin and IVTFF locator metadata

This is a follow-up to exp_589–592. It tests whether line-initial `daiin` differs across IVTFF locator categories inside Currier A/B and P0, without treating those locators as paragraph-boundary labels.

## Important format clarification
The official IVTFF specification (R. Zandbergen, format issue 2.0.2, 8 July 2025) defines:
- `@`: locus position is unrelated to, or not readily described relative to, the previous item; it is always used for the first item on a page.
- `+`: locus is generally below the previous item.
- `*`: locus is at the start of the line below the previous item at the left margin, while the previous item was not.
- Paragraph boundaries are separate dedicated in-text comments: `<%>` starts a paragraph and `<$>` ends it. Their placement is a transcriber decision.

Therefore these categories are **page/layout locator codes**, not paragraph-opening vs continuation classes. The script does not currently test the dedicated `<%>` / `<$>` markers, because prior corpus cleanup removes them; this should be a separate, carefully validated test.

Official reference: https://voynich.nu/software/ivtt/IVTFF_format.pdf (Table 8 and §6.9).

## Protocol
- Corpus: ZL3b IVTFF, source digest recorded in `results.json`.
- Filters: Currier A/B separately, locus P0, lines with at least two cleaned tokens; locator modifier categories @, +, *, and none.
- Statistics: observed first `daiin`, within-line inventory/length expectation, enrichment, 5,000 fixed-seed Monte Carlo position draws, one-sided upper-tail and lower-tail p-values; Holm correction within each Currier dialect / tail family.
- Minimum stratum size: 50 lines; smaller categories are descriptive/omitted from inference, not declared null.
- No paid API required.

## Interpretation limits
An upper-tail p-value tests initial excess; a lower-tail p-value tests initial deficit. A Monte Carlo p-value at 0.0002 is the resolution floor for 5,000 replicates. These are conditional position statistics, not evidence of word meaning or decipherment.
