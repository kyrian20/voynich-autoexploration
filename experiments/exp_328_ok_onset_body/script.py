"""
exp_328: ok-Onset Body Structure — Bimodal B0 Distribution and A/B ok↔qok Coupling (H528)

Background:
- exp_321 (F323): ok-onset B0 = 'e'=43.5%, 'a'=43.3% — the ONLY major onset class with
  nearly equal bimodal B0. All others are unimodal: d='a'(73%), sh='e'(73%), ch='e'(60%),
  y=gallows(80%), s='a'(63%), qok='e'(48%).
- exp_324 (F326): A-dialect ok↔qok bidirectional coupling 2.03×/1.68× (absent in B: 1.16/0.96×)

Hypothesis: ok has TWO structural sub-classes:
  (a) ok+'e'-body words: okeedy, okeey (template-copying forms, like qok+'e' forms)
  (b) ok+'a'-body words: okaiin, okain, okar, okal (aiin-body doublets with d-onset)
  If confirmed, ok = compound onset class overlapping with both qok (template forms) and d/s (aiin forms)

Questions:
1. What are the top ok-onset word types? Partition by B0 ('e' vs 'a' vs other).
2. Are the B0='e' forms and B0='a' forms structurally distinct (different suffixes, lengths)?
3. A-dialect: how does the ok vocabulary differ? Does A-dialect ok 'e'/'a' balance shift?
4. Is the ok↔qok A-dialect coupling explained by specific ok-word types that precede qok-onset?
5. How does ok compare to ot-onset? (ot is a separate class — does it also show bimodal B0?)
"""
from pathlib import Path as _RepositoryPath

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
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

def folio_base(folio): return re.sub(r'[rv]$', '', folio)

def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

def parse_vms():
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

    mid_bigrams_by_dialect={'A':[],'B':[]}
    mid_words_by_dialect={'A':[],'B':[]}
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
            mid=words[1:-1]
            for w in mid:
                mid_words_by_dialect[dialect].append(w)
            for i in range(len(mid)-1):
                mid_bigrams_by_dialect[dialect].append((mid[i],mid[i+1]))
    return mid_bigrams_by_dialect, mid_words_by_dialect

print("Loading corpus...")
bigrams_by_d, words_by_d = parse_vms()
print(f"B MID words: {len(words_by_d['B'])}, A MID words: {len(words_by_d['A'])}")

def get_body(w, onset_len):
    """Return body of word after removing onset."""
    return w[onset_len:] if len(w) > onset_len else ''

