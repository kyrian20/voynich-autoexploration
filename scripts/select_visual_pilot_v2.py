#!/usr/bin/env python3
"""Select visual pilot v2 using inventory metadata only; never approve tasks."""
import argparse
import gzip
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_holdout_locus_coverage import (
    SOURCE_NAMES, audit as audit_frozen_holdout, _unique_manifest_keys,
)


def load_verified_frozen_manifest(manifest_bytes: bytes, root: Path) -> dict:
    """Reject altered leaf allocations before a visual pilot can see train rows.

    Reuse the independent frozen-salt/source-hash/coverage auditor, not the
    pilot's own count-only partition checks. This is an operational gate,
    not historically blind or semantic validation.
    """
    # Parse the SAME bytes whose SHA-256 the caller records (no second read).
    manifest = json.loads(manifest_bytes, object_pairs_hook=_unique_manifest_keys)
    sources = {
        name: (root / 'data' / 'transcriptions' / name).read_bytes()
        for name in SOURCE_NAMES
    }
    audit_frozen_holdout(sources, manifest)
    return manifest


def check_inventory_provenance(inventory, manifest):
    """Reject a mismatched edition or row before selecting any train leaves.

    This checks inventory declarations against the frozen manifest. The CLI
    separately hashes the source files; neither check proves image alignment.
    """
    expected = manifest.get('corpora')
    sources = inventory.get('sources')
    if not isinstance(expected, dict) or not isinstance(sources, list):
        raise ValueError('Missing corpus provenance')
    if len(sources) != len(expected):
        raise ValueError('Unexpected source edition count')
    by_edition = {}
    seen_paths = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError('Malformed source provenance')
        edition, path, sha = (source.get('edition'), source.get('path'),
                              source.get('sha256'))
        if (not isinstance(edition, str) or not edition
                or not isinstance(path, str) or not isinstance(sha, str)
                or edition in by_edition or path in seen_paths):
            raise ValueError('Duplicate or malformed source provenance')
        reference = expected.get(Path(path).name)
        if (not reference or reference.get('path') != path
                or reference.get('sha256') != sha):
            raise ValueError('Inventory source differs from holdout manifest')
        by_edition[edition] = sha
        seen_paths.add(path)
    if seen_paths != {item['path'] for item in expected.values()}:
        raise ValueError('Missing or unexpected inventory source')
    records = inventory.get('records')
    if not isinstance(records, list) or not records:
        raise ValueError('Missing inventory records')
    seen_occurrences, seen_loci = set(), set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError('Malformed inventory record')
        edition = row.get('edition')
        if edition not in by_edition or row.get('source_sha256') != by_edition[edition]:
            raise ValueError('Inventory row/source provenance mismatch')
        occurrence = row.get('occurrence_id')
        locus = row.get('id')
        if (not isinstance(occurrence, str) or not occurrence
                or not isinstance(locus, str) or not locus
                or occurrence in seen_occurrences or (edition, locus) in seen_loci):
            raise ValueError('Duplicate or malformed inventory occurrence/locus')
        # Provenance labels alone do not bind a record to its claimed folio.
        # Validate ALL partitions, including held-out and named-page records:
        # a forged test/development locator must not pass merely because it
        # carries a correct source hash. This is a shape check, not a replay
        # of the original source line (see maintenance limitations).
        folio = row.get('folio')
        if (not isinstance(folio, str) or not folio or folio != folio.strip()
                or not locus.startswith(folio + '.')
                or len(locus) <= len(folio) + 1):
            raise ValueError('Inventory locator/folio mismatch')
        seen_occurrences.add(occurrence)
        seen_loci.add((edition, locus))


def check_source_bytes(inventory, root):
    """Check actual source bytes against the inventory's declared hashes."""
    for source in inventory['sources']:
        path = root / source['path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Source bytes differ from frozen provenance: ' + source['path'])


def build(inventory, manifest):
    check_inventory_provenance(inventory, manifest)
    partitions = manifest['partitions']
    sets = {}
    for name in ('train', 'development', 'test'):
        values = partitions[name]
        if (not isinstance(values, list)
                or any(type(value) is not int or value <= 0 for value in values)):
            raise ValueError('Invalid physical leaf IDs in ' + name)
        if len(values) != len(set(values)):
            raise ValueError('Duplicate physical leaf ID in ' + name)
        if manifest['counts'][name] != len(values):
            raise ValueError('Manifest count mismatch in ' + name)
        sets[name] = set(values)
    if (sets['train'] & sets['development']
            or sets['train'] & sets['test']
            or sets['development'] & sets['test']):
        raise ValueError('Partition overlap')
    if len(set.union(*sets.values())) != manifest['eligible_count']:
        raise ValueError('Manifest eligible leaf count mismatch')
    train = sets['train']
    groups = defaultdict(list)
    for row in inventory['records']:
        match = re.fullmatch(r'f(\d+)[rv]\d*', row['folio'])
        if match and int(match[1]) in train:
            locator = row.get('id')
            prefix = row['folio'] + '.'
            if (not isinstance(locator, str)
                    or not locator.startswith(prefix)
                    or len(locator) == len(prefix)):
                raise ValueError('Train locator/folio mismatch')
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
    inventory = json.loads(gzip.decompress(raw))
    manifest = load_verified_frozen_manifest(manifest_raw, root)
    check_inventory_provenance(inventory, manifest)
    check_source_bytes(inventory, root)
    report = build(inventory, manifest)
    report['input_sha256'] = {'inventory_gzip': hashlib.sha256(raw).hexdigest(),
                              'manifest': hashlib.sha256(manifest_raw).hexdigest()}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'leaves': report['selected_leaves'],
                      'records': sum(r['source_records'] for r in report['leaves']),
                      'locators': sum(r['distinct_locators'] for r in report['leaves'])}))

if __name__ == '__main__':
    main()
