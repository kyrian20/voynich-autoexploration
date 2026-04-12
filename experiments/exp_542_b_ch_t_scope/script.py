"""
exp_542: B ch→t CONF section scope (H_new_FE)
Test: is B ch→t (E=1.77×/obs=35, F548) B-dialect-wide or section-specific?
Also: A herbal_a ch→t rate; ch→k and ch→l cross-section consistency.
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
    """Returns lines keyed by section_label.
    Sections: A herbal_a (n<=56 not b_dialect); B herbal (b_dialect, folio<=72);
    B astro (b_dialect, folio 73-84); B cosmo (b_dialect, folio 85-102); B pharma (b_dialect, folio 103-116).
    Uses folio number extracted from folio_raw field for B section classification.
    """
    sections = defaultdict(list)
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
            # B-dialect detection
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = (edy_count / len(words)) >= 0.05
            # Extract folio number from folio_raw
            folio = folio_raw.lstrip('+*=&~')
            m2 = re.search(r'(\d+)', folio)
            folio_num = int(m2.group(1)) if m2 else 0
            if is_b:
                if folio_num <= 72:
                    sections['B herbal'].append(words)
                elif folio_num <= 84:
                    sections['B astro'].append(words)
                elif folio_num <= 102:
                    sections['B cosmo'].append(words)
                elif folio_num <= 116:
                    sections['B pharma'].append(words)
            else:
                if n <= 56:
                    sections['A herbal_a'].append(words)
    return sections

sections = parse_corpus(CORPUS)
for label in ['A herbal_a', 'B herbal', 'B astro', 'B pharma', 'B cosmo']:
    print(f"{label}: {len(sections[label])} lines")

def ch_bigrams(lines):
    """Compute ch→X bigrams and ch→t specifically."""
    sender_bigrams = []
    for ln in lines:
        for i in range(len(ln) - 1):
            if get_onset(ln[i]) == 'ch':
                sender_bigrams.append(get_onset(ln[i+1]))
    N_sender = len(sender_bigrams)
    target_cnt = Counter(sender_bigrams)

    # Expected baseline: onset rates in non-pos1 positions
    mid_onsets = [get_onset(w) for ln in lines for w in ln[1:]]
    N_mid = len(mid_onsets)
    mid_rates = Counter(mid_onsets)

    return N_sender, target_cnt, mid_rates, N_mid

print(f"\n{'='*65}")
print(f"ch→t, ch→k, ch→l: section breakdown")
print(f"{'='*65}")
print(f"{'Section':<15} {'N_sender':<10} {'t_obs':<7} {'t_E':<7} {'t_flag':<10} {'k_obs':<7} {'k_E':<7} {'l_obs':<7} {'l_E':<7}")

target_sums = defaultdict(lambda: [0, 0.0])  # obs, exp

for label in ['A herbal_a', 'B herbal', 'B astro', 'B pharma', 'B cosmo']:
    lines = sections[label]
    if not lines:
        print(f"{label:<15} (no lines)")
        continue
    N_sender, target_cnt, mid_rates, N_mid = ch_bigrams(lines)

    def get_signal(target):
        obs = target_cnt.get(target, 0)
        exp_rate = mid_rates.get(target, 0) / N_mid if N_mid else 0
        exp = exp_rate * N_sender
        E = obs / exp if exp > 0 else 0
        return obs, exp, E

    t_obs, t_exp, t_E = get_signal('t')
    k_obs, k_exp, k_E = get_signal('k')
    l_obs, l_exp, l_E = get_signal('l')

    print(f"{label:<15} {N_sender:<10} {t_obs:<7} {t_E:<7.2f} {flag(t_obs, t_E):<10} {k_obs:<7} {k_E:<7.2f} {l_obs:<7} {l_E:<7.2f}")

print(f"\n{'='*65}")
print(f"B all pooled (herbal+astro+pharma+cosmo): full ch→X table")
print(f"{'='*65}")
b_all_lines = sections['B herbal'] + sections['B astro'] + sections['B pharma'] + sections['B cosmo']
N_sender_B, target_cnt_B, mid_rates_B, N_mid_B = ch_bigrams(b_all_lines)
print(f"B all N_sender={N_sender_B}")
print(f"{'ch→X':<12} {'obs':<6} {'exp':<7} {'E×':<6} {'flag'}")
for target, obs in sorted(target_cnt_B.items(), key=lambda x: -x[1])[:12]:
    exp_rate = mid_rates_B.get(target, 0) / N_mid_B if N_mid_B else 0
    exp = exp_rate * N_sender_B
    E = obs / exp if exp > 0 else 0
    print(f"ch→{target:<9} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")

# Also check: for A herbal_a, what is ch→t and ch→qot?
print(f"\n{'='*65}")
print(f"A herbal_a ch→X: focus on t, k, l, qot, d")
print(f"{'='*65}")
N_sender_A, target_cnt_A, mid_rates_A, N_mid_A = ch_bigrams(sections['A herbal_a'])
print(f"A herbal_a N_sender={N_sender_A}")
for target in ['t', 'k', 'l', 'd', 'qot', 'ch', 'sh']:
    obs = target_cnt_A.get(target, 0)
    exp_rate = mid_rates_A.get(target, 0) / N_mid_A if N_mid_A else 0
    exp = exp_rate * N_sender_A
    E = obs / exp if exp > 0 else 0
    print(f"ch→{target:<9} {obs:<6} {exp:<7.1f} {E:.2f}×  {flag(obs, E)}")
