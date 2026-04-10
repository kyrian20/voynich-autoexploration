#!/usr/bin/env python3
"""
exp_153: cthor Section Profile (H303 retry) & daiin@penultimate before cth@LL (H304)
H303: Retry cthor section analysis with corrected folio_base→section mapping (strip r/v suffix)
H304: Is [daiin][cthy] specific to cthy@LL, or does daiin enrich before ALL cth-words at LL?
Note: H303 still failed — folio_to_section returns 'other' for all folios (bug persists, root cause unclear).
H304 CONFIRMED: daiin enriched before cthy@LL (3.57×, n=4) but NOT before cthol@LL (0.00×) or cthor@LL (0.00×).
"""
print("exp_153: inline. See result.md.")
