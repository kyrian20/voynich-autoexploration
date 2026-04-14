#!/usr/bin/env python3
"""
exp_587: Transliteration Replication — Session R2 (v101 Claston)

Replicates five pre-registered findings under the v101 (Claston) transliteration
system, which uses a single-character-per-glyph encoding (latin-1) independent
of the EVA letter system.

Confirmed character mapping from STA1_def.pdf (Zandbergen):
  v101 '1'→ch, '2'→sh, '8'→d, '9'→y, 'h'→k, 'k'→t, 'K'→cth, 'H'→ckh,
  'J'→cph, 'G'→cph-variant, 'U'→cth-variant, 'F'→cfh, '4'→q, 'o'→o,
  'a'→a, 's'→s, 'y'→r, 'e'→l, 'c'→EVA-e, 'N'→n, 'm'→iin, 'n'→in,
  'i'→i, 'I'→ii, 'z'→ir, 'Z'→iir, 'p'→m, 'g'→p, 'f'→f, 'C'→ee,
  'l'→ckhh, 'L'→cthh, 'A'→open-o, 'M'→iiin.
  'j' treated as k-gallows variant (frequent context: 'oj1c89'='okchedy').

EVA 'edy' → v101 'c89' (c=EVA-e, 8=d, 9=y).
EVA 'eedy' → v101 'cc89' or 'C89' (C=ee-ligature).

Onset class mappings (derived from mapping table):
  qok = '4oh' or '4oj' (q+o+k, j=k-variant)
  qot = '4ok' (q+o+t)
  qo  = '4o'
  cth = 'K' or 'U'
  ckh = 'H'
  cph = 'J' or 'G'
  ch  = '1'
  sh  = '2'
  ok  = 'oh' or 'oj' (o+k)
  ot  = 'ok' (o+t)
  ol  = 'oe' (o+l)
  d   = '8'
  s   = 's'
  y   = '9'
  k   = 'h' or 'j' (k-gallows)
  t   = 'k' (t-gallows)
  l   = 'e'
  r   = 'y'
  p   = 'g'
  f   = 'f' or 'F' (cfh treated as f-variant)
  a   = 'a'
  o   = 'o' (bare)

Dialect agreement gate: ≥95% per-folio agreement with ZL3b (required before proceeding).
Actual gate result: 95.0% (191/201 shared folios agree).

Pre-registered findings:
  F1: Three-layer positional architecture — ≥75% class-category agreement
  F2: Terminal-layer dialect inversion — zero overlap, d=A-term, B-member in B
  F3: Bigram cross-dialect invariants — ≥4/5 directionally replicated
  F4: A-herbal paragraph chain d→qot→ch→o→sh — >95th pct both null models
  F5: Systematic -edy suffix transformation — ≥75% of onset classes

Plan references: transliteration_replication_plan.md §7.3, §8.5
"""

import sys, os, re, random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

V101_PATH = str(ROOT / 'data' / 'transcriptions' / 'v101_claston.txt')
ZL3B_PATH = str(ROOT / 'data' / 'transcriptions' / 'eva_zl3b.txt')

SEED = 587000

# ── v101 Character Set ──────────────────────────────────────────────────────

# Clean character set: only characters with confirmed Claston mapping.
# 'j' added as k-gallows variant (445 body occurrences, context 'oj1c89'='okchedy').
V101_CLEAN = frozenset('12489acefghijklmnopsyzACFGHIJKLMNUZ')

# ── v101 Tokenizer ───────────────────────────────────────────────────────────

def tokenize_v101(text: str) -> list:
    """v101 tokenizer: split on period/comma, keep only clean tokens (len≥2)."""
    text = text.rstrip('-=\n')
    return [t for t in re.split(r'[.,]+', text)
            if len(t) >= 2 and all(c in V101_CLEAN for c in t)]

# ── v101 Onset Classifier ────────────────────────────────────────────────────

ALL_ONSET_CLASSES = [
    'qok', 'qot', 'qo', 'cth', 'sch', 'ckh', 'cph',
    'ch', 'sh', 'ok', 'ot', 'ol',
    'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f', 'a', 'o',
]

