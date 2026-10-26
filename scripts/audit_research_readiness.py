#!/usr/bin/env python3
"""Descriptive audit of lexical information preservation, never a new EXP.

Only stdout is written. Historical tokenizers, sources and result files are not
changed. A candidate projection is compared on identical raw records; no
statistical significance, translation or official conformance is asserted.
"""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ivtff_lossless import lex, tokens
from scripts.audit_legacy_portability import MANIFEST

ROW = re.compile(r'^<(?P<page>f(?:[0-9]+[rv][1-6]?|Ros))\.(?P<number>[0-9]+),(?P<locus>[^>]*)>\s*(?P<body>.*)$')
SOURCES = [('ZL3b', 'eva_zl3b.txt'), ('ZL3a', 'zl3a.txt'), ('IT2a', 'eva_it2a.txt')]


def old_tokens(body):
    return re.findall('[a-z]+', re.sub(r'<[^>]*>|\{[^}]*\}|\[[^\]]*\]', ' ', body).lower())


def audit_source(label, filename):
    path = ROOT / 'data/transcriptions' / filename
    raw = path.read_bytes()
    diagnostics = collections.Counter()
    features = collections.Counter()
    examples = []
    changed_examples = []
    count = valid = changed = 0
    legacy_target = candidate_target = 0
    opaque_only_recovered = []
    payload_hashes = hashlib.sha256()
    for source_line, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        match = ROW.match(line)
        if not match:
            # Python regex \\d also accepts Unicode decimal digits.
            # Reject invalid numeric tags instead of silently losing records.
            if line.startswith('<f') and any(
                ch.isdecimal() and not ch.isascii()
                for ch in line.partition('>')[0]
            ):
                raise ValueError(f'Non-ASCII decimal digit in IVTFF identifier at source line {source_line}')
            continue
        count += 1
        body = match['body']
        parsed = lex(body)
        reconstructed = ''.join(s.raw for s in parsed.spans)
        if body != reconstructed:
            raise ValueError(f'Raw payload lost: {filename}:{source_line}')
        payload_hashes.update((body + '\n').encode())
        # Validate nested offsets, not merely top-level round-tripping.
        def visit(spans):
            for span in spans:
                if body[span.start:span.end] != span.raw:
                    raise ValueError('Incorrect raw source offset')
                features[span.kind] += 1
                visit(span.children)
                for option in span.options:
                    visit(option)
        visit(parsed.spans)
        identifier = match['page'] + '.' + match['number']
        if parsed.diagnostics:
            diagnostics.update(x['code'] for x in parsed.diagnostics)
            if len(examples) < 30:
                examples.append({'id': identifier, 'source_line': source_line,
                                 'raw_body': body, 'diagnostics': parsed.diagnostics})
            continue
        # Continuations require document-level assembly, which this audit does
        # not attempt. Refuse a partial-line projection rather than dropping it.
        try:
            candidate = tokens([parsed])
        except ValueError:
            diagnostics['continuation_requires_assembly'] += 1
            continue
        valid += 1
        historical = old_tokens(body)
        legacy_target += historical.count('daiin')
        candidate_target += candidate.count('daiin')
        if historical != candidate:
            changed += 1
            if len(changed_examples) < 20:
                changed_examples.append({'id': identifier, 'historical': historical,
                                         'candidate_primary_split_expand': candidate})
        if not historical and candidate:
            opaque_only_recovered.append({'id': identifier, 'tokens': candidate})
    return {'transcription': label, 'source': str(path.relative_to(ROOT)),
            'source_sha256': hashlib.sha256(raw).hexdigest(), 'records': count,
            'raw_payloads_roundtrip': True, 'nested_offsets_checked': True,
            'raw_payload_stream_sha256': payload_hashes.hexdigest(),
            'projectable_records': valid, 'unprojected_records': count - valid,
            'diagnostic_event_counts': dict(sorted(diagnostics.items())),
            'feature_counts_including_all_alternatives': dict(sorted(features.items())),
            'changed_token_lists_on_same_projectable_records': changed,
            'exact_daiin_on_same_projectable_records': {'historical': legacy_target, 'candidate': candidate_target},
            'previously_token_empty_records_represented': opaque_only_recovered,
            'diagnostic_examples': examples, 'changed_examples': changed_examples}


def main():
    manifest = json.loads(MANIFEST.read_text())
    missing = [{'script': entry['path'], 'target': target['relative_path'],
                'required': target.get('required'), 'usage': target.get('usage', 'unclassified')}
               for entry in manifest['files'] for target in entry['targets']
               if not (ROOT / target['relative_path']).exists()]
    print(json.dumps({'audit': 'intensive_research_readiness', 'version': 1,
                      'migration_files': len(manifest['files']), 'missing_input_references': missing,
                      'candidate_policy': {'uncertain_space': 'split', 'alternatives': 'primary', 'ligatures': 'expand',
                                           'high_ascii': 'opaque literal code, not decoded', 'whitespace': 'layout only'},
                      'files': [audit_source(*source) for source in SOURCES],
                      'limitations': ['Lexical layer only; full alphabet-specific and document-level conformance not certified.',
                                      'Candidate views are not replacements for production experiments.',
                                      'Related transcriptions are not independent manuscripts.',
                                      'Static portability verification does not execute all 624 historical directories.']},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
