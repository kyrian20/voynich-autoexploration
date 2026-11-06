#!/usr/bin/env python3
"""Reconcile historical and corrected line-boundary token populations.

The baseline reader is copied from commit 76717eff613c3235526a3e9097a581149fca5e1b.
The corrected reader is imported from the neighboring analysis directory.
This is a deterministic count audit; it does not fit or score a predictor.
"""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[2]
CORPUS = REPO_ROOT / "data/transcriptions/eva_zl3b.txt"
EXPECTED_CORPUS_SHA256 = "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc"
EXPECTED_CURRENT_READER_SHA256 = "97e5cbc0f63cf3ca52fc555334e595d6f24d94a425e549c0c125d00f5d016059"
BASELINE_COMMIT = "76717eff613c3235526a3e9097a581149fca5e1b"
CURRENT_READER_COMMIT = "60d0bdb64931f1659c5f662a31d7471dbef5058f"

HISTORICAL_SNAPSHOTS = [
    {"stage":"legacy_initial","commit":"76717eff613c3235526a3e9097a581149fca5e1b","reader_git_blob":"d04a1f943499b3cc0cec24a34abf0aed696c0577","tokens":35318,"candidates":35111,"positives":3923,"heldout_candidates":6229,"heldout_positives":719},
    {"stage":"unknown_glyph_barrier","commit":"3b708ae620c28991817d2ff25c909ac8f3208ec7","reader_git_blob":"ace8602e8c8f2d96948199d17be913db8cb7384f","tokens":35187,"candidates":34885,"positives":3892,"heldout_candidates":6210,"heldout_positives":714},
    {"stage":"brace_ligature_quarantine","commit":"2f09be288f9b1133c121a179b21bb25cec84783a","reader_git_blob":"a7c1f3818bb7b4760b5890e7d757b292885d6df6","tokens":34632,"candidates":33977,"positives":3809,"heldout_candidates":6049,"heldout_positives":701},
    {"stage":"high_ascii_barrier","commit":"147717da1975b5f70a91ce8a3f23ea2684b15ba4","reader_git_blob":"c67af601233f87f576dceedbe983800f2ce540bc","tokens":34553,"candidates":33841,"positives":3780,"heldout_candidates":6017,"heldout_positives":696},
    {"stage":"interposed_non_p_loci","commit":"2bc8a80bba447c8fbf2b855f916117bf33c8e546","reader_git_blob":"d604768de1eaf385b12231ba8077ff3401252d03","tokens":34553,"candidates":33770,"positives":3709,"heldout_candidates":6004,"heldout_positives":683},
    {"stage":"paragraph_markers","commit":"01921a61a7939f4562260b9097e553176a8bf3d9","reader_git_blob":"acb3009a1c06fdd2872b1a960994fdc04500bbcd","tokens":34553,"candidates":33293,"positives":3232,"heldout_candidates":5913,"heldout_positives":592},
    {"stage":"unsupported_symbol_barrier","commit":"560c464fc7cc0715f92647cdbb677abc6cee6cdc","reader_git_blob":"e60587e3cf7572e77886cca5090c8f02e1ac65d6","tokens":34509,"candidates":33229,"positives":3223,"heldout_candidates":5905,"heldout_positives":592},
    {"stage":"uncertain_comma_quarantine","commit":"8e553e823fc5c929345b05573195617a3029682f","reader_git_blob":"d1e5fcbe4cd8c433ee8f043d5e6bda4d722e481c","tokens":29906,"candidates":26824,"positives":2554,"heldout_candidates":4792,"heldout_positives":468},
    {"stage":"final_reader","commit":"60d0bdb64931f1659c5f662a31d7471dbef5058f","reader_git_blob":"8d3773334852fa0433cb155633e2f7060d9afb53","tokens":29906,"candidates":26824,"positives":2554,"heldout_candidates":4792,"heldout_positives":468}
]
TOKEN_RULE_DELTAS = [
    {"rule":"question_mark_and_unknown_glyph_barriers","tokens":-131,"candidates":-226,"positives":-31},
    {"rule":"brace_ligature_quarantine","tokens":-555,"candidates":-908,"positives":-83},
    {"rule":"high_ascii_glyph_code_barrier","tokens":-79,"candidates":-136,"positives":-29},
    {"rule":"unsupported_inline_symbol_barrier","tokens":-44,"candidates":-64,"positives":-9},
    {"rule":"uncertain_comma_quarantine","tokens":-4603,"candidates":-6405,"positives":-669}
]
CANDIDATE_ONLY_DELTAS = [
    {"rule":"interposed_non_p_locus_barrier","tokens":0,"candidates":-71,"positives":-71},
    {"rule":"paragraph_marker_barriers","tokens":0,"candidates":-477,"positives":-477}
]
TRANSIENT_BRACE_REGEX = {
    "buggy_commit":"9acca7185c058d731d096835b6fa51e874752e3e",
    "buggy_reader_git_blob":"6204cd3337eba184c2551d132f054a4e02f4c2b6",
    "buggy_tokens":27510,
    "buggy_candidates":24744,
    "buggy_positives":2199,
    "repair_commit":"e94994afd18f0add3403743a9ae5eabf73025629",
    "repair_reader_git_blob":"536f31a7ce90c0d26b520fc6e07842bb0cf2fe64",
    "restored_tokens":29906,
    "restored_candidates":26824,
    "restored_positives":2554,
    "interpretation":"Transient literal-brace-regex defect; excluded from the stable decomposition."
}

