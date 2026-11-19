#!/usr/bin/env python3
"""EXP-620: read-only census of header/line folio disagreement in exact IVTFF inputs.

Not a complete IVTFF validator, not a reproduction of historical experiments.
No tokens are rewritten; only records matching the frozen parsers' header/line
regular expressions enter the denominator. All other lines are counted separately.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HEADER = re.compile(r"^<(f\d+[rv])>\s+<!([^>]*)>")
LINE = re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
Q = re.compile(r"\$Q=([^\s>]+)")
INPUTS = ("data/transcriptions/eva_zl3b.txt", "data/transcriptions/eva_it2a.txt")


def census(raw):
    active = None
    active_q = "?"
    totals = dict(headers=0, recognized_lines=0, matching=0, mismatched=0,
                  without_header=0, q_t_matching=0, q_t_mismatched=0,
                  other_nonblank=0, blank=0)
    examples = []
    for n, line in enumerate(raw.splitlines(), 1):
        h = HEADER.match(line)
        if h:
            active = h.group(1)
            q = Q.search(h.group(2))
            active_q = q.group(1) if q else "?"
            totals["headers"] += 1
            continue
        m = LINE.match(line)
        if m:
            totals["recognized_lines"] += 1
            if active is None:
                totals["without_header"] += 1
            elif m.group(1) != active:
                totals["mismatched"] += 1
                if active_q == "T":
                    totals["q_t_mismatched"] += 1
                if len(examples) < 20:
                    examples.append(dict(physical_line=n, header_folio=active,
                                         line_folio=m.group(1), header_q=active_q))
            else:
                totals["matching"] += 1
                if active_q == "T":
                    totals["q_t_matching"] += 1
            continue
        totals["blank" if not line.strip() else "other_nonblank"] += 1
    assert totals["recognized_lines"] == (totals["matching"] +
            totals["mismatched"] + totals["without_header"])
    return dict(totals=totals, first_20_mismatches=examples)


def self_test():
    sample = ("# comment\n<f1r> <! $Q=T>\n<f1r.1,P0> chay\n"
              "<f2r.1,P0> shay\n<f2r> <! $Q=A>\n<f2r.1,P0> shay\n")
    t = census(sample)["totals"]
    assert (t["headers"], t["recognized_lines"], t["matching"],
            t["mismatched"], t["q_t_mismatched"]) == (2, 3, 2, 1, 1)
    assert census("<f1r.1,P0> chay\n")["totals"]["without_header"] == 1


def main():
    self_test()
    output = {"status": "DESCRIPTIVE_CENSUS_ONLY", "scope":
              "Only header and line records recognized by frozen EXP-613/617 regex; "
              "other records excluded from denominator; no IVTFF grammar adjudication",
              "sources": {}}
    for name in INPUTS:
        data = Path(name).read_bytes()
        raw = data.decode("utf-8")
        output["sources"][name] = dict(sha256=hashlib.sha256(data).hexdigest(),
                                      bytes=len(data), **census(raw))
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:]:
        raise SystemExit("No optional inputs: canonical repository paths are fixed")
    main()
