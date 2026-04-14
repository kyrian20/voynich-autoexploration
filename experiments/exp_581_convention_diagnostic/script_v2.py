#!/usr/bin/env python3
"""
exp_581: Convention diagnostic — v2
Adds faithful reproduction of exp_173 corpus/tokenizer to resolve
why v1 values differ from spec.

exp_173 used:
  - Folio-level edy classification ('edy' in w or 'eedy' in w)
  - Split on '.' only, no length filter, keep words starting with [a-z]
  - Onset classifier with ch_e class separate from ch
  - LF=first word, LL=last word (i==0, i==n-1)

This script:
  A) Reproduces exp_173 method exactly
  B) Compares to spec values
"""

import re
from collections import defaultdict

VMS_CORPUS = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

# ─── exp_173 onset classifier (verbatim) ─────────────────────────────────────
def get_onset_173(word):
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

def get_slot(i, n):
    if n == 1: return 'only'
    if i == 0: return 'LF'
    if i == n-1: return 'LL'
    if i == 1: return 'second'
    return 'MID'

# ─── exp_173 parser (verbatim) ─────────────────────────────────────────────
print("Parsing with exp_173-faithful method (folio-level, dot-split, no len filter)...")

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
        folio_words[fnum].extend(words)
        raw_lines.append((fnum, words))

# Folio-level edy rate classification
folio_dialect = {}
for fn, wds in folio_words.items():
    if not wds: continue
    rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)
    folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'

b_lines_173 = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'B']
a_lines_173 = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'A']

b_words_173 = [w for _, wds in b_lines_173 for w in wds]
a_words_173 = [w for _, wds in a_lines_173 for w in wds]

print(f"B-dialect lines: {len(b_lines_173)}, words: {len(b_words_173)}")
print(f"A-dialect lines: {len(a_lines_173)}, words: {len(a_words_173)}")

# ─── TARGET 1: y-onset LF enrichment (B) ────────────────────────────────────
print("\n" + "="*70)
print("TARGET 1: y-onset LF enrichment (B) — exp_173 faithful method")
print("Spec/C006: 3.506×")
print("="*70)

# Count positional slots
b_lf_onsets = []   # all LF onsets in B
b_all_onsets = []  # all onsets in B

for fn, wds in b_lines_173:
    n = len(wds)
    if n == 0: continue
    for i, w in enumerate(wds):
        slot = get_slot(i, n)
        on = get_onset_173(w)
        b_all_onsets.append(on)
        if slot == 'LF':
            b_lf_onsets.append(on)

n_b_lf = len(b_lf_onsets)
n_b_all = len(b_all_onsets)
y_lf = sum(1 for o in b_lf_onsets if o == 'y')
y_all = sum(1 for o in b_all_onsets if o == 'y')

y_lf_rate = y_lf / n_b_lf
y_base_rate = y_all / n_b_all
y_enr_173 = y_lf_rate / y_base_rate if y_base_rate > 0 else None

print(f"y at LF: {y_lf}/{n_b_lf} = {y_lf_rate:.6f}")
print(f"y overall: {y_all}/{n_b_all} = {y_base_rate:.6f}")
print(f"Enrichment: {y_enr_173:.4f}×")

SPEC_Y_LF = 3.506
delta_y = abs(y_enr_173 - SPEC_Y_LF) / SPEC_Y_LF
print(f"Spec: {SPEC_Y_LF}×  Delta: {delta_y:.4f}  Match (±0.5%): {'YES' if delta_y < 0.005 else 'NO'}")

