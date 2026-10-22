"""
exp_104: B ch+d Cluster Analysis (H197) and Heaps' Law Vocabulary Growth (H198)

H197: Is "chd" a morphological unit in B? Are chd-words a distinct class?
H198: Does Voynichese follow Heaps' law (natural language vocabulary growth)?
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')


def folio_base(folio):
    return re.sub(r'\.\d+$', '', folio)


def classify_dialect(folio_stats):
    total = folio_stats.get('total', 0)
    if total == 0:
        return 'unknown'
    rate = (folio_stats.get('edy', 0) + folio_stats.get('eedy', 0)) / total
    return 'B' if rate >= 0.05 else 'A'


def classify_section(folio):
    m = re.match(r'f(\d+)([rv])', folio)
    if not m:
        return 'unknown'
    n = int(m.group(1))
    if n <= 57:
        return 'herbal'
    if 67 <= n <= 73:
        return 'astro'
    if 75 <= n <= 84:
        return 'cosmo'
    if 87 <= n <= 102:
        return 'pharma'
    if 103 <= n <= 116:
        return 'stars'
    return 'other'


def parse_voynich():
    folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'):
                    folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'):
                    folio_word_stats[fb]['edy'] += 1

    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

    records = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m:
                continue
            folio_raw = m.group(1)
            locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~')
            fb = folio_base(folio)
            dialect = folio_dialect.get(fb, 'unknown')
            section = classify_section(fb)

            lc_stripped = locus_code.lstrip('+*=/~&')
            is_para_start = lc_stripped.startswith('@')
            is_body = lc_stripped.lstrip('@').startswith('P')
            if not is_body:
                continue

            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue

            for pos, w in enumerate(words):
                records.append({
                    'dialect': dialect,
                    'section': section,
                    'folio': fb,
                    'word': w,
                    'is_para_start': is_para_start and pos == 0,
                    'is_line_first': pos == 0,
                    'is_line_last': pos == len(words) - 1,
                    'pos': pos,
                })

    return records


def h197_chd_cluster_analysis(records):
    """H197: Is chd- a morphological unit in B?"""
    print("=" * 70)
    print("H197: B ch+d Cluster Analysis")
    print("=" * 70)

    # Extract all chd-words in B and A
    b_records = [r for r in records if r['dialect'] == 'B']
    a_records = [r for r in records if r['dialect'] == 'A']

    # chd words = words starting with 'chd' or 'che' followed by 'd'
    # (che+d forms: chedar = ch+e+d+ar; chdaiin = ch+d+aiin)
    # Let's look at all ch-words with 'd' as second or third character

    def get_chd_form(word):
        """Classify ch-word by d-element position."""
        if not word.startswith('ch'):
            return None
        rest = word[2:]  # after 'ch'
        if rest.startswith('d'):
            return 'chd'  # chdaiin, chdal, chdar, chdy
        if rest.startswith('ed'):
            return 'ched'  # chedar, chedaiin, chedal
        if rest.startswith('eed'):
            return 'cheed'  # cheedaiin
        return None

    print(f"\n--- B dialect: chd/ched forms ---")
    b_chd_records = [r for r in b_records if get_chd_form(r['word'])]
    b_all_ch_records = [r for r in b_records if r['word'].startswith('ch')]

    print(f"B total ch-words: {len(b_all_ch_records)}")
    print(f"B chd/ched words: {len(b_chd_records)} ({len(b_chd_records)/len(b_all_ch_records)*100:.1f}% of B ch-words)")

    # Word frequency
    b_chd_counter = Counter(r['word'] for r in b_chd_records)
    print(f"\nTop B chd/ched words:")
    for word, cnt in b_chd_counter.most_common(20):
        form = get_chd_form(word)
        print(f"  {word}: {cnt} (form={form})")

    # Positional behavior of chd vs bare_ch
    print(f"\n--- Positional profiles: chd-type vs bare_ch in B ---")
    b_bare_ch = [r for r in b_records if r['word'].startswith('ch') and
                 not r['word'].startswith('chd') and not r['word'].startswith('ched')]

    def pos_profile(recs, label):
        n = len(recs)
        if n == 0:
            return
        ps = sum(1 for r in recs if r['is_para_start'])
        lf = sum(1 for r in recs if r['is_line_first'])
        ll = sum(1 for r in recs if r['is_line_last'])
        print(f"  {label}: n={n}, PS={ps/n*100:.1f}%, LFirst={lf/n*100:.1f}%, LLast={ll/n*100:.1f}%")

    pos_profile(b_chd_records, "B chd/ched forms")
    pos_profile(b_bare_ch, "B bare_ch (no d-element)")
    pos_profile(a_records, "A all-words")

    # Compare chd suffix patterns
    print(f"\n--- Suffix patterns for B chd-words vs all B ch-words ---")
    def get_suffix(word):
        """Extract suffix from word."""
        if word.endswith('eedy'):
            return '-eedy'
        if word.endswith('edy'):
            return '-edy'
        if word.endswith('aiin'):
            return '-aiin'
        if word.endswith('ain'):
            return '-ain'
        if word.endswith('eey'):
            return '-eey'
        if word.endswith('ey'):
            return '-ey'
        if word.endswith('al'):
            return '-al'
        if word.endswith('ar'):
            return '-ar'
        if word.endswith('ol'):
            return '-ol'
        if word.endswith('or'):
            return '-or'
        if word.endswith('dy'):
            return '-dy'
        if word.endswith('y'):
            return '-y'
        if word.endswith('n'):
            return '-n'
        return '-other'

    chd_suffixes = Counter(get_suffix(r['word']) for r in b_chd_records)
    all_ch_suffixes = Counter(get_suffix(r['word']) for r in b_all_ch_records)
    n_chd = len(b_chd_records)
    n_all = len(b_all_ch_records)

    print(f"{'Suffix':<12} {'chd_n':>6} {'chd%':>7} {'all_ch%':>8} {'Enrich':>8}")
    all_suffixes = set(list(chd_suffixes.keys()) + list(all_ch_suffixes.keys()))
    suffix_enrich = []
    for suffix in all_suffixes:
        chd_n = chd_suffixes.get(suffix, 0)
        all_n = all_ch_suffixes.get(suffix, 0)
        chd_rate = chd_n / n_chd if n_chd > 0 else 0
        all_rate = all_n / n_all if n_all > 0 else 0
        enrich = chd_rate / all_rate if all_rate > 0 else float('inf')
        suffix_enrich.append((suffix, chd_n, chd_rate, all_n, all_rate, enrich))
    suffix_enrich.sort(key=lambda x: -x[5])
    for suffix, chd_n, chd_rate, all_n, all_rate, enrich in suffix_enrich:
        enr_str = f"{enrich:.2f}×" if enrich != float('inf') else "∞"
        print(f"  {suffix:<12} {chd_n:>6} {chd_rate*100:>6.1f}% {all_rate*100:>7.1f}% {enr_str:>8}")

    # Section distribution of chd forms
    print(f"\n--- chd-word section distribution in B ---")
    sect_chd = Counter(r['section'] for r in b_chd_records)
    sect_all = Counter(r['section'] for r in b_records)
    for sect, n_sect in sorted(sect_chd.items(), key=lambda x: -x[1]):
        all_n = sect_all.get(sect, 0)
        print(f"  {sect}: {n_sect}/{all_n} ({n_sect/all_n*100:.1f}% of B {sect} words)")

    # Is chd a reduced form of ch + another word (d-onset word)?
    # Compare chd-words to bigrams where d-onset word follows ch-word
    print(f"\n--- Is chd = ch+d compound or ch-stem+d-suffix? ---")
    print("  chd words with -aiin suffix: might be ch+daiin (= ch-stem + d-onset + aiin)")
    print("  chd words with -al/-ar suffix: might be ch+dal/dar (ch-stem + d-closer)")
    for word, cnt in b_chd_counter.most_common(10):
        suf = get_suffix(word)
        form = get_chd_form(word)
        # Could this be ch + d-initial word?
        d_word = word[2:]  # strip 'ch' → remaining could be a d-word
        alt_word = word[3:]  # strip 'chd' or 'che' → check if d...
        print(f"  {word}({cnt}): form={form}, suffix={suf}, after-ch='{d_word}'")


def h198_heaps_law(records):
    """H198: Heaps' law vocabulary growth by section."""
    print("\n" + "=" * 70)
    print("H198: Heaps' Law — Vocabulary Growth by Section")
    print("=" * 70)

    def compute_heaps(words):
        """Return (tokens_list, types_list) for Heaps' law fitting."""
        seen = set()
        tokens = []
        types = []
        for i, w in enumerate(words):
            seen.add(w)
            tokens.append(i + 1)
            types.append(len(seen))
        return tokens, types

    def fit_heaps_beta(tokens, types):
        """Fit V = K * N^beta using log-linear regression on second half."""
        # Use second half to avoid initial noise
        half = len(tokens) // 2
        if half < 10:
            return None, None
        log_n = [math.log(tokens[i]) for i in range(half, len(tokens))]
        log_v = [math.log(types[i]) for i in range(half, len(tokens))]
        # Simple linear regression on log-log
        n_pts = len(log_n)
        mean_x = sum(log_n) / n_pts
        mean_y = sum(log_v) / n_pts
        num = sum((log_n[i] - mean_x) * (log_v[i] - mean_y) for i in range(n_pts))
        den = sum((log_n[i] - mean_x) ** 2 for i in range(n_pts))
        beta = num / den if den > 0 else 0
        log_K = mean_y - beta * mean_x
        K = math.exp(log_K)
        return beta, K

    # Compute for each section and dialect
    section_words = defaultdict(list)
    for r in records:
        key = f"{r['dialect']}_{r['section']}"
        section_words[key].append(r['word'])

    print(f"\n{'Section':<20} {'N_words':>8} {'V_unique':>9} {'TTR':>6} {'beta':>7} {'K':>8} {'V@1000':>8} {'V@5000':>8}")
    print(f"(NL expect: beta≈0.5-0.7)")

    results = []
    for key in sorted(section_words.keys()):
        words = section_words[key]
        if len(words) < 200:
            continue
        tokens, types = compute_heaps(words)
        N = len(tokens)
        V = len(set(words))
        ttr = V / N
        beta, K = fit_heaps_beta(tokens, types)
        if beta is None:
            continue
        v_at_1000 = K * (1000 ** beta) if N >= 1000 else None
        v_at_5000 = K * (5000 ** beta) if N >= 5000 else None

        v1k_str = f"{v_at_1000:.0f}" if v_at_1000 else "N/A"
        v5k_str = f"{v_at_5000:.0f}" if v_at_5000 else "N/A"
        print(f"  {key:<20} {N:>8} {V:>9} {ttr:>6.3f} {beta:>7.3f} {K:>8.1f} {v1k_str:>8} {v5k_str:>8}")
        results.append((key, N, V, beta, K))

    # Summary: what beta values mean
    print(f"\nInterpretation:")
    print(f"  beta < 0.4: highly repetitive (formulaic/cipher)")
    print(f"  beta 0.4-0.5: somewhat repetitive")
    print(f"  beta 0.5-0.7: natural language range")
    print(f"  beta > 0.7: very diverse (random/noisy)")

    # Compare dialect A vs B overall
    a_words = [r['word'] for r in records if r['dialect'] == 'A']
    b_words = [r['word'] for r in records if r['dialect'] == 'B']

    for label, words in [('A overall', a_words), ('B overall', b_words)]:
        tokens, types = compute_heaps(words)
        beta, K = fit_heaps_beta(tokens, types)
        N = len(tokens)
        V = len(set(words))
        print(f"\n  {label}: N={N}, V={V}, TTR={V/N:.3f}, beta={beta:.3f}, K={K:.1f}")

    # Sample points for visual inspection
    print(f"\n--- Sample Heaps' curve points (A herbal) ---")
    a_herbal = [r['word'] for r in records
                if r['dialect'] == 'A' and r['section'] == 'herbal']
    tokens, types = compute_heaps(a_herbal)
    for n_target in [100, 200, 500, 1000, 2000, 3000, 5000]:
        if n_target <= len(tokens):
            print(f"  N={n_target}: V={types[n_target-1]}")


def main():
    print("Loading data...")
    records = parse_voynich()
    print(f"Total word tokens: {len(records)}")

    h197_chd_cluster_analysis(records)
    h198_heaps_law(records)


if __name__ == '__main__':
    main()
