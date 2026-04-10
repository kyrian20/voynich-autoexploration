#!/usr/bin/env python3
"""
exp_117: The 'Other' Suffix Category — What Are Words With No Identified Suffix? (H228)
Also: H229: Paragraph-Internal Vocabulary Repetition (within-para vs cross-para cohesion)
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


def get_suffix(word):
    for suf in ['eeedy','eeey','eedy','edy','eey','aiin','ain','ol','or','ar','al','ey','dy','y']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return 'other'


def get_onset_class(word):
    w = word
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    if w.startswith('olk'): return 'olk'
    if w.startswith('d'): return 'd'
    if w.startswith('s'): return 's'
    return 'other'


def shannon_entropy(counts):
    total = sum(counts.values())
    if total == 0: return 0.0
    return -sum((c/total)*math.log2(c/total) for c in counts.values() if c > 0)


def parse_eva(path):
    edy_counts = defaultdict(int)
    total_counts = defaultdict(int)
    records = []
    para_id = [0]  # mutable counter

    current_para = {}  # folio -> para counter

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

            prefix = ''.join(c for c in locus_type if c in '@+*=~&')
            lt = locus_type[len(prefix):]
            is_body = bool(re.match(r'P', lt))
            if not is_body: continue

            is_para_start = '@' in prefix or '*' in prefix

            text_clean = re.sub(r'<[^>]*>', '', text)
            text_clean = re.sub(r'\[[^\]]*\]', lambda m: m.group(0)[1:-1].split(':')[0], text_clean)
            text_clean = re.sub(r'\{[^}]*\}', '', text_clean)
            text_clean = re.sub(r'@\d+;?', '', text_clean)
            text_clean = re.sub(r'<%>|<!.*?>|<\$>', '', text_clean)

            words = [w for w in re.split(r'[-.\s,]', text_clean)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue

            # Para tracking
            if is_para_start or folio_num not in current_para:
                current_para[folio_num] = current_para.get(folio_num, 0) + 1

            para_key = (folio_num, current_para[folio_num])

            for w in words:
                for suf_check in ['edy', 'eedy']:
                    if w.endswith(suf_check):
                        edy_counts[folio_num] += 1
                total_counts[folio_num] += 1
                records.append({
                    'word': w, 'folio': folio_num,
                    'line_in_folio': line_in_folio,
                    'section': SECTION_MAP.get(folio_num, 'other'),
                    'para_key': para_key,
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def h228_other_suffix(records):
    print("=" * 70)
    print("H228: The 'Other' Suffix Category")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']

    # Identify "other" words
    other_words = [r['word'] for r in body if get_suffix(r['word']) == 'other']
    all_words = [r['word'] for r in body]

    print(f"\nTotal body tokens: {len(all_words)}")
    print(f"'other' suffix tokens: {len(other_words)} ({100*len(other_words)/len(all_words):.1f}%)")

    # Frequency distribution
    other_counts = Counter(other_words)
    all_counts = Counter(all_words)

    print(f"\n--- Top 50 'other' words by frequency ---")
    print(f"{'Word':<16} {'n':<6} {'length':<8} {'onset':<8} {'ends_with'}")
    for word, cnt in other_counts.most_common(50):
        onset = get_onset_class(word)
        # What are the last 1-4 chars?
        ends = word[-4:] if len(word) >= 4 else word
        print(f"{word:<16} {cnt:<6} {len(word):<8} {onset:<8} {ends}")

    # Length distribution comparison: 'other' vs suffixed
    print(f"\n--- Length distribution: 'other' vs suffixed ---")
    suf_words = [r['word'] for r in body if get_suffix(r['word']) != 'other']
    suf_counts = Counter(suf_words)
    print(f"\n{'Length':<8} {'other_n':<10} {'other%':<10} {'suf_n':<10} {'suf%'}")
    other_len = Counter(len(w) for w in other_words)
    suf_len = Counter(len(w) for w in suf_words)
    for length in sorted(set(other_len) | set(suf_len)):
        o_n = other_len.get(length, 0)
        s_n = suf_len.get(length, 0)
        o_pct = 100*o_n/max(1,len(other_words))
        s_pct = 100*s_n/max(1,len(suf_words))
        print(f"{length:<8} {o_n:<10} {o_pct:<10.1f} {s_n:<10} {s_pct:.1f}")

    # Onset class distribution of 'other' words
    print(f"\n--- Onset class distribution of 'other' vs suffixed words ---")
    other_onset = Counter(get_onset_class(r['word']) for r in body if get_suffix(r['word']) == 'other')
    suf_onset = Counter(get_onset_class(r['word']) for r in body if get_suffix(r['word']) != 'other')
    all_onset = Counter(get_onset_class(r['word']) for r in body)

    o_total = sum(other_onset.values())
    s_total = sum(suf_onset.values())
    a_total = sum(all_onset.values())

    print(f"\n{'Onset':<8} {'other%':<10} {'suf%':<10} {'all%':<10} {'other/suf ratio'}")
    for cls in sorted(set(other_onset) | set(suf_onset), key=lambda x: -other_onset.get(x,0)):
        o_pct = 100*other_onset.get(cls,0)/max(1,o_total)
        s_pct = 100*suf_onset.get(cls,0)/max(1,s_total)
        a_pct = 100*all_onset.get(cls,0)/max(1,a_total)
        ratio = (o_pct / s_pct) if s_pct > 0 else float('inf')
        print(f"{cls:<8} {o_pct:<10.2f} {s_pct:<10.2f} {a_pct:<10.2f} {ratio:.2f}")

    # Section distribution
    print(f"\n--- Section distribution of 'other' words ---")
    other_section = Counter(r['section'] for r in body if get_suffix(r['word']) == 'other')
    all_section = Counter(r['section'] for r in body)
    print(f"\n{'Section':<10} {'other_n':<10} {'all_n':<10} {'other_rate%':<14} {'all_rate%'}")
    for s in ['herbal','cosmo','stars','pharma','astro']:
        o_n = other_section.get(s, 0)
        a_n = all_section.get(s, 0)
        print(f"{s:<10} {o_n:<10} {a_n:<10} {100*o_n/max(1,a_n):<14.1f} {100*a_n/max(1,sum(all_section.values())):.1f}")

    # Hapax analysis
    print(f"\n--- Hapax analysis (frequency = 1) ---")
    other_hapax = sum(1 for w, c in other_counts.items() if c == 1)
    suf_hapax = sum(1 for w, c in suf_counts.items() if c == 1)
    other_unique = len(other_counts)
    suf_unique = len(suf_counts)
    print(f"'other' unique types: {other_unique}")
    print(f"'other' hapax (n=1): {other_hapax} ({100*other_hapax/max(1,other_unique):.1f}% of types)")
    print(f"Suffixed unique types: {suf_unique}")
    print(f"Suffixed hapax (n=1): {suf_hapax} ({100*suf_hapax/max(1,suf_unique):.1f}% of types)")

    # Sub-pattern analysis: what endings do 'other' words have?
    print(f"\n--- Sub-pattern: common 2-char endings of 'other' words ---")
    endings_2 = Counter(w[-2:] for w in other_words if len(w) >= 2)
    print(f"\n{'Ending':<8} {'n':<6} {'%'}")
    for ending, cnt in endings_2.most_common(20):
        print(f"{ending:<8} {cnt:<6} {100*cnt/len(other_words):.1f}%")

    print(f"\n--- Sub-pattern: common 3-char endings of 'other' words ---")
    endings_3 = Counter(w[-3:] for w in other_words if len(w) >= 3)
    for ending, cnt in endings_3.most_common(15):
        print(f"{ending:<8} {cnt:<6} {100*cnt/len(other_words):.1f}%")

    # Could we extend the suffix list? Most common single-char endings
    print(f"\n--- Most common final chars of 'other' words ---")
    final_chars = Counter(w[-1] for w in other_words)
    for ch, cnt in final_chars.most_common(15):
        print(f"  '{ch}': {cnt} ({100*cnt/len(other_words):.1f}%)")

    # Short words (2-3 char) — likely function words?
    print(f"\n--- Short 'other' words (length 2-4): likely function words ---")
    short_others = {w: c for w, c in other_counts.items() if len(w) <= 4}
    for w, c in sorted(short_others.items(), key=lambda x: -x[1])[:30]:
        print(f"  '{w}': {c}")


def h229_para_cohesion(records):
    print("\n" + "=" * 70)
    print("H229: Paragraph-Internal Vocabulary Repetition")
    print("=" * 70)

    body = [r for r in records if r['section'] != 'other']

    # Group by paragraph
    paras = defaultdict(list)
    for r in body:
        paras[r['para_key']].append(r['word'])

    para_sizes = Counter(len(words) for words in paras.values())
    print(f"\nTotal paragraphs: {len(paras)}")
    print(f"Para sizes: min={min(para_sizes.keys())}, max={max(para_sizes.keys())}, "
          f"mean={sum(k*v for k,v in para_sizes.items())/sum(para_sizes.values()):.1f}")

    # Within-para type/token ratio
    print(f"\n--- Within-para type/token ratio (vocabulary richness) ---")
    ttr_by_size = defaultdict(list)
    for pk, words in paras.items():
        n = len(words)
        unique = len(set(words))
        ttr = unique / n
        # Bin by size
        size_bin = min(n // 10 * 10, 100)
        ttr_by_size[size_bin].append(ttr)

    print(f"\n{'Size bin':<12} {'Mean TTR':<12} {'n_paras'}")
    for size_bin in sorted(ttr_by_size.keys()):
        ttrs = ttr_by_size[size_bin]
        print(f"{size_bin:<12} {sum(ttrs)/len(ttrs):<12.3f} {len(ttrs)}")

    # Within-para vs cross-para word sharing
    print(f"\n--- Within-para vs cross-para word overlap ---")

    # For each paragraph, compute overlap with:
    # (a) the next paragraph (adjacent)
    # (b) a random non-adjacent paragraph

    sorted_para_keys = sorted(paras.keys())
    n_paras = len(sorted_para_keys)

    within_overlaps = []  # within-para self-repetition rate
    adj_overlaps = []     # overlap with next paragraph
    non_adj_overlaps = [] # overlap with a random non-adjacent paragraph

    import random
    random.seed(42)

    for i, pk in enumerate(sorted_para_keys):
        words = paras[pk]
        word_set = set(words)

        # Self: how many words appear more than once in para?
        word_counts = Counter(words)
        n_repeated = sum(1 for w in words if word_counts[w] > 1)
        self_rep_rate = n_repeated / len(words) if words else 0
        within_overlaps.append(self_rep_rate)

        # Adjacent paragraph overlap
        if i < n_paras - 1:
            next_pk = sorted_para_keys[i+1]
            # Only count adjacent in same section
            if next_pk[0] == pk[0] or abs(next_pk[0] - pk[0]) <= 2:
                next_words = set(paras[next_pk])
                inter = len(word_set & next_words)
                union = len(word_set | next_words)
                adj_overlaps.append(inter / union if union > 0 else 0)

        # Non-adjacent paragraph (5+ paragraphs away)
        if n_paras > 10:
            candidates = [j for j in range(n_paras) if abs(j - i) >= 5]
            if candidates:
                j = random.choice(candidates)
                nonadj_pk = sorted_para_keys[j]
                nonadj_words = set(paras[nonadj_pk])
                inter = len(word_set & nonadj_words)
                union = len(word_set | nonadj_words)
                non_adj_overlaps.append(inter / union if union > 0 else 0)

    print(f"\nWithin-para word repetition rate: {sum(within_overlaps)/len(within_overlaps):.3f}")
    print(f"Adjacent-para Jaccard overlap: {sum(adj_overlaps)/max(1,len(adj_overlaps)):.3f}")
    print(f"Non-adjacent-para Jaccard overlap: {sum(non_adj_overlaps)/max(1,len(non_adj_overlaps)):.3f}")
    print(f"Adjacent/non-adjacent ratio: {(sum(adj_overlaps)/max(1,len(adj_overlaps))) / max(0.001, sum(non_adj_overlaps)/max(1,len(non_adj_overlaps))):.2f}×")

    # Stem (onset class) repetition within para
    print(f"\n--- Within-para onset class repetition ---")
    para_onset_rep = []
    for pk, words in paras.items():
        if len(words) < 5: continue
        onsets = [get_onset_class(w) for w in words]
        onset_counts = Counter(onsets)
        n_repeated_onset = sum(1 for o in onsets if onset_counts[o] > 1)
        para_onset_rep.append(n_repeated_onset / len(onsets))

    print(f"Mean onset repetition rate within paragraphs: {sum(para_onset_rep)/max(1,len(para_onset_rep)):.3f}")

    # By section: do some sections have more within-para cohesion?
    print(f"\n--- Within-para self-repetition by section ---")
    section_paras = defaultdict(list)
    for pk, words in paras.items():
        folio = pk[0]
        section = SECTION_MAP.get(folio, 'other')
        if section == 'other': continue
        word_counts = Counter(words)
        n_repeated = sum(1 for w in words if word_counts[w] > 1)
        rep_rate = n_repeated / len(words) if words else 0
        section_paras[section].append(rep_rate)

    print(f"\n{'Section':<10} {'Mean rep rate':<16} {'n_paras'}")
    for s in ['herbal','cosmo','stars','pharma','astro']:
        rates = section_paras[s]
        if not rates: continue
        print(f"{s:<10} {sum(rates)/len(rates):<16.3f} {len(rates)}")

    # Top within-para repeated words
    print(f"\n--- Most repeated words within single paragraphs ---")
    para_repeats = Counter()
    for pk, words in paras.items():
        word_counts = Counter(words)
        for w, c in word_counts.items():
            if c >= 3:
                para_repeats[w] += 1  # count paragraphs where this word appears 3+ times

    print(f"\n{'Word':<16} {'Paras with ≥3 occ':<20} {'Onset':<8} {'Suffix'}")
    for word, cnt in para_repeats.most_common(20):
        print(f"{word:<16} {cnt:<20} {get_onset_class(word):<8} {get_suffix(word)}")


def main():
    print("Loading data...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total body tokens: {len(records)}")

    h228_other_suffix(records)
    h229_para_cohesion(records)


if __name__ == '__main__':
    main()
