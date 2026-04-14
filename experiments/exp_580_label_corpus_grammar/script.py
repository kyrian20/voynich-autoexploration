#!/usr/bin/env python3
"""
exp_580: Label corpus grammar investigation
Characterizes structural properties of VMS label text vs body text.
"""

import re
import sys
from collections import Counter, defaultdict
import math

TRANSCRIPTION = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

# ─── EVA onset classification (canonical, from exp_565/566/etc.) ─────────────
def get_onset(word):
    """Return onset class for an EVA word (canonical classification)."""
    w = word.lower()
    # Order matters: check longer prefixes first
    if w.startswith('qok'):    return 'qok'
    if w.startswith('qot'):    return 'qot'
    if w.startswith('qo'):     return 'qo'
    if w.startswith('cth'):    return 'cth'
    if w.startswith('ckh'):    return 'ckh'
    if w.startswith('cph'):    return 'cph'
    if w.startswith('sch'):    return 'sch'
    if w.startswith('ch'):     return 'ch'
    if w.startswith('sh'):     return 'sh'
    if w.startswith('ok'):     return 'ok'
    if w.startswith('ol'):     return 'ol'
    if w.startswith('ot'):     return 'ot'
    if w.startswith('of'):     return 'of'
    if w.startswith('or'):     return 'or'
    if w.startswith('o'):      return 'o'
    if w.startswith('d'):      return 'd'
    if w.startswith('y'):      return 'y'
    if w.startswith('s'):      return 's'
    if w.startswith('t'):      return 't'
    if w.startswith('k'):      return 'k'
    if w.startswith('p'):      return 'p'
    if w.startswith('f'):      return 'f'
    if w.startswith('l'):      return 'l'
    if w.startswith('r'):      return 'r'
    if w.startswith('a'):      return 'a'
    if w.startswith('e'):      return 'e'
    if w.startswith('i'):      return 'i'
    if w.startswith('n'):      return 'n'
    return 'other'

def has_am_suffix(word):
    w = word.lower()
    return w.endswith('am') or w.endswith('aiin')

def get_suffix_class(word):
    """Broad suffix classification."""
    w = word.lower()
    if w.endswith('aiin'): return 'aiin'
    if w.endswith('ain'):  return 'ain'
    if w.endswith('am'):   return 'am'
    if w.endswith('edy'):  return 'edy'
    if w.endswith('dy'):   return 'dy'
    if w.endswith('ey'):   return 'ey'
    if w.endswith('y'):    return 'y'
    if w.endswith('ol'):   return 'ol'
    if w.endswith('al'):   return 'al'
    if w.endswith('or'):   return 'or'
    if w.endswith('ar'):   return 'ar'
    if w.endswith('ly'):   return 'ly'
    if w.endswith('in'):   return 'in'
    if w.endswith('r'):    return 'r'
    return 'other'

# ─── Parse ZL3b ───────────────────────────────────────────────────────────────
# Label locus codes: lines starting with L or radial R (Ri, Ro)
LABEL_CODE_RE = re.compile(r'^[&@*+=~][LR][^P]')

def is_body_code(code):
    return bool(re.match(r'^[&@*+=~]P', code))

def is_label_code(code):
    return bool(LABEL_CODE_RE.match(code))

def parse_eva_tokens(text_line):
    """Parse EVA tokens from a transcription line. Returns list of clean tokens."""
    # Remove special markup: <...>, {...}, [...alternatives...], @codes;
    # Remove uncertainty markers and non-token content
    line = text_line.strip()
    # Remove location prefix like <f2r.14,@L0>
    line = re.sub(r'<f[^>]+>', '', line)
    # Remove comments and special codes
    line = re.sub(r'<!.*?>', '', line)
    line = re.sub(r'<\$>', '', line)    # paragraph end marker
    line = re.sub(r'<%>', '', line)     # paragraph start marker
    # Handle uncertainty: {a:b} → a (take first alternative)
    line = re.sub(r'\{([^}:]+):[^}]+\}', r'\1', line)
    line = re.sub(r'\{([^}]+)\}', r'\1', line)
    # Handle [a:b] alternations → a (take first)
    line = re.sub(r'\[([^\]:|]+)[:|][^\]]+\]', r'\1', line)
    line = re.sub(r'\[([^\]]+)\]', r'\1', line)
    # Remove uncertainty ? marks attached to characters
    line = re.sub(r'\?', '', line)
    # Remove non-Voynich markers and other special chars
    line = re.sub(r'@\d+;', '', line)
    line = re.sub(r'[<>{}]', '', line)
    # Remove line-internal hyphen (word break markers)
    line = re.sub(r'<->', '', line)
    # Remove leading/trailing whitespace and continuation marks
    line = line.strip()
    # Split on word separators: period, comma, space
    tokens = re.split(r'[.,\s\-]+', line)
    # Filter: lowercase alphabetic tokens, length >= 2
    clean = []
    for t in tokens:
        t = t.lower().strip()
        if len(t) >= 2 and re.match(r'^[a-z]+$', t):
            clean.append(t)
    return clean

