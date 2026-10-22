#!/usr/bin/env python3
"""Exhaustive descriptive token-policy audit; no EXP IDs or significance tests.

All 128 views share raw records. Control endpoints must equal existing reference
implementations record by record. Only stdout is written.
"""
from __future__ import annotations
import collections
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.ivtff_lossless import lex, tokens
from scripts.audit_research_readiness import ROW, SOURCES, old_tokens
from scripts.audit_ivtff_metadata import HEADER, parse_currier_language
from experiments.exp_601_folio_clustered_confirmation.script import parse as native_601

FACTORS = ('ligatures', 'alternatives', 'high_ascii', 'unreadable',
           'layout_whitespace', 'inline_annotations', 'nonalpha_glyphs')
FULL = (1 << len(FACTORS)) - 1


def project(payload, mask, *, join_commas=False):
    if payload.diagnostics or any(s.kind == 'continuation' for s in payload.spans):
        raise ValueError('Unresolved payload/continuation; refusing partial comparison')
    output, word = [], []

    def flush():
        if word:
            output.append(''.join(word))
        word.clear()

    def visit(spans):
        for s in spans:
            kind = s.kind
            if kind in {'word_space', 'drawing_space'} or (kind == 'uncertain_space' and not join_commas):
                flush()
            elif kind == 'ligature':
                visit(s.children) if mask & 1 else flush()
            elif kind == 'alternatives':
                visit(s.options[0]) if mask & 2 else flush()
            elif kind == 'high_ascii':
                word.append(s.raw) if mask & 4 else flush()
            elif kind == 'unreadable':
                word.append(s.raw) if mask & 8 else flush()
            elif kind == 'layout_whitespace':
                if not mask & 16:
                    flush()
            elif kind in {'comment', 'text_tag', 'paragraph_start', 'paragraph_end'}:
                if not mask & 32:
                    flush()
            elif kind == 'glyph':
                if mask & 64:
                    word.append(s.raw)
                elif 'a' <= s.raw.lower() <= 'z':
                    word.append(s.raw.lower())
                else:
                    flush()
    visit(payload.spans)
    flush()
    return output


def empty_metric():
    return {'records': 0, 'token_lines': 0, 'tokens': 0, 'target': 0,
            'initial': 0, 'final': 0, 'expected_initial': 0.0}


def update(metric, words):
    metric['records'] += 1
    metric['token_lines'] += bool(words)
    metric['tokens'] += len(words)
    target = words.count('daiin')
    metric['target'] += target
    metric['initial'] += bool(words and words[0] == 'daiin')
    metric['final'] += bool(words and words[-1] == 'daiin')
    if words:
        metric['expected_initial'] += target / len(words)


def finish(metric):
    expected = metric['expected_initial']
    return {**metric, 'initial_enrichment': metric['initial'] / expected if expected else None}


def shapley(values):
    n = len(FACTORS)
    if len(values) != 2 ** n:
        raise ValueError('Incomplete factorial grid')
    contributions = {}
    for i, name in enumerate(FACTORS):
        value = 0.0
        for mask in range(2 ** n):
            if mask & (1 << i):
                continue
            k = mask.bit_count()
            weight = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
            value += weight * (values[mask | (1 << i)] - values[mask])
        contributions[name] = value
    if abs(sum(contributions.values()) - (values[-1] - values[0])) > 1e-8:
        raise ValueError('Shapley decomposition does not reconstruct the endpoint change')
    return contributions


def read_records(path):
    raw = path.read_bytes()
    records = []
    active_page = None
    language = 'unknown'
    seen = set()
    for number, line in enumerate(raw.decode('utf-8-sig').splitlines(), 1):
        header = HEADER.match(line)
        if header:
            active_page = header[1]
            language = parse_currier_language(header[2]) or 'unknown'
            continue
        match = ROW.match(line)
        if not match:
            continue
        if match['page'] != active_page:
            raise ValueError(f'Locus/page mismatch at source line {number}')
        identifier = match['page'] + '.' + match['number']
        if identifier in seen:
            raise ValueError(f'Duplicate locus {identifier}; refusing ambiguous pairing')
        seen.add(identifier)
        payload = lex(match['body'])
        if any(s.kind == 'text_tag' and s.raw.startswith('<@L=') for s in payload.spans):
            raise ValueError('Inline language scope needs separate adjudication')
        records.append({'id': identifier, 'source_line': number, 'folio': match['page'],
                        'currier': language, 'locus': match['locus'].split(';')[0][1:],
                        'body': match['body'], 'payload': payload})
    if not records:
        raise ValueError('No records')
    return raw, records


