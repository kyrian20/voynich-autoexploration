"""
exp_523: A herbal_a sh-LF CL cyclicity test + full sh-LF within-line grammar

H_new_EM: Does sh-LF route back to d or qot, completing the CL chain cycle?
           d→qot(F491,CONF)→ch(F490,CONF)→o(F506,CONF)→sh(F507,dir) — is sh→d/qot present?
H_new_EL: What is the full pos1/pos2/pen routing for sh-LF in A herbal_a?

Also:
- Full sh-LF CL sender profile (sh→X for all X)
- Full sh-LF CL receiver profile (X→sh for all X)
- Cross-validation of F507 (o→sh) from receiver side
- Complete chain link re-verification at current methodology
- o-LF pos2 pooled A herbal_a + A stars check (F504/F505 extension)
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

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def parse_corpus(path):
    folio_lines = defaultdict(list)
    # Also keep folio_page mapping for CL pairs (we need to track which lines are on same folio)
    folio_page_lines = defaultdict(list)  # key = (folio_raw, n)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(path, encoding='utf-8') as f:
        raw = f.read()
    for m in pat.finditer(raw):
        folio_raw, line_idx_str, locus_raw, text = m.groups()
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
        line_idx = int(line_idx_str)
        folio_lines[n].append(words)
        folio_page_lines[folio].append((line_idx, words))
    return folio_lines, folio_page_lines

folio_lines, folio_page_lines = parse_corpus(CORPUS)

# Section definitions (by folio number)
a_ha = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
a_st = {n: ls for n, ls in folio_lines.items() if 57 <= n <= 72 and not is_b_dialect(ls)}
b_as = {n: ls for n, ls in folio_lines.items() if 73 <= n <= 84 and is_b_dialect(ls)}

def all_lines(section):
    return [ln for ls in section.values() for ln in ls]

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

print(f"A herbal_a: {len(a_ha)} folios, {len(all_lines(a_ha))} lines")
print(f"A stars: {len(a_st)} folios, {len(all_lines(a_st))} lines")

# ─────────────────────────────────────────────────────────────────────────────
# Baselines
# ─────────────────────────────────────────────────────────────────────────────

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

# ─────────────────────────────────────────────────────────────────────────────
# Within-line grammar profile
# ─────────────────────────────────────────────────────────────────────────────

def positional_profile(section, lf_class, baselines):
    lines = [ln for ln in all_lines(section) if get_onset(ln[-1]) == lf_class]
    print(f"\n  {lf_class}-LF (N_lines={len(lines)}):")
    for pos_name, pos_idx, min_len in [('pos1', 0, 2), ('pos2', 1, 3), ('pen', -2, 3)]:
        elig = [ln for ln in lines if len(ln) >= min_len]
        if pos_idx >= 0:
            counts = Counter(get_onset(ln[pos_idx]) for ln in elig)
        else:
            counts = Counter(get_onset(ln[pos_idx]) for ln in elig)
        base_counts, base_total = baselines[pos_name]
        N_elig = len(elig)
        print(f"\n    {pos_name} (N_elig={N_elig}):")
        if N_elig == 0:
            print("      (no eligible lines)")
            continue
        # Show top classes + chain-relevant classes
        chain = {'d','qot','ch','o','sh','ok','ot','y','cth','s','k',lf_class}
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

# ─────────────────────────────────────────────────────────────────────────────
# Cross-line coupling
# ─────────────────────────────────────────────────────────────────────────────

def build_cl_pairs_folio(section, folio_page_lines, n_set):
    """Build within-folio consecutive line pairs using folio page groupings."""
    pairs = []
    for folio, page_lines in folio_page_lines.items():
        n = folio_num(folio)
        if n not in n_set:
            continue
        sorted_lines = sorted(page_lines, key=lambda x: x[0])
        for i in range(len(sorted_lines) - 1):
            pairs.append((sorted_lines[i][1], sorted_lines[i+1][1]))
    return pairs

a_ha_n_set = set(a_ha.keys())

def build_cl_pairs_simple(section):
    """Within-folio pairs using folio_lines ordering (same as exp_511/522)."""
    # Since folio_lines groups all lines for a folio number together,
    # pairs are consecutive lines within the same folio.
    pairs = []
    for n, lines in section.items():
        for i in range(len(lines) - 1):
            pairs.append((lines[i], lines[i+1]))
    return pairs

# Use same method as exp_511/522
def cl_survey(pairs, section_name):
    N_pairs = len(pairs)
    # Global LF base (for expected values)
    lf_base = Counter(get_onset(p[1][-1]) for p in pairs)

    print(f"\n  {section_name} CL: {N_pairs} pairs")
    print(f"  LF distribution: " + ', '.join(f"{cls}:{cnt}({100*cnt/N_pairs:.1f}%)" for cls, cnt in lf_base.most_common(10)))

    return pairs, lf_base, N_pairs

def cl_sender(pairs, sender_class, lf_base, N_pairs, label=''):
    cond_pairs = [p for p in pairs if get_onset(p[0][-1]) == sender_class]
    N_cond = len(cond_pairs)
    recv_counts = Counter(get_onset(p[1][-1]) for p in cond_pairs)
    chain = ['d','qot','ch','o','sh','ok','ot','y','cth','k','s','t']
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
    chain = ['d','qot','ch','o','sh','ok','ot','y','cth','k','s','t']
    print(f"\n  X→{recv_class} (N_cond={N_cond}) {label}")
    if N_cond == 0:
        print("    (no eligible pairs)")
        return
    # Use sender base (from line-1 of all pairs)
    send_base = Counter(get_onset(p[0][-1]) for p in pairs)
    N_send = len(pairs)
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
# PART 1: sh-LF within-line grammar (H_new_EL)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: sh-LF WITHIN-LINE GRAMMAR (H_new_EL)")
print("="*70)

a_ha_baselines = compute_baselines(a_ha)
positional_profile(a_ha, 'sh', a_ha_baselines)

print("\n--- o-LF for comparison (chain predecessor) ---")
positional_profile(a_ha, 'o', a_ha_baselines)

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: CL chain cyclicity (H_new_EM)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: CL CHAIN CYCLICITY (H_new_EM)")
print("="*70)

pairs_aha = build_cl_pairs_simple(a_ha)
pairs_info, lf_base, N_pairs = cl_survey(pairs_aha, 'A herbal_a')

# Chain link verification table
print("\n  --- Full chain link re-verification ---")
chain_links = [
    ('d', 'qot', 'F491 CONF'),
    ('qot', 'ch', 'F490 CONF'),
    ('ch', 'o', 'F506 CONF'),
    ('o', 'sh', 'F507 dir'),
]
print(f"  {'Link':12} {'obs':>5} {'exp':>6} {'E':>7}  N_cond  Finding  Flag")
for sender, receiver, fid in chain_links:
    cond = [p for p in pairs_aha if get_onset(p[0][-1]) == sender]
    N_cond = len(cond)
    obs = sum(1 for p in cond if get_onset(p[1][-1]) == receiver)
    exp = (lf_base.get(receiver, 0) / N_pairs) * N_cond
    E = obs / exp if exp > 0 else 0.0
    print(f"  {sender}→{receiver:6} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {N_cond:>6}  {fid:12}  {flag(obs, E)}")

# sh as sender — what follows sh?
print("\n  --- sh-LF as SENDER ---")
cl_sender(pairs_aha, 'sh', lf_base, N_pairs, '(H_new_EM: does sh→d/qot complete the cycle?)')

# sh as receiver — what precedes sh? (cross-check F507 from receiver side)
print("\n  --- sh-LF as RECEIVER ---")
cl_receiver(pairs_aha, 'sh', lf_base, N_pairs, '(cross-check: is o→sh present from receiver side?)')

# Cycle-closing candidates
print("\n  --- Cycle-closing candidates ---")
cycle_tests = [
    ('sh', 'd'), ('sh', 'qot'), ('sh', 'ch'), ('sh', 'o'), ('sh', 'sh'),
    ('o', 'd'), ('o', 'qot'), ('sh', 'y'), ('sh', 't'), ('sh', 'ok'),
]
print(f"  {'Link':14} {'obs':>5} {'exp':>6} {'E':>7}  N_cond  Flag")
for sender, receiver in cycle_tests:
    cond = [p for p in pairs_aha if get_onset(p[0][-1]) == sender]
    N_cond = len(cond)
    obs = sum(1 for p in cond if get_onset(p[1][-1]) == receiver)
    exp = (lf_base.get(receiver, 0) / N_pairs) * N_cond
    E = obs / exp if exp > 0 else 0.0
    print(f"  {sender}→{receiver:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {N_cond:>6}  {flag(obs, E)}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: Full receiver surveys for each chain class
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 3: FULL SENDER/RECEIVER SURVEY FOR CHAIN CLASSES")
print("="*70)

for cls in ['d', 'qot', 'ch', 'o', 'sh']:
    cl_sender(pairs_aha, cls, lf_base, N_pairs)

# ─────────────────────────────────────────────────────────────────────────────
# PART 4: o-LF pos2 cross-section check (F504/F505 scope)
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 4: o-LF POS2 CROSS-SECTION (F504/F505 SCOPE CHECK)")
print("="*70)

for sname, section in [('A herbal_a', a_ha), ('A stars', a_st)]:
    lines = all_lines(section)
    print(f"\n  {sname} ({len(lines)} lines):")
    base = compute_baselines(section)
    o_lines = [ln for ln in lines if get_onset(ln[-1]) == 'o' and len(ln) >= 3]
    n_elig = len(o_lines)
    pos2_base_counts, pos2_base_total = base['pos2']
    print(f"  o-LF pos2 (N_elig={n_elig}):")
    pos2_counts = Counter(get_onset(ln[1]) for ln in o_lines)
    print(f"  {'cls':8} {'obs':>5} {'exp':>6} {'E':>7}  flag")
    for cls in ['o', 'cth', 'ch', 'sh', 'y', 'd', 'ok', 'ot', 'qot']:
        obs = pos2_counts.get(cls, 0)
        exp = (pos2_base_counts.get(cls, 0) / pos2_base_total) * n_elig if pos2_base_total > 0 else 0
        E = obs / exp if exp > 0 else 0.0
        print(f"  {cls:8} {obs:>5} {exp:>6.1f} {E:>7.2f}x  {flag(obs, E)}")
