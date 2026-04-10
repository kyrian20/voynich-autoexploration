#!/usr/bin/env python3
"""
exp_123: Onset-Class Transition Matrix (H244) + Stars "Other" Onset Class (H242)
H244: Full Markov grammar over onset classes — forbidden/mandatory transitions, directed cycle?
H242: What specific words constitute "other"-onset at stars line-starts?
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

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s','other']

def get_onset(word):
    for o in ONSETS[:-1]:
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


# ─────────────────────────── H244 ───────────────────────────
def h244_onset_grammar(records, dialect_map):
    print("\n" + "="*60)
    print("H244: ONSET-CLASS TRANSITION MATRIX (MARKOV GRAMMAR)")
    print("="*60)

    ONSET_ORDER = ['s','d','ch','sh','cth','ok','ot','qok','qot','qo','ol','other']

    for dialect_label, recs in [('ALL', records), ('A-dialect', [r for r in records if r['dialect']=='A']),
                                  ('B-dialect', [r for r in records if r['dialect']=='B'])]:
        recs_with_next = [r for r in recs if r['next_word']]
        total = len(recs_with_next)

        # Baseline onset distribution
        baseline = Counter(get_onset(r['word']) for r in recs)
        baseline_next = Counter(get_onset(r['next_word']) for r in recs_with_next)
        baseline_total = sum(baseline_next.values())

        print(f"\n{'='*50}")
        print(f"--- {dialect_label} Onset Transition Matrix ---")
        print(f"{'='*50}")
        print(f"n={total} word pairs")
        print(f"\nRows = current onset, Cols = next onset (enrichment vs baseline)")

        # Print header
        header = f"{'from\\to':10s}"
        for onset in ONSET_ORDER:
            header += f" {onset:6s}"
        header += f"  {'H(next)':8s} {'n':6s}"
        print(header)

        # Compute per-source-onset transition
        transition_matrix = {}  # src -> Counter of next onsets
        for r in recs_with_next:
            src = get_onset(r['word'])
            tgt = get_onset(r['next_word'])
            if src not in transition_matrix:
                transition_matrix[src] = Counter()
            transition_matrix[src][tgt] += 1

        # Print enrichment matrix
        forbidden_pairs = []  # enrichment < 0.15
        mandatory_pairs = []  # enrichment > 3.0
        for src in ONSET_ORDER:
            counts = transition_matrix.get(src, Counter())
            n_src = sum(counts.values())
            if n_src == 0:
                continue
            H = shannon_entropy(counts)
            row = f"{src:10s}"
            for tgt in ONSET_ORDER:
                obs = counts.get(tgt, 0) / n_src
                base = baseline_next.get(tgt, 0) / baseline_total if baseline_total else 0
                enr = obs / base if base > 0 else float('inf')
                if counts.get(tgt, 0) >= 5:  # Only flag with sufficient n
                    if enr < 0.15:
                        forbidden_pairs.append((src, tgt, enr, counts.get(tgt, 0)))
                    if enr > 3.0:
                        mandatory_pairs.append((src, tgt, enr, counts.get(tgt, 0)))
                row += f" {enr:6.2f}"
            row += f"  {H:8.3f} {n_src:6d}"
            print(row)

        print(f"\n  FORBIDDEN pairs (enr<0.15, n≥5):")
        for src, tgt, enr, n in sorted(forbidden_pairs, key=lambda x: x[2]):
            print(f"    {src}→{tgt}: {enr:.3f}× (n={n})")
        print(f"\n  MANDATORY pairs (enr>3.0, n≥5):")
        for src, tgt, enr, n in sorted(mandatory_pairs, key=lambda x: -x[2]):
            print(f"    {src}→{tgt}: {enr:.2f}× (n={n})")

        # Which onset is most constrained (lowest H)?
        print(f"\n  Onset-class collocational entropy (H of next onset):")
        h_by_onset = []
        for src in ONSET_ORDER:
            counts = transition_matrix.get(src, Counter())
            n_src = sum(counts.values())
            if n_src < 20: continue
            H = shannon_entropy(counts)
            h_by_onset.append((src, H, n_src))
        baseline_H = shannon_entropy(baseline_next)
        print(f"  Baseline H(next onset) = {baseline_H:.3f}")
        for src, H, n_src in sorted(h_by_onset, key=lambda x: x[1]):
            print(f"    {src:8s}: H={H:.3f} (Δ{H-baseline_H:+.3f})  n={n_src}")

    # Grammar cycle detection
    print(f"\n--- Grammar Cycle Analysis (All corpus) ---")
    print("Testing proposed cycle chains:")
    recs_all = [r for r in records if r['next_word']]
    all_baseline_next = Counter(get_onset(r['next_word']) for r in recs_all)
    all_total = sum(all_baseline_next.values())

    transition_all = defaultdict(Counter)
    for r in recs_all:
        transition_all[get_onset(r['word'])][get_onset(r['next_word'])] += 1

    def chain_enr(chain):
        """Compute enrichment for each step in a chain."""
        results = []
        for i in range(len(chain)-1):
            src, tgt = chain[i], chain[i+1]
            n_src = sum(transition_all[src].values())
            obs = transition_all[src].get(tgt, 0) / max(n_src, 1)
            base = all_baseline_next.get(tgt, 0) / max(all_total, 1)
            enr = obs / base if base > 0 else 0
            results.append((src, tgt, enr, transition_all[src].get(tgt, 0)))
        return results

    test_chains = [
        ['s', 'd', 'ch', 'cth'],
        ['s', 'ch', 'cth'],
        ['s', 'ch', 'd', 'cth'],
        ['d', 'ch', 'cth'],
        ['d', 'sh', 'cth'],
        ['sh', 'qok', 'ch'],
        ['sh', 'qo', 'ch'],
        ['ch', 'ch', 'cth'],
        ['qok', 'sh', 'qok'],  # B-paradigm cycle
        ['ol', 'd', 'ch'],
        ['ch', 'd', 'cth'],
        ['cth', 'd', 'cth'],  # cth→d→cth cycle?
        ['ot', 'ch', 'ot'],   # B-paradigm ot cycle?
    ]
    for chain in test_chains:
        steps = chain_enr(chain)
        step_str = ' → '.join(f'{s}→{t}={e:.2f}×(n={n})' for s,t,e,n in steps)
        mean_enr = (sum(e for _,_,e,_ in steps) / len(steps)) if steps else 0
        print(f"  {' → '.join(chain)}: [{step_str}] mean={mean_enr:.2f}×")


# ─────────────────────────── H242 ───────────────────────────
def h242_stars_other(records, dialect_map, line_records):
    print("\n" + "="*60)
    print("H242: STARS 'OTHER'-ONSET CLASS CHARACTERIZATION")
    print("="*60)

    stars_folios = set(range(103, 117))

    stars_recs = [r for r in records if r['folio'] in stars_folios]
    print(f"\nStars records: {len(stars_recs)}")
    stars_total = len(stars_recs)

    # All "other"-onset words in stars
    stars_other = [r for r in stars_recs if get_onset(r['word']) == 'other']
    print(f"Stars 'other'-onset tokens: {len(stars_other)} ({len(stars_other)/stars_total:.3f})")

    # Frequency table of "other"-onset words in stars
    stars_other_words = Counter(r['word'] for r in stars_other)
    print(f"\n--- Top 'other'-onset words in stars ---")
    for w, cnt in stars_other_words.most_common(30):
        rate = cnt / stars_total
        # What suffix does this word have?
        suf = get_suffix(w)
        # Is it a standalone short word (1-3 chars)?
        print(f"  {w:15s}: {cnt:4d} ({rate:.4f}) suf={suf}")

    # Stars pos-0 "other" words
    print(f"\n--- Stars line-START 'other'-onset words ---")
    stars_first_other = []
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in stars_folios: continue
        if words and get_onset(words[0]) == 'other':
            stars_first_other.append(words[0])
    first_other_cnt = Counter(stars_first_other)
    n_first_other = len(stars_first_other)
    total_lines = sum(1 for (f,l), w in line_records.items() if f in stars_folios and w)
    print(f"  Lines starting with 'other' onset: {n_first_other}/{total_lines} ({n_first_other/total_lines:.3f})")
    for w, cnt in first_other_cnt.most_common(20):
        suf = get_suffix(w)
        print(f"    {w:15s}: {cnt:3d}  suf={suf}")

    # Characterize: are these standalone (no suffix match), short, or compound?
    print(f"\n--- Analysis: breakdown of 'other'-onset in stars ---")
    short_words = [(w, c) for w,c in stars_other_words.items() if len(w) <= 3]
    medium_words = [(w, c) for w,c in stars_other_words.items() if 4 <= len(w) <= 5]
    long_words = [(w, c) for w,c in stars_other_words.items() if len(w) >= 6]

    print(f"  Short (≤3 chars): {len(short_words)} types, {sum(c for _,c in short_words)} tokens")
    for w, c in sorted(short_words, key=lambda x: -x[1])[:10]:
        print(f"    {w:8s}: {c}")
    print(f"  Medium (4-5 chars): {len(medium_words)} types, {sum(c for _,c in medium_words)} tokens")
    for w, c in sorted(medium_words, key=lambda x: -x[1])[:10]:
        print(f"    {w:8s}: {c}  suf={get_suffix(w)}")
    print(f"  Long (≥6 chars): {len(long_words)} types, {sum(c for _,c in long_words)} tokens")
    for w, c in sorted(long_words, key=lambda x: -x[1])[:10]:
        print(f"    {w:8s}: {c}  suf={get_suffix(w)}")

    # Does "other" at stars line-start overlap with overall "other" top words?
    print(f"\n--- Overall 'other'-onset top words (all corpus) ---")
    all_other = Counter(r['word'] for r in records if get_onset(r['word']) == 'other')
    for w, cnt in all_other.most_common(20):
        in_stars = stars_other_words.get(w, 0)
        print(f"  {w:15s}: total={cnt:5d}  stars={in_stars:3d}  ({in_stars/cnt:.2f} in stars)")

    # Stars line-end "other"
    print(f"\n--- Stars line-END 'other'-onset words ---")
    stars_last_other = []
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in stars_folios: continue
        if words and get_onset(words[-1]) == 'other':
            stars_last_other.append(words[-1])
    last_other_cnt = Counter(stars_last_other)
    n_last_other = len(stars_last_other)
    print(f"  Lines ending with 'other' onset: {n_last_other}/{total_lines} ({n_last_other/total_lines:.3f})")
    for w, cnt in last_other_cnt.most_common(15):
        suf = get_suffix(w)
        print(f"    {w:15s}: {cnt:3d}  suf={suf}")

    # Compare star-start "other" vs star-end "other" — same words?
    first_set = set(w for w,c in first_other_cnt.most_common(20))
    last_set = set(w for w,c in last_other_cnt.most_common(20))
    overlap = first_set & last_set
    print(f"\n  Overlap (top-20 start vs top-20 end): {overlap}")

    # Do these "other" words appear in labels? (may be proper names if they appear in diagrams)
    print(f"\n--- Top 'other' stars words: onset analysis ---")
    for w, cnt in stars_other_words.most_common(15):
        # Does this word start with known letters suggesting a specific onset?
        first2 = w[:2] if len(w) >= 2 else w
        print(f"  {w:15s}: starts_with={w[0]}  first2={first2}  suf={get_suffix(w)}")

    # Folio-level: which folios have the most "other" starts?
    print(f"\n--- Folio-level 'other' rate at line-start ---")
    folio_first_onset = defaultdict(Counter)
    for (folio_num, line_in_folio), words in line_records.items():
        if folio_num not in stars_folios: continue
        if words:
            folio_first_onset[folio_num][get_onset(words[0])] += 1
    for folio_num in sorted(folio_first_onset.keys()):
        total_f = sum(folio_first_onset[folio_num].values())
        other_f = folio_first_onset[folio_num].get('other', 0)
        d_f = folio_first_onset[folio_num].get('d', 0)
        s_f = folio_first_onset[folio_num].get('s', 0)
        print(f"  f{folio_num}: total={total_f} | other={other_f/total_f:.2f} d={d_f/total_f:.2f} s={s_f/total_f:.2f}")


def main():
    print("Loading records...")
    records, dialect_map, line_records = parse_eva(DATA)
    print(f"Total: {len(records)} records, {len(line_records)} lines")

    h244_onset_grammar(records, dialect_map)
    h242_stars_other(records, dialect_map, line_records)

if __name__ == '__main__':
    main()
