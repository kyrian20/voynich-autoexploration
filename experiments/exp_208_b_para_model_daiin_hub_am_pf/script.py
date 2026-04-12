"""
exp_208: H394 B para-opening formula (what opens B paragraphs?);
         H395 daiin as hub in A (bridge between sh-domain and cth-domain);
         H396 complete B paragraph model (line-by-line register analysis);
         H397 -am words at A pf_ll vs WP-LL (is -am the A para-terminal suffix?)
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

# ==========================================================
# H394 + H396: B Para-Opening Formula + Complete B Paragraph
# ==========================================================
def h394_h396_b_para_model(paragraphs):
    print("=== H394 + H396: B Para-Opening Formula and Complete B Paragraph Model ===")

    # Collect B-dialect paragraph-level word data
    # For each word: dialect, line_idx (0=first, 1=second, ...), para-relative (first/mid/last line)
    # Also: position within line (0=LF/PS, mid, last)

    b_total_words = Counter()       # overall B onset count
    b_all_total = 0

    # Line-index buckets: 0, 1, 2, 3, 4, 5+
    b_line_onset = defaultdict(Counter)   # b_line_onset[line_idx_bucket] = Counter of onset
    b_line_total = defaultdict(int)

    # Para-position buckets: first / middle / last
    b_para_pos_onset = defaultdict(Counter)  # b_para_pos_onset['first'/'mid'/'last'] = Counter
    b_para_pos_total = defaultdict(int)

    # PS vs first-line body
    b_ps_onset = Counter()
    b_ps_total = 0
    b_fl_body_onset = Counter()
    b_fl_body_total = 0

    # PS word distribution (top words)
    b_ps_words = Counter()

    # Tier classification
    b_para_counts = 0

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        if not lines:
            continue
        b_para_counts += 1
        n_lines = len(lines)

        for line_idx, line in enumerate(lines):
            # line position in paragraph
            if n_lines == 1:
                para_pos = 'first'  # single-line para = first/last
            elif line_idx == 0:
                para_pos = 'first'
            elif line_idx == n_lines - 1:
                para_pos = 'last'
            else:
                para_pos = 'middle'

            line_bucket = min(line_idx, 5)  # 0,1,2,3,4,5+

            for pos, word in enumerate(line):
                onset = get_onset(word)
                b_total_words[onset] += 1
                b_all_total += 1
                b_line_onset[line_bucket][onset] += 1
                b_line_total[line_bucket] += 1
                b_para_pos_onset[para_pos][onset] += 1
                b_para_pos_total[para_pos] += 1

                # PS (pos=0, line_idx=0)
                if line_idx == 0 and pos == 0:
                    b_ps_onset[onset] += 1
                    b_ps_total += 1
                    b_ps_words[word] += 1
                # First-line body (pos>=1, line_idx=0)
                elif line_idx == 0 and pos >= 1:
                    b_fl_body_onset[onset] += 1
                    b_fl_body_total += 1

    print(f"\nB paragraphs: {b_para_counts}, total B words: {b_all_total}")

    print(f"\nB PS (pos=0, line_idx=0): n={b_ps_total}")
    print(f"{'Onset':<8} {'n':>5} {'%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(b_total_words, key=lambda o: -b_ps_onset.get(o, 0)):
        n = b_ps_onset.get(onset, 0)
        if n < 1:
            continue
        ps_pct = n / b_ps_total
        base_pct = b_total_words[onset] / b_all_total if b_all_total > 0 else 0
        enr = ps_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {ps_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print(f"\nTop 20 B PS words:")
    for word, n in b_ps_words.most_common(20):
        onset = get_onset(word)
        print(f"  {word} ({onset}): n={n}")

    print(f"\nB First-line body (pos>=1, line_idx=0): n={b_fl_body_total}")
    print(f"{'Onset':<8} {'n':>5} {'%':>7} {'base%':>7} {'Enr':>6}")
    for onset in sorted(b_total_words, key=lambda o: -b_fl_body_onset.get(o, 0)):
        n = b_fl_body_onset.get(onset, 0)
        if n < 2:
            continue
        fl_pct = n / b_fl_body_total
        base_pct = b_total_words[onset] / b_all_total
        enr = fl_pct / base_pct if base_pct > 0 else 0
        print(f"{onset:<8} {n:>5} {fl_pct*100:>6.2f}% {base_pct*100:>6.2f}% {enr:>6.2f}×")

    print("\n\nH396: B Paragraph Line-by-Line Onset Distribution")
    print("Line index | n_words | top onsets (enrichment vs B baseline)")
    for bucket in range(6):
        n = b_line_total.get(bucket, 0)
        if n < 10:
            continue
        label = str(bucket) if bucket < 5 else '5+'
        print(f"\n  Line {label} (n={n}):")
        print(f"  {'Onset':<8} {'n':>5} {'%':>7} {'base%':>7} {'Enr':>6}")
        onset_data = []
        for onset, cnt in b_line_onset[bucket].items():
            base = b_total_words[onset] / b_all_total if b_all_total > 0 else 0
            enr = (cnt / n) / base if base > 0 else 0
            onset_data.append((onset, cnt, cnt/n, base, enr))
        for onset, cnt, pct, base, enr in sorted(onset_data, key=lambda x: -x[4]):
            if cnt < 2:
                continue
            print(f"  {onset:<8} {cnt:>5} {pct*100:>6.2f}% {base*100:>6.2f}% {enr:>6.2f}×")

    print("\n\nH396: B Para-Position Summary (first/middle/last para line)")
    for ppos in ['first', 'middle', 'last']:
        n = b_para_pos_total.get(ppos, 0)
        print(f"\n  {ppos.upper()} lines (n={n}):")
        print(f"  {'Onset':<8} {'n':>5} {'%':>7} {'base%':>7} {'Enr':>6}")
        onset_data = []
        for onset, cnt in b_para_pos_onset.get(ppos, {}).items():
            base = b_total_words[onset] / b_all_total if b_all_total > 0 else 0
            enr = (cnt / n) / base if base > 0 else 0
            onset_data.append((onset, cnt, cnt/n, base, enr))
        for onset, cnt, pct, base, enr in sorted(onset_data, key=lambda x: -x[4]):
            if cnt < 2:
                continue
            print(f"  {onset:<8} {cnt:>5} {pct*100:>6.2f}% {base*100:>6.2f}% {enr:>6.2f}×")


# ==========================================================
# H395: daiin as Hub in A — Para Line Position and sh→daiin→cth
# ==========================================================
def h395_daiin_hub_a(paragraphs):
    print("\n\n=== H395: daiin as Central Hub in A-Dialect ===")

    # daiin enrichment by paragraph line index
    a_total_words = Counter()
    a_all_total = 0
    a_daiin_by_line = Counter()       # line_idx bucket
    a_total_by_line = Counter()

    # Also track daiin at WP-LL (last word of non-last lines)
    a_daiin_wp_ll = 0
    a_daiin_pf_ll = 0
    a_wp_ll_total = 0
    a_pf_ll_total = 0
    a_daiin_fl_ll = 0   # last word of first line (line_idx=0, last pos)
    a_fl_ll_total = 0

    # sh → daiin → cth triple: count by where the triple occurs (which para line)
    # Also: daiin cth-attraction by para line (does daiin→cth enrichment vary by line?)
    a_daiin_total_by_para_line = Counter()    # 'first','middle','last'
    a_daiin_cth_by_para_line = Counter()

    # Bigrams for analysis
    # To track daiin→cth by para position, scan all bigrams
    a_daiin_cth_count = 0
    a_daiin_total_bigrams = 0
    a_daiin_by_para_pos = Counter()
    a_daiin_cth_by_para_pos = Counter()

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        if not lines:
            continue
        n_lines = len(lines)

        for line_idx, line in enumerate(lines):
            # Para-position label
            if n_lines == 1:
                para_pos = 'first'
            elif line_idx == 0:
                para_pos = 'first'
            elif line_idx == n_lines - 1:
                para_pos = 'last'
            else:
                para_pos = 'middle'

            line_bucket = min(line_idx, 5)
            is_last_line = (line_idx == n_lines - 1)

            for pos, word in enumerate(line):
                a_total_words[get_onset(word)] += 1
                a_all_total += 1
                a_total_by_line[line_bucket] += 1
                if word == 'daiin':
                    a_daiin_by_line[line_bucket] += 1

                # WP-LL vs PF-LL for daiin
                if pos == len(line) - 1:  # last word of this line
                    if is_last_line:
                        a_pf_ll_total += 1
                        if word == 'daiin':
                            a_daiin_pf_ll += 1
                    else:
                        a_wp_ll_total += 1
                        if word == 'daiin':
                            a_daiin_wp_ll += 1
                        if line_idx == 0:
                            a_fl_ll_total += 1
                            if word == 'daiin':
                                a_daiin_fl_ll += 1

                # daiin by para position
                if word == 'daiin':
                    a_daiin_by_para_pos[para_pos] += 1

            # Bigrams within this line: daiin→cth tracking by para position
            for i in range(len(line) - 1):
                if line[i] == 'daiin':
                    a_daiin_total_bigrams += 1
                    a_daiin_by_para_pos[para_pos]  # already counted above for position
                    if get_onset(line[i+1]) == 'cth':
                        a_daiin_cth_count += 1
                        a_daiin_cth_by_para_pos[para_pos] += 1

    # Overall daiin baseline
    daiin_base_rate = a_total_words.get('daiin', 0) / a_all_total if a_all_total > 0 else 0
    print(f"\nA-dialect: total words={a_all_total}, daiin base rate={daiin_base_rate*100:.2f}%")
    print(f"  WP-LL: daiin={a_daiin_wp_ll}/{a_wp_ll_total} ({a_daiin_wp_ll/a_wp_ll_total*100:.2f}%)")
    enr = (a_daiin_wp_ll/a_wp_ll_total) / daiin_base_rate if daiin_base_rate > 0 and a_wp_ll_total > 0 else 0
    print(f"    Enrichment vs baseline: {enr:.2f}×")
    print(f"  PF-LL: daiin={a_daiin_pf_ll}/{a_pf_ll_total} ({a_daiin_pf_ll/a_pf_ll_total*100:.2f}%)")
    enr = (a_daiin_pf_ll/a_pf_ll_total) / daiin_base_rate if daiin_base_rate > 0 and a_pf_ll_total > 0 else 0
    print(f"    Enrichment vs baseline: {enr:.2f}×")
    print(f"  First-line LL (last word of first para line): daiin={a_daiin_fl_ll}/{a_fl_ll_total} ({a_daiin_fl_ll/a_fl_ll_total*100:.2f}% if >{0})")
    if a_fl_ll_total > 0:
        enr = (a_daiin_fl_ll/a_fl_ll_total) / daiin_base_rate if daiin_base_rate > 0 else 0
        print(f"    Enrichment vs baseline: {enr:.2f}×")

    print("\ndaiin by paragraph line index (0=first, 5+=late):")
    print(f"{'line_idx':<10} {'daiin_n':>8} {'line_n':>8} {'daiin%':>8} {'base%':>8} {'Enr':>6}")
    for bucket in range(6):
        n = a_total_by_line.get(bucket, 0)
        d = a_daiin_by_line.get(bucket, 0)
        if n < 5:
            continue
        pct = d / n
        enr = pct / daiin_base_rate if daiin_base_rate > 0 else 0
        label = str(bucket) if bucket < 5 else '5+'
        print(f"{'line_'+label:<10} {d:>8} {n:>8} {pct*100:>7.2f}% {daiin_base_rate*100:>7.2f}% {enr:>6.2f}×")

    print("\ndaiin→cth by paragraph position (first/middle/last line):")
    # Need separate bigram tracking by para position
    # Let me redo the bigram tracking
    daiin_bigrams_by_pos = defaultdict(lambda: {'total': 0, 'cth': 0})
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        if not lines:
            continue
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            if n_lines == 1:
                para_pos = 'first'
            elif line_idx == 0:
                para_pos = 'first'
            elif line_idx == n_lines - 1:
                para_pos = 'last'
            else:
                para_pos = 'middle'
            for i in range(len(line) - 1):
                if line[i] == 'daiin':
                    daiin_bigrams_by_pos[para_pos]['total'] += 1
                    if get_onset(line[i+1]) == 'cth':
                        daiin_bigrams_by_pos[para_pos]['cth'] += 1

    # Overall baseline: cth rate
    cth_rate = a_total_words.get('cth', 0) / a_all_total if a_all_total > 0 else 0
    print(f"  A-dialect cth-onset baseline rate: {cth_rate*100:.2f}%")
    print(f"  {'Para pos':<10} {'daiin_n':>8} {'cth_n':>6} {'cth%':>8} {'Enr':>6}")
    for ppos in ['first', 'middle', 'last']:
        stats = daiin_bigrams_by_pos[ppos]
        tot = stats['total']
        cth_n = stats['cth']
        if tot < 1:
            print(f"  {ppos:<10} {'—':>8} {'—':>6} {'—':>8} {'—':>6}")
            continue
        pct = cth_n / tot
        enr = pct / cth_rate if cth_rate > 0 else 0
        print(f"  {ppos:<10} {tot:>8} {cth_n:>6} {pct*100:>7.2f}% {enr:>6.2f}×")

    # sh → daiin: does daiin appear more after sh-words?
    print("\nsh-onset → daiin enrichment in A (by para position):")
    sh_daiin_by_pos = defaultdict(lambda: {'total': 0, 'daiin': 0})
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        if not lines:
            continue
        n_lines = len(lines)
        for line_idx, line in enumerate(lines):
            if n_lines == 1:
                para_pos = 'first'
            elif line_idx == 0:
                para_pos = 'first'
            elif line_idx == n_lines - 1:
                para_pos = 'last'
            else:
                para_pos = 'middle'
            for i in range(len(line) - 1):
                if get_onset(line[i]) == 'sh':
                    sh_daiin_by_pos[para_pos]['total'] += 1
                    if line[i+1] == 'daiin':
                        sh_daiin_by_pos[para_pos]['daiin'] += 1

    print(f"  A-dialect daiin base rate: {daiin_base_rate*100:.2f}%")
    for ppos in ['first', 'middle', 'last']:
        stats = sh_daiin_by_pos[ppos]
        tot = stats['total']
        d_n = stats['daiin']
        if tot < 1:
            continue
        pct = d_n / tot
        enr = pct / daiin_base_rate if daiin_base_rate > 0 else 0
        print(f"  sh→daiin [{ppos}]: n={tot}, daiin_n={d_n}, pct={pct*100:.2f}%, enr={enr:.2f}×")


# ==========================================================
# H397: -am Suffix at A pf_ll vs WP-LL vs Line-by-Line
# ==========================================================
def h397_am_pf_ll(paragraphs):
    print("\n\n=== H397: -am Suffix at A/B pf_ll vs WP-LL ===")

    for dialect in ['A', 'B']:
        am_all = 0
        total_all = 0
        am_wp_ll = 0
        total_wp_ll = 0
        am_pf_ll = 0
        total_pf_ll = 0
        am_mid = 0
        total_mid = 0
        am_lf = 0
        total_lf = 0

        # By paragraph line index for A
        am_by_line = Counter()
        total_by_line = Counter()

        for para in paragraphs:
            if para['dialect'] != dialect:
                continue
            lines = para['lines']
            if not lines:
                continue
            n_lines = len(lines)

            for line_idx, line in enumerate(lines):
                n_words = len(line)
                is_last_line = (line_idx == n_lines - 1)
                line_bucket = min(line_idx, 5)

                for pos, word in enumerate(line):
                    is_am = word.endswith('am')
                    total_all += 1
                    if is_am:
                        am_all += 1

                    # Position within line
                    is_lf = (pos == 0)
                    is_ll = (pos == n_words - 1)
                    is_mid_pos = (not is_lf and not is_ll) or (n_words <= 2)

                    if is_lf:
                        total_lf += 1
                        if is_am:
                            am_lf += 1
                    elif is_ll:
                        if is_last_line:
                            total_pf_ll += 1
                            if is_am:
                                am_pf_ll += 1
                        else:
                            total_wp_ll += 1
                            if is_am:
                                am_wp_ll += 1
                    else:
                        total_mid += 1
                        if is_am:
                            am_mid += 1

                    # By paragraph line index
                    total_by_line[line_bucket] += 1
                    if is_am:
                        am_by_line[line_bucket] += 1

        base = am_all / total_all if total_all > 0 else 0
        print(f"\n{dialect}-dialect: -am base rate = {am_all}/{total_all} = {base*100:.3f}%")

        def print_row(label, am, tot):
            if tot == 0:
                print(f"  {label:<20}: n=0")
                return
            pct = am / tot
            enr = pct / base if base > 0 else 0
            print(f"  {label:<20}: am={am}/{tot} ({pct*100:.3f}%), enr={enr:.2f}×")

        print_row("LF", am_lf, total_lf)
        print_row("MID", am_mid, total_mid)
        print_row("WP-LL", am_wp_ll, total_wp_ll)
        print_row("PF-LL", am_pf_ll, total_pf_ll)

        if dialect == 'A':
            print(f"\n  A -am by paragraph line index:")
            for bucket in range(6):
                n = total_by_line.get(bucket, 0)
                a = am_by_line.get(bucket, 0)
                if n < 5:
                    continue
                pct = a / n
                enr = pct / base if base > 0 else 0
                label = str(bucket) if bucket < 5 else '5+'
                print(f"    line {label}: am={a}/{n} ({pct*100:.3f}%), enr={enr:.2f}×")

        # Top -am words at pf_ll
        am_pf_words = Counter()
        am_wp_words = Counter()
        am_all_words = Counter()
        for para in paragraphs:
            if para['dialect'] != dialect:
                continue
            lines = para['lines']
            if not lines:
                continue
            n_lines = len(lines)
            for line_idx, line in enumerate(lines):
                is_last_line = (line_idx == n_lines - 1)
                for pos, word in enumerate(line):
                    if not word.endswith('am'):
                        continue
                    am_all_words[word] += 1
                    if pos == len(line) - 1:
                        if is_last_line:
                            am_pf_words[word] += 1
                        else:
                            am_wp_words[word] += 1

        print(f"\n  Top -am words at {dialect} PF-LL:")
        for word, n in am_pf_words.most_common(10):
            tot_w = am_all_words[word]
            print(f"    {word}: pf_ll={n}, all={tot_w}")
        print(f"  Top -am words at {dialect} WP-LL:")
        for word, n in am_wp_words.most_common(10):
            tot_w = am_all_words[word]
            print(f"    {word}: wp_ll={n}, all={tot_w}")


if __name__ == '__main__':
    paragraphs, folio_dialect = parse_corpus()
    a_count = sum(1 for p in paragraphs if p['dialect'] == 'A')
    b_count = sum(1 for p in paragraphs if p['dialect'] == 'B')
    print(f"Corpus: {len(paragraphs)} paragraphs — A={a_count}, B={b_count}")

    h394_h396_b_para_model(paragraphs)
    h395_daiin_hub_a(paragraphs)
    h397_am_pf_ll(paragraphs)
