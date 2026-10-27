#!/usr/bin/env python3
"""Prepare coordinator and annotator packets; no image or semantic inference."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_label_partition_coverage import load_verified_coverage_inputs

INVENTORY = ROOT / 'research/decipherment/2026-10-25-label-inventory/inventory.json.gz'
MANIFEST = ROOT / 'research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json'
CATEGORIES = ('plant_or_plant_part', 'human_or_body', 'animal',
              'astronomical_or_geometric', 'vessel_or_object', 'mixed',
              'no_identifiable_referent', 'uncertain')

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def build(inventory):
    groups = {}
    for record in inventory['records']:
        groups.setdefault(record['id'], []).append(record)
    queue, mapping = [], []
    for locator, rows in sorted(groups.items()):
        task_id = 'visual-' + sha(locator.encode())[:20]
        queue.append({'task_id': task_id,
            'status': 'BLOCKED_MASKED_IMAGE_AND_REGION_REQUIRED',
            'masked_image_path': None, 'masked_image_sha256': None,
            'mask_reviewed_by': None, 'annotation_ready': False})
        mapping.append({'task_id': task_id, 'locator': locator,
            'folio': rows[0]['folio'], 'region_xywh': None,
            'shared_illustration_group': None,
            'source_occurrence_ids': [r['occurrence_id'] for r in rows],
            'source_rows': [{'edition': r['edition'], 'source_line': r['source_line'],
                'source_sha256': r['source_sha256']} for r in rows],
            'archived_image_sources': [r['image_source_archived'] for r in rows
                                       if r['image_source_archived']],
            'warning': 'Locator pairing only; not verified label-to-object alignment.'})
    if len({r['task_id'] for r in queue}) != len(queue):
        raise ValueError('Task ID collision')
    return {'status': 'PREPARATION_ONLY_NO_BLIND_ANNOTATION_PERFORMED',
            'categories': list(CATEGORIES), 'tasks': queue}, {'tasks': mapping}

def validate_annotation(row, tasks):
    required = ('task_id', 'annotator_id', 'round', 'category', 'confidence',
                'image_sha256', 'timestamp', 'saw_eva', 'saw_prior_hypotheses',
                'external_referent', 'external_source', 'notes')
    if any(k not in row for k in required):
        raise ValueError('Missing annotation fields')
    if row['task_id'] not in tasks:
        raise ValueError('Unknown task')
    task = tasks[row['task_id']]
    if (task.get('annotation_ready') is not True or
            task.get('status') != 'READY' or not task.get('masked_image_path') or
            not task.get('mask_reviewed_by') or
            not isinstance(task.get('masked_image_sha256'), str) or
            len(task['masked_image_sha256']) != 64 or
            any(c not in '0123456789abcdef' for c in task['masked_image_sha256'])):
        raise ValueError('Task lacks reviewed masked image')
    if row['image_sha256'] != task['masked_image_sha256']:
        raise ValueError('Annotation image hash mismatch')
    if not isinstance(row['annotator_id'], str) or not row['annotator_id'].strip():
        raise ValueError('Annotator identity required')
    if row['category'] not in CATEGORIES or row['confidence'] not in ('low', 'medium', 'high'):
        raise ValueError('Unsupported category/confidence')
    if type(row['saw_eva']) is not bool or type(row['saw_prior_hypotheses']) is not bool:
        raise ValueError('Exposure declarations must be boolean')
    if row['round'] != 'independent_initial':
        raise ValueError('Only independent initial annotations accepted by this validator')
    if not row['timestamp'] or not isinstance(row['timestamp'], str):
        raise ValueError('Timestamp required')
    if row['saw_eva'] or row['saw_prior_hypotheses']:
        raise ValueError('Exposed annotation cannot enter blinded initial evaluation')
    if row['external_referent'] is not None and not row['external_source']:
        raise ValueError('Named referent requires a source')
    return True

def prepare_verified_queue(inventory_bytes, manifest_bytes, root):
    """Verify frozen source rows and leaf partitions before exporting packets.

    The direct build() helper remains fixture-only; this is the CLI input gate.
    Neither this check nor the queue authorizes visual annotations.
    """
    inventory, _ = load_verified_coverage_inputs(inventory_bytes, manifest_bytes, root)
    queue, mapping = build(inventory)
    queue['inventory_archive_sha256'] = sha(inventory_bytes)
    return queue, mapping


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', type=Path, default=INVENTORY)
    parser.add_argument('--manifest', type=Path, default=MANIFEST)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    raw = args.inventory.read_bytes()
    manifest_raw = args.manifest.read_bytes()
    queue, mapping = prepare_verified_queue(raw, manifest_raw, ROOT)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name, value in [('annotator-queue.json.gz', queue), ('coordinator-map.json.gz', mapping)]:
        data = gzip.compress((json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode(), mtime=0)
        (args.out_dir / name).write_bytes(data)
        hashes[name] = sha(data)
    (args.out_dir / 'SHA256.json').write_text(json.dumps(hashes, indent=2)+'\n')
    print(json.dumps({'tasks': len(queue['tasks']), 'ready': 0,
                      'source_rows': len(inventory['records'])}, sort_keys=True))

if __name__ == '__main__':
    main()
