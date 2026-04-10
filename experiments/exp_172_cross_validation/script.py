#!/usr/bin/env python3
"""
exp_172: Cross-validation of robust findings.
Three splits:
1. Random 80/20 stratified by dialect (baseline check)
2. Leave-one-section-out within A-dialect
3. Leave-one-section-out within B-dialect

For each split, recompute top 20 findings on train, test on held-out.
Report: train estimate, test estimate, ratio (test/train), PASS (≥50% magnitude) / FAIL.
"""
import re, random, math
from collections import Counter, defaultdict

VMS_CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'
RANDOM_SEED = 42

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
folio_to_section = {}
for sec, folios in SECTION_RANGES.items():
    for fn in folios:
        folio_to_section[fn] = sec

def get_slot(i, n):
    if n == 1: return 'only'
    if i == 0: return 'LF'
    if i == n-1: return 'LL'
    if i == 1: return 'second'
    return 'MID'

# ── Parse VMS ─────────────────────────────────────────────────────────────────
def parse_vms(path):
    folio_words = defaultdict(list)
    raw_lines = []  # (fnum, words, section)
    with open(path) as f:
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
            sec = folio_to_section.get(fnum, 'other')
            raw_lines.append((fnum, words, sec))
    return folio_words, raw_lines

print("Parsing VMS...")
folio_words, raw_lines = parse_vms(VMS_CORPUS)

folio_dialect = {}
for fn, wds in folio_words.items():
    if len(wds) < 10: continue
    rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'

# Add dialect to raw_lines
all_lines = [(fn, wds, sec, folio_dialect.get(fn, 'unknown')) for fn, wds, sec in raw_lines]
a_lines = [(fn, wds, sec) for fn, wds, sec, d in all_lines if d == 'A']
b_lines = [(fn, wds, sec) for fn, wds, sec, d in all_lines if d == 'B']

print(f"A-dialect: {len(a_lines)} lines, B-dialect: {len(b_lines)} lines")

