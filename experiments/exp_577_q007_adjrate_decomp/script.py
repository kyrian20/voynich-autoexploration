"""
exp_577: Q007 Three-Way Constraint Diagnosis — adj_rate Onset Decomposition

The Q007 three-way constraint: VMS achieves simultaneously:
  (1) Restricted vocabulary for sh/ch/d onset classes (CP90 ratios << simulation)
  (2) Low adj_rate (global=0.009; consecutive identical word pairs are rare)
  (3) Some Menzerath structure

The simulation CANNOT achieve (1)+(2) simultaneously: clamping sh/ch/d vocabulary
reduces CP90 over-production but raises adj_rate to 126.3% of VMS (exp_304 finding).

This experiment diagnoses the constraint by asking: WHERE does VMS's adj_rate of 0.009
come from, and how does VMS achieve it with restricted vocabulary?

ANALYSIS 1: Onset-class decomposition of adj_rate in VMS
For each onset class c, what fraction of adjacent identical word pairs are c-onset?
  → Which onset classes contribute most to VMS adj_rate?
  → Which onset classes have near-zero self-pair rate?

ANALYSIS 2: Within-onset identical pair rate vs vocabulary richness
For each onset class: compute P(w[i]=w[i+1] | onset(w[i])=onset(w[i+1])=c)
  → Classes with low vocabulary richness (low CP90) should have HIGHER identical pair rates
     IF words were randomly drawn from a finite pool
  → If VMS violates this expectation (low richness + low identical pair rate for some class),
     that class has a structural mechanism preventing word-level repetition

ANALYSIS 3: Routing structure vs self-repetition
For sh/ch/d onset classes, what fraction of their tokens are immediately followed
by a word of the SAME onset (self-succession) vs a different onset (routing)?
  → High routing = few consecutive same-onset tokens = lower vocabulary pressure on adj_rate
  → If sh→qok routing is strong, consecutive sh tokens are rare → sh word identical pairs rare

ANALYSIS 4: Simulation comparison (baseline vs clamp_all_7)
Compare VMS vs baseline simulation vs clamp_all_7 simulation on:
  - Per-onset identical pair rates
  - Per-onset vocabulary sizes
  → Identify where the clamp_all_7 adj_rate increase comes from specifically

PURPOSE: Understand what the constraint tells us about how VMS generates sh/ch/d words.
Does the low adj_rate in VMS imply a context-conditional generation mechanism?
"""
from pathlib import Path as _RepositoryPath

import os, re, random, math
from collections import Counter, deque, defaultdict

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
LATIN_CORPUS = os.path.join(REPO_DIR, 'data/reference_corpora/latin/cicero_de_officiis_latin.txt')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
SEED = 577000

ONSET_ORDER=[
    ('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o'),
]
SUFFIX_PATTERNS=['eedy','edy','aiin','ain','am','ey','ol','or','al','ar','dy']
SPARSE_ONSETS={'qok','ok','ot','qot'}

def get_onset(w):
    for prefix, label in ONSET_ORDER:
        if w.startswith(prefix): return label
    return 'other'

def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total = stats['total']
    if total == 0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total >= 0.05 else 'A'

def parse_vms_b_lines():
    folio_word_stats = defaultdict(lambda: {'total':0,'edy':0,'eedy':0})
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio = m.group(1).lstrip('+*=&~'); fb = folio_base(folio)
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            for w in words:
                folio_word_stats[fb]['total'] += 1
                if w.endswith('eedy'): folio_word_stats[fb]['eedy'] += 1
                elif w.endswith('edy'): folio_word_stats[fb]['edy'] += 1
    folio_dialect = {fb: classify_dialect(stats) for fb, stats in folio_word_stats.items()}
    b_lines = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'<([^.]+)\.(\d+),([^>]+)>', line)
            if not m: continue
            folio_raw = m.group(1); locus_code = m.group(3)
            folio = folio_raw.lstrip('+*=&~'); fb = folio_base(folio)
            if folio_dialect.get(fb, 'unknown') != 'B': continue
            lc_stripped = locus_code.lstrip('+*=/~&')
            if not lc_stripped.lstrip('@').startswith('P'): continue
            text = re.sub(r'<[^>]+>', '', line)
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if words: b_lines.append(words)
    return b_lines

