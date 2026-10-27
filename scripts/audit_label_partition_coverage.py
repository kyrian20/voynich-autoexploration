#!/usr/bin/env python3
"""Metadata-only coverage audit; no EVA token comparisons or semantic outcomes."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_visual_inventory_completeness import audit as audit_inventory_completeness
from scripts.select_visual_pilot_v2 import load_verified_frozen_manifest
INVENTORY=ROOT/'research/decipherment/2026-10-25-label-inventory/inventory.json.gz'
MANIFEST=ROOT/'research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json'
FOLIO=re.compile(r'^f(\d+)[rv][1-6]?$')

def partition_map(manifest):
    result={}
    if set(manifest['partitions'])!={'train','development','test'}:
        raise ValueError('Exactly train/development/test required')
    for name,leaves in manifest['partitions'].items():
        for leaf in leaves:
            if type(leaf) is not int or leaf<=0 or leaf in result:
                raise ValueError('Invalid or overlapping leaf partition')
            result[leaf]=name
    return result

def leaf_id(folio):
    if folio=='fRos': return None
    match=FOLIO.fullmatch(folio)
    if not match: raise ValueError('Unrecognized folio')
    return int(match[1])

def build(inventory,manifest):
    assignment=partition_map(manifest)
    sources={s['edition']:s for s in inventory['sources']}
    if len(sources)!=2 or len(sources)!=len(inventory['sources']):
        raise ValueError('Two distinct editions required')
    for s in sources.values():
        reference=manifest['corpora'].get(Path(s['path']).name)
        if not reference or reference['sha256']!=s['sha256']:
            raise ValueError('Source identity differs from partition manifest')
    by_source={e:{} for e in sources}
    strata=defaultdict(list)
    seen=set()
    for row in inventory['records']:
        edition=row['edition']
        if edition not in sources or row['source_sha256']!=sources[edition]['sha256']:
            raise ValueError('Record/source identity mismatch')
        if row['occurrence_id'] in seen or row['id'] in by_source[edition]:
            raise ValueError('Duplicate occurrence or source locus')
        seen.add(row['occurrence_id']);by_source[edition][row['id']]=row
        leaf=leaf_id(row['folio'])
        if leaf is not None and leaf not in assignment:
            raise ValueError('Numeric leaf absent from partition')
        partition=assignment[leaf] if leaf is not None else 'UNASSIGNED'
        strata[(edition,row['locus'],partition)].append((leaf,row['folio']))
    cells=[]
    for edition,locus,partition in sorted((e,t,p) for e in sources for t in {r['locus'] for r in by_source[e].values()} for p in ('train','development','test','UNASSIGNED')):
        values=strata[(edition,locus,partition)]
        leaves=Counter(leaf for leaf,folio in values if leaf is not None)
        cells.append({'edition':edition,'locus':locus,'partition':partition,
            'source_rows':len(values),'numeric_leaves':len(leaves),
            'folios':sorted({folio for leaf,folio in values}),
            'rows_per_leaf':{str(k):v for k,v in sorted(leaves.items())},
            'largest_leaf_share':max(leaves.values())/len(values) if leaves else None})
    editions=sorted(sources)
    a,b=editions
    common=set(by_source[a]) & set(by_source[b])
    mismatches=[{'id':key,'types':{a:by_source[a][key]['locus'],b:by_source[b][key]['locus']}}
        for key in sorted(common) if by_source[a][key]['locus']!=by_source[b][key]['locus']]
    unmatched=[]
    for edition,other in [(a,b),(b,a)]:
        excluded=defaultdict(list)
        for row in sources[other]['excluded_rows']:excluded[row['id']].append(row)
        for key in sorted(set(by_source[edition])-set(by_source[other])):
            unmatched.append({'edition':edition,'id':key,'locus':by_source[edition][key]['locus'],
                'other_edition':other,'counterpart_excluded_rows':excluded.get(key,[]),
                'counterpart_status':'PRESENT_OUTSIDE_SELECTION' if key in excluded else 'NOT_IN_PARSED_INVENTORY'})
    return {'status':'METADATA_COVERAGE_ONLY_NO_SEMANTIC_EVALUATION',
        'source_rows':len(seen),'union_locus_ids':len(set.union(*(set(v) for v in by_source.values()))),
        'common_locus_ids':len(common),'type_mismatches':mismatches,
        'per_source':{e:{'selected_rows':len(rows),
            'numeric_leaves':len({leaf_id(r['folio']) for r in rows.values()}-{None}),
            'unassigned_rows':sum(leaf_id(r['folio']) is None for r in rows.values())}
            for e,rows in by_source.items()},
        'strata':cells,'unmatched':unmatched,
        'limitations':['L/R subtype does not establish an independently identified object.',
            'Same locator across editions is a textual pairing, not independently verified image alignment.',
            'No semantic outcomes inspected; no power or significance calculation.',
            'Existing holdout has historical exposure; fRos remains unassigned.']}

def load_verified_coverage_inputs(inventory_bytes, manifest_bytes, root):
    """Fail closed on altered source rows or frozen leaf allocations.

    This is an operational input gate, not independent IVTFF or semantic
    validation. Preserve the archived inputs; never rebuild them here.
    """
    manifest = load_verified_frozen_manifest(manifest_bytes, root)
    inventory = json.loads(gzip.decompress(inventory_bytes))
    audit_inventory_completeness(inventory, manifest, root)
    return inventory, manifest


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    archive=INVENTORY.read_bytes();manifest=MANIFEST.read_bytes()
    inventory, frozen = load_verified_coverage_inputs(archive, manifest, ROOT)
    result=build(inventory, frozen)
    result['inputs_sha256']={'inventory_archive':hashlib.sha256(archive).hexdigest(),
                            'partition_manifest':hashlib.sha256(manifest).hexdigest()}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('source_rows','union_locus_ids','common_locus_ids','per_source')},sort_keys=True))
if __name__=='__main__':main()
