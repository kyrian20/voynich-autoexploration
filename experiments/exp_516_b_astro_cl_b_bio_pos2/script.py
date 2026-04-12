"""
exp_516: B astro within-folio CL survey + B bio pos2 grammar survey
Questions:
  H_new_DE: Does F444's B astro ch→qot CL survive section-specific baseline?
             Are there other confirmed B astro CL rules?
  H_new_CD: Does B bio have confirmed pos2 routing rules?

Method:
  CL: within-folio consecutive LF-onset pairs, section-specific baselines.
  Pos2: len>=3 methodology, cross-class and self-chain, section-specific baseline.
"""

import re
from collections import Counter, defaultdict

CORPUS = "/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt"
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
b_astro_by_folio = {}
b_bio_lines = []

for n, lines in folio_lines.items():
    if not is_b_dialect(lines):
        continue
    if 73 <= n <= 84:
        b_astro_by_folio[n] = lines
    elif n >= 117:
        b_bio_lines.extend(lines)

b_astro_lines = [ln for lines in b_astro_by_folio.values() for ln in lines]
print(f"B astro: {len(b_astro_by_folio)} folios, {len(b_astro_lines)} lines")
print(f"B bio: {len(b_bio_lines)} lines")


# ==================== PART 1: B ASTRO CL SURVEY ====================

def get_within_folio_pairs(section_by_folio):
    pairs = []
    for n in sorted(section_by_folio):
        lines = section_by_folio[n]
        lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
        for i in range(len(lf_onsets) - 1):
            if lf_onsets[i] and lf_onsets[i+1]:
                pairs.append((lf_onsets[i], lf_onsets[i+1]))
    return pairs

b_astro_pairs = get_within_folio_pairs(b_astro_by_folio)
N_pairs = len(b_astro_pairs)
lf_dist = Counter(get_onset(ln[-1]) for ln in b_astro_lines if ln)
total_lf = sum(lf_dist.values())

print(f"\n{'='*60}")
print(f"B astro CL survey — within-folio pairs")
print(f"  Lines: {len(b_astro_lines)}, Pairs: {N_pairs}")
print(f"  Top LF classes: {dict(lf_dist.most_common(8))}")

pair_counts = Counter(b_astro_pairs)
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

# Specific scope checks
print("\n  F444 scope checks (B astro, section-specific baseline):")
for (a, b) in [('ch', 'qot'), ('qot', 'ch'), ('ch', 'ok'), ('d', 'qok'), ('qok', 'd'), ('sh', 'd')]:
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


# ==================== PART 2: B BIO POS2 SURVEY ====================

print(f"\n\n{'='*60}")
print(f"B bio pos2 survey (len>=3)")
print(f"  Lines: {len(b_bio_lines)}")

# pos2 baseline (len>=3)
all_pos2 = [get_onset(ln[1]) for ln in b_bio_lines if len(ln) >= 3]
pos2_base = Counter(all_pos2)
total_pos2 = sum(pos2_base.values())
print(f"  pos2 baseline lines: {total_pos2}")
print(f"  Top pos2 classes: {dict(sorted(pos2_base.items(), key=lambda x: -x[1])[:8])}")

lf_dist_bio = Counter(get_onset(ln[-1]) for ln in b_bio_lines if ln)
print(f"  Top LF classes: {dict(lf_dist_bio.most_common(8))}")

print(f"\n  {'LF-class':<8} {'pos2-onset':<10} {'obs':>5} {'N_elig':>6} {'E':>7}  flag")
pos2_results = []
for lf_class, lf_n in sorted(lf_dist_bio.items(), key=lambda x: -x[1]):
    lf_lines = [ln for ln in b_bio_lines if get_onset(ln[-1]) == lf_class]
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
        if E < 1.5 or obs < 3:
            continue
        flag = 'CONF' if E >= 1.5 and obs >= 10 else \
               ('dir' if E >= 2.0 and obs >= 5 else \
               '(dir)' if E >= 2.5 and obs >= 3 else '')
        is_self = (lf_class == onset)
        cross_marker = '' if is_self else '*'
        print(f"  {lf_class:<8} → {onset:<10} obs={obs:>4}/{N_elig:>4} E={E:>6.2f}×  {flag} {cross_marker}")
        pos2_results.append((lf_class, onset, obs, N_elig, E, is_self))

if not pos2_results:
    print("  No pos2 enrichments at E>=1.5×/obs>=3")

print(f"\n  (* = cross-class routing)")
