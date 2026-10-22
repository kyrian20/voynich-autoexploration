"""
exp_326: ch↔sh Mutual Avoidance — Section-Level vs Grammar-Level Mechanism (H527)

Question: Is the ch↔sh bidirectional avoidance (B-dialect: ch→sh 0.567×, sh→ch 0.555×)
explained by section-level clustering (ch and sh appear in different sections),
or is it a genuine sequential grammar rule that persists even within mixed-onset lines?

Two tests:
  1. Section analysis: ch/sh frequency per section (herbal/pharma/astro/bio/cosmo/stars/text)
     If ch concentrates in sections where sh is rare, that explains the bigram avoidance.
  2. Within-mixed-line analysis: among lines containing at least one ch-onset AND at least
     one sh-onset word, compute ch→sh and sh→ch bigram enrichment within those lines only.
     If avoidance persists within mixed-onset lines, it's a sequential grammar rule.
"""
from pathlib import Path as _RepositoryPath

import os, re, math
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

def infer_section(fb):
    """Infer manuscript section from folio base string."""
    m = re.match(r'f(\d+)', fb.lower())
    if not m:
        return 'unknown'
    n = int(m.group(1))
    # Standard VMS section assignments
    if n <= 57:
        return 'herbal'
    elif n <= 73:
        return 'astro'
    elif n <= 84:
        return 'bio'
    elif n <= 86:
        return 'cosmo'
    elif n <= 102:
        return 'pharma'
    else:
        return 'stars_text'

def parse_vms():
    # Pass 1: determine folio dialect
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

    # Pass 2: collect line-level data
    # Each record: (fb, dialect, section, line_words, locus_code)
    line_records = []
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
            section = infer_section(fb)
            line_records.append((fb, dialect, section, words))

    return line_records, folio_dialect

print("Loading corpus...")
line_records, folio_dialect = parse_vms()
print(f"Loaded {len(line_records)} paragraph lines")

b_lines = [(fb, sect, words) for fb, d, sect, words in line_records if d == 'B']
a_lines = [(fb, sect, words) for fb, d, sect, words in line_records if d == 'A']
print(f"B lines: {len(b_lines)}, A lines: {len(a_lines)}")

# ---- TEST 1: Section-level ch/sh frequency ----
print("\n" + "="*70)
print("TEST 1: ch/sh Frequency by Section")
print("="*70)

def section_onset_table(lines, label):
    """Compute per-section onset frequency for ch and sh."""
    # Use MID words only (pos 1 to n-2)
    section_counts = defaultdict(Counter)
    for fb, sect, words in lines:
        mid = words[1:-1]
        for w in mid:
            o = get_onset(w)
            section_counts[sect][o] += 1

    print(f"\n{label}")
    print(f"{'Section':<15} {'ch':>6} {'sh':>6} {'total':>7} {'%ch':>6} {'%sh':>6} {'ch/(ch+sh)':>12}")
    print("-"*65)
    for sect in sorted(section_counts.keys()):
        ctr = section_counts[sect]
        total = sum(ctr.values())
        ch = ctr.get('ch', 0)
        sh = ctr.get('sh', 0)
        pch = 100 * ch / total if total > 0 else 0
        psh = 100 * sh / total if total > 0 else 0
        ratio = ch / (ch + sh) if (ch + sh) > 0 else float('nan')
        print(f"{sect:<15} {ch:>6} {sh:>6} {total:>7} {pch:>6.1f}% {psh:>6.1f}% {ratio:>12.3f}")

    # Summary: what is section-level variance of ch/sh ratio?
    ratios = []
    for sect, ctr in section_counts.items():
        ch = ctr.get('ch', 0)
        sh = ctr.get('sh', 0)
        if (ch + sh) >= 10:
            ratios.append(ch / (ch + sh))
    if ratios:
        mean_r = sum(ratios) / len(ratios)
        var_r = sum((r - mean_r)**2 for r in ratios) / len(ratios)
        print(f"\nSection ch/(ch+sh) ratios: {[f'{r:.3f}' for r in ratios]}")
        print(f"Mean: {mean_r:.3f}, Std: {var_r**0.5:.3f}")
        print(f"Low std → ch/sh is UNIFORM across sections (not section-segregated)")
        print(f"High std → ch/sh varies by section (section segregation may explain avoidance)")

    return section_counts

b_sect = section_onset_table(b_lines, "B-DIALECT")
a_sect = section_onset_table(a_lines, "A-DIALECT")

# ---- TEST 2: Within-mixed-line bigram analysis ----
print("\n" + "="*70)
print("TEST 2: ch↔sh Bigram Enrichment Within Mixed-Onset Lines")
print("="*70)

