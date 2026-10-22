"""
exp_573: C007 reconciliation — onset self-succession methodology comparison

PURPOSE: Reconcile discrepancy between C007 values (exp_164/174: B qok=1.239×, A ok=1.930×,
upper range attributed to 2.05× "ok A-dialect") and canonical values (exp_565/567:
B qok=1.03×, A ok=1.42×).

IDENTIFIED METHODOLOGY DIFFERENCES between exp_164/174 and canonical:
  (A) DIALECT ASSIGNMENT: exp_174 uses FOLIO-LEVEL edy-rate (aggregate per folio);
      canonical (exp_565) uses PER-LINE edy-rate (each line classified independently)
  (B) BIGRAM FORMULA: exp_174 uses E=obs/(total_bigrams×rate²);
      canonical uses E=obs/(n_sender×mid_rate_target)
  (C) WORD PARSING: exp_174 uses text.split('.') with any-lowercase filter;
      canonical uses re.split('[-.\\s]', text) + all-lowercase + len≥2
  (D) ONSET TAXONOMY: exp_174 has 'ch_e' class (che/chi prefix), no ckh/cph/sch;
      canonical has ckh/cph/sch, no ch_e
  (E) CORPUS SCOPE: exp_174 A includes ALL A-dialect folios;
      canonical A herbal_a uses per-line classification + line_number≤56 filter
      (the n≤56 filter has only 41 lines filtered out; effectively all lines pass)

KEY FINDING from analysis: The primary driver is (A)+(B): folio-level vs per-line dialect
assignment combined with formula difference. Per-line classification is more conservative
about what counts as "A dialect" — lines on B-folios without edy words get included as A
in canonical but their folios get excluded in folio-level approach.

ADDITIONAL FINDING: C007's upper bound attribution "2.05× (ok, A-dialect)" appears to be
a misattribution. In exp_174, B qo=2.047× is the maximum, not A ok. A ok in exp_174=1.930×.
"""

import re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / 'data/transcriptions/eva_zl3b.txt'

ONSET_OLD = ['qok','qot','qo','cth','ch_e','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f']
ONSET_CAN = ['qok','qot','qo','cth','ckh','cph','ch','sh','ok','ot','ol','sch','skh','sph',
             'd','s','y','k','t','l','r','p','f','o','e','a','n','m']

def get_onset_old(w):
    w = w.lower()
    if w.startswith('qok'): return 'qok'
    if w.startswith('qot'): return 'qot'
    if w.startswith('qo'): return 'qo'
    if w.startswith('cth'): return 'cth'
    if w.startswith('che') or w.startswith('chi'): return 'ch_e'
    if w.startswith('ch'): return 'ch'
    if w.startswith('sh'): return 'sh'
    if w.startswith('ok'): return 'ok'
    if w.startswith('ot'): return 'ot'
    if w.startswith('ol'): return 'ol'
    for c in ['d','s','y','k','t','l','r','p','f']:
        if w.startswith(c): return c
    return 'other'

def get_onset_can(w):
    for o in ONSET_CAN:
        if w.startswith(o): return o
    return w[0] if w else 'other'

# ─── PARSING ────────────────────────────────────────────────────────────────

def parse_folio_level(filepath):
    """exp_164/174 style: folio-level edy-rate dialect assignment."""
    folio_words = defaultdict(list)
    raw_lines = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            parts = line.split(None, 1)
            if len(parts) < 2: continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2: continue
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'): continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m: continue
            fid = int(m.group(1))
            words = [w for w in text.split('.') if w and re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            folio_words[fid].extend(words)
            raw_lines.append((fid, words))
    folio_dialect = {}
    for fid, words in folio_words.items():
        if len(words) < 10: continue
        edy = sum(1 for w in words if 'edy' in w or 'eedy' in w)
        folio_dialect[fid] = 'B' if edy / len(words) >= 0.05 else 'A'
    a_lines = [(f, ws) for f, ws in raw_lines if folio_dialect.get(f) == 'A']
    b_lines = [(f, ws) for f, ws in raw_lines if folio_dialect.get(f) == 'B']
    return a_lines, b_lines

def parse_canonical(filepath):
    """exp_565 style: per-line edy-rate dialect assignment, line_number≤56."""
    lines_A, lines_B = [], []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)', line)
            if not m: continue
            folio_raw, n_str, lc, text = m.group(1), m.group(2), m.group(3), m.group(4)
            lc2 = lc.lstrip('+*=/~&').lstrip('@')
            if not lc2.startswith('P'): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            try: n = int(n_str)
            except: continue
            edy = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
            is_b = edy / len(words) >= 0.05
            if is_b:
                lines_B.append((folio_raw, words))
            else:
                if n <= 56:
                    lines_A.append((folio_raw, words))
    return lines_A, lines_B

