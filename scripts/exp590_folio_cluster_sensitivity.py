#!/usr/bin/env python3
"""Folio-clustered descriptive sensitivity analysis for exact EVA token daiin."""
from __future__ import annotations
import hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata import parse_currier_language

SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
OUT = ROOT / "research/experiments"
HEADER = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))>\s*(.*)$")
TEXT_LINE = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),[^>]*>\s*(.*)$")
TOKEN = re.compile(r"[a-z]+")
TARGET = "daiin"
BOOTSTRAP_N = 20_000
BOOTSTRAP_SEED = 20261022


def analyze_text(text: str) -> dict:
    currier_by_folio = {}
    rows = text.splitlines()
    for row in rows:
        match = HEADER.match(row)
        if match:
            language = parse_currier_language(match.group(2))
            if language:
                currier_by_folio[match.group(1)] = language
    folios = {}
    parsed_lines = 0
    for row in rows:
        match = TEXT_LINE.match(row)
        if not match:
            continue
        folio, _line_number, body = match.groups()
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]", " ", body).lower()
        tokens = TOKEN.findall(body)
        if not tokens:
            continue
        parsed_lines += 1
        stats = folios.setdefault(folio, {
            "folio": folio, "currier": currier_by_folio.get(folio, "unknown"),
            "lines": 0, "tokens": 0, "target_occurrences": 0,
            "lines_containing_target": 0, "target_bearing_lines_starting_target": 0,
            "target_bearing_lines_ending_target": 0,
        })
        n_target = tokens.count(TARGET)
        stats["lines"] += 1
        stats["tokens"] += len(tokens)
        stats["target_occurrences"] += n_target
        stats["lines_containing_target"] += int(n_target > 0)
        stats["target_bearing_lines_starting_target"] += int(n_target > 0 and tokens[0] == TARGET)
        stats["target_bearing_lines_ending_target"] += int(n_target > 0 and tokens[-1] == TARGET)
    return {"parsed_lines": parsed_lines, "folios": list(folios.values())}


def lcg_random(seed: int):
    state = seed & 0xFFFFFFFF
    while True:
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        yield state / 4294967296


def bootstrap_difference(a: list[float], b: list[float], n: int = BOOTSTRAP_N,
                         seed: int = BOOTSTRAP_SEED) -> dict:
    if not a or not b:
        raise ValueError("Both Currier classes need folios containing daiin.")
    observed = sum(a) / len(a) - sum(b) / len(b)
    random_values = lcg_random(seed)
    differences = []
    for _ in range(n):
        mean_a = sum(a[min(int(next(random_values) * len(a)), len(a) - 1)]
                     for _ in range(len(a))) / len(a)
        mean_b = sum(b[min(int(next(random_values) * len(b)), len(b) - 1)]
                     for _ in range(len(b))) / len(b)
        differences.append(mean_a - mean_b)
    differences.sort()
    return {
        "estimand": "unweighted mean across folios with daiin-bearing lines of the share of those lines starting with daiin",
        "difference_A_minus_B": observed,
        "percentile_95_ci": [differences[int(0.025 * n)], differences[int(0.975 * n)]],
        "folios_A": len(a), "folios_B": len(b),
        "bootstrap_replicates": n, "seed": seed,
    }


