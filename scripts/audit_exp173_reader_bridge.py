#!/usr/bin/env python3
"""Paired descriptive F3/F6 reader bridge; no p-values or new EXP."""
from __future__ import annotations
import argparse
from collections import defaultdict
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import audit_exp173_currier_crosswalk as legacy
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens
from scripts.audit_exp173_line_null import expectation

SOURCES = [('ZL3b', 'eva_zl3b.txt'), ('ZL3a', 'zl3a.txt'), ('IT2a', 'eva_it2a.txt')]
POLICIES = {f'{space}/{alt}/{lig}': dict(uncertain_space=space, alternatives=alt, ligatures=lig)
            for space, alt, lig in itertools.product(('split', 'join'), ('primary', 'exclude_word'), ('expand', 'opaque'))}
DEFAULT = 'split/primary/expand'


def historical_tokens(body):
    return [w for w in body.split('.') if w and legacy.WORD_START.match(w) and not w.startswith('<')]


def metrics(lines):
    nonempty = [line for line in lines if line]
    return {'lines': len(nonempty), 'tokens': sum(map(len, nonempty)),
            'singleton_lines': sum(len(line) == 1 for line in nonempty),
            'am_final': expectation(nonempty, lambda w: w.endswith('am'), -1) if nonempty else None,
            'y_initial': expectation(nonempty, lambda w: w.lower().startswith('y'), 0) if nonempty else None}


def paired_leave_one_out(rows, old, new):
    groups = defaultdict(list)
    for row in rows:
        groups[row['number']].append(row['id'])
    if len(groups) < 2:
        raise ValueError('At least two numeric folios required')
    output = []
    for number in sorted(groups):
        ids = [row['id'] for row in rows if row['number'] != number]
        a, b = metrics([old[x] for x in ids]), metrics([new[x] for x in ids])
        effects = {}
        for key in ('am_final', 'y_initial'):
            x, y = a[key]['ratio_within_line'], b[key]['ratio_within_line']
            effects[key] = {'historical': x, 'candidate': y,
                            'candidate_minus_historical': y - x if x is not None and y is not None else None}
        output.append({'removed_numeric_folio': number, 'removed_lines': len(groups[number]), 'effects': effects})
    return output


def audit_source(label, filename):
    path = ROOT / 'data/transcriptions' / filename
    raw, records = read_records(path)
    p_records = [r for r in records if r['locus'].startswith('P') and legacy.FOLIO_NUMBER.match(r['folio'])]
    # Verify exact reconstruction before using the common record IDs.
    native_rows, _, _ = legacy.read_legacy_population(raw.decode('utf-8-sig'))
    reconstructed = [{'page': r['folio'], 'number': int(legacy.FOLIO_NUMBER.match(r['folio'])[1]),
                      'tokens': historical_tokens(r['body'])} for r in p_records if historical_tokens(r['body'])]
    if reconstructed != native_rows:
        raise ValueError(f'Historical population reconstruction mismatch: {label}')
    selected = [{**r, 'number': int(legacy.FOLIO_NUMBER.match(r['folio'])[1])}
                for r in p_records if r['currier'] == 'B']
    views = {'historical': {r['id']: historical_tokens(r['body']) for r in selected}}
    for name, policy in POLICIES.items():
        views[name] = {r['id']: tokens([r['payload']], **policy) for r in selected}
    common = [r for r in selected if all(v[r['id']] for v in views.values())]
    ids = [r['id'] for r in common]
    profiles = {}
    for name, view in views.items():
        profiles[name] = {'own_eligible': metrics(list(view.values())),
                          'common_eligible': metrics([view[x] for x in ids]),
                          'empty_ids': [r['id'] for r in selected if not view[r['id']]]}
    changes = []
    for r in selected:
        old = views['historical'][r['id']]
        changed = {name: v[r['id']] for name, v in views.items() if v[r['id']] != old}
        if changed:
            changes.append({'id': r['id'], 'source_line': r['source_line'], 'page': r['folio'],
                            'raw_body': r['body'], 'historical': old, 'different_views': changed})
    endpoint_changes = []
    for r in selected:
        old, new = views['historical'][r['id']], views[DEFAULT][r['id']]
        signature = lambda words: [bool(words and words[-1].endswith('am')),
                                   bool(words and words[0].lower().startswith('y'))]
        if signature(old) != signature(new):
            endpoint_changes.append({'id': r['id'], 'old_signature_am_y': signature(old),
                                     'new_signature_am_y': signature(new),
                                     'old_first': old[0] if old else None, 'new_first': new[0] if new else None,
                                     'old_last': old[-1] if old else None, 'new_last': new[-1] if new else None})
    result = {'transcription': label, 'source': str(path.relative_to(ROOT)),
              'source_sha256': hashlib.sha256(raw).hexdigest(),
              'historical_population_reconstructed': True,
              'raw_B_P_records': len(selected), 'common_nonempty_records': len(ids),
              'common_id_sha256': hashlib.sha256(('\n'.join(ids) + '\n').encode()).hexdigest(),
              'profiles': profiles, 'changed_rows': len(changes),
              'default_endpoint_changes': endpoint_changes}
    if label == 'ZL3b':
        prior = json.loads((ROOT / 'research/maintenance/2026-10-23-exp173-line-null/results.json').read_text())
        own = profiles['historical']['own_eligible']
        if any(own[key] != prior[key] for key in ('lines', 'tokens', 'singleton_lines', 'am_final', 'y_initial')):
            raise ValueError('Previous line-null snapshot no longer reproduced')
        result['leave_one_numeric_folio_out'] = paired_leave_one_out(common, views['historical'], views[DEFAULT])
    return result, changes


