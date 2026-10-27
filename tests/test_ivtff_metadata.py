"""Regression tests for IVTFF Currier-language metadata parsing.

Run from the repository root:
    python tests/test_ivtff_metadata.py
"""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_ivtff_metadata import HEADER, SOURCE, collect_folio_languages, parse_currier_language
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


def check_duplicate_folio_headers() -> None:
    # A repeated header silently overwrote the previous $L assignment.
    # Detect both conflicting and identical repetitions, even when the first
    # header lacks $L; panels and the named Rosettes page are separate IDs.
    clean = "<f1r> <! $L=A>\\n<f67r1> <! $L=B>\\n<fRos> <! $Q=A>\\n"
    pages, missing, count = collect_folio_languages(clean)
    assert pages == {"f1r": "A", "f67r1": "B"}, pages
    assert missing == ["fRos"], missing
    assert count == 3, count

    for page in ("f1r", "f67r1", "fRos"):
        for first in ("<! $L=A>", "<! $Q=A>"):
            for second in ("<! $L=A>", "<! $L=B>"):
                duplicated = f"<{page}> {first}\\n<{page}> {second}\\n"
                try:
                    collect_folio_languages(duplicated)
                except ValueError as exc:
                    assert f"Duplicate IVTFF folio header {page} at line 2" in str(exc), str(exc)
                else:
                    raise AssertionError(f"Duplicate IVTFF header accepted: {duplicated!r}")

    # The original ZL3b source is frozen. A regression must not silently
    # change its page census while strengthening validation.
    original = SOURCE.read_bytes().decode("utf-8-sig")
    _, _, original_count = collect_folio_languages(original)
    assert original_count == 227, original_count


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

    check_duplicate_folio_headers()
    check_tokenizers()
    check_brace_inventory()
    print("IVTFF metadata and tokenizer regression tests passed.")


if __name__ == "__main__":
    main()
