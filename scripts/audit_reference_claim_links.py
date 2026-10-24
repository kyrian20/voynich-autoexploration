"""Read-only adjudication of historical reference-reader claims; no simulations."""
import argparse
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = 'b31492596c3e9a0c3f322c0ece62fa13a84d739d'
CASE_IDS = {
    'EXP-267': ('experiments/exp_267_word_length_position/script.py', 105892, 'tokens'),
    'EXP-288': ('experiments/exp_288_stolfi_onset_decomp/script.py', 87754, 'onset_records'),
    'EXP-001': ('experiments/exp_001_word_initial_entropy/script.py', 991553, 'tokens'),
    'EXP-170': ('experiments/exp_170_naibbe_simulation/script.py', 97164, 'lines'),
}
RESULT_BLOBS = {
    'EXP-267': ('experiments/exp_267_word_length_position/result.md', '92c47d101d35543dabce569f877cbf98176db246'),
    'EXP-288': ('experiments/exp_288_stolfi_onset_decomp/result.md', 'c2c5711acf98c8779c179088275a4218699d3caf'),
}


def unique_index(rows, key_field, source):
    """Index audited records without silently overwriting duplicate identities."""
    if not isinstance(rows, list):
        raise ValueError(f'{source}: expected a list')
    indexed = {}
    for offset, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'{source}: row {offset} is not an object')
        key = row.get(key_field)
        if not isinstance(key, str) or not key:
            raise ValueError(f'{source}: missing {key_field} in row {offset}')
        if key in indexed:
            raise ValueError(f'{source}: duplicate {key_field}: {key}')
        indexed[key] = row
    return indexed


def git_blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def entropy(values):
    from collections import Counter
    counts = Counter(values)
    n = len(values)
    return -sum((v / n) * math.log2(v / n) for v in counts.values()) if n else 0.0


def parse_position_table(md):
    matches = re.findall(r'^\| ([AB]) \| (LF|MID|LL) \| (\d+) \| ([0-9.]+) \|', md, re.M)
    # A dict comprehension alone silently overwrites repeated table rows.
    # Require exactly one source row for every A/B x LF/MID/LL cell.
    expected = {(dialect, position) for dialect in 'AB'
                for position in ('LF', 'MID', 'LL')}
    keys = [(dialect, position) for dialect, position, _, _ in matches]
    if len(keys) != len(expected) or set(keys) != expected:
        raise ValueError('Expected exactly one row per dialect and position in EXP-267 position table')
    return {(dialect, position): float(mean)
            for dialect, position, _, mean in matches}


