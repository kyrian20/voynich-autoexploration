"""
exp_082: Aiin-Dom Register e-Infix Following Distribution (H129),
         Aiin-Dom -ol/-or Paradigm Analysis (H128),
         B Paragraph Structure Parsability (H130)

H129: In aiin-dom, she- prefix SUPPRESSES qo (0.41×). What does she- predict instead?
H128: Aiin-dom has -ol=13.6%, -or=12.2% — 2× more than y-dom. Why?
H130: Can B's tripartite paragraph grammar predict para-boundaries from word features?
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

def is_she_word(word):
    return word.startswith('she') and len(word) > 3

def is_sh_other(word):
    return word.startswith('sh') and len(word) > 2 and not is_she_word(word)

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
# H129: What Does she- Predict in Aiin-Dom?
# ============================================================

def h129_she_following_in_registers(aiin_recs, y_recs, b_recs):
    print("\n=== H129: she- Following Distribution in Registers ===")

    def following_dist(recs, word_filter, label, classes=None):
        total = 0
        following = Counter()
        for r in recs:
            ws = r['words']
            for i in range(len(ws)-1):
                if word_filter(ws[i]):
                    oc = onset_class(ws[i+1])
                    following[oc] += 1
                    total += 1

        # Base rates
        all_onsets = Counter(onset_class(w) for r in recs for w in r['words'])
        all_total = sum(all_onsets.values())

        print(f"\n{label} (n_she={total} following transitions):")
        print(f"{'Onset':<8} {'Count':>6} {'Rate':>8} {'Base':>8} {'Enr':>8}")
        for oc in ['qo','ch','sh','o','d','s','k','y','p','other']:
            cnt = following.get(oc, 0)
            rate = cnt / max(total, 1)
            base = all_onsets.get(oc, 0) / max(all_total, 1)
            enr = rate / max(base, 0.001)
            print(f"  {oc:<6} {cnt:>6} {rate:>7.1%} {base:>7.1%} {enr:>7.2f}×")
        return following, total

    # she- words
    aiin_she, aiin_she_n = following_dist(aiin_recs, is_she_word, "Aiin-dom: she-→X")
    y_she, y_she_n = following_dist(y_recs, is_she_word, "Y-dom: she-→X")
    b_she, b_she_n = following_dist(b_recs, is_she_word, "B: she-→X")

    # sh-other words (for comparison)
    aiin_sh, aiin_sh_n = following_dist(aiin_recs, is_sh_other, "Aiin-dom: sh-other→X")
    y_sh, y_sh_n = following_dist(y_recs, is_sh_other, "Y-dom: sh-other→X")

    # Summary table
    print("\n--- Summary: Top following onset for she- by register ---")
    for name, fol, n in [("Aiin-dom she-", aiin_she, aiin_she_n),
                          ("Y-dom she-", y_she, y_she_n),
                          ("B she-", b_she, b_she_n)]:
        if n == 0:
            print(f"  {name}: n=0")
            continue
        top = fol.most_common(3)
        print(f"  {name} (n={n}): top={[(oc, f'{c/n:.0%}') for oc,c in top]}")

    # What is she- enrichment for ch specifically in aiin-dom?
    print("\n--- she-→ch enrichment detail for aiin-dom ---")
    # Get base ch rate
    all_aiin_onsets = Counter(onset_class(w) for r in aiin_recs for w in r['words'])
    aiin_total = sum(all_aiin_onsets.values())
    ch_base = all_aiin_onsets.get('ch', 0) / max(aiin_total, 1)
    she_ch_rate = aiin_she.get('ch', 0) / max(aiin_she_n, 1)
    print(f"  she-→ch rate: {she_ch_rate:.1%} (base ch={ch_base:.1%}, enrichment={she_ch_rate/max(ch_base,0.001):.2f}×)")

    # What specific she- words appear in aiin-dom?
    print("\n--- Top she- words in aiin-dom ---")
    she_words_aiin = Counter()
    for r in aiin_recs:
        for w in r['words']:
            if is_she_word(w):
                she_words_aiin[w] += 1
    for w, cnt in she_words_aiin.most_common(10):
        print(f"  {w}: {cnt}")


# ============================================================
# H128: Aiin-Dom -ol/-or Paradigm Analysis
# ============================================================

def h128_ol_or_paradigm(aiin_recs, y_recs):
    print("\n=== H128: Aiin-Dom -ol/-or Paradigm Analysis ===")

    def ol_or_by_onset(recs, label):
        onset_total = Counter()
        onset_ol = Counter()
        onset_or = Counter()
        for r in recs:
            for w in r['words']:
                oc = onset_class(w)
                onset_total[oc] += 1
                if w.endswith('ol') and len(w) > 2:
                    onset_ol[oc] += 1
                if w.endswith('or') and len(w) > 2:
                    onset_or[oc] += 1

        print(f"\n{label}:")
        print(f"{'Onset':<8} {'Total':>6} {'-ol %':>8} {'-or %':>8} {'-ol+or %':>10}")
        for oc in ['qo','ch','sh','o','d','s','k','y','p','other']:
            tot = onset_total.get(oc, 0)
            if tot < 5:
                continue
            ol_r = onset_ol.get(oc, 0) / max(tot, 1)
            or_r = onset_or.get(oc, 0) / max(tot, 1)
            print(f"  {oc:<6} {tot:>6} {ol_r:>7.1%} {or_r:>7.1%} {ol_r+or_r:>9.1%}")

    ol_or_by_onset(aiin_recs, "Aiin-dom")
    ol_or_by_onset(y_recs, "Y-dom")

    # Top -ol words in aiin-dom vs y-dom
    print("\n--- Top -ol words: Aiin-dom vs Y-dom ---")
    aiin_ol = Counter()
    y_ol = Counter()
    for r in aiin_recs:
        for w in r['words']:
            if w.endswith('ol') and len(w) > 2:
                aiin_ol[w] += 1
    for r in y_recs:
        for w in r['words']:
            if w.endswith('ol') and len(w) > 2:
                y_ol[w] += 1

    print("Aiin-dom top -ol: " + str(aiin_ol.most_common(10)))
    print("Y-dom top -ol: " + str(y_ol.most_common(10)))

    # Top -or words
    print("\n--- Top -or words: Aiin-dom vs Y-dom ---")
    aiin_or = Counter()
    y_or = Counter()
    for r in aiin_recs:
        for w in r['words']:
            if w.endswith('or') and len(w) > 2:
                aiin_or[w] += 1
    for r in y_recs:
        for w in r['words']:
            if w.endswith('or') and len(w) > 2:
                y_or[w] += 1

    print("Aiin-dom top -or: " + str(aiin_or.most_common(10)))
    print("Y-dom top -or: " + str(y_or.most_common(10)))

    # Do the same stems appear with different suffixes in aiin-dom vs y-dom?
    # Compare: ch+ol vs ch+ey rates in each register
    print("\n--- Suffix paradigm contrast for ch-onset words ---")
    def ch_suffix_dist(recs, label):
        ch_total = 0
        suf_cnt = Counter()
        for r in recs:
            for w in r['words']:
                if w.startswith('ch'):
                    ch_total += 1
                    suf = get_suffix(w)
                    if suf:
                        suf_cnt[suf] += 1
        print(f"\n{label} ch-onset (n={ch_total}):")
        for suf, cnt in suf_cnt.most_common(8):
            print(f"  -{suf}: {cnt} ({cnt/max(ch_total,1):.1%})")

    ch_suffix_dist(aiin_recs, "Aiin-dom")
    ch_suffix_dist(y_recs, "Y-dom")

    # Similarly for o-onset words
    print("\n--- Suffix paradigm contrast for o-onset words ---")
    def o_suffix_dist(recs, label):
        o_total = 0
        suf_cnt = Counter()
        for r in recs:
            for w in r['words']:
                if w.startswith('o') and not w.startswith('ol') and not w.startswith('or'):
                    o_total += 1
                    suf = get_suffix(w)
                    if suf:
                        suf_cnt[suf] += 1
        print(f"\n{label} o-onset (n={o_total}):")
        for suf, cnt in suf_cnt.most_common(8):
            print(f"  -{suf}: {cnt} ({cnt/max(o_total,1):.1%})")

    o_suffix_dist(aiin_recs, "Aiin-dom")
    o_suffix_dist(y_recs, "Y-dom")


# ============================================================
# H130: B Paragraph Structure Parsability
# ============================================================

def h130_b_para_parsability(b_recs):
    print("\n=== H130: B Paragraph Structure Parsability ===")

    labeled = classify_para_boundary(b_recs)

    # For each line, code:
    # - first_word_p: first word is p-onset?
    # - last_word_am: last word ends in -am?
    # - last_word_o: last word is o-onset?
    # - last_word_edy: last word ends in -edy or -eedy?
    # - is_para_start: this line is a para-start (ground truth)
    # Prediction: predict next line is para-start if this line's last word is o-onset

    # Build line-level features
    lines = []
    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        first = ws[0]
        last = ws[-1]
        lines.append({
            'is_para_start': r['is_para_start'],
            'is_para_final_line': is_pf,
            'first_p': onset_class(first) == 'p',
            'last_am': last.endswith('am'),
            'last_o': onset_class(last) == 'o',
            'last_d': onset_class(last) == 'd',
            'last_edy': last.endswith('edy') or last.endswith('eedy'),
            'last_word': last,
            'first_word': first,
        })

    n = len(lines)
    print(f"\nTotal B lines: {n}")

    # Ground truth stats
    n_para_start = sum(1 for l in lines if l['is_para_start'])
    n_para_final = sum(1 for l in lines if l['is_para_final_line'])
    print(f"Para-starts: {n_para_start} ({n_para_start/n:.1%})")
    print(f"Para-final lines: {n_para_final} ({n_para_final/n:.1%})")

    # Feature rates
    n_first_p = sum(1 for l in lines if l['first_p'])
    n_last_am = sum(1 for l in lines if l['last_am'])
    n_last_o = sum(1 for l in lines if l['last_o'])
    n_last_d = sum(1 for l in lines if l['last_d'])
    n_last_edy = sum(1 for l in lines if l['last_edy'])
    print(f"\nLine features:")
    print(f"  first-word p-onset: {n_first_p} ({n_first_p/n:.1%})")
    print(f"  last-word -am: {n_last_am} ({n_last_am/n:.1%})")
    print(f"  last-word o-onset: {n_last_o} ({n_last_o/n:.1%})")
    print(f"  last-word d-onset: {n_last_d} ({n_last_d/n:.1%})")
    print(f"  last-word -edy/-eedy: {n_last_edy} ({n_last_edy/n:.1%})")

    # How well do features predict para-start for THIS line?
    print(f"\n--- Feature rates CONDITIONAL on para-start/non-para-start ---")
    for feat, name in [('first_p', 'first-word p-onset'),
                        ('last_am', 'last-word -am'),
                        ('last_o', 'last-word o-onset'),
                        ('last_d', 'last-word d-onset')]:
        n_feat_ps = sum(1 for l in lines if l['is_para_start'] and l[feat])
        n_feat_nps = sum(1 for l in lines if not l['is_para_start'] and l[feat])
        n_ps = n_para_start
        n_nps = n - n_para_start
        rate_ps = n_feat_ps / max(n_ps, 1)
        rate_nps = n_feat_nps / max(n_nps, 1)
        print(f"  {name}: para-start={rate_ps:.1%}, non-para-start={rate_nps:.1%}, enrichment={rate_ps/max(rate_nps,0.001):.2f}×")

    # How well does previous-line's last_o predict NEXT line's para_start?
    print(f"\n--- Using previous line's features to predict next-line para-start ---")
    print("(Predicting: will the NEXT line be a para-start?)")
    # para-final lines should have last word o-onset
    for feat, name in [('last_o', 'last-word o-onset'),
                        ('last_am', 'last-word -am'),
                        ('last_d', 'last-word d-onset'),
                        ('last_edy', 'last-word -edy')]:
        n_feat_pf = sum(1 for l in lines if l['is_para_final_line'] and l[feat])
        n_feat_npf = sum(1 for l in lines if not l['is_para_final_line'] and l[feat])
        n_pf = n_para_final
        n_npf = n - n_para_final
        rate_pf = n_feat_pf / max(n_pf, 1)
        rate_npf = n_feat_npf / max(n_npf, 1)
        enr = rate_pf / max(rate_npf, 0.001)
        print(f"  {name}: para-final line={rate_pf:.1%}, within-para={rate_npf:.1%}, enrichment={enr:.2f}×")

    # Simple classifier: predict para-final if last word is o-onset
    # Precision = P(actually para-final | predicted para-final)
    # Recall = P(predicted para-final | actually para-final)
    print(f"\n--- Precision/Recall for para-final prediction ---")
    for feat, name in [('last_o', 'last-word o-onset'),
                        ('last_d', 'last-word d-onset')]:
        tp = sum(1 for l in lines if l['is_para_final_line'] and l[feat])
        fp = sum(1 for l in lines if not l['is_para_final_line'] and l[feat])
        fn = sum(1 for l in lines if l['is_para_final_line'] and not l[feat])
        tn = sum(1 for l in lines if not l['is_para_final_line'] and not l[feat])
        prec = tp / max(tp + fp, 1)
        rec = tp / max(tp + fn, 1)
        f1 = 2*prec*rec / max(prec+rec, 0.001)
        print(f"  {name}: TP={tp}, FP={fp}, FN={fn} | Precision={prec:.1%}, Recall={rec:.1%}, F1={f1:.1%}")

    # Breakdown: what fraction of para-final lines DON'T have o-onset last word?
    para_final_lines = [l for l in lines if l['is_para_final_line']]
    last_onset_dist = Counter(onset_class(l['last_word']) for l in para_final_lines)
    print(f"\n--- Last-word onset distribution for para-final lines (n={len(para_final_lines)}) ---")
    for oc, cnt in last_onset_dist.most_common():
        print(f"  {oc}: {cnt} ({cnt/max(len(para_final_lines),1):.1%})")

    # Breakdown: what fraction of para-start lines DON'T have p-onset first word?
    para_start_lines = [l for l in lines if l['is_para_start']]
    first_onset_dist = Counter(onset_class(l['first_word']) for l in para_start_lines)
    print(f"\n--- First-word onset distribution for para-start lines (n={len(para_start_lines)}) ---")
    for oc, cnt in first_onset_dist.most_common():
        print(f"  {oc}: {cnt} ({cnt/max(len(para_start_lines),1):.1%})")

    # -am in context: within-para vs para-final
    print(f"\n--- -am last word: within-para vs para-final ---")
    am_within = sum(1 for l in lines if not l['is_para_final_line'] and l['last_am'])
    am_para = sum(1 for l in lines if l['is_para_final_line'] and l['last_am'])
    within_total = sum(1 for l in lines if not l['is_para_final_line'])
    para_total = len(para_final_lines)
    print(f"  Within-para lines with -am last: {am_within}/{within_total} = {am_within/max(within_total,1):.1%}")
    print(f"  Para-final lines with -am last: {am_para}/{para_total} = {am_para/max(para_total,1):.1%}")

    # Tripartite breakdown: how often does the full pattern hold?
    # Pattern: [p-onset para-start] -> [...] -> [-am within-para line-end] -> [...] -> [o-onset para-final]
    # Check: what % of para-final lines have o-onset last word?
    # What % of within-para line-finals have -am last word?
    # What % of para-starts have p-onset first word?
    pf_o_rate = sum(1 for l in para_final_lines if l['last_o']) / max(len(para_final_lines), 1)
    within_am_rate = am_within / max(within_total, 1)
    ps_p_rate = sum(1 for l in para_start_lines if l['first_p']) / max(len(para_start_lines), 1)
    print(f"\n--- Tripartite grammar compliance ---")
    print(f"  Para-final last-word is o-onset: {pf_o_rate:.1%}")
    print(f"  Within-para last-word is -am: {within_am_rate:.1%}")
    print(f"  Para-start first-word is p-onset: {ps_p_rate:.1%}")


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
    print(f"Pharma A: {len(a_recs)-len(herbal_recs)} recs from {len(pharma_folios)} folios")

    # H129
    h129_she_following_in_registers(aiin_recs, y_recs, b_recs)

    # H128
    h128_ol_or_paradigm(aiin_recs, y_recs)

    # H130
    h130_b_para_parsability(b_recs)

if __name__ == '__main__':
    main()
