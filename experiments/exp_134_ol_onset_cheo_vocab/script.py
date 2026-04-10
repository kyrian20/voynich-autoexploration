#!/usr/bin/env python3
"""
exp_134: ol-Onset Characterization (H262) + Stars ch+eo Vocabulary (H263)

H262: Is ol-onset a distinct onset class with sub-classes? Cosmo=2.06× corpus.
H263: Are cheo/cheody/cheeo stars-exclusive ch+eo morphological sub-class?
"""

import re
import math
from collections import defaultdict, Counter

CORPUS_PATH = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_CLASSES = [
    'qok', 'qot', 'qo',
    'cth', 'ch', 'sh',
    'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f',
    'other'
]

SUFFIX_LIST = ['eeedy', 'eeey', 'eedy', 'edy', 'eey', 'aiin', 'ain', 'air',
               'am', 'ol', 'or', 'ar', 'al', 'ey', 'dy', 'y']

def folio_to_section(f):
    if 1 <= f <= 57:    return 'herbal'
    elif 67 <= f <= 73: return 'astro'
    elif 75 <= f <= 84: return 'cosmo'
    elif 87 <= f <= 102: return 'pharma'
    elif 103 <= f <= 116: return 'stars'
    return None

def get_onset(word):
    w = word.lower()
    for cls in ONSET_CLASSES[:-1]:
        if w.startswith(cls):
            return cls
    return 'other'

def get_suffix(word):
    w = word.lower()
    for s in SUFFIX_LIST:
        if w.endswith(s) and len(w) > len(s):
            return s
    return 'other'

def parse_corpus(path):
    records = []
    folio_word_counts = defaultdict(lambda: defaultdict(int))

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^>]+)>(.*)', line)
            if not m:
                continue
            locus_code, text_raw = m.group(1), m.group(2)
            parts = locus_code.split(',')
            if len(parts) < 2:
                continue
            locus_type_raw = parts[1]
            locus_type = locus_type_raw.lstrip('@+*=~&')
            if not re.match(r'P', locus_type):
                continue

            folio_str = parts[0]
            fm = re.search(r'(\d+)', folio_str)
            if not fm:
                continue
            folio_num = int(fm.group(1))
            section = folio_to_section(folio_num)
            if not section:
                continue

            text = re.sub(r'<[^>]*>', '', text_raw)
            text = re.sub(r'\[[^\]]*\]', ' ', text)
            text = re.sub(r'[*@&~=+$#{}?!]', '', text)
            text = text.replace('-', ' ').replace('.', ' ').replace(',', ' ')
            words = [w for w in text.lower().split() if re.match(r'^[a-z]{2,}$', w)]
            if not words:
                continue

            for w in words:
                folio_word_counts[folio_num][w] += 1

            records.append({
                'folio': folio_num,
                'section': section,
                'words': words,
            })

    folio_dialect = {}
    for folio, wc in folio_word_counts.items():
        total = sum(wc.values())
        edy = sum(v for w, v in wc.items() if w.endswith('edy') or w.endswith('eedy'))
        folio_dialect[folio] = 'B' if total > 0 and edy / total >= 0.05 else 'A'

    for r in records:
        r['dialect'] = folio_dialect.get(r['folio'], 'A')

    return records, folio_dialect


