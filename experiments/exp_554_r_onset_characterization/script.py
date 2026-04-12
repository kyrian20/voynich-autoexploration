import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(w):
    for o in ONSET_PRIORITY:
        if w.startswith(o):
            return o
    return w[0] if w else None

def parse_corpus(filepath):
    lines_A, lines_B = [], []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m:
                continue
            folio_raw, n_str, lc, text = m.group(1), m.group(2), m.group(3), m.group(4)
            lc2 = lc.lstrip('+*=/~&').lstrip('@')
            if not lc2.startswith('P'):
                continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            try:
                n = int(n_str)
            except:
                continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy_count / len(words) >= 0.05
            if is_b:
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, words))
    return lines_A, lines_B

lines_A, lines_B = parse_corpus(CORPUS)
print(f"Corpus: {len(lines_A)} A herbal_a lines, {len(lines_B)} B all lines")

def get_r_words(lines):
    return [w for _, words in lines for w in words if get_onset(w) == 'r']

# Part 1: Vocabulary
print("\n=== Part 1: r-onset vocabulary ===")
for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    tokens = get_r_words(lines)
    total = len(tokens)
    ctr = Counter(tokens)
    print(f"\n{label}: {total} r-onset tokens")
    for w, c in ctr.most_common(20):
        print(f"  {w}: {c} ({100*c/total:.1f}%)")

# Part 2: Positional distribution
print("\n=== Part 2: r-onset positional distribution ===")
def compute_baseline_onset_frac(lines, target_onset):
    total_all = 0; total_target = 0
    for _, words in lines:
        for w in words:
            total_all += 1
            if get_onset(w) == target_onset: total_target += 1
    return total_target / total_all if total_all > 0 else 0

def positional_analysis(lines, target_onset):
    counts = {'pos1':[0,0],'MID':[0,0],'LL':[0,0],'LF':[0,0]}
    for _, words in lines:
        n = len(words)
        if n < 2: continue
        for i, w in enumerate(words):
            o = get_onset(w)
            if i == 0: pos='pos1'
            elif i == n-1: pos='LF'
            elif i == n-2: pos='LL'
            else: pos='MID'
            counts[pos][1] += 1
            if o == target_onset: counts[pos][0] += 1
    return counts

for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    result = positional_analysis(lines, 'r')
    base_frac = compute_baseline_onset_frac(lines, 'r')
    print(f"\n{label}: r baseline frac = {base_frac:.4f}")
    for pos in ['pos1','MID','LL','LF']:
        obs, total = result[pos]
        exp = base_frac * total
        E = obs/exp if exp > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10: flag = 'CONF'
        elif E >= 2.0 and obs >= 5: flag = 'dir'
        elif E >= 2.5 and obs >= 3: flag = '(dir)'
        elif E < 0.7 and obs >= 3: flag = 'DEPL'
        print(f"  {pos}: obs={obs}/{total}, exp={exp:.1f}, E={E:.2f}x {flag}")

# Part 3: Within-line bigrams (MID baseline)
print("\n=== Part 3: r-onset within-line bigrams ===")
def mid_onset_dist(lines):
    dist = Counter(); total = 0
    for _, words in lines:
        n = len(words)
        for i in range(1, n-1):
            o = get_onset(words[i])
            if o: dist[o] += 1; total += 1
    return dist, total

def bigrams_from_onset(lines, sender_onset):
    pairs = []
    for _, words in lines:
        n = len(words)
        for i in range(n-1):
            if get_onset(words[i]) == sender_onset:
                pairs.append(get_onset(words[i+1]))
    return pairs

