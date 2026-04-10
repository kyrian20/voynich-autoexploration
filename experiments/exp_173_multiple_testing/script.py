#!/usr/bin/env python3
"""
exp_173: Bonferroni and BH-FDR re-analysis of quantitative findings.
Computes proper p-values for the top 30 candidate findings and applies
multiple-testing correction.

Test types:
- Enrichment ratios with count data: binomial test (one-sided)
- Bigram enrichments: Fisher's exact test on 2×2 contingency tables
- Positional enrichments: binomial test
- Categorical exclusions (0/n): one-sided exact binomial

Corrections: Bonferroni (α=0.05/30), BH-FDR (q=0.05).
"""
import re, math
from collections import Counter, defaultdict
from scipy import stats
import numpy as np

VMS_CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

# ── Onset classifier ──────────────────────────────────────────────────────────
def get_onset(word):
    w = word.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'):  return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    if w.startswith('ch'):  return 'ch'
    if w.startswith('sh'):  return 'sh'
    if w.startswith('ok'):  return 'ok'
    if w.startswith('ot'):  return 'ot'
    if w.startswith('ol'):  return 'ol'
    if w.startswith('d'):   return 'd'
    if w.startswith('s'):   return 's'
    if w.startswith('y'):   return 'y'
    if w.startswith('k'):   return 'k'
    if w.startswith('t'):   return 't'
    if w.startswith('l'):   return 'l'
    if w.startswith('r'):   return 'r'
    return 'other'

SECTION_RANGES = {
    'herbal':  list(range(1, 67)),
    'astro':   list(range(67, 85)),
    'pharma':  list(range(88, 103)),
    'cosmo':   list(range(85, 88)),
    'stars':   list(range(103, 117)),
    'bio':     list(range(75, 85)) + list(range(116, 118)),
}
folio_to_section = {fn: s for s, folios in SECTION_RANGES.items() for fn in folios}

def get_slot(i, n):
    if n == 1: return 'only'
    if i == 0: return 'LF'
    if i == n-1: return 'LL'
    if i == 1: return 'second'
    return 'MID'

# ── Parse VMS ─────────────────────────────────────────────────────────────────
print("Parsing VMS corpus...")
folio_words = defaultdict(list)
raw_lines = []
with open(VMS_CORPUS) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('#'): continue
        parts = line.split(None, 1)
        if len(parts) < 2: continue
        locus_raw, text = parts
        lparts = locus_raw.split(',')
        if len(lparts) < 2: continue
        folio_base = lparts[0].split('.')[0].lstrip('<')
        m = re.match(r'f(\d+)', folio_base)
        if not m: continue
        fnum = int(m.group(1))
        lt = lparts[1].rstrip('>').lstrip('@+*=~&')
        if not lt.startswith('P'): continue
        words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
        if not words: continue
        folio_words[fnum].extend(words)
        raw_lines.append((fnum, words))

folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'

a_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'A']
b_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'B']

a_words = [w for _, wds in a_lines for w in wds]
b_words = [w for _, wds in b_lines for w in wds]
all_words = a_words + b_words

a_n = len(a_words)
b_n = len(b_words)
all_n = len(all_words)

a_onset = Counter(get_onset(w) for w in a_words)
b_onset = Counter(get_onset(w) for w in b_words)

a_lf = [wds[0] for _, wds in a_lines if wds]
a_ll = [wds[-1] for _, wds in a_lines if wds]
b_lf = [wds[0] for _, wds in b_lines if wds]
b_ll = [wds[-1] for _, wds in b_lines if wds]

print(f"A-dialect: {a_n} words, {len(a_lines)} lines")
print(f"B-dialect: {b_n} words, {len(b_lines)} lines")

# ── Statistical test helpers ──────────────────────────────────────────────────
def binom_p(k, n, p0, alternative='greater'):
    """One-sided binomial test p-value: P(X >= k | n, p0) for 'greater'."""
    if n < 10:
        return None
    result = stats.binomtest(k, n, p0, alternative=alternative)
    return result.pvalue

def fisher_p(a, b, c, d):
    """Fisher's exact test p-value (one-sided) for 2×2 table:
    | a  b |
    | c  d |
    Tests: a/(a+b) > c/(c+d)
    """
    _, p = stats.fisher_exact([[a, b], [c, d]], alternative='greater')
    return p

def enrich(k, n, p0):
    return (k/n) / p0 if n > 0 and p0 > 0 else None