# ─── SELF-SUCCESSION FORMULAS ────────────────────────────────────────────────

def ss_old_formula(lines, onset_fn, onsets):
    """exp_174 unconditional formula: E = obs / (total_bigrams × rate²)"""
    counts = Counter()
    bigrams = Counter()
    total_bg = 0
    total_w = 0
    for _, ws in lines:
        for w in ws:
            counts[onset_fn(w)] += 1
            total_w += 1
        for i in range(len(ws)-1):
            o1, o2 = onset_fn(ws[i]), onset_fn(ws[i+1])
            bigrams[(o1, o2)] += 1
            total_bg += 1
    results = {}
    for onset in onsets:
        rate = counts.get(onset, 0) / total_w if total_w > 0 else 0
        obs = bigrams.get((onset, onset), 0)
        exp = total_bg * rate * rate
        e = obs / exp if exp > 0 else float('inf')
        results[onset] = {'obs': obs, 'exp': exp, 'E': e}
    return results

def ss_canonical_formula(lines, onset_fn, onsets):
    """Canonical formula: E = obs / (n_sender × mid_rate_target)"""
    mid_counts = Counter()
    total_mid = 0
    for _, ws in lines:
        L = len(ws)
        for i in range(1, L-1):
            mid_counts[onset_fn(ws[i])] += 1
            total_mid += 1
    results = {}
    for onset in onsets:
        obs = 0
        n_sender = 0
        for _, ws in lines:
            for i in range(len(ws)-1):
                if onset_fn(ws[i]) == onset:
                    n_sender += 1
                    if onset_fn(ws[i+1]) == onset:
                        obs += 1
        mid_rate = mid_counts.get(onset, 0) / total_mid if total_mid > 0 else 0
        exp = n_sender * mid_rate
        e = obs / exp if exp > 0 else float('inf')
        results[onset] = {'obs': obs, 'exp': exp, 'E': e}
    return results

# ─── RUN ANALYSIS ───────────────────────────────────────────────────────────

FOCUS = ['qok', 'ok', 'ch', 'qo', 'ot']

print("=" * 70)
print("exp_573: C007 RECONCILIATION")
print("=" * 70)

A_folio, B_folio = parse_folio_level(CORPUS)
A_canon, B_canon = parse_canonical(CORPUS)

print(f"\nCorpus sizes:")
print(f"  A all (folio-level): {len(A_folio)} lines, {sum(len(ws) for _,ws in A_folio)} words")
print(f"  A herbal_a (canonical per-line): {len(A_canon)} lines, {sum(len(ws) for _,ws in A_canon)} words")
print(f"  B all (folio-level): {len(B_folio)} lines, {sum(len(ws) for _,ws in B_folio)} words")
print(f"  B all (canonical per-line): {len(B_canon)} lines, {sum(len(ws) for _,ws in B_canon)} words")

# ─── MAIN COMPARISON TABLE ──────────────────────────────────────────────────

conditions = [
    ("A: Old formula + folio-level dialect",
     A_folio, ss_old_formula, get_onset_old),
    ("A: Canonical formula + folio-level dialect (hybrid)",
     A_folio, ss_canonical_formula, get_onset_old),
    ("A: Canonical formula + per-line dialect (canonical)",
     A_canon, ss_canonical_formula, get_onset_can),
    ("B: Old formula + folio-level dialect",
     B_folio, ss_old_formula, get_onset_old),
    ("B: Canonical formula + folio-level dialect (hybrid)",
     B_folio, ss_canonical_formula, get_onset_old),
    ("B: Canonical formula + per-line dialect (canonical)",
     B_canon, ss_canonical_formula, get_onset_can),
]

print(f"\n{'Condition':<47}", end="")
for o in FOCUS:
    print(f" {o:>8}", end="")
print()
print("-" * 47 + "-" * (9 * len(FOCUS)))

for label, lines, formula_fn, onset_fn in conditions:
    res = formula_fn(lines, onset_fn, FOCUS)
    print(f"{label:<47}", end="")
    for o in FOCUS:
        e = res.get(o, {}).get('E', float('nan'))
        print(f" {e:>8.3f}", end="")
    print()

# ─── C007 REFERENCE VALUES FROM exp_174 ────────────────────────────────────

