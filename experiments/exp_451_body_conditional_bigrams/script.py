"""
exp_451: Body-Conditional Succession Rules Beyond sh→qok (H_new_M)
Q: Is the she-body→qok rule (F372) a general principle, or specific to sh→qok?
   For each major onset class, do body subdivisions (first body char after onset)
   predict the successor onset class at E≥1.5×?

Method: B-dialect MID bigrams. For each (onset_class, first_body_char) group
   with ≥20 tokens, compute successor onset distribution vs baseline.
"""
import re
from collections import defaultdict, Counter

ZL3B = '/Users/asash/voynich-cryptanalyst/data/transcriptions/eva_zl3b.txt'

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']
# Target onset classes to analyze as predecessors
TARGET_ONSETS = ['sh', 'ch', 'd', 'y', 'ol', 'ok', 'qok', 's', 'ot']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def get_first_body_char(word, onset):
    """First character after the onset string."""
    body = word[len(onset):]
    if body:
        return body[0]
    return '_'  # bare onset word (no body)

def parse_corpus():
    pattern = re.compile(r'<([^.]+)\.(\d+),([^>]+)>([^<]*)')
    folios = defaultdict(list)
    with open(ZL3B, encoding='utf-8') as f:
        for line in f:
            for m in pattern.finditer(line):
                folio = m.group(1).lstrip('+*=&~')
                lc = m.group(3).lstrip('+*=/~&')
                if not lc.lstrip('@').startswith('P'):
                    continue
                text = m.group(4).strip()
                words = [w for w in re.split(r'[-.\s]', text)
                         if re.match(r'^[a-z]+$', w) and len(w) >= 2]
                if words:
                    folios[folio].append(words)
    return folios

def classify_dialects(folios):
    dialect = {}
    for folio, lines in folios.items():
        total = sum(len(ws) for ws in lines)
        if total == 0: continue
        edy = sum(1 for ws in lines for w in ws
                  if w.endswith('edy') or w.endswith('eedy'))
        dialect[folio] = 'B' if edy / total >= 0.05 else 'A'
    return dialect

def collect_mid_bigrams(folios, dialect_map, target_dialect):
    """
    Returns:
    - body_bigrams[(onset, body_char)][(succ_onset)] = count
    - onset_total[(onset, body_char)] = total predecessor count
    - baseline_succ[(succ_onset)] = count (all MID successors for each onset class)
    - baseline_pred[(onset)] = total count for each onset class
    """
    body_bigrams = defaultdict(Counter)  # (onset, body_char) -> Counter(succ_onset)
    onset_body_total = Counter()  # (onset, body_char) -> count as predecessor
    baseline_succ_given_onset = defaultdict(Counter)  # onset -> Counter(succ_onset)
    total_mid_bigrams = 0
    succ_onset_total = Counter()  # total successor onset distribution

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]

        for line_words in cont_lines:
            lw = len(line_words)
            if lw < 4:
                continue
            mid_words = line_words[1:lw-1]
            for i in range(len(mid_words) - 1):
                w1 = mid_words[i]
                w2 = mid_words[i+1]
                on1 = get_onset(w1)
                on2 = get_onset(w2)
                if on1 == 'other' or on2 == 'other':
                    continue
                bc1 = get_first_body_char(w1, on1) if on1 != 'other' else '_'
                body_bigrams[(on1, bc1)][on2] += 1
                onset_body_total[(on1, bc1)] += 1
                baseline_succ_given_onset[on1][on2] += 1
                succ_onset_total[on2] += 1
                total_mid_bigrams += 1

    return body_bigrams, onset_body_total, baseline_succ_given_onset, total_mid_bigrams, succ_onset_total

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    for dialect in ['B', 'A']:
        print(f"\n{'='*65}")
        print(f"  {dialect}-DIALECT: Body-conditional succession rules")
        print(f"{'='*65}")

        body_bigrams, onset_body_total, baseline_succ, total_mid, succ_total = \
            collect_mid_bigrams(folios, dialect_map, dialect)

        # For each target onset, show body-char breakdown of successor distribution
        for onset in TARGET_ONSETS:
            # Get all (onset, body_char) keys with this onset
            body_keys = [(on, bc) for (on, bc) in onset_body_total
                         if on == onset and onset_body_total[(on, bc)] >= 15]
            if not body_keys:
                continue

            # Baseline: P(succ_onset | onset) for this onset class
            base_total = sum(baseline_succ[onset].values())
            if base_total < 20:
                continue

            print(f"\n--- {onset}-onset (baseline N={base_total}) ---")
            # Top successor onsets for this class (top 6)
            top_succs = [s for s, _ in baseline_succ[onset].most_common(6)]

            # Sort body chars by frequency
            body_keys.sort(key=lambda k: -onset_body_total[k])
            for (on, bc) in body_keys[:8]:
                n_pred = onset_body_total[(on, bc)]
                print(f"  body_char='{bc}' (N={n_pred}):", end='')
                notable = []
                for succ in top_succs:
                    obs = body_bigrams[(on, bc)][succ]
                    base_p = baseline_succ[onset][succ] / base_total
                    exp = n_pred * base_p
                    E = obs / exp if exp >= 3 else None
                    if E is not None and (E >= 1.4 or E <= 0.6):
                        direction = '↑' if E >= 1.4 else '↓'
                        notable.append(f"{succ}={E:.2f}×{direction}(N={obs})")
                if notable:
                    print(' ' + ', '.join(notable))
                else:
                    print(' near-baseline')

        # Summary: which (onset, body_char) groups show strongest enrichment E≥1.5 at N≥10?
        print(f"\n{'='*65}")
        print(f"  {dialect}: All enriched cases E≥1.5× at N≥10")
        print(f"{'='*65}")
        enriched_cases = []
        for (on, bc), n_pred in onset_body_total.items():
            if n_pred < 15:
                continue
            base_total = sum(baseline_succ[on].values())
            if base_total < 20:
                continue
            for succ, obs in body_bigrams[(on, bc)].items():
                base_p = baseline_succ[on][succ] / base_total
                exp = n_pred * base_p
                if exp >= 3 and obs >= 10:
                    E = obs / exp
                    if E >= 1.5:
                        enriched_cases.append((on, bc, succ, obs, exp, E))

        enriched_cases.sort(key=lambda x: -x[5])
        print(f"  {'predecessor':<12} {'succ':>6} {'obs':>5} {'exp':>6} {'E':>6}")
        for (on, bc, succ, obs, exp, E) in enriched_cases[:25]:
            print(f"  {on}+'{bc}'→{succ:<8}: obs={obs:>4}, exp={exp:>5.1f}, E={E:.2f}×")

        # Depleted cases E≤0.5× at N≥5 observations with exp≥3
        print(f"\n{dialect}: Depleted cases E≤0.5× at N(obs)≥5, exp≥3")
        depleted = []
        for (on, bc), n_pred in onset_body_total.items():
            if n_pred < 15:
                continue
            base_total = sum(baseline_succ[on].values())
            if base_total < 20:
                continue
            for succ in baseline_succ[on]:
                obs = body_bigrams[(on, bc)][succ]
                base_p = baseline_succ[on][succ] / base_total
                exp = n_pred * base_p
                if exp >= 5 and obs <= exp * 0.5:
                    E = obs / exp
                    depleted.append((on, bc, succ, obs, exp, E))
        depleted.sort(key=lambda x: x[5])
        for (on, bc, succ, obs, exp, E) in depleted[:15]:
            print(f"  {on}+'{bc}'→{succ:<8}: obs={obs:>4}, exp={exp:>5.1f}, E={E:.2f}×")

if __name__ == '__main__':
    main()
