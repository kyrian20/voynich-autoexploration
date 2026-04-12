"""
exp_548: o→a coupling deep characterization (H_new_FJ)
1. Which specific a-onset words follow o?
2. Reverse coupling a→o — symmetric or directional?
3. B section scope: B herbal vs B astro vs B pharma
4. A section scope: A stars (57-72), A cosmo (73-90 A-dialect)
5. Positional context: where in lines do o→a pairs occur?
"""

import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh',
    'ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f',
    'o','e','a','n','m'
]

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else None

def parse_corpus(path):
    sections = defaultdict(list)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m:
                continue
            folio_raw, n_str, lc, text = m.groups()
            n = int(n_str)
            lc_clean = lc.lstrip('+*=/~&').lstrip('@')
            if not lc_clean.startswith('P'):
                continue
            words = [w for w in re.split(r'[-.\s]', text)
                     if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words:
                continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy_count / len(words) >= 0.05

            folio = folio_raw.lstrip('+*=&~')
            m2 = re.search(r'(\d+)', folio)
            folio_num = int(m2.group(1)) if m2 else 0

            if is_b:
                sections['B_all'].append((folio_raw, words))
                if folio_num <= 72:
                    sections['B_herbal'].append((folio_raw, words))
                elif folio_num <= 84:
                    sections['B_astro'].append((folio_raw, words))
                elif folio_num <= 116:
                    sections['B_pharma'].append((folio_raw, words))
            else:
                if n <= 56:
                    sections['A_ha'].append((folio_raw, words))
                elif folio_num <= 72:
                    sections['A_stars'].append((folio_raw, words))
                elif folio_num <= 90:
                    sections['A_cosmo'].append((folio_raw, words))

    return sections

sections = parse_corpus(CORPUS)
for k, v in sections.items():
    print(f"{k}: {len(v)} lines")

def compute_bigram_stats(lines, sender_onset, target_onset=None, label=''):
    """Compute bigrams from sender_onset; if target_onset given, focus on that target."""
    all_words = [w for _, ws in lines for w in ws]
    N_total = len(all_words)

    # MID baseline
    mid_onset_counts = Counter()
    mid_total = 0
    for _, ws in lines:
        n = len(ws)
        for i in range(1, n-1):
            mid_onset_counts[get_onset(ws[i])] += 1
            mid_total += 1

    sender_count = 0
    target_counts = Counter()
    target_words = Counter()  # specific words
    position_counts = Counter()  # where in line (pos1=0, MID, LL, LF)

    for _, ws in lines:
        n = len(ws)
        for i in range(n-1):
            if get_onset(ws[i]) == sender_onset:
                sender_count += 1
                tgt_word = ws[i+1]
                tgt_onset = get_onset(tgt_word)
                target_counts[tgt_onset] += 1
                if target_onset is None or tgt_onset == target_onset:
                    target_words[tgt_word] += 1
                    # position of the sender
                    if i == 0:
                        pos = 'pos1'
                    elif i == n-2:
                        pos = 'LL'
                    elif i == n-1:
                        pos = 'LF_sender'
                    else:
                        pos = 'MID'
                    position_counts[pos] += 1

    return sender_count, target_counts, target_words, position_counts, mid_onset_counts, mid_total

print("\n" + "="*60)
print("=== Part 1: Specific a-onset words following o ===")
for label, key in [("A herbal_a", "A_ha"), ("B all", "B_all")]:
    lines = sections[key]
    sc, tc, tw, pc, mid_c, mid_t = compute_bigram_stats(lines, 'o', 'a', label)
    exp_a_rate = mid_c.get('a', 0) / mid_t if mid_t else 0
    exp_a = exp_a_rate * sc
    obs_a = tc.get('a', 0)
    E_a = obs_a / exp_a if exp_a else 0
    print(f"\n{label}: o→a obs={obs_a}, exp={exp_a:.1f}, E={E_a:.2f}×")
    print(f"Specific a-onset words that follow o (top 15):")
    for w, c in tw.most_common(15):
        print(f"  {w}: {c}")
    print(f"Position of o-sender in o→a pairs:")
    total_pairs = sum(pc.values())
    for pos, cnt in sorted(pc.items(), key=lambda x: -x[1]):
        print(f"  {pos}: {cnt}/{total_pairs} ({100*cnt/total_pairs:.1f}%)")

print("\n" + "="*60)
print("=== Part 2: Reverse coupling a→o ===")
for label, key in [("A herbal_a", "A_ha"), ("B all", "B_all")]:
    lines = sections[key]
    all_words = [w for _, ws in lines for w in ws]
    N_total = len(all_words)
    mid_c = Counter()
    mid_t = 0
    for _, ws in lines:
        n = len(ws)
        for i in range(1, n-1):
            mid_c[get_onset(ws[i])] += 1
            mid_t += 1

    a_sender_count = 0
    a_to_o = 0
    for _, ws in lines:
        n = len(ws)
        for i in range(n-1):
            if get_onset(ws[i]) == 'a':
                a_sender_count += 1
                if get_onset(ws[i+1]) == 'o':
                    a_to_o += 1

    exp_o_rate = mid_c.get('o', 0) / mid_t if mid_t else 0
    exp_o = exp_o_rate * a_sender_count
    E_ao = a_to_o / exp_o if exp_o else 0
    flag = ''
    if E_ao >= 1.5 and a_to_o >= 10:
        flag = 'CONF'
    elif E_ao >= 2.0 and a_to_o >= 5:
        flag = 'dir'
    elif E_ao >= 2.5 and a_to_o >= 3:
        flag = '(dir)'
    elif E_ao < 0.7 and a_to_o >= 3:
        flag = 'DEPL'
    print(f"\n{label}: a-sender={a_sender_count}; a→o: obs={a_to_o}, exp={exp_o:.1f}, E={E_ao:.2f}× {flag}")

print("\n" + "="*60)
print("=== Part 3: B section scope of o→a ===")
for label, key in [("B herbal", "B_herbal"), ("B astro", "B_astro"), ("B pharma", "B_pharma")]:
    lines = sections.get(key, [])
    if not lines:
        print(f"\n{label}: 0 lines, skip")
        continue
    sc, tc, tw, pc, mid_c, mid_t = compute_bigram_stats(lines, 'o', 'a', label)
    obs_a = tc.get('a', 0)
    exp_a_rate = mid_c.get('a', 0) / mid_t if mid_t else 0
    exp_a = exp_a_rate * sc
    E_a = obs_a / exp_a if exp_a else 0
    flag = ''
    if E_a >= 1.5 and obs_a >= 10:
        flag = 'CONF'
    elif E_a >= 2.0 and obs_a >= 5:
        flag = 'dir'
    elif E_a >= 2.5 and obs_a >= 3:
        flag = '(dir)'
    elif E_a < 0.7 and obs_a >= 3:
        flag = 'DEPL'
    print(f"\n{label} ({len(lines)} lines): o-sender={sc}; o→a: obs={obs_a}, exp={exp_a:.1f}, E={E_a:.2f}× {flag}")

print("\n" + "="*60)
print("=== Part 4: A section scope of o→a ===")
for label, key in [("A herbal_a", "A_ha"), ("A stars", "A_stars"), ("A cosmo", "A_cosmo")]:
    lines = sections.get(key, [])
    if not lines:
        print(f"\n{label}: 0 lines, skip")
        continue
    sc, tc, tw, pc, mid_c, mid_t = compute_bigram_stats(lines, 'o', 'a', label)
    obs_a = tc.get('a', 0)
    exp_a_rate = mid_c.get('a', 0) / mid_t if mid_t else 0
    exp_a = exp_a_rate * sc
    E_a = obs_a / exp_a if exp_a else 0
    flag = ''
    if E_a >= 1.5 and obs_a >= 10:
        flag = 'CONF'
    elif E_a >= 2.0 and obs_a >= 5:
        flag = 'dir'
    elif E_a >= 2.5 and obs_a >= 3:
        flag = '(dir)'
    elif E_a < 0.7 and obs_a >= 3:
        flag = 'DEPL'
    print(f"\n{label} ({len(lines)} lines): o-sender={sc}; o→a: obs={obs_a}, exp={exp_a:.1f}, E={E_a:.2f}× {flag}")

print("\n" + "="*60)
print("=== Part 5: a-onset general bigram profile (what a→X looks like) ===")
for label, key in [("A herbal_a", "A_ha"), ("B all", "B_all")]:
    lines = sections[key]
    mid_c = Counter()
    mid_t = 0
    for _, ws in lines:
        n = len(ws)
        for i in range(1, n-1):
            mid_c[get_onset(ws[i])] += 1
            mid_t += 1

    a_sc = 0
    a_tc = Counter()
    for _, ws in lines:
        n = len(ws)
        for i in range(n-1):
            if get_onset(ws[i]) == 'a':
                a_sc += 1
                a_tc[get_onset(ws[i+1])] += 1

    print(f"\n{label}: a-sender bigrams={a_sc}")
    print("Top a→X:")
    for tgt, obs in a_tc.most_common(12):
        if obs < 2:
            break
        exp_rate = mid_c.get(tgt, 0) / mid_t if mid_t else 0
        exp_n = exp_rate * a_sc
        E = obs / exp_n if exp_n else 0
        flag = ''
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
        elif E < 0.7 and obs >= 3:
            flag = 'DEPL'
        print(f"  a→{tgt}: obs={obs}, exp={exp_n:.1f}, E={E:.2f}× {flag}")
