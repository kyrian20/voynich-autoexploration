"""
exp_512: A herbal_a d→qot→ch CL chain verification (H_new_CV)
Also: ok-LF pos2/pen co-occurrence test (H_new_CU)
Also: CL scope test in A cosmo and B herbal (H_new_CT)
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
    return word[0] if word else None

def folio_num(folio):
    m = re.search(r'f(\d+)', folio)
    return int(m.group(1)) if m else None

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words: return False
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

# Section assignments
a_herbal_a_by_folio = {n: lines for n, lines in folio_lines.items() if n <= 56}
a_cosmo_by_folio = {n: lines for n, lines in folio_lines.items() if 85 <= n <= 102}
a_herbal_a_all = [ln for lines in a_herbal_a_by_folio.values() for ln in lines]

# B herbal: folio <=72, B-dialect
b_herbal_by_folio = {}
for n, lines in folio_lines.items():
    if n > 72: continue
    if is_b_dialect(lines):
        b_herbal_by_folio[n] = lines
b_herbal_all = [ln for lines in b_herbal_by_folio.values() for ln in lines]

print(f"A herbal_a: {len(a_herbal_a_all)} lines, {len(a_herbal_a_by_folio)} folios")
print(f"A cosmo: {sum(len(v) for v in a_cosmo_by_folio.values())} lines, {len(a_cosmo_by_folio)} folios")
print(f"B herbal: {len(b_herbal_all)} lines, {len(b_herbal_by_folio)} folios")

def get_within_folio_pairs(section_by_folio):
    """Return LF onset sequence (list of folio-pairs)."""
    pairs = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return pairs

def get_within_folio_triples(section_by_folio):
    triples = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 2):
            if lf_onsets[i] and lf_onsets[i+1] and lf_onsets[i+2]:
                triples.append((lf_onsets[i], lf_onsets[i+1], lf_onsets[i+2]))
    return triples

def cl_e(section_by_folio, a, b, label):
    """Compute E(a→b CL) in section."""
    pairs = get_within_folio_pairs(section_by_folio)
    all_lf = [ln[-1] for lines in section_by_folio.values() for ln in lines if ln]
    all_onsets = [get_onset(w) for w in all_lf]
    lf_counts = Counter(all_onsets)
    total = sum(lf_counts.values())
    base_a = lf_counts.get(a, 0) / total
    base_b = lf_counts.get(b, 0) / total
    obs = sum(1 for (x, y) in pairs if x == a and y == b)
    exp = base_a * base_b * len(pairs)
    E = obs / exp if exp > 0 else float('inf')
    flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else ("(dir)" if E >= 2.5 and obs >= 3 else ""))
    print(f"  {label} {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag} (N_pairs={len(pairs)}, base_{a}={base_a:.1%})")
    return obs, exp, E

# ============================================================
print("\n" + "="*60)
print("PART 1: H_new_CV — d→qot→ch triple chain verification")
print("="*60)

triples = get_within_folio_triples(a_herbal_a_by_folio)
pairs = get_within_folio_pairs(a_herbal_a_by_folio)
all_lf_a = [get_onset(ln[-1]) for lines in a_herbal_a_by_folio.values() for ln in lines if ln]
lf_base_a = Counter(all_lf_a)
N = sum(lf_base_a.values())
base = {o: c/N for o, c in lf_base_a.items()}

N_trips = len(triples)

# Test d→qot→ch triple
obs_dqotch = sum(1 for (a,b,c) in triples if a=='d' and b=='qot' and c=='ch')
exp_dqotch = base.get('d',0) * base.get('qot',0) * base.get('ch',0) * N_trips
E_dqotch = obs_dqotch / exp_dqotch if exp_dqotch > 0 else float('inf')
print(f"d→qot→ch: obs={obs_dqotch}, exp={exp_dqotch:.2f}, E={E_dqotch:.2f}× (N_triples={N_trips})")

# Test d→*→ch (any middle class, gap-2 d→ch)
obs_d2ch = sum(1 for (a,b,c) in triples if a=='d' and c=='ch')
exp_d2ch = base.get('d',0) * base.get('ch',0) * N_trips
E_d2ch = obs_d2ch / exp_d2ch if exp_d2ch > 0 else float('inf')
print(f"d→*→ch (any middle): obs={obs_d2ch}, exp={exp_d2ch:.2f}, E={E_d2ch:.2f}×")

# For context: what's the middle-onset distribution in d→*→ch triples?
d_star_ch = [(b) for (a,b,c) in triples if a=='d' and c=='ch']
if d_star_ch:
    print(f"  Middle classes in d→*→ch: {Counter(d_star_ch).most_common(5)}")

# What does qot precede after d?
d_to_qot = [(c) for (a,b,c) in triples if a=='d' and b=='qot']
if d_to_qot:
    print(f"  After d→qot, next LF: {Counter(d_to_qot).most_common(6)}")

# What does * precede ch?
star_to_ch = [(a) for (a,b,c) in triples if b=='qot' and c=='ch']
if star_to_ch:
    print(f"  Before qot→ch, prior LF: {Counter(star_to_ch).most_common(6)}")

# ============================================================
print("\n" + "="*60)
print("PART 2: H_new_CU — A herbal_a ok-LF pos2/pen co-occurrence")
print("="*60)

ok_lf = [ln for ln in a_herbal_a_all if get_onset(ln[-1]) == 'ok']
ok_elig = [ln for ln in ok_lf if len(ln) >= 3]
n_elig = len(ok_elig)

def get_pos(ln, pos):
    if pos == 'pos2': return ln[1] if len(ln) >= 2 else None
    if pos == 'pen': return ln[-2] if len(ln) >= 3 else None
    return None

# pos2 ok-self
p2_ok = [ln for ln in ok_elig if get_onset(get_pos(ln, 'pos2')) == 'ok']
pen_ok = [ln for ln in ok_elig if get_onset(get_pos(ln, 'pen')) == 'ok']
both = [ln for ln in ok_elig if get_onset(get_pos(ln, 'pos2')) == 'ok'
        and get_onset(get_pos(ln, 'pen')) == 'ok']

n_p2 = len(p2_ok)
n_pen = len(pen_ok)
n_both = len(both)
p_p2 = n_p2 / n_elig
p_pen = n_pen / n_elig
exp_both = p_p2 * p_pen * n_elig
E_both = n_both / exp_both if exp_both > 0 else float('inf')

# Section baselines
all_pos2 = [get_onset(get_pos(ln, 'pos2')) for ln in a_herbal_a_all if len(ln) >= 3]
all_pen = [get_onset(get_pos(ln, 'pen')) for ln in a_herbal_a_all if len(ln) >= 3]
base_p2_ok = Counter(all_pos2).get('ok', 0) / len(all_pos2) if all_pos2 else 0
base_pen_ok = Counter(all_pen).get('ok', 0) / len(all_pen) if all_pen else 0
E_p2 = p_p2 / base_p2_ok if base_p2_ok > 0 else float('inf')
E_pen = p_pen / base_pen_ok if base_pen_ok > 0 else float('inf')

print(f"ok-LF N={len(ok_lf)}, N_elig={n_elig} (len≥3)")
print(f"  pos2=ok: obs={n_p2}/{n_elig} ({p_p2:.1%}), base={base_p2_ok:.1%}, E={E_p2:.2f}× (F467 repro)")
print(f"  pen=ok: obs={n_pen}/{n_elig} ({p_pen:.1%}), base={base_pen_ok:.1%}, E={E_pen:.2f}× (F485 repro)")
print(f"  BOTH pos2=ok AND pen=ok: obs={n_both}/{n_elig}, exp={exp_both:.2f}, E_cooccur={E_both:.2f}×")
if E_both >= 1.5 and n_both >= 5:
    print(f"  → ELEVATED (CONF)")
elif E_both >= 2.0 and n_both >= 3:
    print(f"  → ELEVATED (dir)")
elif E_both <= 0.5:
    print(f"  → DEPLETED")
else:
    print(f"  → INDEPENDENT/above-baseline")

# ============================================================
print("\n" + "="*60)
print("PART 3: H_new_CT — CL scope: F490/F491 in A cosmo and B herbal")
print("="*60)

print("\nA cosmo CL:")
cl_e(a_cosmo_by_folio, 'd', 'qot', 'A cosmo')
cl_e(a_cosmo_by_folio, 'qot', 'ch', 'A cosmo')
# B herbal CL:
print("\nB herbal CL:")
cl_e(b_herbal_by_folio, 'd', 'qot', 'B herbal')
cl_e(b_herbal_by_folio, 'qot', 'ch', 'B herbal')

# Also report A herbal_a reproductions
print("\nA herbal_a (reproductions from exp_511):")
cl_e(a_herbal_a_by_folio, 'd', 'qot', 'A herbal_a')
cl_e(a_herbal_a_by_folio, 'qot', 'ch', 'A herbal_a')

# Full top CL for A cosmo
print("\n--- A cosmo top CL enrichments (obs≥3, E≥1.5×) ---")
pairs_cosmo = get_within_folio_pairs(a_cosmo_by_folio)
all_lf_cosmo = [get_onset(ln[-1]) for lines in a_cosmo_by_folio.values() for ln in lines if ln]
lf_base_cosmo = Counter(all_lf_cosmo)
N_cosmo = sum(lf_base_cosmo.values())
pair_counts_cosmo = Counter(pairs_cosmo)
for (a, b), obs in sorted(pair_counts_cosmo.items(), key=lambda x: -x[1]):
    ba = lf_base_cosmo.get(a, 0) / N_cosmo
    bb = lf_base_cosmo.get(b, 0) / N_cosmo
    if ba == 0 or bb == 0: continue
    exp = ba * bb * len(pairs_cosmo)
    if exp == 0: continue
    E = obs / exp
    if obs < 3 or E < 1.5: continue
    flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else "(dir)" if E >= 2.5 and obs >= 3 else "")
    print(f"  {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")

print("\n=== SUMMARY ===")
print(f"PART 1 — d→qot→ch triple: obs={obs_dqotch}/exp={exp_dqotch:.2f} → E={E_dqotch:.2f}×")
print(f"PART 1 — d→*→ch gap-2: obs={obs_d2ch}/exp={exp_d2ch:.2f} → E={E_d2ch:.2f}×")
print(f"PART 2 — ok-LF pos2+pen co-occurrence: obs={n_both}/exp={exp_both:.2f} → E={E_both:.2f}×")
