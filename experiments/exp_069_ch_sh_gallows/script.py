"""
exp_069: ch vs sh Discrimination (H085) + Gallows Individual Positional Grammar (H086)
H085: What determines whether ch or sh appears? Are they in complementary distribution?
H086: Do k, t, f, p have individual positional grammars, or are k/t truly interchangeable?
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
            is_continuation = locus_code.startswith('+')
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
                'is_continuation': is_continuation,
                'words': tokens
            })
    return records

def onset_class(word):
    """Classify word onset for gallows analysis."""
    if word.startswith('qo'):
        return 'qo'
    if word.startswith('ch') and len(word) > 2:
        return 'ch'
    if word.startswith('sh') and len(word) > 2:
        return 'sh'
    if word.startswith('cth') and len(word) > 3:
        return 'cth'
    for g in ['k', 't', 'f', 'p']:
        if word.startswith(g) and not word.startswith('ch') and not word.startswith('sh') and len(word) > 1:
            return g
    if word.startswith('d'):
        return 'd'
    if word.startswith('s'):
        return 's'
    if word.startswith('y'):
        return 'y'
    if word.startswith('o'):
        return 'o'
    if word.startswith('a'):
        return 'a'
    return 'other'

def main():
    records = parse_corpus(DATA_PATH)

    # H085: ch vs sh discrimination
    print("="*70)
    print("H085: ch vs sh DISCRIMINATION — WHAT DETERMINES WHICH APPEARS?")
    print("="*70)

    for dialect in ['A', 'B']:
        dialect_recs = [r for r in records if r['currier'] == dialect]
        print(f"\n--- Currier {dialect} ---")

        # Collect ch-onset and sh-onset words with their left-context word
        ch_words = []
        sh_words = []
        ch_left_ctx = []  # word before ch-word
        sh_left_ctx = []  # word before sh-word
        ch_suf = []
        sh_suf = []
        ch_lens = []
        sh_lens = []
        ch_pos = {'first': 0, 'medial': 0, 'last': 0}
        sh_pos = {'first': 0, 'medial': 0, 'last': 0}

        for r in dialect_recs:
            ws = r['words']
            n = len(ws)
            for i, w in enumerate(ws):
                is_ch = w.startswith('ch') and len(w) > 2
                is_sh = w.startswith('sh') and len(w) > 2
                if not is_ch and not is_sh:
                    continue
                suf = suffix_group(w) or '(none)'
                length = len(w)
                # Left context word
                left = ws[i-1] if i > 0 else None
                # Position
                if i == 0:
                    pos_label = 'first'
                elif i == n - 1:
                    pos_label = 'last'
                else:
                    pos_label = 'medial'
                if is_ch:
                    ch_words.append(w)
                    ch_suf.append(suf)
                    ch_lens.append(length)
                    ch_pos[pos_label] += 1
                    if left:
                        ch_left_ctx.append(onset_class(left))
                else:
                    sh_words.append(w)
                    sh_suf.append(suf)
                    sh_lens.append(length)
                    sh_pos[pos_label] += 1
                    if left:
                        sh_left_ctx.append(onset_class(left))

        n_ch = len(ch_words)
        n_sh = len(sh_words)
        total = n_ch + n_sh
        print(f"  ch words: {n_ch} ({100*n_ch/max(total,1):.1f}%), sh words: {n_sh} ({100*n_sh/max(total,1):.1f}%)")

        # Top ch words
        print(f"\n  Top ch words: {', '.join(f'{w}({c})' for w,c in Counter(ch_words).most_common(10))}")
        print(f"  Top sh words: {', '.join(f'{w}({c})' for w,c in Counter(sh_words).most_common(10))}")

        # Positional comparison
        def pct(d, k):
            return 100 * d.get(k, 0) / max(sum(d.values()), 1)
        print(f"\n  Position     ch%    sh%")
        for pos in ['first', 'medial', 'last']:
            print(f"  {pos:<12} {pct(ch_pos, pos):>5.1f}% {pct(sh_pos, pos):>5.1f}%")

        # Suffix comparison
        ch_suf_c = Counter(ch_suf)
        sh_suf_c = Counter(sh_suf)
        print(f"\n  Suffix       ch%    sh%    ratio")
        for suf in SUFFIX_LIST + ['(none)']:
            cp = ch_suf_c.get(suf, 0) / max(n_ch, 1)
            sp = sh_suf_c.get(suf, 0) / max(n_sh, 1)
            if cp > 0.03 or sp > 0.03:
                ratio = cp / max(sp, 1e-10)
                print(f"  {suf:<10} {100*cp:>5.1f}% {100*sp:>5.1f}% {ratio:>6.2f}×")

        # Left context class distribution
        if ch_left_ctx and sh_left_ctx:
            ch_ctx_c = Counter(ch_left_ctx)
            sh_ctx_c = Counter(sh_left_ctx)
            print(f"\n  Left-context onset class distribution:")
            print(f"  {'Class':<8} {'ch%':>7} {'sh%':>7} {'Ratio':>7}")
            all_classes = set(ch_ctx_c.keys()) | set(sh_ctx_c.keys())
            for cls in sorted(all_classes):
                cp = ch_ctx_c.get(cls, 0) / max(len(ch_left_ctx), 1)
                sp = sh_ctx_c.get(cls, 0) / max(len(sh_left_ctx), 1)
                if cp > 0.03 or sp > 0.03:
                    ratio = cp / max(sp, 1e-10)
                    print(f"  {cls:<8} {100*cp:>6.1f}% {100*sp:>6.1f}% {ratio:>7.2f}×")

        # Section distribution
        ch_sec = Counter()
        sh_sec = Counter()
        for r in dialect_recs:
            sec = r['section'] or '?'
            for w in r['words']:
                if w.startswith('ch') and len(w) > 2:
                    ch_sec[sec] += 1
                elif w.startswith('sh') and len(w) > 2:
                    sh_sec[sec] += 1
        if len(ch_sec) > 1 or len(sh_sec) > 1:
            print(f"\n  Section ch/sh ratio:")
            for sec in sorted(set(ch_sec.keys()) | set(sh_sec.keys())):
                total_sec = ch_sec.get(sec, 0) + sh_sec.get(sec, 0)
                sh_frac = sh_sec.get(sec, 0) / max(total_sec, 1)
                print(f"    {sec}: ch={ch_sec.get(sec,0)}, sh={sh_sec.get(sec,0)}, sh/(ch+sh)={100*sh_frac:.1f}%")

        # Mean word length
        if ch_lens and sh_lens:
            print(f"\n  Mean length: ch={sum(ch_lens)/len(ch_lens):.2f}, sh={sum(sh_lens)/len(sh_lens):.2f}")

    # H086: Gallows individual positional grammar
    print(f"\n{'='*70}")
    print("H086: GALLOWS LETTERS INDIVIDUAL POSITIONAL GRAMMAR (k, t, f, p in B)")
    print(f"{'='*70}")

    b_records = [r for r in records if r['currier'] == 'B']

    # Collect positional stats for each gallows letter
    gallows = ['k', 't', 'f', 'p']
    stats = {g: {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0} for g in gallows}
    total_pos = {'first': 0, 'medial': 0, 'last': 0, 'para_first': 0, 'total': 0}

    for r in b_records:
        ws = r['words']
        n = len(ws)
        if n == 0:
            continue
        for i, w in enumerate(ws):
            oc = onset_class(w)
            pos = 'medial' if 0 < i < n-1 else ('first' if i == 0 else 'last')
            total_pos[pos] += 1
            total_pos['total'] += 1
            if i == 0 and r['is_para_start']:
                total_pos['para_first'] += 1
            if oc in gallows:
                stats[oc][pos] += 1
                stats[oc]['total'] += 1
                if i == 0 and r['is_para_start']:
                    stats[oc]['para_first'] += 1

    # Total baseline rates
    n_total = total_pos['total']
    base_first = total_pos['first'] / max(n_total, 1)
    base_medial = total_pos['medial'] / max(n_total, 1)
    base_last = total_pos['last'] / max(n_total, 1)
    base_para = total_pos['para_first'] / max(n_total, 1)

    print(f"\nCurrier B baseline: first={100*base_first:.1f}%, medial={100*base_medial:.1f}%, last={100*base_last:.1f}%, para_first={100*base_para:.2f}%")
    print(f"\n{'Gallows':<10} {'Count':>7} {'%all':>6} {'first%':>8} {'enr_first':>11} {'medial%':>9} {'enr_med':>9} {'last%':>7} {'enr_last':>9} {'para_f%':>9} {'enr_para':>10}")

    for g in gallows:
        s = stats[g]
        n_g = s['total']
        if n_g == 0:
            continue
        pct_all = n_g / n_total
        pct_first = s['first'] / max(n_g, 1)
        pct_med = s['medial'] / max(n_g, 1)
        pct_last = s['last'] / max(n_g, 1)
        pct_para = s['para_first'] / max(n_g, 1)
        print(f"{g:<10} {n_g:>7} {100*pct_all:>5.1f}% {100*pct_first:>7.1f}% {pct_first/max(base_first,1e-10):>10.2f}× {100*pct_med:>8.1f}% {pct_med/max(base_medial,1e-10):>8.2f}× {100*pct_last:>6.1f}% {pct_last/max(base_last,1e-10):>8.2f}× {100*pct_para:>8.2f}% {pct_para/max(base_para,1e-10):>9.2f}×")

    # Suffix distribution for each gallows
    print(f"\n--- GALLOWS SUFFIX DISTRIBUTION (Currier B) ---")
    g_suf = {g: Counter() for g in gallows}
    g_total = {g: 0 for g in gallows}
    all_b_suf = Counter()
    n_all_b = 0
    for r in b_records:
        for w in r['words']:
            oc = onset_class(w)
            suf = suffix_group(w) or '(none)'
            all_b_suf[suf] += 1
            n_all_b += 1
            if oc in gallows:
                g_suf[oc][suf] += 1
                g_total[oc] += 1

    header = f"{'Suffix':<8}"
    for g in gallows:
        header += f" {g+' %':>7}"
    header += f" {'all B%':>7}"
    print(header)
    for suf in SUFFIX_LIST + ['(none)']:
        row = f"{suf:<8}"
        any_sig = False
        vals = []
        for g in gallows:
            p = g_suf[g].get(suf, 0) / max(g_total[g], 1)
            vals.append(p)
            if p > 0.03:
                any_sig = True
        ab_p = all_b_suf.get(suf, 0) / max(n_all_b, 1)
        if any_sig or ab_p > 0.03:
            for p in vals:
                row += f" {100*p:>6.1f}%"
            row += f" {100*ab_p:>6.1f}%"
            print(row)

    # Top words for each gallows
    print(f"\n--- TOP WORDS BY GALLOWS ONSET (Currier B, top 8) ---")
    g_words = {g: Counter() for g in gallows}
    for r in b_records:
        for w in r['words']:
            oc = onset_class(w)
            if oc in gallows:
                g_words[oc][w] += 1
    for g in gallows:
        top = g_words[g].most_common(8)
        print(f"  {g}: {', '.join(f'{w}({c})' for w,c in top)}")

    # Section distribution for gallows
    print(f"\n--- GALLOWS RATE BY SECTION (Currier B) ---")
    g_sec = {g: Counter() for g in gallows}
    sec_total = Counter()
    for r in b_records:
        sec = r['section'] or '?'
        for w in r['words']:
            oc = onset_class(w)
            sec_total[sec] += 1
            if oc in gallows:
                g_sec[oc][sec] += 1

    header2 = f"{'Section':<10}"
    for g in gallows:
        header2 += f" {g+'%':>6}"
    print(header2)
    for sec in sorted(sec_total.keys()):
        row2 = f"{sec:<10}"
        n_sec = sec_total[sec]
        for g in gallows:
            p = g_sec[g].get(sec, 0) / max(n_sec, 1)
            row2 += f" {100*p:>5.1f}%"
        print(row2)

if __name__ == '__main__':
    main()
