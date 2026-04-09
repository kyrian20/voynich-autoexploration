"""
exp_084: B ol-Prefix Word Class (H136), A she- Para-Start Specificity (H137),
         daiin Hierarchical Boundary Analysis (H138)

H136: Do B ol-prefix words (olfchedy, olkey, oly, olkam) serve a dual role:
      para-start markers (some) AND within-para line-final markers (others)?
H137: Are she-prefix sh-forms MORE enriched at A para-starts than plain sh-forms?
H138: Is daiin rate monotonically increasing from para-start to para-final in A?
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

AIIN_DOM_FOLIOS = {
    'f1r','f1v','f2r','f2v','f3r','f3v','f4r','f4v','f5r','f5v',
    'f6r','f6v','f7r','f7v','f8r','f8v','f13r','f13v','f14r','f14v',
    'f15r','f15v','f16r','f16v'
}

def folio_base(folio):
    return folio.split('.')[0]

def onset_class(word):
    if word.startswith('qo'):  return 'qo'
    if word.startswith('ch'):  return 'ch'
    if word.startswith('sh'):  return 'sh'
    if word.startswith('p'):   return 'p'
    if word.startswith('t') and not word.startswith('th'): return 't'
    if word.startswith('k'):   return 'k'
    if word.startswith('d'):   return 'd'
    if word.startswith('s'):   return 's'
    if word.startswith('y'):   return 'y'
    if word.startswith('o'):   return 'o'
    return 'other'

KNOWN_SUFFIXES = [
    'eedy','edy','eey','ain','aiin','ol','or','ey','dy','am','al','y'
]

def get_suffix(word):
    for suf in KNOWN_SUFFIXES:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def parse_voynich(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            text = line[m.end():].strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_raw = parts[0]
            locus_code = parts[1]
            folio = folio_raw.lstrip('+*=&~')
            is_para_start = locus_code.lstrip('+*=/~&').startswith('@')
            is_body = locus_code.lstrip('+*@=/~&').startswith('P')
            if not is_body:
                continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            records.append({
                'folio': folio,
                'folio_base': folio_base(folio),
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start,
            })
    return records

def assign_dialect(recs):
    folio_words = defaultdict(list)
    for r in recs:
        for w in r['words']:
            folio_words[r['folio_base']].append(w)

    b_folios = set()
    for folio, ws in folio_words.items():
        edy_count = sum(1 for w in ws if w.endswith('edy') or w.endswith('eedy'))
        if edy_count / max(len(ws), 1) >= 0.05:
            b_folios.add(folio)

    a_recs, b_recs = [], []
    for r in recs:
        if r['folio_base'] in b_folios:
            b_recs.append(r)
        else:
            a_recs.append(r)
    return a_recs, b_recs

def classify_para_boundary(recs):
    result = []
    n = len(recs)
    for i, r in enumerate(recs):
        is_pf = (i + 1 >= n) or recs[i + 1]['is_para_start']
        result.append((r, is_pf))
    return result

def group_into_paragraphs(recs):
    paragraphs = []
    current_para = []
    for r in recs:
        if r['is_para_start'] and current_para:
            paragraphs.append(current_para)
            current_para = [r]
        elif r['is_para_start']:
            current_para = [r]
        else:
            current_para.append(r)
    if current_para:
        paragraphs.append(current_para)
    return paragraphs


# ============================================================
# H136: B ol-Prefix Word Class
# ============================================================

def h136_ol_prefix_class(b_recs):
    print("\n=== H136: B ol-Prefix Word Class ===")

    labeled = classify_para_boundary(b_recs)

    # All words and their positions
    total_words = 0
    total_lines = len(labeled)
    para_starts = sum(1 for r, _ in labeled if r['is_para_start'])
    para_finals = sum(1 for _, is_pf in labeled if is_pf)

    # Collect positional stats for each word
    word_stats = defaultdict(lambda: {
        'total': 0,
        'line_first': 0,
        'line_last': 0,
        'para_start_first': 0,  # first word of para-start line
        'para_final_last': 0,    # last word of para-final line
    })

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        for w in ws:
            word_stats[w]['total'] += 1
            total_words += 1
        word_stats[ws[0]]['line_first'] += 1
        word_stats[ws[-1]]['line_last'] += 1
        if r['is_para_start']:
            word_stats[ws[0]]['para_start_first'] += 1
        if is_pf:
            word_stats[ws[-1]]['para_final_last'] += 1

    # Extract all ol-prefix words
    ol_words = [(w, stats) for w, stats in word_stats.items() if w.startswith('ol') and len(w) > 2]
    ol_words.sort(key=lambda x: -x[1]['total'])

    print(f"\nTotal B lines: {total_lines}, para-starts: {para_starts}, para-finals: {para_finals}")
    print(f"Total B words (tokens): {total_words}")

    # Base rates
    line_first_base = total_lines / total_words
    line_last_base = total_lines / total_words
    ps_first_base = para_starts / total_words
    pf_last_base = para_finals / total_words

    print(f"\nBase rates: line-first={1/total_lines*total_lines/total_words:.3f}, para-start-first={para_starts/total_words:.4f}")

    print(f"\n--- B ol-prefix words: positional statistics ---")
    print(f"{'Word':<15} {'Total':>5} {'LFirst%':>8} {'LLast%':>8} {'PSFirst%':>9} {'PFLast%':>8}")
    for w, stats in ol_words[:25]:
        tot = stats['total']
        if tot < 3:
            continue
        lf_r = stats['line_first'] / tot
        ll_r = stats['line_last'] / tot
        ps_r = stats['para_start_first'] / tot
        pf_r = stats['para_final_last'] / tot
        print(f"  {w:<13} {tot:>5} {lf_r:>7.1%} {ll_r:>7.1%} {ps_r:>8.1%} {pf_r:>7.1%}")

    # Compare ol-prefix sub-classes:
    # Group 1: oly, oldy, olkam, olkedy — known line-closers
    # Group 2: olfchedy, olkey — known para-starters
    # Group 3: others
    LINE_CLOSERS = {'oly', 'oldy', 'olkam', 'olkedy', 'olchedy', 'olky'}
    PARA_STARTERS = {'olfchedy', 'olkey', 'olkal', 'olkaiin', 'olkain'}

    print(f"\n--- ol-prefix sub-class positional roles ---")
    def group_stats(group_name, words_set):
        g_total = sum(word_stats[w]['total'] for w in words_set)
        g_ll = sum(word_stats[w]['line_last'] for w in words_set)
        g_ps = sum(word_stats[w]['para_start_first'] for w in words_set)
        g_pf = sum(word_stats[w]['para_final_last'] for w in words_set)
        print(f"\n  {group_name} (total={g_total}):")
        print(f"    line-last%: {g_ll/max(g_total,1):.1%}")
        print(f"    para-start first%: {g_ps/max(g_total,1):.1%}")
        print(f"    para-final last%: {g_pf/max(g_total,1):.1%}")

    # All ol-prefix combined
    all_ol_words = {w for w, _ in ol_words}
    group_stats("All ol-prefix", all_ol_words)
    group_stats("ol-line-closers (oly/oldy/olkam)", LINE_CLOSERS & all_ol_words)
    group_stats("ol-other (not line-closers)", all_ol_words - LINE_CLOSERS)

    # Non-ol o-onset words
    non_ol_o_words = {w for w in word_stats if w.startswith('o') and not w.startswith('ol') and len(w) > 2}
    group_stats("Non-ol o-onset words", non_ol_o_words)


# ============================================================
# H137: A she- vs sh-other Para-Start Enrichment
# ============================================================

def h137_she_para_start(a_recs):
    print("\n=== H137: A she- vs sh-other Para-Start Enrichment ===")

    labeled = classify_para_boundary(a_recs)

    total_lines = len(labeled)
    para_starts = sum(1 for r, _ in labeled if r['is_para_start'])
    para_finals = sum(1 for _, is_pf in labeled if is_pf)

    # Collect for she-words, sh-other-words, che-words, ch-other-words
    groups = {
        'she-': {'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0},
        'sh-other': {'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0},
        'che-': {'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0},
        'ch-other': {'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0},
        'daiin': {'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0},
    }

    def word_group(w):
        if w == 'daiin':
            return 'daiin'
        if w.startswith('she') and len(w) > 3:
            return 'she-'
        if w.startswith('sh') and len(w) > 2:
            return 'sh-other'
        if w.startswith('che') and len(w) > 3:
            return 'che-'
        if w.startswith('ch') and len(w) > 2:
            return 'ch-other'
        return None

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        for w in ws:
            g = word_group(w)
            if g:
                groups[g]['total'] += 1

        # First word of line
        g = word_group(ws[0])
        if g:
            groups[g]['line_first'] += 1
            if r['is_para_start']:
                groups[g]['ps_first'] += 1

        # Last word of line
        g = word_group(ws[-1])
        if g:
            groups[g]['line_last'] += 1
            if is_pf:
                groups[g]['pf_last'] += 1

    total_words = sum(g['total'] for g in groups.values())

    print(f"\nA lines: {total_lines}, para-starts: {para_starts}, para-finals: {para_finals}")
    print(f"\n--- Positional rates by word group ---")
    print(f"{'Group':<12} {'Total':>5} {'LFirst%':>8} {'LLast%':>8} {'PSFirst%':>9} {'PFLast%':>8} {'PSEnr':>7}")
    for gname, stats in groups.items():
        tot = stats['total']
        if tot == 0:
            continue
        lf_r = stats['line_first'] / tot
        ll_r = stats['line_last'] / tot
        ps_r = stats['ps_first'] / tot
        pf_r = stats['pf_last'] / tot
        # Para-start first enrichment vs base
        ps_base = para_starts / total_lines
        ps_enr = (stats['ps_first'] / max(stats['line_first'], 1)) / max(ps_base, 0.001)
        print(f"  {gname:<10} {tot:>5} {lf_r:>7.1%} {ll_r:>7.1%} {ps_r:>8.1%} {pf_r:>7.1%} {ps_enr:>6.2f}×")

    # Top she- words at para-starts
    she_ps_words = Counter()
    for r, _ in labeled:
        if r['is_para_start'] and r['words']:
            w = r['words'][0]
            if w.startswith('she') and len(w) > 3:
                she_ps_words[w] += 1

    print(f"\nTop she- words at A para-starts: {she_ps_words.most_common(10)}")

    # Top ch- words at para-starts
    ch_ps_words = Counter()
    for r, _ in labeled:
        if r['is_para_start'] and r['words']:
            w = r['words'][0]
            if w.startswith('ch') and len(w) > 2:
                ch_ps_words[w] += 1

    print(f"Top ch- words at A para-starts: {ch_ps_words.most_common(10)}")


# ============================================================
# H138: daiin Hierarchical Boundary Analysis
# ============================================================

def h138_daiin_hierarchy(a_recs):
    print("\n=== H138: daiin Hierarchical Boundary Analysis ===")

    paragraphs = group_into_paragraphs(a_recs)
    print(f"\nTotal A paragraphs: {len(paragraphs)}")

    # For each line in a paragraph, compute its RELATIVE POSITION
    # Position = (line_index) / (len(para) - 1) for multi-line paras
    # Position 0.0 = first line; 1.0 = last line

    # Group by position bucket
    n_buckets = 5
    bucket_daiin_counts = [0] * n_buckets
    bucket_total_words = [0] * n_buckets
    bucket_line_counts = [0] * n_buckets
    bucket_last_daiin = [0] * n_buckets  # daiin as last word

    for para in paragraphs:
        n_lines = len(para)
        if n_lines < 2:
            continue
        for idx, r in enumerate(para):
            # relative position: 0 = first, 1 = last
            rel_pos = idx / (n_lines - 1)
            bucket = min(int(rel_pos * n_buckets), n_buckets - 1)

            ws = r['words']
            bucket_total_words[bucket] += len(ws)
            bucket_line_counts[bucket] += 1
            daiin_count = ws.count('daiin')
            bucket_daiin_counts[bucket] += daiin_count
            if ws and ws[-1] == 'daiin':
                bucket_last_daiin[bucket] += 1

    print(f"\n--- daiin rate by paragraph position (5 buckets, 0=first 1=last) ---")
    print(f"{'Bucket':<10} {'Position':>10} {'Lines':>6} {'daiin%':>8} {'LastDaiin%':>12}")
    bucket_labels = ['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0']
    for i in range(n_buckets):
        daiin_r = bucket_daiin_counts[i] / max(bucket_total_words[i], 1)
        last_r = bucket_last_daiin[i] / max(bucket_line_counts[i], 1)
        print(f"  {bucket_labels[i]:<10} {i*0.2+0.1:>10.1f} {bucket_line_counts[i]:>6} {daiin_r:>7.1%} {last_r:>11.1%}")

    # Detailed: compare first, middle, last lines
    first_line_daiin = 0
    first_line_words = 0
    last_line_daiin = 0
    last_line_words = 0
    mid_line_daiin = 0
    mid_line_words = 0

    for para in paragraphs:
        n = len(para)
        if n < 3:
            continue
        # First line
        first_ws = para[0]['words']
        first_line_words += len(first_ws)
        first_line_daiin += first_ws.count('daiin')
        # Last line
        last_ws = para[-1]['words']
        last_line_words += len(last_ws)
        last_line_daiin += last_ws.count('daiin')
        # Middle lines
        for r in para[1:-1]:
            ws = r['words']
            mid_line_words += len(ws)
            mid_line_daiin += ws.count('daiin')

    print(f"\n--- daiin rate by line position in multi-line paragraphs (n≥3) ---")
    print(f"  First line: {first_line_daiin/max(first_line_words,1):.2%} ({first_line_words} words)")
    print(f"  Middle lines: {mid_line_daiin/max(mid_line_words,1):.2%} ({mid_line_words} words)")
    print(f"  Last line: {last_line_daiin/max(last_line_words,1):.2%} ({last_line_words} words)")

    # Is daiin rate monotonically increasing through paragraph?
    # Use all paragraphs of length 4+
    print(f"\n--- daiin rate by line ordinal within para (paras ≥4 lines) ---")
    ordinal_counts = defaultdict(lambda: [0, 0])  # [daiin, total]
    for para in paragraphs:
        n = len(para)
        if n < 4:
            continue
        for idx, r in enumerate(para):
            ws = r['words']
            ordinal_counts[idx][0] += ws.count('daiin')
            ordinal_counts[idx][1] += len(ws)

    for idx in sorted(ordinal_counts.keys())[:8]:
        d, t = ordinal_counts[idx]
        print(f"  Line {idx+1}: {d/max(t,1):.2%} daiin ({t} words)")

    # Daiin rate at LAST WORD POSITION
    print(f"\n--- daiin as LAST WORD by paragraph position ---")
    for para in paragraphs:
        pass  # already computed in bucket analysis above

    # More precise: daiin as last word rate for each line position
    pos_last_daiin = defaultdict(lambda: [0, 0])  # [daiin_last, total_lines]
    for para in paragraphs:
        n = len(para)
        if n < 2:
            continue
        for idx, r in enumerate(para):
            ws = r['words']
            pos_last_daiin[idx][1] += 1
            if ws and ws[-1] == 'daiin':
                pos_last_daiin[idx][0] += 1

    print(f"\n--- daiin as last word by line ordinal (paras ≥2 lines, first 8) ---")
    for idx in sorted(pos_last_daiin.keys())[:8]:
        d, t = pos_last_daiin[idx]
        print(f"  Line {idx+1}: {d/max(t,1):.2%} daiin-last ({t} lines)")

    # Overall daiin as last word for ALL lines in A
    total_a_lines = 0
    total_a_daiin_last = 0
    for r in a_recs:
        ws = r['words']
        if ws:
            total_a_lines += 1
            if ws[-1] == 'daiin':
                total_a_daiin_last += 1
    print(f"\nOverall A daiin-as-last-word: {total_a_daiin_last}/{total_a_lines} = {total_a_daiin_last/max(total_a_lines,1):.2%}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading data...")
    recs = parse_voynich(DATA_PATH)
    print(f"Total body records: {len(recs)}")

    a_recs, b_recs = assign_dialect(recs)
    print(f"A: {len(a_recs)}, B: {len(b_recs)}")

    # H136
    h136_ol_prefix_class(b_recs)

    # H137
    h137_she_para_start(a_recs)

    # H138
    h138_daiin_hierarchy(a_recs)

if __name__ == '__main__':
    main()
