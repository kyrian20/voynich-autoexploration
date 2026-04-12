"""
exp_329: ok+'e' vs ok+'a' MID Position Distribution (H532)

Background:
- exp_328 (F330): ok = compound onset class with two sub-classes:
  - ok+'e'-body (43%): template-copying forms (okeedy, okeey, okedy) = qok-'q' substitutes
  - ok+'a'-body (43%): aiin-doublets (okaiin, okain, okar, okal) = d-onset substitutes
- If ok is a genuine grammatical composite, the two sub-classes should occupy different
  positions within MID span: ok+'e' ~ qok positions, ok+'a' ~ d-onset positions

Questions:
1. For B-dialect MID words, compute per-onset-class mean MID position index
2. Partition ok words by B0 ('e' vs 'a'); compute mean position for each sub-class
3. Compare: ok+'e' vs qok, ok+'a' vs d-onset
4. Statistical test: is the positional difference between ok+'e' and ok+'a' significant?
5. Also test ot+'e' vs ot+'a' (ot is structurally isomorphic per F330)

MID position index: 0 = first MID word, n-1 = last MID word
Normalized position: position / (line_length - 3) where 3 = first + last + 1
Or: use raw index from start of MID (0 = just after LF word, n-1 = just before LL word)
"""

import os, re, math
from collections import Counter, defaultdict
import statistics

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def get_b0(w, onset_label):
    onset_lengths = {'qok':3,'qot':3,'qo':2,'cth':3,'ch':2,'sh':2,'ok':2,'ot':2,'ol':2,
                     'd':1,'s':1,'y':1,'k':1,'t':1,'l':1,'r':1,'p':1,'f':1,'o':1}
    l = onset_lengths.get(onset_label, 1)
    body = w[l:]
    return body[0] if body else ''

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def parse_vms_with_positions():
    """Parse VMS and return (word, onset, b0, mid_idx, mid_span, norm_pos, dialect) tuples."""
    folio_word_stats=defaultdict(lambda:{'total':0,'edy':0,'eedy':0})
    with open(DATA_PATH,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'): continue
            m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
            if not m: continue
            folio=m.group(1).lstrip('+*=&~'); fb=folio_base(folio)
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            for w in words:
                folio_word_stats[fb]['total']+=1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy']+=1
                elif w.endswith('edy'): folio_word_stats[fb]['edy']+=1
    folio_dialect={fb:classify_dialect(stats) for fb,stats in folio_word_stats.items()}

    records = []  # (word, onset, b0, mid_idx, mid_span, dialect)
    with open(DATA_PATH,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#'): continue
            m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
            if not m: continue
            folio_raw=m.group(1); locus_code=m.group(3)
            folio=folio_raw.lstrip('+*=&~'); fb=folio_base(folio)
            dialect=folio_dialect.get(fb,'unknown')
            if dialect not in ('A','B'): continue
            lc_stripped=locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text=re.sub(r'<[^>]+>','',line)
            words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
            if len(words)<3: continue
            mid = words[1:-1]
            mid_span = len(mid)
            for idx, w in enumerate(mid):
                onset = get_onset(w)
                b0 = get_b0(w, onset)
                # Normalized position: 0.0 = start of MID, 1.0 = end of MID
                norm_pos = idx / (mid_span - 1) if mid_span > 1 else 0.5
                records.append((w, onset, b0, idx, mid_span, norm_pos, dialect))

    return records

print("Loading corpus with positions...")
records = parse_vms_with_positions()
print(f"Total MID word instances: {len(records)}")

b_records = [(w, onset, b0, idx, span, npos) for w, onset, b0, idx, span, npos, d in records if d == 'B']
a_records = [(w, onset, b0, idx, span, npos) for w, onset, b0, idx, span, npos, d in records if d == 'A']
print(f"B MID instances: {len(b_records)}, A MID instances: {len(a_records)}")

def mean_sem(values):
    if not values: return float('nan'), float('nan')
    m = statistics.mean(values)
    if len(values) < 2: return m, float('nan')
    s = statistics.stdev(values)
    sem = s / math.sqrt(len(values))
    return m, sem

def analyze_positions(records, label):
    print(f"\n{'='*70}")
    print(f"MID POSITION ANALYSIS — {label}")
    print(f"{'='*70}")

    # Per-onset normalized position
    onset_positions = defaultdict(list)
    for w, onset, b0, idx, span, npos in records:
        onset_positions[onset].append(npos)

    print(f"\n{'Onset class':<12} {'N':>6} {'mean_pos':>10} {'SEM':>8} {'median':>8}")
    print("-"*50)
    for onset in ['qok', 'ch', 'sh', 'ok', 'ot', 'd', 'y', 's']:
        pos = onset_positions[onset]
        m, sem = mean_sem(pos)
        med = statistics.median(pos) if pos else float('nan')
        print(f"{onset:<12} {len(pos):>6} {m:>10.4f} {sem:>8.4f} {med:>8.4f}")

    # ok and ot partitioned by B0
    print(f"\n--- ok sub-class position analysis ---")
    for onset_label, prefix_len in [('ok', 2), ('ot', 2)]:
        e_pos = [npos for w, onset, b0, idx, span, npos in records if onset == onset_label and b0 == 'e']
        a_pos = [npos for w, onset, b0, idx, span, npos in records if onset == onset_label and b0 == 'a']
        c_pos = [npos for w, onset, b0, idx, span, npos in records if onset == onset_label and b0 not in ('e','a')]

        m_e, sem_e = mean_sem(e_pos)
        m_a, sem_a = mean_sem(a_pos)

        # Get qok and d positions for comparison
        qok_pos = onset_positions.get('qok', [])
        d_pos = onset_positions.get('d', [])
        m_qok = statistics.mean(qok_pos) if qok_pos else float('nan')
        m_d = statistics.mean(d_pos) if d_pos else float('nan')

        print(f"\n{onset_label}-onset B0 partition:")
        print(f"  {onset_label}+'e' (N={len(e_pos)}): mean_pos={m_e:.4f} ± {sem_e:.4f}")
        print(f"  {onset_label}+'a' (N={len(a_pos)}): mean_pos={m_a:.4f} ± {sem_a:.4f}")
        print(f"  {onset_label}+'other' (N={len(c_pos)})")
        print(f"  qok  (N={len(qok_pos)}): mean_pos={m_qok:.4f} (reference for 'e')")
        print(f"  d    (N={len(d_pos)}): mean_pos={m_d:.4f} (reference for 'a')")

        if m_e != float('nan') and m_a != float('nan'):
            diff = m_a - m_e
            diff_sigma = abs(diff) / (sem_e**2 + sem_a**2)**0.5 if (sem_e > 0 and sem_a > 0) else float('nan')
            print(f"\n  ok+'a' - ok+'e' = {diff:+.4f} (expected positive if 'a' is later)")
            print(f"  z-score: {diff_sigma:.2f}σ")
            if diff > 0.02:
                print(f"  → ok+'a' appears LATER in MID span than ok+'e'")
            elif diff < -0.02:
                print(f"  → ok+'a' appears EARLIER in MID span than ok+'e'")
            else:
                print(f"  → No significant positional difference between ok+'e' and ok+'a'")

    # Position distribution histograms (crude)
    print(f"\n--- Normalized position histogram (B-dialect) ---")
    BINS = 4
    bin_labels = ['0.0-0.25 (early)', '0.25-0.5 (mid-early)', '0.5-0.75 (mid-late)', '0.75-1.0 (late)']
    for onset, b0_filter, label in [
        ('qok', None, 'qok (all)'),
        ('ok', 'e', "ok+'e'"),
        ('ok', 'a', "ok+'a'"),
        ('ok', None, 'ok (all)'),
        ('ot', 'e', "ot+'e'"),
        ('ot', 'a', "ot+'a'"),
        ('d', None, 'd (all)'),
        ('ch', None, 'ch (all)'),
        ('sh', None, 'sh (all)'),
    ]:
        if b0_filter:
            pos_list = [npos for w, o, b0, idx, span, npos in records if o == onset and b0 == b0_filter]
        else:
            pos_list = [npos for w, o, b0, idx, span, npos in records if o == onset]

        if not pos_list: continue
        n = len(pos_list)
        bins = [0]*BINS
        for p in pos_list:
            b = min(int(p * BINS), BINS-1)
            bins[b] += 1
        pcts = [100*b/n for b in bins]
        hist = ' | '.join(f"{p:5.1f}%" for p in pcts)
        print(f"  {label:<18} N={n:>5}: [{hist}]")

analyze_positions(b_records, "B-DIALECT")
analyze_positions(a_records, "A-DIALECT")

# ---- Cross-class comparison: do ok+'a' and d-onset have similar position distributions? ----
print(f"\n{'='*70}")
print("CROSS-CLASS STRUCTURAL COMPARISON")
print(f"{'='*70}")

print("\nExpected if ok is a compound class:")
print("  ok+'e' ≈ qok position distribution")
print("  ok+'a' ≈ d-onset position distribution")
print("  ok (all) ≈ between qok and d")

b_positions = {onset: [npos for w, o, b0, idx, span, npos in b_records if o == onset]
               for onset in ['qok','ch','sh','ok','ot','d','y','s']}
ok_e_pos = [npos for w, o, b0, idx, span, npos in b_records if o == 'ok' and b0 == 'e']
ok_a_pos = [npos for w, o, b0, idx, span, npos in b_records if o == 'ok' and b0 == 'a']

def pos_summary(pos_list):
    if not pos_list: return 'N/A'
    m = statistics.mean(pos_list)
    q1 = statistics.quantiles(pos_list, n=4)[0]
    q3 = statistics.quantiles(pos_list, n=4)[2]
    return f"mean={m:.3f} [Q1={q1:.3f}, Q3={q3:.3f}]"

print(f"\nB-dialect position summaries:")
print(f"  qok:    {pos_summary(b_positions['qok'])}")
print(f"  ok+'e': {pos_summary(ok_e_pos)}")
print(f"  ok+'a': {pos_summary(ok_a_pos)}")
print(f"  d:      {pos_summary(b_positions['d'])}")
print(f"  ch:     {pos_summary(b_positions['ch'])}")
print(f"  sh:     {pos_summary(b_positions['sh'])}")
print(f"  y:      {pos_summary(b_positions['y'])}")
