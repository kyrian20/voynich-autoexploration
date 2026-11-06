"""Literal equal-after-one-deletion-per-word filter (Zhang–Sheng v2).

Independent of the frozen 2026-11-01 Levenshtein audit. No claim is made
that this reproduces the paper's unpublished propensity correction.
"""

DIGRAPHS = ('cth', 'ckh', 'cph', 'cfh', 'ch', 'sh')


def eva_glyphs(word):
    """Tokenize the six conventional multi-character EVA glyphs atomically."""
    out = []
    i = 0
    while i < len(word):
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
