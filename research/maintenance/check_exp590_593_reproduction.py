#!/usr/bin/env python3
"""Fail-closed provenance gate for EXP-590/593 (2026-11-18).

This does not reproduce the published Monte Carlo results. Never replace a
missing historical generator with a newly written script and call it a replay.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

FILES = (
    "research/experiments/2026-11-18-exp590-corrected-L-metadata.json",
    "research/experiments/2026-11-18-exp593-corrected-L-metadata.json",
)

def inspect(root, paths=FILES):
    issues = []
    records = []
    for relative in paths:
        path = root / relative
        if not path.is_file():
            issues.append(f"{relative}: missing result JSON")
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            issues.append(f"{relative}: unreadable JSON: {exc}")
            continue
        records.append(record)
        source = record.get("source")
        digest = record.get("source_sha256")
        if not isinstance(source, str) or not isinstance(digest, str):
            issues.append(f"{relative}: source path or SHA-256 absent")
        else:
            source_path = (root / source).resolve()
            if not source_path.is_relative_to(root.resolve()) or not source_path.is_file():
                issues.append(f"{relative}: exact source file unavailable")
            elif hashlib.sha256(source_path.read_bytes()).hexdigest() != digest:
                issues.append(f"{relative}: source SHA-256 mismatch")
        for key in ("generator_path", "generator_sha256", "reproduction_command",
                    "reproduction_log_path", "reproduced_output_sha256"):
            if not record.get(key):
                issues.append(f"{relative}: no attested {key}")
        if record.get("reproduction_status") not in ("REPRODUCED", "VALIDATED"):
            issues.append(f"{relative}: no attested reproduction status")
    if len(records) == len(paths) and len({r.get("source_sha256") for r in records}) != 1:
        issues.append("EXP-590/593: declared source digests differ")
    return issues

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    issues = inspect(args.root)
    print(json.dumps({"gate": "exp590_exp593_provenance",
                      "status": "BLOCKED" if issues else "READY_FOR_INDEPENDENT_REPRODUCTION_REVIEW",
                      "issues": issues}, indent=2))
    return 2 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
