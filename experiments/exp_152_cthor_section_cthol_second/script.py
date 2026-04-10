#!/usr/bin/env python3
"""
exp_152: cthor Section Profile & cthol@Second Analysis
H301, H302, bonus cthy@LL penultimate
Note: Section analysis failed due to folio_base/section_key mismatch.
Analysis run inline. See result.md.
Bug: SECTION_MAP used 'f1' keys but folio_base values are 'f1r'/'f1v'.
Fix: folio_num = int(re.sub(r'[rv]', '', folio_base[1:]).strip()) to get numeric folio.
"""
print("exp_152: inline. See result.md.")
