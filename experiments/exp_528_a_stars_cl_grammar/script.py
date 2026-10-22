"""
exp_528: A stars cross-line (CL) coupling grammar

A stars has 131 within-folio CL pairs across 5 folios.
Folio 58 dominates: 72/131 pairs (55%).
LF distribution: d(18.4%), ch(16.9%), a(11%), o(10.3%), sh(7.4%), ok(7.4%), ot(6.6%).

Questions:
1. Does A stars have a CL chain analogous to A herbal_a (d→qot→ch→o→sh)?
2. Which LF class pairs are coupled in A stars CL?
3. Is f58 special, or do all A stars folios show similar CL patterns?
4. Cross-section: do any A herbal_a CL signals (d→qot, d→ch etc.) replicate in A stars?

Methodology: same as exp_511-524 (within-folio consecutive line pairs, LF class of sender vs receiver).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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

folio_lines = parse_corpus(CORPUS)

a_stars_folios = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
a_ha_folios = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}

a_stars_lines = [ln for ls in a_stars_folios.values() for ln in ls]
a_ha_lines = [ln for ls in a_ha_folios.values() for ln in ls]

print(f"A stars: {len(a_stars_folios)} folios, {len(a_stars_lines)} lines")
print(f"A herbal_a: {len(a_ha_folios)} folios, {len(a_ha_lines)} lines")

def build_cl_pairs(section_folios):
    """Build consecutive within-folio line pairs."""
    pairs = []  # [(sender_LF, receiver_LF)]
    for n, lines in sorted(section_folios.items()):
        for i in range(len(lines) - 1):
            sender_lf = get_onset(lines[i][-1])
            receiver_lf = get_onset(lines[i+1][-1])
            pairs.append((sender_lf, receiver_lf))
    return pairs

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

a_stars_pairs = build_cl_pairs(a_stars_folios)
a_ha_pairs = build_cl_pairs(a_ha_folios)

# LF base rates
a_stars_lf = Counter(get_onset(ln[-1]) for ln in a_stars_lines)
N_st = len(a_stars_lines)
a_ha_lf = Counter(get_onset(ln[-1]) for ln in a_ha_lines)
N_ha = len(a_ha_lines)

N_pairs_st = len(a_stars_pairs)
N_pairs_ha = len(a_ha_pairs)

print(f"\nA stars CL pairs: {N_pairs_st}")
print(f"A herbal_a CL pairs: {N_pairs_ha}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Full CL matrix for A stars
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: A STARS FULL CL MATRIX")
print("="*70)

def cl_sender(pairs, sender_class, lf_base, N_pairs, label=""):
    """For a given sender LF class, compute receiver distribution."""
    sender_pairs = [(s, r) for s, r in pairs if s == sender_class]
    N_cond = len(sender_pairs)
    receiver_counts = Counter(r for _, r in sender_pairs)

    print(f"\n  {label} {sender_class}-LF as SENDER (N_cond={N_cond}):")
    if N_cond == 0:
        print("    (no pairs)")
        return

    rows = []
    for cls, obs in receiver_counts.most_common(12):
        exp = (lf_base.get(cls, 0) / N_pairs) * N_cond
        E = obs / exp if exp > 0 else 0
        rows.append((cls, obs, exp, E))
    # Add key classes not in top
    key_classes = {'d', 'ch', 'a', 'o', 'sh', 'ok', 'ot', 'y', 's', sender_class}
    shown = {cls for cls, _, _, _ in rows}
    for cls in key_classes - shown:
        obs = receiver_counts.get(cls, 0)
        exp = (lf_base.get(cls, 0) / N_pairs) * N_cond
        E = obs / exp if exp > 0 else 0
        rows.append((cls, obs, exp, E))
    rows.sort(key=lambda x: -x[3])

    print(f"  {'cls':>8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    seen = set()
    for cls, obs, exp, E in rows:
        if cls in seen: continue
        seen.add(cls)
        print(f"  {cls:>8} {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flag(obs, E)}")
    return receiver_counts, N_cond

# A stars: receiver LF base rate = lf_base[cls] / N_pairs
# Standard: receiver base = a_stars_lf[cls] / N_stars
# We'll use section-wide LF distribution as baseline (consistent with exp_511-524)
a_stars_lf_base = {cls: cnt / N_st for cls, cnt in a_stars_lf.items()}

def cl_sender_survey(pairs, lf_base, N_pairs, N_total, label, top_classes=None):
    """Survey all major senders."""
    if top_classes is None:
        lf_counts = Counter(s for s, _ in pairs)
        top_classes = [cls for cls, _ in lf_counts.most_common() if lf_counts[cls] >= 3]

    for sender in top_classes:
        sender_pairs = [(s, r) for s, r in pairs if s == sender]
        N_cond = len(sender_pairs)
        receiver_counts = Counter(r for _, r in sender_pairs)

        print(f"\n  [{label}] {sender}-LF as SENDER (N_cond={N_cond}):")
        if N_cond == 0:
            print("    (no pairs)")
            continue

        rows = []
        all_classes = set(list(receiver_counts.keys()) + ['d','ch','a','o','sh','ok','ot','y','ol','s',sender])
        for cls in all_classes:
            obs = receiver_counts.get(cls, 0)
            base_rate = lf_base.get(cls, 0)
            exp = base_rate * N_cond
            E = obs / exp if exp > 0 else 0
            rows.append((cls, obs, exp, E))
        rows.sort(key=lambda x: -x[3])

        print(f"  {'cls':>8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
        seen = set()
        for cls, obs, exp, E in rows[:15]:
            if cls in seen: continue
            seen.add(cls)
            print(f"  {cls:>8} {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flag(obs, E)}")

major_classes = ['d', 'ch', 'a', 'o', 'sh', 'ok', 'ot', 'y', 'ol', 's']
cl_sender_survey(a_stars_pairs, a_stars_lf_base, N_pairs_st, N_st, "A stars", major_classes)

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: Top CL signals summary (above any threshold)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: A STARS CL SIGNALS ABOVE THRESHOLD")
print("="*70)

# Compute all pairwise E values
above_threshold = []
for sender in major_classes:
    sender_pairs = [(s, r) for s, r in a_stars_pairs if s == sender]
    N_cond = len(sender_pairs)
    if N_cond < 3:
        continue
    receiver_counts = Counter(r for _, r in sender_pairs)
    for receiver, obs in receiver_counts.items():
        base_rate = a_stars_lf_base.get(receiver, 0)
        exp = base_rate * N_cond
        E = obs / exp if exp > 0 else 0
        flg = flag(obs, E)
        if obs >= 3 and E >= 2.5:
            above_threshold.append((sender, receiver, obs, exp, E, flg))

above_threshold.sort(key=lambda x: -x[4])
print("\nAll A stars CL signals at (dir) or above:")
if above_threshold:
    print(f"  {'sender':>8} → {'recv':>8}  {'obs':>5} {'exp':>6} {'E':>7}  flag")
    for sender, recv, obs, exp, E, flg in above_threshold:
        print(f"  {sender:>8} → {recv:>8}  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
else:
    print("  None above (dir) threshold")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: A herbal_a chain signals in A stars (cross-section check)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: A HERBAL_a CL CHAIN SIGNALS IN A STARS")
print("="*70)

# A herbal_a confirmed CL signals: d→qot(F491), d→t(F508), qot→ch(F490), ch→o(F506), o→sh(F507)
chain_signals = [
    ('d', 'qot', 'F491 CONF'),
    ('d', 't', 'F508 CONF'),
    ('qot', 'ch', 'F490 CONF'),
    ('ch', 'o', 'F506 CONF'),
    ('o', 'sh', 'F507 (dir)'),
    ('sh', 'ok', 'F509 dir'),
    ('sh', 't', 'F510 (dir)'),
    ('t', 'd', 'near-CONF'),
]

print(f"\nA herbal_a chain signals replicated in A stars:")
print(f"  {'signal':>30}  {'obs':>5} {'exp':>6} {'E':>7}  flag  [A_ha_signal]")
for sender, recv, ha_label in chain_signals:
    sender_pairs = [(s, r) for s, r in a_stars_pairs if s == sender]
    N_cond = len(sender_pairs)
    obs = sum(1 for _, r in sender_pairs if r == recv)
    base_rate = a_stars_lf_base.get(recv, 0)
    exp = base_rate * N_cond if N_cond > 0 else 0
    E = obs / exp if exp > 0 else 0
    print(f"  {sender}→{recv:>6} (N_cond={N_cond:>3})  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flag(obs,E)}  [{ha_label}]")

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: Folio-specific CL (is f58 driving everything?)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 4: FOLIO-SPECIFIC CL PATTERNS (is f58 driving signals?)")
print("="*70)

for n in sorted(a_stars_folios.keys()):
    lines = a_stars_folios[n]
    pairs = [(get_onset(lines[i][-1]), get_onset(lines[i+1][-1])) for i in range(len(lines)-1)]
    lf_this = Counter(get_onset(ln[-1]) for ln in lines)
    N_this = len(lines)
    print(f"\n  Folio {n}: {N_this} lines, {len(pairs)} pairs")
    print(f"  LF: {', '.join(f'{cls}={cnt}' for cls, cnt in lf_this.most_common(6))}")
    # Show any sender→recv with obs>=2
    for sender in ['d','ch','a','o','sh','ok']:
        sp = [(s,r) for s,r in pairs if s == sender]
        rc = Counter(r for _,r in sp)
        for recv, obs in rc.most_common(3):
            if obs >= 2:
                base_rate = a_stars_lf_base.get(recv, 0)
                exp = base_rate * len(sp)
                E = obs/exp if exp > 0 else 0
                print(f"    {sender}→{recv}: obs={obs}, E={E:.2f}×  {flag(obs,E)}")
