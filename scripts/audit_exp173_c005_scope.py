"""Read-only adjudication of the statistical scope of EXP-173/C005.

Does not execute EXP-173, import scipy, or parse manuscript text.
"""
import argparse
import ast
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'experiments/exp_173_multiple_testing/script.py'
REPORT = 'experiments/exp_173_multiple_testing/result.md'
CLAIMS = 'state/committed_claims.md'
EXPECTED_BLOBS = {
    SCRIPT: '3fb1eeb92c301d3caf841499571f5e1a8b590bcc',
    REPORT: '6c192f887af65e1153435fab1561c52fedb0f608',
    CLAIMS: '02cb4c1780aadf4c3d94fd907621ec1416b49bed',
}
REQUIRED_SCRIPT = (
    "rate = sum(1 for w in wds if 'edy' in w or 'eedy' in w) / len(wds)",
    "folio_dialect[fn] = 'B' if rate >= 0.05 else 'A'",
    "b_lines = [(fn, wds) for fn, wds in raw_lines if folio_dialect.get(fn) == 'B']",
    "am_ll_b = sum(1 for w in b_ll if w.endswith('am'))",
    "am_base_b = sum(1 for w in b_words if w.endswith('am')) / b_n",
    'p_am_ll_b = binom_p(am_ll_b, n_ll_b, am_base_b)',
)


def git_blob_sha1(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()


def binomial_upper_tail(n, k, p):
    """Exact binomial tail, suitable for this small illustrative counterexample."""
    if not (0 <= k <= n and 0 <= p <= 1):
        raise ValueError('Invalid binomial parameters')
    return math.fsum(math.comb(n, i) * p**i * (1 - p)**(n-i) for i in range(k, n+1))


def cluster_counterexample(folios=20, lines_per_folio=10, positive_folios=2, p0=0.05):
    """All line outcomes in a folio are identical; toy data, NOT VMS."""
    if not (0 <= positive_folios <= folios and folios > 0 and lines_per_folio > 0):
        raise ValueError('Invalid cluster design')
    n_lines = folios * lines_per_folio
    k_lines = positive_folios * lines_per_folio
    return {
        'type': 'synthetic_perfect_within_folio_correlation',
        'folios': folios, 'lines_per_folio': lines_per_folio,
        'positive_folios': positive_folios, 'null_probability': p0,
        'line_level_n': n_lines, 'line_level_k': k_lines,
        'line_binomial_p': round(binomial_upper_tail(n_lines, k_lines, p0), 12),
        'folio_binomial_p': round(binomial_upper_tail(folios, positive_folios, p0), 12),
    }


def check_contract(script, report, claims):
    ast.parse(script)  # syntax only; never imports/executes the historical experiment
    for snippet in REQUIRED_SCRIPT:
        if snippet not in script:
            raise ValueError('EXP-173 code no longer matches audited statistical contract: ' + snippet)
    for marker in ('6.811', '6.27e-161', 'Bonferroni m=175'):
        if marker not in report:
            raise ValueError('EXP-173 report claim missing: ' + marker)
    for marker in ('## C005:', '6.811', '6.27 × 10^-161', '**Supporting experiments**: exp_173'):
        if marker not in claims:
            raise ValueError('C005 public commitment missing: ' + marker)


def result_snapshot():
    return {
        'schema_version': 1,
        'scope': 'Static C005/EXP-173 claim-method adjudication; no VMS data or p-value recomputation',
        'historical_git_blob_sha1': EXPECTED_BLOBS,
        'historical_claim': {'enrichment': 6.811, 'reported_p': '6.27e-161',
                             'status': 'REPORTED_NOT_REPRODUCED_HERE'},
        'method_flags': {
            'currier_class_from_metadata_L': False,
            'currier_class_from_edy_threshold': True,
            'line_binomial_uses_within_B_base_rate': True,
            'folio_cluster_robust_p_calculated': False,
            'conclusion': 'Significance scope unresolved; enrichment magnitude not refuted',
        },
        'synthetic_control': cluster_counterexample(),
    }


def audit(root=ROOT):
    raw = {path: (root / path).read_bytes() for path in EXPECTED_BLOBS}
    for path, expected in EXPECTED_BLOBS.items():
        if git_blob_sha1(raw[path]) != expected:
            raise ValueError('Historical file changed: ' + path)
    check_contract(*(raw[p].decode('utf-8') for p in (SCRIPT, REPORT, CLAIMS)))
    return result_snapshot()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.check and args.out:
        parser.error('--check and --out are mutually exclusive')
    result = audit()
    if args.check:
        expected = json.loads(args.check.read_text(encoding='utf-8'))
        if result != expected:
            raise SystemExit('FAIL: EXP-173/C005 snapshot mismatch')
        print('PASS: EXP-173/C005 historical source contract and snapshot')
    elif args.out:
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
