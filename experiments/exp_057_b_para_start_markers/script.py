"""
exp_057: Currier B Paragraph-Start Markers (H064)
Tests whether -dy marks paragraph starts in Currier B, as it does in Currier A (4.39×, F061).
Also checks if y-initial words are similarly suppressed at B para-starts.
Full comparison of A vs B paragraph-level positional grammar.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def get_line_type(locus_code):
    """Return 'para_start', 'continuation', or 'other' based on locus prefix."""
    if locus_code.startswith('@'):
        return 'para_start'
    elif locus_code.startswith('+'):
        return 'continuation'
    else:
        return 'other'

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def parse_corpus(path):
    """Parse body text, returning lines with (words, line_type, currier)."""
    lines = []
    current_currier = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue

            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)

            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            locus_code = parts[1].strip()

            if not is_body_locus(locus_code):
                continue

            line_type = get_line_type(locus_code)
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]

            if not tokens:
                continue

            lines.append({
                'words': tokens,
                'line_type': line_type,
                'currier': current_currier
            })

    return lines

def analyze_paragraph_markers(lines, dialect):
    """
    For the given dialect, analyze:
    1. First word of para_start lines vs continuation lines vs all lines
    2. Suffix distribution at para-start first words vs baseline
    3. Last word of para_start lines vs para-end lines vs all
    4. y-initial suppression at para-starts
    """
    filtered = [l for l in lines if l['currier'] == dialect]

    para_starts = [l for l in filtered if l['line_type'] == 'para_start']
    continuations = [l for l in filtered if l['line_type'] == 'continuation']
    all_lines = filtered

    print(f"\n{'='*70}")
    print(f"PARAGRAPH MARKER ANALYSIS: Currier {dialect}")
    print(f"{'='*70}")
    print(f"Total lines: {len(all_lines)} | Para-starts: {len(para_starts)} | Continuations: {len(continuations)}")

    # Build global suffix distribution (first words of ALL lines, baseline)
    baseline_first = Counter()
    for l in all_lines:
        w = l['words'][0]
        suf = suffix_group(w) or '(none)'
        baseline_first[suf] += 1
    n_baseline = sum(baseline_first.values())

    # Para-start first words
    ps_first = Counter()
    for l in para_starts:
        w = l['words'][0]
        suf = suffix_group(w) or '(none)'
        ps_first[suf] += 1
    n_ps = sum(ps_first.values())

    # Continuation first words
    cont_first = Counter()
    for l in continuations:
        w = l['words'][0]
        suf = suffix_group(w) or '(none)'
        cont_first[suf] += 1
    n_cont = sum(cont_first.values())

    print(f"\n--- FIRST WORD SUFFIX DISTRIBUTION ---")
    print(f"{'Suffix':<8} {'PS%':>6} {'Cont%':>7} {'All%':>6} {'PS/All ratio':>13}")
    suffixes_of_interest = ['dy', 'edy', 'chy', 'aiin', 'ain', 'iin', 'ol', 'or', 'al', 'ar', 'y', 'ey', '(none)']
    for suf in suffixes_of_interest:
        ps_p = ps_first.get(suf, 0) / max(n_ps, 1)
        cont_p = cont_first.get(suf, 0) / max(n_cont, 1)
        all_p = baseline_first.get(suf, 0) / max(n_baseline, 1)
        ratio = ps_p / max(all_p, 1e-10)
        print(f"{suf:<8} {100*ps_p:>5.1f}% {100*cont_p:>6.1f}% {100*all_p:>5.1f}% {ratio:>13.2f}×")

    # y-initial analysis
    print(f"\n--- y-INITIAL SUPPRESSION ---")
    ps_y = sum(1 for l in para_starts if l['words'][0].startswith('y'))
    cont_y = sum(1 for l in continuations if l['words'][0].startswith('y'))
    all_y = sum(1 for l in all_lines if l['words'][0].startswith('y'))
    print(f"  y-initial at para-starts: {ps_y}/{n_ps} = {100*ps_y/max(n_ps,1):.1f}%")
    print(f"  y-initial at continuations: {cont_y}/{n_cont} = {100*cont_y/max(n_cont,1):.1f}%")
    print(f"  y-initial at all lines: {all_y}/{len(all_lines)} = {100*all_y/max(len(all_lines),1):.1f}%")
    ratio = (ps_y/max(n_ps,1)) / max(all_y/max(len(all_lines),1), 1e-10)
    print(f"  Para-start y-initial ratio vs baseline: {ratio:.2f}×")

    # Top first words at para-starts
    print(f"\n--- TOP FIRST WORDS AT PARA-STARTS ---")
    ps_first_words = Counter()
    for l in para_starts:
        ps_first_words[l['words'][0]] += 1

    all_first_words = Counter()
    for l in all_lines:
        all_first_words[l['words'][0]] += 1
    n_all_first = sum(all_first_words.values())

    print(f"{'Word':<12} {'PS_count':>9} {'PS%':>6} {'All%':>6} {'Ratio':>7}")
    for word, count in ps_first_words.most_common(15):
        ps_p = count / max(n_ps, 1)
        all_p = all_first_words.get(word, 0) / max(n_all_first, 1)
        ratio = ps_p / max(all_p, 1e-10)
        print(f"{word:<12} {count:>9} {100*ps_p:>5.1f}% {100*all_p:>5.1f}% {ratio:>7.2f}×")

    # Last word analysis
    print(f"\n--- LAST WORD SUFFIX AT PARA-STARTS ---")
    ps_last = Counter()
    for l in para_starts:
        if len(l['words']) > 0:
            w = l['words'][-1]
            suf = suffix_group(w) or '(none)'
            ps_last[suf] += 1

    all_last = Counter()
    for l in all_lines:
        if len(l['words']) > 0:
            w = l['words'][-1]
            suf = suffix_group(w) or '(none)'
            all_last[suf] += 1
    n_all_last = sum(all_last.values())
    n_ps_last = sum(ps_last.values())

    print(f"{'Suffix':<8} {'PS%':>6} {'All%':>6} {'Ratio':>7}")
    for suf in suffixes_of_interest:
        ps_p = ps_last.get(suf, 0) / max(n_ps_last, 1)
        all_p = all_last.get(suf, 0) / max(n_all_last, 1)
        ratio = ps_p / max(all_p, 1e-10)
        if ps_last.get(suf, 0) >= 3 or all_last.get(suf, 0) >= 5:
            print(f"{suf:<8} {100*ps_p:>5.1f}% {100*all_p:>5.1f}% {ratio:>7.2f}×")

    # Specific check for -dy suffix
    print(f"\n--- -dy SUFFIX DETAIL ---")
    dy_words_ps = [l['words'][0] for l in para_starts if suffix_group(l['words'][0]) == 'dy']
    dy_words_all = [l['words'][0] for l in all_lines if suffix_group(l['words'][0]) == 'dy']
    print(f"  -dy first words at para-starts: {len(dy_words_ps)}")
    print(f"  Top -dy words at para-starts: {Counter(dy_words_ps).most_common(10)}")
    print(f"  Top -dy words overall: {Counter(dy_words_all).most_common(10)}")

    return {
        'n_para_starts': n_ps,
        'n_continuations': n_cont,
        'n_all': len(all_lines),
        'ps_first': ps_first,
        'baseline_first': baseline_first,
    }

def compare_dialects(lines):
    """Direct comparison of A vs B paragraph marker patterns."""
    print(f"\n{'='*70}")
    print("CROSS-DIALECT COMPARISON: Para-start first-word -dy rate")
    print(f"{'='*70}")

    for dialect in ['A', 'B']:
        filtered = [l for l in lines if l['currier'] == dialect]
        para_starts = [l for l in filtered if l['line_type'] == 'para_start']
        all_lines = filtered

        n_ps = len(para_starts)
        n_all = len(all_lines)

        ps_dy = sum(1 for l in para_starts if suffix_group(l['words'][0]) == 'dy') if para_starts else 0
        all_dy = sum(1 for l in all_lines if suffix_group(l['words'][0]) == 'dy') if all_lines else 0

        ps_rate = ps_dy / max(n_ps, 1)
        all_rate = all_dy / max(n_all, 1)
        ratio = ps_rate / max(all_rate, 1e-10)

        print(f"\nCurrier {dialect}:")
        print(f"  Para-starts: {n_ps}, -dy: {ps_dy} ({100*ps_rate:.1f}%)")
        print(f"  All lines: {n_all}, -dy: {all_dy} ({100*all_rate:.1f}%)")
        print(f"  Enrichment ratio: {ratio:.2f}×")

        # y-initial
        ps_y = sum(1 for l in para_starts if l['words'][0].startswith('y')) if para_starts else 0
        all_y = sum(1 for l in all_lines if l['words'][0].startswith('y')) if all_lines else 0
        ps_y_rate = ps_y / max(n_ps, 1)
        all_y_rate = all_y / max(n_all, 1)
        y_ratio = ps_y_rate / max(all_y_rate, 1e-10)
        print(f"  y-initial at para-starts: {ps_y} ({100*ps_y_rate:.1f}%), all: {100*all_y_rate:.1f}%, ratio: {y_ratio:.2f}×")

def main():
    lines = parse_corpus(DATA_PATH)
    print(f"Total lines parsed: {len(lines)}")
    print(f"Currier A: {sum(1 for l in lines if l['currier'] == 'A')} lines")
    print(f"Currier B: {sum(1 for l in lines if l['currier'] == 'B')} lines")

    analyze_paragraph_markers(lines, 'A')
    analyze_paragraph_markers(lines, 'B')
    compare_dialects(lines)

if __name__ == '__main__':
    main()
