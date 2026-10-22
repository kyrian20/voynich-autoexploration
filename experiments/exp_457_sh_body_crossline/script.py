"""
exp_457: B sh-onset Body-Conditional Cross-Line Routing (H_new_T)
Q: Is the B sh→d cross-line coupling (F438, E=1.58×/N=19) driven by
   non-shedy (bare/aiin-body) sh words at LL, while shedy at LL routes
   to qok (continuing the within-line rule)?

Prediction 1 (edy extends cross-line): shedy at LL → qok E≥1.3×;
   bare/aiin sh at LL → d E≥2.0×.
Prediction 2 (edy within-line only): shedy at LL → d same as aggregate;
   both groups route similarly.

Also: extend to other onset classes (ch, ok, ol) to check broader edy/aiin
body-class cross-line asymmetry (H_new_U exploration).
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

def collect_crossline_body_bigrams(folios, dialect_map, target_dialect):
    cl_body = defaultdict(Counter)   # (ll_onset, ll_body_char) -> Counter(lf_onset)
    ll_body_total = Counter()         # (ll_onset, ll_body_char) -> total
    lf_onset_total = Counter()        # lf_onset -> total
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
            cl_body[(ll_on, ll_bc)][lf_on] += 1
            ll_body_total[(ll_on, ll_bc)] += 1
            lf_onset_total[lf_on] += 1
            total_cl += 1

    return cl_body, ll_body_total, lf_onset_total, total_cl

def analyze_onset_body_cl(onset, cl_body, ll_body_total, lf_onset_total, total_cl,
                           target_lf_classes=None):
    """Print body-conditional cross-line analysis for a given onset class."""
    body_keys = [(on, bc) for (on, bc) in ll_body_total if on == onset]
    body_keys.sort(key=lambda k: -ll_body_total[k])

    # Aggregate onset total
    onset_total = sum(ll_body_total[k] for k in body_keys)
    if onset_total == 0:
        return

    # Determine top LF successors overall for this onset
    all_after = Counter()
    for bk in body_keys:
        for lf, cnt in cl_body[bk].items():
            all_after[lf] += cnt
    if target_lf_classes:
        top_lf = target_lf_classes
    else:
        top_lf = [lf for lf, _ in all_after.most_common(6)]

    print(f"\n{'='*60}")
    print(f"  {onset.upper()}-onset at LL (total N={onset_total})")
    print(f"  Overall cross-line dist: ", end='')
    for lf in top_lf:
        obs_total = all_after[lf]
        base_p = lf_onset_total[lf] / total_cl
        exp_total = onset_total * base_p
        E = obs_total / exp_total if exp_total > 0 else 0
        print(f"{lf}={E:.2f}×(N={obs_total}) ", end='')
    print()
    print(f"{'='*60}")

    # Print body-conditional breakdown
    header = f"  {'body':>8}  {'N(LL)':>6}"
    for lf in top_lf:
        header += f"  {'→'+lf:>12}"
    print(header)

    for (on, bc) in body_keys[:8]:
        n_ll = ll_body_total[(on, bc)]
        if n_ll < 5:
            continue
        # Show top words in this body group
        print(f"  '{bc}':  {n_ll:>6}", end='')
        for lf in top_lf:
            obs = cl_body[(on, bc)][lf]
            base_p = lf_onset_total[lf] / total_cl
            exp = n_ll * base_p
            if exp >= 1.0:
                E = obs / exp
                mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                print(f"  {E:.2f}×{mk}(N={obs:2d})", end='')
            else:
                print(f"  {'--':>12}", end='')
        print()

    # Edy vs aiin contrast table
    print(f"\n  Edy vs aiin body contrast for {onset.upper()}:")
    edy_key = (onset, 'e')
    ain_key = (onset, 'a')
    n_edy = ll_body_total.get(edy_key, 0)
    n_ain = ll_body_total.get(ain_key, 0)
    if n_edy > 0 or n_ain > 0:
        print(f"  {'body':>6}  {'N':>5}  ", end='')
        for lf in top_lf:
            print(f"  {'→'+lf:>10}", end='')
        print()
        for bc_label, n_bc, key in [('edy(e)', n_edy, edy_key), ('aiin(a)', n_ain, ain_key)]:
            if n_bc < 3:
                print(f"  {bc_label:>6}  {n_bc:>5}  (insufficient N)")
                continue
            print(f"  {bc_label:>6}  {n_bc:>5}  ", end='')
            for lf in top_lf:
                obs = cl_body[key][lf]
                base_p = lf_onset_total[lf] / total_cl
                exp = n_bc * base_p
                if exp >= 0.5:
                    E = obs / exp
                    mk = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                    print(f"  {E:.2f}×{mk}(N={obs:2d})", end='')
                else:
                    print(f"  {'dir':>10}", end='')
            print()

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    # Focus: B-dialect
    cl_body, ll_body_total, lf_onset_total, total_cl = \
        collect_crossline_body_bigrams(folios, dialect_map, 'B')

    print("="*60)
    print("  EXP_457: Body-Conditional Cross-Line Routing (B-dialect)")
    print(f"  Total CL pairs: {total_cl}")
    print("="*60)

    # Primary focus: sh onset (H_new_T)
    # Key question: does shedy at LL → d or → qok?
    analyze_onset_body_cl('sh', cl_body, ll_body_total, lf_onset_total, total_cl,
                          target_lf_classes=['d', 'qok', 'sh', 's', 'ch'])

    # Secondary: verify d onset (F441 confirmation)
    analyze_onset_body_cl('d', cl_body, ll_body_total, lf_onset_total, total_cl,
                          target_lf_classes=['sh', 'qok', 's', 'ch', 'd'])

    # H_new_U exploration: ch onset body split CL
    analyze_onset_body_cl('ch', cl_body, ll_body_total, lf_onset_total, total_cl,
                          target_lf_classes=['ch', 'qok', 'd', 'sh', 's'])

    # ok onset body split CL (ok→y is F438)
    analyze_onset_body_cl('ok', cl_body, ll_body_total, lf_onset_total, total_cl,
                          target_lf_classes=['y', 'ok', 'qok', 'd', 'ch'])

    # s onset body split CL (s→s is F438)
    analyze_onset_body_cl('s', cl_body, ll_body_total, lf_onset_total, total_cl,
                          target_lf_classes=['s', 'sh', 'qok', 'd', 'ch'])

    # Summary: notable edy/aiin body contrasts
    print(f"\n{'='*60}")
    print("  SUMMARY: edy vs aiin body-class cross-line enrichment comparison")
    print(f"  (within-class E comparison: edy vs aiin body for each onset)")
    print(f"{'='*60}")
    print(f"  {'onset':>6}  {'body':>6}  {'N':>5}  top-lf   E_CL   (vs within-line rule)")

    for onset in ['sh', 'ch', 'ok', 'd', 's', 'qok', 'ol']:
        for bc in ['e', 'a']:
            key = (onset, bc)
            n_ll = ll_body_total.get(key, 0)
            if n_ll < 8:
                continue
            # Find best CL enrichment
            best_lf, best_E, best_N = '', 0.0, 0
            for lf, obs in cl_body[key].items():
                base_p = lf_onset_total[lf] / total_cl
                exp = n_ll * base_p
                if exp >= 2 and obs >= 4:
                    E = obs / exp
                    if E > best_E:
                        best_E, best_lf, best_N = E, lf, obs
            if best_E >= 1.3:
                # Annotate with known within-line rule
                wl_note = ''
                if onset == 'qok' and bc == 'e': wl_note = '← F439 qok+edy→qok within'
                if onset == 'qok' and bc == 'a': wl_note = '← F439 qok+aiin→sh within'
                if onset == 'sh' and bc == 'e': wl_note = '← F439/F372 shedy→qok within'
                print(f"  {onset:>6}  {'edy' if bc=='e' else 'aiin':>6}  {n_ll:>5}  →{best_lf:<6}  {best_E:.2f}×(N={best_N})  {wl_note}")

if __name__ == '__main__':
    main()
