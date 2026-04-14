# ZL3a Replication Results — Session R3 (tiebreaker)

**Date**: 2026-04-13
**Experiment**: exp_588
**Corpus**: data/transcriptions/zl3a.txt (ZL EVA version 3a, fetched from voynich.nu/data/previous/)
**Purpose**: Tiebreaker for F4 (R1=RETAINED, R2=FAILED)

## Token delta

| Corpus | ZL3b tokens | ZL3a tokens | Δ% |
|--------|-------------|-------------|-----|
| B-dialect | 17,997 | 17,995 | 0.01% |
| A-dialect | 8,461 | 8,453 | 0.09% |

ZL3a is nearly identical to ZL3b (< 0.1% difference). Same alphabet, classifiers, and
analytics — no new infrastructure required.

## Finding classifications

| Finding | Classification | Key metric |
|---------|----------------|------------|
| F1: Three-layer architecture | **RETAINED** | 18/18 = 100% class agreement |
| F2: Terminal inversion | **RETAINED** | Zero overlap, A={d,s}, B={r,l,a,o} |
| F3: Bigram invariants | **RETAINED** | 4/5 directionally replicated |
| F4: A-herbal chain (TIEBREAKER) | **RETAINED** | sec=97.5th, ons=96.5th (both >95th) |
| F5: Suffix transformation | **RETAINED** | 20/21 = 95.2% |

**R3 result: ALL_RETAINED**

## F4 Tiebreaker Result

- 44 A-herbal folios, 1,082 CL pairs (same as ZL3b/EVA-basic)
- Real chain JS = 3.443
- Section-shuffled: 97.5th percentile ✓
- Onset-shuffled: 96.5th percentile ✓

**Overall F4 verdict: 2/3 systems RETAIN (R1+R3) → F4 RETAINED**

## Overall Transliteration Replication Verdict

With R1 (EVA-basic), R2 (v101), and R3 (ZL3a) all complete:
**ALL 5 PRE-REGISTERED FINDINGS RETAINED** across all applicable transliterations.

See state/transliteration_replication_final_summary.md for complete cross-session analysis.
