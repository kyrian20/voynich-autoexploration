"""
exp_203: pol-Prefix PS vs WP-LF (H374), [ch][daiin][cth] Triple (H375),
         daiin@LF in A successor (H376), pch-Prefix PS Successor (H377)

Parser: identical to exp_201/202 (ZL3b paragraph-aware, dot-split words).
"""
import re
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'


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
# H374: pol-Prefix PS vs WP-LF Separation
# ─────────────────────────────────────────────

def h374_pol_ps_separation(paragraphs):
    print("=" * 60)
    print("H374: pol-Prefix PS vs WP-LF Separation")
    print("=" * 60)

    # Position categories: PS = first word of first line; WP-LF = first word of non-first lines
    # MID = non-first within line; LL = last word (len>1)

    pol_positions = Counter()  # ps / wp_lf / mid / ll
    pch_positions = Counter()  # same
    all_positions = Counter()  # baseline

    pol_word_positions = defaultdict(Counter)
    pch_word_positions = defaultdict(Counter)

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        for line_idx, line in enumerate(lines):
            is_ps_line = (line_idx == 0)
            n = len(line)
            for pos, word in enumerate(line):
                # Determine position category
                if pos == 0:
                    if is_ps_line:
                        pos_cat = 'ps'
                    else:
                        pos_cat = 'wp_lf'
                elif pos == n - 1 and n > 1:
                    pos_cat = 'll'
                else:
                    pos_cat = 'mid'

                all_positions[pos_cat] += 1

                is_pol = word.startswith('pol') and len(word) >= 3
                is_pch = (word.startswith('pch') or word.startswith('psh')) and len(word) >= 3

                if is_pol:
                    pol_positions[pos_cat] += 1
                    pol_word_positions[word][pos_cat] += 1
                if is_pch:
                    pch_positions[pos_cat] += 1
                    pch_word_positions[word][pos_cat] += 1

    total_all = sum(all_positions.values())
    total_pol = sum(pol_positions.values())
    total_pch = sum(pch_positions.values())

    print(f"\nB corpus total words: {total_all}")
    print(f"pol-prefix total: {total_pol}")
    print(f"pch-prefix total: {total_pch}")

    print(f"\n{'Position':<10} {'base_n':>7} {'base%':>7} | {'pol_n':>6} {'pol%':>7} {'pol_enr':>8} | {'pch_n':>6} {'pch%':>7} {'pch_enr':>8}")
    for pos in ['ps', 'wp_lf', 'mid', 'll']:
        bn = all_positions[pos]
        bp = bn / total_all * 100 if total_all else 0
        pln = pol_positions[pos]
        plp = pln / total_pol * 100 if total_pol else 0
        ple = plp / bp if bp > 0 else float('inf')
        pcn = pch_positions[pos]
        pcp = pcn / total_pch * 100 if total_pch else 0
        pce = pcp / bp if bp > 0 else float('inf')
        print(f"{pos:<10} {bn:>7} {bp:>7.2f}% | {pln:>6} {plp:>7.2f}% {ple:>8.2f}× | {pcn:>6} {pcp:>7.2f}% {pce:>8.2f}×")

    print(f"\nTop pol-words by position:")
    for w in sorted(pol_word_positions, key=lambda x: -sum(pol_word_positions[x].values())):
        total = sum(pol_word_positions[w].values())
        if total < 2:
            continue
        d = pol_word_positions[w]
        print(f"  {w}(n={total}): ps={d['ps']}, wp_lf={d['wp_lf']}, mid={d['mid']}, ll={d['ll']}")

    print(f"\nTop pch-words by position:")
    for w in sorted(pch_word_positions, key=lambda x: -sum(pch_word_positions[x].values())):
        total = sum(pch_word_positions[w].values())
        if total < 2:
            continue
        d = pch_word_positions[w]
        print(f"  {w}(n={total}): ps={d['ps']}, wp_lf={d['wp_lf']}, mid={d['mid']}, ll={d['ll']}")


# ─────────────────────────────────────────────
# H375: [ch-word][daiin][cth-word] Triple
# ─────────────────────────────────────────────

