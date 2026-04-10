#!/usr/bin/env python3
"""
exp_143: cthor→ot bigram analysis (H283) and cth-runs in A-herbal (H284)
"""

import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58):    SECTION_MAP[f] = 'herbal'
for f in range(67, 74):   SECTION_MAP[f] = 'astro'
for f in range(75, 85):   SECTION_MAP[f] = 'cosmo'
for f in range(87, 103):  SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'

ONSET_CLASSES = {
    "qok": re.compile(r'^qok'),
    "qot": re.compile(r'^qot'),
    "qo":  re.compile(r'^qo(?![kt])'),
    "cth": re.compile(r'^cth'),
    "ch":  re.compile(r'^ch(?!e)'),
    "ch_e":re.compile(r'^che'),
    "sh":  re.compile(r'^sh'),
    "ok":  re.compile(r'^ok'),
    "ot":  re.compile(r'^ot'),
    "ol":  re.compile(r'^ol'),
    "d":   re.compile(r'^d'),
    "s":   re.compile(r'^s'),
    "y":   re.compile(r'^y'),
    "k":   re.compile(r'^k'),
    "t":   re.compile(r'^t'),
    "l":   re.compile(r'^l'),
    "r":   re.compile(r'^r'),
    "p":   re.compile(r'^p'),
    "f":   re.compile(r'^f'),
}


def get_onset(word):
    for name, pat in ONSET_CLASSES.items():
        if pat.match(word):
            return name
    return 'other'


