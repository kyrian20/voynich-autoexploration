"""
exp_529: A stars f58 within-folio CL + B herbal CL grammar

Part 1: H_new_ET — f58 within-folio CL (power test for A stars flat CL)
  f58 has 72 CL pairs (55% of A stars). If A stars has CL structure, it should be
  visible in f58 alone. This tests whether the flat pooled result is a power issue.

Part 2: B herbal CL grammar — first CL survey for B herbal section
  B herbal: 14 folios, 272 lines. Expect ~200-250 CL pairs.
  Does B herbal have a CL chain analogous to A herbal_a's d→qot→ch→o→sh?
  B herbal's dominant LF classes are different from A herbal_a.
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

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

folio_lines = parse_corpus(CORPUS)

a_stars_folios = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
b_herbal_folios = {n: ls for n, ls in folio_lines.items() if n <= 72 and is_b_dialect(ls)}

b_herbal_lines = [ln for ls in b_herbal_folios.values() for ln in ls]
b_herbal_lf = Counter(get_onset(ln[-1]) for ln in b_herbal_lines)
N_bh = len(b_herbal_lines)

print(f"A stars folios: {sorted(a_stars_folios.keys())}")
print(f"B herbal: {len(b_herbal_folios)} folios, {N_bh} lines")
for n in sorted(b_herbal_folios.keys()):
    lines = b_herbal_folios[n]
    print(f"  n={n}: {len(lines)} lines, {len(lines)-1} pairs")

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: f58 within-folio CL (H_new_ET test)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: f58 WITHIN-FOLIO CL (H_new_ET POWER TEST)")
print("="*70)

f58_lines = a_stars_folios[58]
f58_pairs = [(get_onset(f58_lines[i][-1]), get_onset(f58_lines[i+1][-1]))
             for i in range(len(f58_lines)-1)]
f58_lf = Counter(get_onset(ln[-1]) for ln in f58_lines)
N_f58 = len(f58_lines)
N_f58_pairs = len(f58_pairs)

print(f"\nf58: {N_f58} lines, {N_f58_pairs} pairs")
print(f"LF distribution: {dict(f58_lf.most_common(8))}")

# Baseline: f58 LF distribution
f58_lf_base = {cls: cnt / N_f58 for cls, cnt in f58_lf.items()}

# Compute all pairwise for f58
above_threshold_f58 = []
major_classes_f58 = [cls for cls, cnt in f58_lf.most_common() if cnt >= 5]

for sender in major_classes_f58:
    sender_pairs = [(s, r) for s, r in f58_pairs if s == sender]
    N_cond = len(sender_pairs)
    if N_cond < 3:
        continue
    receiver_counts = Counter(r for _, r in sender_pairs)

    print(f"\n  f58 {sender}-LF as SENDER (N_cond={N_cond}):")
    all_recvs = set(list(receiver_counts.keys()) + ['d','ch','a','o','sh','ok','ot','y','s', sender])
    rows = []
    for recv in all_recvs:
        obs = receiver_counts.get(recv, 0)
        exp = f58_lf_base.get(recv, 0) * N_cond
        E = obs / exp if exp > 0 else 0
        rows.append((recv, obs, exp, E))
    rows.sort(key=lambda x: -x[3])

    print(f"  {'cls':>8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    seen = set()
    for recv, obs, exp, E in rows[:12]:
        if recv in seen: continue
        seen.add(recv)
        flg = flag(obs, E)
        print(f"  {recv:>8} {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
        if obs >= 3 and E >= 2.5:
            above_threshold_f58.append((sender, recv, obs, exp, E, flg, 'f58'))

print(f"\n--- f58 CL signals above (dir) ---")
if above_threshold_f58:
    for sender, recv, obs, exp, E, flg, src in above_threshold_f58:
        print(f"  {sender}→{recv}: obs={obs}, E={E:.2f}×  {flg}")
else:
    print("  NONE above (dir) threshold")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: B herbal CL grammar
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: B HERBAL CL GRAMMAR")
print("="*70)

bh_pairs = []
for n, lines in sorted(b_herbal_folios.items()):
    for i in range(len(lines)-1):
        sender_lf = get_onset(lines[i][-1])
        recv_lf = get_onset(lines[i+1][-1])
        bh_pairs.append((sender_lf, recv_lf))

N_bh_pairs = len(bh_pairs)
bh_lf_base = {cls: cnt / N_bh for cls, cnt in b_herbal_lf.items()}

print(f"\nB herbal CL pairs: {N_bh_pairs}")
print(f"\nB herbal LF distribution:")
for cls, cnt in b_herbal_lf.most_common(12):
    print(f"  {cls}: {cnt} ({100*cnt/N_bh:.1f}%)")

# Full sender survey for B herbal major LF classes
major_bh = [cls for cls, cnt in b_herbal_lf.most_common() if cnt >= 7]
print(f"\nMajor B herbal LF classes (N_lf≥7): {major_bh}")

above_threshold_bh = []

for sender in major_bh:
    sender_pairs = [(s, r) for s, r in bh_pairs if s == sender]
    N_cond = len(sender_pairs)
    receiver_counts = Counter(r for _, r in sender_pairs)

    print(f"\n  B herbal {sender}-LF as SENDER (N_cond={N_cond}):")
    key_classes = {'d','ch','a','o','sh','ok','ot','y','qok','qot','ol','t','s', sender}
    all_recvs = set(list(receiver_counts.keys())) | key_classes
    rows = []
    for recv in all_recvs:
        obs = receiver_counts.get(recv, 0)
        exp = bh_lf_base.get(recv, 0) * N_cond
        E = obs / exp if exp > 0 else 0
        rows.append((recv, obs, exp, E))
    rows.sort(key=lambda x: -x[3])

    print(f"  {'cls':>8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    seen = set()
    for recv, obs, exp, E in rows[:15]:
        if recv in seen: continue
        seen.add(recv)
        flg = flag(obs, E)
        print(f"  {recv:>8} {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
        if obs >= 3 and E >= 2.5:
            above_threshold_bh.append((sender, recv, obs, exp, E, flg))

print("\n" + "="*70)
print("PART 2 SUMMARY: B HERBAL CL SIGNALS ABOVE THRESHOLD")
print("="*70)
if above_threshold_bh:
    print(f"\n  {'sender':>8} → {'recv':>8}  {'obs':>5} {'exp':>6} {'E':>7}  flag")
    for sender, recv, obs, exp, E, flg in sorted(above_threshold_bh, key=lambda x: -x[4]):
        print(f"  {sender:>8} → {recv:>8}  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
else:
    print("  NONE above (dir) threshold")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: A herbal_a chain signals in B herbal
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: A HERBAL_a CHAIN SIGNALS IN B HERBAL")
print("="*70)

chain_signals = [
    ('d', 'qot', 'F491 CONF'),
    ('d', 't', 'F508 CONF'),
    ('qot', 'ch', 'F490 CONF'),
    ('ch', 'o', 'F506 CONF'),
    ('o', 'sh', 'F507 (dir)'),
    ('sh', 'ok', 'F509 dir'),
]

print(f"\n  {'signal':>30}  {'obs':>5} {'exp':>6} {'E':>7}  flag  [A_ha_signal]")
for sender, recv, ha_label in chain_signals:
    sp = [(s, r) for s, r in bh_pairs if s == sender]
    N_cond = len(sp)
    obs = sum(1 for _, r in sp if r == recv)
    base_rate = bh_lf_base.get(recv, 0)
    exp = base_rate * N_cond if N_cond > 0 else 0
    E = obs / exp if exp > 0 else 0
    print(f"  {sender}→{recv:>6} (N_cond={N_cond:>3})  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flag(obs,E)}  [{ha_label}]")
