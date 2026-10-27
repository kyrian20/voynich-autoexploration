#!/usr/bin/env python3
"""Bind archived label-inventory rows to exact source lines without rewriting them.

This is a provenance audit, not an independent IVTFF conformity certificate.
The original inventory builder used utf-8-sig decoding and splitlines().
"""
import argparse
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_label_occurrence_inventory import ROW
from scripts.select_visual_pilot_v2 import (
    check_inventory_provenance,
    check_source_bytes,
    load_unique_inventory,
)

INVENTORY = Path("research/decipherment/2026-10-25-label-inventory/inventory.json.gz")
MANIFEST = Path("research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json")


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def audit(inventory, manifest, root):
    """Check every archived row against the corresponding original physical line.

    Uses the frozen inventory's source_line, raw_line, raw_line_sha256 and
    occurrence_id. No tokenization, semantic inference or held-out fitting.
    """
    check_inventory_provenance(inventory, manifest)
    check_source_bytes(inventory, root)
    source_lines = {}
    counts = Counter()
    for source in inventory["sources"]:
        raw = (root / source["path"]).read_bytes()
        source_lines[source["edition"]] = raw.decode("utf-8-sig").splitlines()
    seen_lines = set()
    for row in inventory["records"]:
        edition = row["edition"]
        number = row.get("source_line")
        if type(number) is not int or not 1 <= number <= len(source_lines[edition]):
            raise ValueError("Invalid inventory source_line: " + edition)
        key = (edition, number)
        if key in seen_lines:
            raise ValueError("Duplicate physical source line: " + str(key))
        seen_lines.add(key)
        original = source_lines[edition][number - 1]
        if row.get("occurrence_id") != f"{edition}:{number}":
            raise ValueError("Inventory occurrence/source_line mismatch: " + str(key))
        if row.get("raw_line") != original:
            raise ValueError("Inventory raw_line differs from original: " + str(key))
        if row.get("raw_line_sha256") != sha256(original.encode("utf-8")):
            raise ValueError("Inventory raw_line_sha256 mismatch: " + str(key))
        match = ROW.match(original)
        if match is None:
            raise ValueError("Original line is not a parsed locus: " + str(key))
        folio, locus_id, code, body = match.groups()
        if (row.get("folio") != folio
                or row.get("locus_id") != locus_id
                or row.get("id") != f"{folio}.{locus_id}"
                or row.get("raw_body") != body
                or row.get("locus") != code.split(";")[0][1:]):
            raise ValueError("Inventory fields differ from original locus: " + str(key))
        counts[edition] += 1
    return {
        "status": "SOURCE_LINE_BINDING_PASS",
        "scope": "Archived L/R inventory rows only; exact physical lines and selected metadata",
        "record_count": len(inventory["records"]),
        "records_by_edition": dict(sorted(counts.items())),
        "source_sha256": {s["edition"]: s["sha256"] for s in inventory["sources"]},
        "limitations": [
            "Does not independently certify IVTFF tokenization or completeness of the L/R selection.",
            "Does not verify image-to-object alignment or independent semantic annotation.",
            "Does not consume development/test outcomes or assert a translation.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    inventory_bytes = (root / args.inventory).read_bytes()
    manifest_bytes = (root / args.manifest).read_bytes()
    inventory = load_unique_inventory(inventory_bytes)
    manifest = json.loads(manifest_bytes)
    result = audit(inventory, manifest, root)
    result["input_sha256"] = {
        "inventory_gzip": sha256(inventory_bytes),
        "manifest": sha256(manifest_bytes),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "records": result["record_count"],
                      "by_edition": result["records_by_edition"]}, sort_keys=True))


if __name__ == "__main__":
    main()
