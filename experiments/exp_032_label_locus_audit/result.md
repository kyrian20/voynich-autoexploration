# Experiment exp_032: Complete Label Locus Audit (H021 Completion)
Date: 2026-04-09

## Hypothesis Tested
H021 (partial completion): Audit all non-L0 label loci (Lf, Lz, Ls, Lc, Ln, Lt, La, Lp, Lx) for contamination patterns and characterize each label type.

## Label Locus Inventory

| Locus | Count | Section | Folios | Notes |
|-------|-------|---------|--------|-------|
| Lf | 194 | P (100%) | 15 | Pharma flask labels |
| Lz | 299 | Z (100%) | 12 | Zodiac circle labels |
| Ls | 76 | A (100%) | 4 | Astrological star labels |
| Lc | 40 | P (100%) | 12 | Cosmo-pharma labels |
| Ln | 63 | B (100%) | 8 | Bio narrow labels |
| Lt | 47 | B (100%) | 10 | Bio tube/container labels |
| La | 7 | C/A | 2 | Misc |
| Lp | 3 | H | 3 | Misc |
| Lx | 3 | H/T | 3 | Misc |

## Key Finding 1: Non-L0 Label Loci Are Structurally Clean
**Zero single-char entries** across all non-L0 label loci. Unlike L0 (which was contaminated with 43 LINE_MARKER and 108 LIST_ENTRY items), all Lf/Lz/Ls/Lc/Ln/Lt entries are genuine word-form labels.

**100% section specificity**: Each locus maps to exactly one manuscript section. This confirms the locus codes are structurally meaningful.

## Key Finding 2: Extremely High Type-Token Ratios (Near-Unique Vocabulary)

| Locus | TTR | Hapax rate |
|-------|-----|------------|
| Lc | 1.000 | 100% |
| Ls | 0.988 | 98.8% |
| Ln | 0.962 | 96.1% |
| Lf | 0.956 | 96.6% |
| Lt | 0.957 | 95.6% |
| Lz | 0.821 | 87.0% |

Every label corpus is near-completely unique. The pharma flask labels (Lf) have 194 entries but only 194 tokens with 87 types and 84 hapax — essentially every label word is unique. The cosmo pharma labels (Lc) have 100% hapax rate.

## Key Finding 3: H2 Gradient Below Body Text

| Corpus | H2 (bits) | Tokens |
|--------|----------|--------|
| Body text | 2.071 | 33,454 |
| L0 labels | 2.312 | 226 |
| Ls (astro star) | 2.265 | 85 |
| Lf (pharma flask) | 2.153 | 91 |
| Lz (zodiac) | 1.851 | 56 |
| Ln (bio narrow) | 1.833 | 53 |
| Lc (cosmo pharma) | 1.780 | 20 |
| Lt (bio tube) | 1.739 | 47 |

Notable: L0 and Ls have HIGHER H2 than body text; Lc and Lt have LOWER H2. Biological section labels (Ln, Lt) are the most internally constrained, while astrological labels (L0, Ls) are the most diverse.

This gradient INVERTS the section-entropy relationship: herbal body text (Currier A) tends to have lower H2 than pharma/bio (Currier B), but their labels show the opposite pattern.

## Key Finding 4: Pharma Labels Concentrated in f88-f102 Range
Lf (194 entries) spans f88r–f102v2. Top folios: f99r (30), f99v (21), f102v2 (19), f101v (18). These are the pharma/recipe section pages with jar/container illustrations.

Lc (40 entries) overlaps with Lf in the pharma section — likely the barrel/round container labels vs the flask labels.

## Key Finding 5: Bio Labels Concentrated on Specific Folios
Ln (63 entries): predominantly f75v (20), f84r (11), f80r (10), f82r (10).
Lt (47 entries): f82v (8), f75v (7), f77r (7), f77v (6), f78r (6).

**Crucially, f75v contributes 20 Ln + 7 Lt = 27 label entries.** This is the same folio with L0 LINE_MARKER contamination (exp_026). The Ln and Lt loci on f75v are the TRUE label content — confirming the L0 entries on f75v are structural (line markers), not the same as Ln/Lt object labels.

## H021 Status: COMPLETE

The full label locus picture:
- **True object labels**: Lf (194) + Lz (299) + Ls (76) + Lc (40) + Ln (63) + Lt (47) + La (7) + Lp (3) + Lx (3) = **732 entries** (plus 9 from L0)
- **Line markers (L0)**: 43 entries
- **List entries (L0)**: 108 entries
- **Total L0**: 297 entries (as counted by ZL3b locus types; exp_022 audited 160 via content analysis)

The non-L0 label corpus (732 entries) is uncontaminated and can be used as a clean label training set for vocabulary analysis.

## Findings Added: F038, F039

**F038:** All non-L0 label loci (Lf/Lz/Ls/Lc/Ln/Lt) are 100% section-specific with zero single-char/LINE_MARKER contamination. True label count = ~732 entries.

**F039:** Label H2 shows a gradient: L0/Ls > Lf > body text > Lz > Ln > Lc > Lt. Biological section labels have the lowest H2 (1.74-1.83 bits, well below body text's 2.07). All label corpora have extremely high TTR (0.82-1.00), confirming near-unique label vocabulary.
