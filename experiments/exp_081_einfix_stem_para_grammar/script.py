"""
exp_081: e-Infix Stem Class Analysis (H123), B Para-Final Suffix Paradigm (H124),
         Aiin-Dom vs Y-Dom Full Grammar Comparison (H125)

H123: Is the e-infix a productive morphological operation (same stem appears with/without e)
      or a stem class marker (distinct stems appear in e vs non-e contexts)?
H124: What suffix paradigm do B para-final words use? Is there a morphological contrast
      between within-para line-final and para-final words?
H125: Does the grammar-morphology dissociation extend to aiin-dom vs y-dom Herbal A?
"""

import re
import sys
import math
from collections import defaultdict, Counter

DATA_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

AIIN_DOM_FOLIOS = {
    'f1r','f1v','f2r','f2v','f3r','f3v','f4r','f4v','f5r','f5v',
    'f6r','f6v','f7r','f7v','f8r','f8v','f13r','f13v','f14r','f14v',
    'f15r','f15v','f16r','f16v'
}

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
    'eedy','edy','eey','edy','ain','aiin','ol','or','ey','dy','am','al','y'
]

def get_suffix(word):
    for suf in KNOWN_SUFFIXES:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def get_stem_info(word):
    """
    Returns (onset, has_e_infix, stem_core, suffix) for a word.
    stem_core is the part between onset(+e) and suffix.
    """
    suf = get_suffix(word)
    if suf is None:
        return None

    # Determine onset and e-infix
    if word.startswith('she') and len(word) > 3:
        onset, has_e = 'sh', True
        after_onset = word[3:]  # after 'she'
    elif word.startswith('sh') and len(word) > 2:
        onset, has_e = 'sh', False
        after_onset = word[2:]  # after 'sh'
    elif word.startswith('che') and len(word) > 3:
        onset, has_e = 'ch', True
        after_onset = word[3:]
    elif word.startswith('ch') and len(word) > 2:
        onset, has_e = 'ch', False
        after_onset = word[2:]
    elif word.startswith('ke') and len(word) > 2:
        onset, has_e = 'k', True
        after_onset = word[2:]
    elif word.startswith('k') and len(word) > 1:
        onset, has_e = 'k', False
        after_onset = word[1:]
    elif word.startswith('oe') and len(word) > 2:
        onset, has_e = 'o', True
        after_onset = word[2:]
    elif word.startswith('o') and len(word) > 1:
        onset, has_e = 'o', False
        after_onset = word[1:]
    else:
        return None

    # stem_core = after removing suffix from after_onset
    if after_onset.endswith(suf):
        stem_core = after_onset[:-len(suf)]
    else:
        return None

    return (onset, has_e, stem_core, suf)

def is_e_suffix(suf):
    return suf in ('edy','eedy','ey','eey')

def is_e_infix_word(word):
    for prefix in ('she','che','ke','oe','qoe'):
        if word.startswith(prefix) and len(word) > len(prefix):
            return True
    return False

def bigram_ppl_reduction(recs):
    """Compute bigram vs unigram PPL reduction."""
    words = [w for r in recs for w in r['words']]
    unigram_counts = Counter(words)
    total = len(words)
    if total == 0:
        return 0.0

    # Onset class unigram distribution
    onset_counts = Counter(onset_class(w) for w in words)
    onset_total = sum(onset_counts.values())

    # Bigram onset-class transitions
    bigrams = []
    for r in recs:
        ws = r['words']
        for i in range(len(ws)-1):
            bigrams.append((onset_class(ws[i]), onset_class(ws[i+1])))
    if not bigrams:
        return 0.0

    bigram_counts = Counter(bigrams)
    context_counts = Counter(b[0] for b in bigrams)
    classes = list(onset_counts.keys())
    n_classes = len(classes)

    def unigram_log2(cls):
        c = onset_counts.get(cls, 0)
        return math.log2((c + 1) / (onset_total + n_classes))

    def bigram_log2(ctx, tgt):
        c = bigram_counts.get((ctx, tgt), 0)
        ctx_c = context_counts.get(ctx, 0)
        return math.log2((c + 1) / (ctx_c + n_classes))

    uni_lp = sum(unigram_log2(onset_class(ws[i+1]))
                 for r in recs for ws in [r['words']]
                 for i in range(len(ws)-1)) / max(len(bigrams),1)
    bi_lp = sum(bigram_log2(onset_class(ws[i]), onset_class(ws[i+1]))
                for r in recs for ws in [r['words']]
                for i in range(len(ws)-1)) / max(len(bigrams),1)

    # PPL = 2^(-avg_log2_prob); reduction = (uni_ppl - bi_ppl) / uni_ppl
    uni_ppl = 2**(-uni_lp)
    bi_ppl = 2**(-bi_lp)
    return (uni_ppl - bi_ppl) / uni_ppl if uni_ppl > 0 else 0.0

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
            is_line_first = locus_code.lstrip('+*@=/~&').endswith('.1') or '.1,' in locus_code
            records.append({
                'folio': folio,
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start,
                'is_line_first': is_line_first,
            })
    return records