# Exact legacy tokenization and P-row selection from BASELINE_COMMIT.
ROW = re.compile(r"^<(?P<ident>[^>]+)>\s+(?P<body>.*)$")
UNCERTAIN = re.compile(r"\{[^}]*\}|\?")


def legacy_tokens(body: str, policy: str = "primary") -> list[str]:
    body = re.sub(r"<![^>]*>", " ", body)
    body = re.sub(r"<[^>]*>", " ", body)
    body = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", body)
    body = re.sub(r"\[([^\]]*)\]", r"\1", body)
    out: list[str] = []
    for item in re.split(r"[.\s,]+", body):
        if not item or (policy == "drop_uncertain_word" and UNCERTAIN.search(item)):
            continue
        item = re.sub(r"\{[^}]*\}", " ", item)
        item = re.sub(r"@\d+;?", " ", item)
        out.extend(word.lower() for word in re.findall(r"[A-Za-z]+", item))
    return out


def legacy_parse(path: Path) -> dict[str, list[dict[str, object]]]:
    pages: dict[str, list[dict[str, object]]] = collections.defaultdict(list)
    for lineno, raw in enumerate(path.read_text(encoding="latin-1").splitlines(), 1):
        match = ROW.match(raw.strip())
        if not match or "," not in match["ident"]:
            continue
        ident, locus = match["ident"].split(",", 1)
        parts = ident.split(".")
        if len(parts) < 2:
            continue
        page = parts[0]
        page_match = re.fullmatch(r"f(\d+)[rv][1-6]?", page)
        locus_code = re.sub(r"^[+*@=~&!/]+", "", locus.strip())
        if (not page_match and page != "fRos") or not re.fullmatch(r"P(?:0|1|b|c|r|t)", locus_code):
            continue
        words = legacy_tokens(match["body"])
        if words:
            pages[page].append({"words": words, "line": lineno})
    return dict(pages)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def token_count(pages: dict[str, list[dict[str, object]]]) -> int:
    return sum(
        sum(word is not None for word in row["words"])
        for rows in pages.values()
        for row in rows
    )


def line_count(pages: dict[str, list[dict[str, object]]]) -> int:
    return sum(len(rows) for rows in pages.values())


def load_current_reader():
    path = REPO_ROOT / "research/analysis/2026-10-28-line-boundary-reproduction/line_boundary_replication.py"
    actual = digest(path)
    if actual != EXPECTED_CURRENT_READER_SHA256:
        raise SystemExit(f"current reader SHA-256 mismatch: {actual}")
    sys.path.insert(0, str(REPO_ROOT))
    spec = importlib.util.spec_from_file_location("line_boundary_replication", path)
    if spec is None or spec.loader is None:
        raise SystemExit("could not load the current line-boundary reader")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, actual


