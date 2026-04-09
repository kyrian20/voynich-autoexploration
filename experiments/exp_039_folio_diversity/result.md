# Experiment exp_039: Folio-Level Vocabulary Diversity
Date: 2026-04-09

## Question (H035)
Which folios are statistical outliers in vocabulary diversity (TTR)?

## Results

### Section Mean TTR
| Section | Mean TTR | Folios |
|---------|---------|--------|
| Cosmo (C) | 0.838 | 2 |
| Herbal (H) | 0.835 | 122 |
| Pharma (P) | 0.771 | 16 |
| Special (S) | 0.646 | 25 |
| Text (T) | 0.645 | 6 |
| Bio (B) | 0.552 | 19 |

**Bio section is the most repetitive (TTR=0.552), herbal the most diverse (TTR=0.835).** This is counter-intuitive — bio folios have larger plants/figures and less text per folio, leading to higher repetition within fewer tokens.

### Top Outliers (highest TTR — most diverse)
| Folio | Tokens | TTR | Section | Notes |
|-------|--------|-----|---------|-------|
| f48r | 74 | **1.000** | Herbal B | All 74 tokens unique! |
| f96v | 50 | **1.000** | Herbal A | All 50 tokens unique |
| f87v | 71 | 0.986 | Herbal A | |
| f90r1 | 61 | 0.967 | Herbal A | |
| f7r | 55 | 0.964 | Herbal A | |

All high-TTR outliers are herbal section. f48r and f96v have ALL UNIQUE vocabulary — every word appears exactly once.

### Bottom Outliers (lowest TTR — most repetitive)
| Folio | Tokens | TTR | Section | z-score | Notes |
|-------|--------|-----|---------|---------|-------|
| f76r | 543 | **0.466** | Text (T) | -1.7 | "Key-like" sequence folio |
| f84v | 322 | 0.478 | Bio (B) | -2.0 | |
| f116r | 523 | 0.505 | Special (S) | -1.8 | |
| f77v | 320 | 0.506 | Bio (B) | | |
| f108v | 561 | 0.517 | Special (S) | -1.7 | |

**f76r** (the "key-like sequence" folio from exp_011/013) is the MOST REPETITIVE folio in the entire manuscript at TTR=0.466 — significantly below the Text section mean (0.645, z=-1.7). This repetitiveness is consistent with f76r's structural role (formulaic text associated with the L0 line-marker system).

### Notable Individual Outliers
- **f19r** (Herbal): TTR=0.653, z=-2.6 — most repetitive herbal folio
- **f101r, f89r2** (Pharma): TTR=0.641/0.644, z≈-2.0 — most repetitive pharma folios
- **f81r, f81v** (Bio): TTR=0.610-0.620, z=+1.6-1.8 — most diverse bio folios

## Finding (F046)
- Bio section has lowest mean TTR (0.552) — most repetitive section
- Herbal has highest mean TTR (0.835) — most diverse section
- f76r (key-like sequence folio) is most repetitive in manuscript: TTR=0.466 (z=-1.7 for Text section)
- f48r and f96v (herbal) have TTR=1.000 (all-unique vocabulary, 50-74 tokens)
- High-TTR outliers cluster exclusively in herbal; low-TTR outliers in bio/text/special (all Currier B)
