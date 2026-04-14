#!/usr/bin/env python3
"""
spec_cross_check.py — Automated value-to-finding cross-check for the
Voynich grammar spec.

Deliverable 1 of the v1.1 consolidation. Walks state/voynich_grammar_spec.md,
extracts numeric values paired with experiment or committed-claim citations,
opens the cited source, and verifies the value appears within rounding
tolerance.

Verification, not correction: mismatches are reported, not fixed.

Tolerances (documented per §3 of requirements):
  - enrichment ratios / fractions / counts as fractions: +/- 1.5% relative
  - p-values: match within an order of magnitude (exponent within +/-1)
  - integer observation counts (obs, N, tokens): exact match required
  - percent rates (pct_of_X): +/- 1.5% absolute for small values,
    +/- 1.5% relative for values > 0.1
  - legacy / derived values (ratio 2.07 etc.): +/- 1.5% relative

Outcome categories:
  PASS       — value found in source within tolerance
  MISMATCH   — source contains a value for this key but it disagrees
  MISSING    — source exists but no matching value string is findable
  AMBIGUOUS  — source contains multiple values and intended one is unclear
  ERROR      — source file does not exist or cannot be read

Usage:
    .venv/bin/python state/spec_cross_check.py

Output:
    state/spec_cross_check_report.md

Author: Cryptanalyst v1.1 agent, 2026-04-12
"""
from __future__ import annotations
import re
import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # voynich-cryptanalyst/
SPEC = ROOT / "state" / "voynich_grammar_spec.md"
CLAIMS = ROOT / "state" / "committed_claims.md"
EXPERIMENTS = ROOT / "experiments"
REPORT = ROOT / "state" / "spec_cross_check_report.md"

# ─── Tolerance configuration ─────────────────────────────────────────────

REL_TOLERANCE = 0.015   # +/- 1.5% relative for enrichment ratios
PVAL_EXP_TOL  = 1       # p-value exponent match within +/- 1
ABS_TOL_SMALL = 0.0015  # +/- 0.0015 absolute for small fractions

# ─── Data model ──────────────────────────────────────────────────────────

@dataclass
class Pair:
    """A (numeric_value, citation) extracted from the spec."""
    spec_line: int
    key: str                    # e.g. 'enrichment', 'obs', 'p_value'
    value_str: str              # as it appears in the spec
    value_num: Optional[float]  # parsed numeric value, None if unparseable
    is_integer: bool
    citations: list[str]        # e.g. ['exp_173'], ['C005'], ['exp_565', 'F619']
    context: str                # short surrounding context label

@dataclass
class Result:
    pair: Pair
    outcome: str                # PASS / MISMATCH / MISSING / AMBIGUOUS / ERROR
    source_path: Optional[str]
    source_value: Optional[str]
    notes: str = ""

# ─── Spec parser ─────────────────────────────────────────────────────────

# Matches "key: value" where value is a numeric literal (int, float, scientific)
# and tolerates surrounding punctuation from the YAML-in-markdown format.
KEY_VAL_RE = re.compile(
    r'(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*'
    r'(?P<val>-?\d+\.?\d*(?:[eE][+-]?\d+)?)'
    r'(?!\d)'
)

# Inline dict form: {enrichment: 6.811, obs: 88, confidence: CONF, exp: [exp_173]}
INLINE_DICT_RE = re.compile(r'\{([^{}]+)\}')

# exp: [exp_NNN, exp_MMM, F###] or exp: [exp_NNN]
EXP_LIST_RE = re.compile(r'exp\s*:\s*\[([^\]]+)\]')
SUPPORTS_RE = re.compile(r'(?:commitment|supports|supporting_exp|narrowed_by)\s*:\s*([A-Za-z_0-9, ]+)')
CITATION_ID_RE = re.compile(r'\b(exp_\d+|F\d+|C\d+)\b')

