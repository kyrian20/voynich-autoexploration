"""
exp_128: p-Prefix (H254) and r-Prefix (H255) Class Characterization
====================================================================
H254: p-initial words — is p a morphological PREFIX (like y-) or an independent onset?
      p-stripped stems: what onset classes? Section/dialect/position profile.
      Cross-reference with p-onset = B-para-start marker (F057).

H255: r-initial words — is r a morphological PREFIX?
      r-stripped stems; section/dialect/position profile.
      Compared with other prefix classes.
"""

import re
from collections import defaultdict, Counter
import math

SUFFIXES = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am',
            'ol','or','ar','al','ey','dy','y']

def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

def get_onset(word):
    for pat in ['qok','qot','qo','cth','ch','sh','ok','ot','ol','olk','d','s']:
        if word.startswith(pat):
            return pat
    if len(word) >= 1 and word[0] in 'yklrtpf':
        return word[0]
    return 'other'

SECTION_MAP = {}
for f in range(1,   58): SECTION_MAP[f] = 'herbal'
for f in range(67,  74): SECTION_MAP[f] = 'astro'
for f in range(75,  85): SECTION_MAP[f] = 'cosmo'
for f in range(87, 103): SECTION_MAP[f] = 'pharma'
for f in range(103,117): SECTION_MAP[f] = 'stars'

def get_section(fn): return SECTION_MAP.get(fn, 'other')
def parse_folio_num(locus):
    m = re.match(r'f(\d+)', locus)
    return int(m.group(1)) if m else None

def parse_corpus(path):
    raw_lines = []
    folio_word_counts = defaultdict(Counter)
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw, text_raw = m.group(1), m.group(2)
            parts = locus_raw.split(',')
            locus = parts[0]
            locus_type_raw = parts[1] if len(parts) > 1 else ''
            locus_type = locus_type_raw.lstrip('@+*=~&')
            folio_num = parse_folio_num(locus)
            if folio_num is None:
                continue
            if not re.match(r'P', locus_type):
                continue
            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'![\w.;@]*', '', text)
            text = re.sub(r'[*@&~=+$#{}?]', '', text)
            words = [w for w in re.split(r'[-.\s,]+', text)
                     if re.match(r'^[a-z]{2,}$', w)]
            if words:
                raw_lines.append((locus, folio_num, words))
                for w in words:
                    folio_word_counts[folio_num][w] += 1

    dialect_b = {}
    for fnum, cnt in folio_word_counts.items():
        total = sum(cnt.values())
        edy_count = sum(v for w, v in cnt.items() if w.endswith('edy') or w.endswith('eedy'))
        dialect_b[fnum] = (edy_count / total >= 0.05) if total > 0 else False

    records = []
    # Also track paragraph starts
    prev_locus = None
    para_starts = set()  # (folio_num, locus) that are paragraph starts
    for locus, folio_num, words in raw_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus, 'folio_num': folio_num,
            'dialect': dialect, 'section': section, 'words': words,
        })
    return records, folio_word_counts

# ── Generic prefix analyzer ───────────────────────────────────────────────────

