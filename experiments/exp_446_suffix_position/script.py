"""
exp_446: Suffix Type Positional Distribution (H_new_H)
Q: Do specific suffix types (aiin/edy/ol/dy/am) show position-specific
   preferences (LF/MID/LL enrichment)?

Method: ZL3B continuation lines. Decompose each word. Count suffix-type rates
at LF/MID/LL. E = suffix_rate_at_pos / suffix_rate_global.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']
SUFFIXES = [
    'aiin', 'aiir', 'ain', 'air', 'aii',
    'eedy', 'edy', 'eey', 'ey',
    'ckhy', 'ckh', 'cthy', 'cth',
    'chedy', 'chey', 'chol', 'cheol', 'cheor', 'chor', 'cho', 'ch',
    'shedy', 'shey', 'shol', 'shor', 'sho', 'sh',
    'dy', 'y',
    'ar', 'or', 'ol', 'al',
    'am', 'om',
    'iin', 'iir', 'in',
    'l', 'r', 'n',
]
SUFFIXES.sort(key=lambda x: -len(x))

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def strip_suffix(body):
    for s in SUFFIXES:
        if body.endswith(s) and len(body) > len(s):
            return body[:-len(s)], s
        elif body == s:
            return '', s
    return body, ''

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # suf_pos[dialect][pos][suffix] = count
    suf_pos = {d: {p: Counter() for p in ['LF','MID','LL','ALL']}
               for d in ['A','B']}
    # Total words per pos
    n_pos = {d: {p: 0 for p in ['LF','MID','LL','ALL']} for d in ['A','B']}

    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)

        for ci, line_words in enumerate(cont_lines):
            if ci == 0:
                pos = 'LF'
            elif ci == cn - 1:
                pos = 'LL'
            else:
                pos = 'MID'

            for word in line_words:
                onset = get_onset(word)
                if onset == 'other':
                    continue
                body = word[len(onset):]
                _, suffix = strip_suffix(body)
                suf_pos[d][pos][suffix] += 1
                suf_pos[d]['ALL'][suffix] += 1
                n_pos[d][pos] += 1
                n_pos[d]['ALL'] += 1

    # Compute enrichment by suffix type and position
    print("=== Suffix type positional enrichment (E≥1.4, global N≥50) ===\n")
    for d in ['A','B']:
        print(f"\n{d}-dialect:")
        global_total = n_pos[d]['ALL']
        # Get all suffixes with global N≥50
        major_suffixes = [s for s, cnt in suf_pos[d]['ALL'].items() if cnt >= 50]
        major_suffixes.sort(key=lambda s: -suf_pos[d]['ALL'][s])

        print(f"  {'Suffix':<8}  {'Global%':>8}  {'LF%':>6}  {'LF E':>6}  "
              f"{'MID%':>6}  {'MID E':>6}  {'LL%':>6}  {'LL E':>6}  {'Global N':>8}")

        for suf in major_suffixes:
            global_n = suf_pos[d]['ALL'][suf]
            global_rate = global_n / global_total

            rows = {}
            for pos in ['LF','MID','LL']:
                pos_n = n_pos[d][pos]
                obs = suf_pos[d][pos][suf]
                rate = obs / pos_n if pos_n > 0 else 0
                E = rate / global_rate if global_rate > 0 else 0
                rows[pos] = (rate, E, obs)

            lf_r, lf_E, lf_obs = rows['LF']
            mid_r, mid_E, mid_obs = rows['MID']
            ll_r, ll_E, ll_obs = rows['LL']

            # Only print if any position E≥1.4 or E≤0.6
            if max(lf_E, mid_E, ll_E) >= 1.4 or min(lf_E, mid_E, ll_E) <= 0.6:
                print(f"  {suf:<8}  {global_rate*100:>7.1f}%  "
                      f"{lf_r*100:>5.1f}%  {lf_E:>6.2f}×  "
                      f"{mid_r*100:>5.1f}%  {mid_E:>6.2f}×  "
                      f"{ll_r*100:>5.1f}%  {ll_E:>6.2f}×  "
                      f"{global_n:>8}")

    # Specific suffix classes: edy-class, aiin-class, ol-class, am-class, dy-class
    print("\n\n=== Suffix CLASS positional summary ===\n")

    EDY_CLASS = {'eedy', 'edy', 'eey', 'ey'}
    AIIN_CLASS = {'aiin', 'aiir', 'ain', 'air', 'aii', 'iin', 'iir', 'in'}
    OL_CLASS = {'ol', 'al', 'or', 'ar'}
    AM_CLASS = {'am', 'om'}
    DY_CLASS = {'dy', 'y'}

    CLASSES = {
        'edy-class': EDY_CLASS,
        'aiin-class': AIIN_CLASS,
        'ol-class': OL_CLASS,
        'am-class': AM_CLASS,
        'dy-class': DY_CLASS,
        'no-suffix': {''},
    }

    for d in ['A','B']:
        print(f"{d}-dialect:")
        global_total = n_pos[d]['ALL']
        print(f"  {'Class':<12}  {'Global%':>8}  {'LF E':>7}  {'MID E':>7}  {'LL E':>7}  {'LF N':>6}  {'LL N':>6}")
        for cls_name, cls_suffixes in CLASSES.items():
            global_n = sum(suf_pos[d]['ALL'].get(s, 0) for s in cls_suffixes)
            global_rate = global_n / global_total if global_total > 0 else 0
            if global_rate < 0.005:
                continue

            row = {}
            for pos in ['LF','MID','LL']:
                pos_n = n_pos[d][pos]
                obs = sum(suf_pos[d][pos].get(s, 0) for s in cls_suffixes)
                rate = obs / pos_n if pos_n > 0 else 0
                E = rate / global_rate if global_rate > 0 else 0
                row[pos] = (rate, E, obs)

            lf_r, lf_E, lf_obs = row['LF']
            mid_r, mid_E, mid_obs = row['MID']
            ll_r, ll_E, ll_obs = row['LL']

            print(f"  {cls_name:<12}  {global_rate*100:>7.1f}%  "
                  f"{lf_E:>7.2f}×  {mid_E:>7.2f}×  {ll_E:>7.2f}×  "
                  f"{lf_obs:>6}  {ll_obs:>6}")
        print()

    # Top words by position — LF, MID, LL distinct word forms
    print("\n=== Top 10 suffix types at LF vs LL ===\n")
    for d in ['A','B']:
        print(f"{d}-dialect:")
        for pos in ['LF','LL']:
            pos_total = n_pos[d][pos]
            top = suf_pos[d][pos].most_common(10)
            print(f"  {pos} (N={pos_total}):")
            for suf, cnt in top:
                suf_display = repr(suf) if suf == '' else suf
                g_cnt = suf_pos[d]['ALL'].get(suf, 0)
                g_rate = g_cnt / n_pos[d]['ALL']
                rate = cnt / pos_total
                E = rate / g_rate if g_rate > 0 else 0
                print(f"    {suf_display:<8}: {cnt:>4} ({rate*100:.1f}%)  global={g_rate*100:.1f}%  E={E:.2f}×")
        print()

if __name__ == '__main__':
    main()
