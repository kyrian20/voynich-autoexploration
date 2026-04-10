"""
exp_127: Full A-Dialect Line Template 4-gram (H253) + aiin→am Construction (H252) + y-Prefix Characterization (H251)
=====================================================================================================================
H253: Is [-or/-ol][daiin][cth-onset][-am/-dy/-al] the canonical A-dialect 4-word sentence?
      Search for 4-grams matching this template; compute enrichment vs random.

H252: What specific word pairs drive the aiin→am=4.62× bigram? Is [daiin][dam] a fixed phrase?
      Tabulate top [word_aiin][word_am] bigrams; count occurrences; section/folio distribution.

H251: y-prefix class full characterization — what are the 1374 y-words?
      y-stripped stem distribution; dialect/section/position profile; A-y vs B-y sub-types.
"""

import re
from collections import defaultdict, Counter

# ── suffix/onset/section utilities ──────────────────────────────────────────

SUFFIXES = ['eeedy','eeey','eedy','edy','eey','aiin','ain','air','am',
            'ol','or','ar','al','ey','dy','y']

def get_suffix(word):
    for s in SUFFIXES:
        if word.endswith(s) and len(word) > len(s):
            return s
    return 'other'

def has_suffix(word, suf):
    return word.endswith(suf) and len(word) > len(suf)

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

# ── corpus parser ─────────────────────────────────────────────────────────────

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
    for locus, folio_num, words in raw_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus, 'folio_num': folio_num,
            'dialect': dialect, 'section': section, 'words': words,
        })
    return records

# ── H252: aiin→am construction ───────────────────────────────────────────────

def analyze_aiin_am(records):
    print("=" * 70)
    print("H252: aiin→am CONSTRUCTION — WHAT SPECIFIC WORD PAIRS DRIVE 4.62×?")
    print("=" * 70)

    # Collect all word bigrams within lines where W1 has -aiin and W2 has -am
    aiin_am_pairs = Counter()
    aiin_am_lines = []
    aiin_am_section = Counter()

    # Also collect all bigrams for enrichment baseline
    total_bigrams = 0
    aiin_total = Counter()  # all W2 after aiin-words
    am_baseline = Counter()  # all words with -am suffix

    for rec in records:
        words = rec['words']
        n = len(words)
        for i in range(n - 1):
            w1, w2 = words[i], words[i+1]
            total_bigrams += 1
            s1, s2 = get_suffix(w1), get_suffix(w2)
            if s1 == 'aiin':
                aiin_total[s2] += 1
                if s2 == 'am':
                    aiin_am_pairs[(w1, w2)] += 1
                    aiin_am_section[rec['section']] += 1
                    aiin_am_lines.append({
                        'folio': rec['folio_num'],
                        'section': rec['section'],
                        'dialect': rec['dialect'],
                        'w1': w1, 'w2': w2,
                        'context': words[max(0,i-1):min(n,i+3)]
                    })

    # am baseline
    total_words = sum(len(r['words']) for r in records)
    am_words = Counter()
    for rec in records:
        for w in rec['words']:
            if has_suffix(w, 'am'):
                am_words[w] += 1

    print(f"\nTotal [aiin-word][am-word] bigrams: {sum(aiin_am_pairs.values())}")
    print(f"Unique pairs: {len(aiin_am_pairs)}")
    print(f"\nTop aiin→am word pairs:")
    for (w1,w2), cnt in aiin_am_pairs.most_common(20):
        print(f"  {w1:<15} → {w2:<15}  n={cnt}")

    print(f"\nSection distribution of aiin→am bigrams:")
    total = sum(aiin_am_section.values())
    for sec, cnt in aiin_am_section.most_common():
        print(f"  {sec:<10}: {cnt:>4} ({cnt/total:.1%})")

    # What follows daiin specifically?
    print(f"\nWhat follows 'daiin' (top next-word by onset class)?")
    daiin_next = Counter()
    daiin_next_word = Counter()
    daiin_next_am = []
    for rec in records:
        words = rec['words']
        for i, w in enumerate(words[:-1]):
            if w == 'daiin':
                nxt = words[i+1]
                daiin_next[get_suffix(nxt)] += 1
                daiin_next_word[nxt] += 1
                if has_suffix(nxt, 'am'):
                    daiin_next_am.append({
                        'context': words[max(0,i-1):min(len(words),i+3)],
                        'folio': rec['folio_num'],
                        'section': rec['section']
                    })

    daiin_total = sum(daiin_next.values())
    print(f"  Total post-daiin words: {daiin_total}")
    for s, cnt in daiin_next.most_common(8):
        print(f"  Suffix -{s:<8}: {cnt:>4} ({cnt/daiin_total:.1%})")
    print(f"  Top next words: " + ", ".join(f"{w}({c})" for w,c in daiin_next_word.most_common(10)))
    print(f"  daiin→am bigrams: {len(daiin_next_am)}")
    if daiin_next_am:
        print(f"  Top daiin→am contexts:")
        for ex in daiin_next_am[:10]:
            print(f"    f{ex['folio']} [{ex['section']}]: {' '.join(ex['context'])}")

    return aiin_am_pairs

