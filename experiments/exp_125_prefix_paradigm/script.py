#!/usr/bin/env python3
"""
exp_125: Full Prefix Paradigm Reconstruction (H249) + B-Dialect cth Analysis (H250)
H249: Do all major stem classes take (bare/qo-/l-) prefixes? Generalize four-prefix system.
H250: What are the 52 cth-onset tokens in B-dialect? Code-switching or formula?
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
                })

    dialect_map = {fnum: ('B' if edy_counts[fnum]/max(1,total_counts[fnum]) >= 0.05 else 'A')
                   for fnum in total_counts}
    for r in records:
        r['dialect'] = dialect_map.get(r['folio'], 'A')

    return records, dialect_map


def analyze_stem_prefix_paradigm(stem, records, vocab, all_words):
    """Analyze how a stem takes different prefixes."""
    # Prefixes to test: bare, qo-, l-, o- (o-prefix for labels mainly, but also body)
    prefixes = {
        'bare': stem,
        'qo+': 'qo' + stem,
        'l+': 'l' + stem,
        'o+': 'o' + stem,
    }
    results = {}
    for pref_name, pref_form in prefixes.items():
        # Find all words that start with pref_form (to catch all suffix variants)
        stem_recs = [r for r in records if r['word'].startswith(pref_form) and
                     len(r['word']) > len(pref_form)]
        # Also include exact match if it's in vocab
        exact_recs = [r for r in records if r['word'] == pref_form]
        all_recs = stem_recs + [r for r in exact_recs if r not in stem_recs]
        # Deduplicate
        seen = set()
        unique_recs = []
        for r in all_recs:
            if id(r) not in seen:
                seen.add(id(r))
                unique_recs.append(r)

        if not unique_recs:
            results[pref_name] = None
            continue

        n = len(unique_recs)
        words = Counter(r['word'] for r in unique_recs)
        dial = Counter(r['dialect'] for r in unique_recs)
        sec = Counter(r['section'] for r in unique_recs)
        pos_first = sum(1 for r in unique_recs if r['is_line_first'])
        pos_last = sum(1 for r in unique_recs if r['is_line_last'])
        suf = Counter(get_suffix(r['word']) for r in unique_recs)

        results[pref_name] = {
            'n': n,
            'top_words': words.most_common(3),
            'A': dial['A'],
            'B': dial['B'],
            'A_frac': dial['A']/n,
            'sections': dict(sec.most_common()),
            'first_frac': pos_first/n,
            'last_frac': pos_last/n,
            'top_suf': suf.most_common(2),
        }
    return results


def h249_prefix_paradigm(records, dialect_map):
    print("\n" + "="*60)
    print("H249: FULL PREFIX PARADIGM RECONSTRUCTION")
    print("="*60)

    all_words = Counter(r['word'] for r in records)
    vocab = set(all_words.keys())
    total = len(records)

    a_total = sum(1 for r in records if r['dialect'] == 'A')
    b_total = sum(1 for r in records if r['dialect'] == 'B')
    section_totals = Counter(r['section'] for r in records)

    # Test major stem classes
    stem_classes = {
        'k-stems': ['k', 'ka', 'ke', 'ki'],  # bare k-initial stems
        'ch-stems': ['ch'],
        'sh-stems': ['sh'],
        't-stems': ['t'],
        'r-stems': ['r'],
    }

    # The core test: for top stems in each class, does bare/qo/l/o form exist?
    print("\n--- Prefix paradigm test (top words by frequency) ---")

    # Pick representative stems — actual high-frequency ones
    test_stems = [
        # k-stems (from exp_124 results)
        ('kaiin', 'k-stem'),
        ('kedy', 'k-stem'),
        ('keedy', 'k-stem'),
        ('keey', 'k-stem'),
        ('kain', 'k-stem'),
        ('kar', 'k-stem'),
        # ch-stems
        ('chedy', 'ch-stem'),
        ('chey', 'ch-stem'),
        ('chedy', 'ch-stem'),
        # sh-stems
        ('shedy', 'sh-stem'),
        ('shey', 'sh-stem'),
        # t-stems
        ('taiin', 't-stem'),
        ('teedy', 't-stem'),
        ('tain', 't-stem'),
        # r-stems
        ('raiin', 'r-stem'),
        ('rain', 'r-stem'),
    ]

    for stem, stem_class in test_stems:
        print(f"\n  [{stem_class}] Base stem: '{stem}' (n={all_words.get(stem, 0)})")
        # Check each prefix form
        forms = {
            'bare': stem,
            'qo+': 'qo' + stem,
            'l+': 'l' + stem,
            'o+': 'o' + stem,
        }
        for pref, form in forms.items():
            n = all_words.get(form, 0)
            if n == 0:
                print(f"    {pref:6s}: {form:20s} n=0 (absent)")
                continue
            recs = [r for r in records if r['word'] == form]
            d = Counter(r['dialect'] for r in recs)
            s = Counter(r['section'] for r in recs)
            top_sec = s.most_common(1)[0] if s else ('?', 0)
            a_frac = d['A']/n
            print(f"    {pref:6s}: {form:20s} n={n:4d}  A={d['A']} B={d['B']} (A%={a_frac:.2f}) "
                  f"top_sec={top_sec[0]}({top_sec[1]/n:.2f})")

    # Broader analysis: for each prefix class, what STEMS do they take?
    print("\n\n--- Stem recovery across prefix classes ---")

    def compute_prefix_stats(prefix_str):
        """Get all words starting with prefix_str and analyze stem recovery."""
        pref_recs = [r for r in records if r['word'].startswith(prefix_str)
                     and len(r['word']) > len(prefix_str)]
        pref_words = Counter(r['word'] for r in pref_recs)
        n_total = sum(pref_words.values())
        # Stem recovery: does word[len(prefix):] appear in vocab?
        with_stem = [(w, w[len(prefix_str):]) for w in pref_words if len(w[len(prefix_str):]) >= 2]
        in_vocab = sum(1 for w, s in with_stem if s in vocab)
        # Dialect
        d = Counter(r['dialect'] for r in pref_recs)
        # Section
        s = Counter(r['section'] for r in pref_recs)
        # Suffix
        suf = Counter(get_suffix(r['word']) for r in pref_recs)
        return {
            'n_tokens': n_total,
            'n_types': len(pref_words),
            'stem_recovery_types': in_vocab/len(with_stem) if with_stem else 0,
            'stem_recovery_tokens': sum(pref_words[w] for w, s in with_stem if s in vocab)/n_total if n_total else 0,
            'A_rate': d['A']/n_total if n_total else 0,
            'B_rate': d['B']/n_total if n_total else 0,
            'top_sections': dict(s.most_common(3)),
            'top_suffix': suf.most_common(3),
        }

    for prefix_str in ['qo', 'l', 'o', 'k', 'r', 't', 'y', 'p']:
        stats = compute_prefix_stats(prefix_str)
        if stats['n_tokens'] < 50: continue
        print(f"\n  prefix='{prefix_str}':")
        print(f"    n={stats['n_tokens']:5d} tokens, {stats['n_types']:3d} types")
        print(f"    Stem recovery: types={stats['stem_recovery_types']:.3f}, tokens={stats['stem_recovery_tokens']:.3f}")
        print(f"    A/B: {stats['A_rate']:.3f}/{stats['B_rate']:.3f} (ratio={stats['A_rate']/stats['B_rate']:.2f})")
        print(f"    Sections: {stats['top_sections']}")
        print(f"    Top suffixes: {stats['top_suffix']}")

    # Section-dialect matrix for prefix classes
    print("\n\n--- Prefix class × Dialect × Section matrix ---")
    print(f"{'Prefix':8s} | {'A-herb':8s} | {'A-phar':8s} | {'B-herb':8s} | {'B-cosmo':8s} | {'B-stars':8s}")
    for pref in ['qo', 'l', 'k', 't', 'r']:
        pref_recs = [r for r in records if r['word'].startswith(pref)
                     and len(r['word']) > len(pref)]
        n = len(pref_recs)
        if n == 0: continue
        def rate(d, sec): return sum(1 for r in pref_recs if r['dialect']==d and r['section']==sec)/n
        print(f"  {pref:6s}  | {rate('A','herbal'):8.3f} | {rate('A','pharma'):8.3f} | "
              f"{rate('B','herbal'):8.3f} | {rate('B','cosmo'):8.3f} | {rate('B','stars'):8.3f}")


def h250_b_dialect_cth(records, dialect_map):
    print("\n" + "="*60)
    print("H250: B-DIALECT cth-ONSET TOKENS")
    print("="*60)

    b_recs = [r for r in records if r['dialect'] == 'B']
    b_cth = [r for r in b_recs if r['word'].startswith('cth')]
    print(f"\nB-dialect total tokens: {len(b_recs)}")
    print(f"B-dialect cth-onset tokens: {len(b_cth)} ({len(b_cth)/len(b_recs)*1000:.2f}‰)")

    # Which specific cth-words appear in B-dialect?
    print(f"\n--- cth-words in B-dialect ---")
    b_cth_words = Counter(r['word'] for r in b_cth)
    a_cth_words = Counter(r['word'] for r in records if r['dialect'] == 'A' and r['word'].startswith('cth'))
    for w, cnt in b_cth_words.most_common(20):
        a_cnt = a_cth_words.get(w, 0)
        print(f"  {w:15s}: B={cnt:3d}  A={a_cnt:4d}  B_frac={cnt/(cnt+a_cnt):.3f}")

    # Which folios/sections contain B-dialect cth?
    print(f"\n--- B-dialect cth by section ---")
    b_cth_by_sec = Counter(r['section'] for r in b_cth)
    b_by_sec = Counter(r['section'] for r in b_recs)
    for sec, cnt in b_cth_by_sec.most_common():
        rate = cnt / b_by_sec[sec] if b_by_sec[sec] else 0
        print(f"  {sec:8s}: {cnt:3d}/{b_by_sec[sec]:5d} = {rate*1000:.2f}‰")

    # Which specific B-dialect folios contain cth?
    print(f"\n--- B-dialect folios with cth tokens ---")
    b_cth_by_folio = Counter(r['folio'] for r in b_cth)
    for folio, cnt in sorted(b_cth_by_folio.items()):
        b_folio_total = sum(1 for r in b_recs if r['folio'] == folio)
        rate = cnt / b_folio_total if b_folio_total else 0
        sec = SECTION_MAP.get(folio, 'other')
        print(f"  f{folio:3d} ({sec:8s}): {cnt:3d}/{b_folio_total:4d} = {rate*1000:.2f}‰")

    # What context (neighboring words) do B-dialect cth-tokens appear in?
    print(f"\n--- B-dialect cth bigram context ---")
    pre_cth_b = Counter(r['prev_word'] for r in b_cth if r['prev_word'])
    post_cth_b = Counter(r['next_word'] for r in b_cth if r['next_word'])
    pre_onset_b = Counter(get_onset(r['prev_word']) for r in b_cth if r['prev_word'])
    post_onset_b = Counter(get_onset(r['next_word']) for r in b_cth if r['next_word'])
    n_pre = sum(pre_cth_b.values())
    n_post = sum(post_cth_b.values())

    # B-dialect baseline for comparison
    b_next_onset = Counter(get_onset(r['next_word']) for r in b_recs if r['next_word'])
    b_total_next = sum(b_next_onset.values())
    b_prev_onset = Counter(get_onset(r['prev_word']) for r in b_recs if r['prev_word'])
    b_total_prev = sum(b_prev_onset.values())

    print(f"  Pre-cth (B-dialect) onset:")
    for onset, cnt in pre_onset_b.most_common(8):
        obs = cnt/n_pre
        base = b_prev_onset[onset]/b_total_prev if b_total_prev else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
    print(f"  Post-cth (B-dialect) onset:")
    for onset, cnt in post_onset_b.most_common(8):
        obs = cnt/n_post
        base = b_next_onset[onset]/b_total_next if b_total_next else 0
        enr = obs/base if base else 0
        print(f"    {onset:8s}: {cnt} ({obs:.3f} vs {base:.3f} = {enr:.2f}×)")
    print(f"  Top words before B-cth: {pre_cth_b.most_common(8)}")
    print(f"  Top words after B-cth: {post_cth_b.most_common(8)}")

    # Are B-dialect cth-tokens surrounded by A-paradigm or B-paradigm words?
    print(f"\n--- A-paradigm vs B-paradigm context for B-dialect cth ---")
    a_paradigm_suffixes = {'ol', 'or', 'y', 'aiin'}
    b_paradigm_suffixes = {'edy', 'eedy', 'eey', 'eeey', 'ain', 'ey'}

    for r in b_cth[:20]:
        prev_suf = get_suffix(r['prev_word']) if r['prev_word'] else 'none'
        next_suf = get_suffix(r['next_word']) if r['next_word'] else 'none'
        prev_paradigm = 'A' if prev_suf in a_paradigm_suffixes else ('B' if prev_suf in b_paradigm_suffixes else '?')
        next_paradigm = 'A' if next_suf in a_paradigm_suffixes else ('B' if next_suf in b_paradigm_suffixes else '?')
        print(f"  [{r['prev_word']or'START':12s}({prev_paradigm})] {r['word']:15s} [{r['next_word']or'END':12s}({next_paradigm})] "
              f"folio={r['folio']} sec={r['section']}")

    # cth→cth self-clustering in B
    print(f"\n--- cth→cth self-clustering in B-dialect ---")
    b_cth_with_next = [r for r in b_cth if r['next_word'] and r['next_word'].startswith('cth')]
    print(f"  cth→cth transitions in B: {len(b_cth_with_next)}/{len(b_cth)} = {len(b_cth_with_next)/len(b_cth):.3f}")
    for r in b_cth_with_next:
        print(f"    {r['word']:15s} → {r['next_word']:15s}  folio={r['folio']} sec={r['section']}")

    # Positional distribution of B-dialect cth
    print(f"\n--- B-dialect cth positional distribution ---")
    first = sum(1 for r in b_cth if r['is_line_first'])
    last = sum(1 for r in b_cth if r['is_line_last'])
    mid = len(b_cth) - first - last
    n = len(b_cth)
    a_cth = [r for r in records if r['dialect'] == 'A' and r['word'].startswith('cth')]
    a_n = len(a_cth)
    a_first = sum(1 for r in a_cth if r['is_line_first'])
    a_last = sum(1 for r in a_cth if r['is_line_last'])
    a_mid = a_n - a_first - a_last
    print(f"  B-cth: first={first/n:.3f}, mid={mid/n:.3f}, last={last/n:.3f} (n={n})")
    print(f"  A-cth: first={a_first/a_n:.3f}, mid={a_mid/a_n:.3f}, last={a_last/a_n:.3f} (n={a_n})")


def main():
    print("Loading records...")
    records, dialect_map = parse_eva(DATA)
    print(f"Total: {len(records)} records")

    all_words = Counter(r['word'] for r in records)
    vocab = set(all_words.keys())

    h249_prefix_paradigm(records, dialect_map)
    h250_b_dialect_cth(records, dialect_map)

if __name__ == '__main__':
    main()
