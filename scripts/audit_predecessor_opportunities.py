#!/usr/bin/env python3
"""Exact exchange opportunities; no association test or token deletion."""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_exp173_reader_bridge as bridge
import audit_exp173_paragraph_strata as strata
from audit_token_policy_sensitivity import read_records
from ivtff_lossless import tokens

CONTROLS = ('interior', 'length', 'edges', 'edges_length')


def key(word, control):
    if not word:
        raise ValueError('Empty token')
    if control == 'interior':
        return ()
    if control == 'length':
        return (len(word),)
    if control == 'edges':
        return (word[0], word[-1])
    if control == 'edges_length':
        return (word[0], word[-1], len(word))
    raise ValueError('Unknown control')


def opportunity(words, control):
    if not words or any(not w for w in words):
        raise ValueError('Nonempty line and tokens required')
    if control not in CONTROLS:
        raise ValueError('Unknown control')
    if len(words) < 3:
        return {'candidates': {}, 'variable': False, 'change_probability_exact': '0'}
    observed = words[-2]
    candidates = Counter(w for w in words[1:-1] if key(w, control) == key(observed, control))
    probability = Fraction(sum(candidates.values()) - candidates[observed], sum(candidates.values()))
    return {'candidates': dict(sorted(candidates.items())), 'variable': len(candidates) > 1,
            'change_probability_exact': str(probability)}


def summarize(rows, control):
    result = {}
    for category in ('am_final', 'other_final'):
        selected = [(identifier, words) for identifier, words in rows
                    if words[-1].endswith('am') == (category == 'am_final')]
        details = [(identifier, opportunity(words, control)) for identifier, words in selected]
        expected = sum((Fraction(d['change_probability_exact']) for _, d in details), Fraction())
        result[category] = {'lines': len(details), 'variable_lines': sum(d['variable'] for _, d in details),
                            'expected_changed_predecessors_exact': str(expected),
                            'expected_changed_predecessors': float(expected)}
        if control == 'edges_length':
            result[category]['variable_rows'] = [{'id': identifier, **detail} for identifier, detail in details if detail['variable']]
    return result


def run():
    snapshot = ROOT / 'research/maintenance/2026-10-23-paragraph-strata/results.json'
    prior = json.loads(snapshot.read_text())
    files = []
    for (label, filename), previous in zip(bridge.SOURCES, prior['files']):
        raw, records = read_records(ROOT / 'data/transcriptions' / filename)
        if previous['transcription'] != label or hashlib.sha256(raw).hexdigest() != previous['source_sha256']:
            raise ValueError('Source drift')
        ids = previous['strata']['P0/no_marked_end']['ids']
        by_id = {r['id']: r for r in records}
        selected = [by_id[x] for x in ids]
        if any(r['currier'] != 'B' or strata.stratum(r) != 'P0/no_marked_end' for r in selected):
            raise ValueError('Population drift')
        profiles = {}
        for name, policy in bridge.POLICIES.items():
            rows = [(r['id'], tokens([r['payload']], **policy)) for r in selected]
            metric = strata.metric([words for _, words in rows])
            if metric != previous['profiles'][name]['P0/no_marked_end']:
                raise ValueError('Previous metrics drift')
            profiles[name] = {control: summarize(rows, control) for control in CONTROLS}
        files.append({'transcription': label, 'source_sha256': previous['source_sha256'],
                      'selected_id_sha256': hashlib.sha256(('\n'.join(ids)+'\n').encode()).hexdigest(),
                      'profiles': profiles})
    paths = ['scripts/audit_predecessor_opportunities.py', 'scripts/audit_exp173_reader_bridge.py',
             'scripts/audit_exp173_paragraph_strata.py', 'scripts/audit_token_policy_sensitivity.py',
             'scripts/ivtff_lossless.py', str(snapshot.relative_to(ROOT)),
             'research/maintenance/2026-10-23-predecessor-opportunities/PROTOCOL.md']
    return {'status': 'EXPLORATORY_EXCHANGE_SUPPORT_DIAGNOSTIC',
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
            raise SystemExit('Opportunity snapshot mismatch')
        print('Predecessor opportunity snapshot verified')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(result, ensure_ascii=False)+'\n').encode()
        args.output.write_bytes(gzip.compress(raw, mtime=0) if args.output.suffix == '.gz' else raw)
        print('Predecessor opportunity results written')
