#!/usr/bin/env python3
"""Independent *coverage* audit of the frozen prospective physical-leaf holdout.

Do not treat named/non-numeric loci as test leaves. No tokens are decoded, no
scientific hypothesis is evaluated, and no historical manifest is rewritten.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

# Support both `python scripts/...` and `import scripts...` without changing
# the archived reader or its historical tokenization policy.
if __package__:
    from .ivtff_physical_rows import checked_physical_lines
else:
    from ivtff_physical_rows import checked_physical_lines

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json"
SOURCE_NAMES = ("eva_zl3b.txt", "eva_it2a.txt")
# Independent locks: the v2 manifest is not an authority for its own source
# hashes. A changed source plus a synchronously rehashed manifest must fail.
# These are the original frozen bytes, not hashes read from the manifest.
FROZEN_SOURCE_SHA256 = {
    "eva_zl3b.txt": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
    "eva_it2a.txt": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
}
# Historical split identity is frozen independently of the manifest and its
# generator: an internally consistent but reassigned manifest must fail.
FROZEN_SALT = "VOYNICH-FUTURE-RULES-2026-10-23-v1"
# The frozen split also carries scientific-use restrictions. A manifest with
# unchanged source hashes and folio assignments must not be allowed to claim
# VALIDATED status, remove its prior-exposure caveat or change test-use rules.
# Keep this contract independent of the manifest generator and JSON file.
FROZEN_CONTRACT = {
    "status": "PROPOSED_FOR_FUTURE_RULES",
    "supersedes": "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest.json",
    "correction": "Include optional numeric panels after r/v in IVTFF folio headers",
    "unit": "physical_leaf_number; recto and verso and panels grouped",
    "allocation": {"train": 0.70, "development": 0.15, "test": 0.15},
    "selection": "shared leaves in both editions; panel-aware header IDs only",
    "caveat": "Not a historically untouched holdout; previously inspected leaves remain exposed.",
    "forbidden": [
        "selecting rules on test folios",
        "tuning on test outcomes",
        "claiming a historically independent or semantic validation",
    ],
}
FROZEN_FIELDS = set(FROZEN_CONTRACT) | {
    "schema_version", "corpora", "salt", "partitions", "counts",
    "eligible_count", "source_only_leaves",
}
# Independent IVTFF-shaped tag checks: do not count a prefix match as a
# complete header or locus. This is a coverage audit, not full IVTFF parsing.
PAGE_ID = re.compile(r"^f(?:[0-9]+[rv][1-6]?|Ros)$")
RECORD_ID = re.compile(
    # Accept printable ASCII locator/transcriber symbols only. The previous
    # [^;>] admitted spaces, Unicode and '<' as valid three-character codes;
    # a coverage-only run could then certify malformed locus identifiers.
    # Keep this structural constraint aligned with the strict census without
    # treating agreement as full IVTFF or semantic validation.
    r"^(f(?:[0-9]+[rv][1-6]?|Ros))\.(?P<line>[0-9]{1,3}),[!-:=?-~]{3}(?:;[!-:=?-~])?$"
)


def physical_page_identity(page: str) -> tuple:
    """Logical IVTFF page identity; zero padding cannot create a second page."""
    if page == "fRos":
        return ("Ros",)
    match = re.fullmatch(r"f([0-9]+)([rv])([1-6]?)", page)
    if match is None:
        raise ValueError(f"Invalid physical page identity: {page}")
    return ("numeric", int(match.group(1)), match.group(2), match.group(3))


def _unique_manifest_keys(pairs: list[tuple[str, object]]) -> dict:
    """Reject duplicate JSON members at every depth before checking a holdout."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate holdout manifest JSON key: {key}")
        result[key] = value
    return result


def load_manifest(path: Path = MANIFEST) -> dict:
    """Parse the frozen manifest without silently accepting overwritten keys."""
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_manifest_keys)


