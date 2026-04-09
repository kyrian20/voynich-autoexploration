"""
exp_072: sh→qo Coupling Analysis (H092) + Currier A Sequential Grammar (H091, H093)
H092: Is the sh→qo transition (36.6%) a tight bi-word construction or a coincidence?
H091/H093: What is Currier A's sequential grammar (onset transition matrix)?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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
    if word.startswith('a') and len(word) > 1:
        return 'a'
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

def main():
    records = parse_corpus(DATA_PATH)
    b_records = [r for r in records if r['currier'] == 'B']
    a_records = [r for r in records if r['currier'] == 'A']

    # H092: sh→qo coupling analysis
    print("="*70)
    print("H092: sh→qo COUPLING ANALYSIS IN CURRIER B")
    print("="*70)

    # Top sh-word + qo-word bigrams in B
    sh_qo_bigrams = Counter()
    sh_other_bigrams = defaultdict(Counter)  # after sh, what onset appears?
    qo_rate_by_section = {}

    onset_after_sh = Counter()
    onset_after_ch = Counter()
    onset_after_d = Counter()
    onset_after_o = Counter()
    onset_after_qo = Counter()

    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            if oc1 == 'sh':
                onset_after_sh[oc2] += 1
                if oc2 == 'qo':
                    sh_qo_bigrams[(ws[i], ws[i+1])] += 1
            elif oc1 == 'ch':
                onset_after_ch[oc2] += 1
            elif oc1 == 'd':
                onset_after_d[oc2] += 1
            elif oc1 == 'o':
                onset_after_o[oc2] += 1
            elif oc1 == 'qo':
                onset_after_qo[oc2] += 1

    # sh→qo section by section
    print(f"\n--- sh→qo RATE BY SECTION ---")
    sections = sorted(set(r['section'] for r in b_records if r['section']))
    for sec in sections:
        sec_recs = [r for r in b_records if r['section'] == sec]
        n_sh_qo = 0
        n_sh_total = 0
        n_sh_all = 0
        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                if onset_class(ws[i]) == 'sh':
                    n_sh_total += 1
                    if onset_class(ws[i+1]) == 'qo':
                        n_sh_qo += 1
            n_sh_all += sum(1 for w in ws if w.startswith('sh') and len(w) > 2)
        sec_qo_rate = sum(1 for r in sec_recs for w in r['words'] if onset_class(w) == 'qo') / max(sum(len(r['words']) for r in sec_recs), 1)
        sh_to_qo_rate = n_sh_qo / max(n_sh_total, 1)
        print(f"  {sec}: sh→qo={100*sh_to_qo_rate:.1f}% ({n_sh_qo}/{n_sh_total}), baseline qo-rate={100*sec_qo_rate:.1f}%, enrichment={sh_to_qo_rate/max(sec_qo_rate,1e-10):.2f}×")

    # Comparison: P(qo after X) for different onset classes
    print(f"\n--- P(qo NEXT) AFTER EACH ONSET CLASS ---")
    print(f"{'From onset':<12} {'n_qo_next':>10} {'n_total':>8} {'P(qo|X)':>9} {'baseline':>9} {'ratio':>7}")
    b_words = [w for r in b_records for w in r['words']]
    base_qo = sum(1 for w in b_words if onset_class(w) == 'qo') / max(len(b_words), 1)
    for oc_name, counter in [('sh', onset_after_sh), ('ch', onset_after_ch),
                              ('d', onset_after_d), ('o', onset_after_o), ('qo', onset_after_qo)]:
        n_total = sum(counter.values())
        n_qo = counter.get('qo', 0)
        if n_total < 10:
            continue
        p_qo = n_qo / n_total
        ratio = p_qo / max(base_qo, 1e-10)
        print(f"{oc_name+'→':>12} {n_qo:>10} {n_total:>8} {100*p_qo:>8.1f}% {100*base_qo:>8.1f}% {ratio:>7.2f}×")

    # Top sh-qo bigrams
    print(f"\n--- TOP sh→qo BIGRAMS (Currier B) ---")
    for (w1, w2), c in sh_qo_bigrams.most_common(20):
        print(f"  {w1} {w2}: {c}")

    # Section-level top sh→qo bigrams
    print(f"\n--- TOP sh→qo BIGRAMS BY SECTION ---")
    for sec in ['B', 'H', 'S']:
        sec_bigrams = Counter()
        sec_recs = [r for r in b_records if r['section'] == sec]
        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                if onset_class(ws[i]) == 'sh' and onset_class(ws[i+1]) == 'qo':
                    sec_bigrams[(ws[i], ws[i+1])] += 1
        print(f"\n  Section {sec}: {', '.join(f'{w1} {w2}({c})' for (w1,w2),c in sec_bigrams.most_common(8))}")

    # Is sh→qo more likely mid-line or cross-line?
    print(f"\n--- sh→qo WITHIN-LINE vs CROSS-LINE ---")
    within_line = 0
    cross_line = 0
    # All records are single-line transcriptions; cross-line means last word of line i → first word of line i+1
    # We can't easily track this without knowing which record follows which.
    # Instead, check if the sh→qo pair is within a single record vs not.
    # Since each record is one line: within-line = both words in same record.
    # Cross-line: sh is last word of line, qo is first word of next line (separate records).
    within_sh_qo = 0
    within_sh = 0
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            if onset_class(ws[i]) == 'sh':
                within_sh += 1
                if onset_class(ws[i+1]) == 'qo':
                    within_sh_qo += 1
    print(f"  Within-line sh→qo: {within_sh_qo}/{within_sh} = {100*within_sh_qo/max(within_sh,1):.1f}%")
    # Note: overall sh→qo in transition matrix was computed the same way (within-line only)
    # The cross-line transition isn't captured in this data since each record is one line

    # H091/H093: Currier A sequential grammar
    print(f"\n{'='*70}")
    print("H091/H093: CURRIER A SEQUENTIAL GRAMMAR (onset transition matrix)")
    print(f"{'='*70}")

    # A onset transition matrix
    print_classes = ['p', 't', 'k', 'ch', 'sh', 'qo', 'd', 'y', 'o', 'a']
    a_transitions = defaultdict(Counter)
    a_totals = Counter()

    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            a_transitions[oc1][oc2] += 1
            a_totals[oc1] += 1

    print(f"\n--- A ONSET TRANSITION MATRIX ---")
    header = f"{'From→':>8}"
    for oc in print_classes:
        header += f" {oc:>6}"
    header += f" {'other':>6}"
    print(header)
    for oc1 in print_classes:
        n = a_totals[oc1]
        if n < 20:
            continue
        row = f"{oc1+'→':>8}"
        for oc2 in print_classes:
            p = a_transitions[oc1].get(oc2, 0) / max(n, 1)
            row += f" {100*p:>5.1f}%"
        known = sum(a_transitions[oc1].get(oc2, 0) for oc2 in print_classes)
        other_p = (n - known) / max(n, 1)
        row += f" {100*other_p:>5.1f}%"
        print(row)

    # Top predecessors of ch in A
    print(f"\n--- TOP PREDECESSORS OF ch IN CURRIER A ---")
    before_ch_a = Counter()
    before_sh_a = Counter()
    n_ch_a = 0
    n_sh_a = 0
    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i in range(1, n):
            oc_curr = onset_class(ws[i])
            oc_prev = onset_class(ws[i-1])
            if oc_curr == 'ch':
                before_ch_a[oc_prev] += 1
                n_ch_a += 1
            elif oc_curr == 'sh':
                before_sh_a[oc_prev] += 1
                n_sh_a += 1

    print(f"  ch predecessors (n={n_ch_a}): {', '.join(f'{c}({v}, {100*v/max(n_ch_a,1):.1f}%)' for c,v in before_ch_a.most_common(8))}")
    print(f"  sh predecessors (n={n_sh_a}): {', '.join(f'{c}({v}, {100*v/max(n_sh_a,1):.1f}%)' for c,v in before_sh_a.most_common(8))}")

    # P(ch | daiin prev) in A
    a_words = [w for r in a_records for w in r['words']]
    base_ch_a = sum(1 for w in a_words if w.startswith('ch') and len(w) > 2) / max(len(a_words), 1)
    print(f"\n  A baseline ch-rate: {100*base_ch_a:.1f}%")

    # Conditional P(ch | prev onset class) in A
    print(f"\n--- P(ch NEXT) AFTER EACH ONSET CLASS IN CURRIER A ---")
    for oc in print_classes:
        n_total = a_totals[oc]
        n_ch = a_transitions[oc].get('ch', 0)
        if n_total < 20:
            continue
        p_ch = n_ch / n_total
        ratio = p_ch / max(base_ch_a, 1e-10)
        print(f"  {oc+'→':<8} ch: {n_ch}/{n_total} = {100*p_ch:.1f}% (ratio vs baseline: {ratio:.2f}×)")

    # A sequential grammar by section
    print(f"\n--- A SEQUENTIAL GRAMMAR BY SECTION ---")
    a_sections = sorted(set(r['section'] for r in a_records if r['section']))
    for sec in a_sections:
        sec_recs = [r for r in a_records if r['section'] == sec]
        n_sec = sum(len(r['words']) for r in sec_recs)
        if n_sec < 200:
            continue
        sec_before_ch = Counter()
        n_ch_sec = 0
        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(1, n):
                if onset_class(ws[i]) == 'ch':
                    sec_before_ch[onset_class(ws[i-1])] += 1
                    n_ch_sec += 1
        print(f"\n  Section {sec} (n_words={n_sec}, n_ch={n_ch_sec}):")
        print(f"  ch predecessors: {', '.join(f'{c}({v}, {100*v/max(n_ch_sec,1):.1f}%)' for c,v in sec_before_ch.most_common(5))}")

    # sh→ in A
    print(f"\n--- A: WHAT FOLLOWS sh? ---")
    a_after_sh = Counter()
    n_sh_a_total = 0
    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            if onset_class(ws[i]) == 'sh':
                a_after_sh[onset_class(ws[i+1])] += 1
                n_sh_a_total += 1
    print(f"  After sh (n={n_sh_a_total}): {', '.join(f'{c}({v}, {100*v/max(n_sh_a_total,1):.1f}%)' for c,v in a_after_sh.most_common(8))}")

if __name__ == '__main__':
    main()
