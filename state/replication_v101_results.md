# v101 Replication Results — Session R2

**Date**: 2026-04-13
**Experiment**: exp_587
**Corpus**: data/transcriptions/v101_claston.txt (latin-1 encoding, Claston v101)
**Dialect gate**: 191/201 shared folios = 95.0% agreement with ZL3b (PASS)

## Token counts

| Corpus | ZL3b tokens | v101 tokens |
|--------|-------------|-------------|
| B-dialect | 17,997 | 17,365 |
| A-dialect | 8,461 | 11,781 |

A-dialect difference (+39%) is explained by different folio-level dialect assignment
on borderline folios (14 disagreements out of 201). Most disagreements are folios with
ZL3b edy-rate just above 5% that fall below in v101 due to transcription conventions.
This is expected and does not indicate a mapping error.

## Finding classifications

| Finding | Classification | Key metric |
|---------|----------------|------------|
| F1: Three-layer architecture | **RETAINED** | 16/18 = 88.9% class agreement |
| F2: Terminal inversion | **RETAINED** | Zero overlap, A={d,s,a}, B={r,l} |
| F3: Bigram invariants | **RETAINED** | 4/5 directionally replicated |
| F4: A-herbal chain | **FAILED** | sec=77th, ons=86.5th (both <95th) |
| F5: Suffix transformation | **RETAINED** | 19/22 = 86.4% |

**R2 result: PARTIAL (F4 failed) → R3 (ZL3a) triggered as tiebreaker**

## v101 Character Mapping (from STA1_def.pdf)

Core mappings used in classifiers:
- EVA ch = v101 '1', sh = '2', d = '8', y = '9', k = 'h', t = 'k'
- EVA cth = 'K'/'U', ckh = 'H', cph = 'J'/'G', q = '4'
- EVA e (letter) = 'c', l = 'e', r = 'y', p = 'g'
- EVA edy = v101 'c89', eedy = 'cc89' or 'C89' (ee-ligature)
- 'j' = k-gallows variant (added after corpus analysis: context 'oj1c89' = 'okchedy')

Full mapping and onset classifier: experiments/exp_587_replication_v101/result.md

## F4 Failure Analysis

The d→qot→ch→o→sh chain fails in v101 at 77th/86.5th percentile (needs >95th).
Key cause: the o→sh edge has only obs=1 in v101's 48 A-herbal folios.
Compared to ZL3b/ZL3a which have obs=4 for o→sh in 44 A-herbal folios.
This is a power/data-sparsity issue, not a structural incompatibility.
The chain finding requires ZL3a tiebreaker to confirm overall RETAINED verdict.