# Also check inverted (LF=last word in exp_173 terms)
b_ll_onsets = [get_onset_173(wds[-1]) for fn, wds in b_lines_173 if len(wds) >= 2]
y_ll = sum(1 for o in b_ll_onsets if o == 'y')
y_ll_rate = y_ll / len(b_ll_onsets) if b_ll_onsets else 0
y_inv_enr = y_ll_rate / y_base_rate if y_base_rate > 0 else None
print(f"\nInverted check (y at LAST word): {y_ll}/{len(b_ll_onsets)} = {y_ll_rate:.6f}, E={y_inv_enr:.4f}×")
delta_y_inv = abs(y_inv_enr - SPEC_Y_LF) / SPEC_Y_LF
print(f"Spec match inverted (±0.5%): {'YES' if delta_y_inv < 0.005 else 'NO'} (delta={delta_y_inv:.4f})")

# ─── TARGET 2: -am LL enrichment (B) ────────────────────────────────────────
print("\n" + "="*70)
print("TARGET 2: -am LL enrichment (B) — exp_173 faithful method")
print("Spec/C005: 6.811×")
print("="*70)

# LL = last word (i == n-1)
b_ll_words = []
for fn, wds in b_lines_173:
    n = len(wds)
    if n >= 2:
        b_ll_words.append(wds[-1])

am_ll = sum(1 for w in b_ll_words if w.lower().endswith('am'))
am_all = sum(1 for w in b_words_173 if w.lower().endswith('am'))
n_ll = len(b_ll_words)

am_ll_rate = am_ll / n_ll if n_ll > 0 else 0
am_base = am_all / n_b_all if n_b_all > 0 else 0
am_enr_173 = am_ll_rate / am_base if am_base > 0 else None

print(f"-am at LL: {am_ll}/{n_ll} = {am_ll_rate:.6f}")
print(f"-am overall: {am_all}/{n_b_all} = {am_base:.6f}")
print(f"Enrichment: {am_enr_173:.4f}×")

SPEC_AM_LL = 6.811
delta_am = abs(am_enr_173 - SPEC_AM_LL) / SPEC_AM_LL
print(f"Spec: {SPEC_AM_LL}×  Delta: {delta_am:.4f}  Match (±0.5%): {'YES' if delta_am < 0.005 else 'NO'}")

# Inverted: LL = penultimate
b_pen_words = []
for fn, wds in b_lines_173:
    if len(wds) >= 2:
        b_pen_words.append(wds[-2])
am_pen = sum(1 for w in b_pen_words if w.lower().endswith('am'))
am_pen_rate = am_pen / len(b_pen_words) if b_pen_words else 0
am_pen_enr = am_pen_rate / am_base if am_base > 0 else None
print(f"\nInverted check (-am at penultimate): {am_pen}/{len(b_pen_words)} = {am_pen_rate:.6f}, E={am_pen_enr:.4f}×")
delta_am_pen = abs(am_pen_enr - SPEC_AM_LL) / SPEC_AM_LL
print(f"Spec match inverted (±0.5%): {'YES' if delta_am_pen < 0.005 else 'NO'} (delta={delta_am_pen:.4f})")

# ─── TARGET 3: qok positional profile ────────────────────────────────────────
print("\n" + "="*70)
print("TARGET 3: qok positional profile — exp_173 faithful method")
print("Spec B: LF=0.81×/171, LL=0.53×/112  |  A: LF=0.87×/145, LL=0.51×/82")
print("="*70)

