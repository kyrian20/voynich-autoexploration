#!/usr/bin/env python3
"""EXP-620 follow-up: classify records excluded by the frozen header/line regex.

Read-only; preserves input bytes. Categories are *lexical shapes*, not normative
IVTFF validation. No linguistic event counts or corpus corrections are inferred.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

INPUTS = ("data/transcriptions/eva_zl3b.txt", "data/transcriptions/eva_it2a.txt")
HEADER = re.compile(r"^<(f\\d+[rv])>\\s+<!([^>]*)>")
LINE = re.compile(r"^<(f\\d+[rv])\\.\\d+,[^>]*>\\s*(.*)$")
LINE_PREFIX = re.compile(r"^<([^>]+)>")
FOLIO_PREFIX = re.compile(r"^<f\\d+[rv](?:\\.|>)")
COMMENT = re.compile(r"^\\s*#")

def classify(line):
    if not line.strip():
        return "blank"
    if HEADER.match(line):
        return "recognized_header"
    if LINE.match(line):
        return "recognized_line"
    if COMMENT.match(line):
        return "comment"
    if line.lstrip().startswith("#"):
        return "comment"
    if LINE_PREFIX.match(line):
        return "other_angle_record"
    if FOLIO_PREFIX.match(line):
        return "malformed_folio_prefix"
    if line.lstrip().startswith("<"):
        return "unclosed_angle_record"
    return "other_text"

def analyze(data):
    raw = data.decode("utf-8")
    counts = collections.Counter()
    examples = {}
    for n, line in enumerate(raw.splitlines(), 1):
        category = classify(line)
        counts[category] += 1
        if category not in ("blank", "recognized_header", "recognized_line"):
            examples.setdefault(category, [])
            if len(examples[category]) < 8:
                # No corpus text is echoed: physical positions suffice for review.
                examples[category].append(n)
    excluded = sum(v for k, v in counts.items()
                   if k not in ("blank", "recognized_header", "recognized_line"))
    assert excluded + counts["blank"] + counts["recognized_header"] + counts["recognized_line"] == sum(counts.values())
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data),
            "physical_lines": sum(counts.values()), "excluded_nonblank": excluded,
            "categories": dict(sorted(counts.items())),
            "first_8_physical_lines_per_excluded_category": examples}

def self_test():
    sample = ("# comment\\n<f1r> <! $Q=T>\\n<f1r.1,P0> chay\\n"
              "<f1r.2,P0>\\n<bad> x\\n<f1r.3,P0\\nother\\n\\n").encode()
    r = analyze(sample)
    assert r["physical_lines"] == 8
    assert r["categories"]["comment"] == 1
    assert r["categories"]["recognized_header"] == 1
    assert r["categories"]["recognized_line"] == 2
    assert r["categories"]["other_angle_record"] == 1
    assert r["categories"]["malformed_folio_prefix"] == 1
    assert r["categories"]["other_text"] == 1
    assert r["excluded_nonblank"] == 4

def main():
    self_test()
    result = {"status": "LEXICAL_TRIAGE_NOT_IVTFF_ADJUDICATION",
              "policy": "Mutually exclusive first-match categories; regex identical to EXP-620 census; no semantic inference",
              "deterministic": True, "seed": None, "sources": {}}
    for path in INPUTS:
        result["sources"][path] = analyze(Path(path).read_bytes())
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
