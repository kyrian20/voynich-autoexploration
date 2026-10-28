#!/usr/bin/env python3
"""Regression tests for non-destructive IVTFF ligature views."""
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scripts.audit_ivtff_ligature_views as ligature_audit
from scripts.audit_ivtff_ligature_views import tokenize_views, summarize_lines, TEXT_LINE, legacy_parser_coverage


def main() -> None:
    # Some valid folio-line IDs include a subdivision digit (e.g. f67r1.5).
    assert TEXT_LINE.match("<f1r.1,@P0> daiin"), "basic IVTFF line ID not parsed"
    assert TEXT_LINE.match("<f67r1.5,@Cc> daiin"), "subdivided folio line ID not parsed"
    assert TEXT_LINE.match("<fRos.23,@L0> daiin"), "Rosetta folio line ID not parsed"
    legacy = legacy_parser_coverage("<f1r.1,@P0> daiin\n<f67r1.5,@Cc> daiin\n<fRos.23,@L0> daiin")
    assert legacy["nonempty_token_lines"] == 1, legacy
    assert legacy["tokens"] == 1, legacy

    views = tokenize_views("dai{ch}in daiin {y'}")
    assert views["historical"] == ["dai", "in", "daiin"], views
    assert views["expanded"] == ["daichin", "daiin", "y"], views
    assert [u["kind"] for u in views["atomic_units"]] == [
        "word", "ligature", "word", "word", "ligature"
    ], views
    assert views["atomic_units"][1]["raw"] == "{ch}", views
    assert views["atomic_units"][1]["start"] == 3, views
    assert views["atomic_units"][1]["end"] == 7, views
    assert views["atomic_units"][1]["raw_start"] == 3, views
    assert views["atomic_units"][1]["raw_end"] == 7, views

    tagged = tokenize_views("<!note> dai{ch}in")
    tagged_ligature = next(u for u in tagged["atomic_units"] if u["kind"] == "ligature")
    assert tagged_ligature["raw_start"] == 11, tagged
    assert tagged_ligature["raw_end"] == 15, tagged

    # The baseline-style uncertainty filter excludes ligatures nested inside
    # square-bracket annotations; this is reported separately in the audit.
    bracketed = tokenize_views("daiin [{ch}:foo]")
    assert bracketed["historical"] == ["daiin"], bracketed
    assert not any(u["kind"] == "ligature" for u in bracketed["atomic_units"]), bracketed

    lines = [
        {"folio": "f1r", "line": 1, "body": "dai{ch}in daiin"},
        {"folio": "f1r", "line": 2, "body": "daiin daiin"},
    ]
    summary = summarize_lines(lines)
    assert summary["text_lines"] == 2, summary
    assert summary["lines_with_ligatures"] == 1, summary
    assert summary["ligature_spans"] == 1, summary
    assert summary["exact_daiin_occurrences"]["historical"] == 3, summary
    assert summary["exact_daiin_occurrences"]["expanded"] == 3, summary
    assert summary["lines_changed_vs_historical"]["atomic"] == 1, summary
    assert summary["lines_changed_vs_historical"]["expanded"] == 1, summary
    # The old splitlines() reader could promote a record embedded in a
    # comment via U+2028 (and seven other separators) into a false record.
    # Verify both the legacy comparator and the full descriptive audit reject
    # such sources rather than publishing contaminated token counts.
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "synthetic.ivtff"
        clean = "<f1r> <! $L=A>\n<f1r.1,@P0> daiin\n"
        with patch.object(ligature_audit, "ROOT", root):
            for newline in ("\n", "\r\n", "\r"):
                source.write_bytes(clean.replace("\n", newline).encode("utf-8"))
                verified = ligature_audit.audit_source("synthetic", source)
                assert verified["text_lines"] == 1, verified
                assert verified["exact_daiin_occurrences"]["historical"] == 1, verified

            for separator in "\v\f\x1c\x1d\x1e\x85\u2028\u2029":
                contaminated = (
                    "<f1r> <! $L=A>\n"
                    "# comment" + separator + "<f1r.1,@P0> daiin\n"
                    "<f1r.2,@P0> chedy\n"
                )
                source.write_bytes(contaminated.encode("utf-8"))
                try:
                    legacy_parser_coverage(contaminated)
                except ValueError as exc:
                    assert "Non-physical IVTFF line separator" in str(exc), exc
                else:
                    raise AssertionError("Legacy comparison accepted a forged physical row")
                try:
                    ligature_audit.audit_source("synthetic", source)
                except ValueError as exc:
                    assert "invalid IVTFF page/locus structure" in str(exc), exc
                else:
                    raise AssertionError("Ligature audit accepted a forged IVTFF record")

            # The historical broad regex matches this malformed tag, but the
            # independent structural audit must reject its missing delimiter.
            source.write_text(
                "<f1r> <! $L=A>\n<f1r.1,@P0>garbage\n", encoding="utf-8"
            )
            try:
                ligature_audit.audit_source("synthetic", source)
            except ValueError as exc:
                assert "invalid IVTFF page/locus structure" in str(exc), exc
            else:
                raise AssertionError("Malformed IVTFF locus was counted as text")

    print("IVTFF ligature view regression tests passed.")


if __name__ == "__main__":
    main()
