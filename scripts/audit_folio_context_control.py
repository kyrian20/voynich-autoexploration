#!/usr/bin/env python3
"""Support of a different null: folio inventory, fixed line templates."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_exp173_reader_bridge as bridge
import audit_exp173_paragraph_strata as strata
from audit_token_policy_sensitivity import read_records
from ivtff_lossless import tokens


def group(identifier):
    match = re.fullmatch(r'f([0-9]+)[rv][0-9]*\.[0-9]+', identifier)
    if not match:
        raise ValueError('Unresolved physical folio: '+identifier)
    return int(match[1])


def signature(word):
    if not word:
        raise ValueError('Empty token')
    return word[0], word[-1], len(word)


def analyze(rows):
    if not rows or len({identifier for identifier, _ in rows}) != len(rows):
        raise ValueError('Empty population or duplicate IDs')
    pools = defaultdict(Counter)
    for identifier, words in rows:
        number = group(identifier)
        if not words or any(not w for w in words):
            raise ValueError('Empty line/token')
        for word in words[1:-1]:
            pools[number, signature(word)][word] += 1
    result = {}
    for category in ('am_final', 'other_final'):
        selected = [(identifier, words) for identifier, words in rows
                    if words[-1].endswith('am') == (category == 'am_final')]
        details = []
        expectation = Fraction()
        for identifier, words in selected:
            probability = Fraction()
            if len(words) >= 3:
                pool = pools[group(identifier), signature(words[-2])]
                probability = Fraction(sum(pool.values()) - pool[words[-2]], sum(pool.values()))
            expectation += probability
            if probability:
                details.append({'id': identifier, 'physical_folio': group(identifier),
                                'change_probability_exact': str(probability)})
        result[category] = {'lines': len(selected), 'variable_lines': len(details),
                            'variable_physical_folios': sorted({d['physical_folio'] for d in details}),
                            'expected_changed_predecessors_exact': str(expectation),
                            'expected_changed_predecessors': float(expectation), 'variable_rows': details}
    return result


def run():
    snapshot = ROOT / 'research/maintenance/2026-10-23-paragraph-strata/results.json'
    previous = json.loads(snapshot.read_text())
    files = []
    for (label, filename), old in zip(bridge.SOURCES, previous['files']):
        raw, records = read_records(ROOT / 'data/transcriptions' / filename)
        if old['transcription'] != label or hashlib.sha256(raw).hexdigest() != old['source_sha256']:
            raise ValueError('Source drift')
        ids = old['strata']['P0/no_marked_end']['ids']
        by_id = {r['id']: r for r in records}
        selected = [by_id[x] for x in ids]
        if any(r['currier'] != 'B' or strata.stratum(r) != 'P0/no_marked_end' for r in selected):
            raise ValueError('Population drift')
        profiles = {}
        for name, policy in bridge.POLICIES.items():
            rows = [(r['id'], tokens([r['payload']], **policy)) for r in selected]
            if strata.metric([words for _, words in rows]) != old['profiles'][name]['P0/no_marked_end']:
                raise ValueError('Metric drift')
            profiles[name] = analyze(rows)
        files.append({'transcription': label, 'source_sha256': old['source_sha256'],
                      'selected_id_sha256': hashlib.sha256(('\n'.join(ids)+'\n').encode()).hexdigest(),
                      'profiles': profiles})
    paths = ['scripts/audit_folio_context_control.py', 'scripts/audit_exp173_reader_bridge.py',
             'scripts/audit_exp173_paragraph_strata.py', 'scripts/audit_token_policy_sensitivity.py',
             'scripts/ivtff_lossless.py', str(snapshot.relative_to(ROOT)),
             'research/maintenance/2026-10-23-folio-context-control/PROTOCOL.md']
    return {'status': 'EXPLORATORY_ALTERNATIVE_NULL_SUPPORT',
            'preserves_line_inventory': False, 'preserves_physical_folio_inventory': True,
            'dependencies_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
            'files': files}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    if bool(args.output) == bool(args.check):
        parser.error('Choose --output or --check')
    result = run()
    if args.check:
        raw = args.check.read_bytes()
        if args.check.suffix == '.gz':
            raw = gzip.decompress(raw)
        if result != json.loads(raw):
            raise SystemExit('Folio-control snapshot mismatch')
        print('Folio-control snapshot verified')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(result, ensure_ascii=False)+'\n').encode()
        args.output.write_bytes(gzip.compress(raw, mtime=0) if args.output.suffix == '.gz' else raw)
        print('Folio-control results written')
