#!/usr/bin/env python3
"""Select visual pilot v2 using inventory metadata only; never approve tasks."""
import argparse
import gzip
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

def build(inventory, manifest):
    partitions = manifest['partitions']
    train = set(partitions['train'])
    if train & (set(partitions['development']) | set(partitions['test'])):
        raise ValueError('Partition overlap')
    groups = defaultdict(list)
    for row in inventory['records']:
        match = re.fullmatch(r'f(\d+)[rv]\d*', row['folio'])
        if match and int(match[1]) in train:
            groups[int(match[1])].append(row)
    selected = sorted(groups)[:12]
    leaves = []
    for leaf in selected:
        rows = groups[leaf]
        leaves.append({
            'leaf': leaf, 'source_records': len(rows),
            'distinct_locators': len({r['id'] for r in rows}),
            'folios': sorted({r['folio'] for r in rows}),
            'locators': sorted({r['id'] for r in rows}),
            'archived_source_folios': sorted({r['folio'] for r in rows
                                              if r['image_source_archived']}),
            'annotation_ready': False})
    return {'status': 'SELECTED_NOT_ANNOTATION_READY', 'selection_version': 2,
            'eligible_train_leaves': sorted(groups), 'selected_leaves': selected,
            'leaves': leaves,
            'limitations': ['Metadata eligibility is not verified object alignment.',
                            'Historically exposed training material.',
                            'No masks approved or independent annotations produced.']}

def main():
    root = Path(__file__).resolve().parents[1]
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inventory', type=Path, default=root/'research/decipherment/2026-10-25-label-inventory/inventory.json.gz')
    p.add_argument('--manifest', type=Path, default=root/'research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    raw, manifest_raw = args.inventory.read_bytes(), args.manifest.read_bytes()
    report = build(json.loads(gzip.decompress(raw)), json.loads(manifest_raw))
    report['input_sha256'] = {'inventory_gzip': hashlib.sha256(raw).hexdigest(),
                              'manifest': hashlib.sha256(manifest_raw).hexdigest()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'leaves': report['selected_leaves'],
                      'records': sum(r['source_records'] for r in report['leaves']),
                      'locators': sum(r['distinct_locators'] for r in report['leaves'])}))

if __name__ == '__main__':
    main()
