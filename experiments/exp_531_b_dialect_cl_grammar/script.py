"""
exp_531: B-dialect CL grammar — pooled B herbal+pharma d→ok confirmation + B astro full survey

Part 1: Pooled B herbal + B pharma d→ok (from exp_530 candidate CONF)
  exp_530 found: B herbal d→ok E=1.75×/obs=9; B pharma d→ok E=1.90×/obs=4
  Pooled: N_cond=70, obs=13, exp=7.25, E=1.79× (CONF candidate if pooling valid)
  Test: explicit pooled analysis with B herbal+pharma combined dataset
  Also check d→d and other B pharma signals.

Part 2: B astro full CL grammar survey (high power: ~690 pairs)
  B astro: folios 73-84 B-dialect — highest power B-dialect section for CL
  Survey all major senders for signals ≥(dir) threshold
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

b_herbal_folios = {n: ls for n, ls in folio_lines.items() if n <= 72 and is_b_dialect(ls)}
b_pharma_folios = {n: ls for n, ls in folio_lines.items() if 103 <= n <= 116 and is_b_dialect(ls)}
b_astro_folios  = {n: ls for n, ls in folio_lines.items() if 73 <= n <= 84 and is_b_dialect(ls)}

print(f"B herbal: {len(b_herbal_folios)} folios, {sum(len(v) for v in b_herbal_folios.values())} lines")
print(f"B pharma: {len(b_pharma_folios)} folios, {sum(len(v) for v in b_pharma_folios.values())} lines")
print(f"B astro:  {len(b_astro_folios)} folios, {sum(len(v) for v in b_astro_folios.values())} lines")

def build_cl_pairs(section_folios):
    pairs = []
    for n, lines in sorted(section_folios.items()):
        for i in range(len(lines) - 1):
            sender_lf = get_onset(lines[i][-1])
            recv_lf = get_onset(lines[i+1][-1])
            pairs.append((sender_lf, recv_lf))
    return pairs

def section_lf_base(section_folios):
    all_lines = [ln for ls in section_folios.values() for ln in ls]
    lf = Counter(get_onset(ln[-1]) for ln in all_lines)
    N = len(all_lines)
    return {cls: cnt/N for cls, cnt in lf.items()}, N, lf

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Pooled B herbal + B pharma d→ok confirmation
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 1: POOLED B herbal + B pharma CL GRAMMAR")
print("="*70)

# Combine folios
b_hp_folios = {}
b_hp_folios.update(b_herbal_folios)
b_hp_folios.update(b_pharma_folios)

b_hp_pairs = build_cl_pairs(b_hp_folios)
b_hp_base, N_hp, b_hp_lf = section_lf_base(b_hp_folios)

print(f"\nPooled B herbal+pharma: {len(b_hp_folios)} folios, {N_hp} lines, {len(b_hp_pairs)} pairs")
print(f"\nPooled LF distribution:")
for cls, cnt in b_hp_lf.most_common(12):
    print(f"  {cls}: {cnt} ({100*cnt/N_hp:.1f}%)")

# Full sender survey for pooled
major_hp = [cls for cls, cnt in b_hp_lf.most_common() if cnt >= 10]
print(f"\nMajor LF classes (N_lf≥10): {major_hp}")

above_threshold_hp = []

for sender in major_hp:
    sender_pairs = [(s, r) for s, r in b_hp_pairs if s == sender]
    N_cond = len(sender_pairs)
    receiver_counts = Counter(r for _, r in sender_pairs)

    print(f"\n  Pooled {sender}-LF as SENDER (N_cond={N_cond}):")
    key_classes = {'d','ch','a','o','sh','ok','ot','y','qok','qot','ol','t','s', sender}
    all_recvs = set(list(receiver_counts.keys())) | key_classes
    rows = []
    for recv in all_recvs:
        obs = receiver_counts.get(recv, 0)
        exp = b_hp_base.get(recv, 0) * N_cond
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
            above_threshold_hp.append((sender, recv, obs, exp, E, flg))

print("\n" + "="*70)
print("PART 1 SUMMARY: POOLED B herbal+pharma ABOVE THRESHOLD")
print("="*70)
if above_threshold_hp:
    print(f"\n  {'sender':>8} → {'recv':>8}  {'obs':>5} {'exp':>6} {'E':>7}  flag")
    for sender, recv, obs, exp, E, flg in sorted(above_threshold_hp, key=lambda x: -x[4]):
        print(f"  {sender:>8} → {recv:>8}  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
else:
    print("  NONE above (dir) threshold")

# Specific check: d→ok
print("\n--- d→ok specific check ---")
d_pairs = [(s,r) for s,r in b_hp_pairs if s == 'd']
N_cond_d = len(d_pairs)
obs_dok = sum(1 for _,r in d_pairs if r == 'ok')
exp_dok = b_hp_base.get('ok', 0) * N_cond_d
E_dok = obs_dok / exp_dok if exp_dok > 0 else 0
print(f"  d→ok: N_cond={N_cond_d}, obs={obs_dok}, exp={exp_dok:.2f}, E={E_dok:.2f}×  {flag(obs_dok, E_dok)}")
# Compare B herbal only
bh_pairs = build_cl_pairs(b_herbal_folios)
bh_base, N_bh, bh_lf = section_lf_base(b_herbal_folios)
bh_d = [(s,r) for s,r in bh_pairs if s == 'd']
obs_bh = sum(1 for _,r in bh_d if r == 'ok')
exp_bh = bh_base.get('ok', 0) * len(bh_d)
print(f"  B herbal only d→ok: N_cond={len(bh_d)}, obs={obs_bh}, exp={exp_bh:.2f}, E={obs_bh/exp_bh if exp_bh > 0 else 0:.2f}×  {flag(obs_bh, obs_bh/exp_bh if exp_bh > 0 else 0)}")
# B pharma only
bp_pairs = build_cl_pairs(b_pharma_folios)
bp_base, N_bp, bp_lf = section_lf_base(b_pharma_folios)
bp_d = [(s,r) for s,r in bp_pairs if s == 'd']
obs_bp = sum(1 for _,r in bp_d if r == 'ok')
exp_bp = bp_base.get('ok', 0) * len(bp_d)
print(f"  B pharma only d→ok: N_cond={len(bp_d)}, obs={obs_bp}, exp={exp_bp:.2f}, E={obs_bp/exp_bp if exp_bp > 0 else 0:.2f}×  {flag(obs_bp, obs_bp/exp_bp if exp_bp > 0 else 0)}")

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: B astro full CL grammar survey
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("PART 2: B astro FULL CL GRAMMAR SURVEY")
print("="*70)

b_astro_pairs = build_cl_pairs(b_astro_folios)
b_astro_base, N_ba, b_astro_lf = section_lf_base(b_astro_folios)

print(f"\nB astro: {len(b_astro_folios)} folios, {N_ba} lines, {len(b_astro_pairs)} pairs")
print(f"\nB astro LF distribution:")
for cls, cnt in b_astro_lf.most_common(12):
    print(f"  {cls}: {cnt} ({100*cnt/N_ba:.1f}%)")

major_ba = [cls for cls, cnt in b_astro_lf.most_common() if cnt >= 10]
print(f"\nMajor B astro LF classes (N_lf≥10): {major_ba}")

above_threshold_ba = []

for sender in major_ba:
    sender_pairs = [(s, r) for s, r in b_astro_pairs if s == sender]
    N_cond = len(sender_pairs)
    receiver_counts = Counter(r for _, r in sender_pairs)

    print(f"\n  B astro {sender}-LF as SENDER (N_cond={N_cond}):")
    key_classes = {'d','ch','a','o','sh','ok','ot','y','qok','qot','ol','t','s', sender}
    all_recvs = set(list(receiver_counts.keys())) | key_classes
    rows = []
    for recv in all_recvs:
        obs = receiver_counts.get(recv, 0)
        exp = b_astro_base.get(recv, 0) * N_cond
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
            above_threshold_ba.append((sender, recv, obs, exp, E, flg))
        elif obs >= 10 and E >= 1.5:
            above_threshold_ba.append((sender, recv, obs, exp, E, flg))

print("\n" + "="*70)
print("PART 2 SUMMARY: B astro CL SIGNALS ABOVE THRESHOLD")
print("="*70)
# Deduplicate
seen_pairs = set()
dedup = []
for item in sorted(above_threshold_ba, key=lambda x: -x[4]):
    key = (item[0], item[1])
    if key not in seen_pairs:
        seen_pairs.add(key)
        dedup.append(item)

if dedup:
    print(f"\n  {'sender':>8} → {'recv':>8}  {'obs':>5} {'exp':>6} {'E':>7}  flag")
    for sender, recv, obs, exp, E, flg in dedup:
        print(f"  {sender:>8} → {recv:>8}  {obs:>5} {exp:>6.2f} {E:>7.2f}×  {flg}")
else:
    print("  NONE above (dir) threshold")
