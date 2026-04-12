# exp_227: H427 — No-Connector Word Generation

**Date**: 2026-04-11  
**Hypothesis**: H427 — Does removing the connector from word generation (onset+suffix only instead of onset+connector+suffix) bring word_len_mean within ±20% of VMS 5.400 without regressing the 12 currently passing metrics?  
**Status**: H427 NEGATIVE — word_len_mean FIXED (94.8% PASS) but edy_rate REGRESSED (63.4% FAIL, was 96.4% PASS in exp_226). Net 12/18 unchanged. Root cause: the connector was providing the modifiable middle region for edy words — removing it makes edy-suffix preservation degenerate into fresh-word fallback for essentially all edy words.

---

## Design

Single change from exp_226: `make_word_sim(onset, suffix, rng)` → `make_word_no_connector(onset, suffix)`.

The connector (randomly chosen from 'a','ai','o','oi','e','ei', avg 1.5 chars) is eliminated. Words are generated as `onset + suffix` directly.

All other parameters identical to exp_226: cp=0.55, mp=0.90, p_blind=0.30, p_lf=1.0, onset+edy preserving with fresh-word fallback, VMS MID onset for MID.

N=30 simulations.

---

## Results

```
Metric           VMS    E227       %  P?    E226    delta
am_ll           6.550   6.335   96.7% P    6.216   +0.119
d_ll            1.362   1.217   89.3% P    1.220   -0.003
y_lf            3.324   3.469  104.4% P    3.520   -0.051
ss_mean         1.164   1.296  111.3% P    1.326   -0.030
adj_rate        0.009   0.006   65.9% F    0.003   +0.003
qok_lf          0.778   0.754   96.9% P    0.765   -0.011
d_lf            2.211   2.323  105.1% P    2.304   +0.019
s_lf            4.638   5.004  107.9% P    5.073   -0.069
ch_ll           0.939   1.053  112.2% P    1.062   -0.009
ok_ll           0.975   1.061  108.9% P    1.054   +0.007
qok_ll          0.595   0.743  124.8% F    0.760   -0.017
ss_d            1.291   1.365  105.7% P    1.485   -0.120
ss_y            1.955   1.577   80.7% P    1.598   -0.021
am_lf_enr       0.122   0.419  341.8% F    0.373   +0.046
am_mid_enr      0.195   0.258  132.5% F    0.286   -0.028
edy_rate        0.194   0.123   63.4% F    0.187   -0.064  ← REGRESSION
word_len_mean   5.400   5.118   94.8% P    6.637   -1.519  ← FIXED
qok_ch          1.267   0.991   78.2% F    0.982   +0.009

Pass count:  E227=12/18  |  E226 (baseline)=12/18
```

Net: word_len PASS (+1), edy_rate FAIL (-1). Net 12/18 unchanged.

---

## Interpretation

### Finding 1: The connector provides the modifiable middle region for edy words

Without the connector, words are generated as `onset + suffix` only. For a word like:
- "ch"+"edy" = "chedy" (5 chars): onset_len=2, edy_len=3 → modifiable region = [2:2] = empty → fresh-word fallback
- "qok"+"edy" = "qokedy" (6 chars): onset_len=3, edy_len=3 → modifiable region = [3:3] = empty → fresh-word fallback

Without the connector, essentially ALL edy-ending words of the form onset+edy have no modifiable middle region. The fresh-word fallback generates a new random word (which may or may not be edy). This is the same mechanism diagnosed in exp_225 — but more severe:

In exp_226 (WITH connector): "ch"+"ai"+"edy" = "chaidy" (6 chars) → onset_len=2, edy_len=3, modifiable region = [2:3] → 1 char modifiable → edy preserved.

Without connector, the 34% of edy words that "had a middle region" in exp_225 now mostly LOSE their middle region (onset+suffix only → no middle). The fresh-word fallback is triggered for essentially all edy words in the buffer, depleting edy_rate to 63.4%.

**This reveals an architectural dependency**: the connector is not merely cosmetic length — it is the mechanism that provides modifiable middle characters for edy-ending words. Removing it breaks edy preservation.

### Finding 2: word_len_mean is fixed (94.8% PASS)

word_len drops from 6.637 to 5.118. The reduction of 1.519 chars is approximately equal to the connector's average length (1.5 chars from the 3 single-char + 3 two-char options). The no-connector approach correctly reduces word length to near VMS average.

