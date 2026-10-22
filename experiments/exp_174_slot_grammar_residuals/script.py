"""
exp_174: Slot-Grammar Residuals — Template vs. Grammar Discrimination

Template hypothesis: VMS words are assembled by filling positional slots
(gallows@slot1, suffix@slotN, etc.) with position-independent slot fillers.
Under a pure template model, word-internal structure should be entirely
captured by the slot + filler combination, with no residual grammar.

Grammar hypothesis: Onset classes have CONTEXT-DEPENDENT behavior that
cannot be reduced to slot-filler patterns. Specifically:
  (a) Successor distributions differ by onset class, not just by position
  (b) Self-succession is onset-class-specific, not position-class-specific
  (c) Positional enrichments are onset-specific, not interchangeable

Discrimination: If template, then controlling for line position should
eliminate onset-class effects. If grammar, then onset effects should
PERSIST after controlling for position.

Method: For each line position (LF, second, MID, LL, only), compute the
onset-class distribution. Then measure how much of the onset-class
sequential effects (self-succession, qok→ch, daiin→cth) survive after
position is controlled.

Tests:
  H1: Onset self-succession (qok, ok, ch) survives within position-strata
  H2: qok→ch enrichment is not explained by positional co-occurrence
  H3: -am words at LL are specifically -am, not any LL word
  H4: y-onset words at LF are specifically y-onset, not any LF word
"""
from pathlib import Path as _RepositoryPath

import sys
import os

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
sys.path.insert(0, os.path.join(REPO_DIR, 'src'))

from collections import defaultdict, Counter
import math

# ─── CORPUS PARSING ───────────────────────────────────────────────────────────

import re

def parse_corpus(path):
    lines_by_folio = defaultdict(list)
    with open(path, encoding='utf-8') as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw.startswith('#'):
                continue
            parts = raw.split(None, 1)
            if len(parts) < 2:
                continue
            locus_raw, text = parts
            lparts = locus_raw.split(',')
            if len(lparts) < 2:
                continue
            lt = lparts[1].rstrip('>').lstrip('@+*=~&')
            if not lt.startswith('P'):
                continue
            folio_base = lparts[0].split('.')[0].lstrip('<')
            m = re.match(r'f(\d+)', folio_base)
            if not m:
                continue
            fid = int(m.group(1))
            words = [w for w in text.split('.') if w and re.match(r'[a-z]', w) and not w.startswith('<')]
            if not words:
                continue
            lines_by_folio[fid].append(words)
    return lines_by_folio

def assign_dialect(lines, min_words=10, threshold=0.05):
    """Folio-level edy/eedy rate >= threshold → B-dialect."""
    all_words = [w for line in lines for w in line]
    if len(all_words) < min_words:
        return None
    edy_count = sum(1 for w in all_words if 'edy' in w or 'eedy' in w)
    rate = edy_count / len(all_words)
    return 'B' if rate >= threshold else 'A'

# ─── ONSET TAXONOMY ───────────────────────────────────────────────────────────

def get_onset(word):
    w = word
    for prefix in ['qok', 'qot', 'qo']:
        if w.startswith(prefix):
            return prefix
    if w.startswith('cth'):
        return 'cth'
    if w.startswith('che') or w.startswith('chi'):
        return 'ch_e'
    if w.startswith('ch'):
        return 'ch'
    if w.startswith('sh'):
        return 'sh'
    for prefix in ['ok', 'ot', 'ol', 'd', 's', 'y', 'k', 't', 'l', 'r', 'p', 'f']:
        if w.startswith(prefix):
            return prefix
    return 'other'

def get_position(i, n):
    if n == 1:
        return 'only'
    if i == 0:
        return 'LF'
    if i == n - 1:
        return 'LL'
    if i == 1 and n > 2:
        return 'second'
    return 'MID'

# ─── MAIN ANALYSIS ────────────────────────────────────────────────────────────

