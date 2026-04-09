"""
exp_085: she- Dual Function Analysis (H140), B ol-Prefix Stem Structure (H141),
         -am Suffix Onset-Class Distribution (H143)

H140: Are she-prefix's para-start function and qo-predictor function the SAME thing?
H141: Does B ol-prefix stem complexity predict positional role (line-closer vs para-starter)?
H143: What onset classes take -am suffix? Is -am onset-structured?
"""

import re
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

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

def classify_para_boundary(recs):
    result = []
    n = len(recs)
    for i, r in enumerate(recs):
        is_pf = (i + 1 >= n) or recs[i + 1]['is_para_start']
        result.append((r, is_pf))
    return result

GALLOWS = {'k','t','p','f'}

def has_gallows(stem):
    return any(c in GALLOWS for c in stem)

def is_she_word(word):
    return word.startswith('she') and len(word) > 3

def is_sh_other(word):
    return word.startswith('sh') and len(word) > 2 and not is_she_word(word)


# ============================================================
# H140: she- Dual Function Analysis
# ============================================================

def h140_she_dual_function(a_recs):
    print("\n=== H140: she- Dual Function — Para-Start Marker AND qo-Predictor ===")

    labeled = classify_para_boundary(a_recs)

    # For each A record, categorize the line by what opens it
    # Then compute qo-onset rate on that same line
    she_opens_para = {'qo_rate': 0, 'total': 0, 'qo_bigrams': 0, 'total_bigrams': 0}
    sh_other_opens_para = {'qo_rate': 0, 'total': 0, 'qo_bigrams': 0, 'total_bigrams': 0}
    she_opens_nonpara = {'qo_rate': 0, 'total': 0, 'qo_bigrams': 0, 'total_bigrams': 0}
    sh_other_opens_nonpara = {'qo_rate': 0, 'total': 0, 'qo_bigrams': 0, 'total_bigrams': 0}

    def categorize_opening(word):
        if is_she_word(word):
            return 'she'
        elif is_sh_other(word):
            return 'sh_other'
        return 'other'

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        opener_type = categorize_opening(ws[0])
        is_ps = r['is_para_start']

        # Compute qo_rate on this line (fraction of words that are qo-onset)
        qo_count = sum(1 for w in ws if onset_class(w) == 'qo')
        total_words = len(ws)

        # Bigrams (sequential transitions ON THIS LINE)
        bigrams_here = 0
        qo_bigrams_here = 0
        for i in range(len(ws)-1):
            if onset_class(ws[i]) == 'sh' or is_she_word(ws[i]) or is_sh_other(ws[i]):
                bigrams_here += 1
                if onset_class(ws[i+1]) == 'qo':
                    qo_bigrams_here += 1

        if opener_type == 'she':
            if is_ps:
                she_opens_para['total'] += total_words
                she_opens_para['qo_rate'] += qo_count
            else:
                she_opens_nonpara['total'] += total_words
                she_opens_nonpara['qo_rate'] += qo_count
        elif opener_type == 'sh_other':
            if is_ps:
                sh_other_opens_para['total'] += total_words
                sh_other_opens_para['qo_rate'] += qo_count
            else:
                sh_other_opens_nonpara['total'] += total_words
                sh_other_opens_nonpara['qo_rate'] += qo_count

    print(f"\n--- qo rate on lines by opener type and para-start status ---")
    for name, stats in [("she- opens para-start", she_opens_para),
                         ("she- opens non-para-start", she_opens_nonpara),
                         ("sh-other opens para-start", sh_other_opens_para),
                         ("sh-other opens non-para-start", sh_other_opens_nonpara)]:
        if stats['total'] == 0:
            continue
        qr = stats['qo_rate'] / stats['total']
        print(f"  {name}: qo_rate={qr:.2%} (over {stats['total']} words)")

    # Better: compute TRANSITION RATES (she-→qo) on para-start lines vs non-para-start lines
    print(f"\n--- she-→qo and sh-other→qo transition rates by line type ---")

    she_qo_ps = 0; she_tot_ps = 0
    she_qo_nps = 0; she_tot_nps = 0
    sho_qo_ps = 0; sho_tot_ps = 0
    sho_qo_nps = 0; sho_tot_nps = 0

    for r, _ in labeled:
        ws = r['words']
        is_ps = r['is_para_start']
        for i in range(len(ws)-1):
            curr, nxt = ws[i], ws[i+1]
            if is_she_word(curr):
                if is_ps:
                    she_tot_ps += 1
                    if onset_class(nxt) == 'qo': she_qo_ps += 1
                else:
                    she_tot_nps += 1
                    if onset_class(nxt) == 'qo': she_qo_nps += 1
            elif is_sh_other(curr):
                if is_ps:
                    sho_tot_ps += 1
                    if onset_class(nxt) == 'qo': sho_qo_ps += 1
                else:
                    sho_tot_nps += 1
                    if onset_class(nxt) == 'qo': sho_qo_nps += 1

    print(f"  she-→qo on para-start lines: {she_qo_ps}/{she_tot_ps} = {she_qo_ps/max(she_tot_ps,1):.1%}")
    print(f"  she-→qo on non-para-start lines: {she_qo_nps}/{she_tot_nps} = {she_qo_nps/max(she_tot_nps,1):.1%}")
    print(f"  sh-other→qo on para-start lines: {sho_qo_ps}/{sho_tot_ps} = {sho_qo_ps/max(sho_tot_ps,1):.1%}")
    print(f"  sh-other→qo on non-para-start lines: {sho_qo_nps}/{sho_tot_nps} = {sho_qo_nps/max(sho_tot_nps,1):.1%}")

    # Base qo rate
    qo_base = sum(1 for r in a_recs for w in r['words'] if onset_class(w) == 'qo') / \
               max(sum(len(r['words']) for r in a_recs), 1)
    print(f"  Base qo rate in A: {qo_base:.1%}")

    # Count how many para-start lines begin with she- vs sh-other
    ps_she = sum(1 for r, _ in labeled if r['is_para_start'] and r['words'] and is_she_word(r['words'][0]))
    ps_sh_other = sum(1 for r, _ in labeled if r['is_para_start'] and r['words'] and is_sh_other(r['words'][0]))
    ps_total = sum(1 for r, _ in labeled if r['is_para_start'])
    nps_she = sum(1 for r, _ in labeled if not r['is_para_start'] and r['words'] and is_she_word(r['words'][0]))
    print(f"\n  Para-start lines with she-opener: {ps_she}/{ps_total} = {ps_she/max(ps_total,1):.1%}")
    print(f"  Para-start lines with sh-other opener: {ps_sh_other}/{ps_total} = {ps_sh_other/max(ps_total,1):.1%}")
    print(f"  Non-para-start lines with she-opener: {nps_she}/{len(labeled)-ps_total} = {nps_she/max(len(labeled)-ps_total,1):.1%}")

    # For Pharma A: does she-para-start function hold?
    pharma_folios = set()
    folio_words = defaultdict(list)
    for r in a_recs:
        for w in r['words']:
            folio_words[r['folio_base']].append(w)
    for folio, ws in folio_words.items():
        ol_rate = sum(1 for w in ws if w.endswith('ol')) / max(len(ws), 1)
        if ol_rate >= 0.15 and folio not in AIIN_DOM_FOLIOS:
            pharma_folios.add(folio)

    pharma_recs = [r for r in a_recs if r['folio_base'] in pharma_folios]
    pharma_labeled = classify_para_boundary(pharma_recs)

    pharma_ps = sum(1 for r, _ in pharma_labeled if r['is_para_start'])
    pharma_ps_she = sum(1 for r, _ in pharma_labeled if r['is_para_start'] and r['words'] and is_she_word(r['words'][0]))
    pharma_ps_sh = sum(1 for r, _ in pharma_labeled if r['is_para_start'] and r['words'] and is_sh_other(r['words'][0]))
    print(f"\n  Pharma A para-starts: {pharma_ps} total; she-opener: {pharma_ps_she} ({pharma_ps_she/max(pharma_ps,1):.1%}); sh-other: {pharma_ps_sh} ({pharma_ps_sh/max(pharma_ps,1):.1%})")

    # Pharma A she-→qo rate
    pharma_she_qo = 0; pharma_she_tot = 0
    for r in pharma_recs:
        ws = r['words']
        for i in range(len(ws)-1):
            if is_she_word(ws[i]):
                pharma_she_tot += 1
                if onset_class(ws[i+1]) == 'qo': pharma_she_qo += 1
    print(f"  Pharma A she-→qo: {pharma_she_qo}/{pharma_she_tot} = {pharma_she_qo/max(pharma_she_tot,1):.1%}")


