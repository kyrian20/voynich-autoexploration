#!/usr/bin/env python3
"""EXP-260 scope audit: replay frozen legacy statistic and compute genuine pair MI.

This is a correction of an estimator/claim, not a reproduction of the original
full experiment or an inference about the language of the manuscript.
"""
import argparse
import ast
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/exp_260_char_bigram_pmi/script.py"
REPORT = ROOT / "experiments/exp_260_char_bigram_pmi/result.md"
SOURCE_GIT_BLOB = "529aba21b65ae010c5fec3eb5fb1e85b220101d2"
REPORT_GIT_BLOB = "8f32661cf088c75854aac750bfd13b8b975a2859"
INPUT_PATHS = ("data/transcriptions/eva_zl3b.txt",
               "data/reference_corpora/latin/cicero_de_officiis_latin.txt")
FUNCTIONS = ("clean_token", "get_dialect", "parse_vms", "parse_latin", "compute_pmi")
ARCHIVED = {"A": (1.815, 43428), "B": (2.087, 69050),
            "bilingual_reference": (0.781, 427471)}


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\0" + raw).hexdigest()


def check_frozen_inputs():
    manifest = json.loads((ROOT / "research/CORPUS_INPUT_MANIFEST.json").read_text())
    entries = {entry["path"]: entry for entry in manifest["files"]}
    result = {}
    for name in INPUT_PATHS:
        raw = (ROOT / name).read_bytes()
        entry = entries[name]
        if len(raw) != entry["bytes"] or sha256(raw) != entry["sha256"]:
            raise ValueError("Frozen corpus changed: " + name)
        result[name] = {"sha256": sha256(raw), "bytes": len(raw)}
    review = json.loads((ROOT / "research/CORPUS_IDENTITY_REVIEW.json").read_text())
    record = next(x for x in review["excluded_from_new_language_baselines"]
                  if x["path"] == INPUT_PATHS[1])
    if (record["issue"] != "BILINGUAL_REQUIRES_FILTER_AUDIT"
            or record["sha256"] != result[INPUT_PATHS[1]]["sha256"]):
        raise ValueError("Bilingual reference adjudication changed")
    return result


def load_legacy_functions():
    raw = SOURCE.read_bytes()
    if git_blob(raw) != SOURCE_GIT_BLOB:
        raise ValueError("Historical script blob changed")
    tree = ast.parse(raw, filename=str(SOURCE))
    nodes = [n for n in tree.body
             if isinstance(n, ast.FunctionDef) and n.name in FUNCTIONS]
    if [n.name for n in nodes] != list(FUNCTIONS):
        raise ValueError("Historical function inventory/order changed")
    # Only function definitions execute, never the historical top-level script.
    ns = {"re": re, "math": math, "Counter": Counter,
          "EVA_CHARS": set("acdehiklmnoqrsty")}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), "exec"), ns)
    return ns, sha256(raw)


def true_adjacent_pair_mi(words):
    """I(X;Y) for ALL within-word adjacent pairs, with pair marginals."""
    pairs = Counter((a, b) for w in words for a, b in zip(w, w[1:]))
    n = sum(pairs.values())
    if n == 0:
        raise ValueError("No adjacent pairs")
    left, right = Counter(), Counter()
    for (a, b), count in pairs.items():
        left[a] += count
        right[b] += count
    mi = math.fsum((count / n) * math.log2(count * n / (left[a] * right[b]))
                   for (a, b), count in pairs.items())
    return {"mi_bits": mi, "n_pairs": n, "distinct_pairs": len(pairs)}


def audit():
    inputs = check_frozen_inputs()
    if git_blob(REPORT.read_bytes()) != REPORT_GIT_BLOB:
        raise ValueError("Historical report blob changed")
    historical, source_sha256 = load_legacy_functions()
    a, b = historical["parse_vms"](str(ROOT / INPUT_PATHS[0]))
    mixed = historical["parse_latin"](str(ROOT / INPUT_PATHS[1]))
    rows = {}
    for label, words, char_filter in (
        ("A", a, historical["EVA_CHARS"]),
        ("B", b, historical["EVA_CHARS"]),
        ("bilingual_reference", mixed, None),
    ):
        _, _, _, legacy_n, legacy_mi = historical["compute_pmi"](
            words, char_filter, min_count=20)
        archived_mi, archived_n = ARCHIVED[label]
        if abs(legacy_mi - archived_mi) > 0.00050000001 or legacy_n != archived_n:
            raise ValueError("Legacy statistic differs from archived EXP-260: " + label)
        corrected = true_adjacent_pair_mi(words)
        if corrected["n_pairs"] != legacy_n:
            raise ValueError("Pair denominator changed: " + label)
        rows[label] = {
            "tokens": len(words),
            "token_sequence_sha256": sha256(json.dumps(
                words, ensure_ascii=True, separators=(",", ":")).encode()),
            "archived_legacy_bits_rounded": archived_mi,
            "legacy_statistic_bits_replayed": legacy_mi,
            "correct_pair_mi_bits": corrected["mi_bits"],
            "difference_correct_minus_legacy_bits": corrected["mi_bits"] - legacy_mi,
            "adjacent_pairs": legacy_n,
            "distinct_pairs": corrected["distinct_pairs"],
        }
    return {
        "status": "INVALID_FOR_CLAIM",
        "invalid_claim": "EXP-260 legacy 'MI' and ratios as Shannon adjacent-character mutual information",
        "historical_script_git_blob": SOURCE_GIT_BLOB,
        "historical_script_sha256": source_sha256,
        "historical_report_git_blob": REPORT_GIT_BLOB,
        "historical_report_sha256": sha256(REPORT.read_bytes()),
        "inputs": inputs,
        "parameters": {"legacy_min_count": 20, "seed": None,
                       "reader": "historical EXP-260 AST-isolated functions",
                       "corrected": "all within-word pairs; pair marginals"},
        "rows": rows,
        "limitations": [
            "Historical VMS reader and heuristic folio classes retained solely for matched comparison.",
            "Bilingual reference is not monolingual Latin; no corrected Latin baseline is claimed.",
            "Correct pair MI is descriptive, not a validated cipher or translation test.",
            "No new experiment ID and no modification of frozen originals.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise SystemExit("EXP-260 scope snapshot differs")
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False,
                                       allow_nan=False) + "\\n")
    print(json.dumps({"status": result["status"],
                      "mi_bits": {k: {"legacy": v["legacy_statistic_bits_replayed"],
                                      "corrected": v["correct_pair_mi_bits"]}
                                  for k, v in result["rows"].items()}},
                     sort_keys=True))


if __name__ == "__main__":
    main()
