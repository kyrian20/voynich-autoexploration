"""
exp_541: ch-onset full characterization (H_new_FC)
4-part methodology identical to exp_540 (sh) and exp_534-537 (template classes).
A herbal_a and B all.
Parts: (1) vocabulary, (2) positional distribution, (3) within-line bigrams, (4) ch-LF lines pos1 profile.
Compare ch profile to sh (F544/F545) and template classes (F539/F543).
"""

import re
from collections import Counter, defaultdict

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
    lines_A_ha = []  # A herbal_a: n<=56, not b_dialect
    lines_B_all = []  # all b_dialect
    with open(path, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw.startswith('<'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', raw)
            if not m:
                continue
            folio_raw, n_str, locus, text = m.groups()
            folio = folio_raw.lstrip('+*=&~')
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
            # B-dialect detection
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
    ch_total = onset_counts.get('ch', 0)
    ch_rate = ch_total / N_words if N_words else 0
    print(f"\nTotal words: {N_words}; ch tokens: {ch_total} ({ch_rate:.1%})")

    # --- Part 1: Vocabulary ---
    ch_words = [w for w in all_words if get_onset(w) == 'ch']
    ch_word_cnt = Counter(ch_words)
    N_ch = len(ch_words)
    print(f"\n## Part 1: ch Vocabulary ({N_ch} tokens, {len(ch_word_cnt)} types)")
    top20 = ch_word_cnt.most_common(20)
    top_str = ', '.join(f"{w}({c/N_ch:.1%})" for w, c in top20)
    print(f"Top words: {top_str}")

    # Body class analysis
    def body_class(word):
        stem = word[2:] if word.startswith('ch') else word  # remove 'ch' prefix
        if stem.endswith('aiin') or stem.endswith('ain'):
            return 'aiin-body'
        if stem.endswith('edy') or stem.endswith('eedy'):
            return 'edy-body'
        if stem.endswith('y') or stem.endswith('ey') or stem.endswith('eey'):
            return 'y-body'
        if stem.endswith('ol') or stem.endswith('or') or stem.endswith('al') or stem.endswith('ar'):
            return 'al/ol-body'
        if stem.endswith('o') or stem.startswith('o'):
            return 'o-body'
        if stem.startswith('d'):
            return 'd-mediated'
        if stem == '' or len(stem) <= 1:
            return 'bare-ch'
        return 'other'

    body_counts = Counter(body_class(w) for w in ch_words)
    print("Body class breakdown:")
    for bc, cnt in body_counts.most_common():
        print(f"  {bc}: {cnt} ({cnt/N_ch:.1%})")

    # --- Part 2: Positional distribution ---
    print(f"\n## Part 2: ch Positional Distribution")
    pos1_elig = [ln for ln in lines if len(ln) >= 2]
    mid_elig = [ln for ln in lines if len(ln) >= 3]
    ll_elig = [ln for ln in lines if len(ln) >= 3]
    lf_elig = [ln for ln in lines if len(ln) >= 2]

    N_pos1 = sum(len(ln) for ln in pos1_elig)
    N_mid = sum(len(ln[1:-1]) for ln in mid_elig)
    N_ll = sum(1 for ln in ll_elig)
    N_lf = sum(1 for ln in lf_elig)

    obs_pos1 = sum(1 for ln in pos1_elig if get_onset(ln[0]) == 'ch')
    obs_mid = sum(sum(1 for w in ln[1:-1] if get_onset(w) == 'ch') for ln in mid_elig)
    obs_ll = sum(1 for ln in ll_elig if get_onset(ln[-2]) == 'ch')
    obs_lf = sum(1 for ln in lf_elig if get_onset(ln[-1]) == 'ch')

    # Baseline
    pos1_all = [ln[0] for ln in pos1_elig]
    base_pos1 = sum(1 for w in pos1_all if get_onset(w) == 'ch') / len(pos1_all) if pos1_all else 0
    base_mid_words = [w for ln in mid_elig for w in ln[1:-1]]
    base_mid = sum(1 for w in base_mid_words if get_onset(w) == 'ch') / len(base_mid_words) if base_mid_words else 0
    all_pen = [ln[-2] for ln in ll_elig]
    base_ll = sum(1 for w in all_pen if get_onset(w) == 'ch') / len(all_pen) if all_pen else 0
    all_lf_w = [ln[-1] for ln in lf_elig]
    base_lf = sum(1 for w in all_lf_w if get_onset(w) == 'ch') / len(all_lf_w) if all_lf_w else 0

    print(f"Baseline ch rate: overall={ch_rate:.3f}, pos1={base_pos1:.3f}, MID={base_mid:.3f}, LL={base_ll:.3f}, LF={base_lf:.3f}")
    print(f"{'Position':<8} {'obs/N':<15} {'rate':<8} {'E×':<6} {'flag'}")
    for pos_name, obs, N_pos, base in [
        ('pos1', obs_pos1, len(pos1_elig), ch_rate),
        ('MID', obs_mid, N_mid, ch_rate),
        ('LL', obs_ll, N_ll, ch_rate),
        ('LF', obs_lf, N_lf, ch_rate),
    ]:
        rate = obs / N_pos if N_pos else 0
        E = rate / ch_rate if ch_rate else 0
        print(f"{pos_name:<8} {obs}/{N_pos:<12} {rate:.3f}   {E:.2f}×  {flag(obs, E)}")

    # --- Part 3: Within-line bigrams (ch→X) ---
    print(f"\n## Part 3: ch Within-line Bigrams (ch→X)")
    sender_bigrams = []
    for ln in lines:
        for i in range(len(ln) - 1):
            if get_onset(ln[i]) == 'ch':
                sender_bigrams.append(get_onset(ln[i+1]))
    N_sender = len(sender_bigrams)
    print(f"ch sender bigrams: N={N_sender}")

    target_cnt = Counter(sender_bigrams)
    # Expected: target onset baseline rate in all non-final positions (MID positions)
    mid_onsets = [get_onset(w) for ln in lines for w in ln[1:]]  # all positions except pos1
    N_mid_all = len(mid_onsets)
    mid_onset_rate = Counter(mid_onsets)

    print(f"{'ch→X':<12} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for target, obs in sorted(target_cnt.items(), key=lambda x: -x[1])[:15]:
        exp_rate = mid_onset_rate.get(target, 0) / N_mid_all if N_mid_all else 0
        exp = exp_rate * N_sender
        E = obs / exp if exp > 0 else 0
        print(f"ch→{target:<9} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

    # --- Part 4: ch-LF lines pos1 profile ---
    print(f"\n## Part 4: ch-LF Lines Pos1 Profile")
    ch_lf_lines = [ln for ln in lf_elig if get_onset(ln[-1]) == 'ch']
    N_chLF = len(ch_lf_lines)
    chLF_rate = N_chLF / len(lf_elig)
    print(f"ch-LF lines: {N_chLF} ({chLF_rate:.1%} of {len(lf_elig)} lines)")

    # pos1 of ch-LF lines (len>=2)
    chLF_elig = [ln for ln in ch_lf_lines if len(ln) >= 2]
    pos1_targets = Counter(get_onset(ln[0]) for ln in chLF_elig)
    N_chLF_elig = len(chLF_elig)

    # baseline pos1 onset rates
    pos1_all_onsets = Counter(get_onset(ln[0]) for ln in pos1_elig)
    N_pos1_all = sum(pos1_all_onsets.values())

    print(f"ch-LF eligible (len>=2): {N_chLF_elig}")
    print(f"{'pos1 onset':<14} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for onset, obs in sorted(pos1_targets.items(), key=lambda x: -x[1])[:12]:
        base_rate = pos1_all_onsets.get(onset, 0) / N_pos1_all if N_pos1_all else 0
        exp = base_rate * N_chLF_elig
        E = obs / exp if exp > 0 else 0
        print(f"{onset:<14} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

print("\n\n## Cross-dialect summary")
print("See result.md for synthesis.")
