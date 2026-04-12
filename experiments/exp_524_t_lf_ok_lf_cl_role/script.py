"""
exp_524: A herbal_a t-LF and ok-LF CL roles + within-line grammar

H_new_EQ: What does t-LF route to in CL? t is multiply-fed (from d F508+sh F510). Is it a relay or terminal?
H_new_EP: What does ok-LF route to in CL? sh→ok established (F509 dir). Does ok then route back into chain?

Also:
- Full t-LF and ok-LF within-line grammar (pos1/pos2/pen)
- Complete receiver survey: who precedes t-LF and ok-LF?
- Check d→ok CL (d is a hub: d→qot CONF, d→t CONF; does d also route to ok?)
"""

import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset):
            return onset
    return 'other'

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def parse_corpus(path):
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, _, locus_raw, text = m.groups()
        folio = folio_raw.lstrip('+*=&~')
        lc = locus_raw.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'):
            continue
        words = [w for w in re.split(r'[-.\s]', text)
                 if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words:
            continue
        n = folio_num(folio)
        if n is None:
            continue
        folio_lines[n].append(words)
    return folio_lines

folio_lines = parse_corpus(CORPUS)
a_ha = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}

def all_lines(section):
    return [ln for ls in section.values() for ln in ls]

print(f"A herbal_a: {len(a_ha)} folios, {len(all_lines(a_ha))} lines")

def compute_baselines(section):
    lines = all_lines(section)
    pos1_counts = Counter()
    pos2_counts = Counter()
    pen_counts = Counter()
    for ln in lines:
        if len(ln) >= 2:
            pos1_counts[get_onset(ln[0])] += 1
        if len(ln) >= 3:
            pos2_counts[get_onset(ln[1])] += 1
            pen_counts[get_onset(ln[-2])] += 1
    return {
        'pos1': (pos1_counts, sum(pos1_counts.values())),
        'pos2': (pos2_counts, sum(pos2_counts.values())),
        'pen': (pen_counts, sum(pen_counts.values())),
    }

def flag(obs, E):
    if obs >= 10 and E >= 1.5:
        return 'CONF'
    elif obs >= 5 and E >= 2.0:
        return 'dir'
    elif obs >= 3 and E >= 2.5:
        return '(dir)'
    elif E >= 1.0:
        return f'{E:.2f}×'
    else:
        return f'DEPL {E:.2f}×'

