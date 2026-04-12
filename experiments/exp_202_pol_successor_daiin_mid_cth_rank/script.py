"""
exp_202: pol-Prefix Successor Profile (H370), daiin@MID A Adjacency (H371),
         Unified cth-Introduction Ranking (H372), cosmo B shedy WP-LL vs PF-LL (H373)

Parser copied from exp_201 (working ZL3b paragraph-aware parser).
"""
import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


# ─────────────────────────────────────────────
# Parser (identical to exp_201)
# ─────────────────────────────────────────────

def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
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


def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    if w.startswith('y'): return 'y'
    if w.startswith('k'): return 'k'
    if w.startswith('t'): return 't'
    if w.startswith('l'): return 'l'
    if w.startswith('r'): return 'r'
    if w.startswith('p'): return 'p'
    if w.startswith('f'): return 'f'
    if w.startswith('o'): return 'o'
    return 'other'


def parse_corpus():
    # Pass 1: compute per-folio edy-rate for dialect detection
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

    folio_dialect = {fb: classify_dialect(stats)
                     for fb, stats in folio_word_stats.items()}

    # Pass 2: extract paragraphs
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
                current_para = {
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'lines': []
                }
                paragraphs.append(current_para)

            if current_para is not None:
                current_para['lines'].append(words)

    return paragraphs, folio_dialect


# ─────────────────────────────────────────────
# H370: pol-Prefix Word Successor Profile in B@LF
# ─────────────────────────────────────────────

def h370_pol_successor(paragraphs):
    print("=" * 60)
    print("H370: pol-Prefix Successor Profile at B@LF")
    print("=" * 60)

    pol_successor_onsets = Counter()
    pol_successor_words = Counter()
    pol_word_successors = defaultdict(Counter)
    pol_section_successors = defaultdict(Counter)

    baseline_second_onsets = Counter()

    n_pol_lf_lines = 0
    n_baseline = 0

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        section = para['section']
        for line in para['lines']:
            if len(line) < 2:
                continue
            first = line[0]
            second = line[1]
            second_onset = get_onset(second)
            baseline_second_onsets[second_onset] += 1
            n_baseline += 1

            if first.startswith('pol') and len(first) >= 3:
                pol_successor_onsets[second_onset] += 1
                pol_successor_words[second] += 1
                pol_word_successors[first][second_onset] += 1
                pol_section_successors[section][second_onset] += 1
                n_pol_lf_lines += 1

    print(f"\nB lines with pol-prefix at LF (≥2 words): {n_pol_lf_lines}")
    print(f"Baseline B lines ≥2 words: {n_baseline}")

    print("\nSuccessor onset distribution (pol@LF → second word onset):")
    print(f"{'Onset':<8} {'pol_n':>6} {'pol%':>7} {'base%':>7} {'Enrich':>8}")
    all_onsets = set(list(pol_successor_onsets.keys()) + list(baseline_second_onsets.keys()))
    rows = []
    for onset in all_onsets:
        pn = pol_successor_onsets[onset]
        pp = pn / n_pol_lf_lines * 100 if n_pol_lf_lines else 0
        bp = baseline_second_onsets[onset] / n_baseline * 100 if n_baseline else 0
        enr = pp / bp if bp > 0 else float('inf')
        rows.append((onset, pn, pp, bp, enr))
    rows.sort(key=lambda x: -x[4])
    for onset, pn, pp, bp, enr in rows:
        if pn > 0 or bp > 1.0:
            enr_str = f"{enr:.2f}×" if bp > 0 else "∞"
            print(f"{onset:<8} {pn:>6} {pp:>7.2f}% {bp:>7.2f}% {enr_str:>8}")

    print(f"\nTop specific successor words after pol@LF:")
    for word, n in pol_successor_words.most_common(12):
        print(f"  {word}: {n}")

    print(f"\nBy pol-word (n≥2):")
    for polw in sorted(pol_word_successors, key=lambda x: -sum(pol_word_successors[x].values())):
        total = sum(pol_word_successors[polw].values())
        if total < 2:
            continue
        top = pol_word_successors[polw].most_common(4)
        top_str = ', '.join(f"{o}({n})" for o, n in top)
        print(f"  {polw}(n={total}): {top_str}")

    print(f"\nBy section:")
    for sec, cnt in sorted(pol_section_successors.items()):
        total = sum(cnt.values())
        top = cnt.most_common(4)
        top_str = ', '.join(f"{o}({n})" for o, n in top)
        print(f"  {sec}(n={total}): {top_str}")

    # Compare to daiin@LF B successors
    daiin_lf_succ = Counter()
    n_daiin_lf = 0
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        for line in para['lines']:
            if len(line) >= 2 and line[0] == 'daiin':
                daiin_lf_succ[get_onset(line[1])] += 1
                n_daiin_lf += 1

    print(f"\nComparison — B daiin@LF successors (n={n_daiin_lf}) vs pol@LF vs baseline:")
    print(f"{'Onset':<8} {'daiin%':>8} {'pol%':>8} {'base%':>8}")
    for onset in ['sh', 'ch', 'qok', 'd', 's', 'qot', 'qo', 'ok', 'y', 'ol', 'cth']:
        dp = daiin_lf_succ[onset] / n_daiin_lf * 100 if n_daiin_lf else 0
        pp = pol_successor_onsets[onset] / n_pol_lf_lines * 100 if n_pol_lf_lines else 0
        bp = baseline_second_onsets[onset] / n_baseline * 100 if n_baseline else 0
        print(f"{onset:<8} {dp:>8.2f}% {pp:>8.2f}% {bp:>8.2f}%")


