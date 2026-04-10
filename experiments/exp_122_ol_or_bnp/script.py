#!/usr/bin/env python3
"""
exp_122: -ol vs -or Suffix Bigram Contexts (H240) + B-Dialect NP Template (H241)
H240: Are -ol and -or suffix words context-distinguishable? chol→daiin vs chor→cth directly
H241: B-dialect NP template — what precedes otaiin? [W1][otaiin][ot-word] in stars?
"""
import re
import math
from collections import defaultdict, Counter

DATA = 'data/transcriptions/eva_zl3b.txt'

SECTION_MAP = {}
for f in range(1, 58): SECTION_MAP[f] = 'herbal'
for f in range(67, 74): SECTION_MAP[f] = 'astro'
for f in range(75, 85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103, 117): SECTION_MAP[f] = 'stars'

SUFFIX_LIST = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am','ol','or','ar','al','ey','dy','y']

def get_suffix(word):
    for s in SUFFIX_LIST:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

def get_onset(word):
    for o in ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s']:
        if word.startswith(o):
            return o
    return 'other'

def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)

def parse_eva(path):
    edy_counts = defaultdict(int)
    total_counts = defaultdict(int)
    records = []
    line_records = defaultdict(list)

    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or not line.startswith('<'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m: continue
            locus_code = m.group(1)
            text = m.group(2).strip()

            comma_idx = locus_code.find(',')
            if comma_idx < 0: continue
            folio_line = locus_code[:comma_idx]
            locus_type = locus_code[comma_idx+1:]

            fm = re.match(r'f(\d+)', folio_line)
            if not fm: continue
            folio_num = int(fm.group(1))

            lm = re.match(r'f\w+\.(\d+)', folio_line)
            line_in_folio = int(lm.group(1)) if lm else 0

            prefix_chars = set('@+*=~&')
            prefix = ''
            for c in locus_type:
                if c in prefix_chars: prefix += c
                else: break
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            if not is_body: continue

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda mm: mm.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            n = len(words)
            for i, w in enumerate(words):
                for suf_check in ['edy', 'eedy']:
                    if w.endswith(suf_check):
                        edy_counts[folio_num] += 1
                total_counts[folio_num] += 1
                records.append({
                    'word': w, 'folio': folio_num,
                    'line': line_in_folio,
                    'pos_in_line': i,
                    'n_in_line': n,
                    'is_line_first': (i == 0),
                    'is_line_last': (i == n-1),
                    'prev_word': words[i-1] if i > 0 else None,
                    'next_word': words[i+1] if i < n-1 else None,
                    'section': SECTION_MAP.get(folio_num, 'other'),
                    'line_words': words,
                })
            line_records[(folio_num, line_in_folio)] = words

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map, line_records


def bigram_enrich(recs_with_next, target_onsets, baseline_total, baseline_onsets):
    """Given records and baseline, compute enrichment for each target onset."""
    n = len(recs_with_next)
    next_onset_cnt = Counter(get_onset(r['next_word']) for r in recs_with_next if r['next_word'])
    result = {}
    for onset in target_onsets:
        obs = next_onset_cnt.get(onset, 0) / max(n, 1)
        base = baseline_onsets.get(onset, 0) / max(baseline_total, 1)
        enr = obs / base if base > 0 else float('inf')
        result[onset] = (next_onset_cnt.get(onset, 0), obs, base, enr)
    return result


# ─────────────────────────── H240 ───────────────────────────
def h240_ol_vs_or(records, dialect_map):
    print("\n" + "="*60)
    print("H240: -ol vs -or SUFFIX BIGRAM CONTEXTS")
    print("="*60)

    a_records = [r for r in records if r['dialect'] == 'A']
    b_records = [r for r in records if r['dialect'] == 'B']

    # Full corpus baseline
    all_next_onset = Counter(get_onset(r['next_word']) for r in records if r['next_word'])
    all_total = sum(all_next_onset.values())

    target_onsets = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','other']

    for dialect_label, recs in [('A-dialect', a_records), ('B-dialect', b_records), ('All', records)]:
        # Baseline within dialect
        d_next = Counter(get_onset(r['next_word']) for r in recs if r['next_word'])
        d_total = sum(d_next.values())

        print(f"\n{'='*40}")
        print(f"--- {dialect_label} -ol vs -or Suffix Bigram ---")
        print(f"{'='*40}")

        for suffix_filter in ['ol', 'or']:
            # Words ending in -ol or -or (with onset prefix)
            suffix_recs = [r for r in recs if get_suffix(r['word']) == suffix_filter and r['next_word']]
            n = len(suffix_recs)
            if n == 0:
                print(f"  {suffix_filter}: no records")
                continue

            next_onset_cnt = Counter(get_onset(r['next_word']) for r in suffix_recs)
            H = shannon_entropy(next_onset_cnt)

            print(f"\n  -{suffix_filter} words (n={n}, H_next={H:.3f})")
            top_words = Counter(r['word'] for r in suffix_recs).most_common(5)
            print(f"  Top words: {', '.join(f'{w}({c})' for w,c in top_words)}")
            print(f"  {'Onset':8s} | {'n':>5} | {'obs':>6} | {'base':>6} | {'enr':>6}")
            for onset in target_onsets:
                obs_cnt = next_onset_cnt.get(onset, 0)
                obs_rate = obs_cnt / n
                base_rate = d_next.get(onset, 0) / d_total if d_total else 0
                enr = obs_rate / base_rate if base_rate > 0 else float('inf')
                marker = '←' if enr >= 1.5 or enr <= 0.5 else ''
                print(f"  {onset:8s} | {obs_cnt:5d} | {obs_rate:6.3f} | {base_rate:6.3f} | {enr:6.2f}× {marker}")

        # Compare specific word pairs: chol vs chor, shol vs shor
        print(f"\n  --- Specific word comparisons in {dialect_label} ---")
        for w1, w2 in [('chol', 'chor'), ('shol', 'shor'), ('dol', 'dor'), ('ol', 'or')]:
            r1 = [r for r in recs if r['word'] == w1 and r['next_word']]
            r2 = [r for r in recs if r['word'] == w2 and r['next_word']]
            if not r1 and not r2: continue
            n1, n2 = len(r1), len(r2)
            next1 = Counter(get_onset(r['next_word']) for r in r1)
            next2 = Counter(get_onset(r['next_word']) for r in r2)
            print(f"\n  {w1}(n={n1}) vs {w2}(n={n2}):")
            for onset in ['cth','d','ch','sh','qok','other']:
                r1_rate = next1.get(onset,0)/max(n1,1)
                r2_rate = next2.get(onset,0)/max(n2,1)
                base = d_next.get(onset,0)/max(d_total,1)
                print(f"    {onset:8s}: {w1}={r1_rate:.3f}({next1.get(onset,0)}) "
                      f"[enr={r1_rate/base:.2f}×] | {w2}={r2_rate:.3f}({next2.get(onset,0)}) "
                      f"[enr={r2_rate/base:.2f}×]")

    # Suffix-level bigram: for EACH suffix, what onset follows?
    print(f"\n\n--- Full suffix→next-onset enrichment table (A-dialect) ---")
    a_recs = [r for r in records if r['dialect'] == 'A' and r['next_word']]
    a_d_next = Counter(get_onset(r['next_word']) for r in a_recs)
    a_d_total = sum(a_d_next.values())

    key_suffixes = ['ol','or','y','ey','aiin','ain','al','ar','edy','eedy','eey','dy']
    key_onsets = ['cth','d','ch','sh','qok','ot','ok','other']

    header = f"{'Suffix':8s} | n      " + ' | '.join(f'{o:5s}' for o in key_onsets)
    print(f"  {header}")
    for suf in key_suffixes:
        suf_recs = [r for r in a_recs if get_suffix(r['word']) == suf]
        n = len(suf_recs)
        if n < 10: continue
        next_cnt = Counter(get_onset(r['next_word']) for r in suf_recs)
        vals = []
        for onset in key_onsets:
            obs = next_cnt.get(onset,0)/n
            base = a_d_next.get(onset,0)/a_d_total if a_d_total else 0
            enr = obs/base if base > 0 else 0
            vals.append(f'{enr:5.2f}')
        print(f"  {suf:8s} | {n:6d} " + ' | '.join(vals))

    # Positional: chol vs chor at first/mid/last
    print(f"\n--- chol vs chor positional distribution ---")
    for w in ['chol','chor','shol','shor']:
        w_recs = [r for r in records if r['word'] == w]
        n = len(w_recs)
        if n == 0: continue
        first = sum(1 for r in w_recs if r['is_line_first'])
        last = sum(1 for r in w_recs if r['is_line_last'])
        mid = n - first - last
        d = Counter(r['dialect'] for r in w_recs)
        print(f"  {w:8s}: n={n:4d} | first={first/n:.2f} mid={mid/n:.2f} last={last/n:.2f} | "
              f"A={d['A']} B={d['B']}")


# ─────────────────────────── H241 ───────────────────────────
def h241_b_np_template(records, dialect_map, line_records):
    print("\n" + "="*60)
    print("H241: B-DIALECT NP TEMPLATE")
    print("="*60)

    b_records = [r for r in records if r['dialect'] == 'B']
    b_folios = {fnum for fnum,d in dialect_map.items() if d == 'B'}
    stars_folios = {f for f in range(103, 117)}

    b_next = Counter(get_onset(r['next_word']) for r in b_records if r['next_word'])
    b_total = sum(b_next.values())

    # Test [W1][otaiin][ot-word] in B-dialect
    print(f"\n--- Trigrams [W1][otaiin][W3] in B-dialect ---")
    otaiin_trigrams = []
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in b_folios: continue
        for i in range(1, len(words)-1):
            if words[i] == 'otaiin':
                w1 = words[i-1]
                w3 = words[i+1]
                otaiin_trigrams.append({'w1': w1, 'w3': w3, 'folio': folio_num,
                                         'w3_onset': get_onset(w3), 'w1_onset': get_onset(w1)})

    print(f"  Total [W1][otaiin][W3] in B-dialect: {len(otaiin_trigrams)}")
    w3_onset_cnt = Counter(t['w3_onset'] for t in otaiin_trigrams)
    w1_onset_cnt = Counter(t['w1_onset'] for t in otaiin_trigrams)
    n = len(otaiin_trigrams)
    if n > 0:
        print(f"\n  W3 (after otaiin) onset enrichment vs B-baseline:")
        for onset, cnt in w3_onset_cnt.most_common(8):
            obs = cnt/n
            base = b_next.get(onset,0)/b_total if b_total else 0
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")

        print(f"\n  W1 (before otaiin) onset enrichment vs B-baseline:")
        b_onset_all = Counter(get_onset(r['word']) for r in b_records)
        b_word_total = sum(b_onset_all.values())
        for onset, cnt in w1_onset_cnt.most_common(8):
            obs = cnt/n
            base = b_onset_all.get(onset,0)/b_word_total if b_word_total else 0
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")

    # Stars-specific: what precedes otaiin in stars?
    print(f"\n--- In STARS: what precedes otaiin? ---")
    stars_pre_otaiin = []
    stars_post_otaiin = []
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in stars_folios: continue
        for i, w in enumerate(words):
            if w == 'otaiin':
                if i > 0:
                    stars_pre_otaiin.append(words[i-1])
                if i < len(words)-1:
                    stars_post_otaiin.append(words[i+1])
    stars_pre_onset = Counter(get_onset(w) for w in stars_pre_otaiin)
    stars_post_onset = Counter(get_onset(w) for w in stars_post_otaiin)
    stars_pre_words = Counter(stars_pre_otaiin)
    stars_post_words = Counter(stars_post_otaiin)
    n_pre = len(stars_pre_otaiin)
    n_post = len(stars_post_otaiin)
    stars_b_recs = [r for r in records if r['folio'] in stars_folios]
    stars_onset_all = Counter(get_onset(r['word']) for r in stars_b_recs)
    stars_total = sum(stars_onset_all.values())

    print(f"  Pre-otaiin tokens: {n_pre}")
    if n_pre > 0:
        print(f"  Pre-otaiin onset distribution:")
        for onset, cnt in stars_pre_onset.most_common(8):
            base = stars_onset_all.get(onset,0)/stars_total if stars_total else 0
            obs = cnt/n_pre
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
        print(f"  Top pre-otaiin words: {stars_pre_words.most_common(10)}")
    print(f"\n  Post-otaiin tokens: {n_post}")
    if n_post > 0:
        print(f"  Post-otaiin onset:")
        for onset, cnt in stars_post_onset.most_common(6):
            base = stars_onset_all.get(onset,0)/stars_total if stars_total else 0
            obs = cnt/n_post
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
        print(f"  Top post-otaiin words: {stars_post_words.most_common(10)}")

    # Test [W1][shedy][qok-word] in B
    print(f"\n--- Trigrams [W1][shedy][qok-word] in B-dialect ---")
    shedy_trig = []
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in b_folios: continue
        for i in range(1, len(words)-1):
            if words[i] == 'shedy' and get_onset(words[i+1]) == 'qok':
                shedy_trig.append({'w1': words[i-1], 'folio': folio_num})
    print(f"  [W1][shedy][qok] trigrams: {len(shedy_trig)}")
    if shedy_trig:
        w1_onset_cnt2 = Counter(get_onset(t['w1']) for t in shedy_trig)
        w1_words2 = Counter(t['w1'] for t in shedy_trig)
        b_onset_all = Counter(get_onset(r['word']) for r in b_records)
        b_word_total = sum(b_onset_all.values())
        for onset, cnt in w1_onset_cnt2.most_common(6):
            base = b_onset_all.get(onset,0)/b_word_total if b_word_total else 0
            obs = cnt/len(shedy_trig)
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
        print(f"  Top W1 words: {w1_words2.most_common(8)}")

    # General: what precedes shedy?
    print(f"\n--- General: what precedes shedy in B? ---")
    pre_shedy = [r['prev_word'] for r in b_records if r['word'] == 'shedy' and r['prev_word']]
    pre_shedy_onset = Counter(get_onset(w) for w in pre_shedy)
    pre_shedy_words = Counter(pre_shedy)
    n_ps = len(pre_shedy)
    b_onset_all = Counter(get_onset(r['word']) for r in b_records)
    b_word_total = sum(b_onset_all.values())
    print(f"  Pre-shedy tokens: {n_ps}")
    if n_ps > 0:
        for onset, cnt in pre_shedy_onset.most_common(8):
            base = b_onset_all.get(onset,0)/b_word_total if b_word_total else 0
            obs = cnt/n_ps
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
        print(f"  Top pre-shedy words: {pre_shedy_words.most_common(10)}")

    # Test: in B-dialect, does otaiin precede ot-words at line-boundaries?
    print(f"\n--- otaiin positional role in B-dialect (all B, not just stars) ---")
    b_otaiin_recs = [r for r in b_records if r['word'] == 'otaiin']
    n_ot = len(b_otaiin_recs)
    if n_ot > 0:
        first = sum(1 for r in b_otaiin_recs if r['is_line_first'])
        last = sum(1 for r in b_otaiin_recs if r['is_line_last'])
        mid = n_ot - first - last
        print(f"  otaiin in B: n={n_ot}, first={first/n_ot:.2f}, mid={mid/n_ot:.2f}, last={last/n_ot:.2f}")
        next_onset_b = Counter(get_onset(r['next_word']) for r in b_otaiin_recs if r['next_word'])
        nb = sum(next_onset_b.values())
        print(f"  B-dialect after-otaiin onset:")
        for onset, cnt in next_onset_b.most_common(6):
            base = b_next.get(onset,0)/b_total if b_total else 0
            obs = cnt/nb
            enr = obs/base if base > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")

    # Compare A-dialect daiin NP vs B-dialect otaiin NP (summary)
    print(f"\n--- Summary: A-daiin NP vs B-otaiin NP ---")
    a_daiin_recs = [r for r in records if r['dialect'] == 'A' and r['word'] == 'daiin' and r['next_word']]
    a_daiin_next = Counter(get_onset(r['next_word']) for r in a_daiin_recs)
    n_ad = len(a_daiin_recs)
    a_next = Counter(get_onset(r['next_word']) for r in records if r['dialect'] == 'A' and r['next_word'])
    a_total_n = sum(a_next.values())

    b_otaiin_next_recs = [r for r in records if r['dialect'] == 'B' and r['word'] == 'otaiin' and r['next_word']]
    b_otaiin_next = Counter(get_onset(r['next_word']) for r in b_otaiin_next_recs)
    n_bo = len(b_otaiin_next_recs)

    print(f"  A-daiin(n={n_ad}): post-onset distribution:")
    for onset in ['cth','ch','sh','d','qok','ot','ok','other']:
        ad_rate = a_daiin_next.get(onset,0)/max(n_ad,1)
        base = a_next.get(onset,0)/max(a_total_n,1)
        enr = ad_rate/base if base > 0 else 0
        bo_rate = b_otaiin_next.get(onset,0)/max(n_bo,1)
        bbase = b_next.get(onset,0)/max(b_total,1)
        benr = bo_rate/bbase if bbase > 0 else 0
        print(f"    {onset:8s}: A-daiin={ad_rate:.3f}(enr={enr:.2f}×) | B-otaiin={bo_rate:.3f}(enr={benr:.2f}×)")


def main():
    print("Loading records...")
    records, dialect_map, line_records = parse_eva(DATA)
    print(f"Total: {len(records)} records, {len(line_records)} lines")
    print(f"Dialects: A={sum(1 for d in dialect_map.values() if d=='A')}, "
          f"B={sum(1 for d in dialect_map.values() if d=='B')}")

    h240_ol_vs_or(records, dialect_map)
    h241_b_np_template(records, dialect_map, line_records)

if __name__ == '__main__':
    main()