def native_bridge(path, records):
    native = native_601(path)
    by_line = {r['source_line']: r for r in records}
    native_words = {r['line']: r['words'] for r in native}
    candidate = {r['source_line']: tokens([r['payload']]) for r in records
                 if r['currier'] == 'B' and r['locus'] == 'P0'}
    candidate = {key: value for key, value in candidate.items() if len(value) >= 2}
    common = sorted(set(native_words) & set(candidate))
    result = {}
    for name, words in [('native_601', native_words), ('candidate', candidate)]:
        metric = empty_metric()
        common_metric = empty_metric()
        for value in words.values():
            update(metric, value)
        for key in common:
            update(common_metric, words[key])
        result[name] = {'own_eligible': finish(metric), 'common_eligible': finish(common_metric)}
    result['common_records'] = len(common)
    result['native_only_ids'] = [by_line[key]['id'] for key in sorted(set(native_words) - set(candidate))]
    result['candidate_only_ids'] = [by_line[key]['id'] for key in sorted(set(candidate) - set(native_words))]
    return result


def audit_source(label, filename):
    path = ROOT / 'data/transcriptions' / filename
    raw, records = read_records(path)
    scopes = ('all', 'A_P0_min2', 'B_P0_min2', 'A_P0_common_min2', 'B_P0_common_min2')
    grid = [{key: empty_metric() for key in scopes} for _ in range(FULL + 1)]
    common_ids = {'A': [], 'B': []}
    endpoints_changed = []
    comma_metrics = {name: empty_metric() for name in ('split', 'join', 'split_common_min2', 'join_common_min2')}
    for r in records:
        views = [project(r['payload'], mask) for mask in range(FULL + 1)]
        if views[0] != old_tokens(r['body']):
            raise ValueError(f'Legacy endpoint disagrees at {label}/{r["id"]}')
        if views[FULL] != tokens([r['payload']]):
            raise ValueError(f'Candidate endpoint disagrees at {label}/{r["id"]}')
        for mask, words in enumerate(views):
            update(grid[mask]['all'], words)
        cls = r['currier']
        if cls in ('A', 'B') and r['locus'] == 'P0':
            common = all(len(words) >= 2 for words in views)
            if common:
                common_ids[cls].append(r['id'])
            for mask, words in enumerate(views):
                if len(words) >= 2:
                    update(grid[mask][cls + '_P0_min2'], words)
                if common:
                    update(grid[mask][cls + '_P0_common_min2'], words)
        signature = lambda w: (w.count('daiin'), bool(w and w[0] == 'daiin'), bool(w and w[-1] == 'daiin'))
        if signature(views[0]) != signature(views[-1]):
            endpoints_changed.append({'id': r['id'], 'currier': cls, 'locus': r['locus'], 'raw_body': r['body'],
                                      'legacy': views[0], 'candidate': views[-1]})
        split, join = views[-1], project(r['payload'], FULL, join_commas=True)
        if join != tokens([r['payload']], uncertain_space='join'):
            raise ValueError('Comma sensitivity projection disagrees with reference')
        update(comma_metrics['split'], split)
        update(comma_metrics['join'], join)
        if cls == 'B' and r['locus'] == 'P0' and len(split) >= 2 and len(join) >= 2:
            update(comma_metrics['split_common_min2'], split)
            update(comma_metrics['join_common_min2'], join)
    completed = [{scope: finish(metric) for scope, metric in row.items()} for row in grid]
    return {'transcription': label, 'source': str(path.relative_to(ROOT)),
            'source_sha256': hashlib.sha256(raw).hexdigest(), 'records': len(records),
            'endpoint_equivalence_checked_per_record': True,
            'policies': [{'mask': mask, 'enabled': [factor for bit, factor in enumerate(FACTORS) if mask & (1 << bit)],
                          'metrics': metrics} for mask, metrics in enumerate(completed)],
            'common_P0_records': {cls: {'count': len(ids), 'sha256_of_newline_ids': hashlib.sha256(('\n'.join(ids) + '\n').encode()).hexdigest()}
                                  for cls, ids in common_ids.items()},
            'target_count_shapley': shapley([row['all']['target'] for row in completed]),
            'initial_count_shapley': shapley([row['all']['initial'] for row in completed]),
            'endpoint_target_or_position_changes': endpoints_changed,
            'comma_sensitivity_separate_from_factorial': {name: finish(value) for name, value in comma_metrics.items()},
            'native_EXP601_bridge': native_bridge(path, records)}


def main():
    output = {'audit': 'descriptive_token_policy_factorial_sensitivity', 'version': 1,
              'factors': list(FACTORS), 'policy_count': FULL + 1,
              'protocol': 'research/maintenance/2026-10-22-token-sensitivity/PROTOCOL.md',
              'files': [audit_source(*source) for source in SOURCES],
              'limitations': ['Exploratory sensitivity, not a new confirmatory experiment or decipherment.',
                              'Shapley values attribute changes within this grid; they are not causal evidence.',
                              'Commas are split in the factorial; their join sensitivity is reported separately.',
                              'No bootstrap intervals or new p-values; ratios are descriptive.',
                              'Alternative transcriptions are not independent samples.']}
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