# ============================================================
# H141: B ol-Prefix Stem Structure
# ============================================================

def h141_ol_stem_structure(b_recs):
    print("\n=== H141: B ol-Prefix Stem Complexity and Positional Role ===")

    labeled = classify_para_boundary(b_recs)

    # For all ol-prefix words, compute:
    # - stem = part between 'ol' and suffix
    # - stem length
    # - does stem contain gallows (k, t, p, f)?
    # - positional role

    ol_words_stats = defaultdict(lambda: {
        'total': 0, 'line_first': 0, 'line_last': 0, 'ps_first': 0, 'pf_last': 0,
        'stem': '', 'stem_len': 0, 'has_gallows': False, 'suffix': ''
    })

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        for w in ws:
            if not w.startswith('ol') or len(w) <= 2:
                continue
            suf = get_suffix(w)
            if suf is None:
                stem = w[2:]
            else:
                stem = w[2:-len(suf)]
            ol_words_stats[w]['total'] += 1
            ol_words_stats[w]['stem'] = stem
            ol_words_stats[w]['stem_len'] = len(stem)
            ol_words_stats[w]['has_gallows'] = has_gallows(stem)
            ol_words_stats[w]['suffix'] = suf or ''

        if ws[0].startswith('ol'):
            ol_words_stats[ws[0]]['line_first'] += 1
            if r['is_para_start']:
                ol_words_stats[ws[0]]['ps_first'] += 1

        if ws[-1].startswith('ol'):
            ol_words_stats[ws[-1]]['line_last'] += 1
            if is_pf:
                ol_words_stats[ws[-1]]['pf_last'] += 1

    # Separate by stem complexity
    simple_stem = []  # stem len 0-1
    medium_stem = []  # stem len 2-3
    complex_stem = []  # stem len 4+
    gallows_stem = []  # stem contains gallows

    for w, stats in ol_words_stats.items():
        if stats['total'] < 3:
            continue
        if stats['has_gallows']:
            gallows_stem.append((w, stats))
        if stats['stem_len'] <= 1:
            simple_stem.append((w, stats))
        elif stats['stem_len'] <= 3:
            medium_stem.append((w, stats))
        else:
            complex_stem.append((w, stats))

    def group_positional_summary(name, word_list):
        tot = sum(s['total'] for _, s in word_list)
        ll = sum(s['line_last'] for _, s in word_list)
        lf = sum(s['line_first'] for _, s in word_list)
        ps = sum(s['ps_first'] for _, s in word_list)
        pf = sum(s['pf_last'] for _, s in word_list)
        if tot == 0:
            return
        print(f"\n  {name} (n_types={len(word_list)}, total={tot}):")
        print(f"    line-first: {lf/tot:.1%}, line-last: {ll/tot:.1%}")
        print(f"    PS-first: {ps/tot:.1%}, PF-last: {pf/tot:.1%}")
        print(f"    Top words: {sorted(word_list, key=lambda x: -x[1]['total'])[:5]}")

    print(f"\nB ol-prefix stem complexity groups:")
    group_positional_summary("Simple stem (len≤1, e.g. oly=ol+y)", simple_stem)
    group_positional_summary("Medium stem (len 2-3, e.g. olky=ol+k+y)", medium_stem)
    group_positional_summary("Complex stem (len 4+, e.g. olchedy=ol+ch+edy)", complex_stem)
    group_positional_summary("Gallows-containing stem (any length)", gallows_stem)

    # Print full table for all ol words with stats
    print(f"\n--- Full B ol-prefix word table (n≥3) ---")
    print(f"{'Word':<15} {'n':>4} {'Stem':<10} {'StemLen':>7} {'Gallows':>8} {'LLast%':>7} {'PSFirst%':>9}")
    sorted_words = sorted(ol_words_stats.items(), key=lambda x: -x[1]['total'])
    for w, stats in sorted_words:
        if stats['total'] < 3:
            continue
        ll_r = stats['line_last'] / stats['total']
        ps_r = stats['ps_first'] / stats['total']
        gal = 'Y' if stats['has_gallows'] else 'N'
        print(f"  {w:<13} {stats['total']:>4} {stats['stem']:<10} {stats['stem_len']:>7} {gal:>8} {ll_r:>6.0%} {ps_r:>8.0%}")


