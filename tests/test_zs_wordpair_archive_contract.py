"""Guard the archived Zhang–Sheng partial-audit receipt against output drift.

The archive has 54 flat run_records; the original main() printed a different
nested schema. Only two preselected, frozen-source rows are recomputed here.
The other 52 rows are NOT certified by this bounded CI check.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "research/maintenance/2026-11-01-zs-wordpair-audit"
SPEC = importlib.util.spec_from_file_location("zs_wordpair_receipt", AUDIT_DIR / "wordpair_audit.py")
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Duplicate JSON key in frozen receipt: {key}")
        out[key] = value
    return out


def reject_nonfinite(value):
    raise ValueError(f"Nonfinite JSON constant in frozen receipt: {value}")


def load_archive():
    return json.loads(
        (AUDIT_DIR / "results.json").read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=reject_nonfinite,
    )


FIELDS = {
    "source", "view", "top_k", "seed", "shuffles", "pages", "lines",
    "tokens", "eligible_pairs", "raw_spearman",
    "additive_residual_spearman", "residual_pearson",
}
SOURCES = ("eva_zl3b.txt", "eva_it2a.txt")
VIEWS = ("split", "join", "legacy_ascii")
TOP_K = (150, 300, 600)
SEEDS = (20261101, 20261102, 20261103)


class WordPairArchiveContractTests(unittest.TestCase):
    def test_archive_grid_and_source_receipts(self):
        archive = load_archive()
        self.assertEqual(set(archive), {"status", "sources", "run_records"})
        self.assertEqual(archive["status"], "EXPLORATORY_PARTIAL_REIMPLEMENTATION")
        self.assertEqual(set(archive["sources"]), set(SOURCES))
        for source in SOURCES:
            self.assertEqual(
                archive["sources"][source],
                {"sha256": audit.SOURCE_LOCK[source][0],
                 "git_blob_sha": audit.SOURCE_LOCK[source][1]},
            )
        rows = archive["run_records"]
        self.assertEqual(len(rows), 54)
        observed = set()
        for row in rows:
            self.assertEqual(set(row), FIELDS)
            key = (row["source"], row["view"], row["top_k"], row["seed"])
            self.assertNotIn(key, observed, f"Repeated archived run: {key}")
            observed.add(key)
            self.assertEqual(row["shuffles"], 20)
            self.assertEqual(row["pages"], 225)
            for field in ("raw_spearman", "additive_residual_spearman", "residual_pearson"):
                self.assertTrue(math.isfinite(row[field]))
        expected = {(s, v, k, seed) for s in SOURCES for v in VIEWS
                    for k in TOP_K for seed in SEEDS}
        self.assertEqual(observed, expected)

    def test_flat_projection_is_compatible_with_frozen_schema(self):
        archived = load_archive()["run_records"][0]
        synthetic_metric = {
            "seed": archived["seed"], "shuffles": archived["shuffles"],
            "n_pages": archived["pages"], "n_lines": archived["lines"],
            "n_tokens": archived["tokens"], "n_eligible_pairs": archived["eligible_pairs"],
            "score_raw_spearman": archived["raw_spearman"],
            "score_additive_propensity_residual_spearman": archived["additive_residual_spearman"],
            "score_pearson_residuals": archived["residual_pearson"],
        }
        flat = audit.flatten_run_records({
            archived["source"]: {archived["view"]: {str(archived["top_k"]): [synthetic_metric]}}
        })
        self.assertEqual(flat, [archived])

    def test_replay_two_frozen_primary_rows(self):
        """Recompute exactly one preselected 150-type seed per edition, not 54."""
        archive = load_archive()
        for source in SOURCES:
            with self.subTest(source=source):
                path = ROOT / "data/transcriptions" / source
                snapshot, receipt = audit.load_verified_source(path)
                self.assertEqual(receipt, archive["sources"][source])
                pages = audit.read_pages(
                    path, uncertain_space="split", categories={"P", "C", "R"},
                    keep_empty=True, source_text=snapshot,
                )
                pages = [page for page in pages if page["id"] not in {"f116v", "fRos"}]
                result = audit.metric(pages, seed=20261101, shuffles=20, top_k=150)
                got = audit.flatten_run_records({
                    source: {"split": {"150": [result]}}
                })[0]
                expected = next(row for row in archive["run_records"]
                                if (row["source"], row["view"], row["top_k"], row["seed"])
                                == (source, "split", 150, 20261101))
                for field in FIELDS:
                    if field in ("raw_spearman", "additive_residual_spearman", "residual_pearson"):
                        self.assertAlmostEqual(got[field], expected[field], places=9,
                                               msg=f"{source}: {field}")
                    else:
                        self.assertEqual(got[field], expected[field],
                                         f"{source}: {field}")
                print(
                    f"REPLAY source={source} sha256={receipt['sha256']} "
                    f"seed=20261101 shuffles=20 top_k=150 pages={got['pages']} "
                    f"lines={got['lines']} tokens={got['tokens']} "
                    f"eligible_pairs={got['eligible_pairs']} "
                    f"residual_spearman={got['additive_residual_spearman']:.12f}",
                    flush=True,
                )


if __name__ == "__main__":
    unittest.main()
