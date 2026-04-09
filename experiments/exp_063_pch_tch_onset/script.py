"""
exp_063: B Para-Start pch/tch Onset Class Analysis (H073)
Tests whether 'pch' and 'tch' onset words in Currier B are a distinct structural vocabulary
(concentrated at para-starts, distinctive suffix distribution, absent from labels).
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
SUFFIX_LIST = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y', 'ol', 'or', 'al', 'ar', 'iin', 'in']

LABEL_LOCI = ('Lf', 'Ls', 'Lz', 'Lc', 'Ln', 'Lt')

def suffix_group(word):
    for suf in SUFFIX_LIST:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def is_label_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return any(base.startswith(lc) for lc in LABEL_LOCI)

def parse_corpus(path):
    records = []
    current_currier = None
    current_section = None
    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line or line.startswith('#'):
                continue
            m_c = re.search(r'\$L=([AB])', line)
            if m_c:
                current_currier = m_c.group(1)
            m_s = re.search(r'\$I=([A-Z]+)', line)
            if m_s:
                current_section = m_s.group(1)
            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_raw = parts[0].strip()
            locus_code = parts[1].strip()
            folio_id = folio_raw.split('.')[0] if '.' in folio_raw else folio_raw
            is_body = is_body_locus(locus_code)
            is_label = is_label_locus(locus_code)
            if not is_body and not is_label:
                continue
            line_type = 'para_start' if locus_code.startswith('@') else ('continuation' if locus_code.startswith('+') else 'other')
            text = line[m.end():].strip()
            text = clean_text(text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            if not tokens:
                continue
            records.append({
                'folio': folio_id,
                'currier': current_currier,
                'section': current_section,
                'line_type': line_type,
                'locus_type': 'body' if is_body else 'label',
                'words': tokens,
            })
    return records

def main():
    records = parse_corpus(DATA_PATH)

    # Separate B body text
    b_body = [r for r in records if r['currier'] == 'B' and r['locus_type'] == 'body']
    b_para_starts = [r for r in b_body if r['line_type'] == 'para_start']
    b_cont = [r for r in b_body if r['line_type'] == 'continuation']
    b_all_lines = b_body

    all_b_words = [w for r in b_all_lines for w in r['words']]
    n_b = len(all_b_words)

    # Label words (all dialects)
    label_words = [w for r in records if r['locus_type'] == 'label' for w in r['words']]
    n_label = len(label_words)

    # Classify onset types
    def onset_type(word):
        if word.startswith('pch'):
            return 'pch'
        if word.startswith('tch'):
            return 'tch'
        if word.startswith('p') and not word.startswith('pch'):
            return 'p_other'
        if word.startswith('t') and not word.startswith('tch'):
            return 't_other'
        return 'other'

    # Word-level analysis: pch vs tch vs p_other vs t_other
    onset_all = Counter(onset_type(w) for w in all_b_words)
    onset_ps = Counter(onset_type(r['words'][0]) for r in b_para_starts)
    onset_cont = Counter(onset_type(r['words'][0]) for r in b_cont)

    n_ps = len(b_para_starts)
    n_cont = len(b_cont)

    print("="*70)
    print("H073: pch/tch ONSET CLASS ANALYSIS — Currier B")
    print("="*70)

    print(f"\nCorpus sizes: B body={n_b} tokens, B para-starts={n_ps} lines, B cont={n_cont} lines")

    print(f"\n--- ONSET TYPE FREQUENCIES (all B body words) ---")
    for ot in ['pch', 'tch', 'p_other', 't_other']:
        print(f"  {ot}: {onset_all.get(ot, 0)} ({100*onset_all.get(ot,0)/n_b:.2f}%)")

    # Para-start first-word analysis
    print(f"\n--- PARA-START FIRST WORD ONSET DISTRIBUTION ---")
    print(f"{'Onset':<12} {'PS_first':>9} {'PS%':>6} {'All_words%':>11} {'Ratio':>7}")
    for ot in ['pch', 'tch', 'p_other', 't_other']:
        ps_cnt = onset_ps.get(ot, 0)
        all_cnt = onset_all.get(ot, 0)
        ps_p = ps_cnt / max(n_ps, 1)
        all_p = all_cnt / max(n_b, 1)
        ratio = ps_p / max(all_p, 1e-10)
        print(f"{ot:<12} {ps_cnt:>9} {100*ps_p:>5.1f}% {100*all_p:>10.2f}% {ratio:>7.2f}×")

    # Most common pch and tch words
    pch_words = Counter(w for w in all_b_words if w.startswith('pch'))
    tch_words = Counter(w for w in all_b_words if w.startswith('tch'))

    print(f"\n--- TOP pch-INITIAL WORDS IN CURRIER B (ALL positions) ---")
    for w, c in pch_words.most_common(15):
        suf = suffix_group(w) or '(none)'
        print(f"  {w:<20} {c:>5} ({100*c/n_b:.3f}%): suffix={suf}")

    print(f"\n--- TOP tch-INITIAL WORDS IN CURRIER B (ALL positions) ---")
    for w, c in tch_words.most_common(15):
        suf = suffix_group(w) or '(none)'
        print(f"  {w:<20} {c:>5} ({100*c/n_b:.3f}%): suffix={suf}")

    # pch/tch positional profile
    print(f"\n--- pch/tch WORD POSITIONAL PROFILE ---")
    pch_total_words = sum(pch_words.values())
    tch_total_words = sum(tch_words.values())
    pch_ps_first = sum(onset_ps.get('pch', 0) for _ in [1])
    tch_ps_first = onset_ps.get('tch', 0)
    pch_cont_first = onset_cont.get('pch', 0)
    tch_cont_first = onset_cont.get('tch', 0)

    # All positions analysis
    pch_first_all = sum(1 for r in b_all_lines if r['words'][0].startswith('pch'))
    tch_first_all = sum(1 for r in b_all_lines if r['words'][0].startswith('tch'))
    pch_last_all = sum(1 for r in b_all_lines if r['words'][-1].startswith('pch'))
    tch_last_all = sum(1 for r in b_all_lines if r['words'][-1].startswith('tch'))
    n_lines_b = len(b_all_lines)

    print(f"pch words: {pch_total_words} total, {pch_first_all} line-first ({100*pch_first_all/n_lines_b:.1f}%)")
    print(f"  para-start first: {pch_ps_first}/{n_ps} = {100*pch_ps_first/max(n_ps,1):.1f}%")
    print(f"  continuation first: {pch_cont_first}/{n_cont} = {100*pch_cont_first/max(n_cont,1):.1f}%")
    print(f"  line-last: {pch_last_all}/{n_lines_b} = {100*pch_last_all/n_lines_b:.1f}%")

    print(f"tch words: {tch_total_words} total, {tch_first_all} line-first ({100*tch_first_all/n_lines_b:.1f}%)")
    print(f"  para-start first: {tch_ps_first}/{n_ps} = {100*tch_ps_first/max(n_ps,1):.1f}%")
    print(f"  continuation first: {tch_cont_first}/{n_cont} = {100*tch_cont_first/max(n_cont,1):.1f}%")
    print(f"  line-last: {tch_last_all}/{n_lines_b} = {100*tch_last_all/n_lines_b:.1f}%")

    # Suffix distribution of pch and tch words vs p_other and t_other
    print(f"\n--- SUFFIX DISTRIBUTION COMPARISON ---")
    def suffix_dist(words_list):
        return Counter(suffix_group(w) or '(none)' for w in words_list)

    pch_suf = suffix_dist(w for w in all_b_words if w.startswith('pch'))
    tch_suf = suffix_dist(w for w in all_b_words if w.startswith('tch'))
    p_other_suf = suffix_dist(w for w in all_b_words if w.startswith('p') and not w.startswith('pch'))
    t_other_suf = suffix_dist(w for w in all_b_words if w.startswith('t') and not w.startswith('tch'))

    n_pch = sum(pch_suf.values())
    n_tch = sum(tch_suf.values())
    n_po = sum(p_other_suf.values())
    n_to = sum(t_other_suf.values())

    print(f"{'Suffix':<8} {'pch%':>7} {'tch%':>7} {'p_other%':>9} {'t_other%':>9}")
    for suf in SUFFIX_LIST[:12] + ['(none)']:
        pp = pch_suf.get(suf, 0) / max(n_pch, 1)
        tp = tch_suf.get(suf, 0) / max(n_tch, 1)
        pop = p_other_suf.get(suf, 0) / max(n_po, 1)
        top = t_other_suf.get(suf, 0) / max(n_to, 1)
        if pp > 0.01 or tp > 0.01 or pop > 0.01 or top > 0.01:
            print(f"{suf:<8} {100*pp:>6.1f}% {100*tp:>6.1f}% {100*pop:>8.1f}% {100*top:>8.1f}%")

    # Label presence check
    pch_in_labels = sum(1 for w in label_words if w.startswith('pch'))
    tch_in_labels = sum(1 for w in label_words if w.startswith('tch'))
    print(f"\n--- LABEL PRESENCE ---")
    print(f"pch words in labels: {pch_in_labels}/{n_label}")
    print(f"tch words in labels: {tch_in_labels}/{n_label}")

    # Cross-section analysis: where do pch/tch words appear?
    print(f"\n--- SECTION DISTRIBUTION of pch/tch words in Currier B ---")
    section_counter = defaultdict(lambda: {'pch': 0, 'tch': 0, 'total': 0})
    for r in b_body:
        for w in r['words']:
            sec = r['section'] or '?'
            section_counter[sec]['total'] += 1
            if w.startswith('pch'):
                section_counter[sec]['pch'] += 1
            elif w.startswith('tch'):
                section_counter[sec]['tch'] += 1
    for sec in sorted(section_counter.keys()):
        d = section_counter[sec]
        print(f"  {sec}: total={d['total']}, pch={d['pch']} ({100*d['pch']/max(d['total'],1):.2f}%), tch={d['tch']} ({100*d['tch']/max(d['total'],1):.2f}%)")

if __name__ == '__main__':
    main()
