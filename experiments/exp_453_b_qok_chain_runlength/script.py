"""
exp_453: B qok Chain Run-Length Distribution (H_new_O)
Q: Does B qok self-replication (edy-body→qok E=1.52×) produce super-geometric chains?

Method: Extract all qok-onset word runs in B continuation lines.
Compare observed run-length distribution to geometric expectation.
Also: within qok chains, what fraction are edy-body vs aiin-body consecutive pairs?
Cross-check: A qok and B ot for comparison.
"""
from pathlib import Path as _RepositoryPath
import re
import math
from collections import defaultdict, Counter

ZL3B = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

ONSETS = ['qok','qot','qo','cth','ch','sh','ok','ot','ol','d','s','y','k','t','l','r','p','f','o']

def get_onset(word):
    for on in ONSETS:
        if word.startswith(on):
            return on
    return 'other'

def get_first_body_char(word, onset):
    body = word[len(onset):]
    return body[0] if body else '_'

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

def extract_runs(folios, dialect_map, target_dialect, target_onset):
    """Extract all runs of target_onset in continuation lines."""
    run_lengths = []
    run_bodies = []  # body chars in each run
    single_total = 0  # single occurrences (run=1)
    total_words = 0

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3:
            continue
        cont_lines = lines[1:-1]

        for line_words in cont_lines:
            total_words += len(line_words)
            current_run = []
            for w in line_words:
                if get_onset(w) == target_onset:
                    current_run.append(w)
                else:
                    if current_run:
                        run_lengths.append(len(current_run))
                        run_bodies.append([get_first_body_char(w, target_onset) for w in current_run])
                        current_run = []
            if current_run:
                run_lengths.append(len(current_run))
                run_bodies.append([get_first_body_char(w, target_onset) for w in current_run])

    return run_lengths, run_bodies, total_words

def geometric_fit(run_lengths):
    """Fit geometric distribution: P(L=k) = p*(1-p)^(k-1) via MLE."""
    if not run_lengths:
        return 0, 0
    n = len(run_lengths)
    mean_L = sum(run_lengths) / n
    p = 1.0 / mean_L  # MLE for geometric
    return p, mean_L