# ─────────────────────────────────────────────
# H371: daiin@MID in A — Predecessor and Successor Onset
# ─────────────────────────────────────────────

def h371_daiin_mid_a(paragraphs):
    print("\n" + "=" * 60)
    print("H371: daiin@MID in A — Predecessor and Successor Onset")
    print("=" * 60)

    a_pair_pred_baseline = Counter()  # all predecessor onsets in A bigrams
    a_pair_succ_baseline = Counter()

    daiin_mid_pred = Counter()
    daiin_mid_succ = Counter()
    daiin_ll_pred = Counter()

    n_daiin_mid = 0
    n_daiin_ll = 0
    n_baseline_pairs = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            n = len(line)
            if n < 2:
                continue
            # Baseline: all adjacent pairs
            for j in range(n - 1):
                a_pair_pred_baseline[get_onset(line[j])] += 1
                a_pair_succ_baseline[get_onset(line[j+1])] += 1
                n_baseline_pairs += 1

            # daiin@LL (last word, line len≥2)
            if line[-1] == 'daiin' and n >= 2:
                daiin_ll_pred[get_onset(line[-2])] += 1
                n_daiin_ll += 1

            # daiin@MID (positions 1..n-2, i.e. not first and not last)
            for j in range(1, n - 1):
                if line[j] == 'daiin':
                    daiin_mid_pred[get_onset(line[j-1])] += 1
                    daiin_mid_succ[get_onset(line[j+1])] += 1
                    n_daiin_mid += 1

    print(f"\nA daiin@MID: {n_daiin_mid}, daiin@LL: {n_daiin_ll}")
    print(f"Baseline A adjacent pairs: {n_baseline_pairs}")

    print(f"\ndaiin@MID PREDECESSOR onset vs daiin@LL predecessor vs baseline:")
    print(f"{'Onset':<8} {'mid_n':>6} {'mid%':>7} {'ll_n':>6} {'ll%':>7} {'base%':>7} {'mid_enr':>8} {'ll_enr':>8}")
    all_preds = set(list(daiin_mid_pred.keys()) + list(daiin_ll_pred.keys()))
    rows = []
    for onset in all_preds:
        mn = daiin_mid_pred[onset]
        mp = mn / n_daiin_mid * 100 if n_daiin_mid else 0
        ln = daiin_ll_pred[onset]
        lp = ln / n_daiin_ll * 100 if n_daiin_ll else 0
        bp = a_pair_pred_baseline[onset] / n_baseline_pairs * 100 if n_baseline_pairs else 0
        me = mp / bp if bp > 0 else float('inf')
        le = lp / bp if bp > 0 else float('inf')
        rows.append((onset, mn, mp, ln, lp, bp, me, le))
    rows.sort(key=lambda x: -x[2])
    for onset, mn, mp, ln, lp, bp, me, le in rows:
        me_str = f"{me:.2f}×" if bp > 0 else "∞"
        le_str = f"{le:.2f}×" if bp > 0 else "∞"
        print(f"{onset:<8} {mn:>6} {mp:>7.2f}% {ln:>6} {lp:>7.2f}% {bp:>7.2f}% {me_str:>8} {le_str:>8}")

    print(f"\ndaiin@MID SUCCESSOR onset vs baseline (A):")
    print(f"{'Onset':<8} {'mid_n':>6} {'mid%':>7} {'base%':>7} {'mid_enr':>8}")
    rows2 = []
    for onset in daiin_mid_succ:
        mn = daiin_mid_succ[onset]
        mp = mn / n_daiin_mid * 100 if n_daiin_mid else 0
        bp = a_pair_succ_baseline[onset] / n_baseline_pairs * 100 if n_baseline_pairs else 0
        me = mp / bp if bp > 0 else float('inf')
        rows2.append((onset, mn, mp, bp, me))
    rows2.sort(key=lambda x: -x[2])
    for onset, mn, mp, bp, me in rows2:
        me_str = f"{me:.2f}×" if bp > 0 else "∞"
        print(f"{onset:<8} {mn:>6} {mp:>7.2f}% {bp:>7.2f}% {me_str:>8}")

    # Top specific predecessor words before daiin@MID
    print(f"\nTop specific predecessor words before daiin@MID:")
    pred_word_counts = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(1, len(line) - 1):
                if line[j] == 'daiin':
                    pred_word_counts[line[j-1]] += 1
    for w, n in pred_word_counts.most_common(10):
        print(f"  {w}: {n}")

    print(f"\nTop specific successor words after daiin@MID:")
    succ_word_counts = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(1, len(line) - 1):
                if line[j] == 'daiin':
                    succ_word_counts[line[j+1]] += 1
    for w, n in succ_word_counts.most_common(10):
        print(f"  {w}: {n}")


