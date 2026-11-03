#!/usr/bin/env python3
"""Check reconstructed files against a pinned historical SHA-256 manifest.

A supplied test manifest can check bytes, but cannot certify the historical
run-03 identity. Neither result attests that a simulator was actually run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'experiments/common_battery_2026_10_22/data/run-03/SHA256.json'
# Frozen run-03 manifest bytes, including its trailing newline.
HISTORICAL_MANIFEST_SHA256 = 'f5e8d316e7e0712ef9cfbc20be158eef5159aca9daf4bfc4f254b96ebc95bf8b'
HISTORICAL_FILES = frozenset({
    'resultados.json', 'seleccion.json', 'tokens.jsonl.gz', 'vistas_referencia.json',
})


def _regular_file(path):
    # A symlink in any ancestor could redirect a seemingly local receipt to
    # unrelated bytes. This is a provenance gate, not a sandbox.
    absolute = path.absolute()
    if any(part.is_symlink() for part in (absolute, *absolute.parents)):
        raise ValueError(f'Symlinked reconstruction path: {path}')
    if not path.is_file():
        # Preserve FileNotFoundError for missing files in the public API.
        if not path.exists():
            raise FileNotFoundError(path)
        raise ValueError(f'Not a regular reconstruction file: {path}')


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate manifest key: {key}')
        result[key] = value
    return result


def verify(directory, manifest=MANIFEST):
    manifest = Path(manifest)
    directory = Path(directory)
    _regular_file(manifest)
    raw_manifest = manifest.read_bytes()
    manifest_sha256 = hashlib.sha256(raw_manifest).hexdigest()
    pinned = manifest.absolute() == MANIFEST.absolute()
    if pinned and manifest_sha256 != HISTORICAL_MANIFEST_SHA256:
        raise ValueError('Historical run-03 manifest SHA-256 mismatch')
    expected = json.loads(raw_manifest.decode('utf-8'), object_pairs_hook=_unique_pairs)
    if not isinstance(expected, dict) or not expected:
        raise ValueError('Empty or malformed reconstruction manifest')
    if pinned and set(expected) != HISTORICAL_FILES:
        raise ValueError('Historical run-03 manifest file set mismatch')
    checked = []
    for name, digest in expected.items():
        if (not isinstance(name, str) or not name or '/' in name or '\\' in name
                or Path(name).name != name or name in ('.', '..')):
            raise ValueError('Manifest entries must be filenames')
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'Invalid SHA-256 digest in manifest: {name}')
        file = directory / name
        _regular_file(file)
        actual = hashlib.sha256(file.read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f'Reconstruction hash mismatch: {name}')
        checked.append({'file': name, 'sha256': actual})
    return {
        'status': ('EXACT_HISTORICAL_HASH_MATCH' if pinned
                   else 'SUPPLIED_MANIFEST_HASH_MATCH'),
        'historical_manifest_pinned': pinned,
        'manifest_sha256': manifest_sha256,
        'checked': checked,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.directory), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
