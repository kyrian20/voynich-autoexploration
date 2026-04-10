#!/usr/bin/env python3
"""
exp_124: l-Onset and k-Onset Prefix Class Characterization (H247 + H248)
H247: Is 'l' a B-dialect morphological prefix? l-stripped stem recovery, section/dialect distribution
H248: k-onset words — standalone class or l-stripped stems?
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


def h247_l_onset(records, dialect_map):
    print("\n" + "="*60)
    print("H247: l-ONSET PREFIX CLASS CHARACTERIZATION")
    print("="*60)

    # Build full vocabulary
    all_words = Counter(r['word'] for r in records)
    total_tokens = len(records)
    vocab = set(all_words.keys())

    # Extract all l-initial words (not starting with recognized onsets)
    l_recs = [r for r in records if r['word'].startswith('l') and len(r['word']) >= 3]
    l_words = Counter(r['word'] for r in l_recs)
    l_total = sum(l_words.values())

    print(f"\nTotal l-initial tokens: {l_total} ({l_total/total_tokens:.4f})")
    print(f"Total l-initial types: {len(l_words)}")

    # Top l-initial words
    print(f"\n--- Top l-initial words ---")
    for w, cnt in l_words.most_common(30):
        suf = get_suffix(w)
        # What's the stem after stripping 'l'?
        stem = w[1:]
        in_vocab = stem in vocab
        stem_onset = get_onset(stem)
        print(f"  {w:15s}: {cnt:4d}  suf={suf:6s}  stem='{stem}'  stem_in_vocab={in_vocab}  stem_onset={stem_onset}")

    # l-stripped stem recovery rate
    print(f"\n--- l-stripped stem analysis ---")
    # All l-initial words
    l_types_with_stem = [(w, w[1:]) for w in l_words if len(w[1:]) >= 2]
    n_with_stem_in_vocab = sum(1 for w, s in l_types_with_stem if s in vocab)
    total_l_types = len(l_types_with_stem)
    # Weighted by token count
    n_with_stem_tok = sum(l_words[w] for w, s in l_types_with_stem if s in vocab)
    print(f"  l-types tested: {total_l_types}")
    print(f"  l-stem in vocab (types): {n_with_stem_in_vocab}/{total_l_types} = {n_with_stem_in_vocab/total_l_types:.3f}")
    print(f"  l-stem in vocab (tokens): {n_with_stem_tok}/{l_total} = {n_with_stem_tok/l_total:.3f}")

    # Compare to qo-prefix recovery rate
    qo_recs = [r for r in records if r['word'].startswith('qo') and len(r['word']) > 2]
    qo_words = Counter(r['word'] for r in qo_recs)
    qo_types = [(w, w[2:]) for w in qo_words if len(w[2:]) >= 2]
    qo_in_vocab = sum(1 for w, s in qo_types if s in vocab)
    qo_total = len(qo_types)
    print(f"\n  qo-prefix recovery: {qo_in_vocab}/{qo_total} = {qo_in_vocab/qo_total:.3f} (benchmark)")
    # o-prefix recovery
    o_recs = [r for r in records if r['word'].startswith('o') and len(r['word']) > 1
              and not r['word'].startswith('ol') and not r['word'].startswith('ot')
              and not r['word'].startswith('ok')]
    o_words = Counter(r['word'] for r in o_recs)
    o_types = [(w, w[1:]) for w in o_words if len(w[1:]) >= 2]
    o_in_vocab = sum(1 for w, s in o_types if s in vocab)
    o_total = len(o_types)
    if o_total > 0:
        print(f"  o-prefix recovery: {o_in_vocab}/{o_total} = {o_in_vocab/o_total:.3f} (benchmark)")

    # Dialect and section distribution of l-initial words
    print(f"\n--- l-initial dialect distribution ---")
    l_by_dialect = Counter(r['dialect'] for r in l_recs)
    a_total = sum(1 for r in records if r['dialect'] == 'A')
    b_total = sum(1 for r in records if r['dialect'] == 'B')
    l_a_rate = l_by_dialect['A'] / a_total if a_total else 0
    l_b_rate = l_by_dialect['B'] / b_total if b_total else 0
    print(f"  A-dialect: {l_by_dialect['A']} ({l_a_rate:.4f}‰ * 1000 = {l_a_rate*1000:.2f}‰)")
    print(f"  B-dialect: {l_by_dialect['B']} ({l_b_rate:.4f}‰ * 1000 = {l_b_rate*1000:.2f}‰)")
    print(f"  A/B ratio: {l_a_rate/l_b_rate:.3f} (>1=A-dominant, <1=B-dominant)")

    print(f"\n--- l-initial section distribution ---")
    section_totals = Counter(r['section'] for r in records)
    l_by_section = Counter(r['section'] for r in l_recs)
    for sec in ['herbal','astro','cosmo','pharma','stars']:
        rate = l_by_section[sec] / section_totals[sec] if section_totals[sec] else 0
        overall = l_total / total_tokens
        enr = rate / overall if overall else 0
        print(f"  {sec:8s}: {l_by_section[sec]:4d}/{section_totals[sec]:5d} = {rate:.4f} (enr={enr:.2f}×)")

    # Suffix distribution of l-initial words
    print(f"\n--- l-initial suffix distribution ---")
    l_suffix = Counter(get_suffix(w) for w in l_words.elements())
    total_suffix = Counter(get_suffix(r['word']) for r in records)
    n_l = sum(l_suffix.values())
    n_all = sum(total_suffix.values())
    for suf, cnt in l_suffix.most_common(10):
        obs = cnt/n_l
        base = total_suffix[suf]/n_all if n_all else 0
        enr = obs/base if base else 0
        print(f"  {suf:8s}: {cnt:4d} ({obs:.3f} vs {base:.3f} base = {enr:.2f}×)")

    # What comes BEFORE l-initial words?
    print(f"\n--- What precedes l-initial words? (bigram context) ---")
    pre_l_onset = Counter(get_onset(r['prev_word']) for r in l_recs if r['prev_word'])
    post_l_onset = Counter(get_onset(r['next_word']) for r in l_recs if r['next_word'])
    all_onset_base = Counter(get_onset(r['word']) for r in records)
    all_n = sum(all_onset_base.values())
    n_pre = sum(pre_l_onset.values())
    n_post = sum(post_l_onset.values())
    print(f"  Pre-l onset:")
    for onset, cnt in pre_l_onset.most_common(8):
        obs = cnt/n_pre
        base = all_onset_base[onset]/all_n if all_n else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
    print(f"  Post-l onset:")
    for onset, cnt in post_l_onset.most_common(8):
        obs = cnt/n_post
        base = all_onset_base[onset]/all_n if all_n else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")

    # Positional distribution
    print(f"\n--- l-initial positional distribution ---")
    first = sum(1 for r in l_recs if r['is_line_first'])
    last = sum(1 for r in l_recs if r['is_line_last'])
    mid = l_total - first - last
    print(f"  first={first/l_total:.3f}, mid={mid/l_total:.3f}, last={last/l_total:.3f}")

    # Compare to qo-prefix positional distribution
    qo_recs_all = [r for r in records if r['word'].startswith('qo') and len(r['word']) > 2]
    qo_tot = len(qo_recs_all)
    first_q = sum(1 for r in qo_recs_all if r['is_line_first'])
    last_q = sum(1 for r in qo_recs_all if r['is_line_last'])
    mid_q = qo_tot - first_q - last_q
    print(f"  qo-prefix: first={first_q/qo_tot:.3f}, mid={mid_q/qo_tot:.3f}, last={last_q/qo_tot:.3f}")

    # Sub-analysis: lch- vs lsh- vs lk-
    print(f"\n--- l-initial sub-class analysis ---")
    for sub_prefix in ['lch', 'lsh', 'lk', 'lr', 'lq', 'lt', 'ld', 'lc']:
        sub_recs = [r for r in l_recs if r['word'].startswith(sub_prefix)]
        n = len(sub_recs)
        if n < 5: continue
        sub_words = Counter(r['word'] for r in sub_recs)
        # Stem after stripping 'l'
        stems = [(w, w[1:]) for w in sub_words]
        in_vocab_rate = sum(1 for w, s in stems if s in vocab) / len(stems) if stems else 0
        d_dist = Counter(r['dialect'] for r in sub_recs)
        sec_dist = Counter(r['section'] for r in sub_recs)
        a_rate = d_dist['A'] / (d_dist['A'] + d_dist['B']) if (d_dist['A'] + d_dist['B']) > 0 else 0
        top_sec = sec_dist.most_common(1)[0][0]
        top_sec_rate = sec_dist.most_common(1)[0][1] / n
        top_suf = Counter(get_suffix(r['word']) for r in sub_recs).most_common(1)[0]
        print(f"  {sub_prefix:5s}: n={n:4d} types={len(sub_words):3d} "
              f"A_frac={a_rate:.2f} top_sec={top_sec}({top_sec_rate:.2f}) "
              f"top_suf={top_suf[0]}({top_suf[1]/n:.2f}) "
              f"stem_in_vocab={in_vocab_rate:.2f}")


def h248_k_onset(records, dialect_map):
    print("\n" + "="*60)
    print("H248: k-ONSET CLASS CHARACTERIZATION")
    print("="*60)

    all_words = Counter(r['word'] for r in records)
    total_tokens = len(records)
    vocab = set(all_words.keys())

    # k-initial words (not starting with recognized onset)
    k_recs = [r for r in records if r['word'].startswith('k') and len(r['word']) >= 2]
    k_words = Counter(r['word'] for r in k_recs)
    k_total = sum(k_words.values())

    # Also get l-initial words for comparison
    l_recs = [r for r in records if r['word'].startswith('l') and len(r['word']) >= 3]

    print(f"\nTotal k-initial tokens: {k_total} ({k_total/total_tokens:.4f})")
    print(f"Total k-initial types: {len(k_words)}")

    # Top k-initial words
    print(f"\n--- Top k-initial words ---")
    for w, cnt in k_words.most_common(25):
        suf = get_suffix(w)
        # Is lw in vocab? (i.e., is l+w a word?)
        l_form = 'l' + w
        l_in_vocab = l_form in vocab
        # Is the word itself = l-stripped form of an lk-word?
        print(f"  {w:15s}: {cnt:4d}  suf={suf:6s}  l+w_in_vocab={l_in_vocab}")

    # Dialect distribution
    print(f"\n--- k-initial dialect distribution ---")
    k_by_dialect = Counter(r['dialect'] for r in k_recs)
    a_total = sum(1 for r in records if r['dialect'] == 'A')
    b_total = sum(1 for r in records if r['dialect'] == 'B')
    k_a_rate = k_by_dialect['A'] / a_total if a_total else 0
    k_b_rate = k_by_dialect['B'] / b_total if b_total else 0
    print(f"  A-dialect: {k_by_dialect['A']} ({k_a_rate*1000:.2f}‰)")
    print(f"  B-dialect: {k_by_dialect['B']} ({k_b_rate*1000:.2f}‰)")
    print(f"  A/B ratio: {k_a_rate/k_b_rate:.3f}")

    # Section distribution
    print(f"\n--- k-initial section distribution ---")
    section_totals = Counter(r['section'] for r in records)
    k_by_section = Counter(r['section'] for r in k_recs)
    overall_rate = k_total/total_tokens
    for sec in ['herbal','astro','cosmo','pharma','stars']:
        rate = k_by_section[sec] / section_totals[sec] if section_totals[sec] else 0
        enr = rate / overall_rate if overall_rate else 0
        print(f"  {sec:8s}: {k_by_section[sec]:4d}/{section_totals[sec]:5d} = {rate:.4f} (enr={enr:.2f}×)")

    # Suffix distribution
    print(f"\n--- k-initial suffix distribution ---")
    k_suffix = Counter(get_suffix(r['word']) for r in k_recs)
    total_suffix = Counter(get_suffix(r['word']) for r in records)
    n_k = sum(k_suffix.values())
    n_all = sum(total_suffix.values())
    for suf, cnt in k_suffix.most_common(10):
        obs = cnt/n_k
        base = total_suffix[suf]/n_all if n_all else 0
        enr = obs/base if base else 0
        print(f"  {suf:8s}: {cnt:4d} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")

    # Are kaiin and lkaiin related? Do they co-occur in same paragraphs?
    print(f"\n--- kaiin vs lkaiin co-occurrence analysis ---")
    para_words = defaultdict(set)
    # Group by folio (rough paragraph approximation)
    for r in records:
        para_words[r['folio']].add(r['word'])
    kaiin_folios = {r['folio'] for r in records if r['word'] == 'kaiin'}
    lkaiin_folios = {r['folio'] for r in records if r['word'] == 'lkaiin'}
    both = kaiin_folios & lkaiin_folios
    either = kaiin_folios | lkaiin_folios
    print(f"  kaiin appears in {len(kaiin_folios)} folios")
    print(f"  lkaiin appears in {len(lkaiin_folios)} folios")
    print(f"  Both: {len(both)} folios")
    print(f"  Expected if random: {len(kaiin_folios)*len(lkaiin_folios)/len(para_words):.1f} folios")
    print(f"  kaiin folios: {sorted(kaiin_folios)[:15]}")
    print(f"  lkaiin folios: {sorted(lkaiin_folios)[:15]}")

    # kaiin: what's the ONSET of kaiin in the 'other' class?
    print(f"\n--- kaiin, keedy etc: are they standalone or l-stripped forms? ---")
    for target_w, l_form in [('kaiin','lkaiin'),('keedy','lkeedy'),('keey','lkeey'),('kain','lkain')]:
        target_cnt = all_words.get(target_w, 0)
        l_cnt = all_words.get(l_form, 0)
        target_sec = Counter(r['section'] for r in records if r['word'] == target_w)
        l_sec = Counter(r['section'] for r in records if r['word'] == l_form)
        target_d = Counter(r['dialect'] for r in records if r['word'] == target_w)
        l_d = Counter(r['dialect'] for r in records if r['word'] == l_form)
        print(f"  {target_w}(n={target_cnt}) vs {l_form}(n={l_cnt}):")
        print(f"    {target_w}: A={target_d['A']}, B={target_d['B']}, "
              f"stars={target_sec['stars']}, herbal={target_sec['herbal']}")
        print(f"    {l_form}: A={l_d['A']}, B={l_d['B']}, "
              f"stars={l_sec['stars']}, herbal={l_sec['herbal']}")

    # Compare to qo-/o- prefix system
    print(f"\n--- Comparison: qo-prefix vs l-prefix vs k-standalone ---")
    # qo-stripped k-stems
    qo_k_words = [(w, w[2:]) for w in vocab if w.startswith('qo') and w[2:].startswith('k')]
    k_as_qo_stems = [(stem, w) for w, stem in qo_k_words if stem in vocab]
    print(f"  qo+k words with k-stem in vocab: {len(k_as_qo_stems)}")
    for w, stem in sorted(k_as_qo_stems, key=lambda x: -all_words.get(x[0],0))[:8]:
        print(f"    qok-compound: '{w}' → strip qo → '{stem}' (n={all_words.get(stem,0)})")

    # Big picture: which words starting with lk appear and does stripping l give k-words in vocab?
    print(f"\n--- lk-words and their k-stems ---")
    lk_recs = [r for r in records if r['word'].startswith('lk')]
    lk_words = Counter(r['word'] for r in lk_recs)
    for w, cnt in lk_words.most_common(15):
        stem = w[1:]
        in_vocab = stem in vocab
        stem_cnt = all_words.get(stem, 0)
        print(f"  {w:15s}: {cnt:3d}  stem='{stem}'  in_vocab={in_vocab}  stem_n={stem_cnt}")

    # Positional analysis for k-initial words
    print(f"\n--- k-initial positional distribution ---")
    first = sum(1 for r in k_recs if r['is_line_first'])
    last = sum(1 for r in k_recs if r['is_line_last'])
    mid = k_total - first - last
    print(f"  first={first/k_total:.3f}, mid={mid/k_total:.3f}, last={last/k_total:.3f}")

    # What precedes and follows k-initial words?
    print(f"\n--- Pre/post k-initial onset ---")
    pre_k = Counter(get_onset(r['prev_word']) for r in k_recs if r['prev_word'])
    post_k = Counter(get_onset(r['next_word']) for r in k_recs if r['next_word'])
    all_onset = Counter(get_onset(r['word']) for r in records)
    all_n = sum(all_onset.values())
    n_pre = sum(pre_k.values())
    n_post = sum(post_k.values())
    print(f"  Pre-k onset (n={n_pre}):")
    for onset, cnt in pre_k.most_common(6):
        obs = cnt/n_pre; base = all_onset[onset]/all_n if all_n else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
    print(f"  Post-k onset (n={n_post}):")
    for onset, cnt in post_k.most_common(6):
        obs = cnt/n_post; base = all_onset[onset]/all_n if all_n else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")


def main():
    print("Loading records...")
    records, dialect_map, line_records = parse_eva(DATA)
    print(f"Total: {len(records)} records")

    h247_l_onset(records, dialect_map)
    h248_k_onset(records, dialect_map)

if __name__ == '__main__':
    main()
