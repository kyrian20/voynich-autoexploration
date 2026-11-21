"""Synthetic regression for cross-header Currier $L contradictions (no corpus mutation)."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_ivtff_metadata.py"
spec = importlib.util.spec_from_file_location("audit_ivtff_metadata", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestCrossHeaderCurrier(unittest.TestCase):
    def test_identical_repeat_is_stable(self):
        pages = {}
        module.record_language(pages, "f1r", "A")
        module.record_language(pages, "f1r", "A")
        self.assertEqual(pages, {"f1r": "A"})

    def test_conflicting_repeat_is_rejected(self):
        pages = {}
        module.record_language(pages, "f1r", "A")
        with self.assertRaisesRegex(ValueError, "Conflicting IVTFF"):
            module.record_language(pages, "f1r", "B")
        self.assertEqual(pages, {"f1r": "A"})

    def test_different_folios_are_independent(self):
        pages = {}
        module.record_language(pages, "f1r", "A")
        module.record_language(pages, "f1v", "B")
        self.assertEqual(pages, {"f1r": "A", "f1v": "B"})


    def test_main_rejects_conflict_from_actual_header_scan(self):
        """Exercise the parser loop, not only the extracted helper."""
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text("<f1r> $L=A\n<f1r> $L=B\n", encoding="utf-8")
            with patch.object(module, "SOURCE", source):
                with self.assertRaisesRegex(ValueError, "Conflicting IVTFF"):
                    module.main()

    def test_main_accepts_repeated_consistent_headers(self):
        """A repeated header must not increase the unique folio count."""
        import contextlib
        import io
        import json
        import tempfile
        from unittest.mock import patch
        headers = [
            f"<f{number}r> $L={'A' if number <= 51 else 'B'}"
            for number in range(1, 102)
        ]
        headers.append("<f1r> $L=A")
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "synthetic.ivtff"
            source.write_text("\n".join(headers) + "\n", encoding="utf-8")
            output = io.StringIO()
            with patch.object(module, "SOURCE", source), contextlib.redirect_stdout(output):
                module.main()
            result = json.loads(output.getvalue())
            self.assertEqual(result["folio_headers"], 102)
            self.assertEqual(result["folios_with_currier_language"], 101)
            self.assertEqual(result["language_counts"], {"A": 51, "B": 50})

if __name__ == "__main__":
    unittest.main()
