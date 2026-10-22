"""
exp_547: o-onset full characterization
4-part profile: vocabulary, positional distribution, bigrams, o-LF pos1 grammar

Context:
- o-onset is the CL chain pivot in A herbal_a: ch→o CONF (F506), o→sh CONF (F507)
- F502/F503: o-LF pos1=y CONF cross-section (pooled A herbal+stars)
- F504: o-LF pos2=o-self (dir) in A herbal_a
- F505: o-LF pos2=cth (dir) in A herbal_a
- o is a major onset class but has never received formal 4-part characterization

Goal: complete o-onset positional profile analogous to exp_540-545 (sh, ch, d, y).
Focus: A herbal_a and B all; special attention to cross-dialectal stability vs d/y which show A/B inversions.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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
    lines_A_ha = []
    lines_B = []
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
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A_ha.append((folio_raw, words))

    return lines_A_ha, lines_B

lines_A, lines_B = parse_corpus(CORPUS)

print(f"A herbal_a: {len(lines_A)} lines")
print(f"B all: {len(lines_B)} lines")

for label, lines in [("A herbal_a", lines_A), ("B all", lines_B)]:
    print(f"\n{'='*60}")
    print(f"=== {label} ===")
    print(f"{'='*60}")

    all_words = [w for _, ws in lines for w in ws]
    o_words = [w for w in all_words if get_onset(w) == 'o']
    N_total = len(all_words)
    N_o = len(o_words)
    base_rate = N_o / N_total if N_total else 0

    print(f"\n--- Part 1: o Vocabulary ---")
    print(f"Total words: {N_total}, o-onset words: {N_o} ({100*N_o/N_total:.1f}%)")
    o_freq = Counter(o_words)
    print("Top 20 o-onset words:")
    for w, c in o_freq.most_common(20):
        print(f"  {w}: {c} ({100*c/N_o:.1f}%)")

    # Body classification
    body_classes = {
        'y-body': sum(c for w, c in o_freq.items() if 'y' in w[1:]),
        'aiin-body': sum(c for w, c in o_freq.items() if 'aiin' in w or 'ain' in w),
        'edy-body': sum(c for w, c in o_freq.items() if w.endswith('edy') or w.endswith('eedy')),
        'ol/or/ar': sum(c for w, c in o_freq.items() if w in ('ol','or','oar') or w.endswith('ol') or w.endswith('or')),
        'ch-bench': sum(c for w, c in o_freq.items() if 'ch' in w[1:]),
        'sh-bench': sum(c for w, c in o_freq.items() if 'sh' in w[1:]),
    }
    print("\nBody class distribution:")
    for bc, cnt in sorted(body_classes.items(), key=lambda x: -x[1]):
        print(f"  {bc}: {cnt} ({100*cnt/N_o:.1f}%)")

    print(f"\n--- Part 2: Positional Distribution ---")
    pos_counts = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}
    pos_totals = {'pos1': 0, 'MID': 0, 'LL': 0, 'LF': 0}

    for _, ws in lines:
        n = len(ws)
        if n < 2:
            continue
        for i, w in enumerate(ws):
            if i == 0:
                pos = 'pos1'
            elif i == n - 1:
                pos = 'LF'
            elif i == n - 2:
                pos = 'LL'
            else:
                pos = 'MID'
            pos_totals[pos] += 1
            if get_onset(w) == 'o':
                pos_counts[pos] += 1

    # Baseline: overall o rate across the corpus
    overall_o_rate = N_o / N_total if N_total else 0

    print(f"Overall o-onset rate: {100*overall_o_rate:.2f}%")
    for pos in ['pos1', 'MID', 'LL', 'LF']:
        obs = pos_counts[pos]
        tot = pos_totals[pos]
        obs_rate = obs / tot if tot else 0
        E = obs_rate / overall_o_rate if overall_o_rate else 0
        flag = ''
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
        elif E < 0.7:
            flag = 'DEPL'
        print(f"  {pos}: {obs}/{tot} ({100*obs_rate:.2f}%) E={E:.2f}× {flag}")

    print(f"\n--- Part 3: Within-line Bigrams (o→X) ---")
    sender_count = 0
    target_counts = Counter()

    for _, ws in lines:
        n = len(ws)
        for i in range(n - 1):
            if get_onset(ws[i]) == 'o':
                sender_count += 1
                target_counts[get_onset(ws[i+1])] += 1

    # Baseline: MID position onset distribution
    mid_onset_counts = Counter()
    mid_total = 0
    for _, ws in lines:
        n = len(ws)
        for i in range(1, n - 1):
            mid_onset_counts[get_onset(ws[i])] += 1
            mid_total += 1

    print(f"Total o-sender bigrams: {sender_count}")
    print(f"MID baseline words: {mid_total}")
    print("\nTop bigrams (o→X):")
    for tgt, obs in target_counts.most_common(20):
        if obs < 2:
            break
        exp_rate = mid_onset_counts.get(tgt, 0) / mid_total if mid_total else 0
        exp_n = exp_rate * sender_count
        E = obs / exp_n if exp_n > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
        elif E < 0.7 and obs >= 3:
            flag = 'DEPL'
        print(f"  o→{tgt}: obs={obs}, exp={exp_n:.1f}, E={E:.2f}× {flag}")

    print(f"\n--- Part 4: o-LF pos1 Profile ---")
    o_lf_lines = [(fo, ws) for fo, ws in lines if len(ws) >= 2 and get_onset(ws[-1]) == 'o']
    N_olf = len(o_lf_lines)
    print(f"o-LF lines: {N_olf}")

    pos1_counts = Counter()
    pos1_elig = 0
    for _, ws in o_lf_lines:
        if len(ws) >= 2:
            pos1_counts[get_onset(ws[0])] += 1
            pos1_elig += 1

    # Baseline: overall pos1 onset distribution
    pos1_base = Counter()
    pos1_base_total = 0
    for _, ws in lines:
        if len(ws) >= 2:
            pos1_base[get_onset(ws[0])] += 1
            pos1_base_total += 1

    print(f"o-LF lines eligible for pos1 (len≥2): {pos1_elig}")
    print("\nPos1 routing for o-LF lines:")
    for onset, obs in pos1_counts.most_common(15):
        base_cnt = pos1_base.get(onset, 0)
        base_rate = base_cnt / pos1_base_total if pos1_base_total else 0
        exp_n = base_rate * pos1_elig
        E = obs / exp_n if exp_n > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
        elif E < 0.7 and obs >= 3:
            flag = 'DEPL'
        print(f"  {onset}@pos1: obs={obs}/{pos1_elig}, E={E:.2f}× {flag}")

    print(f"\n--- Part 5: o-LF CL Receiver Profile (for reference) ---")
    # What LF class comes AFTER an o-LF line? (o as CL sender)
    # Group by folio, get consecutive pairs
    folio_lines = defaultdict(list)
    for fo, ws in lines:
        folio_lines[fo].append(ws)

    cl_target_counts = Counter()
    cl_sender_total = 0
    for fo, fo_lines_list in folio_lines.items():
        for i in range(len(fo_lines_list) - 1):
            sender_ws = fo_lines_list[i]
            target_ws = fo_lines_list[i + 1]
            if len(sender_ws) >= 2 and len(target_ws) >= 2:
                if get_onset(sender_ws[-1]) == 'o':
                    cl_sender_total += 1
                    cl_target_counts[get_onset(target_ws[-1])] += 1

    # Baseline: overall LF distribution
    lf_base = Counter()
    lf_base_total = 0
    for _, ws in lines:
        if len(ws) >= 2:
            lf_base[get_onset(ws[-1])] += 1
            lf_base_total += 1

    print(f"o-LF CL sender pairs: {cl_sender_total}")
    print("\nCL targets after o-LF (o→X at CL level):")
    for tgt, obs in cl_target_counts.most_common(15):
        if obs < 2:
            break
        base_rate = lf_base.get(tgt, 0) / lf_base_total if lf_base_total else 0
        exp_n = base_rate * cl_sender_total
        E = obs / exp_n if exp_n > 0 else 0
        flag = ''
        if E >= 1.5 and obs >= 10:
            flag = 'CONF'
        elif E >= 2.0 and obs >= 5:
            flag = 'dir'
        elif E >= 2.5 and obs >= 3:
            flag = '(dir)'
        elif E < 0.7 and obs >= 3:
            flag = 'DEPL'
        print(f"  o→{tgt} CL: obs={obs}, exp={exp_n:.1f}, E={E:.2f}× {flag}")
