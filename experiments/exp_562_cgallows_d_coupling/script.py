"""
exp_562: Compound gallows → d universal coupling analysis (H_new_FY)
All 4 compound gallows (cth, ckh, cph, sch) route to d within A lines.
Parts:
1. Combined compound gallows → d bigram strength (pooled)
2. Directionality: within lines containing both c-gallows and d, is c-gallows before d?
3. [y][ckh][d] triplet — does the y→ckh→d chain exist?
4. Position of c-gallows→d pairs within lines
5. Reverse: d→c-gallows routing in A
"""

import re
from collections import Counter, defaultdict

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
ONSET_PRIORITY = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
                  'd','s','y','k','t','l','r','p','f','o','e','a','n','m']
COMPOUND_GALLOWS = {'cth', 'ckh', 'cph', 'sch'}

def get_onset(w):
    for o in ONSET_PRIORITY:
        if w.startswith(o):
            return o
    return w[0] if w else None

def parse_corpus(filepath):
    lines_A = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m: continue
            folio_raw, n_str, lc, text = m.group(1), m.group(2), m.group(3), m.group(4)
            lc2 = lc.lstrip('+*=/~&').lstrip('@')
            if not lc2.startswith('P'): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            try: n = int(n_str)
            except: continue
            edy_count = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy_count / len(words) >= 0.05
            if not is_b and n <= 56:
                lines_A.append((folio_raw, words))
    return lines_A

lines_A = parse_corpus(CORPUS)
print(f"A herbal_a: {len(lines_A)} lines")

all_A_words = [w for fo, ws in lines_A for w in ws]
total_A = len(all_A_words)
print(f"A words: {total_A}")

# MID baseline
mid_counts = Counter()
total_mid = 0
for fo, ws in lines_A:
    L = len(ws)
    for i in range(1, L-1):
        mid_counts[get_onset(ws[i])] += 1
        total_mid += 1

print(f"\nMID baseline: {total_mid} words")
print(f"MID d rate: {mid_counts['d']/total_mid:.4f}")
mid_cgallows_total = sum(mid_counts[cls] for cls in COMPOUND_GALLOWS)
print(f"MID compound gallows total: {mid_cgallows_total} ({100*mid_cgallows_total/total_mid:.2f}%)")

# --- Part 1: Combined compound gallows → d bigram strength ---
print("\n=== PART 1: Combined compound gallows → d bigram analysis ===")

# Per-class and combined
cgallows_d_bigrams = defaultdict(Counter)  # cgallows_class -> target_class -> count
cgallows_total_bigrams = defaultdict(int)

for fo, ws in lines_A:
    for i in range(len(ws) - 1):
        onset_i = get_onset(ws[i])
        if onset_i in COMPOUND_GALLOWS:
            cgallows_d_bigrams[onset_i][get_onset(ws[i+1])] += 1
            cgallows_total_bigrams[onset_i] += 1

# Combined
combined_d_bigrams = 0
combined_total = sum(cgallows_total_bigrams.values())
for cls in COMPOUND_GALLOWS:
    combined_d_bigrams += cgallows_d_bigrams[cls].get('d', 0)

print(f"\nPer-class c-gallows → d bigrams:")
for cls in sorted(COMPOUND_GALLOWS):
    n_sender = cgallows_total_bigrams[cls]
    obs_d = cgallows_d_bigrams[cls].get('d', 0)
    exp_d = (mid_counts['d'] / total_mid) * n_sender if total_mid > 0 else 0
    e = obs_d / exp_d if exp_d > 0 else float('inf')
    flag = 'CONF' if e >= 1.5 and obs_d >= 10 else ('dir' if e >= 2.0 and obs_d >= 5 else ('(dir)' if e >= 2.5 and obs_d >= 3 else ''))
    print(f"  {cls}→d: obs={obs_d}/{n_sender}, exp={exp_d:.1f}, E={e:.2f}× {flag}")

print(f"\nCombined compound gallows → d:")
combined_exp = (mid_counts['d'] / total_mid) * combined_total
combined_e = combined_d_bigrams / combined_exp if combined_exp > 0 else float('inf')
flag = 'CONF' if combined_e >= 1.5 and combined_d_bigrams >= 10 else ('dir' if combined_e >= 2.0 and combined_d_bigrams >= 5 else '')
print(f"  COMBINED: obs={combined_d_bigrams}/{combined_total}, exp={combined_exp:.1f}, E={combined_e:.2f}× {flag}")