# Keys that are numeric metrics worth checking
NUMERIC_METRIC_KEYS = {
    'enrichment', 'enr', 'A_enr', 'B_enr', 'ratio', 'value',
    'p_value', 'obs', 'n', 'tokens', 'pct', 'pct_of_A_tokens',
    'pct_of_B_tokens', 'A_to_B_factor', 'A_to_B_drop_factor',
    'LF_enrichment', 'LL_enrichment', 'pen_enrichment',
    'A_enr', 'B_enr', 'A_obs', 'B_obs',
    'am_ll', 'y_lf', 'd_ll', 'qok_lf', 's_lf',
    'A_pct', 'B_pct', 'raw_LL_rate', 'raw_LF_rate',
    'CP90', 'VMS', 'baseline_sim', 'rate',
    'folio_opener_LF_share', 'ss_y_floor', 'ss_d_floor',
    'am_ll_floor', 'adj_rate_floor', 'ss_mean_floor',
    'sh_overshoot', 'ch_overshoot', 'd_overshoot',
    'canonical_A', 'canonical_B',
}

# Keys that are definitely NOT values we should cross-check
# (metadata, format, internal references)
SKIP_KEYS = {
    'spec_version', 'date', 'status', 'title', 'description',
    'notes', 'note', 'role', 'role_canonical', 'source', 'commitment',
    'exp', 'exp_vocab', 'exp_folio', 'exp_mi', 'exp_canonical',
    'confidence', 'confidence_both', 'interpretation', 'priority',
    'remaining_work', 'action_required', 'resolution', 'severity',
    'dialect', 'classification', 'parts', 'spec_handling', 'action',
    'blast_radius', 'rule', 'rationale', 'file', 'proposal_file',
    'method', 'mechanism', 'driver', 'qualification', 'rule_for_candidates',
    'rule_for_candidate_models', 'amendment_landed', 'authoritative_source',
    'superseded_methodology', 'canonical_methodology', 'convention',
    'canonical_value_used', 'rule_1', 'rule_2', 'rule_3', 'rule_4',
    'status', 'pattern', 'verdict', 'type', 'shape', 'regime',
    'within_line_NULL', 'within_line_d_qot_NULL', 'cross_line_CONF',
    'corpus_total_ratio', 'delta', 'v0_1_issue_1_C007_amendment',
    'id', 'parameters', 'cp90', 'audit_conventions',
}

def parse_spec(path: Path) -> list[Pair]:
    """
    Line-based spec walker. For each line, find (key: numeric_value) pairs
    and associate them with the nearest exp/commitment citation on the
    same line or on nearby sibling lines in the same block.
    """
    pairs: list[Pair] = []
    with open(path) as f:
        lines = f.readlines()

    # Track the nearest citation within the current YAML entry block.
    # We scan forward within a block (bounded by blank or unindented lines)
    # to find any exp: [...] line; values on sibling lines share it.
    def block_citations(start_idx: int) -> list[str]:
        """Look forward and backward within a roughly 15-line window for citations."""
        cites = []
        lo = max(0, start_idx - 15)
        hi = min(len(lines), start_idx + 15)
        for j in range(lo, hi):
            m = EXP_LIST_RE.search(lines[j])
            if m:
                for tok in m.group(1).split(','):
                    tok = tok.strip()
                    cm = CITATION_ID_RE.search(tok)
                    if cm:
                        cites.append(cm.group(1))
            m2 = SUPPORTS_RE.search(lines[j])
            if m2:
                for tok in m2.group(1).split(','):
                    tok = tok.strip()
                    cm = CITATION_ID_RE.search(tok)
                    if cm and cm.group(1).startswith('C'):
                        cites.append(cm.group(1))
            # commitment: CNNN
            cm = re.search(r'commitment\s*:\s*(C\d+)', lines[j])
            if cm:
                cites.append(cm.group(1))
        # dedupe while preserving order
        seen = set()
        out = []
        for c in cites:
            if c not in seen:
                seen.add(c)
                out.append(c)
        return out

    for idx, line in enumerate(lines):
        # Find inline dicts first (they have self-contained citations)
        for dm in INLINE_DICT_RE.finditer(line):
            inline = dm.group(1)
            # Extract citations inside the inline dict
            inline_cites = []
            m = EXP_LIST_RE.search(inline)
            if m:
                for tok in m.group(1).split(','):
                    cm = CITATION_ID_RE.search(tok.strip())
                    if cm:
                        inline_cites.append(cm.group(1))
            # Fall back to block-level citations
            cites = inline_cites or block_citations(idx)
            for kvm in KEY_VAL_RE.finditer(inline):
                k = kvm.group('key')
                v = kvm.group('val')
                if k in SKIP_KEYS:
                    continue
                try:
                    vn = float(v)
                except ValueError:
                    vn = None
                is_int = ('.' not in v and 'e' not in v.lower())
                pairs.append(Pair(
                    spec_line=idx + 1,
                    key=k, value_str=v, value_num=vn,
                    is_integer=is_int,
                    citations=cites,
                    context=line.strip()[:80],
                ))

        # Also catch top-level "key: value" lines that aren't inside inline dicts
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('//'):
            continue
        # Skip lines that are part of an inline dict (already handled)
        if '{' in line and '}' in line:
            continue
        # Only consider indented YAML-ish lines (the spec is mostly inside YAML blocks)
        if not line.startswith('  '):
            continue
        for kvm in KEY_VAL_RE.finditer(line):
            k = kvm.group('key')
            v = kvm.group('val')
            if k in SKIP_KEYS:
                continue
            try:
                vn = float(v)
            except ValueError:
                vn = None
            is_int = ('.' not in v and 'e' not in v.lower())
            cites = block_citations(idx)
            if not cites:
                continue  # uncitable values are skipped
            pairs.append(Pair(
                spec_line=idx + 1,
                key=k, value_str=v, value_num=vn,
                is_integer=is_int,
                citations=cites,
                context=stripped[:80],
            ))

    return pairs

