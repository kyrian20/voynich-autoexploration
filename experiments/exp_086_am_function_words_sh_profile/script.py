"""
exp_086: -am Core Function Words & sh-Onset Positional Profile
Tests H144, H145, H142

H144: sh-onset has low line-last% and high line-first% — explaining -am suppression (sh-words are line-openers, not line-enders)
H145: dam/otam/okam/qokam are a closed class of within-para line-ending function words (high LLast%, low LFirst%, within-para enriched)
H142: Positional grammar models hold across ALL folio sections (Pharma A, Astro B, Special) — not section-specific
"""
from pathlib import Path as _RepositoryPath

import re
from collections import defaultdict

DATA_PATH = str(_RepositoryPath(__file__).resolve().parents[2] / 'data/transcriptions/eva_zl3b.txt')

# Folios classified as aiin-dominant (from prior experiments)
AIIN_DOM_FOLIOS = {
    'f1r','f1v','f2r','f2v','f3r','f3v','f4r','f4v',
    'f5r','f5v','f6r','f6v','f7r','f7v','f8r','f8v',
    'f13r','f13v','f16r','f16v','f65r','f65v','f66r','f66v'
}

def folio_base(folio):
    return folio.split('.')[0]

def is_para_start(locus_code):
    return locus_code.lstrip('+*=/~&').startswith('@')

def is_body(locus_code):
    return locus_code.lstrip('+*@=/~&').startswith('P')

def get_onset(word):
    if word.startswith('qo'): return 'qo'
    if word.startswith('ch'): return 'ch'
    if word.startswith('sh'): return 'sh'
    if word.startswith('cth'): return 'cth'
    if word and word[0] in 'p': return 'p'
    if word and word[0] in 't': return 't'
    if word and word[0] in 'k': return 'k'
    if word and word[0] in 'd': return 'd'
    if word and word[0] in 's': return 's'
    if word and word[0] in 'y': return 'y'
    if word and word[0] in 'o': return 'o'
    return 'other'

def get_suffix(word):
    for suf in ['eedy','eey','edy','edy','aiin','ain','am','ey','dy','y','ol','or','ar']:
        if word.endswith(suf) and len(word) > len(suf):
            return suf
    return None

def get_edy_rate(words):
    if not words: return 0.0
    n = sum(1 for w in words if w.endswith('edy') or w.endswith('eedy'))
    return n / len(words)

def is_b_dialect(folio_base_name, edy_rate_map):
    return edy_rate_map.get(folio_base_name, 0) >= 0.05

# Parse data
def load_data():
    records = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            m = re.match(r'^<([^>]+)>', line)
            if not m: continue
            locus_raw = m.group(1)
            text = line[m.end():].strip()
            parts = locus_raw.split(',')
            if len(parts) < 2: continue
            folio_raw = parts[0]
            locus_code = parts[1]
            folio = folio_raw.lstrip('+*=&~')
            if not is_body(locus_code): continue
            words = [w for w in re.split(r'[-.\s]', text) if re.match(r'^[a-z]+$', w) and len(w) >= 2]
            if not words: continue
            fb = folio_base(folio)
            records.append({
                'folio': fb,
                'folio_raw': folio_raw,
                'locus': locus_code,
                'words': words,
                'is_para_start': is_para_start(locus_code),
            })
    return records

def compute_edy_rates(records):
    folio_words = defaultdict(list)
    for rec in records:
        folio_words[rec['folio']].extend(rec['words'])
    return {f: get_edy_rate(ws) for f, ws in folio_words.items()}

def assign_dialects(records, edy_rate_map):
    for rec in records:
        rec['is_b'] = is_b_dialect(rec['folio'], edy_rate_map)
        rec['is_a'] = not rec['is_b']
        rec['is_aiin_dom'] = rec['folio'] in AIIN_DOM_FOLIOS
    return records

def classify_para_boundary(records):
    """Mark is_para_final: True if the NEXT record is a para-start."""
    for i, rec in enumerate(records):
        if i + 1 < len(records):
            rec['is_para_final'] = records[i+1]['is_para_start']
        else:
            rec['is_para_final'] = False
    return records

