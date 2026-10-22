"""
exp_518: A cosmo CL survey (proper dialect filter) + inline co-occurrence tests
Questions:
  - F492 validation: does A cosmo ch→ok CL survive with proper A-dialect-only filter?
  - Full A cosmo CL survey (section-specific, within-folio, A-dialect only).
  - H_new_DA: ot-LF pos1+pos2=y co-occurrence in A herbal_a (inline, tiny).
  - H_new_DB: cth-LF pos2=qot AND pen=d co-occurrence in A herbal_a (inline, tiny).
"""
from pathlib import Path as _RepositoryPath

import re
from collections import Counter, defaultdict

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

# PROPERLY FILTERED A cosmo (A-dialect only, 85-102)
a_cosmo_by_folio = {}
for n, lines in folio_lines.items():
    if 85 <= n <= 102 and not is_b_dialect(lines):
        a_cosmo_by_folio[n] = lines

# PROPERLY FILTERED A herbal_a (A-dialect only, <=56)
a_herbal_by_folio = {}
for n, lines in folio_lines.items():
    if n <= 56 and not is_b_dialect(lines):
        a_herbal_by_folio[n] = lines

a_cosmo_lines = [ln for lines in a_cosmo_by_folio.values() for ln in lines]
a_herbal_lines = [ln for lines in a_herbal_by_folio.values() for ln in lines]

print(f"A cosmo (A-dialect only, n=85-102): {len(a_cosmo_by_folio)} folios, {len(a_cosmo_lines)} lines")
print(f"A herbal_a (A-dialect only, n<=56): {len(a_herbal_by_folio)} folios, {len(a_herbal_lines)} lines")


def get_within_folio_pairs(section_by_folio):
    pairs = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return pairs


# ==================== PART 1: A cosmo CL survey ====================

a_cosmo_pairs = get_within_folio_pairs(a_cosmo_by_folio)
N_pairs = len(a_cosmo_pairs)
lf_dist = Counter(get_onset(ln[-1]) for ln in a_cosmo_lines if ln)
total_lf = sum(lf_dist.values())

print(f"\n{'='*60}")
print(f"A cosmo CL survey (A-dialect only)")
print(f"  Folios: {len(a_cosmo_by_folio)}, Lines: {len(a_cosmo_lines)}, Pairs: {N_pairs}")
print(f"  Top LF classes: {dict(lf_dist.most_common(8))}")

pair_counts = Counter(a_cosmo_pairs)
results = []
for (a, b), obs in pair_counts.items():
    if obs < 3:
        continue
    base_a = lf_dist.get(a, 0) / total_lf
    base_b = lf_dist.get(b, 0) / total_lf
    if base_a == 0 or base_b == 0:
        continue
    exp = base_a * base_b * N_pairs
    E = obs / exp
    if E < 1.5:
        continue
    results.append((a, b, obs, exp, E))

results.sort(key=lambda x: -x[4])
print(f"\n  {'A→B':<16} {'obs':>5} {'exp':>6} {'E':>7}  status")
for a, b, obs, exp, E in results[:20]:
    flag = 'CONF' if E >= 1.5 and obs >= 10 else \
           ('dir' if E >= 2.0 and obs >= 5 else \
           '(dir)' if E >= 2.5 and obs >= 3 else '')
    print(f"  {a}→{b:<12} {obs:>5}  {exp:>6.2f}  {E:>6.2f}×  {flag}")

# F492 validation check
print(f"\n  F492 validation (ch→ok):")
for (a, b) in [('ch', 'ok'), ('ok', 'ch'), ('ch', 'ch'), ('d', 'qot'), ('qot', 'ch')]:
    obs = pair_counts.get((a, b), 0)
    base_a = lf_dist.get(a, 0) / total_lf
    base_b = lf_dist.get(b, 0) / total_lf
    if base_a == 0 or base_b == 0:
        print(f"  {a}→{b}: insufficient base")
        continue
    exp = base_a * base_b * N_pairs
    E = obs / exp if exp > 0 else float('inf')
    flag = 'CONF' if E >= 1.5 and obs >= 10 else \
           ('dir' if E >= 2.0 and obs >= 5 else \
           '(dir)' if E >= 2.5 and obs >= 3 else '')
    print(f"  {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")


# ==================== PART 2: H_new_DA — ot-LF pos1+pos2=y co-occurrence ====================