# ─────────────────────────────────────────────
# H372: Unified Ranking of 6 cth-Introduction Constructions
# ─────────────────────────────────────────────

def h372_cth_ranking(paragraphs):
    print("\n" + "=" * 60)
    print("H372: Unified cth-Introduction Construction Ranking")
    print("=" * 60)

    def analyze_cth_constructions(paras_subset, label):
        construct_counts = {
            'ychor_stem': {'cth': 0, 'total': 0},
            'daiin': {'cth': 0, 'total': 0},
            'ch_onset': {'cth': 0, 'total': 0},
            'k_onset': {'cth': 0, 'total': 0},
            'sh_nonshe': {'cth': 0, 'total': 0},
            'd_onset': {'cth': 0, 'total': 0},
            'all': {'cth': 0, 'total': 0},
        }

        pred_word_cth = Counter()
        pred_word_total = Counter()

        for para in paras_subset:
            for line in para['lines']:
                for j in range(len(line) - 1):
                    pred = line[j]
                    succ = line[j+1]
                    is_cth = get_onset(succ) == 'cth'
                    pred_onset = get_onset(pred)

                    construct_counts['all']['total'] += 1
                    if is_cth:
                        construct_counts['all']['cth'] += 1

                    pred_word_total[pred] += 1
                    if is_cth:
                        pred_word_cth[pred] += 1

                    # Classify predecessor
                    if pred.startswith('ychor'):
                        construct_counts['ychor_stem']['total'] += 1
                        if is_cth:
                            construct_counts['ychor_stem']['cth'] += 1
                    if pred == 'daiin':
                        construct_counts['daiin']['total'] += 1
                        if is_cth:
                            construct_counts['daiin']['cth'] += 1
                    if pred_onset == 'ch':
                        construct_counts['ch_onset']['total'] += 1
                        if is_cth:
                            construct_counts['ch_onset']['cth'] += 1
                    if pred_onset == 'k':
                        construct_counts['k_onset']['total'] += 1
                        if is_cth:
                            construct_counts['k_onset']['cth'] += 1
                    if pred_onset == 'sh' and not (pred.startswith('she') or pred.startswith('shee')):
                        construct_counts['sh_nonshe']['total'] += 1
                        if is_cth:
                            construct_counts['sh_nonshe']['cth'] += 1
                    if pred_onset == 'd':
                        construct_counts['d_onset']['total'] += 1
                        if is_cth:
                            construct_counts['d_onset']['cth'] += 1

        total_bigrams = construct_counts['all']['total']
        total_cth = construct_counts['all']['cth']
        base_rate = total_cth / total_bigrams if total_bigrams else 0

        print(f"\n  {label}: bigrams={total_bigrams}, cth-successor={total_cth} ({base_rate*100:.2f}%)")
        print(f"  {'Construction':<14} {'n_pred':>8} {'cth_n':>6} {'cth%':>8} {'base%':>8} {'Enrich':>8}")

        ranked = []
        for cls in ['ychor_stem', 'daiin', 'ch_onset', 'k_onset', 'sh_nonshe', 'd_onset']:
            d = construct_counts[cls]
            n = d['total']
            cth_n = d['cth']
            rate = cth_n / n if n else 0
            enr = rate / base_rate if base_rate else 0
            ranked.append((cls, n, cth_n, rate, enr))
        ranked.sort(key=lambda x: -x[4])

        for cls, n, cth_n, rate, enr in ranked:
            print(f"  {cls:<14} {n:>8} {cth_n:>6} {rate*100:>8.2f}% {base_rate*100:>8.2f}% {enr:>8.2f}×")

        # Top specific cth-predecessor words (min 5 total occurrences)
        print(f"\n  Top cth-predecessor words (n_total≥5, sorted by enrichment):")
        rows = []
        for w, cth_n in pred_word_cth.most_common(50):
            tot = pred_word_total[w]
            if tot < 5:
                continue
            rate = cth_n / tot
            enr = rate / base_rate if base_rate else 0
            rows.append((w, tot, cth_n, rate, enr))
        rows.sort(key=lambda x: -x[4])
        print(f"  {'Word':<16} {'total':>6} {'cth_n':>6} {'cth%':>8} {'enr':>8}")
        for w, tot, cth_n, rate, enr in rows[:15]:
            print(f"  {w:<16} {tot:>6} {cth_n:>6} {rate*100:>8.2f}% {enr:>8.2f}×")

    a_herbal = [p for p in paragraphs if p['dialect'] == 'A' and p['section'] == 'herbal']
    a_all = [p for p in paragraphs if p['dialect'] == 'A']

    analyze_cth_constructions(a_herbal, "A-herbal only")
    analyze_cth_constructions(a_all, "All A-dialect")


