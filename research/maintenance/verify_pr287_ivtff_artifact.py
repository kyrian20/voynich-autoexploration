#!/usr/bin/env python3
"""Offline, fail-closed verifier for the exact-head IVTFF receipt from PR #287.

Download GitHub Actions artifact 14191233024 from run 43789138871.
This checks archived bytes, inner checksum and fixed corpus identities; it
does not validate IVTFF grammar, corpus bytes, or linguistic hypotheses.
"""
import argparse
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ZIP_SHA = "9f316ae1993389803d7b0af7b66db0bf6e2dbd45279e7a4547d8326786c31fd6"
MAX_MEMBER_BYTES = 4 * 1024 * 1024  # generous bound for a three-source audit receipt
MAX_ZIP_BYTES = 8 * 1024 * 1024  # cap compressed archive input, not just expanded members
SOURCES = {
    "data/transcriptions/eva_zl3b.txt": "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
    "data/transcriptions/zl3a.txt": "56419297682d338ff1a0a17f5ae251e3ee3e2c5bf05a62db04c5385ef30b36a2",
    "data/transcriptions/eva_it2a.txt": "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
}


def reject_duplicate_fields(pairs: list[tuple[str, object]]) -> dict:
    """Reject ambiguous JSON mappings instead of accepting the last value."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def reject_nonfinite_constant(value: str) -> None:
    """Reject non-standard NaN/Infinity accepted by Python's default JSON parser."""
    raise ValueError(f"non-finite JSON constant: {value}")


def verify(path: Path, expected_zip_sha: str = ZIP_SHA) -> dict:
    # Hash incrementally: path.read_bytes() formerly loaded an arbitrarily large
    # attacker-controlled ZIP into RAM before the member-size checks ran.
    if path.stat().st_size > MAX_ZIP_BYTES:
        raise ValueError("oversized ZIP archive")
    digest = hashlib.sha256()
    total = 0
    with ExitStack() as stack:
        stream = stack.enter_context(path.open("rb"))
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            total += len(chunk)
            if total > MAX_ZIP_BYTES:
                raise ValueError("oversized ZIP archive")
            digest.update(chunk)
        actual = digest.hexdigest()
        if actual != expected_zip_sha:
            raise ValueError("ZIP SHA-256 mismatch")
        stream.seek(0)
        archive = stack.enter_context(zipfile.ZipFile(stream))
        # Same open descriptor: pathname replacement cannot redirect parsing.
        # Concurrent in-place modification remains outside this guarantee.
        if sorted(archive.namelist()) != ["ivtff-minimum-format.json", "ivtff-minimum-format.sha256"]:
            raise ValueError("unexpected ZIP members")
        # Check declared sizes and cap actual streaming reads: a forged ZIP can
        # advertise a small size yet expand to a much larger payload.
        for member in archive.infolist():
            # Reject encrypted entries explicitly instead of broadly catching
            # RuntimeError, which could mask unrelated programming defects.
            if member.flag_bits & 0x1:
                raise ValueError("encrypted ZIP member")
            limit = 4096 if member.filename.endswith(".sha256") else MAX_MEMBER_BYTES
            if member.file_size > limit:
                raise ValueError("oversized ZIP member")
        def bounded_read(name: str, limit: int) -> bytes:
            with archive.open(name) as stream:
                data = stream.read(limit + 1)
            if len(data) > limit:
                raise ValueError("oversized ZIP member")
            return data
        payload = bounded_read("ivtff-minimum-format.json", MAX_MEMBER_BYTES)
        manifest = bounded_read("ivtff-minimum-format.sha256", 4096).decode("ascii").strip()
        # Detect persistent in-place edits after the first digest. This is not
        # an atomic snapshot and cannot exclude adversarial transient rewrites.
        stream.seek(0)
        second_digest = hashlib.sha256()
        second_total = 0
        for chunk in iter(lambda: stream.read(64 * 1024), b""):
            second_total += len(chunk)
            if second_total > MAX_ZIP_BYTES:
                raise ValueError("oversized ZIP archive")
            second_digest.update(chunk)
        if second_total != total or second_digest.hexdigest() != actual:
            raise ValueError("ZIP changed during verification")
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", manifest)
    # The archived PR #287 runner used an absolute temporary pathname in
    # sha256sum output; synthetic receipts use the bare member name. Reject
    # traversal or any other alias without rejecting those historical bytes.
    permitted_targets = {
        "ivtff-minimum-format.json",
        "/home/runner/work/_temp/ivtff-minimum-format.json",
    }
    if not match or match.group(2) not in permitted_targets:
        raise ValueError("invalid inner manifest")
    inner_sha = hashlib.sha256(payload).hexdigest()
    if inner_sha != match.group(1):
        raise ValueError("inner JSON SHA-256 mismatch")
    report = json.loads(payload, object_pairs_hook=reject_duplicate_fields,
                        parse_constant=reject_nonfinite_constant)
    if not isinstance(report, dict):
        raise ValueError("invalid report object")
    if report.get("audit") != "IVTFF file-level minimums" or report.get("status") != "PASS":
        raise ValueError("unexpected audit/status")
    records = report.get("files")
    if not isinstance(records, list) or len(records) != len(SOURCES):
        raise ValueError("unexpected record count")
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("invalid file record")
        source = record.get("source")
        if not isinstance(source, str) or source not in SOURCES or source in seen:
            raise ValueError("unknown or duplicate source")
        if record.get("sha256") != SOURCES[source] or record.get("status") != "PASS" or record.get("errors") != []:
            raise ValueError("corpus digest/status mismatch")
        seen.add(source)
    if seen != set(SOURCES):
        raise ValueError("missing corpus")
    return {"status": "VERIFIED_RECEIPT_ONLY", "zip_sha256": actual,
            "json_sha256": inner_sha, "corpus_sha256": {key: SOURCES[key] for key in sorted(seen)}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact_zip", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.artifact_zip, expected_zip_sha=ZIP_SHA), indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, RecursionError, zipfile.BadZipFile, UnicodeError, KeyError, TypeError, NotImplementedError) as exc:
        print(f"REJECTED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
