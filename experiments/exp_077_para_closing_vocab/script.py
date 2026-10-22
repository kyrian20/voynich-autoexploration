"""
exp_077: Para-Closing Vocabulary (H109, H112), Pharma A sh-Words (H110),
         daiin→qo→X Trigram in Aiin-Dom A (H111)

H109: What specific o-words close B paragraphs? What specific words appear at B para-finals?
H110: Do Pharma A sh-words differ from Herbal A sh-words in stem and suffix?
H111: Does the daiin→qo→X chain in aiin-dom A have a constrained third word?
H112: What specific ch-words appear at A para-finals?
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

def suffix_class(word):
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

def classify_para_boundary(recs):
    """Return list of (record, is_para_final) pairs."""
    result = []
    n = len(recs)
    for i, r in enumerate(recs):
        is_pf = False
        if i + 1 < n:
            is_pf = recs[i + 1]['is_para_start']
        else:
            is_pf = True
        result.append((r, is_pf))
    return result

def main():
    records = parse_corpus(DATA_PATH)
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']
    herbal_a = [r for r in a_records if r['section'] == 'H']
    pharma_a = [r for r in a_records if r['section'] == 'P']
    aiin_dom_a = [r for r in a_records if r['folio'] in AIIN_DOM_FOLIOS]
    y_dom_a = [r for r in a_records if r['folio'] not in AIIN_DOM_FOLIOS and r['section'] == 'H']

    # ================================================================
    print("="*70)
    print("H109: B PARA-CLOSING VOCABULARY (o-onset para-final words)")
    print("="*70)

    b_classified = classify_para_boundary(b_records)
    all_b_words = [w for r in b_records for w in r['words']]
    b_word_freq = Counter(all_b_words)
    n_b = len(all_b_words)

    para_final_b = [(r, pf) for r, pf in b_classified if pf]
    para_interior_b = [(r, pf) for r, pf in b_classified if not pf]

    pf_last_words_b = Counter(r['words'][-1] for r, _ in para_final_b if r['words'])
    pi_last_words_b = Counter(r['words'][-1] for r, _ in para_interior_b if r['words'])

    n_pf = sum(pf_last_words_b.values())
    n_pi = sum(pi_last_words_b.values())

    print(f"\nB para-final last words: n={n_pf}")
    print(f"Top B para-final last words (any onset):")
    print(f"  {'Word':<15} {'PF count':>8} {'PF %':>7} {'Corp freq':>10} {'Corp %':>7} {'Enrichment':>11}")
    for word, cnt in pf_last_words_b.most_common(25):
        pf_pct = 100 * cnt / max(n_pf, 1)
        corp_pct = 100 * b_word_freq.get(word, 0) / max(n_b, 1)
        pi_cnt = pi_last_words_b.get(word, 0)
        enr = (cnt / max(n_pf, 1)) / max(b_word_freq.get(word, 0) / max(n_b, 1), 1e-10)
        print(f"  {word:<15} {cnt:>8} {pf_pct:>6.1f}% {b_word_freq.get(word,0):>10} {corp_pct:>6.1f}% {enr:>10.2f}×")

    # Specifically o-onset para-final words
    print(f"\nB o-onset para-final words (specifically):")
    o_pf = Counter(w for w in (r['words'][-1] for r, _ in para_final_b if r['words']) if onset_class(w) == 'o')
    for word, cnt in o_pf.most_common(20):
        enr = (cnt / max(n_pf, 1)) / max(b_word_freq.get(word, 0) / max(n_b, 1), 1e-10)
        print(f"  {word}: {cnt} ({enr:.2f}×)")

    # Compare o-onset within-para line-final
    o_pi = Counter(w for w in (r['words'][-1] for r, _ in para_interior_b if r['words']) if onset_class(w) == 'o')
    print(f"\nTop B o-onset within-para line-final words:")
    for word, cnt in o_pi.most_common(15):
        pct_pi = 100 * cnt / max(n_pi, 1)
        enr = (cnt / max(n_pi, 1)) / max(b_word_freq.get(word, 0) / max(n_b, 1), 1e-10)
        print(f"  {word}: {cnt} ({pct_pi:.1f}%, {enr:.2f}×)")

    # By section
    print(f"\nB para-final last words by section:")
    pf_by_section = defaultdict(Counter)
    for r, is_pf in b_classified:
        if is_pf and r['words']:
            sec = r['section'] or 'UNK'
            pf_by_section[sec][r['words'][-1]] += 1
    for sec in sorted(pf_by_section, key=lambda s: -sum(pf_by_section[s].values())):
        n_sec = sum(pf_by_section[sec].values())
        print(f"  {sec} (n={n_sec}): {dict(pf_by_section[sec].most_common(5))}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H112: A PARA-CLOSING ch-WORDS")
    print(f"{'='*70}")

    a_classified = classify_para_boundary(a_records)
    all_a_words = [w for r in a_records for w in r['words']]
    a_word_freq = Counter(all_a_words)
    n_a = len(all_a_words)

    para_final_a = [(r, pf) for r, pf in a_classified if pf]
    para_interior_a = [(r, pf) for r, pf in a_classified if not pf]

    pf_last_words_a = Counter(r['words'][-1] for r, _ in para_final_a if r['words'])
    pi_last_words_a = Counter(r['words'][-1] for r, _ in para_interior_a if r['words'])
    n_pf_a = sum(pf_last_words_a.values())
    n_pi_a = sum(pi_last_words_a.values())

    print(f"\nA para-final last words: n={n_pf_a}")
    print(f"Top A para-final last words:")
    print(f"  {'Word':<15} {'PF count':>8} {'PF %':>7} {'Corp freq':>10} {'Enrichment':>11}")
    for word, cnt in pf_last_words_a.most_common(25):
        enr = (cnt / max(n_pf_a, 1)) / max(a_word_freq.get(word, 0) / max(n_a, 1), 1e-10)
        print(f"  {word:<15} {cnt:>8} {100*cnt/max(n_pf_a,1):>6.1f}% {a_word_freq.get(word,0):>10} {enr:>10.2f}×")

    print(f"\nA ch-onset para-final words specifically:")
    ch_pf_a = Counter(w for w in (r['words'][-1] for r, _ in para_final_a if r['words']) if onset_class(w) == 'ch')
    for word, cnt in ch_pf_a.most_common(20):
        enr = (cnt / max(n_pf_a, 1)) / max(a_word_freq.get(word, 0) / max(n_a, 1), 1e-10)
        print(f"  {word}: {cnt} ({enr:.2f}×)")

    print(f"\nA d-onset para-final words:")
    d_pf_a = Counter(w for w in (r['words'][-1] for r, _ in para_final_a if r['words']) if onset_class(w) == 'd')
    for word, cnt in d_pf_a.most_common(15):
        enr = (cnt / max(n_pf_a, 1)) / max(a_word_freq.get(word, 0) / max(n_a, 1), 1e-10)
        print(f"  {word}: {cnt} ({enr:.2f}×)")

    # ================================================================
    print(f"\n{'='*70}")
    print("H110: PHARMA A vs HERBAL A sh-WORD COMPARISON")
    print(f"{'='*70}")

    pharma_sh = Counter(w for r in pharma_a for w in r['words'] if onset_class(w) == 'sh')
    herbal_sh = Counter(w for r in herbal_a for w in r['words'] if onset_class(w) == 'sh')
    n_pharma_sh = sum(pharma_sh.values())
    n_herbal_sh = sum(herbal_sh.values())

    print(f"\nPharma A sh-words: {n_pharma_sh} total")
    print("Top Pharma A sh-words:")
    for word, cnt in pharma_sh.most_common(20):
        pct = 100 * cnt / max(n_pharma_sh, 1)
        print(f"  {word}: {cnt} ({pct:.1f}%)")

    print(f"\nHerbal A sh-words: {n_herbal_sh} total")
    print("Top Herbal A sh-words:")
    for word, cnt in herbal_sh.most_common(20):
        pct = 100 * cnt / max(n_herbal_sh, 1)
        print(f"  {word}: {cnt} ({pct:.1f}%)")

    # Suffix distribution for sh-words by section
    print(f"\nSuffix distribution of sh-words:")
    for label, recs in [('Pharma A', pharma_a), ('Herbal A', herbal_a)]:
        sh_words = [w for r in recs for w in r['words'] if onset_class(w) == 'sh']
        suf_dist = Counter(suffix_class(w) for w in sh_words)
        n = len(sh_words)
        print(f"  {label} (n={n}):", {s: f"{100*c/max(n,1):.1f}%" for s, c in suf_dist.most_common(8)})

    # What follows sh in Pharma A vs Herbal A
    print(f"\nWhat follows sh-words (transition distribution):")
    for label, recs in [('Pharma A', pharma_a), ('Herbal A', herbal_a)]:
        sh_nexts = Counter()
        n_sh = 0
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                if onset_class(ws[i]) == 'sh':
                    sh_nexts[onset_class(ws[i+1])] += 1
                    n_sh += 1
        print(f"  {label}: n(sh)={n_sh}")
        for oc, cnt in sh_nexts.most_common(8):
            print(f"    sh→{oc}: {cnt} ({100*cnt/max(n_sh,1):.1f}%)")

    # ================================================================
    print(f"\n{'='*70}")
    print("H111: daiin→qo→X TRIGRAM IN AIIN-DOM HERBAL A")
    print(f"{'='*70}")

    # In aiin-dom A, find all daiin → qo-word → X patterns
    daiin_qo_x = Counter()  # X onset class
    daiin_qo_x_words = Counter()  # actual X words
    n_daiin_qo = 0

    for r in aiin_dom_a:
        ws = r['words']
        for i in range(len(ws) - 2):
            if ws[i] == 'daiin' and onset_class(ws[i+1]) == 'qo':
                x_oc = onset_class(ws[i+2])
                x_word = ws[i+2]
                daiin_qo_x[x_oc] += 1
                daiin_qo_x_words[x_word] += 1
                n_daiin_qo += 1

    print(f"\nAiin-dom A: daiin → qo-word → X trigrams (n={n_daiin_qo})")
    print(f"X onset class distribution:")
    all_aiin_words = [w for r in aiin_dom_a for w in r['words']]
    base_onset_aiin = Counter(onset_class(w) for w in all_aiin_words)
    n_aiin = len(all_aiin_words)
    for oc, cnt in daiin_qo_x.most_common():
        base_p = base_onset_aiin.get(oc, 0) / max(n_aiin, 1)
        enr = (cnt / max(n_daiin_qo, 1)) / max(base_p, 1e-10)
        print(f"  X={oc}: {cnt} ({100*cnt/max(n_daiin_qo,1):.1f}%, {enr:.2f}×)")

    print(f"\nActual daiin→qo→X word triplets:")
    # Find the full triplets
    triplets = []
    for r in aiin_dom_a:
        ws = r['words']
        for i in range(len(ws) - 2):
            if ws[i] == 'daiin' and onset_class(ws[i+1]) == 'qo':
                triplets.append((ws[i], ws[i+1], ws[i+2]))
    triplet_c = Counter(triplets)
    for tri, cnt in triplet_c.most_common(20):
        print(f"  {tri[0]} → {tri[1]} → {tri[2]}: {cnt}")

    # For comparison: non-daiin d-word → qo → X in aiin-dom
    other_d_qo_x = Counter()
    n_other_d_qo = 0
    for r in aiin_dom_a:
        ws = r['words']
        for i in range(len(ws) - 2):
            if ws[i] != 'daiin' and onset_class(ws[i]) == 'd' and onset_class(ws[i+1]) == 'qo':
                other_d_qo_x[onset_class(ws[i+2])] += 1
                n_other_d_qo += 1

    print(f"\nNon-daiin d→qo→X in aiin-dom (n={n_other_d_qo}):")
    for oc, cnt in other_d_qo_x.most_common():
        base_p = base_onset_aiin.get(oc, 0) / max(n_aiin, 1)
        enr = (cnt / max(n_other_d_qo, 1)) / max(base_p, 1e-10)
        print(f"  X={oc}: {cnt} ({100*cnt/max(n_other_d_qo,1):.1f}%, {enr:.2f}×)")

    # What precedes daiin→qo in aiin-dom?
    print(f"\nWhat precedes daiin in aiin-dom A (when daiin is followed by qo)?")
    preceding = Counter()
    for r in aiin_dom_a:
        ws = r['words']
        for i in range(1, len(ws) - 1):
            if ws[i] == 'daiin' and onset_class(ws[i+1]) == 'qo':
                preceding[onset_class(ws[i-1])] += 1
    for oc, cnt in preceding.most_common():
        print(f"  {oc}→daiin→qo: {cnt}")

if __name__ == '__main__':
    main()