def get_onset_v101(word: str) -> str:
    """Priority-ordered prefix onset classifier for v101 tokens.

    Derived from the confirmed STA1_def.pdf Claston mapping table.
    Priority: longer prefixes first; 'j' treated as k-gallows variant.
    """
    # q-bench (4=q, o=o, h/j=k, k=t)
    if word.startswith('4oh'): return 'qok'   # q+o+k
    if word.startswith('4oj'): return 'qok'   # q+o+k-variant
    if word.startswith('4ok'): return 'qot'   # q+o+t
    if word.startswith('4o'):  return 'qo'    # q+o
    # sch must precede s and ch
    if word.startswith('s1'):  return 'sch'   # s+ch
    # single-char compound gallows
    if word.startswith('K'):   return 'cth'
    if word.startswith('U'):   return 'cth'   # cth-variant
    if word.startswith('H'):   return 'ckh'
    if word.startswith('J'):   return 'cph'
    if word.startswith('G'):   return 'cph'   # cph-variant
    # ch/sh single glyphs
    if word.startswith('1'):   return 'ch'
    if word.startswith('2'):   return 'sh'
    # o-prefix (oh/oj/ok/oe before bare 'o')
    if word.startswith('oh'):  return 'ok'    # o+k
    if word.startswith('oj'):  return 'ok'    # o+k-variant
    if word.startswith('ok'):  return 'ot'    # o+t
    if word.startswith('oe'):  return 'ol'    # o+l
    # single-char onsets
    if word.startswith('8'):   return 'd'
    if word.startswith('s'):   return 's'
    if word.startswith('9'):   return 'y'
    if word.startswith('h'):   return 'k'
    if word.startswith('j'):   return 'k'     # k-gallows variant
    if word.startswith('k'):   return 't'
    if word.startswith('e'):   return 'l'
    if word.startswith('y'):   return 'r'
    if word.startswith('g'):   return 'p'
    if word.startswith('f'):   return 'f'
    if word.startswith('F'):   return 'f'     # cfh → f-variant
    if word.startswith('a'):   return 'a'
    if word.startswith('o'):   return 'o'     # bare o (after all o-prefix checks)
    return 'other'

# ── v101 Suffix Classifier (for F5) ─────────────────────────────────────────

# B-dialect suffixes in v101 (EVA -edy/-eedy)
B_SUFFIXES_V101 = {'c89', 'cc89', 'C89'}

# A-dialect suffixes in v101 (EVA -ol/-or/-ey)
A_SUFFIXES_V101 = {'oe', 'oy', 'c9'}

def has_b_suffix(word: str) -> bool:
    return any(word.endswith(s) for s in B_SUFFIXES_V101)

def has_a_suffix(word: str) -> bool:
    return any(word.endswith(s) for s in A_SUFFIXES_V101)

# ── Dialect Classifier ───────────────────────────────────────────────────────

def has_edy_v101(word: str) -> bool:
    """True if word contains v101 'edy' or 'eedy' pattern."""
    return 'c89' in word or 'C89' in word

def folio_dialect_v101(words: list, threshold: float = 0.05, min_toks: int = 10):
    if len(words) < min_toks:
        return None
    rate = sum(1 for w in words if has_edy_v101(w)) / len(words)
    return 'B' if rate >= threshold else 'A'

# ── v101 Corpus Loader ───────────────────────────────────────────────────────

# Locus format: <folio.lineno>text
# Body lines: lineno is an integer. Non-body: lineno is a word (label, ring, etc.)
BODY_LOCUS_RE = re.compile(r'^<(\d+[rv]\d*)\.(\d+)>(.*)')

# Herbal A folio range for F4
A_HERBAL_MAX_FOLIO = 56

def load_v101_corpus(dialect: str = 'B') -> list:
    """Load v101 corpus filtered to the requested dialect.

    Returns list of (folio_label, words) tuples.
    Uses folio-level dialect assignment (edy-rate per folio ≥5% = B).
    """
    folio_raw: dict = defaultdict(list)
    with open(V101_PATH, encoding='latin-1') as f:
        for line in f:
            m = BODY_LOCUS_RE.match(line)
            if not m:
                continue
            folio, lineno, text = m.group(1), int(m.group(2)), m.group(3)
            toks = tokenize_v101(text)
            if toks:
                folio_raw[folio].append(toks)

    # Folio-level dialect assignment
    folio_dialect = {}
    for folio, lines in folio_raw.items():
        words = [w for l in lines for w in l]
        folio_dialect[folio] = folio_dialect_v101(words)

    # Filter to requested dialect
    out = []
    for folio, lines in folio_raw.items():
        if folio_dialect.get(folio) != dialect:
            continue
        for words in lines:
            out.append((folio, words))
    return out

