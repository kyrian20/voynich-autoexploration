"""
exp_070: k+-dy Particle Analysis (H087) + ch-ch/sh-sh Bigram Constructions (H088)
H087: Is 'kedy' a positionally-restricted grammatical particle?
H088: Do ch-ch and sh-sh self-following bigrams form bi-word constructions?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
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

def main():
    records = parse_corpus(DATA_PATH)
    b_records = [r for r in records if r['currier'] == 'B']

    # H087: k+-dy particle analysis
    print("="*70)
    print("H087: k+-dy PARTICLE ANALYSIS")
    print("="*70)

    # Collect all k-onset words and classify by suffix
    k_dy_words = []    # k words with -dy suffix
    k_other_words = [] # k words with other suffix
    k_dy_pos = {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0}
    k_other_pos = {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0}

    # Left and right context for k-dy words
    k_dy_left = []
    k_dy_right = []
    k_other_left = []
    k_other_right = []

    # All word positions for baseline
    total_pos = {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0}

    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            pos = 'medial' if 0 < i < n-1 else ('first' if i == 0 else 'last')
            total_pos[pos] += 1
            total_pos['total'] += 1
            if i == 0 and r['is_para_start']:
                total_pos['para_first'] += 1

            if onset_class(w) != 'k':
                continue
            suf = suffix_group(w) or '(none)'
            left = onset_class(ws[i-1]) if i > 0 else None
            right = onset_class(ws[i+1]) if i < n-1 else None

            if suf == 'dy':
                k_dy_words.append(w)
                k_dy_pos[pos] += 1
                if i == 0 and r['is_para_start']:
                    k_dy_pos['para_first'] += 1
                if left:
                    k_dy_left.append(left)
                if right:
                    k_dy_right.append(right)
            else:
                k_other_words.append(w)
                k_other_pos[pos] += 1
                if i == 0 and r['is_para_start']:
                    k_other_pos['para_first'] += 1
                if left:
                    k_other_left.append(left)
                if right:
                    k_other_right.append(right)

    n_total = total_pos['total']
    n_kd = len(k_dy_words)
    n_ko = len(k_other_words)

    base_first = total_pos['first'] / max(n_total, 1)
    base_med = (n_total - total_pos['first'] - total_pos['last']) / max(n_total, 1)
    base_last = total_pos['last'] / max(n_total, 1)
    base_para = total_pos['para_first'] / max(n_total, 1)

    print(f"\nk+-dy words: {n_kd}, k+other-suffix words: {n_ko}")
    print(f"\nTop k-dy words: {', '.join(f'{w}({c})' for w,c in Counter(k_dy_words).most_common(10))}")
    print(f"Top k-other words: {', '.join(f'{w}({c})' for w,c in Counter(k_other_words).most_common(10))}")

    def pos_pct(pos_dict, total):
        n = sum(pos_dict.values())
        return {k: v/max(n, 1) for k, v in pos_dict.items()}

    kd_p = pos_pct(k_dy_pos, n_kd)
    ko_p = pos_pct(k_other_pos, n_ko)

    print(f"\n{'Position':<15} {'k-dy%':>8} {'enr_kd':>8} {'k-other%':>10} {'enr_ko':>9}")
    for pos, base in [('first', base_first), ('medial', base_med), ('last', base_last), ('para_first', base_para)]:
        kd = k_dy_pos[pos] / max(n_kd, 1)
        ko = k_other_pos[pos] / max(n_ko, 1)
        print(f"{pos:<15} {100*kd:>7.1f}% {kd/max(base,1e-10):>7.2f}× {100*ko:>9.1f}% {ko/max(base,1e-10):>8.2f}×")

    # Left and right context for k-dy
    if k_dy_left:
        kd_lc = Counter(k_dy_left)
        ko_lc = Counter(k_other_left)
        kd_rc = Counter(k_dy_right)
        ko_rc = Counter(k_other_right)
        print(f"\n--- Left context class (word before k) ---")
        print(f"{'Class':<10} {'k-dy%':>8} {'k-other%':>10} {'Ratio':>7}")
        for cls in sorted(set(kd_lc.keys()) | set(ko_lc.keys())):
            kdp = kd_lc.get(cls, 0) / max(len(k_dy_left), 1)
            kop = ko_lc.get(cls, 0) / max(len(k_other_left), 1)
            if kdp > 0.03 or kop > 0.03:
                print(f"{cls:<10} {100*kdp:>7.1f}% {100*kop:>9.1f}% {kdp/max(kop,1e-10):>7.2f}×")
        print(f"\n--- Right context class (word after k) ---")
        print(f"{'Class':<10} {'k-dy%':>8} {'k-other%':>10} {'Ratio':>7}")
        for cls in sorted(set(kd_rc.keys()) | set(ko_rc.keys())):
            kdp = kd_rc.get(cls, 0) / max(len(k_dy_right), 1)
            kop = ko_rc.get(cls, 0) / max(len(k_other_right), 1)
            if kdp > 0.03 or kop > 0.03:
                print(f"{cls:<10} {100*kdp:>7.1f}% {100*kop:>9.1f}% {kdp/max(kop,1e-10):>7.2f}×")

    # H088: ch-ch and sh-sh bigram constructions
    print(f"\n{'='*70}")
    print("H088: ch-ch AND sh-sh SELF-FOLLOWING BIGRAM CONSTRUCTIONS")
    print(f"{'='*70}")

    for dialect in ['A', 'B']:
        d_recs = [r for r in records if r['currier'] == dialect]
        print(f"\n--- Currier {dialect} ---")

        # Collect bigrams
        ch_ch = Counter()   # ch word pairs (w1, w2) where both start with ch
        sh_sh = Counter()   # sh word pairs
        ch_other = Counter()  # ch words followed by non-ch
        sh_other = Counter()  # sh words followed by non-sh
        other_ch = Counter()  # non-ch words followed by ch
        other_sh = Counter()  # non-sh words followed by sh

        # Positional data for ch-ch pairs
        ch_ch_pos = {'first': 0, 'medial': 0, 'last': 0}
        ch_ch_total = 0
        sh_sh_pos = {'first': 0, 'medial': 0, 'last': 0}
        sh_sh_total = 0

        for r in d_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                w1, w2 = ws[i], ws[i+1]
                oc1 = 'ch' if (w1.startswith('ch') and len(w1) > 2) else \
                      ('sh' if (w1.startswith('sh') and len(w1) > 2) else 'other')
                oc2 = 'ch' if (w2.startswith('ch') and len(w2) > 2) else \
                      ('sh' if (w2.startswith('sh') and len(w2) > 2) else 'other')

                if oc1 == 'ch' and oc2 == 'ch':
                    ch_ch[(w1, w2)] += 1
                    pos2 = 'medial' if 0 < i+1 < n-1 else ('first' if i+1 == 0 else 'last')
                    ch_ch_pos[pos2] += 1
                    ch_ch_total += 1
                elif oc1 == 'sh' and oc2 == 'sh':
                    sh_sh[(w1, w2)] += 1
                    pos2 = 'medial' if 0 < i+1 < n-1 else ('first' if i+1 == 0 else 'last')
                    sh_sh_pos[pos2] += 1
                    sh_sh_total += 1
                elif oc1 == 'ch':
                    ch_other[w2] += 1
                elif oc1 == 'sh':
                    sh_other[w2] += 1
                if oc2 == 'ch':
                    other_ch[w1] += 1
                elif oc2 == 'sh':
                    other_sh[w1] += 1

        n_ch = sum(ch_ch.values()) + sum(ch_other.values())
        n_sh = sum(sh_sh.values()) + sum(sh_other.values())
        p_ch_ch = sum(ch_ch.values()) / max(n_ch, 1)
        p_sh_sh = sum(sh_sh.values()) / max(n_sh, 1)

        print(f"\n  ch→ch rate: {100*p_ch_ch:.1f}% ({sum(ch_ch.values())}/{n_ch})")
        print(f"  sh→sh rate: {100*p_sh_sh:.1f}% ({sum(sh_sh.values())}/{n_sh})")

        # Overall ch/sh rate for baseline
        all_words = []
        for r in d_recs:
            all_words.extend(r['words'])
        n_all = len(all_words)
        base_ch = sum(1 for w in all_words if w.startswith('ch') and len(w) > 2) / max(n_all, 1)
        base_sh = sum(1 for w in all_words if w.startswith('sh') and len(w) > 2) / max(n_all, 1)
        print(f"  Expected if random: ch baseline={100*base_ch:.1f}%, sh baseline={100*base_sh:.1f}%")
        print(f"  ch→ch enrichment: {p_ch_ch/max(base_ch,1e-10):.2f}×, sh→sh enrichment: {p_sh_sh/max(base_sh,1e-10):.2f}×")

        # Top ch-ch and sh-sh bigrams
        print(f"\n  Top ch-ch bigrams:")
        for (w1, w2), c in ch_ch.most_common(10):
            print(f"    {w1} {w2}: {c}")
        print(f"\n  Top sh-sh bigrams:")
        for (w1, w2), c in sh_sh.most_common(10):
            print(f"    {w1} {w2}: {c}")

        # Position distribution for ch-ch and sh-sh (second word position)
        print(f"\n  Position of second word in ch-ch pair: first={ch_ch_pos['first']}, medial={ch_ch_pos['medial']}, last={ch_ch_pos['last']}")
        print(f"  Position of second word in sh-sh pair: first={sh_sh_pos['first']}, medial={sh_sh_pos['medial']}, last={sh_sh_pos['last']}")

        # Top words BEFORE ch and sh
        print(f"\n  Top words before ch (in other→ch pairs):")
        print(f"    {', '.join(f'{w}({c})' for w,c in Counter(other_ch).most_common(8))}")
        print(f"  Top words before sh (in other→sh pairs):")
        print(f"    {', '.join(f'{w}({c})' for w,c in Counter(other_sh).most_common(8))}")

        # Is the second ch in a ch-ch pair different from a random ch word?
        ch_ch_second = Counter(w2 for (w1, w2), c in ch_ch.items() for _ in range(c))
        all_ch = Counter(w for w in all_words if w.startswith('ch') and len(w) > 2)
        print(f"\n  Second word in ch-ch pair (top 8): {', '.join(f'{w}({c})' for w,c in ch_ch_second.most_common(8))}")
        print(f"  All ch words (top 8): {', '.join(f'{w}({c})' for w,c in all_ch.most_common(8))}")

if __name__ == '__main__':
    main()