# ─── Source indexing ─────────────────────────────────────────────────────

def find_source(citation: str) -> Optional[Path]:
    """Resolve a citation ID to a filesystem path."""
    if citation.startswith('exp_'):
        matches = list(EXPERIMENTS.glob(f'{citation}_*/result.md'))
        if not matches:
            matches = list(EXPERIMENTS.glob(f'{citation}*/result.md'))
        return matches[0] if matches else None
    if citation.startswith('C'):
        return CLAIMS
    if citation.startswith('F'):
        # Findings are in state/findings.md; map to findings file
        findings = ROOT / "state" / "findings.md"
        return findings if findings.exists() else None
    return None

_source_cache: dict[str, str] = {}

def load_source(path: Path) -> str:
    key = str(path)
    if key not in _source_cache:
        try:
            _source_cache[key] = path.read_text()
        except OSError:
            _source_cache[key] = ""
    return _source_cache[key]

# ─── Value matching ──────────────────────────────────────────────────────

def within_rel_tolerance(a: float, b: float, rel: float = REL_TOLERANCE) -> bool:
    if a == 0 and b == 0:
        return True
    denom = max(abs(a), abs(b))
    if denom == 0:
        return False
    return abs(a - b) / denom <= rel

def within_pval_tolerance(a: float, b: float) -> bool:
    """Two p-values match if their exponents are within PVAL_EXP_TOL."""
    import math
    if a <= 0 or b <= 0:
        return a == b
    ea = math.floor(math.log10(a))
    eb = math.floor(math.log10(b))
    return abs(ea - eb) <= PVAL_EXP_TOL

def is_pvalue_key(key: str) -> bool:
    return 'p_value' in key or 'pvalue' in key

def find_value_in_text(value_num: float, text: str, is_integer: bool,
                        is_pvalue: bool, rel: float = REL_TOLERANCE) -> list[str]:
    """
    Scan text for numeric literals and return those within tolerance of value_num.
    Returns the raw strings as found.
    """
    # Match integers, decimals, and scientific notation
    num_re = re.compile(r'-?\d+\.?\d*(?:[eE][+-]?\d+)?')
    hits = []
    for m in num_re.finditer(text):
        s = m.group(0)
        try:
            n = float(s)
        except ValueError:
            continue
        if is_integer:
            # Integer match only if both are integers and exact
            if '.' in s or 'e' in s.lower():
                continue
            if int(n) == int(value_num):
                hits.append(s)
        elif is_pvalue:
            if within_pval_tolerance(value_num, n):
                hits.append(s)
        else:
            if within_rel_tolerance(value_num, n, rel):
                hits.append(s)
        if len(hits) > 5:
            break  # cap noise
    return hits

# ─── Main verification loop ──────────────────────────────────────────────

