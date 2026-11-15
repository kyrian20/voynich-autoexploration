import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/replay_exp580_label_counts.py"
spec = importlib.util.spec_from_file_location("exp580_replay", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class LabelCountReplayTests(unittest.TestCase):
    def test_extract_known_counts(self):
        output = "\n".join(f"{name}: {n}" for name, n in module.EXPECTED.items())
        self.assertEqual(module.extract(output), module.EXPECTED)

    def test_detect_arithmetic_error(self):
        output = "\n".join(f"{name}: {n + (1 if name == 'Label-exclusive types' else 0)}"
                           for name, n in module.EXPECTED.items())
        with self.assertRaises(ValueError):
            module.extract(output)

    def test_detect_missing_metric(self):
        with self.assertRaises(ValueError):
            module.extract("Label types: 1036")

if __name__ == "__main__":
    unittest.main()
