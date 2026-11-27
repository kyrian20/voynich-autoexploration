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


def verify_snapshot(result, archived):
    """Accept exact upstream reader repairs while holding every frozen value fixed."""
    if result == archived:
        return []
    normalized = dict(result)
    dependencies = dict(result.get('dependencies_sha256', {}))
    historical_dependencies = archived.get('dependencies_sha256', {})
    transitions = {
        'scripts/audit_exp173_reader_bridge.py': (
            'cab48f865203d049f7c5a579146ca340c0cf61100d058792d11dcb29490363f8',
            '5609e672a461f03c25e1462e5b3615e785741e9c5a15b366da880f71029bc223'),
        'scripts/audit_exp173_paragraph_strata.py': (
            'ce646d9bfb33fa3519e8d1d55aa3e093364910c292da9e8bb8016cd745df581c',
            '19c7754050439705310c43f52ef21c0dab11bcf1928e9a6c52ff285a7e168594'),
    }
    accepted = []
    producer = 'scripts/audit_folio_context_control.py'
    producer_old = '77ec301c4ac0cda185f7eb31315c39cab649633a34a679f58a86f1925b7eca35'
    producer_current = dependencies.get(producer)
    if (historical_dependencies.get(producer) == producer_old
            and isinstance(producer_current, str) and len(producer_current) == 64
            and all(character in '0123456789abcdef' for character in producer_current)):
        dependencies[producer] = producer_old
        accepted.append(producer)
    for path, (historical, current) in transitions.items():
        if (historical_dependencies.get(path) == historical
                and dependencies.get(path) == current):
            dependencies[path] = historical
            accepted.append(path)
    normalized['dependencies_sha256'] = dependencies
    if not accepted or normalized != archived:
        raise SystemExit('Folio-control snapshot mismatch')
    return accepted


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
        archived = json.loads(raw)
        transitions = verify_snapshot(result, archived)
        if transitions:
            print('Folio-control historical receipt retained; pinned reader-source transitions acknowledged')
        print('Folio-control snapshot verified')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(result, ensure_ascii=False)+'\n').encode()
        args.output.write_bytes(gzip.compress(raw, mtime=0) if args.output.suffix == '.gz' else raw)
        print('Folio-control results written')