def analyze_adjrate_decomposition(b_lines, label="VMS B-dialect"):
    """Full adj_rate analysis: onset decomposition, vocab richness, routing."""
    all_words = [w for l in b_lines for w in l]
    n_words = len(all_words)

    # Global adj_rate
    global_adj = sum(1 for i in range(len(all_words)-1) if all_words[i] == all_words[i+1]) / (n_words-1)

    print(f"\n{'='*70}")
    print(f"ANALYSIS: {label}")
    print(f"{'='*70}")
    print(f"Total words: {n_words:,} | Global adj_rate: {global_adj:.4f} ({global_adj*100:.3f}%)")

    # ANALYSIS 1: Onset-class decomposition of adj_rate
    print(f"\n--- ANALYSIS 1: Onset-class contribution to adj_rate ---")
    onset_adj_pairs = Counter()  # onset class of the pair
    onset_tokens = Counter()    # total tokens per onset class
    onset_same_onset_pairs = Counter()  # consecutive same-onset pairs (not necessarily same word)

    for i in range(len(all_words)-1):
        w1 = all_words[i]; w2 = all_words[i+1]
        o1 = get_onset(w1)
        onset_tokens[o1] += 1
        if w1 == w2:
            onset_adj_pairs[o1] += 1
        if o1 == get_onset(w2):
            onset_same_onset_pairs[o1] += 1

    total_adj_pairs = sum(onset_adj_pairs.values())
    print(f"\nTotal identical adjacent pairs: {total_adj_pairs}")
    print(f"  (global adj_rate = {total_adj_pairs/(n_words-1):.4f})\n")

    major_classes = ['qok','ok','ot','qot','sh','ch','d','y','s','t','ol','l','r']
    print(f"{'Onset':<8} {'Tokens':>7} {'%Total':>7} {'IdPairs':>8} {'IdRate%':>9} {'%AdjContr':>10} {'SameOns%':>10} {'VocabN':>7} {'CP90':>5}")
    print("-"*80)

    onset_vocab = {}
    onset_cp90 = {}

    for onset_class in major_classes:
        tokens = onset_tokens.get(onset_class, 0)
        if tokens < 10: continue
        id_pairs = onset_adj_pairs.get(onset_class, 0)
        same_onset = onset_same_onset_pairs.get(onset_class, 0)
        id_rate = id_pairs / tokens if tokens else 0
        pct_adj = id_pairs / total_adj_pairs * 100 if total_adj_pairs else 0
        same_onset_pct = same_onset / tokens * 100 if tokens else 0
        pct_total = tokens / n_words * 100

        # Vocabulary size for this onset class (all positions)
        onset_words = [w for w in all_words if get_onset(w) == onset_class]
        type_counts = Counter(onset_words)
        n_types = len(type_counts)
        # CP90: how many types needed to cover 90% of tokens
        sorted_types = sorted(type_counts.values(), reverse=True)
        cumsum = 0; cp90 = 0; target = sum(sorted_types) * 0.90
        for c in sorted_types:
            cumsum += c; cp90 += 1
            if cumsum >= target: break
        onset_vocab[onset_class] = n_types
        onset_cp90[onset_class] = cp90

        print(f"{onset_class:<8} {tokens:>7,} {pct_total:>6.1f}% {id_pairs:>8} {id_rate*100:>8.3f}% {pct_adj:>9.1f}% {same_onset_pct:>9.1f}% {n_types:>7} {cp90:>5}")

    # ANALYSIS 2: Vocabulary richness vs identical pair rate
    print(f"\n--- ANALYSIS 2: Vocabulary richness vs adjacent identical pair rate ---")
    print(f"Expected (random draw from finite pool): P(adj_identical) = sum_w(p(w)^2) = 1/CP90_effective")
    print(f"\n{'Onset':<8} {'CP90':>6} {'Expected%':>10} {'Actual%':>9} {'Ratio':>7} {'Interpretation'}")
    print("-"*65)
    for onset_class in major_classes:
        tokens = onset_tokens.get(onset_class, 0)
        if tokens < 10: continue
        cp90 = onset_cp90.get(onset_class, 0)
        if cp90 == 0: continue
        # Expected adj rate if randomly drawing from cp90 types uniformly
        expected_adj = 1.0 / cp90
        actual_adj = onset_adj_pairs.get(onset_class, 0) / tokens if tokens else 0
        ratio = actual_adj / expected_adj if expected_adj > 0 else 0
        if ratio < 0.2:
            interp = "MUCH LESS than expected — anti-repetition structure"
        elif ratio < 0.5:
            interp = "less than expected — some anti-repetition"
        elif ratio < 1.5:
            interp = "near expected — consistent with random draw"
        else:
            interp = "MORE than expected — repetition amplification"
        print(f"{onset_class:<8} {cp90:>6} {expected_adj*100:>9.3f}% {actual_adj*100:>8.3f}% {ratio:>7.3f} {interp}")

    # ANALYSIS 3: Routing structure — do sh/ch/d route away from themselves?
    print(f"\n--- ANALYSIS 3: Self-routing vs other-routing for sh/ch/d ---")
    print(f"(What fraction of sh/ch/d tokens are followed by same-onset vs other onset?)")
    print(f"\n{'Onset':<8} {'Tokens':>7} {'→Self%':>8} {'→qok%':>8} {'→ch%':>7} {'→sh%':>7} {'→d%':>7} {'→y%':>7} {'→other%':>8}")
    print("-"*75)
    for onset_class in ['sh', 'ch', 'd', 'qok', 'ok']:
        tokens_before = [i for i in range(len(all_words)-1) if get_onset(all_words[i]) == onset_class]
        if len(tokens_before) < 10: continue
        successors = Counter(get_onset(all_words[i+1]) for i in tokens_before)
        total = len(tokens_before)
        self_pct = successors.get(onset_class, 0) / total * 100
        qok_pct = successors.get('qok', 0) / total * 100
        ch_pct = successors.get('ch', 0) / total * 100
        sh_pct = successors.get('sh', 0) / total * 100
        d_pct = successors.get('d', 0) / total * 100
        y_pct = successors.get('y', 0) / total * 100
        other = 100 - sum(successors.get(o, 0) for o in ['qok','ok','ot','qot','ch','sh','d','y']) / total * 100
        print(f"{onset_class:<8} {total:>7} {self_pct:>7.1f}% {qok_pct:>7.1f}% {ch_pct:>6.1f}% {sh_pct:>6.1f}% {d_pct:>6.1f}% {y_pct:>6.1f}% {other:>7.1f}%")

    # ANALYSIS 4: MID-only analysis (most relevant for vocabulary clamping)
    print(f"\n--- ANALYSIS 4: MID-position only adj_rate decomposition ---")
    mid_pairs = []
    for l in b_lines:
        if len(l) < 3: continue
        for idx in range(1, len(l)-2):  # MID positions (not LF, not LL)
            mid_pairs.append((l[idx], l[idx+1]))

    mid_adj = sum(1 for w1, w2 in mid_pairs if w1 == w2) / len(mid_pairs) if mid_pairs else 0
    print(f"MID-position adj_rate: {mid_adj:.4f}")

    mid_onset_adj = Counter()
    mid_onset_total = Counter()
    for w1, w2 in mid_pairs:
        o1 = get_onset(w1)
        mid_onset_total[o1] += 1
        if w1 == w2: mid_onset_adj[o1] += 1

    print(f"\n{'Onset':<8} {'MIDtok':>7} {'MIDadj':>7} {'MIDrate%':>9}")
    print("-"*35)
    for onset_class in major_classes:
        tokens = mid_onset_total.get(onset_class, 0)
        if tokens < 5: continue
        adj = mid_onset_adj.get(onset_class, 0)
        print(f"{onset_class:<8} {tokens:>7} {adj:>7} {adj/tokens*100:>8.3f}%")

    # KEY DIAGNOSTIC: What would happen if VMS sh/ch/d vocabulary were compressed?
    print(f"\n--- ANALYSIS 5: Hypothetical adj_rate under vocabulary compression ---")
    print(f"If sh/ch/d vocabulary compressed to VMS CP90 types and drawn uniformly,")
    print(f"what would be the expected adjacent pair rate for each class?")
    print(f"\n{'Onset':<8} {'CurrentCP90':>12} {'HypCP90':>9} {'CurrentAdj%':>12} {'HypAdj%':>10} {'delta_adj':>10}")
    print("-"*65)

    # VMS target CP90 values for sh/ch/d (from exp_302 MID-only analysis)
    # For all-positions CP90: these are different from MID-only
    # Let's use the actual VMS values we just computed
    global_adj_contribution = {}
    for onset_class in ['sh', 'ch', 'd']:
        tokens = onset_tokens.get(onset_class, 0)
        if tokens < 10: continue
        current_cp90 = onset_cp90.get(onset_class, 0)
        current_adj = onset_adj_pairs.get(onset_class, 0) / tokens if tokens else 0

        # If we compress vocabulary to exactly VMS CP90 types drawn uniformly:
        hyp_adj = 1.0 / current_cp90 if current_cp90 > 0 else 0

        # Expected change in global adj_rate:
        pct_total = tokens / n_words
        delta_adj = (hyp_adj - current_adj) * pct_total

        global_adj_contribution[onset_class] = delta_adj
        print(f"{onset_class:<8} {current_cp90:>12} {current_cp90:>9} {current_adj*100:>11.3f}% {hyp_adj*100:>9.3f}% {delta_adj*100:>+10.3f}%")

    # What would global adj_rate become if VMS had SIMULATION-LEVEL vocabulary?
    print(f"\n--- ANALYSIS 6: Summary interpretation ---")
    print(f"\nKey question: does VMS sh/ch/d simultaneously have restricted vocabulary AND low adj_rate?")
    for onset_class in ['sh', 'ch', 'd']:
        tokens = onset_tokens.get(onset_class, 0)
        if tokens < 10: continue
        cp90 = onset_cp90.get(onset_class, 0)
        actual_adj = onset_adj_pairs.get(onset_class, 0) / tokens if tokens else 0
        expected_random_adj = 1.0 / cp90 if cp90 > 0 else 0
        print(f"\n  {onset_class}-onset: CP90={cp90} types (over simulation by ~3×)")
        print(f"    If random draw from CP90 pool: expected adj_rate = {expected_random_adj*100:.3f}%")
        print(f"    Actual VMS adj_rate for this class: {actual_adj*100:.3f}%")
        if actual_adj < expected_random_adj * 0.5:
            print(f"    → VMS {onset_class} adj_rate is MUCH LOWER than random-pool prediction")
            print(f"    → STRUCTURAL EVIDENCE: VMS actively suppresses {onset_class}-word repetition")
            print(f"    → This cannot be explained by finite pool alone — requires anti-repetition mechanism")
        elif actual_adj < expected_random_adj:
            print(f"    → VMS {onset_class} adj_rate is lower than random-pool (ratio={actual_adj/expected_random_adj:.2f}×)")
        else:
            print(f"    → VMS {onset_class} adj_rate is at or above random-pool prediction")

    return {
        'global_adj': global_adj,
        'onset_adj_pairs': dict(onset_adj_pairs),
        'onset_tokens': dict(onset_tokens),
        'onset_vocab': onset_vocab,
        'onset_cp90': onset_cp90,
    }

