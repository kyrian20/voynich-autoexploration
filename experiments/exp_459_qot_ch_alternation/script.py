"""
exp_459: B ch↔qot Cross-Line Alternation and qot Body-Conditional CL (H_new_X)
Q: Does B qot at LL → ch at next LF (completing ch↔qot cross-line alternating pair)?
   Does qot+edy at LL specifically drive the →ch cross-line coupling?
   For A: does A ch→ch CL chain extend to multiple lines?

Method:
  Part A: B qot-onset body-conditional cross-line (LL→next LF).
  Part B: Full B cross-line onset matrix comparison (to identify all complementary pairs).
  Part C: A dialect — ch cross-line triple chain (ch at LL of line N, ch at LF of N+1, ch at LL of N+1 or LF of N+2).
"""
from pathlib import Path as _RepositoryPath
import re
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

def collect_all_cl_pairs(folios, dialect_map, target_dialect):
    """Collect all (LL_onset, LL_body, LF_onset) triples for cross-line pairs."""
    cl_pairs = []   # [(ll_on, ll_bc, lf_on)]
    lf_total = Counter()
    ll_on_total = Counter()
    total_cl = 0

    for folio, lines in folios.items():
        if folio not in dialect_map or dialect_map[folio] != target_dialect:
            continue
        n = len(lines)
        if n < 3: continue
        cont_lines = lines[1:-1]
        cn = len(cont_lines)
        for ci in range(cn - 1):
            ll_word = cont_lines[ci][-1]
            lf_word = cont_lines[ci+1][0]
            ll_on = get_onset(ll_word)
            lf_on = get_onset(lf_word)
            if ll_on == 'other' or lf_on == 'other': continue
            ll_bc = get_first_body_char(ll_word, ll_on)
            cl_pairs.append((ci, ll_on, ll_bc, lf_on, folio))
            lf_total[lf_on] += 1
            ll_on_total[ll_on] += 1
            total_cl += 1

    return cl_pairs, lf_total, ll_on_total, total_cl

def analyze_qot_cl_body(cl_pairs, lf_total, ll_on_total, total_cl, dialect):
    """Body-conditional analysis for qot onset at LL."""
    qot_body_cl = defaultdict(Counter)
    qot_body_total = Counter()

    for ci, ll_on, ll_bc, lf_on, folio in cl_pairs:
        if ll_on != 'qot': continue
        qot_body_cl[ll_bc][lf_on] += 1
        qot_body_total[ll_bc] += 1

    qot_total = sum(qot_body_total.values())
    print(f"\n{dialect}-dialect: qot at LL → next LF (total N={qot_total})")
    print(f"  Overall qot CL distribution:")
    all_qot_cl = Counter()
    for bc_data in qot_body_cl.values():
        all_qot_cl.update(bc_data)
    top_lf = ['ch', 'qok', 'd', 's', 'sh', 'qot', 'y']
    for lf in top_lf:
        obs = all_qot_cl[lf]
        base_p = lf_total[lf] / total_cl
        exp = qot_total * base_p
        if exp >= 1:
            E = obs / exp
            mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
            print(f"    →{lf}: E={E:.2f}×{mk}(N={obs})", end='  ')
    print()

    print(f"\n  Body-conditional breakdown:")
    header = f"  {'body':>6}  {'N':>5}"
    for lf in top_lf:
        header += f"  {'→'+lf:>10}"
    print(header)

    body_keys = sorted(qot_body_total.keys(), key=lambda bc: -qot_body_total[bc])
    for bc in body_keys:
        n = qot_body_total[bc]
        if n < 5: continue
        row = f"  '{bc}':  {n:>5}"
        for lf in top_lf:
            obs = qot_body_cl[bc][lf]
            base_p = lf_total[lf] / total_cl
            exp = n * base_p
            if exp >= 0.8:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"  {E:.2f}×{mk}(N={obs:2d})"
            else:
                row += f"  {'dir('+str(obs)+')':>10}"
        print(row)

    # edy vs aiin focus
    print(f"\n  edy vs aiin body contrast for qot CL ({dialect}):")
    for bc_label, bc in [('edy(e)', 'e'), ('aiin(a)', 'a')]:
        n = qot_body_total.get(bc, 0)
        if n < 3:
            print(f"    {bc_label}: N={n} (insufficient)")
            continue
        row = f"    {bc_label}: N={n}  "
        for lf in top_lf:
            obs = qot_body_cl[bc][lf]
            base_p = lf_total[lf] / total_cl
            exp = n * base_p
            if exp >= 0.5:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"→{lf}={E:.2f}×{mk}(N={obs}) "
            elif obs > 0:
                row += f"→{lf}=dir(N={obs}) "
        print(row)

