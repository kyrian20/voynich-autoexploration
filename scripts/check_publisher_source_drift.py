#!/usr/bin/env python3
"""Refuse stale-result publication when concurrent Git changes affect inputs.

Only *new* files with the four scheduled generators' exact output names may
appear on master during a publisher rebase. Existing results, corrections,
archived evidence, scripts and corpus files are not exempt.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from pathlib import Path


_GENERATED_OUTPUT = re.compile(
    r"research/experiments/(?:"
    r"\d{4}-\d{2}-\d{2}-exp(?:590|593)-corrected-L-metadata\.(?:json|md)"
    r"|exp_622_ch_sh_specificity_interaction/(?:results\.json|result\.md)"
    r"|exp_623_it2a_ch_sh_specificity_replication/(?:results\.json|result\.md)"
    r")\Z"
)



# These are the four scheduled publisher output contracts, not an assertion
# that the reported statistics are scientifically valid. The frozen corpus
# hashes are independently pinned; a syntactically valid but unrelated JSON
# must not be exempt from the source-drift guard.
_PUBLISHER_SOURCE_SHA256 = {
    "data/transcriptions/eva_zl3b.txt":
        "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
    "data/transcriptions/eva_it2a.txt":
        "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
}


def _validate_generated_schema(doc: dict, path: str) -> str | None:
    """Check the minimum known publisher schema, without claiming reproduction."""
    if "exp_622_" in path:
        exp, source = 622, "data/transcriptions/eva_zl3b.txt"
    elif "exp_623_" in path:
        exp, source = 623, "data/transcriptions/eva_it2a.txt"
    elif "-exp590-" in path:
        exp, source = "EXP-590", "data/transcriptions/eva_zl3b.txt"
    elif "-exp593-" in path:
        exp, source = "EXP-593", "data/transcriptions/eva_zl3b.txt"
    else:
        return "unknown scheduled output schema"

    if type(doc.get("experiment")) is not type(exp) or doc.get("experiment") != exp:
        return "wrong or missing experiment identity"
    if doc.get("source") != source or doc.get("source_sha256") != _PUBLISHER_SOURCE_SHA256[source]:
        return "wrong or missing pinned corpus provenance"
    if not isinstance(doc.get("limitations"), list) or not doc["limitations"] or not all(
            isinstance(x, str) and x.strip() for x in doc["limitations"]):
        return "missing or malformed limitations"

    def count(obj, key, positive=False):
        value = obj.get(key)
        return type(value) is int and value >= (1 if positive else 0)

    def probability(obj, key):
        value = obj.get(key)
        return type(value) in (int, float) and math.isfinite(value) and 0 <= value <= 1

    if exp == "EXP-590":
        metrics, perm = doc.get("metrics"), doc.get("permutation_test")
        if not isinstance(metrics, dict) or not isinstance(perm, dict):
            return "missing EXP-590 metrics/permutation_test"
        if not all(count(metrics, key, positive=(key in ("tokens", "lines")))
                   for key in ("tokens", "lines", "target_occurrences",
                               "line_initial_occurrences", "line_final_occurrences")):
            return "invalid EXP-590 count fields"
        # EXP-590's Currier classes form an exhaustive partition of the
        # published aggregate. Type-valid but contradictory totals must not
        # receive the concurrent-output exemption.
        if (metrics["target_occurrences"] > metrics["tokens"]
                or metrics["line_initial_occurrences"] >
                    min(metrics["target_occurrences"], metrics["lines"])
                or metrics["line_final_occurrences"] >
                    min(metrics["target_occurrences"], metrics["lines"])):
            return "inconsistent EXP-590 aggregate counts"
        currier = metrics.get("currier")
        groups = ("A", "B", "unknown")
        fields = ("target_occurrences", "line_initial_lines",
                  "line_final_lines", "lines")
        if (not isinstance(currier, dict) or set(currier) != set(groups)
                or any(not isinstance(currier[group], dict)
                       or not all(count(currier[group], field) for field in fields)
                       for group in groups)):
            return "invalid EXP-590 Currier partition"
        for group in groups:
            row = currier[group]
            if (row["target_occurrences"] > metrics["target_occurrences"]
                    or row["line_initial_lines"] >
                        min(row["target_occurrences"], row["lines"])
                    or row["line_final_lines"] >
                        min(row["target_occurrences"], row["lines"])):
                return "inconsistent EXP-590 Currier subgroup counts"
        for subtotal, aggregate in (
            ("target_occurrences", "target_occurrences"),
            ("line_initial_lines", "line_initial_occurrences"),
            ("line_final_lines", "line_final_occurrences"),
            ("lines", "lines"),
        ):
            if sum(currier[group][subtotal] for group in groups) != metrics[aggregate]:
                return "inconsistent EXP-590 Currier partition totals"
        if (not count(perm, "permutations", positive=True)
                or not count(perm, "seed")
                or not probability(perm, "empirical_one_sided_p")):
            return "invalid EXP-590 permutation fields"
    elif exp == "EXP-593":
        variants, observed, tests = doc.get("variants"), doc.get("observed"), doc.get("tests")
        if (not isinstance(variants, list) or not variants
                or not all(isinstance(x, str) and x for x in variants)
                or len(set(variants)) != len(variants)
                or not isinstance(observed, dict) or set(observed) != set(variants)
                or not isinstance(tests, dict) or set(tests) != set(variants)):
            return "invalid EXP-593 variant/test coverage"
        if not all(count(doc, key, positive=(key != "seed"))
                   for key in ("lines", "tokens", "permutations", "seed")):
            return "invalid EXP-593 count fields"
        for variant in variants:
            if not isinstance(observed[variant], dict) or not isinstance(tests[variant], dict):
                return "invalid EXP-593 per-variant record"
            if not all(count(observed[variant], key)
                       for key in ("occurrences", "line_initial", "line_final")):
                return "invalid EXP-593 observed counts"
            # The publisher may only exempt coherent generated results from
            # source-drift rejection. This mirrors the archive's count and
            # Currier partition guards; it does not recompute any permutation.
            row = observed[variant]
            if (row["occurrences"] > doc["tokens"]
                    or row["line_initial"] > min(row["occurrences"], doc["lines"])
                    or row["line_final"] > min(row["occurrences"], doc["lines"])):
                return "inconsistent EXP-593 observed counts"
            classes = row.get("by_currier")
            groups = ("A", "B", "unknown")
            fields = ("occurrences", "line_initial", "line_final")
            if (not isinstance(classes, dict) or set(classes) != set(groups)
                    or any(not isinstance(classes[group], dict)
                           or not all(count(classes[group], field) for field in fields)
                           for group in groups)):
                return "invalid EXP-593 Currier partition"
            for group in groups:
                values = classes[group]
                if (values["occurrences"] > row["occurrences"]
                        or values["line_initial"] > min(values["occurrences"], doc["lines"])
                        or values["line_final"] > min(values["occurrences"], doc["lines"])):
                    return "inconsistent EXP-593 Currier subgroup counts"
            if any(sum(classes[group][field] for group in groups) != row[field]
                   for field in fields):
                return "inconsistent EXP-593 Currier partition totals"
            fraction = row.get("initial_fraction")
            expected_fraction = (row["line_initial"] / row["occurrences"]
                                 if row["occurrences"] else None)
            if (expected_fraction is None and fraction is not None) or (
                    expected_fraction is not None
                    and (type(fraction) not in (int, float)
                         or not math.isfinite(fraction)
                         or not math.isclose(fraction, expected_fraction,
                                             rel_tol=0, abs_tol=1e-12))):
                return "inconsistent EXP-593 initial fraction"
            if not all(probability(tests[variant], key)
                       for key in ("empirical_p", "max_stat_adjusted_p")):
                return "invalid EXP-593 p-value"
    else:
        if (not all(count(doc, key, positive=True)
                    for key in ("occurrences_with_two_neighbors", "matched_strata",
                                "folios_in_matched_strata", "permutation_replicates"))
                or not count(doc, "permutation_exceedances")
                or doc["permutation_exceedances"] > doc["permutation_replicates"]
                or not probability(doc, "two_sided_permutation_p")
                or type(doc.get("interaction_next_minus_prev")) not in (int, float)
                or not math.isfinite(doc["interaction_next_minus_prev"])
                or not isinstance(doc.get("interpretation"), str)
                or not doc["interpretation"].strip()):
            return "invalid EXP-622/623 result fields"
    return None




def _validate_new_generated_blob(repo: Path, object_id: bytes, path: str) -> str | None:
    """Basic integrity gate, NOT scientific validation of a published result.

    The Git tree mode check alone accepts an empty, corrupt or ambiguous blob
    with an allowlisted filename. Read the *candidate commit's* blob rather
    than the working tree, which can differ during a concurrent publication.
    """
    result = subprocess.run(
        ["git", "cat-file", "blob", object_id.decode("ascii")],
        cwd=repo, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"Cannot inspect generated output Git blob: {path}: "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    if not result.stdout.strip():
        return "empty or whitespace-only output"
    try:
        text = result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return "non-UTF-8 output"
    if path.endswith(".json"):
        def unique_pairs(pairs):
            value = {}
            for key, item in pairs:
                if key in value:
                    raise ValueError(f"duplicate JSON key: {key}")
                value[key] = item
            return value

        def invalid_constant(value):
            raise ValueError(f"non-finite JSON constant: {value}")

        try:
            parsed = json.loads(
                text, object_pairs_hook=unique_pairs,
                parse_constant=invalid_constant,
            )
        except ValueError as exc:
            return f"invalid or ambiguous JSON ({exc})"
        if not isinstance(parsed, dict):
            return "JSON root must be an object"

        def finite_numbers(value):
            if type(value) is float:
                return math.isfinite(value)
            if isinstance(value, dict):
                return all(finite_numbers(item) for item in value.values())
            if isinstance(value, list):
                return all(finite_numbers(item) for item in value)
            return True

        # json.loads also accepts 1e999 as float('inf'), independently
        # of parse_constant, so reject numeric overflow at any depth.
        if not finite_numbers(parsed):
            return "non-finite JSON number"
        schema_problem = _validate_generated_schema(parsed, path)
        if schema_problem:
            return schema_problem
    return None


def changed_source_paths(repo: Path, baseline: str, candidate: str) -> list[str]:
    """List changes that cannot be safely rebased over generated results.

    Git's NUL-delimited status format avoids quoting/whitespace ambiguities.
    --no-renames makes moves visible as a deletion plus an addition.
    """
    if not baseline or not candidate:
        raise ValueError("Both baseline and candidate commits are required")
    # A tree diff cannot establish commit ancestry. Two divergent commits
    # can contain identical files and thus produce an empty diff. A rewritten
    # master must fail closed even in that case. The workflow fetches full
    # history before calling this guard.
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline, candidate],
        cwd=repo, capture_output=True, check=False,
    )
    if ancestry.returncode != 0:
        if ancestry.returncode == 1:
            raise RuntimeError(
                "Cannot verify source drift: candidate is not a descendant "
                "of the generating checkout commit"
            )
        raise RuntimeError(
            f"Cannot verify source drift (merge-base exit {ancestry.returncode}): "
            f"{ancestry.stderr.decode('utf-8', errors='replace').strip()}"
        )
    cmd = ["git", "diff", "--name-status", "-z", "--no-renames",
           baseline, candidate, "--", "."]
    result = subprocess.run(cmd, cwd=repo, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Cannot verify source drift (git exit {result.returncode}): "
            f"{result.stderr.decode('utf-8', errors='replace').strip()}"
        )
    fields = result.stdout.split(b"\0")
    if fields[-1:] != [b""] or (len(fields) - 1) % 2:
        raise RuntimeError("Cannot parse NUL-delimited Git change statuses")
    changed = []
    for index in range(0, len(fields) - 1, 2):
        status = fields[index].decode("ascii", errors="replace")
        path = fields[index + 1].decode("utf-8", errors="surrogateescape")
        if status == "A" and _GENERATED_OUTPUT.fullmatch(path):
            # A pathname allowlist alone also accepts Git symlinks (mode 120000)
            # and executable/non-regular entries. Only ordinary text blobs may
            # be exempted from source-drift detection.
            entry = subprocess.run(
                ["git", "ls-tree", "-z", candidate, "--", path],
                cwd=repo, capture_output=True, check=False,
            )
            if entry.returncode != 0:
                raise RuntimeError(
                    f"Cannot verify generated output Git mode: {path}: "
                    f"{entry.stderr.decode('utf-8', errors='replace').strip()}"
                )
            records = entry.stdout.split(b"\0")
            try:
                if len(records) != 2 or records[-1] != b"":
                    raise ValueError("expected exactly one Git tree entry")
                metadata, actual_path = records[0].split(b"\t", 1)
                mode, kind, _object_id = metadata.split()
                if actual_path != path.encode("utf-8", errors="surrogateescape"):
                    raise ValueError("tree path differs")
            except ValueError as exc:
                raise RuntimeError(
                    f"Cannot verify generated output Git tree entry: {path}"
                ) from exc
            if mode != b"100644" or kind != b"blob":
                changed.append(f"A unsafe Git mode/type ({mode.decode('ascii', errors='replace')}) {path}")
                continue
            problem = _validate_new_generated_blob(repo, _object_id, path)
            if problem:
                changed.append(f"A invalid generated output ({problem}) {path}")
            continue
        changed.append(f"{status} {path}")
    return changed


def assert_no_source_drift(repo: Path, baseline: str, candidate: str) -> None:
    changed = changed_source_paths(repo, baseline, candidate)
    if changed:
        raise RuntimeError(
            "Source or existing evidence changed since workflow checkout; "
            "refusing to rebase stale generated results:\n" + "\n".join(changed)
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="origin/master")
    args = parser.parse_args()
    assert_no_source_drift(args.repo, args.base, args.head)
    print(f"Publisher source/evidence tree unchanged: {args.base} -> {args.head} "
          "(only new, known scheduled output files exempt)")


if __name__ == "__main__":
    main()