def load_v101_a_herbal_folio_lines(max_folio: int = A_HERBAL_MAX_FOLIO) -> dict:
    """Load A-dialect herbal folio lines for CL chain analysis.

    Returns dict: folio_num (int) → list_of_word_lists.
    Only includes folios with numeric folio number ≤ max_folio, classified A-dialect.
    """
    folio_raw: dict = defaultdict(list)
    with open(V101_PATH, encoding='latin-1') as f:
        for line in f:
            m = BODY_LOCUS_RE.match(line)
            if not m:
                continue
            folio_str, lineno, text = m.group(1), int(m.group(2)), m.group(3)
            # Extract numeric folio number
            fm = re.match(r'^(\d+)[rv]', folio_str)
            if not fm:
                continue
            fnum = int(fm.group(1))
            if fnum > max_folio:
                continue
            toks = tokenize_v101(text)
            if toks:
                folio_raw[(fnum, folio_str)].append(toks)

    # Keep only A-dialect folios
    out = {}
    for (fnum, folio_str), lines in folio_raw.items():
        words = [w for l in lines for w in l]
        if len(words) < 10:
            continue
        if folio_dialect_v101(words) == 'A':
            if fnum not in out:
                out[fnum] = []
            out[fnum].extend(lines)
    return out

# ── Analytics (inline, parameterised on onset_fn) ───────────────────────────

def get_slot(i, n):
    if n == 1:   return 'only'
    if i == 0:   return 'LF'
    if i == n-1: return 'LL'
    if i == 1:   return 'second'
    return 'MID'

def positional_enrichment_v101(corpus, target_class):
    """Compute (E_LF, obs_LF, E_LL, obs_LL) for target_class."""
    all_words = [w for _, ws in corpus for w in ws]
    total_n = len(all_words)
    if total_n == 0:
        return float('nan'), 0, float('nan'), 0
    base_rate = sum(1 for w in all_words if get_onset_v101(w) == target_class) / total_n

    lf_words = [w for _, ws in corpus for i,w in enumerate(ws) if get_slot(i,len(ws))=='LF']
    ll_words = [w for _, ws in corpus for i,w in enumerate(ws) if get_slot(i,len(ws))=='LL']

    def enrich(slot_words):
        n = len(slot_words)
        if n == 0 or base_rate == 0:
            return float('nan'), 0
        obs = sum(1 for w in slot_words if get_onset_v101(w) == target_class)
        return (obs / n) / base_rate, obs

    e_lf, obs_lf = enrich(lf_words)
    e_ll, obs_ll = enrich(ll_words)
    return e_lf, obs_lf, e_ll, obs_ll

def bigram_enrichment_v101(corpus, sender, receiver):
    """Returns (E, obs_pair, n_sender)."""
    n_sender, obs_pair, n_receiver_total, n_positions = 0, 0, 0, 0
    for _, words in corpus:
        for i in range(len(words) - 1):
            n_positions += 1
            if get_onset_v101(words[i+1]) == receiver:
                n_receiver_total += 1
            if get_onset_v101(words[i]) == sender:
                n_sender += 1
                if get_onset_v101(words[i+1]) == receiver:
                    obs_pair += 1
    if n_sender == 0 or n_positions == 0:
        return float('nan'), obs_pair, n_sender
    rate_recv = n_receiver_total / n_positions
    expected = n_sender * rate_recv
    return obs_pair / expected if expected > 0 else float('nan'), obs_pair, n_sender

# ── F1: Positional architecture ──────────────────────────────────────────────

CONF_E = 1.5
CONF_N = 20

def classify_positional_architecture(corpus):
    """Classify each onset class as opener / terminal / mid / rare."""
    result = {}
    for cls in ALL_ONSET_CLASSES:
        e_lf, obs_lf, e_ll, obs_ll = positional_enrichment_v101(corpus, cls)
        if obs_lf < CONF_N and obs_ll < CONF_N:
            result[cls] = ('rare', e_lf, obs_lf, e_ll, obs_ll)
            continue
        lf_conf = (e_lf == e_lf) and (e_lf >= CONF_E) and (obs_lf >= CONF_N)
        ll_conf = (e_ll == e_ll) and (e_ll >= CONF_E) and (obs_ll >= CONF_N)
        if lf_conf and not ll_conf:
            cat = 'opener'
        elif ll_conf and not lf_conf:
            cat = 'terminal'
        elif lf_conf and ll_conf:
            cat = 'opener' if e_lf >= e_ll else 'terminal'
        else:
            cat = 'mid'
        result[cls] = (cat, e_lf, obs_lf, e_ll, obs_ll)
    return result

