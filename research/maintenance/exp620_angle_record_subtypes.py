#!/usr/bin/env python3
"""EXP-620: narrow read-only subtype census of previously excluded angle records.

Lexical diagnostics ONLY. This does not decide IVTFF validity or eligibility
for ch/sh events. Frozen corpora and historical outputs are never modified.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

INPUTS = ("data/transcriptions/eva_zl3b.txt", "data/transcriptions/eva_it2a.txt")
EXPECTED = {
    INPUTS[0]: ("bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc", 1231),
    INPUTS[1]: ("7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5", 1066),
}
HEADER = re.compile(r"^<(f\d+[rv])>\s+<!([^>]*)>")
LINE = re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
ANGLE = re.compile(r"^<([^>]+)>")
FOLIO = re.compile(r"^f\d+[rv]$")
LOCUS = re.compile(r"^f\d+[rv]\.")
FOLIO_LINE = re.compile(r"^f\d+[rv]\.\d+(?:,.*)?$")
# Panel identifiers include a digit after the recto/verso marker (e.g. f67r1).
# These are lexical candidates only, not a decision on IVTFF eligibility.
PANEL = re.compile(r"^f\d+[rv]\d+$")
PANEL_LOCUS = re.compile(r"^f\d+[rv]\d+\.\d+(?:,.*)?$")
# Named composite page identifiers, observed literally as fRos in ZL3b.
# Syntax-only candidates: IVTFF validity and eligibility remain unadjudicated.
NAMED_FOLIO = re.compile(r"^f[A-Z][A-Za-z0-9]*$")
NAMED_LOCUS = re.compile(r"^f[A-Z][A-Za-z0-9]*\.\d+(?:,.*)?$")
def subtype(s):
    m = ANGLE.match(s)
    if not m:
        return None
    if HEADER.match(s) or LINE.match(s):
        return None
    tag = m.group(1)
    if tag.startswith("!"):
        return "bang_tag"
    if FOLIO.fullmatch(tag):
        return "bare_folio_tag"
    if FOLIO_LINE.fullmatch(tag):
        return "numbered_folio_locus_other_shape"
    if LOCUS.match(tag):
        return "folio_locus_non_numeric"
    if PANEL.fullmatch(tag):
        return "panel_header_candidate"
    if PANEL_LOCUS.fullmatch(tag):
        return "panel_locus_candidate"
    if NAMED_FOLIO.fullmatch(tag):
        return "named_folio_header_candidate"
    if NAMED_LOCUS.fullmatch(tag):
        return "named_folio_locus_candidate"
    if tag.startswith("f"):
        return "other_f_prefixed_tag"
    return "other_tag"

def analyze(data):
    counts = collections.Counter()
    examples = {}
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        category = subtype(line)
        if category is None:
            continue
        counts[category] += 1
        if len(examples.setdefault(category, [])) < 12:
            examples[category].append(number)
    return {"counts": dict(sorted(counts.items())),
            "total": sum(counts.values()),
            "sample_physical_line_numbers": examples}

def self_test():
    assert subtype("<f1r> <! $Q=T>") is None
    assert subtype("<f1r.1,P0> chay") is None
    assert subtype("<f1r.1> chay") == "numbered_folio_locus_other_shape"
    assert subtype("<f1r.1,P0> chay") is None
    assert subtype("<f1r.1junk> chay") == "folio_locus_non_numeric"
    # Historical LINE parser accepts arbitrary comma metadata: do not mislabel it as excluded.\n    assert subtype("<f1r.1,P0junk> chay") is None
    assert subtype("<f1r.a,P0> chay") == "folio_locus_non_numeric"
    assert subtype("<f1r>") == "bare_folio_tag"
    # Literal examples from the frozen ZL3b/IT2a f67r1 panel (physical lines
    # 2815/2823 and 1767/1768 respectively); lexical classification only.
    assert subtype("<f67r1>    <! $Q=I $P=B $F=a $B=1 $I=A $H=4>") == "panel_header_candidate"
    assert subtype("<f67r1.1,@P0>     <%>teeodaiin.shey") == "panel_locus_candidate"
    assert subtype("<f67r1.2,+P0>     daiir.okeody") == "panel_locus_candidate"
    assert subtype("<f67r1.1>") == "panel_locus_candidate"
    assert subtype("<f67r1.1junk>") == "other_f_prefixed_tag"
    assert subtype("<f67r1.1,@P0junk>") == "panel_locus_candidate"
    # Literal ZL3b composite page examples near physical line 5253.
    assert subtype("<fRos>     <! $Q=N $P=D $B=1>") == "named_folio_header_candidate"
    assert subtype("<fRos.1,@L0>      <!1:11>saeeasa?") == "named_folio_locus_candidate"
    assert subtype("<fRos.2,@Cc>      <!10:30>oto.tosaes") == "named_folio_locus_candidate"
    assert subtype("<fRos.bad,@L0> text") == "other_f_prefixed_tag"
    assert subtype("<fRos.1junk>") == "other_f_prefixed_tag"
    assert subtype("<!meta>") == "bang_tag"
    assert subtype("<x>") == "other_tag"
    assert subtype("# comment") is None

def main():
    self_test()
    result = {"status": "DESCRIPTIVE_ONLY_NOT_IVTFF_ADJUDICATION",
              "deterministic": True, "seed": None, "sources": {}}
    for path in INPUTS:
        data = Path(path).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        expected_hash, expected_count = EXPECTED[path]
        if digest != expected_hash:
            raise SystemExit(f"Source SHA-256 mismatch: {path} {digest}")
        stats = analyze(data)
        if stats["total"] != expected_count:
            raise SystemExit(f"Excluded angle denominator changed: {path}: {stats['total']}")
        result["sources"][path] = {"sha256": digest, "bytes": len(data), **stats}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