def audit(root=ROOT):
    readers = json.loads((root / 'research/maintenance/2026-10-22-remaining-readers/results.json').read_text(encoding='utf-8'))
    identities = json.loads((root / 'research/CORPUS_IDENTITY_REVIEW.json').read_text(encoding='utf-8'))
    excluded = unique_index(identities['excluded_from_new_language_baselines'], 'path', 'Corpus identity')
    if readers['source_commit'] != 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41':
        raise ValueError('Reader snapshot changed; re-adjudicate instead of reusing results')
    cases = unique_index(readers['cases'], 'experiment_path', 'Reader replay')
    if set(cases) != {v[0] for v in CASE_IDS.values()}:
        raise ValueError('Reader set changed')
    summary = {}
    for key, (script, count, unit) in CASE_IDS.items():
        case = cases[script]
        if (case['selected_units'], case['unit'], case['status']) != (count, unit, 'ISOLATED_READER_REPLAY_MATCHED'):
            raise ValueError(f'{key}: frozen selection changed')
        script_bytes = (root / script).read_bytes()
        corpus_bytes = (root / case['corpus']).read_bytes()
        if hashlib.sha256(script_bytes).hexdigest() != case['script_sha256']:
            raise ValueError(f'{key}: script SHA256 mismatch')
        if hashlib.sha256(corpus_bytes).hexdigest() != case['corpus_sha256']:
            raise ValueError(f'{key}: corpus SHA256 mismatch')
        identity = excluded[case['corpus']]
        if (identity['sha256'], identity['issue'], identity['adjudicated_language']) != (
            case['corpus_sha256'], case['identity_issue'], case['adjudicated_language']
        ):
            raise ValueError(f'{key}: identity manifest mismatch')
        summary[key] = {'source_script_sha256': case['script_sha256'],
                        'corpus_sha256': case['corpus_sha256'],
                        'unit': unit, 'selected_units': count,
                        'adjudicated_language': case['adjudicated_language']}
    md = {}
    for key, (path, blob) in RESULT_BLOBS.items():
        data = (root / path).read_bytes()
        if git_blob_sha(data) != blob:
            raise ValueError(f'{key}: historical report changed; review before adjudication')
        md[key] = data.decode('utf-8')
    table = parse_position_table(md['EXP-267'])
    if 'In both dialects MID has the shortest words' not in md['EXP-267']:
        raise ValueError('EXP-267 claim text changed')
    script267 = (root / CASE_IDS['EXP-267'][0]).read_text(encoding='utf-8')
    if not re.search(r"elif idx == 0:\s*lpos = 'LF'", script267):
        raise ValueError('EXP-267 index semantics changed')
    if 'Index 0 = line-final word (LF)' not in md['EXP-267']:
        raise ValueError('EXP-267 contradictory index text changed')
    if 'reduces uncertainty about the suffix by ~0.7 bits' not in md['EXP-288']:
        raise ValueError('EXP-288 entropy interpretation changed')
    if 'Latin Cicero Control' not in md['EXP-288'] or '### 5. Word Length Distributions vs. Latin' not in md['EXP-267']:
        raise ValueError('Historical control labels changed')
    toy = [('A', 'x'), ('A', 'x'), ('B', 'y'), ('B', 'y')]
    h_suffix = entropy([s for _, s in toy])
    within = [entropy([s for o, s in toy if o == group]) for group in ('A', 'B')]
    mi = h_suffix - sum(within) / len(within)
    span = max(within) - min(within)
    assert (h_suffix, mi, span) == (1.0, 1.0, 0.0)
    return {
        'schema_version': 1,
        'source_commit': BASE_COMMIT,
        'scope': 'Read-only claim-to-output adjudication; historical experiment metrics not rerun',
        'readers': summary,
        'checks': {
            'EXP-267_B_MID_shortest': {
                'archived_B_MID_mean': table['B', 'MID'],
                'archived_B_LL_mean': table['B', 'LL'],
                'MID_is_shortest': table['B', 'MID'] < table['B', 'LL'],
                'status': 'CONTRADICTED_BY_ARCHIVED_TABLE',
            },
            'EXP-267_index_0': {
                'script_label': 'LF=line-first',
                'archived_report_label': 'LF=line-final (in word-index heading)',
                'status': 'INTERNAL_LABEL_CONTRADICTION',
            },
            'EXP-267_Latin_comparison': 'INVALID_FOR_MONOLINGUAL_LATIN_CLAIM',
            'EXP-288_Latin_control': 'INVALID_FOR_MONOLINGUAL_LATIN_CLAIM',
            'EXP-288_entropy_range_as_mutual_information': {
                'toy_within_onset_entropy_range_bits': span,
                'toy_mutual_information_bits': mi,
                'status': 'NOT_A_VALID_MI_ESTIMATOR',
            },
            'EXP-001_Latin_Vulgate': 'ALREADY_FLAGGED_WRONG_LANGUAGE',
            'EXP-170': 'EXCLUDED_FROM_THIS_ADJUDICATION_OPEN_PR_2',
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit()
    if args.check:
        expected = json.loads(args.check.read_text(encoding='utf-8'))
        if result != expected:
            raise SystemExit('Snapshot mismatch')
        print('PASS: reference claim adjudication snapshot matches')
    elif args.out:
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    main()
