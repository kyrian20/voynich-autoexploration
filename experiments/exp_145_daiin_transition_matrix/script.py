#!/usr/bin/env python3
"""
exp_145: daiin Transition Matrix — H287
Is daiin a cth-specific determiner or general linker?
Compute daiin→[onset] enrichment across all onset classes in A and B dialects.
Compare with aiin/ar/ol→cth enrichment to isolate uniqueness.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict

CORPUS_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Onset classes (order matters — longer/more specific first)
ONSET_CLASSES = [
    ('qok', re.compile(r'^qok')),
    ('qot', re.compile(r'^qot')),
    ('qo',  re.compile(r'^qo')),
    ('cth', re.compile(r'^cth')),
    ('ch_e',re.compile(r'^che')),
    ('ch',  re.compile(r'^ch')),
    ('sh',  re.compile(r'^sh')),
    ('ok',  re.compile(r'^ok')),
    ('ot',  re.compile(r'^ot')),
    ('ol',  re.compile(r'^ol')),
    ('d',   re.compile(r'^d')),
    ('s',   re.compile(r'^s')),
    ('y',   re.compile(r'^y')),
    ('k',   re.compile(r'^k')),
    ('t',   re.compile(r'^t')),
    ('l',   re.compile(r'^l')),
    ('r',   re.compile(r'^r')),
    ('p',   re.compile(r'^p')),
    ('f',   re.compile(r'^f')),
    ('other', re.compile(r'.')),
]

def get_onset(word):
    for cls, pat in ONSET_CLASSES:
        if pat.match(word):
            return cls
    return 'other'

def get_folio_dialect(folio_base, folio_words):
    """Assign dialect: B if edy/eedy rate >= 5% and >= 10 words."""
    if len(folio_words) < 10:
        return 'unknown'
    b_count = sum(1 for w in folio_words if w.endswith('edy') or w.endswith('eedy'))
    return 'B' if b_count / len(folio_words) >= 0.05 else 'A'

def parse_corpus():
    folio_words = defaultdict(list)
    with open(CORPUS_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(' ', 1)
            if len(parts) < 2:
                continue
            locus_raw = parts[0]
            text = parts[1]
            locus_parts = locus_raw.split(',')
            if len(locus_parts) < 1:
                continue
            folio_str = locus_parts[0]
            folio_base = folio_str.split('.')[0]
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            folio_words[folio_base].extend(words)
    return folio_words

def compute_transition_enrichment(folio_words):
    """
    For each dialect (A/B), compute:
    1. daiin→[onset] counts and enrichment vs dialect baseline
    2. aiin/ar/ol→cth counts (to test uniqueness of daiin)
    3. B-dialect: daiin→sh/ch_e enrichment (parallel role check)
    """
    # Assign dialects
    dialect_map = {}
    for fb, words in folio_words.items():
        dialect_map[fb] = get_folio_dialect(fb, words)

    # Collect all words by dialect with bigram context
    a_words = []
    b_words = []
    for fb, words in folio_words.items():
        d = dialect_map[fb]
        if d == 'A':
            a_words.extend(words)
        elif d == 'B':
            b_words.extend(words)

    def bigram_analysis(words, particle):
        """Compute transition matrix: particle → onset counts and enrichment."""
        total = len(words)
        # Baseline onset rates
        onset_counts = defaultdict(int)
        for w in words:
            onset_counts[get_onset(w)] += 1

        # Bigram: particle → next word onset
        transition_counts = defaultdict(int)
        particle_total = 0
        for i in range(len(words) - 1):
            if words[i] == particle:
                next_onset = get_onset(words[i+1])
                transition_counts[next_onset] += 1
                particle_total += 1

        results = {}
        for onset_cls, _ in ONSET_CLASSES:
            observed = transition_counts[onset_cls]
            baseline_rate = onset_counts[onset_cls] / total if total > 0 else 0
            expected = particle_total * baseline_rate
            enrichment = (observed / particle_total) / baseline_rate if baseline_rate > 0 and particle_total > 0 else 0
            results[onset_cls] = {
                'observed': observed,
                'particle_total': particle_total,
                'observed_rate': observed / particle_total if particle_total > 0 else 0,
                'baseline_rate': baseline_rate,
                'enrichment': enrichment
            }
        return results, particle_total

    print("=" * 70)
    print("A-DIALECT: daiin TRANSITION MATRIX")
    print("=" * 70)
    a_daiin_results, a_daiin_total = bigram_analysis(a_words, 'daiin')
    print(f"daiin total transitions (A): {a_daiin_total}")
    print(f"{'Onset':<8} {'Observed':>8} {'Obs%':>7} {'Baseline%':>10} {'Enrichment':>11}")
    print("-" * 50)
    for onset_cls, _ in ONSET_CLASSES:
        r = a_daiin_results[onset_cls]
        if r['observed'] > 0 or r['baseline_rate'] > 0.01:
            print(f"{onset_cls:<8} {r['observed']:>8} {r['observed_rate']*100:>7.1f}% {r['baseline_rate']*100:>9.1f}% {r['enrichment']:>10.2f}x")

    print()
    print("A-DIALECT: OTHER PARTICLES → cth")
    print("-" * 50)
    for particle in ['aiin', 'ar', 'ol', 'chol', 'dain', 'qokeey', 'saiin']:
        results, total = bigram_analysis(a_words, particle)
        r = results['cth']
        print(f"  {particle:<10} n={total:>4}, cth: {r['observed']:>3} ({r['observed_rate']*100:.1f}%), enrichment={r['enrichment']:.2f}x")

    print()
    print("=" * 70)
    print("B-DIALECT: daiin TRANSITION MATRIX")
    print("=" * 70)
    b_daiin_results, b_daiin_total = bigram_analysis(b_words, 'daiin')
    print(f"daiin total transitions (B): {b_daiin_total}")
    print(f"{'Onset':<8} {'Observed':>8} {'Obs%':>7} {'Baseline%':>10} {'Enrichment':>11}")
    print("-" * 50)
    for onset_cls, _ in ONSET_CLASSES:
        r = b_daiin_results[onset_cls]
        if r['observed'] > 0 or r['baseline_rate'] > 0.01:
            print(f"{onset_cls:<8} {r['observed']:>8} {r['observed_rate']*100:>7.1f}% {r['baseline_rate']*100:>9.1f}% {r['enrichment']:>10.2f}x")

    print()
    print("B-DIALECT: OTHER PARTICLES → sh/ch_e")
    print("-" * 50)
    for particle in ['aiin', 'ar', 'ol', 'chol']:
        results_sh, total = bigram_analysis(b_words, particle)
        r_sh = results_sh['sh']
        r_che = results_sh['ch_e']
        print(f"  {particle:<10} n={total:>4}, sh: {r_sh['observed']:>3} ({r_sh['enrichment']:.2f}x), ch_e: {r_che['observed']:>3} ({r_che['enrichment']:.2f}x)")

    print()
    print("=" * 70)
    print("COMPARISON: A daiin→cth vs B daiin→cth")
    print("=" * 70)
    a_r = a_daiin_results['cth']
    b_r = b_daiin_results['cth']
    print(f"A daiin→cth: {a_r['observed']} ({a_r['observed_rate']*100:.1f}%), enrichment={a_r['enrichment']:.2f}x")
    print(f"B daiin→cth: {b_r['observed']} ({b_r['observed_rate']*100:.1f}%), enrichment={b_r['enrichment']:.2f}x")
    a_r_sh = a_daiin_results['sh']
    b_r_sh = b_daiin_results['sh']
    a_r_che = a_daiin_results['ch_e']
    b_r_che = b_daiin_results['ch_e']
    print(f"A daiin→sh:  {a_r_sh['observed']} ({a_r_sh['observed_rate']*100:.1f}%), enrichment={a_r_sh['enrichment']:.2f}x")
    print(f"B daiin→sh:  {b_r_sh['observed']} ({b_r_sh['observed_rate']*100:.1f}%), enrichment={b_r_sh['enrichment']:.2f}x")
    print(f"A daiin→ch_e:{a_r_che['observed']} ({a_r_che['observed_rate']*100:.1f}%), enrichment={a_r_che['enrichment']:.2f}x")
    print(f"B daiin→ch_e:{b_r_che['observed']} ({b_r_che['observed_rate']*100:.1f}%), enrichment={b_r_che['enrichment']:.2f}x")

if __name__ == '__main__':
    folio_words = parse_corpus()
    compute_transition_enrichment(folio_words)
