#!/usr/bin/env python3
"""Fail on unreviewed corpus changes, additions, removals or empty inputs."""
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'research/CORPUS_INPUT_MANIFEST.json'


def verify(root, manifest):
    expected = {entry['path']: entry for entry in manifest['files']}
    actual = {p.relative_to(root).as_posix() for folder in ('data/transcriptions','data/reference_corpora')
              for p in (root/folder).rglob('*.txt') if p.is_file()}
    errors = [f'Unregistered corpus: {p}' for p in sorted(actual-set(expected))]
    errors += [f'Missing corpus: {p}' for p in sorted(set(expected)-actual)]
    for name in sorted(actual & set(expected)):
        raw = (root/name).read_bytes()
        entry = expected[name]
        if len(raw) != entry['bytes'] or hashlib.sha256(raw).hexdigest() != entry['sha256']:
            errors.append(f'Corpus changed: {name}')
        if not raw and entry.get('status') != 'BLOCKED_EMPTY_DO_NOT_USE':
            errors.append(f'Unexpected empty corpus: {name}')
        if entry.get('status') == 'BLOCKED_EMPTY_DO_NOT_USE' and raw:
            errors.append(f'Quarantined corpus requires provenance review: {name}')
    return errors


if __name__=='__main__':
    manifest=json.loads(MANIFEST.read_text())
    errors=verify(ROOT,manifest)
    print(json.dumps({'files_checked':len(manifest['files']), 'errors':errors,
        'quarantined':[x['path'] for x in manifest['files'] if x['status']=='BLOCKED_EMPTY_DO_NOT_USE'],
        'scope':'Byte identity only; provenance, licensing and IVTFF conformance not certified.'},indent=2))
    raise SystemExit(bool(errors))