def h375_ch_daiin_cth_triple(paragraphs):
    print("\n" + "=" * 60)
    print("H375: [ch-word][daiin][cth-word] Triple in A-Dialect")
    print("=" * 60)

    # Collect all A-dialect lines
    triples = []         # (ch_word, cth_word, folio)
    other_daiin_mid = 0  # daiin@MID with non-ch pred or non-cth succ

    # Baseline rates
    total_mid = 0        # all daiin@MID
    ch_pred_mid = 0      # daiin@MID with ch-onset predecessor
    cth_succ_mid = 0     # daiin@MID with cth-onset successor
    ch_cth_triple = 0    # daiin@MID with both ch-pred AND cth-succ

    # Random triple baseline: P(ch-onset predecessor) × P(cth-onset successor) × daiin_rate
    all_a_words = Counter()
    all_a_pairs = Counter()
    total_a_words = 0
    total_a_pairs = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j, w in enumerate(line):
                all_a_words[get_onset(w)] += 1
                total_a_words += 1
            for j in range(len(line) - 1):
                all_a_pairs[(get_onset(line[j]), get_onset(line[j+1]))] += 1
                total_a_pairs += 1

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            n = len(line)
            # Find daiin at MID positions (1..n-2)
            for j in range(1, n - 1):
                if line[j] != 'daiin':
                    continue
                total_mid += 1
                pred = line[j-1]
                succ = line[j+1]
                pred_onset = get_onset(pred)
                succ_onset = get_onset(succ)
                if pred_onset == 'ch':
                    ch_pred_mid += 1
                if succ_onset == 'cth':
                    cth_succ_mid += 1
                if pred_onset == 'ch' and succ_onset == 'cth':
                    ch_cth_triple += 1
                    triples.append((pred, succ, para['folio']))

    print(f"\nA daiin@MID total: {total_mid}")
    print(f"daiin@MID with ch-pred: {ch_pred_mid} ({ch_pred_mid/total_mid*100:.1f}%)")
    print(f"daiin@MID with cth-succ: {cth_succ_mid} ({cth_succ_mid/total_mid*100:.1f}%)")
    print(f"daiin@MID with BOTH ch-pred AND cth-succ: {ch_cth_triple} ({ch_cth_triple/total_mid*100:.1f}%)")

    # Expected if independent: P(ch-pred) × P(cth-succ) × total_mid
    p_ch_pred = ch_pred_mid / total_mid if total_mid else 0
    p_cth_succ = cth_succ_mid / total_mid if total_mid else 0
    expected_if_independent = p_ch_pred * p_cth_succ * total_mid
    enrichment = ch_cth_triple / expected_if_independent if expected_if_independent > 0 else float('inf')
    print(f"\nExpected (if pred/succ independent): {expected_if_independent:.1f}")
    print(f"Enrichment: {enrichment:.2f}×")

    print(f"\nAll [ch-word][daiin][cth-word] triples:")
    triple_counter = Counter((pred, cth) for pred, cth, _ in triples)
    for (pred, cth), n in sorted(triple_counter.items(), key=lambda x: -x[1]):
        print(f"  [{pred}][daiin][{cth}]: {n}")

    # Also count some control triples for context
    print(f"\nControl: [non-ch-pred][daiin][cth-word] triples:")
    non_ch_cth = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            n = len(line)
            for j in range(1, n - 1):
                if line[j] != 'daiin':
                    continue
                pred = line[j-1]
                succ = line[j+1]
                if get_onset(pred) != 'ch' and get_onset(succ) == 'cth':
                    non_ch_cth[(pred, succ)] += 1

    total_non_ch_cth = sum(non_ch_cth.values())
    print(f"  Total non-ch-pred daiin→cth: {total_non_ch_cth}")
    for (pred, cth), n in non_ch_cth.most_common(5):
        print(f"    [{pred}][daiin][{cth}]: {n}")


# ─────────────────────────────────────────────
# H376: daiin@LF in A — Successor Profile
# ─────────────────────────────────────────────

