#!/usr/bin/env python3
"""Read-only audit of archived EXP-170; never import/run the simulator.

Extract only named metric functions and the bounded VMS baseline block by AST.
No cipher imports, plaintext loading, encryption or historical writes execute.
"""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXP = Path('experiments/exp_170_naibbe_simulation')
CONDITIONS = ('italian_A', 'italian_B', 'latin_A', 'latin_B')
FUNCTIONS = {'get_onset', 'has_edy', 'parse_vms', 'compute_metrics',
             'summarize_distribution', 'inside_interval'}
# Exact table row labels, in report order. qo/sh self-succession are archived
# but not part of the historical 16-metric comparison.
ROWS = {
    'edy rate (B-dialect marker)': 'edy_rate',
    'l-onset rate (F131)': 'l_onset_rate',
    '-edy/-ol ratio (B-suffix paradigm)': 'edy_ol_ratio',
    '-am LL enrichment (F087)': 'am_ll_enrichment',
    'y-onset LF enrichment (F098)': 'y_lf_enrichment',
    'cth LF enrichment (~1.0 expected B)': 'cth_lf_enrichment',
    'sh LF enrichment (B opener)': 'sh_lf_enrichment',
    'qok LF enrichment (depleted in B)': 'qok_lf_enrichment',
    'd LL enrichment (line-closing)': 'd_ll_enrichment',
    'daiin→cth enrichment': 'daiin_cth_enrichment',
    'k@para-start enrichment (F101)': 'k_para_start_enrichment',
    'qok self-succession enrichment': 'qok_self_succ',
    'ok self-succession enrichment': 'ok_self_succ',
    'ch self-succession enrichment': 'ch_self_succ',
    'd self-succession enrichment': 'd_self_succ',
    'qok→ch enrichment': 'qok_ch_enrichment',
}


def historical_namespace(source):
    tree = ast.parse(source)
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in FUNCTIONS]
    if {n.name for n in selected} != FUNCTIONS:
        raise ValueError('Missing historical function')
    ns = dict(Counter=Counter, defaultdict=defaultdict, re=re, math=math)
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<EXP170 functions>', 'exec'), ns)
    return ns, tree


def baseline(ns, tree, corpus):
    # Bound by assignments, not line numbers; exclude all print statements.
    def assigns(node, name):
        return isinstance(node, ast.Assign) and any(
            isinstance(x, ast.Name) and x.id == name
            for target in node.targets for x in ast.walk(target))
    start = next(i for i, n in enumerate(tree.body) if assigns(n, 'folio_words'))
    end = next(i for i, n in enumerate(tree.body) if assigns(n, 'vms_a_metrics'))
    block = [n for n in tree.body[start:end+1] if not isinstance(n, ast.Expr)]
    ns['VMS_CORPUS'] = str(corpus)
    exec(compile(ast.Module(body=block, type_ignores=[]), '<EXP170 baseline>', 'exec'), ns)
    return ns['vms_b_metrics']


def quantile(values, probability):
    """Linear interpolation, rank (n-1)*p; explicitly distinct from legacy ranks."""
    values = sorted(values)
    rank = (len(values)-1)*probability
    lo = math.floor(rank)
    hi = math.ceil(rank)
    return values[lo] + (values[hi]-values[lo])*(rank-lo)


def summarize(values):
    values = [v for v in values if v is not None]
    if not values:
        return dict(n=0, mean=None, std=None, p5=None, p95=None)
    ordered = sorted(values)
    n = len(values)
    mean = math.fsum(values)/n
    return dict(n=n, mean=mean,
                std=math.sqrt(math.fsum((v-mean)**2 for v in values)/n),
                p5=ordered[int(.05*n)], p95=ordered[min(n-1, int(.95*n))])


def status(value, lower, upper):
    if value is None or lower is None:
        return 'N/A'
    return 'BELOW' if value < lower else 'ABOVE' if value > upper else 'INSIDE'


def report_tables(text):
    rows = {}
    counts = {}
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [x.strip().replace('**', '') for x in line.strip('|').split('|')]
        if cells[0] in ROWS:
            if len(cells) != 6:
                raise ValueError('Malformed metric row')
            parsed = []
            for cell in cells[2:]:
                m = re.fullmatch(r'([\d.]+)\s*\[([\d.]+),([\d.]+)\]\s*→\s*(INSIDE|ABOVE|BELOW)', cell)
                if not m:
                    raise ValueError(f'Malformed cell: {cell}')
                parsed.append(dict(mean=float(m[1]), p5=float(m[2]), p95=float(m[3]), status=m[4]))
            metric = ROWS[cells[0]]
            if metric in rows:
                raise ValueError(f'Duplicate historical metric row: {metric}')
            rows[metric] = dict(vms=float(cells[1]), conditions=dict(zip(CONDITIONS, parsed)))
        for key in ('INSIDE', 'ABOVE', 'BELOW'):
            if cells[0].startswith(key+' ('):
                if key in counts:
                    raise ValueError(f'Duplicate historical count row: {key}')
                if len(cells) != len(CONDITIONS) + 1:
                    raise ValueError(f'Malformed historical count row: {key}')
                counts[key] = dict(zip(CONDITIONS, map(int, cells[1:])))
    if set(rows) != set(ROWS.values()) or set(counts) != {'INSIDE', 'ABOVE', 'BELOW'}:
        raise ValueError('Incomplete historical tables')
    return rows, counts


def parse_archive(text):
    """Reject duplicate JSON keys at every depth before auditing archived vectors."""
    def unique_pairs(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f'Duplicate EXP-170 archive JSON key: {key}')
            obj[key] = value
        return obj
    return json.loads(text, object_pairs_hook=unique_pairs)


