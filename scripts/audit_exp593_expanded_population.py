#!/usr/bin/env python3
"""Exploratory max-T sensitivity for EXP-593 on the broader EXP-590 page scope."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
OUT = ROOT / "research/maintenance/2026-11-04-exp593-expanded-population-sensitivity.json"
PAGE_LINE = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),[^>]*>\s*(.*)$")
TOKEN = re.compile(r"[a-z]+")
VARIANTS = ("daiin", "dain", "daiiin")
N_PERM = 5000
SEED = 0x59320261104

class XorShift32:
    def __init__(self, seed: int) -> None:
        self.state = seed & 0xFFFFFFFF
    def random(self) -> float:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= x >> 17
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state / 2**32

def parse(raw: bytes) -> list[list[str]]:
    lines = []
    for row in raw.decode("utf-8-sig").splitlines():
        match = PAGE_LINE.match(row)
        if not match:
            continue
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]", " ", match.group(3))
        tokens = TOKEN.findall(body.lower())
        if tokens:
            lines.append(tokens)
    return lines

# Archived descriptive fields are immutable too. The historical JSON predates
# the later null_model narrative; do not manufacture that field in the archive.
ARCHIVE_METADATA = {
    "status": "EXPLORATORY",
    "parent_analysis": "EXP-593",
    "scope": "EXP-590 broad page-ID pattern, including numbered pages and fRos",
    "source": "data/transcriptions/eva_zl3b.txt",
    "limitations": [
        "Sensitivity analysis only; does not replace or alter archived EXP-593.",
        "Exploratory variant set and previously selected target words.",
        "Alternative PRNG stream is not an exact replay of EXP-593's Python random.shuffle stream.",
        "Uniform draw per line has the same null distribution for line-initial counts as shuffling tokens within each line.",
    ],
}

def validate_archive_metadata(archived: dict) -> None:
    for key, expected in ARCHIVE_METADATA.items():
        if key not in archived or archived[key] != expected:
            raise AssertionError(f"archive metadata mismatch: {key}")
    # The archive has no null_model field: reject undocumented additions rather
    # than silently treating an unreviewed narrative as reproduced history.
    if "null_model" in archived:
        raise AssertionError("archive metadata mismatch: unexpected null_model")

import math

def compare(expected, actual, path="root"):
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            raise AssertionError(f"{path}: expected object")
        if set(expected) != set(actual):
            missing = sorted(set(expected) - set(actual))
            extra = sorted(set(actual) - set(expected))
            raise AssertionError(f"{path}: object keys mismatch; missing={missing}, extra={extra}")
        for key, value in expected.items():
            compare(value, actual[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise AssertionError(f"{path}: list mismatch")
        for i, value in enumerate(expected):
            compare(value, actual[i], f"{path}[{i}]")
    elif isinstance(expected, (float, int)) and not isinstance(expected, bool):
        if isinstance(actual, bool) or not isinstance(actual, (float, int)) or not math.isfinite(actual) or not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-12):
            raise AssertionError(f"{path}: archived={expected!r} reproduced={actual!r}")
    elif isinstance(expected, bool):
        # bool is an int subclass in Python: True == 1 must not pass integrity checks.
        if not isinstance(actual, bool) or expected != actual:
            raise AssertionError(f"{path}: archived={expected!r} reproduced={actual!r}")
    elif expected is None:
        if actual is not None:
            raise AssertionError(f"{path}: archived=None reproduced={actual!r}")
    elif expected != actual:
        raise AssertionError(f"{path}: archived={expected!r} reproduced={actual!r}")

def self_test_archive_metadata() -> None:
    """Exercise the actual archived file, not only a synthetic expected dict."""
    import copy
    archived = json.loads(OUT.read_text(encoding="utf-8"))
    validate_archive_metadata(archived)
    for key in ARCHIVE_METADATA:
        altered = copy.deepcopy(archived)
        altered[key] = [] if key == "limitations" else "TAMPERED"
        try:
            validate_archive_metadata(altered)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"negative regression failed for {key}")
    for key in ARCHIVE_METADATA:
        altered = copy.deepcopy(archived)
        del altered[key]
        try:
            validate_archive_metadata(altered)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"missing-field regression failed for {key}")
    altered = copy.deepcopy(archived)
    altered["null_model"] = "unverified historical assertion"
    try:
        validate_archive_metadata(altered)
    except AssertionError:
        pass
    else:
        raise AssertionError("negative regression failed for null_model")
    # Reject unexpected or missing nested fields, not merely altered values.
    for original, changed, label in (
        ({"tests": {"daiin": {"empirical_p": 0.1}}}, {"tests": {"daiin": {"empirical_p": 0.1, "unexpected": 1}}}, "extra nested key"),
        ({"tests": {"daiin": {"empirical_p": 0.1}}}, {"tests": {"daiin": {}}}, "missing nested key"),
        ({"tests": {"daiin": {"null_exceedances": 1}}}, {"tests": {"daiin": {"null_exceedances": True}}}, "boolean substituted for numeric"),
        ({"tests": {"daiin": {"flag": True}}}, {"tests": {"daiin": {"flag": 1}}}, "numeric substituted for boolean"),
        ({"tests": {"daiin": {"null_exceedances": 1}}}, {"tests": {"daiin": {"null_exceedances": float("nan")}}}, "non-finite NaN"),
        ({"tests": {"daiin": {"null_exceedances": 1}}}, {"tests": {"daiin": {"null_exceedances": float("inf")}}}, "non-finite infinity"),
    ):
        try:
            compare(original, changed, "negative_regression")
        except AssertionError:
            pass
        else:
            raise AssertionError(f"strict-key regression failed: {label}")
    print("ARCHIVE_METADATA_NEGATIVE_REGRESSIONS_PASS")

def main() -> None:
    raw = SOURCE.read_bytes()
    lines = parse(raw)
    observed = {w: {"occurrences": 0, "line_initial": 0, "line_final": 0} for w in VARIANTS}
    for tokens in lines:
        for word in VARIANTS:
            observed[word]["occurrences"] += tokens.count(word)
            observed[word]["line_initial"] += int(tokens[0] == word)
            observed[word]["line_final"] += int(tokens[-1] == word)
    rng = XorShift32(SEED)
    null = {word: [] for word in VARIANTS}
    for _ in range(N_PERM):
        counts = {word: 0 for word in VARIANTS}
        for tokens in lines:
            first = tokens[int(rng.random() * len(tokens))]
            for word in VARIANTS:
                counts[word] += int(first == word)
        for word in VARIANTS:
            null[word].append(counts[word])
    means = {w: sum(null[w]) / N_PERM for w in VARIANTS}
    sds = {w: (sum((x - means[w]) ** 2 for x in null[w]) / N_PERM) ** 0.5 for w in VARIANTS}
    def zscore(word: str, value: int | float) -> float:
        return (value - means[word]) / sds[word] if sds[word] else 0.0
    max_null_z = [max(zscore(w, null[w][i]) for w in VARIANTS) for i in range(N_PERM)]
    tests = {}
    for word in VARIANTS:
        exceed = sum(x >= observed[word]["line_initial"] for x in null[word])
        max_exceed = sum(x >= zscore(word, observed[word]["line_initial"]) for x in max_null_z)
        tests[word] = {
            "null_mean_initial": means[word], "null_sd_initial": sds[word],
            "observed_standardized_statistic": zscore(word, observed[word]["line_initial"]),
            "empirical_p": (exceed + 1) / (N_PERM + 1),
            "maxT_adjusted_p": (max_exceed + 1) / (N_PERM + 1),
            "null_exceedances": exceed, "maxT_exceedances": max_exceed,
        }
    result = {
        "status": "EXPLORATORY", "parent_analysis": "EXP-593",
        "scope": "EXP-590 broad page-ID pattern, including numbered pages and fRos",
        "source": "data/transcriptions/eva_zl3b.txt",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "lines": len(lines), "tokens": sum(map(len, lines)),
        "variants": list(VARIANTS), "observed": observed, "tests": tests,
        "permutations": N_PERM, "seed": f"0x{SEED:x}", "prng": "xorshift32",
        "null_model": "Synchronized independent uniform token draw per line; distribution-equivalent to within-line shuffle for line-initial counts. max-T uses the maximum per-variant standardized statistic on each replicate.",
        "limitations": [
            "Sensitivity analysis only; does not replace or alter archived EXP-593.",
            "Exploratory variant set and previously selected target words.",
            "Does not test semantics or provide a decipherment.",
            "Alternative PRNG stream is not an exact replay of EXP-593's Python random.shuffle stream.",
            "Current page-ID coverage does not establish full IVTFF conformance."
        ],
    }
    # Historical archive is immutable: verify against it, never overwrite it.
    archived = json.loads(OUT.read_text(encoding="utf-8"))
    validate_archive_metadata(archived)
    for key in ("source_sha256", "lines", "tokens", "variants", "observed", "permutations", "seed", "prng", "tests"):
        compare(archived[key], result[key], key)
    print(json.dumps({"status": "MATCH_ARCHIVED_NUMERICS", "archive": str(OUT), "source_sha256": result["source_sha256"]}, indent=2))

if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--self-test-contract"]:
        self_test_archive_metadata()
    elif len(sys.argv) == 1:
        main()
    else:
        raise SystemExit("usage: audit_exp593_expanded_population.py [--self-test-contract]")
