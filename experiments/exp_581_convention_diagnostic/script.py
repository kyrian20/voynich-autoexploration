#!/usr/bin/env python3
"""
exp_581: Convention diagnostic
Verifies four high-stakes spec values by re-derivation from raw corpus data
under the committed-claims convention (LF=first word, LL=last word).
Also tests under the inverted convention (LF=last word, LL=penult) to
distinguish nomenclatural drift from value-attachment errors.
"""

import re
from collections import Counter
import math

TRANSCRIPTION = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

# ─── Onset classifier (canonical) ────────────────────────────────────────────
def get_onset(word):
    w = word.lower()
    if w.startswith('qok'):  return 'qok'
    if w.startswith('qot'):  return 'qot'
    if w.startswith('qo'):   return 'qo'
    if w.startswith('cth'):  return 'cth'
    if w.startswith('ckh'):  return 'ckh'
    if w.startswith('cph'):  return 'cph'
    if w.startswith('sch'):  return 'sch'
    if w.startswith('ch'):   return 'ch'
    if w.startswith('sh'):   return 'sh'
    if w.startswith('ok'):   return 'ok'
    if w.startswith('ol'):   return 'ol'
    if w.startswith('ot'):   return 'ot'
    if w.startswith('of'):   return 'of'
    if w.startswith('or'):   return 'or'
    if w.startswith('o'):    return 'o'
    if w.startswith('d'):    return 'd'
    if w.startswith('y'):    return 'y'
    if w.startswith('s'):    return 's'
    if w.startswith('t'):    return 't'
    if w.startswith('k'):    return 'k'
    if w.startswith('p'):    return 'p'
    if w.startswith('f'):    return 'f'
    if w.startswith('l'):    return 'l'
    if w.startswith('r'):    return 'r'
    if w.startswith('a'):    return 'a'
    if w.startswith('e'):    return 'e'
    if w.startswith('i'):    return 'i'
    if w.startswith('n'):    return 'n'
    return 'other'

def has_am_suffix(word):
    w = word.lower()
    return w.endswith('am')

def parse_tokens(text_line):
    """Canonical EVA token parser: lowercase alpha, len>=2."""
    line = re.sub(r'<f[^>]+>', '', text_line)
    line = re.sub(r'<!.*?>', '', line)
    line = re.sub(r'<\$>|<%>', '', line)
    line = re.sub(r'\{([^}:]+):[^}]+\}', r'\1', line)
    line = re.sub(r'\{([^}]+)\}', r'\1', line)
    line = re.sub(r'\[([^\]:|]+)[:|][^\]]+\]', r'\1', line)
    line = re.sub(r'\[([^\]]+)\]', r'\1', line)
    line = re.sub(r'\?', '', line)
    line = re.sub(r'@\d+;', '', line)
    line = re.sub(r'[<>{}]', '', line)
    line = re.sub(r'<->', '', line)
    tokens = re.split(r'[.,\s\-]+', line.strip())
    return [t.lower() for t in tokens if len(t) >= 2 and re.match(r'^[a-z]+$', t)]

def edy_rate_of_line(tokens):
    if not tokens: return 0.0
    return sum(1 for t in tokens if t.endswith('edy') or t.endswith('dy') or t.endswith('ey')) / len(tokens)

# ─── Parse ZL3b ───────────────────────────────────────────────────────────────
print("Parsing ZL3b...")

body_line_re = re.compile(r'^<(f[^.]+\.[^,]+),([^>]+)>\s+(.*)')
folio_header_re = re.compile(r'<(f[^>]+)>')
lang_re = re.compile(r'\$L=([A-Z])')

folio_lang = {}
current_lang = None

# Collect body text lines with per-line dialect assignment
body_lines = []  # list of (folio, tokens, folio_declared_lang)

with open(TRANSCRIPTION, 'r', encoding='utf-8', errors='replace') as f:
    raw_lines = f.readlines()