# ── BH-FDR correction ─────────────────────────────────────────────────────────
def bh_correct(p_values, q=0.05):
    """Benjamini-Hochberg FDR correction. Returns list of booleans (reject H0)."""
    n = len(p_values)
    if n == 0:
        return []
    # Pair with original indices
    indexed = [(p, i) for i, p in enumerate(p_values) if p is not None]
    indexed_sorted = sorted(indexed, key=lambda x: x[0])
    reject = [False] * n
    for rank, (p, orig_idx) in enumerate(indexed_sorted, 1):
        threshold = (rank / n) * q
        if p <= threshold:
            reject[orig_idx] = True
    # BH is monotone: if rank k is rejected, all ranks < k are also rejected
    # Apply cumulative: find largest k such that p(k) <= k/m * q
    max_reject = -1
    for rank, (p, orig_idx) in enumerate(indexed_sorted, 1):
        if p <= (rank / n) * q:
            max_reject = rank
    # All tests up to max_reject are rejected
    reject2 = [False] * n
    for rank, (p, orig_idx) in enumerate(indexed_sorted, 1):
        if rank <= max_reject:
            reject2[orig_idx] = True
    return reject2

# ── Define the 30 candidate findings ─────────────────────────────────────────
print("\nComputing p-values for 30 candidate findings...")

findings = []  # list of (id, description, dialect, family, test_fn)

# ── FAMILY 1: Positional grammar ──────────────────────────────────────────────

# F1: y-onset LF enrichment in A-dialect
y_lf_a = sum(1 for w in a_lf if get_onset(w) == 'y')
n_lf_a = len(a_lf)
y_base_a = a_onset.get('y', 0) / a_n
p_y_lf_a = binom_p(y_lf_a, n_lf_a, y_base_a)
findings.append(('F1', 'y-onset LF enrichment (A)', 'A', 'positional',
    y_lf_a, n_lf_a, y_base_a, y_lf_a/n_lf_a/y_base_a, p_y_lf_a))

# F2: cth LF depletion in A (test for depletion: one-sided less)
cth_lf_a = sum(1 for w in a_lf if get_onset(w) == 'cth')
cth_base_a = a_onset.get('cth', 0) / a_n
p_cth_lf_a = binom_p(cth_lf_a, n_lf_a, cth_base_a, alternative='less')
findings.append(('F2', 'cth LF depletion (A)', 'A', 'positional',
    cth_lf_a, n_lf_a, cth_base_a, enrich(cth_lf_a, n_lf_a, cth_base_a), p_cth_lf_a))

# F3: -am LL enrichment in B
am_ll_b = sum(1 for w in b_ll if w.endswith('am'))
n_ll_b = len(b_ll)
am_base_b = sum(1 for w in b_words if w.endswith('am')) / b_n
p_am_ll_b = binom_p(am_ll_b, n_ll_b, am_base_b)
findings.append(('F3', '-am LL enrichment (B)', 'B', 'positional',
    am_ll_b, n_ll_b, am_base_b, enrich(am_ll_b, n_ll_b, am_base_b), p_am_ll_b))

# F4: -am LL enrichment in A
am_ll_a = sum(1 for w in a_ll if w.endswith('am'))
n_ll_a = len(a_ll)
am_base_a = sum(1 for w in a_words if w.endswith('am')) / a_n
p_am_ll_a = binom_p(am_ll_a, n_ll_a, am_base_a)
findings.append(('F4', '-am LL enrichment (A)', 'A', 'positional',
    am_ll_a, n_ll_a, am_base_a, enrich(am_ll_a, n_ll_a, am_base_a), p_am_ll_a))

# F5: d LL enrichment in A
d_ll_a = sum(1 for w in a_ll if get_onset(w) == 'd')
d_base_a = a_onset.get('d', 0) / a_n
p_d_ll_a = binom_p(d_ll_a, n_ll_a, d_base_a)
findings.append(('F5', 'd LL enrichment (A)', 'A', 'positional',
    d_ll_a, n_ll_a, d_base_a, enrich(d_ll_a, n_ll_a, d_base_a), p_d_ll_a))

# F6: y-onset LF enrichment in B
y_lf_b = sum(1 for w in b_lf if get_onset(w) == 'y')
n_lf_b = len(b_lf)
y_base_b = b_onset.get('y', 0) / b_n
p_y_lf_b = binom_p(y_lf_b, n_lf_b, y_base_b)
findings.append(('F6', 'y-onset LF enrichment (B)', 'B', 'positional',
    y_lf_b, n_lf_b, y_base_b, enrich(y_lf_b, n_lf_b, y_base_b), p_y_lf_b))