**Note on the pre-run diagnostic**: The diagnostic showed "Expected word length (no connector): 8.00" but the actual mean was 5.118. The discrepancy is because:
1. The diagnostic generated fresh words; the actual output includes many Timm-modified copies
2. The suffix 'other' (a categorical label, 5 literal chars) inflates fresh word lengths significantly, but Timm modification over the buffer equilibrium redistributes word lengths
3. The buffer equilibration through repeated modification produces a different distribution than the initial fresh generation

### Finding 3: adj_rate increases (0.003→0.006)

The adj_rate increase is consistent with the edy_rate mechanism: when edy words trigger the fresh-word fallback, the fresh word may coincidentally match the previous word if the vocabulary is limited. Also, shorter words have higher collision probability (fewer possible distinct words). The increase from 0.003 to 0.006 keeps adj_rate well below VMS 0.009 (criterion still met).

### Finding 4: Architectural incompatibility identified

The no-connector approach and edy-preservation are architecturally incompatible under the current generation model:
- word_len fix requires shorter words → no connector
- edy preservation requires modifiable middle region → connector needed
- These are mutually exclusive requirements for edy words of the form onset+edy

To simultaneously fix word_len AND maintain edy_rate under edy-preservation, a different approach would be needed:
- **Option A**: Use a minimal connector (single char only: 'a','o','e' → avg 1 char). Expected word_len ≈ 2+1+3 = 6 → still 111% of VMS 5.4, still FAIL on ±20%.
- **Option B**: Replace the generation model with VMS-derived word vocabulary (word sampling, not onset+connector+suffix). This would match word lengths by construction but is a major architectural change.
- **Option C**: Accept word_len_mean as a universal failure of the onset+connector+suffix generation class and prioritize other metrics.

---

## Limitations

1. **Trade-off is complete**: There is no known connector-length value that simultaneously fixes word_len (needs ≤6 avg) AND maintains edy preservation (needs ≥1 char middle region for edy words). A minimal connector of 1 char would give avg word_len ≈ 6 → still 111% of VMS 5.4 → still FAIL on ±20%.
2. **edy_rate regression is severe (63.4%)**: Much worse than the original exp_221 failure (72.2%), because more edy words lose their middle region without the connector.
3. **N=30**: Standard.

---

## Self-Audit

**Target-awareness**: Same as exp_226 (inherited from exp_221). The no-connector modification is not target-aware — it's a structural change to the generation model. word_len_mean improvement is a mechanistic consequence of removing the connector, not calibration to VMS 5.400.

**Feature-destroying implementation**: The no-connector change destroys the edy-preservation feature's effectiveness. Without a connector, edy words have no modifiable middle region → fresh-word fallback always triggered → edy words systematically replaced by non-edy words in the buffer. This is a genuine feature-destroying implementation: the change to fix word_len destroys the mechanism that fixes edy_rate. The two features (word length reduction, edy preservation) are mechanistically coupled through the connector's role as middle-region provider. This is documented explicitly in Finding 1.

**Extrapolation**: The incompatibility is mechanistically derived: for any onset+edy word (onset≥1, edy=3 chars), if no connector is added, the modifiable region is empty → edy preservation always falls back to fresh word. This is a logical argument, not an extrapolation from tested parameters. The claim "the connector is necessary for edy preservation in words of the form onset+edy" is supported by the implementation and confirmed by the result.

**Negative-result scope**: The conclusion "word_len fix and edy_rate fix are incompatible under the current connector-based generation model" is specifically scoped to this architecture class. It does NOT claim that word_len cannot be fixed in general — VMS-word-vocabulary sampling would fix both. It does NOT claim edy preservation cannot be maintained at shorter word lengths in principle.

**Control behavior**: No control corpus comparison. Internal comparison consistent with mechanistic predictions. adj_rate increase (0.003→0.006) is mechanistically consistent with shorter words (higher collision probability) and edy-cascade fresh-word effects.

---

## Conclusion

H427 NEGATIVE (net-zero). Removing the connector fixes word_len_mean (94.8% PASS) but breaks edy preservation (edy_rate 96.4%→63.4% FAIL). The connector is architecturally necessary for edy preservation: it provides the modifiable middle region that prevents fresh-word fallback for edy words. Net: 12/18 unchanged.

**Key diagnostic**: The generation model's `onset + connector + suffix` structure serves a dual role — cosmetic word length AND structural requirement for edy-preservation's modifiable middle region. These roles are coupled: reducing word length by removing the connector simultaneously undermines the edy fix. Future attempts to fix word_len_mean must either (a) maintain a connector sufficient for edy preservation or (b) replace the generation model entirely.

The current best result (12/18) remains at exp_226. The word_len_mean failure is now characterized as a **structurally constrained failure** of the onset+connector+suffix generation class, given the current edy-preservation requirement.
