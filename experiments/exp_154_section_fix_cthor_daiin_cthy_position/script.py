#!/usr/bin/env python3
"""
exp_154: Section Bug Fix (H305 diagnostic), cthor Section Profile (H303 retry),
         daiin→cthy Positional Analysis (H306), and Corrected Full cth Paradigm

H305: Identified section bug — folio_base='<f1r' (leading '<' not stripped).
      Fix: folio_raw.split('.')[0].lstrip('<') → 'f1r' → folio_num=1 → section='herbal'. WORKS.
H303: cthor is 97% in A-herbal (32/33). Profile corrected: second=2.16× ENRICHED,
      LF=0.38× DEPLETED. F158's "cthor=LF-opener" CORRECTED.
H306: daiin→cthy bigrams (n=9): cthy at LL=55.6% (2.12× enriched) — CONFIRMED.
      daiin is an LL-specific selector for cthy.
BONUS: Full cth paradigm corrected — exp_151/152 had swapped LF/second labels.
       cthor=second (2.16×); cthol=MID (1.33×); cthy=LL (1.63×); cthom=LL (2.49×).
"""
print("exp_154: inline. See result.md.")
