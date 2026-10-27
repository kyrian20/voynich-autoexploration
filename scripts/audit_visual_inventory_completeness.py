#!/usr/bin/env python3
"""Independent physical-line census of the archived explicit L/R inventory.

Checks selection completeness under the documented ROW/HEADER policy,
not full IVTFF conformance or semantic validity. Archived inputs are immutable.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_visual_inventory_source_rows import audit as audit_source_binding
from scripts.select_visual_pilot_v2 import load_unique_inventory, load_verified_frozen_manifest

INVENTORY = Path('research/decipherment/2026-10-25-label-inventory/inventory.json.gz')
MANIFEST = Path('research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json')
# Separate scanner from the inventory builder; this is a physical-line census.
RECORD = re.compile(r'<([^<>.,\s]+)\.([^<>,\s]+),([^<>]+)>\s*(.*)')
PAGE = re.compile(r'<([^<>.,\s]+)>\s*(.*)')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def census(raw):
    """Return source line numbers of explicit L/R loci and undecidable lines."""
    selected, undecidable = set(), []
    for number, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        if not line.strip() or line.lstrip().startswith('#') or PAGE.fullmatch(line):
            continue
        match = RECORD.fullmatch(line)
        if match is None:
            undecidable.append(number)
            continue
        marker = match.group(3).split(';', 1)[0]
        if len(marker) < 2:
            undecidable.append(number)
        elif marker[1:].startswith(('L', 'R')):
            selected.add(number)
    return selected, undecidable


def audit(inventory, manifest, root):
    """Compare independent L/R census with ALL archived rows, including holdout."""
    audit_source_binding(inventory, manifest, root)
    by_edition = {}
    for row in inventory['records']:
        by_edition.setdefault(row['edition'], set()).add(row['source_line'])
    counts = {}
    for source in inventory['sources']:
        edition = source['edition']
        raw = (root / source['path']).read_bytes()
        expected, undecidable = census(raw)
        if undecidable:
            raise ValueError(f'Undecidable physical lines in {edition}: {undecidable[:20]}')
        observed = by_edition.get(edition, set())
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        if missing or extra:
            raise ValueError(f'L/R selection mismatch {edition}: missing={missing[:20]} extra={extra[:20]}')
        if source.get('selected_rows') != len(expected):
            raise ValueError(f'Archived selected_rows disagrees with census: {edition}')
        counts[edition] = len(expected)
    return {
        'status': 'COMPLETE_UNDER_DECLARED_LR_ROW_POLICY',
        'selected_by_edition': dict(sorted(counts.items())),
        'selected_total': sum(counts.values()),
        'source_sha256': {s['edition']: s['sha256'] for s in inventory['sources']},
        'limitations': [
            'Independent physical-line census uses the declared L/R selection grammar; not a full independent IVTFF parser.',
            'A malformed source line is a blocking undecidable line, not silently assumed to be non-L/R.',
            'Does not establish image-to-object alignment, semantic truth, or a translation.',
            'All partitions are audited for provenance only; no held-out outcomes are evaluated.',
        ],
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--inventory', type=Path, default=INVENTORY)
    p.add_argument('--manifest', type=Path, default=MANIFEST)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    root = args.root.resolve()
    inventory_bytes = (root / args.inventory).read_bytes()
    manifest_bytes = (root / args.manifest).read_bytes()
    report = audit(load_unique_inventory(inventory_bytes), load_verified_frozen_manifest(manifest_bytes, root), root)
    report['input_sha256'] = {'inventory_gzip': digest(inventory_bytes), 'manifest': digest(manifest_bytes)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'selected_total': report['selected_total'],
                      'by_edition': report['selected_by_edition']}, sort_keys=True))


if __name__ == '__main__':
    main()