def validate_archive(archive, expected_keys):
    """Reject incomplete, ambiguous, or non-numeric archived metric vectors."""
    if (not isinstance(archive, dict) or set(archive) != set(CONDITIONS)
            or any(not isinstance(runs, list) or len(runs) != 100
                   for runs in archive.values())):
        raise ValueError('Expected four conditions of 100 archived runs')
    for runs in archive.values():
        for run in runs:
            if not isinstance(run, dict) or set(run) != expected_keys:
                raise ValueError('Metric schema mismatch')
            if any(v is not None and (type(v) not in (int, float) or not math.isfinite(v))
                   for v in run.values()):
                raise ValueError('Non-finite or non-numeric metric')


def audit(root=ROOT):
    source = (root/EXP/'script.py').read_text()
    ns, tree = historical_namespace(source)
    targets = baseline(ns, tree, root/'data/transcriptions/eva_zl3b.txt')
    archive = parse_archive((root/EXP/'data/simulation_results.json').read_text())
    validate_archive(archive, set(targets))
    tables, reported_counts = report_tables((root/EXP/'result.md').read_text())
    numeric_errors, status_errors, baseline_errors = [], [], []
    counts = {c: Counter() for c in CONDITIONS}
    metrics = {}
    for key in targets:
        cells = {}
        for condition, runs in archive.items():
            values = [r[key] for r in runs if r[key] is not None]
            stats = summarize(values)
            legacy = ns['summarize_distribution'](values)
            for name in ('mean', 'std', 'p5', 'p95'):
                if stats[name] is None:
                    if legacy[name] is not None:
                        raise ValueError(f'EXP-170 legacy summary mismatch: {key}/{condition}/{name}')
                elif legacy[name] is None or not math.isclose(
                        stats[name], legacy[name], rel_tol=1e-12, abs_tol=1e-12):
                    raise ValueError(f'EXP-170 legacy summary mismatch: {key}/{condition}/{name}')
            verdict = status(targets[key], stats['p5'], stats['p95'])
            if verdict != ns['inside_interval'](targets[key], legacy):
                raise ValueError(f'EXP-170 legacy status mismatch: {key}/{condition}')
            cells[condition] = dict(legacy=stats, status=verdict,
                min=min(values), max=max(values),
                linear_p5=quantile(values, .05), linear_p95=quantile(values, .95),
                linear_p025=quantile(values, .025), linear_p975=quantile(values, .975),
                status_central95=status(targets[key], quantile(values, .025), quantile(values, .975)),
                upper_tail_exceedances=sum(v >= targets[key] for v in values),
                upper_tail_plus_one=(1+sum(v >= targets[key] for v in values))/(len(values)+1))
            if key in tables:
                counts[condition][verdict] += 1
                saved = tables[key]['conditions'][condition]
                for name in ('mean', 'p5', 'p95'):
                    if f'{stats[name]:.3f}' != f'{saved[name]:.3f}':
                        numeric_errors.append(dict(metric=key, condition=condition, field=name,
                                                   reported=saved[name], recomputed=stats[name]))
                if saved['status'] != verdict:
                    status_errors.append(dict(metric=key, condition=condition, reported=saved['status'], recomputed=verdict))
        metrics[key] = dict(vms=targets[key], conditions=cells)
        if key in tables and f'{targets[key]:.3f}' != f"{tables[key]['vms']:.3f}":
            baseline_errors.append(dict(metric=key, reported=tables[key]['vms'], recomputed=targets[key]))
    paths = [EXP/'script.py', EXP/'result.md', EXP/'data/simulation_results.json', Path('data/transcriptions/eva_zl3b.txt')]
    return dict(schema_version=1, base_commit='b31492596c3e9a0c3f322c0ece62fa13a84d739d',
        sha256={str(p): hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
        scope='Archived vectors and historical metric/baseline replay only; no cipher execution',
        archive_runs={c:len(archive[c]) for c in CONDITIONS},
        baseline_lines=len(ns['b_word_lists']), baseline_paragraph_starts=len(ns['b_para_starts']),
        numeric_mismatches=numeric_errors, status_mismatches=status_errors,
        baseline_mismatches=baseline_errors, recomputed_counts={c:dict(counts[c]) for c in CONDITIONS},
        reported_counts=reported_counts, metrics=metrics)



def render_table(result):
    lines = ['# EXP-170 — tabla recalculada del archivo', '',
             'Media [P5, P95] y clasificación histórica; intervalo central nominal del 90 %,',
             'no IC del 95 %. Etiquetas de condiciones preservadas del JSON.', '',
             '| Métrica | VMS histórico | Italian-A | Italian-B | Latin-A* | Latin-B* |',
             '|---|---:|---|---|---|---|']
    for label, key in ROWS.items():
        metric = result['metrics'][key]
        cells = []
        for condition in CONDITIONS:
            cell = metric['conditions'][condition]
            stats = cell['legacy']
            cells.append(f"{stats['mean']:.3f} [{stats['p5']:.3f}, {stats['p95']:.3f}] {cell['status']}")
        lines.append(f"| {label} | {metric['vms']:.3f} | " + ' | '.join(cells) + ' |')
    lines.extend(['', '*Latin es una etiqueta histórica: el archivo de entrada auditado es inglés.', ''])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path, help='Compare with saved audit snapshot')
    parser.add_argument('--format', choices=('json', 'markdown'), default='json')
    args = parser.parse_args()
    result = audit()
    if args.check:
        if result != json.loads(args.check.read_text()):
            raise SystemExit('EXP-170 audit snapshot differs')
        print('EXP-170 archive audit matches snapshot')
    elif args.format == 'markdown':
        print(render_table(result), end='')
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))

if __name__ == '__main__':
    main()
