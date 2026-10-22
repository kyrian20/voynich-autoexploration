"""
exp_455: Cross-Line Body-Conditional Bigrams (H_new_R)
Q: Does the qok+a-body→sh within-line rule (F439, E=1.73×) extend cross-line?
   When a line ends with qok+a-body (vs qok+e-body), does the next line open
   with sh more (vs qok) at LF?

Extend to: do other F439 body-conditional rules (ol body split, ok body split)
operate at the cross-line level?

Method: Cross-line analysis (LL word body-char → LF onset of next line).
Compare body-conditional cross-line enrichment to within-line finding from F439.
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
    """
    For each consecutive line pair (LL of line i → LF of line i+1) in cont lines:
    Record (LL_onset, LL_body_char, LF_onset).
    """
    cl_body = defaultdict(Counter)   # (ll_onset, ll_body_char) -> Counter(lf_onset)
    ll_onset_total = Counter()        # ll_onset -> total
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
            ll_onset_total[ll_on] += 1
            ll_body_total[(ll_on, ll_bc)] += 1
            lf_onset_total[lf_on] += 1
            total_cl += 1

    return cl_body, ll_onset_total, ll_body_total, lf_onset_total, total_cl

def main():
    folios = parse_corpus()
    dialect_map = classify_dialects(folios)

    for dialect in ['B', 'A']:
        cl_body, ll_onset_total, ll_body_total, lf_onset_total, total_cl = \
            collect_crossline_body_bigrams(folios, dialect_map, dialect)

        print(f"\n{'='*60}")
        print(f"  {dialect}-DIALECT: Cross-line body-conditional bigrams")
        print(f"  Total CL pairs: {total_cl}")
        print(f"{'='*60}")

        # For each onset class with body data, check body-conditional CL routing
        # Focus on the onset classes from F439: qok, ol, ok, sh
        for onset in ['qok', 'ol', 'ok', 'sh', 'ch', 'd', 'y', 'ot']:
            total_ll_onset = ll_onset_total[onset]
            if total_ll_onset < 10: continue

            # Baseline: P(lf_onset | ll_onset) from onset total
            # For each body group
            body_keys = [(on, bc) for (on, bc) in ll_body_total if on == onset]
            body_keys.sort(key=lambda k: -ll_body_total[k])

            print(f"\n  {onset}-onset LL (total N={total_ll_onset}):")
            print(f"  {'body':>6}  {'N(LL)':>6}", end='')
            # Determine top successors for this onset class
            all_lf_after = Counter()
            for bc_key in body_keys:
                for lf_on, cnt in cl_body[bc_key].items():
                    all_lf_after[lf_on] += cnt
            top_lf = [lf for lf, _ in all_lf_after.most_common(5)]
            for lf in top_lf:
                print(f"  →{lf}", end='')
            print()

            # Baseline cross-line E for this onset (vs global LF distribution)
            for (on, bc) in body_keys[:6]:
                n_ll = ll_body_total[(on, bc)]
                if n_ll < 5: continue
                print(f"  '{bc}':  {n_ll:>6}", end='')
                for lf in top_lf:
                    obs = cl_body[(on, bc)][lf]
                    # baseline: fraction of all CL pairs with this LF onset
                    base_p = lf_onset_total[lf] / total_cl
                    exp = n_ll * base_p
                    if exp >= 1:
                        E = obs / exp
                        marker = '↑' if E >= 1.4 else ('↓' if E <= 0.6 else ' ')
                        print(f"  {E:.2f}×{marker}(N={obs})", end='')
                    else:
                        print(f"  --", end='')
                print()

        # Summary: notable body-conditional CL enrichments
        print(f"\n  {dialect} notable body-conditional CL enrichments (E≥1.4, obs≥5):")
        notable = []
        for (on, bc), n_ll in ll_body_total.items():
            if n_ll < 8: continue
            for lf_on, obs in cl_body[(on, bc)].items():
                base_p = lf_onset_total[lf_on] / total_cl
                exp = n_ll * base_p
                if exp >= 2 and obs >= 5:
                    E = obs / exp
                    if E >= 1.4:
                        # Also compute overall onset-level E for this ll_onset → lf_onset
                        total_ll_on = ll_onset_total[on]
                        total_lf_all = sum(cl_body[(on, bc2)][lf_on] for (on2, bc2) in ll_body_total if on2 == on)
                        overall_E = total_lf_all / (total_ll_on * base_p) if total_ll_on > 0 and base_p > 0 else 0
                        notable.append((on, bc, lf_on, obs, exp, E, overall_E, n_ll))
        notable.sort(key=lambda x: -x[5])
        print(f"  {'LL onset+body':>15}  {'→LF':>6}  {'obs':>5}  {'exp':>6}  {'E_body':>7}  {'E_overall':>10}  {'N_LL':>6}")
        for (on, bc, lf_on, obs, exp, E, oE, n_ll) in notable[:20]:
            within_note = ' (F439)' if (dialect=='B' and on=='qok' and bc=='a' and lf_on=='sh') else ''
            within_note += ' (F439)' if (dialect=='B' and on=='qok' and bc=='e' and lf_on=='qok') else ''
            print(f"  {on}+'{bc}'→{lf_on:<8}  {obs:>5}  {exp:>6.1f}  {E:>7.2f}×  {oE:>10.2f}×  {n_ll:>6}{within_note}")

if __name__ == '__main__':
    main()
