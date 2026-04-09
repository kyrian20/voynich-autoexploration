"""
exp_054: 'y-' Prefix Paragraph-Start Analysis (H061)
exp_053 found 'y-' initial words (ychor, ycheey, etc.) are 5-6× enriched at line beginnings.
H061: Is this effect concentrated at PARAGRAPH starts (@P0) vs mid-paragraph lines (+P0)?
Also tests H062: -ain concentration at paragraph vs mid-paragraph boundaries.
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def parse_lines_typed(path):
    """
    Parse body text lines tracking line type:
    - 'para_start': @P0 (first line of paragraph)
    - 'continuation': +P0 (continuation line within paragraph)
    - 'para_end': =Pt or any line followed by <$>
    Returns list of dicts: {words, currier, line_type, has_end_marker}
    """
    lines = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for raw_line in f:
            raw_line = raw_line.rstrip('\n')
            if not raw_line or raw_line.startswith('#'):
                continue

            m_c = re.search(r'\$L=([AB])', raw_line)
            if m_c:
                current_currier = m_c.group(1)

            m = re.match(r'^<([^>]+)>', raw_line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            if not is_body_locus(locus_code):
                continue

            # Determine line type from locus prefix character
            first_char = locus_code[0] if locus_code else ''
            if first_char == '@':
                line_type = 'para_start'
            elif first_char == '+':
                line_type = 'continuation'
            elif first_char == '=' or locus_code.lstrip('@+=*').startswith('Pt'):
                line_type = 'para_end'
            else:
                line_type = 'other'

            # Check for <$> in text (paragraph end marker)
            text_raw = raw_line[m.end():].strip()
            has_end = '<$>' in text_raw

            text = clean_text(text_raw)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens:
                continue

            lines.append({
                'words': tokens,
                'currier': current_currier,
                'line_type': line_type,
                'has_end': has_end,
                'n': len(tokens),
            })

    return lines

def compute_enrichment(lines, test_fn, currier='A'):
    """
    For lines matching currier, compute:
    - fraction of para_start lines where first word satisfies test_fn
    - fraction of continuation lines where first word satisfies test_fn
    - fraction of all lines where last word satisfies test_fn
    """
    para_start_total = 0
    para_start_match = 0
    continuation_total = 0
    continuation_match = 0
    para_end_total = 0
    para_end_match_last = 0
    all_total = 0
    all_match_first = 0
    all_match_last = 0

    for line in lines:
        if line['currier'] != currier:
            continue
        words = line['words']
        if not words:
            continue

        all_total += 1
        if test_fn(words[0]):
            all_match_first += 1
        if test_fn(words[-1]):
            all_match_last += 1

        if line['line_type'] == 'para_start':
            para_start_total += 1
            if test_fn(words[0]):
                para_start_match += 1
        elif line['line_type'] == 'continuation':
            continuation_total += 1
            if test_fn(words[0]):
                continuation_match += 1

        if line['has_end']:
            para_end_total += 1
            if test_fn(words[-1]):
                para_end_match_last += 1

    return {
        'para_start_rate': para_start_match / max(1, para_start_total),
        'continuation_rate': continuation_match / max(1, continuation_total),
        'all_first_rate': all_match_first / max(1, all_total),
        'para_end_rate': para_end_match_last / max(1, para_end_total),
        'all_last_rate': all_match_last / max(1, all_total),
        'para_start_total': para_start_total,
        'continuation_total': continuation_total,
        'para_end_total': para_end_total,
        'all_total': all_total,
    }

def main():
    lines = parse_lines_typed(DATA_PATH)
    print(f"Total lines parsed: {len(lines)}")

    # Count line types
    for currier in ['A', 'B']:
        cur_lines = [l for l in lines if l['currier'] == currier]
        types = Counter(l['line_type'] for l in cur_lines)
        print(f"Currier {currier}: {len(cur_lines)} lines — types: {dict(types)}")

    print()

    # === 1. 'y-' initial words: para_start vs continuation ===
    def is_y_initial(word):
        return word.startswith('y') and len(word) >= 3

    def is_ych(word):
        return word.startswith('ych') and len(word) >= 4

    print("=" * 70)
    print("'y-' INITIAL WORDS: Para-start vs Continuation Line Beginnings")
    print("=" * 70)

    for currier in ['A', 'B']:
        result = compute_enrichment(lines, is_y_initial, currier)
        result_ych = compute_enrichment(lines, is_ych, currier)

        print(f"\nCurrier {currier}:")
        print(f"  Any y-initial word:")
        print(f"    Para-start (@P0): {100*result['para_start_rate']:.1f}% ({result['para_start_total']} para-starts)")
        print(f"    Continuation (+P0): {100*result['continuation_rate']:.1f}% ({result['continuation_total']} continuations)")
        print(f"    All lines (baseline): {100*result['all_first_rate']:.1f}%")
        if result['continuation_rate'] > 0:
            ratio = result['para_start_rate'] / result['continuation_rate']
            print(f"    Para-start/continuation ratio: {ratio:.2f}×")

        print(f"  'ych-' specific words:")
        print(f"    Para-start: {100*result_ych['para_start_rate']:.1f}%")
        print(f"    Continuation: {100*result_ych['continuation_rate']:.1f}%")
        print(f"    All lines: {100*result_ych['all_first_rate']:.1f}%")

    # === 2. -ain suffix: para-start vs continuation vs para-end ===
    def ends_ain(word):
        return word.endswith('ain') and len(word) > 3

    def ends_aiin(word):
        return word.endswith('aiin') and len(word) > 4

    print("\n" + "=" * 70)
    print("-ain/-aiin SUFFIX: Para-level positional analysis")
    print("=" * 70)

    for currier in ['A', 'B']:
        result_ain = compute_enrichment(lines, ends_ain, currier)
        result_aiin = compute_enrichment(lines, ends_aiin, currier)

        print(f"\nCurrier {currier}:")
        print(f"  -ain words:")
        print(f"    Para-start first: {100*result_ain['para_start_rate']:.1f}%")
        print(f"    Continuation first: {100*result_ain['continuation_rate']:.1f}%")
        print(f"    All lines first: {100*result_ain['all_first_rate']:.1f}%")
        print(f"    Para-end last: {100*result_ain['para_end_rate']:.1f}% ({result_ain['para_end_total']} para-ends)")
        print(f"    All lines last: {100*result_ain['all_last_rate']:.1f}%")

        print(f"  -aiin words:")
        print(f"    Para-start first: {100*result_aiin['para_start_rate']:.1f}%")
        print(f"    Continuation first: {100*result_aiin['continuation_rate']:.1f}%")
        print(f"    Para-end last: {100*result_aiin['para_end_rate']:.1f}%")

    # === 3. Line-type distribution of all suffix classes ===
    print("\n" + "=" * 70)
    print("SUFFIX FIRST-WORD RATES BY LINE TYPE: Currier A")
    print("=" * 70)

    # Collect first-word suffix distributions by line type
    a_para_start_firsts = [l['words'][0] for l in lines if l['currier'] == 'A' and l['line_type'] == 'para_start' and l['words']]
    a_continuation_firsts = [l['words'][0] for l in lines if l['currier'] == 'A' and l['line_type'] == 'continuation' and l['words']]

    def get_suffix_rates(word_list):
        counts = Counter()
        for w in word_list:
            for suf in SUFFIX_LIST:
                if w.endswith(suf) and len(w) > len(suf):
                    counts[suf] += 1
                    break
        total = len(word_list)
        return {k: v/total for k, v in counts.items()}, total

    para_start_dist, para_start_n = get_suffix_rates(a_para_start_firsts)
    cont_dist, cont_n = get_suffix_rates(a_continuation_firsts)

    print(f"\n{'Suffix':<10} {'Para-start%':>13} {'Continuation%':>15} {'Ratio':>7}")
    all_suffixes = sorted(set(para_start_dist) | set(cont_dist), key=lambda s: -(para_start_dist.get(s,0)+cont_dist.get(s,0)))
    for suf in all_suffixes:
        ps = para_start_dist.get(suf, 0.0)
        ct = cont_dist.get(suf, 0.0)
        ratio = ps / max(ct, 1e-6)
        flag = "***" if ratio > 3 else ("**" if ratio > 2 else ("*" if ratio > 1.5 else ""))
        print(f"-{suf:<9} {100*ps:>12.1f}% {100*ct:>14.1f}% {ratio:>6.2f}{flag}")
    print(f"{'(N)':>10} {para_start_n:>13} {cont_n:>15}")

    # 'y-' initial in para-start vs continuation
    y_para_start = sum(1 for w in a_para_start_firsts if w.startswith('y'))
    y_cont = sum(1 for w in a_continuation_firsts if w.startswith('y'))
    print(f"\ny-initial words:")
    print(f"  Para-start: {y_para_start}/{para_start_n} = {100*y_para_start/max(1,para_start_n):.1f}%")
    print(f"  Continuation: {y_cont}/{cont_n} = {100*y_cont/max(1,cont_n):.1f}%")
    if y_cont > 0:
        print(f"  Para-start/cont ratio: {(y_para_start/max(1,para_start_n))/(y_cont/max(1,cont_n)):.2f}×")

    # === 4. Top para-start words ===
    print("\n" + "=" * 70)
    print("TOP WORDS AT PARAGRAPH STARTS IN CURRIER A")
    print("=" * 70)
    para_start_freq = Counter(a_para_start_firsts)
    all_a_freq = Counter(w for l in lines if l['currier'] == 'A' for w in l['words'])
    n_all_a = sum(all_a_freq.values())
    n_para_starts = para_start_n

    enrichment_list = []
    for w, c in para_start_freq.most_common(30):
        p_para = c / n_para_starts
        p_any = all_a_freq.get(w, 0) / n_all_a
        if p_any > 0:
            enrichment_list.append((w, c, p_para, p_any, p_para/p_any))
    enrichment_list.sort(key=lambda x: -x[4])

    print(f"{'Word':<12} {'Para-n':>7} {'P(w|start)':>12} {'P(w)':>9} {'Ratio':>7}")
    for w, c, pp, pa, r in enrichment_list[:20]:
        print(f"{w:<12} {c:>7} {100*pp:>11.1f}% {100*pa:>8.2f}% {r:>6.2f}×")

if __name__ == '__main__':
    main()
