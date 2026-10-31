#!/usr/bin/env python3
"""Refuse stale-result publication when concurrent Git changes affect inputs.

Only *new* files with the four scheduled generators' exact output names may
appear on master during a publisher rebase. Existing results, corrections,
archived evidence, scripts and corpus files are not exempt.
"""
from __future__ import annotations

import argparse
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
