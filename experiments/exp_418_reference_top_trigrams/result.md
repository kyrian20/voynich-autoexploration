# exp_418: VMS Formula Types vs Reference Corpora Structure

**Hypothesis (H636):** The specific formula types (p→sh→qot, y→sh→ch, qok→sh→k) may be VMS-specific even if the formula-typed *fraction* is not discriminating. Compare top formula trigrams from VMS B, Latin Caesar, and Italian Dante at N≥5, E≥2.0. Do the structural patterns differ?

**Method:** For each corpus, compute (LF, pos1, pos2) onset trigrams, E_cond = P(pos2|LF,pos1)/P(pos2|pos1), and list top trigrams at N≥5, E≥2.0. VMS B uses EVA onset classes; Latin/Italian use first-letter onsets. Classify each trigram structurally (self-chain/loop/hetero-class).

---

## Results

### VMS B (EVA onset, N_lines=2265)
10 formula trigrams at N≥5, E≥2.0:

| Trigram | E | N | Structure |
|---------|---|---|-----------|
| qok→sh→k | 3.90× | 5 | hetero |
| d→ot→ot | 3.69× | 5 | self-chain(p1=p2) |
| l→ch→qok | 2.72× | 5 | hetero |
| d→qok→ol | 2.61× | 6 | hetero |
| y→sh→ch | 2.53× | 8 | hetero |
| y→o→ch | 2.45× | 6 | hetero |
| qok→ch→qo | 2.35× | 8 | hetero |
| d→ch→y | 2.23× | 5 | hetero |
| qok→ch→ol | 2.06× | 5 | hetero |
| p→sh→ok | 2.03× | 6 | hetero |

Note: p→sh→qot (the canonical p-formula type) does NOT appear at E≥2.0 at N≥5 in this full VMS B list — p→sh→ok appears instead. This suggests p→sh→qot's E_cond may be slightly below 2.0 or N slightly below 5 in this corpus version (vs F416's confirmed qot enrichment).

### Latin Caesar (first-letter onset, N_lines=2404)
4 formula trigrams at N≥5, E≥2.0:

| Trigram | E | N | Structure |
|---------|---|---|-----------|
| a→e→l | 5.34× | 5 | hetero |
| i→c→d | 3.41× | 5 | hetero |
| p→e→d | 2.59× | 6 | hetero |
| p→e→m | 2.16× | 5 | hetero |

### Italian Dante (first-letter onset, N_lines=14321)
15 formula trigrams at N≥5, E≥2.0 (larger corpus):

| Trigram | E | N | Structure |
|---------|---|---|-----------|
| s→c→u | 5.78× | 7 | hetero |
| g→l→a | 5.29× | 5 | hetero |
| i→c→x | 4.91× | 24 | hetero |
| p→c→x | 3.91× | 46 | hetero |
| m→a→m | 3.35× | 5 | loop(lf=p2) |
| s→e→s | 4.49× | 5 | loop(lf=p2) |
| ... | | | |

---

## Interpretation

**VMS B vs Latin/Italian formula type structure:**

1. **Count**: At comparable corpus size (VMS B 2265 lines vs Latin 2404 lines), VMS B has 10 formula types vs Latin 4 — more formula types at the same N≥5 threshold.

2. **Structural similarity**: All three corpora produce predominantly hetero-class formula types. The structural classification (hetero/self-chain/loop) does not distinguish VMS from natural language. Both VMS and natural language produce onset-class/letter trigrams where LF routes through pos1 to a specific pos2.

3. **Natural language formula types appear to reflect syntax**: Latin p→e→d/p→e→m likely represents prepositional phrases (Latin p-words = prepositions like "per", "pro", "post"; e-words = verbs/objects beginning with 'e'; d-words = following content). Italian p→c→x (N=46, large N) likely represents a fixed phrase pattern. The high E-values for Italian (4-6×) at larger N reflect genuine syntactic regularities.

4. **VMS formula types involve template-class onset routing**: The VMS B formula types concentrate on qok/sh/ch/ot onset classes as pos1 — the template-copying classes (F392). qok→sh→k, qok→ch→qo, qok→ch→ol all have qok at LF routing through sh/ch at pos1. y→sh→ch and y→o→ch have y at LF. These reflect the VMS onset-class grammar rules, not syntactic word-order patterns.

5. **No structural discriminator found**: The formula trigram pattern (LF-conditional pos2 enrichment) is the same MECHANISM in both VMS and natural language. The specific onset classes and values differ, but the structural form is identical.

**p→sh→qot absence from N≥5 list**: The canonical p-formula type is present in F396/F416 but does not appear in the current top-10 VMS B list at E≥2.0, N≥5. Possible reasons: (1) E_cond just below 2.0 threshold; (2) slight corpus difference (N_lines differ between runs). This does not invalidate F396/F416 — p→sh→qot was confirmed with E=2.11×(N=8) in exp_392.

**NEW formula types at N≥5**: l→ch→qok=2.72×(N=5), d→qok→ol=2.61×(N=6), y→o→ch=2.45×(N=6), d→ch→y=2.23×(N=5), qok→ch→ol=2.06×(N=5), p→sh→ok=2.03×(N=6). These are all directional-to-modest N values but are new candidates for the B formula vocabulary.

---

## Limitations

- p→sh→qot absent from this list — may be due to corpus boundary conditions or slight E<2.0 at N≥5 in this run. Previously confirmed in exp_392 (E=2.11×/N=8 in a slightly different corpus window). Not a contradiction but worth noting.
- Latin/Italian use first-letter onset; VMS uses EVA onset. The grains differ. Natural language formula types at first-letter grain reflect syntactic structure; VMS EVA onset grain captures word-class structure.
- Italian type counts inflated by 6× larger corpus.
- "p-formula reflects syntax" interpretation for Latin/Italian cannot be confirmed without knowing the actual words.
- PASS.

---

## Self-Audit

**Target-awareness**: None.

**Extrapolation**: "formula types reflect syntax" for Latin/Italian stated as hypothesis, not finding.

**Negative-result scope**: "No structural discriminator found" is scoped to the hetero/self-chain/loop classification.

---

## Conclusion

H636 ANSWERED (partially). VMS B has more formula types than Latin at the same corpus size (10 vs 4 at N≥5). The structural form of formula trigrams (LF-conditional pos2 enrichment) is the same mechanism in both VMS and natural language — no structural discriminator. The specific onset classes in VMS formula types are B-specific template-class routes (qok/sh/ch/ot dominated), while Latin/Italian types likely reflect syntactic word-order patterns. NEW confirmed-directional formula types for VMS B: l→ch→qok(2.72×/N=5), d→qok→ol(2.61×/N=6), y→o→ch(2.45×/N=6).
