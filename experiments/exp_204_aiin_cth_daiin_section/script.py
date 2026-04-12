"""
exp_204: -aiin Class as cth-Introducer (H378), cth-Successor Profile (H379),
         daiin→cth by A-Section (H380), A-Dialect pol-Prefix Words (H381)

Parser: identical to exp_201-203 (ZL3b paragraph-aware, dot-split words).
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
# H378: -aiin Suffix Words as cth-Introduction Class
# ─────────────────────────────────────────────

def h378_aiin_cth(paragraphs):
    print("=" * 60)
    print("H378: -aiin Suffix Words as cth-Introduction Class in A")
    print("=" * 60)

    # Collect all A bigrams
    aiin_cth = Counter()     # aiin-word → cth_count
    aiin_total = Counter()   # aiin-word → total_successor_count
    all_cth = 0
    all_pairs = 0

    aiin_word_freq = Counter()  # total frequency of each aiin-word

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                pred = line[j]
                succ = line[j+1]
                all_pairs += 1
                is_cth = get_onset(succ) == 'cth'
                if is_cth:
                    all_cth += 1
                aiin_word_freq[pred] += 1
                if pred.endswith('aiin'):
                    aiin_total[pred] += 1
                    if is_cth:
                        aiin_cth[pred] += 1

    base_rate = all_cth / all_pairs if all_pairs else 0
    total_aiin_pairs = sum(aiin_total.values())
    total_aiin_cth = sum(aiin_cth.values())

    print(f"\nAll A bigrams: {all_pairs}, cth-successor: {all_cth} ({base_rate*100:.2f}%)")
    print(f"All A -aiin word predecessor bigrams: {total_aiin_pairs}")
    print(f"All A -aiin word → cth successor: {total_aiin_cth} ({total_aiin_cth/total_aiin_pairs*100:.2f}%)")
    print(f"-aiin class enrichment vs baseline: {(total_aiin_cth/total_aiin_pairs)/base_rate:.2f}×")

    print(f"\nIndividual -aiin words (n_total≥5, sorted by cth rate):")
    print(f"{'Word':<16} {'total':>6} {'cth_n':>6} {'cth%':>8} {'base%':>8} {'enr':>8}")
    rows = []
    for w in sorted(aiin_total, key=lambda x: -aiin_total[x]):
        tot = aiin_total[w]
        cth_n = aiin_cth.get(w, 0)
        if tot < 3:
            continue
        rate = cth_n / tot
        enr = rate / base_rate if base_rate else 0
        rows.append((w, tot, cth_n, rate, enr))
    rows.sort(key=lambda x: -x[4])
    for w, tot, cth_n, rate, enr in rows[:15]:
        print(f"{w:<16} {tot:>6} {cth_n:>6} {rate*100:>8.2f}% {base_rate*100:>8.2f}% {enr:>8.2f}×")

    # Also show which -aiin words have ZERO cth successors
    print(f"\n-aiin words with zero cth successors (n_total≥3):")
    for w in sorted(aiin_total, key=lambda x: -aiin_total[x]):
        tot = aiin_total[w]
        if tot < 3:
            continue
        cth_n = aiin_cth.get(w, 0)
        if cth_n == 0:
            print(f"  {w}(n={tot}): cth=0")

    # Compare: non-aiin d-onset words vs daiin for cth rate
    print(f"\nD-onset breakdown for context:")
    d_total = Counter()
    d_cth = Counter()
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                pred = line[j]
                succ = line[j+1]
                if get_onset(pred) == 'd':
                    d_total[pred] += 1
                    if get_onset(succ) == 'cth':
                        d_cth[pred] += 1
    print(f"  daiin: total={d_total['daiin']}, cth={d_cth['daiin']}, rate={d_cth['daiin']/d_total['daiin']*100:.2f}% ({d_cth['daiin']/d_total['daiin']/base_rate:.2f}×)")
    for w in ['dain', 'dal', 'dar', 'dam', 'daiin']:
        if w == 'daiin':
            continue
        tot = d_total[w]
        cth = d_cth.get(w, 0)
        if tot < 3:
            continue
        print(f"  {w}: total={tot}, cth={cth}, rate={cth/tot*100:.2f}% ({cth/tot/base_rate:.2f}×)")


# ─────────────────────────────────────────────
# H379: cth-Word Successor Profile in A
# ─────────────────────────────────────────────

def h379_cth_successor(paragraphs):
    print("\n" + "=" * 60)
    print("H379: cth-Word Successor Profile in A-Dialect")
    print("=" * 60)

    cth_succ_onsets = Counter()
    cth_succ_words = Counter()
    cth_word_succ = defaultdict(Counter)  # per cth-word

    baseline_succ_onsets = Counter()
    n_baseline = 0
    n_cth_pairs = 0

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for j in range(len(line) - 1):
                pred = line[j]
                succ = line[j+1]
                baseline_succ_onsets[get_onset(succ)] += 1
                n_baseline += 1
                if get_onset(pred) == 'cth':
                    cth_succ_onsets[get_onset(succ)] += 1
                    cth_succ_words[succ] += 1
                    cth_word_succ[pred][get_onset(succ)] += 1
                    n_cth_pairs += 1

    print(f"\nA cth-onset predecessor bigrams: {n_cth_pairs}; baseline: {n_baseline}")
    print(f"\ncth-word successor onset distribution:")
    print(f"{'Onset':<8} {'cth_n':>6} {'cth%':>8} {'base%':>8} {'Enrich':>8}")
    rows = []
    for onset in set(list(cth_succ_onsets.keys()) + list(baseline_succ_onsets.keys())):
        cn = cth_succ_onsets[onset]
        cp = cn / n_cth_pairs * 100 if n_cth_pairs else 0
        bp = baseline_succ_onsets[onset] / n_baseline * 100 if n_baseline else 0
        enr = cp / bp if bp > 0 else float('inf')
        rows.append((onset, cn, cp, bp, enr))
    rows.sort(key=lambda x: -x[4])
    for onset, cn, cp, bp, enr in rows:
        if cn > 0 or bp > 1.0:
            enr_str = f"{enr:.2f}×" if bp > 0 else "∞"
            print(f"{onset:<8} {cn:>6} {cp:>8.2f}% {bp:>8.2f}% {enr_str:>8}")

    print(f"\nTop specific successor words after cth-onset:")
    for w, n in cth_succ_words.most_common(15):
        print(f"  {w}: {n}")

    # Key: is cth→daiin enriched?
    daiin_after_cth = cth_succ_words['daiin']
    daiin_base = baseline_succ_onsets.get('d', 0) / n_baseline
    daiin_after_cth_rate = daiin_after_cth / n_cth_pairs if n_cth_pairs else 0
    print(f"\ncth→daiin specifically:")
    print(f"  cth→daiin: {daiin_after_cth}/{n_cth_pairs} = {daiin_after_cth_rate*100:.2f}%")

    # Count daiin frequency in A for proper baseline
    daiin_count = 0
    total_a_words = 0
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        for line in para['lines']:
            for w in line:
                total_a_words += 1
                if w == 'daiin':
                    daiin_count += 1
    daiin_rate = daiin_count / total_a_words if total_a_words else 0
    print(f"  daiin corpus rate in A: {daiin_count}/{total_a_words} = {daiin_rate*100:.2f}%")
    enr = (daiin_after_cth_rate) / daiin_rate if daiin_rate else float('inf')
    print(f"  cth→daiin enrichment vs daiin base rate: {enr:.2f}×")

    # Per top cth-words
    print(f"\nTop cth-words successor profiles:")
    for cw in ['cthy', 'cthol', 'cthor', 'cthey', 'cthaiin', 'cthdy']:
        n_total = sum(cth_word_succ[cw].values())
        if n_total < 5:
            continue
        top3 = cth_word_succ[cw].most_common(4)
        top_str = ', '.join(f"{o}({n})" for o, n in top3)
        print(f"  {cw}(n={n_total}): {top_str}")


# ─────────────────────────────────────────────
# H380: daiin→cth by A-Section
# ─────────────────────────────────────────────

def h380_daiin_cth_section(paragraphs):
    print("\n" + "=" * 60)
    print("H380: daiin→cth Enrichment by A-Dialect Section")
    print("=" * 60)

    # Per section stats
    section_data = defaultdict(lambda: {'daiin_cth': 0, 'daiin_total': 0, 'all_cth': 0, 'all_pairs': 0})

    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        section = para['section']
        for line in para['lines']:
            for j in range(len(line) - 1):
                pred = line[j]
                succ = line[j+1]
                is_cth = get_onset(succ) == 'cth'
                section_data[section]['all_pairs'] += 1
                if is_cth:
                    section_data[section]['all_cth'] += 1
                if pred == 'daiin':
                    section_data[section]['daiin_total'] += 1
                    if is_cth:
                        section_data[section]['daiin_cth'] += 1

    print(f"\n{'Section':<10} {'all_pairs':>10} {'base_cth%':>10} {'daiin_n':>8} {'daiin_cth':>10} {'daiin_cth%':>12} {'enr':>8}")
    sections = ['herbal', 'pharma', 'astro', 'other']
    for section in sections:
        d = section_data[section]
        ap = d['all_pairs']
        ac = d['all_cth']
        base = ac / ap * 100 if ap else 0
        dn = d['daiin_total']
        dc = d['daiin_cth']
        dcpct = dc / dn * 100 if dn else 0
        enr = dcpct / base if base else float('inf')
        print(f"{section:<10} {ap:>10} {base:>10.2f}% {dn:>8} {dc:>10} {dcpct:>12.2f}% {enr:>8.2f}×")

    # Total A for reference
    d = {'daiin_cth': sum(v['daiin_cth'] for v in section_data.values()),
         'daiin_total': sum(v['daiin_total'] for v in section_data.values()),
         'all_cth': sum(v['all_cth'] for v in section_data.values()),
         'all_pairs': sum(v['all_pairs'] for v in section_data.values())}
    ap = d['all_pairs']
    base = d['all_cth'] / ap * 100 if ap else 0
    dn = d['daiin_total']
    dc = d['daiin_cth']
    dcpct = dc / dn * 100 if dn else 0
    enr = dcpct / base if base else float('inf')
    print(f"{'ALL-A':<10} {ap:>10} {base:>10.2f}% {dn:>8} {dc:>10} {dcpct:>12.2f}% {enr:>8.2f}×")

    # Also: daiin frequency by section for context
    print(f"\ndaiin frequency by A-section:")
    daiin_freq = defaultdict(lambda: {'daiin': 0, 'total': 0})
    for para in paragraphs:
        if para['dialect'] != 'A':
            continue
        section = para['section']
        for line in para['lines']:
            for w in line:
                daiin_freq[section]['total'] += 1
                if w == 'daiin':
                    daiin_freq[section]['daiin'] += 1
    for section in sections:
        d = daiin_freq[section]
        pct = d['daiin'] / d['total'] * 100 if d['total'] else 0
        print(f"  {section}: {d['daiin']}/{d['total']} = {pct:.2f}% daiin")


# ─────────────────────────────────────────────
# H381: A-Dialect pol-Prefix Words
# ─────────────────────────────────────────────

def h381_a_pol_prefix(paragraphs):
    print("\n" + "=" * 60)
    print("H381: A-Dialect pol-Prefix Words")
    print("=" * 60)

    a_pol_words = Counter()
    a_pol_positions = defaultdict(Counter)  # word → {ps, wp_lf, mid, ll}
    a_pol_sections = defaultdict(Counter)
    b_pol_words = Counter()

    for para in paragraphs:
        dialect = para['dialect']
        section = para['section']
        lines = para['lines']
        for line_idx, line in enumerate(lines):
            is_ps_line = (line_idx == 0)
            n = len(line)
            for pos, word in enumerate(line):
                if not (word.startswith('pol') and len(word) >= 3):
                    continue
                if pos == 0:
                    pos_cat = 'ps' if is_ps_line else 'wp_lf'
                elif pos == n - 1 and n > 1:
                    pos_cat = 'll'
                else:
                    pos_cat = 'mid'

                if dialect == 'A':
                    a_pol_words[word] += 1
                    a_pol_positions[word][pos_cat] += 1
                    a_pol_sections[word][section] += 1
                elif dialect == 'B':
                    b_pol_words[word] += 1

    total_a_pol = sum(a_pol_words.values())
    total_b_pol = sum(b_pol_words.values())

    print(f"\nA pol-prefix total: {total_a_pol}")
    print(f"B pol-prefix total: {total_b_pol}")

    print(f"\nA pol-prefix words (all):")
    for w, n in sorted(a_pol_words.items(), key=lambda x: -x[1]):
        pos = a_pol_positions[w]
        sections = ', '.join(f"{s}({c})" for s, c in sorted(a_pol_sections[w].items()))
        print(f"  {w}(n={n}): ps={pos['ps']}, wp_lf={pos['wp_lf']}, mid={pos['mid']}, ll={pos['ll']} | sections: {sections}")

    # Aggregate positional distribution for A pol-words
    a_pos_total = defaultdict(int)
    for w, pos_cnt in a_pol_positions.items():
        for pc, cnt in pos_cnt.items():
            a_pos_total[pc] += cnt

    print(f"\nA pol-prefix aggregate position (n={total_a_pol}):")
    for pc in ['ps', 'wp_lf', 'mid', 'll']:
        n = a_pos_total[pc]
        pct = n / total_a_pol * 100 if total_a_pol else 0
        print(f"  {pc}: {n} ({pct:.1f}%)")

    print(f"\nComparison B pol-prefix aggregate (n={total_b_pol}):")
    # From H374: ps=5(7.1%), wp_lf=56(80.0%), mid=9(12.9%), ll=0(0.0%)
    print(f"  B: ps=5(7.1%), wp_lf=56(80.0%), mid=9(12.9%), ll=0(0.0%)")

    # Show B's most common pol-words for comparison
    print(f"\nTop B pol-prefix words:")
    for w, n in sorted(b_pol_words.items(), key=lambda x: -x[1])[:8]:
        print(f"  {w}: {n}")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("Parsing corpus...")
    paragraphs, folio_dialect = parse_corpus()
    a_paras = [p for p in paragraphs if p['dialect'] == 'A']
    b_paras = [p for p in paragraphs if p['dialect'] == 'B']
    print(f"Total: {len(paragraphs)} paragraphs (A={len(a_paras)}, B={len(b_paras)})")

    h378_aiin_cth(paragraphs)
    h379_cth_successor(paragraphs)
    h380_daiin_cth_section(paragraphs)
    h381_a_pol_prefix(paragraphs)