# ─────────────────────────────────────────────
# H373: cosmo B shedy/chedy — WP-LL vs PF-LL
# ─────────────────────────────────────────────

def h373_cosmo_shedy_restriction(paragraphs):
    print("\n" + "=" * 60)
    print("H373: cosmo B shedy/chedy — PF-LL Restriction vs WP-LL Elevation")
    print("=" * 60)

    target_words = {'shedy', 'chedy'}

    pf_ll_words = Counter()
    wp_ll_words = Counter()
    pf_ll_total = 0
    wp_ll_total = 0

    para_details = []
    cosmo_b_count = 0

    for para in paragraphs:
        if para['dialect'] != 'B' or para['section'] != 'cosmo':
            continue
        cosmo_b_count += 1
        lines = para['lines']
        if not lines:
            continue

        # PF-LL = last word of last line (if last line has ≥1 word)
        last_line = lines[-1]
        if last_line:
            pf_word = last_line[-1]
            pf_ll_words[pf_word] += 1
            pf_ll_total += 1
        else:
            pf_word = None

        # WP-LL = last words of non-last lines (line must have ≥2 words to define LL distinctly)
        wp_matches = []
        for i, line in enumerate(lines[:-1]):
            if len(line) >= 2:
                wp_word = line[-1]
                wp_ll_words[wp_word] += 1
                wp_ll_total += 1
                if wp_word in target_words:
                    wp_matches.append((i, wp_word))

        para_details.append({
            'folio': para['folio'],
            'pf': pf_word,
            'wp_matches': wp_matches,
            'n_lines': len(lines),
        })

    print(f"\ncosmo B paragraphs: {cosmo_b_count}")
    print(f"PF-LL total: {pf_ll_total}")
    print(f"WP-LL total: {wp_ll_total}")

    print(f"\n{'Word':<12} {'PF_n':>5} {'PF%':>8} {'WP_n':>5} {'WP%':>8} {'PF/WP enr':>10}")
    for word in ['shedy', 'chedy', 'orol', 'lshedy', 'qokaiin', 'chey', 'shey', 'qokedy', 'sheol']:
        pf_n = pf_ll_words[word]
        wp_n = wp_ll_words[word]
        pf_p = pf_n / pf_ll_total * 100 if pf_ll_total else 0
        wp_p = wp_n / wp_ll_total * 100 if wp_ll_total else 0
        enr_str = f"{pf_p/wp_p:.2f}×" if wp_p > 0 else ("∞" if pf_n > 0 else "—")
        print(f"{word:<12} {pf_n:>5} {pf_p:>8.2f}% {wp_n:>5} {wp_p:>8.2f}% {enr_str:>10}")

    print(f"\nAll cosmo B PF-LL words (n≥2 or in target_words):")
    print(f"  {'Word':<16} {'PF_n':>5} {'PF%':>8} {'WP_n':>5} {'WP%':>8} {'PF/WP enr':>10}")
    for word, n in sorted(pf_ll_words.items(), key=lambda x: -x[1]):
        if n < 2 and word not in target_words:
            continue
        pf_p = n / pf_ll_total * 100 if pf_ll_total else 0
        wp_n = wp_ll_words[word]
        wp_p = wp_n / wp_ll_total * 100 if wp_ll_total else 0
        enr_str = f"{pf_p/wp_p:.2f}×" if wp_p > 0 else ("∞" if n > 0 else "—")
        print(f"  {word:<16} {n:>5} {pf_p:>8.2f}% {wp_n:>5} {wp_p:>8.2f}% {enr_str:>10}")

    print(f"\nParagraph folio details (shedy/chedy at PF or WP-LL):")
    for pd in para_details:
        if pd['pf'] in target_words or pd['wp_matches']:
            print(f"  {pd['folio']} (n_lines={pd['n_lines']}): PF={pd['pf']}, WP-LL_matches={pd['wp_matches']}")

    print(f"\nSummary — cosmo B shedy/chedy position breakdown:")
    for word in ['shedy', 'chedy']:
        pf_n = pf_ll_words[word]
        wp_n = wp_ll_words[word]
        total_ll = pf_n + wp_n
        if total_ll == 0:
            print(f"  {word}: NO occurrences at LL in cosmo B")
        else:
            print(f"  {word}: total LL={total_ll}, PF={pf_n}({pf_n/total_ll*100:.1f}%), WP={wp_n}({wp_n/total_ll*100:.1f}%)")

    # All B context
    b_pf = Counter()
    b_wp = Counter()
    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        if not lines:
            continue
        if lines[-1]:
            b_pf[lines[-1][-1]] += 1
        for line in lines[:-1]:
            if len(line) >= 2:
                b_wp[line[-1]] += 1

    print(f"\nAll-B context — shedy/chedy LL breakdown:")
    for word in ['shedy', 'chedy']:
        pf_n = b_pf[word]
        wp_n = b_wp[word]
        total = pf_n + wp_n
        if total > 0:
            print(f"  All B {word}: total_LL={total}, PF={pf_n}({pf_n/total*100:.1f}%), WP={wp_n}({wp_n/total*100:.1f}%)")
        else:
            print(f"  All B {word}: 0 LL occurrences")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    a_paras = [p for p in paragraphs if p['dialect'] == 'A']
    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    cosmo_b = [p for p in paragraphs if p['dialect'] == 'B' and p['section'] == 'cosmo']
    print(f"Total: {len(paragraphs)} paragraphs (A={len(a_paras)}, B={len(b_paras)})")
    print(f"cosmo B: {len(cosmo_b)}")

    h370_pol_successor(paragraphs)
    h371_daiin_mid_a(paragraphs)
    h372_cth_ranking(paragraphs)
    h373_cosmo_shedy_restriction(paragraphs)
