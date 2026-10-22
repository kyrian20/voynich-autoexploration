"""
exp_543: d-onset full characterization (H_new_FF)
4-part methodology identical to exp_540-541 (sh, ch) and exp_534-537 (template classes).
A herbal_a and B all.
Parts: (1) vocabulary, (2) positional distribution, (3) within-line bigrams, (4) d-LF lines pos1 profile.
Key questions: d LF dominance in A herbal_a; d→qot within-line vs CL; d vocabulary (daiin-dominated?).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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
    d_total = onset_counts.get('d', 0)
    d_rate = d_total / N_words if N_words else 0
    print(f"\nTotal words: {N_words}; d tokens: {d_total} ({d_rate:.1%})")

    # --- Part 1: Vocabulary ---
    d_words = [w for w in all_words if get_onset(w) == 'd']
    d_word_cnt = Counter(d_words)
    N_d = len(d_words)
    print(f"\n## Part 1: d Vocabulary ({N_d} tokens, {len(d_word_cnt)} types)")
    top20 = d_word_cnt.most_common(20)
    top_str = ', '.join(f"{w}({c/N_d:.1%})" for w, c in top20)
    print(f"Top words: {top_str}")

    # Body class analysis (suffix-based)
    def body_class(word):
        # strip 'd' onset
        stem = word[1:] if word.startswith('d') and len(word) > 1 else word
        if stem == 'aiin' or stem == 'ain' or stem.endswith('aiin') or stem.endswith('ain'):
            return 'aiin-body'
        if stem.endswith('edy') or stem.endswith('eedy'):
            return 'edy-body'
        if stem.endswith('y') or stem.endswith('ey') or stem.endswith('eey'):
            return 'y-body'
        if stem.endswith('ol') or stem.endswith('or') or stem.endswith('al') or stem.endswith('ar'):
            return 'al/ol-body'
        if stem.startswith('ch') or stem.endswith('ch'):
            return 'ch-mediated'
        if stem == '' or len(stem) <= 0:
            return 'bare-d'
        return 'other'

    body_counts = Counter(body_class(w) for w in d_words)
    print("Body class breakdown:")
    for bc, cnt in body_counts.most_common():
        print(f"  {bc}: {cnt} ({cnt/N_d:.1%})")

    # --- Part 2: Positional distribution ---
    print(f"\n## Part 2: d Positional Distribution")
    pos1_elig = [ln for ln in lines if len(ln) >= 2]
    mid_elig = [ln for ln in lines if len(ln) >= 3]
    ll_elig = [ln for ln in lines if len(ln) >= 3]
    lf_elig = [ln for ln in lines if len(ln) >= 2]

    obs_pos1 = sum(1 for ln in pos1_elig if get_onset(ln[0]) == 'd')
    obs_mid = sum(sum(1 for w in ln[1:-1] if get_onset(w) == 'd') for ln in mid_elig)
    obs_ll = sum(1 for ln in ll_elig if get_onset(ln[-2]) == 'd')
    obs_lf = sum(1 for ln in lf_elig if get_onset(ln[-1]) == 'd')

    N_pos1_lines = len(pos1_elig)
    N_mid_words = sum(len(ln[1:-1]) for ln in mid_elig)
    N_ll_lines = len(ll_elig)
    N_lf_lines = len(lf_elig)

    print(f"Baseline d rate: {d_rate:.3f}")
    print(f"{'Position':<8} {'obs/N':<15} {'rate':<8} {'E×':<6} {'flag'}")
    for pos_name, obs, N_pos in [
        ('pos1', obs_pos1, N_pos1_lines),
        ('MID', obs_mid, N_mid_words),
        ('LL', obs_ll, N_ll_lines),
        ('LF', obs_lf, N_lf_lines),
    ]:
        rate = obs / N_pos if N_pos else 0
        E = rate / d_rate if d_rate else 0
        print(f"{pos_name:<8} {obs}/{N_pos:<12} {rate:.3f}   {E:.2f}×  {flag(obs, E)}")

    # --- Part 3: Within-line bigrams (d→X) ---
    print(f"\n## Part 3: d Within-line Bigrams (d→X)")
    sender_bigrams = []
    for ln in lines:
        for i in range(len(ln) - 1):
            if get_onset(ln[i]) == 'd':
                sender_bigrams.append(get_onset(ln[i+1]))
    N_sender = len(sender_bigrams)
    print(f"d sender bigrams: N={N_sender}")

    target_cnt = Counter(sender_bigrams)
    # Expected: target onset rate in non-pos1 positions
    mid_onsets = [get_onset(w) for ln in lines for w in ln[1:]]
    N_mid_all = len(mid_onsets)
    mid_onset_rate = Counter(mid_onsets)

    print(f"{'d→X':<12} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for target, obs in sorted(target_cnt.items(), key=lambda x: -x[1])[:15]:
        exp_rate = mid_onset_rate.get(target, 0) / N_mid_all if N_mid_all else 0
        exp = exp_rate * N_sender
        E = obs / exp if exp > 0 else 0
        print(f"d→{target:<10} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

    # --- Part 4: d-LF lines pos1 profile ---
    print(f"\n## Part 4: d-LF Lines Pos1 Profile")
    d_lf_lines = [ln for ln in lf_elig if get_onset(ln[-1]) == 'd']
    N_dLF = len(d_lf_lines)
    dLF_rate = N_dLF / len(lf_elig)
    print(f"d-LF lines: {N_dLF} ({dLF_rate:.1%} of {len(lf_elig)} lines)")

    dLF_elig = [ln for ln in d_lf_lines if len(ln) >= 2]
    pos1_targets = Counter(get_onset(ln[0]) for ln in dLF_elig)
    N_dLF_elig = len(dLF_elig)

    pos1_all_onsets = Counter(get_onset(ln[0]) for ln in pos1_elig)
    N_pos1_all = sum(pos1_all_onsets.values())

    print(f"d-LF eligible (len>=2): {N_dLF_elig}")
    print(f"{'pos1 onset':<14} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
    for onset, obs in sorted(pos1_targets.items(), key=lambda x: -x[1])[:12]:
        base_rate = pos1_all_onsets.get(onset, 0) / N_pos1_all if N_pos1_all else 0
        exp = base_rate * N_dLF_elig
        E = obs / exp if exp > 0 else 0
        print(f"{onset:<14} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

    # --- Part 5: d→qot check (within-line vs expected) ---
    print(f"\n## Part 5: d→qot within-line (vs CL F491)")
    d_to_qot_obs = target_cnt.get('qot', 0)
    exp_rate_qot = mid_onset_rate.get('qot', 0) / N_mid_all if N_mid_all else 0
    exp_qot = exp_rate_qot * N_sender
    E_qot = d_to_qot_obs / exp_qot if exp_qot > 0 else 0
    print(f"d→qot: obs={d_to_qot_obs}, exp={exp_qot:.1f}, E={E_qot:.2f}× → {flag(d_to_qot_obs, E_qot)}")
    print(f"NOTE: F491 is CL (cross-line) d→qot CONF. Within-line d→qot E={E_qot:.2f}× tells if they are the SAME or DIFFERENT mechanisms.")

print("\n\n## Cross-dialect summary")
print("See result.md for synthesis.")
