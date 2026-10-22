"""
exp_178: Naibbe A-Dialect Coverage Analysis

Task 5 of Phase 3 methodological consolidation.

Loads existing exp_170 simulation results (400 Naibbe runs across 4 conditions)
and compares them against VMS A-dialect metric targets. Documents the A-dialect
gap in Naibbe null simulation coverage.

DESIGN NOTE: Naibbe is a B-dialect cipher — it was calibrated against Currier B
vocabulary statistics (edy suffix, qok prefix, l-onset bias). Comparing Naibbe
output against A-dialect metrics is inherently a mismatch: Naibbe targets a
different subdialect. This comparison is therefore exploratory, not definitive.
The correct null simulation for A-dialect would require a cipher calibrated to
Currier A. No such cipher exists in the published literature.

Despite this limitation, the comparison is informative: position-blind mechanisms
fail on positional grammar regardless of vocabulary calibration. If Naibbe fails
on A-dialect positional metrics (as it fails on B-dialect), the failure is
attributable to the position-blind mechanism, not just the vocabulary mismatch.
"""
from pathlib import Path as _RepositoryPath

import os, sys, json, math, numpy as np

REPO_DIR = os.path.expanduser(str(_RepositoryPath(__file__).resolve().parents[2]))
EXP170_DATA = os.path.join(REPO_DIR, 'experiments/exp_170_naibbe_simulation/data/simulation_results.json')
OUT_DIR = os.path.join(REPO_DIR, 'experiments/exp_178_naibbe_a_dialect/data')
os.makedirs(OUT_DIR, exist_ok=True)

# ── VMS A-dialect targets (from exp_173 candidate findings) ──────────────────
VMS_A = {
    'am_ll_enrichment':     3.562,   # F4: -am LL enrichment A-dialect
    'y_lf_enrichment':      2.459,   # F1: y-onset LF enrichment A-dialect
    'd_ll_enrichment':      1.667,   # F5: d LL enrichment A-dialect
    'cth_lf_enrichment':    0.159,   # F2: cth LF depletion A-dialect (strong depletion)
    'ok_self_succ':         1.930,   # F11: ok self-succession A-dialect
    'ch_self_succ':         1.427,   # F12: ch self-succession A-dialect
    'qok_self_succ':        1.623,   # F13: qok self-succession A-dialect
    'daiin_cth_enrichment': 2.839,   # F7: daiin→cth enrichment A-dialect
    'edy_rate':             0.043,   # A-dialect edy rate (low — edy is B marker)
    'edy_ol_ratio':         0.650,   # A-dialect edy/ol ratio (A favors -ol)
}

# A-dialect label for display
METRIC_LABELS = {
    'am_ll_enrichment':     '-am LL enrichment',
    'y_lf_enrichment':      'y-onset LF enrichment',
    'd_ll_enrichment':      'd-onset LL enrichment',
    'cth_lf_enrichment':    'cth LF enrichment (depleted in A)',
    'ok_self_succ':         'ok self-succession',
    'ch_self_succ':         'ch self-succession',
    'qok_self_succ':        'qok self-succession',
    'daiin_cth_enrichment': 'daiin→cth enrichment',
    'edy_rate':             'edy rate',
    'edy_ol_ratio':         'edy/ol ratio',
}

def ci95(vals):
    """Return (mean, lo, hi) 95% CI from list of floats."""
    arr = [v for v in vals if v is not None and not math.isnan(v)]
    if not arr:
        return 0, 0, 0
    arr.sort()
    n = len(arr)
    lo = arr[int(0.025 * n)]
    hi = arr[int(0.975 * n)]
    return sum(arr)/n, lo, hi

def status(vms_val, lo, hi):
    """INSIDE/ABOVE/BELOW from the VMS perspective."""
    if vms_val > hi:
        return 'ABOVE'   # VMS value above cipher CI → cipher underproduces
    elif vms_val < lo:
        return 'BELOW'   # VMS value below cipher CI → cipher overproduces
    else:
        return 'inside'  # VMS within cipher CI → cipher reproduces

