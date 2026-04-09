"""
exp_073: Medial Trigram Structure (H095) + d→qo Suppression (H094) + daiin Sequential Role (H096)
H094: Is d→ch coupling the complement of sh→qo? Does d occupy a complementary sequential slot?
H095: Do three-word medial sequences (qo+ch/sh+word) appear as specific repeated trigrams?
H096: Is daiin specifically enriched as a ch-predecessor (controlling for d-class frequency)?
"""

import re
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

def clean_text(text):
    return re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)

def is_body_locus(locus_code):
    base = locus_code.lstrip('+*@=/~&')
    return base.startswith('P')

def onset_class(word):
    if word.startswith('qo') and len(word) > 2:
        return 'qo'
    if word.startswith('ch') and len(word) > 2:
        return 'ch'
    if word.startswith('sh') and len(word) > 2:
        return 'sh'
    if word.startswith('p') and len(word) > 1:
        return 'p'
    if word.startswith('t') and len(word) > 1:
        return 't'
    if word.startswith('k') and len(word) > 1:
        return 'k'
    if word.startswith('d') and len(word) > 1:
        return 'd'
    if word.startswith('s') and not word.startswith('sh') and len(word) > 1:
        return 's'
    if word.startswith('y') and len(word) > 1:
        return 'y'
    if word.startswith('o') and len(word) > 1:
        return 'o'
    return 'other'

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
            if not is_body_locus(locus_code):
                continue
            base_locus = locus_code.lstrip('+*=/~&')
            is_para_start = base_locus.startswith('@')
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
                'is_para_start': is_para_start,
                'words': tokens
            })
    return records

