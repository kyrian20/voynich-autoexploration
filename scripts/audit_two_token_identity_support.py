#!/usr/bin/env python3
"""Decompose existing two-token context support, without tuning or inference."""
from collections import Counter, defaultdict
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from analyze_two_token_residual import TwoToken, bucket, triples

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT/'research/maintenance/2026-10-23-identity-support'
INPUT = ROOT/'research/analysis/2026-10-22-residual-order/inputs.json'
PREVIOUS = ROOT/'research/analysis/2026-10-23-two-token-residual/results.json.gz'
CATEGORIES = ('unseen_H2', 'unseen_W2', 'single_identity', 'proportional_distribution', 'different_distribution')


def decompose(model, rows):
    identities = defaultdict(set)
    for h, identity in model.tables[1]:
        identities[h].add(identity)
    counts = Counter({name: 0 for name in CATEGORIES})
    support = Counter({'at_least_5': 0, 'at_least_20': 0})
    for (z, a, b), n in triples(rows).items():
        h, w = model.contexts(z, a)
        nh, nw = model.totals[0].get(h, 0), model.totals[1].get(w, 0)
        if not nh:
            category = 'unseen_H2'
        elif not nw:
            category = 'unseen_W2'
        elif len(identities[h]) == 1:
            category = 'single_identity'
        elif all(model.tables[1][w].get(t, 0)*nh == count*nw
                 for t, count in model.tables[0][h].items()):
            category = 'proportional_distribution'
        else:
            category = 'different_distribution'
            for threshold in (5, 20):
                support[f'at_least_{threshold}'] += n*(nw >= threshold)
        counts[category] += n
    total = sum(counts.values())
    if total != sum(triples(rows).values()):
        raise ValueError('Non-exhaustive classification')
    return {'triplets': total, 'categories': dict(counts),
            'different_distribution_training_support': dict(support),
            'seen_H2_contexts': total-counts['unseen_H2'],
            'seen_W2_contexts': total-counts['unseen_H2']-counts['unseen_W2']}


def controls():
    results = {}
    for positive in (True, False):
        pairs = [('aba', 'xx'), ('aca', 'yy')] if positive else [
            ('aba', 'xx'), ('aba', 'yy'), ('aca', 'xx'), ('aca', 'yy')]
        train = [{'group': 'train', 'tokens': [z, 'mid', b]} for z, b in pairs for _ in range(50)]
        dev = [{'group': 'dev', 'tokens': [z, 'mid', b]} for z, b in pairs]
        result = decompose(TwoToken(train, dev), dev)
        expected = 'different_distribution' if positive else 'proportional_distribution'
        assert result['categories'][expected] == result['triplets']
        results['positive' if positive else 'negative'] = result
    train = [{'group': 'train', 'tokens': ['aba', 'mid', 'xx']}]*20
    dev = [{'group': 'dev', 'tokens': ['aba', 'mid', 'xx']}]
    model = TwoToken(train, dev)
    assert decompose(model, dev)['categories']['single_identity'] == 1
    absent = [{'group': 'test', 'tokens': ['aza', 'mid', 'xx']},
              {'group': 'test', 'tokens': ['long', 'mid', 'xx']}]
    result = decompose(model, absent)
    assert result['categories']['unseen_W2'] == 1 and result['categories']['unseen_H2'] == 1
    results['single_and_unseen'] = result
    return results


def run():
    checked = controls()
    prior = {r['label']: r for r in json.loads(gzip.decompress(PREVIOUS.read_bytes()))['results']}
    results = []
    for source in json.loads(INPUT.read_text())['sources']:
        rows = source['records']
        parts = [[r for r in rows if predicate(bucket(r['group']))]
                 for predicate in (lambda b: b >= 2, lambda b: b == 1, lambda b: b == 0)]
        groups = [{r['group'] for r in part} for part in parts]
        assert not any(groups[i] & groups[j] for i, j in ((0, 1), (0, 2), (1, 2)))
        model = TwoToken(*parts[:2])
        development, test = [decompose(model, part) for part in parts[1:]]
        old = prior[source['label']]
        for key in ('triplets', 'seen_H2_contexts', 'seen_W2_contexts'):
            assert test[key] == old['real'][key], (source['label'], key)
        assert model.weights == old['weights_H2_W2']
        results.append({'label': source['label'], 'development': development, 'test': test,
                        'unchanged_weights_H2_W2': model.weights})
    paths = [INPUT, PREVIOUS, Path(__file__), PACKAGE/'PROTOCOL.md',
             ROOT/'scripts/analyze_two_token_residual.py',
             INPUT.parent/'residual_order.py', INPUT.parent/'residual_order_calibrated.py']
    return {'status': 'DESCRIPTIVE_IMPLEMENTATION_AUDIT', 'controls': checked, 'results': results,
            'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = run()
    path = PACKAGE/'results.json'
    if args.check:
        assert result == json.loads(path.read_text()), 'Snapshot mismatch'
        print('Identity support snapshot verified')
    else:
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
        for r in result['results']:
            print(r['label'], json.dumps(r['test']))