def inspect_source(raw: bytes, *, include_page_ids: bool = False,
                   include_locus_ids: bool = False) -> dict:
    leaves: set[int] = set()
    named_headers: Counter[str] = Counter()
    named_loci: Counter[str] = Counter()
    page_ids: set[str] = set()
    seen_page_keys: set[tuple] = set()
    locus_ids: list[str] = []
    seen_locus_keys: set[tuple[str, int, str]] = set()
    numeric_tags = numeric_headers = numeric_loci = 0
    active_page = None
    for line_no, line in checked_physical_lines(raw.decode("utf-8-sig")):
        # A leading space or tab must not silently erase a physical page or
        # locus from this standalone census. The strict reader diagnoses this,
        # but the coverage-only audit must fail independently too.
        if line.lstrip(" \t") != line and line.lstrip(" \t").startswith("<f"):
            raise ValueError(f"Indented folio tag at source line {line_no}")
        # A slash is a continuation marker, not permission to conceal a
        # physical page/locus tag. The independent strict census rejects
        # these rows; the holdout coverage audit must also fail closed rather
        # than silently losing a locus while a caller updates the source hash.
        stripped = line.lstrip(" \t")
        if stripped.startswith("/") and stripped[1:].lstrip(" \t").startswith("<f"):
            raise ValueError(f"Folio tag hidden behind continuation slash at source line {line_no}")
        if not line.startswith("<f"):
            continue
        end = line.find(">")
        if end < 0 or (end + 1 < len(line) and line[end + 1] not in " \t"):
            raise ValueError(f"Malformed folio tag boundary at source line {line_no}")
        tag = line[1:end]
        is_header = PAGE_ID.fullmatch(tag) is not None
        locus = RECORD_ID.fullmatch(tag)
        if not is_header and locus is None:
            kind = "numeric" if len(line) > 2 and line[2].isdigit() else "named"
            raise ValueError(f"Unparsed {kind} folio header at source line {line_no}")
        page = tag if is_header else locus.group(1)
        if not is_header:
            # An exact duplicate locator is a repeated physical record, not
            # an additional independent observation. Match the strict IVTFF
            # census before certifying coverage in standalone mode.
            locus_number = int(locus.group("line"))
            # The numeric line is a physical index, not an opaque string:
            # .01 and .1 with the same page/locator denote the same locus.
            # Preserve distinct locator/transcriber suffixes as separate IDs.
            locus_key = (page, locus_number, tag.split(",", 1)[1])
            if locus_key in seen_locus_keys:
                raise ValueError(f"Duplicate locus identifier {tag} at source line {line_no}")
            seen_locus_keys.add(locus_key)
            if not 1 <= locus_number <= 160:
                raise ValueError(f"Locus number outside 1..160 at source line {line_no}: {tag}")
            locus_ids.append(tag)
        if is_header:
            # A set of page IDs is not enough: a repeated physical header
            # changes the source structure without changing leaf membership.
            # Reject it here as well as in the independent strict census.
            # f01r and f1r denote the same physical page. Keep raw spelling
            # for reporting, but reject duplicate logical page identities.
            page_key = physical_page_identity(page)
            if page_key in seen_page_keys:
                raise ValueError(f"Duplicate physical folio header {page} at source line {line_no}")
            seen_page_keys.add(page_key)
            active_page = page
            page_ids.add(page)
        elif page != active_page:
            raise ValueError(f"Orphan or mismatched locus at source line {line_no}")
        if page == "fRos":
            if is_header:
                named_headers["Ros"] += 1
            else:
                named_loci["Ros"] += 1
            continue
        leaf = int(re.match(r"^f([0-9]+)", page).group(1))
        if leaf <= 0:
            raise ValueError(f"Nonpositive physical leaf at source line {line_no}")
        numeric_tags += 1
        if is_header:
            numeric_headers += 1
        else:
            numeric_loci += 1
        leaves.add(leaf)
    if not leaves:
        raise ValueError("No numeric physical leaves found")
    result = {
        "numeric_tag_count": numeric_tags,
        "numeric_page_header_count": numeric_headers,
        "numeric_locus_record_count": numeric_loci,
        "numeric_leaves": sorted(leaves),
        "named_tag_count": sum(named_headers.values()) + sum(named_loci.values()),
        "named_page_headers": dict(sorted(named_headers.items())),
        "named_page_header_count": sum(named_headers.values()),
        "named_locus_records": dict(sorted(named_loci.items())),
        "named_locus_record_count": sum(named_loci.values()),
    }
    # The crosswalk needs exact page identities, not just leaf-number coverage.
    # Keep the historical audit JSON unchanged unless explicitly requested.
    if include_page_ids:
        result["page_ids"] = sorted(page_ids)
    if include_locus_ids:
        result["locus_ids"] = sorted(locus_ids)
    return result


