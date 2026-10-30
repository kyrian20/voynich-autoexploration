#!/usr/bin/env python3
"""Hash-gated reconciliation of IVTFF high-ASCII-only rows in EXP-590 coverage.

The historical ASCII-only token view and all source transcriptions are frozen.
This audit uses the existing lossless lexer only to demonstrate that omitted
records carry opaque high-ASCII glyph codes, not decoded character meanings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.audit_ivtff_ligature_views import TEXT_LINE, tokenize_views
from scripts.audit_ivtff_page_locus_ids import audit_text, structural_errors
from scripts.ivtff_physical_rows import checked_physical_lines
from scripts.ivtff_lossless import lex
from scripts.ivtff_rows import tokens_rows

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "ZL3b": ("eva_zl3b.txt", "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"),
    "ZL3a": ("zl3a.txt", "56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2"),
    "IT2a": ("eva_it2a.txt", "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"),
}
EXPECTED = {
    "ZL3b": (5385, 5376, 122, 168, 9, 0, ("f49v.11", "f49v.21", "f49v.27",
                                     "f49v.29", "f49v.35", "f49v.41",
                                     "f66r.24", "f66r.38", "f66r.42")),
    "ZL3a": (5389, 5380, 117, 160, 8, 1, ("f49v.11", "f49v.21", "f49v.27",
                                     "f49v.29", "f49v.35", "f49v.41",
                                     "f66r.24", "f66r.38", "f66r.42")),
    "IT2a": (5215, 5207, 0, 0, 0, 8, ("f49v.11", "f49v.21", "f49v.27",
                                     "f49v.29", "f49v.35", "f49v.41",
                                     "f66r.24", "f66r.42")),
}


def selected_codes(spans) -> list[str]:
    """Count codes in primary-visible text, not comments or bracketed alternatives."""
    codes = []
    for span in spans:
        if span.kind == "high_ascii":
            if not span.raw[1:-1].isascii():
                raise ValueError("Non-ASCII IVTFF high-ASCII digits")
            value = int(span.raw[1:-1])
            if not 128 <= value <= 255:
                raise ValueError("High-ASCII code outside 128..255")
            codes.append(span.raw)
        elif span.kind == "ligature":
            codes.extend(selected_codes(span.children))
        elif span.kind == "unresolved" and span.raw == "@":
            # lex() reports malformed @ codes but this census previously
            # ignored its diagnostics whenever an ASCII token was present.
            raise ValueError("Malformed primary IVTFF high-ASCII code")
        # Do not descend into alternatives: the historical comparison drops
        # all square-bracket readings, including any high-ASCII codes inside.
    return codes


def analyze_text(text: str) -> dict:
    total = tokenized = code_rows = code_count = 0
    omitted = []
    for number, row in checked_physical_lines(text):
        if row.lstrip().startswith("#"):
            continue
        match = TEXT_LINE.match(row)
        if match is None or not match.group(3).strip():
            continue
        folio, line_number, body = match.groups()
        total += 1
        historical = tokenize_views(body)["historical"]
        if historical:
            tokenized += 1
        payload = lex(body)
        codes = selected_codes(payload.spans)
        if codes:
            code_rows += 1
            code_count += len(codes)
        if not historical:
            # A historical ASCII-empty row can contain either an opaque
            # high-ASCII glyph or an explicit unreadable '?' marker. These
            # are different evidence classes and must not be merged.
            opaque = tokens_rows([payload], uncertain_space="split",
                                 alternatives="primary", ligatures="expand")
            if codes and opaque == codes:
                kind = "HIGH_ASCII_ONLY"
            elif not codes and opaque == ["?"]:
                kind = "UNREADABLE_ONLY"
            else:
                raise ValueError("Unadjudicated ASCII-empty IVTFF record")
            omitted.append({"source_line": number, "locus": f"f{folio}.{line_number}",
                            "raw_body": body, "classification": kind,
                            "high_ascii_codes": codes, "opaque_tokens": opaque})
    return {
        "nonempty_text_records": total,
        "ascii_tokenized_records": tokenized,
        "records_with_selected_high_ascii": code_rows,
        "selected_high_ascii_codes": code_count,
        "high_ascii_only_records": sum(x["classification"] == "HIGH_ASCII_ONLY" for x in omitted),
        "unreadable_only_records": sum(x["classification"] == "UNREADABLE_ONLY" for x in omitted),
        "ascii_omitted_but_opaque_nonempty": omitted,
    }


def audit(root: Path = ROOT) -> dict:
    results = {}
    for label, (filename, expected_hash) in SOURCES.items():
        path = root / "data/transcriptions" / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"{label}: missing or linked frozen transcription")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != expected_hash:
            raise ValueError(f"{label}: frozen corpus SHA-256 mismatch")
        text = raw.decode("utf-8-sig")
        errors = structural_errors(audit_text(text))
        if errors:
            raise ValueError(f"{label}: structural IVTFF errors: {errors}")
        result = analyze_text(text)
        expected = EXPECTED[label]
        observed = (result["nonempty_text_records"], result["ascii_tokenized_records"],
                    result["records_with_selected_high_ascii"],
                    result["selected_high_ascii_codes"],
                    result["high_ascii_only_records"], result["unreadable_only_records"],
                    tuple(row["locus"] for row in result["ascii_omitted_but_opaque_nonempty"]))
        if observed != expected:
            raise ValueError(f"{label}: frozen high-ASCII coverage drift: {observed}")
        results[label] = {"path": f"data/transcriptions/{filename}",
                          "sha256": digest, **result}
    return {
        "status": "REPRODUCED_SCOPE_ONLY",
        "scope": "Opaque high-ASCII versus unreadable record coverage under frozen ASCII-only view",
        "historical_experiment_reexecuted": False,
        "historical_results_modified": False,
        "high_ascii_decoded": False,
        "seeds": None,
        "policy": "Square-bracket readings excluded for historical comparability; high-ASCII glyph codes remain opaque and question marks mean unreadable, not empty",
        "limitations": [
            "This does not prove all IVTFF 2.0.2 constructs are handled correctly.",
            "Counts are descriptive, not linguistic evidence or a new predictor.",
            "Related transcriptions are alternative readings of one manuscript.",
            "No historical metric or held-out folio is rehabilitated.",
        ],
        "sources": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Exclusive-create JSON evidence file")
    args = parser.parse_args()
    output = json.dumps(audit(), sort_keys=True, indent=2, ensure_ascii=False,
                        allow_nan=False) + "\n"
    if args.out:
        with args.out.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
