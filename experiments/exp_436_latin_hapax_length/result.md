# exp_436: Hapax/Frequent Word Length Gradient in Latin vs VMS (H_new_E)

**Hypothesis (H_new_E):** Does natural language (Latin, Italian) show the same hapax-longer/frequent-shorter gradient as VMS (F435)? If yes: the F435 finding is a universal statistical property, not VMS-specific.

**Method:** Caesar's Gallic Wars (Latin, 23274 tokens) and Dante's Divine Comedy (Italian, 92754 tokens). Tokenize; compute word frequency; compare mean word length for hapax (f=1) vs mid (f=2-4) vs frequent (f≥5).

---

## Results

| Corpus | Hapax mean len | Freq mean len | Ratio |
|--------|---------------|---------------|-------|
| Latin (Caesar) | 8.55 | 4.78 | **1.79×** |
| Italian (Dante) | 7.36 | 3.84 | **1.92×** |
| VMS A | 6.33 | 4.47 | **1.42×** |
| VMS B | 6.59 | 4.96 | **1.33×** |

**Latin by frequency class:**

| Class | N tokens | Mean len | >6 chars | ≤3 chars |
|-------|----------|----------|----------|----------|
| hapax(f=1) | 3799 | 8.55 | 78.8% | 1.4% |
| mid(f=2-4) | 4368 | 7.67 | 66.4% | 2.2% |
| freq(f≥5) | 15107 | 4.78 | 23.9% | 37.3% |

---

## Interpretation

**H_new_E ANSWERED: The hapax-longer pattern IS UNIVERSAL in natural language. VMS shows the same gradient but LESS strongly (1.33-1.42× vs 1.79-1.92× in Latin/Italian).**

The hapax/frequent length ratio in natural language is 1.79-1.92× — LARGER than VMS's 1.33-1.42×. This pattern arises from Zipf's law mechanics: high-frequency words in natural language are function words (et, in, ad, non, la, di, che = 2-4 chars), while rare words are long content words (inflected forms, compound forms, specialized vocabulary). The same statistical force operates in VMS but produces a WEAKER gradient than in natural language.

**Revision to F435 interpretation:**
F435 claimed hapax words are "structurally abnormal, not consistent with simple productive morphological system." This finding must be qualified: the hapax-longer gradient per se is a universal statistical property. The VMS gradient (1.33-1.42×) is actually WEAKER than natural language (1.79-1.92×), suggesting VMS has MORE uniform word lengths across frequency classes than Latin or Italian.

However, the specific midfix length claim from F435 remains distinct:
- VMS frequent words have near-zero midfix (A: 0.43 chars, B: 0.36 chars) — effectively onset+suffix only
- VMS hapax words have large midfix (A: 2.73 chars, B: 2.79 chars)
- Latin/Italian do not have an equivalent "midfix" decomposition — their frequent function words are short because they're short words, not because they have zero midfix length after stripping onset+suffix

The VMS midfix result (6-8× hapax/freq midfix ratio) is not directly comparable to natural language, because VMS has a specific morphological template (onset+midfix+suffix) that Latin lacks.

**What F435 should say (revised):** The word length gradient is a universal property present in natural language (1.79-1.92×) and in VMS (1.33-1.42×, weaker). VMS is distinctive in that frequent words have near-zero midfix (template skeletons), while hapax words have substantial midfix — a decomposition not applicable to Latin/Italian. The gradient per se is not VMS-specific; the midfix-layer-specific analysis is VMS-specific.

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No feature-destroying elements.
**Extrapolation**: No over-strong claims.
**Negative-result scope**: This IS a partially negative result — the F435 pattern is present in natural language. The claim "hapaxes are structurally abnormal (not consistent with productive morphology)" is SOFTENED: the length gradient is universal; the midfix-specific analysis is VMS-specific.
**Control behavior**: The control (Latin/Italian) shows a LARGER ratio than VMS (1.79-1.92× vs 1.33-1.42×). This is the Catch 1 pattern (control exceeds real data). Investigation: the control is measuring the universal Zipfian hapax/frequent distinction, and VMS is LESS extreme than natural language on this dimension. This reversal is the finding, not a confound. No flag needed — the comparison is interpretable and expected once the mechanism is understood.

---

## Conclusion

H_new_E ANSWERED: Hapax-longer gradient is universal in natural language (Latin 1.79×, Italian 1.92×) and STRONGER than VMS (1.33-1.42×). F435's "hapax structurally abnormal" claim must be qualified: word-length gradient per se is universal; VMS midfix-layer-specific analysis (6-8× hapax/freq ratio) remains VMS-specific but is now contextualized. **Revises F435 interpretation (see below); no new finding ID.**

**F435 Revision Note:** "Hapax words are longer than frequent words (ratio 1.33-1.42×), consistent with the universal Zipfian pattern (Latin=1.79×, Italian=1.92×, both larger than VMS). VMS shows this pattern LESS strongly than natural language. The midfix-layer analysis (6-8× midfix ratio) is VMS-specific and does not have a direct natural-language comparison."