def analyze_prefix(prefix_char, records, global_vocab):
    """Characterize words starting with prefix_char (1 char) as morphological prefix."""
    words_data = defaultdict(lambda: {'n':0, 'A':0, 'B':0, 'sections': Counter(),
                                       'positions': []})
    stem_counts = Counter()
    by_dialect = {'A': Counter(), 'B': Counter()}
    by_section = Counter()
    positions = []
    para_positions = []  # line-start within paragraph
    all_vocab = set(w for cnt in global_vocab.values() for w in cnt.keys())

    # Count para-starts by detecting locus type
    # (We approximate paragraph-start as "first word of a line starting with =" in locus type)
    # We use positional info from the records

    for rec in records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w.startswith(prefix_char) and len(w) >= 2 and w != prefix_char:
                stem = w[len(prefix_char):]
                words_data[w]['n'] += 1
                words_data[w][rec['dialect']] += 1
                words_data[w]['sections'][rec['section']] += 1
                stem_counts[stem] += 1
                by_dialect[rec['dialect']][w] += 1
                by_section[rec['section']] += 1
                pos = 'start' if i == 0 else ('end' if i == n-1 else 'mid')
                positions.append(pos)

    all_tokens = sum(d['n'] for d in words_data.values())
    if all_tokens == 0:
        print(f"No {prefix_char}-initial words found.")
        return

    print(f"\n{'='*70}")
    print(f"H25{'4' if prefix_char=='p' else '5'}: {prefix_char.upper()}-PREFIX CLASS CHARACTERIZATION")
    print(f"{'='*70}")
    print(f"\nTotal {prefix_char}-initial tokens: {all_tokens:,}")
    print(f"Unique types: {len(words_data)}")

    a_n = sum(d['A'] for d in words_data.values())
    b_n = sum(d['B'] for d in words_data.values())
    print(f"Dialect: A={a_n:,} ({a_n/all_tokens:.1%}), B={b_n:,} ({b_n/all_tokens:.1%}), A/B={a_n/b_n:.2f}" if b_n else "")

    print(f"\nSection distribution:")
    for sec, cnt in by_section.most_common():
        print(f"  {sec:<10}: {cnt:>5} ({cnt/all_tokens:.1%})")

    print(f"\nPosition distribution:")
    pos_cnt = Counter(positions)
    for p in ['start', 'mid', 'end']:
        cnt = pos_cnt.get(p, 0)
        print(f"  {p:<8}: {cnt:>5} ({cnt/all_tokens:.1%})")

    print(f"\nTop 30 {prefix_char}-initial words:")
    print(f"{'Word':<20} {'n':>5} {'A':>5} {'B':>5} {'B%':>6} {'Herbal%':>8} {'Stars%':>7}")
    print("-" * 62)
    sorted_words = sorted(words_data.items(), key=lambda x: -x[1]['n'])
    for w, d in sorted_words[:30]:
        total = d['n']
        b_frac = d['B'] / total if total else 0
        herbal_frac = d['sections']['herbal'] / total if total else 0
        stars_frac = d['sections']['stars'] / total if total else 0
        print(f"{w:<20} {total:>5} {d['A']:>5} {d['B']:>5} {b_frac:>5.1%} {herbal_frac:>7.1%} {stars_frac:>6.1%}")

    # Stem recovery: what % of stripped stems appear in vocabulary?
    stems_in_vocab = sum(cnt for stem, cnt in stem_counts.items() if stem in all_vocab)
    total_tokens_with_stem = all_tokens  # every p-word has a stem
    print(f"\nStem recovery: {stems_in_vocab/all_tokens:.1%} ({stems_in_vocab}/{all_tokens} tokens have stem in vocab)")

    # Stem onset distribution
    stem_onset = Counter()
    for stem, cnt in stem_counts.items():
        stem_onset[get_onset(stem)] += cnt
    total_stem = sum(stem_onset.values())
    print(f"\nStem onset distribution (after stripping {prefix_char}-):")
    for onset, cnt in stem_onset.most_common(10):
        print(f"  {onset:<8}: {cnt:>5} ({cnt/total_stem:.1%})")

    # Top stems
    print(f"\nTop 20 {prefix_char}-stripped stems:")
    for stem, cnt in stem_counts.most_common(20):
        in_vocab = '✓' if stem in all_vocab else '✗'
        print(f"  {prefix_char}+{stem:<16} {in_vocab}  onset={get_onset(stem):<6}  n={cnt}")

    # A vs B vocabulary
    a_types = set(by_dialect['A'].keys())
    b_types = set(by_dialect['B'].keys())
    j = len(a_types & b_types) / len(a_types | b_types) if (a_types | b_types) else 0
    print(f"\nA-{prefix_char} types: {len(a_types)}, B-{prefix_char} types: {len(b_types)}, Jaccard={j:.3f}")
    print(f"A-exclusive (top 10): {sorted(a_types - b_types, key=lambda x: -by_dialect['A'][x])[:10]}")
    print(f"B-exclusive (top 10): {sorted(b_types - a_types, key=lambda x: -by_dialect['B'][x])[:10]}")

    # Suffix distribution
    suf_cnt = Counter()
    for w, d in words_data.items():
        suf_cnt[get_suffix(w)] += d['n']
    print(f"\nSuffix distribution of {prefix_char}-initial words:")
    for suf, cnt in suf_cnt.most_common(10):
        print(f"  -{suf:<8}: {cnt:>5} ({cnt/all_tokens:.1%})")

    # Para-start analysis: does this prefix appear at paragraph starts?
    # Approximate: look at line-start rate vs baseline
    # Baseline line-start rate for all words
    all_positions = []
    for rec in records:
        n = len(rec['words'])
        for i in range(n):
            all_positions.append('start' if i==0 else ('end' if i==n-1 else 'mid'))
    all_start_rate = sum(1 for p in all_positions if p=='start') / len(all_positions)
    this_start_rate = pos_cnt.get('start', 0) / all_tokens
    start_enrich = this_start_rate / all_start_rate if all_start_rate > 0 else 0
    print(f"\nLine-start rate: {this_start_rate:.1%} vs baseline {all_start_rate:.1%} → {start_enrich:.2f}× enrichment")

    return words_data, stem_counts

