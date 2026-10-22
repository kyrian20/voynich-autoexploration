"""
exp_076: Pharma A Dialect Position (H105) + Aiin-Dom d→qo Mechanism (H106)
         + Special Section Line-Final "Other" Decomposition (H107)
         + Para-Interior vs Para-Final Line-Ending (H108)

H105: Is Pharma A closer to B in onset-class vocabulary, suffix profile, and vocabulary Jaccard?
H106: Is aiin-dom d→qo=1.55× driven by daiin specifically preceding qo-onset words?
H107: What onset classes make up the "other" category in B Special section line-final words?
H108: Does B paragraph-final last word differ from within-paragraph last word in onset class?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Aiin-dominant Herbal A folios (from exp_059/exp_062)
AIIN_DOM_FOLIOS = {'f6r', 'f6v', 'f7r', 'f7v', 'f8r', 'f8v', 'f9r', 'f9v',
                   'f10r', 'f10v', 'f11r', 'f11v', 'f13r', 'f13v', 'f14r', 'f14v',
                   'f15r', 'f15v', 'f16r', 'f16v', 'f17r', 'f17v', 'f96r', 'f96v'}

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

def first_char(word):
    """Return first character of word (raw, not onset class)."""
    if not word:
        return ''
    return word[0]

def suffix_class(word):
    """Return the dominant suffix of a word."""
    for suf in ['aiin', 'eedy', 'eey', 'edy', 'ain', 'chy', 'dy', 'ey', 'ol', 'or', 'al', 'ar', 'iin', 'in', 'y']:
        if word.endswith(suf) and len(word) > len(suf):
            return '-' + suf
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

    # Split corpora
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']
    herbal_a = [r for r in a_records if r['section'] == 'H']
    pharma_a = [r for r in a_records if r['section'] == 'P']
    aiin_dom_a = [r for r in a_records if r['folio'] in AIIN_DOM_FOLIOS]
    special_b = [r for r in b_records if r['section'] == 'S']

    # ================================================================
    print("="*70)
    print("H105: PHARMA A DIALECT POSITION — ONSET DISTRIBUTION, SUFFIX PROFILE, JACCARD")
    print("="*70)

    # Onset-class frequency distributions
    def onset_dist(recs):
        words = [w for r in recs for w in r['words']]
        c = Counter(onset_class(w) for w in words)
        total = sum(c.values())
        return {oc: c.get(oc, 0) / max(total, 1) for oc in ['qo', 'ch', 'sh', 'd', 's', 'o', 'k', 't', 'p', 'y', 'other']}, total

    def suffix_dist(recs):
        words = [w for r in recs for w in r['words']]
        c = Counter(suffix_class(w) for w in words)
        total = sum(c.values())
        return {suf: c.get(suf, 0) / max(total, 1) for suf in ['-edy', '-eedy', '-ain', '-aiin', '-ol', '-or', '-ey', '-dy', '-chy']}

    def vocab_jaccard(recs1, recs2):
        types1 = set(w for r in recs1 for w in r['words'])
        types2 = set(w for r in recs2 for w in r['words'])
        return len(types1 & types2) / max(len(types1 | types2), 1), len(types1 & types2), len(types1 | types2)

    # Compare onset distributions
    print("\nOnset-class frequency distribution:")
    print(f"  {'Onset':<8}", end="")
    groups = [('Herbal A', herbal_a), ('Pharma A', pharma_a), ('Currier B', b_records)]
    for label, _ in groups:
        print(f"  {label:<12}", end="")
    print()

    dist_map = {}
    for label, recs in groups:
        dist_map[label], n = onset_dist(recs)
        print(f"  n={n} ({label})")

    for oc in ['qo', 'ch', 'sh', 'd', 's', 'o', 'k', 't', 'p', 'y', 'other']:
        print(f"  {oc:<8}", end="")
        for label, _ in groups:
            print(f"  {100*dist_map[label][oc]:>10.1f}%  ", end="")
        print()

    # Suffix profile comparison
    print("\nSuffix profile:")
    print(f"  {'Suffix':<8}", end="")
    for label, _ in groups:
        print(f"  {label:<12}", end="")
    print()
    suf_map = {}
    for label, recs in groups:
        suf_map[label] = suffix_dist(recs)
    for suf in ['-edy', '-eedy', '-ain', '-aiin', '-ol', '-or', '-ey', '-dy', '-chy']:
        print(f"  {suf:<8}", end="")
        for label, _ in groups:
            print(f"  {100*suf_map[label].get(suf, 0):>10.1f}%  ", end="")
        print()

    # Vocabulary Jaccard
    print("\nVocabulary Jaccard:")
    jacc, inter, union = vocab_jaccard(pharma_a, b_records)
    print(f"  Pharma A ↔ Currier B: {jacc:.3f} ({inter} shared / {union} total)")
    jacc, inter, union = vocab_jaccard(herbal_a, b_records)
    print(f"  Herbal A ↔ Currier B: {jacc:.3f} ({inter} shared / {union} total)")
    jacc, inter, union = vocab_jaccard(pharma_a, herbal_a)
    print(f"  Pharma A ↔ Herbal A:  {jacc:.3f} ({inter} shared / {union} total)")
    jacc, inter, union = vocab_jaccard(a_records, b_records)
    print(f"  A global ↔ B global:  {jacc:.3f} ({inter} shared / {union} total)")

    # Top word pairs driving Pharma A sh→qo
    print("\nTop sh→qo word pairs in Pharma A (specific words):")
    sh_qo_pairs = Counter()
    for r in pharma_a:
        ws = r['words']
        for i in range(len(ws) - 1):
            if onset_class(ws[i]) == 'sh' and onset_class(ws[i+1]) == 'qo':
                sh_qo_pairs[(ws[i], ws[i+1])] += 1
    for pair, cnt in sh_qo_pairs.most_common(15):
        print(f"  {pair[0]} → {pair[1]}: {cnt}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H106: AIIN-DOM d→qo MECHANISM — IS daiin THE QO-PREDICTOR?")
    print(f"{'='*70}")

    # In aiin-dom A, compute d→qo specifically for daiin vs other d-words
    daiin_to_qo = 0
    daiin_total = 0
    other_d_to_qo = 0
    other_d_total = 0

    # Also track actual word pairs
    d_qo_pairs = Counter()
    d_qo_by_word = defaultdict(Counter)

    for r in aiin_dom_a:
        ws = r['words']
        for i in range(len(ws) - 1):
            if onset_class(ws[i]) == 'd':
                w_next_oc = onset_class(ws[i+1])
                if ws[i] == 'daiin':
                    daiin_total += 1
                    if w_next_oc == 'qo':
                        daiin_to_qo += 1
                else:
                    other_d_total += 1
                    if w_next_oc == 'qo':
                        other_d_to_qo += 1
                if w_next_oc == 'qo':
                    d_qo_pairs[(ws[i], ws[i+1])] += 1
                    d_qo_by_word[ws[i]][ws[i+1]] += 1

    print(f"\nAiin-dom A: d→qo breakdown:")
    print(f"  daiin→qo: {daiin_to_qo}/{daiin_total} = {100*daiin_to_qo/max(daiin_total,1):.1f}%")
    print(f"  other-d→qo: {other_d_to_qo}/{other_d_total} = {100*other_d_to_qo/max(other_d_total,1):.1f}%")

    # Baseline qo rate in aiin-dom
    aiin_words = [w for r in aiin_dom_a for w in r['words']]
    base_qo = sum(1 for w in aiin_words if onset_class(w) == 'qo') / max(len(aiin_words), 1)
    print(f"  Baseline qo rate in aiin-dom: {100*base_qo:.1f}%")
    print(f"  daiin→qo enrichment: {(daiin_to_qo/max(daiin_total,1))/max(base_qo,1e-10):.2f}×")
    print(f"  other-d→qo enrichment: {(other_d_to_qo/max(other_d_total,1))/max(base_qo,1e-10):.2f}×")

    print(f"\nTop d→qo word pairs in aiin-dom A:")
    for pair, cnt in d_qo_pairs.most_common(15):
        print(f"  {pair[0]} → {pair[1]}: {cnt}")

    # Also check y-dom A for comparison
    y_dom_a = [r for r in a_records
               if r['folio'] not in AIIN_DOM_FOLIOS and r['section'] == 'H']
    y_daiin_to_qo = 0
    y_daiin_total = 0
    y_other_d_to_qo = 0
    y_other_d_total = 0
    for r in y_dom_a:
        ws = r['words']
        for i in range(len(ws) - 1):
            if onset_class(ws[i]) == 'd':
                w_next_oc = onset_class(ws[i+1])
                if ws[i] == 'daiin':
                    y_daiin_total += 1
                    if w_next_oc == 'qo':
                        y_daiin_to_qo += 1
                else:
                    y_other_d_total += 1
                    if w_next_oc == 'qo':
                        y_other_d_to_qo += 1

    y_words = [w for r in y_dom_a for w in r['words']]
    y_base_qo = sum(1 for w in y_words if onset_class(w) == 'qo') / max(len(y_words), 1)
    print(f"\nY-dom Herbal A comparison (baseline qo={100*y_base_qo:.1f}%):")
    print(f"  daiin→qo: {y_daiin_to_qo}/{y_daiin_total} = {100*y_daiin_to_qo/max(y_daiin_total,1):.1f}% ({(y_daiin_to_qo/max(y_daiin_total,1))/max(y_base_qo,1e-10):.2f}×)")
    print(f"  other-d→qo: {y_other_d_to_qo}/{y_other_d_total} = {100*y_other_d_to_qo/max(y_other_d_total,1):.1f}% ({(y_other_d_to_qo/max(y_other_d_total,1))/max(y_base_qo,1e-10):.2f}×)")

    # ================================================================
    print(f"\n{'='*70}")
    print("H107: B SPECIAL SECTION LINE-FINAL 'OTHER' DECOMPOSITION")
    print(f"{'='*70}")

    # Decompose "other" onset words at line-ends in B Special section
    all_b_words = [w for r in b_records for w in r['words']]
    base_onset_b = Counter(onset_class(w) for w in all_b_words)
    n_b_total = len(all_b_words)

    special_last_words = []
    for r in special_b:
        ws = r['words']
        if ws:
            special_last_words.append(ws[-1])

    other_last_words_s = [w for w in special_last_words if onset_class(w) == 'other']
    print(f"\nB Special: {len(special_last_words)} last words; {len(other_last_words_s)} 'other' onset ({100*len(other_last_words_s)/max(len(special_last_words),1):.1f}%)")
    print(f"'Other' line-final words in B Special section — first char distribution:")
    fc_dist = Counter(first_char(w) for w in other_last_words_s)
    for char, cnt in fc_dist.most_common(15):
        print(f"  '{char}': {cnt} ({100*cnt/max(len(other_last_words_s),1):.1f}%)")

    print(f"\nTop 'other' line-final words in B Special section:")
    word_dist = Counter(other_last_words_s)
    for word, cnt in word_dist.most_common(20):
        print(f"  {word}: {cnt}")

    # Compare to non-Special B "other" at line-ends
    non_special_b = [r for r in b_records if r['section'] != 'S']
    non_special_last = [r['words'][-1] for r in non_special_b if r['words']]
    other_last_non_s = [w for w in non_special_last if onset_class(w) == 'other']
    fc_non_s = Counter(first_char(w) for w in other_last_non_s)
    print(f"\nNon-Special B 'other' last words — first char distribution (for comparison):")
    for char, cnt in fc_non_s.most_common(10):
        print(f"  '{char}': {cnt} ({100*cnt/max(len(other_last_non_s),1):.1f}%)")

    # ================================================================
    print(f"\n{'='*70}")
    print("H108: PARA-INTERIOR vs PARA-FINAL LINE-ENDING ONSET DISTRIBUTION")
    print(f"{'='*70}")

    # Classify records: is the NEXT record a para-start? If so, this is para-final.
    # We need to look ahead in the record sequence.
    def classify_para_boundary(recs):
        """Return list of (record, is_para_final) pairs."""
        result = []
        n = len(recs)
        for i, r in enumerate(recs):
            # This line is para-final if the next line is a para-start
            is_pf = False
            if i + 1 < n:
                is_pf = recs[i + 1]['is_para_start']
            else:
                is_pf = True  # last line of corpus
            result.append((r, is_pf))
        return result

    for dialect, d_recs in [('B', b_records), ('A', a_records)]:
        classified = classify_para_boundary(d_recs)
        d_words = [w for r in d_recs for w in r['words']]
        base_onset = Counter(onset_class(w) for w in d_words)
        n_total = len(d_words)

        para_final_last = Counter()
        para_interior_last = Counter()

        for r, is_pf in classified:
            ws = r['words']
            if not ws:
                continue
            last_oc = onset_class(ws[-1])
            if is_pf:
                para_final_last[last_oc] += 1
            else:
                para_interior_last[last_oc] += 1

        n_pf = sum(para_final_last.values())
        n_pi = sum(para_interior_last.values())
        print(f"\nCurrier {dialect}: para-final last words={n_pf}, para-interior last words={n_pi}")
        print(f"  {'Onset':<8} {'Para-final':>12} {'Para-interior':>14} {'P-final enr':>12} {'P-interior enr':>14}")
        for oc in ['qo', 'sh', 'o', 'd', 'ch', 'k', 'other']:
            base_p = base_onset.get(oc, 0) / max(n_total, 1)
            pf_p = para_final_last.get(oc, 0) / max(n_pf, 1)
            pi_p = para_interior_last.get(oc, 0) / max(n_pi, 1)
            pf_enr = pf_p / max(base_p, 1e-10)
            pi_enr = pi_p / max(base_p, 1e-10)
            print(f"  {oc:<8} {100*pf_p:>10.1f}% {100*pi_p:>12.1f}% {pf_enr:>11.2f}× {pi_enr:>13.2f}×")

if __name__ == '__main__':
    main()
