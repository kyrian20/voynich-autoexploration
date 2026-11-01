"""Cross-stratum physical-leaf regression for LIB-EXP-624 allocation only."""
import copy
import unittest

from scripts import prepare_library_exp624_joint_strata as joint
from scripts import prepare_library_exp624_leaf_grouped_splits as grouped


class JointStrataTests(unittest.TestCase):
    def setUp(self):
        # Every leaf has A on recto and B on verso: independent stratum
        # shuffles cannot be assumed safe when pooled.
        self.pages = [
            {"id": f"f{i}{side}", "lang": lang, "words": ["ab"]}
            for i in range(1, 7)
            for side, lang in (("r", "A"), ("v", "B"))
        ]

    def test_one_global_partition_preserves_cross_stratum_leaf_independence(self):
        rows = grouped.grouped_splits(self.pages, 624010, 8)
        result = joint.derive_joint_strata(self.pages, rows)
        self.assertEqual(len(result), 8)
        for row in result:
            train = set(row["train_leaves"])
            test = set(row["test_leaves"])
            self.assertFalse(train & test)
            self.assertEqual(train | test, set(range(1, 7)))
            for name in ("A", "B"):
                part = row["strata"][name]
                self.assertEqual(part["train_leaves"], sorted(train))
                self.assertEqual(part["test_leaves"], sorted(test))
                self.assertEqual(part["train_page_count"] + part["test_page_count"], 6)
            self.assertEqual(row["strata"]["unclassified"]["train_page_count"], 0)
            self.assertEqual(row["strata"]["unclassified"]["test_page_count"], 0)
            self.assertEqual(row["cross_stratum_shared_train_test_leaves"], [])

    def test_reject_cross_stratum_leak_even_when_page_sets_partition(self):
        row = grouped.grouped_splits(self.pages, 624010, 1)[0]
        broken = copy.deepcopy(row)
        # Move B verso to test while A recto of same physical leaf stays train.
        leaf = broken["train_leaves"][0]
        page = f"f{leaf}v"
        broken["train_page_ids"].remove(page)
        broken["test_page_ids"].append(page)
        with self.assertRaisesRegex(ValueError, "Cross-stratum physical-leaf leakage"):
            joint.derive_joint_strata(self.pages, [broken])

    def test_reject_duplicate_or_missing_page_allocation(self):
        row = grouped.grouped_splits(self.pages, 624010, 1)[0]
        duplicated = copy.deepcopy(row)
        duplicated["test_page_ids"].append(duplicated["train_page_ids"][0])
        with self.assertRaisesRegex(ValueError, "does not partition"):
            joint.derive_joint_strata(self.pages, [duplicated])
        missing = copy.deepcopy(row)
        missing["test_page_ids"].pop()
        with self.assertRaisesRegex(ValueError, "does not partition"):
            joint.derive_joint_strata(self.pages, [missing])

    def test_reject_leak_free_partition_not_generated_by_claimed_seed(self):
        # Swap entire physical leaves, preserving every disjointness,
        # coverage, count, and per-stratum invariant. Only RNG provenance fails.
        original = grouped.grouped_splits(self.pages, 624010, 1)[0]
        forged = copy.deepcopy(original)
        train_leaf, test_leaf = forged["train_leaves"][0], forged["test_leaves"][0]
        forged["train_leaves"] = sorted(
            (set(forged["train_leaves"]) - {train_leaf}) | {test_leaf})
        forged["test_leaves"] = sorted(
            (set(forged["test_leaves"]) - {test_leaf}) | {train_leaf})
        forged["train_page_ids"] = sorted(
            p["id"] for p in self.pages
            if grouped.leaf_id(p["id"]) in forged["train_leaves"])
        forged["test_page_ids"] = sorted(
            p["id"] for p in self.pages
            if grouped.leaf_id(p["id"]) in forged["test_leaves"])
        forged["train_page_count"] = len(forged["train_page_ids"])
        forged["test_page_count"] = len(forged["test_page_ids"])
        self.assertFalse(set(forged["train_leaves"]) & set(forged["test_leaves"]))
        self.assertEqual(
            set(forged["train_page_ids"]) | set(forged["test_page_ids"]),
            {p["id"] for p in self.pages})
        with self.assertRaisesRegex(ValueError, "deterministic seed"):
            joint.derive_joint_strata(self.pages, [forged])
        # The actual seeded assignment must still be accepted.
        self.assertEqual(len(joint.derive_joint_strata(self.pages, [original])), 1)

    def test_reject_noninteger_claimed_seed(self):
        original = grouped.grouped_splits(self.pages, 624010, 1)[0]
        for forged_seed in ("624010", True, 624010.0, None):
            with self.subTest(seed=forged_seed):
                forged = copy.deepcopy(original)
                forged["seed"] = forged_seed
                with self.assertRaisesRegex(ValueError, "seed must be an integer"):
                    joint.derive_joint_strata(self.pages, [forged])

    def test_direct_joint_allocation_rejects_physical_page_aliases(self):
        row = grouped.grouped_splits(self.pages, 624010, 1)[0]
        aliased = self.pages + [{"id": "f01R", "lang": "A", "words": ["ab"]}]
        with self.assertRaisesRegex(ValueError, "Duplicate physical page identity"):
            joint.derive_joint_strata(aliased, [row])

    def test_frozen_corpora_and_allocation_are_gated(self):
        sources = {name: (joint.ROOT / "data/transcriptions" / filename).read_bytes()
                   for name, (filename, _) in grouped.historical.SOURCES.items()}
        report = joint.build(sources)
        self.assertEqual(report["status"], "ALLOCATION_ONLY_BLOCKED_FOR_SCIENTIFIC_SCORING")
        self.assertFalse(report["historical_model_executed"])
        self.assertFalse(report["metrics_rehabilitated"])
        self.assertEqual(len(report["joint_allocations"]), 8)
        self.assertEqual([r["seed"] for r in report["joint_allocations"]],
                         [624010 + i * 7919 for i in range(8)])
        for row in report["joint_allocations"]:
            self.assertFalse(set(row["train_leaves"]) & set(row["test_leaves"]))
            self.assertEqual(
                {name: p["train_page_count"] + p["test_page_count"]
                 for name, p in row["strata"].items()},
                {"A": 114, "B": 81, "unclassified": 8},
            )
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            joint.build({"ZL3b": b"altered", "IT2a": sources["IT2a"]})


if __name__ == "__main__":
    unittest.main()
