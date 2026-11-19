#!/usr/bin/env python3
"""Fail-closed provenance gate for EXP-590/593 (2026-11-18).

This does not reproduce the published Monte Carlo results. Never replace a
missing historical generator with a newly written script and call it a replay.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

FILES = (
    "research/experiments/2026-11-18-exp590-corrected-L-metadata.json",
    "research/experiments/2026-11-18-exp593-corrected-L-metadata.json",
)

def inspect(root, paths=FILES):
    issues = []
    records = []
    for relative in paths:
        path = root / relative
        if not path.is_file():
            issues.append(f"{relative}: missing result JSON")
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc:
            issues.append(f"{relative}: unreadable JSON: {exc}")
            continue
        if not isinstance(record, dict):
            issues.append(f"{relative}: result JSON must be an object")
            continue
        records.append(record)
        source = record.get("source")
        digest = record.get("source_sha256")
        if not isinstance(source, str) or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            issues.append(f"{relative}: source path or SHA-256 absent")
        else:
            source_path = (root / source).resolve()
            if not source_path.is_relative_to(root.resolve()) or not source_path.is_file():
                issues.append(f"{relative}: exact source file unavailable")
            elif hashlib.sha256(source_path.read_bytes()).hexdigest() != digest:
                issues.append(f"{relative}: source SHA-256 mismatch")
        for key in ("generator_path", "generator_sha256", "reproduction_command",
                    "reproduction_log_path", "reproduced_output_sha256"):
            if not record.get(key):
                issues.append(f"{relative}: no attested {key}")
        # Nonempty metadata alone is not evidence: verify referenced local bytes.
        for field in ("generator_path", "reproduction_log_path"):
            value = record.get(field)
            if value is None or value == "":
                continue  # already reported by the required-field check above
            if not isinstance(value, str):
                issues.append(f"{relative}: invalid {field} type")
                continue
            candidate = (root / value).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.is_file():
                issues.append(f"{relative}: {field} file unavailable or outside root")
            elif field == "reproduction_log_path":
                expected = record.get("reproduction_log_sha256")
                if not isinstance(expected, str) or len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
                    issues.append(f"{relative}: invalid or missing reproduction log SHA-256")
                elif hashlib.sha256(candidate.read_bytes()).hexdigest() != expected:
                    issues.append(f"{relative}: reproduction log SHA-256 mismatch")
            elif field == "generator_path":
                expected = record.get("generator_sha256")
                if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
                    issues.append(f"{relative}: invalid generator SHA-256")
                elif hashlib.sha256(candidate.read_bytes()).hexdigest() != expected:
                    issues.append(f"{relative}: generator SHA-256 mismatch")
        # A log is not an execution witness if it is merely a second name
        # for the input corpus or the generator (including hardlinks).
        evidence_names = ("source", "generator_path", "reproduction_log_path")
        evidence_paths = []
        for name in evidence_names:
            value = record.get(name)
            if isinstance(value, str) and value.strip():
                candidate = (root / value).resolve()
                if candidate.is_relative_to(root.resolve()) and candidate.is_file():
                    evidence_paths.append((name, candidate))
        for i, (left_name, left_path) in enumerate(evidence_paths):
            for right_name, right_path in evidence_paths[i + 1:]:
                if left_path.samefile(right_path):
                    issues.append(f"{relative}: {left_name} aliases {right_name} evidence")
        for field in ("reproduced_output_sha256",):
            value = record.get(field)
            if value and (not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value)):
                issues.append(f"{relative}: invalid {field}")
        # A declared output digest alone cannot attest to any output bytes.
        # Require an archived output and verify its exact digest before review.
        if record.get("reproduction_status") in ("REPRODUCED", "VALIDATED"):
            output = record.get("reproduced_output_path")
            expected_output = record.get("reproduced_output_sha256")
            if not isinstance(output, str) or not output.strip():
                issues.append(f"{relative}: no attested reproduced_output_path")
            else:
                output_path = (root / output).resolve()
                if not output_path.is_relative_to(root.resolve()) or not output_path.is_file():
                    issues.append(f"{relative}: reproduced output unavailable or outside root")
                elif not isinstance(expected_output, str) or len(expected_output) != 64 or any(c not in "0123456789abcdef" for c in expected_output):
                    issues.append(f"{relative}: invalid reproduced output digest")
                elif any(
                    output_path == evidence_path
                    or (evidence_path.is_file() and output_path.samefile(evidence_path))
                    for evidence_path in (
                        {(root / p).resolve() for p in paths}
                        | {(root / record[k]).resolve() for k in ("source", "generator_path", "reproduction_log_path")
                           if isinstance(record.get(k), str) and record[k].strip()}
                    )
                ):
                    issues.append(f"{relative}: reproduced output aliases a frozen result or an input/log artefact")
                elif hashlib.sha256(output_path.read_bytes()).hexdigest() != expected_output:
                    issues.append(f"{relative}: reproduced output SHA-256 mismatch")
        command = record.get("reproduction_command")
        if command and (not isinstance(command, str) or not command.strip()):
            issues.append(f"{relative}: invalid reproduction_command")
        if record.get("reproduction_status") not in ("REPRODUCED", "VALIDATED"):
            issues.append(f"{relative}: no attested reproduction status")
    # An output must not alias evidence belonging to the *other* record.
    # The per-record guard above cannot see records processed later.
    if len(records) == len(paths):
        evidence = {
            (root / value).resolve()
            for record in records
            for key in ("source", "generator_path", "reproduction_log_path")
            if isinstance((value := record.get(key)), str) and value.strip()
        }
        for relative, record in zip(paths, records):
            output = record.get("reproduced_output_path")
            if (record.get("reproduction_status") in ("REPRODUCED", "VALIDATED")
                    and isinstance(output, str) and output.strip()
                    and any(
                        (root / output).resolve() == evidence_path
                        or ((root / output).is_file() and evidence_path.is_file()
                            and (root / output).samefile(evidence_path))
                        for evidence_path in evidence
                    )):
                issues.append(f"{relative}: reproduced output aliases cross-record input/log evidence")
    if len(records) == len(paths) and any(
        r.get("source_sha256") != records[0].get("source_sha256") for r in records[1:]
    ):
        issues.append("EXP-590/593: declared source digests differ")
    # A single archived output cannot independently attest two different
    # experiment results. Require distinct outputs for the two claims.
    if len(records) == len(paths) and all(
        r.get("reproduction_status") in ("REPRODUCED", "VALIDATED") for r in records
    ):
        outputs = [r.get("reproduced_output_path") for r in records]
        if all(isinstance(p, str) and p.strip() for p in outputs) and any(
            (root / left).resolve() == (root / right).resolve()
            or ((root / left).is_file() and (root / right).is_file()
                and (root / left).samefile(root / right))
            for i, left in enumerate(outputs) for right in outputs[i + 1:]
        ):
            issues.append("EXP-590/593: reused reproduced output path across distinct results")
    return issues

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    issues = inspect(args.root)
    print(json.dumps({"gate": "exp590_exp593_provenance",
                      "status": "BLOCKED" if issues else "READY_FOR_INDEPENDENT_REPRODUCTION_REVIEW",
                      "issues": issues}, indent=2))
    return 2 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