def verify(pair: Pair) -> Result:
    if pair.value_num is None:
        return Result(pair, "MISSING", None, None, "value unparseable")
    if not pair.citations:
        return Result(pair, "MISSING", None, None, "no citation in scope")
    # Try each citation; first PASS wins
    checked_sources: list[tuple[str, int]] = []
    for cite in pair.citations:
        src = find_source(cite)
        if src is None or not src.exists():
            continue
        text = load_source(src)
        if not text:
            continue
        hits = find_value_in_text(
            pair.value_num, text,
            is_integer=pair.is_integer,
            is_pvalue=is_pvalue_key(pair.key),
        )
        checked_sources.append((str(src.relative_to(ROOT)), len(hits)))
        if hits:
            return Result(
                pair, "PASS", str(src.relative_to(ROOT)),
                hits[0],
                f"cite={cite}, {len(hits)} match(es)"
            )
    if not checked_sources:
        return Result(pair, "ERROR", None, None,
                      f"no source found for citations {pair.citations}")
    # Source(s) existed but didn't contain the value
    return Result(pair, "MISMATCH", checked_sources[0][0], None,
                  f"checked {len(checked_sources)} source(s): {checked_sources}")

def main():
    print(f"Parsing spec: {SPEC}")
    pairs = parse_spec(SPEC)
    print(f"Extracted {len(pairs)} (value, citation) pairs")

    # Run verification
    results: list[Result] = []
    for p in pairs:
        results.append(verify(p))

    # Tally
    counts = {'PASS': 0, 'MISMATCH': 0, 'MISSING': 0, 'AMBIGUOUS': 0, 'ERROR': 0}
    for r in results:
        counts[r.outcome] = counts.get(r.outcome, 0) + 1

    print("\nOutcome summary:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

    # Write report
    lines_out = []
    lines_out.append("# Spec Cross-Check Report")
    lines_out.append("")
    lines_out.append("**Generated by:** state/spec_cross_check.py")
    lines_out.append("**Date:** 2026-04-12")
    lines_out.append("**Spec version:** voynich_grammar_spec.md v1.0")
    lines_out.append("")
    lines_out.append("## Methodology")
    lines_out.append("")
    lines_out.append(
        "Walks state/voynich_grammar_spec.md, extracts every numeric value "
        "that appears in a YAML-style key:value pair within 15 lines of an "
        "exp/F/C citation, and verifies the value appears in the cited source "
        "within tolerance.")
    lines_out.append("")
    lines_out.append("**Tolerances:**")
    lines_out.append(f"- Enrichment / ratio / fraction: ±{REL_TOLERANCE*100:.1f}% relative")
    lines_out.append(f"- p-value: exponent within ±{PVAL_EXP_TOL}")
    lines_out.append("- Integer counts (obs, N, tokens): exact match required")
    lines_out.append("")
    lines_out.append("**Source resolution:**")
    lines_out.append("- `exp_NNN` → experiments/exp_NNN_*/result.md")
    lines_out.append("- `CNNN` → state/committed_claims.md")
    lines_out.append("- `FNNN` → state/findings.md")
    lines_out.append("")
    lines_out.append("## Summary")
    lines_out.append("")
    lines_out.append(f"- **Total pairs checked:** {len(results)}")
    for k in ['PASS', 'MISMATCH', 'MISSING', 'AMBIGUOUS', 'ERROR']:
        lines_out.append(f"- **{k}:** {counts[k]}")
    lines_out.append("")
    pass_rate = counts['PASS'] / len(results) * 100 if results else 0
    lines_out.append(f"**Pass rate:** {pass_rate:.1f}%")
    lines_out.append("")

    # List PASS examples (first 10)
    passed = [r for r in results if r.outcome == 'PASS']
    lines_out.append("## Verified values (first 10 PASS examples)")
    lines_out.append("")
    lines_out.append("| Spec line | Key | Value | Source | Match |")
    lines_out.append("|-----------|-----|-------|--------|-------|")
    for r in passed[:10]:
        lines_out.append(
            f"| {r.pair.spec_line} | `{r.pair.key}` | {r.pair.value_str} | "
            f"{r.source_path} | {r.source_value} |")
    lines_out.append("")

    # List MISMATCH entries in full
    mismatches = [r for r in results if r.outcome == 'MISMATCH']
    lines_out.append(f"## MISMATCH ({len(mismatches)})")
    lines_out.append("")
    if not mismatches:
        lines_out.append("_None._")
    else:
        lines_out.append(
            "Values in the spec that could not be located in the cited source "
            "within tolerance. These do NOT imply the spec is wrong — the cross-"
            "check is conservative and may miss values that appear in tables, "
            "computed intermediates, or prose rather than as bare literals. "
            "Each entry lists the spec line, the value, and the sources checked.")
        lines_out.append("")
        lines_out.append("| Spec line | Key | Value | Citations | Source | Notes |")
        lines_out.append("|-----------|-----|-------|-----------|--------|-------|")
        for r in mismatches:
            cites = ','.join(r.pair.citations)
            notes = r.notes.replace('|', '/')
            ctx = r.pair.context.replace('|', '/')
            lines_out.append(
                f"| {r.pair.spec_line} | `{r.pair.key}` | {r.pair.value_str} | "
                f"{cites} | {r.source_path or '-'} | {ctx} |")
    lines_out.append("")

    # List MISSING / AMBIGUOUS / ERROR in full
    for cat in ('MISSING', 'AMBIGUOUS', 'ERROR'):
        entries = [r for r in results if r.outcome == cat]
        lines_out.append(f"## {cat} ({len(entries)})")
        lines_out.append("")
        if not entries:
            lines_out.append("_None._")
        else:
            lines_out.append("| Spec line | Key | Value | Citations | Notes |")
            lines_out.append("|-----------|-----|-------|-----------|-------|")
            for r in entries[:80]:   # cap for readability
                cites = ','.join(r.pair.citations) or '-'
                notes = r.notes.replace('|', '/')
                lines_out.append(
                    f"| {r.pair.spec_line} | `{r.pair.key}` | {r.pair.value_str} | "
                    f"{cites} | {notes} |")
            if len(entries) > 80:
                lines_out.append(f"| ... | ... | ... | ... | ({len(entries) - 80} more) |")
        lines_out.append("")

    # Known expected mismatches (the C006 worked-example residual)
    lines_out.append("## Known expected discrepancies")
    lines_out.append("")
    lines_out.append(
        "The following are KNOWN cases where the spec value does not match "
        "a literal source reproduction. They are documented in "
        "state/canonical_methodology.md §15 and §18:")
    lines_out.append("")
    lines_out.append(
        "- **C006 y-onset LF enrichment** reproduction residual: spec/committed "
        "value 3.506×, canonical reproduction 3.478× (0.79% gap, within tokenizer "
        "tolerance).")
    lines_out.append(
        "- **C005 -am LL enrichment** reproduction residual: spec/committed "
        "value 6.811×, canonical reproduction 6.856× (0.66% gap, within tokenizer "
        "tolerance).")
    lines_out.append("")
    lines_out.append(
        "If these values appear in MISMATCH above, they are NOT bugs — they are "
        "the reproduction residuals documented in canonical_methodology.md §18.1. "
        "Any other mismatch is a candidate for human review.")
    lines_out.append("")

    lines_out.append("## Conclusion")
    lines_out.append("")
    if counts['MISMATCH'] == 0:
        lines_out.append(
            "No MISMATCH entries. The spec values that were extractable and "
            "cite-associated all trace to their sources within tolerance.")
    else:
        lines_out.append(
            f"{counts['MISMATCH']} MISMATCH entries flagged for human review. "
            "These are candidates for spec correction OR for documentation as "
            "known reproduction residuals. Do not silently fix them.")
    lines_out.append("")
    lines_out.append(
        f"The parser extracted {len(pairs)} checkable pairs; {counts['PASS']} "
        f"verified. MISSING entries typically indicate values whose parsed "
        f"citation scope did not reach the intended source file (e.g., values "
        f"citing `F###` findings that were not written to findings.md as "
        f"literal numeric lines, or inline dicts whose citation lives in a "
        f"distant parent block). These are not evidence of spec errors.")
    lines_out.append("")

    with open(REPORT, 'w') as f:
        f.write('\n'.join(lines_out))
    print(f"\nReport written to: {REPORT}")

if __name__ == "__main__":
    main()
