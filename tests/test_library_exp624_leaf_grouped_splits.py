"""Regression of grouped physical-leaf allocation, not historical model scoring."""
import unittest
from scripts import prepare_library_exp624_leaf_grouped_splits as fixed


class LibraryExp624GroupedSplitTests(unittest.TestCase):
    def setUp(self):
        self.pages = [{"id": p, "lang": "A", "words": ["ab"]}
                      for p in ("f1r", "f1v", "f2r1", "f2v2", "f3r", "f3v", "f4r", "f4v")]

    def test_recto_verso_panels_never_cross_split(self):
        rows = fixed.grouped_splits(self.pages, 624010, 8)
        self.assertEqual(len(rows), 8)
        for row in rows:
            self.assertFalse(set(row["train_leaves"]) & set(row["test_leaves"]))
            self.assertEqual(set(row["train_page_ids"]) | set(row["test_page_ids"]),
                             {p["id"] for p in self.pages})
            for leaf in (1, 2, 3, 4):
                ids = {p["id"] for p in self.pages if fixed.leaf_id(p["id"]) == leaf}
                self.assertTrue(ids <= set(row["train_page_ids"]) or
                                ids <= set(row["test_page_ids"]))

    def test_repeatable_and_seed_changes(self):
        self.assertEqual(fixed.grouped_splits(self.pages, 624010, 8),
                         fixed.grouped_splits(list(reversed(self.pages)), 624010, 8))
        self.assertEqual([r["seed"] for r in fixed.grouped_splits(self.pages, 625010, 3)],
                         [625010, 632929, 640848])

    def test_fail_closed_unknown_and_duplicate(self):
        for bad in ("fRos", "f2r7", "f2rgarbage", "f١r", "f2r.1"):
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, "Unrecognized"):
                fixed.grouped_splits(self.pages + [{"id": bad}], 624010, 1)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            fixed.grouped_splits(self.pages + [self.pages[0]], 624010, 1)
        for alias in ("f01r", "f2R1", "f002v2"):
            with self.subTest(alias=alias), self.assertRaisesRegex(ValueError, "Duplicate physical page identity"):
                fixed.grouped_splits(self.pages + [{"id": alias, "lang": "A", "words": ["ab"]}], 624010, 1)
        self.assertEqual(fixed.physical_page_id("f002V2"), (2, "v", 2))
        with self.assertRaisesRegex(ValueError, "two distinct"):
            fixed.grouped_splits(self.pages[:2], 624010, 1)

    def test_source_hash_gate(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            fixed.build({"ZL3b": b"corrupt", "IT2a": b"corrupt"})

    def test_frozen_corpus_allocation(self):
        sources = {label: (fixed.ROOT / "data/transcriptions" / name).read_bytes()
                   for label, (name, _) in fixed.historical.SOURCES.items()}
        report = fixed.build(sources)
        self.assertEqual(report["status"], "BLOCKED_FOR_SCIENTIFIC_SCORING")
        self.assertFalse(report["model_executed"])
        self.assertEqual(set(report["results"]), {"ZL3b", "IT2a"})
        for label, item in report["results"].items():
            self.assertEqual(len(item["eligible_page_ids"]), 203)
            for group, rows in item["groups"].items():
                self.assertEqual(len(rows), 8 if group == "all" else 6)
                for row in rows:
                    self.assertFalse(set(row["train_leaves"]) & set(row["test_leaves"]))
                    self.assertTrue(row["train_page_ids"] and row["test_page_ids"])
                    self.assertEqual(row["train_page_count"] + row["test_page_count"],
                                     203 if group == "all" else (114 if group == "A" else 81))


if __name__ == "__main__":
    unittest.main()
