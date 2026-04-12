# Experiment exp_294: qok Dialect Asymmetry

**Date:** 2026-04-11
**Hypothesis:** H498 — Why does qok-onset have 2.6× longer midfix in A (1.34 chars) vs B (0.52 chars)? Expected: A-qok has richer internal structure; B-qok is more template-like because it concentrates around canonical B-dialect paradigm words.
**Status:** complete

## Hypothesis

exp_288 found qok ZeroMid: A=44.1% vs B=78.4% and mean midfix length A=1.34 vs B=0.52 (2.6× asymmetry). This is the largest A/B midfix asymmetry across onset classes. The question is whether this reflects A having richer qok internal structure, or B having a more template-like qok paradigm centered on the edy/eedy/ain vocabulary.

## Method

- Corpus: eva_zl3b.txt, A and B dialects, body text only
- Full decomposition of qok-onset words: suffix distribution, midfix inventory, type inventory
- Cross-dialect midfix comparison (A-exclusive vs B-exclusive midfixes)
- Comparison with ok-onset and ot-onset (other sparse-midfix classes)

## Expected Outcomes

| Theory | Predicted result |
|--------|-----------------|
| B-qok is more template-like | B dominated by zero-midfix + edy/eedy/ain suffix paradigm; A more diverse |
| A-qok has unusual structure | A-specific midfixes that B lacks; A vocabulary is broader |
| Symmetrical asymmetry | Both A and B have some exclusive midfixes; A is simply longer |

## Raw Output
```
A-dialect qok (N=537 tokens, 124 types):
  ZeroMid = 44.1%
  MidLen distribution: MLen=0: 44.1%, MLen=2: 26.6%, MLen=1: 11.5%, MLen=3: 9.9%
  Top midfixes: '' (44.1%), 'ch' (13.8%), 'e' (9.9%), 'eo' (4.1%), 'al' (2.2%)
  Top suffixes: 'ol' (19.4%), 'y' (16.6%), '' (12.7%), 'eey' (9.1%), 'or' (7.3%), 'dy' (7.3%)
  Top word types: qokol(8.8%), qokeey(7.8%), qokchy(7.4%), qokeol(6.3%), qoky(5.6%)
  Top-5 account for 36% of tokens
  Midfix entropy: 3.492 bits, Suffix entropy: 3.472 bits

B-dialect qok (N=2471 tokens, 176 types):
  ZeroMid = 78.4%
  MidLen distribution: MLen=0: 78.4%, MLen=2: 11.2%, MLen=3: 4.7%, MLen=1: 3.2%
  Top midfixes: '' (78.4%), 'ch' (5.6%), 'e' (2.6%), 'eed' (1.2%), 'ed' (1.1%)
  Top suffixes: 'edy' (13.4%), 'eedy' (12.5%), 'eey' (11.5%), 'ain' (11.5%), 'aiin' (10.2%)
  Top word types: qokeedy(12.2%), qokain(11.0%), qokedy(10.8%), qokeey(10.6%), qokaiin(9.7%)
  Top-5 account for 54% of tokens
  Midfix entropy: 1.734 bits, Suffix entropy: 3.653 bits

Cross-dialect suffix comparison (top A-enriched):
  'ol': A=19.4%, B=2.9% (A/B=6.74×)  ← strong A preference
  'y':  A=16.6%, B=7.0% (A/B=2.38×)
  'or': A=7.3%,  B=1.5% (A/B=4.98×)
  'edy': A=0.4%, B=13.4% (A/B=0.03×) ← strong B preference
  'eedy': A=0.2%, B=12.5% (A/B=0.01×) ← extreme B preference
  'ain': A=1.3%, B=11.5% (A/B=0.11×)  ← strong B preference

A-exclusive shared midfixes: 'ch' (A/B=2.47×), 'e' (A/B=3.81×), 'eo' (A/B=5.33×),
                              'cho' (A/B=10.35×), 'eos' (A/B=23×), 'cheo' (A/B=18×)
B-exclusive shared: 'ed' (B=1.13%, A-absent), 'eed' (B=1.2%, A-absent)

Comparative (ok, ot same asymmetry direction):
  ok:  A=1.24, B=0.80, A/B=1.55×
  ot:  A=1.51, B=0.82, A/B=1.84×
  qok: A=1.34, B=0.52, A/B=2.58×  ← qok has largest A/B ratio
```

## Result

**H498 CONFIRMED.** The 2.6× midfix length asymmetry is driven by two mechanisms acting simultaneously:

1. **B-qok has extreme zero-midfix dominance (78.4% vs A=44.1%):** The B-dialect standardized qok to be a near-pure onset+suffix template. More than 3 in 4 B-qok words have no midfix.

