#!/usr/bin/env python3
"""Read-only EXP-616 legacy JSON schema adjudication; no new Voynich experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = "experiments/exp_616_folio_block_holdout_sensitivity/results.json"
ARCHIVE_GIT_BLOB_SHA1 = "03b8316b10abd511d7bd55546ef7ac051ed97254"
SOURCES = {
    "ZL3b": ("data/transcriptions/eva_zl3b.txt",
             "2a4533ab9bdfa85db9bad602d590978953055df1",
             "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"),
    "IT2a": ("data/transcriptions/eva_it2a.txt",
             "4d6d3f2537b1f507a257529b49c94af7d6e03446",
             "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"),
}
COUNT_FIELDS = ("cells", "folios", "ch_n", "sh_n")
RATE_FIELDS = ("ch_rate", "sh_rate", "difference_sh_minus_ch")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\\0" + raw).hexdigest()


def read_frozen(path: Path, blob_sha1: str, sha256: str | None = None) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or symlinked frozen file: {path}")
    raw = path.read_bytes()
    if git_blob_sha1(raw) != blob_sha1:
        raise ValueError(f"Frozen Git blob SHA-1 mismatch: {path}")
    if sha256 is not None and hashlib.sha256(raw).hexdigest() != sha256:
        raise ValueError(f"Frozen SHA-256 mismatch: {path}")
    return raw


def check_summary(summary: dict) -> None:
    for key in COUNT_FIELDS:
        if type(summary[key]) is not int or summary[key] < 0:
            raise ValueError(f"Invalid nonnegative count: {key}")
    if not summary["ch_n"] or not summary["sh_n"]:
        raise ValueError("Empty ch/sh denominator")
    for key in RATE_FIELDS:
        if not isinstance(summary[key], (int, float)) or not math.isfinite(summary[key]):
            raise ValueError(f"Invalid rate: {key}")
    if not 0 <= summary["ch_rate"] <= 1 or not 0 <= summary["sh_rate"] <= 1:
        raise ValueError("Rate outside [0,1]")
    if not math.isclose(summary["sh_rate"] - summary["ch_rate"],
                        summary["difference_sh_minus_ch"], rel_tol=0, abs_tol=1e-12):
        raise ValueError("Inconsistent sh-minus-ch rate")


def adjudicate(archive: dict) -> dict:
    if archive["experiment"] != "exp_616_folio_block_holdout_sensitivity":
        raise ValueError("Unexpected experiment identity")
    groups = archive["groups"]
    names = [g["name"] for g in groups]
    if len(names) != 4 or len(set(names)) != 4:
        raise ValueError("Expected four distinct historical blocks")
    if any(not g["folios"] or any(type(f) is not int for f in g["folios"]) for g in groups):
        raise ValueError("Invalid block membership")
    all_folios = [f for g in groups for f in g["folios"]]
    if len(all_folios) != len(set(all_folios)):
        raise ValueError("Overlapping historical blocks")
    if set(archive["sources"]) != set(SOURCES) or set(archive["results"]) != set(SOURCES):
        raise ValueError("Unexpected corpus identities")
    if any(archive["sources"][name] != SOURCES[name][1] for name in SOURCES):
        raise ValueError("Historical source Git blob SHA-1 drift")
    out = {}
    for name, original in archive["results"].items():
        total = original["all"]
        check_summary(total)
        leave_out = original["leave_out"]
        contributions = original["group_contributions"]
        if [x["block"] for x in leave_out] != names or [x["block"] for x in contributions] != names:
            raise ValueError("Historical block alignment drift")
        corrected = []
        for index, block in enumerate(names):
            # Historical JSON calls this field 'removed', but its numbers are
            # the observations REMAINING after the block is excluded.
            remaining = leave_out[index]["removed"]
            excluded = contributions[index]["summary"]
            check_summary(remaining)
            check_summary(excluded)
            for field in COUNT_FIELDS:
                if remaining[field] + excluded[field] != total[field]:
                    raise ValueError(f"{name}/{block}: {field} is not additive")
            for side in ("ch", "sh"):
                n = total[side + "_n"]
                rate = (remaining[side + "_n"] * remaining[side + "_rate"]
                        + excluded[side + "_n"] * excluded[side + "_rate"]) / n
                if not math.isclose(rate, total[side + "_rate"], rel_tol=0, abs_tol=1e-12):
                    raise ValueError(f"{name}/{block}: {side} weighted rate drift")
            if excluded["folios"] != len(groups[index]["folios"]):
                raise ValueError(f"{name}/{block}: excluded folio count drift")
            corrected.append({"block": block, "remaining": remaining, "excluded": excluded})
        for field in COUNT_FIELDS:
            if sum(x["excluded"][field] for x in corrected) != total[field]:
                raise ValueError(f"{name}: contributions do not partition total {field}")
        out[name] = {"all": total, "leave_out": corrected}
    return {
        "status": "SCHEMA_CORRECTION_ONLY_NOT_REPRODUCED",
        "experiment": archive["experiment"],
        "legacy_field": "results.*.leave_out[*].removed",
        "legacy_field_actual_meaning": "remaining after excluding the named block",
        "sources": {name: {"path": SOURCES[name][0],
                            "git_blob_sha1": SOURCES[name][1],
                            "sha256": SOURCES[name][2]} for name in SOURCES},
        "results": out,
        "limitations": [
            "No historical EXP-616 script is present in its experiment directory.",
            "Internal arithmetic and source identity checked; source-to-statistic recomputation not performed.",
            "Four heuristic numeric blocks are not verified codicological sections.",
            "ZL3b and IT2a are alternative transcriptions of one manuscript, not independent samples.",
            "No new inference, significance test, semantic anchor, or translation.",
        ],
    }


def audit(root: Path = ROOT) -> dict:
    raw = read_frozen(root / ARCHIVE, ARCHIVE_GIT_BLOB_SHA1)
    for path, blob, sha256 in SOURCES.values():
        read_frozen(root / path, blob, sha256)
    result = adjudicate(json.loads(raw))
    result["archive"] = ARCHIVE
    result["archive_git_blob_sha1"] = ARCHIVE_GIT_BLOB_SHA1
    result["archive_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Create a new JSON file; never overwrite")
    args = parser.parse_args()
    result = audit()
    if args.out:
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\\n")
    print(json.dumps({"status": result["status"],
                      "archive_sha256": result["archive_sha256"],
                      "blocks": {name: len(x["leave_out"]) for name, x in result["results"].items()}},
                     sort_keys=True))


if __name__ == "__main__":
    main()