def analyze_ok_body(words, bigrams, dialect, onset_label, onset_prefix):
    print(f"\n{'='*70}")
    print(f"{onset_label}-ONSET BODY STRUCTURE ({dialect})")
    print(f"{'='*70}")

    # Extract ok-onset MID words
    ok_words = [w for w in words if get_onset(w) == onset_label]
    onset_len = len(onset_prefix)
    print(f"\nTotal {onset_label}-onset MID tokens: {len(ok_words)}")

    # B0 distribution
    b0_counts = Counter()
    for w in ok_words:
        body = get_body(w, onset_len)
        b0 = body[0] if body else ''
        b0_counts[b0] += 1

    total = len(ok_words)
    print(f"\nB0 character distribution:")
    for char, cnt in b0_counts.most_common(10):
        print(f"  '{char}': {cnt} ({100*cnt/total:.1f}%)")

    # Partition by B0: 'e' vs 'a' vs other
    e_words = Counter(w for w in ok_words if len(get_body(w, onset_len)) > 0 and get_body(w, onset_len)[0] == 'e')
    a_words = Counter(w for w in ok_words if len(get_body(w, onset_len)) > 0 and get_body(w, onset_len)[0] == 'a')
    other_words = Counter(w for w in ok_words if len(get_body(w, onset_len)) > 0 and get_body(w, onset_len)[0] not in ('e', 'a'))

    n_e = sum(e_words.values())
    n_a = sum(a_words.values())
    n_other = sum(other_words.values())

    print(f"\nPartition: 'e'-body={n_e} ({100*n_e/total:.1f}%), 'a'-body={n_a} ({100*n_a/total:.1f}%), other={n_other} ({100*n_other/total:.1f}%)")

    # Top word types overall
    ok_type_counts = Counter(ok_words)
    print(f"\nTop-25 {onset_label}-onset word types (with B0 label):")
    print(f"{'word':<22} {'count':>6} {'%':>6} {'B0':>4}")
    cumsum = 0; n_types = len(ok_type_counts)
    cp90_count = 0
    for w, cnt in ok_type_counts.most_common(25):
        body = get_body(w, onset_len)
        b0 = body[0] if body else '?'
        cumsum += cnt
        pct = 100*cnt/total
        print(f"{w:<22} {cnt:>6} {pct:>6.1f}% {'['+b0+']':>4}")
    # Calculate CP90
    cumsum2 = 0
    for w, cnt in ok_type_counts.most_common():
        cumsum2 += cnt
        cp90_count += 1
        if cumsum2 >= 0.9 * total: break
    print(f"\nTotal unique types: {n_types}, CP90: {cp90_count} types for 90% of {total} tokens")

    # Show top 'e'-body and 'a'-body words separately
    print(f"\nTop 'e'-body words (B0='e'):")
    print(f"{'word':<22} {'count':>6} {'body':>10}")
    for w, cnt in e_words.most_common(15):
        body = get_body(w, onset_len)
        print(f"{w:<22} {cnt:>6}   {body}")

    print(f"\nTop 'a'-body words (B0='a'):")
    print(f"{'word':<22} {'count':>6} {'body':>10}")
    for w, cnt in a_words.most_common(15):
        body = get_body(w, onset_len)
        print(f"{w:<22} {cnt:>6}   {body}")

    return ok_type_counts, e_words, a_words

# ---- ok-onset analysis ----
b_ok_types, b_ok_e, b_ok_a = analyze_ok_body(words_by_d['B'], bigrams_by_d['B'], 'B', 'ok', 'ok')
a_ok_types, a_ok_e, a_ok_a = analyze_ok_body(words_by_d['A'], bigrams_by_d['A'], 'A', 'ok', 'ok')

# ---- ot-onset for comparison ----
b_ot_types, b_ot_e, b_ot_a = analyze_ok_body(words_by_d['B'], bigrams_by_d['B'], 'B', 'ot', 'ot')

# ---- ok↔qok bigram analysis for A-dialect ----
print(f"\n{'='*70}")
print(f"A-DIALECT ok↔qok COUPLING ANALYSIS")
print(f"{'='*70}")

