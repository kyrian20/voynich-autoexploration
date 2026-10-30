#!/usr/bin/env python3
"""Non-destructive inventory of IVTFF brace-delimited spans.

This audit does not interpret braces or alter tokenization. Its primary counts
cover brace spans in locus-record bodies, excluding page headers, untagged
prose and inline IVTFF tags. The previous all-non-hash-comment inventory is
retained explicitly as a historical comparison, not overwritten.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path

if __package__:
    from .ivtff_physical_rows import checked_physical_lines
    from .audit_ivtff_page_locus_ids import audit_text as audit_structure, structural_errors
else:
    from ivtff_physical_rows import checked_physical_lines
    from audit_ivtff_page_locus_ids import audit_text as audit_structure, structural_errors

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ("ZL3b", ROOT / "data/transcriptions/eva_zl3b.txt"),
    ("ZL3a", ROOT / "data/transcriptions/zl3a.txt"),
    ("IT2a", ROOT / "data/transcriptions/eva_it2a.txt"),
]


def verified_physical_lines(text: str) -> list[str]:
    """Keep exact source offsets; reject splitlines-only fake separators first."""
    for _ in checked_physical_lines(text):
        pass
    # Now splitlines cannot manufacture rows from U+2028, VT, FF, etc.
    return text.splitlines(keepends=True)


def require_valid_structure(text: str) -> None:
    """Reject malformed page/locus rows before publishing a brace census."""
    errors = structural_errors(audit_structure(text))
    if errors:
        raise ValueError(f"Invalid IVTFF page/locus structure: {errors}")


def audit_text(text: str, sample_limit: int = 20) -> dict:
    """Count brace spans on non-comment lines without interpreting their meaning."""
    spans = []
    unmatched_open = 0
    unmatched_close = 0
    nested_open = 0
    ignored_comment_lines = 0
    absolute_offset = 0

    for line in verified_physical_lines(text):
        if line.lstrip().startswith("#"):
            ignored_comment_lines += 1
            absolute_offset += len(line)
            continue

        # IVTFF 2.0.2 §6.6 requires each ligature to close on the same line.
        # Reset span state for every line so malformed cross-line pairs cannot
        # be accidentally accepted as valid inventory entries.
        start = None
        for local_index, char in enumerate(line):
            index = absolute_offset + local_index
            if char == "{":
                if start is None:
                    start = index
                else:
                    nested_open += 1
            elif char == "}":
                if start is None:
                    unmatched_close += 1
                else:
                    raw = text[start:index + 1]
                    inner = raw[1:-1]
                    spans.append({
                        "offset": start,
                        "length": len(raw),
                        "content": inner,
                        "contains_ascii_letters": any(c.isascii() and c.isalpha() for c in inner),
                        "contains_whitespace": any(c.isspace() for c in inner),
                        "nested_open": "{" in inner,
                    })
                    start = None
        if start is not None:
            unmatched_open += 1
        absolute_offset += len(line)

    content_counts = collections.Counter(span["content"] for span in spans)
    return {
        "ignored_hash_comment_lines": ignored_comment_lines,
        "brace_span_count": len(spans),
        "distinct_contents": len(content_counts),
        "spans_with_ascii_letters": sum(span["contains_ascii_letters"] for span in spans),
        "spans_with_whitespace": sum(span["contains_whitespace"] for span in spans),
        "nested_open_brace_count": nested_open,
        "unmatched_open_brace_count": unmatched_open,
        "unmatched_close_brace_count": unmatched_close,
        "most_common_contents": [
            {"content": content, "count": count}
            for content, count in content_counts.most_common(20)
        ],
        "examples": [
            {k: span[k] for k in ("offset", "length", "content", "contains_ascii_letters")}
            for span in spans[:sample_limit]
        ],
    }



# Restrict the primary inventory to structural locus rows. This deliberately
# follows the folio grammar used by audit_ivtff_page_locus_ids; malformed rows
# belong to that fail-closed structural audit, not to a silently repaired count.
RECORD_PREFIX_RE = re.compile(r"^<f(?:[0-9]+[rv][1-6]?|Ros)\.[0-9]{1,3},[^>]*>(?=[ \t\r\n]|$)")
INLINE_TAG_RE = re.compile(r"<[^>]*>")


def mask_non_record_text(text: str) -> str:
    """Keep locus payload offsets, masking headers, prose and inline IVTFF tags.

    All replacement characters are spaces except line endings. This preserves
    Python-character offsets and line boundaries for audit_text's span report.
    It does not decide the interpretation of braces inside square alternatives.
    """
    output = []
    for line in verified_physical_lines(text):
        prefix = RECORD_PREFIX_RE.match(line)
        if prefix is None:
            output.append("".join(ch if ch in "\r\n" else " " for ch in line))
            continue
        start = prefix.end()
        body = INLINE_TAG_RE.sub(lambda m: " " * len(m.group()), line[start:])
        output.append(" " * start + body)
    masked = "".join(output)
    if len(masked) != len(text):
        raise AssertionError("Mask must preserve character offsets")
    return masked


def main() -> None:
    results = []
    for label, path in FILES:
        if not path.is_file():
            raise FileNotFoundError(f"Required transcription missing; refusing partial audit: {path}")
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        require_valid_structure(text)
        legacy_report = audit_text(text)
        report = audit_text(mask_non_record_text(text))
        results.append({
            "transcription": label,
            "source": str(path.relative_to(ROOT)),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "ignored_hash_comment_lines": legacy_report["ignored_hash_comment_lines"],
            **{k: v for k, v in report.items() if k != "ignored_hash_comment_lines"},
            "excluded_nonrecord_or_inline_tag_spans": (
                legacy_report["brace_span_count"] - report["brace_span_count"]
            ),
            "historical_non_hash_comment_inventory": legacy_report,
        })

    output = {
        "audit": "ivtff_brace_span_inventory",
        "version": 4,
        "purpose": (
            "Count brace-delimited material in structurally valid physical locus rows after masking IVTFF inline tags. "
            "Reject fake Unicode row separators; preserve the prior non-hash-comment inventory separately."
        ),
        "files": results,
        "interpretation_limits": [
            "A brace span containing letters is not by itself proof those letters are lexical tokens.",
            "Brace spans are IVTFF ligature representations under §6.6; their optimal statistical treatment remains an explicit analysis-policy decision.",
            "No historical EXP results are changed or regenerated by this audit.",
            "Counts are descriptive and not a parser-conformance certificate; the structural gate checks page/locus IDs only.",
            "Offsets refer to characters in decoded UTF-8 text, not byte positions.",
        ],
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
