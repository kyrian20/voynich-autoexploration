#!/usr/bin/env python3
"""Regression tests for non-destructive IVTFF ligature views."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_ivtff_ligature_views import tokenize_views, summarize_lines


def main() -> None:
    views = tokenize_views("dai{ch}in daiin {y'}")
    assert views["historical"] == ["dai", "in", "daiin"], views
    assert views["expanded"] == ["daichin", "daiin", "y"], views
    assert [u["kind"] for u in views["atomic_units"]] == [
        "word", "ligature", "word", "word", "ligature"
    ], views
    assert views["atomic_units"][1]["raw"] == "{ch}", views
    assert views["atomic_units"][1]["start"] == 3, views
    assert views["atomic_units"][1]["end"] == 7, views

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
    print("IVTFF ligature view regression tests passed.")


if __name__ == "__main__":
    main()
