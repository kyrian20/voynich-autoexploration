"""
exp_044: Scribal Hand Variation in qo-Rate and Suffix Paradigm Preferences
H050: Do scribal hands 1-5 vary in qo-prefix rate independently of section/dialect?
Also tests: do hands vary in suffix paradigm preferences (-edy vs -ol vs -ain rates)?
"""
from pathlib import Path as _RepositoryPath

import re
import math
from collections import defaultdict, Counter

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

SUFFIXES = ['aiin', 'ain', 'eedy', 'edy', 'chy', 'eey', 'dy', 'ey', 'y',
            'ol', 'or', 'al', 'ar', 'iin', 'in']
seen = set()
SUFFIXES_DEDUP = []
for s in SUFFIXES:
    if s not in seen:
        seen.add(s)
        SUFFIXES_DEDUP.append(s)
SUFFIXES = SUFFIXES_DEDUP


def suffix_group(word):
    for sfx in SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx):
            return sfx, word[:-len(sfx)]
    return None, word


def parse_by_hand_section_currier(path):
    """Parse body text tokens per folio, with hand, section, currier metadata."""
    folio_data = {}  # folio_id → {hand, section, currier, words}
    current_folio = None
    current_hand = None
    current_currier = None
    current_section = None

    with open(path, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Detect folio headers
            m_hand = re.search(r'\$H=(\d+)', line)
            if m_hand:
                current_hand = m_hand.group(1)
            m_cur = re.search(r'\$L=([AB?])', line)
            if m_cur:
                current_currier = m_cur.group(1)
            m_sec = re.search(r'\$I=([A-Z]+)', line)
            if m_sec:
                current_section = m_sec.group(1)

            m2 = re.match(r'^<([^>]+)>', line)
            if not m2:
                continue
            locus_raw = m2.group(1)
            parts = locus_raw.split(',')
            if len(parts) < 2:
                continue
            folio_part = parts[0].strip()
            locus_code = parts[1].strip()

            folio_m = re.match(r'^(f\d+[rv]\d*)', folio_part)
            if folio_m:
                current_folio = folio_m.group(1)
                if current_folio not in folio_data:
                    folio_data[current_folio] = {
                        'hand': current_hand,
                        'currier': current_currier,
                        'section': current_section,
                        'words': []
                    }
                else:
                    # Update metadata if newly found
                    if current_hand and not folio_data[current_folio]['hand']:
                        folio_data[current_folio]['hand'] = current_hand
                    if current_currier and not folio_data[current_folio]['currier']:
                        folio_data[current_folio]['currier'] = current_currier

            if current_folio is None:
                continue

            locus_base = locus_code.lstrip('+*@=/~&')
            if not locus_base.startswith('P'):
                continue

            text = line[m2.end():].strip()
            text = re.sub(r'<%>|<\$>|<->|\{[^}]+\}|\[[^\]]+\]|@\d+;[a-z]*|@\d+;?', '', text)
            tokens = re.split(r'[.\s]+', text)
            tokens = [t.strip() for t in tokens if len(t.strip()) >= 2]
            folio_data[current_folio]['words'].extend(tokens)

    return folio_data


def qo_rate(words):
    """Returns fraction of words starting with 'qo'."""
    if not words:
        return 0.0
    return sum(1 for w in words if w.startswith('qo')) / len(words)


def suffix_rates(words):
    """Returns suffix frequency distribution."""
    sfx_count = Counter()
    total_with_sfx = 0
    for w in words:
        sfx, stem = suffix_group(w)
        if sfx:
            sfx_count[sfx] += 1
            total_with_sfx += 1
    return sfx_count, total_with_sfx


def analyze_by_hand(folio_data):
    """Aggregate statistics by hand number."""
    hand_stats = defaultdict(lambda: {'words': [], 'folios': [], 'currier': Counter(), 'section': Counter()})

    for folio, data in folio_data.items():
        if not data['words'] or len(data['words']) < 20:
            continue
        hand = data['hand'] or '?'
        hand_stats[hand]['words'].extend(data['words'])
        hand_stats[hand]['folios'].append(folio)
        if data['currier']:
            hand_stats[hand]['currier'][data['currier']] += 1
        if data['section']:
            hand_stats[hand]['section'][data['section']] += 1

    return hand_stats


def analyze_within_hand(folio_data, target_hand=None, target_currier=None):
    """
    Within a specific hand+currier combination, compute per-folio qo-rate and
    check if the hand's qo-rate varies independently across folios.
    """
    matching_folios = []
    for folio, data in folio_data.items():
        if len(data['words']) < 30:
            continue
        hand_match = (target_hand is None or data['hand'] == target_hand)
        currier_match = (target_currier is None or data['currier'] == target_currier)
        if hand_match and currier_match:
            matching_folios.append(folio)

    if not matching_folios:
        return

    print(f"\nHand={target_hand}, Currier={target_currier}: {len(matching_folios)} folios")
    rates = []
    for folio in sorted(matching_folios):
        words = folio_data[folio]['words']
        qr = qo_rate(words)
        rates.append(qr)
        sfx, total_sfx = suffix_rates(words)
        top_sfx = sorted(sfx.items(), key=lambda x: -x[1])[:3]
        top_sfx_str = ', '.join(f"-{s}({n})" for s, n in top_sfx)
        sect = folio_data[folio].get('section', '?')
        print(f"  {folio} (sect={sect}, n={len(words)}): qo={qr:.3f}, sfx: {top_sfx_str}")

    if rates:
        mean_qo = sum(rates) / len(rates)
        std_qo = (sum((r - mean_qo)**2 for r in rates) / max(len(rates)-1, 1)) ** 0.5
        print(f"  Mean qo-rate={mean_qo:.3f}, std={std_qo:.3f}")


if __name__ == '__main__':
    print("Loading ZL3b corpus...")
    folio_data = parse_by_hand_section_currier(DATA_PATH)
    print(f"Total folios parsed: {len(folio_data)}")

    hand_stats = analyze_by_hand(folio_data)

    # Main comparison table
    print(f"\n{'='*65}")
    print(f"QO-RATE AND SUFFIX PREFERENCES BY SCRIBAL HAND")
    print(f"{'Hand':<6} {'Folios':>7} {'Tokens':>8} {'Currier':>12} "
          f"{'qo-rate':>8} {'Top 3 suffixes'}")
    print('-' * 65)

    for hand in sorted(hand_stats.keys()):
        data = hand_stats[hand]
        words = data['words']
        folios = data['folios']
        if not words:
            continue
        qr = qo_rate(words)
        sfx, total_sfx = suffix_rates(words)
        top_sfx = sorted(sfx.items(), key=lambda x: -x[1])[:3]
        top_sfx_str = ', '.join(f"-{s}({n})" for s, n in top_sfx)
        currier_str = '/'.join(f"{k}:{v}" for k, v in sorted(data['currier'].items()))
        print(f"  {hand:<4} {len(folios):>7} {len(words):>8} {currier_str:>12} "
              f"{qr:>8.3f}  {top_sfx_str}")

    # Detailed hand-by-hand analysis
    print(f"\n{'='*65}")
    print(f"WITHIN-CURRIER-B ANALYSIS: Do hands vary in qo-rate?")
    # Within Currier B, compare hands 2, 3, 4, 5
    for hand in ['1', '2', '3', '4', '5']:
        analyze_within_hand(folio_data, target_hand=hand, target_currier='B')

    print(f"\n{'='*65}")
    print(f"WITHIN-CURRIER-A ANALYSIS:")
    for hand in ['1', '2', '3']:
        analyze_within_hand(folio_data, target_hand=hand, target_currier='A')

    # Statistical test: is there a hand effect on qo-rate within Currier B?
    print(f"\n{'='*65}")
    print(f"SUFFIX PREFERENCES BY HAND (Currier B only)")
    print(f"Comparing -edy, -ol, -ain, -aiin rates")
    print(f"{'Hand':<6} {'n':>6} {'qo%':>7} {'-edy%':>7} {'-ol%':>7} "
          f"{'-ain%':>7} {'-aiin%':>7}")
    print('-' * 55)

    target_sfx = ['edy', 'ol', 'ain', 'aiin']
    for hand in sorted(hand_stats.keys()):
        data = hand_stats[hand]
        words = data['words']
        if not words or data['currier'].get('B', 0) < 2:
            continue
        # Use only Currier B folios for this hand
        b_words = []
        for f in data['folios']:
            if folio_data[f].get('currier') == 'B' and len(folio_data[f]['words']) >= 20:
                b_words.extend(folio_data[f]['words'])
        if len(b_words) < 50:
            continue
        sfx, total_sfx = suffix_rates(b_words)
        n = len(b_words)
        qr = qo_rate(b_words)
        rates = [100 * sfx.get(s, 0) / max(n, 1) for s in target_sfx]
        rates_str = ''.join(f"{r:>7.1f}" for r in rates)
        print(f"  {hand:<4} {n:>6} {100*qr:>6.1f}%{rates_str}")