def compare_to_geometric(run_lengths, p, n_runs):
    """Compare observed run-length distribution to geometric."""
    from collections import Counter
    obs = Counter(run_lengths)
    max_len = max(run_lengths) if run_lengths else 0

    print(f"  {'len':>5} {'obs':>6} {'exp_geo':>8} {'ratio':>7}")
    total_obs = sum(obs.values())
    cumulative_obs = 0
    cumulative_exp = 0
    for L in range(1, min(max_len+1, 12)):
        obs_n = obs.get(L, 0)
        exp_n = n_runs * p * (1-p)**(L-1)
        ratio = obs_n / exp_n if exp_n > 0 else 0
        cumulative_obs += obs_n
        cumulative_exp += exp_n
        marker = ' <-- EXCESS' if ratio > 2.0 and obs_n >= 3 else (' <-- DEFICIT' if ratio < 0.5 and exp_n >= 3 else '')
        print(f"  {L:>5} {obs_n:>6} {exp_n:>8.1f} {ratio:>7.2f}{marker}")

    # Tail summary
    tail_obs = sum(obs[L] for L in obs if L >= 5)
    tail_exp = sum(n_runs * p * (1-p)**(L-1) for L in range(5, 100))
    print(f"  {'≥5':>5} {tail_obs:>6} {tail_exp:>8.1f} {tail_obs/tail_exp if tail_exp>0 else 0:>7.2f}  (tail)")

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    comparisons = [
        ('B', 'qok', 'B qok (F439: edy-body self-replication)'),
        ('A', 'qok', 'A qok (baseline)'),
        ('B', 'ot', 'B ot (from exp_419: geometric)'),
        ('A', 'y', 'A y (F410: super-geometric)'),
        ('B', 'y', 'B y (baseline)'),
    ]

    for (dialect, onset, label) in comparisons:
        run_lengths, run_bodies, total_words = extract_runs(folios, dialect_map, dialect, onset)
        if not run_lengths:
            continue

        n_runs = len(run_lengths)
        total_tokens = sum(run_lengths)
        p, mean_L = geometric_fit(run_lengths)

        print(f"\n{'='*55}")
        print(f"  {label}")
        print(f"  N_runs={n_runs}, total_onset_tokens={total_tokens}")
        print(f"  mean_L={mean_L:.3f}, geometric_p={p:.3f}")
        print(f"  Single occurrences (L=1): {sum(1 for l in run_lengths if l==1)}")
        print(f"  Chains L≥2: {sum(1 for l in run_lengths if l>=2)}")
        print(f"  Chains L≥3: {sum(1 for l in run_lengths if l>=3)}")
        print(f"  Max chain: {max(run_lengths)}")
        print()
        compare_to_geometric(run_lengths, p, n_runs)

        # For qok chains: body-char analysis within runs
        if onset == 'qok' and dialect == 'B':
            print(f"\n  B qok chain body-char analysis:")
            edy_body_consecutive = 0
            aiin_body_consecutive = 0
            total_consecutive_pairs = 0
            for bodies in run_bodies:
                if len(bodies) >= 2:
                    for i in range(len(bodies)-1):
                        total_consecutive_pairs += 1
                        b1, b2 = bodies[i], bodies[i+1]
                        if b1 == 'e' and b2 == 'e':
                            edy_body_consecutive += 1
                        elif b1 == 'a' and b2 == 'a':
                            aiin_body_consecutive += 1

            # Overall body-char distribution in chains vs singletons
            all_chain_bodies = [b for bodies in run_bodies for b in bodies]
            single_bodies = [bodies[0] for bodies in run_bodies if len(bodies) == 1]
            multi_bodies = [b for bodies in run_bodies if len(bodies) >= 2 for b in bodies]

            chain_bc = Counter(all_chain_bodies)
            single_bc = Counter(single_bodies)
            multi_bc = Counter(multi_bodies)

            n_chain = sum(chain_bc.values())
            n_single = sum(single_bc.values())
            n_multi = sum(multi_bc.values())

            print(f"  Body-char distribution — singletons vs chain members (len≥2):")
            print(f"  {'body':>6} {'single_%':>10} {'chain2+_%':>10}")
            for bc in ['e', 'a', 'c', 'o', 'y', '_']:
                sp = single_bc.get(bc, 0) / n_single if n_single > 0 else 0
                mp = multi_bc.get(bc, 0) / n_multi if n_multi > 0 else 0
                ratio = mp / sp if sp > 0 else 0
                marker = ' E={:.2f}×'.format(ratio) if ratio > 1.2 or ratio < 0.8 else ''
                print(f"  '{bc}':   {sp:>9.1%} {mp:>10.1%}{marker}")

            if total_consecutive_pairs > 0:
                print(f"\n  qok consecutive pairs in chains:")
                print(f"    edy+edy: {edy_body_consecutive}/{total_consecutive_pairs} = {edy_body_consecutive/total_consecutive_pairs:.1%}")
                print(f"    aiin+aiin: {aiin_body_consecutive}/{total_consecutive_pairs} = {aiin_body_consecutive/total_consecutive_pairs:.1%}")

    # Summary: is B qok super-geometric?
    print("\n\n=== Summary: Run-length tail comparison ===")
    print("Super-geometric = observed ≥5 chains significantly exceed geometric prediction.")
    for (dialect, onset, label) in comparisons:
        run_lengths, _, _ = extract_runs(folios, dialect_map, dialect, onset)
        if not run_lengths:
            continue
        n_runs = len(run_lengths)
        p, _ = geometric_fit(run_lengths)
        obs_ge3 = sum(1 for l in run_lengths if l >= 3)
        exp_ge3 = n_runs * sum(p * (1-p)**(L-1) for L in range(3, 100))
        E_tail = obs_ge3 / exp_ge3 if exp_ge3 > 0 else 0
        obs_ge5 = sum(1 for l in run_lengths if l >= 5)
        exp_ge5 = n_runs * sum(p * (1-p)**(L-1) for L in range(5, 100))
        E_tail5 = obs_ge5 / exp_ge5 if exp_ge5 > 0 else 0
        print(f"  {label[:30]:<32} L≥3: E={E_tail:.2f}×(obs={obs_ge3}/exp={exp_ge3:.1f})  L≥5: E={E_tail5:.2f}×(obs={obs_ge5}/exp={exp_ge5:.1f})")

if __name__ == '__main__':
    main()
