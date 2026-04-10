#!/usr/bin/env python3
"""
exp_120: Dialect-Specific Bigram Rules (H236) + otaiin Demonstrative (H237)
H236: Do A-suffix→cth and B-suffix→qok patterns intensify when restricted to dialect?
H237: Is [onset-aiin]→[same-onset] a general pattern? otaiin→ot=4.27×?
"""

import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58): SECTION_MAP[f] = 'herbal'
for f in range(67, 74): SECTION_MAP[f] = 'astro'
for f in range(75, 85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'


def get_suffix(word):
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_onset_class(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('olk'): return 'olk'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    return 'other'


def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)


def parse_eva(path):
    edy_counts = defaultdict(int)
    total_counts = defaultdict(int)
    records = []

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or not line.startswith('<'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m: continue
            locus_code = m.group(1)
            text = m.group(2).strip()

            comma_idx = locus_code.find(',')
            if comma_idx < 0: continue
            folio_line = locus_code[:comma_idx]
            locus_type = locus_code[comma_idx+1:]

            fm = re.match(r'f(\d+)', folio_line)
            if not fm: continue
            folio_num = int(fm.group(1))

            lm = re.match(r'f\w+\.(\d+)', folio_line)
            line_in_folio = int(lm.group(1)) if lm else 0

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            if not is_body: continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            n = len(words)
            for i, w in enumerate(words):
                for suf_check in ['edy', 'eedy']:
                    if w.endswith(suf_check):
                        edy_counts[folio_num] += 1
                total_counts[folio_num] += 1
                records.append({
                    'word': w, 'folio': folio_num,
                    'pos_in_line': i,
                    'n_in_line': n,
                    'is_line_first': (i == 0),
                    'is_line_last': (i == n-1),
                    'prev_word': words[i-1] if i > 0 else None,
                    'next_word': words[i+1] if i < n-1 else None,
                    'section': SECTION_MAP.get(folio_num, 'other'),
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def bigram_enrichment(recs, word, target_onset):
    """Compute enrichment of target_onset as next-onset after word."""
    w_recs = [r for r in recs if r['word'] == word and r['next_word']]
    if not w_recs: return 0, 0, 0
    next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
    w_total = len(w_recs)
    obs_rate = next_onsets.get(target_onset, 0) / w_total

    all_next = Counter(get_onset_class(r['next_word']) for r in recs if r['next_word'])
    all_total = sum(all_next.values())
    base_rate = all_next.get(target_onset, 1) / all_total

    enrich = obs_rate / base_rate if base_rate > 0 else 0
    return obs_rate, base_rate, enrich


def h236_dialect_bigram(records):
    print("=" * 70)
    print("H236: Dialect-Specific Bigram Rules")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']
    a_body = [r for r in body if r['dialect'] == 'A']
    b_body = [r for r in body if r['dialect'] == 'B']

    print(f"\nTotal body: {len(body)}, A-dialect: {len(a_body)}, B-dialect: {len(b_body)}")

    # === Test 1: Pre-cth words in A vs B ===
    print(f"\n--- Test 1: Pre-cth enrichment in A-dialect vs B-dialect vs mixed ---")
    pre_cth_words = ['chor', 'daiin', 'chol', 'shol', 'okaiin', 'chy', 'sho', 'dain']

    print(f"\n{'Word':<14} {'mixed_enr':<14} {'A_enr':<14} {'B_enr':<14} {'A/B ratio'}")
    for w in pre_cth_words:
        _, _, mixed_enr = bigram_enrichment(body, w, 'cth')
        _, _, a_enr = bigram_enrichment(a_body, w, 'cth')
        _, _, b_enr = bigram_enrichment(b_body, w, 'cth')
        ab_ratio = a_enr / b_enr if b_enr > 0.01 else float('inf')
        print(f"{w:<14} {mixed_enr:<14.2f} {a_enr:<14.2f} {b_enr:<14.2f} {ab_ratio:.2f}×")

    # === Test 2: Pre-qok words in A vs B ===
    print(f"\n--- Test 2: Pre-qok enrichment in A-dialect vs B-dialect vs mixed ---")
    pre_qok_words = ['shedy', 'shey', 'chedy', 'qokeedy', 'qokeey', 'cheey']

    print(f"\n{'Word':<14} {'mixed_enr':<14} {'A_enr':<14} {'B_enr':<14} {'B/A ratio'}")
    for w in pre_qok_words:
        _, _, mixed_enr = bigram_enrichment(body, w, 'qok')
        _, _, a_enr = bigram_enrichment(a_body, w, 'qok')
        _, _, b_enr = bigram_enrichment(b_body, w, 'qok')
        ba_ratio = b_enr / a_enr if a_enr > 0.01 else float('inf')
        print(f"{w:<14} {mixed_enr:<14.2f} {a_enr:<14.2f} {b_enr:<14.2f} {ba_ratio:.2f}×")

    # === Test 3: Section-level bigram analysis ===
    print(f"\n--- Test 3: Pre-cth enrichment by SECTION ---")
    sections = ['herbal','cosmo','stars','pharma','astro']
    pre_cth_probe = ['daiin', 'chol', 'chor']

    print(f"\n{'Word':<12}", end='')
    for s in sections:
        print(f"{s:<12}", end='')
    print()

    for w in pre_cth_probe:
        print(f"{w:<12}", end='')
        for s in sections:
            s_recs = [r for r in body if r['section'] == s]
            w_recs = [r for r in s_recs if r['word'] == w and r['next_word']]
            if not w_recs:
                print(f"{'—':<12}", end='')
                continue
            next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
            w_total = len(w_recs)
            obs = next_onsets.get('cth', 0) / w_total
            all_next = Counter(get_onset_class(r['next_word']) for r in s_recs if r['next_word'])
            all_total = sum(all_next.values())
            base = all_next.get('cth', 1) / all_total
            enrich = obs / base if base > 0 else 0
            print(f"{enrich:<12.1f}", end='')
        print()

    # === Test 4: What precedes qok in B-dialect vs A-dialect? ===
    print(f"\n--- Test 4: What MOST OFTEN precedes qok in B vs A dialect? ---")
    for dialect, d_recs in [('A', a_body), ('B', b_body)]:
        qok_recs = [r for r in d_recs if r['next_word'] and get_onset_class(r['next_word']) == 'qok']
        if not qok_recs: continue
        prev_words = Counter(r['word'] for r in qok_recs)
        prev_onset = Counter(get_onset_class(r['word']) for r in qok_recs)
        all_onset_next = Counter(get_onset_class(r['next_word']) for r in d_recs if r['next_word'])
        qok_baseline = all_onset_next.get('qok', 1) / sum(all_onset_next.values())
        print(f"\n  {dialect}-dialect top words before qok-onset ({len(qok_recs)} total):")
        for w, cnt in prev_words.most_common(10):
            pct = 100*cnt/len(qok_recs)
            print(f"    {w}: {cnt} ({pct:.1f}%)")

    # === Test 5: What is the baseline cth-rate by dialect? ===
    print(f"\n--- Test 5: cth-onset token rate by dialect and section ---")
    for dialect, d_recs in [('A', a_body), ('B', b_body)]:
        cth_n = sum(1 for r in d_recs if get_onset_class(r['word']) == 'cth')
        n = len(d_recs)
        print(f"\n  {dialect}-dialect: cth-onset = {cth_n}/{n} = {1000*cth_n/n:.2f}‰")
        for s in sections:
            s_recs = [r for r in d_recs if r['section'] == s]
            if not s_recs: continue
            cth_s = sum(1 for r in s_recs if get_onset_class(r['word']) == 'cth')
            print(f"    {s}: {cth_s}/{len(s_recs)} = {1000*cth_s/len(s_recs):.2f}‰")

    # === Test 6: A-dialect bigram enrichment (A only) full table ===
    print(f"\n--- Test 6: A-dialect specific bigram enrichments ---")
    # Baseline
    a_next_onset = Counter(get_onset_class(r['next_word']) for r in a_body if r['next_word'])
    a_total_next = sum(a_next_onset.values())
    a_baseline = {cls: cnt/a_total_next for cls, cnt in a_next_onset.items()}

    top_a_words = [(w, c) for w, c in Counter(r['word'] for r in a_body).most_common(25)]
    print(f"\n{'Word':<14} {'n':<6} {'->cth enr':<12} {'->ch enr':<12} {'->sh enr':<12} {'->d enr'}")
    for w, cnt in top_a_words:
        if cnt < 15: continue
        w_recs = [r for r in a_body if r['word'] == w and r['next_word']]
        if len(w_recs) < 10: continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)
        cth_enr = (next_onsets.get('cth',0)/w_total) / max(0.001, a_baseline.get('cth',0.001))
        ch_enr = (next_onsets.get('ch',0)/w_total) / max(0.001, a_baseline.get('ch',0.001))
        sh_enr = (next_onsets.get('sh',0)/w_total) / max(0.001, a_baseline.get('sh',0.001))
        d_enr = (next_onsets.get('d',0)/w_total) / max(0.001, a_baseline.get('d',0.001))
        print(f"{w:<14} {cnt:<6} {cth_enr:<12.2f} {ch_enr:<12.2f} {sh_enr:<12.2f} {d_enr:.2f}")


def h237_aiin_demonstrative(records):
    print("\n" + "=" * 70)
    print("H237: -aiin as Cross-Referential Demonstrative Pattern")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']

    # Global baseline
    all_next_onset = Counter(get_onset_class(r['next_word']) for r in body if r['next_word'])
    all_next_total = sum(all_next_onset.values())

    # Test: [onset-aiin] → [same onset] enrichment
    # Pairs to test
    aiin_words = {
        'okaiin': 'ok',
        'qokaiin': 'qok',
        'daiin': 'd',
        'otaiin': 'ot',
        'chaiin': 'ch',
        'shaiin': 'sh',
        'aiin': None,  # standalone - what does it precede?
    }

    print(f"\n--- [onset-aiin] → [same onset] enrichment ---")
    print(f"(Testing: does 'X-aiin' word preferentially precede X-onset words?)")
    print(f"\n{'Word':<14} {'n':<6} {'target_onset':<14} {'same_onset_enr':<16} {'top_next_onset':<16} {'top_enr'}")

    for word, target_onset in sorted(aiin_words.items()):
        w_recs = [r for r in body if r['word'] == word and r['next_word']]
        if len(w_recs) < 5:
            print(f"{word:<14} {len(w_recs):<6} (insufficient data)")
            continue

        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)

        # Same-onset enrichment
        if target_onset:
            same_obs = next_onsets.get(target_onset, 0) / w_total
            same_base = all_next_onset.get(target_onset, 1) / all_next_total
            same_enr = same_obs / same_base if same_base > 0 else 0
        else:
            same_enr = float('nan')
            target_onset = '—'

        # Top next onset
        top_next, top_n = next_onsets.most_common(1)[0]
        top_obs = top_n / w_total
        top_base = all_next_onset.get(top_next, 1) / all_next_total
        top_enr = top_obs / top_base if top_base > 0 else 0

        print(f"{word:<14} {len(w_recs):<6} {target_onset:<14} {same_enr:<16.2f} "
              f"{top_next}={top_enr:.2f}×")

    # Full next-onset enrichment for each aiin-suffix word
    print(f"\n--- Detailed enrichment table for aiin-suffix words ---")
    target_classes = ['ch','sh','qok','ok','ot','cth','d','s','qo']
    print(f"\n{'Word':<14}", end='')
    for cls in target_classes:
        print(f"{cls:<8}", end='')
    print()

    for word in ['okaiin', 'qokaiin', 'daiin', 'otaiin', 'aiin']:
        w_recs = [r for r in body if r['word'] == word and r['next_word']]
        if len(w_recs) < 10:
            print(f"{word:<14} (n={len(w_recs)})")
            continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)
        print(f"{word:<14}", end='')
        for cls in target_classes:
            obs = next_onsets.get(cls, 0) / w_total
            base = all_next_onset.get(cls, 1) / all_next_total
            enrich = obs / base if base > 0 else 0
            mark = '**' if enrich > 2.0 else ('*' if enrich > 1.5 else '  ')
            print(f"{enrich:.1f}{mark:<4}", end='')
        print()

    # otaiin characterization (full)
    print(f"\n--- otaiin characterization ---")
    otaiin_recs = [r for r in body if r['word'] == 'otaiin']
    print(f"\notaiin tokens: {len(otaiin_recs)}")

    if otaiin_recs:
        # Position
        first_n = sum(1 for r in otaiin_recs if r['is_line_first'])
        last_n = sum(1 for r in otaiin_recs if r['is_line_last'])
        mid_n = len(otaiin_recs) - first_n - last_n
        print(f"Positional: first={100*first_n/len(otaiin_recs):.1f}%, last={100*last_n/len(otaiin_recs):.1f}%, mid={100*mid_n/len(otaiin_recs):.1f}%")

        # Section
        section_dist = Counter(r['section'] for r in otaiin_recs)
        all_section = Counter(r['section'] for r in body)
        print(f"Section distribution:")
        for s in ['herbal','cosmo','stars','pharma','astro']:
            n_s = section_dist.get(s, 0)
            total_s = all_section.get(s, 0)
            print(f"  {s}: {n_s} ({1000*n_s/max(1,total_s):.2f}‰)")

        # Dialect
        d_dist = Counter(r['dialect'] for r in otaiin_recs)
        total_a = sum(1 for r in body if r['dialect'] == 'A')
        total_b = sum(1 for r in body if r['dialect'] == 'B')
        print(f"Dialect: A={d_dist.get('A',0)} ({1000*d_dist.get('A',0)/total_a:.2f}‰), "
              f"B={d_dist.get('B',0)} ({1000*d_dist.get('B',0)/total_b:.2f}‰)")

        # Bigrams
        next_w = [r['next_word'] for r in otaiin_recs if r['next_word']]
        print(f"\nWords after otaiin (top 10):")
        for w, c in Counter(next_w).most_common(10):
            print(f"  {w}: {c} (onset={get_onset_class(w)})")

        prev_w = [r['prev_word'] for r in otaiin_recs if r['prev_word']]
        print(f"\nWords before otaiin (top 10):")
        for w, c in Counter(prev_w).most_common(10):
            print(f"  {w}: {c} (onset={get_onset_class(w)})")

    # Test the general pattern: for EACH major onset class, does the
    # [onset-aiin] word preferentially precede [same onset] more than other aiin words?
    print(f"\n--- Generalized: onset_aiin_words → same_onset (does pattern generalize?) ---")
    test_pairs = [
        ('okaiin', 'ok'), ('qokaiin', 'qok'), ('daiin', 'd'),
        ('otaiin', 'ot'), ('aiin', None), ('dain', 'd'),
        ('chol', 'ch'), ('shol', 'sh'), ('chor', 'cth'),
    ]

    print(f"\n{'Word':<14} {'n':<6} {'target':<8} {'obs%':<8} {'base%':<8} {'enrich'}")
    for word, target in test_pairs:
        w_recs = [r for r in body if r['word'] == word and r['next_word']]
        if not w_recs or not target:
            continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)
        obs = next_onsets.get(target, 0) / w_total
        base = all_next_onset.get(target, 1) / all_next_total
        enrich = obs / base if base > 0 else 0
        print(f"{word:<14} {len(w_recs):<6} {target:<8} {100*obs:<8.1f} {100*base:<8.1f} {enrich:.2f}×")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")

    h236_dialect_bigram(records)
    h237_aiin_demonstrative(records)


if __name__ == '__main__':
    main()