def parse_corpus():
    lines = []
    with open(CORPUS, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text = m.group(1), m.group(2).strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_str = parts[0]
            locus_type_raw = parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue
            folio_base = folio_str.split('.')[0]
            m2 = re.match(r'f(\d+)', folio_base)
            if not m2:
                continue
            folio_num = int(m2.group(1))
            section = SECTION_MAP.get(folio_num)
            if section is None:
                continue
            words = [w for w in text.split('.') if re.match(r'[a-z]', w)]
            if not words:
                continue
            lines.append({'folio_base': folio_base, 'folio_num': folio_num,
                          'section': section, 'words': words})
    return lines


def get_folio_dialect(lines):
    folio_counts = defaultdict(lambda: {'edy': 0, 'eedy': 0, 'total': 0})
    for rec in lines:
        fb = rec['folio_base']
        for w in rec['words']:
            folio_counts[fb]['total'] += 1
            if w.endswith('eedy'): folio_counts[fb]['eedy'] += 1
            elif w.endswith('edy'): folio_counts[fb]['edy'] += 1
    dialect = {}
    for fb, cnts in folio_counts.items():
        if cnts['total'] < 10:
            dialect[fb] = 'unknown'
        else:
            rate = (cnts['edy'] + cnts['eedy']) / cnts['total']
            dialect[fb] = 'B' if rate >= 0.05 else 'A'
    return dialect


def analyze_cthor_ot(lines, folio_dialect):
    """H283: cthor->ot specific bigrams and folio distribution."""
    print("="*60)
    print("H283: cthor→ot BIGRAM ANALYSIS")
    print("="*60)

    cthor_ot_bigrams = Counter()       # specific "cthor"+"ot-word" pairs
    cthor_ot_folio = defaultdict(list) # folio -> list of ot-words following cthor
    cthor_midot_context = []           # (folio_num, line_context) for cthor→ot cases

    for rec in lines:
        fb = rec['folio_base']
        fn = rec['folio_num']
        d = folio_dialect.get(fb, 'unknown')
        if d != 'A' or rec['section'] != 'herbal':
            continue
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w == 'cthor' and i < n-1:
                nxt = words[i+1]
                if get_onset(nxt) == 'ot':
                    bigram = f"cthor+{nxt}"
                    cthor_ot_bigrams[bigram] += 1
                    cthor_ot_folio[fn].append(nxt)
                    cthor_midot_context.append((fn, fb, words[max(0,i-1):i+3]))

    print(f"\nTotal cthor→ot bigrams: {sum(cthor_ot_bigrams.values())}")
    print(f"\n--- Top cthor→ot bigrams ---")
    for bigram, n in cthor_ot_bigrams.most_common():
        print(f"  {bigram}: {n}")

    print(f"\n--- cthor→ot by folio ---")
    for fn in sorted(cthor_ot_folio.keys()):
        ot_words = cthor_ot_folio[fn]
        print(f"  f{fn}: {', '.join(ot_words)}")

    print(f"\n--- Context examples (word before, cthor, ot-word, word after) ---")
    for fn, fb, ctx in cthor_midot_context[:15]:
        print(f"  f{fn}: {' '.join(ctx)}")

    # Also count cthor not followed by ot, for comparison
    cthor_total = 0
    cthor_ot_count = 0
    cthor_after_all = Counter()
    for rec in lines:
        fb = rec['folio_base']
        if folio_dialect.get(fb) != 'A' or rec['section'] != 'herbal':
            continue
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w == 'cthor':
                cthor_total += 1
                if i < n-1:
                    nxt_onset = get_onset(words[i+1])
                    cthor_after_all[nxt_onset] += 1
                    if nxt_onset == 'ot':
                        cthor_ot_count += 1

    print(f"\ncthor total (A-herbal): {cthor_total}")
    print(f"cthor followed by ot: {cthor_ot_count} ({cthor_ot_count/cthor_total:.1%})")
    print(f"\n--- What follows cthor (A-herbal) ---")
    t = sum(cthor_after_all.values())
    for onset, c in cthor_after_all.most_common():
        print(f"  {onset}: {c} ({c/t:.1%})")


def analyze_cth_runs(lines, folio_dialect):
    """H284: cth-runs (2+ consecutive cth-words) in A-herbal."""
    print("\n" + "="*60)
    print("H284: cth-RUNS IN A-HERBAL")
    print("="*60)

    cth_bigrams = Counter()    # consecutive cth-word pairs
    cth_trigrams = Counter()   # consecutive cth-word triples
    run_lengths = Counter()    # distribution of run lengths
    folio_run_count = defaultdict(int)  # folio -> number of cth-runs
    run_examples = []

    for rec in lines:
        fb = rec['folio_base']
        fn = rec['folio_num']
        d = folio_dialect.get(fb, 'unknown')
        if d != 'A' or rec['section'] != 'herbal':
            continue
        words = rec['words']
        n = len(words)

        # Find cth-onset word positions
        cth_positions = [i for i, w in enumerate(words) if get_onset(w) == 'cth']

        # Find runs of consecutive cth-words (consecutive positions in the word list)
        if not cth_positions:
            continue
        # Group consecutive positions
        runs = []
        run = [cth_positions[0]]
        for pos in cth_positions[1:]:
            if pos == run[-1] + 1:
                run.append(pos)
            else:
                runs.append(run)
                run = [pos]
        runs.append(run)

        for run in runs:
            run_lengths[len(run)] += 1
            if len(run) >= 2:
                folio_run_count[fn] += 1
                run_words = [words[i] for i in run]
                for j in range(len(run_words)-1):
                    cth_bigrams[f"{run_words[j]}+{run_words[j+1]}"] += 1
                if len(run_words) >= 3:
                    for j in range(len(run_words)-2):
                        cth_trigrams[f"{run_words[j]}+{run_words[j+1]}+{run_words[j+2]}"] += 1
                if len(run_examples) < 10:
                    run_examples.append((fn, fb, run_words, words[max(0,run[0]-1):run[-1]+2]))

    # Also check for "near-consecutive" cth-words (separated by 1 non-cth word)
    near_cth_pairs = Counter()
    for rec in lines:
        fb = rec['folio_base']
        fn = rec['folio_num']
        if folio_dialect.get(fb) != 'A' or rec['section'] != 'herbal':
            continue
        words = rec['words']
        n = len(words)
        for i in range(n-2):
            if get_onset(words[i]) == 'cth' and get_onset(words[i+2]) == 'cth':
                if get_onset(words[i+1]) != 'cth':
                    pair = f"{words[i]}+[{get_onset(words[i+1])}]+{words[i+2]}"
                    near_cth_pairs[pair] += 1

    print(f"\n--- cth-run length distribution (A-herbal) ---")
    total_runs = sum(run_lengths.values())
    for length in sorted(run_lengths.keys()):
        n = run_lengths[length]
        print(f"  Length {length}: {n} runs ({n/total_runs:.1%})")

    print(f"\nRuns of 2+ cth-words: {sum(run_lengths[l] for l in run_lengths if l >= 2)}")

    print(f"\n--- Top cth-bigrams (consecutive pairs) ---")
    for bigram, n in cth_bigrams.most_common(15):
        print(f"  {bigram}: {n}")

    if cth_trigrams:
        print(f"\n--- Top cth-trigrams ---")
        for trigram, n in cth_trigrams.most_common(5):
            print(f"  {trigram}: {n}")

    print(f"\n--- Folios with most cth-runs (2+) ---")
    top_folios = sorted(folio_run_count.items(), key=lambda x: -x[1])[:10]
    for fn, count in top_folios:
        print(f"  f{fn}: {count} runs")

    print(f"\n--- Example cth-runs (word_before, run_words..., word_after) ---")
    for fn, fb, run_words, context in run_examples[:8]:
        print(f"  f{fn}: {' '.join(context)} [run: {' '.join(run_words)}]")

    print(f"\n--- Near-consecutive cth-pairs (separated by 1 non-cth word) ---")
    print(f"Total near-pairs: {sum(near_cth_pairs.values())}")
    for pair, n in near_cth_pairs.most_common(10):
        print(f"  {pair}: {n}")


if __name__ == '__main__':
    print("Loading corpus...")
    lines = parse_corpus()
    print(f"Loaded {len(lines)} lines")
    folio_dialect = get_folio_dialect(lines)
    analyze_cthor_ot(lines, folio_dialect)
    analyze_cth_runs(lines, folio_dialect)