# ============================================================
# H143: -am Suffix Onset-Class Distribution
# ============================================================

def h143_am_onset_class(b_recs, a_recs):
    print("\n=== H143: -am Suffix Onset-Class Distribution ===")

    def am_stats(recs, dialect):
        onset_total = Counter()
        onset_am = Counter()
        total_words = 0

        for r in recs:
            for w in r['words']:
                oc = onset_class(w)
                onset_total[oc] += 1
                total_words += 1
                if w.endswith('am') and len(w) > 2:
                    onset_am[oc] += 1

        total_am = sum(onset_am.values())
        base_am_rate = total_am / max(total_words, 1)

        print(f"\n{dialect} -am distribution (total -am words={total_am}):")
        print(f"{'Onset':<8} {'Total':>6} {'AM count':>8} {'AM rate':>8} {'AM/Total%':>10} {'Enrichment':>11}")
        for oc in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
            tot = onset_total.get(oc, 0)
            am = onset_am.get(oc, 0)
            if tot == 0:
                continue
            am_rate = am / tot
            enr = am_rate / max(base_am_rate, 0.001)
            print(f"  {oc:<6} {tot:>6} {am:>8} {am_rate:>7.1%} {am/max(total_am,1):>9.1%} {enr:>10.2f}×")

        # Top -am words by onset class
        print(f"\n  Top -am words in {dialect}:")
        am_words = Counter()
        for r in recs:
            for w in r['words']:
                if w.endswith('am') and len(w) > 2:
                    am_words[w] += 1
        for w, cnt in am_words.most_common(15):
            oc = onset_class(w)
            print(f"    {w} ({oc}-onset): {cnt}")

        # Internal structure of -am words
        print(f"\n  Stem structure before -am suffix:")
        stem_lengths = Counter()
        for w in am_words:
            oc_len = {'qo':2,'ch':2,'sh':2,'p':1,'t':1,'k':1,'d':1,'s':1,'y':1,'o':1,'other':0}
            oc = onset_class(w)
            ol = oc_len.get(oc, 0)
            stem = w[ol:-2]  # remove onset and -am
            if stem:
                stem_lengths[stem] += am_words[w]
        print(f"  Top stems before -am: {stem_lengths.most_common(15)}")

    am_stats(b_recs, "Currier B")
    am_stats(a_recs, "Currier A")

    # Cross-dialect: which -am words appear in both A and B?
    b_am = Counter()
    a_am = Counter()
    for r in b_recs:
        for w in r['words']:
            if w.endswith('am') and len(w) > 2:
                b_am[w] += 1
    for r in a_recs:
        for w in r['words']:
            if w.endswith('am') and len(w) > 2:
                a_am[w] += 1

    shared = set(b_am.keys()) & set(a_am.keys())
    print(f"\n--- Cross-dialect -am words (appear in both A and B): {len(shared)} types ---")
    shared_sorted = sorted(shared, key=lambda w: -(b_am[w] + a_am[w]))
    for w in shared_sorted[:15]:
        print(f"  {w}: B={b_am[w]}, A={a_am[w]}, onset={onset_class(w)}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading data...")
    recs = parse_voynich(DATA_PATH)
    print(f"Total body records: {len(recs)}")

    a_recs, b_recs = assign_dialect(recs)
    print(f"A: {len(a_recs)}, B: {len(b_recs)}")

    # H140
    h140_she_dual_function(a_recs)

    # H141
    h141_ol_stem_structure(b_recs)

    # H143
    h143_am_onset_class(b_recs, a_recs)

if __name__ == '__main__':
    main()