def edy_rate(tokens):
    """Fraction of tokens ending with 'edy' or starting with edy-like pattern."""
    if not tokens:
        return 0.0
    return sum(1 for t in tokens if t.endswith('edy') or t.endswith('dy') or t.endswith('ey')) / len(tokens)

def dialect_of_line(tokens):
    """Classify a line as A or B by edy-rate (per-line canonical method)."""
    if not tokens:
        return None
    er = edy_rate(tokens)
    if er >= 0.05:
        return 'B'
    return 'A'

# ─── Parse the full transcription ────────────────────────────────────────────
print("Parsing ZL3b transcription...")

# For dialect assignment we'll also use the $L= folio-level language tag
folio_lang = {}
folio_section = {}

# Data structures for labels and body
label_lines = []    # (folio, locus_code, tokens, folio_lang)
body_lines = []     # (folio, locus_code, tokens, folio_lang)

current_folio = None
current_lang = None  # from $L= tag
current_section = None  # from $P= tag (section identifier)

line_re = re.compile(r'^<(f[^.]+\.[^,]+),([^>]+)>\s+(.*)')
folio_header_re = re.compile(r'<(f[^>]+)>')
lang_re = re.compile(r'\$L=([A-Z])')
section_re = re.compile(r'\$P=([A-Z])')

with open(TRANSCRIPTION, 'r', encoding='utf-8', errors='replace') as f:
    raw_lines = f.readlines()

for raw in raw_lines:
    raw = raw.rstrip('\n')

    # Check for folio header
    fh = folio_header_re.search(raw)
    if fh and '<!' in raw and '$' in raw:
        folio_id = fh.group(1)
        current_folio = folio_id
        lang_m = lang_re.search(raw)
        if lang_m:
            current_lang = lang_m.group(1)
            folio_lang[folio_id] = current_lang
        sec_m = section_re.search(raw)
        if sec_m:
            current_section = sec_m.group(1)
            folio_section[folio_id] = current_section
        continue

    # Check for text line
    m = line_re.match(raw)
    if not m:
        continue

    location = m.group(1)
    locus = m.group(2).strip()
    text = m.group(3)

    # Extract folio from location
    folio_m = re.match(r'(f\S+?)\.', location)
    if folio_m:
        this_folio = folio_m.group(1)
    else:
        this_folio = current_folio

    lang = folio_lang.get(this_folio, current_lang)

    tokens = parse_eva_tokens(text)
    if not tokens:
        continue

    if is_label_code(locus):
        label_lines.append((this_folio, locus, tokens, lang))
    elif is_body_code(locus):
        body_lines.append((this_folio, locus, tokens, lang))

print(f"Label lines: {len(label_lines)}")
print(f"Body lines: {len(body_lines)}")

