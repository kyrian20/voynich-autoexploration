"""Literal equal-after-one-deletion-per-word filter (Zhang–Sheng v2).

Independent of the frozen 2026-11-01 Levenshtein audit. No claim is made
that this reproduces the paper's unpublished propensity correction.
"""

import re

DIGRAPHS = ('cth', 'ckh', 'cph', 'cfh', 'ch', 'sh')
OPAQUE_CODE = re.compile(r'@[0-9]{3};')


def eva_glyphs(word):
    """Tokenize EVA digraphs and opaque @NNN; units as in the frozen reader."""
    out = []
    i = 0
    while i < len(word):
        opaque = OPAQUE_CODE.match(word, i)
        if opaque:
            out.append(opaque.group(0))
            i = opaque.end()
            continue
        glyph = next((g for g in DIGRAPHS if word.startswith(g, i)), None)
        if glyph is None:
            glyph = word[i]
        out.append(glyph)
        i += len(glyph)
    return tuple(out)


def equal_after_one_deletion_each(a, b):
    """True iff deleting exactly one glyph from EACH word yields equality.

    The empty string is not a one-glyph word; identical words are excluded
    separately by the historical audit and are not needed for pair scoring.
    """
    x, y = eva_glyphs(a), eva_glyphs(b)
    if not x or len(x) != len(y):
        return False
    return bool({x[:i] + x[i+1:] for i in range(len(x))} &
                {y[:j] + y[j+1:] for j in range(len(y))})
