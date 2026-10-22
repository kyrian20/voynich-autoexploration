#!/usr/bin/env python3
"""Non-destructive sensitivity inventory for IVTFF brace-delimited ligatures.

No historical EXP output is read or rewritten. Three explicit derived views are
compared while the original line body and character offsets remain available.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("ZL3b", ROOT / "data/transcriptions/eva_zl3b.txt"),
    ("ZL3a", ROOT / "data/transcriptions/zl3a.txt"),
    ("IT2a", ROOT / "data/transcriptions/eva_it2a.txt"),
]
TEXT_LINE = re.compile(r"^<f(\d+[rv])\.(\d+),[^>]*>\s*(.*)$")
TAG_RE = re.compile(r"<[^>]*>")
BRACE_RE = re.compile(r"\{[^{}]*\}")
TOKEN_RE = re.compile(r"[a-z]+")
UNIT_RE = re.compile(r"\{[^{}]*\}|[a-z]+")
TARGET = "daiin"


def prepare_body(body: str) -> str:
    """Match the historical baseline's removal of tags and square annotations."""
    body = TAG_RE.sub(" ", body)
    body = re.sub(r"\[[^\]]*\]", " ", body)
    return body.lower()


def tokenize_views(body: str) -> dict:
    """Return historical, atomic-ligature, and expanded views with raw offsets."""
    prepared = prepare_body(body)
    historical_text = BRACE_RE.sub(" ", prepared)
    expanded_text = BRACE_RE.sub(lambda m: m.group(0)[1:-1], prepared)
    historical = TOKEN_RE.findall(historical_text)
    expanded = TOKEN_RE.findall(expanded_text)

    atomic_units = []
    for match in UNIT_RE.finditer(prepared):
        raw = match.group(0)
        if raw.startswith("{") and raw.endswith("}"):
            atomic_units.append({
                "kind": "ligature",
                "raw": raw,
                "content": raw[1:-1],
                "start": match.start(),
                "end": match.end(),
            })
        else:
            atomic_units.append({
                "kind": "word",
                "raw": raw,
                "content": raw,
                "start": match.start(),
                "end": match.end(),
            })
    return {
        "historical": historical,
        "atomic_units": atomic_units,
        "expanded": expanded,
        "prepared_body": prepared,
    }


def summarize_lines(lines: list[dict]) -> dict:
    total_units = {"historical": 0, "atomic": 0, "expanded": 0}
    target_occurrences = {"historical": 0, "atomic": 0, "expanded": 0}
    initial_target_lines = {"historical": 0, "atomic": 0, "expanded": 0}
    changed_vs_historical = {"atomic": 0, "expanded": 0}
    ligature_spans = 0
    lines_with_ligatures = 0

    for line in lines:
        views = tokenize_views(line["body"])
        h = views["historical"]
        a = views["atomic_units"]
        e = views["expanded"]
        ligs = [u for u in a if u["kind"] == "ligature"]
        ligature_spans += len(ligs)
        lines_with_ligatures += bool(ligs)
        total_units["historical"] += len(h)
        total_units["atomic"] += len(a)
        total_units["expanded"] += len(e)
        target_occurrences["historical"] += h.count(TARGET)
        target_occurrences["atomic"] += sum(
            u["kind"] == "word" and u["content"] == TARGET for u in a
        )
        target_occurrences["expanded"] += e.count(TARGET)
        initial_target_lines["historical"] += bool(h and h[0] == TARGET)
        initial_target_lines["atomic"] += bool(
            a and a[0]["kind"] == "word" and a[0]["content"] == TARGET
        )
        initial_target_lines["expanded"] += bool(e and e[0] == TARGET)
        if a != [{"kind": "word", "raw": t, "content": t,
                  "start": -1, "end": -1} for t in h]:
            # The atomic view is structurally different if it contains a ligature;
            # the exact token-list comparison below is used for expanded view.
            if ligs:
                changed_vs_historical["atomic"] += 1
        if e != h:
            changed_vs_historical["expanded"] += 1

    return {
        "text_lines": len(lines),
        "lines_with_ligatures": lines_with_ligatures,
        "ligature_spans": ligature_spans,
        "analysis_units": total_units,
        "exact_daiin_occurrences": target_occurrences,
        "line_initial_daiin_lines": initial_target_lines,
        "lines_changed_vs_historical": changed_vs_historical,
    }


def audit_source(label: str, path: Path) -> dict:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    lines = []
    for row in text.splitlines():
        match = TEXT_LINE.match(row)
        if match:
            folio, line_no, body = match.groups()
            if body.strip():
                lines.append({"folio": folio, "line": int(line_no), "body": body})
    if not lines:
        raise RuntimeError(f"No transcription text lines parsed from {path}")
    return {
        "transcription": label,
        "source": str(path.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        **summarize_lines(lines),
    }


def main() -> None:
    results = []
    for label, path in SOURCES:
        if not path.is_file():
            raise FileNotFoundError(f"Required transcription missing: {path}")
        results.append(audit_source(label, path))
    print(json.dumps({
        "audit": "ivtff_ligature_view_sensitivity_inventory",
        "version": 1,
        "purpose": "Descriptive comparison only; not a registered EXP or a decipherment test.",
        "views": {
            "historical": "remove each brace span before ASCII tokenization",
            "atomic": "preserve each brace span as a typed ligature unit, separate from word units",
            "expanded": "remove delimiters but retain internal characters in a derived token view",
        },
        "cautions": [
            "Raw transcription files and historical experiment outputs are not modified.",
            "Atomic and expanded views are analytical alternatives, not claims that either is universally optimal.",
            "ZL3a and ZL3b are alternative transcriptions of the same manuscript, not independent samples.",
            "This report quantifies sensitivity only; it does not establish lexical meaning.",
        ],
        "files": results,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
