#!/usr/bin/env python3
"""Sensitivity of an existing model using its original split and settings.

No historical outputs are written. Absolute cross-reader losses have different
token events/vocabularies and must not be treated as identical estimands.
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
from experiments.exp_607_heldout_bigram_prediction import script as native
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens


def reconstruct_native_words(body):
    body = re.sub(r'<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?', ' ', body)
    return native.TOKEN_RE.findall(body.lower())


def score_profiles(records, words_by_profile):
    """Same physical rows and folio split for all supplied token profiles."""
    ids = sorted(set.intersection(*(set(words) for words in words_by_profile.values())))
    profiles = {}
    for name, words in words_by_profile.items():
        train, test = collections.defaultdict(list), collections.defaultdict(list)
        # Fixed shuffle consumes tokens in source-line order within each folio.
        for identifier in sorted(ids, key=lambda key: records[key]['source_line']):
            folio = records[identifier]['folio']
            bucket = int(hashlib.sha256(folio.encode()).hexdigest()[:8], 16) % native.TEST_MOD
            (test if bucket == 0 else train)[folio].append(words[identifier])
        assert not set(train) & set(test)
        train_groups, test_groups = sorted(train.items()), sorted(test.items())
        if not train_groups or not test_groups:
            raise ValueError('Empty train or test')
        real = native.score(train_groups, test_groups)
        control = native.score(train_groups, test_groups, shuffled=True)
        profiles[name] = {
            'real': real, 'fixed_shuffled_training_control': control,
            'real_minus_control_gain': real['gain_vs_unigram_bits_per_token'] - control['gain_vs_unigram_bits_per_token'],
            'train_folios': sorted(train), 'test_folios': sorted(test),
            'train_lines': sum(map(len, train.values())),
            'test_lines': sum(map(len, test.values()))}
    return {
        'common_physical_records': len(ids),
        'common_id_set_sha256': hashlib.sha256(('\n'.join(ids) + '\n').encode()).hexdigest(),
        'profiles': profiles,
        'one_reader_only_ids': {name: sorted(set(words) - set(ids)) for name, words in words_by_profile.items()}}


def audit_source(label, relative):
    path = ROOT / relative
    raw, rows = read_records(path)
    # Keep the original basic-page universe, although the lexer handles foldouts.
    rows = [row for row in rows if re.fullmatch(r'f\d+[rv]', row['folio'])]
    reconstructed = collections.defaultdict(list)
    old, candidate = {}, {}
    records = {r['id']: r for r in rows}
    loci = collections.Counter()
    for row in rows:
        words = reconstruct_native_words(row['body'])
        if len(words) >= 2:
            old[row['id']] = words
            reconstructed[row['folio']].append(words)
            loci[row['locus']] += 1
        new_words = [word for word in tokens([row['payload']]) if re.fullmatch(r'[a-z]{2,}', word)]
        if len(new_words) >= 2:
            candidate[row['id']] = new_words
    baseline = native.load(label, relative)
    if sorted(reconstructed.items()) != sorted(baseline['train'] + baseline['test']):
        raise ValueError('Record reconstruction disagrees with original EXP-607 loader')
    saved = json.loads((ROOT / 'experiments/exp_607_heldout_bigram_prediction/results.json').read_text())
    saved = next(source for source in saved['sources'] if source['label'] == label)
    reproduced = {}
    for name, shuffled in [('real_sequence', False), ('shuffled_train_control', True)]:
        score = native.score(baseline['train'], baseline['test'], shuffled=shuffled)
        for key, value in saved[name].items():
            if isinstance(value, (int, float)) and not math.isclose(score[key], value, rel_tol=1e-12, abs_tol=1e-12):
                raise ValueError(f'Historical score mismatch: {label}/{name}/{key}')
        reproduced[name] = score
    return {
        'transcription': label, 'source': relative,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'historical_summary_reproduced': True,
        'native_scope_locus_counts': dict(sorted(loci.items())),
        'historical_scores': reproduced,
        'common_record_comparison': score_profiles(records, {'native_607': old, 'candidate_conservative_ascii': candidate})}


def main():
    if native.ALPHA != .1 or native.BIGRAM_WEIGHT != .5 or native.TEST_MOD != 5:
        raise ValueError('Native model settings changed; refusing unregistered sensitivity')
    result = {
        'audit': 'EXP607_existing_model_reader_sensitivity', 'version': 1,
        'protocol': 'research/maintenance/2026-10-22-token-sensitivity/PROTOCOL.md',
        'fixed_settings': {'alpha': .1, 'bigram_weight': .5, 'test_modulo': 5, 'shuffle_seed_in_native_code': 6072026},
        'candidate_policy': 'Existing lossless primary/split/expand view, then retain only whole tokens matching [a-z]{2,}.',
        'files': [audit_source(label, relative) for label, relative in native.FILES],
        'limitations': [
            'Same historical split already observed; exploratory sensitivity, not fresh held-out confirmation.',
            'Token streams/vocabularies differ: absolute cross-reader losses are not directly comparable.',
            'A single fixed training shuffle is a diagnostic, not a full null distribution.',
            'Related transcriptions are not independent samples.',
            'Original basic-page universe retained; no foldout-page generalization.']}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
