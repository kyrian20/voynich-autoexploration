#!/usr/bin/env python3
"""Frozen EXP-607 locus-scope diagnostic; stdout only, no lexical meanings."""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import random
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_exp607_reader_sensitivity import (
    audit_source, native, reconstruct_native_words)
from scripts.audit_token_policy_sensitivity import read_records
from scripts.check_audit_snapshot import compare
from scripts.ivtff_lossless import tokens

PROTOCOL = 'research/maintenance/2026-10-22-exp607-scope/PROTOCOL.md'
SEEDS = [6072026] + [
    int(hashlib.sha256(f'EXP607-scope-control-v1:{i}'.encode()).hexdigest()[:16], 16)
    for i in range(63)]
TEST_SCOPES = ('mixed', 'P0', 'non_P0', 'labels', 'circular_radial', 'other_paragraph')


def locus_class(locus):
    if locus == 'P0':
        return 'P0'
    if locus.startswith('P'):
        return 'other_paragraph'
    if locus.startswith('L'):
        return 'labels'
    if locus.startswith(('C', 'R')):
        return 'circular_radial'
    raise ValueError(f'Unregistered locus class: {locus}')


def in_scope(row, scope):
    category = locus_class(row['locus'])
    if scope == 'mixed':
        return True
    if scope == 'non_P0':
        return category != 'P0'
    if scope not in TEST_SCOPES:
        raise ValueError(scope)
    return category == scope


def is_test(folio):
    return int(hashlib.sha256(folio.encode()).hexdigest()[:8], 16) % 5 == 0


def select(records, words, ids, scope, test):
    selected = [key for key in ids
                if in_scope(records[key], scope)
                and is_test(records[key]['folio']) == test]
    selected.sort(key=lambda key: records[key]['source_line'])
    grouped = collections.defaultdict(list)
    for key in selected:
        grouped[records[key]['folio']].append(words[key])
    metadata = {
        'lines': len(selected), 'folios': sorted(grouped),
        'id_set_sha256': hashlib.sha256(
            ('\n'.join(sorted(selected)) + '\n').encode()).hexdigest(),
        'locus_counts': dict(sorted(collections.Counter(
            records[key]['locus'] for key in selected).items()))}
    return sorted(grouped.items()), metadata


def shuffle_groups(groups, seed):
    rng = random.Random(seed)
    result = []
    for folio, lines in groups:
        new_lines = []
        for line in lines:
            shuffled = list(line)
            rng.shuffle(shuffled)
            new_lines.append(shuffled)
        result.append((folio, new_lines))
    return result


def evaluate(train, test):
    if {f for f, _ in train} & {f for f, _ in test}:
        raise ValueError('Train/test folios overlap')
    if not train or not test:
        return {'available': False, 'reason': 'empty_train_or_test'}
    real = native.score(train, test)
    if real['tokens_scored'] == 0:
        return {'available': False, 'reason': 'no_test_transitions'}
    control = native.score(train, test, shuffled=True)
    return {
        'available': True, 'real': real, 'original_seed_control': control,
        'real_minus_original_seed_gain':
            real['gain_vs_unigram_bits_per_token']
            - control['gain_vs_unigram_bits_per_token']}


def linear_quantile(values, q):
    ordered = sorted(values)
    if not ordered or not 0 <= q <= 1:
        raise ValueError('Invalid quantile input')
    at = (len(ordered) - 1) * q
    lower = int(at)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (at - lower)


def seed_diagnostic(train, test):
    scored = evaluate(train, test)
    if not scored['available']:
        return scored
    gains = []
    for seed in SEEDS:
        control = native.score(shuffle_groups(train, seed), test)
        if seed == SEEDS[0]:
            compare(scored['original_seed_control'], control)
        gains.append(control['gain_vs_unigram_bits_per_token'])
    real_gain = scored['real']['gain_vs_unigram_bits_per_token']
    return {
        'available': True, 'real_gain_vs_unigram': real_gain,
        'controls': [{'seed': s, 'gain_vs_unigram': g}
                     for s, g in zip(SEEDS, gains)],
        'control_mean': statistics.mean(gains),
        'control_min': min(gains), 'control_max': max(gains),
        'control_q95_linear': linear_quantile(gains, .95),
        'controls_at_least_real': sum(g >= real_gain for g in gains),
        'real_minus_control_mean': real_gain - statistics.mean(gains),
        'original_seed_matches_native': True}