def main():
    print("exp_577: Q007 Three-Way Constraint — adj_rate Onset Decomposition")
    print("="*70)
    print("Purpose: Understand why VMS has low adj_rate despite restricted vocabulary")
    print("         for sh/ch/d onset classes (the Q007 three-way constraint)")

    print("\nLoading VMS B-dialect...")
    b_lines = parse_vms_b_lines()
    n_lines = len(b_lines)
    n_words = sum(len(l) for l in b_lines)
    print(f"  {n_lines} lines, {n_words} words")

    # Main analysis on full B-dialect
    vms_results = analyze_adjrate_decomposition(b_lines, "VMS B-dialect")

    # Summary of the constraint
    print(f"\n\n{'='*70}")
    print(f"CONSTRAINT SUMMARY: Q007 Three-Way for sh/ch/d")
    print(f"{'='*70}")
    print(f"""
From exp_302/304 and this analysis:
- sh/ch/d onset classes over-produce vocabulary in simulation (3-4×)
- Vocabulary clamping to VMS CP90 levels raises adj_rate above tolerance (exp_304: 126.3%)
- This experiment diagnoses WHY:

Question: Does VMS achieve its low adj_rate DESPITE restricted sh/ch/d vocabulary,
          or BECAUSE of some structural mechanism that this experiment can detect?

Expected: if VMS just randomly draws from a finite sh/ch/d pool → adj_rate = 1/CP90
Actual:   (see above for each onset class)

If VMS adj_rate for sh/ch/d << 1/CP90:
  → VMS has an ACTIVE anti-repetition mechanism for sh/ch/d
  → Vocabulary restriction + routing structure together achieve low adj_rate
  → Simulation clamping fails because it doesn't implement the anti-repetition

If VMS adj_rate for sh/ch/d ≈ 1/CP90:
  → VMS's adj_rate constraint IS consistent with random pool draws
  → The simulation failure is because clamping ALSO changes global word composition
     (more frequent sh/ch/d words per onset class → more within-class adjacency)
""")

if __name__ == '__main__':
    main()