for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    mid_dist, mid_total = mid_onset_dist(lines)
    pairs = bigrams_from_onset(lines, 'r')
    n_pairs = len(pairs)
    print(f"\n{label}: {n_pairs} r-sender bigrams")
    recv_ctr = Counter(x for x in pairs if x)
    results = []
    for recv, obs in recv_ctr.most_common(20):
        exp = (mid_dist[recv] / mid_total) * n_pairs if mid_total > 0 else 0
        E = obs/exp if exp > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10: flag = 'CONF'
        elif E >= 2.0 and obs >= 5: flag = 'dir'
        elif E >= 2.5 and obs >= 3: flag = '(dir)'
        elif E < 0.7 and obs >= 3: flag = 'DEPL'
        results.append((recv, obs, exp, E, flag))
    results.sort(key=lambda x: -x[3])
    for recv, obs, exp, E, flag in results[:15]:
        print(f"  r→{recv}: obs={obs}, exp={exp:.1f}, E={E:.2f}x {flag}")
    # Check l→r (confirm l→r CONF from exp_553)
    l_pairs = bigrams_from_onset(lines, 'l')
    l_recv = Counter(x for x in l_pairs if x)
    l_total = len(l_pairs)
    r_obs = l_recv.get('r', 0)
    r_exp_l = (mid_dist['r'] / mid_total) * l_total if mid_total > 0 else 0
    r_E_l = r_obs / r_exp_l if r_exp_l > 0 else 0
    flag_l = 'CONF' if r_E_l >= 1.5 and r_obs >= 10 else ('dir' if r_E_l >= 2.0 and r_obs >= 5 else ('(dir)' if r_E_l >= 2.5 and r_obs >= 3 else ''))
    print(f"  (cross-check) l→r: obs={r_obs}, exp={r_exp_l:.1f}, E={r_E_l:.2f}x {flag_l}")

# Part 4: r-LF pos1 profile
print("\n=== Part 4: r-LF pos1 profile ===")
def lf_pos1_profile(lines, lf_onset):
    lf_lines = [words for _, words in lines if len(words) >= 2 and get_onset(words[-1]) == lf_onset]
    n_lf = len(lf_lines)
    print(f"  N r-LF lines: {n_lf}")
    if n_lf < 5:
        print("  Underpowered"); return
    pos1_all = Counter()
    pos1_total = 0
    for _, words in lines:
        if len(words) >= 2:
            o = get_onset(words[0])
            if o: pos1_all[o] += 1; pos1_total += 1
    pos1_lf = Counter()
    for words in lf_lines:
        o = get_onset(words[0])
        if o: pos1_lf[o] += 1
    results = []
    for onset, obs in pos1_lf.most_common(15):
        exp = (pos1_all[onset] / pos1_total) * n_lf if pos1_total > 0 else 0
        E = obs/exp if exp > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10: flag = 'CONF'
        elif E >= 2.0 and obs >= 5: flag = 'dir'
        elif E >= 2.5 and obs >= 3: flag = '(dir)'
        elif E < 0.7 and obs >= 3: flag = 'DEPL'
        results.append((onset, obs, exp, E, flag))
    results.sort(key=lambda x: -x[3])
    for onset, obs, exp, E, flag in results[:10]:
        print(f"  {onset}@pos1: obs={obs}, exp={exp:.1f}, E={E:.2f}x {flag}")

for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    print(f"\n{label} r-LF:")
    lf_pos1_profile(lines, 'r')

# Part 5: r frequency summary and r→l reverse coupling
print("\n=== Part 5: Summary ===")
for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    r_tokens = get_r_words(lines)
    total_words = sum(len(words) for _, words in lines)
    print(f"{label}: {len(r_tokens)} r tokens ({100*len(r_tokens)/total_words:.2f}% of words)")
    # r→l specifically
    mid_dist, mid_total = mid_onset_dist(lines)
    pairs = bigrams_from_onset(lines, 'r')
    recv_ctr = Counter(x for x in pairs if x)
    n_pairs = len(pairs)
    for target in ['l','ol','r','a','o']:
        obs = recv_ctr.get(target, 0)
        exp = (mid_dist.get(target, 0) / mid_total) * n_pairs if mid_total > 0 else 0
        E = obs/exp if exp > 0 else 0
        flag = 'CONF' if E>=1.5 and obs>=10 else ('dir' if E>=2.0 and obs>=5 else ('(dir)' if E>=2.5 and obs>=3 else ('DEPL' if E<0.7 and obs>=3 else '')))
        print(f"  r→{target}: obs={obs}, exp={exp:.1f}, E={E:.2f}x {flag}")

