"""
exp_083: Liquid-Glide Suffix Substitution Pairs (H132),
         B Para-Start Morphological Marking (H133),
         A Para-Start Markers (H135)

H132: chol↔chey, shor↔sheor — are liquid-final and glide-final word pairs
      complementarily distributed across aiin-dom and y-dom registers?
H133: B para-starts show no p-onset marking — are they morphologically
      indistinguishable from non-para-start lines?
H135: Does A have a para-start morphological marker?
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

AIIN_DOM_FOLIOS = {
    'f1r','f1v','f2r','f2v','f3r','f3v','f4r','f4v','f5r','f5v',
    'f6r','f6v','f7r','f7v','f8r','f8v','f13r','f13v','f14r','f14v',
    'f15r','f15v','f16r','f16v'
}

def folio_base(folio):
    return folio.split('.')[0]

def onset_class(word):
    if word.startswith('qo'):  return 'qo'
    if word.startswith('ch'):  return 'ch'
    if word.startswith('sh'):  return 'sh'
    if word.startswith('p'):   return 'p'
    if word.startswith('t') and not word.startswith('th'): return 't'
    if word.startswith('k'):   return 'k'
    if word.startswith('d'):   return 'd'
    if word.startswith('s'):   return 's'
    if word.startswith('y'):   return 'y'
    if word.startswith('o'):   return 'o'
    return 'other'

KNOWN_SUFFIXES = [
    'eedy','edy','eey','ain','aiin','ol','or','ey','dy','am','al','y'
]

def get_suffix(word):
    for suf in KNOWN_SUFFIXES:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def parse_voynich(path):
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'^<([^>]+)>', line)
            if not m:
                continue
            locus_raw = m.group(1)
            text = line[m.end():].strip()
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_raw = parts[0]
            locus_code = parts[1]
            folio = folio_raw.lstrip('+*=&~')
            is_para_start = locus_code.lstrip('+*=/~&').startswith('@')
            is_body = locus_code.lstrip('+*@=/~&').startswith('P')
            if not is_body:
                continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            records.append({
                'folio': folio,
                'folio_base': folio_base(folio),
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start,
            })
    return records

def assign_dialect(recs):
    folio_words = defaultdict(list)
    for r in recs:
        for w in r['words']:
            folio_words[r['folio_base']].append(w)

    b_folios = set()
    for folio, ws in folio_words.items():
        edy_count = sum(1 for w in ws if w.endswith('edy') or w.endswith('eedy'))
        if edy_count / max(len(ws), 1) >= 0.05:
            b_folios.add(folio)

    a_recs, b_recs = [], []
    for r in recs:
        if r['folio_base'] in b_folios:
            b_recs.append(r)
        else:
            a_recs.append(r)
    return a_recs, b_recs

def pharma_a_folios(a_recs):
    folio_words = defaultdict(list)
    for r in a_recs:
        for w in r['words']:
            folio_words[r['folio_base']].append(w)

    pharma_folios = set()
    for folio, ws in folio_words.items():
        ol_rate = sum(1 for w in ws if w.endswith('ol')) / max(len(ws), 1)
        if ol_rate >= 0.15 and folio not in AIIN_DOM_FOLIOS:
            pharma_folios.add(folio)
    return pharma_folios

def split_herbal_a(a_recs, pharma_folios):
    herbal = [r for r in a_recs if r['folio_base'] not in pharma_folios]
    aiin = [r for r in herbal if r['folio_base'] in AIIN_DOM_FOLIOS]
    y = [r for r in herbal if r['folio_base'] not in AIIN_DOM_FOLIOS]
    return herbal, aiin, y

def classify_para_boundary(recs):
    result = []
    n = len(recs)
    for i, r in enumerate(recs):
        is_pf = (i + 1 >= n) or recs[i + 1]['is_para_start']
        result.append((r, is_pf))
    return result


# ============================================================
# H132: Liquid-Glide Suffix Substitution Pairs
# ============================================================

def h132_suffix_substitution_pairs(aiin_recs, y_recs):
    print("\n=== H132: Liquid-Glide Suffix Substitution Pairs ===")

    # Approach: for each stem (onset+internal_segment), find if it appears
    # with -ol/-or in aiin-dom and -ey/-eey in y-dom

    # Extract (onset, stem, suffix) triples
    def get_stem_suffix_pairs(recs, label):
        triples = Counter()
        for r in recs:
            for w in r['words']:
                suf = get_suffix(w)
                if suf is None:
                    continue
                oc = onset_class(w)
                # stem = everything between onset and suffix
                oc_len = {'qo':2,'ch':2,'sh':2,'p':1,'t':1,'k':1,'d':1,'s':1,'y':1,'o':1,'other':0}
                ol = oc_len.get(oc, 0)
                if ol == 0:
                    continue
                stem = w[ol:-len(suf)]
                if stem:
                    triples[(oc, stem, suf)] += 1
        return triples

    aiin_triples = get_stem_suffix_pairs(aiin_recs, "Aiin-dom")
    y_triples = get_stem_suffix_pairs(y_recs, "Y-dom")

    # Get all (onset, stem) pairs that appear with BOTH liquid and glide suffixes across registers
    # Liquid suffixes: -ol, -or; Glide suffixes: -ey, -eey
    LIQUID = {'ol', 'or'}
    GLIDE = {'ey', 'eey'}

    # For each (onset, stem), compute aiin vs y rate for liquid and glide
    stem_keys = set((oc, stem) for (oc, stem, suf) in aiin_triples) | \
                 set((oc, stem) for (oc, stem, suf) in y_triples)

    candidates = []
    for (oc, stem) in stem_keys:
        # Aiin-dom liquid and glide counts
        a_liq = sum(aiin_triples.get((oc, stem, s), 0) for s in LIQUID)
        a_gli = sum(aiin_triples.get((oc, stem, s), 0) for s in GLIDE)
        a_tot = sum(aiin_triples.get((oc, stem, s), 0) for s in KNOWN_SUFFIXES)

        # Y-dom liquid and glide counts
        y_liq = sum(y_triples.get((oc, stem, s), 0) for s in LIQUID)
        y_gli = sum(y_triples.get((oc, stem, s), 0) for s in GLIDE)
        y_tot = sum(y_triples.get((oc, stem, s), 0) for s in KNOWN_SUFFIXES)

        # Only consider stems with enough tokens
        if a_tot + y_tot < 10:
            continue

        # Compute: in aiin-dom, is liquid preferred? in y-dom, is glide preferred?
        a_liq_rate = a_liq / max(a_tot, 1)
        a_gli_rate = a_gli / max(a_tot, 1)
        y_liq_rate = y_liq / max(y_tot, 1)
        y_gli_rate = y_gli / max(y_tot, 1)

        # Substitution score: aiin prefers liquid, y-dom prefers glide
        # = (a_liq_rate - y_liq_rate) + (y_gli_rate - a_gli_rate)
        sub_score = (a_liq_rate - y_liq_rate) + (y_gli_rate - a_gli_rate)

        candidates.append({
            'onset': oc, 'stem': stem,
            'a_tot': a_tot, 'y_tot': y_tot,
            'a_liq': a_liq, 'a_liq_rate': a_liq_rate,
            'a_gli': a_gli, 'a_gli_rate': a_gli_rate,
            'y_liq': y_liq, 'y_liq_rate': y_liq_rate,
            'y_gli': y_gli, 'y_gli_rate': y_gli_rate,
            'sub_score': sub_score
        })

    # Sort by substitution score
    candidates.sort(key=lambda x: -x['sub_score'])

    print(f"\nTop substitution pairs (aiin-dom liquid > y-dom; y-dom glide > aiin-dom):")
    print(f"{'Word stem':<15} {'a_n':>4} {'a_liq%':>8} {'a_gli%':>8} {'y_n':>4} {'y_liq%':>8} {'y_gli%':>8} {'score':>7}")
    for c in candidates[:20]:
        word_stem = c['onset'] + '+' + c['stem']
        print(f"  {word_stem:<13} {c['a_tot']:>4} {c['a_liq_rate']:>7.0%} {c['a_gli_rate']:>7.0%} "
              f"{c['y_tot']:>4} {c['y_liq_rate']:>7.0%} {c['y_gli_rate']:>7.0%} {c['sub_score']:>7.2f}")

    # Specific focus on ch, sh, cth, k stems
    print(f"\n--- Key stem pairs (ch and sh onset) ---")
    key_stems = [('ch',''), ('ch','k'), ('ch','ok'), ('ch','ot'), ('ch','cth'),
                 ('sh',''), ('sh','k'), ('sh','od'), ('cth','')]  # empty stem = word is just onset+suffix
    # Note: for 'ch' with empty stem, word = ch+suf e.g. chol, chey
    for (oc, stem) in key_stems:
        a_tot = sum(aiin_triples.get((oc, stem, s), 0) for s in KNOWN_SUFFIXES)
        y_tot = sum(y_triples.get((oc, stem, s), 0) for s in KNOWN_SUFFIXES)
        if a_tot + y_tot == 0:
            continue

        a_liq = sum(aiin_triples.get((oc, stem, s), 0) for s in LIQUID)
        a_gli = sum(aiin_triples.get((oc, stem, s), 0) for s in GLIDE)
        y_liq = sum(y_triples.get((oc, stem, s), 0) for s in LIQUID)
        y_gli = sum(y_triples.get((oc, stem, s), 0) for s in GLIDE)

        # Specific suffix breakdown
        a_ol = aiin_triples.get((oc, stem, 'ol'), 0)
        a_or = aiin_triples.get((oc, stem, 'or'), 0)
        a_ey = aiin_triples.get((oc, stem, 'ey'), 0)
        a_eey = aiin_triples.get((oc, stem, 'eey'), 0)
        y_ol = y_triples.get((oc, stem, 'ol'), 0)
        y_or = y_triples.get((oc, stem, 'or'), 0)
        y_ey = y_triples.get((oc, stem, 'ey'), 0)
        y_eey = y_triples.get((oc, stem, 'eey'), 0)

        print(f"\n  {oc}+'{stem}' (word: {oc+stem}):")
        print(f"    Aiin-dom (n={a_tot}): -ol={a_ol}({a_ol/max(a_tot,1):.0%}), -or={a_or}({a_or/max(a_tot,1):.0%}), -ey={a_ey}({a_ey/max(a_tot,1):.0%}), -eey={a_eey}({a_eey/max(a_tot,1):.0%})")
        print(f"    Y-dom    (n={y_tot}): -ol={y_ol}({y_ol/max(y_tot,1):.0%}), -or={y_or}({y_or/max(y_tot,1):.0%}), -ey={y_ey}({y_ey/max(y_tot,1):.0%}), -eey={y_eey}({y_eey/max(y_tot,1):.0%})")


# ============================================================
# H133: B Para-Start Morphological Marking
# ============================================================

def h133_b_para_start_marking(b_recs):
    print("\n=== H133: B Para-Start Morphological Marking ===")

    para_start_words = []  # First words of para-start lines
    non_ps_words = []      # First words of non-para-start lines
    para_start_all = []    # ALL words of para-start lines
    non_ps_all = []        # ALL words of non-para-start lines

    for r in b_recs:
        ws = r['words']
        if not ws:
            continue
        if r['is_para_start']:
            para_start_words.append(ws[0])
            para_start_all.extend(ws)
        else:
            non_ps_words.append(ws[0])
            non_ps_all.extend(ws)

    print(f"\nB para-start lines: {len(para_start_words)}, non-para-start: {len(non_ps_words)}")

    # Onset distribution comparison
    ps_onsets = Counter(onset_class(w) for w in para_start_words)
    nps_onsets = Counter(onset_class(w) for w in non_ps_words)
    ps_n = len(para_start_words)
    nps_n = len(non_ps_words)

    print(f"\n--- First-word onset distribution: para-start vs non-para-start ---")
    print(f"{'Onset':<8} {'PS rate':>8} {'NPS rate':>8} {'Enr':>8}")
    for oc in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
        ps_r = ps_onsets.get(oc, 0) / max(ps_n, 1)
        nps_r = nps_onsets.get(oc, 0) / max(nps_n, 1)
        enr = ps_r / max(nps_r, 0.001)
        if ps_onsets.get(oc, 0) + nps_onsets.get(oc, 0) == 0:
            continue
        print(f"  {oc:<6} {ps_r:>7.1%} {nps_r:>7.1%} {enr:>7.2f}×")

    # Suffix distribution
    ps_sufs = Counter(get_suffix(w) for w in para_start_words if get_suffix(w))
    nps_sufs = Counter(get_suffix(w) for w in non_ps_words if get_suffix(w))
    ps_suf_n = sum(ps_sufs.values())
    nps_suf_n = sum(nps_sufs.values())

    print(f"\n--- First-word suffix distribution: para-start vs non-para-start ---")
    for suf in ['edy','eedy','aiin','y','dy','ey','eey','ol','or','am','al']:
        ps_r = ps_sufs.get(suf, 0) / max(ps_suf_n, 1)
        nps_r = nps_sufs.get(suf, 0) / max(nps_suf_n, 1)
        enr = ps_r / max(nps_r, 0.001)
        if ps_sufs.get(suf, 0) + nps_sufs.get(suf, 0) == 0:
            continue
        print(f"  -{suf:<6} {ps_r:>7.1%} {nps_r:>7.1%} {enr:>7.2f}×")

    # Top specific words at para-starts
    print(f"\n--- Top B para-start first words ---")
    ps_word_counts = Counter(para_start_words)
    all_word_counts = Counter(w for r in b_recs for w in r['words'])
    total_words = sum(all_word_counts.values())
    for w, cnt in ps_word_counts.most_common(15):
        base_rate = all_word_counts.get(w, 0) / max(total_words, 1)
        enr = (cnt / max(ps_n, 1)) / max(base_rate, 0.0001)
        print(f"  {w}: {cnt} ({cnt/max(ps_n,1):.1%}, base {base_rate:.1%}, enr={enr:.1f}×)")

    # Word length comparison
    ps_lengths = Counter(len(w) for w in para_start_words)
    nps_lengths = Counter(len(w) for w in non_ps_words)
    print(f"\n--- First-word length distribution ---")
    for l in range(2, 10):
        ps_r = ps_lengths.get(l, 0) / max(ps_n, 1)
        nps_r = nps_lengths.get(l, 0) / max(nps_n, 1)
        if ps_r + nps_r > 0.01:
            print(f"  len={l}: para-start={ps_r:.1%}, non-para-start={nps_r:.1%}")

    # Daiin at para-start?
    ps_daiin = ps_word_counts.get('daiin', 0)
    nps_daiin = Counter(non_ps_words).get('daiin', 0)
    print(f"\ndaiin as first word: para-start={ps_daiin}/{ps_n}={ps_daiin/max(ps_n,1):.1%}, non-para-start={nps_daiin}/{nps_n}={nps_daiin/max(nps_n,1):.1%}")


# ============================================================
# H135: A Para-Start Morphological Markers
# ============================================================

def h135_a_para_start(a_recs):
    print("\n=== H135: A Para-Start Morphological Markers ===")

    labeled = classify_para_boundary(a_recs)

    para_start_first = []
    non_ps_first = []
    para_final_last = []
    within_para_last = []
    all_first = []

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        all_first.append(ws[0])
        if r['is_para_start']:
            para_start_first.append(ws[0])
        else:
            non_ps_first.append(ws[0])
        if is_pf:
            para_final_last.append(ws[-1])
        else:
            within_para_last.append(ws[-1])

    ps_n = len(para_start_first)
    nps_n = len(non_ps_first)
    print(f"\nA para-start lines: {ps_n}, non-para-start: {nps_n}")
    print(f"A para-final lines: {len(para_final_last)}, within-para: {len(within_para_last)}")

    # First-word onset at para-start vs non-para-start
    ps_onsets = Counter(onset_class(w) for w in para_start_first)
    nps_onsets = Counter(onset_class(w) for w in non_ps_first)
    all_onsets = Counter(onset_class(w) for r in a_recs for w in r['words'])
    all_total = sum(all_onsets.values())

    print(f"\n--- A first-word onset: para-start vs non-para-start ---")
    print(f"{'Onset':<8} {'PS rate':>8} {'NPS rate':>8} {'Enr':>8}")
    for oc in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
        ps_r = ps_onsets.get(oc, 0) / max(ps_n, 1)
        nps_r = nps_onsets.get(oc, 0) / max(nps_n, 1)
        enr = ps_r / max(nps_r, 0.001)
        if ps_onsets.get(oc, 0) + nps_onsets.get(oc, 0) == 0:
            continue
        print(f"  {oc:<6} {ps_r:>7.1%} {nps_r:>7.1%} {enr:>7.2f}×")

    # Daiin at para-start vs para-final vs mid
    def daiin_rates(words, label):
        cnt = sum(1 for w in words if w == 'daiin')
        n = len(words)
        return cnt, n, cnt/max(n,1)

    ps_d, ps_n2, ps_dr = daiin_rates(para_start_first, "para-start first")
    nps_d, nps_n2, nps_dr = daiin_rates(non_ps_first, "non-para-start first")
    pf_d, pf_n, pf_dr = daiin_rates(para_final_last, "para-final last")
    wp_d, wp_n, wp_dr = daiin_rates(within_para_last, "within-para last")

    print(f"\n--- daiin rates at different positions ---")
    print(f"  para-start first word: {ps_d}/{ps_n2} = {ps_dr:.1%}")
    print(f"  non-para-start first word: {nps_d}/{nps_n2} = {nps_dr:.1%}")
    print(f"  para-final last word: {pf_d}/{pf_n} = {pf_dr:.1%}")
    print(f"  within-para last word: {wp_d}/{wp_n} = {wp_dr:.1%}")

    # Top A para-start first words
    print(f"\n--- Top A para-start first words ---")
    ps_words = Counter(para_start_first)
    all_a_words = Counter(w for r in a_recs for w in r['words'])
    total_a = sum(all_a_words.values())
    for w, cnt in ps_words.most_common(15):
        base = all_a_words.get(w, 0) / max(total_a, 1)
        enr = (cnt/max(ps_n,1)) / max(base, 0.0001)
        print(f"  {w}: {cnt} ({cnt/max(ps_n,1):.1%}, base {base:.1%}, enr={enr:.1f}×)")

    # What distinguishes A para-start from para-interior?
    # Is -am enriched at A para-start last words?
    print(f"\n--- A last-word -am: para-final vs within-para ---")
    pf_am = sum(1 for w in para_final_last if w.endswith('am'))
    wp_am = sum(1 for w in within_para_last if w.endswith('am'))
    print(f"  Para-final -am last word: {pf_am}/{len(para_final_last)} = {pf_am/max(len(para_final_last),1):.1%}")
    print(f"  Within-para -am last word: {wp_am}/{len(within_para_last)} = {wp_am/max(len(within_para_last),1):.1%}")

    # Top A para-final last words
    print(f"\n--- Top A para-final last words ---")
    pf_words = Counter(para_final_last)
    for w, cnt in pf_words.most_common(15):
        base = all_a_words.get(w, 0) / max(total_a, 1)
        print(f"  {w} ({onset_class(w)}-onset, -{get_suffix(w)}): {cnt} ({cnt/max(len(para_final_last),1):.1%})")

    # First word onset at A para-final vs non-para-final lines
    # (Is there anything special about A lines AFTER a para-final, i.e., the para-start?)
    print(f"\n--- A onset distribution by line position type ---")
    onset_names = ['qo','ch','sh','p','t','k','d','s','y','o','other']
    pos_types = {'para-start first': para_start_first, 'para-final last': para_final_last}
    for pos_name, words in pos_types.items():
        onset_dist = Counter(onset_class(w) for w in words)
        n = len(words)
        top = [(oc, onset_dist.get(oc,0)/n) for oc in onset_names if onset_dist.get(oc,0) > 0]
        top.sort(key=lambda x: -x[1])
        print(f"  {pos_name}: {[(oc, f'{r:.0%}') for oc,r in top[:5]]}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading data...")
    recs = parse_voynich(DATA_PATH)
    print(f"Total body records: {len(recs)}")

    a_recs, b_recs = assign_dialect(recs)
    pharma_folios = pharma_a_folios(a_recs)
    herbal_recs, aiin_recs, y_recs = split_herbal_a(a_recs, pharma_folios)

    print(f"A: {len(a_recs)}, B: {len(b_recs)}")
    print(f"Herbal A: {len(herbal_recs)} (Aiin-dom: {len(aiin_recs)}, Y-dom: {len(y_recs)})")

    # H132
    h132_suffix_substitution_pairs(aiin_recs, y_recs)

    # H133
    h133_b_para_start_marking(b_recs)

    # H135
    h135_a_para_start(a_recs)

if __name__ == '__main__':
    main()
