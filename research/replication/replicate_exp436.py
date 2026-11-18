#!/usr/bin/env python3
"""Independent provenance-first EXP-436 replication; standard library only."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "latin": "data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt",
    "italian": "data/reference_corpora/italian/dante_divina_commedia.txt",
    "german": "data/reference_corpora/german/goethe_faust.txt",
    "french": "data/reference_corpora/french/voltaire_candide_4650.txt",
}
TOKEN = re.compile(r"[^\\W\\d_]+", re.UNICODE)
START = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\*\*\*", re.I)
END = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK[^\n]*\*\*\*", re.I)

def body(text):
    start, end = START.search(text), END.search(text)
    if not start or not end or end.start() <= start.end():
        raise ValueError("Missing Gutenberg START/END markers; refusing boilerplate")
    return text[start.end():end.start()]

def analyze(words):
    counts = Counter(words)
    groups = {
        "hapax": [w for w in words if counts[w] == 1],
        "mid": [w for w in words if 2 <= counts[w] <= 4],
        "frequent": [w for w in words if counts[w] >= 5],
    }
    means = {k: sum(map(len, ws)) / len(ws) if ws else None for k, ws in groups.items()}
    ratio = means["hapax"] / means["frequent"] if means["hapax"] is not None and means["frequent"] else None
    return {
        "tokens": len(words), "types": len(counts),
        "hapax_types": sum(c == 1 for c in counts.values()),
        "class_tokens": {k: len(ws) for k, ws in groups.items()},
        "mean_lengths": means, "hapax_frequent_ratio": ratio,
    }

def run(root):
    results = {
        "method": "Gutenberg body only; Unicode alphabetic tokens, lowercase, minimum 2 letters; token-weighted mean lengths",
        "limitations": "External controls only. Does not validate VMS measurements or identify its language.",
        "corpora": {},
    }
    for lang, relative in SOURCES.items():
        data = (root / relative).read_bytes()
        content = body(data.decode("utf-8-sig"))
        words = [w.lower() for w in TOKEN.findall(content) if len(w) >= 2]
        results["corpora"][lang] = {
            "path": relative, "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data), **analyze(words),
        }
    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = json.dumps(run(args.root), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")

if __name__ == "__main__":
    main()
