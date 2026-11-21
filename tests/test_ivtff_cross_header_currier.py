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


if __name__ == "__main__":
    unittest.main()
