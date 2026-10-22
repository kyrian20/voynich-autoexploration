#!/usr/bin/env python3
"""Regression test for EXP-590 coverage of valid IVTFF page identifiers."""
from pathlib import Path
import tempfile

from scripts.exp590_daiin_position import load_lines


def main() -> None:
    fixture = """<f1r> <! $L=A>
<f1r.1,@P0> daiin ol
<f67r1> <! $L=B>
<f67r1.5,@Cc> daiin qok
<fRos> <! $L=B>
<fRos.23,@L0> daiin chody
"""
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "fixture.txt"
        path.write_text(fixture, encoding="utf-8")
        _, lines = load_lines(path)

    assert len(lines) == 3, lines
    assert [line["folio"] for line in lines] == ["f1r", "f67r1", "fRos"], lines
    assert [line["line"] for line in lines] == [1, 5, 23], lines
    assert [line["currier"] for line in lines] == ["A", "B", "B"], lines
    assert all(line["tokens"][0] == "daiin" for line in lines), lines
    print("EXP-590 IVTFF page-ID regression tests passed.")


if __name__ == "__main__":
    main()
