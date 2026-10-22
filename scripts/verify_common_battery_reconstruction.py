#!/usr/bin/env python3
"""Verify a temporary reconstruction against the historical hashes, without publishing data."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT/'experiments/common_battery_2026_10_22/data/run-03/SHA256.json'


def verify(directory, manifest=MANIFEST):
    expected = json.loads(Path(manifest).read_text())
    checked = []
    for name, digest in expected.items():
        if Path(name).name != name:
            raise ValueError('Manifest entries must be filenames')
        actual = hashlib.sha256((Path(directory)/name).read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f'Reconstruction hash mismatch: {name}')
        checked.append({'file':name, 'sha256':actual})
    if not checked:
        raise ValueError('Empty reconstruction manifest')
    return {'status':'EXACT_HISTORICAL_HASH_MATCH', 'checked':checked}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.directory),ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