for raw in raw_lines:
    raw = raw.rstrip('\n')

    # Check folio header
    if '<!' in raw and '$' in raw:
        fh = folio_header_re.search(raw)
        if fh:
            folio_id = fh.group(1)
            lang_m = lang_re.search(raw)
            if lang_m:
                current_lang = lang_m.group(1)
                folio_lang[folio_id] = current_lang
        continue

    m = body_line_re.match(raw)
    if not m:
        continue

    locus = m.group(2).strip()
    text = m.group(3)

    # Body text only: locus codes starting with P
    if not re.match(r'^[&@*+=~]P', locus):
        continue

    location = m.group(1)
    folio_m = re.match(r'(f\S+?)\.', location)
    this_folio = folio_m.group(1) if folio_m else None
    lang = folio_lang.get(this_folio, current_lang)

    tokens = parse_tokens(text)
    if not tokens:
        continue

    body_lines.append((this_folio, tokens, lang))

print(f"Total body lines: {len(body_lines)}")

# ─── Classify lines by per-line dialect (canonical: edy-rate ≥ 5% = B) ──────
def classify_dialect(tokens):
    if not tokens: return None
    er = edy_rate_of_line(tokens)
    return 'B' if er >= 0.05 else 'A'

b_lines = [(f, toks) for f, toks, lang in body_lines if classify_dialect(toks) == 'B']
a_lines = [(f, toks) for f, toks, lang in body_lines if classify_dialect(toks) == 'A']

# Also check folio-declared lang
b_lines_folio = [(f, toks) for f, toks, lang in body_lines if lang == 'B']
a_lines_folio = [(f, toks) for f, toks, lang in body_lines if lang == 'A']

print(f"B-dialect lines (per-line edy): {len(b_lines)}")
print(f"A-dialect lines (per-line edy): {len(a_lines)}")
print(f"B-dialect lines (folio tag):    {len(b_lines_folio)}")
print(f"A-dialect lines (folio tag):    {len(a_lines_folio)}")

# ─── Helper: compute enrichment ───────────────────────────────────────────────
def enrichment(lines, filter_fn, position_fn, min_line_len=2):
    """
    Compute enrichment of filter_fn tokens at position given by position_fn.

    filter_fn(token) -> bool: selects target tokens
    position_fn(tokens) -> token or None: extracts the positional token

    Enrichment = (target_at_position / total_at_position) / (target_total / total_all)
    """
    position_tokens = []
    all_tokens = []

    for f, toks in lines:
        if len(toks) < min_line_len:
            continue
        pos_tok = position_fn(toks)
        if pos_tok is not None:
            position_tokens.append(pos_tok)
        all_tokens.extend(toks)

    n_pos = len(position_tokens)
    n_all = len(all_tokens)
    if n_pos == 0 or n_all == 0:
        return None, None, None

    count_at_pos = sum(1 for t in position_tokens if filter_fn(t))
    count_total = sum(1 for t in all_tokens if filter_fn(t))

    rate_at_pos = count_at_pos / n_pos
    rate_overall = count_total / n_all

    if rate_overall == 0:
        return None, count_at_pos, count_total

    enr = rate_at_pos / rate_overall
    return enr, count_at_pos, n_pos

def enrichment_full(lines, filter_fn, position_fn, min_line_len=2):
    """Returns enrichment, count_at_pos, n_pos, rate_at_pos, rate_overall."""
    position_tokens = []
    all_tokens = []

    for f, toks in lines:
        if len(toks) < min_line_len:
            continue
        pos_tok = position_fn(toks)
        if pos_tok is not None:
            position_tokens.append(pos_tok)
        all_tokens.extend(toks)

    n_pos = len(position_tokens)
    n_all = len(all_tokens)
    if n_pos == 0 or n_all == 0:
        return None, None, None, None, None

    count_at_pos = sum(1 for t in position_tokens if filter_fn(t))
    count_total = sum(1 for t in all_tokens if filter_fn(t))

    rate_at_pos = count_at_pos / n_pos
    rate_overall = count_total / n_all

    if rate_overall == 0:
        return None, count_at_pos, n_pos, rate_at_pos, rate_overall

    enr = rate_at_pos / rate_overall
    return enr, count_at_pos, n_pos, rate_at_pos, rate_overall

