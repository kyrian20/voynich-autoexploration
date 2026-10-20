"""Regression tests for IVTFF Currier-language metadata parsing.

Run from the repository root:
    python tests/test_ivtff_metadata.py
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_ivtff_metadata import HEADER, parse_currier_language
from scripts.exp590_daiin_position import load_lines
from experiments.exp_602_independent_ivtff_parser_audit.script import tokens_regex, tokens_scanner


def check(metadata: str, expected: str | None) -> None:
    actual = parse_currier_language(metadata)
    assert actual == expected, f"{metadata!r}: expected {expected!r}, got {actual!r}"


def check_tokenizers() -> None:
    # IVTFF free-text comments terminate at ">", not the nonstandard "?>".
    # This regression catches the old Parser B behavior that swallowed the
    # remainder of a line after encountering a normal <! ... > comment.
    body = "alpha <! $Q=A $L=B> beta <@X=y> gamma {ch} [daiin:dain] @12; omega"
    expected = ["alpha", "beta", "gamma", "daiin", "omega"]
    assert tokens_regex(body) == expected, tokens_regex(body)
    assert tokens_scanner(body) == expected, tokens_scanner(body)

    # A bracketed alternative embedded in a word is spliced inline under the
    # primary-first-alternative policy; it must not become a separate token.
    embedded = "yk[eee:ech]o.[r:s]orarydaiin.cho[?:ch]os"
    assert tokens_regex(embedded) == ["ykeeeo", "rorarydaiin"], tokens_regex(embedded)
    assert tokens_scanner(embedded) == ["ykeeeo", "rorarydaiin"], tokens_scanner(embedded)

    # The first alternative may itself contain IVTFF annotations that are
    # normalized after bracket expansion (braces and @number markers).
    annotated = "qote[{ci}:a]r qok[{oh}:ch]or [@152;:d]ar dai[{cto}:@194;]y"
    expected_annotated = ["qote", "r", "qok", "or", "ar", "dai", "y"]
    assert tokens_regex(annotated) == expected_annotated, tokens_regex(annotated)
    assert tokens_scanner(annotated) == expected_annotated, tokens_scanner(annotated)


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

    # Exercise the real EXP-590 loader: $L overrides a contradictory $Q,
    # and a page without $L remains unknown rather than inheriting $Q.
    fixture = (
        "#=IVTFF Eva- 2.0 M\n"
        "<f1r> <! $Q=A $L=B>\n"
        "<f1r.1,@P0> daiin.foo\n"
        "<f2r> <! $Q=A>\n"
        "<f2r.1,@P0> daiin.bar\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "fixture.ivtff"
        path.write_text(fixture, encoding="utf-8")
        _, rows = load_lines(path)
    assert rows[0]["currier"] == "B", rows[0]
    assert rows[1]["currier"] == "unknown", rows[1]

    check_tokenizers()
    print("IVTFF metadata and tokenizer regression tests passed.")


if __name__ == "__main__":
    main()
