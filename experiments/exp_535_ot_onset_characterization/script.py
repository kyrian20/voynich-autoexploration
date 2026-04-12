"""
exp_535: H588_archived — ot-onset full characterization

Four-part characterization of ot-onset class in both dialects:
1. ot vocabulary (top words, type/token counts)
2. ot positional distribution (pos1, MID, LL, LF) vs section baseline
3. ot within-line bigrams (ot sender → next word onset)
4. ot-LF lines: pos1 opener profile

Compare to qot characterization (F533/F534/F535, exp_534).
"""

import re
from collections import defaultdict, Counter

CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSET_PRIORITY = [
    'qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
    'd','s','y','k','t','l','r','p','f','o','e','a','n','m'
]

def get_onset(word):
    for onset in ONSET_PRIORITY:
        if word.startswith(onset):
            return onset
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

def is_b_dialect(lines):
    words = [w for ln in lines for w in ln]
    if not words:
        return False
    edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return edy / len(words) >= 0.05

def flag(obs, E):
    if obs >= 10 and E >= 1.5: return 'CONF'
    elif obs >= 5 and E >= 2.0: return 'dir'
    elif obs >= 3 and E >= 2.5: return '(dir)'
    elif E >= 1.0: return f'{E:.2f}×'
    else: return f'DEPL {E:.2f}×'

folio_lines = parse_corpus(CORPUS)

a_ha_folios = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
b_all_folios = {n: ls for n, ls in folio_lines.items() if is_b_dialect(ls)}

a_ha_lines = [ln for ls in a_ha_folios.values() for ln in ls]
b_all_lines = [ln for ls in b_all_folios.values() for ln in ls]

print(f"A herbal_a: {len(a_ha_lines)} lines")
print(f"B all: {len(b_all_lines)} lines")

# ============================================================
# Part 1: ot Vocabulary
# ============================================================
print("\n" + "="*60)
print("PART 1: ot VOCABULARY")
print("="*60)

for label, lines in [("A herbal_a", a_ha_lines), ("B all", b_all_lines)]:
    ot_words = [w for ln in lines for w in ln if get_onset(w) == 'ot']
    cnt = Counter(ot_words)
    total = len(ot_words)
    print(f"\n{label}: {total} tokens, {len(cnt)} types")
    print("Top words:", ', '.join(f"{w}({100*c/total:.1f}%)" for w, c in cnt.most_common(12)))

# ============================================================
# Part 2: ot Positional Distribution
# ============================================================
print("\n" + "="*60)
print("PART 2: ot POSITIONAL DISTRIBUTION")
print("="*60)

def positional_stats(lines, label):
    pos1_total = 0; mid_total = 0; ll_total = 0; lf_total = 0
    pos1_ot = 0; mid_ot = 0; ll_ot = 0; lf_ot = 0
    for ln in lines:
        n = len(ln)
        lf_total += 1
        if get_onset(ln[-1]) == 'ot': lf_ot += 1
        if n >= 2:
            pos1_total += 1
            if get_onset(ln[0]) == 'ot': pos1_ot += 1
        if n >= 3:
            ll_total += 1
            if get_onset(ln[-2]) == 'ot': ll_ot += 1
        for w in ln[1:-1]:
            mid_total += 1
            if get_onset(w) == 'ot': mid_ot += 1
    all_words = [w for ln in lines for w in ln]
    base_rate = sum(1 for w in all_words if get_onset(w) == 'ot') / len(all_words)
    print(f"\n{label}: base rate={100*base_rate:.2f}%")
    print(f"{'Pos':>6} {'obs/N':>10} {'rate':>7} {'E':>6} {'flag':>8}")
    for name, obs, N in [
        ('pos1', pos1_ot, pos1_total),
        ('MID',  mid_ot,  mid_total),
        ('LL',   ll_ot,   ll_total),
        ('LF',   lf_ot,   lf_total),
    ]:
        rate = obs/N if N > 0 else 0
        E = rate/base_rate if base_rate > 0 else 0
        print(f"{name:>6} {obs:>4}/{N:<6} {100*rate:>5.1f}%  {E:>5.2f}×  {flag(obs, E)}")

