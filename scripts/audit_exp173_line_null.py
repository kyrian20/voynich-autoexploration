#!/usr/bin/env python3
"""Exact descriptive line-conditioned expectations; no significance test."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import audit_exp173_currier_crosswalk as prior


def expectation(lines, feature, endpoint):
    if not lines or any(not line for line in lines):
        raise ValueError('Nonempty lines required')
    counts = [sum(feature(w) for w in line) for line in lines]
    observed = sum(feature(line[endpoint]) for line in lines)
    exact = sum((Fraction(k, len(line)) for k, line in zip(counts, lines)), Fraction())
    pooled = Fraction(len(lines) * sum(counts), sum(map(len, lines)))
    return {'observed': observed, 'feature_tokens': sum(counts),
            'expected_within_line_fraction': str(exact),
            'expected_within_line': float(exact), 'expected_pooled': float(pooled),
            'ratio_within_line': float(Fraction(observed) / exact) if exact else None,
            'ratio_pooled': float(Fraction(observed) / pooled) if pooled else None}


def run():
    prior.run()  # pin corpus/script and verify historical descriptive metrics
    rows, _, labels = prior.read_legacy_population(prior.SOURCE.read_text(encoding='utf-8-sig'))
    selected = [r for r in rows if labels.get(r['page']) == 'B']
    lines = [r['tokens'] for r in selected]
    return {'status': 'EXPLORATORY_DENOMINATOR_AUDIT',
            'source_sha256': hashlib.sha256(prior.SOURCE.read_bytes()).hexdigest(),
            'reader_sha256': hashlib.sha256(Path(prior.__file__).read_bytes()).hexdigest(),
            'lines': len(lines), 'tokens': sum(map(len, lines)),
            'numeric_folios': len({r['number'] for r in selected}),
            'pages': len({r['page'] for r in selected}),
            'singleton_lines': sum(len(line) == 1 for line in lines),
            'am_final': expectation(lines, lambda w: w.endswith('am'), -1),
            'y_initial': expectation(lines, lambda w: w.lower().startswith('y'), 0),
            'limits': 'Historical parser; no p-values, clustered interval or semantic inference.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise SystemExit('Snapshot mismatch')
        print('Line-null snapshot verified')
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
