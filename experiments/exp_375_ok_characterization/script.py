"""
exp_375: ok-Onset Full Characterization (H589)

ot self-succession is cross-dialectally stable (A=1.94×, B=1.93×, F369).
exp_373: B qot→ot MID E=1.72× (body-parallel templating).
ot is a template class with ZeroMid≥66% (sparse midfix, Phase 6).
This experiment characterizes ot vocabulary, positional grammar, and bigram rules.
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

DATA_PATH = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt'))
TARGET = 'ok'  # onset to characterize
ONSET_LEN = 2  # len('ot')

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

# Pass 2: collect lines
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
        if len(words) < 1:
            continue
        folio_lines[fb].append((line_num, words, dialect))

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

def agg_pos_pair(pp_label):
    if pp_label == "LF→pos1":
        return "LF→pos1"
    elif pp_label == "pos1→pos2":
        return "pos1→pos2"
    elif pp_label == "pre_LL→LL":
        return "pre_LL→LL"
    else:
        return "MID_inner"

register_words = defaultdict(lambda: defaultdict(list))
register_bigrams = defaultdict(lambda: defaultdict(list))

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
        for i, w in enumerate(words):
            cat = pos_category(i, n)
            register_words[dialect][reg].append((w, cat))

        for i in range(n - 1):
            pw = words[i]
            nw = words[i + 1]
            pp = pos_category(i, n)
            np_ = pos_category(i + 1, n)
            pp_label = f"{pp}→{np_}"
            register_bigrams[dialect][reg].append((pw, nw, pp_label))

A_words = register_words['A']['cont']
B_words = register_words['B']['cont']
A_bigrams = register_bigrams['A']['cont']
B_bigrams = register_bigrams['B']['cont']

print(f"A cont words: {len(A_words)}, bigrams: {len(A_bigrams)}")
print(f"B cont words: {len(B_words)}, bigrams: {len(B_bigrams)}")

# === 1. ot Vocabulary ===
print("\n" + "="*65)
print(f"1. {TARGET.upper()} VOCABULARY")
print("="*65)

for dialect, words_list in [('A', A_words), ('B', B_words)]:
    t_words = Counter(w for w, cat in words_list if get_onset(w) == TARGET)
    total_t = sum(t_words.values())
    total_all = len(words_list)
    t_types = len(t_words)
    hapax = sum(1 for cnt in t_words.values() if cnt == 1)
    print(f"\n{dialect}-dialect: {total_t} {TARGET} tokens ({total_t/total_all*100:.1f}% of all), {t_types} types, {hapax} hapax ({hapax/t_types*100:.0f}%)")
    print(f"Top 20 {TARGET} words:")
    for w, cnt in t_words.most_common(20):
        body = w[ONSET_LEN:]
        print(f"  {w}: {cnt} (body={body!r})")

# === 2. Positional Distribution ===
print("\n" + "="*65)
print(f"2. {TARGET.upper()} POSITIONAL DISTRIBUTION (continuation lines)")
print("="*65)

for dialect, words_list in [('A', A_words), ('B', B_words)]:
    total = len(words_list)
    pos_all = Counter(cat for w, cat in words_list)
    pos_t = Counter(cat for w, cat in words_list if get_onset(w) == TARGET)
    total_t_tokens = sum(pos_t.values())
    baseline_t = total_t_tokens / total
    print(f"\n{dialect}-dialect {TARGET} positional distribution (baseline={baseline_t*100:.2f}%):")
    print(f"{'Position':<12} {'N':>7} {'%at_pos':>9} {'baseline%':>11} {'E':>7}")
    for cat in ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']:
        n_t = pos_t.get(cat, 0)
        n_all = pos_all.get(cat, 1)
        p_t_at_pos = n_t / n_all if n_all > 0 else 0
        e = p_t_at_pos / baseline_t if baseline_t > 0 else float('nan')
        print(f"{cat:<12} {n_t:>7} {p_t_at_pos*100:>8.1f}% {baseline_t*100:>10.1f}% {e:>6.2f}×")

# === 3. Self-Succession ===
print("\n" + "="*65)
print(f"3. {TARGET.upper()} SELF-SUCCESSION POSITIONAL")
print("="*65)

for dialect, bigrams_list in [('A', A_bigrams), ('B', B_bigrams)]:
    total_n = len(bigrams_list)
    target_count = sum(1 for pw, nw, pp in bigrams_list if get_onset(nw) == TARGET)
    baseline_t = target_count / total_n

    t_prev = [(pw, nw, pp) for pw, nw, pp in bigrams_list if get_onset(pw) == TARGET]
    t_t = [(pw, nw, pp) for pw, nw, pp in t_prev if get_onset(nw) == TARGET]

    total_prev = len(t_prev)
    total_hits = len(t_t)
    p_glob = total_hits / total_prev if total_prev > 0 else 0
    E_glob = p_glob / baseline_t if baseline_t > 0 else float('nan')
    print(f"\n{dialect}-dialect {TARGET}→{TARGET}: N_prev={total_prev}, N_hits={total_hits}, E={E_glob:.2f}×")

    agg = defaultdict(lambda: [0, 0])
    for pw, nw, pp in t_prev:
        cat = agg_pos_pair(pp)
        agg[cat][0] += 1
        if get_onset(nw) == TARGET:
            agg[cat][1] += 1

    print(f"{'Position':<20} {'N_prev':>8} {'N_hits':>8} {'P(cond)':>10} {'Baseline':>10} {'E':>8}")
    for cat in ["LF→pos1", "pos1→pos2", "MID_inner", "pre_LL→LL"]:
        n_p, n_h = agg[cat]
        if n_p == 0:
            continue
        p_cond = n_h / n_p
        e = p_cond / baseline_t if baseline_t > 0 else float('nan')
        print(f"{cat:<20} {n_p:>8} {n_h:>8} {p_cond*100:>9.1f}% {baseline_t*100:>9.1f}% {e:>8.2f}×")

    same_word = sum(1 for pw, nw, pp in t_t if pw == nw)
    diff_word = total_hits - same_word
    if total_hits > 0:
        print(f"Same word: {same_word}/{total_hits} ({same_word/total_hits*100:.1f}%); Different word: {diff_word}/{total_hits} ({diff_word/total_hits*100:.1f}%)")

    # Top self-succession word pairs
    pair_counts = Counter((pw, nw) for pw, nw, pp in t_t)
    print(f"Top {TARGET}→{TARGET} word pairs: {', '.join(f'{pw}→{nw}({cnt})' for (pw,nw),cnt in pair_counts.most_common(6))}")

# === 4. Cross-Onset Bigram Rules ===
print("\n" + "="*65)
print(f"4. {TARGET.upper()} CROSS-ONSET BIGRAM RULES")
print("="*65)

def analyze_coupling(bigrams, next_onset, dialect):
    total_n = len(bigrams)
    next_count = sum(1 for pw, nw, pp in bigrams if get_onset(nw) == next_onset)
    baseline = next_count / total_n

    t_prev = [(pw, nw, pp) for pw, nw, pp in bigrams if get_onset(pw) == TARGET]
    hits = [(pw, nw, pp) for pw, nw, pp in t_prev if get_onset(nw) == next_onset]

    total_prev = len(t_prev)
    total_hits = len(hits)
    p_glob = total_hits / total_prev if total_prev > 0 else 0
    E_glob = p_glob / baseline if baseline > 0 else float('nan')

    print(f"\n{dialect} {TARGET}→{next_onset}: N_hits={total_hits}/{total_prev}, baseline={baseline*100:.1f}%, E={E_glob:.2f}×")

    agg = defaultdict(lambda: [0, 0])
    for pw, nw, pp in t_prev:
        cat = agg_pos_pair(pp)
        agg[cat][0] += 1
        if get_onset(nw) == next_onset:
            agg[cat][1] += 1

    for cat in ["LF→pos1", "MID_inner", "pre_LL→LL"]:
        n_p, n_h = agg[cat]
        if n_p == 0:
            continue
        p_c = n_h / n_p
        e = p_c / baseline if baseline > 0 else float('nan')
        print(f"  {cat}: {n_h}/{n_p} ({p_c*100:.1f}%), E={e:.2f}×")

    pair_counts = Counter((pw, nw) for pw, nw, pp in hits)
    top_pairs = ', '.join(f'{pw}→{nw}({cnt})' for (pw,nw),cnt in pair_counts.most_common(4))
    print(f"  Top pairs: {top_pairs}")
    return E_glob, total_hits

print(f"\n--- A-dialect {TARGET} outgoing couplings ---")
for next_onset in ['d', 'ch', 'sh', 'qok', 'ok', 'qot', 'y', 'ol', 'r']:
    analyze_coupling(A_bigrams, next_onset, 'A')

print(f"\n--- B-dialect {TARGET} outgoing couplings ---")
for next_onset in ['d', 'ch', 'sh', 'qok', 'ok', 'qot', 'y', 'ol', 'r']:
    analyze_coupling(B_bigrams, next_onset, 'B')

# === 5. ot Body Structure ===
print("\n" + "="*65)
print(f"5. {TARGET.upper()} BODY STRUCTURE")
print("="*65)
for dialect, words_list in [('A', A_words), ('B', B_words)]:
    t_words = [w for w, cat in words_list if get_onset(w) == TARGET]
    bodies = Counter(w[ONSET_LEN:] for w in t_words)
    total = len(t_words)
    print(f"\n{dialect}-dialect {TARGET} bodies (N={total}, top 15):")
    for body, cnt in bodies.most_common(15):
        print(f"  {TARGET}+'{body}': {cnt} ({cnt/total*100:.1f}%)")

# === 6. Full ot successor distribution ===
print("\n" + "="*65)
print(f"6. FULL {TARGET.upper()} SUCCESSOR DISTRIBUTION")
print("="*65)

for dialect, bigrams_list in [('A', A_bigrams), ('B', B_bigrams)]:
    total_n = len(bigrams_list)
    t_prev = [(get_onset(nw), pp) for pw, nw, pp in bigrams_list if get_onset(pw) == TARGET]
    total_prev = len(t_prev)
    if total_prev == 0:
        continue
    next_onset_counts = Counter(onset for onset, pp in t_prev)
    all_next_counts = Counter(get_onset(nw) for pw, nw, pp in bigrams_list)
    print(f"\n{dialect}-dialect {TARGET} successors (N_prev={total_prev}):")
    print(f"{'Onset':<10} {'N':>6} {'P(cond)':>9} {'baseline':>10} {'E':>7}")
    for onset in ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'y', 'ol', 's', 'r', 'other']:
        n = next_onset_counts.get(onset, 0)
        p_cond = n / total_prev
        base = all_next_counts.get(onset, 0) / total_n
        e = p_cond / base if base > 0 else float('nan')
        if n > 0 or onset in ['d', 'ch']:
            print(f"{onset:<10} {n:>6} {p_cond*100:>8.1f}% {base*100:>9.1f}% {e:>6.2f}×")
