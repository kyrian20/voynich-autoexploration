#!/usr/bin/env python3
"""Read-only scope audit: EXP-601 resampled IVTFF page/panel IDs, not physical leaves."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "experiments/exp_601_folio_clustered_confirmation/script.py"
RESULT = "experiments/exp_601_folio_clustered_confirmation/results.json"
CORPUS = "data/transcriptions/eva_zl3b.txt"
FROZEN_BLOBS = {
    SCRIPT: "1bdb44324c0e27483d0e57fbc7ec37795745d2a8",
    RESULT: "485e489c2552d4b492ae11a51f063cdea8524de7",
}
CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
PAGE_ID = re.compile(r"f([1-9][0-9]*)([rv])([0-9]*)\Z", flags=re.ASCII)
# SHA-256 of JSON-compact, ASCII-encoded, ordered historical page/panel IDs.
# Independently reconstructed from frozen results.json; not a corpus digest.
FROZEN_PAGE_IDS_SHA256 = "03817ab591c91407bb9502f7ae2cf33fc946fc2b43c1cb4228e41ff7bc5d5795"


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def frozen_bytes(path: Path, *, blob_sha1: str | None = None,
                 sha256: str | None = None) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or symlinked frozen source: {path}")
    raw = path.read_bytes()
    if blob_sha1 is not None and git_blob_sha1(raw) != blob_sha1:
        raise ValueError(f"Frozen Git blob SHA-1 mismatch: {path}")
    if sha256 is not None and hashlib.sha256(raw).hexdigest() != sha256:
        raise ValueError(f"Frozen SHA-256 mismatch: {path}")
    return raw


def unique_json_pairs(pairs: list[tuple[str, object]]) -> dict:
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"Duplicate JSON key: {key}")
        out[key] = value
    return out


def leaf_and_side(page: str) -> tuple[int, str]:
    if type(page) is not str:
        raise ValueError("Non-string IVTFF page identifier")
    match = PAGE_ID.fullmatch(page)
    if match is None:
        raise ValueError(f"Unrecognized IVTFF page/panel identifier: {page!r}")
    return int(match.group(1)), match.group(2)


def classify_units(ids: list[str]) -> dict:
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate historical page/panel identifiers")
    grouped = collections.defaultdict(list)
    for page in ids:
        leaf, _ = leaf_and_side(page)
        grouped[leaf].append(page)
    by_leaf = {str(leaf): sorted(pages) for leaf, pages in sorted(grouped.items())}
    both_sides = sum(len({leaf_and_side(p)[1] for p in pages}) == 2
                     for pages in by_leaf.values())
    histogram = collections.Counter(len(pages) for pages in by_leaf.values())
    return {
        "historical_resampling_units": len(ids),
        "distinct_numbered_physical_leaves": len(by_leaf),
        "leaves_with_both_sides": both_sides,
        "leaves_with_one_side": len(by_leaf) - both_sides,
        "page_panel_units_per_leaf_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "page_panel_ids_by_numbered_leaf": by_leaf,
    }


def adjudicate(archive: dict) -> dict:
    if archive["experiment"] != "exp_601_folio_clustered_confirmation":
        raise ValueError("Unexpected historical experiment")
    if archive["source"]["path"] != CORPUS or archive["source"]["sha256"] != CORPUS_SHA256:
        raise ValueError("Historical corpus provenance drift")
    if archive["sample"]["eligible_lines"] != 2325:
        raise ValueError("Historical sample drift")
    if archive["primary_effect"]["bootstrap_replicates"] != 20000:
        raise ValueError("Historical bootstrap count drift")
    if archive["primary_effect"]["bootstrap_seed"] != 60120261019:
        raise ValueError("Historical bootstrap seed drift")
    rows = archive["leave_one_folio_out"]["all_folios"]
    ids = [r["folio"] for r in rows]
    if archive["sample"]["represented_folios"] != len(ids):
        raise ValueError("Historical resampling-unit count drift")
    # The previous summary-only guard could accept f103r -> f103r1: same
    # leaf, side, unit count and histogram, but a different historical ID.
    identity_sha256 = hashlib.sha256(
        json.dumps(ids, ensure_ascii=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if identity_sha256 != FROZEN_PAGE_IDS_SHA256:
        raise ValueError("Frozen page/panel identity or order drift")
    result = classify_units(ids)
    if (result["historical_resampling_units"],
        result["distinct_numbered_physical_leaves"],
        result["leaves_with_both_sides"],
        result["page_panel_units_per_leaf_histogram"]) != (
            81, 40, 36, {"1": 3, "2": 35, "4": 2}):
        raise ValueError("Frozen page/panel-to-physical-leaf crosswalk drift")
    return {
        "status": "INVALID_FOR_CLAIM",
        "invalid_for_claim": [
            "The historical bootstrap interval is a physical-leaf-clustered uncertainty interval.",
            "The historical leave-one-folio-out range is leave-one-physical-leaf-out.",
        ],
        "retained_without_recalculation": [
            "The historical observed/expected positional enrichment is a descriptive statistic.",
            "The historical conditional within-line randomization tests a different null.",
            "The original bootstrap, its seed, its negative controls and its reported interval remain archived.",
        ],
        "historical_experiment": archive["experiment"],
        "historical_bootstrap_seed": archive["primary_effect"]["bootstrap_seed"],
        "historical_page_ids_sha256": identity_sha256,
        "historical_bootstrap_replicates": archive["primary_effect"]["bootstrap_replicates"],
        "source_sha256": CORPUS_SHA256,
        "audit_type": "metadata-only; no rebootstrap and no corpus re-tokenization",
        "crosswalk": result,
        "limitations": [
            "The historical parser groups by page/panel identifier (fNNr/v or foldout suffix), not by numbered physical leaf.",
            "This audit does not recompute a physical-leaf bootstrap interval or significance.",
            "Numbered leaves are a conservative grouping proxy, not a codicological reconstruction of bifolios.",
            "No language, cipher, meaning, or decipherment is inferred.",
        ],
    }


def audit(root: Path = ROOT) -> dict:
    source_script = frozen_bytes(root / SCRIPT, blob_sha1=FROZEN_BLOBS[SCRIPT])
    raw = frozen_bytes(root / RESULT, blob_sha1=FROZEN_BLOBS[RESULT])
    frozen_bytes(root / CORPUS, sha256=CORPUS_SHA256)
    archive = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_json_pairs)
    result = adjudicate(archive)
    result["historical_script_git_blob_sha1"] = FROZEN_BLOBS[SCRIPT]
    result["historical_script_sha256"] = hashlib.sha256(source_script).hexdigest()
    result["historical_results_git_blob_sha1"] = FROZEN_BLOBS[RESULT]
    result["historical_results_sha256"] = hashlib.sha256(raw).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Create a new JSON artifact without overwriting")
    args = parser.parse_args()
    result = audit()
    if args.out:
        with args.out.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    print(json.dumps({
        "status": result["status"],
        "historical_results_sha256": result["historical_results_sha256"],
        "historical_units": result["crosswalk"]["historical_resampling_units"],
        "numbered_physical_leaves": result["crosswalk"]["distinct_numbered_physical_leaves"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