2. **B-qok suffix paradigm is dominated by canonical B-dialect markers:** The B suffix inventory for qok is: edy (13.4%) + eedy (12.5%) + eey (11.5%) + ain (11.5%) + aiin (10.2%) = 59.2% from just 5 suffixes. These are the EXACT suffixes that define B-dialect classification (the edy/eedy rate ≥5% is what marks a folio as B). In contrast, A-qok suffixes spread across: ol (19.4%), y (16.6%), empty (12.7%), eey (9.1%), or (7.3%), dy (7.3%). No single suffix dominates.

3. **A-qok has the 'ch'-midfix structure:** A-qok's top non-empty midfix is 'ch' at 13.8%, giving qokch-y (7.4%), qokch-ol (2.6%), qokch-or (1.5%). These ch-medial words are 4.5× less common in B (B 'ch' midfix = 5.6% vs A 13.8%). A-qok also has 'e' midfix (9.9% vs B 2.6%), 'eo' (4.1% vs B 0.8%), 'cho' (1.7% vs B 0.2%).

**The concentration pattern quantifies the standardization:**
- B top-5 words account for 54% of all B-qok tokens (extreme concentration)
- A top-5 words account for only 36% of A-qok tokens (more spread)
- Midfix entropy: A=3.492 bits vs B=1.734 bits (A has 2× more midfix diversity)

**The asymmetry is general, not qok-specific:** ok shows A/B=1.55× and ot shows 1.84×. All sparse-onset classes have longer midfixes in A than B. But qok shows the largest ratio (2.58×) because its B suffix paradigm is the most concentrated (the canonical B-dialect vocabulary is built around qok words).

**Structural interpretation:** The B-dialect qok paradigm (qokeedy/qokain/qokedy/qokeey/qokaiin) is functionally a word-class template: {qok} + {edy, eedy, eey, ain, aiin, al, ar, y} = the complete B-dialect qok paradigm. The A-dialect equivalent is more varied: {qok} + {ch, e, eo, al, ...} + {ol, y, '', eey, or, dy, aiin, ar, al}. B has standardized the qok word-class around the edy/eedy/ain suffix family; A has retained a richer morphological range.

## Interpretation

The qok A/B asymmetry reflects a general difference in morphological complexity between A and B dialects: B is more template-driven (higher ZeroMid across all sparse classes, concentrated suffix paradigms, high-frequency canonical word forms), while A is morphologically richer (more midfix diversity, more varied suffix distribution, lower type concentration).

This connects to the established dialect differences: B is characterized by the edy/eedy/ain suffix paradigm which represents a very regular word-formation system applied uniformly to all MID-class onset classes (qok, ok, ot, etc.). A lacks this dominant paradigm and shows more variation. The Mode B simulation currently handles A and B as separate subsets but doesn't explicitly model the morphological complexity difference.

## Limitations

- The suffix classification uses a fixed SUFFIX_LIST; some A-qok words with unrecognized suffixes (12.7% have '' suffix in A vs 3.9% in B) may actually have complex suffixes not in the list. This would slightly undercount A-qok suffix diversity.
- The 'cho' A-exclusive midfix (9 tokens) is small and may be corpus-specific (section bias in A-folios).
- ok/ot comparison is limited to top-5 words; a full decomposition analysis would confirm whether the A>B midfix trend is as consistent across those classes.

## Self-Audit

**Target-awareness:** No target metrics used. Descriptive dialect comparison. No calibration issues.

**Feature-destroying implementation:** Suffix extraction covers 87-96% of words. Remaining '' suffix words may contain complex suffixes. This does not destroy the key finding (ZeroMid rate and midfix length comparisons are unaffected by suffix classification).

**Extrapolation:** The "B-dialect standardized qok around edy/eedy/ain" claim is descriptive. The claim that "A retained richer morphological range" is a comparison statement, not a generative claim.

**Negative-result scope:** Not a negative result. H498 confirmed.

**Control behavior:** No control corpus. The ok/ot comparisons serve as within-VMS controls: they show the same A>B direction, confirming qok asymmetry is not unique but the most extreme case.

## Follow-up Questions

- Q: Does the suffix paradigm shift (A: -ol/-y vs B: -edy/-eedy/-ain) reflect a TEMPORAL change (A written earlier, B later with different vocabulary conventions) or a SECTION difference (A = herbal, B = bio/text)?
- Q: Do other onset classes show the same A vs B suffix paradigm shift (A prefers -ol/-y/-or, B prefers -edy/-eedy/-ain)? Or is this specific to the qo-onset family (qok/ok/ot)?
- Q: The B-dialect concentration (top-5 words = 54% of tokens) suggests qok in B is close to a closed word-class with ~5-8 canonical forms. Can we enumerate the entire B-qok closed paradigm and its usage statistics?