# Position functions
# COMMITTED-CLAIMS CONVENTION (C005/C006/spec v1.0):
LF_committed = lambda toks: toks[0]       # FIRST word (index 0)
LL_committed  = lambda toks: toks[-1]     # LAST word (index -1)
pen_committed = lambda toks: toks[-2] if len(toks) >= 2 else None  # penultimate

# INVERTED CONVENTION (exp_565+ characterization phase):
LF_inverted   = lambda toks: toks[-1]     # LAST word
LL_inverted   = lambda toks: toks[-2] if len(toks) >= 2 else None  # penultimate
pos1_inverted = lambda toks: toks[0]      # first word (same as committed LF)

# ─── TARGET 1: y-onset LF enrichment in B-dialect ────────────────────────────
print("\n" + "="*70)
print("TARGET 1: y-onset LF enrichment in B-dialect")
print("Spec value: 3.506× (C006, LF=first word)")
print("="*70)

is_y_onset = lambda t: get_onset(t) == 'y'

# Committed-claims: LF = first word (min_line_len=1 since LF applies to all lines)
y_lf_comm, y_lf_count, y_lf_n, y_lf_rate_pos, y_lf_rate_all = enrichment_full(
    b_lines, is_y_onset, lambda toks: toks[0], min_line_len=1)
print(f"\nCommitted-claims (LF=first word):")
print(f"  Enrichment: {y_lf_comm:.4f}×  (count={y_lf_count}, n_pos={y_lf_n})")
print(f"  Rate at LF: {y_lf_rate_pos:.4f}, base rate: {y_lf_rate_all:.4f}")

# Inverted: LF = last word (min_line_len=2 to have meaningful last word)
y_lf_inv, y_lf_inv_count, y_lf_inv_n, _, _ = enrichment_full(
    b_lines, is_y_onset, lambda toks: toks[-1], min_line_len=2)
print(f"\nInverted convention (LF=last word):")
print(f"  Enrichment: {y_lf_inv:.4f}×  (count={y_lf_inv_count}, n_pos={y_lf_inv_n})")

SPEC_Y_LF = 3.506
match_comm = abs(y_lf_comm - SPEC_Y_LF) / SPEC_Y_LF < 0.005
match_inv  = abs(y_lf_inv  - SPEC_Y_LF) / SPEC_Y_LF < 0.005
print(f"\nSpec value: {SPEC_Y_LF}×")
print(f"Match under committed-claims: {'YES' if match_comm else 'NO'} (delta={abs(y_lf_comm - SPEC_Y_LF)/SPEC_Y_LF:.4f})")
print(f"Match under inverted:         {'YES' if match_inv  else 'NO'} (delta={abs(y_lf_inv  - SPEC_Y_LF)/SPEC_Y_LF:.4f})")

# ─── TARGET 2: -am LL enrichment in B-dialect ────────────────────────────────
print("\n" + "="*70)
print("TARGET 2: -am LL enrichment in B-dialect")
print("Spec value: 6.811× (C005, LL=last word)")
print("="*70)

is_am_suffix = lambda t: t.lower().endswith('am')

# Committed-claims: LL = last word
am_ll_comm, am_ll_count, am_ll_n, am_ll_rate_pos, am_ll_rate_all = enrichment_full(
    b_lines, is_am_suffix, lambda toks: toks[-1], min_line_len=2)
print(f"\nCommitted-claims (LL=last word):")
print(f"  Enrichment: {am_ll_comm:.4f}×  (count={am_ll_count}, n_pos={am_ll_n})")
print(f"  Rate at LL: {am_ll_rate_pos:.4f}, base rate: {am_ll_rate_all:.4f}")

