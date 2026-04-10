#!/usr/bin/env python3
"""
exp_121: Trigram Phrase Structure (H238) + Stars Catalog Template (H239)
H238: Extract [W1][daiin][cth-word] trigrams in A-dialect; characterize W1 onset class
H239: Per-line suffix sequence in stars paragraphs; repeating template?
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
    line_records = defaultdict(list)  # (folio_num, line_in_folio) -> word list

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


# ─────────────────────────── H238 ───────────────────────────
def h238_trigram_phrase(records, dialect_map, line_records):
    print("\n" + "="*60)
    print("H238: TRIGRAM PHRASE STRUCTURE [W1][daiin][cth-word]")
    print("="*60)

    a_records = [r for r in records if r['dialect'] == 'A']
    print(f"\nA-dialect records: {len(a_records)}")

    # Get A-dialect onset baseline
    a_onset_counts = Counter(get_onset(r['word']) for r in a_records)
    a_total = sum(a_onset_counts.values())

    # Get A-dialect suffix baseline
    a_suffix_counts = Counter(get_suffix(r['word']) for r in a_records)

    # Extract trigrams [W1][daiin][W3] where W3 is cth-onset
    # Work from line_records for A-dialect folios
    trigrams = []
    daiin_total = 0
    w1_onsets = Counter()
    w1_suffixes = Counter()
    w3_words = Counter()
    w1_words = Counter()

    a_folios = {fnum for fnum, d in dialect_map.items() if d == 'A'}

    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in a_folios: continue
        for i in range(len(words)):
            if words[i] == 'daiin':
                daiin_total += 1
                if i > 0 and i < len(words) - 1:
                    w3_onset = get_onset(words[i+1])
                    if w3_onset == 'cth':
                        w1 = words[i-1]
                        w3 = words[i+1]
                        w1_onsets[get_onset(w1)] += 1
                        w1_suffixes[get_suffix(w1)] += 1
                        w3_words[w3] += 1
                        w1_words[w1] += 1
                        trigrams.append({'w1': w1, 'w3': w3, 'folio': folio_num})

    print(f"A-dialect daiin occurrences: {daiin_total}")
    print(f"Trigrams [W1][daiin][cth-word]: {len(trigrams)}")
    if daiin_total > 0:
        print(f"Rate of daiin→[W][cth] as trigram: {len(trigrams)/daiin_total:.3f}")

    print(f"\n--- W1 Onset Distribution (n={sum(w1_onsets.values())}) ---")
    for onset, cnt in w1_onsets.most_common(12):
        base_rate = a_onset_counts[onset] / a_total if a_total > 0 else 0
        obs_rate = cnt / sum(w1_onsets.values()) if w1_onsets else 0
        enr = obs_rate / base_rate if base_rate > 0 else float('inf')
        print(f"  {onset:8s}: {cnt:4d} ({obs_rate:.3f} obs vs {base_rate:.3f} base = {enr:.2f}×)")

    print(f"\n--- W1 Suffix Distribution (n={sum(w1_suffixes.values())}) ---")
    for suf, cnt in w1_suffixes.most_common(10):
        base_rate = a_suffix_counts[suf] / a_total if a_total > 0 else 0
        obs_rate = cnt / sum(w1_suffixes.values()) if w1_suffixes else 0
        enr = obs_rate / base_rate if base_rate > 0 else float('inf')
        print(f"  {suf:8s}: {cnt:4d} ({obs_rate:.3f} obs vs {base_rate:.3f} base = {enr:.2f}×)")

    print(f"\n--- Top W1 words (before daiin before cth) ---")
    for w, cnt in w1_words.most_common(15):
        onset = get_onset(w)
        suf = get_suffix(w)
        print(f"  {w:12s}: {cnt:3d}  [onset={onset}, suf={suf}]")

    print(f"\n--- Top W3 words (cth-onset after daiin) ---")
    for w, cnt in w3_words.most_common(15):
        print(f"  {w:12s}: {cnt}")

    # 4-gram: look one step further back [W0][W1][daiin][cth]
    print(f"\n--- 4-gram: [W0][W1][daiin][cth-word] ---")
    fourgrams_w0_onset = Counter()
    fourgrams_w0_words = Counter()
    fourgram_count = 0
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in a_folios: continue
        for i in range(1, len(words)):
            if words[i] == 'daiin' and i > 1 and i < len(words) - 1:
                if get_onset(words[i+1]) == 'cth':
                    fourgram_count += 1
                    w0 = words[i-2]
                    fourgrams_w0_onset[get_onset(w0)] += 1
                    fourgrams_w0_words[w0] += 1
    if fourgram_count > 0:
        print(f"  4-grams [W0][W1][daiin][cth]: {fourgram_count}")
        print(f"  W0 onset distribution:")
        for onset, cnt in fourgrams_w0_onset.most_common(8):
            base_rate = a_onset_counts[onset] / a_total if a_total > 0 else 0
            obs_rate = cnt / fourgram_count
            enr = obs_rate / base_rate if base_rate > 0 else float('inf')
            print(f"    {onset:8s}: {cnt} ({obs_rate:.3f} vs {base_rate:.3f} = {enr:.2f}×)")
        print(f"  Top W0 words:")
        for w, cnt in fourgrams_w0_words.most_common(10):
            print(f"    {w:12s}: {cnt}")

    # What is W2 when daiin is at line-start?
    print(f"\n--- daiin as line-FIRST word: W2 onset enrichment ---")
    daiin_first_w2 = Counter()
    daiin_first_total = 0
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in a_folios: continue
        if words and words[0] == 'daiin' and len(words) > 1:
            daiin_first_total += 1
            daiin_first_w2[get_onset(words[1])] += 1
    if daiin_first_total > 0:
        print(f"  Lines starting with daiin: {daiin_first_total}")
        for onset, cnt in daiin_first_w2.most_common(8):
            base_rate = a_onset_counts[onset] / a_total if a_total > 0 else 0
            obs_rate = cnt / daiin_first_total
            enr = obs_rate / base_rate if base_rate > 0 else float('inf')
            print(f"  {onset:8s}: {cnt} ({obs_rate:.3f} vs {base_rate:.3f} = {enr:.2f}×)")

    # Test: what's before daiin?  (general, not just in trigram)
    print(f"\n--- General: what onset precedes daiin in A-dialect? ---")
    pre_daiin_onset = Counter()
    pre_daiin_words = Counter()
    for r in a_records:
        if r['word'] == 'daiin' and r['prev_word']:
            pre_daiin_onset[get_onset(r['prev_word'])] += 1
            pre_daiin_words[r['prev_word']] += 1
    n_pre = sum(pre_daiin_onset.values())
    if n_pre > 0:
        print(f"  Total daiin with prev word: {n_pre}")
        for onset, cnt in pre_daiin_onset.most_common(10):
            base_rate = a_onset_counts[onset] / a_total if a_total > 0 else 0
            obs_rate = cnt / n_pre
            enr = obs_rate / base_rate if base_rate > 0 else float('inf')
            print(f"  {onset:8s}: {cnt:4d} ({obs_rate:.3f} vs {base_rate:.3f} = {enr:.2f}×)")
        print(f"  Top pre-daiin words:")
        for w, cnt in pre_daiin_words.most_common(12):
            print(f"    {w:12s}: {cnt}")


# ─────────────────────────── H239 ───────────────────────────
def h239_stars_catalog(records, dialect_map, line_records):
    print("\n" + "="*60)
    print("H239: STARS SECTION CATALOG TEMPLATE")
    print("="*60)

    stars_folios = {fnum for fnum, sec in SECTION_MAP.items() if sec == 'stars'}
    print(f"\nStars folio nums: {sorted(stars_folios)}")

    stars_recs = [r for r in records if r['section'] == 'stars']
    print(f"Stars word tokens: {len(stars_recs)}")

    if not stars_recs:
        print("No stars records found!")
        return

    stars_folio_nums = sorted(set(r['folio'] for r in stars_recs))
    print(f"Stars folios present: {stars_folio_nums}")
    print(f"Dialect distribution: A={sum(1 for f in stars_folio_nums if dialect_map.get(f)=='A')}, "
          f"B={sum(1 for f in stars_folio_nums if dialect_map.get(f)=='B')}")

    # Get per-line word sequences for stars
    stars_lines = {}  # (folio, line) -> words
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num in stars_folios and words:
            stars_lines[(folio_num, line_in_folio)] = words

    print(f"\nLines in stars: {len(stars_lines)}")
    line_lengths = [len(w) for w in stars_lines.values()]
    if line_lengths:
        print(f"Mean words/line: {sum(line_lengths)/len(line_lengths):.2f}")
        llen_cnt = Counter(line_lengths)
        print(f"Line length distribution:")
        for l in sorted(llen_cnt):
            print(f"  {l:3d} words: {llen_cnt[l]}")

    # Per-line suffix sequences
    suffix_sequences = []
    onset_sequences = []
    for key in sorted(stars_lines.keys()):
        words = stars_lines[key]
        suf_seq = tuple(get_suffix(w) for w in words)
        ons_seq = tuple(get_onset(w) for w in words)
        suffix_sequences.append(suf_seq)
        onset_sequences.append(ons_seq)

    # Most common suffix sequences
    print(f"\n--- Top suffix sequences ---")
    seq_cnt = Counter(suffix_sequences)
    for seq, cnt in seq_cnt.most_common(20):
        seq_str = ' '.join(seq)
        print(f"  n={cnt:3d}: [{seq_str}]")

    # Most common onset sequences
    print(f"\n--- Top onset sequences ---")
    ons_seq_cnt = Counter(onset_sequences)
    for seq, cnt in ons_seq_cnt.most_common(20):
        seq_str = ' '.join(seq)
        print(f"  n={cnt:3d}: [{seq_str}]")

    # Position-specific suffix distribution
    print(f"\n--- Position-specific suffix (stars lines) ---")
    pos_suffix = defaultdict(Counter)
    for seq in suffix_sequences:
        for i, s in enumerate(seq):
            pos_suffix[i][s] += 1

    # Baseline suffix in stars
    stars_suffix_all = Counter(get_suffix(r['word']) for r in stars_recs)
    stars_total = sum(stars_suffix_all.values())
    baseline_H = -sum((c/stars_total)*math.log2(c/stars_total)
                      for c in stars_suffix_all.values() if c > 0)
    print(f"  Baseline suffix H = {baseline_H:.3f}")

    for pos in sorted(pos_suffix.keys()):
        total = sum(pos_suffix[pos].values())
        if total < 5: continue
        H = -sum((c/total)*math.log2(c/total) for c in pos_suffix[pos].values() if c > 0)
        top3 = pos_suffix[pos].most_common(3)
        top_str = ' | '.join(f'{s}={c/total:.2f}' for s,c in top3)
        print(f"  pos {pos}: n={total:3d}  H={H:.3f} (Δ{H-baseline_H:+.3f}) | {top_str}")

    # Position-specific onset distribution
    print(f"\n--- Position-specific onset (stars lines) ---")
    pos_onset = defaultdict(Counter)
    for seq in onset_sequences:
        for i, o in enumerate(seq):
            pos_onset[i][o] += 1

    stars_onset_all = Counter(get_onset(r['word']) for r in stars_recs)
    baseline_onset_H = -sum((c/stars_total)*math.log2(c/stars_total)
                             for c in stars_onset_all.values() if c > 0)
    print(f"  Baseline onset H = {baseline_onset_H:.3f}")

    for pos in sorted(pos_onset.keys()):
        total = sum(pos_onset[pos].values())
        if total < 5: continue
        H = -sum((c/total)*math.log2(c/total) for c in pos_onset[pos].values() if c > 0)
        top3 = pos_onset[pos].most_common(3)
        top_str = ' | '.join(f'{o}={c/total:.2f}' for o,c in top3)
        print(f"  pos {pos}: n={total:3d}  H={H:.3f} (Δ{H-baseline_onset_H:+.3f}) | {top_str}")

    # Common 2-gram onset patterns at each position pair
    print(f"\n--- Common onset bigrams by position pair ---")
    pair_onset = defaultdict(Counter)
    for seq in onset_sequences:
        for i in range(len(seq)-1):
            pair_onset[i][(seq[i], seq[i+1])] += 1
    for pos in sorted(pair_onset.keys()):
        total = sum(pair_onset[pos].values())
        if total < 5: continue
        top = pair_onset[pos].most_common(3)
        top_str = '; '.join(f'[{p[0]} {p[1]}]={c/total:.2f}' for p,c in top)
        print(f"  pos ({pos},{pos+1}): n={total} | {top_str}")

    # otaiin positional analysis in stars
    print(f"\n--- otaiin in stars: position distribution ---")
    otaiin_pos = Counter()
    otaiin_contexts = []
    for key in sorted(stars_lines.keys()):
        words = stars_lines[key]
        for i, w in enumerate(words):
            if w == 'otaiin':
                otaiin_pos[i] += 1
                context = words[max(0,i-2):i+3]
                otaiin_contexts.append((key, i, context))
    print(f"  otaiin in stars total: {sum(otaiin_pos.values())}")
    for pos, cnt in sorted(otaiin_pos.items()):
        print(f"    abs pos {pos}: {cnt}")
    print(f"  Sample contexts:")
    for key, pos, ctx in otaiin_contexts[:12]:
        print(f"    f{key[0]}.L{key[1]} pos{pos}: {' '.join(ctx)}")

    # ot-onset clustering in stars
    print(f"\n--- ot-onset run-length analysis in stars ---")
    ot_run_lengths = []
    for seq in onset_sequences:
        run = 0
        for o in seq:
            if o in ('ot', 'ok'):
                run += 1
            else:
                if run > 0:
                    ot_run_lengths.append(run)
                run = 0
        if run > 0:
            ot_run_lengths.append(run)
    print(f"  ot/ok-onset runs: {len(ot_run_lengths)} total")
    for l, c in sorted(Counter(ot_run_lengths).items()):
        print(f"    run of {l}: {c}")

    # What comes right after otaiin in stars?
    print(f"\n--- After otaiin in stars: next onset enrichment ---")
    post_otaiin = Counter()
    post_otaiin_words = Counter()
    for key in sorted(stars_lines.keys()):
        words = stars_lines[key]
        for i, w in enumerate(words):
            if w == 'otaiin' and i < len(words) - 1:
                nw = words[i+1]
                post_otaiin[get_onset(nw)] += 1
                post_otaiin_words[nw] += 1
    n_post = sum(post_otaiin.values())
    if n_post > 0:
        stars_onset_base = {o: c/stars_total for o,c in stars_onset_all.items()}
        print(f"  n={n_post}")
        for onset, cnt in post_otaiin.most_common(8):
            base_rate = stars_onset_base.get(onset, 0)
            obs_rate = cnt / n_post
            enr = obs_rate / base_rate if base_rate > 0 else float('inf')
            print(f"  {onset:8s}: {cnt} ({obs_rate:.3f} vs {base_rate:.3f} = {enr:.2f}×)")
        print(f"  Top words after otaiin:")
        for w, cnt in post_otaiin_words.most_common(10):
            print(f"    {w:12s}: {cnt}")

    # Folio-by-folio onset at position 0
    print(f"\n--- Folio-level: onset at pos 0 ---")
    folio_pos0 = defaultdict(Counter)
    for (folio_num, line_in_folio), words in sorted(stars_lines.items()):
        if words:
            folio_pos0[folio_num][get_onset(words[0])] += 1
    for folio_num in sorted(folio_pos0.keys()):
        top = folio_pos0[folio_num].most_common(3)
        top_str = ' | '.join(f'{o}={c}' for o,c in top)
        total = sum(folio_pos0[folio_num].values())
        d = dialect_map.get(folio_num, '?')
        print(f"  f{folio_num:3d} ({d}): n={total} lines | {top_str}")

    # Stars-specific: compare first half vs second half of lines
    print(f"\n--- Stars onset: first-half vs second-half of line ---")
    first_half_onsets = Counter()
    second_half_onsets = Counter()
    for seq in onset_sequences:
        n = len(seq)
        mid = n // 2
        for i, o in enumerate(seq):
            if i < mid:
                first_half_onsets[o] += 1
            else:
                second_half_onsets[o] += 1
    fh_total = sum(first_half_onsets.values())
    sh_total = sum(second_half_onsets.values())
    print(f"  First half (n={fh_total}): {dict(first_half_onsets.most_common(6))}")
    print(f"  Second half (n={sh_total}): {dict(second_half_onsets.most_common(6))}")
    print(f"  Onset enrichment in 2nd half vs 1st half:")
    all_onsets = set(first_half_onsets) | set(second_half_onsets)
    for o in sorted(all_onsets, key=lambda x: -(second_half_onsets[x]/max(sh_total,1) /
                                                  max(first_half_onsets[x]/max(fh_total,1), 0.001))):
        fh_rate = first_half_onsets[o] / fh_total if fh_total else 0
        sh_rate = second_half_onsets[o] / sh_total if sh_total else 0
        enr = sh_rate / fh_rate if fh_rate > 0 else float('inf')
        if first_half_onsets[o] + second_half_onsets[o] < 5: continue
        print(f"    {o:8s}: 1st={fh_rate:.3f} 2nd={sh_rate:.3f} enr={enr:.2f}×")


def main():
    print("Loading records...")
    records, dialect_map, line_records = parse_eva(DATA)
    print(f"Total records: {len(records)}")
    print(f"Total lines: {len(line_records)}")
    print(f"A-dialect folios: {sum(1 for d in dialect_map.values() if d=='A')}")
    print(f"B-dialect folios: {sum(1 for d in dialect_map.values() if d=='B')}")

    h238_trigram_phrase(records, dialect_map, line_records)
    h239_stars_catalog(records, dialect_map, line_records)

if __name__ == '__main__':
    main()
