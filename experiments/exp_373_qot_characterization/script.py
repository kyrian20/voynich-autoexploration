"""
exp_373: qot-Onset Full Characterization (H587)

qot is the highest A-dialect self-succession class (E=2.60×), LF-enriched (F368),
with qot→daiin A E=2.52× (F366), qot→y A E=1.75×, qot→r B E=2.00× (exp_367).
This experiment characterizes qot vocabulary, positional grammar, and bigram rules.
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
        if len(words) < 1:
            continue
        folio_lines[fb].append((line_num, words, dialect))

# Register classification and collect by register
register_words = defaultdict(lambda: defaultdict(list))  # [dialect][register] = list of (word, position_cat)
register_lines = defaultdict(lambda: defaultdict(list))  # [dialect][register] = list of word lists
register_bigrams = defaultdict(lambda: defaultdict(list))  # [dialect][register] = list of (pw, nw, pos_pair)

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
        register_lines[dialect][reg].append(words)

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

# === 1. qot Vocabulary ===
print("\n" + "="*65)
print("1. QOT VOCABULARY")
print("="*65)

for dialect, words_list in [('A', A_words), ('B', B_words)]:
    qot_words = Counter(w for w, cat in words_list if get_onset(w) == 'qot')
    total_qot = sum(qot_words.values())
    total_all = len(words_list)
    qot_types = len(qot_words)
    hapax = sum(1 for cnt in qot_words.values() if cnt == 1)
    print(f"\n{dialect}-dialect: {total_qot} qot tokens ({total_qot/total_all*100:.1f}% of all words), {qot_types} unique types, {hapax} hapax ({hapax/qot_types*100:.0f}%)")
    print("Top 20 qot words:")
    for w, cnt in qot_words.most_common(20):
        body = w[3:]  # strip 'qot' onset
        print(f"  {w}: {cnt} (body={body!r})")

# === 2. Positional Distribution ===
print("\n" + "="*65)
print("2. QOT POSITIONAL DISTRIBUTION (continuation lines)")
print("="*65)

for dialect, words_list, bigrams_list in [('A', A_words, A_bigrams), ('B', B_words, B_bigrams)]:
    total = len(words_list)
    pos_all = Counter(cat for w, cat in words_list)
    pos_qot = Counter(cat for w, cat in words_list if get_onset(w) == 'qot')
    total_qot_tokens = sum(pos_qot.values())
    baseline_qot = total_qot_tokens / total
    print(f"\n{dialect}-dialect qot positional distribution:")
    print(f"{'Position':<12} {'N_qot':>7} {'%qot':>8} {'baseline%':>10} {'E':>7}")
    for cat in ['LF', 'pos1', 'MID_inner', 'pre_LL', 'LL']:
        n_qot = pos_qot.get(cat, 0)
        n_all = pos_all.get(cat, 1)
        p_qot_at_pos = n_qot / n_all if n_all > 0 else 0
        e = p_qot_at_pos / baseline_qot if baseline_qot > 0 else float('nan')
        print(f"{cat:<12} {n_qot:>7} {p_qot_at_pos*100:>7.1f}% {baseline_qot*100:>9.1f}% {e:>6.2f}×")

# === 3. qot→qot Self-Succession Positional ===
print("\n" + "="*65)
print("3. QOT SELF-SUCCESSION POSITIONAL DECOMPOSITION")
print("="*65)

for dialect, bigrams_list in [('A', A_bigrams), ('B', B_bigrams)]:
    total_n = len(bigrams_list)
    qot_count = sum(1 for pw, nw, pp in bigrams_list if get_onset(nw) == 'qot')
    baseline_qot = qot_count / total_n

    qot_prev = [(pw, nw, pp) for pw, nw, pp in bigrams_list if get_onset(pw) == 'qot']
    qot_qot = [(pw, nw, pp) for pw, nw, pp in qot_prev if get_onset(nw) == 'qot']

    total_prev = len(qot_prev)
    total_hits = len(qot_qot)
    p_glob = total_hits / total_prev if total_prev > 0 else 0
    E_glob = p_glob / baseline_qot if baseline_qot > 0 else float('nan')
    print(f"\n{dialect}-dialect qot→qot: N_prev={total_prev}, N_hits={total_hits}, E={E_glob:.2f}×")

    agg = defaultdict(lambda: [0, 0])
    for pw, nw, pp in qot_prev:
        cat = agg_pos_pair(pp)
        agg[cat][0] += 1
        if get_onset(nw) == 'qot':
            agg[cat][1] += 1

    print(f"{'Position':<20} {'N_prev':>8} {'N_hits':>8} {'P(cond)':>10} {'Baseline':>10} {'E':>8}")
    for cat in ["LF→pos1", "pos1→pos2", "MID_inner", "pre_LL→LL"]:
        n_p, n_h = agg[cat]
        if n_p == 0:
            continue
        p_cond = n_h / n_p
        e = p_cond / baseline_qot if baseline_qot > 0 else float('nan')
        print(f"{cat:<20} {n_p:>8} {n_h:>8} {p_cond*100:>9.1f}% {baseline_qot*100:>9.1f}% {e:>8.2f}×")

    # Word-level: same vs different word
    same_word = sum(1 for pw, nw, pp in qot_qot if pw == nw)
    diff_word = total_hits - same_word
    print(f"Same word: {same_word}/{total_hits} ({same_word/total_hits*100:.1f}%); Different word: {diff_word}/{total_hits} ({diff_word/total_hits*100:.1f}%)")

# === 4. qot Cross-Onset Bigram Rules ===
print("\n" + "="*65)
print("4. QOT CROSS-ONSET BIGRAM RULES")
print("="*65)

def analyze_qot_coupling(bigrams, next_onset, dialect):
    total_n = len(bigrams)
    next_count = sum(1 for pw, nw, pp in bigrams if get_onset(nw) == next_onset)
    baseline = next_count / total_n

    qot_prev = [(pw, nw, pp) for pw, nw, pp in bigrams if get_onset(pw) == 'qot']
    hits = [(pw, nw, pp) for pw, nw, pp in qot_prev if get_onset(nw) == next_onset]

    total_prev = len(qot_prev)
    total_hits = len(hits)
    p_glob = total_hits / total_prev if total_prev > 0 else 0
    E_glob = p_glob / baseline if baseline > 0 else float('nan')

    print(f"\n{dialect} qot→{next_onset}: N_hits={total_hits}/{total_prev}, baseline={baseline*100:.1f}%, P(cond)={p_glob*100:.1f}%, E={E_glob:.2f}×")

    # Positional
    agg = defaultdict(lambda: [0, 0])
    for pw, nw, pp in qot_prev:
        cat = agg_pos_pair(pp)
        agg[cat][0] += 1
        if get_onset(nw) == next_onset:
            agg[cat][1] += 1

    for cat in ["LF→pos1", "pos1→pos2", "MID_inner", "pre_LL→LL"]:
        n_p, n_h = agg[cat]
        if n_p == 0:
            continue
        p_c = n_h / n_p
        e = p_c / baseline if baseline > 0 else float('nan')
        print(f"  {cat}: {n_h}/{n_p} ({p_c*100:.1f}%), E={e:.2f}×")

    # Top word pairs
    pair_counts = Counter((pw, nw) for pw, nw, pp in hits)
    print(f"  Top pairs: {', '.join(f'{pw}→{nw}({cnt})' for (pw,nw),cnt in pair_counts.most_common(5))}")

    return E_glob, total_hits

# A-dialect: qot→daiin, qot→y, qot→qot(already done)
print("\n--- A-dialect qot outgoing couplings ---")
for next_onset in ['d', 'y', 'ch', 'sh', 'qok', 'ok', 'ot', 'r']:
    analyze_qot_coupling(A_bigrams, next_onset, 'A')

print("\n--- B-dialect qot outgoing couplings ---")
for next_onset in ['r', 'd', 'y', 'ch', 'sh', 'qok', 'ok', 'ot']:
    analyze_qot_coupling(B_bigrams, next_onset, 'B')

# === 5. qot Body Structure ===
print("\n" + "="*65)
print("5. QOT BODY STRUCTURE (onset-stripped)")
print("="*65)
for dialect, words_list in [('A', A_words), ('B', B_words)]:
    qot_words = [w for w, cat in words_list if get_onset(w) == 'qot']
    bodies = Counter(w[3:] for w in qot_words)  # strip 'qot'
    zero_mid_count = sum(cnt for body, cnt in bodies.items() if len(body) <= 2)  # short body = just suffix
    total = len(qot_words)
    print(f"\n{dialect}-dialect qot bodies (N={total}):")
    print(f"Top 15 bodies:")
    for body, cnt in bodies.most_common(15):
        print(f"  qot+'{body}': {cnt} ({cnt/total*100:.1f}%)")

# === 6. Full qot bigram row (all successors) ===
print("\n" + "="*65)
print("6. FULL QOT SUCCESSOR DISTRIBUTION")
print("="*65)

for dialect, bigrams_list in [('A', A_bigrams), ('B', B_bigrams)]:
    total_n = len(bigrams_list)
    qot_prev = [(get_onset(nw), pp) for pw, nw, pp in bigrams_list if get_onset(pw) == 'qot']
    total_prev = len(qot_prev)
    if total_prev == 0:
        continue
    next_onset_counts = Counter(onset for onset, pp in qot_prev)
    all_next_counts = Counter(get_onset(nw) for pw, nw, pp in bigrams_list)
    print(f"\n{dialect}-dialect qot successors (N_prev={total_prev}):")
    print(f"{'Onset':<10} {'N':>6} {'P(cond)':>9} {'baseline':>10} {'E':>7}")
    for onset in ['d', 'ch', 'sh', 'qok', 'ok', 'ot', 'qot', 'y', 'ol', 's', 'r', 'other']:
        n = next_onset_counts.get(onset, 0)
        p_cond = n / total_prev
        base = all_next_counts.get(onset, 0) / total_n
        e = p_cond / base if base > 0 else float('nan')
        if n > 0 or onset in ['d', 'ch']:
            print(f"{onset:<10} {n:>6} {p_cond*100:>8.1f}% {base*100:>9.1f}% {e:>6.2f}×")