# ── F2: Terminal sets ─────────────────────────────────────────────────────────

def get_conf_terminals(corpus, min_e=CONF_E, min_obs=CONF_N):
    """Return onset classes with CONF LL enrichment (E≥min_e, obs≥min_obs)."""
    result = {}
    for cls in ALL_ONSET_CLASSES:
        _, _, _, e_ll, obs_ll = positional_enrichment_v101(corpus, cls)
        if (e_ll == e_ll) and (e_ll >= min_e) and (obs_ll >= min_obs):
            result[cls] = (round(e_ll, 3), obs_ll)
    # Also check positional_enrichment_v101 for e_ll
    return result

def get_conf_terminals_v2(corpus, min_e=CONF_E, min_obs=CONF_N):
    result = {}
    all_words = [w for _, ws in corpus for w in ws]
    total_n = len(all_words)
    if total_n == 0: return result
    ll_words = [w for _, ws in corpus for i,w in enumerate(ws) if get_slot(i,len(ws))=='LL']
    n_ll = len(ll_words)
    for cls in ALL_ONSET_CLASSES:
        base_rate = sum(1 for w in all_words if get_onset_v101(w)==cls) / total_n
        if base_rate == 0 or n_ll == 0: continue
        obs = sum(1 for w in ll_words if get_onset_v101(w)==cls)
        e = (obs/n_ll) / base_rate
        if e >= min_e and obs >= min_obs:
            result[cls] = (round(e,3), obs)
    return result

# ── F3: Bigram invariants ─────────────────────────────────────────────────────

BIGRAM_INVARIANTS = [
    ('y',   'y',   'elevated'),
    ('sh',  'qok', 'elevated'),
    ('ok',  'ok',  'elevated'),
    ('qok', 's',   'elevated'),
    ('sh',  'ch',  'depleted'),
]

def compute_bigram_invariants(a_corp, b_corp):
    results = {}
    for (sender, receiver, direction) in BIGRAM_INVARIANTS:
        ae, ao, an = bigram_enrichment_v101(a_corp, sender, receiver)
        be, bo, bn = bigram_enrichment_v101(b_corp, sender, receiver)
        if direction == 'elevated':
            a_ok = (ae == ae) and ae > 1.0
            b_ok = (be == be) and be > 1.0
        else:
            a_ok = (ae == ae) and ae < 1.0
            b_ok = (be == be) and be < 1.0
        results[f'{sender}→{receiver}'] = {
            'direction': direction,
            'A_E': round(ae, 3) if ae == ae else float('nan'),
            'B_E': round(be, 3) if be == be else float('nan'),
            'A_obs': ao, 'B_obs': bo,
            'A_ok': a_ok, 'B_ok': b_ok,
            'replicated': a_ok and b_ok,
        }
    return results

# ── F4: A-herbal paragraph chain ─────────────────────────────────────────────

TARGET_CHAIN = ['d', 'qot', 'ch', 'o', 'sh']

def build_ll_ll_pairs(folio_lines: dict) -> list:
    """CL bigrams = (LL-onset[i], LL-onset[i+1]) per exp_583 methodology."""
    pairs = []
    for fnum in sorted(folio_lines):
        lines = folio_lines[fnum]
        ll_onsets = [get_onset_v101(l[-1]) for l in lines if l]
        for i in range(len(ll_onsets) - 1):
            pairs.append((ll_onsets[i], ll_onsets[i+1]))
    return pairs

def chain_strength(pairs, chain):
    """Joint enrichment product: E = obs/(f_a*f_b*N)."""
    if not pairs:
        return 0.0
    total = len(pairs)
    lf_base = Counter(a for a, b in pairs)
    pc = Counter(pairs)
    js = 1.0
    for i in range(len(chain) - 1):
        a, b = chain[i], chain[i+1]
        fa = lf_base.get(a, 0) / total
        fb = lf_base.get(b, 0) / total
        if fa == 0 or fb == 0:
            return 0.0
        obs = pc.get((a, b), 0)
        js *= obs / (fa * fb * total)
    return js

