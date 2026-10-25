#!/usr/bin/env python3
"""Render a layered SVG for coordinator inspection, NEVER an annotator asset.

The original image remains embedded beneath rectangles. Do not distribute this
SVG as blinded input. A flattened asset and independent review are still needed.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'

def rectangle(value, bounds):
    if not isinstance(value, list) or len(value) != 4 or any(type(v) is not int for v in value):
        raise ValueError('Rectangle requires four integer coordinates')
    x,y,w,h = value
    if min(x,y)<0 or min(w,h)<=0 or x+w>bounds[0] or y+h>bounds[1]:
        raise ValueError('Rectangle outside source image')
    return x,y,w,h

def render(plan, source):
    if hashlib.sha256(source).hexdigest() != plan['source_sha256']:
        raise ValueError('Source image SHA256 mismatch')
    size=plan['source_size']
    if not isinstance(size,list) or len(size)!=2 or any(type(v) is not int or v<=0 for v in size):
        raise ValueError('Invalid source dimensions')
    if not plan.get('crop_xywh') or not plan.get('mask_rectangles_xywh'):
        raise ValueError('No proposed crop/masks; manual segmentation required')
    crop=rectangle(plan['crop_xywh'],size)
    masks=[rectangle(r,size) for r in plan['mask_rectangles_xywh']]
    x,y,w,h=crop
    root=ET.Element('svg',xmlns=SVG,width=str(w),height=str(h),viewBox=f'{x} {y} {w} {h}')
    ET.SubElement(root,'title').text='COORDINATOR ONLY: layered mask proposal, not blinded input'
    ET.SubElement(root,'desc').text='Original image is embedded and recoverable. No independent mask review.'
    ET.SubElement(root,'image',x='0',y='0',width=str(size[0]),height=str(size[1]),
                  **{'{http://www.w3.org/1999/xlink}href': 'data:image/jpeg;base64,'+base64.b64encode(source).decode()})
    for mx,my,mw,mh in masks:
        ET.SubElement(root,'rect',x=str(mx),y=str(my),width=str(mw),height=str(mh),fill='black')
    return ET.tostring(root,encoding='utf-8',xml_declaration=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--folio',required=True)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args()
    matches=[r for r in json.loads(args.plan.read_text())['plans'] if r['folio']==args.folio]
    if len(matches)!=1: raise ValueError('Expected one exact folio plan')
    data=render(matches[0],args.source.read_bytes())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_bytes(data)
    print(json.dumps({'status':'COORDINATOR_PREVIEW_ONLY','output_sha256':hashlib.sha256(data).hexdigest(),
                      'annotation_ready':False,'independent_review':False},sort_keys=True))

if __name__=='__main__': main()