def analyze_mixed_lines(lines, label):
    """
    For lines containing both ch and sh onset words:
    Compare ch→sh and sh→ch bigram enrichment WITHIN those lines vs global baseline.
    """
    # Classify lines
    mixed_lines_data = []  # lines with both ch and sh
    ch_only_lines = 0
    sh_only_lines = 0
    neither_lines = 0

    for fb, sect, words in lines:
        mid = words[1:-1]
        onsets = [get_onset(w) for w in mid]
        has_ch = 'ch' in onsets
        has_sh = 'sh' in onsets

        if has_ch and has_sh:
            mixed_lines_data.append((fb, sect, mid, onsets))
        elif has_ch:
            ch_only_lines += 1
        elif has_sh:
            sh_only_lines += 1
        else:
            neither_lines += 1

    total = len(lines)
    print(f"\n--- {label} ---")
    print(f"Total lines: {total}")
    print(f"Mixed (ch+sh): {len(mixed_lines_data)} ({100*len(mixed_lines_data)/total:.1f}%)")
    print(f"ch-only: {ch_only_lines} ({100*ch_only_lines/total:.1f}%)")
    print(f"sh-only: {sh_only_lines} ({100*sh_only_lines/total:.1f}%)")
    print(f"neither: {neither_lines} ({100*neither_lines/total:.1f}%)")

    # Global bigram counts (MID words, all lines)
    global_bigrams = Counter()
    global_onset_counts = Counter()
    for fb, sect, words in lines:
        mid = words[1:-1]
        onsets = [get_onset(w) for w in mid]
        for o in onsets:
            global_onset_counts[o] += 1
        for i in range(len(onsets)-1):
            global_bigrams[(onsets[i], onsets[i+1])] += 1

    def compute_enrichment(bigrams, onset_counts, o1, o2):
        total_onsets = sum(onset_counts.values())
        obs = bigrams.get((o1, o2), 0)
        exp = onset_counts[o1] * onset_counts[o2] / total_onsets if total_onsets > 0 else 0
        enr = obs / exp if exp > 0 else float('nan')
        return obs, exp, enr

    print(f"\nGlobal enrichment (all lines, baseline from exp_324):")
    for o1, o2 in [('ch','sh'), ('sh','ch'), ('ch','ch'), ('sh','sh'), ('ch','qok'), ('sh','qok')]:
        obs, exp, enr = compute_enrichment(global_bigrams, global_onset_counts, o1, o2)
        print(f"  {o1}→{o2}: obs={obs}, exp={exp:.1f}, E={enr:.3f}×")

    # Mixed-line bigrams
    mixed_bigrams = Counter()
    mixed_onset_counts = Counter()
    for fb, sect, mid, onsets in mixed_lines_data:
        for o in onsets:
            mixed_onset_counts[o] += 1
        for i in range(len(onsets)-1):
            mixed_bigrams[(onsets[i], onsets[i+1])] += 1

    print(f"\nWithin MIXED lines only (lines containing BOTH ch and sh):")
    print(f"(N mixed lines = {len(mixed_lines_data)}, total MID words in mixed lines = {sum(mixed_onset_counts.values())})")
    for o1, o2 in [('ch','sh'), ('sh','ch'), ('ch','ch'), ('sh','sh'), ('ch','qok'), ('sh','qok')]:
        obs, exp, enr = compute_enrichment(mixed_bigrams, mixed_onset_counts, o1, o2)
        print(f"  {o1}→{o2}: obs={obs}, exp={exp:.1f}, E={enr:.3f}×")

    # For interpretation: if avoidance persists (E<1) in mixed lines, it's grammatical
    ch_sh_mixed_obs = mixed_bigrams.get(('ch','sh'), 0)
    sh_ch_mixed_obs = mixed_bigrams.get(('sh','ch'), 0)
    ch_mixed = mixed_onset_counts.get('ch', 0)
    sh_mixed = mixed_onset_counts.get('sh', 0)
    total_mixed_onsets = sum(mixed_onset_counts.values())
    if total_mixed_onsets > 0:
        exp_ch_sh = ch_mixed * sh_mixed / total_mixed_onsets
        exp_sh_ch = sh_mixed * ch_mixed / total_mixed_onsets
        print(f"\nInterpretation:")
        if exp_ch_sh > 0:
            print(f"  ch→sh mixed-line E = {ch_sh_mixed_obs/exp_ch_sh:.3f}×")
        if exp_sh_ch > 0:
            print(f"  sh→ch mixed-line E = {sh_ch_mixed_obs/exp_sh_ch:.3f}×")
        if exp_ch_sh > 0 and exp_sh_ch > 0:
            avg_e = ((ch_sh_mixed_obs/exp_ch_sh) + (sh_ch_mixed_obs/exp_sh_ch)) / 2
            if avg_e < 0.8:
                print(f"  → Avoidance PERSISTS in mixed lines (avg E={avg_e:.3f}) = GRAMMATICAL RULE")
            elif avg_e > 0.9:
                print(f"  → Avoidance DISAPPEARS in mixed lines (avg E={avg_e:.3f}) = SECTION ARTIFACT")
            else:
                print(f"  → Ambiguous (avg E={avg_e:.3f})")

    return mixed_lines_data

b_mixed = analyze_mixed_lines(b_lines, "B-DIALECT")
a_mixed = analyze_mixed_lines(a_lines, "A-DIALECT")

