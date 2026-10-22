#!/usr/bin/env python3
"""Fetch the exact historical comparator linked by the British Library catalogue."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

MANIFEST = 'https://bl.digirati.io/iiif/ark:/81055/vdc_100058663072.0x000001'


def select_comparator(manifest):
    matches = [c for c in manifest['items']
               if c.get('label', {}).get('en') == ['f.27v']]
    if len(matches) != 1:
        raise ValueError('Expected one exact f.27v canvas')
    c = matches[0]
    body = c['items'][0]['items'][0]['body']
    service = body['service'][0]['@id']
    if not service.startswith('https://bl.digirati.io/images/ark:/81055/'):
        raise ValueError('Unexpected image service')
    return {'canvas':c['id'], 'canvas_label':c['label'],
            'image_url':service+'/full/full/0/default.jpg',
            'width':c['width'], 'height':c['height']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--cache-dir',type=Path,required=True)
    args=parser.parse_args()
    args.cache_dir.mkdir(parents=True,exist_ok=True)
    with urlopen(MANIFEST,timeout=40) as r:
        raw=r.read()
    m=json.loads(raw)
    receipt={'manifest_url':MANIFEST,
             'manifest_sha256':hashlib.sha256(raw).hexdigest(),
             'rights':m.get('rights'),**select_comparator(m)}
    with urlopen(receipt['image_url'],timeout=40) as r:
        image=r.read()
    if not image.startswith(bytes.fromhex('ffd8ff')):
        raise ValueError('Not a JPEG response')
    (args.cache_dir/'egerton747-manifest.json').write_bytes(raw)
    (args.cache_dir/'egerton747-27v.jpg').write_bytes(image)
    receipt.update(image_sha256=hashlib.sha256(image).hexdigest(),
                   image_bytes=len(image))
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()

