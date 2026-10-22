"""
exp_513: A herbal_a pos2 cross-class routing survey (H_new_CX)
Question: With pos2 self-chaining retracted (F468), what cross-class pos2 rules exist in A herbal_a?
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

pat = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
with open(CORPUS, encoding='utf-8') as f:
    raw = f.read()

a_herbal = []
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
    if n and n <= 56:
        a_herbal.append(words)

# pos2 baseline (len>=3, excluding LF position)
all_pos2 = [get_onset(ln[1]) for ln in a_herbal if len(ln) >= 3]
pos2_base = Counter(all_pos2)
total_pos2 = sum(pos2_base.values())

# LF distribution
all_lf = [get_onset(ln[-1]) for ln in a_herbal]
lf_counts = Counter(all_lf)

print(f"A herbal_a: {len(a_herbal)} lines")
print(f"pos2 baseline: {total_pos2} pos2 observations (len>=3)")

print("\n--- pos2 baseline rates ---")
for onset, cnt in sorted(pos2_base.items(), key=lambda x: -x[1])[:12]:
    print(f"  {onset}: {cnt}/{total_pos2} ({cnt/total_pos2:.1%})")

print("\n--- FULL pos2 survey: all LF classes, all pos2 onsets (len>=3) ---")
print("Showing E>=1.5x and obs>=3 (cross-class only)")
print(f"{'LF-class':<8} {'pos2-onset':<10} {'obs':>5} {'N_elig':>6} {'E':>7}  flag")

all_results = []
for lf_class, lf_n in sorted(lf_counts.items(), key=lambda x: -x[1])[:15]:
    lf_lines = [ln for ln in a_herbal if get_onset(ln[-1]) == lf_class]
    elig = [ln for ln in lf_lines if len(ln) >= 3]
    N_elig = len(elig)
    if N_elig < 5:
        continue
    pos2_dist = Counter(get_onset(ln[1]) for ln in elig)
    for onset, obs in sorted(pos2_dist.items(), key=lambda x: -x[1]):
        base = pos2_base.get(onset, 0) / total_pos2 if total_pos2 > 0 else 0
        if base == 0:
            continue
        E = (obs / N_elig) / base
        all_results.append((lf_class, onset, obs, N_elig, E))
        if E < 1.5 or obs < 3:
            continue
        flag = 'CONF' if E >= 1.5 and obs >= 10 else \
               ('dir' if E >= 2.0 and obs >= 5 else \
               '(dir)' if E >= 2.5 and obs >= 3 else '')
        cross = '' if onset == lf_class else '←cross'
        print(f"{lf_class:<8} → {onset:<8} obs={obs:>4}/{N_elig:>4} E={E:>6.2f}×  {flag} {cross}")

print("\n--- qot-LF detailed pos2 distribution ---")
qot_lines = [ln for ln in a_herbal if get_onset(ln[-1]) == 'qot']
qot_elig = [ln for ln in qot_lines if len(ln) >= 3]
print(f"qot-LF: N={len(qot_lines)}, N_elig={len(qot_elig)}")
qot_pos2 = Counter(get_onset(ln[1]) for ln in qot_elig)
for onset, obs in sorted(qot_pos2.items(), key=lambda x: -x[1])[:8]:
    base = pos2_base.get(onset, 0) / total_pos2 if total_pos2 > 0 else 0
    E = (obs / len(qot_elig)) / base if base > 0 else 0
    flag = 'CONF' if E >= 1.5 and obs >= 10 else ('dir' if E >= 2.0 and obs >= 5 else '')
    print(f"  {onset}: obs={obs}/{len(qot_elig)} ({obs/len(qot_elig):.1%}) vs base={base:.1%}, E={E:.2f}× {flag}")