# Section classification
def classify_section(folio):
    """Rough section classification by folio number."""
    # Extract number
    m = re.match(r'f(\d+)([rv])', folio)
    if not m: return 'unknown'
    n = int(m.group(1))
    side = m.group(2)
    # Herbal: f1-f57 (rough)
    if n <= 57: return 'herbal'
    # Astro: f67-f73
    if 67 <= n <= 73: return 'astro'
    # Cosmo: f75-f84
    if 75 <= n <= 84: return 'cosmo'
    # Pharma: f87-f102
    if 87 <= n <= 102: return 'pharma'
    # Stars/Special: f103-f116
    if 103 <= n <= 116: return 'stars'
    # Bio: f75-f84 overlap — use Currier B dialect assignment mainly
    return 'other'


def h144_sh_onset_positional_profile(a_recs, b_recs):
    """
    H144: sh-onset has low line-last% and high line-first% in both dialects.
    Compare to other onset classes. If sh-words are pure line-openers, -am suppression follows.
    """
    print("=== H144: sh-Onset Positional Profile (Line-Opener Hypothesis) ===\n")

    for dialect_name, recs in [('A', a_recs), ('B', b_recs)]:
        print(f"--- Currier {dialect_name}: Onset positional profiles ---")
        onset_stats = defaultdict(lambda: {'total': 0, 'lf': 0, 'll': 0, 'psf': 0, 'pfl': 0, 'am_count': 0})

        for rec in recs:
            words = rec['words']
            n = len(words)
            if n == 0: continue
            psf = rec['is_para_start']
            pfl = rec['is_para_final']

            for i, w in enumerate(words):
                onset = get_onset(w)
                s = onset_stats[onset]
                s['total'] += 1
                s['am_count'] += 1 if w.endswith('am') and len(w) > 2 else 0
                if i == 0:
                    s['lf'] += 1
                    if psf: s['psf'] += 1
                if i == n - 1:
                    s['ll'] += 1
                    if pfl: s['pfl'] += 1

        # Print table
        print(f"{'Onset':<8} {'Total':>7} {'LFirst%':>8} {'LLast%':>8} {'PSFirst%':>9} {'PFLast%':>8} {'AM%':>7}")
        for onset in ['qo','ch','sh','p','t','k','d','s','y','o','other']:
            s = onset_stats[onset]
            if s['total'] == 0: continue
            lf_pct = 100 * s['lf'] / s['total']
            ll_pct = 100 * s['ll'] / s['total']
            psf_pct = 100 * s['psf'] / s['total']
            pfl_pct = 100 * s['pfl'] / s['total']
            am_pct = 100 * s['am_count'] / s['total']
            print(f"  {onset:<6} {s['total']:>7} {lf_pct:>7.1f}% {ll_pct:>7.1f}% {psf_pct:>8.1f}% {pfl_pct:>7.1f}% {am_pct:>6.1f}%")
        print()