def main():
    records = parse_corpus(DATA_PATH)
    b_records = [r for r in records if r['currier'] == 'B']
    a_records = [r for r in records if r['currier'] == 'A']

    b_words = [w for r in b_records for w in r['words']]
    a_words = [w for r in a_records for w in r['words']]

    # H094: d→qo suppression and d sequential role
    print("="*70)
    print("H094: d→qo SUPPRESSION AND COMPLEMENTARY SLOT ANALYSIS")
    print("="*70)

    base_ch_b = sum(1 for w in b_words if onset_class(w) == 'ch') / max(len(b_words), 1)
    base_qo_b = sum(1 for w in b_words if onset_class(w) == 'qo') / max(len(b_words), 1)

    # For each onset class, compute what follows
    # Already computed in exp_072 for overall B; let's also compute P(ch|X) for B
    print(f"\n--- P(ch NEXT) AND P(qo NEXT) AFTER EACH ONSET CLASS IN CURRIER B ---")
    onset_bigrams_b = defaultdict(Counter)
    onset_totals_b = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            onset_bigrams_b[oc1][oc2] += 1
            onset_totals_b[oc1] += 1

    key_classes = ['p', 't', 'k', 'ch', 'sh', 'qo', 'd', 's', 'y', 'o']
    print(f"\n{'From':>8} {'n':>6} {'P(ch|X)':>9} {'enr_ch':>8} {'P(qo|X)':>9} {'enr_qo':>8} {'P(d|X)':>8} {'enr_d':>7}")
    for oc1 in key_classes:
        n = onset_totals_b[oc1]
        if n < 50:
            continue
        p_ch = onset_bigrams_b[oc1].get('ch', 0) / max(n, 1)
        p_qo = onset_bigrams_b[oc1].get('qo', 0) / max(n, 1)
        p_d = onset_bigrams_b[oc1].get('d', 0) / max(n, 1)
        base_d = sum(1 for w in b_words if onset_class(w) == 'd') / max(len(b_words), 1)
        print(f"{oc1+'→':>8} {n:>6} {100*p_ch:>8.1f}% {p_ch/max(base_ch_b,1e-10):>7.2f}× {100*p_qo:>8.1f}% {p_qo/max(base_qo_b,1e-10):>7.2f}× {100*p_d:>7.1f}% {p_d/max(base_d,1e-10):>7.2f}×")

    # What follows d? And what precedes d?
    before_d = Counter()
    after_d = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            if oc1 == 'd':
                after_d[oc2] += 1
            if oc2 == 'd':
                before_d[oc1] += 1

    print(f"\n  What follows d in B: {', '.join(f'{c}({v})' for c,v in after_d.most_common(8))}")
    print(f"  What precedes d in B: {', '.join(f'{c}({v})' for c,v in before_d.most_common(8))}")

    # Is there a "d→ch" coupling analogous to sh→qo?
    # d→ch conditional probability vs baseline
    n_d = onset_totals_b.get('d', 0)
    p_ch_after_d = onset_bigrams_b['d'].get('ch', 0) / max(n_d, 1)
    p_qo_after_d = onset_bigrams_b['d'].get('qo', 0) / max(n_d, 1)
    n_sh = onset_totals_b.get('sh', 0)
    p_qo_after_sh = onset_bigrams_b['sh'].get('qo', 0) / max(n_sh, 1)
    p_ch_after_sh = onset_bigrams_b['sh'].get('ch', 0) / max(n_sh, 1)

    print(f"\n  P(ch|d) = {100*p_ch_after_d:.1f}% (ratio: {p_ch_after_d/max(base_ch_b,1e-10):.2f}×)")
    print(f"  P(qo|d) = {100*p_qo_after_d:.1f}% (ratio: {p_qo_after_d/max(base_qo_b,1e-10):.2f}×)")
    print(f"  P(ch|sh) = {100*p_ch_after_sh:.1f}% (ratio: {p_ch_after_sh/max(base_ch_b,1e-10):.2f}×)")
    print(f"  P(qo|sh) = {100*p_qo_after_sh:.1f}% (ratio: {p_qo_after_sh/max(base_qo_b,1e-10):.2f}×)")

    # H095: Medial trigrams (qo+ch/sh+word)
    print(f"\n{'='*70}")
    print("H095: MEDIAL TRIGRAM STRUCTURE (qo+ch/sh+word in B)")
    print(f"{'='*70}")

    # Collect all trigrams in B
    all_trigrams = Counter()
    qo_ch_trigrams = Counter()  # qo-onset + ch-onset + any
    qo_sh_trigrams = Counter()  # qo-onset + sh-onset + any
    sh_qo_ch_trigrams = Counter()  # sh+qo+ch sequence

    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 2):
            trigram = (ws[i], ws[i+1], ws[i+2])
            all_trigrams[trigram] += 1
            oc1 = onset_class(ws[i])
            oc2 = onset_class(ws[i+1])
            oc3 = onset_class(ws[i+2])
            if oc1 == 'qo' and oc2 == 'ch':
                qo_ch_trigrams[trigram] += 1
            if oc1 == 'qo' and oc2 == 'sh':
                qo_sh_trigrams[trigram] += 1
            if oc1 == 'sh' and oc2 == 'qo' and oc3 == 'ch':
                sh_qo_ch_trigrams[trigram] += 1

    print(f"\nTotal B trigram types: {len(all_trigrams)}")
    print(f"Total qo+ch trigrams: {sum(qo_ch_trigrams.values())} tokens, {len(qo_ch_trigrams)} types")
    print(f"Total qo+sh trigrams: {sum(qo_sh_trigrams.values())} tokens, {len(qo_sh_trigrams)} types")
    print(f"sh+qo+ch trigrams: {sum(sh_qo_ch_trigrams.values())} tokens, {len(sh_qo_ch_trigrams)} types")

    # Top qo+ch trigrams
    print(f"\n--- TOP qo+ch+X TRIGRAMS ---")
    for trigram, count in qo_ch_trigrams.most_common(15):
        w1, w2, w3 = trigram
        oc3 = onset_class(w3)
        print(f"  {w1} {w2} {w3} (w3 onset: {oc3}): {count}")

    # Top qo+sh trigrams
    print(f"\n--- TOP qo+sh+X TRIGRAMS ---")
    for trigram, count in qo_sh_trigrams.most_common(15):
        w1, w2, w3 = trigram
        oc3 = onset_class(w3)
        print(f"  {w1} {w2} {w3} (w3 onset: {oc3}): {count}")

    # Top sh+qo+ch trigrams (the full coupling sequence)
    print(f"\n--- TOP sh+qo+ch TRIGRAMS ---")
    for trigram, count in sh_qo_ch_trigrams.most_common(15):
        print(f"  {' '.join(trigram)}: {count}")

    # What is the word after qo+ch pairs? (third word onset distribution)
    qo_ch_third = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 2):
            if onset_class(ws[i]) == 'qo' and onset_class(ws[i+1]) == 'ch':
                qo_ch_third[onset_class(ws[i+2])] += 1

    print(f"\n--- ONSET CLASS OF THIRD WORD AFTER qo+ch ---")
    n_qo_ch = sum(qo_ch_third.values())
    for oc, count in qo_ch_third.most_common(8):
        print(f"  {oc}: {count} ({100*count/max(n_qo_ch,1):.1f}%)")

    # H096: daiin specifically as ch-predecessor in A
    print(f"\n{'='*70}")
    print("H096: daiin SPECIFICALLY AS ch-PREDECESSOR IN CURRIER A")
    print(f"{'='*70}")

    # In A, compute P(ch|daiin) vs P(ch|other-d-words)
    base_ch_a = sum(1 for w in a_words if onset_class(w) == 'ch') / max(len(a_words), 1)

    daiin_then_ch = 0
    daiin_total = 0
    otherd_then_ch = 0
    otherd_total = 0

    top_d_words_before_ch = Counter()
    top_d_words_not_before_ch = Counter()

    for r in a_records:
        ws = r['words']
        n = len(ws)
        for i in range(n - 1):
            w1 = ws[i]
            oc1 = onset_class(w1)
            oc2 = onset_class(ws[i+1])
            if oc1 == 'd':
                if w1 == 'daiin':
                    daiin_total += 1
                    if oc2 == 'ch':
                        daiin_then_ch += 1
                        top_d_words_before_ch[w1] += 1
                    else:
                        top_d_words_not_before_ch[w1] += 1
                else:
                    otherd_total += 1
                    if oc2 == 'ch':
                        otherd_then_ch += 1
                        top_d_words_before_ch[w1] += 1
                    else:
                        top_d_words_not_before_ch[w1] += 1

    p_ch_daiin = daiin_then_ch / max(daiin_total, 1)
    p_ch_otherd = otherd_then_ch / max(otherd_total, 1)

    print(f"\n  A baseline ch-rate: {100*base_ch_a:.1f}%")
    print(f"  P(ch | daiin): {100*p_ch_daiin:.1f}% ({daiin_then_ch}/{daiin_total}) → ratio: {p_ch_daiin/max(base_ch_a,1e-10):.2f}×")
    print(f"  P(ch | other-d): {100*p_ch_otherd:.1f}% ({otherd_then_ch}/{otherd_total}) → ratio: {p_ch_otherd/max(base_ch_a,1e-10):.2f}×")

    # Top d-words before ch
    print(f"\n  Top d-words that precede ch: {', '.join(f'{w}({c})' for w,c in top_d_words_before_ch.most_common(10))}")
    print(f"  Top d-words NOT preceding ch: {', '.join(f'{w}({c})' for w,c in top_d_words_not_before_ch.most_common(10))}")

    # By section
    print(f"\n  P(ch | daiin) by A section:")
    a_sections = sorted(set(r['section'] for r in a_records if r['section']))
    for sec in a_sections:
        sec_recs = [r for r in a_records if r['section'] == sec]
        n_words = sum(len(r['words']) for r in sec_recs)
        if n_words < 200:
            continue
        d_ch = 0
        d_total = 0
        for r in sec_recs:
            ws = r['words']
            n = len(ws)
            for i in range(n - 1):
                if ws[i] == 'daiin':
                    d_total += 1
                    if onset_class(ws[i+1]) == 'ch':
                        d_ch += 1
        p = d_ch / max(d_total, 1)
        base_ch_sec = sum(1 for r in sec_recs for w in r['words'] if onset_class(w) == 'ch') / max(n_words, 1)
        print(f"    {sec}: P(ch|daiin)={100*p:.1f}% ({d_ch}/{d_total}), baseline ch%={100*base_ch_sec:.1f}%, ratio={p/max(base_ch_sec,1e-10):.2f}×")

    # Also check daiin specifically as sh-predecessor
    daiin_then_sh = sum(1 for r in a_records for i, w in enumerate(r['words'][:-1]) if w == 'daiin' and onset_class(r['words'][i+1]) == 'sh')
    print(f"\n  daiin→sh in A: {daiin_then_sh}/{daiin_total} = {100*daiin_then_sh/max(daiin_total,1):.1f}%")

    base_sh_a = sum(1 for w in a_words if onset_class(w) == 'sh') / max(len(a_words), 1)
    print(f"  A baseline sh-rate: {100*base_sh_a:.1f}%, ratio: {daiin_then_sh/max(daiin_total,1)/max(base_sh_a,1e-10):.2f}×")

if __name__ == '__main__':
    main()