def main() -> None:
    source_sha = digest(CORPUS)
    if source_sha != EXPECTED_CORPUS_SHA256:
        raise SystemExit(f"ZL3b SHA-256 mismatch: {source_sha}")
    current, current_sha = load_current_reader()
    baseline = legacy_parse(CORPUS)
    old_tokens = token_count(baseline)
    old_lines = line_count(baseline)
    matrix: dict[str, dict[str, int]] = {}
    for comma_policy in ("quarantine", "split"):
        for ligature_policy in ("quarantine", "expand_ascii"):
            pages = current.parse(
                CORPUS,
                "primary",
                uncertain_space_policy=comma_policy,
                ligature_policy=ligature_policy,
            )
            pnames = sorted(pages)
            all_candidates = current.candidates(pages, pnames)
            heldout_pages = set(pnames[::5])
            train = [r for r in all_candidates if r["page"] not in heldout_pages]
            test = [r for r in all_candidates if r["page"] in heldout_pages]
            train, test, duplicate_lines = current.embargo(train, test)
            matrix[f"{comma_policy}+{ligature_policy}"] = {
                "lines": line_count(pages),
                "tokens": token_count(pages),
                "pages": len(pages),
                "candidates": len(all_candidates),
                "positive_candidates": sum(r["y"] for r in all_candidates),
                "every_fifth_page_candidates_after_embargo": len(test),
                "every_fifth_page_positives_after_embargo": sum(r["y"] for r in test),
                "duplicate_line_texts_embargoed": duplicate_lines,
            }
    if old_tokens != 35318 or old_lines != 4130:
        raise SystemExit(f"legacy baseline mismatch: tokens={old_tokens}, lines={old_lines}")
    if any(v["lines"] != 4130 or v["pages"] != 207 for v in matrix.values()):
        raise SystemExit("line/page population changed across reader sensitivity views")
    q = matrix["quarantine+quarantine"]["tokens"]
    q_expand = matrix["quarantine+expand_ascii"]["tokens"]
    split = matrix["split+quarantine"]["tokens"]
    split_expand = matrix["split+expand_ascii"]["tokens"]
    sensitivity = {
        "current_default_tokens": q,
        "comma_split_tokens": split,
        "ascii_ligature_expansion_with_comma_quarantine": q_expand,
        "ascii_ligature_expansion_with_comma_split": split_expand,
        "comma_policy_effect_at_quarantined_ligatures": split - q,
        "ascii_ligature_effect_with_comma_quarantine": q_expand - q,
        "comma_ligature_interaction": (split_expand - split) - (q_expand - q),
        "legacy_minus_comma_split_ascii_expansion_counterfactual": old_tokens - split_expand,
    }
    accounted_tokens = sum(x["tokens"] for x in TOKEN_RULE_DELTAS)
    accounted_candidates = sum(x["candidates"] for x in TOKEN_RULE_DELTAS + CANDIDATE_ONLY_DELTAS)
    accounted_positives = sum(x["positives"] for x in TOKEN_RULE_DELTAS + CANDIDATE_ONLY_DELTAS)
    if accounted_tokens != -5412 or old_tokens + accounted_tokens != q:
        raise SystemExit("sequential reader-rule decomposition does not reconcile the default population")
    if accounted_candidates != -8287 or accounted_positives != -1369:
        raise SystemExit("sequential candidate-population decomposition does not reconcile")
    if (split - q, q_expand - q, split_expand - split, old_tokens - split_expand) != (4603, 252, 271, 538):
        raise SystemExit("counterfactual sensitivity matrix changed unexpectedly")
    if matrix["quarantine+quarantine"]["candidates"] != 26824 or matrix["quarantine+quarantine"]["positive_candidates"] != 2554:
        raise SystemExit("current default candidate population changed unexpectedly")
    result = {
        "audit_type": "deterministic population reconciliation; no predictor fitting or scoring",
        "baseline_commit": BASELINE_COMMIT,
        "current_reader_commit": CURRENT_READER_COMMIT,
        "current_reader_sha256": current_sha,
        "corpus": {"path": "data/transcriptions/eva_zl3b.txt", "sha256": source_sha, "bytes": CORPUS.stat().st_size},
        "legacy": {"lines": old_lines, "pages": len(baseline), "tokens": old_tokens},
        "current_sensitivity_matrix": matrix,
        "historical_reader_snapshots": HISTORICAL_SNAPSHOTS,
        "token_count_rule_deltas": TOKEN_RULE_DELTAS,
        "candidate_only_rule_deltas": CANDIDATE_ONLY_DELTAS,
        "transient_brace_regex_regression": TRANSIENT_BRACE_REGEX,
        "sensitivity": sensitivity,
        "decomposition": {
            "legacy_default_tokens": old_tokens,
            "current_default_tokens": q,
            "default_gap": old_tokens - q,
            "default_gap_unattributed": old_tokens - q + accounted_tokens,
            "default_gap_reconciliation": "131 + 555 + 79 + 44 + 4603 = 5412",
            "legacy_minus_split_ascii_expansion_counterfactual": sensitivity["legacy_minus_comma_split_ascii_expansion_counterfactual"],
            "candidate_gap": 8287,
            "positive_candidate_gap": 1369,
        },
        "corpus_git_blob_sha_constant_across_snapshots": "2a4533ab9bdfa85db9bad602d590978953055df1",
        "physical_row_helper_git_blob_sha_constant_across_snapshots": "eb50eee4b7ca3e44fb2e9f265337e6cbefbe0678",
        "interpretation": "The 5,412-token default difference is fully reconciled by stable reader commits. The separate 538-token figure applies only to the comma-split plus ASCII-ligature-expansion counterfactual; it is not an unattributed gap in the current default.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