def h145_am_core_function_words(a_recs, b_recs):
    """
    H145: dam, otam, okam, qokam are a closed class of within-para line-ending function words.
    Profile: high LLast%, low LFirst%, within-para enriched, near-zero PSFirst.
    """
    print("=== H145: -am Core Function Word Class (dam, otam, okam, qokam) ===\n")

    CORE_AM = {'dam', 'otam', 'okam', 'qokam', 'cham', 'ram'}
    REFERENCE_CLOSERS = {'oly', 'oldy'}  # pure line-closers for comparison
    REFERENCE_DAIIN = {'daiin'}  # para-closer

    def word_stats(recs, target_words):
        stats = {w: {'total': 0, 'lf': 0, 'll': 0, 'psf': 0, 'pfl': 0, 'within_para': 0} for w in target_words}
        for rec in recs:
            words = rec['words']
            n = len(words)
            psf = rec['is_para_start']
            pfl = rec['is_para_final']
            for i, w in enumerate(words):
                if w not in target_words: continue
                s = stats[w]
                s['total'] += 1
                if not psf and not pfl: s['within_para'] += 1
                if i == 0:
                    s['lf'] += 1
                    if psf: s['psf'] += 1
                if i == n - 1:
                    s['ll'] += 1
                    if pfl: s['pfl'] += 1
        return stats

    for dialect_name, recs in [('A', a_recs), ('B', b_recs)]:
        print(f"--- Currier {dialect_name}: Core -am function word profiles ---")
        all_target = CORE_AM | REFERENCE_CLOSERS | REFERENCE_DAIIN
        stats = word_stats(recs, all_target)
        print(f"{'Word':<12} {'n':>5} {'LFirst%':>8} {'LLast%':>7} {'PSFirst%':>9} {'PFLast%':>8} {'WithinPara%':>12}")
        for w in sorted(all_target, key=lambda x: -(stats[x]['total'])):
            s = stats[w]
            if s['total'] == 0: continue
            lf_pct = 100 * s['lf'] / s['total']
            ll_pct = 100 * s['ll'] / s['total']
            psf_pct = 100 * s['psf'] / s['total']
            pfl_pct = 100 * s['pfl'] / s['total']
            wp_pct = 100 * s['within_para'] / s['total']
            print(f"  {w:<10} {s['total']:>5} {lf_pct:>7.1f}% {ll_pct:>6.1f}% {psf_pct:>8.1f}% {pfl_pct:>7.1f}% {wp_pct:>11.1f}%")
        print()

    # Compare: daiin-like para-final vs -am-like within-para
    print("--- Expected function-word roles ---")
    print("  WITHIN-PARA LINE-CLOSERS (expected): high LLast%, low PSFirst%, low PFLast%")
    print("  PARA-FINAL MARKER (daiin): low LFirst%, high PFLast%, low PSFirst%")
    print("  PARA-START MARKERS (she-words): high PSFirst%")
    print()