def h376_daiin_lf_a(paragraphs):
    print("\n" + "=" * 60)
    print("H376: daiin@LF Successor Profile in A-Dialect")
    print("=" * 60)

    # daiin@LF = daiin at position 0 in a line (includes PS and WP-LF)
    daiin_lf_a_succ = Counter()
    daiin_lf_a_succ_words = Counter()
    n_daiin_lf_a = 0

    # daiin@LF PS vs WP-LF separation
    daiin_ps_succ = Counter()
    daiin_wplf_succ = Counter()
    n_daiin_ps = 0
    n_daiin_wplf = 0

    # Baseline: all A second-word onsets
    a_second_word_onsets = Counter()
    n_a_second_words = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line_idx, line in enumerate(para['lines']):
            is_ps_line = (line_idx == 0)
            n = len(line)
            if n >= 2:
                second_onset = get_onset(line[1])
                a_second_word_onsets[second_onset] += 1
                n_a_second_words += 1

                if line[0] == 'daiin':
                    daiin_lf_a_succ[second_onset] += 1
                    daiin_lf_a_succ_words[line[1]] += 1
                    n_daiin_lf_a += 1
                    if is_ps_line:
                        daiin_ps_succ[second_onset] += 1
                        n_daiin_ps += 1
                    else:
                        daiin_wplf_succ[second_onset] += 1
                        n_daiin_wplf += 1

    print(f"\nA daiin@LF (all): {n_daiin_lf_a} (PS={n_daiin_ps}, WP-LF={n_daiin_wplf})")
    print(f"Baseline A second-word lines: {n_a_second_words}")

    print(f"\ndaiin@LF(A) successor onset vs baseline vs B daiin@LF vs A daiin@MID:")
    # From exp_201: B daiin@LF successor: sh=35.63%(2.15×), ch=37.93%(2.00×)
    # From exp_202: A daiin@MID successor: cth=13.28%(3.05×)
    b_daiin_lf_succ = {'sh': 35.63, 'ch': 37.93, 'cth': 0.0, 'qok': 3.45, 'd': 2.30, 'qo': 0.0, 'qot': 1.15, 'ok': 2.30}
    a_daiin_mid_succ = {'cth': 13.28, 'd': 19.53, 'ch': 18.75, 'qok': 6.64, 'sh': 5.47}

    print(f"{'Onset':<8} {'A_LF_n':>7} {'A_LF%':>7} {'base%':>7} {'A_LF_enr':>9} | {'B_LF%':>7} {'A_MID%':>7}")
    rows = []
    for onset in set(list(daiin_lf_a_succ.keys()) + list(a_second_word_onsets.keys())):
        ln = daiin_lf_a_succ[onset]
        lp = ln / n_daiin_lf_a * 100 if n_daiin_lf_a else 0
        bp = a_second_word_onsets[onset] / n_a_second_words * 100 if n_a_second_words else 0
        enr = lp / bp if bp > 0 else float('inf')
        b_pct = b_daiin_lf_succ.get(onset, 0.0)
        a_mid_pct = a_daiin_mid_succ.get(onset, 0.0)
        rows.append((onset, ln, lp, bp, enr, b_pct, a_mid_pct))
    rows.sort(key=lambda x: -x[4])
    for onset, ln, lp, bp, enr, b_pct, a_mid_pct in rows:
        if ln > 0 or bp > 1.0:
            enr_str = f"{enr:.2f}×" if bp > 0 else "∞"
            print(f"{onset:<8} {ln:>7} {lp:>7.2f}% {bp:>7.2f}% {enr_str:>9} | {b_pct:>7.2f}% {a_mid_pct:>7.2f}%")

    print(f"\nTop successor words after daiin@LF in A:")
    for w, n in daiin_lf_a_succ_words.most_common(10):
        print(f"  {w}: {n}")

    print(f"\ndaiin@PS in A (n={n_daiin_ps}) successor onsets:")
    if n_daiin_ps > 0:
        for onset, n in sorted(daiin_ps_succ.items(), key=lambda x: -x[1]):
            print(f"  {onset}: {n} ({n/n_daiin_ps*100:.1f}%)")
    else:
        print("  No A daiin@PS occurrences found")

    print(f"\ndaiin@WP-LF in A (n={n_daiin_wplf}) top onsets:")
    if n_daiin_wplf > 0:
        for onset, n in sorted(daiin_wplf_succ.items(), key=lambda x: -x[1])[:6]:
            bp = a_second_word_onsets[onset] / n_a_second_words * 100 if n_a_second_words else 0
            enr = (n/n_daiin_wplf*100) / bp if bp > 0 else float('inf')
            print(f"  {onset}: {n} ({n/n_daiin_wplf*100:.1f}%, enr={enr:.2f}×)")


# ─────────────────────────────────────────────
# H377: pch-Prefix Successor Profile at PS
# ─────────────────────────────────────────────