# --- Part 2: Directionality --- within lines with both c-gallows AND d
print("\n=== PART 2: Directionality of c-gallows vs d within co-occurring lines ===")

co_occur_lines = []
cgall_before_d_count = 0
d_before_cgall_count = 0
neither_count = 0  # multiple or tied

for fo, ws in lines_A:
    onsets = [get_onset(w) for w in ws]
    has_cgall = any(o in COMPOUND_GALLOWS for o in onsets)
    has_d = any(o == 'd' for o in onsets)
    if has_cgall and has_d:
        co_occur_lines.append((fo, ws, onsets))
        # Find all positions of c-gallows and d
        cgall_positions = [i for i, o in enumerate(onsets) if o in COMPOUND_GALLOWS]
        d_positions = [i for i, o in enumerate(onsets) if o == 'd']
        # Is at least one c-gallows before at least one d? (directional ordering)
        before = any(cp < dp for cp in cgall_positions for dp in d_positions)
        after = any(cp > dp for cp in cgall_positions for dp in d_positions)
        if before and not after:
            cgall_before_d_count += 1
        elif after and not before:
            d_before_cgall_count += 1
        else:
            neither_count += 1  # both orderings present or equal

print(f"Lines with both c-gallows and d: {len(co_occur_lines)}")
print(f"  c-gallows BEFORE d (exclusively): {cgall_before_d_count} ({100*cgall_before_d_count/max(1,len(co_occur_lines)):.1f}%)")
print(f"  d BEFORE c-gallows (exclusively): {d_before_cgall_count} ({100*d_before_cgall_count/max(1,len(co_occur_lines)):.1f}%)")
print(f"  Mixed (both orderings): {neither_count} ({100*neither_count/max(1,len(co_occur_lines)):.1f}%)")

# Expected under random ordering: if positions random, roughly equal before/after
# More rigorous: expected directional rate if c-gallows and d positions independent
# Baseline: among ALL lines, what fraction have c-gallows before d (when both present)?
# The directional ratio
total_ordered = cgall_before_d_count + d_before_cgall_count
if total_ordered > 0:
    dir_ratio = cgall_before_d_count / total_ordered
    print(f"\n  Directional ratio (before/total ordered): {cgall_before_d_count}/{total_ordered} = {dir_ratio:.3f}")
    print(f"  (Expected 0.50 if random; >0.67 would be noteworthy)")

# --- Part 3: [y][ckh][d] triplet analysis ---
print("\n=== PART 3: [y][ckh][d] triplet analysis ===")

ykh_d_triplets = 0
ykh_total = 0
for fo, ws in lines_A:
    for i in range(len(ws) - 2):
        if get_onset(ws[i]) == 'y' and get_onset(ws[i+1]) == 'ckh':
            ykh_total += 1
            if get_onset(ws[i+2]) == 'd':
                ykh_d_triplets += 1

print(f"[y][ckh] consecutive pairs: {ykh_total}")
print(f"[y][ckh][d] triplets: {ykh_d_triplets}")
if ykh_total > 0:
    print(f"Rate of [y][ckh]→d: {ykh_d_triplets}/{ykh_total} = {100*ykh_d_triplets/ykh_total:.1f}%")

# Baseline: of all [y][ckh] pairs, what fraction are followed by d?
# Expected: MID rate of d = mid_counts['d'] / total_mid
expected_d_after_ykh = (mid_counts['d'] / total_mid) * ykh_total
print(f"Expected [y][ckh]→d if MID baseline: {expected_d_after_ykh:.1f}")
if ykh_total > 0 and expected_d_after_ykh > 0:
    e = ykh_d_triplets / expected_d_after_ykh
    print(f"E([y][ckh]→d vs MID): {e:.2f}×")

# Also check [o][ckh][d]
okh_d_triplets = 0
okh_total = 0
for fo, ws in lines_A:
    for i in range(len(ws) - 2):
        if get_onset(ws[i]) == 'o' and get_onset(ws[i+1]) == 'ckh':
            okh_total += 1
            if get_onset(ws[i+2]) == 'd':
                okh_d_triplets += 1

