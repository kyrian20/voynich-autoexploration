"""Deterministic preflight regressions; no corpus or EXP archive mutations."""
import tempfile
import unittest
from pathlib import Path
from scripts.audit_readiness_ascii_guard import SOURCES, audit_sources, scan_text


class ReadinessAsciiGuardTest(unittest.TestCase):
    def test_accepts_ascii_panel_and_rosettes(self):
        text = "<f68r3.12,@Ls> doaro\n<fRos.160,@P0> daiin\n"
        self.assertEqual(scan_text(text), 2)

    def test_rejects_nonascii_digits_in_all_id_positions(self):
        for row in (
            "<f٦8r3.12,@Ls> doaro",
            "<f68r٣.12,@Ls> doaro",
            "<f68r3.١٢,@Ls> doaro",
            "<fRos.٢3,@P0> daiin",
        ):
            with self.subTest(row=row), self.assertRaisesRegex(ValueError, "non-ASCII"):
                scan_text("<f1r.1,@P0> daiin\n" + row, "synthetic")

    def test_does_not_promote_unrelated_unicode_metadata(self):
        self.assertEqual(scan_text("# رقم ١٢\n<unrelated.١٢> text\n"), 0)

    def test_fail_closed_on_missing_corpus(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                audit_sources(Path(temp))

    def test_audit_provenance_and_failure_on_corrupted_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            directory = root / "data" / "transcriptions"
            directory.mkdir(parents=True)
            for name in SOURCES:
                (directory / name).write_text("<f1r.1,@P0> daiin\n", encoding="utf-8")
            report = audit_sources(root)
            self.assertEqual([f["candidate_row_prefixes_checked"] for f in report["files"]], [1] * 3)
            self.assertEqual(report["status"], "PASS")
            (directory / SOURCES[1]).write_text("<f1r.٢,@P0> daiin\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, SOURCES[1]):
                audit_sources(root)


if __name__ == "__main__":
    unittest.main()