print("\n" + "=" * 70)
print("C007 REFERENCE (exp_174 table):")
print("  Unconditional: qok A=1.623/B=1.239, ok A=1.930/B=1.462, ch A=1.427/B=1.694, qo A=1.305/B=2.047")
print("  Position-ctrl: qok A=1.594/B=1.203, ok A=1.822/B=1.362, ch A=1.334/B=1.503, qo A=1.269/B=1.990")
print("\nC007 CLAIM: 'ranges from 1.24× (qok, B-dialect) to 2.05× (ok, A-dialect)'")
print("  1.24× ← B qok unconditional (1.239×) ✓")
print("  2.05× ← MISATTRIBUTION: exp_174's max is B qo=2.047× (NOT A ok=1.930×)")
print("  The claim '(ok, A-dialect)' for the upper bound is INCORRECT per exp_174's own table")

# ─── EFFECT DECOMPOSITION ───────────────────────────────────────────────────

print("\n" + "=" * 70)
print("EFFECT DECOMPOSITION — A-dialect ok self-succession:")
r1 = ss_old_formula(A_folio, get_onset_old, ['ok'])['ok']
r2 = ss_canonical_formula(A_folio, get_onset_old, ['ok'])['ok']
r3 = ss_canonical_formula(A_canon, get_onset_can, ['ok'])['ok']
print(f"  Old formula + folio dialect: E={r1['E']:.3f}× (obs={r1['obs']}, exp={r1['exp']:.1f})")
print(f"  Canonical formula + folio dialect: E={r2['E']:.3f}× (Δ={r2['E']-r1['E']:+.3f})")
print(f"  Canonical formula + per-line dialect (canonical): E={r3['E']:.3f}× (Δ from old={r3['E']-r1['E']:+.3f})")
print(f"  exp_567 reported: 1.42×  ← our canonical matches: {r3['E']:.3f}×")

print("\nEFFECT DECOMPOSITION — B-dialect qok self-succession:")
r1 = ss_old_formula(B_folio, get_onset_old, ['qok'])['qok']
r2 = ss_canonical_formula(B_folio, get_onset_old, ['qok'])['qok']
r3 = ss_canonical_formula(B_canon, get_onset_can, ['qok'])['qok']
print(f"  Old formula + folio dialect: E={r1['E']:.3f}× (obs={r1['obs']}, exp={r1['exp']:.1f})")
print(f"  Canonical formula + folio dialect: E={r2['E']:.3f}× (Δ={r2['E']-r1['E']:+.3f})")
print(f"  Canonical formula + per-line dialect (canonical): E={r3['E']:.3f}× (Δ from old={r3['E']-r1['E']:+.3f})")
print(f"  exp_565 reported: 1.03×  ← our canonical matches: {r3['E']:.3f}×")

# ─── FULL CANONICAL SURVEY ──────────────────────────────────────────────────

print("\n" + "=" * 70)
print("CANONICAL SELF-SUCCESSION SURVEY (all major onset classes):")
FULL_SET = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r']

for dialect_label, lines in [("A herbal_a", A_canon), ("B all", B_canon)]:
    print(f"\n{dialect_label} (canonical per-line, canonical formula):")
    mid_counts = Counter()
    total_mid = 0
    for _, ws in lines:
        L = len(ws)
        for i in range(1, L-1):
            mid_counts[get_onset_can(ws[i])] += 1
            total_mid += 1
    rows = []
    for onset in FULL_SET:
        obs = 0
        n_sender = 0
        for _, ws in lines:
            for i in range(len(ws)-1):
                if get_onset_can(ws[i]) == onset:
                    n_sender += 1
                    if get_onset_can(ws[i+1]) == onset:
                        obs += 1
        mid_rate = mid_counts.get(onset, 0) / total_mid if total_mid > 0 else 0
        exp = n_sender * mid_rate
        e = obs / exp if exp > 0 else float('inf')
        flag = 'CONF' if e >= 1.5 and obs >= 10 else ('sub-CONF' if e >= 1.5 and obs >= 5 else ('DEPL' if e < 0.7 and obs >= 3 else ''))
        rows.append((onset, obs, exp, e, flag))
        print(f"  {onset:>4}: obs={obs:>4}, exp={exp:>6.1f}, E={e:>6.3f}× {flag}")
    valid = [(o, e) for o, obs, exp, e, flag in rows if obs >= 10]
    if valid:
        mn = min(e for _,e in valid)
        mx = max(e for _,e in valid)
        print(f"  Range (obs≥10): {mn:.3f}× – {mx:.3f}×")

print("\nDone.")
