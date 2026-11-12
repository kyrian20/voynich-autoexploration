#!/usr/bin/env python3
"""Check the IVTFF file-level minimums used by the repository corpora.

This is a narrow file-structure audit, not a complete IVTFF validator. It checks
ASCII bytes, physical line endings, the 2048-character line limit, and the
18-character file-header fields defined in IVTFF 2.0.2, §§5.1 and 6.1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CORPORA = (
    "data/transcriptions/eva_zl3b.txt",
    "data/transcriptions/zl3a.txt",
    "data/transcriptions/eva_it2a.txt",
)
MAX_LINE_CHARS = 2048
HEADER_RE = re.compile(rb"^#=IVTFF [!-~]{4} [0-9]\.[0-9] [MDA]")


def physical_lines(raw: bytes) -> tuple[list[bytes], list[int]]:
    """Split only on CR, LF, and CRLF; report any other control byte later."""
    lines: list[bytes] = []
    endings: list[int] = []
    start = 0
    i = 0
    while i < len(raw):
        if raw[i] == 13:
            lines.append(raw[start:i])
            if i + 1 < len(raw) and raw[i + 1] == 10:
                endings.append(2)
                i += 2
            else:
                endings.append(1)
                i += 1
            start = i
        elif raw[i] == 10:
            lines.append(raw[start:i])
            endings.append(1)
            i += 1
            start = i
        else:
            i += 1
    if start < len(raw):
        lines.append(raw[start:])
    elif not lines:
        lines.append(b"")
    return lines, endings


def audit_bytes(raw: bytes, *, source: str = "<bytes>") -> dict:
    lines, endings = physical_lines(raw)
    errors: list[dict] = []
    for line_no, line in enumerate(lines, 1):
        if len(line) > MAX_LINE_CHARS:
            errors.append({"code": "line_too_long", "line": line_no,
                           "length": len(line), "maximum": MAX_LINE_CHARS})
        # Record the first occurrence of each independent byte-error class.
        # Stopping after the first malformed byte concealed a second class on
        # the same physical line (e.g. a UTF-8 byte followed by a TAB).
        seen_non_ascii = False
        seen_control = False
        for offset, byte in enumerate(line):
            if byte > 127 and not seen_non_ascii:
                errors.append({"code": "non_ascii_byte", "line": line_no,
                               "column": offset + 1, "value": byte})
                seen_non_ascii = True
            elif (byte < 32 or byte == 127) and not seen_control:
                errors.append({"code": "control_byte_in_line", "line": line_no,
                               "column": offset + 1, "value": byte})
                seen_control = True
            if seen_non_ascii and seen_control:
                break
    header = lines[0] if lines else b""
    if len(header) < 18:
        errors.append({"code": "file_header_too_short", "length": len(header), "minimum": 18})
    elif not HEADER_RE.match(header):
        errors.append({"code": "invalid_file_header", "prefix": header[:18].decode("ascii", "replace")})
    return {
        "source": source,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "physical_line_count": len(lines),
        "maximum_line_chars": max((len(line) for line in lines), default=0),
        "line_ending_counts": {
            "lf_or_cr": sum(n == 1 for n in endings),
            "crlf": sum(n == 2 for n in endings),
        },
        "header_prefix": header[:18].decode("ascii", "replace"),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }


def audit_path(path: Path) -> dict:
    try:
        label = str(path.relative_to(ROOT))
    except ValueError:
        label = str(path)
    return audit_bytes(path.read_bytes(), source=label)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Write the JSON receipt to this path")
    parser.add_argument("paths", nargs="*", help="Files to audit (defaults to the three canonical corpora)")
    args = parser.parse_args()
    paths = [
        Path(p) if Path(p).is_absolute() else ROOT / Path(p)
        for p in args.paths
    ] if args.paths else [ROOT / p for p in CORPORA]
    # Never allow a JSON receipt to overwrite a source transcription. Resolve
    # aliases and symlinks before reading or writing any file.
    if args.out is not None:
        output = args.out.resolve()
        # Path.resolve catches symlinks, but not hard links to the same inode.
        # An existing hard-linked output would truncate the input on write.
        if any(path.resolve() == output or
               (args.out.exists() and path.exists() and
                args.out.samefile(path)) for path in paths):
            print("Refusing --out: receipt path aliases an input corpus", file=sys.stderr)
            return 2
    reports = []
    for path in paths:
        try:
            reports.append(audit_path(path))
        except OSError as exc:
            reports.append({"source": str(path), "status": "FAIL",
                            "errors": [{"code": "read_error", "message": str(exc)}]})
    result = {"audit": "IVTFF file-level minimums", "standard": "IVTFF issue 2.0.2",
              "scope": ["ASCII bytes", "physical CR/LF line endings", "2048-character line limit",
                        "18-character file header"], "files": reports,
              "status": "PASS" if reports and all(r["status"] == "PASS" for r in reports) else "FAIL"}
    rendered = json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    if args.out:
        # Atomic replacement avoids mutating an unrelated file that happens
        # to share the receipt destination's inode through a hard link.
        temporary = None
        cleanup_failed = False
        try:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="\n",
                dir=args.out.parent, prefix=".ivtff-receipt-",
                suffix=".tmp", delete=False,
            ) as stream:
                temporary = Path(stream.name)
                stream.write(rendered)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, args.out)
        except OSError as exc:
            print(f"Cannot write IVTFF receipt: {exc}", file=sys.stderr)
            return 2
        finally:
            if temporary is not None:
                try:
                    temporary.unlink(missing_ok=True)
                except OSError as exc:
                    # Cleanup failure must not mask the primary write error.
                    # Surface the leaked temporary path for manual recovery.
                    print(f"Cannot remove temporary IVTFF receipt {temporary}: {exc}",
                          file=sys.stderr)
                    cleanup_failed = True
        if cleanup_failed:
            # A leaked receipt can expose content and requires manual recovery.
            # Do not report successful completion when cleanup has failed.
            return 2
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
