#!/usr/bin/env python3
"""Regression tests for folio-level daiin sensitivity analysis."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.exp590_folio_cluster_sensitivity import analyze_text, bootstrap_difference

FIXTURE = """<f1r> <! $Q=A $L=A>
<f1r.1,@P0> daiin ol daiin
<f1r.2,@P0> ol daiin
<f2r> <! $Q=B $L=B>
<f2r.1,@P0> daiin qok
<f2r.2,@P0> qok daiin
<f3r> <! $Q=A>
<f3r.1,@P0> daiin ol
"""

def main():
    parsed = analyze_text(FIXTURE)
    assert parsed["parsed_lines"] == 5, parsed
    by_folio = {f["folio"]: f for f in parsed["folios"]}
    assert by_folio["f1r"]["currier"] == "A"
    assert by_folio["f2r"]["currier"] == "B"
    assert by_folio["f3r"]["currier"] == "unknown"
    assert by_folio["f1r"]["target_occurrences"] == 3
    assert by_folio["f1r"]["lines_containing_target"] == 2
    assert by_folio["f1r"]["target_bearing_lines_starting_target"] == 1
    assert by_folio["f1r"]["target_bearing_lines_ending_target"] == 2
    first = bootstrap_difference([1.0, 0.0], [0.0, 0.0], n=1000, seed=42)
    second = bootstrap_difference([1.0, 0.0], [0.0, 0.0], n=1000, seed=42)
    assert first == second
    assert first["difference_A_minus_B"] == 0.5
    assert first["percentile_95_ci"][0] <= first["difference_A_minus_B"] <= first["percentile_95_ci"][1]
    print("Folio-level daiin sensitivity regression tests passed.")

if __name__ == "__main__":
    main()
