"""
exp_090: Grammar Model Falsification Test (H146), A Line Structure Analysis (H156/H157)

H146: Use positional grammar models to PREDICT paragraph structure in held-out sections.
      Evaluate precision/recall against actual locus-code para-start markers.
H156/H157: A line structure — onset profiles by position within line; d-onset as A line-closer?
"""

import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def folio_base(folio):
    return folio.split('.')[0]

def is_para_start(locus_code):
    return locus_code.lstrip('+*=/~&').startswith('@')

def is_body(locus_code):
    return locus_code.lstrip('+*@=/~&').startswith('P')

def get_onset(word):
    if word.startswith('qo'): return 'qo'
    if word.startswith('ch'): return 'ch'
    if word.startswith('sh'): return 'sh'
    for c in 'ptksyd':
        if word.startswith(c): return c
    if word.startswith('o'): return 'o'
    return 'other'

def is_y_compound(word):
    if not word.startswith('y') or len(word) < 4: return False
    rest = word[1:]
    return rest.startswith('ch') or rest.startswith('sh') or rest[0] in 'kt'

def is_she_word(word):
    return word.startswith('she') and len(word) > 3

def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m: return 'unknown'
    n = int(m.group(1))
    if n <= 57: return 'herbal'
    if 67 <= n <= 73: return 'astro'
    if 75 <= n <= 84: return 'cosmo'
    if 87 <= n <= 102: return 'pharma'
    if 103 <= n <= 116: return 'stars'
    return 'other'

