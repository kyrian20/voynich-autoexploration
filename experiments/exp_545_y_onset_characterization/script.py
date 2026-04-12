"""
exp_545: y-onset full characterization (H_new_FG)
4-part methodology: vocabulary, positional, within-line bigrams, y-LF pos1 profile.
A herbal_a and B all.
Focus: y LF enrichment in B; y as pos1 opener for o/ok/ot LF lines; y→ch, y→d coupling.
Compare y to ch/sh/d/template class profiles for complete major-class taxonomy.
"""

import re
from collections import Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else '?'

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.2: return f'{E:.2f}×'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

def parse_corpus(path):
    lines_A_ha = []
    lines_B_all = []
    with open(path, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw.startswith('<'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', raw)
            if not m:
                continue
            folio_raw, n_str, locus, text = m.groups()
            lc = locus.lstrip('+*=/~&').lstrip('@')
            if not lc.startswith('P'):
                continue
            try:
                n = int(n_str)
            except ValueError:
                continue
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = (edy_count / len(words)) >= 0.05
            if is_b:
                lines_B_all.append(words)
            elif n <= 56:
                lines_A_ha.append(words)
    return lines_A_ha, lines_B_all

lines_A, lines_B = parse_corpus(CORPUS)
print(f"A herbal_a: {len(lines_A)} lines; B all: {len(lines_B)} lines")

for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    print(f"\n{'='*60}")
    print(f"SECTION: {label}")
    print(f"{'='*60}")

    all_words = [w for ln in lines for w in ln]
    N_words = len(all_words)
    onset_counts = Counter(get_onset(w) for w in all_words)
    y_total = onset_counts.get('y', 0)
    y_rate = y_total / N_words if N_words else 0
    print(f"\nTotal words: {N_words}; y tokens: {y_total} ({y_rate:.1%})")

    # --- Part 1: Vocabulary ---
    y_words = [w for w in all_words if get_onset(w) == 'y']
    y_word_cnt = Counter(y_words)
    N_y = len(y_words)
    print(f"\n## Part 1: y Vocabulary ({N_y} tokens, {len(y_word_cnt)} types)")
    top20 = y_word_cnt.most_common(20)
    print(f"Top words: {', '.join(f'{w}({c/N_y:.1%})' for w, c in top20)}")

    # Body class (y is mostly the word 'y' itself plus compound forms)
    print("Single-char 'y' proportion:", y_word_cnt.get('y', 0) / N_y if N_y else 0)
    non_bare = [(w, c) for w, c in y_word_cnt.most_common() if w != 'y']
    print(f"Non-bare-y top types ({len(non_bare)} types): {', '.join(f'{w}({c/N_y:.1%})' for w, c in non_bare[:10])}")

    # --- Part 2: Positional distribution ---
    print(f"\n## Part 2: y Positional Distribution")
    pos1_elig = [ln for ln in lines if len(ln) >= 2]
    mid_elig = [ln for ln in lines if len(ln) >= 3]
    ll_elig = [ln for ln in lines if len(ln) >= 3]
    lf_elig = [ln for ln in lines if len(ln) >= 2]

    obs_pos1 = sum(1 for ln in pos1_elig if get_onset(ln[0]) == 'y')
    obs_mid = sum(sum(1 for w in ln[1:-1] if get_onset(w) == 'y') for ln in mid_elig)
    obs_ll = sum(1 for ln in ll_elig if get_onset(ln[-2]) == 'y')
    obs_lf = sum(1 for ln in lf_elig if get_onset(ln[-1]) == 'y')

    N_pos1_lines = len(pos1_elig)
    N_mid_words = sum(len(ln[1:-1]) for ln in mid_elig)
    N_ll_lines = len(ll_elig)
    N_lf_lines = len(lf_elig)

    print(f"Baseline y rate: {y_rate:.3f}")
    print(f"{'Position':<8} {'obs/N':<15} {'rate':<8} {'E×':<6} {'flag'}")
    for pos_name, obs, N_pos in [
        ('pos1', obs_pos1, N_pos1_lines),
        ('MID', obs_mid, N_mid_words),
        ('LL', obs_ll, N_ll_lines),
        ('LF', obs_lf, N_lf_lines),
    ]:
        rate = obs / N_pos if N_pos else 0
        E = rate / y_rate if y_rate else 0
        print(f"{pos_name:<8} {obs}/{N_pos:<12} {rate:.3f}   {E:.2f}×  {flag(obs, E)}")

    # --- Part 3: Within-line bigrams (y→X) ---
    print(f"\n## Part 3: y Within-line Bigrams (y→X)")
    sender_bigrams = []
    for ln in lines:
        for i in range(len(ln) - 1):
            if get_onset(ln[i]) == 'y':
                sender_bigrams.append(get_onset(ln[i+1]))
    N_sender = len(sender_bigrams)
    print(f"y sender bigrams: N={N_sender}")

    target_cnt = Counter(sender_bigrams)
    mid_onsets = [get_onset(w) for ln in lines for w in ln[1:]]
    N_mid_all = len(mid_onsets)
    mid_onset_rate = Counter(mid_onsets)

    print(f"{'y→X':<12} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for target, obs in sorted(target_cnt.items(), key=lambda x: -x[1])[:15]:
        exp_rate = mid_onset_rate.get(target, 0) / N_mid_all if N_mid_all else 0
        exp = exp_rate * N_sender
        E = obs / exp if exp > 0 else 0
        print(f"y→{target:<10} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

    # --- Part 4: y-LF lines pos1 profile ---
    print(f"\n## Part 4: y-LF Lines Pos1 Profile")
    y_lf_lines = [ln for ln in lf_elig if get_onset(ln[-1]) == 'y']
    N_yLF = len(y_lf_lines)
    yLF_rate = N_yLF / len(lf_elig)
    print(f"y-LF lines: {N_yLF} ({yLF_rate:.1%} of {len(lf_elig)} lines)")

    yLF_elig = [ln for ln in y_lf_lines if len(ln) >= 2]
    pos1_targets = Counter(get_onset(ln[0]) for ln in yLF_elig)
    N_yLF_elig = len(yLF_elig)

    pos1_all_onsets = Counter(get_onset(ln[0]) for ln in pos1_elig)
    N_pos1_all = sum(pos1_all_onsets.values())

    print(f"y-LF eligible (len>=2): {N_yLF_elig}")
    print(f"{'pos1 onset':<14} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for onset, obs in sorted(pos1_targets.items(), key=lambda x: -x[1])[:12]:
        base_rate = pos1_all_onsets.get(onset, 0) / N_pos1_all if N_pos1_all else 0
        exp = base_rate * N_yLF_elig
        E = obs / exp if exp > 0 else 0
        print(f"{onset:<14} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

print("\n## Cross-dialect summary — see result.md")