# ── Compute the top-20 robust findings on a set of lines ──────────────────────
def compute_findings(lines):
    """
    Compute all top-20 findings. Lines is a list of (fn, wds, sec).
    Returns dict of finding_name -> value.
    """
    if not lines:
        return {}

    wds_all = [w for _, wds, _ in lines for w in wds]
    n = len(wds_all)
    if n == 0:
        return {}

    onset_counts = Counter(get_onset(w) for w in wds_all)
    line_words = [wds for _, wds, _ in lines]

    # Positional slot words
    lf_words = [wds[0] for wds in line_words if wds]
    ll_words  = [wds[-1] for wds in line_words if wds]
    n_lf = len(lf_words)
    n_ll = len(ll_words)

    results = {}

    def enrich(numerator_rate, baseline_rate):
        return numerator_rate / baseline_rate if baseline_rate > 0 else None

    # F1: y-onset LF enrichment (F098/F159)
    y_rate = onset_counts.get('y', 0) / n
    y_at_lf = sum(1 for w in lf_words if get_onset(w) == 'y') / n_lf if n_lf else 0
    results['y_lf_enrichment'] = enrich(y_at_lf, y_rate)

    # F2: cth LF depletion in A (expect ~0.15x) / near-baseline in B
    cth_rate = onset_counts.get('cth', 0) / n
    cth_at_lf = sum(1 for w in lf_words if get_onset(w) == 'cth') / n_lf if n_lf else 0
    results['cth_lf_enrichment'] = enrich(cth_at_lf, cth_rate)

    # F3: -am LL enrichment (F087)
    am_rate = sum(1 for w in wds_all if w.endswith('am')) / n
    am_at_ll = sum(1 for w in ll_words if w.endswith('am')) / n_ll if n_ll else 0
    results['am_ll_enrichment'] = enrich(am_at_ll, am_rate)

    # F4: daiin→cth bigram enrichment
    dai_bg, dai_cth = 0, 0
    for wds in line_words:
        for i in range(len(wds)-1):
            if wds[i] == 'daiin':
                dai_bg += 1
                if get_onset(wds[i+1]) == 'cth':
                    dai_cth += 1
    results['daiin_cth_enrichment'] = (dai_cth / dai_bg) / cth_rate if dai_bg > 0 and cth_rate > 0 else 0

    # F5: daiin→y bigram enrichment (known ~3-4×)
    dai_y = 0
    y_at_pos = onset_counts.get('y', 0) / n
    for wds in line_words:
        for i in range(len(wds)-1):
            if wds[i] == 'daiin' and get_onset(wds[i+1]) == 'y':
                dai_y += 1
    results['daiin_y_enrichment'] = (dai_y / dai_bg) / y_rate if dai_bg > 0 and y_rate > 0 else 0

    # F6: qok→ch enrichment (B sequential grammar)
    qok_bg, qok_ch = 0, 0
    ch_rate = (onset_counts.get('ch', 0) + onset_counts.get('ch_e', 0)) / n
    for wds in line_words:
        for i in range(len(wds)-1):
            if get_onset(wds[i]) == 'qok':
                qok_bg += 1
                if get_onset(wds[i+1]) in ('ch', 'ch_e'):
                    qok_ch += 1
    results['qok_ch_enrichment'] = (qok_ch / qok_bg) / ch_rate if qok_bg > 0 and ch_rate > 0 else 0

    # F7-F10: onset self-succession enrichments
    for cls in ['qok', 'ok', 'ch', 'd']:
        bg, ss = 0, 0
        cls_rate = onset_counts.get(cls, 0) / n
        for wds in line_words:
            for i in range(len(wds)-1):
                if get_onset(wds[i]) == cls:
                    bg += 1
                    if get_onset(wds[i+1]) == cls:
                        ss += 1
        results[f'{cls}_self_succ'] = (ss / bg) / cls_rate if bg > 0 and cls_rate > 0 else 0

    # F11: edy rate
    results['edy_rate'] = sum(1 for w in wds_all if 'edy' in w or 'eedy' in w) / n

    # F12: edy/ol ratio
    edy_c = sum(1 for w in wds_all if 'edy' in w)
    ol_c  = sum(1 for w in wds_all if w.endswith('ol'))
    results['edy_ol_ratio'] = edy_c / ol_c if ol_c > 0 else None

    # F13: sh LF enrichment
    sh_rate = onset_counts.get('sh', 0) / n
    sh_at_lf = sum(1 for w in lf_words if get_onset(w) == 'sh') / n_lf if n_lf else 0
    results['sh_lf_enrichment'] = enrich(sh_at_lf, sh_rate)

    # F14: d LL enrichment
    d_rate = onset_counts.get('d', 0) / n
    d_at_ll = sum(1 for w in ll_words if get_onset(w) == 'd') / n_ll if n_ll else 0
    results['d_ll_enrichment'] = enrich(d_at_ll, d_rate)

    # F15: qok LF enrichment (depleted in B)
    qok_rate = onset_counts.get('qok', 0) / n
    qok_at_lf = sum(1 for w in lf_words if get_onset(w) == 'qok') / n_lf if n_lf else 0
    results['qok_lf_enrichment'] = enrich(qok_at_lf, qok_rate)

    # F16: l-onset rate
    results['l_onset_rate'] = onset_counts.get('l', 0) / n

    # F17: [ch][daiin]→cth enrichment (5.89×)
    ch_dai_bg, ch_dai_cth = 0, 0
    for wds in line_words:
        for i in range(len(wds)-2):
            if get_onset(wds[i]) == 'ch' and wds[i+1] == 'daiin':
                ch_dai_bg += 1
                if get_onset(wds[i+2]) == 'cth':
                    ch_dai_cth += 1
    results['ch_daiin_cth_enrichment'] = (ch_dai_cth / ch_dai_bg) / cth_rate if ch_dai_bg > 0 and cth_rate > 0 else 0

    # F18: qo self-succession (known 2.05× in B, 1.31× in A)
    qo_bg, qo_ss = 0, 0
    qo_rate = onset_counts.get('qo', 0) / n
    for wds in line_words:
        for i in range(len(wds)-1):
            if get_onset(wds[i]) == 'qo':
                qo_bg += 1
                if get_onset(wds[i+1]) == 'qo':
                    qo_ss += 1
    results['qo_self_succ'] = (qo_ss / qo_bg) / qo_rate if qo_bg > 0 and qo_rate > 0 else 0

    # F19: daiin rate (B-dialect should have daiin ~10-15% of all words in B?)
    results['daiin_rate'] = sum(1 for w in wds_all if w == 'daiin') / n

    # F20: n_tokens (to verify splits have adequate data)
    results['n_tokens'] = n

    return results

# ── SPLIT 1: Random 80/20 stratified by dialect ───────────────────────────────
print("\n" + "="*70)
print("SPLIT 1: RANDOM 80/20 STRATIFIED BY DIALECT")
print("="*70)

random.seed(RANDOM_SEED)
folios_a = list(set(fn for fn, _, _ in a_lines))
folios_b = list(set(fn for fn, _, _ in b_lines))
random.shuffle(folios_a)
random.shuffle(folios_b)

# 80% train folios
train_a_folios = set(folios_a[:int(0.8*len(folios_a))])
train_b_folios = set(folios_b[:int(0.8*len(folios_b))])
test_a_folios  = set(folios_a[int(0.8*len(folios_a)):])
test_b_folios  = set(folios_b[int(0.8*len(folios_b)):])

train_a = [(fn, wds, sec) for fn, wds, sec in a_lines if fn in train_a_folios]
test_a  = [(fn, wds, sec) for fn, wds, sec in a_lines if fn in test_a_folios]
train_b = [(fn, wds, sec) for fn, wds, sec in b_lines if fn in train_b_folios]
test_b  = [(fn, wds, sec) for fn, wds, sec in b_lines if fn in test_b_folios]

