"""
exp_079: e-Vowel Infix Morphological Pattern (H117), A Line-Closers (H118),
         Pharma A qo Distribution (H119)

H117: Does e-vowel infix after onset (she-, che-, de-, oe-) consistently predict different sequential behavior?
H118: Does Currier A have line-closing words equivalent to B's oly/otam/okam?
H119: Is Pharma A's elevated X→qo driven by higher qo base-rate or genuine grammar?
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

def e_infix_class(word):
    """Classify word by onset + e-infix pattern."""
    # sh-forms: she- (e after sh) vs sh-other
    if word.startswith('she') and len(word) > 3:
        return ('sh', 'e')
    elif word.startswith('sh') and len(word) > 2:
        return ('sh', 'no-e')
    # ch-forms: che- (e after ch) vs ch-other
    elif word.startswith('che') and len(word) > 3:
        return ('ch', 'e')
    elif word.startswith('ch') and len(word) > 2:
        return ('ch', 'no-e')
    # d-forms: de- (e after d) vs d-other
    elif word.startswith('de') and len(word) > 2:
        return ('d', 'e')
    elif word.startswith('d') and len(word) > 1:
        return ('d', 'no-e')
    # o-forms: oe- (e after o) vs o-other
    elif word.startswith('oe') and len(word) > 2:
        return ('o', 'e')
    elif word.startswith('o') and len(word) > 1:
        return ('o', 'no-e')
    # qo-forms: qoe- (e after qo) vs qo-other
    elif word.startswith('qoe') and len(word) > 3:
        return ('qo', 'e')
    elif word.startswith('qo') and len(word) > 2:
        return ('qo', 'no-e')
    # k-forms: ke- vs k-other
    elif word.startswith('ke') and len(word) > 2:
        return ('k', 'e')
    elif word.startswith('k') and len(word) > 1:
        return ('k', 'no-e')
    return (None, None)

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
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']
    herbal_a = [r for r in a_records if r['section'] == 'H']
    pharma_a = [r for r in a_records if r['section'] == 'P']

    # ================================================================
    print("="*70)
    print("H117: e-VOWEL INFIX MORPHOLOGICAL PATTERN ACROSS ONSET CLASSES")
    print("="*70)

    for dialect_label, recs in [('Currier A', a_records), ('Currier B', b_records)]:
        all_words = [w for r in recs for w in r['words']]
        n_total = len(all_words)
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(n_total, 1)
        base_ch = sum(1 for w in all_words if onset_class(w) == 'ch') / max(n_total, 1)

        # Compute e-infix stats
        e_stats = defaultdict(lambda: {'e_n': 0, 'e_qo': 0, 'e_ch': 0,
                                        'noe_n': 0, 'noe_qo': 0, 'noe_ch': 0})
        e_words = defaultdict(Counter)
        noe_words = defaultdict(Counter)

        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                onset, has_e = e_infix_class(ws[i])
                if onset is None:
                    continue
                next_oc = onset_class(ws[i+1])
                if has_e == 'e':
                    e_stats[onset]['e_n'] += 1
                    if next_oc == 'qo':
                        e_stats[onset]['e_qo'] += 1
                    if next_oc == 'ch':
                        e_stats[onset]['e_ch'] += 1
                    e_words[onset][ws[i]] += 1
                else:
                    e_stats[onset]['noe_n'] += 1
                    if next_oc == 'qo':
                        e_stats[onset]['noe_qo'] += 1
                    if next_oc == 'ch':
                        e_stats[onset]['noe_ch'] += 1
                    noe_words[onset][ws[i]] += 1

        print(f"\n{dialect_label} (base qo={100*base_qo:.1f}%, ch={100*base_ch:.1f}%):")
        print(f"  {'Onset':<6} {'e-forms count':>14} {'e-→qo':>8} {'enr_qo':>8} {'e-→ch':>8} {'enr_ch':>8} {'noe-→qo':>9} {'noe_enr':>8} top-e-words")
        for onset in ['sh', 'ch', 'd', 'o', 'qo', 'k']:
            s = e_stats[onset]
            if s['e_n'] < 5:
                continue
            e_qo_p = s['e_qo'] / max(s['e_n'], 1)
            e_ch_p = s['e_ch'] / max(s['e_n'], 1)
            noe_qo_p = s['noe_qo'] / max(s['noe_n'], 1)
            e_enr_qo = e_qo_p / max(base_qo, 1e-10)
            e_enr_ch = e_ch_p / max(base_ch, 1e-10)
            noe_enr_qo = noe_qo_p / max(base_qo, 1e-10)
            top_e = [w for w, _ in e_words[onset].most_common(3)]
            print(f"  {onset:<6} {s['e_n']:>14} {100*e_qo_p:>7.1f}% {e_enr_qo:>7.2f}× {100*e_ch_p:>7.1f}% {e_enr_ch:>7.2f}× {100*noe_qo_p:>8.1f}% {noe_enr_qo:>7.2f}× {top_e}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H118: CURRIER A LINE-CLOSING WORDS (≥60% LINE-FINAL)")
    print(f"{'='*70}")

    # Find A words with high line-final rate
    a_word_first = Counter()
    a_word_mid = Counter()
    a_word_last = Counter()
    a_word_total = Counter()

    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            a_word_total[w] += 1
            if i == 0:
                a_word_first[w] += 1
            elif i == n - 1:
                a_word_last[w] += 1
            else:
                a_word_mid[w] += 1

    n_a_total = sum(a_word_total.values())
    a_word_freq = Counter(a_word_total)

    print(f"\nCurrier A words with ≥60% line-final rate and ≥10 occurrences:")
    print(f"  {'Word':<15} {'Total':>7} {'Last':>6} {'Last%':>7} {'Onset':>7} {'Preceding onset (most common)':>30}")
    line_closers_a = []
    for word, total in a_word_freq.most_common():
        if total < 10:
            break
        last = a_word_last.get(word, 0)
        last_pct = 100 * last / max(total, 1)
        if last_pct >= 60:
            line_closers_a.append((word, total, last, last_pct))

    # For each line closer, find preceding onset
    preceding_a = defaultdict(Counter)
    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i in range(1, n):
            if a_word_last.get(ws[i], 0) / max(a_word_total.get(ws[i], 1), 1) >= 0.60 and a_word_total.get(ws[i], 0) >= 10:
                preceding_a[ws[i]][onset_class(ws[i-1])] += 1

    for word, total, last, last_pct in sorted(line_closers_a, key=lambda x: -x[3])[:30]:
        oc = onset_class(word)
        top_prec = [f"{oc}({c})" for oc, c in preceding_a[word].most_common(2)]
        print(f"  {word:<15} {total:>7} {last:>6} {last_pct:>6.1f}% {oc:>7} {', '.join(top_prec)}")

    # Also find B line closers for comparison
    print(f"\nCurrier B words with ≥60% line-final rate and ≥10 occurrences:")
    b_word_first = Counter()
    b_word_mid = Counter()
    b_word_last = Counter()
    b_word_total = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            b_word_total[w] += 1
            if i == 0:
                b_word_first[w] += 1
            elif i == n - 1:
                b_word_last[w] += 1
            else:
                b_word_mid[w] += 1

    line_closers_b = []
    for word, total in b_word_total.most_common():
        if total < 10:
            break
        last = b_word_last.get(word, 0)
        last_pct = 100 * last / max(total, 1)
        if last_pct >= 60:
            line_closers_b.append((word, total, last, last_pct))

    print(f"  {'Word':<15} {'Total':>7} {'Last':>6} {'Last%':>7} {'Onset':>7}")
    for word, total, last, last_pct in sorted(line_closers_b, key=lambda x: -x[3])[:30]:
        oc = onset_class(word)
        print(f"  {word:<15} {total:>7} {last:>6} {last_pct:>6.1f}% {oc:>7}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H119: PHARMA A qo DISTRIBUTION AND GRAMMAR EFFECTS")
    print(f"{'='*70}")

    for label, recs in [('Herbal A', herbal_a), ('Pharma A', pharma_a), ('Currier B', b_records)]:
        all_words = [w for r in recs for w in r['words']]
        n_total = len(all_words)
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(n_total, 1)

        # Compute P(qo_next | X) for each onset class
        transitions = defaultdict(Counter)
        totals = Counter()
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                oc1 = onset_class(ws[i])
                oc2 = onset_class(ws[i+1])
                transitions[oc1][oc2] += 1
                totals[oc1] += 1

        print(f"\n{label}: base_qo={100*base_qo:.1f}%")
        print(f"  {'Onset':<8} {'n':>6} {'→qo':>8} {'enr_qo':>8}")
        for oc in ['sh', 'ch', 'o', 'd', 's', 'y', 'k', 'qo']:
            n = totals.get(oc, 0)
            if n < 10:
                continue
            p_qo = transitions[oc].get('qo', 0) / max(n, 1)
            enr = p_qo / max(base_qo, 1e-10)
            print(f"  {oc+'→':<8} {n:>6} {100*p_qo:>7.1f}% {enr:>7.2f}×")

        # qo word distribution in Pharma A vs Herbal A
        qo_words = Counter(w for w in all_words if onset_class(w) == 'qo')
        n_qo = sum(qo_words.values())
        print(f"  Top qo-words: {list(qo_words.most_common(8))}")

if __name__ == '__main__':
    main()