def h142_cross_section_grammar(records):
    """
    H142: Positional grammar models hold across ALL folio sections.
    Check: -am within-para vs para-final; she-para-start; daiin para-final.
    Across sections: Herbal A, Pharma A, Herbal B, Astro/Cosmo B, Stars/Special B.
    """
    print("=== H142: Cross-Section Universality of Positional Grammar ===\n")

    # Classify records by section and dialect
    for rec in records:
        rec['section'] = classify_section(rec['folio'])

    # Compute edy rates per folio (already done via dialect)
    # Group by section + dialect
    section_dialect = defaultdict(list)
    for rec in records:
        key = (rec['section'], 'B' if rec['is_b'] else 'A')
        section_dialect[key].append(rec)

    print(f"--- Section + dialect breakdown ---")
    for key in sorted(section_dialect.keys()):
        print(f"  {key}: {len(section_dialect[key])} lines, {sum(len(r['words']) for r in section_dialect[key])} words")
    print()

    # For each group: compute -am rate (within-para vs para-final), she-para-start rate, daiin-para-final rate
    print(f"--- -am rate: within-para vs para-final line ---")
    print(f"{'Section':>15} {'Dialect':>7} {'N_lines':>8} {'AM_within%':>11} {'AM_parfinal%':>13} {'Ratio':>7}")
    for key in sorted(section_dialect.keys()):
        recs_sect = section_dialect[key]
        within_words, within_am = 0, 0
        final_words, final_am = 0, 0
        for rec in recs_sect:
            words = rec['words']
            is_pf = rec['is_para_final']
            is_ps = rec['is_para_start']
            for w in words:
                is_am = w.endswith('am') and len(w) > 2
                if is_pf:
                    final_words += 1
                    if is_am: final_am += 1
                else:
                    within_words += 1
                    if is_am: within_am += 1
        if within_words < 50: continue
        am_w = 100 * within_am / within_words if within_words else 0
        am_f = 100 * final_am / final_words if final_words else 0
        ratio = am_w / am_f if am_f > 0 else float('inf')
        print(f"  {key[0]:>13} {key[1]:>7} {len(recs_sect):>8} {am_w:>10.2f}% {am_f:>12.2f}% {ratio:>7.2f}×")
    print()

    print(f"--- she-prefix para-start enrichment by section ---")
    print(f"{'Section':>15} {'Dialect':>7} {'she-PSFirst%':>13} {'she-NonPS%':>11} {'Enrichment':>11}")
    for key in sorted(section_dialect.keys()):
        recs_sect = section_dialect[key]
        if key[1] != 'A': continue  # she- is A marker
        ps_lines = [r for r in recs_sect if r['is_para_start']]
        non_ps_lines = [r for r in recs_sect if not r['is_para_start']]
        def she_rate(lines):
            if not lines: return 0.0
            n_she = sum(1 for r in lines if r['words'] and r['words'][0].startswith('she') and len(r['words'][0]) > 3)
            return 100 * n_she / len(lines)
        r_ps = she_rate(ps_lines)
        r_non = she_rate(non_ps_lines)
        enrich = (r_ps / r_non) if r_non > 0 else float('inf')
        if len(recs_sect) < 30: continue
        print(f"  {key[0]:>13} {key[1]:>7} {r_ps:>12.1f}% {r_non:>10.1f}% {enrich:>10.2f}×")
    print()

    print(f"--- daiin para-final enrichment by section ---")
    print(f"{'Section':>15} {'Dialect':>7} {'daiin-PFLast%':>14} {'daiin-other-last%':>17} {'Enrichment':>11}")
    for key in sorted(section_dialect.keys()):
        recs_sect = section_dialect[key]
        if key[1] != 'A': continue  # daiin is A marker
        pf_lines = [r for r in recs_sect if r['is_para_final'] and r['words']]
        non_pf_lines = [r for r in recs_sect if not r['is_para_final'] and r['words']]
        def daiin_last_rate(lines):
            if not lines: return 0.0
            n = sum(1 for r in lines if r['words'][-1] == 'daiin')
            return 100 * n / len(lines)
        r_pf = daiin_last_rate(pf_lines)
        r_non = daiin_last_rate(non_pf_lines)
        enrich = (r_pf / r_non) if r_non > 0 else float('inf')
        if len(recs_sect) < 30: continue
        print(f"  {key[0]:>13} {key[1]:>7} {r_pf:>13.1f}% {r_non:>16.1f}% {enrich:>10.2f}×")
    print()

    # B dialect: o-onset para-start enrichment by section
    print(f"--- B o-onset para-start enrichment by section ---")
    print(f"{'Section':>15} {'Dialect':>7} {'o-PSFirst%':>11} {'o-NonPS%':>10} {'Enrichment':>11}")
    for key in sorted(section_dialect.keys()):
        recs_sect = section_dialect[key]
        if key[1] != 'B': continue
        ps_lines = [r for r in recs_sect if r['is_para_start']]
        non_ps_lines = [r for r in recs_sect if not r['is_para_start']]
        def o_onset_rate(lines):
            if not lines: return 0.0
            n = sum(1 for r in lines if r['words'] and get_onset(r['words'][0]) == 'o')
            return 100 * n / len(lines)
        r_ps = o_onset_rate(ps_lines)
        r_non = o_onset_rate(non_ps_lines)
        enrich = (r_ps / r_non) if r_non > 0 else float('inf')
        if len(recs_sect) < 30: continue
        print(f"  {key[0]:>13} {key[1]:>7} {r_ps:>10.1f}% {r_non:>9.1f}% {enrich:>10.2f}×")
    print()


def main():
    print("Loading data...")
    records = load_data()
    edy_map = compute_edy_rates(records)
    records = assign_dialects(records, edy_map)
    records = classify_para_boundary(records)
    a_recs = [r for r in records if r['is_a']]
    b_recs = [r for r in records if r['is_b']]
    print(f"Total body records: {len(records)}")
    print(f"A: {len(a_recs)}, B: {len(b_recs)}\n")

    h144_sh_onset_positional_profile(a_recs, b_recs)
    h145_am_core_function_words(a_recs, b_recs)
    h142_cross_section_grammar(records)

if __name__ == '__main__':
    main()