# ── FAMILY 2: Bigram enrichments ──────────────────────────────────────────────

def bigram_fisher(lines, word_a_test, word_b_test):
    """Count bigrams where word A matches test_fn_a and word B matches test_fn_b.
    Returns (k=both, n=a_total, p0=b_rate_overall)
    """
    a_yes_b_yes = 0
    a_yes_b_no  = 0
    a_no_b_yes  = 0
    a_no_b_no   = 0
    for _, wds in lines:
        for i in range(len(wds)-1):
            a_match = word_a_test(wds[i])
            b_match = word_b_test(wds[i+1])
            if a_match:
                if b_match: a_yes_b_yes += 1
                else: a_yes_b_no += 1
            else:
                if b_match: a_no_b_yes += 1
                else: a_no_b_no += 1
    return a_yes_b_yes, a_yes_b_no, a_no_b_yes, a_no_b_no

# F7: daiin→cth enrichment (A)
a7, b7, c7, d7 = bigram_fisher(a_lines,
    lambda w: w == 'daiin',
    lambda w: get_onset(w) == 'cth')
p_dai_cth_a = fisher_p(a7, b7, c7, d7) if a7 + b7 >= 5 else None
enr_dai_cth_a = (a7/(a7+b7)) / ((a7+c7)/(a7+b7+c7+d7)) if (a7+b7) > 0 and (a7+c7) > 0 else None
findings.append(('F7', 'daiin→cth enrichment (A)', 'A', 'bigram',
    a7, a7+b7, (a7+c7)/(a7+b7+c7+d7), enr_dai_cth_a, p_dai_cth_a))

# F8: [ch][daiin]→cth enrichment (A)
ch_dai_cth = 0; ch_dai_other = 0
for _, wds in a_lines:
    for i in range(len(wds)-2):
        if get_onset(wds[i]) == 'ch' and wds[i+1] == 'daiin':
            if get_onset(wds[i+2]) == 'cth': ch_dai_cth += 1
            else: ch_dai_other += 1
# Compare to baseline: P(cth | position i+2)
# Use 2×2: [ch][daiin]→cth vs all [X][daiin]→cth
all_dai_bg = 0; all_dai_cth = 0
for _, wds in a_lines:
    for i in range(len(wds)-1):
        if wds[i] == 'daiin':
            all_dai_bg += 1
            if get_onset(wds[i+1]) == 'cth': all_dai_cth += 1
# Fisher: ch-daiin-cth vs other-daiin-cth
a8 = ch_dai_cth
b8 = ch_dai_other
# Baseline daiin→cth excluding ch-daiin cases
c8 = all_dai_cth - ch_dai_cth
d8 = (all_dai_bg - ch_dai_cth - ch_dai_other) - c8
p_ch_dai_cth = fisher_p(a8, b8, c8, d8) if a8+b8 >= 5 else None
enr_ch_dai_cth = (a8/(a8+b8)) / ((a8+c8)/(a8+b8+c8+d8)) if (a8+b8)>0 and (a8+c8)>0 else None
findings.append(('F8', '[ch][daiin]→cth enrichment (A)', 'A', 'bigram',
    a8, a8+b8, (a8+c8)/(a8+b8+c8+d8), enr_ch_dai_cth, p_ch_dai_cth))

# F9: qok→ch enrichment (B)
a9, b9, c9, d9 = bigram_fisher(b_lines,
    lambda w: get_onset(w) == 'qok',
    lambda w: get_onset(w) in ('ch', 'ch_e'))
p_qok_ch_b = fisher_p(a9, b9, c9, d9) if a9+b9 >= 5 else None
enr_qok_ch_b = (a9/(a9+b9)) / ((a9+c9)/(a9+b9+c9+d9)) if (a9+b9)>0 and (a9+c9)>0 else None
findings.append(('F9', 'qok→ch enrichment (B)', 'B', 'bigram',
    a9, a9+b9, (a9+c9)/(a9+b9+c9+d9), enr_qok_ch_b, p_qok_ch_b))

# F10: daiin→y enrichment (A)
a10, b10, c10, d10 = bigram_fisher(a_lines,
    lambda w: w == 'daiin',
    lambda w: get_onset(w) == 'y')
