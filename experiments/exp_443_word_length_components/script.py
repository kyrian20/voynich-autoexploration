"""
exp_443: Word-Length Component Analysis (H494)
Measure onset/midfix/suffix component lengths in VMS corpus by dialect/position.
Target: identify which component drives the 22% length overproduction in simulation (exp_217).
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter
import statistics

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

def decompose(word):
    onset = get_onset(word)
    if onset == 'other':
        return None
    body = word[len(onset):]
    midfix, suffix = strip_suffix(body)
    return onset, midfix, suffix

def parse_corpus():
    """Returns {folio: [line_words_list, ...]} in line order."""
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
        if total == 0:
            continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    print(f"Total folios: {len(folios)}")
    for d in ['A','B']:
        print(f"  {d}-dialect folios: {sum(1 for v in dialect_map.values() if v == d)}")

    # Collect by dialect and position
    # pos_comp[dialect][pos] = {component: [lengths]}
    pos_comp = {d: {p: defaultdict(list) for p in ['LF','MID','LL','ALL']}
                for d in ['A','B']}
    onset_comp = {d: defaultdict(lambda: defaultdict(list)) for d in ['A','B']}

    for folio, lines in folios.items():
        if folio not in dialect_map:
            continue
        d = dialect_map[folio]
        n = len(lines)
        if n < 3:
            continue  # need at least 3 lines for continuation lines

        cont_lines = lines[1:-1]  # skip folio-first and folio-last
        cn = len(cont_lines)

        for ci, line_words in enumerate(cont_lines):
            if ci == 0:
                pos = 'LF'
            elif ci == cn - 1:
                pos = 'LL'
            else:
                pos = 'MID'

            for word in line_words:
                r = decompose(word)
                if r is None:
                    continue
                onset, midfix, suffix = r
                wlen = len(word)
                mlen = len(midfix)
                slen = len(suffix)
                olen = len(onset)

                for p in [pos, 'ALL']:
                    pos_comp[d][p]['word_len'].append(wlen)
                    pos_comp[d][p]['onset_len'].append(olen)
                    pos_comp[d][p]['midfix_len'].append(mlen)
                    pos_comp[d][p]['suffix_len'].append(slen)
                    pos_comp[d][p]['body_len'].append(olen + mlen)

                onset_comp[d][onset]['midfix_len'].append(mlen)
                onset_comp[d][onset]['suffix_len'].append(slen)
                onset_comp[d][onset]['word_len'].append(wlen)

    # Summary by dialect
    print("\n=== Overall component means (continuation lines only) ===")
    for d in ['A','B']:
        pc = pos_comp[d]['ALL']
        n = len(pc['word_len'])
        print(f"\n{d}-dialect (N={n} words):")
        for comp in ['word_len','onset_len','midfix_len','suffix_len','body_len']:
            vals = pc[comp]
            if not vals:
                continue
            print(f"  {comp}: mean={sum(vals)/len(vals):.3f}  median={statistics.median(vals):.1f}")

    # By position
    print("\n=== Component means by position ===")
    for d in ['A','B']:
        print(f"\n{d}-dialect:")
        print(f"  {'Pos':<5} {'N':>6}  {'word':>6}  {'midfix':>7}  {'suffix':>7}")
        for pos in ['LF','MID','LL']:
            pc = pos_comp[d][pos]
            wl = pc['word_len']
            ml = pc['midfix_len']
            sl = pc['suffix_len']
            if not wl:
                continue
            print(f"  {pos:<5} {len(wl):>6}  {sum(wl)/len(wl):>6.3f}  "
                  f"{sum(ml)/len(ml):>7.3f}  {sum(sl)/len(sl):>7.3f}")

    # By onset class
    print("\n=== Component means by onset class (ALL positions combined) ===")
    for d in ['A','B']:
        print(f"\n{d}-dialect:")
        print(f"  {'Onset':<6}  {'N':>5}  {'word':>6}  {'midfix':>7}  {'suffix':>7}  {'zero-mf%':>9}")
        for onset in ONSETS:
            od = onset_comp[d][onset]
            wl = od['word_len']
            ml = od['midfix_len']
            if not wl or len(wl) < 5:
                continue
            sl = od['suffix_len']
            zero_mf = sum(1 for x in ml if x == 0) / len(ml) * 100
            print(f"  {onset:<6}  {len(wl):>5}  {sum(wl)/len(wl):>6.2f}  "
                  f"{sum(ml)/len(ml):>7.3f}  {sum(sl)/len(sl):>7.3f}  {zero_mf:>9.1f}%")

    # Midfix length distribution
    print("\n=== Midfix length distribution ===")
    for d in ['A','B']:
        ml = pos_comp[d]['ALL']['midfix_len']
        total = len(ml)
        cnt = Counter(ml)
        row = "  ".join(f"mf={k}: {cnt[k]/total*100:.1f}%" for k in sorted(cnt.keys())[:8])
        print(f"  {d}: {row}")

    # Suffix length distribution
    print("\n=== Suffix length distribution ===")
    for d in ['A','B']:
        sl = pos_comp[d]['ALL']['suffix_len']
        total = len(sl)
        cnt = Counter(sl)
        row = "  ".join(f"suf={k}: {cnt[k]/total*100:.1f}%" for k in sorted(cnt.keys())[:8])
        print(f"  {d}: {row}")

    # VMS target analysis (22% overproduction)
    print("\n=== 22%-overproduction gap analysis ===")
    for d in ['A','B']:
        pc = pos_comp[d]['ALL']
        mean_o = sum(pc['onset_len']) / len(pc['onset_len'])
        mean_m = sum(pc['midfix_len']) / len(pc['midfix_len'])
        mean_s = sum(pc['suffix_len']) / len(pc['suffix_len'])
        mean_w = sum(pc['word_len']) / len(pc['word_len'])
        sim_w = mean_w * 1.22
        excess = sim_w - mean_w
        print(f"\n{d}-dialect:")
        print(f"  VMS: onset={mean_o:.3f} + midfix={mean_m:.3f} + suffix={mean_s:.3f} = {mean_w:.3f}")
        print(f"  Sim(+22%): {sim_w:.3f} (excess={excess:.3f} chars)")
        print(f"  If all excess in midfix: sim_midfix would be {mean_m + excess:.3f} "
              f"({(mean_m+excess)/mean_m:.2f}× actual)")
        print(f"  If all excess in suffix: sim_suffix would be {mean_s + excess:.3f} "
              f"({(mean_s+excess)/mean_s:.2f}× actual)")

if __name__ == '__main__':
    main()
