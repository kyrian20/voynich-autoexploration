"""
exp_212: H398 — B First-Line y-Onset Specific Words;
         H399 — B Last-Line qot Depletion at PF-LL vs WP-LL

H398: B first-line body (pos≥1, line_idx=0) has y-onset enriched (1.88×, n≈39, from F208).
  What specific y-onset words drive this? Are they the same as top B LF y-onset words?
  Is the enrichment section-specific?

H399: B last-line qot depletion (0.16× from F208) is the sharpest B last-line constraint.
  Is qot equally depleted at B PF-LL (para-final LL specifically)?
  What are the most common B PF-LL qo-class words, if any?
  Does this confirm B qo-class is fully excluded from paragraph boundaries?

Uses exp_208 parser (corrected version).
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

def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'other'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    if 117 <= n <= 202:
        return 'cosmo'
    return 'other'

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
            section = classify_section(fb)

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
                current_para = {'dialect': dialect, 'section': section,
                                'folio': fb, 'lines': []}
                paragraphs.append(current_para)
            if current_para is not None:
                current_para['lines'].append(words)
    return paragraphs, folio_dialect


paragraphs, folio_dialect = parse_corpus()

b_paras = [p for p in paragraphs if p['dialect'] == 'B' and len(p['lines']) >= 2]
print(f"B paragraphs (≥2 lines): {len(b_paras)}")

# =====================================================================
# H398: B First-Line y-Onset Word Inventory
# =====================================================================
print("\n=== H398: B First-Line y-Onset Word Inventory ===")

# Collect all B first-line body (pos≥1, line_idx=0) words
b_fl_body_words = []       # (word, section) for pos≥1 words on first line
b_fl_body_y_words = []     # y-onset only
b_fl_y_section = defaultdict(Counter)  # section → word counts

# Also collect B LF overall (all line first words) for comparison
b_lf_y_words = Counter()   # top B LF y-onset words overall
b_lf_total = 0
b_lf_y_total = 0

b_fl_body_total = 0
b_fl_body_y_total = 0
b_all_y_total = 0
b_all_total = 0

for para in b_paras:
    n_lines = len(para['lines'])
    section = para['section']
    for line_idx, line in enumerate(para['lines']):
        for pos, word in enumerate(line):
            b_all_total += 1
            if get_onset(word) == 'y':
                b_all_y_total += 1
            # LF tracking (pos=0, any line)
            if pos == 0:
                b_lf_total += 1
                if get_onset(word) == 'y':
                    b_lf_y_total += 1
                    b_lf_y_words[word] += 1
            # First-line body (line_idx=0, pos≥1)
            if line_idx == 0 and pos >= 1:
                b_fl_body_total += 1
                b_fl_body_words.append((word, section))
                if get_onset(word) == 'y':
                    b_fl_body_y_total += 1
                    b_fl_body_y_words.append((word, section))
                    b_fl_y_section[section][word] += 1

b_y_base_rate = b_all_y_total / b_all_total if b_all_total > 0 else 0
b_fl_y_rate = b_fl_body_y_total / b_fl_body_total if b_fl_body_total > 0 else 0
b_fl_y_enrichment = b_fl_y_rate / b_y_base_rate if b_y_base_rate > 0 else 0

print(f"B overall y-onset base rate: {b_all_y_total}/{b_all_total} = {b_y_base_rate:.4f} ({b_y_base_rate*100:.2f}%)")
print(f"B first-line body y-onset: {b_fl_body_y_total}/{b_fl_body_total} = {b_fl_y_rate:.4f} ({b_fl_y_rate*100:.2f}%)")
print(f"B first-line body y-onset enrichment: {b_fl_y_enrichment:.2f}× (matches F208: 1.88×)")
print()

# Top y-onset words in B first-line body
y_words_counter = Counter(w for w, _ in b_fl_body_y_words)
print(f"Top B first-line body y-onset words (n={b_fl_body_y_total} total):")
for word, cnt in y_words_counter.most_common(15):
    # Compare to overall B LF rate
    lf_cnt = b_lf_y_words.get(word, 0)
    lf_rate = lf_cnt / b_lf_total if b_lf_total > 0 else 0
    fl_rate = cnt / b_fl_body_total
    print(f"  {word:<15} n={cnt:3d}  fl_body_rate={fl_rate:.4f}  lf_rate={lf_rate:.4f}  ratio={fl_rate/lf_rate:.2f}×" if lf_rate > 0 else
          f"  {word:<15} n={cnt:3d}  fl_body_rate={fl_rate:.4f}  lf_rate=0  (fl-only)")

print()
print(f"Top B LF y-onset words overall (for comparison, n={b_lf_y_total}/{b_lf_total} = {b_lf_y_total/b_lf_total*100:.1f}%):")
for word, cnt in b_lf_y_words.most_common(10):
    print(f"  {word:<15} n={cnt:3d}  lf_rate={cnt/b_lf_total:.4f}")

print()
print("Section breakdown of B first-line body y-onset words:")
for section in sorted(b_fl_y_section.keys()):
    words = b_fl_y_section[section]
    total_in_section = sum(words.values())
    top_words = ', '.join(f"{w}({c})" for w, c in words.most_common(5))
    print(f"  {section:<10}: n={total_in_section:3d}  top: {top_words}")

# =====================================================================
# H399: B PF-LL qot Depletion vs WP-LL
# =====================================================================
print("\n=== H399: B PF-LL qo-Class Depletion vs WP-LL ===")

# Collect B LL words by para position (WP-LL vs PF-LL)
# WP-LL = last word of non-last lines within a paragraph
# PF-LL = last word of the last line of a paragraph

b_wp_ll = []   # (word, section)
b_pf_ll = []   # (word, section)

b_all_words = Counter()  # overall B word onset counts
b_all_words_n = 0

for para in b_paras:
    n_lines = len(para['lines'])
    section = para['section']
    for line_idx, line in enumerate(para['lines']):
        for word in line:
            b_all_words[get_onset(word)] += 1
            b_all_words_n += 1
        # LL word
        if len(line) >= 2:  # at least 2 words on line
            ll_word = line[-1]
            if line_idx < n_lines - 1:
                b_wp_ll.append((ll_word, section))
            else:
                b_pf_ll.append((ll_word, section))

n_b_wp_ll = len(b_wp_ll)
n_b_pf_ll = len(b_pf_ll)

print(f"B WP-LL words: {n_b_wp_ll}")
print(f"B PF-LL words: {n_b_pf_ll}")
print()

# Compute base rates for qo-class onsets
qo_onsets = ['qo', 'qot', 'qok']
print("B base rates vs WP-LL vs PF-LL for qo-class:")
print(f"{'Onset':<8} {'Base rate':<12} {'WP-LL rate':<13} {'WP-LL enr':<11} {'PF-LL rate':<13} {'PF-LL enr':<10}")

for onset in qo_onsets:
    base_n = b_all_words.get(onset, 0)
    base_rate = base_n / b_all_words_n if b_all_words_n > 0 else 0

    wp_n = sum(1 for w, _ in b_wp_ll if get_onset(w) == onset)
    wp_rate = wp_n / n_b_wp_ll if n_b_wp_ll > 0 else 0
    wp_enr = wp_rate / base_rate if base_rate > 0 else 0

    pf_n = sum(1 for w, _ in b_pf_ll if get_onset(w) == onset)
    pf_rate = pf_n / n_b_pf_ll if n_b_pf_ll > 0 else 0
    pf_enr = pf_rate / base_rate if base_rate > 0 else 0

    print(f"  {onset:<6} {base_rate:.4f}({base_n}) {wp_rate:.4f}({wp_n})  {wp_enr:.2f}×     {pf_rate:.4f}({pf_n})  {pf_enr:.2f}×")

print()
print("Full onset enrichment at B PF-LL vs base rate:")
pf_ll_counter = Counter(get_onset(w) for w, _ in b_pf_ll)
pf_ll_words = Counter(w for w, _ in b_pf_ll)
wp_ll_counter = Counter(get_onset(w) for w, _ in b_wp_ll)

for onset, _ in ONSET_ORDER:
    base_r = b_all_words.get(onset, 0) / b_all_words_n if b_all_words_n > 0 else 0
    pf_r = pf_ll_counter.get(onset, 0) / n_b_pf_ll if n_b_pf_ll > 0 else 0
    wp_r = wp_ll_counter.get(onset, 0) / n_b_wp_ll if n_b_wp_ll > 0 else 0
    pf_enr = pf_r / base_r if base_r > 0 else 0
    wp_enr = wp_r / base_r if base_r > 0 else 0
    if pf_ll_counter.get(onset, 0) > 0 or wp_ll_counter.get(onset, 0) > 2:
        print(f"  {onset:<6}: base={base_r:.4f}  pf_ll={pf_r:.4f}({pf_ll_counter.get(onset,0)}) {pf_enr:.2f}×  "
              f"wp_ll={wp_r:.4f}({wp_ll_counter.get(onset,0)}) {wp_enr:.2f}×")

print()
print(f"Top B PF-LL words (n={n_b_pf_ll}):")
for word, cnt in pf_ll_words.most_common(15):
    print(f"  {word:<15} n={cnt:3d}  onset={get_onset(word)}")

print()
print("B PF-LL by section:")
pf_ll_section = defaultdict(list)
for w, sec in b_pf_ll:
    pf_ll_section[sec].append(w)
for sec, words in sorted(pf_ll_section.items()):
    qot_words = [w for w in words if w.startswith('qot')]
    qo_words = [w for w in words if get_onset(w) in ['qo','qot','qok']]
    print(f"  {sec:<10}: n={len(words):3d}  qo-class={len(qo_words)}({len(qo_words)/len(words)*100:.1f}%)  "
          f"qot={len(qot_words)}({len(qot_words)/len(words)*100:.1f}%)")

print()
print("B WP-LL qo-class comparison (for contrast):")
for onset in qo_onsets:
    wp_n = sum(1 for w, _ in b_wp_ll if get_onset(w) == onset)
    base_n = b_all_words.get(onset, 0)
    base_rate = base_n / b_all_words_n if b_all_words_n > 0 else 0
    wp_rate = wp_n / n_b_wp_ll if n_b_wp_ll > 0 else 0
    wp_enr = wp_rate / base_rate if base_rate > 0 else 0
    print(f"  {onset:<6}: B WP-LL n={wp_n}/{n_b_wp_ll} = {wp_rate:.4f} ({wp_enr:.2f}× vs base {base_rate:.4f})")
