"""
exp_199: B WP-LF Composition + d+ch → sh Successor + Gallows+ch Folio Distribution

H359: What displaces k at B within-para LF?
H360: Which specific sh-words follow d+ch lines?
H361: Is p+ch vs k+ch hierarchy consistent across herbal A folios?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

def folio_base(folio): return re.sub(r'\.\d+$', '', folio)

def classify_dialect(stats):
    total = stats.get('total', 0)
    if total == 0: return 'unknown'
    rate = (stats.get('edy', 0) + stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'

def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m: return 'unknown'
    n = int(m.group(1))
    if n <= 57: return 'herbal'
    if 103 <= n <= 116: return 'stars'
    return 'other'

def get_onset(word):
    w = word.lower()
    for prefix in ['qok','qot','qo','cth','ch','sh','ok','ot','ol']:
        if w.startswith(prefix): return prefix
    for c in ['d','s','y','k','t','l','r','p','f','o']:
        if w.startswith(c): return c
    return 'other'

def parse_corpus():
    folio_stats = defaultdict(lambda: {'total':0,'edy':0,'eedy':0})
    with open(DATA_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            fb = folio_base(m.group(1).lstrip('+*=&~'))
            text = re.sub(r'<[^>]+>','',line)
            words = [w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            for w in words:
                folio_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(s) for fb,s in folio_stats.items()}

    paragraphs = []
    current = None
    with open(DATA_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1)
            lc = m.group(3)
            fb = folio_base(folio_raw.lstrip('+*=&~'))
            dialect = folio_dialect.get(fb,'unknown')
            section = classify_section(fb)
            lc_s = lc.lstrip('+*=/~&')
            is_ps = lc_s.startswith('@')
            is_body = lc_s.lstrip('@').startswith('P')
            if not is_body: continue
            text = re.sub(r'<[^>]+>','',line)
            words = [w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            if not words: continue
            if is_ps:
                current = {'dialect':dialect,'section':section,'folio':fb,'lines':[]}
                paragraphs.append(current)
            if current is not None:
                current['lines'].append(words)
    return paragraphs

def h359_b_wplf(paragraphs):
    print("="*70)
    print("H359: B vs A Within-Para LF Onset Distribution")
    print("="*70)

    for dial in ['A','B']:
        paras = [p for p in paragraphs if p['dialect']==dial]
        wplf = []
        for p in paras:
            for i in range(1, len(p['lines'])):
                if p['lines'][i]:
                    wplf.append(get_onset(p['lines'][i][0]))

        print(f"\nDialect {dial} WP-LF (n={len(wplf)}):")
        cnt = Counter(wplf)
        for onset in sorted(cnt, key=lambda x: -cnt[x])[:15]:
            print(f"  {onset}: {cnt[onset]} ({cnt[onset]/len(wplf):.1%})")

    # Compute enrichment: B vs A at WP-LF
    a_paras = [p for p in paragraphs if p['dialect']=='A']
    b_paras = [p for p in paragraphs if p['dialect']=='B']

    a_wplf = Counter()
    b_wplf = Counter()
    for p in a_paras:
        for i in range(1,len(p['lines'])):
            if p['lines'][i]: a_wplf[get_onset(p['lines'][i][0])] += 1
    for p in b_paras:
        for i in range(1,len(p['lines'])):
            if p['lines'][i]: b_wplf[get_onset(p['lines'][i][0])] += 1

    total_a = sum(a_wplf.values())
    total_b = sum(b_wplf.values())
    print(f"\nB vs A WP-LF enrichment:")
    print(f"{'Onset':<8} {'B%':>7} {'A%':>7} {'B/A':>8}")
    all_onsets = set(a_wplf) | set(b_wplf)
    results = []
    for onset in all_onsets:
        b_rate = b_wplf.get(onset,0)/total_b
        a_rate = a_wplf.get(onset,0)/total_a
        ratio = b_rate/a_rate if a_rate > 0.001 else float('inf')
        results.append((onset, b_rate, a_rate, ratio))
    results.sort(key=lambda x: -x[3])
    for onset, br, ar, ratio in results:
        if br > 0.003 or ar > 0.003:
            print(f"{onset:<8} {br:>7.2%} {ar:>7.2%} {ratio:>8.2f}×")

def h360_dch_sh_successor(paragraphs):
    print("\n"+"="*70)
    print("H360: d+ch → sh Successor Analysis (A Dialect)")
    print("="*70)

    a_paras = [p for p in paragraphs if p['dialect']=='A']

    dch_nexts = []   # next-line openers after d+ch lines
    ych_nexts = []   # next-line openers after y+ch lines
    base_nexts = []  # all next-line openers (baseline)

    for p in a_paras:
        lines = p['lines']
        for i in range(len(lines)-1):
            if not lines[i] or not lines[i+1]: continue
            w0 = lines[i][0]
            w_next = lines[i+1][0]
            base_nexts.append(w_next)
            is_dch = w0.startswith('d') and len(w0)>=3 and w0[1:3] in ('ch','sh')
            is_ych = w0.startswith('y') and len(w0)>=3 and w0[1:3] in ('ch','sh')
            if is_dch:
                dch_nexts.append(w_next)
            if is_ych:
                ych_nexts.append(w_next)

    # Collect sh-onset words after d+ch specifically
    sh_after_dch = [w for w in dch_nexts if get_onset(w)=='sh']
    sh_baseline = [w for w in base_nexts if get_onset(w)=='sh']

    print(f"\nsh-onset words after d+ch lines (n={len(sh_after_dch)}):")
    sh_dch_cnt = Counter(sh_after_dch)
    sh_base_cnt = Counter(sh_baseline)
    total_sh_base = len(sh_baseline)
    total_dch = len(dch_nexts)
    for w, cnt in sh_dch_cnt.most_common(10):
        base_n = sh_base_cnt.get(w, 0)
        dch_rate = cnt/len(sh_after_dch) if sh_after_dch else 0
        base_rate = base_n/total_sh_base if total_sh_base else 0
        enrich = dch_rate/base_rate if base_rate > 0.001 else float('inf')
        print(f"  {w}: {cnt} in d+ch context ({dch_rate:.1%}); base={base_n}({base_rate:.1%}); enrich={enrich:.1f}×")

    # vs sh-words after y+ch
    sh_after_ych = [w for w in ych_nexts if get_onset(w)=='sh']
    print(f"\nsh-onset words after y+ch lines (n={len(sh_after_ych)}) [for contrast]:")
    for w, cnt in Counter(sh_after_ych).most_common(5):
        print(f"  {w}: {cnt}")

    # d+ch → specific word (not just onset)
    print(f"\nTop specific next words after d+ch (n={len(dch_nexts)}):")
    dch_word_cnt = Counter(dch_nexts)
    base_word_cnt = Counter(base_nexts)
    total_base = len(base_nexts)
    for w, cnt in dch_word_cnt.most_common(15):
        base_n = base_word_cnt.get(w,0)
        dch_rate = cnt/len(dch_nexts)
        base_rate = base_n/total_base if total_base else 0
        enrich = dch_rate/base_rate if base_rate > 0.001 else float('inf')
        print(f"  {w}: {cnt} ({dch_rate:.1%}) vs base {base_n}({base_rate:.1%}) = {enrich:.1f}×")

def h361_gallows_folio(paragraphs):
    print("\n"+"="*70)
    print("H361: Gallows+ch Para-Starter Distribution by Folio (Herbal A)")
    print("="*70)

    herbal_a = [p for p in paragraphs if p['dialect']=='A' and p['section']=='herbal']
    folio_ps = defaultdict(list)
    for p in herbal_a:
        if p['lines'] and p['lines'][0]:
            folio_ps[p['folio']].append(p['lines'][0][0])

    print(f"\n{'Folio':<8} {'n':>4} {'p+ch%':>7} {'t+ch%':>7} {'k+ch%':>7} {'f+ch%':>7} {'OTHER':>7}")
    print('-'*52)

    # Sort by folio number
    def folio_sort(fb):
        m = re.match(r'f(\d+)([rv])', fb)
        return (int(m.group(1)), m.group(2)) if m else (999,'z')

    for fb in sorted(folio_ps, key=folio_sort):
        ps_words = folio_ps[fb]
        n = len(ps_words)
        if n < 3: continue
        p_ch = sum(1 for w in ps_words if w.startswith('p') and len(w)>=3 and w[1:3] in ('ch','sh'))
        t_ch = sum(1 for w in ps_words if w.startswith('t') and len(w)>=3 and w[1:3] in ('ch','sh'))
        k_ch = sum(1 for w in ps_words if w.startswith('k') and len(w)>=3 and w[1:3] in ('ch','sh'))
        f_ch = sum(1 for w in ps_words if w.startswith('f') and len(w)>=3 and w[1:3] in ('ch','sh'))
        other = n - p_ch - t_ch - k_ch - f_ch
        print(f"{fb:<8} {n:>4} {p_ch/n:>7.1%} {t_ch/n:>7.1%} {k_ch/n:>7.1%} {f_ch/n:>7.1%} {other/n:>7.1%}")

paragraphs = parse_corpus()
h359_b_wplf(paragraphs)
h360_dch_sh_successor(paragraphs)
h361_gallows_folio(paragraphs)
