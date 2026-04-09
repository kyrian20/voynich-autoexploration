"""
exp_091: A Line Structure Deep Analysis (H158/H159)

H158: d+ch compound words in A (dchor, dchol, dchey) are A's line-initial opener system,
      analogous to y+k/t compounds in B. A uses d-prefix for line-initial marker; B uses y-prefix.
H159: Three-level positional paradigm for ch-stems in A: bare ch < ? < d+ch.
      Does d+ch in A show the same y/qo enrichment pattern as B?

Also: full characterization of A mid-line ch-onset words.
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

def is_d_ch_compound(word):
    """d-prefix + ch-stem: dchor, dchol, dchey, dcheey, etc."""
    return word.startswith('dch') and len(word) >= 4

def is_y_compound(word):
    """y-prefix + k/t/ch/sh stem."""
    if not word.startswith('y') or len(word) < 4: return False
    rest = word[1:]
    return rest.startswith('ch') or rest.startswith('sh') or rest[0] in 'kt'

def strip_d_prefix(word):
    """Strip d- prefix from d+ch compounds."""
    if word.startswith('dch'):
        return word[1:]  # returns ch+stem
    return None

def strip_y_prefix(word):
    """Strip y- prefix."""
    if word.startswith('y'): return word[1:]
    return None

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


def h158_d_ch_opener_system(a_recs, b_recs):
    """
    H158: d+ch compounds in A as line-initial opener system.
    Compare d+ch (A) vs y+k/t (B) as positional opener morphemes.
    """
    print("=== H158: d+ch Compounds in A as Line-Initial Opener System ===\n")

    # A: d+ch compound positional profile
    print("--- A dialect: d+ch compound profile ---")
    dch_types = Counter()
    dch_stats = {'total': 0, 'lf': 0, 'll': 0, 'psf': 0}
    non_dch_stats = {'total': 0, 'lf': 0, 'll': 0}

    for rec in a_recs:
        words = rec['words']
        n = len(words)
        ps = rec['is_para_start']
        for i, w in enumerate(words):
            if is_d_ch_compound(w):
                dch_stats['total'] += 1
                dch_types[w] += 1
                if i == 0:
                    dch_stats['lf'] += 1
                    if ps: dch_stats['psf'] += 1
                if i == n-1: dch_stats['ll'] += 1
            else:
                non_dch_stats['total'] += 1
                if i == 0: non_dch_stats['lf'] += 1
                if i == n-1: non_dch_stats['ll'] += 1

    dt = dch_stats['total']
    nt = non_dch_stats['total']
    print(f"  d+ch total tokens: {dt}")
    print(f"  d+ch LFirst%: {100*dch_stats['lf']/dt:.1f}% (enrichment vs background: {(dch_stats['lf']/dt)/(non_dch_stats['lf']/nt):.2f}×)")
    print(f"  d+ch LLast%: {100*dch_stats['ll']/dt:.1f}%")
    print(f"  d+ch PSFirst%: {100*dch_stats['psf']/dt:.1f}%")
    print(f"  Background LFirst%: {100*non_dch_stats['lf']/nt:.1f}%")
    print()

    print(f"  Top d+ch word types:")
    for w, c in dch_types.most_common(20):
        # Per-word stats
        wl = 0; wf = 0; wt = 0
        for rec in a_recs:
            words = rec['words']
            n = len(words)
            for i, x in enumerate(words):
                if x == w:
                    wt += 1
                    if i == 0: wf += 1
                    if i == n-1: wl += 1
        print(f"    {w}: n={wt}, LFirst={100*wf/wt:.1f}%, LLast={100*wl/wt:.1f}%")
    print()

    # Comparison: y+ch compounds in A (these also exist)
    print("--- A dialect: y+ch compound profile (comparison) ---")
    ych_types = Counter()
    ych_stats = {'total': 0, 'lf': 0, 'll': 0}
    for rec in a_recs:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w.startswith('ych') and len(w) >= 4:
                ych_stats['total'] += 1
                ych_types[w] += 1
                if i == 0: ych_stats['lf'] += 1
                if i == n-1: ych_stats['ll'] += 1
    yt = ych_stats['total']
    if yt > 0:
        print(f"  y+ch total tokens: {yt}")
        print(f"  y+ch LFirst%: {100*ych_stats['lf']/yt:.1f}%")
        print(f"  y+ch LLast%: {100*ych_stats['ll']/yt:.1f}%")
        print(f"  Top y+ch words: {ych_types.most_common(10)}")
    print()


def h159_ch_stem_positional_paradigm(a_recs):
    """
    H159: Three-level positional paradigm for ch-stems in A.
    Test: bare ch < d+ch paradigm (like bare < qo < y in B for k/t stems).
    """
    print("=== H159: ch-Stem Positional Paradigm in A ===\n")

    # Collect d+ch forms and their stems (stripping 'd')
    dch_stems = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0})
    bare_ch_stats = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0})
    dch_word_map = {}
    bare_word_map = {}

    for rec in a_recs:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if is_d_ch_compound(w):
                # stem = ch+... (strip the d)
                stem = w[1:]  # e.g., "dchor" → "chor"
                dch_stems[stem]['total'] += 1
                if i == 0: dch_stems[stem]['lf'] += 1
                if i == n-1: dch_stems[stem]['ll'] += 1
                dch_word_map[stem] = w
            elif w.startswith('ch') and not is_d_ch_compound(w):
                stem = w  # bare ch form
                bare_ch_stats[stem]['total'] += 1
                if i == 0: bare_ch_stats[stem]['lf'] += 1
                if i == n-1: bare_ch_stats[stem]['ll'] += 1
                bare_word_map[stem] = w

    # Find shared ch-stems (appear as both d+ch and bare ch)
    shared_ch = set(dch_stems.keys()) & set(bare_ch_stats.keys())
    print(f"ch-stems appearing as both d+ch and bare ch: {len(shared_ch)}")
    print()

    if shared_ch:
        print(f"{'ch-stem':<12} {'dch-form':<12} {'dch-LF%':>8} {'dch-n':>6} | {'bare-form':<12} {'bare-LF%':>8} {'bare-n':>6} | {'dch/bare ratio':>14}")
        stem_totals = [(s, dch_stems[s]['total'] + bare_ch_stats[s]['total']) for s in shared_ch]
        stem_totals.sort(key=lambda x: -x[1])
        for stem, _ in stem_totals[:20]:
            ds = dch_stems[stem]
            bs = bare_ch_stats[stem]
            d_lf = 100 * ds['lf'] / ds['total'] if ds['total'] else 0
            b_lf = 100 * bs['lf'] / bs['total'] if bs['total'] else 0
            ratio = d_lf / b_lf if b_lf > 0 else float('inf')
            print(f"  {stem:<12} {dch_word_map.get(stem,'—'):<12} {d_lf:>7.1f}% {ds['total']:>6} | {bare_word_map.get(stem,stem):<12} {b_lf:>7.1f}% {bs['total']:>6} | {ratio:>13.2f}×")

    print()
    # Aggregate stats for shared ch-stems
    if shared_ch:
        total_d_lf = sum(dch_stems[s]['lf'] for s in shared_ch)
        total_d = sum(dch_stems[s]['total'] for s in shared_ch)
        total_b_lf = sum(bare_ch_stats[s]['lf'] for s in shared_ch)
        total_b = sum(bare_ch_stats[s]['total'] for s in shared_ch)
        print(f"SHARED ch-STEMS AGGREGATE:")
        print(f"  d+ch form: LFirst={100*total_d_lf/total_d:.1f}% ({total_d_lf}/{total_d})")
        print(f"  bare ch form: LFirst={100*total_b_lf/total_b:.1f}% ({total_b_lf}/{total_b})")
        print(f"  d+ch / bare ratio: {(total_d_lf/total_d) / (total_b_lf/total_b):.2f}×")
        print()

    # Also compute: is there a y+ch compound class in A that is even MORE line-initial?
    ych_shared = {}
    for rec in a_recs:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w.startswith('ych') and len(w) >= 4:
                stem = w[1:]  # ychor → chor
                if stem not in ych_shared:
                    ych_shared[stem] = {'total': 0, 'lf': 0, 'll': 0}
                ych_shared[stem]['total'] += 1
                if i == 0: ych_shared[stem]['lf'] += 1
                if i == n-1: ych_shared[stem]['ll'] += 1

    truly_shared = set(dch_stems.keys()) & set(bare_ch_stats.keys()) & set(ych_shared.keys())
    if truly_shared:
        print("ch-stems appearing as ALL THREE: d+ch, bare ch, y+ch:")
        print(f"{'stem':<12} {'dch-LF%':>8} {'ych-LF%':>8} {'bare-LF%':>8}")
        for stem in sorted(truly_shared, key=lambda s: -(dch_stems[s]['total'] + ych_shared.get(s, {}).get('total', 0))):
            ds = dch_stems[stem]
            ys = ych_shared.get(stem, {'total': 0, 'lf': 0})
            bs = bare_ch_stats[stem]
            d_lf = 100 * ds['lf'] / ds['total'] if ds['total'] else 0
            y_lf = 100 * ys['lf'] / ys['total'] if ys['total'] else 0
            b_lf = 100 * bs['lf'] / bs['total'] if bs['total'] else 0
            print(f"  {stem:<12} {d_lf:>7.1f}% (n={ds['total']}) {y_lf:>7.1f}% (n={ys['total']}) {b_lf:>7.1f}% (n={bs['total']})")
        print()


def h160_a_mid_line_ch_analysis(a_recs):
    """
    New: What are the specific ch-onset words at A's mid-line (pos1, pos2)?
    What is the pattern of the A [opener → ch mid] → [d closer] structure?
    """
    print("=== H160: A Mid-Line ch-Onset Words and Following Patterns ===\n")

    # Words at pos1 by onset
    pos1_ch = Counter()
    pos1_non_ch = Counter()

    for rec in a_recs:
        words = rec['words']
        if len(words) < 2: continue
        w1 = words[1]
        if get_onset(w1) == 'ch':
            pos1_ch[w1] += 1
        else:
            pos1_non_ch[w1] += 1

    print(f"Top A words at pos1 (2nd position):")
    print(f"Top ch-onset at pos1:")
    for w, c in pos1_ch.most_common(15):
        print(f"  {w}: {c}")
    print(f"\nTop non-ch at pos1 (for comparison):")
    for w, c in pos1_non_ch.most_common(10):
        print(f"  {w}: {c} (onset={get_onset(w)})")
    print()

    # What word at pos0 PRECEDES ch at pos1?
    # Build pos0 → pos1 transitions for ch-onset at pos1
    opener_to_ch = Counter()
    opener_onset_to_ch = Counter()
    for rec in a_recs:
        words = rec['words']
        if len(words) < 2: continue
        w0, w1 = words[0], words[1]
        if get_onset(w1) == 'ch':
            opener_to_ch[w0] += 1
            opener_onset_to_ch[get_onset(w0)] += 1

    n_ch_mid = sum(opener_onset_to_ch.values())
    print(f"What opens A lines that have ch at pos1? (n={n_ch_mid})")
    print("By onset:")
    for onset, c in opener_onset_to_ch.most_common():
        print(f"  {onset}: {c} ({100*c/n_ch_mid:.1f}%)")
    print("Top opening words:")
    for w, c in opener_to_ch.most_common(10):
        print(f"  {w}: {c} ({100*c/n_ch_mid:.1f}%), onset={get_onset(w)}")
    print()

    # A line sequence: what FOLLOWS ch at pos1?
    ch_pos1_to_pos2 = Counter()
    for rec in a_recs:
        words = rec['words']
        if len(words) < 3: continue
        w1, w2 = words[1], words[2]
        if get_onset(w1) == 'ch':
            ch_pos1_to_pos2[get_onset(w2)] += 1
    n_ch_pos2 = sum(ch_pos1_to_pos2.values())
    print(f"After ch at pos1, what onset appears at pos2? (n={n_ch_pos2})")
    for onset, c in ch_pos1_to_pos2.most_common():
        print(f"  {onset}: {c} ({100*c/n_ch_pos2:.1f}%)")
    print()

    # Full A line: d-opener → ch-mid → d-closer template
    # Count lines fitting this pattern
    n_d_ch_d = 0
    n_d_ch_any = 0
    n_any_ch_d = 0
    for rec in a_recs:
        words = rec['words']
        n = len(words)
        if n < 3: continue
        has_d_opener = get_onset(words[0]) == 'd'
        has_ch_mid = any(get_onset(words[i]) == 'ch' for i in range(1, n-1))
        has_d_closer = get_onset(words[-1]) == 'd'
        if has_d_opener and has_ch_mid and has_d_closer:
            n_d_ch_d += 1
        if has_d_opener and has_ch_mid:
            n_d_ch_any += 1
        if has_ch_mid and has_d_closer:
            n_any_ch_d += 1

    n_total = sum(1 for r in a_recs if len(r['words']) >= 3)
    p_d_open = sum(1 for r in a_recs if len(r['words']) >= 3 and get_onset(r['words'][0]) == 'd') / n_total
    p_ch_mid = sum(1 for r in a_recs if len(r['words']) >= 3 and any(get_onset(r['words'][i]) == 'ch' for i in range(1, len(r['words'])-1))) / n_total
    p_d_close = sum(1 for r in a_recs if len(r['words']) >= 3 and get_onset(r['words'][-1]) == 'd') / n_total
    p_chance = p_d_open * p_ch_mid * p_d_close

    print(f"A line template [d-opener → ch-mid → d-closer]:")
    print(f"  n≥3-word A lines: {n_total}")
    print(f"  Observed d+ch+d template: {n_d_ch_d} ({100*n_d_ch_d/n_total:.1f}%)")
    print(f"  Expected by independence: {100*p_chance:.1f}%")
    print(f"  Template enrichment: {(n_d_ch_d/n_total)/p_chance:.2f}×")
    print(f"  d+ch (opener+mid): {n_d_ch_any} ({100*n_d_ch_any/n_total:.1f}%)")
    print(f"  ch+d (mid+closer): {n_any_ch_d} ({100*n_any_ch_d/n_total:.1f}%)")
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

    h158_d_ch_opener_system(a_recs, b_recs)
    h159_ch_stem_positional_paradigm(a_recs)
    h160_a_mid_line_ch_analysis(a_recs)

if __name__ == '__main__':
    main()
