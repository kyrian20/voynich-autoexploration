"""
exp_129: p+r Line Bracket (H256) and raiin vs aiin Context (H257)
==================================================================
H256: Do B-dialect lines template as [p-word at start][content][r-word at end]?
      Co-occurrence analysis; enrichment of r at line-end given p at line-start.

H257: raiin vs aiin context comparison.
      Pre/post-word onset class; section/position distribution.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

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
    for locus, folio_num, words in raw_lines:
        dialect = 'B' if dialect_b.get(folio_num, False) else 'A'
        section = get_section(folio_num)
        records.append({
            'locus': locus, 'folio_num': folio_num,
            'dialect': dialect, 'section': section, 'words': words,
        })
    return records

# ── H256: p+r line bracket ───────────────────────────────────────────────────

def analyze_pr_bracket(records):
    print("=" * 70)
    print("H256: p+r LINE BRACKET — DO B-DIALECT LINES TEMPLATE AS [p-word][...][r-word]?")
    print("=" * 70)

    # For each line: does it start with a p-word? does it end with an r-word?
    sections = ['herbal', 'astro', 'cosmo', 'pharma', 'stars', 'other']

    # Count line types by dialect and section
    stats = {
        'has_p_start': defaultdict(Counter),   # dialect, section
        'has_r_end': defaultdict(Counter),
        'has_both': defaultdict(Counter),
        'total': defaultdict(Counter),
    }

    pr_lines = []  # lines with both p-start and r-end

    for rec in records:
        words = rec['words']
        n = len(words)
        if n < 2:
            continue
        d = rec['dialect']
        s = rec['section']
        stats['total'][d][s] += 1

        has_p = words[0].startswith('p') and len(words[0]) >= 2
        has_r = words[-1].startswith('r') and len(words[-1]) >= 2

        if has_p:
            stats['has_p_start'][d][s] += 1
        if has_r:
            stats['has_r_end'][d][s] += 1
        if has_p and has_r:
            stats['has_both'][d][s] += 1
            pr_lines.append({
                'folio': rec['folio_num'], 'section': s, 'dialect': d,
                'words': words, 'n': n,
                'p_word': words[0], 'r_word': words[-1]
            })

    print(f"\nTotal B-dialect lines (n≥2): {sum(stats['total']['B'].values())}")
    print(f"B-lines with p-start: {sum(stats['has_p_start']['B'].values())} ({sum(stats['has_p_start']['B'].values())/max(sum(stats['total']['B'].values()),1):.1%})")
    print(f"B-lines with r-end: {sum(stats['has_r_end']['B'].values())} ({sum(stats['has_r_end']['B'].values())/max(sum(stats['total']['B'].values()),1):.1%})")
    print(f"B-lines with BOTH (p-start AND r-end): {sum(stats['has_both']['B'].values())} ({sum(stats['has_both']['B'].values())/max(sum(stats['total']['B'].values()),1):.1%})")

    # Enrichment: P(r-end | p-start) vs P(r-end | no p-start)
    b_total = sum(stats['total']['B'].values())
    b_p_start = sum(stats['has_p_start']['B'].values())
    b_r_end = sum(stats['has_r_end']['B'].values())
    b_both = sum(stats['has_both']['B'].values())

    if b_p_start > 0:
        p_r_given_p = b_both / b_p_start
        p_r_given_no_p = (b_r_end - b_both) / (b_total - b_p_start) if b_total > b_p_start else 0
        print(f"\nEnrichment analysis (B-dialect):")
        print(f"  P(r-end | p-start) = {p_r_given_p:.3f} ({b_both}/{b_p_start})")
        print(f"  P(r-end | no p-start) = {p_r_given_no_p:.3f}")
        print(f"  Enrichment: {p_r_given_p/p_r_given_no_p:.2f}×" if p_r_given_no_p > 0 else "  (insufficient data)")

    print(f"\np+r co-occurrence by section (B-dialect):")
    print(f"  {'Section':<10} {'Total':>7} {'p-start':>9} {'r-end':>7} {'Both':>7} {'Both%':>7}")
    for sec in sections:
        tot = stats['total']['B'].get(sec, 0)
        if tot == 0:
            continue
        ps = stats['has_p_start']['B'].get(sec, 0)
        re = stats['has_r_end']['B'].get(sec, 0)
        bo = stats['has_both']['B'].get(sec, 0)
        print(f"  {sec:<10} {tot:>7} {ps:>7} ({ps/tot:.1%}) {re:>5} ({re/tot:.1%}) {bo:>5} ({bo/tot:.1%})")

    # Independence test: P(both) vs P(p)*P(r)
    p_p_start = b_p_start / b_total if b_total > 0 else 0
    p_r_end = b_r_end / b_total if b_total > 0 else 0
    p_both_observed = b_both / b_total if b_total > 0 else 0
    p_both_expected = p_p_start * p_r_end
    print(f"\nIndependence test (B-dialect):")
    print(f"  P(p-start) = {p_p_start:.3f}")
    print(f"  P(r-end) = {p_r_end:.3f}")
    print(f"  P(both) expected by independence = {p_both_expected:.4f} ({p_both_expected*b_total:.1f} lines)")
    print(f"  P(both) observed = {p_both_observed:.4f} ({b_both} lines)")
    if p_both_expected > 0:
        print(f"  Enrichment = {p_both_observed/p_both_expected:.2f}×")

    print(f"\nLines with BOTH p-start AND r-end ({len(pr_lines)} total):")
    print(f"Top p+r line pairs:")
    pr_pairs = Counter((ex['p_word'], ex['r_word']) for ex in pr_lines)
    for (pw, rw), cnt in pr_pairs.most_common(15):
        print(f"  {pw:<15} ... {rw:<15}  n={cnt}")

    print(f"\nSample p+r lines:")
    for ex in pr_lines[:15]:
        print(f"  f{ex['folio']} [{ex['section']}] (n={ex['n']}): {' '.join(ex['words'])}")

    # Also check A-dialect for comparison
    a_total = sum(stats['total']['A'].values())
    a_both = sum(stats['has_both']['A'].values())
    a_p = sum(stats['has_p_start']['A'].values())
    a_r = sum(stats['has_r_end']['A'].values())
    print(f"\nA-dialect comparison:")
    print(f"  Total A-lines: {a_total}")
    print(f"  A p-start: {a_p} ({a_p/a_total:.1%})")
    print(f"  A r-end: {a_r} ({a_r/a_total:.1%})")
    print(f"  A both: {a_both} ({a_both/a_total:.1%})")

# ── H257: raiin vs aiin context ──────────────────────────────────────────────

def analyze_raiin_vs_aiin(records):
    print()
    print("=" * 70)
    print("H257: raiin vs aiin — DIFFERENT SYNTACTIC CONTEXTS?")
    print("=" * 70)

    # Collect pre/post contexts for raiin and aiin
    context = {
        'raiin': {'pre': Counter(), 'post': Counter(), 'section': Counter(), 'dialect': Counter(), 'positions': []},
        'aiin': {'pre': Counter(), 'post': Counter(), 'section': Counter(), 'dialect': Counter(), 'positions': []},
    }

    for rec in records:
        words = rec['words']
        n = len(words)
        for i, w in enumerate(words):
            if w not in ('raiin', 'aiin'):
                continue
            ctx = context[w]
            ctx['section'][rec['section']] += 1
            ctx['dialect'][rec['dialect']] += 1
            pos = 'start' if i == 0 else ('end' if i == n-1 else 'mid')
            ctx['positions'].append(pos)
            if i > 0:
                ctx['pre'][get_onset(words[i-1])] += 1
            if i < n - 1:
                ctx['post'][get_onset(words[i+1])] += 1

    for w in ['raiin', 'aiin']:
        ctx = context[w]
        total = sum(ctx['section'].values())
        print(f"\n{'='*40}")
        print(f"Word: {w} (n={total})")
        print(f"  Dialect: A={ctx['dialect']['A']} ({ctx['dialect']['A']/total:.1%}), B={ctx['dialect']['B']} ({ctx['dialect']['B']/total:.1%})")
        print(f"  Section: " + ", ".join(f"{s}={ctx['section'][s]} ({ctx['section'][s]/total:.1%})" for s in ['herbal','cosmo','pharma','stars','other'] if ctx['section'][s] > 0))
        pos_c = Counter(ctx['positions'])
        print(f"  Position: start={pos_c['start']} ({pos_c['start']/total:.1%}), mid={pos_c['mid']} ({pos_c['mid']/total:.1%}), end={pos_c['end']} ({pos_c['end']/total:.1%})")

        pre_total = sum(ctx['pre'].values())
        post_total = sum(ctx['post'].values())
        print(f"  Pre-word onset class ({pre_total} instances):")
        for o, cnt in ctx['pre'].most_common(8):
            print(f"    {o:<8}: {cnt:>4} ({cnt/pre_total:.1%})")
        print(f"  Post-word onset class ({post_total} instances):")
        for o, cnt in ctx['post'].most_common(8):
            print(f"    {o:<4}: {cnt:>4} ({cnt/post_total:.1%})")

    # Compute enrichment of pre/post onset for raiin vs aiin
    # Baseline: overall corpus onset distribution
    all_words = [w for rec in records for w in rec['words']]
    total_all = len(all_words)
    baseline_onset = Counter(get_onset(w) for w in all_words)
    baseline_frac = {o: cnt/total_all for o, cnt in baseline_onset.items()}

    print(f"\n--- Onset enrichment vs corpus baseline ---")
    print(f"{'Onset':<8} {'raiin_pre':>10} {'aiin_pre':>10} {'raiin_post':>11} {'aiin_post':>11}")
    print("-" * 55)
    raiin_pre_total = sum(context['raiin']['pre'].values())
    aiin_pre_total = sum(context['aiin']['pre'].values())
    raiin_post_total = sum(context['raiin']['post'].values())
    aiin_post_total = sum(context['aiin']['post'].values())

    key_onsets = sorted(set(list(context['raiin']['pre'].keys()) + list(context['aiin']['pre'].keys())),
                        key=lambda x: -(context['raiin']['pre'].get(x,0)+context['aiin']['pre'].get(x,0)))[:12]
    for o in key_onsets:
        base = baseline_frac.get(o, 0.001)
        rp = context['raiin']['pre'].get(o,0)/raiin_pre_total if raiin_pre_total else 0
        ap = context['aiin']['pre'].get(o,0)/aiin_pre_total if aiin_pre_total else 0
        ro = context['raiin']['post'].get(o,0)/raiin_post_total if raiin_post_total else 0
        ao = context['aiin']['post'].get(o,0)/aiin_post_total if aiin_post_total else 0
        print(f"{o:<8} {rp/base:>9.2f}× {ap/base:>9.2f}× {ro/base:>10.2f}× {ao/base:>10.2f}×")

    # Structural question: does raiin → r-particle (like rar, ral)?
    print(f"\nPost-raiin word distribution (top):")
    raiin_post_words = Counter()
    for rec in records:
        words = rec['words']
        for i, w in enumerate(words):
            if w == 'raiin' and i < len(words)-1:
                raiin_post_words[words[i+1]] += 1
    for w, cnt in raiin_post_words.most_common(10):
        print(f"  {w:<15} n={cnt}")

    print(f"\nPost-aiin word distribution (top):")
    aiin_post_words = Counter()
    for rec in records:
        words = rec['words']
        for i, w in enumerate(words):
            if w == 'aiin' and i < len(words)-1:
                aiin_post_words[words[i+1]] += 1
    for w, cnt in aiin_post_words.most_common(10):
        print(f"  {w:<15} n={cnt}")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    corpus_path = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
    print("Loading corpus...")
    records = parse_corpus(corpus_path)
    total_words = sum(len(r['words']) for r in records)
    print(f"Loaded {len(records)} lines, {total_words:,} word tokens")

    analyze_pr_bracket(records)
    analyze_raiin_vs_aiin(records)
