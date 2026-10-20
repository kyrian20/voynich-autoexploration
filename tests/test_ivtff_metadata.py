"""Regression tests for IVTFF Currier-language metadata parsing.

Run from the repository root:
    python tests/test_ivtff_metadata.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_ivtff_metadata import HEADER, parse_currier_language


def check(metadata: str, expected: str | None) -> None:
    actual = parse_currier_language(metadata)
    assert actual == expected, f"{metadata!r}: expected {expected!r}, got {actual!r}"


def main() -> None:
    # $L wins even when $Q contradicts it; $Q means quire, not Currier language.
    check("<! $Q=A $L=B>", "B")
    check("<! $Q=B $L=A>", "A")

    # A terminal $L value immediately before the closing '>' is valid.
    header = HEADER.match("<f1r> <! $Q=A $L=B>")
    assert header is not None
    check(header.group(2), "B")

    # Never infer Currier language from quire ($Q) or illustration ($I).
    check("<! $Q=A $I=B>", None)
    check("<! $I=A>", None)

    # Only A/B are accepted as Currier language values.
    check("<! $L=C>", None)
    check("<! $L=A>", "A")
    print("IVTFF metadata regression tests passed (7 assertions).")


if __name__ == "__main__":
    main()