def assign_dialect(recs):
    # Assign A or B by checking -edy rate per folio
    folio_words = defaultdict(list)
    for r in recs:
        for w in r['words']:
            folio_words[r['folio']].append(w)

    b_folios = set()
    for folio, ws in folio_words.items():
        edy_count = sum(1 for w in ws if w.endswith('edy') or w.endswith('eedy'))
        if edy_count / max(len(ws), 1) >= 0.05:
            b_folios.add(folio)

    a_recs, b_recs = [], []
    for r in recs:
        if r['folio'] in b_folios:
            b_recs.append(r)
        else:
            a_recs.append(r)
    return a_recs, b_recs

def folio_base(folio):
    """Strip the .N suffix from folio names like f1r.3 -> f1r."""
    return folio.split('.')[0]

def pharma_a_folios(a_recs):
    """Identify Pharma A folios by -ol suffix rate (>15%). Returns base folio names."""
    folio_words = defaultdict(list)
    for r in a_recs:
        for w in r['words']:
            folio_words[folio_base(r['folio'])].append(w)

    pharma_folios = set()
    for folio, ws in folio_words.items():
        ol_rate = sum(1 for w in ws if w.endswith('ol')) / max(len(ws), 1)
        if ol_rate >= 0.15 and folio not in AIIN_DOM_FOLIOS:
            pharma_folios.add(folio)
    return pharma_folios

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


# ============================================================
# H123: e-Infix Stem Class Analysis
# ============================================================

def h123_einfix_stem_class(recs, dialect_name):
    """
    For each onset class (sh, ch, k, o):
    - Extract (onset, has_e, stem_core, suffix) for all matching words
    - Find stems that appear in BOTH e-infix and non-e-infix contexts
    - Find stems that appear ONLY in e-infix contexts or ONLY in non-e contexts
    - Compute: what fraction of stems are "pure e" vs "pure non-e" vs "shared"?
    """
    print(f"\n=== H123: e-Infix Stem Class Analysis ({dialect_name}) ===")

    # Collect all stem info
    # stem_data: onset -> {'e': {stem_core: [suffixes]}, 'non-e': {stem_core: [suffixes]}}
    stem_data = defaultdict(lambda: {'e': defaultdict(list), 'non-e': defaultdict(list)})

    word_counts = Counter()
    for r in recs:
        for w in r['words']:
            word_counts[w] += 1

    for word, cnt in word_counts.items():
        info = get_stem_info(word)
        if info is None:
            continue
        onset, has_e, stem_core, suf = info
        if stem_core == '':
            continue  # No stem between onset and suffix
        key = 'e' if has_e else 'non-e'
        for _ in range(cnt):
            stem_data[onset][key][stem_core].append(suf)

    for onset in ['sh', 'ch', 'k', 'o']:
        e_stems = set(stem_data[onset]['e'].keys())
        ne_stems = set(stem_data[onset]['non-e'].keys())
        shared = e_stems & ne_stems
        only_e = e_stems - ne_stems
        only_ne = ne_stems - e_stems

        e_tokens = sum(len(v) for v in stem_data[onset]['e'].values())
        ne_tokens = sum(len(v) for v in stem_data[onset]['non-e'].values())

        print(f"\n{onset}-onset (e: {len(e_stems)} stems/{e_tokens} tok; non-e: {len(ne_stems)} stems/{ne_tokens} tok):")
        print(f"  Shared stems (appear in both): {len(shared)} ({100*len(shared)/max(len(e_stems|ne_stems),1):.0f}% of all stems)")
        print(f"  Only e-infix: {len(only_e)} stems")
        print(f"  Only non-e: {len(only_ne)} stems")

        if shared:
            print(f"  Top shared stems:")
            for stem in sorted(shared, key=lambda s: -len(stem_data[onset]['e'][s])-len(stem_data[onset]['non-e'][s]))[:5]:
                e_sufs = Counter(stem_data[onset]['e'][stem])
                ne_sufs = Counter(stem_data[onset]['non-e'][stem])
                print(f"    '{stem}': e-suffix={dict(e_sufs)}, non-e-suffix={dict(ne_sufs)}")

        # For shared stems, do they use complementary suffixes?
        if shared:
            e_suf_in_shared = []
            ne_suf_in_shared = []
            for stem in shared:
                e_suf_in_shared.extend(stem_data[onset]['e'][stem])
                ne_suf_in_shared.extend(stem_data[onset]['non-e'][stem])
            e_e_rate = sum(1 for s in e_suf_in_shared if is_e_suffix(s)) / max(len(e_suf_in_shared),1)
            ne_e_rate = sum(1 for s in ne_suf_in_shared if is_e_suffix(s)) / max(len(ne_suf_in_shared),1)
            print(f"  In shared stems — e-suffix rate: e-context={e_e_rate:.1%}, non-e-context={ne_e_rate:.1%}")

        # Top pure e-infix stems
        if only_e:
            top_e = sorted(only_e, key=lambda s: -len(stem_data[onset]['e'][s]))[:5]
            print(f"  Top pure e-infix stems: {[(s, Counter(stem_data[onset]['e'][s]).most_common(2)) for s in top_e]}")

    # Check if e-suffix rate differs between e-infix and non-e words overall
    print(f"\n--- Overall e-suffix rate by e-infix status ({dialect_name}) ---")
    for onset in ['sh', 'ch', 'k', 'o']:
        e_sufs = [s for stems in stem_data[onset]['e'].values() for s in stems]
        ne_sufs = [s for stems in stem_data[onset]['non-e'].values() for s in stems]
        e_e_rate = sum(1 for s in e_sufs if is_e_suffix(s)) / max(len(e_sufs),1)
        ne_e_rate = sum(1 for s in ne_sufs if is_e_suffix(s)) / max(len(ne_sufs),1)
        print(f"  {onset}: e-infix → {e_e_rate:.1%} e-suffix ({len(e_sufs)} tok); non-e → {ne_e_rate:.1%} e-suffix ({len(ne_sufs)} tok)")


