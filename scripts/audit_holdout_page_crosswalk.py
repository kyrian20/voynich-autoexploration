#!/usr/bin/env python3
"""Cross-check strict IVTFF page names against frozen physical-leaf partitions.

Header/identifier audit only: never tokenize or score held-out text.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

from audit_holdout_locus_coverage import ROOT, SOURCE_NAMES, audit, load_manifest
from audit_ivtff_page_locus_ids import audit_text, structural_errors

NUMERIC_PAGE = re.compile(r"f([0-9]+)[rv][1-6]?")


def crosswalk(sources: dict[str, bytes], manifest: dict) -> dict:
    coverage = audit(sources, manifest)  # verifies hashes and exact leaf coverage
    allocation = {leaf: group for group, leaves in manifest['partitions'].items()
                  for leaf in leaves}
    editions = {}
    for name in SOURCE_NAMES:
        text = sources[name].decode('utf-8-sig')
        strict = audit_text(text)
        errors = structural_errors(strict)
        if errors:
            raise ValueError(f'{name}: strict structural errors: {errors}')
        pages = {}
        for page in strict['page_names']:
            match = NUMERIC_PAGE.fullmatch(page)
            leaf = int(match.group(1)) if match else None
            pages[page] = {'physical_leaf': leaf,
                           'partition': allocation.get(leaf, 'excluded_unassigned')}
        # Compare independent header recognizers, including panels, to the
        # coverage reader. A broad regex must not add a phantom numeric page.
        strict_leaves = {p['physical_leaf'] for p in pages.values()
                         if p['physical_leaf'] is not None}
        expected = set(coverage['source_coverage'][name]['numeric_leaves'])
        if strict_leaves != expected:
            raise ValueError(f'{name}: page/coverage readers disagree on physical leaves')
        editions[name] = {'sha256': hashlib.sha256(sources[name]).hexdigest(),
                          'pages': pages,
                          'page_count': len(pages),
                          'locus_count': strict['record_count'],
                          'continuation_rows': strict['continuation_lines']}
    left, right = (set(editions[n]['pages']) for n in SOURCE_NAMES)
    shared = sorted(left & right)
    for page in shared:
        if editions[SOURCE_NAMES[0]]['pages'][page] != editions[SOURCE_NAMES[1]]['pages'][page]:
            raise ValueError(f'Cross-edition page assignment mismatch: {page}')
    return {'status': 'IDENTIFIER_CROSSWALK_VERIFIED_NOT_SEMANTIC_VALIDATION',
            'manifest_sha256': hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(),
            'manifest_hash_policy': 'SHA-256 of json.dumps(manifest, sort_keys=True), UTF-8',
            'editions': editions, 'shared_page_count': len(shared),
            'edition_only_pages': {SOURCE_NAMES[0]: sorted(left-right), SOURCE_NAMES[1]: sorted(right-left)},
            'limitations': ['Identifier agreement does not authenticate physical binding or page content.',
                            'Named pages remain excluded/unassigned.',
                            'No tokens, predictive metrics, semantic rules or historically blind validation.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    sources = {name: (ROOT/'data/transcriptions'/name).read_bytes() for name in SOURCE_NAMES}
    result = crosswalk(sources, load_manifest())
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'shared_page_count', 'edition_only_pages')}))


if __name__ == '__main__':
    main()
