"""
exp_537: H_new_EX — qok-onset full characterization

Four-part characterization of qok-onset class in both dialects:
1. qok vocabulary (top words, type/token counts)
2. qok positional distribution (pos1, MID, LL, LF) — completing template class quad
3. qok within-line bigrams (qok sender → next word onset)
4. qok-LF lines: pos1 opener profile

Completes the template class quad: qot (F533/F534), ot (F536/F537), ok (F539/F540), qok (this exp).
Compare against qo-prefix gradient from F539.
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

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
# Part 1: qok Vocabulary
# ============================================================
print("\n" + "="*60)
print("PART 1: qok VOCABULARY")
print("="*60)

for label, lines in [("A herbal_a", a_ha_lines), ("B all", b_all_lines)]:
    qok_words = [w for ln in lines for w in ln if get_onset(w) == 'qok']
    cnt = Counter(qok_words)
    total = len(qok_words)
    print(f"\n{label}: {total} tokens, {len(cnt)} types")
    print("Top words:", ', '.join(f"{w}({100*c/total:.1f}%)" for w, c in cnt.most_common(12)))

# ============================================================
# Part 2: qok Positional Distribution
# ============================================================
print("\n" + "="*60)
print("PART 2: qok POSITIONAL DISTRIBUTION")
print("="*60)

def positional_stats(lines, label):
    pos1_total = 0; mid_total = 0; ll_total = 0; lf_total = 0
    pos1_qok = 0; mid_qok = 0; ll_qok = 0; lf_qok = 0
    for ln in lines:
        n = len(ln)
        lf_total += 1
        if get_onset(ln[-1]) == 'qok': lf_qok += 1
        if n >= 2:
            pos1_total += 1
            if get_onset(ln[0]) == 'qok': pos1_qok += 1
        if n >= 3:
            ll_total += 1
            if get_onset(ln[-2]) == 'qok': ll_qok += 1
        for w in ln[1:-1]:
            mid_total += 1
            if get_onset(w) == 'qok': mid_qok += 1
    all_words = [w for ln in lines for w in ln]
    base_rate = sum(1 for w in all_words if get_onset(w) == 'qok') / len(all_words)
    print(f"\n{label}: base rate={100*base_rate:.2f}%")
    print(f"{'Pos':>6} {'obs/N':>10} {'rate':>7} {'E':>6} {'flag':>8}")
    for name, obs, N in [
        ('pos1', pos1_qok, pos1_total),
        ('MID',  mid_qok,  mid_total),
        ('LL',   ll_qok,   ll_total),
        ('LF',   lf_qok,   lf_total),
    ]:
        rate = obs/N if N > 0 else 0
        E = rate/base_rate if base_rate > 0 else 0
        print(f"{name:>6} {obs:>4}/{N:<6} {100*rate:>5.1f}%  {E:>5.2f}×  {flag(obs, E)}")

positional_stats(a_ha_lines, "A herbal_a")
positional_stats(b_all_lines, "B all")

# ============================================================
# Part 3: qok Within-Line Bigrams (sender)
# ============================================================
print("\n" + "="*60)
print("PART 3: qok WITHIN-LINE BIGRAMS (qok→X)")
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
            if get_onset(ln[i]) == 'qok':
                sender_total += 1
                sender_targets[get_onset(ln[i+1])] += 1
    print(f"\n{label}: {sender_total} qok sender bigrams (total bigrams={total_bigrams})")
    print(f"{'Target':>8} {'obs':>5} {'E':>6} {'flag':>8}")
    for tgt, obs in sender_targets.most_common(12):
        base_rate = all_successors[tgt] / total_bigrams if total_bigrams > 0 else 0
        cond_rate = obs / sender_total if sender_total > 0 else 0
        E = cond_rate / base_rate if base_rate > 0 else 0
        print(f"{tgt:>8} {obs:>5} {E:>6.2f}×  {flag(obs, E)}")

within_line_bigrams(a_ha_lines, "A herbal_a")
within_line_bigrams(b_all_lines, "B all")

# ============================================================
# Part 4: qok-LF Lines — pos1 opener profile
# ============================================================
print("\n" + "="*60)
print("PART 4: qok-LF LINES — pos1 OPENER PROFILE")
print("="*60)

def qok_lf_pos1(lines, label):
    qok_lf_lines = [ln for ln in lines if len(ln) >= 2 and get_onset(ln[-1]) == 'qok']
    all_lines_p2 = [ln for ln in lines if len(ln) >= 2]
    base_pos1 = Counter(get_onset(ln[0]) for ln in all_lines_p2)
    N_base = len(all_lines_p2)
    qoklf_pos1 = Counter(get_onset(ln[0]) for ln in qok_lf_lines)
    N_qoklf = len(qok_lf_lines)
    rate_qoklf = N_qoklf / len(lines) if lines else 0
    print(f"\n{label}: qok-LF lines N={N_qoklf} ({100*rate_qoklf:.1f}%)")
    print(f"{'Class':>8} {'obs':>4}/{N_qoklf}  {'E':>6}  {'flag':>8}")
    for cls, obs in qoklf_pos1.most_common(8):
        base_rate = base_pos1[cls] / N_base if N_base > 0 else 0
        cond_rate = obs / N_qoklf if N_qoklf > 0 else 0
        E = cond_rate / base_rate if base_rate > 0 else 0
        print(f"{cls:>8} {obs:>4}/{N_qoklf}    {E:>5.2f}×  {flag(obs, E)}")

qok_lf_pos1(a_ha_lines, "A herbal_a")
qok_lf_pos1(b_all_lines, "B all")

# ============================================================
# Part 5: Template class quad summary
# ============================================================
print("\n" + "="*60)
print("PART 5: COMPLETE TEMPLATE CLASS QUAD SUMMARY")
print("="*60)
print("Template class positional hierarchy — A herbal_a pos1 E (from F539 + this exp):")
print("  qot: E=1.79× CONF (F533)")
print("  qok: (this experiment)")
print("  ot:  E=1.29× sub-CONF (F536)")
print("  ok:  E=1.10× neutral (F539)")
print()
print("Template class within-line →ch behavior:")
print("  qot→ch: E=1.06× BASELINE (F535)")
print("  qok→ch: (this experiment)")
print("  ot→ch:  E=0.77× DEPLETED (F537)")
print("  ok→ch:  E=1.11× BASELINE (exp_536)")
