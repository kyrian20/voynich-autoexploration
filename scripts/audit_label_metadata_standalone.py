#!/usr/bin/env python3
"""Audit L/R locus metadata directly from raw IVTFF; never infer object identity."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HEADER = re.compile(r'^<(?P<id>[^,<>]+),(?P<marker>[^<>])(?P<type>[A-Z][a-z0-9]*)(?:;[^<>]+)?>')
OBJECT_SUBTYPES = {'La', 'Lc', 'Lf', 'Ln', 'Lp', 'Ls', 'Lt', 'Lz'}

def scan(raw):
    records = []
    for number, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        match = HEADER.match(line)
        if match and match['type'][0] in 'LR':
            records.append({'id': match['id'], 'locus': match['type'],
                            'marker': match['marker'], 'line': number})
    ids = [r['id'] for r in records]
    if len(set(ids)) != len(ids):
        raise ValueError('Repeated locator within one edition; adjudicate instead of deduplicating')
    return records

def summarize(records):
    counts = Counter(r['locus'] for r in records)
    return {'records': len(records), 'subtypes': dict(sorted(counts.items())),
            'object_related_editorial_subtype': sum(v for k, v in counts.items() if k in OBJECT_SUBTYPES),
            'other_locus_subtype': sum(v for k, v in counts.items() if k not in OBJECT_SUBTYPES)}

def build(inputs):
    sets, reports = {}, {}
    for name, raw in sorted(inputs.items()):
        rows = scan(raw)
        sets[name] = {r['id']: r for r in rows}
        reports[name] = {'sha256': hashlib.sha256(raw).hexdigest(), **summarize(rows)}
    union = set().union(*(set(s) for s in sets.values()))
    conflicts = {}
    for locator in sorted(union):
        kinds = sorted({s[locator]['locus'] for s in sets.values() if locator in s})
        if len(kinds) > 1:
            conflicts[locator] = kinds
    return {'status': 'METADATA_AUDIT_NOT_SEMANTIC_VALIDATION',
            'sources': reports, 'union_locators': len(union),
            'missing_from_union': {name: sorted(union-set(rows)) for name, rows in sets.items()},
            'subtype_disagreements': conflicts,
            'limitations': ['Reads locus headers only; not a complete IVTFF parser.',
                           'Subtype relates to editorial layout, not verified semantic identity.',
                           'Editions represent the same manuscript, not independent samples.',
                           'Counts are neither object counts nor effective sample sizes.']}

def checks():
    fixture = b'# <f0.0,@Lp> comment\n<f2r.1,@Lp> word\n<f2r.2,*L0> x\n<f3v.1,/Ro> abc\n<f3v.2,@P0> text\n'
    rows = scan(fixture)
    assert summarize(rows)['records'] == 3
    assert summarize(rows)['object_related_editorial_subtype'] == 1
    assert [r['marker'] for r in rows] == ['@', '*', '/']
    altered = fixture.replace(b'word', b'completely.different.body')
    assert scan(altered) == rows
    try:
        scan(fixture + b'<f2r.1,@Lp> duplicate\n')
    except ValueError:
        pass
    else:
        raise AssertionError('Repeated locator not rejected')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', action='append', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    checks()
    names = [x.name for x in args.source]
    if len(set(names)) != len(names):
        raise ValueError('Source basenames must be unique')
    report = build({x.name: x.read_bytes() for x in args.source})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'union_locators': report['union_locators'],
                      'records': {k:v['records'] for k,v in report['sources'].items()},
                      'fixture_checks': 'PASS'}))

if __name__ == '__main__':
    main()
