"""Synthetic IVTFF page-ID coverage regression for EXP-593 (no science run)."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import exp593_daiin_variants as exp


class PageIdCoverageTests(unittest.TestCase):
    def test_subdivided_and_ros_folios_preserve_currier_and_positions(self):
        fixture = """<f1r> <! $L=A>
<f1r.1,@P0> daiin ol
<f67r1> <! $L=B>
<f67r1.5,@Cc> dain qok
<fRos> <! $L=B>
<fRos.23,@L0> daiiin chody
"""
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text(fixture, encoding="utf-8")
            with patch.object(exp, "SOURCE", source):
                raw, lines = exp.parse()
        self.assertEqual(raw, fixture.encode("utf-8"))
        self.assertEqual(
            [(r["folio"], r["line"], r["currier"], r["tokens"][0]) for r in lines],
            [("f1r", 1, "A", "daiin"),
             ("f67r1", 5, "B", "dain"),
             ("fRos", 23, "B", "daiiin")],
        )

    def test_duplicate_subdivided_locus_fails_closed(self):
        fixture = """<f67r1> <! $L=B>
<f67r1.5,@Cc> daiin qok
<f67r1.5,@Cc> dain qok
"""
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text(fixture, encoding="utf-8")
            with patch.object(exp, "SOURCE", source):
                with self.assertRaisesRegex(ValueError, "duplicate folio/line locus"):
                    exp.parse()


if __name__ == "__main__":
    unittest.main()
