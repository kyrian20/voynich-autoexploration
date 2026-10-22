"""
exp_511: A herbal_a cross-line coupling (CL) systematic survey
Question H_new_CS: Does A herbal_a have confirmed LF→next-LF cross-line coupling rules?
Full N×N onset-class matrix for LF_n → LF_{n+1} pairs within the same folio.
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

def parse_corpus_by_folio():
    """Return dict: folio_n -> list of word-lists (lines), preserving order."""
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

folio_lines = parse_corpus_by_folio()

# A herbal_a: folios n <= 56
a_herbal_a_by_folio = {n: lines for n, lines in folio_lines.items() if n <= 56}
a_herbal_a_all = [ln for lines in a_herbal_a_by_folio.values() for ln in lines]

print(f"A herbal_a: {len(a_herbal_a_all)} lines across {len(a_herbal_a_by_folio)} folios")

# Build LF sequence per folio (preserving line order), then generate consecutive pairs
# within each folio
cl_pairs = []  # list of (lf_n_onset, lf_n1_onset)
for n in sorted(a_herbal_a_by_folio):
    lines = a_herbal_a_by_folio[n]
    # LF word = last word of each line
    lf_onsets = [get_onset(ln[-1]) for ln in lines if ln]
    for i in range(len(lf_onsets) - 1):
        if lf_onsets[i] and lf_onsets[i+1]:
            cl_pairs.append((lf_onsets[i], lf_onsets[i+1]))

print(f"Cross-line pairs (within folios): {len(cl_pairs)}")

# LF baseline from A herbal_a
lf_all = [get_onset(ln[-1]) for ln in a_herbal_a_all if ln]
lf_counts = Counter(lf_all)
total_lf = sum(lf_counts.values())
lf_base = {o: c / total_lf for o, c in lf_counts.items()}

# For each ordered pair (A, B): E = obs(A→B) / (base_A * base_B * N_pairs)
pair_counts = Counter(cl_pairs)
total_pairs = len(cl_pairs)

# Report results
print(f"\nLF distribution (A herbal_a):")
for onset, cnt in sorted(lf_counts.items(), key=lambda x: -x[1])[:12]:
    print(f"  {onset}: {cnt}/{total_lf} ({cnt/total_lf:.1%})")

print(f"\n--- CL matrix: confirmed (E≥1.5×/N≥10) and directional (E≥2.0×/N≥5 or E≥2.5×/N≥3) ---")

results = []
for (a, b), obs in pair_counts.items():
    base_a = lf_base.get(a, 0)
    base_b = lf_base.get(b, 0)
    if base_a == 0 or base_b == 0:
        continue
    expected = base_a * base_b * total_pairs
    if expected == 0:
        continue
    E = obs / expected
    results.append((a, b, obs, expected, E))

results.sort(key=lambda x: -x[4])

print(f"\nTop enriched pairs (obs≥3, E≥1.5×):")
print(f"{'A→B':<12} {'obs':>5} {'exp':>7} {'E':>7}  flag")
for a, b, obs, exp, E in results:
    if obs < 3 or E < 1.5:
        continue
    if E >= 1.5 and obs >= 10:
        flag = "CONF"
    elif E >= 2.0 and obs >= 5:
        flag = "dir"
    elif E >= 2.5 and obs >= 3:
        flag = "(dir)"
    else:
        flag = ""
    print(f"{a}→{b:<8} {obs:>5} {exp:>7.2f} {E:>7.2f}×  {flag}")

print(f"\nDepleted pairs (obs≥3, E≤0.5×):")
print(f"{'A→B':<12} {'obs':>5} {'exp':>7} {'E':>7}")
for a, b, obs, exp, E in sorted(results, key=lambda x: x[4]):
    if obs < 3 or E > 0.5:
        continue
    print(f"{a}→{b:<8} {obs:>5} {exp:>7.2f} {E:>7.2f}×")

# --- Summary table for key onset pairs ---
print("\n--- Detailed check on F438/F445 previously-reported pairs ---")
check_pairs = [
    ('s', 'qot'), ('s', 's'), ('ch', 'ch'), ('ok', 'y'),
    ('sh', 'd'), ('d', 'ch'), ('d', 'd'), ('cth', 'cth'),
    ('ok', 'ok'), ('ot', 'ot'), ('y', 'y'), ('y', 'ok'),
    ('ch', 'ok'), ('d', 'ok'), ('ok', 'd'),
]
for a, b in check_pairs:
    obs = pair_counts.get((a, b), 0)
    base_a = lf_base.get(a, 0)
    base_b = lf_base.get(b, 0)
    if base_a > 0 and base_b > 0:
        exp = base_a * base_b * total_pairs
        E = obs / exp if exp > 0 else 0
        flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else ("(dir)" if E >= 2.5 and obs >= 3 else ""))
        print(f"  {a}→{b}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")

# --- Self-succession summary ---
print("\n--- Self-succession (LF_n = LF_{n+1}) ---")
for onset, base in sorted(lf_base.items(), key=lambda x: -x[1])[:12]:
    obs = pair_counts.get((onset, onset), 0)
    exp = base * base * total_pairs
    E = obs / exp if exp > 0 else 0
    flag = "CONF" if E >= 1.5 and obs >= 10 else ("dir" if E >= 2.0 and obs >= 5 else ("(dir)" if E >= 2.5 and obs >= 3 else ""))
    print(f"  {onset}→{onset}: obs={obs}, exp={exp:.2f}, E={E:.2f}× {flag}")

# --- Check if folio-ordering is consistent ---
print(f"\n--- Folio coverage ---")
for n in sorted(a_herbal_a_by_folio)[:10]:
    print(f"  f{n}: {len(a_herbal_a_by_folio[n])} lines")