def locked_partition(leaf: int) -> str:
    """Independently replay the committed SHA-256 physical-leaf allocation."""
    digest = hashlib.sha256(f"{FROZEN_SALT}:{leaf}".encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big") % 10000
    return "train" if value < 7000 else ("development" if value < 8500 else "test")


def audit(source_bytes: dict[str, bytes], manifest: dict, *,
          enforce_frozen_source_hashes: bool = True) -> dict:
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 2:
        raise ValueError("Requires integer schema version 2 in frozen holdout manifest")
    if set(manifest) != FROZEN_FIELDS:
        raise ValueError("Frozen holdout manifest fields mismatch")
    for field, expected in FROZEN_CONTRACT.items():
        if manifest[field] != expected:
            raise ValueError(f"Frozen holdout contract mismatch: {field}")
    if manifest.get("salt") != FROZEN_SALT:
        raise ValueError("Frozen partition salt mismatch")
    if set(source_bytes) != set(SOURCE_NAMES) or set(manifest["corpora"]) != set(SOURCE_NAMES):
        raise ValueError("Unexpected or missing source edition")
    coverage = {}
    for name in SOURCE_NAMES:
        # Check independently of the mutable manifest before parsing the source.
        # Only synthetic regression fixtures may explicitly opt out.
        sha = hashlib.sha256(source_bytes[name]).hexdigest()
        if (enforce_frozen_source_hashes
                and sha != FROZEN_SOURCE_SHA256[name]):
            raise ValueError(f"Frozen source SHA-256 mismatch for {name}")
        record = inspect_source(source_bytes[name])
        expected = manifest["corpora"][name]
        # The frozen source record has exactly three provenance fields.
        # Extra nested claims must not bypass the top-level manifest gate.
        if not isinstance(expected, dict) or set(expected) != {
            "path", "sha256", "leaf_count"
        }:
            raise ValueError(f"Frozen source metadata fields mismatch for {name}")
        if expected["path"] != f"data/transcriptions/{name}" or expected["sha256"] != sha:
            raise ValueError(f"Source provenance mismatch for {name}")
        if type(expected["leaf_count"]) is not int:
            raise ValueError(f"Frozen leaf count must be integer for {name}")
        if expected["leaf_count"] != len(record["numeric_leaves"]):
            raise ValueError(f"Leaf count mismatch for {name}")
        coverage[name] = {"sha256": sha, **record}

    shared = set(coverage[SOURCE_NAMES[0]]["numeric_leaves"]) & set(coverage[SOURCE_NAMES[1]]["numeric_leaves"])
    if set(manifest["counts"]) != {"train", "development", "test"}:
        raise ValueError("Frozen holdout count fields mismatch")
    if set(manifest["source_only_leaves"]) != set(SOURCE_NAMES):
        raise ValueError("Frozen holdout source-only edition fields mismatch")
    groups = manifest["partitions"]
    if set(groups) != {"train", "development", "test"}:
        raise ValueError("Partition names differ")
    assigned = []
    for group in ("train", "development", "test"):
        values = groups[group]
        if any(type(n) is not int or n <= 0 for n in values) or len(values) != len(set(values)):
            raise ValueError(f"Invalid or duplicated leaves in {group}")
        if type(manifest["counts"][group]) is not int:
            raise ValueError(f"Frozen count must be integer for {group}")
        if manifest["counts"][group] != len(values):
            raise ValueError(f"Count mismatch in {group}")
        assigned.extend(values)
    if len(assigned) != len(set(assigned)) or set(assigned) != shared:
        raise ValueError("Assigned leaves differ from the intersection of source numeric leaves")
    # Counts, uniqueness and coverage alone cannot detect a same-size swap
    # between train and test. Recompute each assignment from the frozen salt.
    for group in ("train", "development", "test"):
        if groups[group] != sorted(groups[group]):
            raise ValueError(f"Unsorted frozen partition: {group}")
        for leaf in groups[group]:
            if locked_partition(leaf) != group:
                raise ValueError(f"Partition hash assignment mismatch: leaf {leaf} in {group}")
    if type(manifest["eligible_count"]) is not int:
        raise ValueError("Frozen eligible count must be integer")
    if manifest["eligible_count"] != len(shared):
        raise ValueError("Eligible count mismatch")
    for name in SOURCE_NAMES:
        expected_only = sorted(set(coverage[name]["numeric_leaves"]) - shared)
        source_only = manifest["source_only_leaves"][name]
        if not isinstance(source_only, list) or any(type(n) is not int for n in source_only):
            raise ValueError(f"Frozen source-only leaves must be integer list for {name}")
        if source_only != expected_only:
            raise ValueError(f"Source-only leaves mismatch for {name}")

    return {
        "status": "COVERAGE_VERIFIED_NOT_IVTFF_OR_SEMANTIC_VALIDATION",
        "manifest": "research/decipherment/2026-10-23-prospective-leaf-holdout/manifest-v2.json",
        "eligible_numeric_physical_leaves": len(shared),
        "partitions": {key: len(groups[key]) for key in ("train", "development", "test")},
        "source_coverage": coverage,
        "named_loci_holdout_status": "EXCLUDED_UNASSIGNED_NOT_VALID_TEST_FOLIOS",
        "limitations": [
            "Named folios (e.g. Ros) cannot be mapped to a physical-leaf split by this manifest.",
            "Numeric folio recognition is a header coverage check, not full IVTFF conformity.",
            "A future model must explicitly reject named/unassigned loci from confirmatory evaluation.",
            "The numeric test leaves were previously inspected historically; this is not a blind semantic validation.",
            "The source transcriptions are two editions of the same manuscript, not independent replications.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    manifest = load_manifest()
    sources = {name: (ROOT / "data/transcriptions" / name).read_bytes() for name in SOURCE_NAMES}
    result = audit(sources, manifest)
    output = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        # A repeated invocation must not truncate prior holdout evidence.
        with args.out.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(output)
    print(json.dumps({
        "status": result["status"],
        "eligible_numeric_physical_leaves": result["eligible_numeric_physical_leaves"],
        "named_locus_records": {k: v["named_locus_records"] for k, v in result["source_coverage"].items()},
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
