"""Synthetic tests for prospective split, without reading real corpus."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "prepare_prospective_leaf_holdout.py"
spec = importlib.util.spec_from_file_location("prospective_leaf_holdout", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def corpus(leaves, reverse=False):
    lines = [f"<f{leaf}{side}.1,+P0> daiin" for leaf in leaves for side in ("r", "v")]
    if reverse:
        lines.reverse()
    return ("\n".join(lines) + "\n").encode()


class ProspectiveHoldoutContract(unittest.TestCase):
    def test_recto_verso_grouped_and_metadata_ignored(self):
        self.assertEqual(module.leaves_from_bytes(b"<f1r.1,+P0> a\n<f1v.2,+P0> b\n"), {1})
        self.assertEqual(module.leaves_from_bytes(b"<f2r> $L=A\n<f2v.1> abc\n"), {2})

    def test_fixed_assignment_independent_of_row_order(self):
        a = module.build_manifest({"eva_zl3b.txt": corpus(range(1, 151)),
                                   "eva_it2a.txt": corpus(range(1, 151), True)})
        b = module.build_manifest({"eva_zl3b.txt": corpus(range(1, 151), True),
                                   "eva_it2a.txt": corpus(range(1, 151))})
        self.assertEqual(a["partitions"], b["partitions"])
        self.assertNotEqual(a["corpora"]["eva_zl3b.txt"]["sha256"],
                            b["corpora"]["eva_zl3b.txt"]["sha256"])
        sets = [set(x) for x in a["partitions"].values()]
        self.assertEqual(len(set.union(*sets)), 150)
        self.assertEqual(sum(map(len, sets)), 150)

    def test_only_shared_leaves_eligible(self):
        a = module.build_manifest({"eva_zl3b.txt": corpus(range(1, 151)),
                                   "eva_it2a.txt": corpus(range(20, 171))})
        self.assertEqual(a["eligible_count"], 131)
        self.assertEqual(a["source_only_leaves"]["eva_zl3b.txt"], list(range(1, 20)))
        self.assertEqual(a["source_only_leaves"]["eva_it2a.txt"], list(range(151, 171)))

    def test_reject_bad_input_and_weak_coverage(self):
        with self.assertRaises(ValueError):
            module.leaves_from_bytes(b"# no folios\n")
        with self.assertRaises(ValueError):
            module.partition(0)
        with self.assertRaises(ValueError):
            module.build_manifest({"eva_zl3b.txt": corpus(range(1, 100))})
        with self.assertRaises(ValueError):
            module.build_manifest({"eva_zl3b.txt": corpus(range(1, 30)),
                                   "eva_it2a.txt": corpus(range(1, 30))})


if __name__ == "__main__":
    unittest.main()
