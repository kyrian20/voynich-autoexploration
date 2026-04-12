"""
exp_514: B sections pos2 cross-class routing survey (H_new_DF)
Question: After retracting all pos2 self-chain findings, do B herbal/astro/pharma have
confirmed cross-class pos2 rules?
Method: Systematic pos2 survey for all LF classes with N_elig>=5 (len>=3) in each B section.
Cross-class only (LF onset != pos2 onset). Correct len>=3 methodology.
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
b_herbal, b_astro, b_pharma = [], [], []
for n, lines in folio_lines.items():
    if not is_b_dialect(lines):
        continue
    if n <= 72:
        b_herbal.extend(lines)
    elif n <= 84:
        b_astro.extend(lines)
    elif n <= 116:
        b_pharma.extend(lines)

sections = [
    ('B herbal', b_herbal),
    ('B astro', b_astro),
    ('B pharma', b_pharma),
]

def pos2_survey(section_lines, label):
    """Full pos2 cross-class survey (len>=3)."""
    print(f"\n{'='*60}")
    print(f"{label} (N={len(section_lines)} lines)")
    print(f"{'='*60}")

    # pos2 baseline (len>=3)
    all_pos2 = [get_onset(ln[1]) for ln in section_lines if len(ln) >= 3]
    pos2_base = Counter(all_pos2)
    total_pos2 = sum(pos2_base.values())

    if total_pos2 == 0:
        print("  No eligible lines.")
        return

    # LF distribution
    all_lf = Counter(get_onset(ln[-1]) for ln in section_lines)

    print(f"pos2 baseline lines: {total_pos2}")
    print(f"Top pos2 classes: {dict(sorted(pos2_base.items(), key=lambda x: -x[1])[:6])}")

    print(f"\n{'LF-class':<8} {'pos2-onset':<10} {'obs':>5} {'N_elig':>6} {'E':>7}  flag")
    results = []
    for lf_class, lf_n in sorted(all_lf.items(), key=lambda x: -x[1]):
        lf_lines = [ln for ln in section_lines if get_onset(ln[-1]) == lf_class]
        elig = [ln for ln in lf_lines if len(ln) >= 3]
        N_elig = len(elig)
        if N_elig < 5:
            continue
        pos2_dist = Counter(get_onset(ln[1]) for ln in elig)
        for onset, obs in sorted(pos2_dist.items(), key=lambda x: -x[1]):
            if onset == lf_class:
                continue  # skip self-chain
            base = pos2_base.get(onset, 0) / total_pos2 if total_pos2 > 0 else 0
            if base == 0:
                continue
            E = (obs / N_elig) / base
            if E < 1.5 or obs < 3:
                continue
            results.append((lf_class, onset, obs, N_elig, E))
            flag = 'CONF' if E >= 1.5 and obs >= 10 else \
                   ('dir' if E >= 2.0 and obs >= 5 else \
                   '(dir)' if E >= 2.5 and obs >= 3 else '')
            print(f"{lf_class:<8} → {onset:<10} obs={obs:>4}/{N_elig:>4} E={E:>6.2f}×  {flag}")

    if not results:
        print("  No cross-class pos2 enrichments at E>=1.5×/obs>=3")

    # Also reproduce F457 (B herbal d→sh)
    if label.startswith('B herbal'):
        print(f"\nF457 reproduction check (B herbal d-LF → sh@pos2):")
        d_lf = [ln for ln in section_lines if get_onset(ln[-1]) == 'd']
        d_elig = [ln for ln in d_lf if len(ln) >= 3]
        sh_obs = sum(1 for ln in d_elig if get_onset(ln[1]) == 'sh')
        base_sh = pos2_base.get('sh', 0) / total_pos2
        E_sh = (sh_obs / len(d_elig)) / base_sh if base_sh > 0 and d_elig else 0
        flag = 'CONF' if E_sh >= 1.5 and sh_obs >= 10 else ('dir' if E_sh >= 2.0 and sh_obs >= 5 else '')
        print(f"  d-LF N_elig={len(d_elig)}, sh@pos2: obs={sh_obs}, E={E_sh:.2f}× {flag}")

for label, section_lines in sections:
    pos2_survey(section_lines, label)

print("\n\n=== SUMMARY ===")
print("Confirmed cross-class pos2 rules (E>=1.5x/N>=10) after correction:")
print("  A herbal_a: F493 qot→sh (E=2.63×/N=10) — THE ONLY ONE IN A-DIALECT")
print("  B herbal: F457 d→sh (E=1.73×/N=10) — repro check above")
print("  (All self-chain pos2 findings retracted F461-F471)")
