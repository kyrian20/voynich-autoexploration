#!/usr/bin/env python3
"""Read-only, hash-gated census of high-ASCII adjacency in EXP-590 source rows.

A code adjacent to ASCII letters may be erased by the historical ASCII-only
view. This is a diagnostic of source spelling, not a corrected tokenizer,
a historical experiment replay, or an assertion about glyph meaning.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import string

from scripts.audit_ivtff_high_ascii_coverage import SOURCES
from scripts.audit_ivtff_ligature_views import TEXT_LINE
from scripts.audit_ivtff_page_locus_ids import audit_text as audit_structure, structural_errors
from scripts.ivtff_lossless import lex
from scripts.ivtff_physical_rows import checked_physical_lines

ROOT = Path(__file__).resolve().parents[1]
ASCII_LETTERS = frozenset(string.ascii_letters)
EXPECTED_CODE_COUNTS = {"ZL3b": (122, 168), "ZL3a": (117, 160), "IT2a": (0, 0)}


def primary_codes(spans):
    """Only primary-visible codes, descending into ligatures but not alternatives."""
    for span in spans:
        if span.kind == "high_ascii":
            digits = span.raw[1:-1]
            if not digits.isascii() or not digits.isdecimal():
                raise ValueError("Non-ASCII IVTFF high-ASCII code")
            if not 128 <= int(digits) <= 255:
                raise ValueError("IVTFF high-ASCII code outside 128..255")
            yield span
        elif span.kind == "ligature":
            yield from primary_codes(span.children)


def analyze_text(text: str) -> dict:
    code_rows = 0
    total_codes = left = right = both = neither = 0
    affected = []
    for source_line, row in checked_physical_lines(text):
        if row.lstrip().startswith("#"):
            continue
        match = TEXT_LINE.match(row)
        if not match or not match.group(3).strip():
            continue
        folio, locus, body = match.groups()
        codes = list(primary_codes(lex(body).spans))
        if not codes:
            continue
        code_rows += 1
        details = []
        for code in codes:
            has_left = code.start > 0 and body[code.start - 1] in ASCII_LETTERS
            has_right = code.end < len(body) and body[code.end] in ASCII_LETTERS
            left += has_left
            right += has_right
            both += has_left and has_right
            neither += not (has_left or has_right)
            total_codes += 1
            if has_left or has_right:
                details.append({"code": code.raw, "offset": code.start,
                                "ascii_left": has_left, "ascii_right": has_right})
        if details:
            affected.append({
                "source_line": source_line,
                "locus": f"f{folio}.{locus}",
                "body_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "raw_body": body,
                "adjacent_codes": details,
            })
    return {
        "rows_with_primary_high_ascii": code_rows,
        "primary_high_ascii_codes": total_codes,
        "codes_with_ascii_left": left,
        "codes_with_ascii_right": right,
        "codes_with_ascii_both_sides": both,
        "codes_with_no_direct_ascii_neighbor": neither,
        "codes_with_at_least_one_ascii_neighbor": total_codes - neither,
        "rows_with_at_least_one_ascii_neighbor": len(affected),
        "affected_rows": affected,
    }


def audit(root: Path = ROOT) -> dict:
    results = {}
    for label, (filename, expected_sha256) in SOURCES.items():
        path = root / "data/transcriptions" / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"{label}: missing or linked frozen corpus")
        raw = path.read_bytes()
        sha256 = hashlib.sha256(raw).hexdigest()
        if sha256 != expected_sha256:
            raise ValueError(f"{label}: frozen SHA-256 mismatch")
        text = raw.decode("utf-8-sig")
        errors = structural_errors(audit_structure(text))
        if errors:
            raise ValueError(f"{label}: structural IVTFF errors: {errors}")
        result = analyze_text(text)
        expected = EXPECTED_CODE_COUNTS[label]
        observed = (result["rows_with_primary_high_ascii"],
                    result["primary_high_ascii_codes"])
        if observed != expected:
            raise ValueError(f"{label}: primary high-ASCII inventory drift: {observed}")
        results[label] = {"source": f"data/transcriptions/{filename}",
                          "sha256": sha256, **result}
    return {
        "status": "DESCRIPTIVE_SOURCE_ADJACENCY_ONLY",
        "question": "How many selected @NNN; codes touch ASCII letters directly in frozen IVTFF locus bodies?",
        "unit": "code span and source locus; not an independent manuscript sample",
        "method": "Raw character adjacency at lexer span offsets, primary readings only; comments and square alternatives excluded",
        "historical_exp590_reexecuted": False,
        "historical_results_modified": False,
        "heldout_evaluation_performed": False,
        "seeds": None,
        "limitations": [
            "ASCII adjacency is a potential fragmentation mechanism, not a proven change in a specific historical metric.",
            "Direct raw adjacency excludes punctuation, comments and brace boundaries between a code and a letter.",
            "No high-ASCII code is assigned a letter or linguistic meaning.",
            "The three editions are alternative transcriptions of one manuscript, not independent validation.",
            "The complete IVTFF interpretation remains unadjudicated; no historical metric is rehabilitated.",
        ],
        "sources": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Exclusive-create evidence JSON; never overwrite")
    args = parser.parse_args()
    output = json.dumps(audit(), ensure_ascii=False, sort_keys=True, indent=2,
                        allow_nan=False) + "\n"
    if args.out is None:
        print(output, end="")
    else:
        with args.out.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(output)


if __name__ == "__main__":
    main()
