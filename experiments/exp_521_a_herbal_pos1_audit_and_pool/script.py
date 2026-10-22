"""
exp_521: A herbal pos1 audit + pooled CONF test + ot-LF pos2=a check

Goals:
1. H_new_EG: Audit F455/F456 — recompute ok-LF and ot-LF pos1=y with strict 1-56 A-dialect
   definition, using same baseline methodology as established findings.
2. H_new_EH: Pool A herbal_a (1-56) + A stars (57-72) o-LF for CONF test
3. H_new_EF: ot-LF pos2=a check in A herbal_a — verify (dir) and examine word identities
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol',
    'sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for o in ONSET_PRIORITY:
        if word.startswith(o):
            return o
    return word[0] if word else 'other'

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def parse_corpus():
    folio_lines = defaultdict(list)
    pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    with open(CORPUS, encoding='utf-8') as f:
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

folio_lines = parse_corpus()

# ── Section definitions ────────────────────────────────────────────────────────
# A herbal_a: 1-56, A-dialect (strict narrow definition)
a_ha_56 = [ln for n, lines in folio_lines.items()
           if n <= 56 and not is_b_dialect(lines)
           for ln in lines]

# A stars: 57-72, A-dialect
a_stars_57_72 = [ln for n, lines in folio_lines.items()
                 if 57 <= n <= 72 and not is_b_dialect(lines)
                 for ln in lines]

# Combined A herbal+stars
a_ha_and_stars = a_ha_56 + a_stars_57_72

# A herbal_a broad: 1-72, A-dialect (what F455/F456 may have used)
a_ha_72 = [ln for n, lines in folio_lines.items()
           if n <= 72 and not is_b_dialect(lines)
           for ln in lines]

print(f"A herbal_a (1-56): {len(a_ha_56)} lines")
print(f"A stars (57-72): {len(a_stars_57_72)} lines")
print(f"Combined (1-72 A-dialect): {len(a_ha_72)} lines")
print(f"A herbal+stars (1-72 A-dialect, same lines): {len(a_ha_and_stars)} lines")
print()

# ── Helper functions ────────────────────────────────────────────────────────────
def compute_pos1(lines, lf_class, pos1_class, min_len=3):
    """Compute E and obs for pos1=pos1_class in lf_class-LF lines."""
    # Section pos1 baseline
    pos1_total = sum(1 for ln in lines if len(ln) >= 2)
    pos1_target = sum(1 for ln in lines if len(ln) >= 2 and get_onset(ln[0]) == pos1_class)
    if pos1_total == 0:
        return None, None, None, None
    base = pos1_target / pos1_total

    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    N_elig = len(elig)
    obs = sum(1 for ln in elig if get_onset(ln[0]) == pos1_class)
    exp = base * N_elig
    E = obs / exp if exp > 0 else 0.0
    return obs, N_elig, exp, E

def compute_pos2(lines, lf_class, pos2_class, min_len=3):
    """Compute E and obs for pos2=pos2_class in lf_class-LF lines."""
    pos2_total = sum(1 for ln in lines if len(ln) >= 3)
    pos2_target = sum(1 for ln in lines if len(ln) >= 3 and get_onset(ln[1]) == pos2_class)
    if pos2_total == 0:
        return None, None, None, None
    base = pos2_target / pos2_total

    elig = [ln for ln in lines if len(ln) >= min_len and get_onset(ln[-1]) == lf_class]
    N_elig = len(elig)
    obs = sum(1 for ln in elig if get_onset(ln[1]) == pos2_class)
    exp = base * N_elig
    E = obs / exp if exp > 0 else 0.0
    return obs, N_elig, exp, E

def flag(obs, E):
    if obs >= 10 and E >= 1.5:
        return 'CONF'
    elif obs >= 5 and E >= 2.0:
        return 'dir'
    elif obs >= 3 and E >= 2.5:
        return '(dir)'
    elif obs >= 1:
        return f'E={E:.2f}×/N={obs}'
    return '---'

# ── H_new_EG: F455/F456 audit ─────────────────────────────────────────────────
print("=== H_new_EG: F455/F456 AUDIT — ok-LF and ot-LF pos1=y ===")
print()
print("F455: ok-LF → y@pos1 (established E=1.62×/obs=12)")
print("F456: ot-LF → y@pos1 (established E=1.83×/obs=11)")
print()

sections = [
    ("A herbal_a (1-56, strict)", a_ha_56),
    ("A stars (57-72)", a_stars_57_72),
    ("A herbal+stars (1-72 A)", a_ha_72),
]

print(f"{'Section':<30} {'LF':>4} {'N_elig':>7} {'obs':>5} {'E':>7} {'flag'}")
print("-" * 65)

for sec_name, sec_lines in sections:
    for lf_class in ['ok', 'ot', 'o']:
        obs, N_elig, exp, E = compute_pos1(sec_lines, lf_class, 'y')
        if N_elig is None or N_elig == 0:
            print(f"  {sec_name:<28} {lf_class:>4} {'---':>7}")
        else:
            f = flag(obs, E)
            print(f"  {sec_name:<28} {lf_class:>4} {N_elig:>7} {obs:>5} {E:>7.2f}x {f}")
    print()

# ── H_new_EH: Pooled A herbal+stars o-LF CONF test ───────────────────────────
print("=== H_new_EH: POOLED A herbal+stars o-LF pos1=y ===")
obs_pool, N_pool, exp_pool, E_pool = compute_pos1(a_ha_and_stars, 'o', 'y')
y_base = sum(1 for ln in a_ha_and_stars if len(ln) >= 2 and get_onset(ln[0]) == 'y')
pos1_total_pool = sum(1 for ln in a_ha_and_stars if len(ln) >= 2)
print(f"A herbal_a (1-56) + A stars (57-72) combined:")
print(f"  Total lines: {len(a_ha_and_stars)}")
print(f"  pos1 baseline y: {y_base}/{pos1_total_pool} = {y_base/pos1_total_pool:.3f}")
print(f"  o-LF N_elig: {N_pool}")
print(f"  obs: {obs_pool}, exp: {exp_pool:.2f}, E: {E_pool:.2f}x")
print(f"  flag: {flag(obs_pool, E_pool)}")
print()

# Also check ok-LF and ot-LF pooled
for lf_class in ['ok', 'ot']:
    obs_p, N_p, exp_p, E_p = compute_pos1(a_ha_and_stars, lf_class, 'y')
    print(f"  {lf_class}-LF pooled: N_elig={N_p}, obs={obs_p}, E={E_p:.2f}x, flag={flag(obs_p, E_p)}")
print()

# ── H_new_EF: ot-LF pos2=a in A herbal_a ─────────────────────────────────────
print("=== H_new_EF: ot-LF pos2=a CHECK IN A herbal_a (1-56) ===")
obs_a, N_a, exp_a, E_a = compute_pos2(a_ha_56, 'ot', 'a')
print(f"  N_elig: {N_a}, obs: {obs_a}, exp: {exp_a:.2f}, E: {E_a:.2f}x, flag: {flag(obs_a, E_a)}")

# Record the 4 lines with ot-LF and pos2=a
ot_elig = [ln for ln in a_ha_56 if len(ln) >= 3 and get_onset(ln[-1]) == 'ot']
pos2_a_lines = [ln for ln in ot_elig if get_onset(ln[1]) == 'a']
print(f"\n  Lines with ot-LF and pos2=a ({len(pos2_a_lines)} lines):")
for ln in pos2_a_lines:
    print(f"    {[get_onset(w) for w in ln]} | words: {ln}")

# Full pos2 distribution for ot-LF in A herbal_a (1-56)
print("\n--- Full ot-LF pos2 distribution (A herbal_a, 1-56) ---")
pos2_total = sum(1 for ln in a_ha_56 if len(ln) >= 3)
pos2_base = defaultdict(int)
for ln in a_ha_56:
    if len(ln) >= 3:
        pos2_base[get_onset(ln[1])] += 1

pos2_dist = Counter(get_onset(ln[1]) for ln in ot_elig)
print(f"N_elig: {len(ot_elig)}")
print(f"{'pos2':<8} {'obs':>5} {'base%':>7} {'E':>7} {'flag'}")
for cls, cnt in pos2_dist.most_common(10):
    base_rate = pos2_base[cls] / pos2_total if pos2_total > 0 else 0
    exp_v = base_rate * len(ot_elig)
    E_v = cnt / exp_v if exp_v > 0 else 0
    f = flag(cnt, E_v)
    print(f"  {cls:<6} {cnt:>5} {base_rate:>7.3f} {E_v:>7.2f}x {f}")

# ── BONUS: ok-LF pos1=y full cross-section scope ─────────────────────────────
print("\n=== BONUS: ok-LF pos1=y by section (F455 scope audit) ===")
b_astro_lines = [ln for n, lines in folio_lines.items()
                 if 73 <= n <= 84 and is_b_dialect(lines)
                 for ln in lines]
b_pharma_lines = [ln for n, lines in folio_lines.items()
                  if 103 <= n <= 116 and is_b_dialect(lines)
                  for ln in lines]
b_herbal_lines = [ln for n, lines in folio_lines.items()
                  if n <= 72 and is_b_dialect(lines)
                  for ln in lines]
a_cosmo_lines = [ln for n, lines in folio_lines.items()
                 if 85 <= n <= 102 and not is_b_dialect(lines)
                 for ln in lines]

sec_groups = [
    ("A herbal_a (1-56)", a_ha_56),
    ("A stars (57-72)", a_stars_57_72),
    ("A cosmo (85-102)", a_cosmo_lines),
    ("B astro (73-84)", b_astro_lines),
    ("B pharma (103-116)", b_pharma_lines),
    ("B herbal (1-72 B)", b_herbal_lines),
]

print(f"{'Section':<25} {'N_elig':>7} {'obs':>5} {'E':>7} {'flag'}")
print("-" * 55)
for sec_name, sec_lines in sec_groups:
    obs, N_elig, exp, E = compute_pos1(sec_lines, 'ok', 'y')
    if N_elig is None or N_elig == 0:
        print(f"  {sec_name:<23} {'---':>7}")
    else:
        f = flag(obs, E)
        print(f"  {sec_name:<23} {N_elig:>7} {obs:>5} {E:>7.2f}x {f}")

print("\nDone.")