def audit(label, relative, previous):
    # Abort on drift before any new scope comparison.
    reproduced = audit_source(label, relative)
    compare(previous, reproduced)
    raw, rows = read_records(ROOT / relative)
    rows = [row for row in rows if re.fullmatch(r'f\d+[rv]', row['folio'])]
    records = {row['id']: row for row in rows}
    old, candidate = {}, {}
    for row in rows:
        a = reconstruct_native_words(row['body'])
        b = [w for w in tokens([row['payload']]) if re.fullmatch(r'[a-z]{2,}', w)]
        if len(a) >= 2:
            old[row['id']] = a
        if len(b) >= 2:
            candidate[row['id']] = b
    ids = sorted(set(old) & set(candidate))
    profiles = {}
    for name, words in [('native_607', old), ('candidate_conservative_ascii', candidate)]:
        cross = {}
        for train_scope in ('mixed', 'P0'):
            train, train_meta = select(records, words, ids, train_scope, False)
            evaluations = {}
            for test_scope in TEST_SCOPES:
                test, test_meta = select(records, words, ids, test_scope, True)
                evaluations[test_scope] = {
                    'test': test_meta, 'scores': evaluate(train, test)}
            cross[train_scope] = {'train': train_meta, 'evaluations': evaluations}
        mixed = cross['mixed']
        prior = previous['common_record_comparison']['profiles'][name]
        compare(prior['real'], mixed['evaluations']['mixed']['scores']['real'])
        compare(prior['fixed_shuffled_training_control'],
                mixed['evaluations']['mixed']['scores']['original_seed_control'])
        train, _ = select(records, words, ids, 'P0', False)
        test, _ = select(records, words, ids, 'P0', True)
        profiles[name] = {
            'cross_scope': cross, 'P0_to_P0_64_seed_diagnostic': seed_diagnostic(train, test)}
    # Physical sample/split metadata must agree across token profiles.
    a, b = profiles.values()
    for scope in ('mixed', 'P0'):
        compare(a['cross_scope'][scope]['train'], b['cross_scope'][scope]['train'])
        for test_scope in TEST_SCOPES:
            compare(a['cross_scope'][scope]['evaluations'][test_scope]['test'],
                    b['cross_scope'][scope]['evaluations'][test_scope]['test'])
    return {
        'transcription': label, 'source': relative,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'previous_mixed_snapshot_reproduced': True,
        'common_physical_records': len(ids), 'profiles': profiles}


def main():
    if (native.ALPHA, native.BIGRAM_WEIGHT, native.TEST_MOD) != (.1, .5, 5):
        raise ValueError('Frozen model settings changed')
    snapshot = json.loads((ROOT / 'research/maintenance/2026-10-22-token-sensitivity/exp607-results.json').read_text())
    prior = {d['transcription']: d for d in snapshot['files']}
    result = {
        'audit': 'EXP607_locus_scope_and_control_seed_diagnostic',
        'version': 1, 'protocol': PROTOCOL,
        'protocol_sha256': hashlib.sha256((ROOT / PROTOCOL).read_bytes()).hexdigest(),
        'settings': {'alpha': .1, 'bigram_weight': .5, 'folio_test_modulo': 5,
                     'control_seed_count': 64, 'q95': 'linear, index (n-1)*q'},
        'files': [audit(label, relative, prior[label]) for label, relative in native.FILES],
        'limits': [
            'Exploratory follow-up on previously observed folios, not fresh confirmation.',
            'No semantic, phonetic, language or decipherment assignments.',
            'A control quantile is not a confidence interval; ranks are not confirmatory p-values.',
            'Conditional on common-record eligibility, basic folios, readers, fixed split and model.',
            'Related transcriptions are sensitivity views of one manuscript.']}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