p_dai_y_a = fisher_p(a10, b10, c10, d10) if a10+b10 >= 5 else None
enr_dai_y_a = (a10/(a10+b10)) / ((a10+c10)/(a10+b10+c10+d10)) if (a10+b10)>0 and (a10+c10)>0 else None
findings.append(('F10', 'daiin→y enrichment (A)', 'A', 'bigram',
    a10, a10+b10, (a10+c10)/(a10+b10+c10+d10), enr_dai_y_a, p_dai_y_a))

# ── FAMILY 3: Self-succession enrichments ─────────────────────────────────────
for fid, cls, dialect, lines_set, words_set in [
    ('F11', 'ok', 'A', a_lines, a_words),
    ('F12', 'ch', 'A', a_lines, a_words),
    ('F13', 'qok', 'A', a_lines, a_words),
    ('F14', 'qo',  'B', b_lines, b_words),
    ('F15', 'ch',  'B', b_lines, b_words),
    ('F16', 'ok',  'B', b_lines, b_words),
]:
    n_ws = len(words_set)
    onset_c = Counter(get_onset(w) for w in words_set)
    cls_rate = onset_c.get(cls, 0) / n_ws
    a_ss, b_ss, c_ss, d_ss = bigram_fisher(lines_set,
        lambda w, c=cls: get_onset(w) == c,
        lambda w, c=cls: get_onset(w) == c)
    p_ss = fisher_p(a_ss, b_ss, c_ss, d_ss) if a_ss+b_ss >= 10 else None
    enr_ss = (a_ss/(a_ss+b_ss)) / cls_rate if (a_ss+b_ss)>0 and cls_rate>0 else None
    findings.append((fid, f'{cls} self-succession ({dialect})', dialect, 'self-succession',
        a_ss, a_ss+b_ss, cls_rate, enr_ss, p_ss))

# ── FAMILY 4: Dialect split (A vs B vocabulary) ───────────────────────────────

# F17: edy rate: B vs A (test: B edy rate > A edy rate using Fisher)
edy_b = sum(1 for w in b_words if 'edy' in w or 'eedy' in w)
edy_a = sum(1 for w in a_words if 'edy' in w or 'eedy' in w)
p_edy = fisher_p(edy_b, b_n - edy_b, edy_a, a_n - edy_a)
enr_edy = (edy_b/b_n) / (edy_a/a_n) if a_n > 0 else None
findings.append(('F17', 'edy rate B > A dialect split', 'AB', 'dialect-split',
    edy_b, b_n, edy_a/a_n, enr_edy, p_edy))

# F18: cth rate: A vs B (A has much more cth than B per-token)
cth_a = a_onset.get('cth', 0)
cth_b = b_onset.get('cth', 0)
p_cth_dialect = fisher_p(cth_a, a_n - cth_a, cth_b, b_n - cth_b)
enr_cth_dialect = (cth_a/a_n) / (cth_b/b_n) if b_n > 0 else None
findings.append(('F18', 'cth rate A > B dialect split', 'AB', 'dialect-split',
    cth_a, a_n, cth_b/b_n, enr_cth_dialect, p_cth_dialect))

# F19: qok rate: B vs A
qok_b = b_onset.get('qok', 0)
qok_a = a_onset.get('qok', 0)
p_qok_dialect = fisher_p(qok_b, b_n - qok_b, qok_a, a_n - qok_a)
enr_qok_dialect = (qok_b/b_n) / (qok_a/a_n) if a_n > 0 else None
findings.append(('F19', 'qok rate B > A dialect split', 'AB', 'dialect-split',
    qok_b, b_n, qok_a/a_n, enr_qok_dialect, p_qok_dialect))

# ── FAMILY 5: cth positional grammar ─────────────────────────────────────────

# F20: cth LL enrichment in A
cth_ll_a = sum(1 for w in a_ll if get_onset(w) == 'cth')
p_cth_ll_a = binom_p(cth_ll_a, n_ll_a, cth_base_a)
findings.append(('F20', 'cth LL enrichment (A)', 'A', 'cth-positional',
    cth_ll_a, n_ll_a, cth_base_a, enrich(cth_ll_a, n_ll_a, cth_base_a), p_cth_ll_a))

# F21: cth-word NEVER LF in A — test depletion
p_cth_lf_depletion = binom_p(cth_lf_a, n_lf_a, cth_base_a, alternative='less')
findings.append(('F21', 'cth LF depletion magnitude (A)', 'A', 'cth-positional',
    cth_lf_a, n_lf_a, cth_base_a, enrich(cth_lf_a, n_lf_a, cth_base_a), p_cth_lf_depletion))