positional_stats(a_ha_lines, "A herbal_a")
positional_stats(b_all_lines, "B all")

# ============================================================
# Part 3: ot Within-Line Bigrams (sender)
# ============================================================
print("\n" + "="*60)
print("PART 3: ot WITHIN-LINE BIGRAMS (ot→X)")
print("="*60)

def within_line_bigrams(lines, label):
    sender_total = 0
    sender_targets = Counter()
    all_successors = Counter()
    total_bigrams = 0
    for ln in lines:
        for i in range(len(ln)-1):
            total_bigrams += 1
            all_successors[get_onset(ln[i+1])] += 1
            if get_onset(ln[i]) == 'ot':
                sender_total += 1
                sender_targets[get_onset(ln[i+1])] += 1
    print(f"\n{label}: {sender_total} ot sender bigrams (total bigrams={total_bigrams})")
    print(f"{'Target':>8} {'obs':>5} {'E':>6} {'flag':>8}")
    for tgt, obs in sender_targets.most_common(12):
        base_rate = all_successors[tgt] / total_bigrams if total_bigrams > 0 else 0
        cond_rate = obs / sender_total if sender_total > 0 else 0
        E = cond_rate / base_rate if base_rate > 0 else 0
        print(f"{tgt:>8} {obs:>5} {E:>6.2f}×  {flag(obs, E)}")

within_line_bigrams(a_ha_lines, "A herbal_a")
within_line_bigrams(b_all_lines, "B all")

# ============================================================
# Part 4: ot-LF Lines — pos1 opener profile
# ============================================================
print("\n" + "="*60)
print("PART 4: ot-LF LINES — pos1 OPENER PROFILE")
print("="*60)

def ot_lf_pos1(lines, label):
    ot_lf_lines = [ln for ln in lines if len(ln) >= 2 and get_onset(ln[-1]) == 'ot']
    all_lines_p2 = [ln for ln in lines if len(ln) >= 2]
    base_pos1 = Counter(get_onset(ln[0]) for ln in all_lines_p2)
    N_base = len(all_lines_p2)
    otlf_pos1 = Counter(get_onset(ln[0]) for ln in ot_lf_lines)
    N_otlf = len(ot_lf_lines)
    rate_otlf = N_otlf / len(lines) if lines else 0
    print(f"\n{label}: ot-LF lines N={N_otlf} ({100*rate_otlf:.1f}%)")
    print(f"{'Class':>8} {'obs':>4}/{N_otlf}  {'E':>6}  {'flag':>8}")
    for cls, obs in otlf_pos1.most_common(8):
        base_rate = base_pos1[cls] / N_base if N_base > 0 else 0
        cond_rate = obs / N_otlf if N_otlf > 0 else 0
        E = cond_rate / base_rate if base_rate > 0 else 0
        print(f"{cls:>8} {obs:>4}/{N_otlf}    {E:>5.2f}×  {flag(obs, E)}")

ot_lf_pos1(a_ha_lines, "A herbal_a")
ot_lf_pos1(b_all_lines, "B all")

# ============================================================
# Part 5: A/B comparison summary vs qot (F533/F534)
# ============================================================
print("\n" + "="*60)
print("PART 5: ot vs qot DIALECT COMPARISON")
print("="*60)
print("Expected from H588_archived:")
print("  - ot likely MID-enriched (template class, opposite of qot in A)")
print("  - ot→ot self-succession cross-dialectally stable (F369: A=1.94×, B=1.93×)")
print("  - B ot/qot pairing: qot→ot CONF (F534); does ot→qot also appear?")
print("  - A: ot is qot's positional complement (qot=LINE-OPENER; ot=?)")
