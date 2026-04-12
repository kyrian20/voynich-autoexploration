"""
exp_519: A cosmo cth CL folio distribution + ot-LF pos2=y targeted + cth CL scope in A herbal_a
Questions:
  H_new_DH: Are cth→cth pairs in A cosmo distributed across folios or clustering in 1-2?
  H_new_DJ: Does cth→cth CL appear in A herbal_a?
  H_new_DI: Full → ol destination survey in A cosmo.
  H_new_DK: A herbal_a ot-LF pos2=y full targeted test.
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

# A cosmo (A-dialect only)
a_cosmo_by_folio = {n: lines for n, lines in folio_lines.items()
                    if 85 <= n <= 102 and not is_b_dialect(lines)}

# A herbal_a (A-dialect only)
a_herbal_by_folio = {n: lines for n, lines in folio_lines.items()
                     if n <= 56 and not is_b_dialect(lines)}

a_cosmo_lines = [ln for lines in a_cosmo_by_folio.values() for ln in lines]
a_herbal_lines = [ln for lines in a_herbal_by_folio.values() for ln in lines]


# ==================== H_new_DH: cth→cth folio distribution ====================

print(f"{'='*60}")
print(f"H_new_DH: cth→cth CL folio distribution in A cosmo")

cth_cth_details = []
for n in sorted(a_cosmo_by_folio):
    lines = a_cosmo_by_folio[n]
    lf_onsets = [(get_onset(ln[-1]), ln[-1], ln) for ln in lines if ln]
    for i in range(len(lf_onsets) - 1):
        a_onset, a_word, a_ln = lf_onsets[i]
        b_onset, b_word, b_ln = lf_onsets[i+1]
        if a_onset == 'cth' and b_onset == 'cth':
            cth_cth_details.append({
                'folio': n,
                'lf1': a_word,
                'lf2': b_word,
                'len1': len(a_ln),
                'len2': len(b_ln)
            })

print(f"  cth->cth pairs: N={len(cth_cth_details)}")
folio_dist = Counter(d['folio'] for d in cth_cth_details)
word_pairs = Counter((d['lf1'], d['lf2']) for d in cth_cth_details)
print(f"  Folio distribution: {dict(sorted(folio_dist.items()))}")
print(f"  Word pairs: {dict(word_pairs.most_common(8))}")
print(f"  Folios contributing: {len(folio_dist)} of {len(a_cosmo_by_folio)} total A cosmo folios")
for d in cth_cth_details:
    print(f"    f{d['folio']}: {d['lf1']}(len={d['len1']}) -> {d['lf2']}(len={d['len2']})")

# Also check cth->ol details
print(f"\n  cth->ol pairs detail:")
cth_ol_details = []
for n in sorted(a_cosmo_by_folio):
    lines = a_cosmo_by_folio[n]
    lf_onsets = [(get_onset(ln[-1]), ln[-1]) for ln in lines if ln]
    for i in range(len(lf_onsets) - 1):
        if lf_onsets[i][0] == 'cth' and lf_onsets[i+1][0] == 'ol':
            cth_ol_details.append({'folio': n, 'lf1': lf_onsets[i][1], 'lf2': lf_onsets[i+1][1]})
print(f"  cth->ol pairs: N={len(cth_ol_details)}")
folio_ol_dist = Counter(d['folio'] for d in cth_ol_details)
print(f"  Folio distribution: {dict(sorted(folio_ol_dist.items()))}")
for d in cth_ol_details:
    print(f"    f{d['folio']}: {d['lf1']} -> {d['lf2']}")


# ==================== H_new_DJ: cth CL scope in A herbal_a ====================

print(f"\n{'='*60}")
print(f"H_new_DJ: cth CL scope in A herbal_a (does cth->cth or cth->ol appear?)")

herbal_pairs = []
for n in sorted(a_herbal_by_folio):
    lines = a_herbal_by_folio[n]
    lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
    for i in range(len(lf_onsets) - 1):
        if lf_onsets[i] and lf_onsets[i+1]:
            herbal_pairs.append((lf_onsets[i], lf_onsets[i+1]))

N_herb = len(herbal_pairs)
herb_pair_counts = Counter(herbal_pairs)
herb_lf_dist = Counter(get_onset(ln[-1]) for ln in a_herbal_lines if ln)
herb_total = sum(herb_lf_dist.values())

for (a, b) in [('cth','cth'), ('cth','ol'), ('ch','ol')]:
    obs = herb_pair_counts.get((a, b), 0)
    base_a = herb_lf_dist.get(a, 0) / herb_total
    base_b = herb_lf_dist.get(b, 0) / herb_total
    if base_a == 0 or base_b == 0:
        print(f"  {a}->{b}: insufficient base (base_a={base_a:.3f}, base_b={base_b:.3f})")
        continue
    exp = base_a * base_b * N_herb
    E = obs / exp if exp > 0 else float('inf')
    flag = 'CONF' if E >= 1.5 and obs >= 10 else \
           ('dir' if E >= 2.0 and obs >= 5 else \
           '(dir)' if E >= 2.5 and obs >= 3 else '')
    print(f"  A herbal_a {a}->{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}x {flag}")

# Also show top cth-sender and cth-receiver pairs in A herbal_a
print(f"\n  A herbal_a cth-involving CL pairs (obs>=2):")
for (a, b), obs in sorted(herb_pair_counts.items(), key=lambda x: -x[1]):
    if (a == 'cth' or b == 'cth') and obs >= 2:
        base_a = herb_lf_dist.get(a, 0) / herb_total
        base_b = herb_lf_dist.get(b, 0) / herb_total
        exp = base_a * base_b * N_herb if base_a and base_b else 0
        E = obs / exp if exp > 0 else float('inf')
        print(f"    {a}->{b}: obs={obs}, E={E:.2f}x")


# ==================== H_new_DI: A cosmo -> ol full survey ====================

print(f"\n{'='*60}")
print(f"H_new_DI: A cosmo CL -> ol full survey (all senders to ol-LF)")

cosmo_pairs = []
for n in sorted(a_cosmo_by_folio):
    lines = a_cosmo_by_folio[n]
    lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
    for i in range(len(lf_onsets) - 1):
        if lf_onsets[i] and lf_onsets[i+1]:
            cosmo_pairs.append((lf_onsets[i], lf_onsets[i+1]))

N_cosmo = len(cosmo_pairs)
cosmo_pair_counts = Counter(cosmo_pairs)
cosmo_lf_dist = Counter(get_onset(ln[-1]) for ln in a_cosmo_lines if ln)
cosmo_total = sum(cosmo_lf_dist.values())

print(f"  ol-LF rate in A cosmo: {cosmo_lf_dist.get('ol',0)}/{cosmo_total} = {cosmo_lf_dist.get('ol',0)/cosmo_total:.3f}")
print(f"  All -> ol pairs (obs>=2):")
for (a, b), obs in sorted(cosmo_pair_counts.items(), key=lambda x: -x[1]):
    if b == 'ol' and obs >= 2:
        base_a = cosmo_lf_dist.get(a, 0) / cosmo_total
        base_b = cosmo_lf_dist.get('ol', 0) / cosmo_total
        exp = base_a * base_b * N_cosmo if base_a and base_b else 0
        E = obs / exp if exp > 0 else float('inf')
        print(f"    {a}->ol: obs={obs}, exp={exp:.2f}, E={E:.2f}x")

print(f"  All ol -> X pairs (obs>=1):")
for (a, b), obs in sorted(cosmo_pair_counts.items(), key=lambda x: -x[1]):
    if a == 'ol' and obs >= 1:
        base_a = cosmo_lf_dist.get('ol', 0) / cosmo_total
        base_b = cosmo_lf_dist.get(b, 0) / cosmo_total
        exp = base_a * base_b * N_cosmo if base_a and base_b else 0
        E = obs / exp if exp > 0 else float('inf')
        print(f"    ol->{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}x")


# ==================== H_new_DK: A herbal_a ot-LF pos2=y targeted ====================

print(f"\n{'='*60}")
print(f"H_new_DK: A herbal_a ot-LF pos2=y full targeted test")

ot_lines = [ln for ln in a_herbal_lines if get_onset(ln[-1]) == 'ot' and len(ln) >= 3]
N_ot = len(ot_lines)

all_pos2 = [get_onset(ln[1]) for ln in a_herbal_lines if len(ln) >= 3]
pos2_base = Counter(all_pos2)
total_pos2 = sum(pos2_base.values())

print(f"  ot-LF N_elig={N_ot} (len>=3)")
ot_pos2_dist = Counter(get_onset(ln[1]) for ln in ot_lines)
print(f"  ot-LF pos2 full distribution: {dict(ot_pos2_dist.most_common(10))}")

print(f"\n  ot-LF pos2 enrichment table:")
for cls, cnt in ot_pos2_dist.most_common():
    base = pos2_base.get(cls, 0) / total_pos2
    if base == 0:
        continue
    exp = base * N_ot
    E = cnt / exp
    if cnt >= 2 or E >= 1.5:
        flag = 'CONF' if E >= 1.5 and cnt >= 10 else \
               ('dir' if E >= 2.0 and cnt >= 5 else \
               '(dir)' if E >= 2.5 and cnt >= 3 else '')
        print(f"    ot-LF pos2={cls}: obs={cnt}, exp={exp:.2f}, E={E:.2f}x {flag}")

# Focused y check
y_obs = ot_pos2_dist.get('y', 0)
y_base = pos2_base.get('y', 0) / total_pos2
y_exp = y_base * N_ot
y_E = y_obs / y_exp if y_exp > 0 else float('inf')
print(f"\n  ot-LF pos2=y: obs={y_obs}, exp={y_exp:.2f}, E={y_E:.2f}x")
if y_obs >= 10:
    print(f"  STATUS: CONF")
elif y_obs >= 5:
    print(f"  STATUS: dir")
elif y_obs >= 3:
    print(f"  STATUS: (dir)")
else:
    print(f"  STATUS: below thresholds (N={y_obs})")
