#!/usr/bin/env python3
"""Inventory explicit L/R loci; derived projections never resolve readings."""
import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ivtff_lossless import lex
from scripts.ivtff_rows import tokens_rows

SOURCES = [('ZL3b', 'data/transcriptions/eva_zl3b.txt'),
           ('IT2a', 'data/transcriptions/eva_it2a.txt')]
ROW = re.compile(r'^<([^<>.,\s]+)\.([^<>,\s]+),([^<>]+)>\s*(.*)$')
HEADER = re.compile(r'^<([^<>.,\s]+)>\s*(.*)$')
def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def extract(text, edition, source_hash, images):
    records, excluded, unparsed = [], [], []
    page, metadata = None, ''
    seen = set()
    for number, line in enumerate(text.splitlines(), 1):
        header = HEADER.match(line)
        if header:
            page, metadata = header.groups()
            continue
        match = ROW.match(line)
        if not match:
            if line.strip() and not line.lstrip().startswith('#'):
                unparsed.append({'source_line': number, 'raw_line': line})
            continue
        folio, locus_id, code, body = match.groups()
        key = f'{folio}.{locus_id}'
        locus = code.split(';')[0]
        if len(locus) < 2:
            unparsed.append({'source_line': number, 'raw_line': line})
            continue
        kind = locus[1:]
        if not kind.startswith(('L', 'R')):
            excluded.append({'source_line': number, 'id': key, 'locus': kind,
                             'reason': 'outside_explicit_L_or_R_selection'})
            continue
        reasons = ['no_independent_visual_referent_annotation']
        if locus[0] not in '@*+=~&':
            reasons.append('special_record_marker_requires_adjudication')
        if folio != page:
            reasons.append('page_header_mismatch')
        if key in seen:
            reasons.append('duplicate_locus_id_in_source')
        seen.add(key)
        payload = lex(body)
        views = {}
        for space, alternative, ligature in product(
                ('split', 'join'), ('primary', 'exclude_word'), ('expand', 'opaque')):
            name = f'{space}/{alternative}/{ligature}'
            try:
                words = tokens_rows([payload], uncertain_space=space,
                                    alternatives=alternative, ligatures=ligature)
                views[name] = {'tokens': words, 'error': None}
            except ValueError as exc:
                views[name] = {'tokens': None, 'error': str(exc)}
        if any(v['error'] for v in views.values()):
            reasons.append('unresolved_projection_requires_adjudication')
        records.append({'occurrence_id': f'{edition}:{number}', 'edition': edition,
            'source_sha256': source_hash, 'source_line': number,
            'raw_line': line, 'raw_line_sha256': digest(line.encode()),
            'folio': folio, 'locus_id': locus_id, 'id': key, 'locus': kind,
            'header_metadata': metadata, 'raw_body': body,
            'lexer_diagnostics': payload.diagnostics, 'views': views,
            'image_source_archived': images.get(folio),
            'visual_category': None, 'external_referent': None,
            'independent_annotation_source': None,
            'eligible_for_semantic_evaluation': False, 'exclusion_reasons': reasons})
    return records, excluded, unparsed

def build(root=ROOT):
    image_path = root / 'research/decipherment/2026-10-22-anchor-review/image-sources.json'
    image_bytes = image_path.read_bytes()
    images = {x['folio']: x for x in json.loads(image_bytes)['images']}
    result = {'status': 'INVENTORY_ONLY_SEMANTIC_EVALUATION_BLOCKED',
        'selection': 'All parsed loci explicitly starting L or R; includes nonnumeric locus IDs. No EVA or image-category filter.',
        'unit': 'Physical source row; tokens are indexed within each named derived view. Continuations are retained but not joined across records.',
        'limitations': ['Existing lexer is not an independently validated full IVTFF parser.',
            'Missing source IDs are transcription coverage differences, not proof of missing manuscript text.',
            'Archived image provenance is not a newly inspected image or an independent referent identification.',
            'Primary readings are editorial projections; alternatives remain in raw_body.',
            'No semantic training, holdout evaluation, or translation performed.'],
        'image_manifest_sha256': digest(image_bytes), 'sources': [], 'records': []}
    ids = {}
    for edition, path in SOURCES:
        raw = (root / path).read_bytes()
        records, excluded, unparsed = extract(raw.decode('utf-8-sig'), edition, digest(raw), images)
        result['sources'].append({'edition': edition, 'path': path, 'sha256': digest(raw),
            'selected_rows': len(records), 'excluded_rows': excluded, 'unparsed_lines': unparsed,
            'locus_counts': dict(sorted(Counter(x['locus'] for x in records).items()))})
        result['records'].extend(records)
        ids[edition] = {x['id'] for x in records}
    union = set.union(*ids.values())
    result['cross_source_coverage'] = {e: {'missing_ids': sorted(union - s)} for e, s in ids.items()}
    result['summary'] = {'source_rows': len(result['records']), 'union_locus_ids': len(union),
        'semantic_eligible_rows': 0,
        'rows_with_projection_errors': sum(any(v['error'] for v in r['views'].values()) for r in result['records']),
        'unparsed_lines': sum(len(s['unparsed_lines']) for s in result['sources'])}
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = build()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['summary'], sort_keys=True))
if __name__ == '__main__':
    main()
