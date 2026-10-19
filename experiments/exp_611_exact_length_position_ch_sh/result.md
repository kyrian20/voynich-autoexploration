# exp611 — Exact word-length and position matching

## Method
Compare ch and sh only within the same exact token length and same character position of the digraph, and only on folios containing both contexts in that stratum. This is stricter than coarse length bins, but remains descriptive: word identity/template, section and hand are not fully controlled; sparse strata are reported transparently.

## ZL3b
- Source SHA-256: bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc
- Matched length-position strata: 32; strata with at least 5 paired folios: 25; paired folio-strata total: 1134
- Matched contexts: ch n=5822, vowel rate=0.8461009962212298; sh n=3389, vowel rate=0.9043965771614045
- Mean of within-folio differences across matched strata (ch−sh): -0.06649514804006545

Most populated matched strata:
- Length 4, position 0: paired folios=154, ch rate=0.881933438985737, sh rate=0.9226441631504922
- Length 5, position 0: paired folios=124, ch rate=0.9116555308092057, sh rate=0.9727272727272728
- Length 6, position 0: paired folios=111, ch rate=0.6417704011065007, sh rate=0.7286432160804021
- Length 3, position 0: paired folios=101, ch rate=0.8299595141700404, sh rate=0.9347826086956522
- Length 7, position 0: paired folios=81, ch rate=0.73224043715847, sh rate=0.8356807511737089
- Length 5, position 1: paired folios=78, ch rate=0.8135593220338984, sh rate=0.8943661971830986
- Length 6, position 1: paired folios=67, ch rate=0.9525, sh rate=0.9735449735449735
- Length 8, position 0: paired folios=63, ch rate=0.8669724770642202, sh rate=0.8857142857142857
- Length 7, position 2: paired folios=43, ch rate=0.9585492227979274, sh rate=1.0
- Length 6, position 2: paired folios=35, ch rate=0.7313432835820896, sh rate=0.8095238095238095

## IT2a
- Source SHA-256: 7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5
- Matched length-position strata: 31; strata with at least 5 paired folios: 25; paired folio-strata total: 1153
- Matched contexts: ch n=5941, vowel rate=0.838411041912136; sh n=3419, vowel rate=0.9005557180462124
- Mean of within-folio differences across matched strata (ch−sh): -0.07133294669182684

Most populated matched strata:
- Length 4, position 0: paired folios=159, ch rate=0.8728139904610492, sh rate=0.9180555555555555
- Length 5, position 0: paired folios=127, ch rate=0.9073387694588584, sh rate=0.9675977653631285
- Length 6, position 0: paired folios=113, ch rate=0.6391184573002755, sh rate=0.7220843672456576
- Length 7, position 0: paired folios=95, ch rate=0.7016317016317016, sh rate=0.8135593220338984
- Length 3, position 0: paired folios=83, ch rate=0.8191489361702128, sh rate=0.9453551912568307
- Length 5, position 1: paired folios=78, ch rate=0.8112582781456954, sh rate=0.9090909090909091
- Length 8, position 0: paired folios=65, ch rate=0.8326180257510729, sh rate=0.9
- Length 6, position 1: paired folios=63, ch rate=0.9519230769230769, sh rate=0.9701492537313433
- Length 7, position 2: paired folios=46, ch rate=0.9476190476190476, sh rate=1.0
- Length 6, position 2: paired folios=39, ch rate=0.7483870967741936, sh rate=0.8260869565217391

## Interpretation
This is a stricter composition check than coarse length bands, not a Parisel replication. The matched aggregate is not causal because token identity and section are not controlled; no p-value is reported.
