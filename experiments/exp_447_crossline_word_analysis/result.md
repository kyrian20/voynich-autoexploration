# exp_447: Cross-Line Coupling Word-Level Analysis (H_new_I + H_new_J)

**H_new_I:** ok(LL)→y(LF) cross-line E=1.52-1.64× — is this class-level or word-type specific?
**H_new_J:** B qok(LL)→s(LF) E=1.51×/N=31 — is this the s→sh→qok formula cycle?

---

## Results

### H_new_I: ok→y Cross-Line Word Pairs

| Dialect | N(ok→y) | ok-word types | y-word types | Same-word pairs |
|---------|---------|--------------|--------------|----------------|
| A | 16 | 16 (all unique) | 16 (all unique) | 0 (0%) |
| B | 21 | 12 distinct ok-words | 20 distinct y-words | 0 (0%) |

**A ok-words at LL (in ok→y): top**: okaiin(2), okain(2), oky(2), okchor(2), okol(1), okchom(1), okchy(1), oka(1)
**B ok-words at LL (in ok→y): top**: okeedy(4/9=44%), okain(4/11=36%), okam(2/11=18%), okaiin(2/10=20%)

**y-words at LF after ok-LL:**
A: ykaiin(2), ychol(1), ytchoy(1), ycheol(1), ychy(1) — all unique
B: ykeol(2), ycheo(1), ykeey(1), ydaiin(1), ykain(1) — all unique

**ok→y rate: A=22.5% (16/71 ok cross-line); ot→y rate: A=10.9% (6/55), B=18.0% (20/111).**
ok→y and ot→y rates: B ok(20.8%) ≈ B ot(18.0%); A ok(22.5%) > A ot(10.9×) — A-specific enrichment of ok→y vs ot→y.

### H_new_J: B qok→s Cross-Line Pairs

| Section | N qok→s | % of total |
|---------|---------|-----------|
| Astro | 16 | **51.6%** |
| Pharma | 13 | **41.9%** |
| Herbal | 2 | 6.5% |

**qok-words at LL (in qok→s pairs)**: qoky(5/20=25%), qokal(4/15=27%), qokam(4/12=33%), qokaly(3/5=60%), qokain(3/13=23%), qokedy(2/9=22%), qokar(2/5=40%), qokey(2/6=33%).

**s-words at LF after qok-LL**: saiin(7), sain(4), sar(4), sal(3), sor(1) — common s-body words.

**s→s cross-line word pairs** (class-level test):
- A s→s (N=8): 0/8 same exact s-word (0%). All unique pairs.
- B s→s (N=10): 1/10 same word (10%). Largely unique pairs.

---

## Interpretation

**H_new_I ANSWERED: ok→y cross-line coupling is CLASS-LEVEL, not word-type specific.** All 16 A pairs and 21 B pairs are distinct word-pair combinations (0% same-word repeat). No single ok-word dominates (okeedy=4/21 in B is the highest, a 19% share). No single y-word dominates. The coupling operates at the onset-class level: ok class at LL consistently predicts y-class at LF regardless of which specific words are involved.

A-specific finding: A ok→y (22.5%) > A ot→y (10.9%), while B ok→y (20.8%) ≈ B ot→y (18.0%). In A, ok and ot are functionally differentiated at the cross-line level — ok specifically forecasts y at LF, ot less so. This is consistent with A's ok↔y structural linkage in within-line grammar (F363: A ok→ok E=1.93×; A y self-succession documented in F401).

**H_new_J ANSWERED: B qok→s cross-line E=1.51× is SECTION-SPECIFIC (astro+pharma), not primarily a formula-cycle effect.**

Key observations:
1. **Astro concentration (16/31=52%)**: B astro has elevated qok-LF (1.91×, F431). If astro lines are qok-dominated, then qok appears frequently at both LF and LL within astro folios. When an astro qok-terminal line (qok at LL) is followed by a non-qok line (s at LF), this generates the cross-line qok→s pair. This is an artifact of astro's high qok density, not a formula-cycle rule.

2. **Pharma concentration (13/31=42%)**: B pharma has B's s-formula class (F376: B s-LF → sh-pos1). If pharma lines have s at LF, and the preceding line ended in qok (a common B word class), this generates qok→s pairs. Pharma concentration is more consistent with the formula-cycle hypothesis.

3. **s-words at LF are common content words (saiin/sain/sar/sal)**: These are not specifically the s-formula opener (which would be identified by s followed by sh at pos1 = the F376 s→sh path). The s-LF words after qok-LL are plain s-onset words, not specifically the formula-triggering type.

4. **qok-words at LL have uniform conversion rates (20-40%)**: No single qok-word has dramatically elevated ok→s rate. This is consistent with class-level coupling rather than specific-word pairing.

**Conclusion for H_new_J**: B qok→s is primarily explained by astro's high qok density (astro qok lines end in qok; next line starts with s). Pharma's s-formula provides a secondary source. The s→sh→qok formula cycle (where qok ends a formula line, then s starts the next cycle) is a plausible partial explanation for the pharma-13 component, but not for the astro-16 component.

**s→s cross-line is class-level**: Both A and B s→s pairs are unique word combinations (0-10% same-word). The self-succession operates at the onset-class level, not as specific-word repetition (unlike A y→y self-succession within-line which is dominated by specific words like yaiin).

---

## Self-Audit

**Target-awareness**: No target-aware elements.
**Feature-destroying implementation**: No issues. Note: the qok-LL onset distribution display in the script had a bug (Counter indexed by onset string vs word string), but the pair-level data was correct and sufficient.
**Extrapolation**: Section-specificity conclusion for H_new_J is based on observed pair counts (31 total; astro=16, pharma=13). The astro-artifact explanation is an inference, not directly tested.
**Negative-result scope**: ok→y class-level conclusion is definitive (16/16 unique pairs in A; 21/21 in B). H_new_J's formula-cycle hypothesis is partially supported (pharma-13) and partially explained by astro density.
**Control behavior**: N/A.

---

## Conclusion

H_new_I ANSWERED: **ok→y cross-line coupling is CLASS-LEVEL** — all unique word pairs, no single word dominant. A ok→y specifically (22.5%) vs ot→y (10.9%), while B ok/ot rates converge (~19-21%). H_new_J ANSWERED: **B qok→s cross-line E=1.51×/N=31 is section-specific** (astro=52%/pharma=42%), not a formula-cycle rule. Astro's high qok density explains the majority of qok→s pairs. **s→s cross-line is class-level** (0-10% same exact word). **No new finding ID** — both results confirm F438 (cross-line coupling is class-level) and extend section-specificity understanding; no novel structural fact beyond existing findings.
