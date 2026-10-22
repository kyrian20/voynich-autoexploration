"""
exp_517: B pharma within-folio CL survey + A herbal_a d→qot→ch triple test
Questions:
  H_new_DG: Does F444's B pharma qok→s CL survive section-specific baseline?
             What other B pharma CL rules exist?
  H_new_CV: Does the A herbal_a d→qot→ch triple appear as an above-baseline sequence?
  H_new_CU: A herbal_a ok-LF: do ok@pos2(dir) and ok@pen(CONF) co-occur in same lines?

Method:
  CL: within-folio consecutive pairs, section-specific baselines.
  Triple: count (d, qot, ch) sequences in within-folio consecutive triples.
  Co-occurrence: count ok@pos2 AND ok@pen in same ok-LF lines.
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

# Build sections
b_pharma_by_folio = {}
a_herbal_by_folio = {}

for n, lines in folio_lines.items():
    if is_b_dialect(lines):
        if 85 <= n <= 116:
            b_pharma_by_folio[n] = lines
    else:
        if n <= 56:
            a_herbal_by_folio[n] = lines

b_pharma_lines = [ln for lines in b_pharma_by_folio.values() for ln in lines]
a_herbal_lines = [ln for lines in a_herbal_by_folio.values() for ln in lines]
print(f"B pharma: {len(b_pharma_by_folio)} folios, {len(b_pharma_lines)} lines")
print(f"A herbal_a: {len(a_herbal_by_folio)} folios, {len(a_herbal_lines)} lines")


# ==================== PART 1: B PHARMA CL SURVEY ====================

def get_within_folio_pairs(section_by_folio):
    pairs = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return pairs

b_pharma_pairs = get_within_folio_pairs(b_pharma_by_folio)
N_pairs = len(b_pharma_pairs)
lf_dist = Counter(get_onset(ln[-1]) for ln in b_pharma_lines if ln)
total_lf = sum(lf_dist.values())

print(f"\n{'='*60}")
print(f"B pharma CL survey — within-folio pairs")
print(f"  Lines: {len(b_pharma_lines)}, Pairs: {N_pairs}")
print(f"  Top LF classes: {dict(lf_dist.most_common(8))}")

pair_counts = Counter(b_pharma_pairs)
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

# F444 scope check
print("\n  F444 scope checks (B pharma, section-specific baseline):")
for (a, b) in [('qok', 's'), ('s', 'qok'), ('l', 'ch'), ('ch', 'l'), ('ok', 'l'), ('d', 'ch'), ('ok', 'ok')]:
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


# ==================== PART 2: A herbal_a d→qot→ch TRIPLE ====================

print(f"\n\n{'='*60}")
print(f"A herbal_a d→qot→ch triple test (H_new_CV)")

a_herbal_pairs_list = get_within_folio_pairs(a_herbal_by_folio)
a_lf_dist = Counter(get_onset(ln[-1]) for ln in a_herbal_lines if ln)
a_total_lf = sum(a_lf_dist.values())
N_a_pairs = len(a_herbal_pairs_list)

# Get triples: (LF_n, LF_{n+1}, LF_{n+2}) within same folio
def get_within_folio_triples(section_by_folio):
    triples = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 2):
            if lf_onsets[i] and lf_onsets[i+1] and lf_onsets[i+2]:
                triples.append((lf_onsets[i], lf_onsets[i+1], lf_onsets[i+2]))
    return triples

a_triples = get_within_folio_triples(a_herbal_by_folio)
N_triples = len(a_triples)
triple_counts = Counter(a_triples)

print(f"  A herbal_a triples: {N_triples}")

# Test specific triples
target_triple = ('d', 'qot', 'ch')
obs_triple = triple_counts.get(target_triple, 0)
p_d = a_lf_dist.get('d', 0) / a_total_lf
p_qot = a_lf_dist.get('qot', 0) / a_total_lf
p_ch = a_lf_dist.get('ch', 0) / a_total_lf
exp_triple = p_d * p_qot * p_ch * N_triples
E_triple = obs_triple / exp_triple if exp_triple > 0 else float('inf')
print(f"  d→qot→ch: obs={obs_triple}, exp={exp_triple:.2f}, E={E_triple:.2f}×")

# Also test d→?→ch (any mediator)
d_to_ch_triples = sum(v for (a,b,c), v in triple_counts.items() if a == 'd' and c == 'ch')
exp_d_to_ch = p_d * p_ch * N_triples
E_d_to_ch = d_to_ch_triples / exp_d_to_ch if exp_d_to_ch > 0 else float('inf')
print(f"  d→*→ch (any mediator): obs={d_to_ch_triples}, exp={exp_d_to_ch:.2f}, E={E_d_to_ch:.2f}×")

# Show top triples starting with d
print(f"\n  Top d-starting triples (obs≥2):")
d_triples = [(t, c) for t, c in triple_counts.items() if t[0] == 'd' and c >= 2]
d_triples.sort(key=lambda x: -x[1])
for (a, b, c), cnt in d_triples[:10]:
    exp = a_lf_dist.get(a,0)/a_total_lf * a_lf_dist.get(b,0)/a_total_lf * a_lf_dist.get(c,0)/a_total_lf * N_triples
    E = cnt / exp if exp > 0 else float('inf')
    print(f"  d→{b}→{c}: obs={cnt}, exp={exp:.2f}, E={E:.2f}×")

# Show top triples overall (obs>=3)
print(f"\n  Top triples overall (obs≥3, E≥2.0):")
top_triples = [(t, c) for t, c in triple_counts.items() if c >= 3]
top_triples_e = []
for (a, b, c), cnt in top_triples:
    exp = a_lf_dist.get(a,0)/a_total_lf * a_lf_dist.get(b,0)/a_total_lf * a_lf_dist.get(c,0)/a_total_lf * N_triples
    if exp > 0:
        E = cnt / exp
        if E >= 2.0:
            top_triples_e.append(((a,b,c), cnt, exp, E))
top_triples_e.sort(key=lambda x: -x[3])
for (a,b,c), cnt, exp, E in top_triples_e[:15]:
    flag = 'CONF' if E >= 1.5 and cnt >= 10 else ('dir' if E >= 2.0 and cnt >= 5 else '(dir)')
    print(f"  {a}→{b}→{c}: obs={cnt}, exp={exp:.2f}, E={E:.2f}× {flag}")


# ==================== PART 3: A herbal_a ok-LF pos2+pen co-occurrence ====================

print(f"\n\n{'='*60}")
print(f"A herbal_a ok-LF pos2+pen co-occurrence (H_new_CU)")

ok_lf_lines = [ln for ln in a_herbal_lines if get_onset(ln[-1]) == 'ok']
ok_elig = [ln for ln in ok_lf_lines if len(ln) >= 3]  # need pos2 AND pen
print(f"  ok-LF lines: {len(ok_lf_lines)}, len>=3 eligible: {len(ok_elig)}")

# pos2 baseline
all_pos2 = [get_onset(ln[1]) for ln in a_herbal_lines if len(ln) >= 3]
pos2_base = Counter(all_pos2)
total_pos2 = sum(pos2_base.values())

# pen baseline
all_pen = [get_onset(ln[-2]) for ln in a_herbal_lines if len(ln) >= 3]
pen_base = Counter(all_pen)
total_pen = sum(pen_base.values())

# Compute individual probabilities for ok-LF eligible lines
ok_pos2_ok = sum(1 for ln in ok_elig if get_onset(ln[1]) == 'ok')
ok_pen_ok = sum(1 for ln in ok_elig if get_onset(ln[-2]) == 'ok')
ok_both_ok = sum(1 for ln in ok_elig if get_onset(ln[1]) == 'ok' and get_onset(ln[-2]) == 'ok')

N_elig = len(ok_elig)
p_pos2_ok = pos2_base.get('ok', 0) / total_pos2
p_pen_ok = pen_base.get('ok', 0) / total_pen

print(f"  pos2 baseline: ok={p_pos2_ok:.3f}")
print(f"  pen baseline: ok={p_pen_ok:.3f}")
print(f"  ok-LF lines with ok@pos2: {ok_pos2_ok}/{N_elig} = {ok_pos2_ok/N_elig:.3f}")
print(f"  ok-LF lines with ok@pen: {ok_pen_ok}/{N_elig} = {ok_pen_ok/N_elig:.3f}")
print(f"  ok-LF lines with BOTH ok@pos2 AND ok@pen: {ok_both_ok}/{N_elig}")

exp_both = (ok_pos2_ok/N_elig) * (ok_pen_ok/N_elig) * N_elig  # if independent given ok-LF
E_cooccur = ok_both_ok / exp_both if exp_both > 0 else float('inf')
print(f"  Expected if independent: {exp_both:.2f}")
print(f"  E_cooccur = {E_cooccur:.2f}×")

# Also check ok@pos2 marginal E (corrected from F467)
E_pos2 = (ok_pos2_ok / N_elig) / p_pos2_ok
E_pen = (ok_pen_ok / N_elig) / p_pen_ok
print(f"\n  ok@pos2 E in ok-LF lines: {E_pos2:.2f}× (N={ok_pos2_ok})")
print(f"  ok@pen E in ok-LF lines: {E_pen:.2f}× (N={ok_pen_ok})")
