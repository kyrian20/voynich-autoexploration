"""
exp_206: H386 B edy-suffix para-terminal class; H387 A qo-onset grammar (sh→qo→sh loop?);
         H388 A sh vs cth paragraph position; H389 B qo-onset grammar.
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

# ============================================================
# H386: B edy-Suffix Para-Terminal Class
# ============================================================
def h386_b_edy_para_terminal(paragraphs):
    print("=== H386: B edy-Suffix Para-Terminal Class ===")

    # All B edy-suffix words positional profile
    b_edy_pos = Counter()
    b_all_pos = Counter()
    b_edy_by_word = defaultdict(Counter)
    b_edy_section = defaultdict(Counter)

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            n = len(line)
            is_ps_line = (line_idx == 0)
            is_last_line = (line_idx == n_lines - 1)
            for pos, word in enumerate(line):
                if pos == 0:
                    cat = 'ps' if is_ps_line else 'wp_lf'
                elif pos == n - 1 and n > 1:
                    if is_last_line:
                        cat = 'pf_ll'
                    else:
                        cat = 'wp_ll'
                else:
                    cat = 'mid'
                b_all_pos[cat] += 1
                if word.endswith('edy') or word.endswith('eedy'):
                    b_edy_pos[cat] += 1
                    b_edy_by_word[word][cat] += 1
                    b_edy_section[para['section']][cat] += 1

    b_all_total = sum(b_all_pos.values())
    b_edy_total = sum(b_edy_pos.values())
    print(f"\nB edy-suffix words total: {b_edy_total}/{b_all_total} = {b_edy_total/b_all_total*100:.2f}%")

    print("\nB edy-suffix positional profile vs all-B baseline:")
    print(f"{'Cat':<8} {'edy_n':>6} {'edy%':>7} {'base%':>7} {'Enr':>6}")
    for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
        n = b_edy_pos.get(cat, 0)
        base_n = b_all_pos.get(cat, 0)
        base_rate = base_n / b_all_total if b_all_total > 0 else 0
        edy_rate = n / b_edy_total if b_edy_total > 0 else 0
        enr = edy_rate / base_rate if base_rate > 0 else 0
        print(f"{cat:<8} {n:>6} {edy_rate*100:>6.2f}% {base_rate*100:>6.2f}% {enr:>6.2f}×")

    print("\nTop B edy-suffix words by frequency (n>=3):")
    edy_counts = Counter({w: sum(cnt.values()) for w, cnt in b_edy_by_word.items()})
    for word, total in edy_counts.most_common(20):
        if total < 3:
            break
        pf = b_edy_by_word[word].get('pf_ll', 0)
        wll = b_edy_by_word[word].get('wp_ll', 0)
        mid = b_edy_by_word[word].get('mid', 0)
        lf = b_edy_by_word[word].get('wp_lf', 0)
        ps = b_edy_by_word[word].get('ps', 0)
        print(f"  {word}: n={total} | ps={ps} lf={lf} mid={mid} wll={wll} pfl={pf}")

    print("\nB edy-suffix by section (pf_ll count):")
    for section in sorted(b_edy_section):
        sc = b_edy_section[section]
        total = sum(sc.values())
        pf = sc.get('pf_ll', 0)
        wll = sc.get('wp_ll', 0)
        print(f"  {section}: n={total} pf_ll={pf} wp_ll={wll}")

    # Also compute A edy-suffix rate for comparison
    a_edy_total = 0
    a_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for w in line:
                a_total += 1
                if w.endswith('edy') or w.endswith('eedy'):
                    a_edy_total += 1
    print(f"\nA edy-suffix rate: {a_edy_total}/{a_total} = {a_edy_total/a_total*100:.2f}% (B: {b_edy_total/b_all_total*100:.2f}%)")

# ============================================================
# H387: A qo-Onset Grammar — Does qo→sh Create a Loop?
# ============================================================
def h387_a_qo_grammar(paragraphs):
    print("\n=== H387: A qo-Onset Grammar — sh→qo→sh Loop? ===")

    # All A bigrams baseline
    a_succ_onset = Counter()
    a_pred_onset = Counter()
    a_pair_total = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                a_succ_onset[get_onset(line[j+1])] += 1
                a_pred_onset[get_onset(line[j])] += 1
                a_pair_total += 1

    baseline_succ = {o: a_succ_onset[o] / a_pair_total for o in a_succ_onset}

    # qo-onset words: qo, qot, qok onset classes
    # Test each qo-class separately and combined
    for qo_class in ['qo', 'qot', 'qok']:
        print(f"\nA {qo_class}-onset successor profile:")
        qo_succ = Counter()
        qo_total = 0
        for para in paragraphs:
            if para['dialect'] != 'A':
                continue
            for line in para['lines']:
                for j in range(len(line) - 1):
                    if get_onset(line[j]) == qo_class:
                        qo_succ[get_onset(line[j+1])] += 1
                        qo_total += 1
        print(f"  n={qo_total} bigrams")
        for onset in sorted(baseline_succ, key=lambda o: -qo_succ.get(o, 0)):
            n = qo_succ.get(onset, 0)
            if n < 2 and onset not in ('sh', 'cth', 'ch', 'd'):
                continue
            base = baseline_succ.get(onset, 0)
            pct = n / qo_total if qo_total > 0 else 0
            enr = pct / base if base > 0 else 0
            print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")

    # Combined qo-class
    print("\nA combined qo-class (qo+qot+qok) successor profile:")
    qo_combined_succ = Counter()
    qo_combined_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                onset = get_onset(line[j])
                if onset in ('qo', 'qot', 'qok'):
                    qo_combined_succ[get_onset(line[j+1])] += 1
                    qo_combined_total += 1
    for onset in sorted(baseline_succ, key=lambda o: -qo_combined_succ.get(o, 0)):
        n = qo_combined_succ.get(onset, 0)
        if n < 3:
            continue
        base = baseline_succ.get(onset, 0)
        pct = n / qo_combined_total if qo_combined_total > 0 else 0
        enr = pct / base if base > 0 else 0
        print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")

    # Is there a [sh][qo][sh] triple?
    sh_qo_sh = 0
    sh_qo_total = 0
    qo_total_all = 0
    qo_sh_succ = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                onset_j = get_onset(line[j])
                if onset_j in ('qo', 'qot', 'qok'):
                    qo_total_all += 1
                    if j < len(line) - 1 and get_onset(line[j+1]) == 'sh':
                        qo_sh_succ += 1
                # [sh][qo][sh]
                if (j >= 1 and j < len(line) - 1 and
                        onset_j in ('qo', 'qot', 'qok') and
                        get_onset(line[j-1]) == 'sh'):
                    sh_qo_total += 1
                    if get_onset(line[j+1]) == 'sh':
                        sh_qo_sh += 1

    qo_sh_rate = qo_sh_succ / qo_total_all if qo_total_all > 0 else 0
    sh_rate_base = baseline_succ.get('sh', 0)
    print(f"\nA qo-class → sh successor: {qo_sh_succ}/{qo_total_all} = {qo_sh_rate*100:.2f}% (base {sh_rate_base*100:.2f}%, {qo_sh_rate/sh_rate_base:.2f}×)")

    sh_rate_for_triple = qo_sh_succ / qo_combined_total if qo_combined_total > 0 else 0
    expected_triple = sh_qo_total * sh_rate_for_triple
    print(f"\n[sh][qo][sh] triple: {sh_qo_total} [sh][qo] cases; expected triple (indep): {expected_triple:.1f}; actual: {sh_qo_sh}")
    if expected_triple > 0:
        print(f"  Enrichment: {sh_qo_sh/expected_triple:.2f}×")

# ============================================================
# H388: A sh vs cth Paragraph Position
# ============================================================
def h388_sh_cth_paragraph_position(paragraphs):
    print("\n=== H388: A sh vs cth Paragraph Position ===")

    # For each paragraph, track word onset by relative line position
    # relative position: line_idx / (n_lines - 1) → binned into 5 groups
    sh_by_linepos = Counter()  # {line_idx_str: count}
    cth_by_linepos = Counter()
    other_by_linepos = Counter()

    # Also: absolute line index 0,1,2,3,4+
    sh_by_absline = Counter()
    cth_by_absline = Counter()
    total_by_absline = Counter()

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        n_lines = len(lines)
        if n_lines == 0:
            continue
        for line_idx, line in enumerate(lines):
            abs_label = str(min(line_idx, 5))  # 0,1,2,3,4,5+
            for word in line:
                onset = get_onset(word)
                total_by_absline[abs_label] += 1
                if onset == 'sh':
                    sh_by_absline[abs_label] += 1
                elif onset == 'cth':
                    cth_by_absline[abs_label] += 1

    # Print rates per paragraph line index
    print("\nA sh-onset and cth-onset rate by paragraph line index (0=first, 5+=all remaining):")
    print(f"{'LineIdx':<8} {'total':>6} {'sh_n':>5} {'sh%':>6} {'cth_n':>6} {'cth%':>6}")
    for li in sorted(total_by_absline, key=lambda x: int(x)):
        total = total_by_absline[li]
        sh_n = sh_by_absline.get(li, 0)
        cth_n = cth_by_absline.get(li, 0)
        sh_rate = sh_n / total if total > 0 else 0
        cth_rate = cth_n / total if total > 0 else 0
        print(f"{li:<8} {total:>6} {sh_n:>5} {sh_rate*100:>5.2f}% {cth_n:>6} {cth_rate*100:>5.2f}%")

    # Also: sh and cth relative to paragraph-first (line 0) vs paragraph-last (last line) vs middle
    sh_para_pos = Counter()  # first / middle / last
    cth_para_pos = Counter()
    all_para_pos = Counter()

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            if n_lines == 1:
                pos_label = 'only'
            elif line_idx == 0:
                pos_label = 'first'
            elif line_idx == n_lines - 1:
                pos_label = 'last'
            else:
                pos_label = 'middle'
            for word in line:
                all_para_pos[pos_label] += 1
                if get_onset(word) == 'sh':
                    sh_para_pos[pos_label] += 1
                elif get_onset(word) == 'cth':
                    cth_para_pos[pos_label] += 1

    total_all = sum(all_para_pos.values())
    sh_total = sum(sh_para_pos.values())
    cth_total = sum(cth_para_pos.values())

    print("\nA sh vs cth by paragraph line position (first/middle/last):")
    print(f"{'ParaPos':<8} {'total':>6} {'sh_n':>5} {'sh%':>6} {'sh_enr':>8} {'cth_n':>6} {'cth%':>6} {'cth_enr':>9}")
    for pos in ['only', 'first', 'middle', 'last']:
        total = all_para_pos.get(pos, 0)
        sh_n = sh_para_pos.get(pos, 0)
        cth_n = cth_para_pos.get(pos, 0)
        if total == 0:
            continue
        base_rate = total / total_all
        sh_rate = sh_n / sh_total if sh_total > 0 else 0
        cth_rate = cth_n / cth_total if cth_total > 0 else 0
        sh_enr = sh_rate / base_rate if base_rate > 0 else 0
        cth_enr = cth_rate / base_rate if base_rate > 0 else 0
        print(f"{pos:<8} {total:>6} {sh_n:>5} {sh_rate*100:>5.2f}% {sh_enr:>7.2f}× {cth_n:>6} {cth_rate*100:>5.2f}% {cth_enr:>8.2f}×")

# ============================================================
# H389: B qo-Onset Grammar
# ============================================================
def h389_b_qo_grammar(paragraphs):
    print("\n=== H389: B qo-Onset Grammar ===")

    # B baseline
    b_succ_onset = Counter()
    b_pred_onset = Counter()
    b_pair_total = 0
    b_word_total = 0
    b_qo_total = 0

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                b_word_total += 1
                onset_j = get_onset(line[j])
                if onset_j in ('qo', 'qot', 'qok'):
                    b_qo_total += 1
                if j < len(line) - 1:
                    b_succ_onset[get_onset(line[j+1])] += 1
                    b_pair_total += 1

    baseline_succ = {o: b_succ_onset[o] / b_pair_total for o in b_succ_onset}

    print(f"\nB qo-class (qo+qot+qok) total: {b_qo_total}/{b_word_total} = {b_qo_total/b_word_total*100:.2f}%")

    # Compare A qo-class rate
    a_qo_total = 0
    a_word_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for w in line:
                a_word_total += 1
                if get_onset(w) in ('qo', 'qot', 'qok'):
                    a_qo_total += 1
    print(f"A qo-class total: {a_qo_total}/{a_word_total} = {a_qo_total/a_word_total*100:.2f}%")

    # B qo-onset successor profiles per class
    for qo_class in ['qo', 'qot', 'qok']:
        print(f"\nB {qo_class}-onset successor profile:")
        qo_succ = Counter()
        qo_total = 0
        for para in paragraphs:
            if para['dialect'] != 'B':
                continue
            for line in para['lines']:
                for j in range(len(line) - 1):
                    if get_onset(line[j]) == qo_class:
                        qo_succ[get_onset(line[j+1])] += 1
                        qo_total += 1
        print(f"  n={qo_total} bigrams")
        for onset in sorted(baseline_succ, key=lambda o: -qo_succ.get(o, 0)):
            n = qo_succ.get(onset, 0)
            if n < 3 and onset not in ('sh', 'cth', 'ch', 'd'):
                continue
            base = baseline_succ.get(onset, 0)
            pct = n / qo_total if qo_total > 0 else 0
            enr = pct / base if base > 0 else 0
            print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")

    # B qo-class positional profile
    print("\nB qo-class positional profile:")
    b_qo_pos = Counter()
    b_all_pos = Counter()
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            n = len(line)
            is_ps = (line_idx == 0)
            is_last = (line_idx == n_lines - 1)
            for pos, word in enumerate(line):
                if pos == 0:
                    cat = 'ps' if is_ps else 'wp_lf'
                elif pos == n - 1 and n > 1:
                    cat = 'pf_ll' if is_last else 'wp_ll'
                else:
                    cat = 'mid'
                b_all_pos[cat] += 1
                if get_onset(word) in ('qo', 'qot', 'qok'):
                    b_qo_pos[cat] += 1

    b_all_total = sum(b_all_pos.values())
    b_qo_pos_total = sum(b_qo_pos.values())
    print(f"{'Cat':<8} {'qo_n':>6} {'qo%':>7} {'base%':>7} {'Enr':>6}")
    for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
        n = b_qo_pos.get(cat, 0)
        base_n = b_all_pos.get(cat, 0)
        base_rate = base_n / b_all_total if b_all_total > 0 else 0
        qo_rate = n / b_qo_pos_total if b_qo_pos_total > 0 else 0
        enr = qo_rate / base_rate if base_rate > 0 else 0
        print(f"{cat:<8} {n:>6} {qo_rate*100:>6.2f}% {base_rate*100:>6.2f}% {enr:>6.2f}×")

    # A qo-class positional for comparison
    print("\nA qo-class positional profile (comparison):")
    a_qo_pos = Counter()
    a_all_pos = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            n = len(line)
            is_ps = (line_idx == 0)
            is_last = (line_idx == n_lines - 1)
            for pos, word in enumerate(line):
                if pos == 0:
                    cat = 'ps' if is_ps else 'wp_lf'
                elif pos == n - 1 and n > 1:
                    cat = 'pf_ll' if is_last else 'wp_ll'
                else:
                    cat = 'mid'
                a_all_pos[cat] += 1
                if get_onset(word) in ('qo', 'qot', 'qok'):
                    a_qo_pos[cat] += 1

    a_all_total = sum(a_all_pos.values())
    a_qo_pos_total = sum(a_qo_pos.values())
    for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
        n = a_qo_pos.get(cat, 0)
        base_n = a_all_pos.get(cat, 0)
        base_rate = base_n / a_all_total if a_all_total > 0 else 0
        qo_rate = n / a_qo_pos_total if a_qo_pos_total > 0 else 0
        enr = qo_rate / base_rate if base_rate > 0 else 0
        print(f"{cat:<8} {n:>6} {qo_rate*100:>6.2f}% {base_rate*100:>6.2f}% {enr:>6.2f}×")

def main():
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    A_count = sum(1 for p in paragraphs if p['dialect'] == 'A')
    B_count = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"Paragraphs: A={A_count}, B={B_count}, total={len(paragraphs)}")

    h386_b_edy_para_terminal(paragraphs)
    h387_a_qo_grammar(paragraphs)
    h388_sh_cth_paragraph_position(paragraphs)
    h389_b_qo_grammar(paragraphs)

if __name__ == '__main__':
    main()
