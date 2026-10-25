#!/usr/bin/env python3
"""Export a flattened PNG candidate; never approve a mask or update the queue.

Requires Pillow==12.3.0. This is a coordinator tool: masking geometry still
requires visual review and an independent reviewer before annotation use.
"""
import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

from PIL import Image
if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.render_coordinator_mask_preview import rectangle


def export_candidate(plan, source):
    if hashlib.sha256(source).hexdigest() != plan['source_sha256']:
        raise ValueError('Source image SHA256 mismatch')
    size = plan['source_size']
    if not isinstance(size, list) or len(size) != 2 or any(type(v) is not int or v <= 0 for v in size):
        raise ValueError('Invalid source dimensions')
    if not plan.get('crop_xywh') or not plan.get('mask_rectangles_xywh'):
        raise ValueError('No crop/masks; manual segmentation required')
    x, y, w, h = rectangle(plan['crop_xywh'], size)
    masks = [rectangle(r, size) for r in plan['mask_rectangles_xywh']]
    with Image.open(io.BytesIO(source)) as original:
        if original.size != tuple(size):
            raise ValueError('Decoded image dimensions differ from plan')
        if getattr(original, 'n_frames', 1) != 1:
            raise ValueError('Multiple image frames are not supported')
        if original.getexif().get(274, 1) != 1:
            raise ValueError('Orientation must be adjudicated in source coordinates')
        # A fresh RGB canvas carries no source EXIF, comments, ICC or PNG text.
        canvas = Image.new('RGB', original.size)
        canvas.paste(original.convert('RGB'))
    for mx, my, mw, mh in masks:
        canvas.paste((0, 0, 0), (mx, my, mx + mw, my + mh))
    crop = canvas.crop((x, y, x + w, y + h))
    output = io.BytesIO()
    crop.save(output, format='PNG')
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--folio', required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    plans = json.loads(args.plan.read_text())['plans']
    matches = [p for p in plans if p['folio'] == args.folio]
    if len(matches) != 1:
        raise ValueError('Expected one exact folio plan')
    if args.out.suffix.lower() != '.png':
        raise ValueError('Output must have .png extension')
    data = export_candidate(matches[0], args.source.read_bytes())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Do not overwrite a reviewed asset or the source.
    with args.out.open('xb') as output:
        output.write(data)
    print(json.dumps({'status': 'FLATTENED_CANDIDATE_NOT_REVIEWED',
                      'annotation_ready': False, 'independent_review': False,
                      'output_sha256': hashlib.sha256(data).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