# ─── Label corpus: section classification ────────────────────────────────────
# Classify labels by section based on locus code second char + folio
def label_section(folio, locus):
    """Classify label into a section category."""
    lc = locus[1:]  # after @ or & etc.
    if lc.startswith('Lz') or lc.startswith('Lz'):
        return 'zodiac'
    if lc.startswith('La'):
        return 'zodiac'
    if lc.startswith('Ls'):
        return 'star'
    if lc.startswith('Ln'):
        return 'balneo'
    if lc.startswith('Lt'):
        return 'pharma'
    if lc.startswith('Lf'):
        return 'cosmo_large'
    if lc.startswith('Lc'):
        return 'circular'
    if lc.startswith('Lp'):
        return 'herbal_plant'
    if lc.startswith('Ri') or lc.startswith('Ro'):
        return 'radial'
    # L0: determine from folio number
    # f1-f72 = herbal; f73-f84 = bio? Actually use folio range
    fm = re.match(r'f(\d+)', folio)
    if fm:
        fn = int(fm.group(1))
        if fn <= 72:
            return 'herbal'
        elif fn <= 84:
            return 'bio'
        elif fn <= 102:
            return 'astro_generic'
        else:
            return 'pharma_generic'
    return 'unknown'

# Assign sections
label_sections = [label_section(f, l) for f, l, _, _ in label_lines]
from collections import Counter
sec_counts = Counter(label_sections)
print("\nLabel sections:")
for k, v in sec_counts.most_common():
    print(f"  {k}: {v} lines")

# ─── Basic stats ─────────────────────────────────────────────────────────────
all_label_tokens = [t for _, _, toks, _ in label_lines for t in toks]
all_body_tokens = [t for _, _, toks, _ in body_lines for t in toks]

print(f"\n=== CORPUS SIZES ===")
print(f"Label lines: {len(label_lines)}, tokens: {len(all_label_tokens)}")
print(f"Body lines: {len(body_lines)}, tokens: {len(all_body_tokens)}")
print(f"Label unique types: {len(set(all_label_tokens))}")
print(f"Body unique types: {len(set(all_body_tokens))}")

# ─── Token length distributions ──────────────────────────────────────────────
print(f"\n=== TOKEN LENGTH ===")
label_lengths = [len(t) for t in all_label_tokens]
body_lengths = [len(t) for t in all_body_tokens]
print(f"Label mean length: {sum(label_lengths)/len(label_lengths):.3f}")
print(f"Body mean length: {sum(body_lengths)/len(body_lengths):.3f}")
for n in [3, 4, 5, 6, 7, 8, 9]:
    lf = sum(1 for l in label_lengths if l == n) / len(label_lengths)
    bf = sum(1 for l in body_lengths if l == n) / len(body_lengths)
    print(f"  len={n}: label={lf:.3f}, body={bf:.3f}")

# ─── Vocabulary overlap ───────────────────────────────────────────────────────
print(f"\n=== VOCABULARY OVERLAP ===")
label_vocab = set(all_label_tokens)
body_vocab = set(all_body_tokens)
overlap = label_vocab & body_vocab
print(f"Label types: {len(label_vocab)}")
print(f"Body types: {len(body_vocab)}")
print(f"Overlap (label ∩ body): {len(overlap)}")
print(f"Fraction of label types in body vocab: {len(overlap)/len(label_vocab):.3f}")
label_tok_in_body = sum(1 for t in all_label_tokens if t in body_vocab)
print(f"Fraction of label tokens in body vocab: {label_tok_in_body/len(all_label_tokens):.3f}")
print(f"Label-exclusive types: {len(label_vocab - body_vocab)}")

# ─── Onset class distribution ────────────────────────────────────────────────
print(f"\n=== ONSET CLASS DISTRIBUTION ===")
label_onsets = Counter(get_onset(t) for t in all_label_tokens)
body_onsets = Counter(get_onset(t) for t in all_body_tokens)
total_label = len(all_label_tokens)
total_body = len(all_body_tokens)

top_onsets = [k for k, _ in body_onsets.most_common(20)]
print(f"{'Onset':8s} {'Label%':8s} {'Body%':8s} {'Ratio':8s}")
for o in top_onsets:
    lp = label_onsets.get(o, 0) / total_label
    bp = body_onsets.get(o, 0) / total_body
    ratio = lp / bp if bp > 0 else float('inf')
    print(f"{o:8s} {lp:.4f}   {bp:.4f}   {ratio:.3f}x")