print(f"\n[o][ckh] consecutive pairs: {okh_total}")
print(f"[o][ckh][d] triplets: {okh_d_triplets}")
if okh_total > 0:
    print(f"Rate: {100*okh_d_triplets/okh_total:.1f}%")

# --- Part 4: Position of c-gallows→d bigrams ---
print("\n=== PART 4: Position of compound gallows → d consecutive bigrams ===")

cg_d_pos = Counter()  # 'pos1→pos2', 'MID→MID', 'LL→LF', etc.
for fo, ws in lines_A:
    L = len(ws)
    for i in range(L - 1):
        if get_onset(ws[i]) in COMPOUND_GALLOWS and get_onset(ws[i+1]) == 'd':
            if i == 0:
                cg_d_pos['pos1→pos2'] += 1
            elif i == L-2:
                cg_d_pos['LL→LF'] += 1
            else:
                cg_d_pos['MID→MID+1'] += 1

print(f"Compound gallows → d bigram positions:")
total_cg_d = sum(cg_d_pos.values())
for pos, cnt in sorted(cg_d_pos.items()):
    print(f"  {pos}: {cnt} ({100*cnt/max(1,total_cg_d):.1f}%)")

# Compare to expected position distribution
total_all_bigrams = 0
pos_dist = Counter()
for fo, ws in lines_A:
    L = len(ws)
    for i in range(L-1):
        if i == 0:
            pos_dist['pos1→pos2'] += 1
        elif i == L-2:
            pos_dist['LL→LF'] += 1
        else:
            pos_dist['MID→MID+1'] += 1
        total_all_bigrams += 1

print(f"\nBaseline bigram position distribution:")
for pos in ['pos1→pos2', 'MID→MID+1', 'LL→LF']:
    rate = pos_dist[pos] / total_all_bigrams if total_all_bigrams > 0 else 0
    obs_rate = cg_d_pos[pos] / total_cg_d if total_cg_d > 0 else 0
    e = obs_rate / rate if rate > 0 else float('inf')
    print(f"  {pos}: base={rate:.3f}, cg→d={obs_rate:.3f}, E={e:.2f}×")

# --- Part 5: Reverse — d → compound gallows (is there a d→c-gallows coupling?) ---
print("\n=== PART 5: Reverse — d → compound gallows routing ===")

d_to_cgall = Counter()
n_d_sender = 0
for fo, ws in lines_A:
    for i in range(len(ws) - 1):
        if get_onset(ws[i]) == 'd':
            d_to_cgall[get_onset(ws[i+1])] += 1
            n_d_sender += 1

print(f"d-sender bigrams: {n_d_sender}")
for cls in sorted(COMPOUND_GALLOWS):
    obs = d_to_cgall[cls]
    exp = (mid_counts[cls] / total_mid) * n_d_sender if total_mid > 0 else 0
    e = obs / exp if exp > 0 else float('inf')
    flag = 'CONF' if e >= 1.5 and obs >= 10 else ('dir' if e >= 2.0 and obs >= 5 else ('(dir)' if e >= 2.5 and obs >= 3 else ('DEPL' if e < 0.7 and obs >= 3 else '')))
    print(f"  d→{cls}: obs={obs}, exp={exp:.1f}, E={e:.2f}× {flag}")

print("\n=== SUMMARY ===")
print(f"Combined c-gallows → d: E={combined_e:.2f}×/obs={combined_d_bigrams} from {combined_total} sender bigrams")
print(f"Directionality: {cgall_before_d_count}/{len(co_occur_lines)} co-occur lines have c-gallows before d exclusively")
if total_ordered > 0:
    print(f"  Directional ratio: {dir_ratio:.3f} (before vs before+after)")
print(f"[y][ckh][d] triplets: {ykh_d_triplets}/{ykh_total} [y][ckh] pairs")
print(f"C-gallows → d position: LL→LF={cg_d_pos.get('LL→LF',0)} ({100*cg_d_pos.get('LL→LF',0)/max(1,total_cg_d):.0f}%), MID→MID+1={cg_d_pos.get('MID→MID+1',0)} ({100*cg_d_pos.get('MID→MID+1',0)/max(1,total_cg_d):.0f}%)")
