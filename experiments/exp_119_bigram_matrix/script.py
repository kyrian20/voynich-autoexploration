#!/usr/bin/env python3
"""
exp_119: Bigram Enrichment Matrix (H233) + D-Onset Function Word Class (H234)
H233: Word → next_onset enrichment matrix — find all pre-nominal determiners
H234: D-onset structural diversity vs other onset classes
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
                    'line_in_folio': line_in_folio,
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


def h233_bigram_matrix(records):
    print("=" * 70)
    print("H233: Bigram Enrichment Matrix — Pre-Nominal Determiners")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']
    n_total = len(body)

    # Global onset class baseline
    all_next_onset = Counter(get_onset_class(r['next_word'])
                              for r in body if r['next_word'])
    all_next_total = sum(all_next_onset.values())
    baseline = {cls: cnt/all_next_total for cls, cnt in all_next_onset.items()}

    # Get top 30 words by frequency
    word_freq = Counter(r['word'] for r in body)
    top_words = [w for w, _ in word_freq.most_common(40)]

    print(f"\n{'Word':<14} {'n':<6} {'onset':<6} {'next_onset enrichment > 1.5×'}")
    print(f"{'':14} {'':6} {'':6} {'top enrichments'}")

    onset_classes = ['ch','sh','qok','ok','ot','qo','cth','d','s','ol','other']

    enrichment_table = []

    for w in top_words:
        w_recs = [r for r in body if r['word'] == w and r['next_word']]
        if len(w_recs) < 15: continue

        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)

        enrichments = {}
        for cls in onset_classes:
            obs_rate = next_onsets.get(cls, 0) / w_total
            base_rate = baseline.get(cls, 0.001)
            enrich = obs_rate / base_rate if base_rate > 0 else 0
            enrichments[cls] = (obs_rate, base_rate, enrich)

        # Find strong enrichments (>1.5×) or depletions (<0.5×)
        strong = [(cls, e) for cls, (obs, base, e) in enrichments.items() if e > 1.5]
        strong.sort(key=lambda x: -x[1])
        strong_str = ', '.join(f"{cls}={e:.2f}×" for cls, e in strong[:4])

        enrichment_table.append((w, word_freq[w], get_onset_class(w), enrichments, strong_str))
        print(f"{w:<14} {word_freq[w]:<6} {get_onset_class(w):<6} {strong_str}")

    # Find words with strongest cth-enrichment
    print(f"\n--- Words with strongest NEXT-cth enrichment ---")
    print(f"{'Word':<14} {'n':<6} {'after-cth%':<12} {'baseline%':<12} {'enrichment'}")
    cth_enrichments = []
    for w, n, onset, enrichments, _ in enrichment_table:
        obs, base, enrich = enrichments.get('cth', (0,0.001,0))
        cth_enrichments.append((w, n, obs, base, enrich))
    for w, n, obs, base, enrich in sorted(cth_enrichments, key=lambda x: -x[4])[:15]:
        print(f"{w:<14} {n:<6} {100*obs:<12.1f} {100*base:<12.1f} {enrich:.2f}×")

    # Find words with strongest NEXT-ch enrichment
    print(f"\n--- Words with strongest NEXT-ch enrichment ---")
    print(f"{'Word':<14} {'n':<6} {'after-ch%':<12} {'baseline%':<12} {'enrichment'}")
    ch_enrichments = []
    for w, n, onset, enrichments, _ in enrichment_table:
        obs, base, enrich = enrichments.get('ch', (0,0.001,0))
        ch_enrichments.append((w, n, obs, base, enrich))
    for w, n, obs, base, enrich in sorted(ch_enrichments, key=lambda x: -x[4])[:10]:
        print(f"{w:<14} {n:<6} {100*obs:<12.1f} {100*base:<12.1f} {enrich:.2f}×")

    # Find words with strongest NEXT-qok enrichment
    print(f"\n--- Words with strongest NEXT-qok enrichment ---")
    print(f"{'Word':<14} {'n':<6} {'after-qok%':<12} {'baseline%':<12} {'enrichment'}")
    qok_enrichments = []
    for w, n, onset, enrichments, _ in enrichment_table:
        obs, base, enrich = enrichments.get('qok', (0,0.001,0))
        qok_enrichments.append((w, n, obs, base, enrich))
    for w, n, obs, base, enrich in sorted(qok_enrichments, key=lambda x: -x[4])[:10]:
        print(f"{w:<14} {n:<6} {100*obs:<12.1f} {100*base:<12.1f} {enrich:.2f}×")

    # Full enrichment table for key determiners
    print(f"\n--- Full enrichment table for top function words ---")
    function_words = ['daiin', 'aiin', 'ol', 'or', 'ar', 'dain', 'al', 'dy']
    print(f"\n{'Word':<10}", end='')
    for cls in onset_classes:
        print(f"{cls:<8}", end='')
    print()

    for w in function_words:
        w_recs = [r for r in body if r['word'] == w and r['next_word']]
        if len(w_recs) < 10:
            print(f"{w:<10} (insufficient data: {len(w_recs)} tokens)")
            continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        w_total = len(w_recs)

        print(f"{w:<10}", end='')
        for cls in onset_classes:
            obs_rate = next_onsets.get(cls, 0) / w_total
            base_rate = baseline.get(cls, 0.001)
            enrich = obs_rate / base_rate
            marker = '**' if enrich > 2.0 else ('*' if enrich > 1.5 else '  ')
            print(f"{enrich:.1f}{marker:<5}", end='')
        print()

    # Bigram entropy: how diverse are the next-word distributions?
    print(f"\n--- Bigram entropy: H(next_onset | word) for top words ---")
    print(f"{'Word':<14} {'n':<6} {'H(next_onset)':<16} {'vs baseline'}")
    baseline_H = shannon_entropy(all_next_onset)
    print(f"{'BASELINE':<14} {all_next_total:<6} {baseline_H:<16.3f}")
    for w in top_words:
        w_recs = [r for r in body if r['word'] == w and r['next_word']]
        if len(w_recs) < 20: continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs)
        H = shannon_entropy(next_onsets)
        print(f"{w:<14} {len(w_recs):<6} {H:<16.3f} {H - baseline_H:+.3f}")


def h234_d_onset_diversity(records):
    print("\n" + "=" * 70)
    print("H234: D-Onset Function Word Class Structural Diversity")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']
    n_total = len(body)

    onset_classes = ['ch','sh','qok','ok','ot','qo','cth','d','s','ol']

    # 1. Positional entropy: how uniformly distributed across positions?
    print(f"\n--- Positional entropy by onset class ---")
    print(f"(High positional entropy = appears in many different line positions)")
    print(f"{'Onset':<8} {'n':<8} {'H(position)':<14} {'first%':<10} {'last%':<10} {'mid%'}")
    for cls in onset_classes:
        cls_recs = [r for r in body if get_onset_class(r['word']) == cls]
        if len(cls_recs) < 50: continue
        pos_counts = Counter()
        for r in cls_recs:
            if r['is_line_first']: pos_counts['first'] += 1
            elif r['is_line_last']: pos_counts['last'] += 1
            else: pos_counts['mid'] += 1
        H_pos = shannon_entropy(pos_counts)
        n = len(cls_recs)
        print(f"{cls:<8} {n:<8} {H_pos:<14.4f} "
              f"{100*pos_counts['first']/n:<10.1f} "
              f"{100*pos_counts['last']/n:<10.1f} "
              f"{100*pos_counts['mid']/n:.1f}")

    # 2. Suffix entropy by onset class
    print(f"\n--- Suffix entropy by onset class ---")
    print(f"{'Onset':<8} {'n':<8} {'H(suffix)':<14} {'Top suffix':<14} {'Top%'}")
    for cls in onset_classes:
        cls_recs = [r for r in body if get_onset_class(r['word']) == cls]
        if len(cls_recs) < 50: continue
        suf_counts = Counter(get_suffix(r['word']) for r in cls_recs)
        H_suf = shannon_entropy(suf_counts)
        top_suf, top_n = suf_counts.most_common(1)[0]
        n = len(cls_recs)
        print(f"{cls:<8} {n:<8} {H_suf:<14.4f} {top_suf:<14} {100*top_n/n:.1f}%")

    # 3. Next-onset entropy by onset class (collocational diversity)
    print(f"\n--- Collocational entropy: H(next_onset) by onset class ---")
    print(f"(High entropy = appears before many different onset classes)")
    print(f"{'Onset':<8} {'n':<8} {'H(next_onset)':<16} {'Top next':<10} {'Top%'}")
    for cls in onset_classes:
        cls_recs = [r for r in body if get_onset_class(r['word']) == cls and r['next_word']]
        if len(cls_recs) < 50: continue
        next_onsets = Counter(get_onset_class(r['next_word']) for r in cls_recs)
        H_next = shannon_entropy(next_onsets)
        top_next, top_n = next_onsets.most_common(1)[0]
        n = len(cls_recs)
        print(f"{cls:<8} {n:<8} {H_next:<16.4f} {top_next:<10} {100*top_n/n:.1f}%")

    # 4. Word-level frequency distribution: does d-onset have a flatter distribution?
    print(f"\n--- Word-level frequency distribution by onset class ---")
    print(f"{'Onset':<8} {'types':<8} {'tokens':<8} {'top5%':<10} {'hapax%':<10} {'H(words)'}")
    for cls in onset_classes:
        cls_words = [r['word'] for r in body if get_onset_class(r['word']) == cls]
        if len(cls_words) < 50: continue
        word_counts = Counter(cls_words)
        n = len(cls_words)
        types = len(word_counts)
        hapax = sum(1 for _, c in word_counts.items() if c == 1)
        top5 = sum(c for _, c in word_counts.most_common(5))
        H_words = shannon_entropy(word_counts)
        print(f"{cls:<8} {types:<8} {n:<8} {100*top5/n:<10.1f} {100*hapax/types:<10.1f} {H_words:.3f}")

    # 5. Positional profiles for ALL d-onset words (top 15)
    print(f"\n--- Individual d-onset word positional profiles ---")
    d_recs = [r for r in body if get_onset_class(r['word']) == 'd']
    d_word_freq = Counter(r['word'] for r in d_recs)
    print(f"\n{'Word':<14} {'n':<6} {'first%':<10} {'last%':<10} {'mid%':<10} {'suffix':<10} {'next-onset enrichment'}")
    for w, cnt in d_word_freq.most_common(15):
        w_recs = [r for r in d_recs if r['word'] == w]
        first_n = sum(1 for r in w_recs if r['is_line_first'])
        last_n = sum(1 for r in w_recs if r['is_line_last'])
        mid_n = cnt - first_n - last_n
        suf = get_suffix(w)

        # Next onset enrichment
        next_onsets = Counter(get_onset_class(r['next_word']) for r in w_recs if r['next_word'])
        n_next = sum(next_onsets.values())
        if n_next > 5:
            # Find top enriched next onset vs baseline
            all_next = Counter(get_onset_class(r['next_word']) for r in body if r['next_word'])
            all_next_n = sum(all_next.values())
            top_enrich = max(next_onsets.keys(),
                             key=lambda cls: (next_onsets.get(cls,0)/n_next) / (all_next.get(cls,1)/all_next_n))
            top_rate = next_onsets.get(top_enrich,0)/n_next
            base_rate = all_next.get(top_enrich,1)/all_next_n
            enrich = top_rate/base_rate
            enrich_str = f"{top_enrich}={enrich:.1f}×"
        else:
            enrich_str = '—'

        print(f"{w:<14} {cnt:<6} {100*first_n/cnt:<10.1f} {100*last_n/cnt:<10.1f} "
              f"{100*mid_n/cnt:<10.1f} {suf:<10} {enrich_str}")

    # 6. Key comparison: d-onset vs ch-onset positional diversity
    print(f"\n--- Positional diversity comparison: d vs ch onset ---")
    for cls in ['d', 'ch', 'sh', 'qok']:
        cls_recs = [r for r in body if get_onset_class(r['word']) == cls]
        cls_words_top = Counter(r['word'] for r in cls_recs).most_common(10)
        print(f"\n  Top 10 {cls}-onset words:")
        print(f"  {'Word':<14} {'n':<6} {'first%':<10} {'last%':<10} {'Role inferred'}")
        for w, cnt in cls_words_top:
            w_recs = [r for r in cls_recs if r['word'] == w]
            first_n = sum(1 for r in w_recs if r['is_line_first'])
            last_n = sum(1 for r in w_recs if r['is_line_last'])
            first_pct = 100*first_n/cnt
            last_pct = 100*last_n/cnt
            role = 'topic' if first_pct > 40 else ('closer' if last_pct > 40 else ('balanced' if (first_pct > 18 and last_pct > 18) else 'mid-content'))
            print(f"  {w:<14} {cnt:<6} {first_pct:<10.1f} {last_pct:<10.1f} {role}")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")

    h233_bigram_matrix(records)
    h234_d_onset_diversity(records)


if __name__ == '__main__':
    main()
