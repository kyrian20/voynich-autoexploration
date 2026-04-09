# Experiment exp_025: Compound-Forming Character Test
Date: 2026-04-09

## Hypothesis Tested
H022: The characters in f66r column 2 (c,d,f,l,o,p,r,s,t,x,y) are the "atomic" non-compound-forming EVA characters; the absent characters (a,e,h,i,k,n,q and others) are exactly the compound-forming ones.

## Method
For each EVA character (≥10 occurrences in body text), computed:
- `compound_rate` = fraction of occurrences inside a known compound form (ch, sh, ee, ain, aiin, ck, kh, cth, ckh, cph, ii, iii, qo)
- `in_col2` = 1 if char in f66r column 2, 0 if not

Fisher's exact test: are compound-forming chars (rate > 40%) significantly less likely to appear in col2?

## Character Compound Rates

| Char | Total | In compound | Rate | In f66r col2 |
|---|---|---|---|---|
| h | 16,016 | 15,954 | 0.996 | **ABSENT** |
| c | 11,822 | 11,761 | 0.995 | **IN COL2** ← anomaly |
| q | 5,276 | 5,152 | 0.976 | ABSENT |
| n | 5,646 | 5,498 | 0.974 | ABSENT |
| i | 10,630 | 9,966 | 0.938 | ABSENT |
| s | 6,308 | 4,195 | 0.665 | **IN COL2** ← partial anomaly |
| e | 17,631 | 8,700 | 0.493 | ABSENT |
| a | 12,465 | 5,168 | 0.415 | ABSENT |
| o | 21,781 | 5,152 | 0.237 | IN COL2 |
| t | 5,774 | 842 | 0.146 | IN COL2 |
| p | 1,443 | 187 | 0.130 | IN COL2 |
| k | 9,803 | 828 | 0.084 | **ABSENT** ← anomaly |
| d, f, l, r, x, y, m, b, g | various | 0 | 0.000 | d/f/l/r/x/y in, m/b/g absent |

## Statistical Test

**2x2 Contingency Table (threshold: compound_rate > 0.40):**

| | In f66r col2 | Not in f66r col2 |
|---|---|---|
| Compound-forming (rate >0.40) | 2 (c, s) | 6 (h, q, n, i, e, a) |
| Standalone (rate ≤0.40) | 9 (d,f,l,o,p,r,t,x,y) | 4 (k, m, b, g) |

Fisher's exact test (one-tailed): **p = 0.063**

Odds ratio = 0.148 — compound-forming chars are 6.7x less likely to appear in col2. The direction is correct but the result is not statistically significant at α = 0.05.

## Key Anomalies

**'c' in col2 with compound_rate=0.995:** 'c' appears inside compounds (ch, ck, cth, ckh, cph) 99.5% of the time — yet IS in f66r col2. This is the biggest exception to H022. It suggests f66r col2 includes compound-INITIATING characters (c starts ch, ck, cth) but excludes compound-COMPLETING characters (h always follows c or s, never initiates). The distinction is "base glyph that can initiate a compound" vs "non-base glyph that only completes compounds."

**'s' in col2 with compound_rate=0.665:** 's' initiates 'sh' but can also stand alone (s- words). Similar to 'c', it's a compound-initiating character.

**'k' absent from col2 with compound_rate=0.084:** 'k' is mostly standalone (only 8.4% compound rate from 'ck' + 'kh'), yet absent from col2. 'k' is used in EVA for gallows characters (k, t, f, p) and forms 'ck', 'kh'. The absence of 'k' from col2 is not explained by compound-formation alone.

## Reformulated Pattern

The compound-rate distinction partially explains col2 membership, but a more accurate formulation:

**In col2**: Characters that CAN stand alone or initiate compounds (c, d, f, l, o, p, r, s, t, x, y)
**Absent**: Characters that exclusively COMPLETE compounds or form self-fusing clusters:
- h (always after c or s, never word-initial as standalone)  
- e (self-fuses: ee, eee)
- i (self-fuses: ii, iii; or follows a: ain, aiin)
- n (terminates: ain, aiin, iin)
- q (locks to 'o': qo almost always)
- a (leads: ain, aiin — but rarely standalone)

The 'k' absence doesn't fit this formulation cleanly (k can stand alone but is absent).

## Verdict

**H022 PARTIALLY SUPPORTED, not statistically significant (p = 0.063).**

The qualitative pattern holds for 6 of the 8 highest-compound-rate chars (h, q, n, i, e, a are all absent). But 'c' (compound_rate=0.995) is IN col2, and 'k' (compound_rate=0.084) is ABSENT. A more precise formulation distinguishes:

- **Compound-initiating chars** (c, s): IN col2, despite high compound rate
- **Compound-completing chars** (h, n): ABSENT, even when compound rate varies

f66r col2 may list "base graphemes that can initiate compounds or stand alone" rather than simply "non-compound-forming chars." This is a slightly more specific hypothesis than H022 as originally stated.
