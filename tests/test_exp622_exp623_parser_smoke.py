"""Minimal IVTFF parser smoke tests; not a full IVTFF conformance suite."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name[:-3], ROOT / "scripts" / name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ParserSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = [load("exp622_ch_sh_specificity.py"),
                       load("exp623_it2a_ch_sh_specificity.py")]

    def parse_text(self, module, text):
        with TemporaryDirectory() as d:
            path = Path(d) / "sample.txt"
            path.write_text(text, encoding="utf-8")
            with patch.object(module, "SOURCE", path):
                return module.parse()[1]

    def test_line_header_and_two_sided_context(self):
        sample = "<f1r.1> achai ashai\n<f1r.2> chai shai\n<f2v.1> ochoy\n"
        for module in self.modules:
            with self.subTest(module=module.__name__):
                rows = self.parse_text(module, sample)
                self.assertEqual(len(rows), 3)
                self.assertEqual([(r["folio"], r["label"]) for r in rows],
                                 [("1r", "ch"), ("1r", "sh"), ("2v", "ch")])

    def test_nontext_headers_ignored(self):
        sample = "<f1r> $L=A\n# commentary achai\n<f1r.1> achai\n"
        for module in self.modules:
            with self.subTest(module=module.__name__):
                rows = self.parse_text(module, sample)
                self.assertEqual(len(rows), 1)

    def test_editorial_markup_excluded(self):
        sample = "<f1r.1> [achai] {ashai} <note> achai\n"
        for module in self.modules:
            with self.subTest(module=module.__name__):
                rows = self.parse_text(module, sample)
                self.assertEqual(len(rows), 1)


if __name__ == "__main__":
    unittest.main()