def ok_qok_coupling(bigrams, words, dialect):
    """Analyze which ok-words most precede qok-words, and vice versa."""
    onset_counts = Counter(get_onset(w) for w in words)
    total = len(words)
    total_bigrams = len(bigrams)

    # ok→qok and qok→ok enrichment
    p_ok = onset_counts.get('ok', 0) / total
    p_qok = onset_counts.get('qok', 0) / total
    obs_ok_qok = sum(1 for w1,w2 in bigrams if get_onset(w1)=='ok' and get_onset(w2)=='qok')
    obs_qok_ok = sum(1 for w1,w2 in bigrams if get_onset(w1)=='qok' and get_onset(w2)=='ok')
    exp_ok_qok = p_ok * p_qok * total_bigrams
    exp_qok_ok = p_qok * p_ok * total_bigrams

    print(f"\n{dialect}: ok→qok: obs={obs_ok_qok}, exp={exp_ok_qok:.1f}, E={obs_ok_qok/exp_ok_qok:.3f}×")
    print(f"{dialect}: qok→ok: obs={obs_qok_ok}, exp={exp_qok_ok:.1f}, E={obs_qok_ok/exp_qok_ok:.3f}×")

    # Per-ok-word P(→qok)
    ok_word_total = Counter()
    ok_word_to_qok = Counter()
    for w1, w2 in bigrams:
        if get_onset(w1) == 'ok':
            ok_word_total[w1] += 1
            if get_onset(w2) == 'qok':
                ok_word_to_qok[w1] += 1

    class_rate = obs_ok_qok / sum(ok_word_total.values()) if ok_word_total else 0
    print(f"\nClass-level P(ok→qok) = {class_rate:.4f}")
    print(f"\nTop ok→qok transitions by count:")
    print(f"{'ok_word':<22} {'total':>6} {'→qok':>6} {'P(→qok)':>8}")
    for w in sorted(ok_word_total.keys(), key=lambda x: ok_word_to_qok.get(x,0), reverse=True)[:15]:
        t = ok_word_total[w]
        n = ok_word_to_qok.get(w, 0)
        p = n/t
        if t >= 2 or n >= 1:
            print(f"{w:<22} {t:>6} {n:>6} {p:>8.3f}")

    # Which qok-words follow ok?
    qok_after_ok = Counter()
    qok_total = Counter(w for w in words if get_onset(w) == 'qok')
    for w1, w2 in bigrams:
        if get_onset(w1) == 'ok' and get_onset(w2) == 'qok':
            qok_after_ok[w2] += 1
    print(f"\nqok-words following ok-onset:")
    for w, cnt in qok_after_ok.most_common(10):
        print(f"  {w}: {cnt} (global qok rank: {list(w for w,_ in qok_total.most_common()).index(w)+1 if w in qok_total else '?'})")

ok_qok_coupling(bigrams_by_d['A'], words_by_d['A'], 'A')
ok_qok_coupling(bigrams_by_d['B'], words_by_d['B'], 'B')

# ---- Cross-dialect ok comparison ----
print(f"\n{'='*70}")
print(f"CROSS-DIALECT ok-ONSET COMPARISON")
print(f"{'='*70}")

b_ok_set = set(b_ok_types.keys())
a_ok_set = set(a_ok_types.keys())
shared_ok = b_ok_set & a_ok_set
jaccard_ok = len(shared_ok) / len(b_ok_set | a_ok_set) if (b_ok_set | a_ok_set) else 0

print(f"\nB ok types: {len(b_ok_set)}, A ok types: {len(a_ok_set)}")
print(f"Shared: {len(shared_ok)}, Jaccard: {jaccard_ok:.3f}")
print(f"\nShared ok types (both dialects):")
shared_sorted = sorted(shared_ok, key=lambda w: -(b_ok_types.get(w,0)+a_ok_types.get(w,0)))
for w in shared_sorted[:20]:
    body_char = w[2:3] if len(w) > 2 else '?'
    print(f"  {w:<22} B={b_ok_types.get(w,0):4d} A={a_ok_types.get(w,0):4d} [B0='{body_char}']")

# ---- Comparison: ok vs qok vs d onset top words ----
print(f"\n{'='*70}")
print(f"STRUCTURAL COMPARISON: ok vs qok vs d (B-dialect, top 10)")
print(f"{'='*70}")

print("\nTop qok-onset words (for template comparison):")
qok_types = Counter(w for w in words_by_d['B'] if get_onset(w) == 'qok')
for w, cnt in qok_types.most_common(10):
    body = w[3:] if len(w) > 3 else ''  # qok = 3 chars
    b0 = body[0] if body else '?'
    print(f"  {w:<20} {cnt:>5} [B0='{b0}']")

print("\nTop d-onset words (for aiin-body comparison):")
d_types = Counter(w for w in words_by_d['B'] if get_onset(w) == 'd')
for w, cnt in d_types.most_common(10):
    body = w[1:] if len(w) > 1 else ''
    b0 = body[0] if body else '?'
    print(f"  {w:<20} {cnt:>5} [B0='{b0}']")