# ============================================================
# H124: B Para-Final vs Line-Final Suffix Paradigm
# ============================================================

def h124_para_final_suffix(b_recs):
    """
    Compare suffix distribution of:
    1. B para-final last words
    2. B within-para line-final last words
    3. B general words
    """
    print(f"\n=== H124: B Para-Final Suffix Paradigm ===")

    labeled = classify_para_boundary(b_recs)

    para_final_last = []
    within_para_final_last = []
    all_words = []

    for r, is_pf in labeled:
        ws = r['words']
        if not ws:
            continue
        last = ws[-1]
        all_words.extend(ws)
        if is_pf:
            para_final_last.append(last)
        else:
            within_para_final_last.append(last)

    def suffix_profile(words, label, n_top=8):
        suf_counts = Counter()
        total = 0
        for w in words:
            suf = get_suffix(w)
            if suf:
                suf_counts[suf] += 1
            total += 1
        print(f"\n{label} (n={total} words):")
        for suf, cnt in suf_counts.most_common(n_top):
            rate = cnt / total
            print(f"  -{suf}: {cnt} ({rate:.1%})")
        # -am rate specifically
        am_cnt = suf_counts.get('am', 0)
        print(f"  -am specifically: {am_cnt} ({am_cnt/max(total,1):.1%})")

    suffix_profile(para_final_last, "B para-final last words")
    suffix_profile(within_para_final_last, "B within-para line-final last words")
    suffix_profile(all_words, "B all words")

    # Onset + suffix combination at para-final
    print(f"\n--- Onset + Suffix at B para-final (top combinations) ---")
    onset_suf = Counter()
    for w in para_final_last:
        oc = onset_class(w)
        suf = get_suffix(w)
        if suf:
            onset_suf[(oc, suf)] += 1
    for (oc, suf), cnt in onset_suf.most_common(10):
        print(f"  {oc}+{suf}: {cnt}")

    # Am at para-final vs within-para for B
    pf_am = sum(1 for w in para_final_last if w.endswith('am'))
    wp_am = sum(1 for w in within_para_final_last if w.endswith('am'))
    pf_total = len(para_final_last)
    wp_total = len(within_para_final_last)
    print(f"\n-am at B para-final: {pf_am}/{pf_total} = {pf_am/max(pf_total,1):.1%}")
    print(f"-am at B within-para line-final: {wp_am}/{wp_total} = {wp_am/max(wp_total,1):.1%}")

    # What are the top B para-final words with onset?
    print(f"\n--- Top B para-final last words ---")
    pf_word_counts = Counter(para_final_last)
    for w, cnt in pf_word_counts.most_common(15):
        print(f"  {w} ({onset_class(w)}-onset, -{get_suffix(w)}): {cnt}")


