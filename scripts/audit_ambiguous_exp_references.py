#!/usr/bin/env python3
"""Inventory ambiguous legacy EXP references without rewriting historical sources.

This is a lexical triage tool: a hit is NOT proof of mistaken attribution.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research/EXPERIMENT_PATH_REGISTRY.json"
PATTERN = re.compile(r"(?<![A-Za-z0-9_])EXP[- _]?(\d{1,4})(?![A-Za-z0-9_])", re.I)
SKIP_PARTS = {".git", ".venv", "venv", "node_modules", ".pytest_cache"}
SUFFIXES = {".md", ".rst", ".txt"}
# Frozen corpus inputs are not historical EXP reports; audit their bytes separately.
RAW_CORPUS_ROOTS = (("data", "transcriptions"), ("data", "reference_corpora"))


def collisions(registry: dict) -> dict[str, list[str]]:
    by_id = defaultdict(list)
    for entry in registry["entries"]:
        by_id[str(entry["legacy_numeric_id"])].append(entry["path"])
    calculated = {key: paths for key, paths in by_id.items() if len(paths) > 1}
    recorded = {
        str(key): [item.removeprefix("GH:") for item in value]
        for key, value in registry["numeric_collisions"].items()
    }
    if calculated != recorded:
        raise ValueError("Registry collision table differs from entries")
    return calculated


def scan(root: Path, registry: dict) -> dict:
    duplicates = collisions(registry)
    hits = []
    unreadable_files = []
    excluded_raw_corpora = []
    skipped_symlinks = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.suffix.lower() not in SUFFIXES:
            continue
        if any(part in SKIP_PARTS for part in relative.parts):
            continue
        rel = relative.as_posix()
        if relative.parts[:2] in RAW_CORPUS_ROOTS:
            excluded_raw_corpora.append(rel)
            continue
        # Never dereference a symlink while constructing a CI artifact.
        if any(root.joinpath(*relative.parts[:i]).is_symlink()
               for i in range(1, len(relative.parts) + 1)):
            skipped_symlinks.append(rel)
            continue
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError) as exc:
            unreadable_files.append({"path": rel, "error_type": type(exc).__name__})
            continue
        for number, line in enumerate(lines, 1):
            for match in PATTERN.finditer(line):
                key = str(int(match.group(1)))
                if key not in duplicates:
                    continue
                # A nearby canonical directory disambiguates this particular reference.
                nearby = line[max(0, match.start()-160):match.end()+160]
                matching_paths = [p for p in duplicates[key] if p in nearby]
                hits.append({
                    "path": rel, "line": number, "alias": key,
                    "classification": "EXPLICIT_PATH_NEARBY" if len(matching_paths) == 1 else
                                      "REVIEW_REQUIRED",
                    "matched_paths": matching_paths,
                    "excerpt": line[:300],
                })
    return {
        "status": "LEXICAL_TRIAGE_NOT_CLAIM_ADJUDICATION",
        "collision_ids": sorted(duplicates, key=int),
        "files_with_hits": len({h["path"] for h in hits}),
        "occurrences": len(hits),
        "review_required": sum(h["classification"] == "REVIEW_REQUIRED" for h in hits),
        "by_alias": dict(sorted(Counter(h["alias"] for h in hits).items(), key=lambda x: int(x[0]))),
        "hits": hits,
        "unreadable_files": unreadable_files,
        "excluded_raw_corpora": excluded_raw_corpora,
        "skipped_symlinks": skipped_symlinks,
        "coverage_complete_for_selected_files": not unreadable_files and not skipped_symlinks,
        "caveats": [
            "A bare EXP number can be clear from paragraph context; lexical flag is not proof of an error.",
            "Nearby path is only a heuristic, not scientific validation of the associated claim.",
            "Only UTF-8 text/Markdown/RST outside frozen data corpora is scanned; code, JSON, PDFs, artifacts and Library files are excluded.",
            "Frozen corpus files are listed as excluded; byte integrity and encoding require separate audits.",
            "Symlinks are not dereferenced; skipped links are reported as incomplete selected-file coverage.",
            "Unreadable candidate files are explicitly reported; an empty hit list is not complete coverage if any are unreadable.",
            "No source files or experiment results are modified.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    registry = json.loads((args.root / "research/EXPERIMENT_PATH_REGISTRY.json").read_text(encoding="utf-8"))
    report = scan(args.root, registry)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "hits"}, ensure_ascii=False))
if __name__ == "__main__":
    main()
