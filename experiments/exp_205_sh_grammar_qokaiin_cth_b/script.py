"""
exp_205: H382 sh-grammar neighborhood in A; H383 qokaiin positional profile A vs B;
         H384 B-dialect cth-rate and cth-word positional profile; H385 [ch][daiin][cth][daiin] quadruple.
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

def get_section(folio_base):
    try:
        n = int(re.sub(r'[a-z]', '', folio_base))
    except:
        return 'other'
    if 1 <= n <= 66:
        return 'herbal'
    elif 67 <= n <= 73:
        return 'pharma'
    elif 67 <= n <= 73 or 103 <= n <= 116:
        return 'pharma'
    elif 68 <= n <= 73:
        return 'pharma'
    elif 74 <= n <= 84:
        return 'astro'
    elif 85 <= n <= 102:
        return 'bio'
    elif 103 <= n <= 116:
        return 'pharma'
    elif 117 <= n <= 146:
        return 'stars'
    elif 147 <= n <= 202:
        return 'cosmo'
    elif 203 <= n <= 234:
        return 'recipe'
    else:
        return 'other'

def get_section_v2(folio_base):
    """Better section assignment."""
    try:
        n = int(re.sub(r'[a-z]', '', folio_base))
    except:
        return 'other'
    if 1 <= n <= 66:
        return 'herbal'
    elif 67 <= n <= 73:
        return 'pharma'
    elif 74 <= n <= 84:
        return 'astro'
    elif 85 <= n <= 102:
        return 'bio'
    elif 103 <= n <= 116:
        return 'pharma'
    elif 117 <= n <= 146:
        return 'stars'
    elif 147 <= n <= 202:
        return 'cosmo'
    elif 203 <= n <= 234:
        return 'recipe'
    else:
        return 'other'

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
    return 'other'

def parse_corpus():
    # Pass 1: dialect detection per folio (use endswith matching as in exp_204)
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

    # Pass 2: build paragraphs
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

def positional_profile(paragraphs, word_filter, dialect_filter=None):
    """Return positional counts for words matching word_filter."""
    counts = Counter()
    for para in paragraphs:
        if dialect_filter and para['dialect'] != dialect_filter:
            continue
        lines = para['lines']
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            n = len(line)
            is_ps_line = (line_idx == 0)
            is_last_line = (line_idx == n_lines - 1)
            for pos, word in enumerate(line):
                if not word_filter(word):
                    continue
                if pos == 0:
                    cat = 'ps' if is_ps_line else 'wp_lf'
                elif pos == n - 1 and n > 1:
                    if is_last_line:
                        cat = 'pf_ll'
                    else:
                        cat = 'wp_ll'
                else:
                    cat = 'mid'
                counts[cat] += 1
    return counts

# ============================================================
# H382: sh-Word Grammar Neighborhood in A
# ============================================================
def h382_sh_grammar_a(paragraphs):
    print("=== H382: sh-Word Grammar Neighborhood in A ===")
    # Predecessor and successor profiles for sh-onset words in A
    # Also: what specifically precedes sh-words most often?
    sh_pred_onset = Counter()
    sh_succ_onset = Counter()
    sh_pred_word = Counter()
    sh_succ_word = Counter()
    all_pairs_total = 0
    all_onset_pred = Counter()
    all_onset_succ = Counter()

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                w = line[j]
                if j > 0:
                    all_pairs_total += 1
                    all_onset_pred[get_onset(line[j-1])] += 1
                if j > 0 and get_onset(w) == 'sh':
                    sh_pred_onset[get_onset(line[j-1])] += 1
                    sh_pred_word[line[j-1]] += 1
                if j < len(line) - 1 and get_onset(w) == 'sh':
                    sh_succ_onset[get_onset(line[j+1])] += 1
                    sh_succ_word[line[j+1]] += 1

    # Total sh-onset words
    sh_total = sum(sh_pred_onset.values())
    print(f"\nTotal A sh-onset bigrams (as successor): {sh_total}")
    print(f"Total A bigrams: {all_pairs_total}")

    # Baseline: across all A bigrams, what fraction of predecessors have each onset?
    baseline_pred = {o: all_onset_pred[o] / all_pairs_total for o in all_onset_pred}
    sh_rate_overall = sh_total / all_pairs_total
    print(f"sh-onset overall rate as successor: {sh_rate_overall:.4f}")

    # Predecessor profile
    print("\nA sh-word predecessor onset enrichment (who precedes sh-words):")
    print(f"{'Onset':<8} {'sh_n':>6} {'sh%':>7} {'base%':>7} {'Enr':>6}")
    pred_total = sum(sh_pred_onset.values())
    for onset in sorted(all_onset_pred, key=lambda o: -sh_pred_onset.get(o, 0)):
        n = sh_pred_onset.get(onset, 0)
        if n < 2:
            continue
        pct = n / pred_total
        base_pct = baseline_pred.get(onset, 0)
        enr = pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>6} {pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    # Top predecessor words
    print("\nTop 10 predecessor words before sh-words:")
    for word, n in sh_pred_word.most_common(10):
        print(f"  {word}: {n}")

    # Successor profile for sh-onset words
    succ_total = sum(sh_succ_onset.values())
    print(f"\nA sh-word successor onset enrichment (who follows sh-words):")
    print(f"{'Onset':<8} {'sh_n':>6} {'sh%':>7} {'base%':>7} {'Enr':>6}")

    # Baseline for successors: need the successor-side baseline
    all_succ_onset = Counter()
    total_succ_pairs = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                all_succ_onset[get_onset(line[j+1])] += 1
                total_succ_pairs += 1
    baseline_succ = {o: all_succ_onset[o] / total_succ_pairs for o in all_succ_onset}

    for onset in sorted(all_succ_onset, key=lambda o: -sh_succ_onset.get(o, 0)):
        n = sh_succ_onset.get(onset, 0)
        if n < 2:
            continue
        pct = n / succ_total
        base_pct = baseline_succ.get(onset, 0)
        enr = pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>6} {pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print("\nTop 10 successor words after sh-words:")
    for word, n in sh_succ_word.most_common(10):
        print(f"  {word}: {n}")

    # Specific sh-word breakdown
    print("\nSh-word frequency table (n>=5):")
    sh_word_count = Counter()
    sh_word_cth_succ = Counter()
    sh_word_daiin_succ = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                w = line[j]
                if get_onset(w) != 'sh':
                    continue
                sh_word_count[w] += 1
                if j < len(line) - 1:
                    s = line[j+1]
                    if get_onset(s) == 'cth':
                        sh_word_cth_succ[w] += 1
                    if s == 'daiin':
                        sh_word_daiin_succ[w] += 1

    cth_base = baseline_succ.get('cth', 0)
    daiin_base = all_succ_onset.get('daiin', 0) / total_succ_pairs if 'daiin' in all_succ_onset else 0
    # daiin base rate
    daiin_cnt = sum(1 for para in paragraphs if para['dialect'] == 'A'
                    for line in para['lines'] for w in line if w == 'daiin')
    daiin_rate_base = daiin_cnt / (sum(len(line) for para in paragraphs if para['dialect'] == 'A'
                                       for line in para['lines']))

    print(f"{'Word':<12} {'total':>6} {'cth_n':>6} {'cth%':>7} {'cth_enr':>8} {'daiin_n':>7} {'daiin%':>8}")
    for word, total in sh_word_count.most_common(20):
        if total < 3:
            continue
        cth_n = sh_word_cth_succ[word]
        daiin_n = sh_word_daiin_succ[word]
        # Use succ pairs for this word
        succ_pairs_word = total  # approximate (each occurrence has a successor unless last in line)
        cth_pct = cth_n / total
        daiin_pct = daiin_n / total
        cth_enr = cth_pct / cth_base if cth_base > 0 else 0
        print(f"{word:<12} {total:>6} {cth_n:>6} {cth_pct*100:>6.2f}% {cth_enr:>7.2f}× {daiin_n:>7} {daiin_pct*100:>7.2f}%")

# ============================================================
# H383: qokaiin Positional Profile in A vs B
# ============================================================
def h383_qokaiin_positional(paragraphs):
    print("\n=== H383: qokaiin Positional Profile A vs B ===")

    for dialect in ['A', 'B']:
        counts = positional_profile(paragraphs, lambda w: w == 'qokaiin', dialect_filter=dialect)
        total = sum(counts.values())
        print(f"\n{dialect}-dialect qokaiin: n={total}")
        if total == 0:
            print("  (no occurrences)")
            continue
        for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
            n = counts.get(cat, 0)
            print(f"  {cat}: {n} ({n/total*100:.1f}%)")

    # Also compare qokaiin's bigram environment in A
    print("\nA qokaiin predecessor/successor onset profile:")
    qokaiin_pred = Counter()
    qokaiin_succ = Counter()
    total_pred = 0
    total_succ = 0
    baseline_pred_A = Counter()
    baseline_succ_A = Counter()
    bp_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                w = line[j]
                if j > 0:
                    baseline_pred_A[get_onset(line[j-1])] += 1
                    bp_total += 1
                if j < len(line) - 1:
                    baseline_succ_A[get_onset(line[j+1])] += 1
                if w == 'qokaiin':
                    if j > 0:
                        qokaiin_pred[get_onset(line[j-1])] += 1
                        total_pred += 1
                    if j < len(line) - 1:
                        qokaiin_succ[get_onset(line[j+1])] += 1
                        total_succ += 1

    if total_pred > 0:
        print(f"qokaiin predecessor n={total_pred}; successor n={total_succ}")
        print("Successor profile:")
        bs_total = sum(baseline_succ_A.values())
        for onset in sorted(baseline_succ_A, key=lambda o: -qokaiin_succ.get(o, 0)):
            n = qokaiin_succ.get(onset, 0)
            if n == 0 and onset not in ('cth', 'ch', 'sh', 'd'):
                continue
            base = baseline_succ_A.get(onset, 0) / bs_total
            pct = n / total_succ if total_succ > 0 else 0
            enr = pct / base if base > 0 else 0
            print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")

# ============================================================
# H384: B-Dialect cth-Rate and cth-Word Positional Profile
# ============================================================
def h384_b_cth_profile(paragraphs):
    print("\n=== H384: B-Dialect cth-Rate and cth-Word Positional Profile ===")

    # Overall cth rate in B
    b_total = 0
    b_cth = 0
    b_cth_words = Counter()
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line in para['lines']:
            for w in line:
                b_total += 1
                if get_onset(w) == 'cth':
                    b_cth += 1
                    b_cth_words[w] += 1

    a_total = 0
    a_cth = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for w in line:
                a_total += 1
                if get_onset(w) == 'cth':
                    a_cth += 1

    print(f"\nA-dialect: cth words = {a_cth}/{a_total} = {a_cth/a_total*100:.3f}%")
    print(f"B-dialect: cth words = {b_cth}/{b_total} = {b_cth/b_total*100:.3f}%")

    print(f"\nTop B cth-words:")
    for w, n in b_cth_words.most_common(10):
        print(f"  {w}: {n}")

    # cth-word positional profile in B
    print("\nB cth-word positional profile:")
    b_cth_pos = positional_profile(paragraphs, lambda w: get_onset(w) == 'cth', dialect_filter='B')
    b_total_pos = positional_profile(paragraphs, lambda w: True, dialect_filter='B')
    b_all_total = sum(b_total_pos.values())
    b_cth_total = sum(b_cth_pos.values())
    print(f"B cth word total positioned: {b_cth_total}")
    for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
        n = b_cth_pos.get(cat, 0)
        base_n = b_total_pos.get(cat, 0)
        base_rate = base_n / b_all_total if b_all_total > 0 else 0
        cth_rate = n / b_cth_total if b_cth_total > 0 else 0
        enr = cth_rate / base_rate if base_rate > 0 else 0
        print(f"  {cat}: {n} ({cth_rate*100:.1f}%, base {base_rate*100:.1f}%, {enr:.2f}×)")

    # A cth-word positional profile for comparison
    print("\nA cth-word positional profile (comparison):")
    a_cth_pos = positional_profile(paragraphs, lambda w: get_onset(w) == 'cth', dialect_filter='A')
    a_total_pos = positional_profile(paragraphs, lambda w: True, dialect_filter='A')
    a_all_total = sum(a_total_pos.values())
    a_cth_total = sum(a_cth_pos.values())
    for cat in ['ps', 'wp_lf', 'mid', 'wp_ll', 'pf_ll']:
        n = a_cth_pos.get(cat, 0)
        base_n = a_total_pos.get(cat, 0)
        base_rate = base_n / a_all_total if a_all_total > 0 else 0
        cth_rate = n / a_cth_total if a_cth_total > 0 else 0
        enr = cth_rate / base_rate if base_rate > 0 else 0
        print(f"  {cat}: {n} ({cth_rate*100:.1f}%, base {base_rate*100:.1f}%, {enr:.2f}×)")

    # B bigram environment of cth-words
    print("\nB cth-word successor onset profile:")
    b_cth_succ = Counter()
    b_all_succ = Counter()
    b_pair_total = 0
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                b_all_succ[get_onset(line[j+1])] += 1
                b_pair_total += 1
                if get_onset(line[j]) == 'cth':
                    b_cth_succ[get_onset(line[j+1])] += 1

    cth_succ_total = sum(b_cth_succ.values())
    print(f"B cth-word bigrams: {cth_succ_total}")
    for onset in sorted(b_all_succ, key=lambda o: -b_cth_succ.get(o, 0)):
        n = b_cth_succ.get(onset, 0)
        if n < 2:
            continue
        base = b_all_succ[onset] / b_pair_total
        pct = n / cth_succ_total if cth_succ_total > 0 else 0
        enr = pct / base if base > 0 else 0
        print(f"  {onset}: {n} ({pct*100:.1f}%, base {base*100:.1f}%, {enr:.2f}×)")

# ============================================================
# H385: [ch][daiin][cth][daiin] Quadruple in A + cross-line cth@LL → daiin@LF
# ============================================================
def h385_quadruple(paragraphs):
    print("\n=== H385: [ch][daiin][cth][daiin] Quadruple in A ===")

    # Count full quadruple vs expected from independent triple+daiin
    quad_total = 0       # [ch][daiin][cth][daiin]
    triple_total = 0     # [ch][daiin][cth]
    cth_daiin_pairs = 0  # [cth][daiin]
    cth_total_pairs = 0  # all cth bigrams

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line)):
                w = line[j]
                # Count cth-daiin pairs
                if get_onset(w) == 'cth' and j < len(line) - 1:
                    cth_total_pairs += 1
                    if line[j+1] == 'daiin':
                        cth_daiin_pairs += 1
                # Count triples: ch -> daiin -> cth
                if (j >= 2 and get_onset(w) == 'cth' and
                        line[j-1] == 'daiin' and get_onset(line[j-2]) == 'ch'):
                    triple_total += 1
                # Count quadruple: ch -> daiin -> cth -> daiin
                if (j >= 2 and j < len(line) - 1 and
                        get_onset(w) == 'cth' and
                        line[j-1] == 'daiin' and get_onset(line[j-2]) == 'ch' and
                        line[j+1] == 'daiin'):
                    quad_total += 1

    # Expected quadruple from independence: triple * cth_daiin_rate
    cth_daiin_rate = cth_daiin_pairs / cth_total_pairs if cth_total_pairs > 0 else 0
    expected_quad = triple_total * cth_daiin_rate
    enr_quad = quad_total / expected_quad if expected_quad > 0 else 0

    print(f"\nA triples [ch][daiin][cth]: {triple_total}")
    print(f"A cth→daiin rate: {cth_daiin_pairs}/{cth_total_pairs} = {cth_daiin_rate*100:.2f}%")
    print(f"Expected quads (if independent): {expected_quad:.1f}")
    print(f"Actual quads [ch][daiin][cth][daiin]: {quad_total}")
    print(f"Quadruple enrichment: {enr_quad:.2f}×")

    # Cross-line: cth@last_word_of_line -> daiin@first_word_of_next_line
    print("\nCross-line: cth@LL → daiin@first-word-of-next-line in A:")
    crossline_total = 0
    crossline_cth_ll = 0
    crossline_cth_daiin = 0
    daiin_as_lf_total = 0
    all_lf_total = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        for li in range(len(lines) - 1):
            line = lines[li]
            next_line = lines[li + 1]
            if not line or not next_line:
                continue
            last_word = line[-1]
            first_next = next_line[0]
            crossline_total += 1
            all_lf_total += 1
            if first_next == 'daiin':
                daiin_as_lf_total += 1
            if get_onset(last_word) == 'cth':
                crossline_cth_ll += 1
                if first_next == 'daiin':
                    crossline_cth_daiin += 1

    daiin_lf_rate = daiin_as_lf_total / all_lf_total if all_lf_total > 0 else 0
    cth_ll_daiin_rate = crossline_cth_daiin / crossline_cth_ll if crossline_cth_ll > 0 else 0
    enr_cross = cth_ll_daiin_rate / daiin_lf_rate if daiin_lf_rate > 0 else 0

    print(f"  Total cross-line transitions: {crossline_total}")
    print(f"  daiin as line-opener rate: {daiin_as_lf_total}/{all_lf_total} = {daiin_lf_rate*100:.2f}%")
    print(f"  cth@LL cases: {crossline_cth_ll}")
    print(f"  cth@LL → daiin@LF: {crossline_cth_daiin} ({cth_ll_daiin_rate*100:.2f}%)")
    print(f"  Enrichment: {enr_cross:.2f}×")

    # Also check cross-line daiin@LL -> cth@LF
    print("\nCross-line: daiin@LL → cth@first-word-of-next-line in A:")
    daiin_ll_total = 0
    daiin_ll_cth_lf = 0
    cth_as_lf_total = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        for li in range(len(lines) - 1):
            line = lines[li]
            next_line = lines[li + 1]
            if not line or not next_line:
                continue
            last_word = line[-1]
            first_next = next_line[0]
            if get_onset(first_next) == 'cth':
                cth_as_lf_total += 1
            if last_word == 'daiin':
                daiin_ll_total += 1
                if get_onset(first_next) == 'cth':
                    daiin_ll_cth_lf += 1

    cth_lf_rate = cth_as_lf_total / all_lf_total if all_lf_total > 0 else 0
    daiin_ll_cth_rate = daiin_ll_cth_lf / daiin_ll_total if daiin_ll_total > 0 else 0
    enr_cross2 = daiin_ll_cth_rate / cth_lf_rate if cth_lf_rate > 0 else 0

    print(f"  cth as line-opener rate: {cth_as_lf_total}/{all_lf_total} = {cth_lf_rate*100:.2f}%")
    print(f"  daiin@LL cases: {daiin_ll_total}")
    print(f"  daiin@LL → cth@LF: {daiin_ll_cth_lf} ({daiin_ll_cth_rate*100:.2f}%)")
    print(f"  Enrichment: {enr_cross2:.2f}×")

    # Extended chain: [daiin][cth][daiin] triple
    print("\nExtended: [daiin][cth][daiin] triple in A:")
    dcd_total = 0
    total_cth_pairs = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(1, len(line) - 1):
                if get_onset(line[j]) == 'cth':
                    total_cth_pairs += 1
                    if line[j-1] == 'daiin' and line[j+1] == 'daiin':
                        dcd_total += 1

    # Expected from independence: (daiin->cth rate) * (cth->daiin rate)
    # daiin->cth rate already measured above (cth_daiin_rate is cth->daiin)
    # Need daiin->cth rate
    daiin_cth_pairs = 0
    daiin_total_pairs = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                if line[j] == 'daiin':
                    daiin_total_pairs += 1
                    if get_onset(line[j+1]) == 'cth':
                        daiin_cth_pairs += 1

    daiin_cth_rate = daiin_cth_pairs / daiin_total_pairs if daiin_total_pairs > 0 else 0
    # Rate of [daiin][cth] where the cth is followed by daiin
    # Expected: (# of daiin->cth pairs) * P(cth->daiin)
    expected_dcd = daiin_cth_pairs * cth_daiin_rate
    enr_dcd = dcd_total / expected_dcd if expected_dcd > 0 else 0
    print(f"  daiin→cth pairs: {daiin_cth_pairs}/{daiin_total_pairs} = {daiin_cth_rate*100:.2f}%")
    print(f"  cth→daiin pairs: {cth_daiin_pairs}/{cth_total_pairs} = {cth_daiin_rate*100:.2f}%")
    print(f"  Expected [daiin][cth][daiin]: {expected_dcd:.1f}")
    print(f"  Actual [daiin][cth][daiin]: {dcd_total}")
    print(f"  Enrichment: {enr_dcd:.2f}×")

def main():
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    A_count = sum(1 for p in paragraphs if p['dialect'] == 'A')
    B_count = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"Paragraphs: A={A_count}, B={B_count}, total={len(paragraphs)}")

    h382_sh_grammar_a(paragraphs)
    h383_qokaiin_positional(paragraphs)
    h384_b_cth_profile(paragraphs)
    h385_quadruple(paragraphs)

if __name__ == '__main__':
    main()