def analyze_ol_onset(records):
    """H262: Characterize ol-onset words."""
    print("=" * 70)
    print("H262: ol-ONSET CHARACTERIZATION")
    print("=" * 70)

    # Collect all words with metadata
    all_word_data = []
    for r in records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            all_word_data.append({
                'word': w,
                'onset': get_onset(w),
                'suffix': get_suffix(w),
                'is_lf': (i == 0),
                'is_ll': (i == n - 1),
                'is_mid': (0 < i < n - 1),
                'frac': i / max(n - 1, 1),
                'section': r['section'],
                'dialect': r['dialect'],
                'folio': r['folio'],
            })

    ol_words = [w for w in all_word_data if w['onset'] == 'ol']
    total_tokens = len(ol_words)
    word_counter = Counter(w['word'] for w in ol_words)
    total_types = len(word_counter)
    hapax = sum(1 for w, c in word_counter.items() if c == 1)

    lf = sum(1 for w in ol_words if w['is_lf'])
    ll = sum(1 for w in ol_words if w['is_ll'])
    mid = sum(1 for w in ol_words if w['is_mid'])

    section_counts = Counter(w['section'] for w in ol_words)
    dialect_counts = Counter(w['dialect'] for w in ol_words)

    corpus_total = len(all_word_data)
    corpus_section = Counter(w['section'] for w in all_word_data)
    corpus_dialect = Counter(w['dialect'] for w in all_word_data)
    corpus_onset = Counter(w['onset'] for w in all_word_data)

    print(f"\nTotal ol-onset tokens: {total_tokens}")
    print(f"Total ol-onset types: {total_types}")
    print(f"Hapax legomena: {hapax} ({100*hapax/total_types:.1f}%)")

    print(f"\nPositional profile:")
    print(f"  Line-first (LF): {lf} ({100*lf/total_tokens:.1f}%)")
    print(f"  Mid-line (MID):  {mid} ({100*mid/total_tokens:.1f}%)")
    print(f"  Line-last (LL):  {ll} ({100*ll/total_tokens:.1f}%)")

    print(f"\nSection distribution (with enrichment):")
    for s in ['herbal', 'pharma', 'stars', 'cosmo', 'astro']:
        n_s = section_counts.get(s, 0)
        base = corpus_section.get(s, 0) / corpus_total
        obs = n_s / total_tokens
        enrich = obs / base if base > 0 else 0
        print(f"  {s:<8}: {n_s:>4} ({100*obs:.1f}%)  base={100*base:.1f}%  enrich={enrich:.2f}×")

    print(f"\nDialect distribution:")
    for d in ['A', 'B']:
        n_d = dialect_counts.get(d, 0)
        base = corpus_dialect.get(d, 0) / corpus_total
        obs = n_d / total_tokens
        enrich = obs / base if base > 0 else 0
        print(f"  {d}: {n_d} ({100*obs:.1f}%)  corpus={100*base:.1f}%  enrich={enrich:.2f}×")

    # Top ol-words with profiles
    print(f"\n### Top ol-Onset Words (top 30)")
    print(f"{'Word':<16} {'n':>5} {'LF%':>6} {'MID%':>6} {'LL%':>6} {'Cosmo%':>8} {'Stars%':>8} {'B%':>6}")
    for word, count in word_counter.most_common(30):
        ws = [w for w in ol_words if w['word'] == word]
        lf_r = sum(1 for w in ws if w['is_lf']) / len(ws)
        ll_r = sum(1 for w in ws if w['is_ll']) / len(ws)
        mid_r = sum(1 for w in ws if w['is_mid']) / len(ws)
        cosmo_r = sum(1 for w in ws if w['section'] == 'cosmo') / len(ws)
        stars_r = sum(1 for w in ws if w['section'] == 'stars') / len(ws)
        b_r = sum(1 for w in ws if w['dialect'] == 'B') / len(ws)
        suf = get_suffix(word)
        print(f"{word:<16} {count:>5} {100*lf_r:>5.1f}% {100*mid_r:>5.1f}% {100*ll_r:>5.1f}% {100*cosmo_r:>7.1f}% {100*stars_r:>7.1f}% {100*b_r:>5.1f}%")

    # Sub-class analysis
    print(f"\n### ol-Onset Sub-Classes by Positional Role")
    word_profile = {}
    for word, count in word_counter.items():
        if count < 3:
            continue
        ws = [w for w in ol_words if w['word'] == word]
        lf_r = sum(1 for w in ws if w['is_lf']) / len(ws)
        ll_r = sum(1 for w in ws if w['is_ll']) / len(ws)
        mid_r = sum(1 for w in ws if w['is_mid']) / len(ws)
        b_r = sum(1 for w in ws if w['dialect'] == 'B') / len(ws)
        cosmo_r = sum(1 for w in ws if w['section'] == 'cosmo') / len(ws)
        word_profile[word] = (count, lf_r, mid_r, ll_r, b_r, cosmo_r)

    openers = [(w, *p) for w, p in word_profile.items() if p[1] >= 0.35]
    closers = [(w, *p) for w, p in word_profile.items() if p[3] >= 0.25 and p[1] < 0.35]
    medials = [(w, *p) for w, p in word_profile.items()
               if p[2] >= 0.55 and p[1] < 0.35 and p[3] < 0.25]

    print(f"\nol-OPENERS (LF≥35%, n≥3): {len(openers)} types")
    for w, c, lf, mid, ll, b, cosmo in sorted(openers, key=lambda x: -x[2])[:10]:
        print(f"  {w:<16} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%  B={100*b:.0f}%  cosmo={100*cosmo:.0f}%")

    print(f"\nol-CLOSERS (LL≥25%, LF<35%, n≥3): {len(closers)} types")
    for w, c, lf, mid, ll, b, cosmo in sorted(closers, key=lambda x: -x[4])[:10]:
        print(f"  {w:<16} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%  B={100*b:.0f}%  cosmo={100*cosmo:.0f}%")

    print(f"\nol-MEDIALS (MID≥55%, n≥3): {len(medials)} types")
    for w, c, lf, mid, ll, b, cosmo in sorted(medials, key=lambda x: -x[3])[:10]:
        print(f"  {w:<16} n={c:>4}  LF={100*lf:.0f}%  MID={100*mid:.0f}%  LL={100*ll:.0f}%  B={100*b:.0f}%  cosmo={100*cosmo:.0f}%")

    # Suffix distribution
    print(f"\n### ol-Onset Suffix Distribution")
    suffix_counts = Counter(get_suffix(w['word']) for w in ol_words)
    for s, n in suffix_counts.most_common(12):
        print(f"  {s:<10} {n:>5} ({100*n/total_tokens:.1f}%)")

    # Bigram context
    print(f"\n### Bigram Context: Pre-ol and Post-ol Onset Enrichment")
    pre_ol = Counter()
    post_ol = Counter()
    total_pre = total_post = 0

    for r in records:
        ws = r['words']
        onsets = [get_onset(w) for w in ws]
        for i, onset in enumerate(onsets):
            if onset != 'ol':
                continue
            if i > 0:
                pre_ol[onsets[i-1]] += 1
                total_pre += 1
            if i < len(onsets) - 1:
                post_ol[onsets[i+1]] += 1
                total_post += 1

    corpus_onset_frac = {cls: corpus_onset.get(cls, 0) / corpus_total for cls in ONSET_CLASSES}

    print("\nPre-ol onset enrichment:")
    print(f"{'Onset':<10} {'n':>5} {'obs%':>8} {'base%':>8} {'enrich':>8}")
    for cls, n in pre_ol.most_common(10):
        obs = n / total_pre
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"{cls:<10} {n:>5} {100*obs:>7.2f}% {100*base:>7.2f}% {enrich:>7.2f}×")

    print("\nPost-ol onset enrichment:")
    print(f"{'Onset':<10} {'n':>5} {'obs%':>8} {'base%':>8} {'enrich':>8}")
    for cls, n in post_ol.most_common(10):
        obs = n / total_post
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"{cls:<10} {n:>5} {100*obs:>7.2f}% {100*base:>7.2f}% {enrich:>7.2f}×")

    # Is ol = o-prefix on l-stem?
    print(f"\n### Morphological Analysis: Is ol = o-prefix on l-stems?")
    ol_stripped = Counter()
    for word, count in word_counter.items():
        if word.startswith('ol') and len(word) > 2:
            stripped = word[2:]  # remove 'ol' prefix
            ol_stripped[stripped] += count

    # Check if stripped forms appear in vocabulary
    all_vocab = Counter(w['word'] for w in all_word_data)
    # l-initial stems
    l_initial = {w: c for w, c in all_vocab.items() if w.startswith('l') and not w.startswith('ol')}

    print(f"Top ol-stripped stems:")
    for stem, count in ol_stripped.most_common(15):
        in_vocab = stem in all_vocab
        l_form = 'l' + stem if ('l' + stem) in all_vocab else None
        print(f"  ol+{stem:<12} n={count:>4}  bare_stem_in_vocab={in_vocab}  l+stem={l_form}")

    # Compare: do common ol-words have l-versions?
    print(f"\nol-word vs l-equivalent:")
    for word, count in word_counter.most_common(10):
        stripped = word[2:] if word.startswith('ol') else ''
        if stripped:
            l_ver = 'l' + stripped
            o_ver = 'o' + stripped
            l_count = all_vocab.get(l_ver, 0)
            bare_count = all_vocab.get(stripped, 0)
            print(f"  {word:<14} n={count:>4}  l-ver='{l_ver}'(n={l_count})  bare='{stripped}'(n={bare_count})")