print("Loading exp_170 simulation results...")
with open(EXP170_DATA) as f:
    data = json.load(f)

conditions = ['italian_A', 'italian_B', 'latin_A', 'latin_B']

print("\n" + "="*90)
print("EXP_178: NAIBBE vs VMS A-DIALECT METRICS")
print("="*90)
print("\nCAVEAT: Naibbe is calibrated for B-dialect. This comparison is exploratory.")
print("Vocabulary metrics (edy_rate, edy_ol_ratio) are expected to fail since")
print("Naibbe targets B vocabulary. Positional metrics are the key discriminators.\n")

# Collect results for JSON output
results = {}

for metric, vms_val in VMS_A.items():
    label = METRIC_LABELS[metric]
    print(f"\n{'─'*90}")
    print(f"Metric: {label}  |  VMS A-dialect: {vms_val:.3f}")
    print(f"{'Condition':>15} {'Mean':>8} {'95% CI':>20} {'Status':>8}")
    results[metric] = {'vms_a': vms_val, 'conditions': {}}
    for cond in conditions:
        if cond not in data:
            continue
        vals = [data[cond][i].get(metric) for i in range(len(data[cond]))
                if isinstance(data[cond], list)]
        # data[cond] may be a dict of sim_index -> metrics
        if isinstance(data[cond], dict):
            vals = [v.get(metric) for v in data[cond].values() if isinstance(v, dict)]
        vals = [v for v in vals if v is not None]
        if not vals:
            print(f"  {cond:>15}: no data")
            continue
        mean, lo, hi = ci95(vals)
        st = status(vms_val, lo, hi)
        print(f"  {cond:>15}: {mean:>7.3f}  [{lo:.3f}, {hi:.3f}]  {st:>8}")
        results[metric]['conditions'][cond] = {
            'mean': round(mean, 4),
            'ci_lo': round(lo, 4),
            'ci_hi': round(hi, 4),
            'status': st
        }

# Save results
with open(os.path.join(OUT_DIR, 'a_dialect_comparison.json'), 'w') as f:
    json.dump(results, f, indent=2)

# ── Summary: INSIDE/ABOVE/BELOW counts ──────────────────────────────────────
print("\n\n" + "="*90)
print("SUMMARY: INSIDE/ABOVE/BELOW COUNTS (A-dialect targets)")
print("="*90)

metrics_list = list(VMS_A.keys())
for cond in conditions:
    counts = {'ABOVE': 0, 'BELOW': 0, 'inside': 0}
    for metric in metrics_list:
        if metric in results and cond in results[metric]['conditions']:
            st = results[metric]['conditions'][cond]['status']
            counts[st] += 1
    print(f"  {cond:>15}: ABOVE={counts['ABOVE']:>2}, BELOW={counts['BELOW']:>2}, inside={counts['inside']:>2}  "
          f"(of {len(metrics_list)} metrics)")

# ── Positional metrics only (excluding vocabulary metrics) ──────────────────
POSITIONAL_METRICS = ['am_ll_enrichment', 'y_lf_enrichment', 'd_ll_enrichment',
                      'cth_lf_enrichment', 'ok_self_succ', 'ch_self_succ',
                      'qok_self_succ', 'daiin_cth_enrichment']

print("\n--- Positional/Sequential metrics only (excluding vocabulary metrics) ---")
for cond in conditions:
    counts = {'ABOVE': 0, 'BELOW': 0, 'inside': 0}
    for metric in POSITIONAL_METRICS:
        if metric in results and cond in results[metric]['conditions']:
            st = results[metric]['conditions'][cond]['status']
            counts[st] += 1
    n = len(POSITIONAL_METRICS)
    print(f"  {cond:>15}: ABOVE={counts['ABOVE']:>2}, BELOW={counts['BELOW']:>2}, inside={counts['inside']:>2}  "
          f"(of {n} positional/sequential metrics)")

print("\nDone. Results saved to data/a_dialect_comparison.json")
