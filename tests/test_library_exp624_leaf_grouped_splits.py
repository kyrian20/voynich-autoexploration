"""Regression of grouped physical-leaf allocation, not historical model scoring."""
import unittest
from unittest.mock import patch
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

    def test_seed_series_rejects_modulo_aliases_and_invalid_types(self):
        # The 32-bit LCG would otherwise produce identical shuffles for
        # seed and seed + 2**32 while recording different seed values.
        original = fixed.grouped_splits(self.pages, 624010, 1)[0]
        self.assertEqual(original["seed"], 624010)
        for invalid in (True, 624010.0, "624010", None):
            with self.subTest(seed=invalid), self.assertRaisesRegex(
                ValueError, "seed_base must be an integer"
            ):
                fixed.grouped_splits(self.pages, invalid, 1)
        for invalid in (-1, 2**32, 624010 + 2**32):
            with self.subTest(seed=invalid), self.assertRaisesRegex(
                ValueError, "seed_base outside unsigned 32-bit range"
            ):
                fixed.grouped_splits(self.pages, invalid, 1)
        for invalid in (True, 1.0, "1", None):
            with self.subTest(repetitions=invalid), self.assertRaisesRegex(
                ValueError, "repetitions must be an integer"
            ):
                fixed.grouped_splits(self.pages, 624010, invalid)
        with self.assertRaisesRegex(ValueError, "At least one repetition"):
            fixed.grouped_splits(self.pages, 624010, 0)
        with self.assertRaisesRegex(ValueError, "seed series exceeds unsigned 32-bit range"):
            fixed.grouped_splits(self.pages, 2**32 - 7919, 2)
        # Boundary control: the last permitted seed is exactly 2**32 - 1.
        rows = fixed.grouped_splits(self.pages, 2**32 - 7920, 2)
        self.assertEqual([r["seed"] for r in rows], [2**32 - 7920, 2**32 - 1])

    def test_source_hash_gate(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            fixed.build({"ZL3b": b"corrupt", "IT2a": b"corrupt"})

    def test_reject_cross_edition_currier_swap_with_same_aggregate_counts(self):
        # Adversarial reader discrepancy: identical frozen bytes and A/B totals,
        # but two eligible pages exchange $L labels in the IT2a projection.
        sources = {label: (fixed.ROOT / "data/transcriptions" / name).read_bytes()
                   for label, (name, _) in fixed.historical.SOURCES.items()}
        original_parse = fixed.historical.parse_pages

        def swapped_it2a(raw):
            pages = original_parse(raw)
            if raw == sources["IT2a"]:
                a = next(p for p in pages if p["lang"] == "A")
                b = next(p for p in pages if p["lang"] == "B")
                a["lang"], b["lang"] = b["lang"], a["lang"]
            return pages

        with patch.object(fixed.historical, "parse_pages", side_effect=swapped_it2a):
            with self.assertRaisesRegex(ValueError, r"per-page Currier [$]L metadata"):
                fixed.build(sources)

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