def analyze_cheo_vocabulary(records):
    """H263: Characterize the ch+eo stars-exclusive vocabulary."""
    print("\n\n" + "=" * 70)
    print("H263: STARS ch+eo VOCABULARY CHARACTERIZATION")
    print("=" * 70)

    # All word data
    all_word_data = []
    for r in records:
        ws = r['words']
        n = len(ws)
        for i, w in enumerate(ws):
            all_word_data.append({
                'word': w,
                'onset': get_onset(w),
                'suffix': get_suffix(w),
                'is_lf': (i == 0),
                'is_ll': (i == n - 1),
                'is_mid': (0 < i < n - 1),
                'frac': i / max(n - 1, 1),
                'section': r['section'],
                'dialect': r['dialect'],
            })

    corpus_total = len(all_word_data)
    corpus_section = Counter(w['section'] for w in all_word_data)
    all_vocab = Counter(w['word'] for w in all_word_data)

    # Define the cheo pattern: words with ch-onset containing 'e*o' pattern
    # cheo, cheeo, cheody, chody, cho, chos, cheos, sheody, sheo, shody, sho
    def is_cheo_pattern(word):
        """ch/sh-onset words ending in o, ody, or containing eo sub-sequence."""
        w = word.lower()
        if w.startswith('ch') or w.startswith('sh'):
            stem = w[2:]
            # Pattern: contains 'e*o' or ends in 'o' or 'ody' or 'os'
            if re.search(r'e*o', stem):
                return True
        return False

    def get_eo_class(word):
        """Classify ch/sh+eo words by pattern."""
        w = word.lower()
        if w.startswith('sh'):
            base = 'sh'
            stem = w[2:]
        elif w.startswith('ch'):
            base = 'ch'
            stem = w[2:]
        else:
            return None

        if stem.startswith('eeeo'):
            return f'{base}+eeeo'
        elif stem.startswith('eeo'):
            return f'{base}+eeo'
        elif stem.startswith('eo'):
            return f'{base}+eo'
        elif stem == 'o' or stem.startswith('o'):
            return f'{base}+o'
        return f'{base}+{stem[:3]}'

    # Extract ch/sh-eo words
    cheo_words = [w for w in all_word_data
                  if is_cheo_pattern(w['word'])]

    # Also extract ALL ch/sh words to compare
    ch_words = [w for w in all_word_data if w['onset'] == 'ch']
    sh_words = [w for w in all_word_data if w['onset'] == 'sh']

    print(f"\nTotal ch/sh-eo words: {len(cheo_words)}")
    print(f"Total ch-onset words: {len(ch_words)}")
    print(f"Total sh-onset words: {len(sh_words)}")

    if not cheo_words:
        print("No ch+eo words found with current pattern.")
        return

    # Section distribution
    section_counts = Counter(w['section'] for w in cheo_words)
    total_cheo = len(cheo_words)

    print(f"\nSection distribution (ch/sh+eo words):")
    for s in ['herbal', 'pharma', 'stars', 'cosmo', 'astro']:
        n_s = section_counts.get(s, 0)
        base = corpus_section.get(s, 0) / corpus_total
        obs = n_s / total_cheo if total_cheo > 0 else 0
        enrich = obs / base if base > 0 else 0
        print(f"  {s:<8}: {n_s:>4} ({100*obs:.1f}%)  base={100*base:.1f}%  enrich={enrich:.2f}×")

    # Positional profile
    lf = sum(1 for w in cheo_words if w['is_lf'])
    ll = sum(1 for w in cheo_words if w['is_ll'])
    mid = sum(1 for w in cheo_words if w['is_mid'])
    dialect_counts = Counter(w['dialect'] for w in cheo_words)

    print(f"\nPositional profile (ch/sh+eo words):")
    print(f"  LF={100*lf/total_cheo:.1f}%  MID={100*mid/total_cheo:.1f}%  LL={100*ll/total_cheo:.1f}%")
    print(f"  Dialect: A={dialect_counts.get('A',0)} ({100*dialect_counts.get('A',0)/total_cheo:.1f}%),  B={dialect_counts.get('B',0)} ({100*dialect_counts.get('B',0)/total_cheo:.1f}%)")

    # Compare to general ch-onset positional profile
    ch_lf = sum(1 for w in ch_words if w['is_lf'])
    ch_ll = sum(1 for w in ch_words if w['is_ll'])
    ch_mid = sum(1 for w in ch_words if w['is_mid'])
    print(f"\nGeneral ch-onset positional profile:")
    print(f"  LF={100*ch_lf/len(ch_words):.1f}%  MID={100*ch_mid/len(ch_words):.1f}%  LL={100*ch_ll/len(ch_words):.1f}%")

    # Top cheo words
    print(f"\n### Top ch/sh+eo Words")
    cheo_counter = Counter(w['word'] for w in cheo_words)
    print(f"{'Word':<16} {'n':>5} {'class':<12} {'LF%':>6} {'MID%':>6} {'LL%':>6} {'Stars%':>8} {'B%':>6}")
    for word, count in cheo_counter.most_common(25):
        ws = [w for w in cheo_words if w['word'] == word]
        lf_r = sum(1 for w in ws if w['is_lf']) / len(ws)
        ll_r = sum(1 for w in ws if w['is_ll']) / len(ws)
        mid_r = sum(1 for w in ws if w['is_mid']) / len(ws)
        stars_r = sum(1 for w in ws if w['section'] == 'stars') / len(ws)
        b_r = sum(1 for w in ws if w['dialect'] == 'B') / len(ws)
        cls = get_eo_class(word) or 'other'
        print(f"{word:<16} {count:>5} {cls:<12} {100*lf_r:>5.1f}% {100*mid_r:>5.1f}% {100*ll_r:>5.1f}% {100*stars_r:>7.1f}% {100*b_r:>5.1f}%")

    # Stars-exclusive ch+eo words
    stars_cheo = Counter(w['word'] for w in cheo_words if w['section'] == 'stars')
    all_cheo = Counter(w['word'] for w in cheo_words)
    stars_exclusive = {w: c for w, c in stars_cheo.items()
                       if sum(1 for x in cheo_words if x['word'] == w and x['section'] != 'stars') == 0}
    print(f"\n### Stars-Exclusive ch/sh+eo Words (appear ONLY in stars):")
    for w, c in sorted(stars_exclusive.items(), key=lambda x: -x[1]):
        print(f"  {w:<16} n={c:>4}")

    # Vowel-length gradient analysis
    print(f"\n### Vowel-Length Gradient: cho → cheo → cheeo → cheeeo?")
    patterns = {
        'ch+o (no e)': [w for w in all_vocab if re.match(r'^ch[^e]', w) or re.match(r'^cho', w)],
        'ch+eo (1e)': [w for w in all_vocab if re.match(r'^ch[e]o', w)],
        'ch+eeo (2e)': [w for w in all_vocab if re.match(r'^ch[e]{2}o', w)],
        'ch+eeeo (3e)': [w for w in all_vocab if re.match(r'^ch[e]{3}o', w)],
    }
    for pattern, words in patterns.items():
        total = sum(all_vocab[w] for w in words)
        if total > 0:
            # Section distribution
            section_dist = Counter()
            pos_dist = {'lf': 0, 'mid': 0, 'll': 0}
            for w in words:
                for wd in all_word_data:
                    if wd['word'] == w:
                        section_dist[wd['section']] += 1
                        if wd['is_lf']: pos_dist['lf'] += 1
                        elif wd['is_ll']: pos_dist['ll'] += 1
                        else: pos_dist['mid'] += 1
            total_with_pos = sum(pos_dist.values())
            stars_pct = 100 * section_dist.get('stars', 0) / total if total > 0 else 0
            cosmo_pct = 100 * section_dist.get('cosmo', 0) / total if total > 0 else 0
            lf_pct = 100 * pos_dist['lf'] / total_with_pos if total_with_pos > 0 else 0
            mid_pct = 100 * pos_dist['mid'] / total_with_pos if total_with_pos > 0 else 0
            ll_pct = 100 * pos_dist['ll'] / total_with_pos if total_with_pos > 0 else 0
            print(f"  {pattern:<18}: n_types={len(words):>3}  n_tokens={total:>5}  stars={stars_pct:.1f}%  cosmo={cosmo_pct:.1f}%  LF={lf_pct:.1f}%  MID={mid_pct:.1f}%  LL={ll_pct:.1f}%")

    # sh+eo parallel
    print(f"\n### sh+eo Parallel (sh equivalent of ch+eo)")
    sh_eo_counter = Counter(w['word'] for w in all_word_data
                             if w['word'].startswith('sh') and re.search(r'e*o', w['word'][2:]))
    print(f"{'Word':<16} {'n':>5} {'Stars%':>8} {'B%':>6}")
    for word, count in sh_eo_counter.most_common(10):
        ws = [w for w in all_word_data if w['word'] == word]
        stars_r = sum(1 for w in ws if w['section'] == 'stars') / len(ws)
        b_r = sum(1 for w in ws if w['dialect'] == 'B') / len(ws)
        print(f"{word:<16} {count:>5} {100*stars_r:>7.1f}% {100*b_r:>5.1f}%")

    # Context: what precedes and follows ch+eo words?
    print(f"\n### Bigram Context: What Precedes/Follows ch+eo Words?")
    pre_cheo = Counter()
    post_cheo = Counter()
    total_pre = total_post = 0
    for r in records:
        ws = r['words']
        for i, w in enumerate(ws):
            if is_cheo_pattern(w):
                if i > 0:
                    pre_cheo[get_onset(ws[i-1])] += 1
                    total_pre += 1
                if i < len(ws) - 1:
                    post_cheo[get_onset(ws[i+1])] += 1
                    total_post += 1

    corpus_onset = Counter(w['onset'] for w in all_word_data)
    corpus_onset_frac = {cls: corpus_onset.get(cls, 0) / corpus_total for cls in ONSET_CLASSES}

    print("\nPre-cheo onset enrichment:")
    for cls, n in pre_cheo.most_common(8):
        obs = n / total_pre
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"  {cls:<10} {n:>5} ({100*obs:.1f}%)  base={100*base:.1f}%  enrich={enrich:.2f}×")

    print("\nPost-cheo onset enrichment:")
    for cls, n in post_cheo.most_common(8):
        obs = n / total_post
        base = corpus_onset_frac.get(cls, 0)
        enrich = obs / base if base > 0 else 0
        print(f"  {cls:<10} {n:>5} ({100*obs:.1f}%)  base={100*base:.1f}%  enrich={enrich:.2f}×")

    # Compare ch+eo vs ch+ol (chol) and ch+edy (chedy)
    print(f"\n### ch-Onset Sub-Class Comparison: ch+eo vs ch+ol vs ch+edy")
    ch_subclasses = {
        'chedy/shedy (B-paradigm)': [w for w in all_word_data if w['word'] in ('chedy', 'shedy')],
        'chol/shol (A-paradigm)': [w for w in all_word_data if w['word'] in ('chol', 'shol')],
        'ch+eo (no-suffix)': [w for w in cheo_words],
    }
    for cls, ws in ch_subclasses.items():
        if ws:
            n = len(ws)
            stars_pct = 100 * sum(1 for w in ws if w['section'] == 'stars') / n
            cosmo_pct = 100 * sum(1 for w in ws if w['section'] == 'cosmo') / n
            herbal_pct = 100 * sum(1 for w in ws if w['section'] == 'herbal') / n
            lf_pct = 100 * sum(1 for w in ws if w['is_lf']) / n
            mid_pct = 100 * sum(1 for w in ws if w['is_mid']) / n
            ll_pct = 100 * sum(1 for w in ws if w['is_ll']) / n
            b_pct = 100 * sum(1 for w in ws if w['dialect'] == 'B') / n
            print(f"\n  {cls}:")
            print(f"    n={n}, stars={stars_pct:.1f}%, cosmo={cosmo_pct:.1f}%, herbal={herbal_pct:.1f}%")
            print(f"    LF={lf_pct:.1f}%, MID={mid_pct:.1f}%, LL={ll_pct:.1f}%, B={b_pct:.1f}%")


def main():
    print("Loading corpus...")
    records, folio_dialect = parse_corpus(CORPUS_PATH)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words} words, {len(set(r['folio'] for r in records))} folios")

    analyze_ol_onset(records)
    analyze_cheo_vocabulary(records)

    print("\nDone.")


if __name__ == '__main__':
    main()
