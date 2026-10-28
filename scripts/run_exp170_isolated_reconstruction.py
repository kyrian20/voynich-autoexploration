#!/usr/bin/env python3
"""Opt-in EXP-170 modern reconstruction in a disposable workspace.

Never execute the historical simulator in the repository checkout: its
top-level code unconditionally writes data/simulation_results.json.
This runner does NOT establish provenance of the 2026 historical vectors.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from audit_exp170_archive import (
    CONDITIONS, EXP, FROZEN_INPUT_SHA256, parse_archive,
    validate_archive, verify_frozen_inputs,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "naibbe_v2.py": "naibbe_v2.py",
    "references/naibbe_tables.csv": "references/naibbe_tables.csv",
}
DESTINATIONS = {
    "historical_script": EXP / "script.py",
    "voynich": Path("data/transcriptions/eva_zl3b.txt"),
    "english_historical_latin_label": Path("data/reference_corpora/latin/vulgate.txt"),
    "naibbe_code": Path("data/derived/naibbe-cipher/naibbe_v2.py"),
    "naibbe_tables": Path("data/derived/naibbe-cipher/references/naibbe_tables.csv"),
    "italian": Path("data/derived/naibbe-cipher/input/examples/divina_commedia.txt"),
}
OUTPUT_NAME = "simulation_results.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_log_bytes(data):
    """Retain exact captured bytes; string inputs are for synthetic test doubles."""
    if data is None:
        return b""
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    raise TypeError(f"Unsupported subprocess log type: {type(data).__name__}")


def checked_source(path, expected):
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise ValueError("Expected an explicit lowercase SHA-256 for every external input")
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or symlinked input: {path}")
    actual = sha256(path)
    if actual != expected:
        raise ValueError(f"Input SHA-256 mismatch: {path}")
    return actual


def preflight(root, naibbe_dir, italian, hashes, out_dir):
    """Validate all inputs and destination before creating any output."""
    verify_frozen_inputs(root)
    external = {
        "naibbe_code": naibbe_dir / SOURCES["naibbe_v2.py"],
        "naibbe_tables": naibbe_dir / SOURCES["references/naibbe_tables.csv"],
        "italian": italian,
    }
    for name, path in external.items():
        checked_source(path, hashes[name])
    latin = root / DESTINATIONS["english_historical_latin_label"]
    if latin.is_symlink() or not latin.is_file():
        raise ValueError("Missing or symlinked English historical Latin-labelled input")
    # This check is not a historical identity claim; the manifest locks bytes.
    latin_sha = sha256(latin)
    if latin_sha != "d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe":
        raise ValueError("Historical Latin-labelled input does not match frozen corpus")
    target = out_dir.resolve(strict=False)
    if target == root.resolve() or root.resolve() in target.parents:
        raise ValueError("Reconstruction output must be outside the source repository")
    if out_dir.is_symlink() or out_dir.exists():
        raise FileExistsError(f"Refusing existing output destination: {out_dir}")
    if not out_dir.parent.is_dir():
        raise ValueError("Output parent directory must already exist")
    return {"external_sha256": hashes, "historical_sha256": FROZEN_INPUT_SHA256,
            "historical_latin_label_sha256": latin_sha,
            "status": "PREFLIGHT_ONLY", "historical_reproduction": False}


def stage_inputs(stage, root, naibbe_dir, italian, hashes):
    """Copy only required inputs; never stage the historical output JSON."""
    inputs = {
        "historical_script": root / DESTINATIONS["historical_script"],
        "voynich": root / DESTINATIONS["voynich"],
        "english_historical_latin_label": root / DESTINATIONS["english_historical_latin_label"],
        "naibbe_code": naibbe_dir / SOURCES["naibbe_v2.py"],
        "naibbe_tables": naibbe_dir / SOURCES["references/naibbe_tables.csv"],
        "italian": italian,
    }
    for name, source in inputs.items():
        target = stage / DESTINATIONS[name]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    archived = stage / EXP / "data" / OUTPUT_NAME
    if archived.exists():
        raise ValueError("Staged historical output unexpectedly exists")
    archived.parent.mkdir(parents=True, exist_ok=True)
    # Compare staged bytes to the independent preflight locks, not to a
    # source that might have changed after preflight (TOCTOU).
    locked = {
        "historical_script": FROZEN_INPUT_SHA256[str(DESTINATIONS["historical_script"])],
        "voynich": FROZEN_INPUT_SHA256[str(DESTINATIONS["voynich"])],
        "english_historical_latin_label":
            "d63b1b81824e259b1cf92ba8a6e5cbbf783e2a83214cf2c3db2ecd1459165bfe",
        "naibbe_code": hashes["naibbe_code"],
        "naibbe_tables": hashes["naibbe_tables"],
        "italian": hashes["italian"],
    }
    for name in inputs:
        target = stage / DESTINATIONS[name]
        if sha256(target) != locked[name]:
            raise ValueError(f"Staged input SHA-256 mismatch: {name}")
    return archived


def run_reconstruction(root, naibbe_dir, italian, hashes, out_dir, execute=False,
                       timeout=3600):
    # The direct Python API must enforce the same guard as the CLI. Invalid
    # timeouts must not reserve a destination or launch any simulator process.
    if isinstance(timeout, bool) or not isinstance(timeout, int) or timeout < 1:
        raise ValueError("timeout must be a positive integer")
    receipt = preflight(root, naibbe_dir, italian, hashes, out_dir)
    if not execute:
        return receipt
    with tempfile.TemporaryDirectory(prefix="voynich-exp170-reconstruction-") as temp:
        stage = Path(temp)
        staged_output = stage_inputs(stage, root, naibbe_dir, italian, hashes)
        # Reserve the destination atomically before the costly 400-run subprocess.
        # Concurrent callers targeting the same path must fail before simulation.
        out_dir.mkdir(mode=0o700, exist_ok=False)
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        launch_error = None
        try:
            proc = subprocess.run(
                [sys.executable, str(stage / EXP / "script.py")],
                cwd=stage, env=env, capture_output=True,
                timeout=timeout, check=False,
                # Capture bytes first: escaped text cannot distinguish a literal
                # backslash-x sequence from an invalid UTF-8 byte.
            )
            raw_stdout = raw_log_bytes(proc.stdout)
            raw_stderr = raw_log_bytes(proc.stderr)
            returncode = proc.returncode
        except subprocess.TimeoutExpired as exc:
            # Python exposes partial raw bytes on timeout.
            raw_stdout = raw_log_bytes(exc.stdout)
            raw_stderr = raw_log_bytes(exc.stderr)
            returncode = 124
        except OSError as exc:
            raw_stdout = b""
            raw_stderr = b""
            launch_error = f"{type(exc).__name__}: {exc}"
            returncode = 126
        stdout = raw_stdout.decode("utf-8", errors="backslashreplace")
        stderr = raw_stderr.decode("utf-8", errors="backslashreplace")
        if returncode == 124:
            stderr += "\nTIMEOUT"
        if launch_error is not None:
            stderr = launch_error
        receipt["returncode"] = returncode
        receipt["status"] = "FAILED"
        if returncode == 0:
            try:
                if not staged_output.is_file() or staged_output.is_symlink():
                    raise ValueError("Simulator reported success but did not create a regular output")
                raw = staged_output.read_bytes()
                archived = parse_archive(raw.decode("utf-8"))
                frozen = parse_archive((root / EXP / "data" / OUTPUT_NAME).read_text())
                expected_keys = set(frozen["italian_A"][0])
                validate_archive(archived, expected_keys)
                receipt["output_sha256"] = hashlib.sha256(raw).hexdigest()
                receipt["status"] = "MODERN_RECONSTRUCTION_UNVALIDATED"
            except (ValueError, UnicodeError, KeyError, IndexError) as exc:
                receipt["validation_error"] = f"{type(exc).__name__}: {exc}"
                receipt["returncode"] = 65
        # Preserve partial/invalid newly generated output for failure analysis.
        # Quarantine under a non-JSON name; never present it as validated output.
        if receipt["status"] == "FAILED" and (staged_output.exists() or staged_output.is_symlink()):
            if staged_output.is_symlink() or not staged_output.is_file():
                receipt["quarantine_error"] = "Generated output is not a regular file"
            else:
                try:
                    failed_bytes = staged_output.read_bytes()
                    failed_name = "simulation_results.failed.bin"
                    with (out_dir / failed_name).open("xb") as failed:
                        failed.write(failed_bytes)
                    receipt["quarantined_output"] = {
                        "name": failed_name,
                        "sha256": hashlib.sha256(failed_bytes).hexdigest(),
                        "size_bytes": len(failed_bytes),
                        "status": "UNVALIDATED_FAILED_OUTPUT",
                    }
                except OSError as exc:
                    receipt["quarantine_error"] = f"{type(exc).__name__}: {exc}"
        # Destination was reserved before subprocess; publish only into that directory.
        (out_dir / "stdout.bin").write_bytes(raw_stdout)
        (out_dir / "stderr.bin").write_bytes(raw_stderr)
        (out_dir / "stdout.log").write_text(stdout, encoding="utf-8")
        (out_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        receipt["raw_logs"] = {
            "stdout": {"sha256": hashlib.sha256(raw_stdout).hexdigest(),
                       "size_bytes": len(raw_stdout)},
            "stderr": {"sha256": hashlib.sha256(raw_stderr).hexdigest(),
                       "size_bytes": len(raw_stderr)},
        }
        if receipt["status"] == "MODERN_RECONSTRUCTION_UNVALIDATED":
            with (out_dir / OUTPUT_NAME).open("xb") as output:
                output.write(raw)
        (out_dir / "receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
        if receipt["status"] == "FAILED":
            raise RuntimeError(f"Reconstruction failed ({receipt['returncode']}); logs saved in {out_dir}")
        return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--naibbe-dir", required=True, type=Path)
    parser.add_argument("--italian-source", required=True, type=Path)
    parser.add_argument("--naibbe-sha256", required=True)
    parser.add_argument("--tables-sha256", required=True)
    parser.add_argument("--italian-sha256", required=True)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--execute", action="store_true",
                        help="Opt in to 400 NEW simulations; default only verifies inputs")
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    hashes = {"naibbe_code": args.naibbe_sha256,
              "naibbe_tables": args.tables_sha256, "italian": args.italian_sha256}
    result = run_reconstruction(ROOT, args.naibbe_dir, args.italian_source,
                                hashes, args.out_dir, args.execute, args.timeout)
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
