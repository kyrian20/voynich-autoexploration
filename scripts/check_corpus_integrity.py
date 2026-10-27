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


# Independent, reviewed baseline from research/CORPUS_INPUT_MANIFEST.json at
# master 99f860444b97171963aacaa0a458e8ec17f3c49c (2026-10-27).
# Do not regenerate these pins from the manifest under test: otherwise a
# coordinated edit to both corpus bytes and manifest could pass the checksum.
FROZEN_SOURCE_COMMIT = "2da0b63617a3d6dc29b47b99a731a8c9692e9aaa"
FROZEN_CORPUS = {
    "data/reference_corpora/arabic/quran_arabic.txt": (112268, "8adc6237eda291ec5e35c0ca1574b9eac6641c387b7f6d5183b112bd766f88c4", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/english/kjv_bible.txt": (1518921, "7fe73321d11257c172a578c4bf35c53ba1859a3b0cbf37cbcd207df2faa8ead6", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/german/goethe_faust.txt": (218446, "470fab58aa9013efde23f082ba0061f1fbc60a5f9b85451d5b4a63b8f9c21e16", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/italian/dante_divina_commedia.txt": (626098, "76a06f77ea52d4c815f27251fa253ddc8383dfdae49a44065e45a15adec828a6", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt": (169680, "026e9c30e84e2418936db5784c1857c30780066df0ae724c959846aac75b1e33", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/latin/caesar_gallic_wars.txt": (964557, "eaa456256c46507f872efd965335b370605e6d323ca89ef2012cb71b516183d7", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/latin/cicero_caesar_latin.txt": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "BLOCKED_EMPTY_DO_NOT_USE"),
    "data/reference_corpora/latin/cicero_de_officiis_latin.txt": (720407, "3a33a076d3dda42673ec7ab0331ae7e58fc150e7e92751c0adf6d1db7297b670", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/latin/virgil_aeneid_latin.txt": (495789, "c844c7d1c6fa4cf798e8bd8b13a855054820811add902e63db7edea5a4f3aa37", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/reference_corpora/latin/vulgate.txt": (5650501, "d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/transcriptions/eva_it2a.txt": (342104, "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/transcriptions/eva_zl3b.txt": (411671, "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/transcriptions/v101_claston.txt": (248567, "f278a451d873c520f7ab509c4af12152698a1d3efd2353924e177a565c17ba7e", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
    "data/transcriptions/zl3a.txt": (411710, "56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2", "FROZEN_BYTES_NOT_SCIENTIFICALLY_VALIDATED"),
}


def verify_frozen_manifest(manifest):
    """Check manifest metadata against an independent, reviewed 14-file lock."""
    if not isinstance(manifest, dict):
        return ['Invalid frozen manifest object']
    errors = []
    if manifest.get('schema_version') != 1 or manifest.get('source_commit') != FROZEN_SOURCE_COMMIT:
        errors.append('Frozen manifest version/source changed without review')
    rows = manifest.get('files')
    if not isinstance(rows, list):
        return errors + ['Frozen manifest files missing']
    observed = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            errors.append('Invalid frozen manifest row')
            continue
        name = row['path']
        if name in observed:
            errors.append(f'Duplicate frozen manifest path: {name}')
        observed[name] = row
    for name in sorted(set(FROZEN_CORPUS) - set(observed)):
        errors.append(f'Frozen corpus removed from manifest: {name}')
    for name in sorted(set(observed) - set(FROZEN_CORPUS)):
        errors.append(f'Unreviewed corpus added to frozen manifest: {name}')
    for name in sorted(set(FROZEN_CORPUS) & set(observed)):
        row = observed[name]
        current = (row.get('bytes'), row.get('sha256'), row.get('status'))
        if type(row.get('bytes')) is not int or current != FROZEN_CORPUS[name]:
            errors.append(f'Frozen corpus metadata changed without review: {name}')
    return errors


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
    folders = ('data/transcriptions', 'data/reference_corpora')
    actual = {p.relative_to(root).as_posix() for folder in folders
              for p in (root/folder).rglob('*.txt') if p.is_file()}
    # A dangling .txt link fails is_file(), and rglob('*.txt') misses
    # symlinked directories entirely. Neither is a reviewed corpus addition.
    # Inventory links independently, without dereferencing their targets.
    links = {p.relative_to(root).as_posix() for folder in folders
             for p in (root/folder).rglob('*') if p.is_symlink()}
    links.update(folder for folder in folders if (root/folder).is_symlink())
    errors = [f'Unregistered corpus: {p}' for p in sorted(actual-set(expected))]
    errors += [f'Unregistered symlink in corpus tree: {p}'
               for p in sorted(links-set(expected))]
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
    errors=verify_frozen_manifest(manifest) + verify(ROOT,manifest)
    print(json.dumps({'files_checked':len(manifest['files']), 'errors':errors,
        'quarantined':[x['path'] for x in manifest['files'] if x['status']=='BLOCKED_EMPTY_DO_NOT_USE'],
        'scope':'Byte identity only; provenance, licensing and IVTFF conformance not certified.'},indent=2))
    raise SystemExit(bool(errors))