# ============================================================
# H125: Aiin-Dom vs Y-Dom Full Grammar Comparison
# ============================================================

def h125_register_grammar_dissociation(a_recs, pharma_folios):
    """
    Full onset-class transition matrix for aiin-dom vs y-dom Herbal A.
    Compare their suffix paradigms to check if grammar and morphology dissociate.
    """
    print(f"\n=== H125: Aiin-Dom vs Y-Dom Grammar-Morphology Dissociation ===")

    # Exclude Pharma A folios
    pharma_bases = {folio_base(f) for f in pharma_folios}
    herbal_recs = [r for r in a_recs if folio_base(r['folio']) not in pharma_bases]
    aiin_recs = [r for r in herbal_recs if folio_base(r['folio']) in AIIN_DOM_FOLIOS]
    y_recs = [r for r in herbal_recs if folio_base(r['folio']) not in AIIN_DOM_FOLIOS]

    print(f"Herbal A: {len(herbal_recs)} recs | Aiin-dom: {len(aiin_recs)} recs | Y-dom: {len(y_recs)} recs")

    # --- Onset-class transition matrices ---
    def build_transition_matrix(recs):
        bigrams = Counter()
        context_counts = Counter()
        for r in recs:
            ws = r['words']
            for i in range(len(ws)-1):
                oc1, oc2 = onset_class(ws[i]), onset_class(ws[i+1])
                bigrams[(oc1, oc2)] += 1
                context_counts[oc1] += 1
        return bigrams, context_counts

    aiin_bg, aiin_ctx = build_transition_matrix(aiin_recs)
    y_bg, y_ctx = build_transition_matrix(y_recs)

    classes = ['qo','ch','sh','p','t','k','d','s','y','o','other']

    # Key transitions to examine
    key_transitions = [
        ('sh','qo'), ('sh','ch'), ('ch','ch'), ('qo','ch'),
        ('d','qo'), ('s','ch'), ('k','ch'), ('o','qo')
    ]

    def enrichment(bigrams, ctx_counts, ctx, tgt, all_words_list):
        """Compute enrichment = P(tgt|ctx) / P(tgt_base)"""
        total = sum(ctx_counts.values())
        tgt_base = sum(bigrams.get((c, tgt), 0) for c in classes) / max(total, 1)
        ctx_c = ctx_counts.get(ctx, 0)
        cond = bigrams.get((ctx, tgt), 0) / max(ctx_c, 1)
        if tgt_base == 0:
            return float('inf') if cond > 0 else 1.0
        return cond / tgt_base

    print(f"\n--- Key transition enrichments ---")
    print(f"{'Transition':<15} {'Aiin-dom':>12} {'Y-dom':>12} {'Ratio A/Y':>12}")
    for ctx, tgt in key_transitions:
        aiin_enr = enrichment(aiin_bg, aiin_ctx, ctx, tgt, [])
        y_enr = enrichment(y_bg, y_ctx, ctx, tgt, [])
        ratio = aiin_enr / max(y_enr, 0.01)
        print(f"  {ctx}→{tgt:<10} {aiin_enr:>10.2f}× {y_enr:>10.2f}× {ratio:>10.2f}")

    # --- Suffix paradigm comparison ---
    def suffix_dist(recs):
        suf_counts = Counter()
        total = 0
        for r in recs:
            for w in r['words']:
                suf = get_suffix(w)
                if suf:
                    suf_counts[suf] += 1
                total += 1
        return suf_counts, total

    aiin_suf, aiin_total = suffix_dist(aiin_recs)
    y_suf, y_total = suffix_dist(y_recs)

    print(f"\n--- Suffix paradigm comparison ---")
    all_sufs = set(aiin_suf.keys()) | set(y_suf.keys())
    key_sufs = ['aiin','ol','or','edy','eedy','ey','eey','dy','am','y']
    print(f"{'Suffix':<10} {'Aiin-dom':>12} {'Y-dom':>12}")
    for suf in key_sufs:
        a_rate = aiin_suf.get(suf, 0) / max(aiin_total, 1)
        y_rate = y_suf.get(suf, 0) / max(y_total, 1)
        print(f"  -{suf:<8} {a_rate:>10.2%} {y_rate:>10.2%}")

    # --- Bigram PPL reduction ---
    aiin_ppl = bigram_ppl_reduction(aiin_recs)
    y_ppl = bigram_ppl_reduction(y_recs)
    print(f"\nBigram PPL reduction: Aiin-dom={aiin_ppl:.1%}, Y-dom={y_ppl:.1%}")

    # --- daiin rate and positional behavior ---
    def daiin_stats(recs, label):
        total_words = 0
        daiin_count = 0
        daiin_line_final = 0
        total_line_final = 0
        for r in recs:
            ws = r['words']
            total_words += len(ws)
            if ws:
                if ws[-1] == 'daiin':
                    daiin_line_final += 1
                total_line_final += 1
            daiin_count += ws.count('daiin')
        rate = daiin_count / max(total_words, 1)
        lf_rate = daiin_line_final / max(total_line_final, 1)
        print(f"\n{label}: daiin rate={rate:.2%}, daiin line-final rate={lf_rate:.2%}")

    daiin_stats(aiin_recs, "Aiin-dom")
    daiin_stats(y_recs, "Y-dom")

    # --- e-infix rate comparison (as measure of e-morphology) ---
    def einfix_rate(recs):
        total = 0
        e_count = 0
        for r in recs:
            for w in r['words']:
                total += 1
                if is_e_infix_word(w):
                    e_count += 1
        return e_count / max(total, 1)

    aiin_einfix = einfix_rate(aiin_recs)
    y_einfix = einfix_rate(y_recs)
    print(f"\ne-infix word rate: Aiin-dom={aiin_einfix:.2%}, Y-dom={y_einfix:.2%}")

    # --- sh→qo specifically, and whether she-→qo drives it ---
    def she_qo_rate(recs):
        she_total, she_qo = 0, 0
        sh_total, sh_qo = 0, 0
        for r in recs:
            ws = r['words']
            for i in range(len(ws)-1):
                oc_next = onset_class(ws[i+1])
                if ws[i].startswith('she') and len(ws[i]) > 3:
                    she_total += 1
                    if oc_next == 'qo': she_qo += 1
                elif ws[i].startswith('sh') and len(ws[i]) > 2:
                    sh_total += 1
                    if oc_next == 'qo': sh_qo += 1
        return (she_qo/max(she_total,1), she_total, sh_qo/max(sh_total,1), sh_total)

    aiin_she_qo = she_qo_rate(aiin_recs)
    y_she_qo = she_qo_rate(y_recs)
    # Base qo rate
    def qo_base(recs):
        all_onsets = [onset_class(w) for r in recs for w in r['words']]
        return all_onsets.count('qo') / max(len(all_onsets), 1)

    aiin_qo_base = qo_base(aiin_recs)
    y_qo_base = qo_base(y_recs)

    print(f"\n--- sh/she- → qo rates ---")
    print(f"Aiin-dom: she-→qo={aiin_she_qo[0]:.1%} (n={aiin_she_qo[1]}), sh-other→qo={aiin_she_qo[2]:.1%} (n={aiin_she_qo[3]}), base qo={aiin_qo_base:.1%}")
    print(f"  Enrichments: she-→qo={aiin_she_qo[0]/max(aiin_qo_base,0.001):.2f}×, sh-other→qo={aiin_she_qo[2]/max(aiin_qo_base,0.001):.2f}×")
    print(f"Y-dom:    she-→qo={y_she_qo[0]:.1%} (n={y_she_qo[1]}), sh-other→qo={y_she_qo[2]:.1%} (n={y_she_qo[3]}), base qo={y_qo_base:.1%}")
    print(f"  Enrichments: she-→qo={y_she_qo[0]/max(y_qo_base,0.001):.2f}×, sh-other→qo={y_she_qo[2]/max(y_qo_base,0.001):.2f}×")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Loading data...")
    recs = parse_voynich(DATA_PATH)
    print(f"Total body records: {len(recs)}")

    a_recs, b_recs = assign_dialect(recs)
    pharma_folios = pharma_a_folios(a_recs)

    print(f"A records: {len(a_recs)}, B records: {len(b_recs)}")
    print(f"Pharma A folios: {len(pharma_folios)} ({sorted(pharma_folios)[:5]}...)")

    # H123: e-infix stem class analysis in both dialects
    h123_einfix_stem_class(b_recs, "Currier B")
    h123_einfix_stem_class(a_recs, "Currier A")

    # H124: B para-final suffix paradigm
    h124_para_final_suffix(b_recs)

    # H125: Aiin-dom vs Y-dom grammar comparison
    h125_register_grammar_dissociation(a_recs, pharma_folios)

if __name__ == '__main__':
    main()