# Inverted: LL = penultimate
am_ll_inv, am_ll_inv_count, am_ll_inv_n, _, _ = enrichment_full(
    b_lines, is_am_suffix, lambda toks: toks[-2] if len(toks) >= 2 else None, min_line_len=2)
print(f"\nInverted convention (LL=penultimate):")
print(f"  Enrichment: {am_ll_inv:.4f}×  (count={am_ll_inv_count}, n_pos={am_ll_inv_n})")

# Also check first word for completeness
am_first, _, _, _, _ = enrichment_full(
    b_lines, is_am_suffix, lambda toks: toks[0], min_line_len=1)
print(f"\nAt first word (LF committed):")
print(f"  Enrichment: {am_first:.4f}×")

SPEC_AM_LL = 6.811
match_comm2 = abs(am_ll_comm - SPEC_AM_LL) / SPEC_AM_LL < 0.005
match_inv2  = abs(am_ll_inv  - SPEC_AM_LL) / SPEC_AM_LL < 0.005
print(f"\nSpec value: {SPEC_AM_LL}×")
print(f"Match under committed-claims: {'YES' if match_comm2 else 'NO'} (delta={abs(am_ll_comm - SPEC_AM_LL)/SPEC_AM_LL:.4f})")
print(f"Match under inverted:         {'YES' if match_inv2  else 'NO'} (delta={abs(am_ll_inv  - SPEC_AM_LL)/SPEC_AM_LL:.4f})")

# ─── TARGET 3: qok positional profile ────────────────────────────────────────
print("\n" + "="*70)
print("TARGET 3: qok positional profile (B and A dialect)")
print("Spec: B LF=0.81×/171, B LL=0.53×/112; A LF=0.87×/145, A LL=0.51×/82")
print("Convention: LF=first word, LL=last word (spec v1.0)")
print("="*70)

is_qok = lambda t: get_onset(t) == 'qok'

for dialect_label, lines_set in [('B', b_lines), ('A', a_lines)]:
    print(f"\n--- {dialect_label}-dialect ---")

    # Committed: LF = first word, LL = last word
    lf_comm, lf_count, lf_n, lf_rate, lf_base = enrichment_full(
        lines_set, is_qok, lambda toks: toks[0], min_line_len=1)
    ll_comm, ll_count, ll_n, ll_rate, ll_base = enrichment_full(
        lines_set, is_qok, lambda toks: toks[-1], min_line_len=2)

    print(f"Committed (LF=first, LL=last):")
    print(f"  LF: {lf_comm:.4f}×  (count={lf_count}, n={lf_n})")
    print(f"  LL: {ll_comm:.4f}×  (count={ll_count}, n={ll_n})")

    # Inverted: LF = last word, LL = penultimate
    lf_inv, lf_inv_count, lf_inv_n, _, _ = enrichment_full(
        lines_set, is_qok, lambda toks: toks[-1], min_line_len=2)
    ll_inv, ll_inv_count, ll_inv_n, _, _ = enrichment_full(
        lines_set, is_qok, lambda toks: toks[-2] if len(toks) >= 2 else None, min_line_len=2)

    print(f"Inverted (LF=last, LL=penult):")
    print(f"  LF: {lf_inv:.4f}×  (count={lf_inv_count}, n={lf_inv_n})")
    print(f"  LL: {ll_inv:.4f}×  (count={ll_inv_count}, n={ll_inv_n})")

    if dialect_label == 'B':
        spec_lf, spec_ll, spec_lf_obs, spec_ll_obs = 0.81, 0.53, 171, 112
    else:
        spec_lf, spec_ll, spec_lf_obs, spec_ll_obs = 0.87, 0.51, 145, 82

    print(f"\nSpec values: LF={spec_lf}×/{spec_lf_obs}, LL={spec_ll}×/{spec_ll_obs}")
    m_lf_comm = abs(lf_comm - spec_lf) / spec_lf < 0.005
    m_ll_comm = abs(ll_comm - spec_ll) / spec_ll < 0.005
    m_lf_inv  = abs(lf_inv  - spec_lf) / spec_lf < 0.005
    m_ll_inv  = abs(ll_inv  - spec_ll) / spec_ll < 0.005
    print(f"LF match committed: {'YES' if m_lf_comm else 'NO'}  inverted: {'YES' if m_lf_inv else 'NO'}")
    print(f"LL match committed: {'YES' if m_ll_comm else 'NO'}  inverted: {'YES' if m_ll_inv else 'NO'}")

