"""
exp_213: H404 — B First-Line y+Gallows-Compound Slot at pos=1

Motivation:
  exp_212 (F212) found that B first-line body y-onset enrichment (1.88×) is driven by
  y+gallows-compound words (ypchedy, ypchdy, ypchey, yfchey) that are first-line-body-specific.
  These words may occupy a specific slot at pos=1 (immediately after PS), bridging PS gallows
  vocabulary → y+gallows → body.

  A-dialect comparison from F207: PS→pos=1 transitions are sh-dominant (shey/sheol/shor).
  Does B have a parallel y+gallows-compound slot at pos=1?

Test:
  (1) B first-line onset distribution at pos=0(PS)/pos=1/pos=2/pos=3+
  (2) y-onset rate and y+gallows-compound rate at each position
  (3) Top B PS→pos=1 transitions (most common PS→pos=1 word pairs)
  (4) Contrast with A PS→pos=1 distribution (for dialect comparison)
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

def is_y_gallows(w):
    """True if word is y-onset + gallows compound (ypch/ytch/ykch/yfch)."""
    return (w.startswith('ypch') or w.startswith('ytch') or
            w.startswith('ykch') or w.startswith('yfch') or
            w.startswith('ypcx') or w.startswith('yfcx'))

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

    paragraphs = []
    current_para = None
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

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            if is_para_start:
                current_para = {'dialect': dialect, 'folio': fb, 'lines': []}
                paragraphs.append(current_para)
            if current_para is not None:
                current_para['lines'].append(words)
    return paragraphs, folio_dialect


paragraphs, folio_dialect = parse_corpus()

for dialect_label in ['B', 'A']:
    paras = [p for p in paragraphs if p['dialect'] == dialect_label and len(p['lines']) >= 2]
    first_lines = [p['lines'][0] for p in paras if len(p['lines'][0]) >= 3]
    print(f"\n{'='*60}")
    print(f"{dialect_label}-DIALECT FIRST-LINE POSITION ANALYSIS (paragraphs with ≥2 lines: {len(paras)})")
    print(f"  First lines with ≥3 words: {len(first_lines)}")

    # Onset distribution by position (0,1,2,3+)
    pos_onset = defaultdict(Counter)  # pos_bucket → onset Counter
    pos_total = defaultdict(int)
    pos_y_gallows = defaultdict(int)
    pos_y = defaultdict(int)
    pos_words = defaultdict(Counter)  # pos_bucket → word Counter

    all_words_n = 0
    all_words_onset = Counter()
    all_y_gallows_n = 0
    all_y_n = 0

    for para in paras:
        fl = para['lines'][0]
        for pos, word in enumerate(fl):
            pos_bucket = min(pos, 3)  # 0,1,2,3+
            pos_onset[pos_bucket][get_onset(word)] += 1
            pos_total[pos_bucket] += 1
            pos_words[pos_bucket][word] += 1
            all_words_n += 1
            all_words_onset[get_onset(word)] += 1
            if get_onset(word) == 'y':
                pos_y[pos_bucket] += 1
                all_y_n += 1
            if is_y_gallows(word):
                pos_y_gallows[pos_bucket] += 1
                all_y_gallows_n += 1

    y_base = all_y_n / all_words_n if all_words_n > 0 else 0
    yg_base = all_y_gallows_n / all_words_n if all_words_n > 0 else 0

    print(f"\n  Base rates (all first-line positions): y={y_base:.4f} ({y_base*100:.1f}%), "
          f"y+gallows={yg_base:.4f} ({yg_base*100:.2f}%)")

    print(f"\n  {'Pos':<5} {'n_total':<10} {'y_rate':<10} {'y_enr':<10} {'y+gal_rate':<12} {'y+gal_enr':<12}")
    for pos_b in range(4):
        n = pos_total.get(pos_b, 0)
        if n == 0:
            continue
        y_r = pos_y.get(pos_b, 0) / n
        yg_r = pos_y_gallows.get(pos_b, 0) / n
        label = str(pos_b) if pos_b < 3 else '3+'
        y_enr = y_r / y_base if y_base > 0 else 0
        yg_enr = yg_r / yg_base if yg_base > 0 else 0
        print(f"  {label:<5} {n:<10} {y_r:.4f}({y_r*100:.1f}%) {y_enr:.2f}×  "
              f"{yg_r:.4f}({yg_r*100:.2f}%) {yg_enr:.2f}×  "
              f"[y_n={pos_y.get(pos_b,0)}, yg_n={pos_y_gallows.get(pos_b,0)}]")

    print(f"\n  Onset distribution at pos=0 (PS) and pos=1 for {dialect_label}-dialect:")
    print(f"  {'Onset':<8} {'PS rate':<12} {'PS enr':<10} {'pos=1 rate':<13} {'pos=1 enr':<12}")
    for onset, _ in ONSET_ORDER:
        b_r = all_words_onset.get(onset, 0) / all_words_n if all_words_n > 0 else 0
        ps_n = pos_onset[0].get(onset, 0)
        p1_n = pos_onset[1].get(onset, 0)
        ps_r = ps_n / pos_total.get(0, 1)
        p1_r = p1_n / pos_total.get(1, 1)
        ps_enr = ps_r / b_r if b_r > 0 else 0
        p1_enr = p1_r / b_r if b_r > 0 else 0
        if ps_n > 0 or p1_n > 0:
            print(f"  {onset:<8} {ps_r:.4f}({ps_n}) {ps_enr:.2f}×  {p1_r:.4f}({p1_n}) {p1_enr:.2f}×")

    print(f"\n  Top {dialect_label} pos=1 words (immediately after PS):")
    for word, cnt in pos_words[1].most_common(15):
        print(f"    {word:<18} n={cnt:3d}  onset={get_onset(word):<6}  y+gal={is_y_gallows(word)}")

    print(f"\n  Top {dialect_label} PS→pos=1 bigrams:")
    bigrams = Counter()
    for para in paras:
        fl = para['lines'][0]
        if len(fl) >= 2:
            bigrams[(fl[0], fl[1])] += 1
    for (ps_w, p1_w), cnt in bigrams.most_common(12):
        print(f"    {ps_w:<20} → {p1_w:<18} n={cnt:2d}  (ps_onset={get_onset(ps_w)}, p1_onset={get_onset(p1_w)}, p1_y_gal={is_y_gallows(p1_w)})")

    print(f"\n  y+gallows words at pos=1 for {dialect_label}-dialect:")
    yg_pos1 = [(w, c) for w, c in pos_words[1].items() if is_y_gallows(w)]
    if yg_pos1:
        for w, c in sorted(yg_pos1, key=lambda x: -x[1]):
            print(f"    {w:<18} n={c}")
    else:
        print("    (none)")
