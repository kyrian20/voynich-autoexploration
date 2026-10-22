#!/usr/bin/env python3
"""Exact concordances for a fixed potential-anchor list; no semantic assignments."""
import collections
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens

TARGETS = ('ytoail', 'keeredal', 'keerodal', 'otaim', 'dam', 'alam',
           'otaimdam', 'kydainy', 'kydain')
FILES = [('ZL3b', 'data/transcriptions/eva_zl3b.txt'),
         ('IT2a', 'data/transcriptions/eva_it2a.txt')]
PROTOCOL = 'research/decipherment/2026-10-22-anchor-review/PROTOCOL.md'


def find_targets(rows, space_policy):
    result = {target: [] for target in TARGETS}
    for row in rows:
        if row['payload'].diagnostics:
            raise ValueError(f"Unresolved payload: {row['id']}")
        words = tokens([row['payload']], uncertain_space=space_policy)
        for index, word in enumerate(words):
            if word in result:
                result[word].append({
                    'id': row['id'], 'folio': row['folio'],
                    'locus': row['locus'], 'source_line': row['source_line'],
                    'token_index_zero_based': index, 'body': row['body'],
                    'left_context': words[max(0, index-2):index],
                    'right_context': words[index+1:index+3]})
    return {
        target: {
            'occurrences': len(matches),
            'folios': sorted({m['folio'] for m in matches}),
            'locus_counts': dict(sorted(collections.Counter(
                m['locus'] for m in matches).items())),
            'matches': matches}
        for target, matches in result.items()}


def main():
    sources = []
    for label, path in FILES:
        raw, rows = read_records(ROOT / path)
        sources.append({
            'label': label, 'path': path,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'raw_records': len(rows),
            'views': {policy: find_targets(rows, policy)
                      for policy in ('split', 'join')}})
    out = {
        'audit': 'fixed_anchor_candidate_exact_concordances', 'version': 1,
        'protocol': PROTOCOL,
        'protocol_sha256': hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'targets': list(TARGETS), 'sources': sources,
        'limits': [
            'Exploratory candidate inventory, not plaintext recovery.',
            'Primary alternatives only; split/join uncertain-space views remain distinct.',
            'Exact tokens only, all loci including subdivided pages.',
            'A repeated token does not establish a shared object or meaning.',
            'An absent token does not refute a proposed plant identity.',
            'Related transcriptions are not independent samples.']}
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

