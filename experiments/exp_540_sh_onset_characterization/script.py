"""
exp_540: H_new_FD — sh-onset full characterization

Four-part characterization of sh-onset class in both dialects:
1. sh vocabulary (top words, type/token counts)
2. sh positional distribution (pos1, MID, LL, LF) vs baseline
3. sh within-line bigrams (sh→X)
4. sh-LF lines: pos1 opener profile

Compare to template class hierarchy (F539): where does sh fit?
sh→qok (F372 CONF); ch↔sh avoidance (F328); sh→ok CL dir (F509).
"""
from pathlib import Path as _RepositoryPath
import re
from collections import defaultdict, Counter

CORPUS = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')
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
a_ha_folios = {n: ls for n, ls in folio_lines.items() if n <= 56 and not is_b_dialect(ls)}
b_all_folios = {n: ls for n, ls in folio_lines.items() if is_b_dialect(ls)}
a_ha_lines = [ln for ls in a_ha_folios.values() for ln in ls]
b_all_lines = [ln for ls in b_all_folios.values() for ln in ls]

print(f"A herbal_a: {len(a_ha_lines)} lines")
print(f"B all: {len(b_all_lines)} lines")

for label, lines in [("A herbal_a", a_ha_lines), ("B all", b_all_lines)]:
    print(f"\n{'='*60}")
    print(f"{label}")
    print(f"{'='*60}")

    # Part 1: Vocabulary
    sh_words = [w for ln in lines for w in ln if get_onset(w) == 'sh']
    cnt = Counter(sh_words)
    total = len(sh_words)
    print(f"\n[VOCAB] {total} tokens, {len(cnt)} types")
    print("Top words:", ', '.join(f"{w}({100*c/total:.1f}%)" for w, c in cnt.most_common(10)))

    # Part 2: Positional distribution
    all_words = [w for ln in lines for w in ln]
    base_rate = sum(1 for w in all_words if get_onset(w) == 'sh') / len(all_words)
    pos1_t = pos1_sh = mid_t = mid_sh = ll_t = ll_sh = lf_t = lf_sh = 0
    for ln in lines:
        lf_t += 1
        if get_onset(ln[-1]) == 'sh': lf_sh += 1
        if len(ln) >= 2:
            pos1_t += 1
            if get_onset(ln[0]) == 'sh': pos1_sh += 1
        if len(ln) >= 3:
            ll_t += 1
            if get_onset(ln[-2]) == 'sh': ll_sh += 1
        for w in ln[1:-1]:
            mid_t += 1
            if get_onset(w) == 'sh': mid_sh += 1
    print(f"\n[POSITIONAL] base_rate={100*base_rate:.2f}%")
    for name, obs, N in [('pos1', pos1_sh, pos1_t), ('MID', mid_sh, mid_t), ('LL', ll_sh, ll_t), ('LF', lf_sh, lf_t)]:
        r = obs/N if N>0 else 0
        E = r/base_rate if base_rate>0 else 0
        print(f"  {name:>6} {obs:>4}/{N:<6} {100*r:.1f}% E={E:.2f}× {flag(obs, E)}")

    # Part 3: Within-line bigrams
    send_n = 0; tgts = Counter(); all_succ = Counter(); tot_bg = 0
    for ln in lines:
        for i in range(len(ln)-1):
            tot_bg += 1
            all_succ[get_onset(ln[i+1])] += 1
            if get_onset(ln[i]) == 'sh':
                send_n += 1
                tgts[get_onset(ln[i+1])] += 1
    print(f"\n[BIGRAMS] {send_n} sh sender bigrams")
    for tgt, obs in tgts.most_common(10):
        br = all_succ[tgt] / tot_bg if tot_bg > 0 else 0
        cr = obs / send_n if send_n > 0 else 0
        E = cr/br if br>0 else 0
        print(f"  sh→{tgt}: {obs} E={E:.2f}× {flag(obs, E)}")

    # Part 4: sh-LF pos1 profile
    sh_lf_lines = [ln for ln in lines if len(ln) >= 2 and get_onset(ln[-1]) == 'sh']
    all_p2 = [ln for ln in lines if len(ln) >= 2]
    base_p1 = Counter(get_onset(ln[0]) for ln in all_p2)
    N_base = len(all_p2)
    shlf_p1 = Counter(get_onset(ln[0]) for ln in sh_lf_lines)
    N_shlf = len(sh_lf_lines)
    print(f"\n[sh-LF pos1] N={N_shlf} ({100*N_shlf/len(lines):.1f}%)")
    for cls, obs in shlf_p1.most_common(8):
        br = base_p1[cls] / N_base if N_base > 0 else 0
        cr = obs / N_shlf if N_shlf > 0 else 0
        E = cr/br if br > 0 else 0
        print(f"  pos1={cls}: {obs}/{N_shlf} E={E:.2f}× {flag(obs, E)}")