def analyze_full_cl_matrix(cl_pairs, lf_total, ll_on_total, total_cl, dialect,
                            onsets_of_interest=None):
    """Print condensed cross-line enrichment matrix."""
    if onsets_of_interest is None:
        onsets_of_interest = ['ch', 'qot', 'sh', 'd', 'qok', 's', 'ok', 'y']

    cl_matrix = defaultdict(Counter)
    for ci, ll_on, ll_bc, lf_on, folio in cl_pairs:
        cl_matrix[ll_on][lf_on] += 1

    print(f"\n{dialect}-dialect: Cross-line onset enrichment matrix (E values, LL→next LF)")
    header = f"  {'LL\\LF':>6}"
    for lf in onsets_of_interest:
        header += f"  {'→'+lf:>9}"
    print(header)
    print(f"  {'N(LL)':>6}", end='')
    for lf in onsets_of_interest:
        print(f"  {lf_total[lf]:>9}", end='')
    print()

    for ll in onsets_of_interest:
        n_ll = ll_on_total[ll]
        if n_ll < 10: continue
        row = f"  {ll+':':>6}"
        for lf in onsets_of_interest:
            obs = cl_matrix[ll][lf]
            base_p = lf_total[lf] / total_cl
            exp = n_ll * base_p
            if exp >= 2:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                row += f"  {E:.2f}×{mk}"
            else:
                row += f"  {'--':>9}"
        print(row)

def analyze_a_ch_chain(cl_pairs, lf_total, ll_on_total, total_cl, dialect):
    """Test: does A ch→ch CL chain extend? (ch at LL of line N predicts ch at LF of N+1,
       and ch at LL of N+1 predicts ch at LF of N+2).
    """
    if dialect != 'A':
        return

    # Index cl_pairs by (folio, ci)
    from collections import defaultdict as dd
    indexed = {}  # (folio, ci) -> (ll_on, ll_bc, lf_on)
    for item in cl_pairs:
        ci, ll_on, ll_bc, lf_on, folio = item
        indexed[(folio, ci)] = (ll_on, ll_bc, lf_on)

    # Find triple patterns: (folio, ci): ll=ch, LF=ch; then check (folio, ci+1): ll=ch, LF=?
    ch_ll_then_ch_lf = 0  # lines where ch-LL → ch-LF (CL pair 1)
    ch_ch_then_ch = 0     # of those, how many also have ch-LF at N+1 as LL-N+1 is ch
    ch_ll_total = 0

    for (folio, ci), (ll_on, ll_bc, lf_on) in indexed.items():
        if ll_on != 'ch': continue
        ch_ll_total += 1
        if lf_on != 'ch': continue
        ch_ll_then_ch_lf += 1
        # Check the next pair
        next_key = (folio, ci + 1)
        if next_key in indexed:
            next_ll_on, _, next_lf_on = indexed[next_key]
            if next_ll_on == 'ch' and next_lf_on == 'ch':
                ch_ch_then_ch += 1

    base_p_ch = lf_total['ch'] / total_cl
    base_p_ch_ll = ll_on_total['ch'] / sum(ll_on_total.values()) if sum(ll_on_total.values()) else 0

    print(f"\nA-dialect: ch→ch→ch cross-line triple chain analysis")
    print(f"  Total A ch at LL: {ch_ll_total}")
    print(f"  ch at LL → ch at next LF: N={ch_ll_then_ch_lf} (E={ch_ll_then_ch_lf/(ch_ll_total*base_p_ch):.2f}× vs base_p={base_p_ch:.3f})")
    if ch_ll_then_ch_lf > 0:
        # Expected triples if independent: ch_ll_then_ch_lf × P(next-line LL=ch) × P(next-next LF=ch)
        # But we need to check conditional: given ch-LF at N+1, what's P(ch-LL at N+1)?
        # Simpler: among ch_ll_then_ch_lf cases, how many extend?
        expected_triples = ch_ll_then_ch_lf * base_p_ch  # P(next pair also ch→ch)
        E_triple = ch_ch_then_ch / expected_triples if expected_triples > 0 else 0
        print(f"  Of ch→ch CL pairs: {ch_ch_then_ch}/{ch_ll_then_ch_lf} extend to triple chain")
        print(f"  Expected triples if random: {expected_triples:.1f}")
        print(f"  Triple chain E = {E_triple:.2f}×")


def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    print("="*65)
    print("  EXP_459: B ch↔qot Cross-Line Alternation (H_new_X)")
    print("="*65)

    for dialect in ['B', 'A']:
        cl_pairs, lf_total, ll_on_total, total_cl = collect_all_cl_pairs(folios, dialect_map, dialect)
        print(f"\n{'='*65}")
        print(f"  {dialect}-DIALECT (total CL pairs: {total_cl})")
        print(f"{'='*65}")

        # Part A: qot onset CL body-conditional
        analyze_qot_cl_body(cl_pairs, lf_total, ll_on_total, total_cl, dialect)

        # Part B: Full cross-line matrix
        analyze_full_cl_matrix(cl_pairs, lf_total, ll_on_total, total_cl, dialect)

    # Part C: A-dialect ch chain analysis
    cl_pairs_A, lf_total_A, ll_on_total_A, total_cl_A = collect_all_cl_pairs(folios, dialect_map, 'A')
    analyze_a_ch_chain(cl_pairs_A, lf_total_A, ll_on_total_A, total_cl_A, 'A')


if __name__ == '__main__':
    main()
