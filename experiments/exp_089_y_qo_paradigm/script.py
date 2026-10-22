"""
exp_089: y+{stem} vs qo+{stem} Positional Paradigm (H154), B Line Structure Template (H155)

H154: y+{stem} (line-initial) and qo+{stem} (mid-line) are alternants of the same stem.
H155: How many B lines follow the full [y/s opener → qo mid → -am/oly closer] template?
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
    for c in 'ptksyd':
        if word.startswith(c): return c
    if word.startswith('o'): return 'o'
    return 'other'

def is_y_compound(word):
    """y-prefix compound: y + [ch/sh/k/t] + ..."""
    if not word.startswith('y') or len(word) < 4: return False
    rest = word[1:]
    return rest.startswith('ch') or rest.startswith('sh') or rest[0] in 'kt'

def is_s_opener(word):
    return word.startswith('s') and not word.startswith('sh') and len(word) >= 3

def is_qo_compound(word):
    return word.startswith('qo') and len(word) > 2

def is_am_closer(word):
    return word.endswith('am') and len(word) > 2

def is_ol_closer(word):
    return word in {'oly', 'oldy'}

def strip_y_prefix(word):
    """Strip y- prefix from y-compound words."""
    if not word.startswith('y'): return None
    rest = word[1:]
    # If starts with ch/sh, stem starts at index 0 of rest
    return rest

def strip_qo_prefix(word):
    """Strip qo- prefix."""
    if word.startswith('qo') and len(word) > 2:
        return word[2:]
    return None

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


def h154_y_qo_positional_paradigm(b_recs, a_recs):
    """
    H154: y+{stem} and qo+{stem} are line-position alternants.
    For each shared stem (appears as both y+stem and qo+stem):
    - Compare LFirst% for y-form vs qo-form
    """
    print("=== H154: y+{stem} vs qo+{stem} Positional Paradigm ===\n")

    for dialect_name, recs in [('B', b_recs), ('A', a_recs)]:
        print(f"--- Currier {dialect_name}: y vs qo stem alternation ---")

        # Collect y-forms and qo-forms with their positions
        y_stems = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0})  # stem -> stats
        qo_stems = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0})  # stem -> stats
        y_word_map = defaultdict(str)   # stem -> full y-word
        qo_word_map = defaultdict(str)  # stem -> full qo-word

        for rec in recs:
            words = rec['words']
            n = len(words)
            for i, w in enumerate(words):
                y_stem = strip_y_prefix(w) if is_y_compound(w) else None
                qo_stem = strip_qo_prefix(w) if is_qo_compound(w) else None

                if y_stem:
                    y_stems[y_stem]['total'] += 1
                    if i == 0: y_stems[y_stem]['lf'] += 1
                    if i == n-1: y_stems[y_stem]['ll'] += 1
                    if not y_word_map[y_stem]: y_word_map[y_stem] = w

                if qo_stem:
                    qo_stems[qo_stem]['total'] += 1
                    if i == 0: qo_stems[qo_stem]['lf'] += 1
                    if i == n-1: qo_stems[qo_stem]['ll'] += 1
                    if not qo_word_map[qo_stem]: qo_word_map[qo_stem] = w

        # Find shared stems
        shared_stems = set(y_stems.keys()) & set(qo_stems.keys())
        print(f"  Stems appearing as both y+stem and qo+stem: {len(shared_stems)}")
        print()

        if shared_stems:
            print(f"  {'Stem':<12} {'y-form':<12} {'y-LF%':>7} {'y-n':>5} | {'qo-form':<12} {'qo-LF%':>8} {'qo-n':>5} | {'y/qo LF ratio':>14}")
            # Sort by stem total frequency
            stem_totals = [(s, y_stems[s]['total'] + qo_stems[s]['total']) for s in shared_stems]
            stem_totals.sort(key=lambda x: -x[1])
            for stem, _ in stem_totals[:25]:
                ys = y_stems[stem]
                qs = qo_stems[stem]
                y_lf = 100 * ys['lf'] / ys['total'] if ys['total'] else 0
                q_lf = 100 * qs['lf'] / qs['total'] if qs['total'] else 0
                ratio = y_lf / q_lf if q_lf > 0 else float('inf')
                print(f"  {stem:<12} {y_word_map[stem]:<12} {y_lf:>6.1f}% {ys['total']:>5} | {qo_word_map[stem]:<12} {q_lf:>7.1f}% {qs['total']:>5} | {ratio:>13.2f}×")
            print()

        # Aggregate stats for shared stems
        if shared_stems:
            total_y_lf = sum(y_stems[s]['lf'] for s in shared_stems)
            total_y = sum(y_stems[s]['total'] for s in shared_stems)
            total_qo_lf = sum(qo_stems[s]['lf'] for s in shared_stems)
            total_qo = sum(qo_stems[s]['total'] for s in shared_stems)
            print(f"  SHARED STEMS AGGREGATE:")
            print(f"    y+stem: LFirst={100*total_y_lf/total_y:.1f}% ({total_y_lf}/{total_y})")
            print(f"    qo+stem: LFirst={100*total_qo_lf/total_qo:.1f}% ({total_qo_lf}/{total_qo})")
            print(f"    y/qo LFirst ratio: {(total_y_lf/total_y)/(total_qo_lf/total_qo):.2f}×")
            print()

        # Also check: do y-stems appear UNATTACHED (as bare stems)?
        bare_stem_stats = defaultdict(lambda: {'total': 0, 'lf': 0})
        for rec in recs:
            words = rec['words']
            n = len(words)
            for i, w in enumerate(words):
                if w in y_stems and not is_y_compound(w) and not is_qo_compound(w):
                    bare_stem_stats[w]['total'] += 1
                    if i == 0: bare_stem_stats[w]['lf'] += 1
        if bare_stem_stats:
            total_bare_lf = sum(v['lf'] for v in bare_stem_stats.values())
            total_bare = sum(v['total'] for v in bare_stem_stats.values())
            if total_bare > 0:
                print(f"  Bare stems (no prefix): n={total_bare}, LFirst%={100*total_bare_lf/total_bare:.1f}%")
        print()


def h155_b_line_structure_template(b_recs):
    """
    H155: What fraction of B lines follow [opener → qo-mid → closer]?
    Also: partial matches and section breakdown.
    """
    print("=== H155: B Line Structure Template Analysis ===\n")

    AM_CORE = {'dam','otam','okam','qokam','cham','ram','qotam'}
    OL_CLOSERS = {'oly','oldy'}

    template_counts = Counter()
    section_template = defaultdict(Counter)

    for rec in b_recs:
        words = rec['words']
        n = len(words)
        if n < 2: continue

        # Classify line opener (position 0)
        first = words[0]
        has_opener = is_y_compound(first) or is_s_opener(first)

        # Classify line closer (position n-1)
        last = words[-1]
        has_am_closer = last in AM_CORE
        has_ol_closer = last in OL_CLOSERS
        has_closer = has_am_closer or has_ol_closer

        # Classify mid-line (positions 1 to n-2 for qo-prefix)
        has_qo_mid = any(is_qo_compound(words[i]) for i in range(1, n-1)) if n >= 3 else False
        has_daiin_opener = first == 'daiin'

        # Build template code
        template = []
        if has_opener: template.append('opener')
        if has_daiin_opener: template.append('daiin-opener')
        if has_qo_mid: template.append('qo-mid')
        if has_am_closer: template.append('am-close')
        elif has_ol_closer: template.append('ol-close')

        template_str = '+'.join(template) if template else 'none'
        template_counts[template_str] += 1

        # Full template
        full = has_opener and has_qo_mid and has_closer
        partial_opener_closer = has_opener and has_closer and not has_qo_mid
        partial_opener_qo = has_opener and has_qo_mid and not has_closer
        partial_qo_closer = not has_opener and has_qo_mid and has_closer

        for key, cond in [
            ('full_template', full),
            ('opener_closer_only', partial_opener_closer),
            ('opener_qo_only', partial_opener_qo),
            ('qo_closer_only', partial_qo_closer),
            ('has_opener', has_opener),
            ('has_qo_mid', has_qo_mid),
            ('has_closer', has_closer),
            ('has_daiin_opener', has_daiin_opener),
            ('none_of_above', not has_opener and not has_qo_mid and not has_closer and not has_daiin_opener),
        ]:
            if cond:
                section_template[rec['section']][key] += 1

    n_b = len(b_recs)
    print(f"Total B lines: {n_b}")
    print()

    # Summary stats
    for key in ['has_opener', 'has_qo_mid', 'has_closer', 'has_daiin_opener',
                'full_template', 'opener_closer_only', 'opener_qo_only', 'qo_closer_only', 'none_of_above']:
        total = sum(s.get(key, 0) for s in section_template.values())
        print(f"  {key}: {total} ({100*total/n_b:.1f}%)")
    print()

    # Top template combinations
    print("Top template combinations:")
    for tmpl, count in template_counts.most_common(20):
        print(f"  {tmpl}: {count} ({100*count/n_b:.1f}%)")
    print()

    # Section breakdown for full template
    print("Full template [opener+qo-mid+closer] by section:")
    for sect in sorted(section_template.keys()):
        n_full = section_template[sect].get('full_template', 0)
        n_sect = sum(1 for r in b_recs if r['section'] == sect)
        if n_sect > 0:
            print(f"  {sect}: {n_full}/{n_sect} ({100*n_full/n_sect:.1f}%)")
    print()

    # Chance baseline: what % would we expect if components were independent?
    n_opener = sum(1 for r in b_recs if r['words'] and (is_y_compound(r['words'][0]) or is_s_opener(r['words'][0])))
    n_qo = sum(1 for r in b_recs if len(r['words']) >= 3 and any(is_qo_compound(r['words'][i]) for i in range(1, len(r['words'])-1)))
    n_closer = sum(1 for r in b_recs if r['words'] and (r['words'][-1] in AM_CORE or r['words'][-1] in OL_CLOSERS))
    p_opener = n_opener / n_b
    p_qo = n_qo / n_b
    p_closer = n_closer / n_b
    p_chance = p_opener * p_qo * p_closer
    n_full_template = sum(s.get('full_template', 0) for s in section_template.values())
    print(f"Observed full template rate: {100*n_full_template/n_b:.1f}%")
    print(f"Expected by independence: {100*p_chance:.1f}% (opener={100*p_opener:.1f}% × qo-mid={100*p_qo:.1f}% × closer={100*p_closer:.1f}%)")
    print(f"Template enrichment: {(n_full_template/n_b) / p_chance:.2f}× above chance")
    print()

    # Also look at 2-word mini-lines: opener → closer (no room for qo-mid)
    print("Two-word lines with opener+closer (direct):")
    n_two_word_match = sum(1 for r in b_recs if len(r['words']) == 2
                           and (is_y_compound(r['words'][0]) or is_s_opener(r['words'][0]))
                           and (r['words'][-1] in AM_CORE or r['words'][-1] in OL_CLOSERS))
    n_two_word = sum(1 for r in b_recs if len(r['words']) == 2)
    print(f"  2-word lines total: {n_two_word}, with opener+closer: {n_two_word_match} ({100*n_two_word_match/max(n_two_word,1):.1f}%)")
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

    h154_y_qo_positional_paradigm(b_recs, a_recs)
    h155_b_line_structure_template(b_recs)

if __name__ == '__main__':
    main()
