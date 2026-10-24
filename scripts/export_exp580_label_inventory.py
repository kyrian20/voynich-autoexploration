#!/usr/bin/env python3
"""Export EXP-580's *historical-parser* label-exclusive inventory with loci.

This reuses the original experiment's globals, not an independent IVTFF parser.
"""
import argparse
from collections import Counter, defaultdict
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/exp_580_label_corpus_grammar/script.py"
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"


def build():
    if not SOURCE.is_file() or not CORPUS.is_file():
        raise RuntimeError("BLOCKED: historical script/corpus missing")
    with redirect_stdout(io.StringIO()):
        namespace = runpy.run_path(str(SOURCE), run_name="exp580_inventory_replay")
    labels = namespace["label_lines"]
    body = namespace["body_lines"]
    body_types = {token for _, _, tokens, _ in body for token in tokens}
    places = defaultdict(list)
    for folio, locus, tokens, _lang in labels:
        for token in tokens:
            if token not in body_types:
                places[token].append({"folio": folio, "locus": locus})
    inventory = [
        {"eva": word, "count": len(loci), "occurrences": loci}
        for word, loci in sorted(places.items())
    ]
    label_types = {token for _, _, tokens, _ in labels for token in tokens}
    summary = {
        "label_lines": len(labels),
        "body_lines": len(body),
        "label_types": len(label_types),
        "body_types": len(body_types),
        "shared_types": len(label_types & body_types),
        "exclusive_types": len(inventory),
        "exclusive_tokens": sum(x["count"] for x in inventory),
    }
    expected = (1087, 4113, 1036, 7030, 489, 547)
    actual = tuple(summary[k] for k in (
        "label_lines", "body_lines", "label_types", "body_types",
        "shared_types", "exclusive_types"
    ))
    if actual != expected:
        raise RuntimeError(f"BLOCKED: historical inventory drift: {actual} != {expected}")
    return {
        "status": "HISTORICAL_PARSER_REPLAY_NOT_INDEPENDENT",
        "source_script_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_corpus_sha256": hashlib.sha256(CORPUS.read_bytes()).hexdigest(),
        "limitations": [
            "Uses original EXP-580 parser and first alternative readings",
            "Folio+locus are not unique line identifiers; multiple records can share them",
            "Exclusivity is relative to historical EXP-580 body-token classification",
            "No independent visual or semantic validation",
        ],
        "summary": summary,
        "inventory": inventory,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {report['summary']['exclusive_types']} historical exclusive EVA types to {args.out}")


if __name__ == "__main__":
    main()
