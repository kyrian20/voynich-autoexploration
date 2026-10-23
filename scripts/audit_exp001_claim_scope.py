"""Read-only scope audit of EXP-001; no corpus replacement or simulation replay."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = '465b2cf05ce1d5715f93894e16dd5c9b5d9753af'
SCRIPT = 'experiments/exp_001_word_initial_entropy/script.py'
REPORT = 'experiments/exp_001_word_initial_entropy/result.md'
CORPUS = 'data/reference_corpora/latin/vulgate.txt'
READERS = 'research/maintenance/2026-10-22-remaining-readers/results.json'
REPORT_GIT_BLOB = '2feb8c7dbb268f46d6a7995ddd2c15a76f6bd907'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def entropy(items):
    counts = Counter(items)
    n = len(items)
    return -sum((v / n) * math.log2(v / n) for v in counts.values()) if n else 0.0


def historical_h2(words):
    chars = ''.join(words)
    return entropy(list(zip(chars, chars[1:]))) - entropy(chars)


def synthetic_control(repeats=128, suffix_length=8):
    """Deterministic non-semantic slot generator; not a model of Voynich."""
    words = [prefix + 'z' * suffix_length for _ in range(repeats) for prefix in 'abcd']
    h_init = entropy([w[0] for w in words])
    h2 = historical_h2(words)
    return {
        'generator': 'fixed four-symbol onset cycle plus repeated z suffix',
        'repeats': repeats,
        'suffix_length': suffix_length,
        'words': len(words),
        'input_sha256': sha256(('\n'.join(words) + '\n').encode()),
        'h_initial_bits': round(h_init, 9),
        'historical_h2_bits': round(h2, 9),
        'gap_bits': round(h_init - h2, 9),
    }


def audit(root=ROOT):
    readers = json.loads((root / READERS).read_text(encoding='utf-8'))
    if readers['source_commit'] != 'aa9ec5399e7a5cdf8d1b2890fa657f1358825b41':
        raise ValueError('Reader provenance changed')
    matching = [c for c in readers['cases'] if c['experiment_path'] == SCRIPT]
    if len(matching) != 1:
        raise ValueError('Expected exactly one EXP-001 reader')
    case = matching[0]
    if (case['corpus'], case['selected_units'], case['unit'], case['adjudicated_language'], case['status']) != (
        CORPUS, 991553, 'tokens', 'English', 'ISOLATED_READER_REPLAY_MATCHED'
    ):
        raise ValueError('EXP-001 reader selection changed')
    if sha256((root / SCRIPT).read_bytes()) != case['script_sha256']:
        raise ValueError('Historical script changed')
    if sha256((root / CORPUS).read_bytes()) != case['corpus_sha256']:
        raise ValueError('Historical corpus changed')
    report_bytes = (root / REPORT).read_bytes()
    if git_blob(report_bytes) != REPORT_GIT_BLOB:
        raise ValueError('Historical report changed')
    report = report_bytes.decode('utf-8')
    for phrase in ('The pure glossographic model is contradicted.',
                   'Latin Vulgate', 'Voynich all', '3.137', '2.341',
                   'the Gutenberg file may be an English Bible'):
        if phrase not in report:
            raise ValueError('Expected archived claim or table missing: ' + phrase)
    return {
        'schema_version': 1,
        'source_commit': SOURCE_COMMIT,
        'scope': 'Static claim-to-reader adjudication plus synthetic mathematical counterexample; no historical metric replay',
        'historical_script_sha256': case['script_sha256'],
        'historical_report_git_blob_sha1': REPORT_GIT_BLOB,
        'reference_corpus_sha256': case['corpus_sha256'],
        'reference_selected_units': case['selected_units'],
        'reference_unit': case['unit'],
        'reference_language': case['adjudicated_language'],
        'archived_vms_h_initial_bits': 3.137,
        'archived_vms_h2_bits': 2.341,
        'archived_latin_label_h_initial_bits': 3.978,
        'claim_status': {
            'latin_vulgate_as_monolingual_latin': 'INVALID_FOR_CLAIM',
            'h_initial_minus_h2_proves_lexicon_or_excludes_nonsemantic_generators': 'NOT_ENTAILED_BY_STATISTIC',
            'voynich_archived_values': 'NOT_REPRODUCED_IN_THIS_AUDIT',
        },
        'synthetic_control': synthetic_control(),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    result = audit()
    if args.check:
        if result != json.loads(args.check.read_text(encoding='utf-8')):
            raise SystemExit('FAIL: EXP-001 claim scope snapshot differs')
        print('PASS: EXP-001 claim scope snapshot matches')
    elif args.out:
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
