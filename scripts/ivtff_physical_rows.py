#!/usr/bin/env python3
"""Strict physical-row iterator for additive IVTFF metadata audits.

Only CR, LF and CRLF delimit source records. Python str.splitlines() also
splits on Unicode/control separators that can forge folio headers inside a
single physical row. Reject those bytes/characters rather than normalizing
them into accepted metadata. This is not full IVTFF conformance.
"""
from __future__ import annotations

NON_PHYSICAL_SEPARATORS = frozenset("\v\f\x1c\x1d\x1e\x85\u2028\u2029")


def checked_physical_lines(text: str):
    """Yield (1-based physical line number, row), failing on fake delimiters."""
    if not isinstance(text, str):
        raise TypeError("IVTFF source must be decoded text")
    for number, row in enumerate(
        text.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1
    ):
        invalid = sorted({ord(char) for char in row if char in NON_PHYSICAL_SEPARATORS})
        if invalid:
            codepoints = ", ".join(f"U+{code:04X}" for code in invalid)
            raise ValueError(
                f"Non-physical IVTFF line separator at line {number}: {codepoints}"
            )
        yield number, row