# ─── Suffix paradigm distribution ────────────────────────────────────────────
print(f"\n=== SUFFIX CLASS DISTRIBUTION ===")
label_suffixes = Counter(get_suffix_class(t) for t in all_label_tokens)
body_suffixes = Counter(get_suffix_class(t) for t in all_body_tokens)
top_suffixes = [k for k, _ in body_suffixes.most_common(12)]
print(f"{'Suffix':8s} {'Label%':8s} {'Body%':8s} {'Ratio':8s}")
for s in top_suffixes:
    lp = label_suffixes.get(s, 0) / total_label
    bp = body_suffixes.get(s, 0) / total_body
    ratio = lp / bp if bp > 0 else float('inf')
    print(f"{s:8s} {lp:.4f}   {bp:.4f}   {ratio:.3f}x")

# ─── Dialect membership of labels ────────────────────────────────────────────
print(f"\n=== LABEL DIALECT MEMBERSHIP ===")
# Per-line edy-rate dialect assignment
label_dialects = []
for (f, lc, toks, folio_lang_val) in label_lines:
    d = dialect_of_line(toks)
    label_dialects.append(d)

dialect_counts = Counter(label_dialects)
print(f"Label lines by per-line dialect (edy-rate ≥0.05 = B):")
print(f"  A: {dialect_counts.get('A', 0)} ({dialect_counts.get('A',0)/len(label_dialects):.3f})")
print(f"  B: {dialect_counts.get('B', 0)} ({dialect_counts.get('B',0)/len(label_dialects):.3f})")
print(f"  None (no tokens): {dialect_counts.get(None, 0)}")

# Check by folio-level $L= assignment
folio_lang_label = Counter(folio_lang.get(f, 'unknown') for f, _, _, _ in label_lines)
print(f"Label lines by folio $L= tag:")
for k, v in folio_lang_label.most_common():
    print(f"  {k}: {v}")

# ─── Dialect features: do A-folio labels show A-dialect markers? ─────────────
print(f"\n=== DIALECT FEATURE TEST ===")
# B-dialect marker: edy suffix
# A-dialect: lower edy rate
a_folio_label_tokens = [t for f, lc, toks, lng in label_lines if lng == 'A' for t in toks]
b_folio_label_tokens = [t for f, lc, toks, lng in label_lines if lng == 'B' for t in toks]
a_body_tokens = [t for f, lc, toks, lng in body_lines if lng == 'A' for t in toks]
b_body_tokens = [t for f, lc, toks, lng in body_lines if lng == 'B' for t in toks]

def edy_frac(tokens):
    if not tokens: return float('nan')
    return sum(1 for t in tokens if t.endswith('edy') or t.endswith('dy')) / len(tokens)

print(f"A-folio labels: {len(a_folio_label_tokens)} tokens, edy-frac={edy_frac(a_folio_label_tokens):.4f}")
print(f"B-folio labels: {len(b_folio_label_tokens)} tokens, edy-frac={edy_frac(b_folio_label_tokens):.4f}")
print(f"A body: {len(a_body_tokens)} tokens, edy-frac={edy_frac(a_body_tokens):.4f}")
print(f"B body: {len(b_body_tokens)} tokens, edy-frac={edy_frac(b_body_tokens):.4f}")

# ─── Positional grammar: labels too short for LF/LL, but check per-label ─────
print(f"\n=== MULTI-WORD LABEL ANALYSIS ===")
# Lines with 2+ tokens
multi_word_labels = [(f, lc, toks, lng) for f, lc, toks, lng in label_lines if len(toks) >= 2]
print(f"Multi-word label lines (≥2 tokens): {len(multi_word_labels)}")
print(f"Total label lines: {len(label_lines)}")
print(f"Single-token labels: {sum(1 for _, _, t, _ in label_lines if len(t) == 1)}")

