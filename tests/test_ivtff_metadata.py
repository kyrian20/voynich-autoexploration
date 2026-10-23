"""Regression tests for IVTFF Currier-language metadata parsing.

Run from the repository root:
    python tests/test_ivtff_metadata.py
"""
import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.audit_ivtff_metadata as metadata_module
from scripts.audit_ivtff_metadata import HEADER, parse_currier_language
from scripts.exp590_daiin_position import load_lines
from experiments.exp_602_independent_ivtff_parser_audit.script import tokens_regex, tokens_scanner
from scripts.audit_ivtff_brace_spans import audit_text


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

    # Empty first alternatives are meaningful: [:y] selects the empty primary
    # reading rather than invalidating the surrounding token.
    empty_primary = "okaiin[:y] otold[:y] chockh[:y]"
    expected_empty_primary = ["okaiin", "otold", "chockh"]
    assert tokens_regex(empty_primary) == expected_empty_primary, tokens_regex(empty_primary)
    assert tokens_scanner(empty_primary) == expected_empty_primary, tokens_scanner(empty_primary)

    # Historical compatibility behavior only (not normative conformance):
    # the lossless lexer flags missing alternative separators. This legacy view
    # treats a bracket without alternatives as one primary reading that is
    # spliced inline. An unmatched bracket is conservatively excluded.
    single_reading = "pre[uncertain]post"
    assert tokens_regex(single_reading) == ["preuncertainpost"], tokens_regex(single_reading)
    assert tokens_scanner(single_reading) == ["preuncertainpost"], tokens_scanner(single_reading)
    malformed = "prefix[unfinished"
    assert tokens_regex(malformed) == [], tokens_regex(malformed)
    assert tokens_scanner(malformed) == [], tokens_scanner(malformed)

    # Paragraph markers and drawing interruptions are structural separators,
    # not lexical characters.
    marked = "<%>alpha.beta<->gamma<~>delta<$>"
    expected_marked = ["alpha", "beta", "gamma", "delta"]
    assert tokens_regex(marked) == expected_marked, tokens_regex(marked)
    assert tokens_scanner(marked) == expected_marked, tokens_scanner(marked)


def check_brace_inventory() -> None:
    # Inventory only: letters inside braces are recorded, not presumed lexical.
    report = audit_text("# editorial note }\ndai{ch}in {abc def} x} {open")
    assert report["brace_span_count"] == 2, report
    assert report["spans_with_ascii_letters"] == 2, report
    assert report["spans_with_whitespace"] == 1, report
    assert report["unmatched_close_brace_count"] == 1, report
    assert report["unmatched_open_brace_count"] == 1, report
    assert report["distinct_contents"] == 2, report
    assert report["ignored_hash_comment_lines"] == 1, report

    # IVTFF 2.0.2 §6.6 requires each ligature to close on the same line.
    cross_line = audit_text("{open\nclose}")
    assert cross_line["brace_span_count"] == 0, cross_line
    assert cross_line["unmatched_open_brace_count"] == 1, cross_line
    assert cross_line["unmatched_close_brace_count"] == 1, cross_line


def check_repeated_page_header_conflicts() -> None:
    # A repeated page with the same $L is harmless; conflicting labels must
    # fail rather than silently allowing the last header to overwrite the first.
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "fixture.ivtff"
        headers = [
            f"<f{i}r> <! $L={'A' if i % 2 else 'B'}>"
            for i in range(1, 102)
        ]
        headers.append("<f1r> <! $L=A>")
        source.write_text("\\n".join(headers) + "\\n", encoding="utf-8")
        output = io.StringIO()
        with (patch.object(metadata_module, "ROOT", root),
              patch.object(metadata_module, "SOURCE", source),
              contextlib.redirect_stdout(output)):
            metadata_module.main()
        report = json.loads(output.getvalue())
        assert report["folios_with_currier_language"] == 101, report
        assert report["folio_headers"] == 102, report

        headers.append("<f1r> <! $L=B>")
        source.write_text("\\n".join(headers) + "\\n", encoding="utf-8")
        with (patch.object(metadata_module, "ROOT", root),
              patch.object(metadata_module, "SOURCE", source),
              contextlib.redirect_stdout(io.StringIO())):
            try:
                metadata_module.main()
            except ValueError as exc:
                assert "Conflicting Currier $L across headers for f1r" in str(exc), exc
            else:
                raise AssertionError("Contradictory page metadata silently overwritten")


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
    for page in ('f67r1', 'f86v6', 'fRos'):
        assert HEADER.match(f'<{page}> <! $L=B>') is not None, page
    try:
        parse_currier_language('<! $L=A $L=B>')
    except ValueError:
        pass
    else:
        raise AssertionError('Contradictory Currier labels accepted')

    # Report the exact loader file used by this run to diagnose stale-checkout mismatches.
    import scripts.exp590_daiin_position as exp590_module
    print(f"EXP-590 loader under test: {Path(exp590_module.__file__).resolve()}")

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

    check_repeated_page_header_conflicts()
    check_tokenizers()
    check_brace_inventory()
    print("IVTFF metadata and tokenizer regression tests passed.")


if __name__ == "__main__":
    main()