print(f"A-dialect: train={len(train_a)} lines ({len(train_a_folios)} folios), "
      f"test={len(test_a)} lines ({len(test_a_folios)} folios)")
print(f"B-dialect: train={len(train_b)} lines ({len(train_b_folios)} folios), "
      f"test={len(test_b)} lines ({len(test_b_folios)} folios)")

def compare_splits(train_set, test_set, dialect_label, split_label):
    train_m = compute_findings(train_set)
    test_m  = compute_findings(test_set)

    print(f"\n--- {dialect_label} | {split_label} ---")
    print(f"{'Finding':<35} {'Train':>8} {'Test':>8} {'Ratio':>7} {'Result':>7}")
    print("-"*65)
    results = {}
    for k in sorted(train_m.keys()):
        if k == 'n_tokens': continue
        tv = train_m.get(k)
        hv = test_m.get(k)
        if tv is None or hv is None or tv == 0:
            ratio = None
            result = 'N/A'
        else:
            ratio = hv / tv
            # PASS if test magnitude is at least 50% of train magnitude
            # For enrichments > 1: test ≥ 0.5 × (train-1) + 1 above-baseline part
            # Simple criterion: ratio ≥ 0.5 and same direction as train
            if tv > 1:
                result = 'PASS' if hv > 1 and ratio >= 0.5 else 'FAIL'
            elif tv < 1:
                result = 'PASS' if hv < 1 and ratio <= 1.5 else 'FAIL'
            else:
                result = 'PASS' if 0.5 <= ratio <= 2.0 else 'FAIL'
        results[k] = (tv, hv, ratio, result)
        tv_str = f"{tv:.3f}" if tv is not None else "N/A"
        hv_str = f"{hv:.3f}" if hv is not None else "N/A"
        r_str  = f"{ratio:.3f}" if ratio is not None else "N/A"
        print(f"  {k:<33} {tv_str:>8} {hv_str:>8} {r_str:>7} {result:>7}")

    pass_count = sum(1 for _, _, _, r in results.values() if r == 'PASS')
    fail_count = sum(1 for _, _, _, r in results.values() if r == 'FAIL')
    na_count   = sum(1 for _, _, _, r in results.values() if r == 'N/A')
    print(f"\n  → PASS: {pass_count}, FAIL: {fail_count}, N/A: {na_count} of {len(results)} findings")
    return results

split1_a = compare_splits(train_a, test_a, "A-dialect", "Random 80/20")
split1_b = compare_splits(train_b, test_b, "B-dialect", "Random 80/20")

# ── SPLIT 2: Leave-one-section-out within A-dialect ───────────────────────────
print("\n" + "="*70)
print("SPLIT 2: LEAVE-ONE-SECTION-OUT WITHIN A-DIALECT")
print("="*70)

# A-dialect sections: herbal, pharma, cosmo (astro has very few A-dialect lines)
a_sections = {}
for fn, wds, sec in a_lines:
    a_sections.setdefault(sec, []).append((fn, wds, sec))

print(f"A-dialect sections: {[(s, len(v)) for s, v in a_sections.items()]}")

for test_sec in ['herbal', 'pharma', 'cosmo']:
    if test_sec not in a_sections:
        continue
    test_set  = a_sections[test_sec]
    train_set = [(fn, wds, sec) for fn, wds, sec in a_lines if sec != test_sec]
    print(f"\n--- A-dialect: train on NOT-{test_sec} ({len(train_set)} lines), "
          f"test on {test_sec} ({len(test_set)} lines) ---")
    _ = compare_splits(train_set, test_set, f"A-dialect LOSO ({test_sec})", f"leave-{test_sec}-out")

# ── SPLIT 3: Leave-one-section-out within B-dialect ───────────────────────────
print("\n" + "="*70)
print("SPLIT 3: LEAVE-ONE-SECTION-OUT WITHIN B-DIALECT")
print("="*70)

b_sections = {}
for fn, wds, sec in b_lines:
    b_sections.setdefault(sec, []).append((fn, wds, sec))

print(f"B-dialect sections: {[(s, len(v)) for s, v in b_sections.items()]}")

for test_sec in ['bio', 'stars', 'herbal']:
    if test_sec not in b_sections:
        continue
    test_set  = b_sections[test_sec]
    train_set = [(fn, wds, sec) for fn, wds, sec in b_lines if sec != test_sec]
    print(f"\n--- B-dialect: train on NOT-{test_sec} ({len(train_set)} lines), "
          f"test on {test_sec} ({len(test_set)} lines) ---")
    _ = compare_splits(train_set, test_set, f"B-dialect LOSO ({test_sec})", f"leave-{test_sec}-out")

print("\n\nDone.")