print(f"\n\n{'='*60}")
print(f"H_new_DA: ot-LF pos1=y AND pos2=y co-occurrence (A herbal_a)")

ot_lf = [ln for ln in a_herbal_lines if get_onset(ln[-1]) == 'ot']
ot_elig = [ln for ln in ot_lf if len(ln) >= 3]
N_elig = len(ot_elig)

all_pos1 = [get_onset(ln[0]) for ln in a_herbal_lines if len(ln) >= 3]
all_pos2 = [get_onset(ln[1]) for ln in a_herbal_lines if len(ln) >= 3]
pos1_base = Counter(all_pos1)
pos2_base = Counter(all_pos2)
total_pos12 = sum(pos1_base.values())

p_pos1_y = pos1_base.get('y', 0) / total_pos12
p_pos2_y = pos2_base.get('y', 0) / sum(pos2_base.values())

ot_pos1_y = sum(1 for ln in ot_elig if get_onset(ln[0]) == 'y')
ot_pos2_y = sum(1 for ln in ot_elig if get_onset(ln[1]) == 'y')
ot_both_y = sum(1 for ln in ot_elig if get_onset(ln[0]) == 'y' and get_onset(ln[1]) == 'y')

print(f"  ot-LF N_elig={N_elig} (len>=3)")
print(f"  pos1 baseline y={p_pos1_y:.3f}, pos2 baseline y={p_pos2_y:.3f}")
print(f"  ot-LF: pos1=y obs={ot_pos1_y} (E={(ot_pos1_y/N_elig)/p_pos1_y:.2f}×)")
print(f"  ot-LF: pos2=y obs={ot_pos2_y} (E={(ot_pos2_y/N_elig)/p_pos2_y:.2f}×)")
print(f"  ot-LF: BOTH pos1=y AND pos2=y obs={ot_both_y}")
exp_both = (ot_pos1_y/N_elig) * (ot_pos2_y/N_elig) * N_elig  # expected if independent
E_cooccur = ot_both_y / exp_both if exp_both > 0 else float('inf')
print(f"  Expected if independent: {exp_both:.2f}, E_cooccur={E_cooccur:.2f}×")


# ==================== PART 3: H_new_DB — cth-LF pos2=qot AND pen=d co-occurrence ====================

print(f"\n\n{'='*60}")
print(f"H_new_DB: cth-LF pos2=qot AND pen=d co-occurrence (A herbal_a)")

cth_lf = [ln for ln in a_herbal_lines if get_onset(ln[-1]) == 'cth']
cth_elig = [ln for ln in cth_lf if len(ln) >= 3]
N_cth = len(cth_elig)

all_pen = [get_onset(ln[-2]) for ln in a_herbal_lines if len(ln) >= 3]
pen_base = Counter(all_pen)
total_pen = sum(pen_base.values())
p_pen_d = pen_base.get('d', 0) / total_pen
p_pos2_qot = pos2_base.get('qot', 0) / sum(pos2_base.values())

cth_pos2_qot = sum(1 for ln in cth_elig if get_onset(ln[1]) == 'qot')
cth_pen_d = sum(1 for ln in cth_elig if get_onset(ln[-2]) == 'd')
cth_both = sum(1 for ln in cth_elig if get_onset(ln[1]) == 'qot' and get_onset(ln[-2]) == 'd')

print(f"  cth-LF N_elig={N_cth} (len>=3)")
print(f"  pos2 baseline qot={p_pos2_qot:.3f}, pen baseline d={p_pen_d:.3f}")
print(f"  cth-LF: pos2=qot obs={cth_pos2_qot} (E={(cth_pos2_qot/N_cth)/p_pos2_qot:.2f}×)")
print(f"  cth-LF: pen=d obs={cth_pen_d} (E={(cth_pen_d/N_cth)/p_pen_d:.2f}×)")
print(f"  cth-LF: BOTH pos2=qot AND pen=d obs={cth_both}")
exp_cth_both = (cth_pos2_qot/N_cth) * (cth_pen_d/N_cth) * N_cth
E_cth_cooccur = cth_both / exp_cth_both if exp_cth_both > 0 else float('inf')
print(f"  Expected if independent: {exp_cth_both:.2f}, E_cooccur={E_cth_cooccur:.2f}×")