# For multi-word labels, compute LF/LL onset distribution
if multi_word_labels:
    lf_onsets = Counter(get_onset(toks[0]) for _, _, toks, _ in multi_word_labels)
    ll_onsets = Counter(get_onset(toks[-1]) for _, _, toks, _ in multi_word_labels)

    # am LL enrichment in labels
    am_ll_label = sum(1 for _, _, t, _ in multi_word_labels if t[-1].endswith('am') or t[-1].endswith('aiin')) / len(multi_word_labels)
    am_all_label = sum(1 for t in all_label_tokens if t.endswith('am') or t.endswith('aiin')) / len(all_label_tokens)

    am_ll_body = sum(1 for _, _, t, _ in body_lines if t and (t[-1].endswith('am') or t[-1].endswith('aiin'))) / len(body_lines)
    am_all_body = sum(1 for t in all_body_tokens if t.endswith('am') or t.endswith('aiin')) / len(all_body_tokens)

    print(f"\n-am LL enrichment (multi-word labels):")
    print(f"  Label: LL rate={am_ll_label:.4f}, overall rate={am_all_label:.4f}, enrichment={am_ll_label/am_all_label:.3f}x" if am_all_label>0 else "  Label: no -am tokens")
    print(f"  Body:  LL rate={am_ll_body:.4f}, overall rate={am_all_body:.4f}, enrichment={am_ll_body/am_all_body:.3f}x" if am_all_body>0 else "  Body: no -am tokens")

    print(f"\ny-onset LF enrichment (multi-word labels):")
    y_lf_label = lf_onsets.get('y', 0) / len(multi_word_labels)
    y_all_label = label_onsets.get('y', 0) / total_label
    y_lf_body_n = sum(1 for _, _, t, _ in body_lines if t and get_onset(t[0]) == 'y')
    y_lf_body = y_lf_body_n / len(body_lines)
    print(f"  Label: LF rate={y_lf_label:.4f}, overall rate={y_all_label:.4f}, enrichment={y_lf_label/y_all_label:.3f}x" if y_all_label > 0 else "  Label: no y-onset")
    print(f"  Body:  LF rate={y_lf_body:.4f}, overall rate={body_onsets.get('y',0)/total_body:.4f}, enrichment={y_lf_body/(body_onsets.get('y',0)/total_body):.3f}x")

    print(f"\nTop 5 LF onsets (multi-word labels):")
    for k, v in lf_onsets.most_common(5):
        lf_rate = v / len(multi_word_labels)
        base_rate = label_onsets.get(k, 0) / total_label
        print(f"  {k}: count={v}, LF_rate={lf_rate:.4f}, base_rate={base_rate:.4f}, E={lf_rate/base_rate:.3f}x" if base_rate > 0 else f"  {k}: count={v}")

    print(f"\nTop 5 LL onsets (multi-word labels):")
    for k, v in ll_onsets.most_common(5):
        ll_rate = v / len(multi_word_labels)
        base_rate = label_onsets.get(k, 0) / total_label
        print(f"  {k}: count={v}, LL_rate={ll_rate:.4f}, base_rate={base_rate:.4f}, E={ll_rate/base_rate:.3f}x" if base_rate > 0 else f"  {k}: count={v}")

# ─── Onset self-succession in multi-word labels ───────────────────────────────
print(f"\n=== ONSET SELF-SUCCESSION (multi-word labels) ===")
# Compute self-succession within each multi-word label
ss_pairs = []
total_pairs = 0
same_onset_pairs = 0
onset_pair_counts = defaultdict(lambda: defaultdict(int))

for _, _, toks, _ in multi_word_labels:
    for i in range(len(toks)-1):
        o1 = get_onset(toks[i])
        o2 = get_onset(toks[i+1])
        onset_pair_counts[o1][o2] += 1
        total_pairs += 1
        if o1 == o2:
            same_onset_pairs += 1

print(f"Total within-label bigram pairs: {total_pairs}")
print(f"Same-onset consecutive pairs: {same_onset_pairs} ({same_onset_pairs/total_pairs:.4f} if total_pairs > 0)")

if total_pairs > 0:
    # Expected self-succession rate from marginal frequencies
    onset_counts = Counter(get_onset(t) for _, _, toks, _ in multi_word_labels for t in toks)
    total_onset = sum(onset_counts.values())
    expected_ss = sum((c/total_onset)**2 for c in onset_counts.values())
    observed_ss = same_onset_pairs / total_pairs
    print(f"Expected SS rate (random): {expected_ss:.4f}")
    print(f"Observed SS rate: {observed_ss:.4f}")
    print(f"SS enrichment: {observed_ss/expected_ss:.3f}x")

    # Per-onset self-succession
    print(f"\nPer-onset self-succession (obs≥5):")
    for onset in sorted(onset_pair_counts.keys()):
        total_sent = sum(onset_pair_counts[onset].values())
        self_succ = onset_pair_counts[onset][onset]
        if total_sent >= 5:
            obs_rate = self_succ / total_sent
            # Body rate for comparison
            body_onset_rate = body_onsets.get(onset, 0) / total_body
            expected_rate = body_onset_rate  # approximate
            print(f"  {onset}: {self_succ}/{total_sent} = {obs_rate:.4f}")

