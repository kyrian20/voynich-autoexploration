"""
exp_080: -am Suffix Class Analysis (H121), e-Infix Suffix Co-Occurrence (H120),
         Pharma A Transitional Analysis (H122)

H120: Do e-infix words (she-, che-, ke-) take specific suffix classes?
H121: Is -am a grammatical line-boundary marker in B?
H122: Where does Pharma A sit on the A-to-B spectrum of features?
"""

import re
import math
from collections import Counter, defaultdict

DATA_PATH = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"

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
    for suf in ['aiin', 'eedy', 'eey', 'edy', 'ain', 'chy', 'dy', 'ey', 'ol', 'or', 'al', 'ar', 'iin', 'in', 'am', 'y']:
        if word.endswith(suf) and len(word) > len(suf):
            return '-' + suf
    return 'other'

def e_infix_class(word):
    if word.startswith('she') and len(word) > 3:
        return ('sh', 'e')
    elif word.startswith('sh') and len(word) > 2:
        return ('sh', 'no-e')
    elif word.startswith('che') and len(word) > 3:
        return ('ch', 'e')
    elif word.startswith('ch') and len(word) > 2:
        return ('ch', 'no-e')
    elif word.startswith('ke') and len(word) > 2:
        return ('k', 'e')
    elif word.startswith('k') and len(word) > 1:
        return ('k', 'no-e')
    elif word.startswith('oe') and len(word) > 2:
        return ('o', 'e')
    elif word.startswith('o') and len(word) > 1:
        return ('o', 'no-e')
    elif word.startswith('qoe') and len(word) > 3:
        return ('qo', 'e')
    elif word.startswith('qo') and len(word) > 2:
        return ('qo', 'no-e')
    return (None, None)

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

def bigram_ppl_reduction(recs, alpha=0.1):
    unigram = Counter()
    bigram = defaultdict(Counter)
    for r in recs:
        ws = r['words']
        for w in ws:
            unigram[onset_class(w)] += 1
        for i in range(len(ws) - 1):
            bigram[onset_class(ws[i])][onset_class(ws[i+1])] += 1
    total = sum(unigram.values())
    n_types = len(unigram)
    log_uni = log_bi = 0.0
    n_tok = n_big = 0
    for r in recs:
        ws = r['words']
        ocs = [onset_class(w) for w in ws]
        for oc in ocs:
            log_uni += math.log2((unigram[oc] + alpha) / (total + alpha * n_types))
            n_tok += 1
        for i in range(len(ocs) - 1):
            oc1, oc2 = ocs[i], ocs[i+1]
            n1 = sum(bigram[oc1].values())
            log_bi += math.log2((bigram[oc1][oc2] + alpha) / (n1 + alpha * n_types))
            n_big += 1
    ppl_uni = 2 ** (-log_uni / max(n_tok, 1))
    ppl_bi = 2 ** (-log_bi / max(n_big, 1))
    return ppl_uni, ppl_bi, 100*(ppl_uni-ppl_bi)/max(ppl_uni,1), n_tok