def run():
    expected = json.loads((ROOT / 'research/maintenance/2026-10-23-exp173-currier-crosswalk/results.json').read_text())
    if legacy.run() != expected:
        raise ValueError('Prior crosswalk snapshot mismatch')
    files, changes = [], {}
    for label, filename in SOURCES:
        result, detail = audit_source(label, filename)
        files.append(result)
        changes[label] = detail
    dependencies = ['scripts/audit_exp173_currier_crosswalk.py', 'scripts/audit_exp173_line_null.py',
                    'scripts/audit_token_policy_sensitivity.py', 'scripts/ivtff_lossless.py',
                    'scripts/audit_research_readiness.py', 'scripts/audit_ivtff_metadata.py']
    return {'audit': 'EXP173_descriptive_reader_bridge', 'status': 'EXPLORATORY_SENSITIVITY',
            'base_commit': '29677e387d9c44983a28d61baad2f14e55a42c8e',
            'policies': POLICIES, 'default_candidate': DEFAULT,
            'dependencies_sha256': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in dependencies},
            'files': files,
            'limits': ['Related transcriptions are not independent samples.',
                       'Candidate lexical view is not full IVTFF certification.',
                       'Literal features on opaque tokens depend on projection policy.',
                       'No p-values, confidence intervals, model rejection or semantic inference.']}, changes


OVERLAY_PATH = ROOT / 'research/maintenance/2026-10-25-ivtff-multiline-dependency-overlay.json'


def verify_snapshot(name, current, archived, overlay):
    """Compare every archived value, allowing one pinned dependency hash only.

    A lexer implementation change must not be mislabeled as an exact historical
    code replay. Scientific outputs and changed-row details must still match.
    """
    if current == archived:
        return 'exact'
    if name != 'results.json':
        raise ValueError(f'Snapshot mismatch: {name}')
    if overlay.get('schema_version') != 1 or overlay.get('status') != 'APPROVED_FOR_EXACT_SNAPSHOT_COMPARISON_ONLY':
        raise ValueError('Invalid dependency provenance overlay')
    dependency = overlay['dependency']
    if dependency != 'scripts/ivtff_lossless.py':
        raise ValueError('Unapproved dependency override')
    if (archived.get('dependencies_sha256', {}).get(dependency) != overlay['archived_sha256'] or
            current.get('dependencies_sha256', {}).get(dependency) != overlay['current_sha256'] or
            overlay['archived_sha256'] == overlay['current_sha256']):
        raise ValueError('Dependency hash differs from approved historical/current pair')
    adjusted = dict(current)
    adjusted['dependencies_sha256'] = dict(current['dependencies_sha256'])
    adjusted['dependencies_sha256'][dependency] = overlay['archived_sha256']
    if adjusted != archived:
        raise ValueError(f'Snapshot mismatch outside pinned dependency: {name}')
    return 'scientific_fields_exact_with_pinned_dependency_change'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-directory', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    if bool(args.output_directory) == bool(args.check):
        parser.error('Choose exactly one of --output-directory or --check')
    result, changes = run()
    payloads = {'results.json': result, 'changed-rows.json.gz': changes}
    if args.check:
        outcomes = {}
        for name, value in payloads.items():
            raw = (args.check / name).read_bytes()
            if name.endswith('.gz'):
                raw = gzip.decompress(raw)
            archived = json.loads(raw)
            overlay = json.loads(OVERLAY_PATH.read_text(encoding='utf-8')) if value != archived else {}
            try:
                outcomes[name] = verify_snapshot(name, value, archived, overlay)
            except ValueError as exc:
                raise SystemExit(str(exc)) from exc
        print('Reader bridge: archived scientific fields and changed rows verified; '
              + json.dumps(outcomes, sort_keys=True))
    else:
        args.output_directory.mkdir(parents=True, exist_ok=True)
        for name, value in payloads.items():
            raw = (json.dumps(value, indent=2 if not name.endswith('.gz') else None, ensure_ascii=False) + '\n').encode()
            (args.output_directory / name).write_bytes(gzip.compress(raw, mtime=0) if name.endswith('.gz') else raw)
        print('Reader bridge: results and changed rows written')


if __name__ == '__main__':
    main()