# ── H253: Full 4-gram A-dialect line template ─────────────────────────────────

def analyze_4gram_template(records):
    print()
    print("=" * 70)
    print("H253: FULL A-DIALECT 4-GRAM TEMPLATE: [-ol/-or][daiin][cth-word][-am/-dy/-al]")
    print("=" * 70)

    # Count 4-grams matching the template
    template_4gram = Counter()
    template_3gram = Counter()  # W1 W2 W3 only (F128 confirmed)
    template_context = []

    # Also compute all 4-gram counts for baseline
    all_4gram_patterns = Counter()
    all_3gram_patterns = Counter()

    for rec in records:
        if rec['dialect'] != 'A':
            continue
        words = rec['words']
        n = len(words)

        for i in range(n - 2):
            w1, w2, w3 = words[i], words[i+1], words[i+2]
            s1 = get_suffix(w1)
            o3 = get_onset(w3)
            all_3gram_patterns[(s1, w2, o3 == 'cth')] += 1

            # 3-gram match: [-ol/-or][daiin-like][cth-word]
            if s1 in ('ol','or') and get_suffix(w2) == 'aiin' and o3 == 'cth':
                template_3gram[(w1, w2, w3)] += 1

            # 4-gram
            if i < n - 3:
                w4 = words[i+3]
                s4 = get_suffix(w4)
                all_4gram_patterns[(s1, w2, o3 == 'cth', s4)] += 1
                if s1 in ('ol','or') and get_suffix(w2) == 'aiin' and o3 == 'cth' and s4 in ('am','dy','al'):
                    template_4gram[(w1, w2, w3, w4)] += 1
                    template_context.append({
                        'folio': rec['folio_num'],
                        'section': rec['section'],
                        'words': [w1, w2, w3, w4],
                        'full_context': words[max(0,i-1):min(n,i+5)]
                    })

    total_3gram = sum(1 for rec in records if rec['dialect']=='A'
                      for i in range(len(rec['words'])-2))
    total_4gram = sum(1 for rec in records if rec['dialect']=='A'
                      for i in range(len(rec['words'])-3))

    print(f"\n3-gram template matches [-ol/-or][aiin-word][cth-onset]: {sum(template_3gram.values())}")
    print(f"Total A-dialect 3-grams: {total_3gram:,}")
    if total_3gram > 0:
        obs_rate = sum(template_3gram.values()) / total_3gram
        # baseline: P(s1 in ol/or) * P(w2=daiin-type) * P(cth-onset)
        print(f"Observed rate: {obs_rate:.4%}")
    print(f"\nTop 3-gram instances:")
    for (w1,w2,w3), cnt in template_3gram.most_common(15):
        print(f"  {w1:<12} {w2:<12} {w3:<12}  n={cnt}")

    print(f"\n4-gram template matches [-ol/-or][aiin][cth][-am/-dy/-al]: {sum(template_4gram.values())}")
    print(f"Total A-dialect 4-grams: {total_4gram:,}")
    if template_4gram:
        print(f"\nTop 4-gram instances:")
        for (w1,w2,w3,w4), cnt in template_4gram.most_common(20):
            print(f"  {w1:<12} {w2:<12} {w3:<12} {w4:<12}  n={cnt}")

        print(f"\nSample contexts:")
        for ex in template_context[:15]:
            print(f"  f{ex['folio']} [{ex['section']}]: {' '.join(ex['full_context'])}")
            print(f"    → MATCH: {' '.join(ex['words'])}")

    # Compute enrichment: how often does the 4-gram appear vs expectation?
    # Independence baseline: P(s1=ol/or) * P(s2=aiin) * P(o3=cth) * P(s4=am/dy/al)
    print(f"\nIndependence baseline computation (A-dialect):")
    a_words = [w for rec in records if rec['dialect']=='A' for w in rec['words']]
    a_total = len(a_words)
    a_suf_counts = Counter(get_suffix(w) for w in a_words)
    a_onset_counts = Counter(get_onset(w) for w in a_words)
    p_ol_or = (a_suf_counts['ol'] + a_suf_counts['or']) / a_total
    p_aiin  = a_suf_counts['aiin'] / a_total
    p_cth   = a_onset_counts['cth'] / a_total
    p_am_dy_al = (a_suf_counts['am'] + a_suf_counts['dy'] + a_suf_counts['al']) / a_total
    expected_rate = p_ol_or * p_aiin * p_cth * p_am_dy_al
    obs_4gram_n = sum(template_4gram.values())
    obs_4gram_rate = obs_4gram_n / total_4gram if total_4gram > 0 else 0
    print(f"  P(-ol/-or)={p_ol_or:.4f}, P(-aiin)={p_aiin:.4f}, P(cth-onset)={p_cth:.4f}, P(-am/-dy/-al)={p_am_dy_al:.4f}")
    print(f"  Expected (independence): {expected_rate:.6f} = {expected_rate*total_4gram:.1f} 4-grams")
    print(f"  Observed: {obs_4gram_n} 4-grams ({obs_4gram_rate:.6f})")
    if expected_rate > 0:
        enrich = obs_4gram_rate / expected_rate
        print(f"  Enrichment: {enrich:.2f}×")

    # Lines containing full template
    lines_with_template = set()
    for ex in template_context:
        lines_with_template.add(ex['folio'])
    a_lines = [rec for rec in records if rec['dialect']=='A']
    print(f"\nA-dialect lines tested: {len(a_lines)}")
    print(f"Lines containing template 4-gram: {sum(template_4gram.values())} occurrences in {len(template_context)} line-positions")

    return template_4gram, template_context