# ── Para-start analysis specific to p-onset ──────────────────────────────────

def analyze_p_para_starts(records):
    """Analyze p-onset words at paragraph starts vs continuation lines.
    A paragraph start line has locus type starting with '=' (new paragraph)."""
    # Reconstruct locus type from the raw file
    corpus_path = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

    para_start_loci = set()
    with open(corpus_path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_raw = m.group(1)
            parts = locus_raw.split(',')
            locus = parts[0]
            locus_type_raw = parts[1] if len(parts) > 1 else ''
            lt = locus_type_raw.lstrip('@+*=~&')
            # Para start: locus type starts with nothing (=P0 stripped) vs +P0
            # In IVTFF: = means new paragraph, + means continuation
            original_prefix = ''
            for c in locus_type_raw:
                if c in '@+*=~&':
                    original_prefix += c
                else:
                    break
            if '=' in original_prefix and 'P' in lt:
                para_start_loci.add(locus)

    print(f"\n--- Para-start analysis (p-prefix) ---")
    print(f"Identified {len(para_start_loci)} paragraph-start loci")

    p_at_para = Counter()
    p_at_cont = Counter()
    for rec in records:
        words = rec['words']
        if not words:
            continue
        first_word = words[0]
        if rec['locus'] in para_start_loci:
            target = p_at_para
        else:
            target = p_at_cont
        if first_word.startswith('p') and len(first_word) >= 2:
            target[first_word] += 1

    total_para = sum(p_at_para.values())
    total_cont = sum(p_at_cont.values())
    total_para_lines = sum(1 for r in records if r['locus'] in para_start_loci)
    total_cont_lines = len(records) - total_para_lines

    print(f"Para-start lines: {total_para_lines}")
    print(f"  p-words as first word: {total_para} ({total_para/total_para_lines:.1%})")
    print(f"Continuation lines: {total_cont_lines}")
    print(f"  p-words as first word: {total_cont} ({total_cont/total_cont_lines:.1%})")
    if total_cont_lines > 0 and total_cont > 0:
        enrich = (total_para/total_para_lines) / (total_cont/total_cont_lines)
        print(f"  Para-start enrichment of p-words: {enrich:.2f}×")

    print(f"Top p-words at para-starts: {p_at_para.most_common(10)}")
    print(f"Top p-words at continuation: {p_at_cont.most_common(10)}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
    print("Loading corpus...")
    records, global_vocab = parse_corpus(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words:,} word tokens")

    # p-prefix analysis
    p_data, p_stems = analyze_prefix('p', records, global_vocab)
    analyze_p_para_starts(records)

    # r-prefix analysis
    r_data, r_stems = analyze_prefix('r', records, global_vocab)

    # Compare p and r to y prefix class (already known from exp_127)
    print(f"\n{'='*70}")
    print("COMPARISON: p / r / y PREFIX CLASSES")
    print(f"{'='*70}")
    print(f"{'Prefix':<8} {'Tokens':>7} {'A/B':>6} {'LineStart%':>11} {'StemRec':>8} {'TopStem':>10}")
    print("-" * 55)
    # y from exp_127: 1372 tokens, ratio=0.81, start=39.6%, stemrec=85.6%
    print(f"{'y':<8} {1372:>7} {'0.81':>6} {'39.6%':>11} {'85.6%':>8} {'k/t 65%':>10}")
    # p and r will be computed above
