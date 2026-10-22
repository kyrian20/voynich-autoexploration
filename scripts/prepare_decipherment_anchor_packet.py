#!/usr/bin/env python3
"""Prepare all Lp-marked loci as potential anchors; no plant/name assignments."""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens

FILES = [('ZL3b', 'data/transcriptions/eva_zl3b.txt'),
         ('IT2a', 'data/transcriptions/eva_it2a.txt')]


def main():
    records = {}
    sources = []
    for label, relative in FILES:
        raw, rows = read_records(ROOT / relative)
        sources.append({'label': label, 'path': relative,
                        'sha256': hashlib.sha256(raw).hexdigest()})
        for row in rows:
            if row['locus'] != 'Lp':
                continue
            item = records.setdefault(row['id'], {
                'id': row['id'], 'folio': row['folio'], 'locus': 'Lp',
                'transcriptions': {}, 'verified_plaintext': None,
                'proposed_reading': None, 'verified_object_identity': None,
                'status': 'TEXT_CANDIDATE_REQUIRES_IMAGE_AND_EXTERNAL_ANCHOR'})
            item['transcriptions'][label] = {
                'source_line': row['source_line'], 'raw_body': row['body'],
                'primary_split_view': tokens([row['payload']]),
                'primary_join_uncertain_spaces_view':
                    tokens([row['payload']], uncertain_space='join')}
    output = {
        'packet': 'potential_decipherment_anchors_Lp', 'version': 1,
        'selection': 'All loci explicitly marked Lp in either supplied transcription; no ranking by desired meaning.',
        'sources': sources, 'candidates': list(records.values()),
        'warnings': [
            'Lp metadata is a locator, not proof of a plant name or its identity.',
            'A missing Lp entry in one transcription is not proof that the manuscript lacks text there.',
            'Preserve alternatives and uncertain spaces; primary projection is not a resolved reading.',
            'No image inspection or external botanical/name verification performed by this generator.',
            'No plaintext, phonetic value or decipherment is established.']}
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