# ── H251: y-prefix characterization ─────────────────────────────────────────

def analyze_y_prefix(records):
    print()
    print("=" * 70)
    print("H251: y-PREFIX CLASS CHARACTERIZATION")
    print("=" * 70)

    y_words = defaultdict(lambda: {'n': 0, 'A': 0, 'B': 0, 'sections': Counter(),
                                    'positions': []})
    y_stems = Counter()
    y_by_dialect = {'A': Counter(), 'B': Counter()}
    y_by_section = Counter()
    y_positions = []  # 0=line-start, 1=other, -1=line-end

    for rec in records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w.startswith('y') and len(w) >= 2 and w != 'y':
                stem = w[1:]  # strip y prefix
                y_words[w]['n'] += 1
                y_words[w][rec['dialect']] += 1
                y_words[w]['sections'][rec['section']] += 1
                y_stems[stem] += 1
                y_by_dialect[rec['dialect']][w] += 1
                y_by_section[rec['section']] += 1
                pos = 'start' if i == 0 else ('end' if i == n-1 else 'mid')
                y_positions.append(pos)

    all_y_tokens = sum(d['n'] for d in y_words.values())
    print(f"\nTotal y-initial words (≥2 chars, excluding 'y'): {all_y_tokens:,}")
    print(f"Unique y-word types: {len(y_words)}")

    print(f"\nTop 30 y-initial words:")
    print(f"{'Word':<18} {'n':>5} {'A':>5} {'B':>5} {'B%':>6} {'Herbal%':>8} {'Stars%':>7}")
    print("-" * 60)
    sorted_y = sorted(y_words.items(), key=lambda x: -x[1]['n'])
    for w, d in sorted_y[:30]:
        a, b = d['A'], d['B']
        total = d['n']
        b_frac = b / total if total else 0
        herbal_frac = d['sections']['herbal'] / total if total else 0
        stars_frac = d['sections']['stars'] / total if total else 0
        print(f"{w:<18} {total:>5} {a:>5} {b:>5} {b_frac:>5.1%} {herbal_frac:>7.1%} {stars_frac:>6.1%}")

    print(f"\ny-word dialect distribution:")
    a_n = sum(d['A'] for d in y_words.values())
    b_n = sum(d['B'] for d in y_words.values())
    print(f"  A-dialect: {a_n:,} tokens ({a_n/all_y_tokens:.1%})")
    print(f"  B-dialect: {b_n:,} tokens ({b_n/all_y_tokens:.1%})")
    print(f"  A/B ratio: {a_n/b_n:.2f}" if b_n else "  B: 0")

    print(f"\ny-word section distribution:")
    for sec, cnt in y_by_section.most_common():
        print(f"  {sec:<10}: {cnt:>5} ({cnt/all_y_tokens:.1%})")

    print(f"\ny-word positional distribution:")
    pos_counter = Counter(y_positions)
    total_pos = len(y_positions)
    for pos in ['start', 'mid', 'end']:
        cnt = pos_counter.get(pos, 0)
        print(f"  {pos:<8}: {cnt:>5} ({cnt/total_pos:.1%})")

    print(f"\nTop 20 y-stripped stems:")
    for stem, cnt in y_stems.most_common(20):
        onset = get_onset(stem)
        print(f"  y+{stem:<16} → stem onset: {onset:<6}  n={cnt}")

    # Stem onset distribution
    stem_onset_dist = Counter()
    for stem, cnt in y_stems.items():
        stem_onset_dist[get_onset(stem)] += cnt
    print(f"\nStem onset distribution (after stripping y-):")
    total_y = sum(stem_onset_dist.values())
    for onset, cnt in stem_onset_dist.most_common(10):
        print(f"  {onset:<8}: {cnt:>5} ({cnt/total_y:.1%})")

    # A-y vs B-y vocabulary
    a_types = set(y_by_dialect['A'].keys())
    b_types = set(y_by_dialect['B'].keys())
    j = len(a_types & b_types) / len(a_types | b_types) if (a_types | b_types) else 0
    print(f"\nA-y types: {len(a_types)}, B-y types: {len(b_types)}, Jaccard={j:.3f}")
    print(f"A-exclusive y types (top 10): {sorted(a_types - b_types, key=lambda x: -y_by_dialect['A'][x])[:10]}")
    print(f"B-exclusive y types (top 10): {sorted(b_types - a_types, key=lambda x: -y_by_dialect['B'][x])[:10]}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
    print(f"Loading corpus...")
    records = parse_corpus(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words:,} word tokens")
    a_recs = [r for r in records if r['dialect']=='A']
    b_recs = [r for r in records if r['dialect']=='B']
    print(f"A-dialect: {sum(len(r['words']) for r in a_recs):,} words | B-dialect: {sum(len(r['words']) for r in b_recs):,} words")

    analyze_aiin_am(records)
    analyze_4gram_template(records)
    analyze_y_prefix(records)
