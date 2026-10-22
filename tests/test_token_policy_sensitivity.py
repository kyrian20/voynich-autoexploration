#!/usr/bin/env python3
"""Endpoint and interaction tests for the descriptive sensitivity audit."""
from pathlib import Path
import sys
import hashlib
import itertools

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ivtff_lossless import lex, tokens
from scripts.audit_research_readiness import old_tokens
from scripts.audit_token_policy_sensitivity import FULL, FACTORS, project, shapley, empty_metric, update, finish
from scripts.audit_exp601_paired_reader_bootstrap import paired_bootstrap
from scripts.audit_exp607_reader_sensitivity import score_profiles
from scripts.check_audit_snapshot import compare


def main():
    fixtures = ['dai{in}.or', 'qo[ke:te]dy', '@140;.daiin', 'cho?daiin',
                'da ii n.or', 'dai<!note>in', "dai'in.or", 'dai[{in}:or].daiin',
                '<%>daiin.or<$>', 'or<->daiin', 'daiin[:y]']
    for raw in fixtures:
        payload = lex(raw)
        assert project(payload, 0) == old_tokens(raw), raw
        assert project(payload, FULL) == tokens([payload]), raw
    assert project(lex('cho?daiin'), 0) == ['cho', 'daiin']
    assert project(lex('cho?daiin'), 8) == ['cho?daiin']
    assert project(lex('dai<!note>in'), 32) == ['daiin']
    assert project(lex('or,y'), FULL, join_commas=True) == ['ory']
    payload = lex('dai[{in}:or].daiin')
    values = [project(payload, mask).count('daiin') for mask in range(FULL + 1)]
    contribution = shapley(values)
    assert abs(contribution['ligatures'] - .5) < 1e-12
    assert abs(contribution['alternatives'] - .5) < 1e-12
    for factor in FACTORS[2:]:
        assert abs(contribution[factor]) < 1e-12
    metric = empty_metric()
    update(metric, ['daiin', 'or', 'daiin'])
    update(metric, ['or', 'daiin'])
    assert metric['target'] == 3 and metric['initial'] == 1
    assert abs(finish(metric)['expected_initial'] - (2 / 3 + 1 / 2)) < 1e-12
    # Independent enumeration of the tiny conditional null, including duplicates.
    permutations = list(itertools.product(
        itertools.permutations(['daiin', 'or', 'daiin']),
        itertools.permutations(['or', 'daiin'])))
    expected = sum((a[0] == 'daiin') + (b[0] == 'daiin') for a, b in permutations) / len(permutations)
    assert abs(metric['expected_initial'] - expected) < 1e-12
    grouped = {'f1r': [1, .5], 'f2r': [0, .25]}
    identical = paired_bootstrap(grouped, grouped, n=100, seed=42)
    assert identical['native'] == identical['candidate']
    assert identical['candidate_minus_native'] == [0.0, 0.0]
    # Same token profiles must give exactly the same model/control scores, with
    # folio-level disjointness even when IDs sort in a different line order.
    folios = [f'f{i}r' for i in range(1, 100)]
    train = next(f for f in folios if int(hashlib.sha256(f.encode()).hexdigest()[:8], 16) % 5 != 0)
    test = next(f for f in folios if int(hashlib.sha256(f.encode()).hexdigest()[:8], 16) % 5 == 0)
    records = {'a': {'folio': train, 'source_line': 20}, 'b': {'folio': test, 'source_line': 10}}
    profile = {'a': ['or', 'daiin', 'or'], 'b': ['daiin', 'or']}
    scored = score_profiles(records, {'old': profile, 'new': profile})
    assert scored['profiles']['old'] == scored['profiles']['new']
    assert not set(scored['profiles']['old']['train_folios']) & set(scored['profiles']['old']['test_folios'])
    compare({'count': 3, 'rate': .5}, {'count': 3, 'rate': .5 + 1e-14})
    for changed in ({'count': 4, 'rate': .5}, {'count': 3, 'rate': .6}, {'count': 3.0, 'rate': .5}):
        try:
            compare({'count': 3, 'rate': .5}, changed)
        except ValueError:
            pass
        else:
            raise AssertionError('Snapshot drift accepted')
    for malformed in ('@12;', '{x', 'dai/'):
        try:
            project(lex(malformed), 0)
        except ValueError:
            pass
        else:
            raise AssertionError('Unresolved input accepted')
    print('Sensitivity endpoints, masked characters, factor interactions and exact expectations passed.')


if __name__ == '__main__':
    main()
