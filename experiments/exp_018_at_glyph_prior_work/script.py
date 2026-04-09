"""
Experiment: exp_018_at_glyph_prior_work
Goal: Search KB and web for prior discussion of @glyph annotations,
non-standard Voynich characters, f57v circular text, f49v margin sequences,
f66r word list, f76r key-like sequences.
"""

# This script documents the KB search methodology.
# Actual searches performed manually / via WebFetch in result.md.

KB_SEARCH_TERMS = [
    "non-standard glyph",
    "rare glyph",
    "anomalous character",
    "EVA exception",
    "@169",
    "@172",
    "key-like",
    "circular text f57v",
    "f49v margin",
    "f66r word list",
    "picnic table",      # Zandbergen's "picnic table" symbol = possibly @NNN?
]

VOYNICH_NU_PAGES = [
    "https://www.voynich.nu/writing.html",      # Zandbergen writing system
    "https://www.voynich.nu/transcr.html",       # transcription notes
    "https://www.voynich.nu/f57v.html",          # f57v folio page
    "https://www.voynich.nu/f66r.html",          # f66r folio page
    "https://www.voynich.nu/f49v.html",          # f49v folio page
]

print("Experiment exp_018: @Glyph Prior Work Check")
print("See result.md for full findings.")
