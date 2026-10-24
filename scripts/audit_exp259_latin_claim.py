#!/usr/bin/env python3
"""Guard EXP-259's historically mislabeled Latin comparator without editing history."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "experiments/exp_259_char_positional_entropy/script.py"
REPORT = "experiments/exp_259_char_positional_entropy/result.md"
CORPUS = "data/reference_corpora/latin/cicero_de_officiis_latin.txt"
SCRIPT_BLOB = "71bbe2778ca04feec492ca300e7e964566e291f8"
REPORT_BLOB = "6dc5dca756638adda60275690be66ec0821c0475"
CORPUS_SHA256 = "3a33a076d3dda42673ec7ab0331ae7e58fc150e7e92751c0adf6d1db7297b670"
ARCHIVED_REFERENCE_TOKENS = 112081
CLAIM_MARKERS = (
    "Latin Cicero comparison",
    "VMS Is Substantially More Constrained Than Latin Char-for-Char",
    "H449 CONFIRMED",
)


def strict_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("Duplicate JSON key: " + key)
        obj[key] = value
    return obj


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def require_unique_path(rows, path, label):
    if not isinstance(rows, list):
        raise ValueError(label + " is not a list")
    matches = [row for row in rows if isinstance(row, dict) and row.get("path") == path]
    if len(matches) != 1:
        raise ValueError(label + ": expected exactly one entry for " + path)
    return matches[0]


def check_bilingual_adjudication(row):
    if (row.get("issue") != "BILINGUAL_REQUIRES_FILTER_AUDIT"
            or row.get("adjudicated_language") != "Latin and English"
            or row.get("adjudicated_work") != "De Officiis #47001"):
        raise ValueError("EXP-259 reference is not adjudicated as bilingual")
    evidence = row.get("evidence")
    if not isinstance(evidence, list) or not any(
            isinstance(item, str) and "ENGLISH TRANSLATION" in item
            for item in evidence):
        raise ValueError("EXP-259 bilingual evidence missing")


def check_provenance(manifest_row, identity_row, corpus_raw):
    digest = hashlib.sha256(corpus_raw).hexdigest()
    if (digest != CORPUS_SHA256 or len(corpus_raw) != 720407
            or manifest_row.get("sha256") != digest
            or manifest_row.get("bytes") != len(corpus_raw)
            or identity_row.get("sha256") != digest
            or identity_row.get("bytes") != len(corpus_raw)):
        raise ValueError("EXP-259 reference corpus provenance mismatch")
    check_bilingual_adjudication(identity_row)
    return digest


def load_historical_reader(script_raw):
    """Isolate only the blob-pinned reference reader, not module top-level code."""
    if git_blob(script_raw) != SCRIPT_BLOB:
        raise ValueError("EXP-259 historical script blob changed")
    tree = ast.parse(script_raw, filename=SCRIPT)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == "parse_latin"]
    if len(nodes) != 1:
        raise ValueError("EXP-259 historical reference reader missing or duplicated")
    namespace = {"re": re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), SCRIPT, "exec"), namespace)
    return namespace["parse_latin"]


def audit(root=ROOT):
    script_raw = (root / SCRIPT).read_bytes()
    report_raw = (root / REPORT).read_bytes()
    if git_blob(report_raw) != REPORT_BLOB:
        raise ValueError("EXP-259 historical report blob changed")
    report = report_raw.decode("utf-8")
    for marker in CLAIM_MARKERS:
        if marker not in report:
            raise ValueError("EXP-259 historical claim marker changed: " + marker)
    manifest = json.loads(
        (root / "research/CORPUS_INPUT_MANIFEST.json").read_text(encoding="utf-8"),
        object_pairs_hook=strict_object)
    identity = json.loads(
        (root / "research/CORPUS_IDENTITY_REVIEW.json").read_text(encoding="utf-8"),
        object_pairs_hook=strict_object)
    raw = (root / CORPUS).read_bytes()
    digest = check_provenance(
        require_unique_path(manifest["files"], CORPUS, "Frozen manifest"),
        require_unique_path(identity["excluded_from_new_language_baselines"],
                            CORPUS, "Identity exclusions"), raw)
    words = load_historical_reader(script_raw)(str(root / CORPUS))
    if len(words) != ARCHIVED_REFERENCE_TOKENS:
        raise ValueError("EXP-259 reference reader token count differs from archive")
    return {
        "scope": "EXP-259 reference-reader replay and comparator claim adjudication only",
        "status": "INVALID_FOR_CLAIM",
        "invalid_claim": "EXP-259's Latin Cicero comparator is monolingual Latin",
        "not_adjudicated": [
            "Historical A/B entropy estimates and their reader/folio classifications",
            "Claims about natural-language morphology or the hoax hypothesis",
            "Full EXP-259 reproduction and IVTFF conformance",
        ],
        "source_script_git_blob": SCRIPT_BLOB,
        "source_script_sha256": hashlib.sha256(script_raw).hexdigest(),
        "source_report_git_blob": REPORT_BLOB,
        "source_report_sha256": hashlib.sha256(report_raw).hexdigest(),
        "reference_path": CORPUS,
        "reference_sha256": digest,
        "reference_bytes": len(raw),
        "historical_reference_tokens_replayed": len(words),
        "historical_reference_token_sequence_sha256": hashlib.sha256(
            json.dumps(words, separators=(",", ":"), ensure_ascii=True).encode()
        ).hexdigest(),
        "reader": "blob-pinned EXP-259 parse_latin AST function, no language filtering",
        "parameters": {"seed": None, "minimum_reference_word_length": 1},
        "limitations": [
            "The archived file contains Latin and English; replay does not isolate either language.",
            "No language-specific entropy was recomputed and no valid Latin baseline substituted.",
            "This does not prove or disprove internal VMS positional structure or a translation.",
            "Corpus bytes, historical script, report, results and committed claims are untouched.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    receipt = json.dumps(audit(), indent=2, sort_keys=True, ensure_ascii=False,
                         allow_nan=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(receipt, encoding="utf-8")
    print("EXP259_SCOPE_RECEIPT=" + json.dumps(
        json.loads(receipt), sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()
