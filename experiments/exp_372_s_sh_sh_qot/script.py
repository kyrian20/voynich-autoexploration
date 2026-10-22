"""
exp_372: B s→sh and A sh→qot Cross-Onset Coupling Positional Decomposition (H585/H586)

Two cross-onset couplings from exp_367's 8x8 matrix:
  B s→sh E=1.98x (N=75): B-dialect s-onset → sh-onset enriched
  A sh→qot E=1.63x (N=29): A-dialect sh-onset → qot-onset enriched

Both need positional decomposition (LF→pos1, pos1→pos2, MID_inner, pre_LL→LL)
and word-level analysis to identify drivers.
Also check: B s→ol (E=1.78×, N=39) and A sh→t (E=2.04×, N=30).
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))

ONSET_ORDER = [
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')
]

def get_onset(word):
    for label, prefix in ONSET_ORDER:
        if word.startswith(prefix):
            return label
    return 'other'

def folio_base(folio):
    return re.sub(r'[rv]$', '', folio)

# Pass 1: dialect classification
folio_word_stats = defaultdict(lambda: {'total': 0, 'edy': 0, 'eedy': 0})
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        fb = folio_base(folio)
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        for w in words:
            folio_word_stats[fb]['total'] += 1
            if w.endswith('eedy'):
                folio_word_stats[fb]['eedy'] += 1
            elif w.endswith('edy'):
                folio_word_stats[fb]['edy'] += 1

def classify_dialect(stats):
    total = stats['total']
    if total == 0:
        return 'unknown'
    return 'B' if (stats['edy'] + stats['eedy']) / total >= 0.05 else 'A'

folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}

# Pass 2: collect lines by folio
folio_lines = defaultdict(list)
with open(DATA_PATH, 'r', encoding='utf-8') as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
        if not m:
            continue
        folio = m.group(1).lstrip('+*=&~')
        line_num = int(m.group(2))
        locus_code = m.group(3)
        fb = folio_base(folio)
        dialect = folio_dialect.get(fb, 'unknown')
        if dialect not in ('A', 'B'):
            continue
        lc = locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        text = re.sub(r'<[^>]+>', '', line)
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if len(words) < 2:
            continue
        folio_lines[fb].append((line_num, words, dialect))

# Register classification
# Structure: register_lines[dialect][register] = list of (words, n_words)
# Bigrams with position: register_lines_bigrams[dialect][register] = list of (prev_w, next_w, pos_pair)
register_bigrams = defaultdict(lambda: defaultdict(list))

def pos_category(idx, n):
    if idx == 0:
        return "LF"
    if idx == 1:
        return "pos1"
    if idx == n - 1:
        return "LL"
    if n >= 4 and idx == n - 2:
        return "pre_LL"
    return "MID_inner"

for fb, lines_list in folio_lines.items():
    if not lines_list:
        continue
    dialect = lines_list[0][2]
    line_nums = [ln for ln, _, _ in lines_list]
    min_ln, max_ln = min(line_nums), max(line_nums)

    for ln, words, d in lines_list:
        if ln == min_ln:
            reg = 'opener'
        elif ln == max_ln:
            reg = 'closer'
        else:
            reg = 'cont'

        n = len(words)
        for i in range(n - 1):
            pw = words[i]
            nw = words[i + 1]
            pp = pos_category(i, n)
            np_ = pos_category(i + 1, n)
            pp_label = f"{pp}→{np_}"
            register_bigrams[dialect][reg].append((pw, nw, pp_label))

A_bigrams = register_bigrams['A']['cont']
B_bigrams = register_bigrams['B']['cont']
print(f"A cont bigrams: {len(A_bigrams)}")
print(f"B cont bigrams: {len(B_bigrams)}")

# === Canonical position pair aggregation ===
def agg_pos_pair(pp_label):
    """Aggregate raw position pair labels into canonical categories."""
    if pp_label == "LF→pos1":
        return "LF→pos1"
    elif pp_label == "pos1→pos2":
        return "pos1→pos2"
    elif pp_label == "pre_LL→LL":
        return "pre_LL→LL"
    elif "MID_inner" in pp_label or "pos1→MID_inner" in pp_label or "pos1→pre_LL" in pp_label:
        return "MID_inner"
    elif "MID_inner→pre_LL" in pp_label:
        return "MID_inner"
    else:
        return "other"

# === Analysis function ===
def analyze_coupling(bigrams, prev_onset, next_onset, label):
    print(f"\n{'='*65}")
    print(f"{label}: {prev_onset}→{next_onset} Positional Decomposition")
    print(f"{'='*65}")

    total_n = len(bigrams)
    next_counts = Counter(get_onset(nw) for _, nw, _ in bigrams)
    baseline_next = next_counts.get(next_onset, 0) / total_n

    print(f"Global baseline P({next_onset}) = {baseline_next*100:.2f}%")

    prev_bigrams = [(pw, nw, pp) for pw, nw, pp in bigrams if get_onset(pw) == prev_onset]
    total_prev = len(prev_bigrams)
    hits = [(pw, nw, pp) for pw, nw, pp in prev_bigrams if get_onset(nw) == next_onset]
    total_hits = len(hits)

    if total_prev == 0:
        print("No data for this onset.")
        return 0.0, 0, 0

    p_global = total_hits / total_prev
    E_global = p_global / baseline_next if baseline_next > 0 else float('nan')
    print(f"Overall: N_prev={total_prev}, N_hits={total_hits}, P({next_onset}|{prev_onset})={p_global*100:.1f}%, E={E_global:.2f}×")

    # Per position pair
    agg = defaultdict(lambda: [0, 0])
    for pw, nw, pp in prev_bigrams:
        cat = agg_pos_pair(pp)
        agg[cat][0] += 1
        if get_onset(nw) == next_onset:
            agg[cat][1] += 1

    print(f"\n{'Position':<20} {'N_prev':>8} {'N_hits':>8} {'P(cond)':>10} {'Baseline':>10} {'E':>8}")
    for cat in ["LF→pos1", "pos1→pos2", "MID_inner", "pre_LL→LL"]:
        n_p, n_h = agg[cat]
        if n_p == 0:
            continue
        p_cond = n_h / n_p
        e = p_cond / baseline_next if baseline_next > 0 else float('nan')
        print(f"{cat:<20} {n_p:>8} {n_h:>8} {p_cond*100:>9.1f}% {baseline_next*100:>9.1f}% {e:>8.2f}×")

    # Top word pairs
    pair_counts = Counter((pw, nw) for pw, nw, pp in hits)
    print(f"\nTop {prev_onset}→{next_onset} word pairs:")
    for (pw, nw), cnt in pair_counts.most_common(10):
        print(f"  {pw}→{nw}: {cnt}")

    # prev_onset word-level breakdown
    prev_word_totals = Counter(pw for pw, nw, pp in prev_bigrams)
    prev_word_hits = Counter(pw for pw, nw, pp in hits)
    print(f"\nTop {prev_onset}-onset predecessor words (hits/total → P(hits)):")
    for pw, total in prev_word_totals.most_common(8):
        h = prev_word_hits.get(pw, 0)
        p_pw = h / total if total > 0 else 0
        marker = " **" if p_pw > baseline_next * 1.5 else ""
        print(f"  {pw}: {h}/{total} ({p_pw*100:.1f}%){marker}")

    # next_onset word distribution
    next_word_counts = Counter(nw for pw, nw, pp in hits)
    print(f"\nTop {next_onset}-onset successor words:")
    for nw, cnt in next_word_counts.most_common(8):
        print(f"  {nw}: {cnt}")

    return E_global, total_hits, total_prev


# === Run analyses ===
print("\n" + "="*70)
print("ANALYSIS 1: B s→sh (H585)")
print("="*70)
E_bssh, n_bssh, t_bssh = analyze_coupling(B_bigrams, "s", "sh", "B-dialect")

print("\n" + "="*70)
print("ANALYSIS 2: B s→ol (control: second s-onset coupling)")
print("="*70)
E_bsol, n_bsol, t_bsol = analyze_coupling(B_bigrams, "s", "ol", "B-dialect")

print("\n" + "="*70)
print("ANALYSIS 3: A sh→qot (H586)")
print("="*70)
E_ashqot, n_ashqot, t_ashqot = analyze_coupling(A_bigrams, "sh", "qot", "A-dialect")

print("\n" + "="*70)
print("ANALYSIS 4: A sh→t (related: sh to t-onset gallows)")
print("="*70)
E_asht, n_asht, t_asht = analyze_coupling(A_bigrams, "sh", "t", "A-dialect")

# Also check B s class overall: what are the main s-onset word types?
print("\n" + "="*70)
print("SUPPLEMENTARY: B s-onset word inventory")
print("="*70)
s_words_B = Counter(pw for pw, nw, pp in B_bigrams if get_onset(pw) == "s")
print(f"Top B s-onset words (N={sum(s_words_B.values())} prev-slots):")
for w, cnt in s_words_B.most_common(12):
    print(f"  {w}: {cnt}")

s_words_A = Counter(pw for pw, nw, pp in A_bigrams if get_onset(pw) == "s")
print(f"\nTop A s-onset words (N={sum(s_words_A.values())} prev-slots):")
for w, cnt in s_words_A.most_common(12):
    print(f"  {w}: {cnt}")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"B s→sh:   E={E_bssh:.2f}× (N={n_bssh}/{t_bssh})")
print(f"B s→ol:   E={E_bsol:.2f}× (N={n_bsol}/{t_bsol})")
print(f"A sh→qot: E={E_ashqot:.2f}× (N={n_ashqot}/{t_ashqot})")
print(f"A sh→t:   E={E_asht:.2f}× (N={n_asht}/{t_asht})")
