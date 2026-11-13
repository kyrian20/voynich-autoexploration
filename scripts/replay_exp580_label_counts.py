#!/usr/bin/env python3
"""Reproduce archived EXP-580 headline counts; not independent IVTFF validation."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments/exp_580_label_corpus_grammar/script.py"
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"
EXPECTED = {
    "Label lines": 1087,
    "Body lines": 4113,
    "Label types": 1036,
    "Body types": 7030,
    "Overlap (label ∩ body)": 489,
    "Label-exclusive types": 547,
}
PATTERNS = {
    "Label lines": r"^Label lines:\s*(\d+)\s*$",
    "Body lines": r"^Body lines:\s*(\d+)\s*$",
    "Label types": r"^Label types:\s*(\d+)\s*$",
    "Body types": r"^Body types:\s*(\d+)\s*$",
    "Overlap (label ∩ body)": r"^Overlap \(label ∩ body\):\s*(\d+)\s*$",
    "Label-exclusive types": r"^Label-exclusive types:\s*(\d+)\s*$",
}

def extract(stdout):
    observed = {}
    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, stdout, re.MULTILINE)
        if len(matches) != 1:
            raise ValueError(f"{name}: expected exactly one occurrence, got {len(matches)}")
        observed[name] = int(matches[0])
    if observed["Label types"] - observed["Overlap (label ∩ body)"] != observed["Label-exclusive types"]:
        raise ValueError("Vocabulary arithmetic inconsistent")
    return observed

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not SCRIPT.is_file() or not CORPUS.is_file():
        raise SystemExit("BLOCKED: EXP-580 script or ZL3b corpus missing")
    run = subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT,
                         capture_output=True, text=True, check=False, timeout=180)
    if run.returncode:
        raise SystemExit(f"BLOCKED: historical script failed ({run.returncode}): {run.stderr[-2000:]}")
    observed = extract(run.stdout)
    report = {
        "status": "REPRODUCED" if observed == EXPECTED else "BLOCKED",
        "scope": "Historical script replay only; not independent parser or semantic validation",
        "python": sys.version.split()[0],
        "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        "corpus_sha256": hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
        "expected": EXPECTED, "observed": observed,
        "differences": {k: {"expected": v, "observed": observed[k]}
                        for k, v in EXPECTED.items() if observed[k] != v},
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    if args.check and observed != EXPECTED:
        raise SystemExit("BLOCKED: historical counts do not match report")

if __name__ == "__main__":
    main()
