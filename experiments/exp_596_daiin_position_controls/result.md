# exp_596 — Results: daiin versus common-word positional controls

**Execution date:** 2026-10-19  
**Workflow:** https://github.com/kyrian20/voynich-autoexploration/actions/runs/39258230375  
**Machine output:** `results.json`

## Question
Is `daiin`'s Currier-B initial-position enrichment distinct from other common EVA strings, or does it belong to a broader word-position pattern?

## Primary Currier-B P0 results

| Token | Count in B/P0 lines | First observed | First expected | Enrichment | Holm-adjusted upper-tail p |
|---|---:|---:|---:|---:|---:|
| `daiin` | 298 | 89 | 31.529 | 2.823× | 0.0012 |
| `aiin` | 359 | 1 | 34.581 | 0.029× | 1.0000 upper; lower-tail adjusted p=0.0012 |
| `chedy` | 479 | 6 | 49.337 | 0.122× | 1.0000 upper; lower-tail adjusted p=0.0012 |
| `dain` | 107 | 34 | 10.714 | 3.173× | 0.0012 |
| `saiin` | 82 | 46 | 9.158 | 5.023× | 0.0012 |
| `qokaiin` | 240 | 25 | 26.846 | 0.931× | 1.0000 |

The primary positive test family contains six predeclared tokens and uses 5,000 within-line random-position draws; Holm correction is applied across those six tests in each transcription/dialect. The p=0.0002 nominal values for the three enriched tokens are at the 5,000-draw Monte Carlo resolution floor; adjusted p=0.0012 is based on that conservative floor.

## Replication in ZL3a

The direction and effect sizes are essentially identical in ZL3a:

| Token | ZL3b enrichment | ZL3a enrichment | First observed in each version |
|---|---:|---:|---:|
| `daiin` | 2.823× | 2.813× | 89 / 89 |
| `dain` | 3.173× | 3.173× | 34 / 34 |
| `saiin` | 5.023× | 5.023× | 46 / 46 |
| `aiin` | 0.029× | 0.029× | 1 / 1 |
| `chedy` | 0.122× | 0.122× | 6 / 6 |
| `qokaiin` | 0.931× | 0.931× | 25 / 25 |

## Currier-A comparison

In A/P0, `daiin` is below its conditional expectation (60 observed vs 69.75 expected in ZL3b; enrichment 0.860×, adjusted upper-tail p=1.00). `dain`, `saiin`, and `qokaiin` show no adjusted significant initial excess. `aiin` has a striking deficit (1 observed vs about 10.09 expected, adjusted lower-tail p=0.0036 in ZL3b and 0.0024 in ZL3a), though this control's extreme positional behavior should be interpreted only as a transcriptional distribution fact. `chedy` is too rare in A/P0 for useful inference (two tokens).

## Interpretation

**The Currier-B effect is not unique to `daiin`.** `dain` and especially `saiin` show even stronger line-initial enrichment in the same null model, while `aiin` and `chedy` are strongly depleted. `qokaiin` is close to its expected first-position count. This is consistent with a heterogeneous positional distribution among frequent EVA tokens rather than one uniform behavior for all common words. It is not evidence that these forms share a meaning or grammatical role; no such claim is made.

In A/P0, `daiin` does not show an initial excess. The Currier A/B distinction from exp_589–595 therefore remains important. Results replicate almost exactly across ZL3a and ZL3b, which share the same locus counts and nearly the same tokens but are distinct transcription files.

## Limitations
- The test conditions on each line's word inventory and length, but not folio, section, paragraph marker, or neighboring-word context.
- The controls were predeclared in the existing exp_589 script; no post-hoc control substitution was made.
- Tokens are literal EVA strings, not confirmed natural-language words.
- These are positional statistics, not a decipherment and not evidence for a particular meaning of `daiin`.

## Next research step
Test neighboring-word context around line-initial `daiin`, `dain`, and `saiin` in Currier B P0: compare their next-token distributions with frequency-matched random starts and report all context classes, including nulls. This asks whether the onset-enriched forms behave similarly after the first token, without assigning semantics.
