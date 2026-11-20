"""Synthetic EXP-593 parser regressions: duplicated folio/line loci fail closed."""
import unittest
from unittest.mock import patch
from scripts import exp593_daiin_variants as exp


class Source:
    def __init__(self, raw):
        self.raw = raw

    def read_bytes(self):
        return self.raw


class DuplicateLocusTests(unittest.TestCase):
    def test_duplicate_locus_rejected_before_statistics(self):
        raw = b"<f1r> $L=A\n<f1r.1,foo> daiin.dain\n<f1r.1,bar> daiin\n"
        with patch.object(exp, "SOURCE", Source(raw)):
            with self.assertRaisesRegex(ValueError, "duplicate folio/line locus: f1r.1"):
                exp.parse()

    def test_distinct_loci_retained(self):
        raw = b"<f1r> $L=A\n<f1r.1,foo> daiin\n<f1r.2,foo> dain\n"
        with patch.object(exp, "SOURCE", Source(raw)):
            result_raw, lines = exp.parse()
        self.assertEqual(result_raw, raw)
        self.assertEqual([(row["folio"], row["line"]) for row in lines],
                         [("f1r", 1), ("f1r", 2)])


if __name__ == "__main__":
    unittest.main()
