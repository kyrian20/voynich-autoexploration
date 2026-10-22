"""
exp_088: daiin-B Cross-Line Connector (H151), oly/oldy Preceding Words (H152), y-Prefix System (H153)

H151: When daiin opens a B line, does the PRECEDING line end with ch/sh words?
      Establishes daiin-B as a cross-line grammatical bridge.
H152: Do words preceding oly/oldy vs -am endings differ by onset class or form?
H153: Are y-compound words (ycheey, ykaiin) exclusively line-initial in B?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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
    if word and word[0] == 'p': return 'p'
    if word and word[0] == 't': return 't'
    if word and word[0] == 'k': return 'k'
    if word and word[0] == 'd': return 'd'
    if word and word[0] == 's': return 's'
    if word and word[0] == 'y': return 'y'
    if word and word[0] == 'o': return 'o'
    return 'other'

def is_y_compound(word):
    """y-prefix compound: y + [ch/sh/k/t] + ..."""
    if not word.startswith('y') or len(word) < 4: return False
    rest = word[1:]
    return (rest.startswith('ch') or rest.startswith('sh') or
            rest.startswith('k') or rest.startswith('t'))

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


def h151_daiin_b_cross_line_connector(b_recs):
    """
    H151: When daiin opens a B line, does the preceding line end with ch/sh words?
    """
    print("=== H151: daiin-B as Cross-Line Connector ===\n")

    # For each B line starting with daiin, examine the preceding line's last word
    daiin_openers = []  # (preceding_last_word, following_first_word, current_last_word)
    non_daiin_openers = []  # for comparison

    for i in range(1, len(b_recs)):
        rec = b_recs[i]
        prev = b_recs[i-1]
        words = rec['words']
        prev_words = prev['words']
        if not words or not prev_words: continue
        # Skip if this line is a para-start (different paragraph context)
        if rec['is_para_start']: continue

        first_word = words[0]
        prev_last = prev_words[-1]
        curr_last = words[-1]

        if first_word == 'daiin':
            daiin_openers.append({
                'prev_last': prev_last,
                'prev_last_onset': get_onset(prev_last),
                'curr_last': curr_last,
                'curr_last_onset': get_onset(curr_last),
                'section': rec['section'],
            })
        else:
            non_daiin_openers.append({
                'prev_last': prev_last,
                'prev_last_onset': get_onset(prev_last),
                'section': rec['section'],
            })

    n_daiin = len(daiin_openers)
    n_non = len(non_daiin_openers)
    print(f"daiin-opening B lines (non-para-start): {n_daiin}")
    print(f"Non-daiin B lines (non-para-start): {n_non}")
    print()

    # Preceding line's last word onset distribution
    daiin_prev_onsets = Counter(x['prev_last_onset'] for x in daiin_openers)
    non_prev_onsets = Counter(x['prev_last_onset'] for x in non_daiin_openers)
    print("Preceding line's last word onset (when daiin opens current line):")
    print(f"{'Onset':<8} {'daiin-prev%':>12} {'non-daiin-prev%':>16} {'Enrichment':>11}")
    for onset in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
        nd = daiin_prev_onsets.get(onset, 0)
        nn = non_prev_onsets.get(onset, 0)
        pd = 100 * nd / n_daiin if n_daiin else 0
        pn = 100 * nn / n_non if n_non else 0
        enrich = (pd / pn) if pn > 0 else float('inf')
        print(f"  {onset:<6} {pd:>11.1f}% {pn:>15.1f}% {enrich:>10.2f}×")
    print()

    # Top preceding last words for daiin-opening lines
    daiin_prev_words = Counter(x['prev_last'] for x in daiin_openers)
    print("Top preceding last words (when daiin opens next line):")
    for w, c in daiin_prev_words.most_common(15):
        print(f"  {w}: {c} ({100*c/n_daiin:.1f}%), onset={get_onset(w)}")
    print()

    # Current line's last word onset (what does a daiin-opened line end with?)
    daiin_curr_onsets = Counter(x['curr_last_onset'] for x in daiin_openers)
    print("daiin-opened line's last word onset:")
    for onset, c in daiin_curr_onsets.most_common():
        print(f"  {onset}: {c} ({100*c/n_daiin:.1f}%)")
    print()

    # Three-line pattern: prev_ends → daiin_opens → curr_ends
    print("Top 3-part pattern (prev_last onset → daiin[0] → curr_last onset):")
    three_patterns = Counter(
        (x['prev_last_onset'], x['curr_last_onset'])
        for x in daiin_openers
    )
    for (p, c_), count in three_patterns.most_common(10):
        print(f"  [{p}] → daiin → [{c_}]: {count} ({100*count/n_daiin:.1f}%)")
    print()


def h152_am_vs_ol_preceding_words(b_recs):
    """
    H152: What words precede -am endings vs oly/oldy endings?
    """
    print("=== H152: Preceding Words for -am vs oly/oldy Line Endings ===\n")

    AM_CORE = {'dam','otam','okam','qokam','cham','ram','qotam'}
    OL_CLOSERS = {'oly','oldy'}

    am_preceding = Counter()
    ol_preceding = Counter()
    am_preceding_onset = Counter()
    ol_preceding_onset = Counter()

    for rec in b_recs:
        words = rec['words']
        n = len(words)
        if n < 2: continue
        last = words[-1]
        second_last = words[-2]
        onset = get_onset(second_last)
        if last in AM_CORE:
            am_preceding[second_last] += 1
            am_preceding_onset[onset] += 1
        elif last in OL_CLOSERS:
            ol_preceding[second_last] += 1
            ol_preceding_onset[onset] += 1

    n_am = sum(am_preceding.values())
    n_ol = sum(ol_preceding.values())
    print(f"Lines ending with -am core (with ≥2 words): {n_am}")
    print(f"Lines ending with oly/oldy (with ≥2 words): {n_ol}")
    print()

    print("Preceding word onset distribution:")
    print(f"{'Onset':<8} {'am-prec%':>10} {'ol-prec%':>10} {'Enrichment(ol/am)':>18}")
    for onset in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
        na = am_preceding_onset.get(onset, 0)
        no = ol_preceding_onset.get(onset, 0)
        pa = 100 * na / n_am if n_am else 0
        po = 100 * no / n_ol if n_ol else 0
        enrich = (po / pa) if pa > 0 else float('inf')
        print(f"  {onset:<6} {pa:>9.1f}% {po:>9.1f}% {enrich:>17.2f}×")
    print()

    print("Top preceding words for -am endings:")
    for w, c in am_preceding.most_common(12):
        print(f"  {w}: {c} ({100*c/n_am:.1f}%), onset={get_onset(w)}")
    print()
    print("Top preceding words for oly/oldy endings:")
    for w, c in ol_preceding.most_common(12):
        print(f"  {w}: {c} ({100*c/n_ol:.1f}%), onset={get_onset(w)}")
    print()


def h153_y_compound_profile(b_recs, a_recs):
    """
    H153: Are y-compound words exclusively line-initial in B?
    Compute y-compound positional profile and compare to qo-prefix profile.
    """
    print("=== H153: y-Compound Prefix System in B ===\n")

    for dialect_name, recs in [('B', b_recs), ('A', a_recs)]:
        print(f"--- Currier {dialect_name}: y-compound word analysis ---")
        y_comp_stats = {'total': 0, 'lf': 0, 'll': 0, 'psf': 0, 'pfl': 0}
        y_comp_types = Counter()
        y_comp_followings = Counter()  # what follows y-compound at line-first?
        non_y_comp_stats = {'total': 0, 'lf': 0, 'll': 0}

        for i, rec in enumerate(recs):
            words = rec['words']
            n = len(words)
            is_ps = rec['is_para_start']
            is_pf = (i + 1 < len(recs)) and recs[i+1]['is_para_start']

            for j, w in enumerate(words):
                if is_y_compound(w):
                    y_comp_stats['total'] += 1
                    y_comp_types[w] += 1
                    if j == 0:
                        y_comp_stats['lf'] += 1
                        if is_ps: y_comp_stats['psf'] += 1
                        if len(words) > 1:
                            y_comp_followings[words[1]] += 1
                    if j == n - 1:
                        y_comp_stats['ll'] += 1
                        if is_pf: y_comp_stats['pfl'] += 1
                else:
                    non_y_comp_stats['total'] += 1
                    if j == 0: non_y_comp_stats['lf'] += 1
                    if j == n - 1: non_y_comp_stats['ll'] += 1

        yt = y_comp_stats['total']
        if yt == 0:
            print("  No y-compound tokens found.")
            continue

        print(f"  y-compound total tokens: {yt} ({100*yt/len(recs):.1f}% of lines)")
        print(f"  y-compound LFirst%: {100*y_comp_stats['lf']/yt:.1f}%")
        print(f"  y-compound LLast%: {100*y_comp_stats['ll']/yt:.1f}%")
        print(f"  y-compound PSFirst%: {100*y_comp_stats['psf']/yt:.1f}%")
        print(f"  y-compound PFLast%: {100*y_comp_stats['pfl']/yt:.1f}%")

        nt = non_y_comp_stats['total']
        print(f"\n  Non-y-compound LFirst%: {100*non_y_comp_stats['lf']/nt:.1f}% (background rate)")
        print(f"  LFirst enrichment for y-compound: {(y_comp_stats['lf']/yt) / (non_y_comp_stats['lf']/nt):.2f}×")

        print(f"\n  Top 20 y-compound word types:")
        for w, c in y_comp_types.most_common(20):
            print(f"    {w}: {c}")

        print(f"\n  When y-compound opens a line, following word:")
        total_yf = sum(y_comp_followings.values())
        onset_following = Counter()
        for w, c in y_comp_followings.items():
            onset_following[get_onset(w)] += c
        for onset, c in onset_following.most_common():
            print(f"    {onset}: {c} ({100*c/total_yf:.1f}%)")
        print(f"  Top following words: {y_comp_followings.most_common(10)}")
        print()

    # Compare y-compound vs qo-compound positional profiles
    print("--- y-compound vs qo-compound positional comparison (B) ---")
    y_stats = defaultdict(int)
    qo_stats = defaultdict(int)
    for i, rec in enumerate(b_recs):
        words = rec['words']
        n = len(words)
        is_ps = rec['is_para_start']
        is_pf = (i + 1 < len(b_recs)) and b_recs[i+1]['is_para_start']
        for j, w in enumerate(words):
            if is_y_compound(w):
                y_stats['total'] += 1
                if j == 0: y_stats['lf'] += 1
                if j == n-1: y_stats['ll'] += 1
                if j == 0 and is_ps: y_stats['psf'] += 1
            elif w.startswith('qo') and len(w) > 2:
                qo_stats['total'] += 1
                if j == 0: qo_stats['lf'] += 1
                if j == n-1: qo_stats['ll'] += 1
                if j == 0 and is_ps: qo_stats['psf'] += 1

    for name, st in [('y-compound', y_stats), ('qo-prefix', qo_stats)]:
        t = st['total']
        if t > 0:
            print(f"  {name}: total={t}, LFirst={100*st['lf']/t:.1f}%, LLast={100*st['ll']/t:.1f}%, PSFirst={100*st['psf']/t:.1f}%")
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

    h151_daiin_b_cross_line_connector(b_recs)
    h152_am_vs_ol_preceding_words(b_recs)
    h153_y_compound_profile(b_recs, a_recs)

if __name__ == '__main__':
    main()
