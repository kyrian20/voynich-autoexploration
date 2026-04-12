"""
exp_216: H407 — A-Dialect VMS Primary Metrics

Motivation:
  All discrimination work (exp_170-211) used B-dialect VMS targets:
    am_ll=6.811, d_ll=1.464, y_lf=3.506, ss_mean=1.465, adj_rate=0.009

  A-dialect primary metrics have never been computed. If the position-aware hybrid
  architecture (exp_211) reproduces A-dialect metrics at the same calibration, it
  strengthens the unified cipher hypothesis. If A-dialect metrics differ significantly,
  it would reveal A-specific gaps.

Test:
  Compute from ZL3b A-dialect paragraphs:
  (1) am_ll: -am suffix LL enrichment
  (2) d_ll: d-onset LL enrichment
  (3) y_lf: y-onset LF enrichment
  (4) ss_mean: onset self-succession (qok, ok, ch)
  (5) adj_rate: exact adjacent word repetition

  Also compute A-dialect base rates for key onset classes, for comparison.
"""
import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_ORDER = [
    ('qok', 'qok'), ('qot', 'qot'), ('qo', 'qo'), ('cth', 'cth'),
    ('ch', 'ch'), ('sh', 'sh'), ('ok', 'ok'), ('ot', 'ot'), ('ol', 'ol'),
    ('d', 'd'), ('s', 's'), ('y', 'y'), ('k', 'k'), ('t', 't'),
    ('l', 'l'), ('r', 'r'), ('p', 'p'), ('f', 'f'), ('o', 'o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    rate = (stats['edy'] + stats['eedy']) / total
    return 'B' if rate >= 0.05 else 'A'

def parse_corpus():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    lines_by_dialect = {'A': [], 'B': []}
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            if dialect not in ('A', 'B'):
                continue

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words:
                lines_by_dialect[dialect].append(words)

    return lines_by_dialect


print("Loading corpus...")
lines_by_dialect = parse_corpus()

B_TARGETS = {'am_ll': 6.811, 'd_ll': 1.464, 'y_lf': 3.506, 'ss_mean': 1.465, 'adj_rate': 0.009}

for dialect in ['A', 'B']:
    lines = lines_by_dialect[dialect]
    all_words = [w for l in lines for w in l]
    n = len(all_words)
    lf_words = [l[0] for l in lines if l]
    ll_words = [l[-1] for l in lines if len(l) > 1]

    print(f"\n{'='*55}")
    print(f"{dialect}-DIALECT PRIMARY METRICS (n={len(lines)} lines, {n} words)")
    print()

    # am_ll
    am_r = sum(1 for w in all_words if w.endswith('am')) / n
    ll_am = sum(1 for w in ll_words if w.endswith('am')) / len(ll_words) if ll_words else 0
    am_ll = ll_am / am_r if am_r > 0 else 0

    # d_ll
    oc = Counter(get_onset(w) for w in all_words)
    d_r = oc.get('d', 0) / n
    ll_d = sum(1 for w in ll_words if get_onset(w) == 'd') / len(ll_words) if ll_words else 0
    d_ll = ll_d / d_r if d_r > 0 else 0

    # y_lf
    y_r = oc.get('y', 0) / n
    y_lf_raw = sum(1 for w in lf_words if get_onset(w) == 'y') / len(lf_words) if lf_words else 0
    y_lf = y_lf_raw / y_r if y_r > 0 else 0

    # ss_mean
    tb = n - 1
    bg = Counter((get_onset(all_words[i]), get_onset(all_words[i+1])) for i in range(tb))
    def ss(o):
        b = oc.get(o, 0) / n
        return bg.get((o, o), 0) / (tb * b * b) if b > 0 and tb > 0 else 1.0
    ss_m = (ss('qok') + ss('ok') + ss('ch')) / 3

    # adj_rate
    adj = sum(1 for i in range(tb) if all_words[i] == all_words[i+1]) / max(1, tb)

    print(f"  Metric            {dialect}-VMS    B-VMS (target)  %B")
    print(f"  am_ll:            {am_ll:.3f}    {B_TARGETS['am_ll']:.3f}           {am_ll/B_TARGETS['am_ll']*100:.1f}%")
    print(f"  d_ll:             {d_ll:.3f}    {B_TARGETS['d_ll']:.3f}           {d_ll/B_TARGETS['d_ll']*100:.1f}%")
    print(f"  y_lf:             {y_lf:.3f}    {B_TARGETS['y_lf']:.3f}           {y_lf/B_TARGETS['y_lf']*100:.1f}%")
    print(f"  ss_mean:          {ss_m:.3f}    {B_TARGETS['ss_mean']:.3f}           {ss_m/B_TARGETS['ss_mean']*100:.1f}%")
    print(f"  adj_rate:         {adj:.5f}  {B_TARGETS['adj_rate']:.5f}         {adj/B_TARGETS['adj_rate']*100:.1f}%")

    print()
    print(f"  Base rates:")
    print(f"    -am suffix rate: {am_r:.4f} ({am_r*100:.2f}%)")
    print(f"    d-onset rate:    {d_r:.4f} ({d_r*100:.2f}%)")
    print(f"    y-onset rate:    {y_r:.4f} ({y_r*100:.2f}%)")
    print()
    print(f"  LL composition:")
    print(f"    n_ll words: {len(ll_words)}")
    print(f"    LL -am rate: {ll_am:.4f} ({ll_am*100:.2f}%)")
    print(f"    LL d-onset rate: {ll_d:.4f} ({ll_d*100:.2f}%)")
    print()
    print(f"  LF composition:")
    print(f"    n_lf words: {len(lf_words)}")
    print(f"    LF y-onset rate: {y_lf_raw:.4f} ({y_lf_raw*100:.2f}%)")
    top_lf = Counter(get_onset(w) for w in lf_words).most_common(8)
    print(f"    Top LF onsets: {top_lf}")
    top_ll = Counter(get_onset(w) for w in ll_words).most_common(8)
    print(f"    Top LL onsets: {top_ll}")

    # ss by onset class
    print()
    print(f"  Self-succession by onset (for ss_mean):")
    for o in ['qok', 'ok', 'ch', 'd', 'sh', 'y', 'p']:
        b_r = oc.get(o, 0) / n
        ss_v = bg.get((o, o), 0) / (tb * b_r * b_r) if b_r > 0 else 0
        print(f"    {o:<6}: {ss_v:.3f}× (n_bigram={bg.get((o,o),0)}, base={b_r:.4f})")
