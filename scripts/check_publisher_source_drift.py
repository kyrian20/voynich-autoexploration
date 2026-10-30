#!/usr/bin/env python3
"""Refuse to publish scheduled results against a changed source tree.

The publisher writes only to research/experiments/. Changes elsewhere in
master since the triggering commit require a fresh run, not a rebase of stale
results. A content-identical change is harmless; git diff compares trees.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def changed_source_paths(repo: Path, baseline: str, candidate: str) -> list[str]:
    if not baseline or not candidate:
        raise ValueError("Both baseline and candidate commits are required")
    cmd = ["git", "diff", "--name-only", "--no-renames", baseline, candidate,
           "--", ".", ":(exclude)research/experiments/**"]
    result = subprocess.run(cmd, cwd=repo, text=True, capture_output=True,
                            check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Cannot verify source drift (git exit {result.returncode}): "
                           f"{result.stderr.strip()}")
    return result.stdout.splitlines()


def assert_no_source_drift(repo: Path, baseline: str, candidate: str) -> None:
    changed = changed_source_paths(repo, baseline, candidate)
    if changed:
        raise RuntimeError("Source tree changed since workflow checkout; "
                           "refusing to rebase stale generated results:\n" +
                           "\n".join(changed))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="origin/master")
    args = parser.parse_args()
    assert_no_source_drift(args.repo, args.base, args.head)
    print(f"Publisher input tree unchanged: {args.base} -> {args.head} "
          "(research/experiments/ output-only changes allowed)")


if __name__ == "__main__":
    main()
