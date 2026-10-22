"""
exp_071: Onset Taxonomy Stability Across B Sections (H089) + Sequential Grammar Cross-Section (H090)
H089: Is the 5-class positional onset taxonomy stable across Currier B sections?
H090: Does the qo+gallows→ch/sh sequential rule hold across all B sections?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def onset_class(word):
    if word.startswith('qo') and len(word) > 2:
        return 'qo'
    if word.startswith('ch') and len(word) > 2:
        return 'ch'
    if word.startswith('sh') and len(word) > 2:
        return 'sh'
    if word.startswith('p') and len(word) > 1:
        return 'p'
    if word.startswith('t') and len(word) > 1:
        return 't'
    if word.startswith('f') and len(word) > 1:
        return 'f'
    if word.startswith('k') and len(word) > 1:
        return 'k'
    if word.startswith('d') and len(word) > 1:
        return 'd'
    if word.startswith('s') and not word.startswith('sh') and len(word) > 1:
        return 's'
    if word.startswith('y') and len(word) > 1:
        return 'y'
    if word.startswith('o') and len(word) > 1:
        return 'o'
    return 'other'

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
            folio_raw = parts[0].strip()
            locus_code = parts[1].strip()
            folio_id = folio_raw.split('.')[0] if '.' in folio_raw else folio_raw
            if not is_body_locus(locus_code):
                continue
            base_locus = locus_code.lstrip('+*=/~&')
            is_para_start = base_locus.startswith('@')
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'is_para_start': is_para_start,
                'words': tokens
            })
    return records

def compute_positional_stats(recs):
    """Return positional stats for each onset class."""
    pos_counts = defaultdict(lambda: {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0})
    total = {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0}

    for r in recs:
        ws = r['words']
        n = len(ws)
        if n == 0:
            continue
        for i, w in enumerate(ws):
            oc = onset_class(w)
            pos = 'medial' if 0 < i < n-1 else ('first' if i == 0 else 'last')
            pos_counts[oc][pos] += 1
            pos_counts[oc]['total'] += 1
            total[pos] += 1
            total['total'] += 1
            if i == 0 and r['is_para_start']:
                pos_counts[oc]['para_first'] += 1
                total['para_first'] += 1

    return pos_counts, total

def main():
    records = parse_corpus(DATA_PATH)
    b_records = [r for r in records if r['currier'] == 'B']

    # H089: Onset taxonomy by section
    print("="*70)
    print("H089: ONSET POSITIONAL TAXONOMY STABILITY ACROSS CURRIER B SECTIONS")
    print("="*70)

    # Get sections with enough data
    sections = sorted(set(r['section'] for r in b_records if r['section']))
    key_classes = ['p', 't', 'k', 'ch', 'sh', 'qo', 'd', 's', 'y']

    # B-wide baseline first
    all_stats, all_total = compute_positional_stats(b_records)
    n_all = all_total['total']
    base_first = all_total['first'] / max(n_all, 1)
    base_para = all_total['para_first'] / max(n_all, 1)
    base_medial = all_total['medial'] / max(n_all, 1)
    base_last = all_total['last'] / max(n_all, 1)

    print(f"\nB-WIDE BASELINE: n={n_all}, first={100*base_first:.1f}%, medial={100*base_medial:.1f}%, last={100*base_last:.1f}%, para_first={100*base_para:.2f}%")
    print(f"\n{'Class':<8} {'count':>6} {'first%':>8} {'enr_1st':>9} {'med%':>8} {'enr_med':>9} {'last%':>7} {'enr_last':>9} {'para%':>7} {'enr_par':>9}")
    for oc in key_classes:
        s = all_stats[oc]
        n = s['total']
        if n < 10:
            continue
        pf = s['first'] / max(n, 1)
        pm = s['medial'] / max(n, 1)
        pl = s['last'] / max(n, 1)
        pp = s['para_first'] / max(n, 1)
        print(f"{oc:<8} {n:>6} {100*pf:>7.1f}% {pf/max(base_first,1e-10):>8.2f}× {100*pm:>7.1f}% {pm/max(base_medial,1e-10):>8.2f}× {100*pl:>6.1f}% {pl/max(base_last,1e-10):>8.2f}× {100*pp:>6.2f}% {pp/max(base_para,1e-10):>8.2f}×")

    print(f"\n--- BY SECTION ---")
    for sec in sections:
        sec_recs = [r for r in b_records if r['section'] == sec]
        if len(sec_recs) < 20:
            continue
        sec_stats, sec_total = compute_positional_stats(sec_recs)
        n_sec = sec_total['total']
        sec_base_first = sec_total['first'] / max(n_sec, 1)
        sec_base_para = sec_total['para_first'] / max(n_sec, 1)
        sec_base_med = sec_total['medial'] / max(n_sec, 1)
        sec_base_last = sec_total['last'] / max(n_sec, 1)

        print(f"\n  Section {sec} (n={n_sec}): base first={100*sec_base_first:.1f}%, para={100*sec_base_para:.2f}%")
        print(f"  {'Class':<8} {'n':>5} {'1st%':>7} {'enr1':>7} {'para%':>8} {'enrP':>7} {'med%':>7} {'enrM':>7}")
        for oc in key_classes:
            s = sec_stats.get(oc, {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0})
            n = s['total']
            if n < 5:
                continue
            pf = s['first'] / max(n, 1)
            pm = s['medial'] / max(n, 1)
            pl = s['last'] / max(n, 1)
            pp = s['para_first'] / max(n, 1)
            print(f"  {oc:<8} {n:>5} {100*pf:>6.1f}% {pf/max(sec_base_first,1e-10):>6.2f}× {100*pp:>7.2f}% {pp/max(sec_base_para,1e-10):>6.2f}× {100*pm:>6.1f}% {pm/max(sec_base_med,1e-10):>6.2f}×")

    # H090: Sequential grammar (qo+gallows→ch/sh) across sections
    print(f"\n{'='*70}")
    print("H090: qo+gallows→ch/sh SEQUENTIAL RULE ACROSS CURRIER B SECTIONS")
    print(f"{'='*70}")

    # For each section: what are the top predecessors of ch and sh words?
    print(f"\n--- PREDECESSOR ONSET CLASS FOR ch WORDS ---")
    for sec in sections:
        sec_recs = [r for r in b_records if r['section'] == sec]
        n_sec_words = sum(len(r['words']) for r in sec_recs)
        if n_sec_words < 200:
            continue

        before_ch = Counter()
        before_sh = Counter()
        n_ch_total = 0
        n_sh_total = 0

        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(1, n):
                w = ws[i]
                w_prev = ws[i-1]
                oc = onset_class(w)
                oc_prev = onset_class(w_prev)
                if oc == 'ch':
                    before_ch[oc_prev] += 1
                    n_ch_total += 1
                elif oc == 'sh':
                    before_sh[oc_prev] += 1
                    n_sh_total += 1

        print(f"\n  Section {sec} (ch n={n_ch_total}, sh n={n_sh_total}):")
        print(f"  Top 6 predecessors of ch: {', '.join(f'{c}({v}, {100*v/max(n_ch_total,1):.1f}%)' for c,v in before_ch.most_common(6))}")
        print(f"  Top 6 predecessors of sh: {', '.join(f'{c}({v}, {100*v/max(n_sh_total,1):.1f}%)' for c,v in before_sh.most_common(6))}")

    # Conditional probability: P(next word is ch | prev is qo) vs P(next word is ch | prev is not qo)
    print(f"\n--- CONDITIONAL PROBABILITY: P(ch next | qo+gallows prev) vs P(ch next | other prev) ---")
    print(f"\n{'Section':<10} {'n_qo_ch':>8} {'n_qo':>7} {'P(ch|qo)':>10} {'n_nonqo_ch':>12} {'n_nonqo':>10} {'P(ch|nonqo)':>12} {'Ratio':>7}")

    for sec in sections:
        sec_recs = [r for r in b_records if r['section'] == sec]
        n_sec_words = sum(len(r['words']) for r in sec_recs)
        if n_sec_words < 200:
            continue

        qo_then_ch = 0
        qo_total = 0
        nonqo_then_ch = 0
        nonqo_total = 0

        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                oc_curr = onset_class(ws[i])
                oc_next = onset_class(ws[i+1])
                is_ch_next = oc_next == 'ch'
                if oc_curr == 'qo':
                    qo_total += 1
                    if is_ch_next:
                        qo_then_ch += 1
                else:
                    nonqo_total += 1
                    if is_ch_next:
                        nonqo_then_ch += 1

        p_ch_given_qo = qo_then_ch / max(qo_total, 1)
        p_ch_given_nonqo = nonqo_then_ch / max(nonqo_total, 1)
        ratio = p_ch_given_qo / max(p_ch_given_nonqo, 1e-10)
        print(f"{sec:<10} {qo_then_ch:>8} {qo_total:>7} {100*p_ch_given_qo:>9.1f}% {nonqo_then_ch:>12} {nonqo_total:>10} {100*p_ch_given_nonqo:>11.1f}% {ratio:>7.2f}×")

    # Also test: P(sh next | qo)
    print(f"\n--- CONDITIONAL PROBABILITY: P(sh next | qo+gallows prev) vs P(sh next | other prev) ---")
    print(f"\n{'Section':<10} {'n_qo_sh':>8} {'n_qo':>7} {'P(sh|qo)':>10} {'n_nonqo_sh':>12} {'n_nonqo':>10} {'P(sh|nonqo)':>12} {'Ratio':>7}")

    for sec in sections:
        sec_recs = [r for r in b_records if r['section'] == sec]
        n_sec_words = sum(len(r['words']) for r in sec_recs)
        if n_sec_words < 200:
            continue

        qo_then_sh = 0
        qo_total = 0
        nonqo_then_sh = 0
        nonqo_total = 0

        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                oc_curr = onset_class(ws[i])
                oc_next = onset_class(ws[i+1])
                is_sh_next = oc_next == 'sh'
                if oc_curr == 'qo':
                    qo_total += 1
                    if is_sh_next:
                        qo_then_sh += 1
                else:
                    nonqo_total += 1
                    if is_sh_next:
                        nonqo_then_sh += 1

        p_sh_given_qo = qo_then_sh / max(qo_total, 1)
        p_sh_given_nonqo = nonqo_then_sh / max(nonqo_total, 1)
        ratio = p_sh_given_qo / max(p_sh_given_nonqo, 1e-10)
        print(f"{sec:<10} {qo_then_sh:>8} {qo_total:>7} {100*p_sh_given_qo:>9.1f}% {nonqo_then_sh:>12} {nonqo_total:>10} {100*p_sh_given_nonqo:>11.1f}% {ratio:>7.2f}×")

    # Bonus: What onset classes most commonly FOLLOW each onset class in B?
    print(f"\n--- B-WIDE ONSET TRANSITION MATRIX (row=current onset, col=next word onset %) ---")
    onset_transitions = defaultdict(Counter)
    transition_totals = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            onset_transitions[oc1][oc2] += 1
            transition_totals[oc1] += 1

    # Print for key classes
    print_classes = ['p', 't', 'k', 'ch', 'sh', 'qo', 'd', 'y', 'o']
    header = f"{'From→':>8}"
    for oc in print_classes:
        header += f" {oc:>6}"
    header += f" {'other':>6}"
    print(header)
    for oc1 in print_classes:
        n = transition_totals[oc1]
        if n < 20:
            continue
        row = f"{oc1+'→':>8}"
        for oc2 in print_classes:
            p = onset_transitions[oc1].get(oc2, 0) / max(n, 1)
            row += f" {100*p:>5.1f}%"
        # 'other' category
        known = sum(onset_transitions[oc1].get(oc2, 0) for oc2 in print_classes)
        other_p = (n - known) / max(n, 1)
        row += f" {100*other_p:>5.1f}%"
        print(row)

if __name__ == '__main__':
    main()
