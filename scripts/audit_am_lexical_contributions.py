#!/usr/bin/env python3
"""Exact lexical decomposition, preserving every line and token."""
from collections import Counter, defaultdict
from fractions import Fraction
import argparse
import hashlib
import gzip
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import audit_exp173_paragraph_strata as strata
import audit_exp173_reader_bridge as bridge
from audit_token_policy_sensitivity import read_records
from ivtff_lossless import tokens


def decompose(lines):
    if not lines or any(not line for line in lines):
        raise ValueError('Nonempty population and lines required')
    observed = Counter()
    expected = defaultdict(Fraction)
    counts = Counter()
    for line in lines:
        for word, count in Counter(line).items():
            if word.endswith('am'):
                counts[word] += count
                expected[word] += Fraction(count, len(line))
        if line[-1].endswith('am'):
            observed[line[-1]] += 1
    total_o, total_e = sum(observed.values()), sum(expected.values(), Fraction())
    rows = []
    for word in sorted(expected):
        o, e = observed[word], expected[word]
        remainder = total_e - e
        rows.append({'word': word, 'tokens': counts[word], 'observed': o,
                     'expected_exact': str(e), 'expected': float(e),
                     'excess_exact': str(Fraction(o) - e),
                     'remaining_observed': total_o - o,
                     'remaining_expected_exact': str(remainder),
                     'remaining_ratio': float(Fraction(total_o-o)/remainder) if remainder else None})
    return {'lines': len(lines), 'tokens': sum(map(len, lines)),
            'observed': total_o, 'expected_exact': str(total_e),
            'types': rows,
            'all_single_type_feature_exclusions_above_one': bool(rows) and all(
                Fraction(r['remaining_expected_exact']) > 0 and
                r['remaining_observed'] > Fraction(r['remaining_expected_exact']) for r in rows)}


def run():
    snapshot_path = ROOT / 'research/maintenance/2026-10-23-paragraph-strata/results.json'
    prior = json.loads(snapshot_path.read_text())
    output = []
    for (label, filename), old in zip(bridge.SOURCES, prior['files']):
        if old['transcription'] != label:
            raise ValueError('Source ordering mismatch')
        raw, records = read_records(ROOT / 'data/transcriptions' / filename)
        if hashlib.sha256(raw).hexdigest() != old['source_sha256']:
            raise ValueError('Source drift')
        ids = old['strata']['P0/no_marked_end']['ids']
        by_id = {r['id']: r for r in records}
        selected = [by_id[x] for x in ids]
        if any(r['currier'] != 'B' or strata.stratum(r) != 'P0/no_marked_end' for r in selected):
            raise ValueError('Population drift')
        profiles = {}
        for name, policy in bridge.POLICIES.items():
            lines = [tokens([r['payload']], **policy) for r in selected]
            result = decompose(lines)
            target = old['profiles'][name]['P0/no_marked_end']['am_final']
            if (result['observed'] != target['observed'] or
                result['expected_exact'] != target['expected_within_line_fraction']):
                raise ValueError('Additive reconstruction mismatch')
            profiles[name] = result
        output.append({'transcription': label, 'source_sha256': old['source_sha256'],
                       'selected_id_sha256': hashlib.sha256(('\n'.join(ids)+'\n').encode()).hexdigest(),
                       'profiles': profiles})
    dependencies = ['scripts/audit_am_lexical_contributions.py',
                    'scripts/audit_exp173_paragraph_strata.py', 'scripts/audit_exp173_reader_bridge.py',
                    'scripts/audit_token_policy_sensitivity.py', 'scripts/ivtff_lossless.py',
                    str(snapshot_path.relative_to(ROOT))]
    return {'status': 'EXPLORATORY_DESCRIPTIVE_DECOMPOSITION',
            'dependencies_sha256': {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in dependencies},
            'files': output}


def verify_snapshot(result, archived):
    """Accept only the two pinned reader-source transitions; preserve all frozen values."""
    if result == archived:
        return []
    normalized = dict(result)
    dependencies = dict(result.get('dependencies_sha256', {}))
    historical_dependencies = archived.get('dependencies_sha256', {})
    transitions = {
        'scripts/audit_exp173_paragraph_strata.py': (
            'ce646d9bfb33fa3519e8d1d55aa3e093364910c292da9e8bb8016cd745df581c',
            '19c7754050439705310c43f52ef21c0dab11bcf1928e9a6c52ff285a7e168594'),
        'scripts/audit_exp173_reader_bridge.py': (
            'cab48f865203d049f7c5a579146ca340c0cf61100d058792d11dcb29490363f8',
            '5609e672a461f03c25e1462e5b3615e785741e9c5a15b366da880f71029bc223'),
    }
    accepted = []
    for path, (historical, current) in transitions.items():
        if (historical_dependencies.get(path) == historical
                and dependencies.get(path) == current):
            dependencies[path] = historical
            accepted.append(path)
    normalized['dependencies_sha256'] = dependencies
    if not accepted or normalized != archived:
        raise SystemExit('Lexical snapshot mismatch')
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
            print('Lexical historical receipt retained; pinned reader-source transitions acknowledged')
        print('Lexical decomposition snapshot verified')
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(result, ensure_ascii=False)+'\n').encode()
        args.output.write_bytes(gzip.compress(raw, mtime=0) if args.output.suffix == '.gz' else raw)
        print('Lexical decomposition written')