def run_section_shuffle(folio_lines, target_chain, n=200, seed=SEED):
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)
    null = []
    for _ in range(n):
        shuf = {fnum: list(lines) for fnum, lines in folio_lines.items()}
        for fnum in shuf:
            rng.shuffle(shuf[fnum])
        null.append(chain_strength(build_ll_ll_pairs(shuf), target_chain))
    pct = sum(1 for v in null if real_js > v) / n * 100
    return real_js, pct, null

def run_onset_shuffle(folio_lines, target_chain, n=200, seed=SEED+1):
    rng = random.Random(seed)
    real_pairs = build_ll_ll_pairs(folio_lines)
    real_js = chain_strength(real_pairs, target_chain)
    null = []
    for _ in range(n):
        all_onsets = [a for a,b in real_pairs] + ([real_pairs[-1][1]] if real_pairs else [])
        perm = list(all_onsets)
        rng.shuffle(perm)
        shuf = [(perm[i], perm[i+1]) for i in range(len(real_pairs))]
        null.append(chain_strength(shuf, target_chain))
    pct = sum(1 for v in null if real_js > v) / n * 100
    return real_js, pct, null

# ── F5: Suffix transformation ─────────────────────────────────────────────────

B_SUFFIX_FOLD_THRESHOLD = 3.0
B_SUFFIX_ABS_THRESHOLD  = 0.05
MIN_TOKENS_FOR_SUFFIX   = 20

def suffix_transformation_analysis(a_corp, b_corp):
    def suf_rate(corpus, cls, suf_fn):
        words = [w for _, ws in corpus for w in ws if get_onset_v101(w) == cls]
        if not words:
            return 0.0, 0
        hits = sum(1 for w in words if suf_fn(w))
        return hits / len(words), len(words)

    results = {}
    for cls in ALL_ONSET_CLASSES:
        a_b, n_a = suf_rate(a_corp, cls, has_b_suffix)
        b_b, n_b = suf_rate(b_corp, cls, has_b_suffix)
        a_a, _   = suf_rate(a_corp, cls, has_a_suffix)
        b_a, _   = suf_rate(b_corp, cls, has_a_suffix)

        if n_a < MIN_TOKENS_FOR_SUFFIX or n_b < MIN_TOKENS_FOR_SUFFIX:
            results[cls] = None
            continue

        fold = (b_b / a_b) if a_b > 0 else float('inf')
        shows = (b_b >= B_SUFFIX_ABS_THRESHOLD) and (
            (a_b == 0) or (fold >= B_SUFFIX_FOLD_THRESHOLD)
        )
        results[cls] = {
            'shows_transform': shows,
            'a_bsuf': round(a_b, 4), 'b_bsuf': round(b_b, 4),
            'a_asuf': round(a_a, 4), 'b_asuf': round(b_a, 4),
            'fold': round(fold, 1) if a_b > 0 else '∞',
            'n_a': n_a, 'n_b': n_b,
        }
    return results

# ── Dialect agreement gate ────────────────────────────────────────────────────

def compute_dialect_agreement():
    """Compare per-folio dialect assignment between v101 and ZL3b."""
    # Build v101 folio dialects
    folio_v101_words = defaultdict(list)
    with open(V101_PATH, encoding='latin-1') as f:
        for line in f:
            m = BODY_LOCUS_RE.match(line)
            if not m: continue
            folio, _, text = m.group(1), m.group(2), m.group(3)
            folio_v101_words[folio].extend(tokenize_v101(text))

    v101_dialects = {}
    for folio, words in folio_v101_words.items():
        v101_dialects[folio] = folio_dialect_v101(words)

    # Build ZL3b folio dialects
    zl3b_re = re.compile(r'^<f(\d+[rv]\d*)\.(\d+),([^>]*)>(.*)')
    folio_zl3b_words = defaultdict(list)
    with open(ZL3B_PATH, encoding='utf-8') as f:
        for line in f:
            m = zl3b_re.match(line)
            if not m: continue
            folio, _, ltype, text = m.group(1), m.group(2), m.group(3), m.group(4)
            if 'P' not in ltype: continue
            text = re.sub(r'\[([^:,\]]+)(?::[^\]]+)?\]', r'\1', text)
            text = re.sub(r'\{[^}]+\}', '', text)
            toks = [t for t in re.split(r'[-.\s]+', text.lower())
                    if t and len(t) >= 2 and t.isalpha()]
            folio_zl3b_words[folio].extend(toks)

    zl3b_dialects = {}
    for folio, words in folio_zl3b_words.items():
        if len(words) < 10: continue
        rate = sum(1 for w in words if 'edy' in w or 'eedy' in w) / len(words)
        zl3b_dialects[folio] = 'B' if rate >= 0.05 else 'A'

    shared = set(v101_dialects.keys()) & set(zl3b_dialects.keys())
    agree = disagree = 0
    for f in shared:
        dv = v101_dialects.get(f)
        dz = zl3b_dialects.get(f)
        if dv is None or dz is None: continue
        if dv == dz: agree += 1
        else: disagree += 1

    total = agree + disagree
    return agree, total, 100.0 * agree / total if total else 0.0