# ─── Bigram patterns in multi-word labels ─────────────────────────────────────
print(f"\n=== ONSET BIGRAMS (multi-word labels, obs≥5) ===")
# Compare label bigrams to body bigrams
body_bigrams = defaultdict(Counter)
for _, _, toks, _ in body_lines:
    for i in range(len(toks)-1):
        o1 = get_onset(toks[i])
        o2 = get_onset(toks[i+1])
        body_bigrams[o1][o2] += 1

# Show top label bigrams vs body rates
print("Top label onset bigrams:")
flat_label_bigrams = [(o1, o2, c) for o1 in onset_pair_counts for o2, c in onset_pair_counts[o1].items()]
flat_label_bigrams.sort(key=lambda x: -x[2])
for o1, o2, c in flat_label_bigrams[:15]:
    label_rate = c / sum(onset_pair_counts[o1].values()) if sum(onset_pair_counts[o1].values()) > 0 else 0
    body_total = sum(body_bigrams[o1].values())
    body_rate = body_bigrams[o1][o2] / body_total if body_total > 0 else 0
    ratio = label_rate / body_rate if body_rate > 0 else float('inf')
    print(f"  {o1}→{o2}: label {c} ({label_rate:.3f}), body_rate={body_rate:.3f}, ratio={ratio:.2f}x")

# ─── Per-section breakdown ────────────────────────────────────────────────────
print(f"\n=== PER-SECTION BREAKDOWN ===")
section_data = defaultdict(list)
for (f, lc, toks, lng), sec in zip(label_lines, label_sections):
    section_data[sec].extend(toks)

for sec in sorted(section_data.keys()):
    toks = section_data[sec]
    if not toks:
        continue
    onset_dist = Counter(get_onset(t) for t in toks)
    edy = edy_frac(toks)
    mean_len = sum(len(t) for t in toks) / len(toks)
    top3 = [(k, v/len(toks)) for k, v in onset_dist.most_common(3)]
    print(f"  {sec}: {len(toks)} tokens, mean_len={mean_len:.2f}, edy={edy:.4f}, top3_onsets={top3}")

# ─── Comparing B-folio label onsets to B body onsets ─────────────────────────
print(f"\n=== B-DIALECT FOLIO LABELS vs BODY ===")
b_label_tokens = [t for f, lc, toks, lng in label_lines if lng == 'B' for t in toks]
b_body_tok_list = [t for f, lc, toks, lng in body_lines if lng == 'B' for t in toks]

if b_label_tokens and b_body_tok_list:
    b_label_onsets = Counter(get_onset(t) for t in b_label_tokens)
    b_body_onsets = Counter(get_onset(t) for t in b_body_tok_list)
    total_bl = len(b_label_tokens)
    total_bb = len(b_body_tok_list)
    print(f"B-folio labels: {total_bl} tokens; B body: {total_bb} tokens")
    top_b = [k for k, _ in b_body_onsets.most_common(12)]
    print(f"{'Onset':8s} {'B-Label%':10s} {'B-Body%':10s} {'Ratio':8s}")
    for o in top_b:
        lp = b_label_onsets.get(o, 0) / total_bl
        bp = b_body_onsets.get(o, 0) / total_bb
        ratio = lp / bp if bp > 0 else float('inf')
        print(f"{o:8s} {lp:.4f}     {bp:.4f}     {ratio:.3f}x")

print("\n=== SUMMARY STATISTICS ===")
print(f"Total label lines: {len(label_lines)}")
print(f"Total label tokens: {len(all_label_tokens)}")
print(f"Label unique types: {len(label_vocab)}")
print(f"Single-token label lines: {sum(1 for _, _, t, _ in label_lines if len(t) == 1)} ({sum(1 for _, _, t, _ in label_lines if len(t) == 1)/len(label_lines):.3f})")
print(f"Multi-word label lines: {len(multi_word_labels)} ({len(multi_word_labels)/len(label_lines):.3f})")
print("Done.")
