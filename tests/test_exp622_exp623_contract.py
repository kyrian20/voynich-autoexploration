"""Synthetic contract checks; no Voynich corpus or scientific claims involved."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MatchedInteractionContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = [
            load_script("exp622_ch_sh_specificity.py"),
            load_script("exp623_it2a_ch_sh_specificity.py"),
        ]

    @staticmethod
    def record(folio, length, position, label, prev, following):
        return {
            "folio": folio, "length": length, "position": position,
            "label": label, "prev_vowel": prev, "next_vowel": following,
        }

    def test_only_strata_with_both_labels(self):
        records = [
            self.record("1r", 5, 1, "ch", False, False),
            self.record("1r", 5, 1, "sh", False, True),
            self.record("2r", 5, 1, "ch", False, True),
            self.record("1r", 6, 1, "sh", False, True),
        ]
        for module in self.modules:
            with self.subTest(script=module.__name__):
                result = module.interaction(records)
                self.assertEqual(len(result), 1)
                self.assertAlmostEqual(result[0][1], 1.0)
                self.assertAlmostEqual(result[0][2], 1.0)
                self.assertAlmostEqual(result[0][3], 0.0)

    def test_preceding_control_subtracted(self):
        records = [
            self.record("1r", 5, 1, "ch", False, False),
            self.record("1r", 5, 1, "sh", True, True),
        ]
        for module in self.modules:
            with self.subTest(script=module.__name__):
                result = module.interaction(records)
                self.assertEqual(len(result), 1)
                self.assertAlmostEqual(result[0][1], 0.0)
                self.assertAlmostEqual(result[0][2], 1.0)
                self.assertAlmostEqual(result[0][3], 1.0)

    def test_equal_weight_per_matched_stratum(self):
        records = [
            self.record("1r", 5, 1, "ch", False, False),
            self.record("1r", 5, 1, "sh", False, True),
            self.record("2r", 5, 1, "ch", False, True),
            self.record("2r", 5, 1, "sh", False, False),
        ]
        for module in self.modules:
            with self.subTest(script=module.__name__):
                contrasts = module.interaction(records)
                self.assertEqual(len(contrasts), 2)
                self.assertAlmostEqual(sum(x[1] for x in contrasts) / len(contrasts), 0.0)


if __name__ == "__main__":
    unittest.main()
