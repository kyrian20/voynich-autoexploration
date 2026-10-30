#!/usr/bin/env python3
"""Read-only sensitivity of EXP-590's positional counts to opaque IVTFF glyphs.

This is NOT a corrected reading or historical permutation replay. It replaces
only valid @128;..@255; codes by a non-decoding marker before applying exactly
the historical annotation-removal regex. ASCII letters touching the marker
remain in one opaque unit, while punctuation still separates units.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_exp590_high_ascii_adjacency import audit as audit_source_codes
from scripts.audit_ivtff_high_ascii_coverage import SOURCES
from scripts.exp590_daiin_position import TEXT_LINE, TOKEN_RE, TARGET, load_lines
from scripts.ivtff_physical_rows import checked_physical_lines

ANNOTATIONS = re.compile(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]")
CODE = re.compile(r"@(?:12[89]|1[3-9][0-9]|2[0-4][0-9]|25[0-5]);")
MARKER = "¤"
OPAQUE_TOKEN = re.compile(r"[a-z¤]+")


def views(body: str) -> tuple[list[str], list[str]]:
    """The historical ASCII view and one explicit non-decoding alternative."""
    if MARKER in body:
        raise ValueError("Opaque sentinel occurs in original IVTFF body")
    historical = TOKEN_RE.findall(ANNOTATIONS.sub(" ", body).lower())
    marked = CODE.sub(MARKER, body)
    opaque = OPAQUE_TOKEN.findall(ANNOTATIONS.sub(" ", marked).lower())
    return historical, opaque


def summarize(tokens_by_row: list[list[str]]) -> dict:
    nonempty = [row for row in tokens_by_row if row]
    return {
        "lines_with_tokens": len(nonempty),
        "tokens": sum(len(row) for row in nonempty),
        "exact_daiin": sum(row.count(TARGET) for row in nonempty),
        "initial_daiin_lines": sum(row[0] == TARGET for row in nonempty),
        "final_daiin_lines": sum(row[-1] == TARGET for row in nonempty),
    }


def analyze_text(text: str) -> dict:
    original_rows, opaque_rows, production_rows = [], [], []
    changed = []
    for source_line, row in checked_physical_lines(text):
        match = TEXT_LINE.match(row)
        if match is None:
            continue
        folio, line, body = match.groups()
        old, new = views(body)
        original_rows.append(old)
        opaque_rows.append(new)
        if old:
            production_rows.append((folio, int(line), old))
        if old != new:
            changed.append({
                "source_line": source_line,
                "locus": f"{folio}.{line}",
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "raw_body": body,
                "historical_tokens": old,
                "opaque_tokens": new,
                "delta_token_count": len(new) - len(old),
                "changed_initial_daiin": bool(old and old[0] == TARGET) != bool(new and new[0] == TARGET),
                "changed_final_daiin": bool(old and old[-1] == TARGET) != bool(new and new[-1] == TARGET),
            })
    historical = summarize(original_rows)
    opaque = summarize(opaque_rows)
    return {
        "physical_locus_records": len(original_rows),
        "historical": historical,
        "opaque_marker": opaque,
        "changed_records": len(changed),
        "previously_ascii_empty_now_opaque": sum(1 for row, new in zip(original_rows, opaque_rows) if not row and new),
        "changed_initial_daiin_records": sum(row["changed_initial_daiin"] for row in changed),
        "changed_final_daiin_records": sum(row["changed_final_daiin"] for row in changed),
        "changed_rows": changed,
        "_production_rows": production_rows,
    }


def audit(root: Path = ROOT) -> dict:
    # Independently established inventory, physical-row and source hash gates.
    source_evidence = audit_source_codes(root)
    results = {}
    for label, (filename, expected_sha) in SOURCES.items():
        path = root / "data" / "transcriptions" / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"{label}: frozen corpus missing or symlink")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected_sha or source_evidence["sources"][label]["sha256"] != digest:
            raise ValueError(f"{label}: source hash mismatch")
        report = analyze_text(raw.decode("utf-8-sig"))
        if label == "ZL3b":
            prod_bytes, prod_rows = load_lines(path)
            actual = [(r["folio"], r["line"], r["tokens"]) for r in prod_rows]
            if prod_bytes != raw or actual != report["_production_rows"]:
                raise ValueError("ZL3b historical token lists differ from EXP-590 production loader")
        del report["_production_rows"]
        results[label] = {
            "source": f"data/transcriptions/{filename}",
            "source_sha256": digest,
            "primary_high_ascii_codes": source_evidence["sources"][label]["primary_high_ascii_codes"],
            **report,
        }
    return {
        "status": "DESCRIPTIVE_OPAQUE_TOKEN_SENSITIVITY_ONLY",
        "question": "Does ignoring high-ASCII glyph codes alter EXP-590 ASCII token counts or daiin line endpoints?",
        "policy": "Replace only @128;..@255; by opaque marker before historical annotation removal; keep adjacent ASCII letters in the same unknown unit; do not decode glyphs",
        "historical_exp590_reexecuted": False,
        "permutations_executed": False,
        "heldout_evaluation_performed": False,
        "seed": None,
        "historical_results_modified": False,
        "limitations": [
            "This is a counterfactual token-boundary policy, not an adjudicated IVTFF reading.",
            "Other unreadable marks such as ? and other IVTFF conventions are not repaired.",
            "Historical permutation p-values are not recomputed or rehabilitated.",
            "ZL3a/ZL3b/IT2a are alternative editions of the same manuscript, not independent replicates.",
            "A positional difference does not establish meaning, language or decipherment.",
        ],
        "sources": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Create new JSON exclusively; never overwrite")
    args = parser.parse_args()
    data = json.dumps(audit(), sort_keys=True, ensure_ascii=False, indent=2,
                      allow_nan=False) + "\n"
    if args.out is None:
        print(data, end="")
    else:
        with args.out.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(data)


if __name__ == "__main__":
    main()
