#!/usr/bin/env python3
"""Fail on unreviewed corpus changes, additions, removals or empty inputs."""
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'research/CORPUS_INPUT_MANIFEST.json'


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def linked_path(root, relative):
    """Reject links in a corpus path, including links in parent directories.

    A matching checksum is not proof that the tracked path itself is the frozen
    corpus when its bytes can be redirected outside the repository.
    """
    parts = Path(relative).parts
    return any((root.joinpath(*parts[:i])).is_symlink()
               for i in range(1, len(parts) + 1))


def verify(root, manifest):
    files = manifest.get('files') if isinstance(manifest, dict) else None
    if not isinstance(files, list) or not files:
        return ['Manifest requires a nonempty files list']
    seen, schema_errors = set(), []
    statuses = {'FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED', 'BLOCKED_EMPTY_DO_NOT_USE'}
    for entry in files:
        if not isinstance(entry, dict):
            schema_errors.append('Manifest entry must be an object')
            continue
        name = entry.get('path')
        if not isinstance(name, str) or not re.fullmatch(r'data/(?:transcriptions|reference_corpora)/[^\\]+\.txt', name) or '..' in Path(name).parts:
            schema_errors.append(f'Invalid corpus path: {name}')
            continue
        if name in seen:
            schema_errors.append(f'Duplicate manifest path: {name}')
        seen.add(name)
        if type(entry.get('bytes')) is not int or entry['bytes'] < 0:
            schema_errors.append(f'Invalid byte size: {name}')
        if not isinstance(entry.get('sha256'), str) or not re.fullmatch('[0-9a-f]{64}', entry['sha256']):
            schema_errors.append(f'Invalid SHA-256: {name}')
        if entry.get('status') not in statuses:
            schema_errors.append(f'Invalid corpus status: {name}')
    if schema_errors:
        return schema_errors
    expected = {entry['path']: entry for entry in manifest['files']}
    actual = {p.relative_to(root).as_posix() for folder in ('data/transcriptions','data/reference_corpora')
              for p in (root/folder).rglob('*.txt') if p.is_file()}
    errors = [f'Unregistered corpus: {p}' for p in sorted(actual-set(expected))]
    errors += [f'Symlink corpus path forbidden: {p}' for p in sorted(expected)
               if linked_path(root, p)]
    errors += [f'Missing corpus: {p}' for p in sorted(set(expected)-actual)]
    for name in sorted(actual & set(expected)):
        if linked_path(root, name):
            continue  # Already reported; never follow an untrusted link to read bytes.
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
    manifest=json.loads(MANIFEST.read_text(), object_pairs_hook=unique_keys)
    errors=verify(ROOT,manifest)
    print(json.dumps({'files_checked':len(manifest['files']), 'errors':errors,
        'quarantined':[x['path'] for x in manifest['files'] if x['status']=='BLOCKED_EMPTY_DO_NOT_USE'],
        'scope':'Byte identity only; provenance, licensing and IVTFF conformance not certified.'},indent=2))
    raise SystemExit(bool(errors))