# ── ZL3b reference classifications ───────────────────────────────────────────

# ZL3b F1 classifications from exp_586 (baseline for agreement calculation)
ZL3B_F1_CLASSES = {
    'qok': 'mid', 'qot': 'mid', 'qo': 'mid',
    'cth': 'rare', 'sch': 'rare', 'ckh': 'rare', 'cph': 'rare',
    'ch': 'mid', 'sh': 'mid',
    'ok': 'mid', 'ot': 'mid', 'ol': 'mid',
    'd': 'opener', 's': 'opener', 'y': 'opener', 'k': 'mid', 't': 'opener',
    'l': 'terminal', 'r': 'terminal', 'p': 'opener', 'f': 'rare',
    'a': 'terminal', 'o': 'terminal',
}

# ── Formatting helpers ────────────────────────────────────────────────────────

def sep(char='─', width=70):
    print(char * width)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sep('═')
    print("exp_587: Transliteration Replication — Session R2 (v101 Claston)")
    sep('═')

    # ── [0] Dialect agreement gate ────────────────────────────────────────────
    print("\n[0] Dialect agreement gate (must be ≥95% to proceed)")
    agree, total, pct = compute_dialect_agreement()
    print(f"  Shared folios: {total}")
    print(f"  Agreement: {agree}/{total} = {pct:.1f}%")
    if pct < 95.0:
        print(f"  ABORT: dialect agreement {pct:.1f}% < 95% gate. Mapping table error.")
        return
    print(f"  Gate: PASS ({pct:.1f}% ≥ 95%)")

    # ── [1] Load corpora ──────────────────────────────────────────────────────
    print("\n[1] Loading v101 corpora...")
    v101_b = load_v101_corpus(dialect='B')
    v101_a = load_v101_corpus(dialect='A')
    n_b = sum(len(ws) for _, ws in v101_b)
    n_a = sum(len(ws) for _, ws in v101_a)
    print(f"  v101 B: {len(v101_b)} lines, {n_b:,} tokens")
    print(f"  v101 A: {len(v101_a)} lines, {n_a:,} tokens")
    print(f"  ZL3b B: ~17,997 tokens (reference exp_586)")
    print(f"  ZL3b A: ~8,461 tokens (reference exp_586)")
    print(f"  Note: v101 A-token count is higher than ZL3b due to different")
    print(f"        folio-level dialect assignment on borderline folios.")

    # ── F1: Three-layer positional architecture ───────────────────────────────
    sep()
    print("\n[F1] Three-layer positional architecture")
    print(f"     CONF: E≥{CONF_E}×, obs≥{CONF_N}")

    v101_b_cls = classify_positional_architecture(v101_b)
    # Use B-dialect for F1 (same as canonical methodology)

    print(f"\n  {'Class':<8} {'ZL3b':<12} {'v101':<12} Match")
    print(f"  {'-'*8} {'-'*12} {'-'*12} -----")
    matches = 0
    total_charted = 0
    for cls in ALL_ONSET_CLASSES:
        z_cat = ZL3B_F1_CLASSES[cls]
        v_cat = v101_b_cls[cls][0]
        if z_cat == 'rare' and v_cat == 'rare':
            print(f"  {cls:<8} {z_cat:<12} {v_cat:<12} — (rare)")
            continue
        if z_cat == 'rare' or v_cat == 'rare':
            # One is rare, other is not — count as mismatch
            total_charted += 1
            m = False
            print(f"  {cls:<8} {z_cat:<12} {v_cat:<12} NO  (rare mismatch)")
            continue
        total_charted += 1
        m = (z_cat == v_cat)
        if m: matches += 1
        # Print enrichment details
        _, e_lf, obs_lf, e_ll, obs_ll = v101_b_cls[cls]
        e_lf_s = f'{e_lf:.2f}' if e_lf == e_lf else 'nan'
        e_ll_s = f'{e_ll:.2f}' if e_ll == e_ll else 'nan'
        print(f"  {cls:<8} {z_cat:<12} {v_cat:<12} {'YES' if m else 'NO '}"
              f"  (LF:{e_lf_s}×{obs_lf}, LL:{e_ll_s}×{obs_ll})")

    agreement_pct = 100.0 * matches / total_charted if total_charted else 0
    print(f"\n  Agreement: {matches}/{total_charted} = {agreement_pct:.1f}%")
    f1_status = ('RETAINED' if agreement_pct >= 75.0 and matches >= 15
                 else ('WEAKENED' if agreement_pct >= 50.0 else 'FAILED'))
    print(f"  Pre-reg threshold: ≥75% (≥15/20). Result: {f1_status}")

    # ── F2: Terminal-layer dialect inversion ──────────────────────────────────
    sep()
    print("\n[F2] Terminal-layer dialect inversion")
    print(f"     CONF terminal: E≥{CONF_E}×, obs≥{CONF_N}")

    a_terms = get_conf_terminals_v2(v101_a)
    b_terms = get_conf_terminals_v2(v101_b)

    print("\n  A-dialect CONF terminals:")
    for cls, (e, obs) in sorted(a_terms.items(), key=lambda x: -x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")
    if not a_terms: print("    (none)")

    print("\n  B-dialect CONF terminals:")
    for cls, (e, obs) in sorted(b_terms.items(), key=lambda x: -x[1][0]):
        print(f"    {cls:<8} E={e:.3f} (n={obs})")
    if not b_terms: print("    (none)")

    a_set = set(a_terms.keys())
    b_set = set(b_terms.keys())
    overlap = a_set & b_set
    d_in_a = 'd' in a_set
    b_canonical = {'r', 'l', 'ol', 'o', 'a'}
    b_member = len(b_canonical & b_set) > 0

    print(f"\n  Overlap: {overlap if overlap else '∅ (zero overlap)'}")
    print(f"  d ∈ A-terminals: {d_in_a}")
    print(f"  B-canonical ∩ B-terminals: {b_canonical & b_set}")

    f2_retained = (len(overlap) == 0) and d_in_a and b_member
    f2_status = 'RETAINED' if f2_retained else 'FAILED'
    print(f"  Result: {f2_status}")

    # ── F3: Bigram invariants ─────────────────────────────────────────────────
    sep()
    print("\n[F3] Bigram matrix cross-dialect invariants")
    print("     Threshold: directional (E>1.0 elevated / E<1.0 depleted) in both dialects")

    bigram_results = compute_bigram_invariants(v101_a, v101_b)

    print(f"\n  {'Pair':<12} {'Direction':<10} {'A_E':<8} {'B_E':<8} Replicated")
    print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*8} ---------")
    n_replicated = 0
    for key, r in bigram_results.items():
        a_e_s = f"{r['A_E']:.3f}{'✓' if r['A_ok'] else '✗'}"
        b_e_s = f"{r['B_E']:.3f}{'✓' if r['B_ok'] else '✗'}"
        rep = 'YES' if r['replicated'] else 'NO'
        if r['replicated']: n_replicated += 1
        print(f"  {key:<12} {r['direction']:<10} {a_e_s:<8} {b_e_s:<8} {rep}")

    print(f"\n  Replicated: {n_replicated}/{len(bigram_results)}")
    f3_status = ('RETAINED' if n_replicated >= 4
                 else ('WEAKENED' if n_replicated >= 3 else 'FAILED'))
    print(f"  Pre-reg threshold: ≥4/5. Result: {f3_status}")

    # ── F4: A-herbal paragraph chain ─────────────────────────────────────────
    sep()
    print("\n[F4] A-herbal paragraph chain d→qot→ch→o→sh")
    print(f"     Corpus: A-dialect herbal folios f1–f{A_HERBAL_MAX_FOLIO}")
    print(f"     CL pairs: (LL-onset[i], LL-onset[i+1]) per exp_583 methodology")

    herbal_lines = load_v101_a_herbal_folio_lines()
    n_folios = len(herbal_lines)
    all_pairs = build_ll_ll_pairs(herbal_lines)
    print(f"  Loaded: {n_folios} A-dialect herbal folios, {len(all_pairs)} CL pairs")

    real_js = chain_strength(all_pairs, TARGET_CHAIN)
    print(f"  Real chain joint-strength: {real_js:.4f}")

    # Per-edge enrichments
    print("\n  Per-edge enrichments:")
    pc = Counter(all_pairs)
    total = len(all_pairs)
    lf_base = Counter(a for a,b in all_pairs)
    for i in range(len(TARGET_CHAIN) - 1):
        a, b = TARGET_CHAIN[i], TARGET_CHAIN[i+1]
        fa = lf_base.get(a, 0) / total if total else 0
        fb = lf_base.get(b, 0) / total if total else 0
        obs = pc.get((a, b), 0)
        e = obs / (fa * fb * total) if fa > 0 and fb > 0 and total > 0 else 0.0
        print(f"    {a}→{b}: E={e:.3f} (obs={obs})")

    print(f"\n  Running null models (N=200)...")
    real_js_sec, pct_sec, _ = run_section_shuffle(herbal_lines, TARGET_CHAIN)
    real_js_ons, pct_ons, _ = run_onset_shuffle(herbal_lines, TARGET_CHAIN)

    print(f"  Section-shuffled: real_js={real_js_sec:.4f} at {pct_sec:.1f}th percentile")
    print(f"  Onset-shuffled:   real_js={real_js_ons:.4f} at {pct_ons:.1f}th percentile")

    f4_retained = (pct_sec > 95.0) and (pct_ons > 95.0)
    f4_status = 'RETAINED' if f4_retained else 'FAILED'
    print(f"  Pre-reg threshold: >95th pct both controls. Result: {f4_status}")

    # ── F5: Systematic -edy suffix transformation ─────────────────────────────
    sep()
    print("\n[F5] Systematic -edy suffix transformation")
    print("     v101: B-suffix = {c89, cc89, C89} (EVA: edy, eedy)")
    print("     v101: A-suffix = {oe, oy, c9} (EVA: ol, or, ey)")
    print(f"     Transform: B-suffix rate in B ≥{B_SUFFIX_FOLD_THRESHOLD}×rate in A AND ≥{B_SUFFIX_ABS_THRESHOLD*100:.0f}% abs")

    f5_results = suffix_transformation_analysis(v101_a, v101_b)

    print(f"\n  {'Class':<8} {'A:Bsuf':<10} {'B:Bsuf':<10} {'fold':<8} Transforms")
    print(f"  {'-'*8} {'-'*10} {'-'*10} {'-'*8} ----------")
    n_transforms = 0
    n_tested = 0
    for cls in ALL_ONSET_CLASSES:
        r = f5_results[cls]
        if r is None:
            print(f"  {cls:<8} — (insufficient data)")
            continue
        n_tested += 1
        t = 'YES' if r['shows_transform'] else 'NO'
        if r['shows_transform']: n_transforms += 1
        fold_s = str(r['fold']) if r['fold'] != '∞' else '∞'
        print(f"  {cls:<8} {r['a_bsuf']:<10.3f} {r['b_bsuf']:<10.3f} {fold_s+'×':<8} {t}")

    pct_transform = 100.0 * n_transforms / n_tested if n_tested else 0
    print(f"\n  Transforms: {n_transforms}/{n_tested} = {pct_transform:.1f}%")
    f5_status = ('RETAINED' if pct_transform >= 75.0
                 else ('WEAKENED' if pct_transform >= 50.0 else 'FAILED'))
    print(f"  Pre-reg threshold: ≥75%. Result: {f5_status}")

    # ── Summary ───────────────────────────────────────────────────────────────
    sep('═')
    print("\n[SUMMARY] v101 Replication Results")
    sep('═')
    statuses = {
        'F1 Positional architecture': f1_status,
        'F2 Terminal inversion':       f2_status,
        'F3 Bigram invariants':        f3_status,
        'F4 A-herbal chain':           f4_status,
        'F5 Suffix transformation':    f5_status,
    }
    for name, st in statuses.items():
        print(f"  {name:<30} {st}")

    all_retained = all(s == 'RETAINED' for s in statuses.values())
    gate_status = 'ALL_RETAINED' if all_retained else 'PARTIAL'
    print(f"\n  R2 GATE: {gate_status}")
    if all_retained:
        print("  → Proceed to: Final summary (R1+R2 both RETAINED; ZL3a not needed)")
    else:
        failed = [k for k, v in statuses.items() if v != 'RETAINED']
        print(f"  → WEAKENED/FAILED: {failed}")
        print("  → R3 (ZL3a) required as tiebreaker per pre-registration §2.3")

if __name__ == '__main__':
    main()