# ---- TEST 3: Within mixed lines — look at actual bigram sequences ----
print("\n" + "="*70)
print("TEST 3: Mixed-Line ch/sh Word Ordering Patterns")
print("="*70)

def show_mixed_line_patterns(mixed_lines_data, label, n_show=20):
    """Show actual ch/sh word ordering in mixed lines."""
    print(f"\n--- {label} (showing up to {n_show} mixed lines) ---")

    # Track: how often ch comes BEFORE sh vs AFTER sh in the same line?
    ch_before_sh = 0
    sh_before_ch = 0
    interleaved = 0

    for fb, sect, mid, onsets in mixed_lines_data[:n_show]:
        ch_positions = [i for i, o in enumerate(onsets) if o == 'ch']
        sh_positions = [i for i, o in enumerate(onsets) if o == 'sh']
        onset_str = ' '.join(onsets)
        print(f"  {fb} [{sect}]: {onset_str}")

    # Full count
    for fb, sect, mid, onsets in mixed_lines_data:
        ch_positions = [i for i, o in enumerate(onsets) if o == 'ch']
        sh_positions = [i for i, o in enumerate(onsets) if o == 'sh']
        first_ch = min(ch_positions)
        first_sh = min(sh_positions)
        last_ch = max(ch_positions)
        last_sh = max(sh_positions)

        if first_ch < first_sh and last_ch < last_sh:
            ch_before_sh += 1
        elif first_sh < first_ch and last_sh < last_ch:
            sh_before_ch += 1
        else:
            interleaved += 1

    total_mixed = len(mixed_lines_data)
    print(f"\n  All-ch-before-sh: {ch_before_sh} ({100*ch_before_sh/total_mixed:.1f}%)")
    print(f"  All-sh-before-ch: {sh_before_ch} ({100*sh_before_ch/total_mixed:.1f}%)")
    print(f"  Interleaved: {interleaved} ({100*interleaved/total_mixed:.1f}%)")

if b_mixed:
    show_mixed_line_patterns(b_mixed, "B-DIALECT")
if a_mixed:
    show_mixed_line_patterns(a_mixed, "A-DIALECT")

# ---- TEST 4: ch/sh ratio by folio (B-dialect) ----
print("\n" + "="*70)
print("TEST 4: Folio-Level ch vs sh Specialization (B-Dialect)")
print("="*70)

folio_ch_sh = defaultdict(Counter)
for fb, sect, words in b_lines:
    mid = words[1:-1]
    for w in mid:
        o = get_onset(w)
        if o in ('ch', 'sh'):
            folio_ch_sh[fb][o] += 1

# Classify folios by their ch/sh mix
ch_dominant = []  # ch/(ch+sh) > 0.7
sh_dominant = []  # ch/(ch+sh) < 0.3
mixed_folios = []  # 0.3-0.7

for fb in sorted(folio_ch_sh.keys()):
    ch = folio_ch_sh[fb].get('ch', 0)
    sh = folio_ch_sh[fb].get('sh', 0)
    total = ch + sh
    if total < 5:
        continue
    ratio = ch / total
    sect = infer_section(fb)
    if ratio > 0.7:
        ch_dominant.append((fb, ch, sh, ratio, sect))
    elif ratio < 0.3:
        sh_dominant.append((fb, ch, sh, ratio, sect))
    else:
        mixed_folios.append((fb, ch, sh, ratio, sect))

print(f"\nFolios with ≥5 ch+sh words (B-dialect):")
print(f"ch-dominant (>70% ch): {len(ch_dominant)}")
print(f"sh-dominant (<30% ch): {len(sh_dominant)}")
print(f"Mixed (30-70% ch): {len(mixed_folios)}")

print(f"\nch-dominant folios:")
for fb, ch, sh, r, sect in sorted(ch_dominant):
    print(f"  {fb:<8} ch={ch:3d} sh={sh:3d} ratio={r:.2f} [{sect}]")

print(f"\nsh-dominant folios:")
for fb, ch, sh, r, sect in sorted(sh_dominant):
    print(f"  {fb:<8} ch={ch:3d} sh={sh:3d} ratio={r:.2f} [{sect}]")

print(f"\nMixed folios (30-70% ch):")
for fb, ch, sh, r, sect in sorted(mixed_folios):
    print(f"  {fb:<8} ch={ch:3d} sh={sh:3d} ratio={r:.2f} [{sect}]")

# Summary
print("\n" + "="*70)
print("SUMMARY INTERPRETATION")
print("="*70)
print("""
H527 decision criteria:
- SECTION ARTIFACT if: (a) strong section-level ch/sh segregation AND
  (b) within-mixed-line avoidance E close to 1.0 (avoidance disappears)
- GRAMMATICAL RULE if: (a) sections share both ch and sh AND
  (b) within-mixed-line E still <0.8 (avoidance persists when both present)
- BOTH if: partial section segregation + partial grammar constraint
""")