def h377_pch_successor(paragraphs):
    print("\n" + "=" * 60)
    print("H377: pch-Prefix Successor Profile at PS")
    print("=" * 60)

    # pch-prefix at PS = first word of first line of paragraph
    pch_ps_succ = Counter()
    pch_ps_succ_words = Counter()
    n_pch_ps = 0

    pol_wplf_succ = Counter()  # for comparison (from H370, re-computing here)
    n_pol_wplf = 0

    # Baseline: all PS second words (in B)
    b_ps_second = Counter()
    n_b_ps_second = 0

    # Baseline: all WP-LF second words (in B)
    b_wplf_second = Counter()
    n_b_wplf_second = 0

    for para in paragraphs:
        if para['dialect'] != 'B':
            continue
        lines = para['lines']
        for line_idx, line in enumerate(lines):
            is_ps_line = (line_idx == 0)
            n = len(line)
            if n < 2:
                continue

            first = line[0]
            second = line[1]
            second_onset = get_onset(second)

            if is_ps_line:
                b_ps_second[second_onset] += 1
                n_b_ps_second += 1
                is_pch = (first.startswith('pch') or first.startswith('psh')) and len(first) >= 3
                if is_pch:
                    pch_ps_succ[second_onset] += 1
                    pch_ps_succ_words[second] += 1
                    n_pch_ps += 1
            else:
                b_wplf_second[second_onset] += 1
                n_b_wplf_second += 1
                is_pol = first.startswith('pol') and len(first) >= 3
                if is_pol:
                    pol_wplf_succ[second_onset] += 1
                    n_pol_wplf += 1

    print(f"\nB pch-prefix at PS: {n_pch_ps}")
    print(f"B pol-prefix at WP-LF: {n_pol_wplf}")
    print(f"Baseline: B PS second words={n_b_ps_second}, B WP-LF second words={n_b_wplf_second}")

    print(f"\npch@PS vs pol@WP-LF successor profile comparison:")
    print(f"{'Onset':<8} {'pch_n':>6} {'pch%':>7} {'ps_base%':>9} {'pch_enr':>8} | {'pol_n':>6} {'pol%':>7} {'wplf_base%':>11} {'pol_enr':>8}")
    all_onsets = set(list(pch_ps_succ.keys()) + list(pol_wplf_succ.keys()) +
                     list(b_ps_second.keys()) + list(b_wplf_second.keys()))
    rows = []
    for onset in all_onsets:
        pn = pch_ps_succ[onset]
        pp = pn / n_pch_ps * 100 if n_pch_ps else 0
        ps_bp = b_ps_second[onset] / n_b_ps_second * 100 if n_b_ps_second else 0
        p_enr = pp / ps_bp if ps_bp > 0 else float('inf')
        pln = pol_wplf_succ[onset]
        plp = pln / n_pol_wplf * 100 if n_pol_wplf else 0
        wplf_bp = b_wplf_second[onset] / n_b_wplf_second * 100 if n_b_wplf_second else 0
        pl_enr = plp / wplf_bp if wplf_bp > 0 else float('inf')
        rows.append((onset, pn, pp, ps_bp, p_enr, pln, plp, wplf_bp, pl_enr))
    rows.sort(key=lambda x: -x[2])
    for onset, pn, pp, ps_bp, p_enr, pln, plp, wplf_bp, pl_enr in rows:
        if pn > 0 or pln > 0 or ps_bp > 1.0:
            pe_str = f"{p_enr:.2f}×" if ps_bp > 0 else "∞"
            ple_str = f"{pl_enr:.2f}×" if wplf_bp > 0 else "∞"
            print(f"{onset:<8} {pn:>6} {pp:>7.2f}% {ps_bp:>9.2f}% {pe_str:>8} | {pln:>6} {plp:>7.2f}% {wplf_bp:>11.2f}% {ple_str:>8}")

    print(f"\nTop pch@PS successor words:")
    for w, n in pch_ps_succ_words.most_common(10):
        print(f"  {w}: {n}")

    print(f"\nTop pol@WP-LF successor words:")
    for onset, n in sorted(pol_wplf_succ.items(), key=lambda x: -x[1])[:8]:
        print(f"  {onset}: {n}")

    # Also: A dialect pch successor at PS
    pch_a_ps_succ = Counter()
    n_pch_a_ps = 0
    a_ps_second = Counter()
    n_a_ps_second = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        lines = para['lines']
        if not lines or len(lines[0]) < 2:
            continue
        first = lines[0][0]
        second = lines[0][1]
        second_onset = get_onset(second)
        a_ps_second[second_onset] += 1
        n_a_ps_second += 1
        is_pch = (first.startswith('pch') or first.startswith('psh')) and len(first) >= 3
        if is_pch:
            pch_a_ps_succ[second_onset] += 1
            n_pch_a_ps += 1

    print(f"\nA pch@PS (n={n_pch_a_ps}) successor onsets vs A PS baseline (n={n_a_ps_second}):")
    for onset in sorted(pch_a_ps_succ, key=lambda x: -pch_a_ps_succ[x]):
        pn = pch_a_ps_succ[onset]
        pp = pn / n_pch_a_ps * 100 if n_pch_a_ps else 0
        bp = a_ps_second[onset] / n_a_ps_second * 100 if n_a_ps_second else 0
        enr = pp / bp if bp > 0 else float('inf')
        print(f"  {onset}: pch_n={pn}({pp:.1f}%), base={bp:.1f}%, enr={enr:.2f}×")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    a_paras = [p for p in paragraphs if p['dialect'] == 'A']
    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    print(f"Total: {len(paragraphs)} paragraphs (A={len(a_paras)}, B={len(b_paras)})")

    h374_pol_ps_separation(paragraphs)
    h375_ch_daiin_cth_triple(paragraphs)
    h376_daiin_lf_a(paragraphs)
    h377_pch_successor(paragraphs)