def positional_profile(section, lf_class, baselines):
    lines = [ln for ln in all_lines(section) if get_onset(ln[-1]) == lf_class]
    print(f"\n  {lf_class}-LF (N_lines={len(lines)}):")
    for pos_name, pos_idx, min_len in [('pos1', 0, 2), ('pos2', 1, 3), ('pen', -2, 3)]:
        elig = [ln for ln in lines if len(ln) >= min_len]
        counts = Counter(get_onset(ln[pos_idx]) for ln in elig)
        base_counts, base_total = baselines[pos_name]
        N_elig = len(elig)
        print(f"\n    {pos_name} (N_elig={N_elig}):")
        if N_elig == 0:
            print("      (no eligible lines)")
            continue
        chain = {'d','qot','ch','o','sh','ok','ot','y','cth','s','k','t',lf_class}
        rows = []
        for cls, obs in counts.most_common(12):
            exp = (base_counts.get(cls, 0) / base_total) * N_elig
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
        shown = {cls for cls, _, _, _ in rows}
        for cls in chain - shown:
            obs = counts.get(cls, 0)
            exp = (base_counts.get(cls, 0) / base_total) * N_elig
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
        rows.sort(key=lambda x: -x[3])
        print(f"    {'cls':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
        seen = set()
        for cls, obs, exp, E in rows:
            if cls in seen: continue
            seen.add(cls)
            print(f"    {cls:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {flag(obs, E)}")

def build_cl_pairs_simple(section):
    pairs = []
    for n, lines in section.items():
        for i in range(len(lines) - 1):
            pairs.append((lines[i], lines[i+1]))
    return pairs

def cl_sender(pairs, sender_class, lf_base, N_pairs, label=''):
    cond_pairs = [p for p in pairs if get_onset(p[0][-1]) == sender_class]
    N_cond = len(cond_pairs)
    recv_counts = Counter(get_onset(p[1][-1]) for p in cond_pairs)
    chain = ['d','qot','ch','o','sh','ok','ot','y','cth','k','s','t','qo','qok']
    print(f"\n  {sender_class}→X (N_cond={N_cond}) {label}")
    if N_cond == 0:
        print("    (no eligible pairs)")
        return
    print(f"  {'→X':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    rows = []
    shown = set()
    for cls, obs in recv_counts.most_common(10):
        exp = (lf_base.get(cls, 0) / N_pairs) * N_cond
        E = obs / exp if exp > 0 else 0.0
        rows.append((cls, obs, exp, E))
        shown.add(cls)
    for cls in chain:
        if cls not in shown:
            obs = recv_counts.get(cls, 0)
            exp = (lf_base.get(cls, 0) / N_pairs) * N_cond
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
    rows.sort(key=lambda x: -x[3])
    seen = set()
    for cls, obs, exp, E in rows[:14]:
        if cls in seen: continue
        seen.add(cls)
        print(f"  {cls:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {flag(obs, E)}")

def cl_receiver(pairs, recv_class, lf_base, N_pairs, label=''):
    cond_pairs = [p for p in pairs if get_onset(p[1][-1]) == recv_class]
    N_cond = len(cond_pairs)
    send_counts = Counter(get_onset(p[0][-1]) for p in cond_pairs)
    send_base = Counter(get_onset(p[0][-1]) for p in pairs)
    N_send = len(pairs)
    chain = ['d','qot','ch','o','sh','ok','ot','y','cth','k','s','t','qo','qok']
    print(f"\n  X→{recv_class} (N_cond={N_cond}) {label}")
    if N_cond == 0:
        print("    (no eligible pairs)")
        return
    print(f"  {'X→':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    rows = []
    shown = set()
    for cls, obs in send_counts.most_common(10):
        exp = (send_base.get(cls, 0) / N_send) * N_cond
        E = obs / exp if exp > 0 else 0.0
        rows.append((cls, obs, exp, E))
        shown.add(cls)
    for cls in chain:
        if cls not in shown:
            obs = send_counts.get(cls, 0)
            exp = (send_base.get(cls, 0) / N_send) * N_cond
            E = obs / exp if exp > 0 else 0.0
            rows.append((cls, obs, exp, E))
    rows.sort(key=lambda x: -x[3])
    seen = set()
    for cls, obs, exp, E in rows[:14]:
        if cls in seen: continue
        seen.add(cls)
        print(f"  {cls:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {flag(obs, E)}")

# ─────────────────────────────────────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────────────────────────────────────
a_ha_baselines = compute_baselines(a_ha)
pairs_aha = build_cl_pairs_simple(a_ha)
N_pairs = len(pairs_aha)
lf_base = Counter(get_onset(p[1][-1]) for p in pairs_aha)

print(f"\nA herbal_a CL: {N_pairs} pairs")
print("LF distribution:")
for cls, cnt in lf_base.most_common(12):
    print(f"  {cls}: {cnt} ({100*cnt/N_pairs:.1f}%)")

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: t-LF CL role (H_new_EQ)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: t-LF CL ROLE (H_new_EQ)")
print("="*70)

print("\n--- t-LF as SENDER ---")
cl_sender(pairs_aha, 't', lf_base, N_pairs, '(H_new_EQ: relay or terminal?)')

print("\n--- t-LF as RECEIVER ---")
cl_receiver(pairs_aha, 't', lf_base, N_pairs, '(confirm F508: d→t, and F510: sh→t)')

print("\n--- t-LF within-line grammar ---")
positional_profile(a_ha, 't', a_ha_baselines)

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: ok-LF CL role (H_new_EP)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: ok-LF CL ROLE (H_new_EP)")
print("="*70)

print("\n--- ok-LF as SENDER ---")
cl_sender(pairs_aha, 'ok', lf_base, N_pairs, '(H_new_EP: does ok route back to d/qot?)')

print("\n--- ok-LF as RECEIVER ---")
cl_receiver(pairs_aha, 'ok', lf_base, N_pairs, '(confirm F509: sh→ok; other senders?)')

print("\n--- ok-LF within-line grammar (reference, already known F455 FLAGGED, F485 CONF) ---")
positional_profile(a_ha, 'ok', a_ha_baselines)

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: d-LF full CL sender survey (to see if d has more than 2 CL channels)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: d-LF FULL CL SENDER SURVEY (IS d A BROADER HUB?)")
print("="*70)

print("\n--- d-LF as SENDER (full distribution) ---")
cl_sender(pairs_aha, 'd', lf_base, N_pairs, '(check all d→X signals: F491 qot, F508 t; any others?)')

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Extended chain — ot-LF CL role (ot receives from d→qot→... nearby?)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 4: ot-LF CL ROLE (UNEXPECTED CHAIN MEMBER?)")
print("="*70)

print("\n--- ot-LF as SENDER ---")
cl_sender(pairs_aha, 'ot', lf_base, N_pairs, '(does ot route to anything in the chain?)')

print("\n--- ot-LF as RECEIVER ---")
cl_receiver(pairs_aha, 'ot', lf_base, N_pairs, '(who feeds ot?)')

# ─────────────────────────────────────────────────────────────────────────────
# PART 5: Complete A herbal_a CL matrix — all pairwise E values (summarized)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 5: COMPLETE A herbal_a CL MATRIX (top signals per sender)")
print("="*70)

major_classes = ['d','ch','cth','ok','k','ot','sh','y','o','qot','s','t','qo','qok']
print(f"\nAll sender→receiver pairs above (dir) or CONF threshold:")
print(f"{'sender→recv':20} {'obs':>5} {'exp':>6} {'E':>7}  N_cond  flag")

results = []
for sender in major_classes:
    cond = [p for p in pairs_aha if get_onset(p[0][-1]) == sender]
    N_cond = len(cond)
    if N_cond < 5:
        continue
    recv_counts = Counter(get_onset(p[1][-1]) for p in cond)
    for recv_cls, obs in recv_counts.items():
        exp = (lf_base.get(recv_cls, 0) / N_pairs) * N_cond
        E = obs / exp if exp > 0 else 0.0
        if (obs >= 3 and E >= 2.5) or (obs >= 5 and E >= 2.0) or (obs >= 10 and E >= 1.5):
            results.append((sender, recv_cls, obs, exp, E, N_cond))

results.sort(key=lambda x: -x[4])
for sender, recv, obs, exp, E, N_cond in results:
    print(f"{sender+'→'+recv:20} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {N_cond:>6}  {flag(obs, E)}")