# F22: cthy LL enrichment in A
cthy_ll_a = sum(1 for w in a_ll if w == 'cthy')
cthy_base_a = sum(1 for w in a_words if w == 'cthy') / a_n
p_cthy_ll_a = binom_p(cthy_ll_a, n_ll_a, cthy_base_a)
findings.append(('F22', 'cthy LL enrichment (A)', 'A', 'cth-positional',
    cthy_ll_a, n_ll_a, cthy_base_a, enrich(cthy_ll_a, n_ll_a, cthy_base_a), p_cthy_ll_a))

# ── FAMILY 6: Suffix paradigm ─────────────────────────────────────────────────

# F23: -ol rate in A (test A > B for -ol dominance)
ol_a = sum(1 for w in a_words if w.endswith('ol'))
ol_b = sum(1 for w in b_words if w.endswith('ol'))
p_ol_dialect = fisher_p(ol_a, a_n - ol_a, ol_b, b_n - ol_b)
enr_ol_dialect = (ol_a/a_n) / (ol_b/b_n) if b_n > 0 else None
findings.append(('F23', '-ol rate A > B (suffix paradigm)', 'AB', 'suffix',
    ol_a, a_n, ol_b/b_n, enr_ol_dialect, p_ol_dialect))

# F24: -or rate in A vs B
or_a = sum(1 for w in a_words if w.endswith('or'))
or_b = sum(1 for w in b_words if w.endswith('or'))
p_or_dialect = fisher_p(or_a, a_n - or_a, or_b, b_n - or_b)
enr_or_dialect = (or_a/a_n) / (or_b/b_n) if b_n > 0 else None
findings.append(('F24', '-or rate A > B (suffix paradigm)', 'AB', 'suffix',
    or_a, a_n, or_b/b_n, enr_or_dialect, p_or_dialect))

# ── FAMILY 7: Word-level identities (most frequent forms) ────────────────────

# F25: daiin is B-dialect line-first enriched
dai_lf_b = sum(1 for w in b_lf if w == 'daiin')
dai_base_b = sum(1 for w in b_words if w == 'daiin') / b_n
p_dai_lf_b = binom_p(dai_lf_b, n_lf_b, dai_base_b)
findings.append(('F25', 'daiin LF enrichment (B)', 'B', 'word-level',
    dai_lf_b, n_lf_b, dai_base_b, enrich(dai_lf_b, n_lf_b, dai_base_b), p_dai_lf_b))

# F26: daiin LF enrichment in A
dai_lf_a = sum(1 for w in a_lf if w == 'daiin')
dai_base_a = sum(1 for w in a_words if w == 'daiin') / a_n
p_dai_lf_a = binom_p(dai_lf_a, n_lf_a, dai_base_a)
findings.append(('F26', 'daiin LF enrichment (A)', 'A', 'word-level',
    dai_lf_a, n_lf_a, dai_base_a, enrich(dai_lf_a, n_lf_a, dai_base_a), p_dai_lf_a))

# F27: sh LF enrichment in B
sh_lf_b = sum(1 for w in b_lf if get_onset(w) == 'sh')
sh_base_b = b_onset.get('sh', 0) / b_n
p_sh_lf_b = binom_p(sh_lf_b, n_lf_b, sh_base_b)
findings.append(('F27', 'sh LF enrichment (B)', 'B', 'positional',
    sh_lf_b, n_lf_b, sh_base_b, enrich(sh_lf_b, n_lf_b, sh_base_b), p_sh_lf_b))

# F28: l-onset rate B > A
l_b = b_onset.get('l', 0)
l_a = a_onset.get('l', 0)
p_l_dialect = fisher_p(l_b, b_n - l_b, l_a, a_n - l_a)
enr_l_dialect = (l_b/b_n) / (l_a/a_n) if a_n > 0 else None
findings.append(('F28', 'l-onset rate B > A', 'AB', 'dialect-split',
    l_b, b_n, l_a/a_n, enr_l_dialect, p_l_dialect))

# F29: qok LF depletion in B
qok_lf_b = sum(1 for w in b_lf if get_onset(w) == 'qok')
qok_base_b = b_onset.get('qok', 0) / b_n
p_qok_lf_b = binom_p(qok_lf_b, n_lf_b, qok_base_b, alternative='less')
findings.append(('F29', 'qok LF depletion (B)', 'B', 'positional',
    qok_lf_b, n_lf_b, qok_base_b, enrich(qok_lf_b, n_lf_b, qok_base_b), p_qok_lf_b))