def build_result(raw: bytes) -> dict:
    parsed = analyze_text(raw.decode("utf-8-sig"))
    folios = parsed["folios"]
    result = {
        "title": "Folio-level descriptive sensitivity for daiin",
        "date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "tokenization": "lowercase ASCII alphabetic runs after removing IVTFF tags, brace spans and square-bracket spans; exact token daiin only",
        "parsed_lines": parsed["parsed_lines"], "folio_count": len(folios),
        "classes": {}, "bootstrap": None,
        "interpretation": "Exploratory descriptive comparison, not a decipherment claim. Folios are resampled as clusters; alternative transcriptions are not independent samples.",
        "limitations": [
            "Token counts depend on the declared simplified tokenization policy.",
            "Currier class is read exclusively from IVTFF $L; missing labels remain unknown.",
            "Only folios with at least one line containing exact daiin enter the unweighted folio-rate comparison.",
            "The interval is a percentile bootstrap interval for a descriptive difference, not a causal or linguistic proof.",
            "No correction is made for prior exploratory selection of daiin among candidate tokens.",
            "ZL3a, ZL3b and IT2a are alternative transcriptions of the same manuscript, not independent samples.",
        ],
    }
    for cls in ("A", "B", "unknown"):
        group = [f for f in folios if f["currier"] == cls]
        target_lines = [f for f in group if f["lines_containing_target"] > 0]
        occurrences = sum(f["target_occurrences"] for f in group)
        bearing_lines = sum(f["lines_containing_target"] for f in group)
        initial_lines = sum(f["target_bearing_lines_starting_target"] for f in group)
        final_lines = sum(f["target_bearing_lines_ending_target"] for f in group)
        rates = [f["target_bearing_lines_starting_target"] / f["lines_containing_target"] for f in target_lines]
        result["classes"][cls] = {
            "folios": len(group), "folios_with_daiin": len(target_lines),
            "parsed_lines": sum(f["lines"] for f in group),
            "target_occurrences": occurrences, "lines_containing_daiin": bearing_lines,
            "target_bearing_lines_starting_daiin": initial_lines,
            "target_bearing_lines_ending_daiin": final_lines,
            "initial_share_among_daiin_bearing_lines": initial_lines / bearing_lines if bearing_lines else None,
            "final_share_among_daiin_bearing_lines": final_lines / bearing_lines if bearing_lines else None,
            "unweighted_mean_folio_initial_share": sum(rates) / len(rates) if rates else None,
        }
    rate_a = [f["target_bearing_lines_starting_target"] / f["lines_containing_target"] for f in folios if f["currier"] == "A" and f["lines_containing_target"] > 0]
    rate_b = [f["target_bearing_lines_starting_target"] / f["lines_containing_target"] for f in folios if f["currier"] == "B" and f["lines_containing_target"] > 0]
    result["bootstrap"] = bootstrap_difference(rate_a, rate_b)
    return result


def render_report(result: dict) -> str:
    c, b = result["classes"], result["bootstrap"]
    lines = [
        "# Folio-level sensitivity analysis for exact token daiin", "",
        f"- Date UTC: {result['date_utc']}",
        f"- Source: {result['source']}",
        f"- Source SHA-256: {result['source_sha256']}",
        f"- Parsed text lines: {result['parsed_lines']:,}",
        f"- Folios with parsed text: {result['folio_count']}", "",
        "## Class-level counts", "",
        "| Currier | Folios | Folios with daiin | Lines | Exact occurrences | Lines containing daiin | Such lines starting daiin | Such lines ending daiin | Start share |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for cls in ("A", "B", "unknown"):
        x = c[cls]
        lines.append(f"| {cls} | {x['folios']} | {x['folios_with_daiin']} | {x['parsed_lines']} | {x['target_occurrences']} | {x['lines_containing_daiin']} | {x['target_bearing_lines_starting_daiin']} | {x['target_bearing_lines_ending_daiin']} | {x['initial_share_among_daiin_bearing_lines']:.4f} |")
    lines += [
        "", "## Folio-cluster bootstrap: Currier A minus Currier B", "",
        f"- Difference in unweighted mean folio rate: {b['difference_A_minus_B']:.6f}",
        f"- Percentile 95% interval: [{b['percentile_95_ci'][0]:.6f}, {b['percentile_95_ci'][1]:.6f}]",
        f"- Folios containing daiin: A={b['folios_A']}, B={b['folios_B']}",
        f"- Replicates / seed: {b['bootstrap_replicates']} / {b['seed']}", "",
        "Per-folio rate = lines containing exact daiin that start with daiin divided by all lines containing exact daiin. Folios are resampled independently within A and B; the comparison uses unweighted mean folio rates.",
        "", "## Interpretation and limitations", "", result["interpretation"], "",
    ]
    lines += [f"- {item}" for item in result["limitations"]]
    lines += ["", "This is a sensitivity analysis, not a new EXP identifier. It does not overwrite the EXP-590 baseline and is not a confirmatory test.", ""]
    return "\n".join(lines)


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing transcription: {SOURCE}")
    result = build_result(SOURCE.read_bytes())
    OUT.mkdir(parents=True, exist_ok=True)
    stem = f"{result['date_utc']}-daiin-folio-cluster-sensitivity"
    (OUT / f"{stem}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / f"{stem}.md").write_text(render_report(result), encoding="utf-8")
    print(json.dumps({"report": f"research/experiments/{stem}.md", "json": f"research/experiments/{stem}.json", "source_sha256": result["source_sha256"], "classes": result["classes"], "bootstrap": result["bootstrap"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
