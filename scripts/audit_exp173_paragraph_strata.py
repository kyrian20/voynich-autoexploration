#!/usr/bin/env python3
"""Explicit paragraph-marker strata; absence is not an inferred paragraph state."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_exp173_reader_bridge as bridge
from audit_token_policy_sensitivity import read_records
from ivtff_lossless import tokens

STRATA = ('P0/marked_end', 'P0/no_marked_end', 'other_P/marked_end', 'other_P/no_marked_end')


def marked_end(payload):
    def nested(spans):
        for span in spans:
            if span.kind == 'paragraph_end':
                return True
            if nested(span.children) or any(nested(option) for option in span.options):
                return True
        return False
    if payload.diagnostics:
        raise ValueError('Unresolved marker payload')
    if any(nested(span.children) or any(nested(option) for option in span.options) for span in payload.spans):
        raise ValueError('Nested paragraph marker requires adjudication')
    return any(span.kind == 'paragraph_end' for span in payload.spans)


def stratum(row):
    return ('P0' if row['locus'] == 'P0' else 'other_P') + ('/marked_end' if marked_end(row['payload']) else '/no_marked_end')


def metric(lines):
    m = bridge.metrics(lines)
    target = m['am_final']
    return {'lines': m['lines'], 'tokens': m['tokens'], 'singleton_lines': m['singleton_lines'],
            'am_final': target,
            'am_final_fraction_of_lines': target['observed'] / m['lines'] if target else None,
            'am_token_fraction': target['feature_tokens'] / m['tokens'] if target else None}


def source(label, filename, previous):
    raw, records = read_records(ROOT / 'data/transcriptions' / filename)
    selected = [r for r in records if r['currier'] == 'B' and r['locus'].startswith('P')
                and bridge.legacy.FOLIO_NUMBER.match(r['folio'])]
    views = {'historical': {r['id']: bridge.historical_tokens(r['body']) for r in selected}}
    for name, policy in bridge.POLICIES.items():
        views[name] = {r['id']: tokens([r['payload']], **policy) for r in selected}
    common = [r for r in selected if all(view[r['id']] for view in views.values())]
    ids = [r['id'] for r in common]
    id_hash = hashlib.sha256(('\n'.join(ids) + '\n').encode()).hexdigest()
    if id_hash != previous['common_id_sha256'] or len(ids) != previous['common_nonempty_records']:
        raise ValueError('Common population drift')
    groups = {key: [r for r in common if stratum(r) == key] for key in STRATA}
    result = {'transcription': label, 'source_sha256': hashlib.sha256(raw).hexdigest(),
              'common_id_sha256': id_hash, 'common_lines': len(common),
              'exact_locus_counts': dict(sorted(Counter(r['locus'] for r in common).items())),
              'strata': {}, 'profiles': {}}
    for key, group in groups.items():
        result['strata'][key] = {'lines': len(group), 'ids': [r['id'] for r in group],
                                'exact_locus_counts': dict(sorted(Counter(r['locus'] for r in group).items()))}
    for name, view in views.items():
        full = bridge.metrics([view[x] for x in ids])
        if full != previous['profiles'][name]['common_eligible']:
            raise ValueError(f'Previous metrics drift: {label}/{name}')
        strata = {key: metric([view[r['id']] for r in group]) for key, group in groups.items()}
        if sum(x['lines'] for x in strata.values()) != len(ids):
            raise ValueError('Strata do not partition common lines')
        if sum(x['am_final']['observed'] if x['am_final'] else 0 for x in strata.values()) != full['am_final']['observed']:
            raise ValueError('Observed counts do not reconstruct')
        if abs(sum(x['am_final']['expected_within_line'] if x['am_final'] else 0 for x in strata.values()) - full['am_final']['expected_within_line']) > 1e-10:
            raise ValueError('Expected counts do not reconstruct')
        result['profiles'][name] = strata
    if label == 'ZL3b':
        group = groups['P0/no_marked_end']
        numbers = sorted({int(bridge.legacy.FOLIO_NUMBER.match(r['folio'])[1]) for r in group})
        result['leave_one_numeric_folio_out_P0_no_marked_end'] = [
            {'removed_numeric_folio': number, 'ratios': {
                name: metric([view[r['id']] for r in group
                              if int(bridge.legacy.FOLIO_NUMBER.match(r['folio'])[1]) != number])['am_final']['ratio_within_line']
                for name, view in views.items()}}
            for number in numbers]
    return result


def run():
    prior_path = ROOT / 'research/maintenance/2026-10-23-exp173-reader-bridge/results.json'
    prior = json.loads(prior_path.read_text())
    previous = {f['transcription']: f for f in prior['files']}
    dependencies = ['scripts/audit_exp173_reader_bridge.py', 'scripts/ivtff_lossless.py',
                    'scripts/audit_token_policy_sensitivity.py', str(prior_path.relative_to(ROOT))]
    return {'status': 'EXPLORATORY_DESCRIPTIVE_STRATA', 'base_commit': '29b86941250e75be46eb62ac9d6efb5032563da0',
            'source_bridge_snapshot_sha256': hashlib.sha256(prior_path.read_bytes()).hexdigest(),
            'dependencies_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
            'files': [source(label, filename, previous[label]) for label, filename in bridge.SOURCES],
            'limits': ['No marked end is not proof of paragraph interior.',
                       'Same related transcriptions and previously observed features.',
                       'No p-values, confidence intervals, new language or semantic inference.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise SystemExit('Paragraph strata snapshot mismatch')
        print('Paragraph strata snapshot verified')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