def main():
    records = parse_corpus(DATA_PATH)
    a_records = [r for r in records if r['currier'] == 'A']
    b_records = [r for r in records if r['currier'] == 'B']
    herbal_a = [r for r in a_records if r['section'] == 'H']
    pharma_a = [r for r in a_records if r['section'] == 'P']

    # ================================================================
    print("="*70)
    print("H120: e-INFIX SUFFIX CO-OCCURRENCE ANALYSIS")
    print("="*70)

    for dialect_label, recs in [('Currier A', a_records), ('Currier B', b_records)]:
        all_words = [w for r in recs for w in r['words']]
        n_total = len(all_words)

        # Compute suffix distribution for e-infix vs non-e-infix by onset
        for onset_target in ['sh', 'ch', 'k', 'o']:
            e_words = [w for w in all_words if e_infix_class(w) == (onset_target, 'e')]
            noe_words = [w for w in all_words if e_infix_class(w) == (onset_target, 'no-e')]
            if len(e_words) < 10:
                continue

            e_suf = Counter(suffix_class(w) for w in e_words)
            noe_suf = Counter(suffix_class(w) for w in noe_words)
            n_e = len(e_words)
            n_noe = len(noe_words)

            print(f"\n{dialect_label} {onset_target}-onset: e-infix (n={n_e}) vs non-e (n={n_noe})")
            print(f"  {'Suffix':<10}", end="")
            for suf in ['-edy', '-eedy', '-ey', '-eey', '-ol', '-or', '-aiin', '-ain', '-am', '-dy', 'other']:
                e_p = e_suf.get(suf, 0) / max(n_e, 1)
                noe_p = noe_suf.get(suf, 0) / max(n_noe, 1)
                if e_p > 0.01 or noe_p > 0.01:
                    print(f"  {suf}: e={100*e_p:.0f}% noe={100*noe_p:.0f}%", end=" |")
            print()

    # ================================================================
    print(f"\n{'='*70}")
    print("H121: -am SUFFIX AS B LINE-BOUNDARY MARKER")
    print(f"{'='*70}")

    # All -am words in B
    b_all_words = [w for r in b_records for w in r['words']]
    n_b = len(b_all_words)
    am_words_b = Counter(w for w in b_all_words if w.endswith('am') and len(w) >= 3)

    print(f"\nAll B words ending in 'am' (n≥3): {len(am_words_b)} types, {sum(am_words_b.values())} tokens")
    print("Top -am words:")
    for word, cnt in am_words_b.most_common(20):
        print(f"  {word}: {cnt}")

    # Positional stats for all -am words
    am_first = am_mid = am_last = am_total = 0
    am_preceding = Counter()
    am_following = Counter()
    for r in b_records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            if w.endswith('am') and len(w) >= 3:
                am_total += 1
                if i == 0:
                    am_first += 1
                elif i == n - 1:
                    am_last += 1
                else:
                    am_mid += 1
                if i > 0:
                    am_preceding[onset_class(ws[i-1])] += 1
                if i < n - 1:
                    am_following[onset_class(ws[i+1])] += 1

    base_last_rate = sum(1 for r in b_records if r['words'] and r['words'][-1].endswith('am') and len(r['words'][-1]) >= 3) / max(len(b_records), 1)

    print(f"\n-am positional stats: n={am_total}")
    print(f"  first: {am_first} ({100*am_first/max(am_total,1):.1f}%)")
    print(f"  middle: {am_mid} ({100*am_mid/max(am_total,1):.1f}%)")
    print(f"  last: {am_last} ({100*am_last/max(am_total,1):.1f}%)")
    print(f"  Base line-final rate for average B word: {100*sum(len(r['words'])>0 for r in b_records)/max(n_b,1):.1f}%")
    print(f"  Preceding onset: {dict(am_preceding.most_common(6))}")
    print(f"  Following onset: {dict(am_following.most_common(6))}")

    # Para-final rate for -am words
    b_classified = classify_para_boundary(b_records)
    am_pf = am_pi = 0
    for r, is_pf in b_classified:
        if r['words']:
            last_w = r['words'][-1]
            if last_w.endswith('am') and len(last_w) >= 3:
                if is_pf:
                    am_pf += 1
                else:
                    am_pi += 1

    n_pf_b = sum(1 for _, is_pf in b_classified if is_pf)
    n_pi_b = sum(1 for _, is_pf in b_classified if not is_pf)
    print(f"\n-am at para-final positions: {am_pf}/{n_pf_b} = {100*am_pf/max(n_pf_b,1):.1f}%")
    print(f"-am at para-interior line-final: {am_pi}/{n_pi_b} = {100*am_pi/max(n_pi_b,1):.1f}%")

    # Compare to A
    a_all_words = [w for r in a_records for w in r['words']]
    am_words_a = Counter(w for w in a_all_words if w.endswith('am') and len(w) >= 3)
    print(f"\nA -am words: {len(am_words_a)} types, {sum(am_words_a.values())} tokens")
    am_last_a = sum(1 for r in a_records for i, w in enumerate(r['words'])
                    if w.endswith('am') and len(w) >= 3 and i == len(r['words']) - 1)
    am_total_a = sum(am_words_a.values())
    print(f"A -am last-rate: {am_last_a}/{am_total_a} = {100*am_last_a/max(am_total_a,1):.1f}%")
    print(f"Top A -am words: {list(am_words_a.most_common(10))}")

    # ================================================================
    print(f"\n{'='*70}")
    print("H122: PHARMA A ON THE A-TO-B SPECTRUM")
    print(f"{'='*70}")

    # Compare multiple features across: Herbal A, aiin-dom A, y-dom A, Pharma A, Currier B
    aiin_dom = [r for r in a_records if r['folio'] in AIIN_DOM_FOLIOS]
    y_dom = [r for r in a_records if r['folio'] not in AIIN_DOM_FOLIOS and r['section'] == 'H']

    groups = [('Herbal A', herbal_a), ('Aiin-dom A', aiin_dom), ('Y-dom A', y_dom),
              ('Pharma A', pharma_a), ('Currier B', b_records)]

    # Feature 1: bigram PPL reduction
    print(f"\nFeature 1: Bigram PPL reduction (sequential grammar strength)")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        ppl_uni, ppl_bi, pct, n_tok = bigram_ppl_reduction(recs)
        print(f"  {label:<20}: {pct:.1f}% (n={n_tok})")

    # Feature 2: sh→qo enrichment
    print(f"\nFeature 2: sh→qo enrichment")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(len(all_words), 1)
        sh_n = sh_qo = 0
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                if onset_class(ws[i]) == 'sh':
                    sh_n += 1
                    if onset_class(ws[i+1]) == 'qo':
                        sh_qo += 1
        enr = (sh_qo / max(sh_n, 1)) / max(base_qo, 1e-10)
        print(f"  {label:<20}: {enr:.2f}× (sh→qo={100*sh_qo/max(sh_n,1):.1f}%, base_qo={100*base_qo:.1f}%)")

    # Feature 3: she-→qo enrichment
    print(f"\nFeature 3: she-→qo enrichment")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        base_qo = sum(1 for w in all_words if onset_class(w) == 'qo') / max(len(all_words), 1)
        she_n = she_qo = 0
        for r in recs:
            ws = r['words']
            for i in range(len(ws) - 1):
                if e_infix_class(ws[i]) == ('sh', 'e'):
                    she_n += 1
                    if onset_class(ws[i+1]) == 'qo':
                        she_qo += 1
        enr = (she_qo / max(she_n, 1)) / max(base_qo, 1e-10)
        print(f"  {label:<20}: {enr:.2f}× (n={she_n})")

    # Feature 4: -edy suffix rate
    print(f"\nFeature 4: -edy suffix rate")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        edy_rate = sum(1 for w in all_words if w.endswith('edy') and len(w) > 3) / max(len(all_words), 1)
        print(f"  {label:<20}: {100*edy_rate:.2f}%")

    # Feature 5: qo-rate
    print(f"\nFeature 5: qo-onset rate")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        qo_rate = sum(1 for w in all_words if onset_class(w) == 'qo') / max(len(all_words), 1)
        print(f"  {label:<20}: {100*qo_rate:.1f}%")

    # Feature 6: Vocabulary Jaccard with B
    print(f"\nFeature 6: Vocabulary Jaccard with Currier B")
    b_types = set(w for r in b_records for w in r['words'])
    for label, recs in groups:
        if label == 'Currier B':
            continue
        if len(recs) < 50:
            continue
        types = set(w for r in recs for w in r['words'])
        jacc = len(types & b_types) / max(len(types | b_types), 1)
        print(f"  {label:<20}: {jacc:.3f} ({len(types & b_types)} shared)")

    # Feature 7: Top qo-word similarity to B
    print(f"\nFeature 7: Top qo-word types")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        qo_words = Counter(w for w in all_words if onset_class(w) == 'qo')
        print(f"  {label:<20}: {list(qo_words.most_common(5))}")

    # Feature 8: d-onset line-final enrichment
    print(f"\nFeature 8: d-onset line-final enrichment")
    for label, recs in groups:
        if len(recs) < 50:
            continue
        all_words = [w for r in recs for w in r['words']]
        base_d = sum(1 for w in all_words if onset_class(w) == 'd') / max(len(all_words), 1)
        last_words = [r['words'][-1] for r in recs if r['words']]
        d_last = sum(1 for w in last_words if onset_class(w) == 'd') / max(len(last_words), 1)
        enr = d_last / max(base_d, 1e-10)
        print(f"  {label:<20}: {enr:.2f}× (d at line-end={100*d_last:.1f}%, base={100*base_d:.1f}%)")

if __name__ == '__main__':
    main()
