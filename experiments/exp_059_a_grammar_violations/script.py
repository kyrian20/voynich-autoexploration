"""
exp_059: Currier A Line Grammar Violations (H066)
Tests whether specific Currier A folios violate the 3-tier line grammar:
  - para-start: -dy enriched, y-initial absent
  - continuation: y-initial enriched
  - line-final: -aiin enriched
Folios that violate these patterns may have different scribal hands, content, or structure.
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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

def get_line_type(locus_code):
    if locus_code.startswith('@'):
        return 'para_start'
    elif locus_code.startswith('+'):
        return 'continuation'
    else:
        return 'other'

def parse_corpus(path):
    lines = []
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

            folio_raw = parts[0].strip()
            locus_code = parts[1].strip()
            folio_id = folio_raw.split('.')[0] if '.' in folio_raw else folio_raw

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
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'line_type': line_type,
                'words': tokens,
            })

    return lines

def grammar_score(flines):
    all_lines = flines
    cont_lines = [l for l in flines if l['line_type'] == 'continuation']
    para_starts = [l for l in flines if l['line_type'] == 'para_start']

    n_all = len(all_lines)
    n_cont = len(cont_lines)
    n_ps = len(para_starts)

    if n_all < 5:
        return None

    y_all = sum(1 for l in all_lines if l['words'][0].startswith('y')) / max(n_all, 1)
    y_cont = sum(1 for l in cont_lines if l['words'][0].startswith('y')) / max(n_cont, 1) if n_cont > 0 else float('nan')
    y_ps = sum(1 for l in para_starts if l['words'][0].startswith('y')) / max(n_ps, 1) if n_ps > 0 else float('nan')

    dy_all = sum(1 for l in all_lines if suffix_group(l['words'][0]) == 'dy') / max(n_all, 1)
    dy_ps = sum(1 for l in para_starts if suffix_group(l['words'][0]) == 'dy') / max(n_ps, 1) if n_ps > 0 else float('nan')

    aiin_last_all = sum(1 for l in all_lines if suffix_group(l['words'][-1]) == 'aiin') / max(n_all, 1)

    dy_ratio = dy_ps / max(dy_all, 1e-10) if dy_ps == dy_ps and dy_all > 0 else float('nan')

    return {
        'n_lines': n_all,
        'n_ps': n_ps,
        'n_cont': n_cont,
        'y_all': y_all,
        'y_ps': y_ps,
        'y_cont': y_cont,
        'dy_all': dy_all,
        'dy_ps': dy_ps,
        'dy_ratio': dy_ratio,
        'aiin_last': aiin_last_all,
    }

def main():
    lines = parse_corpus(DATA_PATH)

    a_lines = [l for l in lines if l['currier'] == 'A']
    a_cont = [l for l in a_lines if l['line_type'] == 'continuation']
    a_ps = [l for l in a_lines if l['line_type'] == 'para_start']

    baseline_y_cont = sum(1 for l in a_cont if l['words'][0].startswith('y')) / max(len(a_cont), 1)
    baseline_y_ps = sum(1 for l in a_ps if l['words'][0].startswith('y')) / max(len(a_ps), 1)
    baseline_dy_all = sum(1 for l in a_lines if suffix_group(l['words'][0]) == 'dy') / max(len(a_lines), 1)
    baseline_dy_ps = sum(1 for l in a_ps if suffix_group(l['words'][0]) == 'dy') / max(len(a_ps), 1)

    print("Currier A corpus-wide baselines:")
    print(f"  y-initial at PS: {100*baseline_y_ps:.1f}% (canonical: ~0%)")
    print(f"  y-initial at continuations: {100*baseline_y_cont:.1f}% (canonical)")
    print(f"  -dy at all first words: {100*baseline_dy_all:.1f}%")
    print(f"  -dy at PS first words: {100*baseline_dy_ps:.1f}%")
    print(f"  -dy PS ratio: {baseline_dy_ps/max(baseline_dy_all,1e-10):.2f}x")

    folio_dict = defaultdict(list)
    for l in a_lines:
        folio_dict[l['folio']].append(l)

    print(f"\n{'='*90}")
    print("PER-FOLIO GRAMMAR SCORES (Currier A, >=15 lines)")
    print(f"{'='*90}")
    print(f"{'Folio':<10} {'Lines':>6} {'PS':>4} {'Cont':>5} {'y@PS':>6} {'y@Cont':>7} {'dy_ratio':>9} {'aiin_last':>10} {'Section':>8}")

    folio_scores = []
    for folio_id, flines in sorted(folio_dict.items()):
        if len(flines) < 15:
            continue
        s = grammar_score(flines)
        if s is None:
            continue
        section = flines[0].get('section', '?')
        s['folio'] = folio_id
        s['section'] = section
        folio_scores.append(s)

    folio_scores.sort(key=lambda x: x['n_lines'], reverse=True)

    for s in folio_scores:
        nan = float('nan')
        y_ps_str = f"{100*s['y_ps']:.1f}%" if s['y_ps']==s['y_ps'] else "N/A"
        y_cont_str = f"{100*s['y_cont']:.1f}%" if s['y_cont']==s['y_cont'] else "N/A"
        dy_str = f"{s['dy_ratio']:.2f}x" if s['dy_ratio']==s['dy_ratio'] else "N/A"
        print(f"{s['folio']:<10} {s['n_lines']:>6} {s['n_ps']:>4} {s['n_cont']:>5} {y_ps_str:>6} {y_cont_str:>7} {dy_str:>9} {100*s['aiin_last']:>9.1f}% {s['section']:>8}")

    # Grammar violators
    print(f"\n{'='*90}")
    print("GRAMMAR VIOLATORS (y@PS>10% with >=3 PS, OR y@cont<5% with >=10 cont):")
    violators = []
    for s in folio_scores:
        violated = False
        reasons = []
        if s['y_ps']==s['y_ps'] and s['y_ps'] > 0.10 and s['n_ps'] >= 3:
            violated = True
            reasons.append(f"y@PS={100*s['y_ps']:.0f}% (should be ~0%)")
        if s['y_cont']==s['y_cont'] and s['y_cont'] < 0.05 and s['n_cont'] >= 10:
            violated = True
            reasons.append(f"y@cont={100*s['y_cont']:.1f}% (should be ~{100*baseline_y_cont:.0f}%)")
        if violated:
            violators.append((s, reasons))

    if violators:
        for s, reasons in sorted(violators, key=lambda x: x[0]['n_lines'], reverse=True):
            print(f"\n  {s['folio']:<10} [{s['section']}] {s['n_lines']} lines, {s['n_ps']} PS, {s['n_cont']} cont")
            for r in reasons:
                print(f"    VIOLATION: {r}")
    else:
        print("  No strong violators found.")

    # Zero-y-initial folios
    zero_y = [s for s in folio_scores if s['y_all'] == 0.0 and s['n_cont'] >= 5]
    print(f"\n{'='*90}")
    print(f"ZERO y-initial folios (>=15 lines, >=5 continuation lines): {len(zero_y)}")
    print(f"{'Folio':<10} {'Lines':>6} {'PS':>4} {'Cont':>5} {'Section':>8}")
    sec_zero = Counter()
    for s in sorted(zero_y, key=lambda x: -x['n_lines']):
        print(f"{s['folio']:<10} {s['n_lines']:>6} {s['n_ps']:>4} {s['n_cont']:>5} {s['section']:>8}")
        sec_zero[s['section']] += 1

    print(f"\nZero-y-initial by section: {dict(sec_zero)}")

    # Summary statistics
    print(f"\n{'='*90}")
    print("FOLIO-LEVEL GRAMMAR CONSISTENCY SUMMARY")
    valid = [s for s in folio_scores if s['y_cont']==s['y_cont'] and s['n_cont']>=10]
    y_cont_vals = [s['y_cont'] for s in valid]
    mean_y = sum(y_cont_vals) / len(y_cont_vals) if y_cont_vals else 0
    std_y = (sum((v - mean_y)**2 for v in y_cont_vals) / max(len(y_cont_vals)-1, 1))**0.5
    print(f"Mean folio y@cont: {100*mean_y:.1f}% ± {100*std_y:.1f}% (n={len(valid)} folios)")

    low_y = [s for s in valid if s['y_cont'] < mean_y - 2*std_y]
    high_y = [s for s in valid if s['y_cont'] > mean_y + 2*std_y]
    print(f"Outliers (<mean-2sd={100*(mean_y-2*std_y):.1f}%): {[s['folio'] for s in low_y]}")
    print(f"Outliers (>mean+2sd={100*(mean_y+2*std_y):.1f}%): {[s['folio'] for s in high_y]}")

if __name__ == '__main__':
    main()