def main():
    path = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')
    lines_by_folio = parse_corpus(path)

    # Assign dialects
    A_lines = []
    B_lines = []
    for fid, lines in lines_by_folio.items():
        dialect = assign_dialect(lines)
        if dialect == 'A':
            A_lines.extend(lines)
        elif dialect == 'B':
            B_lines.extend(lines)

    print(f"A-dialect: {sum(len(l) for l in A_lines)} words, {len(A_lines)} lines")
    print(f"B-dialect: {sum(len(l) for l in B_lines)} words, {len(B_lines)} lines")

    for dialect_name, all_lines in [('A', A_lines), ('B', B_lines)]:
        print(f"\n{'='*70}")
        print(f"DIALECT: {dialect_name}")
        print(f"{'='*70}")

        # Build position-annotated word list
        annotated = []  # (word, onset, position)
        for line in all_lines:
            n = len(line)
            for i, w in enumerate(line):
                pos = get_position(i, n)
                onset = get_onset(w)
                annotated.append((w, onset, pos))

        # ─── H1: Onset self-succession WITHIN position strata ───────────────
        print("\n── H1: Onset self-succession within position strata ──")
        print("Template prediction: self-succession = baseline within each position stratum")
        print("Grammar prediction: onset-class self-succession exceeds baseline within strata")

        # Build bigrams (consecutive words in same line, with positions)
        bigrams = []  # (onset_i, pos_i, onset_j, pos_j)
        for line in all_lines:
            n = len(line)
            for i in range(len(line) - 1):
                oi = get_onset(line[i])
                pi = get_position(i, n)
                oj = get_onset(line[i + 1])
                pj = get_position(i + 1, n)
                bigrams.append((oi, pi, oj, pj))

        # For each (position_i, position_j) pair, compute onset-class transition matrix
        pos_pairs = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        # pos_pairs[(pi, pj)][onset_i][onset_j] += 1
        for oi, pi, oj, pj in bigrams:
            pos_pairs[(pi, pj)][oi][oj] += 1

        target_onsets = ['qok', 'ok', 'ch', 'qo', 'd']
        for onset in target_onsets:
            total_self_succ = 0
            total_expected = 0
            pos_details = []
            for (pi, pj), trans in pos_pairs.items():
                # All transitions from this position pair
                all_from_pi = sum(trans[oi2][oj2] for oi2 in trans for oj2 in trans[oi2])
                from_onset = sum(trans[onset][oj2] for oj2 in trans[onset])
                if from_onset == 0:
                    continue
                # Baseline rate of onset_j = onset in this (pi,pj) context
                all_j_counts = defaultdict(int)
                for oi2 in trans:
                    for oj2, c in trans[oi2].items():
                        all_j_counts[oj2] += c
                total_j = sum(all_j_counts.values())
                baseline = all_j_counts[onset] / total_j if total_j > 0 else 0
                # Observed self-succession rate for this onset in this position context
                obs = trans[onset][onset]
                expected = from_onset * baseline
                total_self_succ += obs
                total_expected += expected
                if expected >= 1:
                    enr = obs / expected
                    pos_details.append(f"  ({pi}→{pj}): obs={obs}, exp={expected:.1f}, enr={enr:.3f}")

            if total_expected > 0:
                overall_enr = total_self_succ / total_expected
                print(f"\n  {onset} self-succession (position-controlled):")
                print(f"    Total: obs={total_self_succ}, exp={total_expected:.1f}, enrichment={overall_enr:.3f}")
                for d in sorted(pos_details):
                    print(d)

        # ─── H2: qok→ch not explained by positional co-occurrence ───────────
        print(f"\n── H2: qok→ch enrichment — positional co-occurrence vs. intrinsic ──")
        # Under template: qok appears at certain positions, ch appears at certain
        # positions; enrichment = P(ch|after qok) vs P(ch|anywhere after position X)
        # We test: within each (pos_i → pos_j) stratum, does qok→ch exceed baseline?

        total_qok_ch = 0
        total_qok_notch = 0
        total_notqok_ch = 0
        total_notqok_notch = 0
        pos_qok_ch = []
        for (pi, pj), trans in pos_pairs.items():
            qok_ch = trans['qok']['ch']
            qok_total = sum(trans['qok'].values())
            # All non-qok words at pi → ch at pj
            notqok_ch = sum(trans[oi2]['ch'] for oi2 in list(trans) if oi2 != 'qok')
            notqok_total = sum(trans[oi2][oj2] for oi2 in list(trans) if oi2 != 'qok' for oj2 in list(trans[oi2]))
            if qok_total >= 5:
                pos_qok_ch.append((pi, pj, qok_ch, qok_total, notqok_ch, notqok_total))
                total_qok_ch += qok_ch
                total_qok_notch += (qok_total - qok_ch)
                total_notqok_ch += notqok_ch
                total_notqok_notch += notqok_total

        print("  qok→ch enrichment within each position stratum (pi→pj with ≥5 qok transitions):")
        for (pi, pj, qok_ch, qok_total, notqok_ch, notqok_total) in pos_qok_ch:
            qok_rate = qok_ch / qok_total if qok_total > 0 else 0
            base_rate = notqok_ch / notqok_total if notqok_total > 0 else 0
            enr = qok_rate / base_rate if base_rate > 0 else float('inf')
            print(f"  ({pi}→{pj}): qok→ch rate={qok_rate:.3f} ({qok_ch}/{qok_total}), baseline={base_rate:.3f}, enr={enr:.3f}")

        # Overall position-controlled enrichment
        if total_qok_ch + total_qok_notch > 0 and total_notqok_ch + total_notqok_notch > 0:
            overall_qok_rate = total_qok_ch / (total_qok_ch + total_qok_notch)
            overall_base = total_notqok_ch / (total_notqok_ch + total_notqok_notch)
            overall_enr = overall_qok_rate / overall_base if overall_base > 0 else float('inf')
            print(f"\n  POSITION-CONTROLLED overall: qok→ch rate={overall_qok_rate:.3f}, baseline={overall_base:.3f}, enr={overall_enr:.3f}")
            print(f"  (Compare unconditional qok→ch enrichment to see position's contribution)")

        # ─── H3: -am specificity at LL ───────────────────────────────────────
        print(f"\n── H3: -am LL enrichment — suffix specificity vs. positional artifact ──")
        # Template prediction: LL words should have generic "LL properties"
        # -am words at LL are just words at LL, not specifically -am
        # Grammar prediction: -am is specifically LL-enriched relative to other suffixes

        suffix_classes = {
            'am': lambda w: w.endswith('am'),
            'al': lambda w: w.endswith('al'),
            'ar': lambda w: w.endswith('ar'),
            'aiin': lambda w: w.endswith('aiin'),
            'edy': lambda w: w.endswith('edy') or w.endswith('eedy'),
            'ol': lambda w: w.endswith('ol'),
            'or': lambda w: w.endswith('or'),
        }

        all_words_flat = [w for line in all_lines for w in line]
        total_words = len(all_words_flat)

        ll_words = [line[-1] for line in all_lines if len(line) > 1]
        total_ll = len(ll_words)

        print(f"  Total LL words: {total_ll}")
        print(f"  Suffix enrichment at LL (per suffix class):")
        print(f"  {'Suffix':<8} {'LL count':>9} {'LL rate':>9} {'Global rate':>12} {'Enrichment':>12}")
        for suf_name, suf_fn in sorted(suffix_classes.items()):
            ll_count = sum(1 for w in ll_words if suf_fn(w))
            global_count = sum(1 for w in all_words_flat if suf_fn(w))
            ll_rate = ll_count / total_ll if total_ll > 0 else 0
            global_rate = global_count / total_words if total_words > 0 else 0
            enr = ll_rate / global_rate if global_rate > 0 else float('inf')
            print(f"  {suf_name:<8} {ll_count:>9} {ll_rate:>9.4f} {global_rate:>12.4f} {enr:>12.3f}")

        # ─── H4: y-onset specificity at LF ───────────────────────────────────
        print(f"\n── H4: y-onset LF enrichment — onset specificity vs. positional artifact ──")
        # Template prediction: LF words are interchangeable "line-opening" fillers
        # Grammar prediction: y-onset specifically enriched at LF vs other onsets

        lf_words = [line[0] for line in all_lines if len(line) > 1]
        total_lf = len(lf_words)

        print(f"  Total LF words: {total_lf}")
        print(f"  Onset enrichment at LF (per onset class):")

        onset_classes = ['qok', 'qo', 'cth', 'ch_e', 'ch', 'sh', 'ok', 'd', 's', 'y', 'k', 't', 'l', 'other']
        print(f"  {'Onset':<8} {'LF count':>9} {'LF rate':>9} {'Global rate':>12} {'Enrichment':>12}")
        for onset in onset_classes:
            lf_count = sum(1 for w in lf_words if get_onset(w) == onset)
            global_count = sum(1 for w in all_words_flat if get_onset(w) == onset)
            lf_rate = lf_count / total_lf if total_lf > 0 else 0
            global_rate = global_count / total_words if total_words > 0 else 0
            enr = lf_rate / global_rate if global_rate > 0 else float('inf')
            if global_count >= 5:
                flag = " ←" if abs(enr - 1) > 0.3 else ""
                print(f"  {onset:<8} {lf_count:>9} {lf_rate:>9.4f} {global_rate:>12.4f} {enr:>12.3f}{flag}")

        # ─── H5: Are self-succession rates position-homogeneous? ────────────
        print(f"\n── H5: Self-succession homogeneity across positions ──")
        print("  Template: self-succession should be constant (word repeats its slot)")
        print("  Grammar: self-succession rate varies by position context")
        # Compare self-succession rate (pi→pj = pi→pi+1) for same-onset pairs
        # across position transitions
        for onset in ['qok', 'ok', 'ch', 'd']:
            print(f"\n  {onset} self-succession by position transition:")
            for (pi, pj), trans in sorted(pos_pairs.items()):
                n_ss = trans[onset][onset]
                n_from = sum(trans[onset].values())
                if n_from >= 3:
                    rate = n_ss / n_from
                    print(f"    ({pi}→{pj}): {n_ss}/{n_from} = {rate:.3f}")

    print("\n\nDone.")

if __name__ == '__main__':
    main()
