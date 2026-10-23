#!/usr/bin/env python3
"""Read-only EXP-173 Currier crosswalk; reproduces its P-line population exactly.

This diagnostic is not a rerun of EXP-173 or a test of statistical significance.
Run: python scripts/audit_exp173_currier_crosswalk.py --check research/maintenance/2026-10-23-exp173-currier-crosswalk/results.json
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
LEGACY = ROOT / "experiments/exp_173_multiple_testing/script.py"
EXPECTED_CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
EXPECTED_LEGACY_BLOB = "3fb1eeb92c301d3caf841499571f5e1a8b590bcc"
HEADER = re.compile(r"^<(f\d+[rv][1-6]?)>\s*(.*)$")
LANGUAGE = re.compile(r"\$L\s*=\s*([^\s>]+)")
FOLIO_NUMBER = re.compile(r"f(\d+)")
WORD_START = re.compile(r"[a-z]")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def read_legacy_population(text: str):
    """Mirror only the historical EXP-173 parsing/classification; no import."""
    page_labels = {}
    rows = []
    by_number = defaultdict(list)
    for raw_line in text.splitlines():
        line = raw_line.strip()
        header = HEADER.match(line)
        if header:
            page, metadata = header.groups()
            values = set(LANGUAGE.findall(metadata))
            if len(values) > 1:
                raise ValueError(f"Conflicting $L in {page}: {sorted(values)}")
            label = next(iter(values), None)
            page_labels[page] = label if label in {"A", "B"} else None
            continue
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) < 2:
            continue
        locus, body = parts
        locus_parts = locus.split(",")
        if len(locus_parts) < 2:
            continue
        page = locus_parts[0].split(".")[0].lstrip("<")
        m = FOLIO_NUMBER.match(page)
        if not m:
            continue
        number = int(m.group(1))
        line_type = locus_parts[1].rstrip(">").lstrip("@+*=~&")
        if not line_type.startswith("P"):
            continue
        tokens = [w for w in body.split(".") if w and WORD_START.match(w) and not w.startswith("<")]
        if not tokens:
            continue
        by_number[number].extend(tokens)
        rows.append({"page": page, "number": number, "tokens": tokens})
    legacy_labels = {}
    for number, tokens in by_number.items():
        if len(tokens) < 10:
            continue
        rate = sum("edy" in w or "eedy" in w for w in tokens) / len(tokens)
        legacy_labels[number] = "B" if rate >= 0.05 else "A"
    return rows, legacy_labels, page_labels


def metrics(rows):
    n_lines = len(rows)
    n_words = sum(len(r["tokens"]) for r in rows)
    am = sum(w.endswith("am") for r in rows for w in r["tokens"])
    am_ll = sum(r["tokens"][-1].endswith("am") for r in rows)
    y = sum(w.lower().startswith("y") for r in rows for w in r["tokens"])
    y_lf = sum(r["tokens"][0].lower().startswith("y") for r in rows)
    return {
        "lines": n_lines, "words": n_words, "am": am, "amLL": am_ll,
        "amLLenrichment": (am_ll / n_lines) / (am / n_words) if am and n_lines else None,
        "y": y, "yLF": y_lf,
        "yLFenrichment": (y_lf / n_lines) / (y / n_words) if y and n_lines else None,
    }


def crosswalk(text):
    rows, legacy, metadata = read_legacy_population(text)
    def hist(r):
        return legacy.get(r["number"])
    def canon(r):
        return metadata.get(r["page"])
    intersection = [r for r in rows if hist(r) and canon(r)]
    confusion = Counter(f"{hist(r) or 'unknown'}->{canon(r) or 'unknown'}" for r in rows)
    mismatch = defaultdict(list)
    unknown = defaultdict(list)
    for r in rows:
        if hist(r) and canon(r) and hist(r) != canon(r):
            mismatch[r["page"]].append(r)
        if not canon(r):
            unknown[r["page"]].append(r)
    return {
        "schema_version": 1,
        "status": "EXPLORATORY_DIAGNOSTIC_NOT_EXP173_REPRODUCTION",
        "unit": "legacy_P_lines_with_nonempty_legacy_tokens",
        "parser": "EXP-173 historical P-only ASCII-dot split, folio-number edy>=0.05; metadata from exact page header $L=A/B",
        "rows": len(rows),
        "headers_recognized": len(metadata),
        "legacy_classified_rows": sum(hist(r) in ("A", "B") for r in rows),
        "metadata_classified_rows": sum(canon(r) in ("A", "B") for r in rows),
        "intersection_rows": len(intersection),
        "confusion_lines": dict(sorted(confusion.items())),
        "mismatch_lines": sum(map(len, mismatch.values())),
        "mismatch_pages": {page: {"legacy": hist(group[0]), "L": canon(group[0]), **metrics(group)} for page, group in sorted(mismatch.items())},
        "metadata_unknown_pages": {page: len(group) for page, group in sorted(unknown.items())},
        "legacy_B": metrics([r for r in rows if hist(r) == "B"]),
        "metadata_B": metrics([r for r in rows if canon(r) == "B"]),
        "intersection_legacy_B": metrics([r for r in intersection if hist(r) == "B"]),
        "intersection_metadata_B": metrics([r for r in intersection if canon(r) == "B"]),
        "inference": "Descriptive sensitivity only. No p-value, bootstrap, corrected parser, or language identification.",
    }


def run():
    raw = SOURCE.read_bytes()
    corpus_hash = hashlib.sha256(raw).hexdigest()
    if corpus_hash != EXPECTED_CORPUS_SHA256:
        raise ValueError(f"Corpus SHA-256 changed: {corpus_hash}")
    legacy_blob = git_blob_sha1(LEGACY.read_bytes())
    if legacy_blob != EXPECTED_LEGACY_BLOB:
        raise ValueError(f"Historical EXP-173 script changed: {legacy_blob}")
    result = crosswalk(raw.decode("utf-8-sig"))
    result["source"] = "data/transcriptions/eva_zl3b.txt"
    result["source_sha256"] = corpus_hash
    result["legacy_script"] = "experiments/exp_173_multiple_testing/script.py"
    result["legacy_script_git_blob_sha1"] = legacy_blob
    if abs(result["legacy_B"]["amLLenrichment"] - 6.8112949758766455) > 1e-10:
        raise ValueError("Historical F3 enrichment not reproduced")
    if abs(result["legacy_B"]["yLFenrichment"] - 3.5056596985274417) > 1e-10:
        raise ValueError("Historical F6 enrichment not reproduced")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="Compare complete result to frozen JSON without writes")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("Crosswalk snapshot mismatch")
        print("Crosswalk snapshot verified")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