# F30: qo self-succession in A (1.31× from F164)
a30, b30, c30, d30 = bigram_fisher(a_lines,
    lambda w: get_onset(w) == 'qo',
    lambda w: get_onset(w) == 'qo')
p_qo_ss_a = fisher_p(a30, b30, c30, d30) if a30+b30 >= 5 else None
qo_base_a = a_onset.get('qo', 0) / a_n
enr_qo_ss_a = (a30/(a30+b30)) / qo_base_a if (a30+b30)>0 and qo_base_a>0 else None
findings.append(('F30', 'qo self-succession (A)', 'A', 'self-succession',
    a30, a30+b30, qo_base_a, enr_qo_ss_a, p_qo_ss_a))

# ── Apply corrections ─────────────────────────────────────────────────────────
p_values = [f[8] for f in findings]
n_tests = len([p for p in p_values if p is not None])
bonf_threshold = 0.05 / n_tests

# BH-FDR
bh_rejects = bh_correct(p_values, q=0.05)

print(f"\n{'='*90}")
print(f"MULTIPLE TESTING CORRECTION: {len(findings)} findings, {n_tests} with valid p-values")
print(f"Bonferroni threshold: p < {bonf_threshold:.6f}")
print(f"BH-FDR threshold: q = 0.05")
print(f"{'='*90}")

families = {}
for idx, (fid, desc, dialect, family, k, n, p0, enr, pval) in enumerate(findings):
    families.setdefault(family, []).append((idx, fid, desc, dialect, k, n, p0, enr, pval,
                                             pval < bonf_threshold if pval is not None else False,
                                             bh_rejects[idx]))

# Print by family
all_survivors_bh = []
all_survivors_bonf = []

for family_name in ['positional', 'bigram', 'self-succession', 'dialect-split',
                    'cth-positional', 'suffix', 'word-level']:
    if family_name not in families:
        continue
    members = families[family_name]
    print(f"\n── FAMILY: {family_name.upper()} ({len(members)} findings) ──")
    print(f"{'ID':<5} {'Description':<42} {'D':>2} {'k':>5} {'n':>6} {'p0':>6} {'Enr':>7} "
          f"{'p-value':>10} {'Bonf':>6} {'BH':>4}")
    print("-"*100)
    for idx, fid, desc, dialect, k, n, p0, enr, pval, bonf_pass, bh_pass in members:
        pstr  = f"{pval:.2e}" if pval is not None else "N/A (n<10)"
        estr  = f"{enr:.3f}" if enr is not None else "N/A"
        bstr  = "YES" if bonf_pass else ("NO" if pval is not None else "---")
        bhstr = "YES" if bh_pass else ("NO" if pval is not None else "---")
        print(f"{fid:<5} {desc:<42} {dialect:>2} {k:>5} {n:>6} {p0:>6.4f} {estr:>7} "
              f"{pstr:>10} {bstr:>6} {bhstr:>4}")
        if bonf_pass: all_survivors_bonf.append((fid, desc, enr))
        if bh_pass:   all_survivors_bh.append((fid, desc, enr))

# ── BH within families ────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("BH-FDR WITHIN FAMILIES (q=0.05, then Bonferroni across families)")
print(f"{'='*70}")
family_survivors = {}
for family_name, members in families.items():
    fam_p = [f[8] for f in members]
    fam_bh = bh_correct(fam_p, q=0.05)
    survivors = [(members[i][1], members[i][2]) for i, r in enumerate(fam_bh) if r]
    family_survivors[family_name] = survivors
    has_any = len(survivors) > 0
    print(f"  {family_name}: {len(survivors)}/{len(members)} pass BH-within-family"
          f" → {survivors[:3]}")

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
print(f"Bonferroni survivors ({len(all_survivors_bonf)}/{len(findings)}):")
for fid, desc, enr in all_survivors_bonf:
    print(f"  {fid}: {desc} (enr={enr:.3f})")
print(f"\nBH-FDR survivors ({len(all_survivors_bh)}/{len(findings)}):")
for fid, desc, enr in all_survivors_bh:
    print(f"  {fid}: {desc} (enr={enr:.3f})")

# ── Effect sizes for underpowered findings ────────────────────────────────────
print(f"\nFindings with n < 10 (EXPLORATORY, no p-value):")
for fid, desc, dialect, family, k, n, p0, enr, pval in findings:
    if pval is None:
        print(f"  {fid}: {desc} (k={k}, n={n}, enr={enr})")

print("\nDone.")
