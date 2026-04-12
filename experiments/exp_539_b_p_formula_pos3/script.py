"""
exp_539: H623_archived — B p-formula pos3 grammar

For B continuation lines with p at LF:
1. pos3 onset distribution (all p-LF lines with ≥4 words)
2. pos3 conditioned on pos2 class (pos2=sh, pos2=qot, etc.)
3. Full path p→sh→qot→pos3 (small N=8 expected)
"""
import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph','d','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset): return onset
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
        if not lc.lstrip('@').startswith('P'): continue
        words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
        if not words: continue
        n = folio_num(folio)
        if n is None: continue
        folio_lines[n].append(words)
    return folio_lines

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words: return False
    return sum(1 for w in words if w.endswith('edy') or w.endswith('eedy')) / len(words) >= 0.05

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

folio_lines = parse_corpus(CORPUS)
b_all_folios = {n: ls for n, ls in folio_lines.items() if is_b_dialect(ls)}
b_all_lines = [ln for ls in b_all_folios.values() for ln in ls]
print(f"B all: {len(b_all_lines)} lines")

# Continuation B p-LF lines (p at LF = word[-1])
b_p_lf = [ln for ln in b_all_lines if get_onset(ln[-1]) == 'p']
b_p_lf_4plus = [ln for ln in b_p_lf if len(ln) >= 4]
print(f"\nB p-LF lines: {len(b_p_lf)} total, {len(b_p_lf_4plus)} with ≥4 words (pos3 accessible)")

# Part 1: pos3 distribution for all B p-LF lines (≥4 words)
print("\n" + "="*60)
print("PART 1: pos3 DISTRIBUTION (all B p-LF lines, ≥4 words)")
print("="*60)

# Baseline: all B p-LF lines pos3 rate vs full B all pos3 rate
all_b_4plus = [ln for ln in b_all_lines if len(ln) >= 4]
base_pos3 = Counter(get_onset(ln[3]) for ln in all_b_4plus)
N_base = len(all_b_4plus)
p_pos3 = Counter(get_onset(ln[3]) for ln in b_p_lf_4plus)
N_plf = len(b_p_lf_4plus)

print(f"Baseline: all B lines ≥4 words N={N_base}")
print(f"B p-LF ≥4 words N={N_plf}")
print(f"{'Onset':>8} {'obs':>5} E flag")
for onset, obs in p_pos3.most_common(12):
    base_rate = base_pos3[onset] / N_base if N_base > 0 else 0
    E = (obs/N_plf) / base_rate if base_rate > 0 else 0
    print(f"{onset:>8} {obs:>5}/{N_plf} E={E:.2f}× {flag(obs, E)}")

# Part 2: pos3 conditioned on pos2 class
print("\n" + "="*60)
print("PART 2: pos3 CONDITIONED ON pos2 CLASS (B p-LF ≥4 words)")
print("="*60)
p_3plus = [ln for ln in b_p_lf if len(ln) >= 3]
print(f"B p-LF ≥3 words: {len(p_3plus)} (pos2 accessible)")
pos2_dist = Counter(get_onset(ln[1]) for ln in p_3plus)
print(f"pos2 distribution: {dict(pos2_dist.most_common(6))}")

for p2_cls in ['sh', 'qot', 'ch', 'ok', 'qok']:
    cond_lines = [ln for ln in b_p_lf_4plus if len(ln) >= 4 and get_onset(ln[1]) == p2_cls]
    N_cond = len(cond_lines)
    if N_cond == 0:
        print(f"\n  pos2={p2_cls}: N=0 (skip)")
        continue
    p3_dist = Counter(get_onset(ln[3]) for ln in cond_lines)
    print(f"\n  pos2={p2_cls}: N={N_cond}")
    for onset, obs in p3_dist.most_common(5):
        base_rate = base_pos3[onset] / N_base if N_base > 0 else 0
        E = (obs/N_cond) / base_rate if base_rate > 0 else 0
        print(f"    pos3={onset}: {obs}/{N_cond} E={E:.2f}× {flag(obs, E)}")

# Part 3: Full path p→sh→qot→pos3
print("\n" + "="*60)
print("PART 3: FULL PATH p→sh→qot→pos3")
print("="*60)
path_lines = [ln for ln in b_p_lf_4plus if len(ln) >= 4 and get_onset(ln[1]) == 'sh' and get_onset(ln[2]) == 'qot']
N_path = len(path_lines)
print(f"p[LF]→sh[pos1]→qot[pos2] lines with ≥4 words: N={N_path}")
if N_path > 0:
    pos3_dist = Counter(get_onset(ln[3]) for ln in path_lines)
    for onset, obs in pos3_dist.most_common():
        base_rate = base_pos3[onset] / N_base if N_base > 0 else 0
        E = (obs/N_path) / base_rate if base_rate > 0 else 0
        print(f"  pos3={onset}: {obs}/{N_path} E={E:.2f}× {flag(obs, E)}")
    print("Lines:")
    for ln in path_lines:
        print(f"  {' '.join(ln)}")