def parse_voynich(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<([^>]+)>', line)
            if not m: continue
            locus_raw = m.group(1)
            text = line[m.end():].strip()
            parts = locus_raw.split(',')
            if len(parts) < 2: continue
            folio_raw = parts[0]
            locus_code = parts[1]
            folio = folio_raw.lstrip('+*=&~')
            if not is_body(locus_code): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            fb = folio_base(folio)
            records.append({
                'folio': fb,
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start(locus_code),
                'section': classify_section(fb),
            })
    return records

def compute_edy_rates(records):
    folio_words = defaultdict(list)
    for rec in records:
        folio_words[rec['folio']].extend(rec['words'])
    return {f: sum(1 for w in ws if w.endswith('edy') or w.endswith('eedy')) / len(ws)
            for f, ws in folio_words.items() if ws}

def assign_dialects(records, edy_map):
    for rec in records:
        rec['is_b'] = edy_map.get(rec['folio'], 0) >= 0.05
    return records

def classify_para_boundary(records):
    for i, rec in enumerate(records):
        rec['is_para_final'] = (i + 1 < len(records)) and records[i+1]['is_para_start']
    return records

def precision_recall_f1(tp, fp, fn):
    p = tp / (tp + fp) if (tp + fp) > 0 else 0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
    return p, r, f1


def h146_grammar_falsification(records):
    """
    H146: Can grammar models predict paragraph structure?
    
    A Model predictions:
    1. she-prefix first word → PREDICT para-start
    2. daiin as last word → PREDICT para-final
    
    B Model predictions:
    1. o-onset first word → PREDICT para-start
    2. -am (dam/otam/okam) as last word → NOT para-final (within-para line-closer)
    
    Evaluate on ALL data (no separate train/test — we test predictive accuracy of the models).
    """
    print("=== H146: Grammar Model Falsification Test ===\n")

    a_recs = [r for r in records if not r['is_b']]
    b_recs = [r for r in records if r['is_b']]

    # A DIALECT MODELS
    print("--- A Dialect: Para-Start Prediction (she-prefix as first word) ---")
    # Predictor: she-prefix first word
    tp, fp, fn, tn = 0, 0, 0, 0
    for rec in a_recs:
        words = rec['words']
        actual_ps = rec['is_para_start']
        predicted_ps = words and is_she_word(words[0])
        if predicted_ps and actual_ps: tp += 1
        elif predicted_ps and not actual_ps: fp += 1
        elif not predicted_ps and actual_ps: fn += 1
        else: tn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    base_rate = sum(1 for r in a_recs if r['is_para_start']) / len(a_recs)
    print(f"  Base rate: {100*base_rate:.1f}%, Precision: {100*p:.1f}%, Recall: {100*r:.1f}%, F1: {100*f1:.1f}%")
    print(f"  TP={tp}, FP={fp}, FN={fn}, TN={tn}")
    print(f"  Precision enrichment over base: {p/base_rate:.2f}×")
    print()

    print("--- A Dialect: Para-Final Prediction (daiin as last word) ---")
    tp, fp, fn, tn = 0, 0, 0, 0
    for rec in a_recs:
        words = rec['words']
        actual_pf = rec['is_para_final']
        predicted_pf = words and words[-1] == 'daiin'
        if predicted_pf and actual_pf: tp += 1
        elif predicted_pf and not actual_pf: fp += 1
        elif not predicted_pf and actual_pf: fn += 1
        else: tn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    base_rate = sum(1 for r in a_recs if r['is_para_final']) / len(a_recs)
    print(f"  Base rate: {100*base_rate:.1f}%, Precision: {100*p:.1f}%, Recall: {100*r:.1f}%, F1: {100*f1:.1f}%")
    print(f"  TP={tp}, FP={fp}, FN={fn}, TN={tn}")
    print(f"  Precision enrichment over base: {p/base_rate:.2f}×")
    print()

    # B DIALECT MODELS
    print("--- B Dialect: Para-Start Prediction (o-onset as first word) ---")
    tp, fp, fn, tn = 0, 0, 0, 0
    for rec in b_recs:
        words = rec['words']
        actual_ps = rec['is_para_start']
        predicted_ps = words and get_onset(words[0]) == 'o'
        if predicted_ps and actual_ps: tp += 1
        elif predicted_ps and not actual_ps: fp += 1
        elif not predicted_ps and actual_ps: fn += 1
        else: tn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    base_rate = sum(1 for r in b_recs if r['is_para_start']) / len(b_recs)
    print(f"  Base rate: {100*base_rate:.1f}%, Precision: {100*p:.1f}%, Recall: {100*r:.1f}%, F1: {100*f1:.1f}%")
    print(f"  TP={tp}, FP={fp}, FN={fn}, TN={tn}")
    print(f"  Precision enrichment over base: {p/base_rate:.2f}×")
    print()

    # Try compound predictor: o-onset LONG first word
    print("--- B Dialect: Para-Start Prediction (olfchedy/olkey-type: o-onset long word) ---")
    tp, fp, fn, tn = 0, 0, 0, 0
    for rec in b_recs:
        words = rec['words']
        actual_ps = rec['is_para_start']
        # Long o-onset first word (len >= 6) with edy/dy suffix
        predicted_ps = (words and get_onset(words[0]) == 'o' and len(words[0]) >= 6 and
                       (words[0].endswith('edy') or words[0].endswith('dy')))
        if predicted_ps and actual_ps: tp += 1
        elif predicted_ps and not actual_ps: fp += 1
        elif not predicted_ps and actual_ps: fn += 1
        else: tn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    base_rate_b = sum(1 for r in b_recs if r['is_para_start']) / len(b_recs)
    print(f"  Precision: {100*p:.1f}%, Recall: {100*r:.1f}%, F1: {100*f1:.1f}%")
    print(f"  TP={tp}, FP={fp}, FN={fn}")
    print(f"  Precision enrichment: {p/base_rate_b:.2f}×")
    print()

    # Combine predictors for B para-start
    print("--- B Dialect: Para-Start Compound Prediction (olfchedy OR olkey OR opchedy) ---")
    TOP_B_PS_WORDS = {'olfchedy', 'olkey', 'opchedy', 'opaiin', 'olkeeey', 'olar'}
    tp, fp, fn, tn = 0, 0, 0, 0
    for rec in b_recs:
        words = rec['words']
        actual_ps = rec['is_para_start']
        predicted_ps = words and words[0] in TOP_B_PS_WORDS
        if predicted_ps and actual_ps: tp += 1
        elif predicted_ps and not actual_ps: fp += 1
        elif not predicted_ps and actual_ps: fn += 1
        else: tn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    print(f"  Precision: {100*p:.1f}%, Recall: {100*r:.1f}%, F1: {100*f1:.1f}%")
    print(f"  TP={tp}, FP={fp}, FN={fn}")
    print(f"  Precision enrichment: {p/base_rate_b:.2f}×")
    print()

    # Section-specific evaluation
    print("--- Section-Specific A Para-Start (she-prefix predictor) ---")
    for sect in ['herbal', 'pharma', 'astro', 'other']:
        sect_recs = [r for r in a_recs if r['section'] == sect]
        if len(sect_recs) < 30: continue
        tp, fp, fn = 0, 0, 0
        for rec in sect_recs:
            words = rec['words']
            actual_ps = rec['is_para_start']
            predicted_ps = words and is_she_word(words[0])
            if predicted_ps and actual_ps: tp += 1
            elif predicted_ps and not actual_ps: fp += 1
            elif not predicted_ps and actual_ps: fn += 1
        p, r, f1 = precision_recall_f1(tp, fp, fn)
        n_ps = sum(1 for r in sect_recs if r['is_para_start'])
        base = n_ps / len(sect_recs)
        print(f"  {sect} (n={len(sect_recs)}, ps={n_ps}, base={100*base:.1f}%): P={100*p:.1f}%, R={100*r:.1f}%, F1={100*f1:.1f}%, enrich={p/base:.2f}×")
    print()

    # Combined model: she-prefix OR o-onset (cross-dialect)
    print("--- Cross-Dialect Para-Start Model (she-prefix for A, o-onset for B) ---")
    combined_recs = records
    tp, fp, fn = 0, 0, 0
    for rec in combined_recs:
        words = rec['words']
        actual_ps = rec['is_para_start']
        if not rec['is_b']:  # A dialect
            predicted_ps = words and is_she_word(words[0])
        else:  # B dialect
            predicted_ps = words and get_onset(words[0]) == 'o'
        if predicted_ps and actual_ps: tp += 1
        elif predicted_ps and not actual_ps: fp += 1
        elif not predicted_ps and actual_ps: fn += 1
    p, r, f1 = precision_recall_f1(tp, fp, fn)
    base = sum(1 for r in records if r['is_para_start']) / len(records)
    print(f"  Combined: P={100*p:.1f}%, R={100*r:.1f}%, F1={100*f1:.1f}%, base={100*base:.1f}%")
    print(f"  Precision enrichment: {p/base:.2f}×, TP={tp}, FP={fp}, FN={fn}")
    print()


def h156_a_line_structure(a_recs):
    """
    H156/H157: A line structure — onset profiles by word position within line.
    What are the typical A line-openers and line-closers?
    """
    print("=== H156/H157: A Line Structure — Position-Specific Onset Profiles ===\n")

    # Compute onset rate at each position (1st, 2nd, 3rd, penultimate, last)
    # Also look at position fractions
    pos_onset = defaultdict(lambda: defaultdict(int))  # position_label -> onset -> count
    pos_total = defaultdict(int)

    for rec in a_recs:
        words = rec['words']
        n = len(words)
        if n == 0: continue

        for i, w in enumerate(words):
            onset = get_onset(w)
            # Absolute positions
            if i == 0: pos_onset['pos0'][onset] += 1; pos_total['pos0'] += 1
            elif i == 1 and n > 1: pos_onset['pos1'][onset] += 1; pos_total['pos1'] += 1
            elif i == 2 and n > 2: pos_onset['pos2'][onset] += 1; pos_total['pos2'] += 1
            # Relative to end
            if i == n-1: pos_onset['last'][onset] += 1; pos_total['last'] += 1
            elif i == n-2 and n > 1: pos_onset['2nd-last'][onset] += 1; pos_total['2nd-last'] += 1

    print(f"A onset % by line position:")
    print(f"{'Onset':<8} {'pos0':>6} {'pos1':>6} {'pos2':>6} {'2nd-last':>9} {'last':>6}")
    for onset in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
        vals = []
        for pos in ['pos0','pos1','pos2','2nd-last','last']:
            n = pos_total[pos]
            c = pos_onset[pos].get(onset, 0)
            vals.append(f"{100*c/n:>5.1f}%" if n > 0 else "   —  ")
        print(f"  {onset:<6} {' '.join(vals)}")
    print()

    # Top words at each position in A
    for pos_label in ['pos0', 'last', '2nd-last']:
        print(f"Top A words at {pos_label}:")
        word_count = Counter()
        for rec in a_recs:
            words = rec['words']
            n = len(words)
            if pos_label == 'pos0' and n >= 1:
                word_count[words[0]] += 1
            elif pos_label == 'last' and n >= 1:
                word_count[words[-1]] += 1
            elif pos_label == '2nd-last' and n >= 2:
                word_count[words[-2]] += 1
        for w, c in word_count.most_common(12):
            print(f"  {w}: {c} ({100*c/pos_total.get(pos_label,1):.1f}%), onset={get_onset(w)}")
        print()

    # d-onset A: is it specifically a line-closer?
    print("--- d-onset A: word-level positional profile ---")
    d_words_stats = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0, 'mid': 0})
    for rec in a_recs:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if get_onset(w) == 'd':
                d_words_stats[w]['total'] += 1
                if i == 0: d_words_stats[w]['lf'] += 1
                elif i == n-1: d_words_stats[w]['ll'] += 1
                else: d_words_stats[w]['mid'] += 1
    # Sort by total frequency
    d_sorted = sorted(d_words_stats.items(), key=lambda x: -x[1]['total'])
    print(f"{'Word':<12} {'n':>5} {'LFirst%':>8} {'LLast%':>7} {'Mid%':>6}")
    for w, s in d_sorted[:15]:
        t = s['total']
        print(f"  {w:<10} {t:>5} {100*s['lf']/t:>7.1f}% {100*s['ll']/t:>6.1f}% {100*s['mid']/t:>5.1f}%")
    print()

    # Compare to B d-onset pattern
    print("--- Comparing A vs B d-onset positional role ---")
    for dialect, recs in [('A', a_recs)]:
        d_total = sum(1 for r in recs for w in r['words'] if get_onset(w) == 'd')
        d_ll = sum(1 for r in recs for i, w in enumerate(r['words'])
                   if get_onset(w) == 'd' and i == len(r['words'])-1)
        d_lf = sum(1 for r in recs for i, w in enumerate(r['words'])
                   if get_onset(w) == 'd' and i == 0)
        print(f"  {dialect}: d-onset n={d_total}, LFirst={100*d_lf/d_total:.1f}%, LLast={100*d_ll/d_total:.1f}%")

    # A line-opening words specific analysis
    print("\n--- A Para-Start line openers (what opens para-start lines in A?) ---")
    ps_openers = Counter()
    non_ps_openers = Counter()
    for rec in a_recs:
        words = rec['words']
        if not words: continue
        first = words[0]
        if rec['is_para_start']:
            ps_openers[first] += 1
        else:
            non_ps_openers[first] += 1
    n_ps = sum(ps_openers.values())
    n_non = sum(non_ps_openers.values())
    print(f"Top A para-start line openers (n={n_ps} para-starts):")
    for w, c in ps_openers.most_common(15):
        non_c = non_ps_openers.get(w, 0)
        ps_rate = c / n_ps
        non_rate = non_c / n_non if n_non else 0
        enrich = ps_rate / non_rate if non_rate > 0 else float('inf')
        print(f"  {w}: ps={c}({100*ps_rate:.1f}%), non-ps={non_c}({100*non_rate:.1f}%), enrich={enrich:.1f}×")
    print()


def main():
    print("Loading data...")
    records = parse_voynich(DATA_PATH)
    edy_map = compute_edy_rates(records)
    records = assign_dialects(records, edy_map)
    records = classify_para_boundary(records)
    a_recs = [r for r in records if not r['is_b']]
    b_recs = [r for r in records if r['is_b']]
    print(f"Total body records: {len(records)}")
    print(f"A: {len(a_recs)}, B: {len(b_recs)}\n")

    h146_grammar_falsification(records)
    h156_a_line_structure(a_recs)

if __name__ == '__main__':
    main()
