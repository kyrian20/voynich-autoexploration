#!/usr/bin/env python3
"""Paired folio bootstrap for a frozen endpoint under two readers; stdout only."""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.exp_601_folio_clustered_confirmation import script as native
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens


def paired_bootstrap(old_folios, new_folios, n=20000, seed=native.SEED):
    if set(old_folios) != set(new_folios) or not old_folios:
        raise ValueError('Folio sets must be nonempty and identical')
    folios = sorted(old_folios)
    rng = random.Random(seed)
    draws = {'native': [], 'candidate': [], 'candidate_minus_native': []}
    for _ in range(n):
        old_o = old_e = new_o = new_e = 0.0
        for _ in folios:
            folio = folios[rng.randrange(len(folios))]
            old_o += old_folios[folio][0]
            old_e += old_folios[folio][1]
            new_o += new_folios[folio][0]
            new_e += new_folios[folio][1]
        if not old_e or not new_e:
            raise ValueError('Zero denominator in a paired bootstrap draw')
        a, b = old_o / old_e, new_o / new_e
        draws['native'].append(a)
        draws['candidate'].append(b)
        draws['candidate_minus_native'].append(b - a)
    return {key: [native.quantile(values, .025), native.quantile(values, .975)] for key, values in draws.items()}


def main():
    path = ROOT / 'data/transcriptions/eva_zl3b.txt'
    raw, records = read_records(path)
    native_rows = native.parse(path)
    native_words = {row['line']: row['words'] for row in native_rows}
    by_line = {row['source_line']: row for row in records}
    candidate_words = {row['source_line']: tokens([row['payload']]) for row in records
                       if row['currier'] == 'B' and row['locus'] == 'P0'}
    candidate_words = {key: words for key, words in candidate_words.items() if len(words) >= 2}
    if set(candidate_words) != set(native_words):
        raise ValueError('Historical bootstrap interval requires unchanged eligible record set')
    grouped = {}
    for name, words in [('native', native_words), ('candidate', candidate_words)]:
        folios = collections.defaultdict(lambda: [0, 0.0])
        for key in sorted(words):
            folio = by_line[key]['folio']
            folios[folio][0] += int(words[key][0] == 'daiin')
            folios[folio][1] += words[key].count('daiin') / len(words[key])
        grouped[name] = dict(folios)
    intervals = paired_bootstrap(grouped['native'], grouped['candidate'])
    saved = json.loads((ROOT / 'experiments/exp_601_folio_clustered_confirmation/results.json').read_text())
    expected = saved['primary_effect']['folio_cluster_bootstrap_ci95_percentile']
    if [round(x, 6) for x in intervals['native']] != expected:
        raise ValueError('Original bootstrap interval did not reproduce')
    effects = {}
    for name, folios in grouped.items():
        observed = sum(x[0] for x in folios.values())
        expectation = sum(x[1] for x in folios.values())
        effects[name] = {'observed': observed, 'expected': expectation, 'enrichment': observed / expectation}
    print(json.dumps({
        'audit': 'EXP601_paired_reader_bootstrap_sensitivity', 'version': 1,
        'source_sha256': hashlib.sha256(raw).hexdigest(),
        'common_lines': len(native_words), 'common_folios': len(grouped['native']),
        'replicates': 20000, 'seed': native.SEED,
        'historical_bootstrap_interval_reproduced': True,
        'effects': effects, 'percentile_95_intervals': intervals,
        'limitations': [
            'Exploratory sensitivity on the same previously observed folios; not an independent confirmatory test.',
            'The same folio draws are used in both views; no source or historical result is overwritten.',
            'No new p-values; intervals quantify the declared folio resampling procedure.',
            'No full IVTFF certification or semantic inference.']}, indent=2))


if __name__ == '__main__':
    main()
