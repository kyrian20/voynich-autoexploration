#!/usr/bin/env python3
"""Retrieve the exact three Yale canvases used for potential-anchor inspection."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen

MANIFEST = 'https://collections.library.yale.edu/manifests/2002046'
LABELS = ('2r', '41v', '65r')


def select_images(manifest):
    selected = []
    for label in LABELS:
        matches = [c for c in manifest['items']
                   if c.get('label', {}).get('none') == [label]]
        if len(matches) != 1:
            raise ValueError(f'Expected one exact canvas label: {label}')
        c = matches[0]
        body = c['items'][0]['items'][0]['body']
        url = body['id']
        if urlsplit(url).scheme != 'https' or urlsplit(url).netloc != 'collections.library.yale.edu':
            raise ValueError('Unexpected source-image host')
        selected.append({
            'folio': 'f'+label, 'canvas': c['id'], 'url': url,
            'width': body['width'], 'height': body['height']})
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-dir', type=Path, required=True)
    args = parser.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    with urlopen(MANIFEST, timeout=40) as response:
        raw = response.read()
    manifest = json.loads(raw)
    selected = select_images(manifest)
    (args.cache_dir/'yale-manifest.json').write_bytes(raw)
    for entry in selected:
        with urlopen(entry['url'], timeout=40) as response:
            data = response.read()
        if not data.startswith(bytes.fromhex('ffd8ff')):
            raise ValueError('Source response is not a JPEG')
        (args.cache_dir/(entry['folio']+'.jpg')).write_bytes(data)
        entry.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    print(json.dumps({
        'manifest_url': MANIFEST,
        'manifest_sha256': hashlib.sha256(raw).hexdigest(),
        'requiredStatement': manifest.get('requiredStatement'),
        'images': selected}, indent=2))


if __name__ == '__main__':
    main()