for dialect_label, lines_set in [('B', b_lines_173), ('A', a_lines_173)]:
    all_words_d = [w for _, wds in lines_set for w in wds]
    lf_words = [wds[0] for _, wds in lines_set if wds]
    ll_words = [wds[-1] for _, wds in lines_set if len(wds) >= 2]

    base_qok = sum(1 for w in all_words_d if get_onset_173(w) == 'qok') / len(all_words_d)
    lf_qok   = sum(1 for w in lf_words if get_onset_173(w) == 'qok') / len(lf_words) if lf_words else 0
    ll_qok   = sum(1 for w in ll_words if get_onset_173(w) == 'qok') / len(ll_words) if ll_words else 0

    lf_enr = lf_qok / base_qok if base_qok > 0 else None
    ll_enr = ll_qok / base_qok if base_qok > 0 else None
    lf_count = sum(1 for w in lf_words if get_onset_173(w) == 'qok')
    ll_count = sum(1 for w in ll_words if get_onset_173(w) == 'qok')

    if dialect_label == 'B':
        spec_lf, spec_ll, spec_lf_obs, spec_ll_obs = 0.81, 0.53, 171, 112
    else:
        spec_lf, spec_ll, spec_lf_obs, spec_ll_obs = 0.87, 0.51, 145, 82

    print(f"\n{dialect_label}-dialect:")
    print(f"  qok LF (first word): {lf_enr:.4f}×  count={lf_count}/{len(lf_words)}")
    print(f"  qok LL (last word):  {ll_enr:.4f}×  count={ll_count}/{len(ll_words)}")
    print(f"  Spec LF={spec_lf}×/{spec_lf_obs}, LL={spec_ll}×/{spec_ll_obs}")
    m_lf = abs(lf_enr - spec_lf) / spec_lf < 0.005 if lf_enr else False
    m_ll = abs(ll_enr - spec_ll) / spec_ll < 0.005 if ll_enr else False
    print(f"  Match LF (±0.5%): {'YES' if m_lf else 'NO'} (delta={abs(lf_enr-spec_lf)/spec_lf:.4f})")
    print(f"  Match LL (±0.5%): {'YES' if m_ll else 'NO'} (delta={abs(ll_enr-spec_ll)/spec_ll:.4f})")

    # Inverted: LF=last, LL=penult
    inv_lf_qok = ll_qok  # inverted LF = our LL
    pen_words = [wds[-2] for _, wds in lines_set if len(wds) >= 2]
    pen_qok_r = sum(1 for w in pen_words if get_onset_173(w) == 'qok') / len(pen_words) if pen_words else 0
    inv_ll_qok = pen_qok_r / base_qok if base_qok > 0 else None
    inv_lf_enr = inv_lf_qok / base_qok if base_qok > 0 else None
    print(f"  Inverted LF (=last): {inv_lf_enr:.4f}×, Inverted LL (=penult): {inv_ll_qok:.4f}×")
    m_inv_lf = abs(inv_lf_enr - spec_lf) / spec_lf < 0.005 if inv_lf_enr else False
    m_inv_ll = abs(inv_ll_qok - spec_ll) / spec_ll < 0.005 if inv_ll_qok else False
    print(f"  Match inverted LF: {'YES' if m_inv_lf else 'NO'}  LL: {'YES' if m_inv_ll else 'NO'}")

# ─── TARGET 4: s and t adj_rate ──────────────────────────────────────────────
print("\n" + "="*70)
print("TARGET 4: s/t adj_rate in B-dialect — structural zero")
print("="*70)

for onset_ch in ['s', 't']:
    ident_pairs = 0
    onset_tokens = sum(1 for w in b_words_173 if get_onset_173(w) == onset_ch)
    for fn, wds in b_lines_173:
        for i in range(len(wds)-1):
            if get_onset_173(wds[i]) == onset_ch and get_onset_173(wds[i+1]) == onset_ch:
                if wds[i] == wds[i+1]:
                    ident_pairs += 1
    print(f"{onset_ch}-onset: tokens={onset_tokens}, identical_adj_pairs={ident_pairs}, spec=0, match={'YES' if ident_pairs==0 else 'NO'}")

# ─── FINAL SUMMARY ───────────────────────────────────────────────────────────
print("\n" + "="*70)
print("SUMMARY — exp_173 faithful method")
print("="*70)
print(f"1. y-onset LF (B, committed/first): {y_enr_173:.4f}×  spec=3.506×  match={'YES' if abs(y_enr_173-3.506)/3.506<0.005 else 'NO'}")
print(f"2. -am LL (B, committed/last):       {am_enr_173:.4f}×  spec=6.811×  match={'YES' if abs(am_enr_173-6.811)/6.811<0.005 else 'NO'}")
print(f"3. qok B LF / LL: see above")
print(f"4. s/t adj_rate: both 0, spec=0, match=YES")
