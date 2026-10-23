#!/usr/bin/env python3
"""EXP-173 F3/F6 metadata-B folio sensitivity, descriptive only; no new EXP.

Use the frozen legacy population from audit_exp173_currier_crosswalk.py.
No historical experiment import, corpus replacement, random seed, or p-value.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"
CROSSWALK = ROOT / "scripts/audit_exp173_currier_crosswalk.py"
LEGACY = ROOT / "experiments/exp_173_multiple_testing/script.py"
EXPECTED_CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
EXPECTED_CROSSWALK_BLOB = "db27baa834a898b2e1b6a78e94a3b8d6d98cff43"
EXPECTED_LEGACY_BLOB = "3fb1eeb92c301d3caf841499571f5e1a8b590bcc"
BASE_COMMIT = "c70a0ba5a97276edce09d7bfe7b8dc88514a2881"


def blob_sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def line_counts(tokens: list[str]) -> dict:
    if not tokens:
        raise ValueError("Empty line is not in the historical population")
    n = len(tokens)
    am = sum(w.endswith("am") for w in tokens)
    y = sum(w.lower().startswith("y") for w in tokens)
    return {"lines": 1, "words": n, "am": am, "amLL": int(tokens[-1].endswith("am")),
            "y": y, "yLF": int(tokens[0].lower().startswith("y")),
            "amExp": am / n, "yExp": y / n}


def sum_counts(rows: list[dict]) -> dict:
    keys = ("lines", "words", "am", "amLL", "y", "yLF", "amExp", "yExp")
    result = {k: 0 for k in keys}
    for row in rows:
        c = line_counts(row["tokens"])
        for k in keys:
            result[k] += c[k]
    return result


def enrichment(counts: dict, metric: str) -> float:
    k, total = ("amLL", "am") if metric == "am" else ("yLF", "y")
    if not counts["lines"] or not counts["words"] or not counts[total]:
        raise ValueError("Undefined enrichment denominator")
    return (counts[k] / counts["lines"]) / (counts[total] / counts["words"])


def rounded(value: float) -> float:
    return round(value, 9)


def analyze(rows: list[dict], labels: dict[str, str | None]) -> dict:
    selected = [r for r in rows if labels.get(r["page"]) == "B"]
    by_folio = defaultdict(list)
    for r in selected:
        m = re.match(r"^f\d+", r["page"])
        if not m:
            raise ValueError("Invalid folio locus: " + r["page"])
        by_folio[m.group()].append(r)  # recto, verso and multi-panel loci stay together
    if len(by_folio) < 3:
        raise ValueError("At least three physical folios needed for jackknife")
    full = sum_counts(selected)
    folio_counts = {p: sum_counts(rs) for p, rs in sorted(by_folio.items())}
    totals = {k: full[k] for k in ("lines", "words", "am", "amLL", "y", "yLF")}
    result = {"metadata_B_physical_folios": len(folio_counts),
              "metadata_B_page_loci": len({r["page"] for r in selected}),
              "metadata_B": totals, "metrics": {}, "folios": {}}
    for p, c in folio_counts.items():
        result["folios"][p] = {k: c[k] for k in totals}
        result["folios"][p]["amExp"] = rounded(c["amExp"])
        result["folios"][p]["yExp"] = rounded(c["yExp"])
    for metric, observed_key, expected_key in (("am", "amLL", "amExp"), ("y", "yLF", "yExp")):
        full_e = enrichment(full, metric)
        leaves = []
        for c in folio_counts.values():
            remaining = {k: full[k] - c[k] for k in totals}
            leaves.append(enrichment(remaining, metric))
        mean = sum(leaves) / len(leaves)
        se = math.sqrt((len(leaves) - 1) / len(leaves) * sum((v - mean) ** 2 for v in leaves))
        positive = sum(c[observed_key] > c[expected_key] + 1e-12 for c in folio_counts.values())
        negative = sum(c[observed_key] < c[expected_key] - 1e-12 for c in folio_counts.values())
        result["metrics"][metric] = {
            "enrichment": rounded(full_e),
            "within_line_exchangeable_expected": rounded(full[expected_key]),
            "observed": full[observed_key],
            "observed_over_exchangeable_expected": rounded(full[observed_key] / full[expected_key]),
            "folio_excess_positive": positive, "folio_excess_negative": negative,
            "folio_excess_zero": len(folio_counts) - positive - negative,
            "leave_one_folio_out_min": rounded(min(leaves)),
            "leave_one_folio_out_max": rounded(max(leaves)),
            "jackknife_se": rounded(se),
            "jackknife_normal95_approx": [rounded(full_e - 1.96 * se), rounded(full_e + 1.96 * se)],
        }
    return result


def run() -> dict:
    raw = CORPUS.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_CORPUS_SHA256:
        raise ValueError("Unexpected corpus SHA-256")
    if blob_sha(CROSSWALK.read_bytes()) != EXPECTED_CROSSWALK_BLOB:
        raise ValueError("Crosswalk parser changed")
    if blob_sha(LEGACY.read_bytes()) != EXPECTED_LEGACY_BLOB:
        raise ValueError("Legacy EXP-173 changed")
    # Only import a standalone read-only audit module, NEVER the legacy experiment.
    import audit_exp173_currier_crosswalk as crosswalk
    rows, _, labels = crosswalk.read_legacy_population(raw.decode("utf-8-sig"))
    result = analyze(rows, labels)
    if len(rows) != 4118 or result["metadata_B"] != {"lines": 2466, "words": 20652, "am": 406,
                                                  "amLL": 331, "y": 851, "yLF": 355}:
        raise ValueError("Historical population/crosswalk count mismatch")
    return {"schema_version": 1, "status": "EXPLORATORY_FOLIO_SENSITIVITY_NOT_PVALUE",
            "source_commit": BASE_COMMIT, "source": "data/transcriptions/eva_zl3b.txt",
            "source_sha256": EXPECTED_CORPUS_SHA256,
            "parser": "scripts/audit_exp173_currier_crosswalk.py",
            "parser_git_blob_sha1": EXPECTED_CROSSWALK_BLOB,
            "legacy_script_git_blob_sha1": EXPECTED_LEGACY_BLOB,
            "population": "legacy P-lines; only explicit page-header $L=B; no missing label imputation",
            "within_line_null": "uniform token permutation within each observed line, conditional on exact token multiset",
            "jackknife": "delete-one-physical-folio, approximate normal 95%; descriptive sensitivity, NOT confirmatory p",
            "randomness": "none", **result}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", type=Path, help="Compare all fields to frozen snapshot")
    args = p.parse_args()
    result = run()
    if args.check:
        if result != json.loads(args.check.read_text(encoding="utf-8")):
            raise SystemExit("EXP-173 folio sensitivity snapshot mismatch")
        print("PASS: EXP-173 metadata-B folio sensitivity snapshot")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