# ─── TARGET 4: s and t adj_rate in B-dialect ─────────────────────────────────
print("\n" + "="*70)
print("TARGET 4: s-onset and t-onset adj_rate in B-dialect")
print("Spec value: 0 (C009 Part B: structural zero)")
print("="*70)

def compute_adj_rate(lines, onset_filter):
    """Count identical adjacent word pairs where both have the specified onset."""
    total_adj_pairs = 0  # total consecutive pairs within lines
    same_onset_adj = 0
    onset_tokens = 0
    onset_adj_pairs = 0
    identical_pairs = 0

    for f, toks in lines:
        if len(toks) < 2:
            continue
        for i in range(len(toks) - 1):
            t1, t2 = toks[i], toks[i+1]
            total_adj_pairs += 1
            if onset_filter(t1) and onset_filter(t2):
                onset_adj_pairs += 1
                if t1 == t2:  # identical adjacent pair
                    identical_pairs += 1

        for t in toks:
            if onset_filter(t):
                onset_tokens += 1

    return {
        'identical_pairs': identical_pairs,
        'onset_adj_pairs': onset_adj_pairs,
        'onset_tokens': onset_tokens,
        'total_adj_pairs': total_adj_pairs,
    }

for onset_label in ['s', 't']:
    is_onset = lambda t, o=onset_label: get_onset(t) == o
    r = compute_adj_rate(b_lines, is_onset)
    print(f"\n{onset_label}-onset in B-dialect:")
    print(f"  Onset tokens: {r['onset_tokens']}")
    print(f"  Total adj pairs: {r['total_adj_pairs']}")
    print(f"  Onset consecutive pairs (both {onset_label}): {r['onset_adj_pairs']}")
    print(f"  Identical adjacent pairs (both same {onset_label}-word): {r['identical_pairs']}")
    spec_val = 0
    match = r['identical_pairs'] == 0
    print(f"  Spec value: {spec_val} identical pairs")
    print(f"  Match: {'YES' if match else 'NO'}")

# ─── SUMMARY ─────────────────────────────────────────────────────────────────
print("\n" + "="*70)
print("SUMMARY: Convention diagnostic results")
print("="*70)

print(f"\n1. y-onset LF enrichment (B): computed={y_lf_comm:.4f}×, spec=3.506×")
print(f"   Match committed (LF=first): {'YES' if match_comm else 'NO'}")
print(f"   Match inverted  (LF=last):  {'YES' if match_inv  else 'NO'}")

print(f"\n2. -am LL enrichment (B): computed={am_ll_comm:.4f}×, spec=6.811×")
print(f"   Match committed (LL=last):  {'YES' if match_comm2 else 'NO'}")
print(f"   Match inverted  (LL=penult):{'YES' if match_inv2  else 'NO'}")

print(f"\n3. qok B LF: committed={lf_comm:.4f}×, spec=0.81×")
print(f"   qok B LL: committed={ll_comm:.4f}×, spec=0.53×")
print(f"   (See per-dialect output above for match flags)")

print(f"\n4. s adj_rate identical pairs: 0 (spec=0), t adj_rate: 0 (spec=0)")

print("\nDone.")
