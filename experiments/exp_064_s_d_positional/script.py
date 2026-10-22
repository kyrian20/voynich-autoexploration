"""
exp_064: B y-Initial Continuation + p-Onset Para-Start Symmetry (H075)
Tests whether B has a symmetric two-marker system: p-onset=para-start, y-initial=continuation.
Also tests H074: s-initial vs d-initial positional distribution.
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

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def parse_corpus(path):
    records = []
    current_currier = None
    current_section = None
    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)
            m_s = re.search(r'\$I=([A-Z]+)', line)
            if m_s:
                current_section = m_s.group(1)
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
            line_type = 'para_start' if locus_code.startswith('@') else ('continuation' if locus_code.startswith('+') else 'other')
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({'currier': current_currier, 'line_type': line_type, 'words': tokens})
    return records

def main():
    records = parse_corpus(DATA_PATH)

    # H075: B y-initial continuation vs p-onset para-start symmetry
    print("="*70)
    print("H075: B TWO-MARKER POSITIONAL SYSTEM: p-onset PS vs y-initial continuation")
    print("="*70)

    for dialect in ['A', 'B']:
        lines = [r for r in records if r['currier'] == dialect]
        ps_lines = [r for r in lines if r['line_type'] == 'para_start']
        cont_lines = [r for r in lines if r['line_type'] == 'continuation']
        all_lines = lines

        n_ps = len(ps_lines)
        n_cont = len(cont_lines)
        n_all = len(all_lines)

        # y-initial rates
        y_all = sum(1 for l in all_lines if l['words'][0].startswith('y')) / max(n_all, 1)
        y_ps = sum(1 for l in ps_lines if l['words'][0].startswith('y')) / max(n_ps, 1)
        y_cont = sum(1 for l in cont_lines if l['words'][0].startswith('y')) / max(n_cont, 1)

        # p-onset rates  
        p_all = sum(1 for l in all_lines if l['words'][0].startswith('p')) / max(n_all, 1)
        p_ps = sum(1 for l in ps_lines if l['words'][0].startswith('p')) / max(n_ps, 1)
        p_cont = sum(1 for l in cont_lines if l['words'][0].startswith('p')) / max(n_cont, 1)

        print(f"\nCurrier {dialect} (all={n_all}, PS={n_ps}, cont={n_cont}):")
        print(f"  y-initial: all={100*y_all:.1f}%, PS={100*y_ps:.1f}% ({y_ps/max(y_all,1e-10):.2f}x), cont={100*y_cont:.1f}% ({y_cont/max(y_all,1e-10):.2f}x)")
        print(f"  p-onset:   all={100*p_all:.1f}%, PS={100*p_ps:.1f}% ({p_ps/max(p_all,1e-10):.2f}x), cont={100*p_cont:.1f}% ({p_cont/max(p_all,1e-10):.2f}x)")

        # Mutual exclusivity: are PS lines with p-onset also y-initial?
        ps_p_y = sum(1 for l in ps_lines if l['words'][0].startswith('p') and l['words'][0].startswith('y'))
        cont_p_y = sum(1 for l in cont_lines if l['words'][0].startswith('p') and l['words'][0].startswith('y'))
        print(f"  p+y overlap at PS: {ps_p_y} (impossible since p!=y)")

    print("\n")

    # H074: s-initial vs d-initial positional distribution in B
    print("="*70)
    print("H074: s-INITIAL vs d-INITIAL POSITIONAL DISTRIBUTION (Currier B)")
    print("="*70)

    b_lines = [r for r in records if r['currier'] == 'B']
    n_all_b = len(b_lines)
    b_all_words = [w for l in b_lines for w in l['words']]
    n_all_words_b = len(b_all_words)

    # For each onset type, compute first-word and last-word rates
    classes = {
        'd': lambda w: w.startswith('d') and not w.startswith('dy'),
        's': lambda w: w.startswith('s') and not w.startswith('sh'),
        'sh': lambda w: w.startswith('sh'),
        'ch': lambda w: w.startswith('ch'),
        'qo': lambda w: w.startswith('qo'),
        'o': lambda w: w.startswith('o'),
        'y': lambda w: w.startswith('y'),
        'p': lambda w: w.startswith('p'),
        'k': lambda w: w.startswith('k'),
        't': lambda w: w.startswith('t') and not w.startswith('tch'),
    }

    print(f"\nCurrier B positional distribution of onset classes ({n_all_b} lines, {n_all_words_b} tokens):")
    print(f"{'Onset':<6} {'All%':>6} {'First%':>7} {'Last%':>7} {'First_ratio':>12} {'Last_ratio':>11}")

    for onset_name, test_fn in sorted(classes.items()):
        n_all_onset = sum(1 for w in b_all_words if test_fn(w))
        n_first = sum(1 for l in b_lines if test_fn(l['words'][0]))
        n_last = sum(1 for l in b_lines if test_fn(l['words'][-1]))

        all_p = n_all_onset / max(n_all_words_b, 1)
        first_p = n_first / max(n_all_b, 1)
        last_p = n_last / max(n_all_b, 1)

        # Compare to: if randomly distributed, first_p should ~ all_p (approximately)
        first_ratio = first_p / max(all_p, 1e-10)
        last_ratio = last_p / max(all_p, 1e-10)

        print(f"{onset_name:<6} {100*all_p:>5.2f}% {100*first_p:>6.2f}% {100*last_p:>6.2f}% {first_ratio:>11.2f}x {last_ratio:>10.2f}x")

    # Suffix distribution for s-initial in B
    print(f"\nSuffix distribution for s-initial words in B:")
    s_words = [w for w in b_all_words if w.startswith('s') and not w.startswith('sh')]
    d_words = [w for w in b_all_words if w.startswith('d')]
    s_suf = Counter(suffix_group(w) or '(none)' for w in s_words)
    d_suf = Counter(suffix_group(w) or '(none)' for w in d_words)
    n_s = len(s_words)
    n_d = len(d_words)
    print(f"s-words: {n_s} tokens | d-words: {n_d} tokens")
    print(f"{'Suffix':<8} {'s%':>6} {'d%':>6}")
    for suf in SUFFIX_LIST + ['(none)']:
        sp = s_suf.get(suf, 0) / max(n_s, 1)
        dp = d_suf.get(suf, 0) / max(n_d, 1)
        if sp > 0.03 or dp > 0.03:
            print(f"{suf:<8} {100*sp:>5.1f}% {100*dp:>5.1f}%")

    # Top s-words in B
    print(f"\nTop s-initial words in B (not sh-):")
    s_counter = Counter(w for w in b_all_words if w.startswith('s') and not w.startswith('sh'))
    for w, c in s_counter.most_common(15):
        print(f"  {w}: {c}")

    # s-initial line-last specific words
    print(f"\ns-initial words that appear at line-last positions in B:")
    s_last = Counter()
    for l in b_lines:
        w = l['words'][-1]
        if w.startswith('s') and not w.startswith('sh'):
            s_last[w] += 1
    for w, c in s_last.most_common(10):
        print(f"  {w}: {c}")

if __name__ == '__main__':
    main()
